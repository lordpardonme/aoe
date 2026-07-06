import base64
import json
import re
from datetime import datetime
from pathlib import Path


OLD_CODEX = Path(r"C:\Users\mohdh\.codex_old")
WORKSPACE = Path(r"C:\Users\mohdh\Documents\Job Hunt")
OUT_DIR = WORKSPACE / "resumes" / "recovered-context"
ASSET_DIR = OUT_DIR / "screenshots"

SESSION = OLD_CODEX / "sessions" / "2026" / "06" / "02" / "rollout-2026-06-02T16-47-01-019e880d-066f-7ee0-9e45-12bf352ec54a.jsonl"
TRANSCRIPTIONS = OLD_CODEX / "transcription-history.jsonl"

KEYWORDS = re.compile(
    r"fuelbuddy|fuel buddy|fulebuddy|auto bay|arjun|wallet|business account|business login|"
    r"dubai|b2b|customer app|meddo|resume|cv|master cv|career evidence|agency|email|apply|"
    r"tracker|sheet|ats|ziina|property finder|bac|cig|derby",
    re.IGNORECASE,
)


def parse_ts(value: str) -> str:
    if not value:
        return ""
    try:
        return datetime.fromisoformat(value.replace("Z", "+00:00")).astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    except ValueError:
        return value


def compact(text: str) -> str:
    return re.sub(r"\s+", " ", text or "").strip()


def data_url_to_png(data_url: str, output: Path) -> None:
    prefix, payload = data_url.split(",", 1)
    if not prefix.startswith("data:image/png;base64"):
        raise ValueError(f"Unsupported image data URL: {prefix[:40]}")
    output.write_bytes(base64.b64decode(payload))


def extract_transcriptions() -> list[dict]:
    items: list[dict] = []
    for line_no, line in enumerate(TRANSCRIPTIONS.read_text(encoding="utf-8").splitlines(), start=1):
        obj = json.loads(line)
        ts = datetime.fromtimestamp(obj["createdAtMs"] / 1000).astimezone()
        text = compact(obj.get("text", ""))
        if KEYWORDS.search(text):
            items.append(
                {
                    "source": str(TRANSCRIPTIONS),
                    "line": line_no,
                    "time": ts.strftime("%Y-%m-%d %H:%M:%S %Z"),
                    "text": text,
                }
            )
    return items


def extract_session() -> tuple[list[dict], list[dict]]:
    items: list[dict] = []
    images: list[dict] = []

    with SESSION.open("r", encoding="utf-8") as handle:
        for line_no, line in enumerate(handle, start=1):
            obj = json.loads(line)
            payload = obj.get("payload", {})
            msg = ""
            if obj.get("type") == "event_msg":
                msg = compact(payload.get("message", ""))
            elif obj.get("type") == "response_item" and payload.get("type") == "message":
                msg = compact(" ".join(part.get("text", "") for part in payload.get("content", [])))

            imgs = payload.get("images") or []
            if msg and KEYWORDS.search(msg):
                items.append(
                    {
                        "source": str(SESSION),
                        "line": line_no,
                        "time": parse_ts(obj.get("timestamp", "")),
                        "text": msg,
                    }
                )

            if imgs and (KEYWORDS.search(msg) or line_no in {1643, 1681}):
                if line_no == 1643:
                    label = "fuelbuddy-assets-dashboard"
                elif "franchise dashboard" in msg.lower():
                    label = "fuelbuddy-franchise-dashboard"
                elif "customer app for dubai" in msg.lower():
                    label = "fuelbuddy-dubai-customer-app"
                elif "wallet thing" in msg.lower() or "fuelbuddy business" in msg.lower():
                    label = "fuelbuddy-business-wallet"
                else:
                    label = "job-hunt-context-image"
                for index, data_url in enumerate(imgs, start=1):
                    path = ASSET_DIR / f"{label}-line-{line_no}-{index}.png"
                    data_url_to_png(data_url, path)
                    images.append(
                        {
                            "source": str(SESSION),
                            "line": line_no,
                            "time": parse_ts(obj.get("timestamp", "")),
                            "message": msg,
                            "file": str(path),
                            "bytes": path.stat().st_size,
                        }
                    )

    return items, images


def write_markdown(transcriptions: list[dict], session_items: list[dict], images: list[dict]) -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)

    md = [
        "# Recovered Job Hunt Context",
        "",
        "Recovered from old Codex history. Keep factual; use for resume/CV tailoring and outreach only.",
        "",
        "## Screenshot Evidence",
        "",
    ]
    for item in images:
        md.extend(
            [
                f"- `{Path(item['file']).name}`",
                f"  - source: `{item['source']}` line `{item['line']}`",
                f"  - time: `{item['time']}`",
                f"  - bytes: `{item['bytes']}`",
                f"  - context: {item['message']}",
            ]
        )

    md.extend(["", "## Dictation History", ""])
    for item in transcriptions:
        md.extend(
            [
                f"### {item['time']} line {item['line']}",
                "",
                item["text"],
                "",
            ]
        )

    md.extend(["", "## Session Messages", ""])
    for item in session_items:
        md.extend(
            [
                f"### {item['time']} line {item['line']}",
                "",
                item["text"],
                "",
            ]
        )

    (OUT_DIR / "recovered-job-hunt-context.md").write_text("\n".join(md), encoding="utf-8")

    summary = [
        "# Resume Memory Rebuild",
        "",
        "Use this as compact working memory for future CV/application work.",
        "",
        "## FuelBuddy Evidence",
        "",
        "- FuelBuddy wallet/payment work: user says they made wallet and payment system, reducing transaction errors by 38%.",
        "- Multi-wallet user feature: main user can delegate/add users, let them use wallet, set/control wallet limits.",
        "- FuelBuddy assets page / Auto Bay: desktop web assets dashboard for gensets, cars, trucks, and anything that stores fuel; distinct from Arjun.",
        "- FuelBuddy Business / business account surface: business login for registered partners; manage orders, fuel storage, filled asset, wallet, assigned users, delegation, account access, credit limits.",
        "- Dubai customer app: Dubai B2B web app, not India consumer delivery flow; used by business customers for tracking.",
        "",
        "## Outreach Workflow",
        "",
        "- Maintain tracker sheet: mark sent/applied, date applied, follow-up date, notes/CV version, sent email ID when available.",
        "- Pick one agency at a time; research specialization; tailor CV to their hiring sectors.",
        "- Use agency inbox from sheet; add person/recruiter email or CC only when credible.",
        "- Show research, recipients, CV angle, email draft, attachment name before sending.",
        "- Send only after explicit approval.",
        "",
        "## Resume Workflow",
        "",
        "- Build master CV/evidence from real product work first; avoid generic bullets.",
        "- For fintech: emphasize FuelBuddy wallet/payment, transaction-error reduction, delegation/limits, KYC/payment UX where truthful.",
        "- For energy/logistics/oil: emphasize FuelBuddy B2B, fleet/assets, fuel operations dashboards.",
        "- For healthcare: emphasize Meddo, booking flows, usability testing.",
        "- For real estate: emphasize marketplace/search/catalog and consumer UX.",
        "- For agencies: create unique agency-specific CV angle, not generic one.",
        "",
        "## Recovered Assets",
        "",
    ]
    for item in images:
        summary.append(f"- {Path(item['file']).name}: {item['message']}")
    (OUT_DIR / "resume-memory-rebuild.md").write_text("\n".join(summary), encoding="utf-8")


def main() -> None:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    ASSET_DIR.mkdir(parents=True, exist_ok=True)
    transcriptions = extract_transcriptions()
    session_items, images = extract_session()
    write_markdown(transcriptions, session_items, images)
    print(f"transcriptions={len(transcriptions)}")
    print(f"session_items={len(session_items)}")
    print(f"images={len(images)}")
    print(OUT_DIR)


if __name__ == "__main__":
    main()
