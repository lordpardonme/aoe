"""
Application Autopsy Engine for AOE.
Inspired by Project Graveyard: detects stalled applications, analyzes cause of death,
and ranks resurrection potential with actionable follow-up advice.
"""

from __future__ import annotations

import sqlite3
from datetime import datetime
from typing import Any, Dict, List
from ..web.db import DB_PATH, init_db

def run_applications_autopsy(days_silent_threshold: int = 7) -> Dict[str, Any]:
    """
    Scans applied leads in SQLite, identifies stalled applications,
    diagnoses causes of death, and calculates resurrection pulses.
    """
    init_db()
    stalled_corpses = []
    
    with sqlite3.connect(DB_PATH) as conn:
        conn.row_factory = sqlite3.Row
        cur = conn.execute("""
            SELECT id, company, role, country, category, contact_email, status,
                   applied_date, follow_up_date, notes, match_score
            FROM leads
            WHERE status IN ('Applied', 'Sent', 'To Contact')
            ORDER BY id DESC
        """)
        rows = [dict(r) for r in cur.fetchall()]

    now = datetime.now()

    for r in rows:
        app_date_str = r.get("applied_date")
        if not app_date_str:
            continue
        try:
            # Parse YYYY-MM-DD or full timestamp
            app_dt = datetime.strptime(app_date_str[:10], "%Y-%m-%d")
            days_silent = (now - app_dt).days
        except Exception:
            days_silent = 0

        if days_silent >= days_silent_threshold:
            # Determine cause of death
            if days_silent >= 21:
                cause = "Ghosted by Recruiter"
                pulse = 35
                recommendation = "Low pulse. Consider reaching out to an alternate contact or moving on."
            elif days_silent >= 14:
                cause = "Stalled in Pipeline"
                pulse = 60
                recommendation = "Prime for a 2-sentence value-add follow-up pitch with recent portfolio work."
            elif days_silent >= 7:
                cause = "Awaiting First Follow-up"
                pulse = 85
                recommendation = "High pulse! Send gentle 7-day conversion nudge referencing previous email."
            else:
                cause = "Warm Pipeline"
                pulse = 95
                recommendation = "Recent dispatch. Await recruiter response."

            stalled_corpses.append({
                "lead_id": r["id"],
                "company": r["company"],
                "role": r["role"],
                "applied_date": app_date_str,
                "days_silent": days_silent,
                "cause_of_death": cause,
                "resurrection_pulse": pulse,
                "pulse_score": pulse,
                "contact_email": r["contact_email"],
                "recommendation": recommendation,
                "recommended_action": recommendation
            })

    # Sort by strongest pulse
    stalled_corpses.sort(key=lambda x: x["resurrection_pulse"], reverse=True)

    high_pulse = [c for c in stalled_corpses if c["resurrection_pulse"] >= 70]
    
    # Calculate dominant cause
    from collections import Counter
    causes = [c["cause_of_death"] for c in stalled_corpses]
    dominant = Counter(causes).most_common(1)[0][0] if causes else "None"

    return {
        "total_scanned": len(rows),
        "total_stalled": len(stalled_corpses),
        "high_pulse_candidates": len(high_pulse),
        "dominant_cause": dominant,
        "high_pulse_corpses": high_pulse,
        "all_stalled": stalled_corpses,
        "autopsies": stalled_corpses
    }
