"""
Zero-Authentication Public API Client for AOE.
All endpoints implemented here are 100% free, requiring zero auth tokens, zero API keys, and zero registration.
"""

from __future__ import annotations

import re
import logging
from typing import Any, Dict, List, Optional
import requests

logger = logging.getLogger("aoe.public_apis")

EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")
USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36"

# =============================================================================
# 1. EMAIL VERIFICATION & DELIVERABILITY (Kickbox Open API + Disify)
# =============================================================================

def verify_email_deliverability(email: str, timeout: int = 6) -> Dict[str, Any]:
    """
    Verifies deliverability, MX records, and disposable inbox status using
    zero-auth public verification endpoints (Kickbox Open API + Disify fallback).
    """
    if not email or not isinstance(email, str):
        return {
            "email": email,
            "status": "invalid_syntax",
            "is_deliverable": False,
            "is_disposable": False,
            "score": 0.0,
            "provider": "local_regex"
        }

    clean_email = email.strip().lower()
    if not EMAIL_REGEX.match(clean_email):
        return {
            "email": clean_email,
            "status": "invalid_syntax",
            "is_deliverable": False,
            "is_disposable": False,
            "score": 0.0,
            "provider": "local_regex"
        }

    # 1. Try Kickbox Open API
    try:
        url = f"https://open.kickbox.com/v1/verify?email={clean_email}&timeout={timeout * 1000}"
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            result = data.get("result", "unknown")
            is_disposable = bool(data.get("disposable", False))
            is_deliverable = result in ["deliverable", "risky"] and not is_disposable
            
            return {
                "email": clean_email,
                "status": result,  # "deliverable", "undeliverable", "risky", "unknown"
                "is_deliverable": is_deliverable,
                "is_disposable": is_disposable,
                "score": float(data.get("sendex", 0.5)),
                "reason": data.get("reason", "accepted"),
                "provider": "kickbox_open"
            }
    except Exception as e:
        logger.debug(f"Kickbox open verification timed out or failed: {e}")

    # 2. Fallback to Disify API
    try:
        url = f"https://www.disify.com/api/email/{clean_email}"
        headers = {"User-Agent": USER_AGENT}
        resp = requests.get(url, headers=headers, timeout=timeout)
        if resp.status_code == 200:
            data = resp.json()
            is_disposable = bool(data.get("disposable", False))
            has_dns = bool(data.get("dns", True))
            is_valid = bool(data.get("format", True)) and has_dns and not is_disposable
            
            return {
                "email": clean_email,
                "status": "deliverable" if is_valid else ("disposable" if is_disposable else "undeliverable"),
                "is_deliverable": is_valid,
                "is_disposable": is_disposable,
                "score": 0.8 if is_valid else 0.1,
                "reason": "dns_valid" if has_dns else "dns_invalid",
                "provider": "disify"
            }
    except Exception as e:
        logger.debug(f"Disify verification failed: {e}")

    # 3. Graceful heuristic fallback if network calls fail
    domain = clean_email.split("@")[-1]
    common_burners = {"mailinator.com", "tempmail.com", "10minutemail.com", "guerrillamail.com", "throwawaymail.com"}
    is_disposable = domain in common_burners
    
    return {
        "email": clean_email,
        "status": "unverified",
        "is_deliverable": not is_disposable,
        "is_disposable": is_disposable,
        "score": 0.5,
        "reason": "heuristics_only",
        "provider": "local_fallback"
    }


# =============================================================================
# 2. ZERO-AUTH JOB FEEDS (Arbeitnow, Remotive, RemoteOK)
# =============================================================================

def fetch_arbeitnow_jobs(query: str = "", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch verified remote & European tech/design postings via Arbeitnow public REST API.
    Zero auth, zero registration.
    """
    url = "https://www.arbeitnow.com/api/job-board-api"
    headers = {"User-Agent": USER_AGENT}
    jobs = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("data", [])[:limit]:
                title = item.get("title", "")
                if query and query.lower() not in title.lower():
                    continue
                jobs.append({
                    "title": title,
                    "company": item.get("company_name", "Unknown"),
                    "location": item.get("location", "Remote"),
                    "job_url": item.get("url", ""),
                    "source": "arbeitnow_api",
                    "category": "Direct",
                    "remote_status": "Remote" if item.get("remote") else "Hybrid/On-site",
                    "date_posted": item.get("created_at", ""),
                    "description": item.get("description", ""),
                    "tags": item.get("tags", [])
                })
    except Exception as e:
        logger.warning(f"Error fetching Arbeitnow jobs: {e}")
    return jobs


def fetch_remotive_jobs(category: str = "design", limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch categorized remote jobs from Remotive public API. Zero auth.
    Categories: 'design', 'software-dev', 'product', 'qa', etc.
    """
    url = f"https://remotive.com/api/remote-jobs?category={category}&limit={limit}"
    headers = {"User-Agent": USER_AGENT}
    jobs = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            for item in data.get("jobs", [])[:limit]:
                jobs.append({
                    "title": item.get("title", ""),
                    "company": item.get("company_name", "Unknown"),
                    "location": item.get("candidate_required_location", "Worldwide"),
                    "job_url": item.get("url", ""),
                    "source": "remotive_api",
                    "category": "Direct",
                    "remote_status": "Remote",
                    "salary_min": item.get("salary", ""),
                    "date_posted": item.get("publication_date", ""),
                    "description": item.get("description", ""),
                    "tags": item.get("tags", [])
                })
    except Exception as e:
        logger.warning(f"Error fetching Remotive jobs: {e}")
    return jobs


def fetch_remoteok_jobs(limit: int = 50) -> List[Dict[str, Any]]:
    """
    Fetch public remote postings from RemoteOK JSON feed. Zero auth.
    """
    url = "https://remoteok.com/api"
    headers = {"User-Agent": USER_AGENT}
    jobs = []
    try:
        resp = requests.get(url, headers=headers, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            raw_items = [x for x in data if isinstance(x, dict) and "position" in x]
            for item in raw_items[:limit]:
                jobs.append({
                    "title": item.get("position", ""),
                    "company": item.get("company", "Unknown"),
                    "location": item.get("location", "Worldwide Remote"),
                    "job_url": item.get("url", ""),
                    "source": "remoteok_api",
                    "category": "Direct",
                    "remote_status": "Remote",
                    "salary_min": item.get("salary_min", ""),
                    "salary_max": item.get("salary_max", ""),
                    "date_posted": item.get("date", ""),
                    "description": item.get("description", ""),
                    "tags": item.get("tags", [])
                })
    except Exception as e:
        logger.warning(f"Error fetching RemoteOK jobs: {e}")
    return jobs


# =============================================================================
# 3. CURRENCY & GEOGRAPHIC UTILITIES (Frankfurter & REST Countries)
# =============================================================================

def convert_currency(amount: float, from_curr: str = "USD", to_curr: str = "GBP") -> Optional[float]:
    """
    Converts currency using the European Central Bank feed via Frankfurter.
    Zero auth. Supports USD, EUR, GBP, INR, etc.
    """
    if from_curr.upper() == to_curr.upper():
        return amount
    try:
        url = f"https://api.frankfurter.app/latest?amount={amount}&from={from_curr.upper()}&to={to_curr.upper()}"
        resp = requests.get(url, timeout=5)
        if resp.status_code == 200:
            rates = resp.json().get("rates", {})
            return rates.get(to_curr.upper())
    except Exception as e:
        logger.debug(f"Frankfurter conversion failed: {e}")
    return None


def get_regional_cv_requirements(country_code_or_name: str) -> Dict[str, Any]:
    """
    Evaluates country-specific CV standards (Photo vs No Photo, Phone format, etc.)
    using local conventions mapped to international ISO standards.
    """
    term = str(country_code_or_name).strip().lower()
    
    # North America: Strictly no photo
    if any(c in term for c in ["us", "united states", "usa", "ca", "canada"]):
        return {
            "region": "North America",
            "photo_required": False,
            "photo_forbidden": True,
            "convention_notes": "Strictly no headshot or personal demographic info (age, marital status)."
        }
    
    # UK / Northern Europe: Strictly no photo
    if any(c in term for c in ["uk", "united kingdom", "great britain", "england", "scotland", "wales", "ireland"]):
        return {
            "region": "UK & Ireland",
            "photo_required": False,
            "photo_forbidden": True,
            "convention_notes": "No photo. Highlight right-to-work status or UK visa availability."
        }
    
    # Middle East / GCC: Professional headshot expected
    if any(c in term for c in ["uae", "dubai", "abu dhabi", "saudi", "riyadh", "qatar", "doha", "kuwait", "bahrain", "oman"]):
        return {
            "region": "Middle East / GCC",
            "photo_required": True,
            "photo_forbidden": False,
            "convention_notes": "Professional corporate headshot standard. Note current visa and availability."
        }
    
    # Default Continental Europe / India / Global
    return {
        "region": "Global / Continental",
        "photo_required": False,
        "photo_forbidden": False,
        "convention_notes": "Standard 1-page modern tech CV. Photo optional."
    }
