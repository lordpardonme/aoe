# AGENTS.md — CareerHero Studio

**Welcome, Agent.** This file is the primary orientation and operating standard for **CareerHero Studio** (`G:\job-hunt-app`). Read this completely before inspecting or modifying code.

---

## 0. Previous Conversation & Memory Migration

If you are continuing work from the private workspace or an earlier session, the complete conversation history, architectural decisions, and verification logs are available:

- **Source Conversation ID:** `806be952-95ef-40b0-9dbd-3500f5c1834e`
- **Transcript Path:** `C:\Users\hayaa\.gemini\antigravity\brain\806be952-95ef-40b0-9dbd-3500f5c1834e\.system_generated\logs\transcript.jsonl`
- **Architectural Decisions & Call Graph:** `decisions.md`
- **Handoff Documentation:** `CAREERHERO_HANDOFF.md`

---

## 1. What is CareerHero Studio?

CareerHero Studio is a standalone, local-first web application and autonomous AI co-pilot designed for high-conversion job applications:

1. **✨ Apply Studio**: Ingests JDs via URL or text, matches keywords to candidate taxonomy, enforces strict 1-page CV layout (Bahnschrift typography, WCAG AA contrast, regional protocols e.g. Middle East photo), and drafts conversational cold emails.
2. **📊 Analytics Dashboard**: Tracks application volume, dispatches today, interview rates, and response activity heatmaps with a working zero-state reset (`POST /api/tracker/clear-all`).
3. **🎯 Leads Queue Hub**: Local-first offline SQLite database (`tracker/jobhunt.db`) containing 590+ target leads across Direct Employers, YC Startups, Agencies, and Social leads with search, filtering, and contextual row actions (`📬 Follow-up` + `↺ Re-apply` on applied leads, `✨ Apply` on uncontacted leads).
4. **⚡ Autonomous Batch Tailoring Engine**: Select 10–50 leads to auto-generate tailored 1-page CVs and drafts to Gmail Drafts or dry-run.
5. **📬 7-Day Follow-Up Automation**: Auto-detects unreplied applications >= 7 days old and drafts punchy 2-sentence conversion pitches.
6. **📥 Inbound Recruiter Scanner**: Scans Gmail API for interview invitations, assessments, and rejections, automatically classifying intent.
7. **🔒 Privacy Shield & Activation Guard**: Zero hardcoded personal information. SQLite database and credentials are local-first and strictly `.gitignore`d. Optional Activation Passkey protects live dispatches.

---

## 2. Core Architecture & Stack

| Layer | Technology | Key Files |
|---|---|---|
| **Backend** | Python 3.11, FastAPI, Uvicorn | `job-agent/src/web/app.py`, `run_app.py` |
| **Frontend** | Single-Page Application (HTML5, Tailwind CSS, Vanilla JS) | `job-agent/frontend/index.html` |
| **Database** | Local SQLite (Local-first, gitignored) | `job-agent/tracker/jobhunt.db`, `src/web/db.py` |
| **PDF Generation** | ReportLab (Single-page budget, Bahnschrift font) | `job-agent/src/pdf.py`, `src/resume.py` |
| **Email & Auth** | Google API Client, Gmail OAuth (`InstalledAppFlow`) | `job-agent/src/gmail.py` |
| **LLM Engine** | Multi-provider (Google Gemini, OpenAI, Claude) | `job-agent/src/llm/` |

---

## 3. Runtimes & Commands

- **Python Virtualenv:** `job-agent/.venv/Scripts/python.exe`
- **Start Web Application:**
  ```bash
  python run_app.py
  # Or headless / no-browser:
  job-agent/.venv/Scripts/python.exe run_app.py --no-browser
  ```
- **Live Localhost URL:** `http://127.0.0.1:8000`
- **Automated Verification:**
  ```bash
  python -u scratch/comprehensive_ui_ux_audit.py
  ```

---

## 4. Standing Operational Rules

1. **Zero Privacy Leak:** Never commit `.db`, `.sqlite`, `token.json`, `credentials.json`, or `.env` to Git. Keep code generic for open-source distribution.
2. **Safe Mode First:** Default `DRY_RUN=True` for all dispatches. Real sends require explicit user toggle or activation passkey.
3. **Log All Decisions:** When adding features or refactoring, record decisions and rationale in `decisions.md`.
4. **Audit Before Complete:** Use headless Playwright testing to verify all buttons, modals, and endpoints before concluding any turn.
