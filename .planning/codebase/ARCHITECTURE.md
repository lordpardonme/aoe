# Architecture

**Analysis Date:** 2026-06-06

## Pattern Overview

**Overall:** Document-centric batch-processing workspace with two main pipelines: a job-hunt resume/tracker repo and a Drive OCR/extraction toolkit

**Key Characteristics:**
- File-based state instead of a database or API server
- One-off scripts that read/write local documents in place
- Generated artifacts are part of the workflow, not just build output
- Heavy manual review gates for outreach and lead classification

## Layers

**Evidence and Tracker Layer:**
- Purpose: Hold the canonical job-hunt truth set and tracker snapshots
- Contains: `Job Hunt/sheet-export.csv`, `Job Hunt/resumes/career-evidence-bank.md`, `Job Hunt/resumes/recovered-context/*.md`, `Job Hunt/resumes/*.xlsx`
- Depends on: Manual curation, spreadsheet exports, and recovered session notes
- Used by: Resume generation, outreach planning, and reconciliation scripts

**Transformation Layer:**
- Purpose: Convert evidence into tailored resumes, scan results, and tracker updates
- Contains: `Job Hunt/resumes/create_*_pdf.py`, `Job Hunt/resumes/mark_*.py`, `Job Hunt/resumes/reconcile_*.py`, `Job Hunt/resumes/generate_opening_scan*.py`
- Depends on: `openpyxl`, `reportlab`, CSV parsing, and local file paths
- Used by: The user when preparing applications and maintaining tracker state

**Extraction Layer:**
- Purpose: Pull text and structured leads out of screenshot-heavy Drive content
- Contains: `drive-extraction/extract-drive-images.js`, `drive-extraction/categorize-unknown-leads.js`, `drive-extraction/create-quick-index.js`, `drive-extraction/summarize-unknown-bucket.js`
- Depends on: Google Drive folder HTML/thumbnails, `sharp`, `tesseract.js`, and local OCR assets
- Used by: Lead review and tracker categorization work

**Output Layer:**
- Purpose: Persist human-reviewable outputs for the next workflow step
- Contains: generated PDFs, categorized `.xlsx` trackers, preview `.csv/.tsv` files, OCR text files, manifests, and Markdown summaries
- Depends on: The upstream scripts completing successfully
- Used by: Manual review, approval, and outreach execution

## Data Flow

**Resume and Outreach Flow:**

1. Tracker exports and evidence notes are read from `Job Hunt/sheet-export.csv` and `Job Hunt/resumes/career-evidence-bank.md`
2. A target-specific Markdown resume is edited or generated in `Job Hunt/resumes/*.md`
3. A `create_*_pdf.py` script renders the matching PDF into `Job Hunt/resumes/*.pdf`
4. Reconciliation scripts update workbook state in `Job Hunt/resumes/*.xlsx`
5. The user reviews the result before any outreach is sent

**Drive Extraction Flow:**

1. `drive-extraction/extract-drive-images.js` fetches a Google Drive folder listing and downloads thumbnails
2. The script preprocesses each image and runs OCR into `drive-extraction/ocr/*.txt`
3. It writes structured records to `drive-extraction/job-leads-extraction.json` and a human-readable report
4. Follow-up scripts bucket leads into agency/direct/unknown review files
5. Preview TSV/CSV files are used to reconcile tracker rows

**State Management:**
- File-based only
- No persistent in-memory service state
- Generated files are overwritten or appended deterministically

## Key Abstractions

**Evidence Bank:**
- Purpose: Preserve defensible claims for resumes and outreach
- Examples: `Job Hunt/resumes/career-evidence-bank.md`, `Job Hunt/resumes/recovered-context/recovered-job-hunt-context.md`
- Pattern: Truth source used to avoid generic or inflated CV bullets

**Target Variant:**
- Purpose: A per-company or per-agency resume version
- Examples: `Job Hunt/resumes/ziina-senior-product-designer-resume.md`, `Job Hunt/resumes/agency-product-designer-resume.md`
- Pattern: Markdown source plus generated PDF companion

**Tracker Row:**
- Purpose: One company, agency, or follow-up record in the outreach workflow
- Examples: `Job Hunt/sheet-export.csv`, `Job Hunt/resumes/agency-outreach-plan.csv`
- Pattern: Spreadsheet record updated by reconciliation scripts

**Lead Record:**
- Purpose: OCR-derived company/contact item from screenshots
- Examples: `drive-extraction/job-leads-extraction.json`, `drive-extraction/unknown-categorization-proposal.md`
- Pattern: Generated record that still needs human verification

## Entry Points

**Drive OCR Entry:**
- Location: `drive-extraction/extract-drive-images.js`
- Triggers: Manual `node` execution
- Responsibilities: Download Drive thumbnails, OCR them, and write extracted artifacts

**Lead Indexing Entry:**
- Location: `drive-extraction/create-quick-index.js`, `drive-extraction/categorize-unknown-leads.js`
- Triggers: Manual `node` execution after OCR output exists
- Responsibilities: Summarize and re-bucket extracted lead data

**Resume / Tracker Entry:**
- Location: `Job Hunt/resumes/generate_opening_scan.py`, `Job Hunt/resumes/generate_opening_scan_xlsx.py`, `Job Hunt/resumes/create_*_pdf.py`
- Triggers: Manual `python` execution
- Responsibilities: Build opening scans, generate PDFs, and update workbook outputs

## Error Handling

**Strategy:** Fail fast on missing files, missing OCR assets, or malformed workbook/input data

**Patterns:**
- Python scripts rely on normal exceptions from `openpyxl`, file I/O, and parsing
- Node scripts throw explicit errors for missing folder data or download failures
- `drive-extraction/extract-drive-images.js` uses a top-level `main().catch(...)` for process-level failure reporting

## Cross-Cutting Concerns

**Logging:**
- Console output only
- Script progress is printed to stdout as each file or row is processed

**Validation:**
- Manual review after generation is the main validation step
- Tracker state is reconciled before any send/update action

**Truthfulness:**
- Resume claims are constrained by `Job Hunt/resumes/career-evidence-bank.md`
- Outreach is intentionally one-by-one and approval-gated

---

*Architecture analysis: 2026-06-06*
*Update when major patterns change*
