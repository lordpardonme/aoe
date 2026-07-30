# Default Application Pipeline (JD / link → tailored packet → send)

This is the standard workflow whenever a JD or a job link is submitted. Follow it
every time. Use the installed job-hunt skills at the marked steps.

## Sources of truth
- **Identity + links:** `candidate-profile.md` (portfolio, live-work links, showreel,
  phone/email, the two tracks). Always pull links from here so they never drift.
- **Claims:** `career-evidence-bank.md` (design track + the Creative Direction /
  Film / Photography section). Never claim anything not backed here.
- **Master resume:** `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` /
  `master-product-designer-cv.md` — reference, do not regenerate.

## Two tracks (keep separate)
- **Product / UI-UX / Product Designer** roles → design-only resume. Do NOT add the
  film/photography/directing career.
- **Creative** roles (motion, video, editing, direction, photography, art direction)
  → lead with the creative career; design is supporting depth.

## Steps
1. **Read the JD/link.** Extract role, required skills, location, contact email.
2. **Invoke `resume-tailoring`** (skill) — research the company/role, pick the angle.
3. **Draft `<slug>-resume.md`** from master CV + evidence bank + candidate-profile
   links. Show the full relevant range; never undersell. Never fabricate — fuzzy
   facts stay generic until confirmed.
4. **Generate the PDF** with the default builder:
   `python build_branded_pdf.py <slug>-resume.md <Out>.pdf "<title>" --preset <brand> --country <cc>`
   Pick branded vs `--ats` mode and check country rules per **AGENTS.md §6.3/§6.4**
   — that is the authoritative version, do not let these two diverge.
   `build_pdf_from_md.py` is the legacy house style, kept as a fallback.

   **Before any of this:** a recruitment agency with no JD gets
   `Mohd_Hayaat_Ali_Master_Product_Designer_CV.pdf` as-is. Do not build.
5. **Invoke `resume-ats-optimizer`** (skill) — verify keyword match vs the JD and
   ATS-safe formatting before sending. Fix gaps.
6. **Write `<slug>-email.txt`** — tight, JD-specific, references the relevant
   credits + showreel/portfolio/live links from candidate-profile.
7. **Send** with the readable sender (never the job-agent .pyc bytecode):
   `python send_application.py --to X --subject "Y" --body-file <slug>-email.txt --attachment <Out>.pdf`
   - Runs from the **job-agent venv** (`job-agent/.venv/Scripts/python.exe`) which has
     googleapiclient. Uses `job-agent/token.json` (hayaat0806@gmail.com, gmail.send).
   - **Send flow = auto high-confidence, hold the rest** (user setting). Legit company
     + real opening + reasonable contact → auto-send. Vague role / personal Gmail /
     brand-email mismatch / scam markers → pause for the user's OK.
8. **Log to the sheet:** append to `Master Job Tracker` (Applied, date, follow-up,
   Gmail message ID) and `Sent By Me`; update `Social Leads Jul 2026` status. Sync
   the sheet every 5 sends. Nothing marked Applied until actually sent.

## Guardrails
- Never run the job-agent `.pyc` bytecode (unauditable; generates its own content;
  risks double-applying). Readable scripts only.
- `job-agent/credentials.json` + `token.json` are live secrets — keep gitignored,
  never commit.
- Confirm the showreel Drive folder is shared "anyone with the link can view."
