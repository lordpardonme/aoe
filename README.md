# Job Hunt Workspace

Private, source-controlled workspace for Mohd Hayaat Ali's job hunt operations.

This repository is the portable copy of the local Job Hunt project. It contains
the tracker reconciliation work, Gmail evidence audit outputs, resume variants,
agency/direct-employer lead extraction, recovery notes, planning maps, and the
rules future coding agents should follow before they touch anything.

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

- `Job Hunt/AGENTS.md`: local agent operating rules from the original workspace.
- `Job Hunt/resumes/`: tailored resumes, ATS reports, email drafts, PDF outputs,
  recovery material, and resume-generation scripts.
- `Job Hunt/sheet-export.csv`: local tracker export snapshot.
- `Job Hunt/.agents/skills/`: local skills used for resume tailoring and
  job-hunt work.

The original nested Git metadata and local Python virtualenv are not tracked.
They are machine-local implementation detail, not portable source.

### `reconciled-tracker-build/`

Tracker reconciliation outputs and scripts.

Important contents:

- `current_tracker.xlsx`: local workbook aligned with the latest reconciliation.
- `gmail-sent-audit-2026-07-06.csv`: latest Gmail sent-mail audit created from
  live Gmail evidence.
- `master_job_tracker_reconciled.xlsx`: reconciled workbook snapshot.
- `*.tsv`: tab-level exports from the reconciled tracker.
- `reconcile_tracker.py` and related scripts: local rebuild helpers.

The live Google Sheet remains the authority when live state may have changed.
Local files are a backup and working copy.

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

- Gmail account used for sent-mail evidence.
- Google Sheet: `Master Job Tracker - Reconciled`.
- GitHub private repository: `lordpardonme/job-hunt-workspace-private`.

Rules:

- Gmail is used to verify what was actually sent.
- The live Google Sheet is the source of truth for tracker state.
- The GitHub repo is the portable private backup and collaboration handoff.

## Latest Reconciliation Snapshot

As of July 6, 2026:

- Gmail sent mail was checked.
- Latest sent application found: Nagarro, sent July 4, 2026.
- No sent Gmail match was found for:
  - `Orchard Lab 47`
  - `Orchard Latch 47`
  - `ORCHIDLAB47`
  - `ORCHID-LATCH-47`
  - `Orchid Lab`
  - `Orchid Latch`
- Live sheet tab `Gmail Sent Audit 2026-07-06` was created.
- Local audit CSV was written to
  `reconciled-tracker-build/gmail-sent-audit-2026-07-06.csv`.
- Recent Gmail-confirmed rows were added or updated in `Master Leads`.

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

1. Identify the exact target.
2. Read existing evidence in `Job Hunt/resumes/`.
3. Reuse real shipped-work evidence.
4. Create or update target-specific Markdown.
5. Generate ATS notes and PDF only when useful.
6. Do not send anything until the user explicitly approves.

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

## Private NPM/NPX Bootstrap

This repository defines a package binary named `job-hunt-workspace`.

From a fresh machine:

```powershell
npx github:lordpardonme/job-hunt-workspace-private job-hunt-workspace-private
```

What it does:

1. Uses Git to clone `https://github.com/lordpardonme/job-hunt-workspace-private.git`.
2. Creates the target folder if needed.
3. Runs the local verification script.
4. Prints the next commands for the coding agent.

It does not publish the project to the public npm registry.

## Rebuilding The Local Working State

After cloning:

```powershell
cd job-hunt-workspace-private
npm run verify
```

If a future task needs Python dependencies, use the active machine's Python
runtime rather than committing a virtualenv. The prior virtualenv was excluded
on purpose.

## Notes For Future Agents

This project is not a generic software product. It is a live job-hunt operating
workspace. The value is in correctness, evidence, and careful state management.

Before doing any outreach or tracker update:

- Confirm the target.
- Confirm the live sheet row.
- Confirm Gmail evidence.
- Present the packet or change summary.
- Wait for approval when the action changes external state.

