# Job Hunt Workspace

Private, source-controlled workspace for Mohd Hayaat Ali's job hunt operations.

This repository is the portable copy of the local Job Hunt project. It contains
the tracker reconciliation work, Gmail evidence audit outputs, master and tailored
resume variants, agency/direct-employer lead extraction, recovery notes, planning maps,
and the rules future coding agents should follow before they touch anything.

The repository is intentionally private. It contains personal career material,
job-search evidence, recruiter/contact data, and generated resume assets.

## Quick Start

### Option 1: Clone With GitHub CLI

Use this when you are on a machine where GitHub CLI is installed.

```powershell
gh auth login
gh repo clone lordpardonme/job-hunt-workspace-private
cd job-hunt-workspace-private
npm run setup
npm run verify
```

### Option 2: One-Line NPM/NPX Bootstrap

Use this when you want a coding agent or a fresh machine to pull the private
workspace from GitHub with one command.

```powershell
npx github:lordpardonme/job-hunt-workspace-private job-hunt-workspace-private
```

Because the repository is private, the machine must already have GitHub access
for `lordpardonme/job-hunt-workspace-private`. If the command cannot authenticate,
run:

```powershell
gh auth login
```

Then retry the `npx` command.

### After Setup

Run these commands inside the cloned repository:

```powershell
npm run setup
npm run verify
npm run agent:context
```

`npm run setup` confirms the workspace structure and prints the next safe steps.
`npm run verify` checks required project files exist.
`npm run agent:context` prints a short operating brief for any coding agent.

## What This Repo Contains

### `Job Hunt/`

Main job-hunt working folder.

Important contents:

- `Job Hunt/AGENTS.md`: complete handoff document and operating rules for AI coding agents.
- `Job Hunt/resumes/`: master & tailored resumes, ATS reports, email drafts, PDF outputs,
  recovery material, and resume-generation scripts.
  - **Master Product Designer CV:** `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` (`master-product-designer-cv.md`)
  - **Master Creative CV (Video, Photo, Motion, Graphic Design):** `Mohd_Hayaat_Ali_Master_Creative_CV.pdf` (`master-creative-cv.md`)
  - **Brand-Aware PDF Renderer:** `build_pdf_from_md.py` (supports `--brand <color>`, `--creative`, `--corporate`, and hyperlink formatting).
- `Job Hunt/sheet-export.csv`: local tracker export snapshot.
- `Job Hunt/.agents/skills/`: local skills used for resume tailoring and job-hunt work.

### `job-agent/`

Python 3.13 CLI application agent (`main.py`) wrapping Gmail API, Google Sheets API, ReportLab PDF rendering, and Jinja2 templating.

### `reconciled-tracker-build/`

Tracker reconciliation outputs and scripts.

Important contents:

- `current_tracker.xlsx`: local workbook aligned with the latest reconciliation.
- `gmail-sent-audit-2026-07-28.csv`: latest Gmail sent-mail audit created from
  live Gmail evidence.
- `master_job_tracker_reconciled.xlsx`: reconciled workbook snapshot.
- `*.tsv`: tab-level exports from the reconciled tracker.
- `reconcile_tracker.py` and related scripts: local rebuild helpers.

The live Google Sheet (`1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI`) remains the authority when live state may have changed.

### `drive-extraction/`

OCR/image extraction and lead categorization material from Drive screenshots.

Important contents:

- `images/`: extracted screenshot images.
- `ocr/`: OCR text files per screenshot.
- `*-proposed.csv` and `*-preview.csv`: proposed tracker rows and update previews.
- JavaScript helper scripts used during extraction and categorization.

### `.planning/`

Architecture, structure, testing, and codebase-map notes for future agents.

### `References and Resources/`

Reference material used for resumes and job-hunt positioning.

## Live Systems

The project has three important live systems:

- Gmail account (`hayaat0806@gmail.com`) used for sent-mail evidence and outreach.
- Google Sheet: `Master Job Tracker` (`1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI`). Features live dynamic Dashboard, native color-coded status dropdowns, and automated sent-mail sync.
- GitHub private repository: `lordpardonme/job-hunt-workspace-private`.

Rules:

- Gmail is used to verify what was actually sent.
- The live Google Sheet is the source of truth for tracker state.
- The GitHub repo is the portable private backup and collaboration handoff.

## Latest Reconciliation Snapshot

As of July 30, 2026:

- **Live Google Sheet Cleaned & Deduplicated:**
  - `Master Job Tracker`: 312 clean, unique lead rows.
  - `Agencies`: 72 unique agency rows (34 marked `Applied`, 34 `To Contact`).
  - `Direct Employers`: 217 unique direct employer rows (62 `Applied`, 145 `To Contact`).
  - `Sent By Me`: 203 logged outbound application entries.
- **Outbound Sends:**
  - July 30, 2026 batch: 11 application emails sent via Gmail API and logged to live Sheet.
- **Master Resumes Registered:**
  - Product & UI/UX Track: `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf`
  - Creative Track (Video, Photo, Motion, Graphic Design): `Mohd_Hayaat_Ali_Master_Creative_CV.pdf` (1-page A4 PDF featuring 10+ yrs photo/video, IITs/IIMs/NITs/DU festivals, and high-profile artist shoots for Travis Scott, Akon, etc.).

## Agent Operating Model

Any coding agent working here should start with:

```powershell
npm run agent:context
npm run verify
```

Then read:

- `AGENTS.md` — start here; the complete agent handoff document
- `POLICY.md`
- `Job Hunt/AGENTS.md`

Do not skip these files. They define the approval boundaries, tracker rules,
Gmail rules, and resume truthfulness rules.

## Safety Rules

These are the non-negotiable rules for this workspace:

1. Do not send emails without explicit approval.
2. Do not update the live Google Sheet without grounding the exact rows/ranges.
3. Do not trust stale local CSVs when live Gmail or live Sheets can verify state.
4. Do not invent experience, metrics, companies, projects, or domain expertise.
5. Do not delete user files unless explicitly asked and the target is verified.
6. Do not commit secrets, tokens, private `.env` files, or local virtualenvs.
7. Keep agency outreach one target at a time unless the user explicitly changes
   the workflow.
8. Treat `pause`, `do not send`, and `wait` as hard stops.

## Typical Workflows

### Resume Tailoring

1. Identify the exact target role and company.
2. Select the relevant track master (Product UI/UX vs Creative/Video/Photo).
3. Read existing evidence in `Job Hunt/resumes/` and `career-evidence-bank.md`.
4. Create or update target-specific Markdown (`<slug>-resume.md`).
5. Render PDF with brand colors: `.venv/Scripts/python.exe "Job Hunt/resumes/build_pdf_from_md.py" <slug>-resume.md <Out>.pdf "<Title>" --brand <color>`.
6. Present packet and do not send anything until the user explicitly approves.

### Tracker Reconciliation

1. Check Gmail sent mail for actual evidence.
2. Read live sheet metadata and bounded ranges.
3. Match by email, company, subject, and Gmail message/thread IDs.
4. Update the live sheet only after row identity is clear.
5. Mirror important outputs into local workbook/CSV files.

### GitHub Backup

1. Keep the repo private.
2. Avoid committing local dependency caches.
3. Commit intentional changes with clear messages.
4. Push to `main` only for stable workspace snapshots.

## NPM Commands

```powershell
npm run setup
npm run verify
npm run agent:context
```

### `npm run setup`

Checks the local workspace and prints next steps.

### `npm run verify`

Validates that core folders and files exist.

### `npm run agent:context`

Prints a short operating brief for a coding agent.

## Rebuilding The Local Working State

After cloning:

```powershell
cd job-hunt-workspace-private
npm run verify
```

If a future task needs Python dependencies, use the active machine's Python
runtime rather than committing a virtualenv.

## Notes For Future Agents

This project is not a generic software product. It is a live job-hunt operating
workspace. The value is in correctness, evidence, and careful state management.

Before doing any outreach or tracker update:

- Confirm the target.
- Confirm the live sheet row.
- Confirm Gmail evidence.
- Present the packet or change summary.
- Wait for approval when the action changes external state.
