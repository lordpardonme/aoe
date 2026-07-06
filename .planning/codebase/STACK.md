# Technology Stack

**Analysis Date:** 2026-06-06

## Languages

**Primary:**
- Python 3 - Resume generation, tracker reconciliation, workbook updates, and evidence recovery in `Job Hunt/resumes/*.py`

**Secondary:**
- JavaScript / Node.js - OCR, Drive extraction, and lead categorization in `drive-extraction/*.js`
- Markdown, CSV, TSV, JSON, XLSX, PDF - Source artifacts and generated outputs used throughout the workflow

## Runtime

**Environment:**
- Windows local workspace with PowerShell orchestration
- Python 3.x from the local developer environment
- Node.js runtime from the Codex runtime bundle for the Drive/OCR scripts
- No long-running server or browser runtime

**Package Manager:**
- None in-repo - there is no `package.json`, `requirements.txt`, or lockfile
- Python and Node dependencies are provided by the local environment/runtime

## Frameworks

**Core:**
- None - this is a script-driven workspace, not an app framework

**Testing:**
- None - no dedicated test runner or test framework is present

**Build/Dev:**
- `openpyxl` - read/write Excel workbooks and rebuild categorized sheets
- `reportlab` - generate the target-specific PDF resumes
- `sharp` - image preprocessing for OCR
- `tesseract.js` - OCR engine used in the Drive extraction pipeline

## Key Dependencies

**Critical:**
- `openpyxl` - updates tracker workbooks and generates `.xlsx` outputs
- `reportlab` - renders the various target resume PDFs
- `sharp` - preprocesses Drive screenshots before OCR
- `tesseract.js` - extracts text from screenshots in `drive-extraction/extract-drive-images.js`

**Infrastructure:**
- Python standard library - `csv`, `pathlib`, `json`, `re`, `datetime`, `base64`
- Node.js built-ins - `fs`, `path`, `module`, `fetch`
- Codex runtime node_modules bundle - required by `drive-extraction/extract-drive-images.js` via `NODE_PATH`

## Configuration

**Environment:**
- Hardcoded local workspace paths are used in several scripts, especially `C:\Users\mohdh\Documents\Job Hunt`
- `drive-extraction/extract-drive-images.js` uses `FOLDER_ID`, `LIMIT`, and `REUSE_OCR`
- `Job Hunt/.codex/environments/environment.toml` stores generated environment metadata
- `Job Hunt/skills-lock.json` records installed skill metadata for the workspace

**Build:**
- No formal build pipeline
- Script outputs are written directly to tracked files such as `*.md`, `*.csv`, `*.tsv`, `*.xlsx`, and `*.pdf`

## Platform Requirements

**Development:**
- Windows paths and PowerShell-friendly invocation are assumed
- Local file access to the workspace is required
- Network access is needed only for the Google Drive thumbnail/folder fetch in `drive-extraction/extract-drive-images.js`

**Production:**
- No deployment target
- Outputs are local documents, spreadsheets, and PDFs used for job-hunt operations

---

*Stack analysis: 2026-06-06*
*Update after major dependency changes*
