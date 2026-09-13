"""Job-description fetching, parsing and modelling.

Given a URL or a block of text, produce a structured :class:`JobDescription`
with the company, role, contact email and the design/product keywords that
should drive resume + cover-letter tailoring.
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import List, Optional

import requests
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field

from .config import get_settings
from .logger import get_logger
from .utils import retry, unique_terms

log = get_logger("jobs")

USER_AGENT = (
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36"
)

# Vocabulary of skills/keywords we can legitimately claim from the master resume.
# JD text is matched against these to decide what to surface.
SKILL_VOCABULARY: List[str] = [
    "product design", "ui design", "ux design", "ui/ux", "interaction design",
    "visual design", "user research", "usability testing", "a/b testing",
    "wireframing", "wireframes", "prototyping", "prototypes", "user flows",
    "information architecture", "journey mapping", "design system", "design systems",
    "figma", "figjam", "framer", "adobe xd", "sketch", "photoshop", "illustrator",
    "after effects", "rive", "miro", "responsive design", "mobile design",
    "web design", "design thinking", "accessibility", "wcag", "developer handoff",
    "design qa", "component library", "auto layout", "stakeholder management",
    "b2b", "saas", "dashboard", "dashboards", "fintech", "payments", "wallet",
    "kyc", "healthcare", "logistics", "marketplace", "e-commerce", "ecommerce",
    "ai", "automation", "analytics", "google analytics", "hotjar",
    "branding", "brand design", "motion design", "video editing", "wix",
    "landing page", "conversion", "onboarding", "personas", "product discovery",
]

# Common word tokens for role detection.
_ROLE_KEYWORDS = [
    "designer", "developer", "engineer", "manager", "producer", "editor",
    "lead", "director", "analyst", "specialist", "consultant", "architect",
    "strategist", "researcher", "generalist", "creative", "marketer",
]

_EMAIL_RE = re.compile(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}")


class JobDescription(BaseModel):
    """Structured representation of a job posting."""

    company: str = "Unknown Company"
    role: str = "the role"
    url: Optional[str] = None
    text: str = ""
    contact_email: Optional[str] = None
    keywords: List[str] = Field(default_factory=list)

    @property
    def matched_skills(self) -> List[str]:
        """Skills from our vocabulary that appear in the JD (title-cased-ish)."""
        return self.keywords


@retry(attempts=3, backoff_seconds=2.0, exceptions=(requests.RequestException,))
def _http_get(url: str) -> str:
    resp = requests.get(url, headers={"User-Agent": USER_AGENT}, timeout=30)
    resp.raise_for_status()
    return resp.text


def _html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "footer", "nav"]):
        tag.decompose()
    text = soup.get_text(separator="\n")
    lines = [ln.strip() for ln in text.splitlines()]
    return "\n".join(ln for ln in lines if ln)


def fetch_from_url(url: str) -> str:
    """Fetch a job posting URL and return cleaned visible text.

    Uses ``requests`` + BeautifulSoup.  If the page is JS-rendered and returns
    little text, optionally falls back to Playwright (when installed).
    """
    log.info("Fetching job description from %s", url)
    html = _http_get(url)
    text = _html_to_text(html)
    if len(text) < 200:
        rendered = _fetch_with_playwright(url)
        if rendered and len(rendered) > len(text):
            text = rendered
    log.info("Extracted %d characters of job text", len(text))
    return text


def _fetch_with_playwright(url: str) -> str:
    """Best-effort JS rendering; silently degrades if Playwright is unavailable."""
    try:
        from playwright.sync_api import sync_playwright  # noqa: WPS433
    except Exception:  # pragma: no cover - optional dependency
        log.warning("Playwright not available; skipping JS render for %s", url)
        return ""
    try:  # pragma: no cover - requires browser binaries
        with sync_playwright() as pw:
            browser = pw.chromium.launch(headless=True)
            page = browser.new_page(user_agent=USER_AGENT)
            page.goto(url, wait_until="networkidle", timeout=45_000)
            html = page.content()
            browser.close()
        return _html_to_text(html)
    except Exception as exc:  # pragma: no cover
        log.warning("Playwright render failed for %s: %s", url, exc)
        return ""


def load_from_file(path: str | Path) -> str:
    """Read a plain-text job description from *path*."""
    p = Path(path)
    if not p.exists():
        raise FileNotFoundError(f"Job description file not found: {p}")
    log.info("Loading job description from %s", p)
    return p.read_text(encoding="utf-8", errors="ignore")


try:
    import yaml
except ImportError:
    yaml = None

def load_profession_vocabulary(profession: Optional[str] = None) -> tuple[List[str], List[str]]:
    if not profession:
        return SKILL_VOCABULARY, _ROLE_KEYWORDS
        
    from .config import PROJECT_ROOT
    yaml_path = PROJECT_ROOT / "professions" / f"{profession}.yaml"
    if not yaml_path.exists():
        return SKILL_VOCABULARY, _ROLE_KEYWORDS
        
    data = {}
    if yaml is not None:
        try:
            with open(yaml_path, "r", encoding="utf-8") as f:
                data = yaml.safe_load(f) or {}
        except Exception:
            return SKILL_VOCABULARY, _ROLE_KEYWORDS
    else:
        current_list = None
        with open(yaml_path, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if line.startswith("skill_vocabulary:"):
                    current_list = data.setdefault("skill_vocabulary", [])
                elif line.startswith("role_keywords:"):
                    current_list = data.setdefault("role_keywords", [])
                elif line.startswith("- ") and current_list is not None:
                    current_list.append(line[2:].strip(" '\""))
                    
    skills = data.get("skill_vocabulary") or SKILL_VOCABULARY
    roles = data.get("role_keywords") or _ROLE_KEYWORDS
    return skills, roles

def extract_keywords(text: str, profession: Optional[str] = None) -> List[str]:
    """Return vocabulary skills that appear in *text*, in vocabulary order."""
    skills, _ = load_profession_vocabulary(profession)
    low = text.lower()
    found = [skill for skill in skills if skill in low]
    # Prettify a few common ones for display.
    pretty = {
        "ui/ux": "UI/UX", "ux design": "UX design", "ui design": "UI design",
        "figma": "Figma", "framer": "Framer", "wcag": "WCAG", "ai": "AI",
        "b2b": "B2B", "saas": "SaaS", "kyc": "KYC",
    }
    return unique_terms(pretty.get(s, s) for s in found)


def guess_role(text: str, hint: Optional[str] = None, role_keywords: Optional[List[str]] = None) -> str:
    """Guess the job title from *text*, preferring an explicit *hint*."""
    if hint:
        return hint.strip()

    if role_keywords is None:
        role_keywords = _ROLE_KEYWORDS

    # Look for explicit "Role:/Position:/Title:" labels first.
    for label in ("position", "role", "job title", "title"):
        m = re.search(rf"{label}\s*[:\-]\s*(.+)", text, re.IGNORECASE)
        if m:
            return m.group(1).splitlines()[0].strip()[:80]

    # Otherwise scan the first lines for something that looks like a title.
    for line in text.splitlines():
        line = line.strip()
        if 3 <= len(line.split()) <= 8 and any(
            kw in line.lower() for kw in role_keywords
        ):
            return line[:80]
    return "the role"


def guess_company(text: str, url: Optional[str], hint: Optional[str] = None) -> str:
    """Guess the company name from *text*/*url*, preferring an explicit *hint*."""
    if hint:
        return hint.strip()

    for label in ("company", "organisation", "organization", "employer"):
        m = re.search(rf"{label}\s*[:\-]\s*(.+)", text, re.IGNORECASE)
        if m:
            return m.group(1).splitlines()[0].strip()[:80]

    m = re.search(r"\bat\s+([A-Z][A-Za-z0-9&.\- ]{2,40})", text)
    if m:
        return m.group(1).strip().rstrip(".")

    if url:
        host = re.sub(r"^https?://(www\.)?", "", url).split("/")[0]
        base = host.split(".")[0]
        if base and base not in {"linkedin", "indeed", "glassdoor", "wellfound"}:
            return base.replace("-", " ").title()

    return "Unknown Company"


def build_job(
    *,
    text: str,
    url: Optional[str] = None,
    company: Optional[str] = None,
    role: Optional[str] = None,
    profession: Optional[str] = None,
) -> JobDescription:
    """Assemble a :class:`JobDescription` from raw text and optional overrides."""
    skills, roles = load_profession_vocabulary(profession)
    keywords = extract_keywords(text, profession)
    email_match = _EMAIL_RE.search(text)
    contact = email_match.group(0) if email_match else None
    if not contact:
        contact = get_settings().default_recipient or None

    job = JobDescription(
        company=guess_company(text, url, company),
        role=guess_role(text, role, role_keywords=roles),
        url=url,
        text=text,
        contact_email=contact,
        keywords=keywords,
    )
    log.info(
        "Parsed job: company=%r role=%r keywords=%d contact=%s",
        job.company, job.role, len(job.keywords), job.contact_email,
    )
    return job
