# Project Instructions

> **Read the root `AGENTS.md` first.** It is the complete handoff document —
> credentials, runtimes, tracker schemas, the send pipeline, hard rules, and
> current state. This file covers only what it does not: communication defaults,
> the activation gate, batch staging, and the multi-agent / agency workflows.

## Default Communication

Use the job-hunt skill stack by default for resume and application work: `resume-tailoring`, `cv-creator`, and `resume-ats-optimizer`. Keep technical accuracy, commands, code, file paths, warnings, and verification details intact. Use `gmail` and `google-sheets` only when the task specifically requires email sending/searching or tracker reads/writes. Use `caveman-compress` when a note, handoff, or generated artifact gets too large to stay readable. Use normal clarity only when terse fragments could cause risk or confusion. Stop only when user says `normal mode` or explicitly asks for a different style.

## Activation Trigger

Do not start any job-hunt work, agent spawning, research, drafting, tracker updates, or follow-up actions unless the user's first command contains the exact, case-sensitive standalone phrase `fuck this shit`.

- If the phrase is absent, stay idle and do nothing job-hunt related.
- If the phrase is present, switch to caveman style first, then treat it as the single start signal for the current session and begin from the orchestrator / queue selector.
- Do not treat near-matches, partial words, or the phrase inside a longer unrelated sentence as valid activation.

## Staging And Sync

Use one local staging page/folder for the current batch.

- Record sends locally first.
- Do not push tracker writes online after every send.
- Batch-sync online tracker data after 10 to 15 applications, or sooner only if the user explicitly asks to sync now.
- When syncing, reconcile the full tracker surface, not just one tab:
  - master tracker
  - agency views
  - direct employer views
  - follow-up views
  - any person-specific outreach rows
- Mark applied everywhere the lead appears.

## Multi-Agent Job Hunt Pipeline

Use a coordinator-plus-specialists pattern for outreach and tracker maintenance.

- Orchestrator / queue selector: choose the next agency or direct employer by checking the tracker and Gmail sent history first.
- Contact research agent: find credible contact names and public email addresses from the sheet, public web, and publicly visible social profiles only.
- CV tailor agent: create a unique CV for the selected agency, company, or role.
- Email draft agent: write the short, non-generic outreach email.
- Compile/review agent: bundle research, recipients, CV angle, draft, and attachment name for user review.
- Self-send reconciler agent: detect messages the user sent outside the workflow and mirror them into the tracker.
- Follow-up agent: send the scheduled follow-up automatically on the assigned date once the original send is already logged and the contact is not flagged do-not-contact.

Use a GSD-style coordinator/worker loop for multi-step outreach. Do not collapse the whole pipeline into one generic pass when the work can be split cleanly.

## Agency Outreach Workflow

For recruitment agency outreach, use a controlled agency-by-agency workflow. Do not mass-send blindly.

1. Pick one agency from the tracker sheet.
2. Research that agency:
   - sectors they hire for
   - whether they focus on IT, fintech, oil and gas, real estate, hospitality, enterprise, outsourcing, healthcare, logistics, or other domains
   - whether they place Product Designer, UI/UX, digital, tech, SaaS, fintech, or related roles
   - relevant recruiter or contact person if available
3. Find better contact emails if possible:
   - use the agency inbox from the sheet
   - add recruiter/person email only when discoverable and credible
   - CC relevant people only when credible
4. Create a unique CV for that agency, not a generic CV:
   - tech/IT agency: emphasize product design, SaaS, fintech, dashboards
   - oil/energy/logistics agency: emphasize FuelBuddy, fleet, operations, dashboards
   - real estate agency: emphasize marketplace/search/catalog and consumer UX
   - healthcare agency: emphasize Meddo, booking flows, usability testing
   - fintech agency: emphasize wallet, payment UX, KYC, transaction-error reduction
5. Draft a short non-generic email.
6. Show the user before sending:
   - agency research summary
   - chosen recipients and CC
   - tailored CV angle
   - email draft
   - attachment name
7. Ask for explicit approval: go ahead or do not send.
8. Only after approval:
   - send the email
   - mark sheet Status as `Applied`
   - add `Date Applied`
   - add `Follow-up Date`
   - add Gmail sent ID
   - add notes about CV version sent
   - set a follow-up reminder or at least update tracker follow-up task
9. Move to the next agency only after completing the current one.

If the user asks to resend a same-day duplicate to an agency already contacted, warn that it can look spammy. Prepare improved follow-up content, but send only if the user explicitly confirms the duplicate send.
