# AGENTS.md — Job Hunt Workspace

**Read this file completely before doing anything.** It is the single handoff
document for this workspace. You should be able to resume work after one read.

---

## 0. Stop and read

This is **not a toy codebase**. It is live operational data for one person's real
job hunt:

- Scripts here **send real email** from a real Gmail account.
- A **live Google Sheet** is the tracker of record and is shared/visible to the user.
- The resumes describe a **real career**; fabricating a claim damages a real person.

Actions with real-world consequences (sending, sheet writes, pushes, deletions)
require **explicit user approval**. See §7.

**Owner:** Mohd Hayaat Ali — Product / UI-UX Designer and Creative (film, photography,
art direction), Delhi NCR, India.

---

## 1. Orient (first 60 seconds)

```bash
npm run verify          # asserts required paths exist
npm run agent:context   # prints the short operating brief
git status -sb          # see uncommitted work before touching anything
```

Then read, in order:

1. This file (all of it)
2. `Job Hunt/resumes/APPLICATION-WORKFLOW.md` — the pipeline in detail
3. `Job Hunt/resumes/candidate-profile.md` — identity and canonical links
4. `POLICY.md` — authority order and the four standing policies
5. `Job Hunt/AGENTS.md` — multi-agent pipeline + agency outreach workflow

---

## 2. Repo map

| Path | What it is |
|---|---|
| `Job Hunt/resumes/` | **The working directory.** Resume markdown, generated PDFs, email bodies, and the generator/sender scripts. `build_branded_pdf.py` is the default builder (see §6.3); `renderers/original/` holds preserved copies of the earlier renderers. |
| `job-agent/` | Python package wrapping Gmail + Sheets + Drive (OAuth lives here). |
| `job-automation-mcp/` | MCP server scaffold (package.json only; not yet implemented). |
| `reconciled-tracker-build/` | Tracker exports and Gmail reconciliation output. |
| `drive-extraction/` | OCR output and extracted lead evidence from screenshots. |
| `References and Resources/` | Supporting reference material. |
| `.planning/codebase/` | Architecture, conventions, stack, testing notes. |
| `scripts/` | Node helpers behind the `npm run` commands. |

---

## 3. Runtimes — which Python for which script

**There are two virtualenvs with different packages. Using the wrong one fails.**

| Runtime | Path | Has | Use for |
|---|---|---|---|
| Root venv | `.venv/Scripts/python.exe` | `reportlab`, `pypdf` | Building and verifying PDFs |
| Agent venv | `job-agent/.venv/Scripts/python.exe` | `google-api-python-client`, `google-auth` | **Sending email**, Sheets access |
| Node ≥18 | system | — | The `npm run` scripts |

Neither venv has the other's packages. Do not try to `pip install` across them —
just call the right interpreter.

Platform is **Windows**. A Bash tool (Git Bash) and PowerShell are both available;
each takes its own syntax. Paths contain spaces (`Job Hunt/`) — always quote them.

---

## 4. Credentials and tokens

**No secret values are stored in this file, and none may ever be committed.**
The repo pushes to GitHub; a leaked `gmail.send` refresh token is a live
send-email-as-the-user capability.

| What | Path | Tracked in git? |
|---|---|---|
| OAuth client (installed app) | `job-agent/credentials.json` | **No** — gitignored |
| User token (access + refresh) | `job-agent/token.json` | **No** — gitignored |
| Agent config | `job-agent/.env` | **No** — gitignored; template at `job-agent/.env.example` |

- **Sending account:** `hayaat0806@gmail.com` (this is the account `token.json`
  authorizes; it is not the same as the contact address on the resumes,
  `mohdhayaat1@outlook.com`).
- **Scopes on the token** (defined at `job-agent/src/config.py:31`):
  `gmail.send`, `gmail.readonly`, `spreadsheets`, `drive.file`.
- **Refresh** is automatic — both `send_application.py` and
  `job-agent/src/config.py` refresh an expired token from the refresh token.

**If the token is missing or cannot refresh:**

```bash
cd job-agent && .venv/Scripts/python.exe authenticate.py
```

This runs an interactive browser OAuth flow and rewrites `token.json`. It needs a
human — you cannot complete it headlessly. If you hit this, stop and tell the user.

**Verify credentials are still safely ignored** (should return nothing):

```bash
git ls-files | grep -iE "token.json|credentials.json|\.env$"
```

**Note on `DRY_RUN`:** `job-agent/.env.example` sets `DRY_RUN=true`, which gates the
`job-agent` CLI. It does **not** gate `send_application.py` — that script sends
immediately unless you pass `--dry-run`.

---

## 5. The live tracker (Google Sheet)

**Spreadsheet ID:** `1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI`

(The ID is not a secret — access is controlled by OAuth. Reach it with the
`mcp-gsheets` connector, or via `job-agent/src/sheet.py`.)

**10 tabs:** `Dashboard`, `Master Job Tracker`, `Agencies`, `Direct Employers`,
`LinkedIn Search`, `Phone WhatsApp`, `Sent By Me`, `Follow Ups`,
`Needs Manual Check`, `Social Leads Jul 2026`.

### Write targets and their exact columns

**`Master Job Tracker`** (A–N) — one row per lead, the master list:

| A | B | C | D | E | F | G |
|---|---|---|---|---|---|---|
| Country / Region | Company / Agency | Email | Type | Status | Date Applied | Follow-up Date |

| H | I | J | K | L | M | N |
|---|---|---|---|---|---|---|
| Notes | Opening Scan Status | Matched Role(s) | Opening Source URL(s) | Confidence | Recommended Action | Scan Date |

**`Sent By Me`** (A–K) — one row per outbound email:

| A | B | C | D | E | F |
|---|---|---|---|---|---|
| Company / Lead | Email(s) | Type | Status | Date Sent | Subject |

| G | H | I | J | K |
|---|---|---|---|---|
| Gmail Message ID | Tracker Match | Recommended Action | Source / Owner | Notes |

**`Social Leads Jul 2026`** (A–J) — leads sourced from screenshots/social:

| A | B | C | D | E |
|---|---|---|---|---|
| Source | Company | Role | Location | Contact |

| F | G | H | I | J |
|---|---|---|---|---|
| Date Seen | Verdict | Reason | Packet Status | Notes |

`Verdict` is one of: `APPLY`, `APPLY (user override)`, `HOLD`, `SKIP`,
`SCAM - EXCLUDED`, `ALREADY APPLIED`, `Research queue`.

**`Dashboard`** — mostly formula-driven; counts update themselves when rows are
appended. `B16` ("Latest Gmail sent by Mohd") is manual.

### Sheet rules

- **Append, don't overwrite.** Use `sheets_append_values` for new rows.
- **Never write a range you haven't read first.** Company-name guessing has
  already caused near-misses. Ground the exact row before any update.
- Preserve Gmail message IDs and evidence links — they're the audit trail.
- Nothing is marked `Applied` until the email has actually been sent.
- Sync the sheet **every 5 sends** rather than after every one.

---

## 6. The application pipeline

The canonical flow whenever a JD, job link, or screenshot arrives. Full version in
`Job Hunt/resumes/APPLICATION-WORKFLOW.md`.

### Content sources of truth — never drift from these

| File (in `Job Hunt/resumes/`) | Role |
|---|---|
| `candidate-profile.md` | Identity, phone/email, **all canonical links** (portfolio, live work, showreel). Pull links from here so they never rot. |
| `career-evidence-bank.md` | **Every claim must be backed here.** If it isn't in the bank, you may not write it. |
| `master-product-designer-cv.md` / `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` | Reference master. **Do not regenerate it.** |

### Two tracks — keep them separate

- **Product / UI-UX roles** → design-only resume. Do **not** add the
  film/photography/directing career.
- **Creative roles** (motion, video, editing, direction, photography, art
  direction) → lead with the creative career; design is supporting depth.
- **Irrelevant or unnamed role** (recruiter posts, "multiple openings") → pitch as
  Product Designer with the master CV.

Showreel: Drive folder linked in `candidate-profile.md`, confirmed shared
"anyone with the link can view."

### Steps

1. **Read the JD.** Extract role, skills, location, contact email.
2. **Invoke the `resume-tailoring` skill** — research the company, pick the angle.
3. **Draft `<slug>-resume.md`** from the master CV + evidence bank + profile links.
   Show the full relevant range; never undersell; never fabricate. Fuzzy facts stay
   generic until the user confirms them.
4. **Build the PDF** with the default builder (root venv). Pick the mode from
   §6.3 and check the country rules in §6.4 first:
   ```bash
   .venv/Scripts/python.exe "Job Hunt/resumes/build_branded_pdf.py" <slug>-resume.md <Output>.pdf "<PDF title>" --preset <brand> --country <cc>
   ```
   Expects `# Name` / `## Title` / contact lines / `## Professional Summary` /
   `## Core Skills` / `## Professional Experience` / `## Selected Live Work` /
   `## Education`. URLs auto-link. An optional `## What I'd Bring To <Company>`
   section renders as a highlighted card in branded mode.
5. **Invoke the `resume-ats-optimizer` skill** — check keyword match vs the JD and
   ATS-safe formatting. Fix gaps before sending.
6. **Write `<slug>-email.txt`** — short, specific, human. See §6.1.
7. **Send** (agent venv — the readable sender, never the `.pyc`):
   ```bash
   job-agent/.venv/Scripts/python.exe "Job Hunt/resumes/send_application.py" --to <email> --subject "<subject>" --body-file <slug>-email.txt --attachment <Output>.pdf
   ```
   Add `--dry-run` to build without sending. On success it prints the Gmail
   message ID — **capture it**, it goes in the sheet.
8. **Log it.** Append to `Master Job Tracker` and `Sent By Me`; update
   `Social Leads Jul 2026`. Sync every 5 sends.

### 6.1 Email voice

The user's standing instruction: *short, to the point, not generic, personal —
it should look like a person wrote it.* Concretely:

- First person, conversational, no corporate throat-clearing.
- Open with something specific to **their** post, not to you.
- No "I am writing to express my keen interest." No AI-slop cadence.
- Disclose blockers honestly and upfront (e.g. an SX Factor post said "priority to
  Malaysians" — the email said so in line two rather than hiding it).
- Links inline, CV attached, signature is name + phone + email. That's it.

### 6.2 Send-confidence policy

The user's setting is **auto-send high-confidence, hold the rest**:

- **Auto-send:** legit named company + a real stated opening + a branded contact
  address.
- **Hold for explicit approval:** vague or unnamed role, personal Gmail contact,
  brand/domain mismatch, stale post, or any scam marker.
- **Never send:** impersonation (fake Google/DreamWorks postings), CV-to-random-
  Gmail farms, anything demanding ID scans or registration fees. Mark
  `SCAM - EXCLUDED` in `Social Leads Jul 2026` and do not engage.

### 6.3 Which resume to send, and how to render it

**`build_branded_pdf.py` is the default builder.** `build_pdf_from_md.py` is the
legacy house style, kept as a fallback; originals are preserved in
`Job Hunt/resumes/renderers/original/`.

Decide in this order — the first match wins:

1. **Recruitment agency AND no JD supplied** → send
   `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` **as-is**. Do not build, do
   not regenerate, do not brand. This is the standing default for agencies.
2. **Check §6.4 country rules.** They can veto branding outright.
3. **JD supplied** → draft `<slug>-resume.md`, then choose:
   - **Creative target** — café, studio, DTC brand, production house, small
     creative team; or any motion / video / photography / art-direction / brand
     role → **branded mode**.
     ```bash
     ... build_branded_pdf.py <slug>-resume.md <Out>.pdf "<title>" --preset nubo
     ... build_branded_pdf.py <slug>-resume.md <Out>.pdf "<title>" --accent "#0058A3" --font clean
     ```
   - **Corporate, enterprise, bank, real ATS, or any recruitment agency** →
     **ATS mode**: `--ats --preset mono` (flat black).
4. **No JD, direct employer, vague or unnamed role** → master CV, per the
   "irrelevant or unnamed role" rule above.

**Benchmark:** `Mohd_Hayaat_Ali_Marketing_Head_nubo.pdf` for creative,
`..._Randstad.pdf` for ATS, `..._IKEA.pdf` for a corporate-but-branded middle.
Use them as reference for *quality*, not as templates — **research each company
fresh; do not clone a previous build.**

**Colour.** One verified hex drives accent, card tint, page wash, rules and
bullet marks. Take it from the company's own site or brand material. **Never
guess** — a near-miss reads as failed impersonation, which is worse than
neutral. Unverified → `--preset default`. A contrast guard darkens light accents
automatically so brand hue never costs legibility.

**Typeface.** Search for the company's actual typeface first; use it if a system
equivalent exists. Otherwise pick the closest pairing: `grotesque` (Arial Black
+ Segoe UI), `clean` (Segoe UI Bold + Segoe UI), `condensed` (Bahnschrift).
Record which case applied in the tracker Notes, and never claim a match that
wasn't verified. *Poppins, Montserrat and Inter are not installed — installing
those three free Google Fonts is the single highest-value upgrade to output
quality.*

**Readability is the point.** Body 9.8pt/15 leading, bullets 9.5/14.6, generous
margins. **Two to three pages is correct; cramping to fit fewer is not.** Role
blocks never split, section headings never orphan, and the highlighted card
flows across a page break with its background intact.

**ATS mode** drops tinted cards, tables, page wash and arrow glyphs; keeps the
accent on headings and links, standard `•` bullets, flat single column.

**Verification is visual.** Page count is not proof. Rasterize with PyMuPDF
(~100 dpi) and *look* at every page before sending — this workspace has shipped
broken layouts (centre-floating rules, orphaned headings, a card leaving a hole)
that page counts passed cleanly.

### 6.4 Country and region CV rules

Local convention is not cosmetic — a photo where one is unexpected creates bias
exposure and can get the CV binned unread; no photo where one is expected reads
as incomplete. `build_branded_pdf.py --country <cc>` enforces this and will
**refuse** rather than silently comply.

| Region | Photo | Notes |
|---|---|---|
| **US / Canada** (`us`, `ca`) | **Never** | "Resume", 1–2pp. No DOB, marital status or nationality. |
| **UK / Ireland / Netherlands / Australia** (`uk`,`ie`,`nl`,`au`) | No | "CV", 2pp. Contact details only. |
| **Germany** (`de`) | **Expected** | *Lebenslauf*. Headshot top-right ~35×45mm, tabular reverse-chronological. AGG makes it optional in law; the expectation persists in practice. |
| **UAE / Saudi / Oman / Qatar** (`ae`,`sa`,`om`,`qa`) | **Expected** | Include nationality and visa status; detailed role descriptions. |
| **Japan** (`jp`) | **Expected** | *Rirekisho* (fixed standard form) **plus** *shokumu keirekisho* (work history). **Design creativity is not appreciated — never send a branded resume.** The builder refuses branded mode for `jp`. |
| **France** (`fr`) | Expected | Photo customary. |
| **India** (`in`) | Optional | 1–2pp. Workspace default. |

Country not listed → omit the photo, use the neutral 2-page format. **Doubt
resolves to omission.**

**Blocker to raise with the user:** there is no headshot in this workspace.
Germany, Gulf, Japan and France applications need one (`--photo <path>`, sized
automatically). Ask for a formal headshot rather than quietly sending a
photo-less CV into a photo-expecting market.

---

## 7. Hard rules

**Activation.** Do not start any job-hunt work — agent spawning, research,
drafting, tracker updates, follow-ups — unless the user's first command contains
the exact, case-sensitive standalone phrase `OrchardLab47`. Near-matches and
partial words do not count. Without it, stay idle.

**External actions need explicit user intent:**

- Gmail sends and draft creation
- Live Google Sheet edits
- GitHub pushes
- File deletions

**`wait`, `pause`, and `do not send` are hard stops.** Stop immediately.

**Never:**

- Run the `job-agent` `.pyc` bytecode. It is unauditable, generates its own
  content, and risks double-applying. Readable scripts only.
- Fabricate experience, metrics, companies, clients, projects, or domain
  expertise. Reframing adjacent real experience is fine; inventing is not.
- Write to the live sheet without grounding the exact rows/ranges first.
- Trust a stale local CSV when live Gmail or live Sheets can verify state.
- Commit secrets, tokens, `.env` files, virtualenvs, or nested git metadata.
- Delete user files without explicit approval and a verified target.
- Mass-send to agencies. One target at a time unless the user asks for a batch.

**Authority order when sources disagree** (from `POLICY.md`):

1. Latest explicit user instruction
2. Live Gmail (sent/received state)
3. Live Google Sheet (tracker state)
4. Local reconciled workbook/CSV
5. Older recovered context and memory

---

## 8. Skills — install these before working

This workspace depends on 7 installed skills. They are managed by
[`npx skills`](https://github.com/vercel-labs/skills) (Vercel Labs), which supports
claude-code, codex, cursor, copilot, gemini, opencode, windsurf, kilo, roo, goose,
amp, droid, trae, and others — so any agentic platform can install them.

### Install everything (one command per source)

```bash
npx skills add varunr89/resume-tailoring-skill -s resume-tailoring -a '*' -y
npx skills add paramchoudhary/resumeskills -s resume-ats-optimizer -a '*' -y
npx skills add erichowens/some_claude_skills -s cv-creator -a '*' -y
npx skills add juliusbrussee/caveman -s caveman,caveman-compress,caveman-stats -a '*' -y
npx skills add vercel-labs/skills -s find-skills -a '*' -y
```

`-a '*'` installs to every agent directory found; `-y` skips prompts. Drop `-a '*'`
and pass e.g. `-a claude-code` or `-a codex` to target one platform. Verify with
`npx skills list`.

### Or restore from the lock files

```bash
npx skills experimental_install
```

**Caveat:** this reads `skills-lock.json` from the current directory, and this repo
has **two** — the root one pins only `caveman`, `caveman-stats`, `find-skills`,
while `Job Hunt/skills-lock.json` pins the job-critical `resume-tailoring`,
`resume-ats-optimizer`, `cv-creator`, `caveman-compress`. Running it from the repo
root alone will **not** get you the resume skills. Either run it in both
directories, or just use the explicit `add` commands above.

### What each skill is for

| Skill | Source (GitHub) | Used for |
|---|---|---|
| **`resume-tailoring`** | `varunr89/resume-tailoring-skill` | **Required** — pipeline step 2. Research the company/role and pick the resume angle before drafting. |
| **`resume-ats-optimizer`** | `paramchoudhary/resumeskills` | **Required** — pipeline step 5. Check keyword match vs the JD and ATS-safe formatting before every send. |
| `cv-creator` | `erichowens/some_claude_skills` | Full CV builds and multi-format export. Optional — the master CV already exists; do not regenerate it. |
| `caveman-compress` | `juliusbrussee/caveman` | Compress a handoff note or generated artifact that has grown too large to stay readable. |
| `caveman` / `caveman-stats` | `juliusbrussee/caveman` | Token-compressed communication mode and its usage stats. Opt-in; see `Job Hunt/AGENTS.md`. |
| `find-skills` | `vercel-labs/skills` | Discover and install additional skills when a task needs capability that isn't here. |

The two marked **Required** are non-negotiable steps in §6. The rest are available
but not part of the send path.

---

## 9. Git

- Repo is **private**: `git@github.com:lordpardonme/job-hunt-workspace-private.git`
- Working branch: `feature/ai-job-application-agent` → PRs to `main`
- Commit meaningful checkpoints with clear messages; keep changes scoped.
- Avoid destructive git commands unless the user explicitly asks.
- Before any command that could discard uncommitted work, run `git status` and
  stash (`-u`) or commit first.

---

## 10. Current state — as of 2026-07-30

| Metric | Value |
|---|---|
| Total leads in `Master Job Tracker` | 309 rows |
| Applied | 96 |
| To contact | 202 |
| `Sent By Me` rows | 204 |

**Last batch:** 11 applications sent 2026-07-30, all logged to `Master Job Tracker`
(rows 299–309), `Sent By Me`, and `Social Leads Jul 2026`:

daysahead.in · DropJ Supply · Filter Coffee Co · Shut Up We Are Talking ·
Purple Oceans · Cerise Patisserie · DAUD Run Club · SX Factor · Designsfield ·
Retailer Sarathi · Infoneo Global

**Open threads to pick up:**

- **Purple Oceans** — application deadline **2026-08-06**.
- **Cerise Patisserie** — the email offered to shoot three reels specifically for
  their product. If they say yes, **the user has to film them.** Do not fabricate
  or substitute generic reels.
- **DAUD Run Club** — the source post was old; the email asked whether the role is
  still open. Low confidence.
- **Follow-ups** — the 2026-07-30 batch is all due **2026-08-06**.
- **Dubai list** — `Social Leads Jul 2026` holds a reference block of ~28 Dubai/UAE
  companies that are **careers-portal only, not email-apply**. Roughly 22 more from
  that list are already tracked. Do not email the portal-only ones.

**Also sent 2026-07-30:** nubo (eatnubo), `hello@eatnubo.com`, Gmail id
`19fb34cd32edb51b` — 360 Marketing Head, first application built with the
branded renderer.

**Sheet note:** the Master Job Tracker was re-sorted and de-duplicated on
2026-07-30 (325 → 313 rows, duplicates only — nothing lost) and the Dashboard was
rebuilt with new metric labels. **Every "Master row N" reference in older Notes
is now stale.** Gmail message IDs are the reliable key.

Update this section whenever you finish a batch, so the next agent starts current.
