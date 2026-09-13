import os
import sys
import subprocess
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent
AGENT_ROOT = ROOT_DIR / "job-agent"

# Smart Virtual Environment Auto-Detection
VENV_PY = AGENT_ROOT / ".venv" / "Scripts" / "python.exe"
if not VENV_PY.exists():
    VENV_PY = AGENT_ROOT / ".venv" / "bin" / "python"

if VENV_PY.exists() and Path(sys.executable).resolve() != VENV_PY.resolve() and not os.environ.get("__REEXEC_VENV__"):
    os.environ["__REEXEC_VENV__"] = "1"
    sys.exit(subprocess.call([str(VENV_PY), *sys.argv]))

if str(AGENT_ROOT) not in sys.path:
    sys.path.insert(0, str(AGENT_ROOT))

from fastapi.testclient import TestClient
from src.web.app import app
from src.web.db import DB_PATH, get_leads_stats, get_ingestion_history, init_db

init_db()
client = TestClient(app)

def run_checks():
    print("================================================================")
    print("AOE ENGINE & AURAJOBS END-TO-END SYSTEM AUDIT")
    print("================================================================")

    # 1. Check Database Health
    print("\n--- 1. SQLite Database Schema & Stats ---")
    assert DB_PATH.exists(), f"Database file not found at {DB_PATH}"
    stats = get_leads_stats()
    print(f"Total Leads: {stats['total_leads']}")
    print(f"Categories: {stats['categories']}")
    assert stats['total_leads'] > 0, "Leads table should not be empty"
    print("Database check passed!")

    # 2. Check Scraper Endpoints
    print("\n--- 2. Scraper Telemetry & History Endpoints ---")
    r_status = client.get("/api/scraper/status")
    assert r_status.status_code == 200, f"Status failed: {r_status.text}"
    status_data = r_status.json()
    print("Scraper Status Response:", status_data)
    assert "is_running" in status_data
    assert "progress" in status_data

    r_hist = client.get("/api/scraper/history")
    assert r_hist.status_code == 200, f"History failed: {r_hist.text}"
    hist_data = r_hist.json()
    print(f"Previous Ingestion Runs in DB: {hist_data['count']}")
    if hist_data['count'] > 0:
        latest = hist_data['runs'][0]
        print(f"Latest Run: ID={latest['id']}, Role={latest['target_role']}, Scraped={latest['total_scraped']}, Ingested={latest['new_leads_added']}, Skipped={latest['duplicates_skipped']}, Time={latest['runtime_seconds']}s")

    # 3. Check Zero-Auth Email Verification Endpoint
    print("\n--- 3. Zero-Auth Email Deliverability Gate ---")
    r_email = client.post("/api/leads/verify-email", json={"lead_id": 1, "email": "test@mailinator.com"})
    assert r_email.status_code == 200, f"Verify email failed: {r_email.text}"
    email_data = r_email.json()
    print("Email Verification (Burner test):", email_data["verification"])
    assert email_data["verification"]["is_disposable"] is True, "Mailinator must be detected as disposable"

    # 4. Check First-Reader Pitch Auditor
    print("\n--- 4. First-Reader Attention Audit Endpoint ---")
    test_subject = "Senior Product Designer - Application"
    test_body = (
        "Hi Careem Team,\n\n"
        "I recently redesigned a multi-region fintech checkout reducing abandonment by 18%. "
        "I would love to bring this systems experience to Careem's design team.\n\n"
        "Here is my portfolio: https://portfolio.com\n\nBest,\nAlex"
    )
    r_audit = client.post("/api/outreach/audit-pitch", json={"subject": test_subject, "body": test_body})
    assert r_audit.status_code == 200, f"Audit pitch failed: {r_audit.text}"
    audit_data = r_audit.json()
    print(f"Attention Score: {audit_data['attention_score']}/100")
    print(f"Hook Rating: {audit_data['breakdown']['hook_rating']}")
    print(f"Est. Scan Time: {audit_data['metrics']['est_scan_seconds']}s")
    print("Recommendations:", audit_data["recommendations"])

    # 5. Check Stalled Applications Autopsy
    print("\n--- 5. Stalled Applications Autopsy Endpoint ---")
    r_autopsy = client.get("/api/applications/autopsy?days=7")
    assert r_autopsy.status_code == 200, f"Autopsy failed: {r_autopsy.text}"
    autopsy_data = r_autopsy.json()
    print(f"Stalled Applications (>=7d): {autopsy_data['total_stalled']}")
    print(f"High Resurrection Candidates: {autopsy_data['high_pulse_candidates']}")
    print(f"Dominant Cause of Death: {autopsy_data['dominant_cause']}")

    # 6. Check Frontend HTML Components
    print("\n--- 6. Frontend index.html Integrity ---")
    frontend_path = AGENT_ROOT / "frontend" / "index.html"
    html_text = frontend_path.read_text(encoding="utf-8")
    
    required_ids = [
        "scraper-modal",
        "btn-run-scraper",
        "scraper-role",
        "scraper-seniority",
        "scraper-geo",
        "scraper-freshness",
        "scraper-mode",
        "scraper-log-terminal",
        "autopsy-container",
        "autopsy-content",
        "autopsy-days-threshold",
        "first-reader-card",
        "first-reader-results",
        "audit-retention-score"
    ]
    for rid in required_ids:
        assert f'id="{rid}"' in html_text or f"id='{rid}'" in html_text, f"Missing HTML element: {rid}"
        print(f"  [OK] Found #{rid}")

    required_js_funcs = [
        "openScraperModal",
        "closeScraperModal",
        "startScraperRun",
        "pollScraperStatus",
        "verifyLeadEmail",
        "runPitchAudit",
        "loadAutopsyReport"
    ]
    for rfn in required_js_funcs:
        assert f"function {rfn}" in html_text or f"async function {rfn}" in html_text or f"{rfn}(" in html_text, f"Missing JS function: {rfn}"
        print(f"  [OK] Found {rfn}()")

    print("\n================================================================")
    print("ALL 6 END-TO-END VERIFICATION SUITES PASSED CLEANLY!")
    print("================================================================")

if __name__ == "__main__":
    run_checks()
