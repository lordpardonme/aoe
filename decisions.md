# Architectural Decisions & Codebase Execution Flow

**Project:** AOE (Autonomous Outreach Engine) (`G:\job-hunt-app`)  
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

### Decision 11: Munder Difflin Multi-Agent Hive Orchestration & MCP Protocol Server
* **Context:** Research into [`munder-difflin`](https://github.com/chaitanyagiri/munder-difflin.git) revealed a local-first multi-agent architecture where role-specialized agents coordinate through a shared ledger and circuit breakers. AOE previously ran application tailoring through a single sequential pipeline. Additionally, external desktop agent harnesses (Munder Difflin, Claude Code, Antigravity `agy`) need a standardized way to drive AOE workflows.
* **Decision:**
  1. Implement an autonomous multi-agent Hive coordinator (`src/hive.py`) featuring four specialized sub-agents:
     - **`ScoutAgent`**: Analyzes JD text/URL, matches candidate taxonomy, calculates fit score.
     - **`ResumeArchitectAgent`**: Tailors bullet points to high-impact achievements and enforces the strict 1-page ReportLab layout.
     - **`CopywriterAgent`**: Crafts punchy cold outreach email and 7-day follow-up conversion copy.
     - **`QualityReviewerAgent`**: Runs First-Reader attention scoring (0-100), audits WCAG AA contrast compliance, and enforces word count budgets.
     - **`HiveCoordinator`**: Supervisor ("God Agent") managing task ledgers and safety circuit breakers (`steer` -> `constrain` -> `stop`).
  2. Implement an MCP (Model Context Protocol) JSON-RPC 2.0 stdio server (`src/mcp_server.py`) exposing AOE tools (`aoe_run_hive_pipeline`, `aoe_list_leads`, `aoe_get_stats`, `aoe_scan_recruiter_replies`) to external desktop orchestrators including Munder Difflin and Antigravity.
  3. Wire `/api/hive/orchestrate` and `/api/hive/status` into the FastAPI web application (`src/web/app.py`).
* **Why this approach?** Unlocks true multi-agent collaboration with audit trails and circuit breakers inside AOE, while enabling plug-and-play integration with Munder Difflin and other MCP-compliant developer tools.

### Decision 12: 100% Authentic Munder Difflin 2D Retro Architecture & LimeZu Pixel Art Floor in Staging Orbit
* **Context:** User requested extracting and implementing the authentic design language, graphics, and multi-agent interaction model from `munder-difflin` (`https://github.com/chaitanyagiri/munder-difflin.git`) in staging (`/staging_office.html`). Early prototypes used canvas primitives and had Z-ordering bugs where monitors were occluding character faces and bodies.
* **Decision:**
  1. **TiledMap & Layer Compositing:** Extract and pre-rasterize the authentic LimeZu RPG Modern Office tileset (`interiors.png`, `office-tileset.png`, `a5-office-floors-walls.png`) and Tiled map (`office.tmj`) into a single full composite `office_floor_full.png` (1088x704). Following Munder Difflin's container hierarchy (`TiledMapRenderer.ts`), all tile layers render first, and characters render on top.
  2. **Seated Character Sprites & Desks:** Station all 15 authentic Scranton characters (Michael, Jim, Dwight, Pam, Ryan, Angela, Andy, Kevin, Oscar, Stanley, Phyllis, Kelly, Meredith, Toby, Creed) on their exact stools. Implement `PortraitArt.paintSeatedSprite` which crops the bottom 8px (legs under desk) and sits the bust and torso cleanly on the chair without any occlusion.
  3. **Munder Difflin Design System:** Implement the exact design tokens (`--cth-cream-50`, `--cth-cream-100`, `--cth-paper-100`, `--cth-ink-900`, `--cth-lemon`, `--cth-sky`, `--cth-coral`), `PixelPanel` styling with 1px inset hairlines, `PixelButton` retro buttons, `PixelBadge` with square status pips, and 220x78px `AgentCard` dock items with token gauges and Michael's golden `BOSS` surface.
  4. **Observable 20s Swarm Simulation:** Wire an observable multi-agent swarm handoff with overhead speech bubbles, flying paper envelopes, Xerox copier paper ejection with blinking green LED, animated CRT monitor desktops (`DeskScreen` scan lines), and live terminal logs.
* **Why this approach?** Delivers 100% authentic visual parity with Munder Difflin while keeping staging completely isolated from production.

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
- **Agent Handoff Guide**: Updated `AOE_HANDOFF.md` with complete API maps, UI specifications, verification commands, and tech stack details.
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

---

### Phase 8: Multi-Environment Orbit Architecture (UAT, Staging, Production) [COMPLETED]

#### Decision 12: Independent Database Isolation per Orbit
* **Context**: Testing experimental scraping runs and mock records risked corrupting production application histories.
* **Decision**:
  - Implemented dynamic database routing in `job-agent/src/web/db.py` via `get_db_path()` and `DynamicPathProxy`.
  - Configured three distinct orbits:
    - **UAT** (Port 8001, `jobhunt_uat.db`): Isolated sandbox for synthetic tests.
    - **Staging** (Port 8002, `jobhunt_staging.db`): Pre-production testing and dry-run validation.
    - **Production** (Port 8000, `jobhunt.db`): Verified leads and authenticated Gmail staging.
  - Created `manage_env.py` CLI supporting `status`, `switch`, `test`, and `promote`.
  - Integrated dynamic topbar environment badge in `frontend/index.html`.

---

### Phase 9: Brand Renaming to AOE, GitHub Rulesets & Repository Hardening [COMPLETED]

#### Decision 13: Renaming from CareerHero Studio to AOE (Autonomous Outreach Engine)
* **Context**: The project has evolved from a single candidate assistant into an autonomous outreach engine spanning multi-board scraping, email deliverability verification, ReportLab PDF layout budgeting, and Gmail API integration.
* **Decision**:
  - Renamed the product and repository to **AOE (Autonomous Outreach Engine)** (`lordpardonme/aoe`).
  - Systematically rebranded all backend services, docstrings, logger names, frontend titles, launcher scripts, and documentation across 16 files (35+ occurrences replaced, 0 residual references).
  - Renamed handoff documentation to `AOE_HANDOFF.md`.

#### Decision 14: Public Repository Lockdown & GitHub Rulesets
* **Context**: Upon making the repository public, the codebase must be protected against unauthorized modifications, accidental force pushes, and broken releases while encouraging community contributions via pull requests.
* **Decision**:
  - Configured active GitHub Rulesets for `main-protection`, `staging-protection`, and `release-tag-protection`:
    - **`main`**: Blocks deletion, blocks force-push, requires pull request with code owner review, linear history.
    - **`staging`**: Blocks deletion, blocks force-push, requires pull request.
    - **`v*.*.*` tags**: Immutable release tags, blocks deletion and modification.
  - Enforced deployment branch policies for `UAT` (uat branch), `Staging` (staging branch), and `Production` (main branch).
  - Added repository variables (`APP_ENV`, `DRY_RUN`, `PYTHON_VERSION`) and secret placeholders (`LLM_API_KEY`, `GMAIL_CREDENTIALS`) for both GitHub Actions and GitHub Codespaces.
  - Authored complete community suite: `LICENSE`, `CONTRIBUTING.md`, `SECURITY.md`, `CODE_OF_CONDUCT.md`, `.github/CODEOWNERS`, `.github/pull_request_template.md`, and issue templates for bug reports and feature requests.
  - Created `.devcontainer/devcontainer.json` for 1-click GitHub Codespaces development.

#### Decision 15: Transition to Strict Proprietary & Source-Available Anti-Copy License
* **Context**: Permissive open-source licenses (like MIT) permit unrestricted copying, cloning, repackaging, commercial exploitation, and closed-source re-hosting of the application. The project owner requires strict legal protections preventing theft, copying, or SaaS deployment of AOE.
* **Decision**:
  - Replaced the permissive MIT license with a **Strict Proprietary & Source-Available License (All Rights Reserved — Strict No-Copy & No-Derivatives)**.
  - Core terms:
    - **No Copying or Mirroring**: Explicit prohibition on duplicating or hosting the codebase without express written consent.
    - **No Derivative Works**: Prohibits building derivative tools, scrapers, or layout clones based on AOE.
    - **No Commercial / SaaS Use**: Completely forbids multi-tenant or commercial exploitation.
    - **Anti-AI Training**: Explicitly blocks automated ingestion into LLM or ML training datasets.
    - **Evaluation Only**: Source is viewable solely for personal technical inspection and security auditing.
    - **Contributor Assignment**: In `CONTRIBUTING.md`, all community contributions are legally assigned to `@lordpardonme`.
---

### Phase 10: 2D Multi-Agent Operations Floor & Staging Environment Isolation [COMPLETED]

#### Decision 16: Strict Staging/UAT Orbit Isolation for 2D Operations Floor
* **Context**: Inspired by Munder-Difflin, the user requested a retro 2D pixel-art virtual office floor where multiple specialized agents occupy desks and communicate via animated flying envelopes. The user specifically required that this new design be deployed exclusively to UAT/Staging and not interfere with or pollute the live Production orbit.
* **Decision**:
  - Keep Production (`APP_ENV=production`, port 8000) completely untouched and stable.
  - Dynamically gate the Operations Floor in `frontend/index.html` via `checkAppEnvironment()`:
    - In Staging (`APP_ENV=staging`, port 8002) and UAT (`APP_ENV=uat`, port 8001), reveal the `🏢 Operations Floor [STAGING]` top tab, sidebar nav item, and `#view-office` section.
    - In Production (`APP_ENV=production`), hide `tab-office` and `nav-office` completely (`classList.add('hidden')`).
  - Create a dedicated standalone staging review page: `frontend/staging_office.html` at `http://127.0.0.1:8002/staging_office.html` for focused evaluation.
* **Why this approach?** Guarantees zero risk to the production application while providing an interactive, full-fidelity testing sandbox in Staging and UAT.

#### Decision 17: UI/UX Pro Max 2D Canvas Engine with Parabolic Envelope Handoffs & SSE Command Center
* **Context**: Static tables fail to visualize the stigmergic coordination between autonomous agents during resume tailoring and outreach generation.
* **Decision**:
  - Implement native HTML5 Canvas 2D engine (`frontend/js/office_canvas.js`) operating at 60 FPS with `image-rendering: pixelated`:
    - 6 dedicated stations: Supervisor Corner Office (Michael), Scout Radar Station, Resume Architect Drafting Table, Copywriter Vintage Typewriter, Quality Reviewer Inspection Station, and Breakroom Recruiter Radar (coffee steam and Gmail listener).
    - Living character animations: idle breathing, rapid typing bobs, glowing CRT monitors, speech bubbles.
    - Parabolic flying envelope handoffs with golden sparkle particle dust between desks.
  - Build interactive Command Center (`frontend/js/command_center.js`):
    - Real-time Server-Sent Events (SSE) listener (`GET /api/hive/stream`).
    - Live terminal stream with ANSI color-coding, pipeline monitor, tasks ledger, agent memory, and queue list.
    - Interactive Supervisor chat (`POST /api/hive/chat`) with natural language commands (`"tailor"`, `"scan"`, `"status"`).
    - Bottom Agent Roster with color-coded badges and status pills.
  - Adhere to `ui-ux-pro-max` standards: WCAG AA contrast (4.5:1 on dark surfaces), touch targets >= 44px, 150-300ms transitions, and responsive drawers.

---

### Phase 11: Authentic Scranton Cast & Munder Difflin Pixel-Art Replication [COMPLETED]

#### Decision 18: Total Purge of Generic Roles & High-Fidelity Munder Difflin 2D Canvas Engine
* **Context**: Initial prototypes used generic role labels ("Boss", "Scout", "Architecture", "Copywriter", "Reviewer") across canvas desk plaques, roster cards, and terminal logs. The user mandated complete alignment with the authentic Dunder Mifflin Scranton cast from *The Office* as depicted in the reference screenshot `media_1789400136267.png`, including Andy Bernard, retro desktop window styling, authentic bullpen desk arrangements, and a continuous 10–15 minute automated play-testing loop.
* **Decision**:
  1. **Purged All Generic Titles**: Systematically replaced all occurrences of "Supervisor", "Scout", "Resume Architect", "Copywriter", "Reviewer", and "Auditor" with canonical cast identities:
     - **Michael Scott**: Regional Manager (Supervision, Mission Delegation, Banter)
     - **Jim Halpert**: Sales / Lead Scout (Live Public Job Board Querying & Scraping)
     - **Dwight Schrute**: Assistant to the Regional Manager / 1-Page Resume Architect (Bahnschrift Layout, Jell-O stapler, Bobblehead, Xerox Copier)
     - **Pam Beesly**: Reception & Candidate Evidence Vault (Intake Counter, Portfolio Assets)
     - **Ryan Howard**: Temp / Cold Outreach Studio (3-Sentence Hook Copywriting)
     - **Angela Martin**: Accounting / Quality & Compliance Gate (First-Reader 100/100 scoring, WCAG AA Audit, Official Stamp)
     - **Andy Bernard**: Regional Sales & Network Outreach (Cornell '95 A Cappella / Acoustic Pitch Studio)
     - **Toby Flenderson**: Annex HR & Recruiter Radar (Gmail Inbound Response Scanner)
  2. **High-Fidelity Munder Difflin Canvas Styling (`frontend/js/office_canvas.js`)**:
     - Warm parchment outer window frame (`#dfd9ce`) with authentic retro desktop title bar (`Munder Difflin` with `File Edit View Window` menu and `_ □ ✕` buttons).
     - Sage-green linoleum floor (`#9fb39b`) with 26px grid lines and `#738676` diamond cross dots.
     - Michael's Executive Corner Office with hardwood parquet planks (`#c4975f`), Scranton calendar, wall clock, World's Best Boss mug, Dundie trophy, and live `awaiting` speech bubble.
     - Scranton Conference Room with two exterior double windows, white mullions, whiteboard, mahogany table, 8 purple conference chairs, and ficus plants.
     - Storage Archive partition with 4 stacked cardboard archive boxes.
     - 10 Bullpen desks with retro CRT monitors, honey/orange swivel chairs, and bespoke character props.
     - Breakroom with water cooler blue bubbles, kitchenette coffee steam, and animated green Xerox copier.
     - Solid brass desk nameplates with screw rivets for all 8 characters.
  3. **Continuous 10–15 Minute Play-Test Verification (`scratch/comprehensive_scranton_playtest.py`)**:
     - Automated headless Playwright script running continuous multi-stage cycles for 12 minutes.
     - Exercises all 8 cast stations, live job querying, 1-page PDF compilation, pitch generation, compliance auditing, tab switching, and 20-second observable multi-agent swarm handoffs.
     - Asserts 0 console errors and 0 page errors throughout the entire endurance run.


#### Decision 19: Ingestion of Full Munder Difflin Design Language, Graphic Assets, and Procedural Pixel-Art Engine
* **Context**: The user instructed to pull the whole design language, graphics, and visual assets from `https://github.com/chaitanyagiri/munder-difflin.git` into the Scranton staging operations floor.
* **Decision**:
  1. **Graphic Tilesets & Maps**: Cloned repository and migrated authentic 32×32 tilesets (`interiors.png`, `office-tileset.png`, `a5-office-floors-walls.png`, and `office.tmj`) into `job-agent/frontend/assets/tilesets/` and `job-agent/frontend/assets/maps/` with complete copyright attribution to LimeZu (`LIMEZUASSETS-LICENSE.txt`, `ATTRIBUTION.md`).
  2. **Comprehensive Design Tokens (`frontend/css/munder_difflin.css`)**:
     - Ported complete token palette: `--cth-cream-*` (surfaces), `--cth-ink-*` (text & borders), `--cth-status-*` (idle, thinking, working, blocked, success), character accents (`coral`, `mint`, `sky`, `lemon`, `lilac`, `peach`).
     - Implemented full Light/Dark mode themes (`:root[data-cth-theme='dark']`) with instant theme switcher.
     - Hard offset drop shadows (`3px 3px 0 rgba(26,19,32,0.14)`) and Google Fonts (`Press Start 2P`, `Inter`, `JetBrains Mono`).
     - Canonical component primitives: `.cth-panel`, `.cth-btn`, `.cth-badge`, `.cth-agent-card`, `.cth-gauge`, and `.cth-tab-strip`.
  3. **Procedural Pixel-Art Bust & Sprite Engine (`frontend/js/portrait_art.js`)**:
     - Ported complete procedural generation engine (`portraitArt.ts`) creating exact 18×28 pixel bust portraits and 18×32 scene sprites for all 15 canonical characters: *Michael, Jim, Pam, Dwight, Kevin, Angela, Oscar, Stanley, Phyllis, Andy, Kelly, Ryan, Toby, Creed, and Meredith*.
     - Generates hairstyles, glasses, ties, cardigans, facial hair, lashes, and multi-tone shading via procedural Uint8ClampedArray pixel buffers.
     - Implemented in-memory offscreen canvas caching (`spriteCanvasCache`) for high-performance 60 FPS drawing in `office_canvas.js`.
  4. **Canonical 220×78 px Docked Agent Cards (`frontend/js/command_center.js`)**:
     - Docked cards strictly conform to Munder Difflin geometry (220×78 px).
     - Michael Scott features the distinctive `is-god` tinted lemon surface, inset gold border, and `BOSS` badge.
     - All cards render real-time procedural busts, uppercase character names in `Press Start 2P`, live status chips, and 8-segment context memory gauges.
  5. **Automated Headless Playwright Verification (`scratch/verify_munder_difflin_design.py`)**:
     - Verified all 15 character recipes, 220×78 px card geometry, procedural canvas pixel data, theme toggling, tab strip navigation, and swarm handoffs with 0 console and 0 page errors.

#### Decision 20: User-Choice Task Assignment Engine & Dual Roster Filtering (Active Crew vs. Full Scranton Cast)
* **Context**: Stationing all 15 authentic Scranton branch characters provided full cast art and canonical desk layout, but displaying all 15 in the dock simultaneously created visual noise, and running only fixed 20s swarm scripts limited user agency. The user asked: *"then why are we using 15 of them? shouldnt we give user a choice to assign task?"*.
* **Decision**:
  1. **Dual Roster Architecture (Talent Pool vs. Active Squad)**:
     - Retained all 15 characters on the 2D floor map as the available Scranton Branch Talent Pool.
     - Added a dock view toggle: **`All Staff (15)`** to browse the full branch, and **`Active Crew`** which filters the bottom dock strip to only display agents currently working on tasks (or with assigned missions) plus Michael Scott (`BOSS`), mirroring Munder Difflin's clean active process strip.
  2. **Universal "Assign Task" Modal (`#modal-assign-task`)**:
     - Accessible from: Header **[⚡ Assign Task]**, Selected Agent Profile **[⚡ Assign Task to {Name}]**, Dock **[➕ Assign Task]**, or clicking any agent's desk on the 2D floor.
     - Features an interactive 15-character picker with 8-bit procedural bust canvases.
     - Selecting any character updates the spotlight card, canonical quotes, and populates 3 one-click preset task templates matching their canonical abilities:
       - *Jim*: Scout Arbeitnow / Remote tech feeds, extract core keywords.
       - *Dwight*: Enforce militant 1-page Bahnschrift PDF budget & trigger green Xerox copier print.
       - *Andy*: Cornell alumni warm networking outreach & memorable referral requests.
       - *Ryan*: Shubham Saboo 3-sentence high-retention outreach hook.
       - *Angela*: 100/100 WCAG AA contrast & 30-second scan audit.
       - *Kelly*: 7-day ghosting recruiter follow-up pitch & interview thank-you notes.
       - *Oscar*: Salary band percentiles & fact-grounded counter-offer negotiation math.
       - *Stanley*: Direct no-fluff application dispatch (Crossword mode).
       - *Toby*: Scan Gmail radar for interview invites & calendar links.
       - *Creed*: Red-team QA & portfolio easter-egg hooks.
       - *Michael*: Full branch swarm delegation brief.
       - *Pam, Kevin, Phyllis, Meredith*: Evidence vault intake, application accounting, warm introductions, unconventional outreach.
     - Provides a free-form `Custom Directive / Prompt` textarea allowing the user to assign *any* custom prompt, company, or role to any chosen character.
  3. **Observable Floor & Ledger Reaction**:
     - The assigned agent transitions to `status = 'working'`, desk CRT screen animates with code lines, and a custom speech bubble appears above their head on the 2D canvas.
     - Dwight triggers the animated green Xerox copy machine with flying paper.
     - The task is tracked live in the **📋 Tasks Ledger** (`#cc-dynamic-tasks-list`) with progress bar and timestamp, and color-logged in the **💻 Terminal**.
     - Tasks auto-complete with verified outputs and update the agent's completed stats.
  4. **Automated Verification (`scratch/test_task_assignment_engine.py`)**:
     - Verified modal opening, character picker, preset filling, custom prompt dispatch, Andy speech bubble, Dwight copier printing, active crew filtering, and tasks ledger completion with 0 console and 0 page errors.

#### Decision 21: Multi-Provider AI Engines Hub & Per-Task Custom Model Assignment
* **Context**: The user asked: *"what is goal for this? i mean what problem is this solving? i mean can we do it better, give user option to add custom models and providers"*. While AOE backend supported multi-provider execution (`src/llm/adapters.py`), the Staging Orbit lacked a dedicated Munder Difflin-styled modal to inspect, test latency, and persist custom LLM providers and model slugs, as well as the ability to assign individual tasks to specific model engines.
* **Decision**:
  1. **AI Engines & Custom Model Hub Modal (`#modal-ai-engines`)**:
     - Built authentic retro Munder Difflin modal accessible via the header `[⚙️ AI Engines]` button.
     - Supports 6 primary provider runtimes:
       - **Google Gemini**: Defaults to `gemini-2.0-flash` (with `gemini-1.5-pro` & `gemini-2.0-flash-lite` chips).
       - **OpenAI**: Defaults to `gpt-4o-mini` (with `gpt-4o`, `o3-mini`, `gpt-4-turbo` chips).
       - **Anthropic Claude**: Defaults to `claude-3-5-sonnet-20241022` (with `claude-3-7-sonnet-20250219`, `claude-3-5-haiku-20241022` chips).
       - **Groq Fast**: Defaults to `llama-3.3-70b-versatile` (with `deepseek-r1-distill-llama-70b`, `mixtral-8x7b-32768` chips).
       - **Ollama (Local Offline)**: Defaults to `llama3.2` on `http://localhost:11434` (with `qwen2.5-coder:32b`, `deepseek-r1:14b` chips).
       - **OpenRouter / Custom (vLLM / LM Studio)**: Defaults to `deepseek/deepseek-r1` on `https://openrouter.ai/api/v1` (with `anthropic/claude-3.7-sonnet`, `meta-llama/llama-3.3-70b-instruct`).
     - Includes model slug input with reactive quick-pick chips, password show/hide key toggle, and custom base URL configuration.
     - Features live **`[⚡ Test Connection]`** probe sending a test prompt to `POST /api/test/llm` and rendering real-time response latency and diagnostic badges.
     - Features **`[💾 Save Configuration]`** calling `POST /api/config` to persist the chosen provider, key, model, and base URL directly to local `.env`.
  2. **Per-Task Engine & Model Selection (`#modal-assign-task`)**:
     - Updated Step 6 in the Universal Task Assignment modal with `#task-model-select`, letting users override the default engine per task dispatch (e.g. run Dwight with Claude 3.7 Sonnet, run Jim with Groq Llama 3.3 70B, or run Michael with local Ollama).
     - Captured engine model in the task ledger (`#cc-dynamic-tasks-list`) with dedicated model badge (e.g. `CLAUDE`, `GEMINI`, `GROQ`) and logged to the Scranton Terminal.
  3. **Automated Verification (`scratch/test_ai_engines_modal.py`)**:
     - Verified modal launch, provider switching (Gemini → Claude → Ollama → Gemini), preset chip selection, show/hide key toggle, configuration saving, per-task custom model dispatch to Dwight, task ledger badge, and terminal logging with 0 console errors and 0 page errors.
     - Captured artifacts: `scranton_ai_engines_modal.png` and `scranton_custom_model_dispatched.png`.

#### Decision 22: Interactive Task Deliverable & Output Inspector Modal & Output Closure
* **Context**: The user identified a critical UX completion gap: *"After assigning and doing everything, what happens? There is no end thing. I don't see anywhere if I assign a task to Toby and ask him to do something. Then if I dispatch the key, it says task completed. So where did this go? If I assign something to Jim, I assign it to Jim, I scout remote design jobs... And plus, the UI, the name is long, it doesn't show anything. If I 10 minutes coffee pitch, fast dispatch, and he started draft, 10-minute coffee chat, task completed. So where is this task getting completed? What is the end result? Where is this screen where I can see it?"*
* **Decision**:
  1. **Task Deliverable & Output Inspector Modal (`#modal-task-deliverable`)**:
     - Built authentic retro Munder Difflin modal in `staging_office.html` with character bust canvas, role/department tags, engine model badge, timestamp, and context-tailored deliverable body.
     - **Email Pitch (Andy, Ryan, Kelly, Stanley, Michael)**: Full subject line and outreach body with word count & reading time badge (`78 words • 20s read`), 1-click **`[📋 Copy Pitch to Clipboard]`**, and **`[📬 Push to Gmail Drafts]`** integration.
     - **1-Page Bahnschrift PDF (Dwight)**: Mathematical single-page budget gauge displaying Line Capacity (`46 / 50 lines`), Page Overflow (`0.00 mm`), Typography (`Bahnschrift DIN 1451`), Contrast Ratio (`7.2:1 WCAG AA`), tailored skill taxonomy chips, summary preview, **`[📄 Download 1-Page PDF]`**, and **`[🖨️ Print on Copier]`** button that triggers the physical green Xerox machine.
     - **Job Scout & Keywords (Jim)**: Matched keyword taxonomy, 3 curated live feed matches, and **`[✨ Pass to Dwight to Tailor 1-Page CV]`** action handoff.
     - **Quality Gate Audit (Angela)**: 100/100 audit scorecard checking WCAG AA contrast, single-page layout budget, ATS machine parseability, and typo continuity, with **`[🛡️ Apply Accounting Stamp]`**.
     - **Inbound Radar Scanner (Toby)**: Scanned thread telemetry, interview invitation counts, recruiter acknowledgements, and parsed intent.
     - **Salary Comp & Negotiation (Oscar)**: 25th-90th percentile compensation benchmarks and fact-grounded counter-offer negotiation scripts.
  2. **Automatic Real-Time Deliverable Popup**:
     - Updated `assignTaskToAgent()` so when any task finishes execution (after 3.6s), it automatically pops up `#modal-task-deliverable` directly in front of the user, providing immediate visual and tactical closure.
  3. **Tasks Ledger Card Fixes & Persistent Deliverable Access**:
     - Eliminated single-line truncation (`white-space: nowrap; overflow: hidden; text-overflow: ellipsis`) on task titles in `#cc-dynamic-tasks-list`. Titles now wrap cleanly with full visibility.
     - Added prominent **`[📦 View Deliverable ↗]`** buttons to all completed task cards (including pre-loaded sample tasks `t1`, `t2`, `t3`), allowing users to inspect or copy outputs at any time.
  4. **Automated Verification (`scratch/test_task_deliverables.py`)**:
     - Verified modal rendering, sample tasks inspection, copy-to-clipboard, auto-popup on task dispatch and completion, and 0 console/page errors.
     - Verified artifacts: `scranton_dwight_deliverable_modal.png`, `scranton_andy_deliverable_modal.png`, and `scranton_tasks_with_deliverables_overview.png`.
