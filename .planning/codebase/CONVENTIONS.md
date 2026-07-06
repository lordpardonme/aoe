# Codebase Conventions

**Analysis Date:** 2026-06-06

## Language and Script Style

**Python scripts:**
- Use top-level constants for source and output paths
- Prefer small helper functions and a single `main()` entry point
- Import order is usually standard library first, then third-party modules
- Write outputs directly with `Path.write_text`, `write_bytes`, or workbook APIs
- Keep logic procedural rather than object-oriented

**Node scripts:**
- Use CommonJS `require()` rather than ES modules
- Set path constants at the top of the file
- Prefer explicit helper functions over classes
- Use `const` for almost everything
- Keep scripts runnable as a single file with `node <script>.js`

## Data Handling

**CSV/XLSX:**
- Treat spreadsheet exports as the main state store for tracker data
- Preserve column names exactly when possible
- Build output rows deterministically so regenerated files are easy to diff

**Markdown:**
- Use Markdown as the human review layer for evidence, ATS notes, and generated summaries
- Keep claim language factual and traceable back to the evidence bank

**PDF Generation:**
- Render target-specific resumes from Markdown-adjacent source content using `reportlab`
- Keep the source Markdown and generated PDF paired by filename

## File and Path Conventions

**Paths:**
- Hardcoded absolute paths are common in this workspace
- Keep path constants near the top of the script so they are easy to update
- Many scripts assume the `Job Hunt` folder lives at `C:\Users\mohdh\Documents\Job Hunt`

**Naming:**
- Python: snake_case filenames such as `generate_opening_scan.py`
- JavaScript: kebab-case filenames such as `create-quick-index.js`
- Resume variants use descriptive target names such as `ziina-senior-product-designer-resume.md`

## Error Handling

**General Approach:**
- Fail fast instead of trying to continue with partial data
- Let file I/O and parser exceptions surface unless a script needs a top-level catch
- Use explicit `throw new Error(...)` in Node when a required asset is missing

**Operational Pattern:**
- If a script cannot find its input export, OCR assets, or target workbook, the run should stop immediately
- Generated artifacts are overwritten intentionally, so reruns should be deliberate

## Review and Truthfulness

**Evidence Discipline:**
- Keep resume claims in sync with `Job Hunt/resumes/career-evidence-bank.md`
- Prefer exact, defensible claims over broad marketing language
- Preserve distinctions between consumer, B2B, franchise, support, and asset-management FuelBuddy surfaces

**Outreach Discipline:**
- Keep agency outreach one-by-one and approval-gated
- Avoid duplicate sends unless the user explicitly approves a resend
- Use tracker notes to capture which PDF version was sent

## Absence of Frameworks

- No CLI framework, web framework, or central app architecture is present
- No shared config layer or typed domain model is currently used
- No test harness exists yet, so script quality depends on manual verification

---

*Conventions analysis: 2026-06-06*
*Update when code style or workflow conventions change*
