# Testing Patterns

**Analysis Date:** 2026-06-06

## Test Framework

**Runner:**
- None - there is no automated test runner in this workspace

**Assertion Library:**
- None - no `jest`, `vitest`, `pytest`, or similar assertion framework is present

**Run Commands:**
```bash
No dedicated test commands are defined in the repository.
```

## Test File Organization

**Location:**
- No `tests/` tree or colocated `*.test.*` files were found
- Validation is done by running the scripts directly and checking their outputs

**Naming:**
- Not applicable yet

**Structure:**
```text
There is no standardized automated test directory structure yet.
```

## Test Structure

**Suite Organization:**
```typescript
Not applicable - there are no describe/it suites in the repository.
```

**Patterns:**
- Manual smoke testing after generation
- Re-run a script and inspect the resulting CSV, XLSX, PDF, or Markdown output
- Check line counts or workbook contents when verifying generated files

## Mocking

**Framework:**
- None

**Patterns:**
```typescript
No mocking patterns are established in this codebase yet.
```

**What to Mock:**
- If automated tests are added, mock file system access, Drive fetches, and workbook writes

**What NOT to Mock:**
- Pure transformations like row bucketing, email normalization, and filename generation

## Fixtures and Factories

**Test Data:**
```text
The closest thing to fixtures today is the real workspace data:
- `Job Hunt/sheet-export.csv`
- `Job Hunt/resumes/agency-outreach-plan.csv`
- `Job Hunt/resumes/recovered-context/*.md`
- `drive-extraction/manifest.json`
- `drive-extraction/ocr/*.txt`
```

**Location:**
- No dedicated fixture directories are present

## Coverage

**Requirements:**
- No automated coverage target

**Configuration:**
- No coverage tooling configured

**View Coverage:**
```bash
No coverage command is defined.
```

## Test Types

**Unit Tests:**
- Not present

**Integration Tests:**
- Not present

**E2E Tests:**
- Not present

## Common Patterns

**Async Testing:**
```typescript
Not currently used.
```

**Error Testing:**
```typescript
Not currently used.
```

**Snapshot Testing:**
- Not used

## Practical Verification

- Run `python` scripts and confirm the target workbook or Markdown file is updated
- Run `node` scripts and confirm the OCR/report files are produced
- Open the generated PDF or spreadsheet to confirm the content is correct
- Use tracker diffs and preview files as the main regression signal

---

*Testing analysis: 2026-06-06*
*Update when test patterns change*
