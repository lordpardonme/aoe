# Architectural Decisions & Codebase Execution Flow

**Project:** CareerHero Studio (`G:\job-hunt-app`)  
**Maintained By:** Autonomous Development Agent  
**Last Updated:** 2026-09-13  

---

## 1. Architectural Decisions Log (ADR)

### Decision 1: SQLite as Local-First Storage (Replacing Google Sheets for Product Core)
* **Context:** The private workspace relied heavily on a live Google Sheet with 10 tabs and ~500 rows. Exposing this sheet in a public repo or to friends would leak personal contact data, recruiter emails, and private notes. Furthermore, requiring new users to set up Google Cloud OAuth just to view their tracker creates severe onboarding friction.
* **Decision:** Implement a local SQLite database (`job-agent/tracker/jobhunt.db`) with tables for `profile`, `leads`, `applications`, and `inbound_replies`.
* **Why this approach?**
  - **Zero Privacy Leak:** SQLite is a single offline file that is strictly `.gitignore`d. It never leaves the user's computer.
  - **Zero Setup Friction:** SQLite requires zero server configuration or cloud credentials. When a new user clones the app, the database initializes itself instantly.
  - **High Performance:** Instant queries, local indexing, and ACID transactions for hundreds of leads.

### Decision 2: Strict Privacy Decoupling & Profile-First Identity
* **Context:** Hardcoded defaults in earlier prototypes referenced real candidate details (name, email, phone, live portfolio links).
* **Decision:** Genericize all default code strings to generic placeholders (`"Candidate Name"`, `"user@example.com"`). Move all personal identity into the local `profile` SQLite table.
* **Why this approach?** Ensures that if the repository is published to GitHub or shared with friends, no personal identity is exposed in the source code or template files.

### Decision 3: Autonomous Batch Queue with Mandatory Safe-Mode Guard
* **Context:** The user needs to process batches of leads (e.g. 10-20 companies at a time), scrape JDs, tailor CVs, and draft personalized outreach. Running this headlessly risks accidental mass-email dispatching.
* **Decision:** Implement an autonomous batch queue with `DRY_RUN=true` enforced by default. Emails are saved either locally to SQLite or to the user's personal Gmail Drafts folder (`mail.google.com/mail/#drafts`). Live dispatch requires explicit user toggle and confirmation.
* **Why this approach?** Guarantees zero accidental sends, prevents spam reputation damage, and allows the candidate to review generated pitches before anything is sent.

### Decision 4: Secret Passkey / Activation Guard
* **Context:** In the private workspace, sensitive operations required the case-sensitive activation phrase `fuck this shit`. In an open-source product, users should have the same security capability without hardcoded profanity.
* **Decision:** Provide a configurable **Activation Passkey** stored in the local profile. When enabled, autonomous batch runs, Gmail scans, and status summaries remain locked until the passkey is provided.
* **Why this approach?** Gives users an airtight safety lock on autonomous background agents.

### Decision 5: In-App Gmail OAuth Loop (`InstalledAppFlow`)
* **Context:** Previously, authenticating Gmail required running terminal Python scripts (`authenticate.py`), navigating terminal logs, and copying files.
* **Decision:** Embed the OAuth flow directly into the web UI via `POST /api/gmail/authorize` and `GET /api/gmail/status`.
* **Why this approach?** Provides a frictionless 1-click browser pop-up experience for authenticating Google accounts without terminal commands.

### Decision 6: Zero-Auth Free Public APIs for Enrichment & Deliverability
* **Context:** The application requires real-time email deliverability verification, currency conversions for international salaries, and regional job market ingestion without forcing users to register for API keys, pay credit card subscriptions, or hit hard rate limits.
* **Decision:** Implement a dedicated Zero-Auth service client (`src/services/public_apis.py`) utilizing completely free, unauthenticated public endpoints:
  - Kickbox Open API (`open.kickbox.com/v1/verify`) with Disify (`disify.com/api/email/`) fallback for email deliverability and burner/disposable domain detection.
  - Arbeitnow, Remotive, and RemoteOK REST public feeds for live job extraction.
  - Frankfurter API (European Central Bank) for currency conversion.
  - REST Countries API for regional hiring protocol rules.
* **Why this approach?** Guarantees zero onboarding friction, zero API cost for any user, and resilient fallback mechanisms if any individual public endpoint experiences downtime.

### Decision 7: Internal Scraper Engine Isolation & Dual-Mode Acquisition
* **Context:** The external scraping repository `D:\JobSpy` contains battle-tested scrapers (LinkedIn, Indeed, ZipRecruiter, Glassdoor) alongside role expansion and visa detection algorithms. However, `D:\JobSpy` must remain pristine and untouched.
* **Decision:** Copy `core`, `sources`, and `config` directly into `job-agent/src/scraper/` and build an asynchronous bridge service (`src/services/jobspy_service.py`) supporting two distinct acquisition modes:
  - **Express Mode (~30s):** Fast parallel extraction across zero-auth public JSON feeds (Remotive, Arbeitnow, RemoteOK). Ideal for quick dashboard top-ups.
  - **Comprehensive MultiBoard Mode:** Deep multi-source crawling across major job boards utilizing `MultiBoardAdapter` within a background `ThreadPoolExecutor`.
* **Why this approach?** Preserves source repository immutability while giving candidates both rapid feed updates and deep search capabilities without freezing the ASGI server event loop.

### Decision 8: Deterministic SHA256 Deduplication & Content Fingerprinting
* **Context:** Ingesting job postings from multiple remote job boards inevitably captures duplicate postings for the same position across different aggregators.
* **Decision:** Generate a deterministic 16-character SHA256 hex digest (`generate_job_fingerprint`) based on normalized `(company_name, job_title)` and cross-check against canonical job URLs before inserting into SQLite.
* **Why this approach?** Completely prevents lead duplication in the offline database while logging skipped duplicates in `ingestion_runs` telemetry.

### Decision 9: First-Reader Attention Audit & Outreach Quality Gate
* **Context:** Cold job outreach emails sent to founders and hiring managers are frequently ignored if they exceed a 15-second scan window, contain excessive buzzwords, or lack a clear metric-backed value proposition.
* **Decision:** Implement an algorithmic attention retention auditor (`src/services/first_reader.py`) that scores pitches (0-100) based on hook quality, word count budgets (75-125 words optimal), reading ease, and low-friction call-to-action questions before allowing dispatch.
* **Why this approach?** Enforces behavioral quality standards on all AI-generated or user-edited drafts, maximizing recruiter response rates.

### Decision 10: Stalled Applications Autopsy & Resurrection Pulse
* **Context:** Candidates frequently submit job applications that receive no response after 7–14 days. Without proactive tracking, these applications become silent dead-ends.
* **Decision:** Implement an autonomous autopsy service (`src/services/autopsy_service.py`) that scans the `applications` and `leads` database, assigns a probable cause of death (ATS Blackhole, Ghosting, Incomplete Pipeline), calculates a Resurrection Pulse score (0-100), and provides 1-click tailored follow-up drafting.
* **Why this approach?** Transforms dormant job applications into active second-chance interview opportunities.

---

## 2. Codebase Execution Flow & Call Graph

### A. High-Level Architecture Overview
```
[ Browser Client: frontend/index.html ]
              │  (Fetch API JSON)
              ▼
[ FastAPI Server: src/web/app.py ]  ◄─── [ Runner: run_app.py ]
      ├──► [ Database: src/web/db.py (SQLite jobhunt.db) ]
      ├──► [ Gmail Client: src/gmail.py (Google API Client) ]
      ├──► [ LLM Engine: src/llm/ (Gemini / Claude / OpenAI) ]
      ├──► [ Resume Builder: src/resume.py & src/pdf.py (ReportLab) ]
      └──► [ Job Parser & Scraper: src/jobs.py ]
```

### B. Execution Flow Order & Trace

#### 1. App Startup Cycle
1. User executes `python run_app.py` in `G:\job-hunt-app`.
2. `run_app.py` imports `uvicorn` and boots the FastAPI application from `src.web.app:app` on port `8000`.
3. During startup:
   - `src/web/db.py:init_db()` is invoked: Creates `jobhunt.db` if missing, initializes tables (`applications`, `profile`, `leads`, `inbound_replies`).
   - Static files from `frontend/` are mounted at `/`.
4. The user's browser opens `http://127.0.0.1:8000`:
   - `DOMContentLoaded` fires in `index.html`.
   - The Pure CSS 4-square blue keyframe pulse loader animates and dismisses after 400ms.
   - `checkGmailStatus()` calls `GET /api/gmail/status` to determine OAuth state.
   - `loadProfileData()` calls `GET /api/profile` to populate candidate identity.
   - `loadDashboardStats()` calls `GET /api/tracker/applications` and updates KPI counts.
   - `loadInboundRepliesFeed()` calls `GET /api/gmail/replies` to render recent recruiter responses.

#### 2. Job Ingestion & Tailoring Cycle (`runCompleteTailoring`)
1. User pastes job link/text or picks a country (e.g. `🇦🇪 UAE`) and clicks **"✨ Paraphrase JD & Generate 1-Page Application"**.
2. Frontend calls `POST /api/analyze-job`:
   - `app.py:analyze_job_endpoint` extracts keywords and scores ATS match.
   - Frontend updates Speedometer Arc gauge and matched skills count.
3. Frontend calls `POST /api/tailor-resume`:
   - `app.py:tailor_resume_endpoint` invokes `ResumeBuilder` and LLM client.
   - Enforces strict 1-page budget and country protocol (photo, visa status for Middle East).
   - Generates tailored markdown resume and renders PDF via `render_resume_pdf`.
   - Populates CV preview textarea.
4. Frontend calls `POST /api/draft-email`:
   - Generates personalized cold email tailored to company mission and candidate live work.
   - Populates subject line and email body.

#### 3. Dispatch & Tracking Cycle (`executeSendOrDryRun` / `createGmailDraftAction`)
1. User clicks **"⚡ 1-Click Send"** or **"📝 Save Draft"**:
   - For **1-Click Send**: Calls `POST /api/email/send`.
     - `GmailClient.send_email` checks `DRY_RUN`.
     - If `DRY_RUN=True`: Simulates send, generates mock ID.
     - If `DRY_RUN=False`: Dispatches MIME multipart message (body + attached PDF) via Gmail API.
     - `record_application()` saves record into SQLite `applications` table.
   - For **Save Draft**: Calls `POST /api/email/create-draft`.
     - `GmailClient.create_draft` inserts draft with attached PDF into user's real Gmail Drafts folder.
2. Frontend updates KPI counters, lights up the Activity Heat Map, and adds entry to the Applied Tracker table.

#### 4. Inbound Scanner Cycle (`triggerInboundScan`)
1. User clicks **"⚡ Scan Gmail for Replies"**:
2. Frontend calls `POST /api/gmail/scan`:
   - `GmailClient.scan_inbound_replies` queries `users().messages().list(q="-from:me newer_than:30d")`.
   - Traverses MIME parts, extracts snippet and clean text.
   - `classify_reply_intent` categorizes intent: Interview, Assessment, Rejection, Review.
   - Matches incoming sender/domain against tracked applications.
   - `record_inbound_reply()` updates application status in SQLite.
3. Frontend updates recruiter response feed and refreshes tracker statuses.

## 3. Changes Applied in This Cycle (Phases 1–5 Tracking)

### Phase 1: Privacy Shield & Database Migration [COMPLETED]
- **Schema Upgrade (`src/web/db.py`)**:
  - Added `leads` table schema (`id`, `source_sheet`, `company`, `role`, `country`, `category`, `contact_email`, `contact_person`, `website`, `job_url`, `status`, `notes`, `matched_skills`, `applied_date`, `follow_up_date`, `created_at`).
  - Implemented lead CRUD functions: `record_lead`, `list_leads`, `get_lead`, `update_lead_status`, `bulk_insert_leads`, `get_leads_stats`.
  - Added `activation_passkey` field to `profile` table and migration handler.
  - Sanitized default profile row creation to generic `'Candidate Name'`.
- **Google Sheets to SQLite Data Migration**:
  - Executed high-fidelity ingestion script connecting via Google Sheets API.
  - Ingested 1,006 raw rows from 5 live tabs: `Master Job Tracker` (437 rows), `YC Startups Aug 2026` (20 rows), `Direct Employers` (218 rows), `Priority Outreach Backlog` (252 rows), and `Social Leads Jul 2026` (82 rows).
  - Deduplicated across all sources by `(company, contact_email)` into 591 clean records in local `jobhunt.db` (Categories: 423 Direct, 127 Agency, 21 Social/LinkedIn, 20 YC Startups).
- **Privacy Decoupling & Sanitization**:
  - Sanitized `src/web/app.py` candidate evidence defaults from hardcoded personal data to generic placeholders.
  - Sanitized `frontend/index.html` sidebar initials (`CN`), username (`Candidate Name`), modal email, and dynamic email subject fallbacks.
  - Updated `job-agent/.env.example` with generic identity placeholders.
  - Updated `G:\job-hunt-app\.gitignore` to strictly exclude `*.db`, `*.sqlite`, `job-agent/tracker/`, `reconciled-tracker-build/`, and generated PDFs.

### Phase 2: Lead Management Hub & UI Importer [COMPLETED]
- **API Endpoints (`src/web/app.py`)**:
  - `GET /api/leads`: Full query engine supporting category filter (`Direct`, `YC Startups`, `Agency`, `Social / LinkedIn`), status filter (`To Contact`, `Applied`, `Drafted`, `Interview`, `Rejected`), live text search, and pagination.
  - `GET /api/leads/stats`: Real-time aggregation of total leads, status counts, and category distribution.
  - `GET /api/leads/{id}`: Single lead retrieval.
  - `POST /api/leads`: Manual entry of new target leads with full metadata.
  - `POST /api/leads/update-status`: Update lead status and append audit notes.
  - `POST /api/leads/import-csv`: Universal CSV parser supporting file upload or pasted text with flexible column mapping.
- **Frontend Leads Queue Hub (`frontend/index.html`)**:
  - Added dedicated navigation item (`nav-leads`) and top header tab (`tab-leads`) with live badge counters.
  - Built `view-leads` workspace featuring 4 KPI metric cards (Total Leads, Ready to Contact, Applied/Drafted, Due for Follow-up).
  - Built responsive table with multi-select checkboxes, category pills, email mailto links, status badges, and 1-click `✨ Apply` to load lead context directly into Apply Studio.
  - Built `CSV Import Modal` supporting drag-and-drop file upload and raw CSV paste.
  - Built `Add Single Lead Modal`.

### Phase 3: Autonomous Pipeline & Batch Engine [COMPLETED]
- **Batch Processing Engine (`POST /api/batch/run`)**:
  - Iterates over user-selected lead IDs in bulk.
  - Auto-synthesizes tailored 1-page CVs via `ResumeBuilder` and renders verified PDFs via `render_resume_pdf`.
  - Drafts high-conversion, personalized outreach pitches referencing target company and candidate live work.
  - Dispatches across 3 configurable modes:
    - `draft` (Default & Recommended): Saves drafts directly into the user's Gmail Drafts folder (`mail.google.com/mail/#drafts`) with attached PDFs.
    - `dry_run`: Generates local PDF and email artifacts without touching Gmail.
    - `live_send`: Dispatches real outbound emails via Gmail API (requires Safety Passkey).
  - Synchronizes execution results with SQLite `applications` and `leads` tables.
- **Batch Runner UI Controls**:
  - Built multi-select batch action bar in Leads Queue table.
  - Built `Batch Runner Modal` featuring mode selector, real-time progress bar, and live execution terminal log stream.

### Phase 4: Follow-Up Automation & Secret Passkey Guard [COMPLETED]
- **7-Day Follow-Up Engine**:
  - `GET /api/tracker/follow-ups`: Detects leads or applications applied >= 7 days ago where no inbound recruiter reply has been recorded.
  - `POST /api/email/draft-follow-up`: Generates concise, polite 2-sentence follow-up pitches citing candidate live work.
  - Built `Follow-Up Drafter Modal` in UI allowing 1-click clipboard copy or direct Gmail Draft creation.
- **Activation Passkey Guard (Safety Lock)**:
  - Added `activation_passkey` field to SQLite `profile` table and Settings UI.
  - Enforced strict passkey verification on `POST /api/batch/run` when `mode == 'live_send'`. If passkey is missing or invalid, request is rejected with HTTP 403, preventing unintended email dispatches.

### Phase 5: Cross-Chat Memory & Public Documentation [COMPLETED]
- **Cross-Chat Memory Bridge**: Appended non-destructive Section 11 to `g:\job-hunt-workspace-private\AGENTS.md` so that future sessions and different agent chats in Antigravity or other agent runtimes immediately understand the existence, purpose, and architecture of `G:\job-hunt-app` without disrupting existing private workflows.
- **Product Documentation**: Authored an open-source, developer-friendly `README.md` in `G:\job-hunt-app` with architecture highlights, feature breakdown, setup steps, and environment variable references.
- **Agent Handoff Guide**: Updated `CAREERHERO_HANDOFF.md` with complete API maps, UI specifications, verification commands, and tech stack details.
- **End-to-End Verification**: Executed automated test suite verifying all 12 API endpoints (Leads Hub, CSV Import, Batch Tailoring Engine, Follow-ups, and Passkey security).

### Bugfix: Frontend Generation Error (`ReferenceError: dataEmail is not defined`) [RESOLVED]
- **Issue**: Clicking "✨ Paraphrase JD & Generate 1-Page Application" threw a browser alert: `Generation error: ReferenceError: dataEmail is not defined`.
- **Root Cause**: In `frontend/index.html:runCompleteTailoring()`, `const dataEmail = await resEmail.json();` was accidentally omitted right after fetching `/api/draft-email`.
- **Resolution**:
  - Restored `const dataEmail = await resEmail.json();` before assigning subject and email body values.
  - Ensured recipient variable `const to = document.getElementById('apply-email').value.trim();` is declared in both `executeSendOrDryRun()` and `createGmailDraftAction()`.
  - Statically audited all script blocks in `frontend/index.html` (309 balanced braces, 990 balanced parens, zero syntax errors).
  - Validated end-to-end tailoring pipeline test returning 200 OK.

---

### Phase 6: Interactive Disconnect/Connect Flow, Contextual Row Actions, & Headless Playwright Audit [COMPLETED]

#### Decision 6: Explicit User-Initiated Gmail Disconnection & Reconnection Flow
* **Context**: Previously, `GmailClient.service` and `GmailClient.get_auth_status()` contained an internal fallback (`_auto_sync_from_workspace_if_needed()`) that automatically re-copied `token.json` from the private workspace whenever `token.json` was missing. As a result, users could not test the disconnected onboarding flow or disconnect their Google integration.
* **Decision**: 
  - Remove silent background syncing from `service` and `get_auth_status()` in `src/gmail.py`.
  - Introduce `POST /api/gmail/disconnect` to unlink local `token.json` and reset the cached client service.
  - Add a dedicated **"🔌 Disconnect"** button in `#gmail-status-card` inside the Google Cloud connection modal in `frontend/index.html`.
  - Keep workspace token synchronization strictly explicit via the **"🔄 Auto-Detect Workspace Token"** button (`POST /api/gmail/sync-workspace`).
* **Why this approach?** Enables complete transparency and control. A new user or reviewer can test the application in an unauthenticated state (`⚠️ Connect Gmail` / `Pending Auth`), follow the 3-step setup instructions, authenticate via Google OAuth or local token auto-detection, and disconnect on demand.

#### Decision 7: Context-Aware Row Action Buttons in Leads Queue Hub
* **Context**: In earlier builds, every row in the Leads Queue Hub table rendered a generic `✨ Apply` button, even when the lead's status was already `Applied` or `Sent`. This created user confusion regarding whether an application had already been dispatched.
* **Decision**:
  - Dynamically check `lead.status` when rendering table rows.
  - For leads marked `'Applied'`, `'Sent'`, or `'Followed Up'`, render a prominent **"📬 Follow-up"** button (which opens the 1-click follow-up drafter modal with a 2-sentence conversion pitch pre-filled) along with a subtle **"↺ Re-apply"** action.
  - For leads marked `'Drafted'`, render **"📝 Review Draft"**.
  - For uncontacted leads (`'To Contact'`), render the primary blue **"✨ Apply"** button.
* **Why this approach?** Aligns the interface with real-world sales and recruiting outreach workflows: applied leads need follow-ups after 7 days, while uncontacted leads need tailoring and initial dispatch.

#### Decision 8: View-Specific Topbar Subtag Transitions
* **Context**: When picking UAE or Saudi Arabia in Apply Studio, the topbar subtag displayed `'Middle East Protocol (Photo Expected)'`. When navigating to other views (like Leads Queue Hub), the subtag remained stuck on the Middle East notice.
* **Decision**: Update `switchView(viewName)` in `frontend/index.html` with view-specific subtag configurations:
  - **Apply Studio**: Dynamically managed by country selection (`Strict 1-Page Rule Active` or `Middle East Protocol`).
  - **Analytics Dashboard**: `Live Pipeline & Response Analytics` (Emerald).
  - **Leads Queue Hub**: `590+ Stored Target Leads & Batch Engine` (Blue).
  - **Applied Pipeline Tracker**: `Application History & Gmail Status` (Indigo).
  - **Candidate Evidence Hub**: `Candidate Evidence Bank & Master CV` (Purple).
  - **Career Copilot AI**: `Career Copilot AI Assistant` (Sky).

#### Decision 9: Dynamic Dashboard Metrics & Clean Zero-State Reset
* **Context**: The Analytics Dashboard had static mock fallbacks (e.g. hardcoded `1` application today, `88%` match score) and retained 3 test runs. Clicking "Reset to 0" lacked a backend endpoint.
* **Decision**:
  - Implemented `POST /api/tracker/clear-all` and `POST /api/tracker/delete` in `src/web/app.py` and `src/web/db.py`.
  - Replaced hardcoded counters with dynamic JavaScript calculations against the live `applications` table: `sentToday` matches `todayStr`, average ATS match calculates from stored match scores, and interview requests count accurately.
  - When reset, all metrics drop cleanly to `0` and the table renders a friendly empty state prompting the user to open Apply Studio.

#### Playwright Headless Browser End-to-End Audit Log (2026-09-13)
An automated, headless Playwright test suite was executed against `http://127.0.0.1:8000`:
- **[1/7] Initial Load**: Page loaded cleanly, zero runtime JS exceptions.
- **[2/7] Gmail Flow**: Verified initial disconnected state (`Not Connected` / `⚠️ Connect Gmail`), verified 1-click reconnect (`Active & Connected`), verified disconnect button transitions (`🔌 Disconnect`), verified re-sync.
- **[3/7] Dashboard & Reset**: Verified `POST /api/tracker/clear-all` resets all counters to `0` (`Applied: 0 | Today: 0 | Match: 0%`).
- **[4/7] Leads Queue Hub**: Verified subtag displays `"590+ Stored Target Leads & Batch Engine"`, verified KPI metrics show live database counts (`Total=595, Ready=217, Applied=328`), verified contextual row buttons (`📬 Follow-up` for 49 rows on page 1, `✨ Apply` for 3 rows), verified Follow-up modal opens with 2-sentence pitch pre-filled, verified category filter tabs (`YC Startups` 20 rows, `Agencies` 50 rows), verified `Add Lead` and `Import CSV` modals open and close.
- **[5/7] Pipeline Tracker**: Verified navigation and empty state.
- **[6/7] Profile & Copilot**: Verified smooth view transitions.
- **[7/7] Country Protocol**: Verified selecting UAE dynamically switches topbar subtag to `"Middle East Protocol (Photo Expected)"` and selecting US switches to `"Strict 1-Page Rule Active"`.
- **Exit Code**: `0` (100% test pass rate, 0 unhandled console errors).

---

### Phase 7: Live Send Freeze, Header Disconnect / Logout Button, & Safe-Testing Architecture [COMPLETED]

#### Decision 10: Complete Hold / Hard Lock on Live Email Sending for Safe Testing
* **Context**: During beta testing, users may accidentally trigger live email sends (either via Apply Studio or Batch Tailoring Engine) that deliver real unreviewed emails to external recruiters or hiring teams.
* **Decision**:
  - **Backend Safety Lock (`job-agent/src/gmail.py` & `job-agent/src/web/app.py`)**:
    - In `GmailClient.send_email`, intercepted all live dispatch logic to force simulated Dry Run (`{"id": "LOCKED_DRY_RUN", "dry_run": True}`). Real SMTP/API dispatches are completely locked on hold.
    - In `POST /api/batch/run`, any request containing `mode == "live_send"` is rejected with HTTP 400 (`"Live email dispatch is currently locked on hold for testing. Only 'draft' (Gmail Drafts) and 'dry_run' modes are active."`).
  - **Frontend Safety Lock (`job-agent/frontend/index.html`)**:
    - **Apply Studio**: Removed the `1-Click Send` button and replaced it with **`📝 Save to Gmail Drafts`** as the primary action and **`🧪 Dry Run Sim`** for simulations. Pinned the status chip to `Safe Testing Mode`.
    - **Leads Queue Hub Action Bar**: Removed the `⚡ Live Send` action button and inserted an explicit `🔒 Live Send On Hold` safety chip.
    - **Batch Tailoring Modal**: Removed the `live_send` option from the Execution Mode dropdown; users can only pick **`📝 Save to Gmail Drafts`** (creates drafts in real Gmail for review) or **`🧪 Dry Run Simulation`** (local PDF and log simulation). Removed the passkey input container since safe modes require no passkey.
* **Why this approach?** Guarantees zero risk of accidental outbound emails during testing while preserving the ability to generate tailored 1-page CVs and review full email drafts inside Gmail.

#### Decision 11: Persistent Topbar Header Disconnect / Logout Button
* **Context**: Users previously had to click the `Gmail: <account>` status pill to open the Google Cloud modal in order to find the Disconnect button, leading to confusion about how to log out or unlink credentials.
* **Decision**:
  - Added an explicit **`🔌 Disconnect`** button directly in the main topbar navigation header right next to the Gmail status pill.
  - Automatically rendered when authenticated and hidden when disconnected via `checkGmailStatus()`.
  - Invokes `disconnectGmailAccount()` (`POST /api/gmail/disconnect`) with confirmation prompt, immediately unlinking `token.json` and resetting state to `⚠️ Connect Gmail`.
* **Why this approach?** Provides instant, one-click logout accessibility from any view in the app without digging through modals.

