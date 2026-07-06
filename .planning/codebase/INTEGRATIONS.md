# External Integrations

**Analysis Date:** 2026-06-06

## APIs & External Services

**External APIs:**
- Google Drive folder HTML and thumbnail endpoints - used by `drive-extraction/extract-drive-images.js` to discover and download screenshot assets
  - Integration method: unauthenticated HTTP `fetch()` to the shared folder page and thumbnail URLs
  - Auth: shared/public access to the folder, not an API token in the repo
  - Endpoints used: folder page plus `thumbnail?id=...` links

**Reference-only web sources:**
- Company websites and LinkedIn pages listed in `drive-extraction/categorize-unknown-leads.js`
  - Integration method: manual verification references, not programmatic API calls
  - Auth: none in the codebase
  - Rate limits: not managed by code

## Data Storage

**Databases:**
- None - the workflow is file-based, not database-backed

**File Storage:**
- Local filesystem workspace - primary storage for CSV, TSV, JSON, XLSX, PDF, Markdown, images, and OCR text
  - SDK/Client: Node `fs` / Python `Path` and workbook libraries
  - Auth: none

**Caching:**
- None

## Authentication & Identity

**Auth Provider:**
- None in code

**OAuth Integrations:**
- None in code

## Monitoring & Observability

**Error Tracking:**
- None

**Analytics:**
- None

**Logs:**
- Standard console output only

## CI/CD & Deployment

**Hosting:**
- None - there is no deployed application

**CI Pipeline:**
- None - no CI workflows were found in this workspace

## Environment Configuration

**Development:**
- Required env vars: `LIMIT`, `REUSE_OCR` for `drive-extraction/extract-drive-images.js`
- Secrets location: none in repo; no secret-bearing config files were found
- Mock/stub services: none

**Staging:**
- Not applicable

**Production:**
- Not applicable

## Webhooks & Callbacks

**Incoming:**
- None

**Outgoing:**
- Google Drive thumbnail and folder fetches are the only clear network calls
  - Trigger: manual execution of `drive-extraction/extract-drive-images.js`
  - Retry logic: none

---

*Integration audit: 2026-06-06*
*Update when adding/removing external services*
