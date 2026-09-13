# CareerHero Studio — Project State & Agent Handoff

**Location:** `G:\job-hunt-app`  
**Last Updated:** 2026-09-13  
**Repo Branch:** `main`  
**Localhost URL:** `http://127.0.0.1:8000` (FastAPI + Static Frontend)  
**Detailed Decisions & Call Graph:** [`decisions.md`](file:///G:/job-hunt-app/decisions.md)

---

## 1. What This Product Is
**CareerHero Studio** is an enterprise-grade, privacy-first local web application and AI job application co-pilot. It is completely decoupled from private personal data and ready for open-source distribution:
- **Local-First SQLite Architecture:** All personal profiles, leads, applications, and inbound email scans reside strictly in offline SQLite (`G:\job-hunt-app\job-agent\tracker\jobhunt.db`), which is strictly `.gitignore`d.
- **Privacy Shield:** Default templates and source files contain zero personal identity. Candidate identity is stored locally in the offline `profile` database table.
- **Safety Locks:** Defaults to Safe Mode (`DRY_RUN=true`). Automated live email dispatches are locked by an optional **Activation Passkey**.
- **Modern UI Canvas:** Ultra-clean light-mode workspace (`#F8FAFC`, `#0F172A` dark slate sidebar, `#2563EB` royal blue accents, pure CSS 4-square grid loader).

---

## 2. Completed Core Capabilities (Phases 1–5 Complete)

### A. Leads Queue Hub (`/api/leads`, `/api/leads/stats`, `/api/leads/import-csv`)
- **590+ Pre-Loaded Target Leads:** Ingested and deduplicated across Direct Employers (420+), Agencies (125+), YC Startups (20), and Social/LinkedIn leads.
- **Interactive Filtering & Category Tabs:** Real-time filtering by category (`All`, `Direct`, `YC Startups`, `Agencies`, `Social / LinkedIn`) and status (`To Contact`, `Applied`, `Drafted`, `Interview`, `Rejected`).
- **Instant Search:** Instant multi-field query matching company name, role, country, and contact email.
- **1-Click Apply Handoff:** Click `✨ Apply` on any lead to load its company, target role, contact email, and detected country directly into the Apply Studio.
- **CSV Importer Modal:** Drag-and-drop file upload or raw CSV paste with intelligent header detection (`Company`, `Role`, `Email`, `Country`, `Category`, `Status`).
- **Add Single Lead Modal:** Quick entry modal for ad-hoc company outreach.

### B. Autonomous Batch Tailoring Engine (`POST /api/batch/run`)
- **Multi-Select Bulk Processing:** Check multiple target leads in the Leads table to trigger batch operations.
- **Autonomous Tailoring:** Auto-synthesizes tailored 1-page CVs via `ResumeBuilder` and renders verified PDFs via `render_resume_pdf`.
- **Personalized Pitch Drafting:** Generates high-conversion email pitches referencing target company and candidate portfolio evidence.
- **3 Execution Modes:**
  1. `draft` (Default): Saves messages with attached PDFs directly into the user's real **Gmail Drafts** folder (`mail.google.com/mail/#drafts`).
  2. `dry_run`: Generates local PDF and email text artifacts without network dispatch.
  3. `live_send`: Dispatches live emails via Gmail API. Guarded by the **Activation Passkey**.
- **Visual Batch Modal:** Includes mode selector, real-time progress bar, and live terminal execution log stream.

### C. Follow-Up Automation & Inbound Reply Scanner (`/api/tracker/follow-ups`, `/api/gmail/scan`)
- **7-Day Follow-Up Detector:** Identifies all applications or leads applied >= 7 days ago with zero inbound recruiter replies.
- **2-Sentence High-Converting Pitch Drafter:** Generates concise, polite follow-ups referencing candidate live work.
- **Follow-Up Drafter Modal:** Allows 1-click clipboard copy or direct Gmail Draft creation.
- **Inbound Recruiter Scanner:** Scans user's Gmail inbox (`gmail.readonly`) for recent recruiter responses, classifies intent (Interview, Challenge/Screening, Rejection, Under Review), and updates application statuses automatically.

### D. The Apply & Tailor Studio (`/api/tailor-resume`, `/api/analyze-job`, `/api/draft-email`)
- **Country-Dependent Sample JDs:** Dynamic prompts reveal sample JDs only *after* location is selected (UAE/Dubai, US/Canada, UK/Europe, India, Saudi Arabia, Germany).
- **Strict 1-Page Formatting Engine:** Automatically fits the resume to a 1-page budget unless 2-page executive is explicitly chosen.
- **Dubai / Middle East Protocol Alert:** Prompts for professional headshot path, nationality, and visa status when UAE or Saudi Arabia is selected.
- **Formatted Print-Ready CV Preview Modal (`[ 👁️ Preview CV ]`):** Formatted document modal with candidate contact details, Dubai metadata, accent rules, bullets, live links, and a direct `window.print()` button.

### E. In-App Gmail OAuth Loop (`/api/gmail/*`)
- **Header Connection Status Pill:** `🟢 Gmail: user@gmail.com` vs `⚠️ Connect Gmail`.
- **3-Step Setup Modal:** Embedded Google Cloud Console instructions, credentials file paste/uploader, and **"Auto-Detect Workspace Token"**.
- **1-Click Interactive OAuth:** Launches local loop, opens browser for consent, and writes local `token.json`.

### F. Analytics Dashboard & Activity Heat Map
- Starting-at-0 dynamic KPI counters (increment live on application actions).
- 30-Day Activity Heat Map (pure CSS/JS matrix).
- Speedometer Arc gauge for ATS keyword match percentage.
- Chronological activity stream tracking last and preceding applications.

---

## 3. Tech Stack & Key Files

| Component | Technology | File Path |
|---|---|---|
| **Backend Application** | FastAPI, Uvicorn, Pydantic | `G:\job-hunt-app\job-agent\src\web\app.py` |
| **Database Layer** | SQLite (`leads`, `applications`, `profile`, `inbound_replies`) | `G:\job-hunt-app\job-agent\src\web\db.py` |
| **Frontend Workspace** | Vanilla HTML5, Tailwind CSS, Pure CSS Grid Loader | `G:\job-hunt-app\job-agent\frontend\index.html` |
| **Gmail Integration** | Google API Client (`gmail.send`, `gmail.readonly`, `gmail.compose`) | `G:\job-hunt-app\job-agent\src\gmail.py` |
| **Resume & PDF Engine**| ReportLab, Docx | `G:\job-hunt-app\job-agent\src\pdf.py` & `src/resume.py` |
| **App Runner** | Python CLI launcher | `G:\job-hunt-app\run_app.py` |
| **Decisions Log** | Architecture Decision Records & Call Graph | `G:\job-hunt-app\decisions.md` |

---

## 4. Quick Start & Verification

### To Run Locally:
```powershell
cd G:\job-hunt-app
python run_app.py
```
Open **`http://127.0.0.1:8000`** in your browser.

### To Run Tests:
```powershell
G:\job-hunt-app\job-agent\.venv\Scripts\python.exe "C:\Users\hayaa\.gemini\antigravity\brain\806be952-95ef-40b0-9dbd-3500f5c1834e\scratch\test_leads_and_batch_endpoints.py"
```
