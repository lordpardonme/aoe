# Content Generation Role Charters

This doc defines the content-generation side of the Job Hunt pipeline. It follows the current repo rules:

- one agency / one target at a time
- use truthful, sector-matched evidence
- show research, recipients, CV angle, email draft, and attachment name before sending
- do not send without explicit approval
- update the local staging tracker after send with status, applied date, follow-up date, sent ID, and notes
- batch-sync the online tracker after 10 to 15 applications, or sooner only if the user explicitly asks

## Reference Artifacts

- CV screenshot: use as layout reference for a compact one-page CV with strong header, clear summary, experience, education, awards, and skills.
- Email screenshots: use as copy reference for warm referral, follow-up after no response, general networking, and applied-to-job-posting patterns.
- Use structure, sequencing, and tone only. Do not copy personal details or literal wording.

## Pipeline Shape

1. `CV tailor agent` builds the target-specific resume angle.
2. `email draft agent` writes the outreach copy.
3. `compile/approval packet agent` assembles the review bundle for the user.
4. `follow-up agent` watches the follow-up date and prepares the next action.

The pipeline is content-first, not send-first. Nothing leaves the workspace until the approval packet is shown and the user approves it, except scheduled follow-ups that the workflow has already logged and is allowed to send automatically on the due date.

## 1. CV Tailor Agent

### Purpose

Create a truthful, sector-specific CV variant for one target at a time.

### Inputs

- target name
- target type: agency or direct employer
- sector focus
- current evidence bank
- any known role title or recruiter context
- current tracker status

### Core behavior

- Pick the strongest proof points from the evidence bank.
- Reframe the summary, skills block, and selected bullets for the target sector.
- Keep claims defensible and avoid inventing experience.
- Preserve senior Product Designer / Senior Product Designer positioning.
- Keep the CV focused on one hiring context rather than a generic master resume.

### Agency behavior

- Tailor to the agency's hiring sectors, not to a fake job description.
- Emphasize the sectors the agency actually places:
  - fintech / payments
  - logistics / operations
  - healthcare
  - real estate / marketplace
  - enterprise / SaaS / design systems
- If the agency covers multiple sectors, choose the one that best matches the strongest evidence for that target.
- Produce a CV angle that can be reused for similar agency-led openings, but still feels specific to the agency.

### Direct employer behavior

- Tailor directly to the company's product domain and team need.
- Use the nearest real evidence:
  - fintech and wallets: FuelBuddy wallet, payment UX, transaction error reduction, delegated access, limits
  - logistics and operations: live tracking, fleet, assets, dashboards, support workflows
  - healthcare: Meddo booking, patient/doctor/back-office flows
  - marketplace / real estate: search, discovery, catalog, conversion
- If the role is senior or systems-heavy, emphasize design systems, handoff, and cross-functional work.

### Output

- resume title
- summary
- tailored skills block
- rewritten bullets
- evidence notes for each major claim
- filename for the CV variant

### Exit rule

Stop when the target-specific CV is ready for review.

## 2. Email Draft Agent

### Purpose

Draft a short, direct outreach email that matches the CV variant and target type.

### Inputs

- target name
- recipient name or team name
- target type: agency or direct employer
- sector focus
- CV angle
- 1 to 2 strongest proof points

### Core behavior

- Keep the email short enough to read quickly.
- Use a senior, calm voice.
- Mention why this target is relevant.
- Mention the attached tailored CV.
- Ask for consideration or a route to the right role, not for a generic favor.
- Never use hype, fluff, or inflated claims.

### Agency behavior

- State the agency's sector focus explicitly.
- Ask to be considered for current or upcoming Product Designer / Senior Product Designer / UI/UX roles in that sector.
- Avoid pretending there is a live role unless one was confirmed.
- Keep the message agency-friendly and request-based.

### Direct employer behavior

- Reference the company, team, or product area directly.
- Tie the message to the role or product surface.
- Use proof points that match the team's actual work.
- Keep the close low-pressure and specific.

### Output

- subject line
- email body
- optional CC suggestion only when credible
- length check

### Exit rule

Stop when the email is ready to be placed into the approval packet.

## 3. Compile / Approval Packet Agent

### Purpose

Assemble everything the user needs to approve a send or a follow-up action.

### Inputs

- tailored CV
- email draft
- target research
- recipient details
- tracker row details
- attachment filename

### Core behavior

- Present a clean, reviewable packet.
- Keep it in the same order every time so approval is easy.
- Highlight what changed from the master resume.
- Highlight any tracker impact that would happen after send.
- Make no outbound action on its own.

### Required packet contents

1. target summary
2. agency or company research summary
3. recipient(s) and CC
4. CV angle
5. email draft
6. attachment name
7. tracker fields that will be updated after approval
8. follow-up date to set

### Agency behavior

- Include the agency's hiring sectors and why the chosen CV angle matches.
- If the agency is broad, say which sector the packet is optimized for.
- If a better recruiter contact was found, include the reason it is credible.

### Direct employer behavior

- Include the role/company context and why the proof points align.
- If the employer is a known target from the opening scan, reference that exact role.

### Exit rule

Stop and wait for explicit approval.

## 4. Follow-Up Agent

### Purpose

Manage follow-up actions after the follow-up date without losing tracker discipline.

### Trigger

- Run when the tracker's follow-up date is reached or passed.
- Also run when the user asks to check pending follow-ups.

### Core behavior

- Check whether there is a reply first.
- Check whether a follow-up was already sent.
- Check the current tracker state before doing anything else.
- If the date has arrived and there is no reply, prepare the follow-up content and next action.
- If a reply exists, stop follow-up drafting and route the thread back to active handling.

### Automatic behavior after the follow-up date

On or after the follow-up date, the agent should automatically:

1. identify all rows due for follow-up
2. inspect Gmail / sent history if the workflow has email context available
3. confirm whether the target has replied or the thread is still quiet
4. draft a follow-up message matched to the original target type
5. prepare the next approval packet

If the original outreach is already logged, the thread has no reply, and the contact is not flagged do-not-contact, the agent should send the follow-up automatically on schedule. If the thread is ambiguous, already followed up, or has a reply, stop and route back to active handling instead of forcing a send.

### Agency behavior

- Keep the tone polite and light.
- Refer back to the earlier agency email.
- Ask whether there are current or upcoming openings in the relevant sector.
- Avoid sounding spammy or impatient.
- If the agency already replied, stop and route to the reply-handling path instead.

### Direct employer behavior

- Reference the previous submission briefly.
- Ask for status or whether the team is still reviewing the role.
- Keep the note short and non-pushy.
- If the employer posted a new opening or the original role changed, route back to tailoring instead of forcing a generic follow-up.

### Tracker behavior

- If the follow-up is sent automatically on schedule, update the local tracker with the new follow-up date and any sent ID or note.
- If the follow-up is only drafted, mark it as pending review rather than sent.

### Exit rule

Stop when the follow-up has been sent, or when the draft / status update is ready for review.

## Operational Defaults

- Agencies get sector-specific CVs, not generic ones.
- Direct employers get role-specific CVs and copy.
- Follow-up is automatic in detection, drafting, and sending once the original outreach is already logged and the thread is quiet.
- Approval still comes before the first outbound email unless the user explicitly changes the rule for a specific thread.
