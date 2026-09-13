"""
AuraJobs / JobSpy Native Ingestion Service for CareerHero Studio.
Orchestrates multi-source scraping, zero-auth feed aggregation, query expansion,
deduplication, visa analysis, and atomic writes to SQLite jobhunt.db.
"""

from __future__ import annotations

import os
import sys
import time
import asyncio
import logging
from datetime import datetime
from concurrent.futures import ThreadPoolExecutor
from typing import Any, Dict, List, Optional
import pandas as pd

from ..scraper.core.expander import RoleExpander
from ..scraper.core.scheduler import BalancedScheduler
from ..scraper.core.normalizer import normalize_dataframe
from ..scraper.core.classifier import RoleClassifier
from ..scraper.core.visa import detect_visa_sponsorship, detect_relocation
from ..scraper.core.scorer import MatchScorer, calculate_age_hours
from ..scraper.core.deduper import deduplicate_jobs
from ..scraper.sources import (
    MultiBoardAdapter,
    RemoteOKAdapter,
    RemotiveAdapter,
    HimalayasAdapter,
    ATSAdapter,
    FreeHireAdapter,
    ArbeitnowAdapter,
    AIJobsAdapter,
)
from ..web.db import ingest_scraped_batch, get_ingestion_history

logger = logging.getLogger("careerhero.scraper_service")

class JobSpyService:
    """Singleton service managing background job ingestion."""
    
    def __init__(self):
        self.is_running = False
        self.target_role = ""
        self.seniority = "Any"
        self.geography = "All"
        self.freshness_hours = 72
        self.mode = "Express"
        self.progress_percent = 0
        self.current_step = "Idle"
        self.start_time = 0.0
        self.elapsed_seconds = 0.0
        self.total_found = 0
        self.new_added = 0
        self.duplicates_skipped = 0
        self.logs: List[str] = []
        self.last_run_summary: Dict[str, Any] = {}
        self.error_message: Optional[str] = None

    def log(self, message: str) -> None:
        ts = datetime.now().strftime("%H:%M:%S")
        entry = f"[{ts}] {message}"
        self.logs.append(entry)
        if len(self.logs) > 100:
            self.logs.pop(0)
        logger.info(entry)

    def get_status(self) -> Dict[str, Any]:
        elapsed = time.time() - self.start_time if self.is_running else self.elapsed_seconds
        return {
            "is_running": self.is_running,
            "target_role": self.target_role,
            "seniority": self.seniority,
            "geography": self.geography,
            "mode": self.mode,
            "progress_percent": self.progress_percent,
            "progress": self.progress_percent,
            "current_step": self.current_step,
            "elapsed_seconds": round(elapsed, 1),
            "total_found": self.total_found,
            "new_added": self.new_added,
            "duplicates_skipped": self.duplicates_skipped,
            "logs": self.logs[-25:],
            "last_run_summary": self.last_run_summary,
            "error_message": self.error_message
        }

    def _execute_sync(self, role: str, seniority: str, geo: str, freshness: int, mode: str) -> Dict[str, Any]:
        """Synchronous execution runner executed inside a worker thread."""
        self.is_running = True
        self.target_role = role
        self.seniority = seniority
        self.geography = geo
        self.freshness_hours = freshness
        self.mode = mode
        self.start_time = time.time()
        self.logs = []
        self.error_message = None
        self.total_found = 0
        self.new_added = 0
        self.duplicates_skipped = 0
        self.progress_percent = 5
        self.current_step = "Initializing Role Taxonomies"

        self.log(f"Starting {mode.upper()} ingestion for '{role}' ({seniority}) in region: {geo} [<={freshness}h]")

        try:
            # 1. Expand role profile
            expander = RoleExpander()
            profile = expander.build_search_profile(
                target_role=role,
                seniority=seniority
            )

            classifier = RoleClassifier(
                positive_terms=profile.get("positive_title_terms", []),
                negative_terms=profile.get("negative_title_terms", [])
            )
            scorer = MatchScorer(
                target_role=role,
                skills=profile.get("skills", []),
                seniority=seniority
            )
            collected_dfs = []

            # 2. Parallel Fast Path: Direct Zero-Auth & ATS Adapters
            self.current_step = "Querying High-Speed Zero-Auth & ATS Adapters"
            self.progress_percent = 25
            self.log("Fetching live postings from Arbeitnow, Remotive, RemoteOK, FreeHire, and ATS boards...")

            rok = RemoteOKAdapter()
            rem = RemotiveAdapter()
            him = HimalayasAdapter()
            ats = ATSAdapter()
            fh = FreeHireAdapter()
            an = ArbeitnowAdapter()
            ai = AIJobsAdapter()

            with ThreadPoolExecutor(max_workers=7) as executor:
                f_rok = executor.submit(rok.fetch_jobs, role)
                f_rem = executor.submit(rem.fetch_jobs, role)
                f_him = executor.submit(him.fetch_jobs, role)
                f_ats = executor.submit(ats.fetch_all_ats, role, profile.get("positive_title_terms", []))
                f_fh = executor.submit(fh.fetch_jobs, role, geo)
                f_an = executor.submit(an.fetch_jobs, role)
                f_ai = executor.submit(ai.fetch_jobs, role)

                df_rok = f_rok.result()
                df_rem = f_rem.result()
                df_him = f_him.result()
                df_ats = f_ats.result()
                df_fh = f_fh.result()
                df_an = f_an.result()
                df_ai = f_ai.result()

            for name, d in [
                ("RemoteOK", df_rok),
                ("Remotive", df_rem),
                ("Himalayas", df_him),
                ("Direct ATS", df_ats),
                ("FreeHire", df_fh),
                ("Arbeitnow", df_an),
                ("AIJobs", df_ai)
            ]:
                if d is not None and not d.empty:
                    collected_dfs.append(d)
                    self.log(f" -> {name}: Retrieved {len(d)} listings")

            # 3. Targeted Multi-Board Scraper (LinkedIn, Indeed, etc.)
            self.current_step = "Executing Targeted Multi-Board Scrapes"
            self.progress_percent = 55

            scheduler = BalancedScheduler()
            search_terms = profile.get("search_terms", [role])
            queues, counts = scheduler.generate_execution_queues(
                search_terms=search_terms,
                geography_choice=geo,
                mode=mode
            )

            max_queries = 6 if mode.lower() == "express" else 25
            multiboard = MultiBoardAdapter(request_delay=1.0)
            executed_queries = 0

            self.log(f"Running up to {max_queries} targeted regional scraper queries...")

            region_order = ["India", "Middle East", "Global"] if geo == "All" else [geo]
            consecutive_empties = 0

            while executed_queries < max_queries:
                progressed = False
                for r in region_order:
                    if executed_queries >= max_queries:
                        break
                    q = queues.get(r)
                    if not q:
                        continue
                    item = next(q, None)
                    if not item:
                        continue
                    progressed = True
                    executed_queries += 1
                    
                    try:
                        res = multiboard.search_single_site(
                            site=item["site"],
                            term=item["term"],
                            location=item["location"],
                            region=item["region"],
                            country=item["country"],
                            hours_old=freshness,
                            results_wanted=15 if mode.lower() == "express" else 25
                        )
                        if res is not None and not res.empty:
                            collected_dfs.append(res)
                            self.log(f" -> [{item['site'].upper()}] {item['term']} in {item['location']}: +{len(res)} jobs")
                    except Exception as e:
                        logger.debug(f"Query failed: {e}")

                if not progressed:
                    consecutive_empties += 1
                    if consecutive_empties > 2:
                        break

            self.progress_percent = 80
            self.current_step = "Normalizing, Filtering & Classifying Leads"
            self.log("Aggregating, normalizing, and calculating match/visa scores...")

            if not collected_dfs:
                self.log("No postings found for current query parameters.")
                raw_combined = pd.DataFrame()
            else:
                raw_combined = pd.concat(collected_dfs, ignore_index=True)

            if not raw_combined.empty:
                df = normalize_dataframe(raw_combined)

                # Age calculation & filtering
                df["date_posted"] = pd.to_datetime(df["date_posted"], errors="coerce", utc=True)
                df["age_hours"] = df["date_posted"].apply(calculate_age_hours)
                df = df[
                    df["age_hours"].isna() | 
                    ((df["age_hours"] >= 0) & (df["age_hours"] <= freshness))
                ].copy()

                # Classifier filter (strict title matching + negative exclusions)
                filtered_df = classifier.filter_dataframe(df)
                if filtered_df.empty and not df.empty:
                    # Fallback to broad match without negative terms
                    fallback_mask = df["title"].apply(lambda t: not any(neg in str(t).lower() for neg in classifier.negative_terms))
                    filtered_df = df[fallback_mask].copy()

                if not filtered_df.empty:
                    # Visa & Relocation detection
                    filtered_df["visa_status"] = filtered_df.apply(
                        lambda r: detect_visa_sponsorship(r.get("title", ""), r.get("description", ""))[0], axis=1
                    )
                    filtered_df["relocation_status"] = filtered_df.apply(
                        lambda r: detect_relocation(r.get("title", ""), r.get("description", ""))[0], axis=1
                    )

                    # Fit Scorer
                    filtered_df["match_score"] = filtered_df.apply(
                        lambda r: scorer.calculate_score(
                            r.get("title", ""),
                            r.get("description", ""),
                            r.get("age_hours"),
                            r.get("visa_status", "UNKNOWN"),
                            r.get("relocation_status", "UNKNOWN")
                        ),
                        axis=1
                    )
                    filtered_df["priority"] = filtered_df.apply(
                        lambda r: scorer.assign_priority(
                            r.get("age_hours"),
                            r.get("visa_status", "UNKNOWN")
                        ),
                        axis=1
                    )

                    deduped_df = deduplicate_jobs(filtered_df)
                else:
                    deduped_df = pd.DataFrame()

                self.total_found = len(deduped_df)
                self.log(f"Total qualified unique jobs ready for ingestion: {self.total_found}")

                # 4. Atomic Database Insert
                self.current_step = "Writing to SQLite Leads Queue"
                self.progress_percent = 92

                records = deduped_df.to_dict(orient="records") if not deduped_df.empty else []
                runtime = time.time() - self.start_time
                meta = {
                    "target_role": role,
                    "geography": geo,
                    "runtime_seconds": runtime,
                    "status": "SUCCESS"
                }

                ingest_res = ingest_scraped_batch(records, run_metadata=meta)
                self.new_added = ingest_res["new_leads_added"]
                self.duplicates_skipped = ingest_res["duplicates_skipped"]
                self.log(f"Ingestion complete: +{self.new_added} new leads inserted, {self.duplicates_skipped} duplicates suppressed.")

            else:
                self.total_found = 0
                self.new_added = 0
                self.duplicates_skipped = 0

            self.progress_percent = 100
            self.current_step = "Completed Successfully"
            self.elapsed_seconds = time.time() - self.start_time

            summary = {
                "role": role,
                "geo": geo,
                "mode": mode,
                "total_found": self.total_found,
                "new_added": self.new_added,
                "duplicates_skipped": self.duplicates_skipped,
                "runtime_seconds": round(self.elapsed_seconds, 1),
                "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            }
            self.last_run_summary = summary
            self.log(f"All operations finished in {self.elapsed_seconds:.1f}s.")
            return summary

        except Exception as e:
            self.error_message = str(e)
            self.current_step = "Failed with Error"
            self.log(f"ERROR: {e}")
            import traceback
            traceback.print_exc()
            return {"status": "ERROR", "message": str(e)}

        finally:
            self.is_running = False

    async def trigger_scrape(self, role: str = "Product Designer", seniority: str = "Any", geo: str = "All", freshness: int = 72, mode: str = "Express") -> Dict[str, Any]:
        """Trigger scrape asynchronously in a threadpool without blocking FastAPI loop."""
        if self.is_running:
            return {"status": "BUSY", "message": "Scraper is already running."}
        
        loop = asyncio.get_event_loop()
        loop.run_in_executor(None, self._execute_sync, role, seniority, geo, freshness, mode)
        return {"status": "TRIGGERED", "message": f"Scrape started for '{role}' in '{geo}' ({mode} mode)."}

# Global singleton instance
scraper_service = JobSpyService()
