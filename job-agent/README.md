# Job Agent

An autonomous AI job-application agent. Give it a job posting (URL or text) and it will:

1. Fetch & parse the job description.
2. Analyse your **master resume** (never modifies it).
3. Generate an **ATS-optimised, tailored resume** (DOCX + PDF).
4. Generate a **tailored cover letter** (Markdown + DOCX + PDF).
5. Generate a **professional application email** (Markdown + HTML).
6. **Send** the email through the Gmail API (with PDF attachments).
7. **Update** your Google Sheet application tracker (+ a local CSV mirror).
8. **Save** every artefact locally under `generated/` and a JSON record under `tracker/`.
9. **Log** every action to `logs/app.log` and every error to `logs/error.log`.
10. **Retry** transient network failures automatically.

A global `DRY_RUN` switch (on by default) lets you generate everything without
sending mail or writing to Sheets until you're ready.

---

## Project structure

```
job-agent/
├── master_resume.docx        # your master resume (read-only source of truth)
├── credentials.json          # Google OAuth client secret
├── token.json                # OAuth token (created by authenticate.py)
├── .env                      # configuration (copy from .env.example)
├── authenticate.py           # one-time Google OAuth flow
├── main.py                   # CLI entrypoint
├── requirements.txt
├── templates/
│   ├── resume_template.docx  # style base for tailored resumes
│   ├── cover_letter.md       # Jinja2 cover-letter template
│   └── email.md              # Jinja2 email template
├── generated/
│   ├── resumes/              # <company>_resume.docx / .pdf
│   ├── coverletters/         # <company>_cover_letter.md / .docx / .pdf
│   └── emails/               # <company>_email.md / .html
├── logs/                     # app.log, error.log
├── tracker/                  # applications.csv + per-application JSON records
├── scripts/
│   └── seed_master_resume.py # (re)generate master_resume.docx
├── src/                      # application package
│   ├── config.py   logger.py  utils.py
│   ├── jobs.py     resume.py   coverletter.py  emailer.py
│   ├── pdf.py      gmail.py    sheet.py
│   ├── agent.py    cli.py
└── tests/                    # pytest suite (fully offline)
```

---

## Setup

### 1. Python

Requires **Python 3.13**. On Windows the interpreter is typically at
`C:\Users\<you>\AppData\Local\Programs\Python\Python313\python.exe`.

### 2. Create a virtual environment & install dependencies

```bash
cd job-agent
python -m venv .venv
# Windows PowerShell:
.venv\Scripts\Activate.ps1
# macOS/Linux:
# source .venv/bin/activate
pip install -r requirements.txt
```

Playwright is optional (used only for JavaScript-heavy job pages). To enable it:

```bash
python -m playwright install chromium
```

### 3. Configure

```bash
cp .env.example .env      # then edit values
```

Key settings:

| Variable | Purpose |
| --- | --- |
| `TRACKER_SPREADSHEET_ID` | Your Google Sheet ID. Leave blank to auto-create one on first live run. |
| `SENDER_EMAIL` | The Gmail account that owns `token.json`. |
| `DEFAULT_RECIPIENT` | Fallback recipient when a posting has no contact email. |
| `DRY_RUN` | `true` = build everything but don't send/track. Set `false` to go live. |
| `CANDIDATE_*` | Your name, contact details and portfolio for letters/emails. |

### 4. Authorise Google (one time)

`credentials.json` and `token.json` are already present in this workspace. If you
ever need to re-authorise (new scopes, revoked token):

```bash
python authenticate.py
```

This opens a browser, and writes/refreshes `token.json`. Scopes used:
`gmail.send`, `gmail.readonly`, `spreadsheets`, `drive.file`.

### 5. Seed the master resume (only if missing)

```bash
python scripts/seed_master_resume.py
```

---

## Usage

```bash
# Full pipeline from a URL
python main.py apply --url https://boards.greenhouse.io/acme/jobs/123

# Full pipeline from a text file (best for reliable company/role detection)
python main.py apply --file jd.txt --company "Acme Labs" --role "Product Designer"

# Generate only the tailored resume
python main.py resume --file jd.txt

# Generate only the email
python main.py email --file jd.txt

# Add a tracker row manually
python main.py tracker --company "Acme Labs" --role "Product Designer" --status Applied

# Build documents and send the email (respects DRY_RUN)
python main.py send --file jd.txt --to hiring@acme.com

# Run self-checks (offline generation + Google connectivity probe)
python main.py test
```

Useful flags on `apply`:

- `--company` / `--role` — override auto-detection (recommended).
- `--to` — override the recipient email.
- `--no-send` — build & track but don't email.
- `--no-sheet` — build & email but don't touch the tracker.

### Going live

Everything runs in **DRY_RUN** by default. When you're happy with the generated
files, set `DRY_RUN=false` in `.env`. The agent will then actually send email and
append to your Google Sheet. Sending email and writing to Sheets are real,
outward-facing actions — review the generated artefacts first.

---

## How tailoring works

Job Agent uses a deterministic, **truthful** tailoring engine (no fabricated
experience):

- It extracts design/product keywords from the JD against a controlled vocabulary.
- It injects a role-specific summary line and a **Key Skills** ATS block listing
  the matched keywords.
- It reorders your Core Capabilities so JD-relevant strengths lead.
- Cover-letter/email highlights are drawn from your real, quantified achievements,
  ranked by relevance to the posting.

The generation layer is modular — you can swap in an LLM by replacing the
tailoring/generation functions in `src/resume.py`, `src/coverletter.py` and
`src/emailer.py` without touching the pipeline.

---

## Testing

```bash
pip install -r requirements.txt
python -m pytest -q
```

All tests are **offline** and force `DRY_RUN=true`, so they never send email or
write to Google Sheets.

---

## Safety notes

- The **master resume is never modified** — it is opened read-only and only
  copies are written to `generated/`.
- `credentials.json`, `token.json` and `.env` are git-ignored.
- `DRY_RUN` defaults to `true`; no email or Sheet write happens until you opt in.
- Every network operation is retried with back-off and fully logged.
```
