# Codebase Structure

**Analysis Date:** 2026-06-06

## Directory Layout

```text
workspace/
├── drive-extraction/                 # OCR and lead-categorization toolkit
│   ├── images/                       # Downloaded Drive thumbnails
│   ├── ocr/                          # OCR text output for each image
│   ├── tessdata/                     # Local Tesseract language data
│   ├── *.js                          # Node scripts for extraction/indexing
│   ├── *.csv / *.tsv / *.md          # Preview and summary outputs
│   └── *.json / folder.html          # Drive manifest snapshots and structured data
└── Job Hunt/                         # Nested git repo for resume and tracker work
    ├── AGENTS.md                     # Repo-specific workflow instructions
    ├── sheet-export.csv              # Tracker export snapshot
    ├── skills-lock.json              # Installed skill metadata
    ├── .codex/environments/          # Codex environment metadata
    ├── .agents/skills/               # Locally installed skills used by the workflow
    └── resumes/
        ├── *.md                      # Resume sources, ATS reports, evidence bank
        ├── *.py                      # Tracker, reconciliation, and PDF generation scripts
        ├── *.pdf                     # Generated target resumes
        ├── *.xlsx                    # Tracker and scan workbooks
        └── recovered-context/        # Recovered notes and screenshot evidence
```

## Directory Purposes

**drive-extraction/**
- Purpose: Convert screenshot-heavy Drive content into searchable lead data
- Contains: Node scripts, OCR assets, generated manifests, preview tables, and extracted text
- Key files: `extract-drive-images.js`, `categorize-unknown-leads.js`, `create-quick-index.js`, `summarize-unknown-bucket.js`
- Subdirectories: `images/`, `ocr/`, `tessdata/`

**Job Hunt/**
- Purpose: Main job-hunt workspace for resume variants, evidence, and tracker maintenance
- Contains: CSV/XLSX trackers, Markdown resume sources, generated PDFs, Python automation, and recovered context
- Key files: `AGENTS.md`, `sheet-export.csv`, `skills-lock.json`
- Subdirectories: `resumes/`, `.agents/skills/`, `.codex/environments/`

**Job Hunt/resumes/**
- Purpose: All resume content and operational scripts live here
- Contains: company-specific resume Markdown, ATS reports, PDF renderers, workbook updaters, and recovery scripts
- Key files: `career-evidence-bank.md`, `recover_old_job_hunt_context.py`, `generate_opening_scan.py`, `create_*_pdf.py`
- Subdirectories: `recovered-context/`

**Job Hunt/resumes/recovered-context/**
- Purpose: Restored memory from older Codex sessions
- Contains: recovered Markdown notes, screenshots, and compressed workflow context
- Key files: `recovered-job-hunt-context.md`, `resume-memory-rebuild.md`, `email-and-copywriting-playbook.md`
- Subdirectories: `screenshots/`

## Key File Locations

**Entry Points:**
- `drive-extraction/extract-drive-images.js` - OCR extraction entry point
- `drive-extraction/categorize-unknown-leads.js` - lead classification and CSV output
- `Job Hunt/resumes/generate_opening_scan.py` - opening scan generator
- `Job Hunt/resumes/generate_opening_scan_xlsx.py` - workbook generator for opening scans
- `Job Hunt/resumes/create_agency_pdf.py` and the other `create_*_pdf.py` scripts - PDF export entry points

**Configuration:**
- `Job Hunt/.codex/environments/environment.toml` - generated Codex environment metadata
- `Job Hunt/skills-lock.json` - installed skill metadata
- `drive-extraction/extract-drive-images.js` - hardcoded Drive folder ID, `LIMIT`, and `REUSE_OCR`

**Core Logic:**
- `Job Hunt/resumes/career-evidence-bank.md` - defensible claim inventory
- `Job Hunt/resumes/recovered-context/recovered-job-hunt-context.md` - raw recovered evidence and transcript history
- `drive-extraction/job-leads-extraction.json` - structured OCR output used by downstream scripts

**Testing:**
- None - there is no `tests/` tree or dedicated test runner

**Documentation:**
- `Job Hunt/AGENTS.md` - repo workflow instructions
- `Job Hunt/resumes/job-opening-scan-notes.md` - scan rationale and prioritized openings
- `Job Hunt/resumes/recovered-context/*.md` - workflow recovery and evidence notes
- `drive-extraction/*.md` - generated summaries and review notes

## Naming Conventions

**Files:**
- `create_<target>_pdf.py` - renders a PDF for a specific target
- `mark_<target>_applied.py` - updates tracker status for one employer
- `reconcile_<purpose>.py` - resolves tracker drift or duplicate sends
- `*-product-designer-resume.md` - target-specific resume source
- `*-senior-product-designer-ats-report.md` - ATS analysis artifact
- `IMG_####.jpg` / `IMG_####.txt` - screenshot images and OCR text pairs

**Directories:**
- Lowercase, hyphenated names for the toolkit directories and most generated folders
- `recovered-context/` for restored memory and evidence
- `images/`, `ocr/`, `tessdata/` for OCR pipeline assets

**Special Patterns:**
- `*.csv` and `*.tsv` are often generated preview or reconciliation files
- `*.xlsx` files are operational tracker workbooks rather than source code
- `*_preview.*` files are temporary review outputs before sheet updates

## Where to Add New Code

**New Feature:**
- Primary code: `Job Hunt/resumes/` or `drive-extraction/` depending on whether the change affects resume ops or OCR extraction
- Tests: none currently; if added, keep them near the related script or in a new `tests/` tree
- Config if needed: sibling script constants or a new shared config file

**New Component/Module:**
- Implementation: `Job Hunt/resumes/` for Python utilities, `drive-extraction/` for Node utilities
- Types: not centralized; keep inline or add a small shared module if reuse grows
- Tests: add alongside the module if automated tests are introduced

**New Route/Command:**
- Definition: not applicable; there is no web server or CLI framework
- Handler: a new script in the relevant directory
- Tests: not currently present

**Utilities:**
- Shared helpers: the same directory as the scripts that consume them, unless reuse justifies extraction
- Type definitions: not currently used

## Special Directories

**Job Hunt/.agents/skills/**
- Purpose: Workspace-installed skill bundles used by the Codex workflow
- Source: Installed from curated skill sources
- Committed: Yes, as workflow support metadata

**Job Hunt/.codex/environments/**
- Purpose: Codex environment metadata
- Source: Generated by the Codex environment tooling
- Committed: Yes

**Job Hunt/.git/**
- Purpose: Nested git repository metadata
- Source: Git
- Committed: No, standard git internals

**drive-extraction/images/**
- Purpose: Downloaded thumbnails from Google Drive
- Source: `extract-drive-images.js`
- Committed: Usually yes in this workspace, because they are part of the extracted evidence set

**drive-extraction/ocr/**
- Purpose: OCR text derived from the downloaded images
- Source: `extract-drive-images.js`
- Committed: Usually yes, for reproducibility and review

---

*Structure analysis: 2026-06-06*
*Update when directory structure changes*
