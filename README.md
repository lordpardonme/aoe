# CareerHero Studio ⚡

> **An enterprise-grade, privacy-first AI application co-pilot and job search pipeline.**  
> Transform job specifications into verified 1-page resumes, draft human outreach pitches, scan inbound recruiter replies, and run autonomous batch queues—100% locally with zero cloud vendor lock-in.

---

## ✨ Features

- 🎯 **Leads Queue Hub**: Manage hundreds of target companies, agencies, and YC startups with category tabs, instant search, and status tracking.
- ⚡ **Autonomous Batch Engine**: Select batches of target companies to auto-synthesize tailored 1-page CVs and save outreach directly to your Gmail Drafts folder (`mail.google.com/mail/#drafts`).
- 📄 **1-Page Tailored Resumes**: Automatically budget content into a strict, pixel-perfect 1-page layout with verified ATS keyword matching.
- 🌍 **Country & Region Protocol Guard**: Adapts formatting and metadata for regional hiring norms (US/Canada 1-page no-photo standard, UAE/Saudi Arabia transferable visa & nationality protocols, UK/Europe standards).
- 📬 **7-Day Follow-Up Automation**: Automatically detects applications pending for 7+ days with zero recruiter response and generates high-converting, 2-sentence follow-up emails.
- 📥 **Inbound Gmail Scanner**: Classifies recruiter email responses into Interview requests, Technical assessments, Rejections, and Application reviews via the Gmail API.
- 🔒 **Privacy-First & Decoupled**: All profile information, leads, and application histories live in a local, offline SQLite database (`jobhunt.db`). Zero tracking data leaves your computer.
- 🛡️ **Activation Passkey Guard**: Configurable security passkey to prevent accidental live email dispatch.

---

## 🚀 Quick Start

### 1. Prerequisites
- Python 3.10+
- (Optional) Google Cloud OAuth client credentials for Gmail integration

### 2. Installation
```bash
git clone https://github.com/your-username/careerhero-studio.git
cd careerhero-studio/job-agent

# Create virtual environment
python -m venv .venv

# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 3. Launch the Studio
```bash
# From the root repository directory
python run_app.py
```
Open **`http://127.0.0.1:8000`** in your browser.

---

## ⚙️ Configuration & Environment

Copy `.env.example` to `.env` to configure optional API keys:
```bash
cp job-agent/.env.example job-agent/.env
```

| Key | Description | Default |
|---|---|---|
| `DRY_RUN` | Prevent external email sending (Safe Mode) | `true` |
| `LLM_PROVIDER` | AI Provider (`gemini`, `openai`, `claude`) | `gemini` |
| `LLM_API_KEY` | API Key for your LLM provider | `""` |
| `SENDER_EMAIL` | Authorized Gmail address | `""` |

---

## 🏗️ Architecture & Documentation

- **Architecture Decisions Log (ADR)**: See [`decisions.md`](decisions.md) for architectural trade-offs, library rationales, and full execution flow graphs.
- **Handoff Documentation**: See [`CAREERHERO_HANDOFF.md`](CAREERHERO_HANDOFF.md) for feature breakdowns and endpoint maps.

---

## 📄 License
MIT License. Free for personal and commercial use.
