"""
email_finder.py — Corporate email permutation generator and recruiter email discovery.
Generates corporate email patterns and validates deliverability via zero-auth public checks.
"""

from __future__ import annotations

import re
import socket
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse

from .services.public_apis import verify_email_deliverability

COMMON_FORMATS = [
    "{first}.{last}@{domain}",
    "{first}@{domain}",
    "{first}{last}@{domain}",
    "{first_initial}{last}@{domain}",
    "{first}.{last_initial}@{domain}",
    "{first_initial}.{last}@{domain}",
    "{last}.{first}@{domain}",
    "{first}_{last}@{domain}",
]


def clean_domain(raw_domain_or_url: str) -> str:
    """Extract clean domain name from URL or raw string."""
    if not raw_domain_or_url:
        return ""
    text = str(raw_domain_or_url).strip().lower()
    if not text.startswith("http://") and not text.startswith("https://"):
        text = "https://" + text
    try:
        parsed = urlparse(text)
        host = parsed.netloc or parsed.path
        host = host.split(":")[0]  # remove port
        if host.startswith("www."):
            host = host[4:]
        return host
    except Exception:
        # Fallback simple regex
        clean = re.sub(r"^https?://", "", raw_domain_or_url.strip().lower())
        return clean.split("/")[0].split(":")[0].replace("www.", "")


def parse_contact_name(full_name: str) -> tuple[str, str]:
    """Parse contact name into cleaned first and last names."""
    if not full_name:
        return "", ""
    # Remove common corporate suffixes, prefixes, or bracketed titles
    cleaned = re.sub(r"\(.*?\)|\[.*?\]", "", full_name)
    cleaned = re.sub(r"\b(mr|mrs|ms|dr|phd|mba|talent|recruiter|hr|head of|director)\b", "", cleaned, flags=re.IGNORECASE)
    cleaned = re.sub(r"[^a-zA-Z\s]", "", cleaned).strip().lower()
    parts = cleaned.split()
    if not parts:
        return "", ""
    first = parts[0]
    last = parts[-1] if len(parts) > 1 else ""
    return first, last


def generate_email_permutations(contact_name: str, domain: str) -> List[str]:
    """Generate prioritized candidate corporate email addresses."""
    dom = clean_domain(domain)
    first, last = parse_contact_name(contact_name)
    if not dom:
        return []

    # If no contact person specified, fallback to standard corporate talent inboxes
    if not first:
        return [
            f"careers@{dom}",
            f"talent@{dom}",
            f"jobs@{dom}",
            f"hiring@{dom}",
            f"recruiting@{dom}",
            f"contact@{dom}",
            f"team@{dom}",
        ]

    first_init = first[0] if first else ""
    last_init = last[0] if last else ""

    candidates = []
    for fmt in COMMON_FORMATS:
        if "{last}" in fmt and not last:
            continue
        if "{last_initial}" in fmt and not last:
            continue
        addr = fmt.format(
            first=first,
            last=last,
            first_initial=first_init,
            last_initial=last_init,
            domain=dom,
        )
        if addr not in candidates:
            candidates.append(addr)

    # Also append team talent inbox as fallback
    candidates.append(f"talent@{dom}")
    candidates.append(f"careers@{dom}")
    return candidates


def check_domain_has_mx(domain: str) -> bool:
    """Quick socket MX or host resolution check without heavy external dependencies."""
    dom = clean_domain(domain)
    if not dom:
        return False
    try:
        # Check standard DNS resolution
        socket.getaddrinfo(dom, 80)
        return True
    except Exception:
        return False


def discover_and_score_emails(
    contact_name: str,
    company: str,
    domain: Optional[str] = None,
    verify_top: int = 3,
) -> Dict[str, Any]:
    """
    Generate corporate email permutations, verify domain health,
    and run deliverability checks on top candidate emails.
    """
    dom = clean_domain(domain)
    if not dom and company:
        # Heuristic domain from company name: remove inc, llc, ltd
        slug = re.sub(r"\b(inc|llc|ltd|corp|corporation|technologies|solutions|group)\b", "", company, flags=re.IGNORECASE)
        slug = re.sub(r"[^a-zA-Z0-9]", "", slug).strip().lower()
        if slug:
            dom = f"{slug}.com"

    candidates = generate_email_permutations(contact_name, dom)
    has_dns = check_domain_has_mx(dom)

    results = []
    # Check top candidate deliverability
    for i, email in enumerate(candidates[:verify_top]):
        verif = verify_email_deliverability(email, timeout=4)
        status = verif.get("status", "unverified")
        deliverable = verif.get("is_deliverable", False)
        score = verif.get("score", 0.5)

        # Confidence heuristic
        confidence = "Medium"
        if deliverable and score >= 0.7:
            confidence = "High (Deliverable)"
        elif verif.get("is_disposable"):
            confidence = "Low (Burner Domain)"
        elif i == 0 and has_dns:
            confidence = "High (Common Pattern)"

        results.append({
            "email": email,
            "status": status,
            "is_deliverable": deliverable,
            "confidence": confidence,
            "score": score,
            "format": "Pattern Match",
        })

    # Add remaining without network check for instant responsiveness
    for email in candidates[verify_top:]:
        results.append({
            "email": email,
            "status": "unverified",
            "is_deliverable": False,
            "confidence": "Alternative Pattern",
            "score": 0.4,
            "format": "Permutation",
        })

    return {
        "company": company,
        "contact_name": contact_name,
        "domain": dom,
        "domain_active": has_dns,
        "primary_email": results[0]["email"] if results else f"careers@{dom}",
        "candidates": results,
    }
