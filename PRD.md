# Product Requirements Document (PRD)
## CareerHero Studio — Autonomous Career Intelligence & High-Conversion Application Copilot

**Version:** 2.0.0  
**Status:** Active Execution  
**Target Environment:** Local-First Windows (Python 3.11, FastAPI, SQLite3, ReportLab)  
**Last Updated:** September 14, 2026  

---

## 1. Product Overview & Vision

CareerHero Studio is a standalone, local-first, autonomous AI co-pilot designed to streamline and accelerate the job acquisition lifecycle for senior professionals and specialists. 

The application unifies multi-channel job market discovery, zero-auth public data verification, automated query expansion, visa/relocation scoring, single-page CV compilation, conversational cold outreach drafting, and inbound recruiter intent classification into a single privacy-preserving workstation tool.

### Core Philosophy
1. **Zero Privacy Leak:** SQLite database, OAuth tokens, personal identifiers, and credentials remain strictly local-first and gitignored.
2. **High-Conversion Quality over Spam:** 1-page CVs tailored to exact JD taxonomy with single-page layout budgeting (Bahnschrift typography, WCAG AA contrast).
3. **Safe Mode First:** All scraping and outreach operations default to safe/dry-run mode. Live external dispatches require explicit user activation passkeys.
4. **Zero-Auth External Integration:** Reliance on 100% free, zero-authentication public APIs and open ATS endpoints to minimize third-party friction and costs.

---

## 2. User Personas & Target Job Families

* **Primary Candidate:** Senior Product Designer / Founding Designer / UI-UX Lead / Full-Stack Engineer actively targeting high-tier remote roles and regional hubs (India, Middle East / UAE / Dubai, and Global).
* **Target Roles:** Product Designer, Senior Product Designer, Staff Designer, UX/UI Lead, Founding Designer, Design Systems Lead, Frontend Engineer, Data Scientist.
* **Excluded Noise:** Graphic Designer, Fashion Designer, CAD/Interior Designer, 3D Artist, Mechanical Designer.

---

## 3. Functional Requirements

### FR-1: Multi-Channel Job Discovery & Scraping Engine
* **AuraJobs Integration:** Native embedding of the `D:\JobSpy` scraping pipeline into `job-agent/src/scraper/`.
* **Aggregator Adapters:** MultiBoard scraping for LinkedIn, Indeed, Glassdoor, Google Jobs, Bayt, and Naukri.
* **Direct ATS Adapters:** Direct API and crawler querying of Greenhouse, Lever, and AshbyHQ boards.
* **Zero-Auth API Feeds:** Clean REST integration with Arbeitnow (Remote/EU), Remotive, freehire, and RemoteOK.
* **Query Expansion:** Dynamic role taxonomy expansion into 30+ semantic variants per job family.
* **Deduplication:** SHA256 content hashing (`company` + normalized `title`) ensuring zero duplicate leads in the database.
* **Freshness Filtering:** Hard windowing to postings <= 72 hours old.
* **Visa & Relocation Analysis:** Regex and NLP detection of sponsorship/relocation mentions.

### FR-2: Verification & Deliverability Protection
* **Email Deliverability Verification:** Integration with Kickbox Open API and Disify API to verify corporate email addresses, detect burner domains, and check MX records before outreach staging.
* **Regional Rules Engine:** Integration with REST Countries to enforce country-specific CV standards (e.g., photo for UAE, strictly no photo for US/UK/Canada).
* **Currency Normalization:** Integration with Frankfurter API to standardize multi-currency salary figures into target currency CTC equivalents.

### FR-3: Leads Queue Hub & Local Relational Storage
* **SQLite Storage (`tracker/jobhunt.db`):** Relational schema isolating `leads`, `applications`, `inbound_replies`, `ingestion_runs`, and `profile`.
* **Categorized Queue:** Filterable tabs by Category (`Direct`, `YC Startups`, `Agency`, `Social`, `Scraped Feed`) and Status (`To Contact`, `Drafted`, `Applied`, `Interviewing`, `Rejected`).
* **Row Actions:** Contextual actions per row: `✨ Apply`, `📬 Follow-up`, `↺ Re-apply`, `✓ Verify Email`.

### FR-4: Agentic Intelligence & Synthesis Layer
* **Single-Page CV Generator:** ReportLab 5.0.1 engine enforcing strict 1-page layout budgeting with dynamic leading, margins, and Bahnschrift font metrics.
* **First-Reader Simulation:** Attention audit scoring cold emails and cover letters for hook strength, conciseness (<120 words), and readability drop-off points.
* **Stalled Lead Autopsy (Project Graveyard Pattern):** Automatic diagnosis of unreplied applications >= 14 days old (e.g. "Ghosted After First Touch", "ATS Rejection").

### FR-5: Dispatch & Inbound Recruiter Hub
* **Gmail In-Browser OAuth:** Single-click browser authorization saving encrypted local tokens.
* **Drafts or Live Dispatch:** One-click generation directly to Gmail Drafts or live dispatch behind an Activation Passkey.
* **Inbound Recruiter Scanner:** Scans Gmail API for incoming responses, classifying intent (`Interview`, `Assessment`, `Rejection`, `Follow-up`) and confidence scoring.

---

## 4. Non-Functional Requirements

1. **Performance:** Express scrape runs finish in < 90 seconds; Deep multi-board runs complete within 10 minutes with intermediate checkpoints every 10 searches.
2. **Reliability:** Individual source failures (e.g., Naukri 406 CAPTCHA or Glassdoor 400) must fail gracefully and not terminate the pipeline.
3. **Privacy:** Zero personal data or credentials committed to Git. Local database `jobhunt.db` and credential files are strictly gitignored.
4. **Usability:** Single-Page Application (SPA) responsive interface with Tailwind CSS, real-time progress indicators, and zero external build tool dependencies.

---

## 5. Success Metrics

* **Zero Duplicates:** 100% suppression of duplicate job leads across continuous scraping runs.
* **Zero Bounce Rate:** >95% valid email deliverability on dispatched outreach via Kickbox pre-flight verification.
* **Time to Apply:** < 30 seconds to generate a tailored 1-page CV and conversational cold outreach draft for any newly discovered lead.
