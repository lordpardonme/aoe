import csv
import json
import math
import re
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd


ROOT = Path(__file__).resolve().parents[1]
BUILD = ROOT / "reconciled-tracker-build"
EXTRACTION = ROOT / "drive-extraction"

MASTER_COLUMNS = [
    "Country / Region",
    "Type",
    "Company / Agency",
    "Company Description",
    "Contact Person",
    "Email Sent To",
    "Email / Contact",
    "Phone / WhatsApp",
    "Role Applied For",
    "Status",
    "Date Email Sent",
    "Date Applied",
    "Follow-up Date",
    "Reply Status",
    "Confidence",
    "Needs Manual Review",
    "Recommended Action",
    "Source",
    "Notes",
    "URLs",
    "Last Gmail Thread ID",
    "Last Gmail Message ID",
]

TAB_COLUMNS = MASTER_COLUMNS

EMAIL_RE = re.compile(r"(?i)\b[A-Z0-9._%+\-]+@[A-Z0-9.\-]+\.[A-Z]{2,}\b")
URL_RE = re.compile(r"(?i)\bhttps?://[^\s,;)\]]+")
PHONE_RE = re.compile(r"(?i)(?:WhatsApp:\s*)?(?:\+\d{1,3}[\s\-]?)?(?:\d[\s\-]?){8,14}\d")

STATUS_RANK = {
    "": 0,
    "To Contact": 1,
    "Networking": 2,
    "Contacted": 3,
    "Applied": 4,
    "Followed Up": 5,
    "Needs Review": 6,
    "Delivery Failed": 7,
    "Rejected / Appeal Sent": 8,
    "Rejected": 9,
    "Interview": 10,
}

REPLY_RANK = {
    "": 0,
    "No Reply": 1,
    "Replied": 2,
    "Replied / Active Process": 3,
    "Bounced": 4,
    "Rejected": 5,
    "Interview": 6,
}

CONF_RANK = {"": 0, "Unknown": 1, "Low": 2, "Medium": 3, "High": 4}


def clean(value):
    if value is None:
        return ""
    if isinstance(value, float) and math.isnan(value):
        return ""
    text = str(value).replace("\r", " ").replace("\n", " ").strip()
    return re.sub(r"\s+", " ", text)


def norm_text(value):
    text = clean(value).lower()
    text = re.sub(r"[^a-z0-9]+", " ", text)
    words = [w for w in text.split() if w not in {"the", "llc", "ltd", "limited", "group", "company", "co"}]
    return " ".join(words)


def split_multi(value):
    text = clean(value)
    if not text:
        return []
    parts = re.split(r"\s*(?:;|\||,)\s*", text)
    return [p.strip() for p in parts if p and p.strip()]


def extract_emails(*values):
    emails = []
    for value in values:
        for email in EMAIL_RE.findall(clean(value)):
            emails.append(email.strip().lower())
    return sorted(set(emails))


def extract_urls(*values):
    urls = []
    for value in values:
        for url in URL_RE.findall(clean(value)):
            urls.append(url.rstrip(".,)"))
    return sorted(set(urls))


def extract_phones(*values):
    phones = []
    for value in values:
        for phone in PHONE_RE.findall(clean(value)):
            p = clean(phone)
            digits = re.sub(r"\D", "", p)
            if len(digits) >= 9 and "202606" not in digits:
                phones.append(p)
    return sorted(set(phones))


def join_unique(*values, sep="; "):
    items = []
    for value in values:
        if isinstance(value, list):
            source = value
        else:
            source = split_multi(value)
        for item in source:
            item = clean(item)
            if item and item not in items:
                items.append(item)
    return sep.join(items)


def infer_company_from_email(email):
    email = clean(email).lower()
    if "@" not in email:
        return ""
    domain = email.split("@", 1)[1]
    stem = domain.split(".")[0]
    special = {
        "twsol": "Teamware Solutions",
        "bypt": "byPeople Technologies",
        "zohomail": "Remote recruiter lead",
        "gmail": "Gmail contact lead",
    }
    if stem in special:
        return special[stem]
    words = re.split(r"[\-_]+", stem)
    return " ".join(w.capitalize() for w in words if w)


def infer_company_from_url(url):
    url = clean(url)
    match = re.search(r"https?://(?:www\.)?([^/]+)", url, re.I)
    if not match:
        return ""
    host = match.group(1)
    stem = host.split(".")[0]
    return " ".join(w.capitalize() for w in re.split(r"[\-_]+", stem) if w)


def confidence_from_numeric(value):
    try:
        score = float(value)
    except Exception:
        return clean(value) or "Unknown"
    if score >= 80:
        return "High"
    if score >= 60:
        return "Medium"
    return "Low"


def normalize_type(value, email_contact="", phone="", urls=""):
    t = clean(value)
    low = t.lower()
    if low in {"remote / global", "remote", "worldwide / remote"}:
        return "LinkedIn Search"
    if "phone" in low or "whatsapp" in low:
        return "Phone / WhatsApp Lead"
    if "form" in low or "docs.google.com/forms" in clean(urls).lower():
        return "Form"
    if "linkedin" in low or "search" in low or "needs email" in low or "find via" in clean(email_contact).lower():
        return "LinkedIn Search"
    if "agenc" in low or "recruiter" in low or "staffing" in low:
        return "Agency"
    if "direct" in low or "employer" in low or "company" in low:
        return "Direct Employer"
    if phone and not extract_emails(email_contact):
        return "Phone / WhatsApp Lead"
    if "docs.google.com/forms" in clean(email_contact).lower():
        return "Form"
    return t or "Direct Employer"


def normalize_country(value, email_contact="", company="", notes="", urls=""):
    country = clean(value)
    if country:
        low = country.lower().strip()
        if low in {"uae", "dubai", "dubai / uae", "uae / dubai", "abu dhabi / uae"}:
            return "UAE / Dubai"
        if low in {"remote", "remote / global", "remote / unclear country", "worldwide"}:
            return "Worldwide / Remote"
        if "dubai" in low and ("gcc" in low or "saudi" in low or "mena" in low):
            return "UAE / GCC"
        if low in {"uae / dubai or gcc", "uae / gcc / mena"}:
            return "UAE / GCC"
        if low == "bangalore":
            return "India / Bangalore"
        if low == "delhi":
            return "India / Delhi"
        return country
    text = " ".join([clean(email_contact), clean(company), clean(notes), clean(urls)]).lower()
    if ".ae" in text or "dubai" in text or "uae" in text or "middleeast" in text or "middle east" in text:
        return "UAE / Dubai"
    if ".in" in text or "india" in text or "bangalore" in text or "delhi" in text or "noida" in text:
        return "India"
    if "germany" in text or "munich" in text or "berlin" in text or "hamburg" in text:
        return "Germany"
    if "netherlands" in text or "amsterdam" in text:
        return "Netherlands"
    if "united kingdom" in text or " uk " in f" {text} " or "london" in text:
        return "United Kingdom"
    if "remote" in text:
        return "Worldwide / Remote"
    return "Worldwide / Remote"


def followup_from_sent(sent_date):
    sent = clean(sent_date)
    if not re.match(r"\d{4}-\d{2}-\d{2}$", sent):
        return ""
    return (datetime.strptime(sent, "%Y-%m-%d") + timedelta(days=7)).strftime("%Y-%m-%d")


def normalize_date(value):
    text = clean(value)
    if not text:
        return ""
    if re.match(r"\d{4}-\d{2}-\d{2}$", text):
        return text
    # Google serials from earlier paste operations.
    if re.match(r"\d+(?:\.0+)?$", text):
        try:
            serial = int(float(text))
            if serial > 30000:
                return (datetime(1899, 12, 30) + timedelta(days=serial)).strftime("%Y-%m-%d")
        except Exception:
            pass
    for fmt in ("%d-%m-%Y", "%m/%d/%Y", "%d/%m/%Y"):
        try:
            return datetime.strptime(text, fmt).strftime("%Y-%m-%d")
        except Exception:
            pass
    return text


def make_row(**kwargs):
    row = {col: "" for col in MASTER_COLUMNS}
    for key, value in kwargs.items():
        if key in row:
            row[key] = clean(value)
    row["Email / Contact"] = join_unique(row.get("Email / Contact", ""))
    row["Email Sent To"] = join_unique(row.get("Email Sent To", ""))
    row["URLs"] = join_unique(row.get("URLs", ""))
    row["Phone / WhatsApp"] = join_unique(row.get("Phone / WhatsApp", ""))
    row["Type"] = normalize_type(row["Type"], row["Email / Contact"], row["Phone / WhatsApp"], row["URLs"])
    row["Country / Region"] = normalize_country(
        row["Country / Region"], row["Email / Contact"], row["Company / Agency"], row["Notes"], row["URLs"]
    )
    row["Date Email Sent"] = normalize_date(row["Date Email Sent"])
    row["Date Applied"] = normalize_date(row["Date Applied"])
    row["Follow-up Date"] = normalize_date(row["Follow-up Date"])
    if row["Status"] == "":
        row["Status"] = "To Contact"
    if row["Confidence"] == "":
        row["Confidence"] = "Unknown"
    if row["Reply Status"] == "" and row["Date Email Sent"]:
        row["Reply Status"] = "No Reply"
    if row["Needs Manual Review"] == "":
        row["Needs Manual Review"] = "Yes" if row["Confidence"] in {"Low", "Unknown"} else "No"
    if not row["Follow-up Date"] and row["Status"] in {"Applied", "Followed Up", "Networking"}:
        row["Follow-up Date"] = followup_from_sent(row["Date Email Sent"] or row["Date Applied"])
    return row


def source_row(source, raw):
    company = clean(raw.get("Company / Agency") or raw.get("lead_name") or raw.get("company"))
    email_contact = clean(raw.get("Email") or raw.get("email") or raw.get("email_contact"))
    website = clean(raw.get("website_or_domain") or raw.get("Opening Source URL(s)") or raw.get("urls"))
    phone = clean(raw.get("phone") or raw.get("Phone / WhatsApp") or raw.get("phone"))
    notes = clean(raw.get("Notes") or raw.get("notes"))
    urls = join_unique(website, raw.get("verification_source", ""))
    country_value = clean(raw.get("Country / Region") or raw.get("country_or_region"))
    if not country_value and source.startswith("Original tracker"):
        country_value = "UAE / Dubai"
    if not company:
        emails = extract_emails(email_contact)
        company = infer_company_from_email(emails[0]) if emails else infer_company_from_url(urls)
    source_bits = [source]
    if raw.get("source_screenshot"):
        source_bits.append(clean(raw.get("source_screenshot")))
    return make_row(
        **{
            "Country / Region": country_value,
            "Type": clean(raw.get("Type") or raw.get("proposed_tab") or raw.get("category")),
            "Company / Agency": company,
            "Company Description": clean(raw.get("category") or raw.get("Company Description")),
            "Email / Contact": email_contact,
            "Phone / WhatsApp": phone,
            "Status": clean(raw.get("Status")) or "To Contact",
            "Date Applied": clean(raw.get("Date Applied")),
            "Follow-up Date": clean(raw.get("Follow-up Date")),
            "Notes": notes,
            "Opening Scan Status": clean(raw.get("Opening Scan Status")),
            "Role Applied For": clean(raw.get("Matched Role(s)") or raw.get("role_applied_for")),
            "URLs": urls,
            "Confidence": clean(raw.get("Confidence") or raw.get("confidence")) or "Unknown",
            "Recommended Action": clean(raw.get("Recommended Action")) or (
                "Run agency website/LinkedIn check" if "agenc" in clean(raw.get("proposed_tab")).lower()
                else "Run company careers/LinkedIn check"
            ),
            "Source": "; ".join(source_bits),
            "Last Gmail Thread ID": clean(raw.get("gmail_thread_id")),
            "Last Gmail Message ID": clean(raw.get("gmail_message_id")),
        }
    )


def gmail_row(raw):
    return make_row(
        **{
            "Country / Region": raw.get("country_region", ""),
            "Type": raw.get("type", ""),
            "Company / Agency": raw.get("company", ""),
            "Company Description": raw.get("company_description", ""),
            "Contact Person": raw.get("contact_person", ""),
            "Email Sent To": raw.get("email_sent_to", ""),
            "Email / Contact": raw.get("email_contact", ""),
            "Phone / WhatsApp": raw.get("phone", ""),
            "Role Applied For": raw.get("role_applied_for", ""),
            "Status": raw.get("status", ""),
            "Date Email Sent": raw.get("date_email_sent", ""),
            "Date Applied": raw.get("date_applied", ""),
            "Follow-up Date": raw.get("follow_up_date", ""),
            "Reply Status": raw.get("reply_status", ""),
            "Confidence": raw.get("confidence", ""),
            "Needs Manual Review": raw.get("needs_manual_review", ""),
            "Recommended Action": raw.get("recommended_action", ""),
            "Source": raw.get("source", ""),
            "Notes": raw.get("notes", ""),
            "URLs": raw.get("urls", ""),
            "Last Gmail Thread ID": raw.get("gmail_thread_id", ""),
            "Last Gmail Message ID": raw.get("gmail_message_id", ""),
        }
    )


def raw_ocr_rows():
    path = EXTRACTION / "job-leads-extraction.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    rows = []
    for item in data:
        title = clean(item.get("title"))
        kind = clean(item.get("kind"))
        locations = item.get("locations") or []
        country = " / ".join(locations) if locations else ""
        ent = item.get("entities", {})
        confidence = confidence_from_numeric(item.get("confidence"))
        notes = "OCR raw safety-net row from screenshot; verify before outreach. " + " | ".join(
            clean(x) for x in (item.get("candidateLines") or [])[:4]
        )
        emails = [e.lower() for e in ent.get("emails", []) if e]
        urls = [u for u in ent.get("urls", []) if u]
        phones = [p for p in ent.get("phones", []) if p]
        if emails:
            for email in sorted(set(emails)):
                rows.append(
                    make_row(
                        **{
                            "Country / Region": country,
                            "Type": "Agency" if "agency" in kind.lower() or "recruiter" in kind.lower() else "Direct Employer",
                            "Company / Agency": infer_company_from_email(email),
                            "Company Description": kind,
                            "Email / Contact": email,
                            "Phone / WhatsApp": join_unique(phones),
                            "Status": "To Contact",
                            "Confidence": confidence,
                            "Needs Manual Review": "Yes",
                            "Recommended Action": "Verify OCR email/domain before outreach",
                            "Source": f"Raw OCR: {title}",
                            "Notes": notes,
                            "URLs": join_unique(urls),
                        }
                    )
                )
        elif phones:
            rows.append(
                make_row(
                    **{
                        "Country / Region": country,
                        "Type": "Phone / WhatsApp Lead",
                        "Company / Agency": f"OCR phone lead - {title}",
                        "Company Description": kind,
                        "Phone / WhatsApp": join_unique(phones),
                        "Status": "To Contact",
                        "Confidence": confidence,
                        "Needs Manual Review": "Yes",
                        "Recommended Action": "Verify phone/WhatsApp lead before outreach",
                        "Source": f"Raw OCR: {title}",
                        "Notes": notes,
                        "URLs": join_unique(urls),
                    }
                )
            )
        elif urls:
            for url in sorted(set(urls)):
                rows.append(
                    make_row(
                        **{
                            "Country / Region": country,
                            "Type": "Form" if "docs.google.com/forms" in url.lower() else "LinkedIn Search",
                            "Company / Agency": "Remote design application form" if "docs.google.com/forms" in url.lower() else infer_company_from_url(url),
                            "Company Description": kind,
                            "Status": "To Contact",
                            "Confidence": confidence,
                            "Needs Manual Review": "Yes",
                            "Recommended Action": "Open form/careers URL and verify role",
                            "Source": f"Raw OCR: {title}",
                            "Notes": notes,
                            "URLs": url,
                        }
                    )
                )
    return rows


def dedupe_key(row):
    company = norm_text(row["Company / Agency"])
    country = dedupe_country_key(row["Country / Region"])
    typ = row["Type"]
    emails = extract_emails(row["Email / Contact"], row["Email Sent To"])
    phones = extract_phones(row["Phone / WhatsApp"])
    urls = extract_urls(row["URLs"], row["Email / Contact"])
    if company and not company.startswith("ocr raw") and not company.startswith("gmail contact"):
        return f"company:{company}|{typ}|{country}"
    if emails:
        return "email:" + emails[0]
    if phones:
        return "phone:" + re.sub(r"\D", "", phones[0])
    if urls:
        return "url:" + urls[0].lower()
    return f"raw:{company}|{country}|{typ}"


def compact_cell(value, limit):
    text = clean(value)
    if len(text) <= limit:
        return text
    cut = text[: limit - 15].rsplit(" ", 1)[0].rstrip(" ;,|")
    return cut + " ... [truncated]"


def country_priority(country):
    low = clean(country).lower()
    if low.startswith("uae / dubai"):
        return 0
    if low.startswith("uae / gcc") or low == "uae":
        return 1
    if "dubai" in low or "uae" in low:
        return 2
    if low.startswith("india"):
        return 3
    if low.startswith("germany"):
        return 4
    if low.startswith("netherlands"):
        return 5
    if low.startswith("united kingdom"):
        return 6
    if "remote" in low or "worldwide" in low:
        return 7
    return 8


def type_priority(typ):
    return {
        "Agency": 0,
        "Direct Employer": 1,
        "Form": 2,
        "LinkedIn Search": 3,
        "Phone / WhatsApp Lead": 4,
    }.get(typ, 9)


def dedupe_country_key(country):
    low = clean(country).lower()
    if "uae" in low or "dubai" in low or "gcc" in low or "middle east" in low or "mena" in low:
        return "uae-gcc"
    if "remote" in low or "worldwide" in low or "global" in low:
        return "remote-global"
    if low.startswith("india"):
        return "india"
    return norm_text(country)


def merge_row(base, new):
    for col in MASTER_COLUMNS:
        a, b = base.get(col, ""), new.get(col, "")
        if not b:
            continue
        if col in {"Email / Contact", "Email Sent To", "Phone / WhatsApp", "URLs", "Source", "Last Gmail Thread ID", "Last Gmail Message ID"}:
            base[col] = join_unique(a, b)
        elif col == "Notes":
            base[col] = join_unique(a, b, sep=" | ")
        elif col == "Status":
            if STATUS_RANK.get(b, 0) >= STATUS_RANK.get(a, 0):
                base[col] = b
        elif col == "Reply Status":
            if REPLY_RANK.get(b, 0) >= REPLY_RANK.get(a, 0):
                base[col] = b
        elif col == "Confidence":
            if CONF_RANK.get(b, 0) >= CONF_RANK.get(a, 0):
                base[col] = b
        elif col == "Needs Manual Review":
            base[col] = "Yes" if "Yes" in {a, b} else (a or b)
        elif col in {"Date Email Sent", "Follow-up Date"}:
            base[col] = max([x for x in [a, b] if x], default="")
        elif col == "Date Applied":
            vals = [x for x in [a, b] if x]
            base[col] = min(vals) if vals else ""
        else:
            if not a or a in {"Unknown", "To Contact", "Find via LinkedIn/Website"}:
                base[col] = b
    if base["Status"] in {"Applied", "Followed Up", "Networking"} and not base["Follow-up Date"]:
        base["Follow-up Date"] = followup_from_sent(base["Date Email Sent"] or base["Date Applied"])
    return base


def load_rows():
    rows = []
    current = pd.read_excel(BUILD / "current_tracker.xlsx", sheet_name="Master Job Tracker", dtype=str).fillna("")
    for raw in current.to_dict("records"):
        rows.append(source_row("Current Master Job Tracker", raw))

    original = pd.ExcelFile(BUILD / "original_tracker.xlsx")
    for sheet in original.sheet_names:
        df = pd.read_excel(BUILD / "original_tracker.xlsx", sheet_name=sheet, dtype=str).fillna("")
        for raw in df.to_dict("records"):
            rows.append(source_row(f"Original tracker: {sheet}", raw))

    for fname in [
        "uae-dubai-proposed.csv",
        "outside-dubai-proposed.csv",
        "proposed-tracker-rows-from-unknown.csv",
        "phone-whatsapp-proposed.csv",
    ]:
        df = pd.read_csv(EXTRACTION / fname, dtype=str).fillna("")
        for raw in df.to_dict("records"):
            rows.append(source_row(f"Screenshot proposal: {fname}", raw))

    with open(BUILD / "gmail_last_month_observations.csv", newline="", encoding="utf-8") as f:
        for raw in csv.DictReader(f):
            rows.append(gmail_row(raw))

    rows.extend(raw_ocr_rows())
    return rows


def build_tables():
    rows = load_rows()
    deduped = {}
    duplicate_hits = 0
    for row in rows:
        key = dedupe_key(row)
        if key in deduped:
            duplicate_hits += 1
            deduped[key] = merge_row(deduped[key], row)
        else:
            deduped[key] = row
    final = list(deduped.values())
    for row in final:
        row["Source"] = compact_cell(row["Source"], 260)
        row["Notes"] = compact_cell(row["Notes"], 420)
        row["URLs"] = compact_cell(row["URLs"], 420)
        row["Recommended Action"] = compact_cell(row["Recommended Action"], 220)
    final.sort(key=lambda r: (
        country_priority(r["Country / Region"]),
        type_priority(r["Type"]),
        r["Country / Region"],
        r["Company / Agency"].lower(),
    ))

    agencies = [r for r in final if r["Type"] == "Agency"]
    direct = [r for r in final if r["Type"] == "Direct Employer"]
    forms = [r for r in final if r["Type"] == "Form" or "docs.google.com/forms" in r["URLs"].lower()]
    linkedin = [
        r for r in final
        if r["Type"] == "LinkedIn Search"
        or (
            r["Type"] in {"Agency", "Direct Employer"}
            and not extract_emails(r["Email / Contact"], r["Email Sent To"])
            and not r["Phone / WhatsApp"]
            and r not in forms
        )
    ]
    phones = [r for r in final if r["Type"] == "Phone / WhatsApp Lead" or r["Phone / WhatsApp"]]

    summary = {
        "input_rows_total_before_dedupe": len(rows),
        "dedupe_merge_hits": duplicate_hits,
        "master_rows": len(final),
        "agencies_rows": len(agencies),
        "direct_employers_rows": len(direct),
        "forms_rows": len(forms),
        "linkedin_search_rows": len(linkedin),
        "phone_whatsapp_rows": len(phones),
        "email_bearing_master_rows": sum(bool(extract_emails(r["Email / Contact"], r["Email Sent To"])) for r in final),
        "unique_emails_in_master": len(set(e for r in final for e in extract_emails(r["Email / Contact"], r["Email Sent To"]))),
        "unique_phones_in_master": len(set(p for r in final for p in extract_phones(r["Phone / WhatsApp"]))),
        "gmail_observation_rows": sum(1 for _ in open(BUILD / "gmail_last_month_observations.csv", encoding="utf-8")) - 1,
        "status_counts": dict(Counter(r["Status"] for r in final)),
        "reply_counts": dict(Counter(r["Reply Status"] or "Blank" for r in final)),
        "type_counts": dict(Counter(r["Type"] for r in final)),
        "country_counts_top": dict(Counter(r["Country / Region"] for r in final).most_common(20)),
    }
    return final, agencies, direct, forms, linkedin, phones, summary


def write_tsv(path, rows):
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=TAB_COLUMNS, delimiter="\t", extrasaction="ignore")
        writer.writeheader()
        writer.writerows(rows)


def dashboard_rows(summary):
    rows = [
        ["Metric", "Value"],
        ["Master leads", "=COUNTA('Master Leads'!C2:C)"],
        ["Unique email-bearing rows", "=COUNTIF('Master Leads'!G2:G,\"*@*\")"],
        ["Agencies", "=COUNTIF('Master Leads'!B2:B,\"Agency\")"],
        ["Direct employers", "=COUNTIF('Master Leads'!B2:B,\"Direct Employer\")"],
        ["Forms", "=COUNTIF('Master Leads'!B2:B,\"Form\")"],
        ["LinkedIn / needs-search rows", "=COUNTA('LinkedIn Search'!C2:C)"],
        ["Phone / WhatsApp rows", "=COUNTA('Phone / WhatsApp'!C2:C)"],
        ["Applied", "=COUNTIF('Master Leads'!J2:J,\"Applied\")"],
        ["Followed up", "=COUNTIF('Master Leads'!J2:J,\"Followed Up\")"],
        ["Needs review", "=COUNTIF('Master Leads'!P2:P,\"Yes\")"],
        ["Replies", "=COUNTIF('Master Leads'!N2:N,\"Replied*\")"],
        ["Bounced", "=COUNTIF('Master Leads'!N2:N,\"Bounced\")"],
        ["Rejected", "=COUNTIF('Master Leads'!N2:N,\"Rejected\")+COUNTIF('Master Leads'!J2:J,\"Rejected*\")"],
        ["Follow-ups due", "=COUNTIFS('Master Leads'!M2:M,\"<=\"&TODAY(),'Master Leads'!M2:M,\"<>\",'Master Leads'!J2:J,\"<>Rejected*\")"],
        ["Last Gmail scan", "2026-06-07"],
        ["Source rows before dedupe", str(summary["input_rows_total_before_dedupe"])],
        ["Dedupe merge hits", str(summary["dedupe_merge_hits"])],
    ]
    return rows


def write_outputs():
    final, agencies, direct, forms, linkedin, phones, summary = build_tables()
    outputs = {
        "Master Leads": final,
        "Agencies": agencies,
        "Direct Employers": direct,
        "Forms": forms,
        "LinkedIn Search": linkedin,
        "Phone / WhatsApp": phones,
    }
    for name, rows in outputs.items():
        write_tsv(BUILD / f"{name.replace(' / ', '_').replace(' ', '_').lower()}.tsv", rows)

    with open(BUILD / "dashboard.tsv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter="\t")
        writer.writerows(dashboard_rows(summary))

    (BUILD / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [
        "# Reconciled Job Tracker Summary",
        "",
        f"- Source rows before dedupe: {summary['input_rows_total_before_dedupe']}",
        f"- Dedupe merge hits: {summary['dedupe_merge_hits']}",
        f"- Final master rows: {summary['master_rows']}",
        f"- Unique emails in master: {summary['unique_emails_in_master']}",
        f"- Unique phones in master: {summary['unique_phones_in_master']}",
        f"- Gmail sent observations merged: {summary['gmail_observation_rows']}",
        "",
        "## Type Counts",
        "",
    ]
    md.extend(f"- {k}: {v}" for k, v in summary["type_counts"].items())
    md.extend(["", "## Reply Counts", ""])
    md.extend(f"- {k}: {v}" for k, v in summary["reply_counts"].items())
    md.extend(["", "## Status Counts", ""])
    md.extend(f"- {k}: {v}" for k, v in summary["status_counts"].items())
    (BUILD / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    write_outputs()
