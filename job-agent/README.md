# Job Hunt Agent

## Overview
Job Hunt Agent is an autonomous, end-to-end job application pipeline. It takes a job description and automatically tailors a master resume, generates a targeted cover letter, drafts an outreach email, sends the application via Gmail, and logs the attempt in a Google Sheets tracker.

## Features
- **Resume Tailoring**: Matches your master CV against JD keywords.
- **PDF Generation**: Creates branded, ATS-friendly PDF resumes and cover letters.
- **Email Generation**: Drafts customized cold outreach emails.
- **Gmail API Integration**: Sends applications directly from your Gmail account.
- **Application Tracking**: Automatically logs applications in a remote Google Sheet and local CSV.
- **Multi-profession Support**: Uses customizable vocabulary packs to adapt to different roles.
- **Dry Run Mode**: Safely test the entire pipeline without sending real emails or writing to Sheets.

## Prerequisites
- Python 3.9+
- A Google Cloud Project with the **Gmail API** and **Google Sheets API** enabled.
- OAuth 2.0 credentials (type: Desktop App).
- A master resume in `.docx` format (`master_resume.docx` in the root).

## Quick Start
1. **Clone the repo:**
   ```bash
   git clone <your-repo-url>
   cd job-agent
   ```
2. **Create a virtual environment:**
   ```bash
   python -m venv .venv
   # Windows:
   .venv\Scripts\activate
   # macOS/Linux:
   source .venv/bin/activate
   ```
3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```
4. **Run the setup wizard (Authentication):**
   Place your downloaded `credentials.json` in the root directory and run:
   ```bash
   python authenticate.py
   ```
5. **Send your first application:**
   ```bash
   # Make sure DRY_RUN=true in .env to test safely
   python -m src.cli apply --url "https://example.com/job/123"
   ```

## Setup Guide

### 1. GCP Project Creation
1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Click the project dropdown at the top and select **New Project**.
3. Name it "JobAgent" and click **Create**.
4. In the sidebar, navigate to **APIs & Services > Library**.
5. Search for and enable the **Gmail API** and **Google Sheets API**.

### 2. OAuth Consent Screen
1. Go to **APIs & Services > OAuth consent screen**.
2. Choose **External** (or Internal if you have a Workspace account).
3. Fill in the required fields (App name: Job Agent, User support email, Developer contact).
4. Add yourself as a Test User.
5. Save and continue.

### 3. Credential Download
1. Go to **APIs & Services > Credentials**.
2. Click **Create Credentials > OAuth client ID**.
3. Choose **Desktop app** as the application type.
4. Name it "Job Agent Desktop" and create.
5. Click **Download JSON** and save it as `credentials.json` in the root of the `job-agent` directory.

### 4. Running the Setup Wizard
Run `python authenticate.py`. This script will open a browser window for you to log into your Google account and authorize the app. Once authorized, a `token.json` file will be generated in the root.

### 5. Manual `.env` Configuration
Copy the provided `.env.example` to `.env`:
```bash
cp .env.example .env
```
Fill in the values according to your needs (see [Configuration Reference](#configuration-reference)).

## Usage

The Agent provides a CLI with various commands for different stages of the application process.

### `apply`
Run the full application pipeline for a single job (tailor -> cover letter -> email -> PDFs -> send -> track).
```bash
python -m src.cli apply --url "https://example.com/job/123"
python -m src.cli apply --text "Raw job description text here" --company "Acme Corp" --role "Engineer"
```

### `resume`
Generate only the tailored resume (DOCX + PDF) without sending or tracking.
```bash
python -m src.cli resume --file "./sample_jd.txt"
```

### `email`
Generate only the application email (Markdown + HTML).
```bash
python -m src.cli email --url "https://example.com/job/123"
```

### `send`
Build the application documents and send the email, but skip updating the tracker.
```bash
python -m src.cli send --url "https://example.com/job/123" --to "hr@example.com"
```

### `tracker`
Append a single row to the application tracker manually.
```bash
python -m src.cli tracker --company "Acme" --role "Developer" --status "Applied"
```

### `test`
Run offline self-checks and probe Google connectivity to ensure your setup is valid.
```bash
python -m src.cli test
```

## Configuration Reference

The `.env` file controls the application's runtime behavior.

| Variable | Description | Example |
| -------- | ----------- | ------- |
| `GOOGLE_CREDENTIALS_FILE` | Path to your GCP OAuth credentials | `credentials.json` |
| `GOOGLE_TOKEN_FILE` | Path to the generated OAuth token | `token.json` |
| `TRACKER_SPREADSHEET_ID` | The ID of your Google Sheet tracker | `1A2b3C4d5E...` |
| `TRACKER_SHEET_NAME` | The specific sheet/tab name | `Applications` |
| `CANDIDATE_NAME` | Your full name | `Mohd Hayaat Ali` |
| `CANDIDATE_EMAIL` | Your contact email for the resume | `user@example.com` |
| `CANDIDATE_PHONE` | Your contact phone number | `+1-555-0100` |
| `CANDIDATE_LOCATION` | Your city/region | `Delhi NCR, India` |
| `CANDIDATE_PORTFOLIO` | Link to your portfolio/website | `https://myportfolio.com` |
| `CANDIDATE_LINKEDIN` | Link to your LinkedIn profile | `https://linkedin.com/in/user` |
| `SENDER_EMAIL` | The Gmail address sending the application | `user@gmail.com` |
| `DEFAULT_RECIPIENT` | Fallback recipient if JD has no email | `jobs@example.com` |
| `DRY_RUN` | Disables sending emails and Sheets API writes | `true` or `false` |
| `MAX_RETRIES` | Network retry attempts | `3` |
| `RETRY_BACKOFF_SECONDS` | Delay between retries | `2` |

## Profession Packs
Profession packs allow the agent to understand different vocabularies and keywords specific to various roles (e.g., frontend developer vs. product designer).
- **Usage**: The agent automatically detects the role and applies the relevant pack.
- **Customization**: You can add new JSON packs in the `src/packs/` directory (or wherever packs are stored) to teach the agent new synonyms and required skills.

## Platform Notes

### Windows
- **Venv Activation**: Use `.venv\Scripts\activate`
- **Fonts**: Ensure necessary fonts (e.g., Arial, Helvetica, or custom fonts) are installed system-wide in `C:\Windows\Fonts` for PDF generation to work properly.

### macOS
- **Venv Activation**: Use `source .venv/bin/activate`
- **Fonts**: PDF generation relies on fonts being available in `/Library/Fonts` or `~/Library/Fonts`.
- **Dependencies**: You might need `brew install pango` or similar if the PDF renderer (like WeasyPrint) is used.

### Linux
- **Venv Activation**: Use `source .venv/bin/activate`
- **Fonts**: Ensure fonts are installed in `/usr/share/fonts/`.
- **Dependencies**: May require `sudo apt install libpango-1.0-0` or similar depending on the PDF rendering backend.

## Architecture

The system follows a sequential pipeline:
1. **Acquisition**: `fetch_from_url` or `load_from_file` gets the JD text.
2. **Parsing**: NLP/regex identifies keywords, company, role, and contact info.
3. **Tailoring**: The `ResumeBuilder` modifies `master_resume.docx` to highlight matched keywords.
4. **Rendering**: The tailored DOCX is converted to a branded PDF.
5. **Drafting**: `CoverLetterBuilder` and `EmailBuilder` generate the outreach texts.
6. **Delivery**: `GmailClient` sends the payload with attachments if `DRY_RUN=false`.
7. **Tracking**: `SheetClient` logs the application in Google Sheets and a local JSON/CSV backup is saved.

## Troubleshooting

- **Google Token Expired / Invalid**: Delete `token.json` and re-run `python authenticate.py`.
- **"Gmail OK" failed in `test` command**: Ensure you added your email as a "Test User" in the GCP OAuth consent screen if the app is still in testing mode.
- **Emails not sending**: Check if `DRY_RUN=true` in `.env`.
- **Missing modules**: Ensure you have activated your virtual environment and run `pip install -r requirements.txt`.

## Contributing
- **Adding Packs**: To add a new profession, create a `<role>.json` mapping keywords and synonyms.
- **Reporting Bugs**: This is a private tool, but fixes can be submitted via direct PRs to the main repository.

## License
UNLICENSED (private)
