"""
Secure, multi-channel RSS & Atom feed adapter for AOE Staging.
Supports WeWorkRemotely, RemoteOK, and Jobicy public feeds.
Features built-in XXE mitigation, SSRF domain whitelisting,
RFC 822 / ISO 8601 date normalization, and HTML sanitization.
"""

from __future__ import annotations

import re
import html
import hashlib
import logging
import urllib.request
import urllib.parse
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime
from typing import Any, Dict, List, Optional, Set
import xml.etree.ElementTree as ET

logger = logging.getLogger("aoe.rss_adapter")

# Gate 4 Security Guardrail: SSRF Domain Whitelist
ALLOWED_RSS_DOMAINS: Set[str] = {
    "weworkremotely.com",
    "www.weworkremotely.com",
    "remoteok.com",
    "www.remoteok.com",
    "jobicy.com",
    "www.jobicy.com",
    "remotive.com",
    "www.remotive.com",
}

# Pre-configured public RSS feed channels
DEFAULT_RSS_FEEDS: Dict[str, Dict[str, str]] = {
    "wwr_design": {
        "name": "WeWorkRemotely • Design & Creative",
        "url": "https://weworkremotely.com/categories/remote-design-jobs.rss",
        "category": "Direct Employers",
        "default_role": "Product Designer"
    },
    "wwr_dev": {
        "name": "WeWorkRemotely • Full-Stack & Dev",
        "url": "https://weworkremotely.com/categories/remote-full-stack-programming-jobs.rss",
        "category": "Direct Employers",
        "default_role": "Full Stack Engineer"
    },
    "wwr_pm": {
        "name": "WeWorkRemotely • Product Management",
        "url": "https://weworkremotely.com/categories/remote-product-management-jobs.rss",
        "category": "Direct Employers",
        "default_role": "Product Manager"
    },
    "remoteok_all": {
        "name": "RemoteOK • Global Remote Feed",
        "url": "https://remoteok.com/remote-jobs.rss",
        "category": "Direct Employers",
        "default_role": "Remote Specialist"
    },
    "jobicy_design": {
        "name": "Jobicy • Remote Design & UX",
        "url": "https://jobicy.com/feed/design-jobs",
        "category": "Direct Employers",
        "default_role": "UI/UX Designer"
    }
}


def sanitize_html(raw_html: Optional[str]) -> str:
    """Strip HTML markup, script/style blocks, and entities to avoid XSS."""
    if not raw_html:
        return ""
    # Strip script and style blocks including interior script text
    clean = re.sub(r"<(script|style)[^>]*>.*?</\1>", " ", raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Strip remaining HTML tags
    clean = re.sub(r"<[^>]+>", " ", clean)
    # Unescape HTML entities
    clean = html.unescape(clean)
    # Collapse multiple whitespaces
    clean = re.sub(r"\s+", " ", clean).strip()
    return clean


def parse_rfc822_date(date_str: Optional[str]) -> str:
    """Parse RFC 822 or ISO 8601 date string into ISO YYYY-MM-DD."""
    if not date_str:
        return datetime.now(timezone.utc).strftime("%Y-%m-%d")
    date_str = date_str.strip()
    try:
        dt = parsedate_to_datetime(date_str)
        return dt.strftime("%Y-%m-%d")
    except Exception:
        pass

    # Fallback to ISO format regex
    iso_match = re.search(r"(\d{4}-\d{2}-\d{2})", date_str)
    if iso_match:
        return iso_match.group(1)

    return datetime.now(timezone.utc).strftime("%Y-%m-%d")


def compute_lead_fingerprint(company: str, role: str, url: str) -> str:
    """Deterministic SHA-256 fingerprint for deduplication."""
    norm = f"{company.strip().lower()}|{role.strip().lower()}|{url.strip().lower()}"
    return hashlib.sha256(norm.encode("utf-8")).hexdigest()


class SecureXMLParser:
    """
    XML parser hardened against XXE (XML External Entity) attacks.
    Disallows external DTD resolution and parameter entity expansions.
    """

    @staticmethod
    def parse_string(xml_text: str) -> ET.Element:
        # Gate 4: Reject entity declarations outright to block XXE / Billion Laughs (CWE-611 / CWE-776)
        if "<!ENTITY" in xml_text.upper():
            raise ValueError("Security violation: Custom DOCTYPE and ENTITY definitions are prohibited in RSS feeds.")
        if "<!DOCTYPE" in xml_text.upper():
            # Strip harmless DOCTYPE declarations without entities
            xml_text = re.sub(r"<!DOCTYPE[^>]*>", "", xml_text, flags=re.IGNORECASE)

        return ET.fromstring(xml_text)


class RSSFeedAdapter:
    """Autonomous RSS Feed Aggregator & Normalizer for AOE."""

    def __init__(self, allowed_domains: Optional[Set[str]] = None) -> None:
        self.allowed_domains = allowed_domains or ALLOWED_RSS_DOMAINS

    def validate_url(self, url: str) -> None:
        """Enforce strict SSRF protection by domain whitelisting and protocol check."""
        parsed = urllib.parse.urlparse(url)
        if parsed.scheme not in ("http", "https"):
            raise ValueError(f"Invalid URL scheme '{parsed.scheme}'. Only http/https are allowed.")

        hostname = (parsed.hostname or "").lower()
        if not hostname:
            raise ValueError("Invalid URL: missing hostname.")

        # Block localhost, loopbacks, and private IP ranges
        if hostname in ("localhost", "127.0.0.1", "0.0.0.0", "::1"):
            raise ValueError(f"SSRF violation: Localhost access prohibited ({hostname}).")
        if hostname.startswith("10.") or hostname.startswith("192.168.") or hostname.startswith("169.254."):
            raise ValueError(f"SSRF violation: Private network address prohibited ({hostname}).")

        # Whitelist domain verification
        if hostname not in self.allowed_domains:
            domain_matched = any(hostname.endswith("." + dom) for dom in self.allowed_domains)
            if not domain_matched:
                raise ValueError(f"SSRF violation: Domain '{hostname}' is not in the allowed RSS feed whitelist.")

    def fetch_feed_xml(self, url: str, timeout: int = 12) -> str:
        """Fetch raw XML payload from remote RSS feed with browser User-Agent."""
        self.validate_url(url)
        req = urllib.request.Request(
            url,
            headers={
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AOE-JobHunt/2.0 (+https://github.com/job-hunt-app)",
                "Accept": "application/rss+xml, application/xml, text/xml;q=0.9, */*;q=0.8",
            }
        )
        with urllib.request.urlopen(req, timeout=timeout) as resp:
            return resp.read().decode("utf-8", errors="replace")

    def parse_feed(self, xml_content: str, default_category: str = "Direct Employers", channel_key: str = "") -> List[Dict[str, Any]]:
        """Parse RSS/Atom XML into standardized AOE lead dictionaries."""
        root = SecureXMLParser.parse_string(xml_content)
        items: List[Dict[str, Any]] = []

        # Strip namespace prefixes from all tags to make parsing universal across RSS & Atom
        for el in root.iter():
            if isinstance(el.tag, str) and "}" in el.tag:
                el.tag = el.tag.split("}", 1)[1]

        raw_elements = root.findall(".//entry") or root.findall(".//item")

        for elem in raw_elements:
            try:
                # 1. Title & Role extraction
                title_elem = elem.find("title")
                raw_title = sanitize_html(title_elem.text if title_elem is not None and title_elem.text else "")
                if not raw_title:
                    continue

                # 2. Company extraction
                # WeWorkRemotely format: "CompanyName: Role Title" or "Role Title at CompanyName"
                company = ""
                role = raw_title

                # Check creator or author first
                creator_elem = elem.find("creator")
                if creator_elem is None:
                    creator_elem = elem.find("author")
                if creator_elem is not None and creator_elem.text:
                    company = sanitize_html(creator_elem.text)

                if not company:
                    if ":" in raw_title:
                        parts = raw_title.split(":", 1)
                        company = parts[0].strip()
                        role = parts[1].strip()
                    elif " at " in raw_title:
                        parts = raw_title.split(" at ", 1)
                        role = parts[0].strip()
                        company = parts[1].strip()
                    elif " - " in raw_title:
                        parts = raw_title.split(" - ", 1)
                        company = parts[0].strip()
                        role = parts[1].strip()
                    else:
                        company = "Remote Tech Co"
                else:
                    # Strip company prefix from role if present (e.g. "Stripe: Senior Product Designer")
                    if role.lower().startswith(company.lower() + ":"):
                        role = role[len(company) + 1:].strip()
                    elif role.lower().startswith(company.lower() + " -"):
                        role = role[len(company) + 2:].strip()
                    elif role.lower().startswith(company.lower() + " –"):
                        role = role[len(company) + 2:].strip()

                # 3. URL / Link extraction
                link = ""
                link_elem = elem.find("link")
                if link_elem is not None:
                    # Could be <link>http...</link> or Atom <link href="..."/>
                    link = link_elem.text or link_elem.attrib.get("href", "")
                if not link:
                    guid_elem = elem.find("guid")
                    if guid_elem is not None and guid_elem.text and guid_elem.text.startswith("http"):
                        link = guid_elem.text

                # 4. Description / Notes extraction
                desc_elem = elem.find("description")
                if desc_elem is None:
                    desc_elem = elem.find("encoded")
                if desc_elem is None:
                    desc_elem = elem.find("summary")
                raw_desc = desc_elem.text if desc_elem is not None and desc_elem.text else ""
                clean_notes = sanitize_html(raw_desc)[:400]  # First 400 chars preview

                # 5. Date parsing
                pub_elem = elem.find("pubDate")
                if pub_elem is None:
                    pub_elem = elem.find("published")
                if pub_elem is None:
                    pub_elem = elem.find("updated")
                raw_date = pub_elem.text if pub_elem is not None and pub_elem.text else None
                formatted_date = parse_rfc822_date(raw_date)

                # 6. Region / Country
                country = "Remote (Worldwide)"
                region_elem = elem.find("region")
                if region_elem is not None and region_elem.text:
                    country = sanitize_html(region_elem.text)
                elif "usa" in raw_title.lower() or "us only" in raw_title.lower():
                    country = "United States"
                elif "uk" in raw_title.lower() or "europe" in raw_title.lower():
                    country = "UK & Europe"

                fp = compute_lead_fingerprint(company, role, link)

                items.append({
                    "company": company,
                    "role": role,
                    "country": country,
                    "category": default_category,
                    "job_url": link.strip(),
                    "website": urllib.parse.urlparse(link).netloc if link else "",
                    "contact_email": "",  # To be discovered via Email Finder
                    "status": "To Contact",
                    "notes": clean_notes,
                    "source_sheet": f"RSS Feed ({channel_key or 'Remote'})",
                    "applied_date": "",
                    "follow_up_date": "",
                    "created_at": formatted_date,
                    "fingerprint": fp
                })
            except Exception as item_err:
                logger.warning("Error parsing RSS item: %s", item_err)
                continue

        return items

    def sync_channel(self, channel_key: str, max_items: int = 25) -> List[Dict[str, Any]]:
        """Fetch and parse an individual pre-configured RSS channel."""
        if channel_key not in DEFAULT_RSS_FEEDS:
            raise ValueError(f"Unknown RSS channel '{channel_key}'. Available: {list(DEFAULT_RSS_FEEDS.keys())}")

        cfg = DEFAULT_RSS_FEEDS[channel_key]
        xml_text = self.fetch_feed_xml(cfg["url"])
        leads = self.parse_feed(
            xml_content=xml_text,
            default_category=cfg.get("category", "Direct Employers"),
            channel_key=cfg.get("name", channel_key)
        )
        return leads[:max_items]
