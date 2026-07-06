# Job Hunt Aim and Workflow

## User Aim

Get Product Designer / Senior Product Designer opportunities, especially in UAE/Dubai and relevant remote/relocation roles, using stronger evidence from real shipped product work instead of generic CV bullets.

Primary job-hunt focus:
- Product Designer / Senior Product Designer
- UI/UX Designer
- Digital Product Designer
- SaaS / fintech / operations dashboard roles
- UAE/Dubai, agencies, direct employers, and relevant startup/product companies

## What Last Night Was About

The work was about rebuilding job applications around real career evidence:
- recover and preserve FuelBuddy product work from old conversations and screenshots
- build a strong master CV/evidence bank
- create tailored CVs for specific companies/agencies
- run ATS-style checks when useful
- draft application emails
- maintain the tracker sheet
- send applications only after explicit approval

## Multi-Agent Pipeline

Use one orchestrator plus specialists so queue control stays separate from research and writing.

Activation gate:
- exact phrase `OrchardLab47`
- case-sensitive
- standalone first command in a new Codex chat
- if absent, do not start job-hunt work
- on activation, switch to caveman first, then run the agents

1. Orchestrator / queue selector
   - checks tracker state and Gmail sent history first
   - picks the next single agency or direct employer
   - routes the target to the right specialist
2. Contact research agent
   - verifies what the target actually does
   - finds credible public contacts from the sheet, public web, and publicly visible social profiles only
   - returns source notes and confidence
3. CV tailor agent
   - rewrites the CV for the selected target
   - keeps the evidence truthful and sector-matched
   - produces a unique CV variant, not a generic master resume
4. Email draft agent
   - writes the short non-generic outreach email
   - keeps tone senior, direct, and calm
5. Compile / approval packet agent
   - bundles research, recipients, CV angle, email draft, and attachment name
   - shows the user what would be sent before any outbound action
6. Self-send reconciler agent
   - detects messages the user sent outside the workflow
   - mirrors them back into the tracker with the right status and notes
7. Follow-up agent
   - watches the follow-up date
   - checks for replies first
   - sends the follow-up automatically when the original outreach is already logged, the thread is quiet, and the contact is not flagged do-not-contact

Reference artifacts:
- CV screenshot: use as the layout reference for a one-page, high-signal CV with header, summary, experience, education, awards, and skills.
- Email screenshots: use as the tone and structure reference for warm referral, follow-up, networking, and applied-to-role notes.
- Do not copy personal details or literal wording. Use structure, sequencing, and tone only.

Source hierarchy:
- tracker sheet
- Gmail sent / reply history
- public web
- publicly visible social profiles

Workflow rule:
- one target at a time
- no blind mass sending
- no tracker write from memory alone
- approval still comes before the first outbound send

Tracker sync rule:
- write to the local staging page first
- batch-sync online tracker after 10 to 15 applications, or on explicit user request
- when syncing, mark applied across every relevant sheet/view
- keep person-specific outreach in the same ledger

## Core Resume Evidence

### FuelBuddy

Use FuelBuddy as strongest evidence for fintech, logistics, operations, B2B SaaS, fleet, fuel/energy, and dashboard-heavy roles.

Facts recovered:
- Wallet/payment UX work reduced transaction errors by 38%.
- Multi-wallet user feature let a main user add/delegate users, allow wallet use, and set wallet/spend limits.
- Business account surface for registered business partners included orders, fuel storage, asset fill state, wallet, assigned users, delegation, access, and credit limits.
- Business wallet screens show wallet balance, overdue/outstanding amount, credit/remaining limit, order history, invoice/money-added tabs, quantity charts, order filters, user management, asset management, shipping address, and billing address editing.
- Dubai B2B customer app was a web app for business customers, not India-style consumer delivery. It supported tracking and business-side fuel operations.
- Franchise dashboard for Dubai/India included map dashboard, live truck tracking, order list, order details, and delayed-order states.
- Auto Bay / assets page was a desktop web flow for gensets, cars, trucks, and other fuel-storing assets. It is distinct from Arjun.
- Auto Bay screens show add-asset flow, OTP/validation/error states, asset details, documents, driver behavior / Great Driving view, and modal states.
- Consumer app redesign simplified diesel doorstep ordering from a 20-22 step flow into location, quantity, date/time, and payment. Use metric: order completion 62% -> 78%.
- Support/ticketing tool reduced manual input 43% and improved ticket handling/resolution 57%.
- Wheels driver app covered assigned truck, QR scan, shift logging, and documents such as driving license and Emirates ID.
- FuelBuddy design system was built from scratch.

### Meddo / Uncover / Doxper

Use for healthcare, booking, patient/doctor, back-office, usability, and design-system roles.

Facts:
- Redesigned Meddo 2.0 across patient app, doctor app, and back-office/backend software.
- Metrics: booking 71% -> 83%, doctor profile views +28%, appointment requests +15%.
- Designed Uncover logo and brand foundation when Meddo shifted to Uncover.
- Worked on Doxper doctor interfaces with pen/tablet digitization.
- Worked on Meddo Sarthi membership product and ABHA health ID integration interfaces.
- Built/upgraded Meddo design system.

### Other Evidence

- AcadPlaza: search/catalog UX, marketplace learning flows, discovery/booking/payment, detail pages, conversion.
- I-DOD: design system from scratch; do not imply fully launched product.

## Tailoring Rules

- Fintech/payments role: lead with FuelBuddy wallet, payment-error reduction, multi-wallet delegation, wallet limits, trust/payment UX.
- Energy/logistics/oil role: lead with FuelBuddy franchise ops, B2B fuel operations, live tracking, fleet/assets, dashboards.
- Healthcare role: lead with Meddo, doctor/patient/back-office flows, booking metrics, usability.
- Real estate/marketplace role: lead with AcadPlaza/search/catalog/consumer marketplace UX.
- Agency role: tailor CV by agency specialization, not by a fake JD.
- Each agency CV should have a skills block and summary that mirror the agency's hiring sector.
- Email copy should sound like a direct request for help finding the right role, not a generic application blast.
- Close with a respectful ask such as "I’d appreciate being considered for relevant openings" rather than a hard sell.

## Outreach Rules

Use controlled one-by-one outreach:
1. Pick one agency/job from tracker.
2. Research agency/company focus.
3. Find credible recipient email and CC only if reliable.
4. Create unique tailored CV angle.
5. Draft short non-generic email.
6. Show user:
   - research summary
   - recipients and CC
   - tailored CV angle
   - email draft
   - attachment name
7. Wait for explicit approval.
8. Only after approval:
   - send email
   - mark the local staging tracker as Applied
   - add Date Applied
   - add Follow-up Date
   - add Gmail sent ID if available
   - add notes about CV version sent
   - create/update follow-up reminder/task
   - queue the record for the next online batch sync instead of writing live immediately

## Assistant Aim

Give user stronger, truthful job applications:
- master CV/evidence bank from real work
- tailored CVs per role/agency
- ATS-aware wording
- clean PDF attachments
- short credible emails using the senior/direct voice in `email-and-copywriting-playbook.md`
- tracker kept current
- no blind mass sending
- no sending without approval

## Recovered Source Files

- `resumes/career-evidence-bank.md`
- `resumes/recovered-context/resume-memory-rebuild.md`
- `resumes/recovered-context/recovered-job-hunt-context.md`
- `resumes/recovered-context/email-and-copywriting-playbook.md`
- `resumes/recovered-context/content-generation-role-charters.md`
- `resumes/recovered-context/screenshots/`
