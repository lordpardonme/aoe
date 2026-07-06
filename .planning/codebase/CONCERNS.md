# Codebase Concerns

**Analysis Date:** 2026-06-06

## Tech Debt

**Hardcoded local paths:**
- Issue: Several scripts assume the workspace lives at `C:\Users\mohdh\Documents\Job Hunt`
- Files: `Job Hunt/resumes/generate_opening_scan.py`, `Job Hunt/resumes/recover_old_job_hunt_context.py`, `Job Hunt/resumes/reconcile_agency_sent_batch.py`, `drive-extraction/extract-drive-images.js`
- Why: Fast local scripting for one machine and one folder layout
- Impact: Scripts break if the repo is moved or run from a different profile
- Fix approach: Add repo-root discovery or a small config file for workspace paths

**Generated artifacts mixed with source:**
- Issue: Source Markdown, generated PDFs, spreadsheets, previews, OCR outputs, and screenshots live together
- Files: `Job Hunt/resumes/*.md`, `Job Hunt/resumes/*.pdf`, `Job Hunt/resumes/*.xlsx`, `drive-extraction/images/`, `drive-extraction/ocr/`, `drive-extraction/*.csv`
- Why: The workflow treats outputs as first-class review artifacts
- Impact: Large diffs, easy to confuse source with generated data, and higher repo size
- Fix approach: Keep a stricter source/output split or document the generation contract more explicitly

## Known Bugs

**No automated regression safety net:**
- Symptoms: Regressions are only caught when a human inspects the output
- Trigger: Any change to resume generation, OCR parsing, or tracker reconciliation
- Workaround: Manually inspect the generated PDF/XLSX/Markdown files after every run
- Root cause: No automated tests or CI checks exist in the workspace

**Drive extraction depends on Google Drive UI shape:**
- Symptoms: Folder parsing or thumbnail download can fail if Google changes the folder markup or thumbnail behavior
- Trigger: Re-running `drive-extraction/extract-drive-images.js` after upstream UI changes or network issues
- Workaround: Reuse `manifest.json` / `full-manifest.json` and existing OCR outputs where possible
- Root cause: The script scrapes folder HTML rather than using a stable API client

## Security Considerations

**Outreach data and local evidence:**
- Risk: Tracker exports and recovered context may expose personal contacts, resume variants, or screenshots if shared broadly
- Current mitigation: All work stays in a local workspace and the user controls send/update approval
- Recommendations: Keep the recovered evidence folder out of any public sync and avoid copying it into unrelated repos

**Duplicate outreach risk:**
- Risk: Resending to the same agency or contact can look spammy and damage credibility
- Current mitigation: Reconciliation scripts and approval gates are part of the workflow
- Recommendations: Preserve sent IDs, dedupe before any send, and treat tracker state as source of truth

## Performance Bottlenecks

**OCR pass over large image sets:**
- Problem: `drive-extraction/extract-drive-images.js` processes screenshots one by one and can be slow on large folders
- Measurement: Not benchmarked here, but the pipeline is clearly image-heavy and sequential
- Cause: OCR plus image preprocessing on each file
- Improvement path: Cache OCR outputs, keep `REUSE_OCR=1` supported, and scope runs with `LIMIT` when validating

**Large recovered context bundle:**
- Problem: `Job Hunt/resumes/recovered-context/recovered-job-hunt-context.md` is very large
- Measurement: Roughly 400 KB of Markdown plus many screenshot assets
- Cause: It contains transcript history and evidence notes from a prior Codex session
- Improvement path: Keep it as an archive and avoid editing it casually

## Fragile Areas

**Absolute-path assumptions:**
- Why fragile: Path constants are embedded in scripts instead of being derived from the current repo root
- Common failures: Script works on one machine but not another
- Safe modification: Centralize root detection and make source/output paths configurable
- Test coverage: None

**Workbook reconciliation scripts:**
- Why fragile: They update spreadsheet files in place and rely on exact column names
- Common failures: A renamed header or changed workbook layout can silently break updates
- Safe modification: Validate headers before writing and fail with a clear error
- Test coverage: None

**Evidence bank truthfulness:**
- Why fragile: Resume copy is intentionally constrained by the evidence bank and recovered notes
- Common failures: Overstated claims or merged product surfaces can weaken applications
- Safe modification: Keep claims tied to named artifacts such as `career-evidence-bank.md`
- Test coverage: Manual only

## Scaling Limits

**Single-machine workflow:**
- Current capacity: Whatever fits on the local disk and can be processed by a single Windows workstation
- Limit: Large OCR runs and many resume variants become tedious to manage manually
- Symptoms at limit: Slow reruns, larger diffs, and harder review
- Scaling path: Introduce better caching, narrow incremental runs, and add verification scripts

## Dependencies at Risk

**`tesseract.js` / local OCR runtime:**
- Risk: OCR extraction is sensitive to runtime bundle changes and language data availability
- Impact: `drive-extraction/extract-drive-images.js` cannot produce `ocr/*.txt`
- Migration plan: Pin the runtime better or package the needed modules locally

**`openpyxl` and `reportlab`:**
- Risk: Workbook and PDF generation depend on environment-installed Python packages
- Impact: Resume generation and tracker writes fail if the packages are missing
- Migration plan: Add an explicit Python dependency manifest

## Missing Critical Features

**Automated test harness:**
- Problem: There is no repeatable test suite for the tracker or resume generation flows
- Current workaround: Manual inspection after each run
- Blocks: Safe refactoring and easy regression detection
- Implementation complexity: Low to medium

**Shared config layer:**
- Problem: Script paths and runtime assumptions are duplicated across files
- Current workaround: Copy/paste constants
- Blocks: Clean relocation of the workspace or reuse in a new environment
- Implementation complexity: Low

## Test Coverage Gaps

**OCR parsing and lead bucketing:**
- What's not tested: Folder parsing, OCR text extraction, and lead categorization
- Risk: Changes in Google Drive HTML or OCR behavior could quietly break the pipeline
- Priority: High
- Difficulty to test: Requires fixture images and a repeatable OCR sample set

**Tracker update scripts:**
- What's not tested: Header matching, status transitions, and duplicate suppression
- Risk: Incorrect workbook edits or stale outreach state
- Priority: High
- Difficulty to test: Needs representative workbook fixtures

**PDF resume generation:**
- What's not tested: Layout stability and content presence in the generated PDFs
- Risk: Broken resume exports with no immediate signal
- Priority: Medium
- Difficulty to test: Requires PDF inspection or rendering comparisons

---

*Concerns audit: 2026-06-06*
*Update as issues are fixed or new ones discovered*
