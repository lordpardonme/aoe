# Technology Stack Architecture & Rationale
## CareerHero Studio — Technical Stack Specification

**Last Updated:** September 14, 2026  
**Project Location:** `G:\job-hunt-app`  

This document provides a comprehensive technical overview of every technology, runtime, library, and API utilized across CareerHero Studio, explaining what each is used for and why it was chosen.

---

## 1. Core Runtime & Backend Services

| Technology | Version | Purpose in Application | Technical Rationale |
|---|---|---|---|
| **Python** | 3.11.x | Primary execution engine | Native asynchronous support (`asyncio`), high-performance data processing (`pandas`), and mature AI/ML ecosystem. |
| **FastAPI** | 0.141.1 | High-performance asynchronous REST API | ASGI standard, automatic OpenAPI documentation, dependency injection, and native support for background tasks. |
| **Uvicorn** | 0.52.4 | Lightning-fast ASGI web server | Low-latency asynchronous request processing with threadpool concurrency. |
| **SQLite3** | 3.x (Embedded) | Local-first relational database | Zero external database server overhead, instant startup, ACID transactional safety, and full offline autonomy. |
| **Pydantic** | 2.13.5 | Strict data schema validation | High-speed data serialization and request/response validation using Rust-powered core. |

---

## 2. Ingestion, Scraping & Aggregation Engine (`src/scraper/`)

| Technology | Purpose in Application | Technical Rationale |
|---|---|---|
| **python-jobspy** | Aggregated scraping across LinkedIn, Indeed, Glassdoor, Google Jobs, ZipRecruiter, and Bayt | Standardizes multi-board scraping protocols with rotating headers and TLS fingerprint emulation. |
| **Pandas** | High-volume job record normalization & tabular transformation | Vectorized operations for salary parsing, date conversion, and fuzzy deduplication. |
| **PyYAML** | Configuration parser for roles, sources, locations, and settings | Clean human-readable taxonomies for target job families and negative keyword exclusions. |
| **Requests & HTTPX** | Direct REST requests to zero-auth job APIs and ATS boards | Synchronous and asynchronous HTTP clients handling retries, timeouts, and JSON parsing. |
| **BeautifulSoup4 & lxml** | HTML description parsing & text sanitization | Converts rich HTML job descriptions into clean plaintext for LLM prompting and keyword matching. |

---

## 3. Zero-Authentication Public APIs (100% Free, Zero Key, Zero Auth)

| API | Base Endpoint | Purpose in CareerHero |
|---|---|---|
| **Kickbox Open API** | `open.kickbox.com/v1/verify` | Real-time deliverability and syntax verification for hiring manager emails to prevent bounces. |
| **Disify API** | `disify.com/api/email/` | Disposable email detection ensuring recruiter contacts are real enterprise domains. |
| **Arbeitnow API** | `arbeitnow.com/api/job-board-api` | Zero-auth JSON feed for verified remote and European tech/design postings. |
| **freehire API** | `freehire.dev/docs/api` | Direct company ATS board aggregator (Greenhouse, Lever, Workable, Ashby). |
| **RemoteOK API** | `remoteok.com/api` | Public real-time JSON stream of global remote design and tech roles. |
| **Remotive API** | `remotive.com/api/remote-jobs` | Curated remote jobs categorized by design, development, and product. |
| **REST Countries** | `restcountries.com` | Country metadata used to trigger regional CV protocols (e.g. photo vs no photo). |
| **Frankfurter API** | `frankfurter.app/docs` | European Central Bank exchange rates for salary normalization across USD, EUR, GBP, AED, INR. |

---

## 4. Document Generation & PDF Typography

| Technology | Version | Purpose in Application | Technical Rationale |
|---|---|---|---|
| **ReportLab** | 5.0.1 | Programmatic single-page PDF CV generation | Pixel-perfect layout engine with dynamic leading calculation, Bahnschrift font support, and WCAG AA contrast compliance. |
| **python-docx** | 1.2.0 | Microsoft Word resume export | Enables export to editable `.docx` formats for agencies requiring raw Word files. |
| **Pillow (PIL)** | 12.3.0 | Image processing and headshot cropping | High-quality circular headshot cropping and resizing for Middle East regional CVs. |

---

## 5. Front-End Interface & Dashboard

| Technology | Purpose in Application | Technical Rationale |
|---|---|---|
| **HTML5 & Vanilla JavaScript** | Single-Page Application (SPA) architecture | Zero compilation steps, zero Node.js dev server lag, instant client-side rendering. |
| **Tailwind CSS (CDN)** | Utility-first responsive styling | Modern dark/light UI design system, compact styling footprint, and accessible color tokens. |
| **Lucide Icons** | Visual UI iconography | Clean SVG icons for actions (Apply, Follow-up, Verify, Settings, Play/Pause). |

---

## 6. Email Integration & Security

| Technology | Purpose in Application | Technical Rationale |
|---|---|---|
| **Google API Client** | Gmail OAuth 2.0 & message dispatch | Official Google SDK for managing drafts, sending emails, and scanning inbound replies. |
| **Activation Passkey Guard** | Hard safety lock gating live dispatches | Cryptographic passkey gating live dispatches to prevent unintended email sending. |
| **Local-First Secret Isolation** | Gitignored `.env`, `credentials.json`, `token.json` | Complete privacy guarantee ensuring sensitive data never touches cloud repos. |
