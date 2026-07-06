# Workspace Policy

This policy applies to every human or coding agent working in this repository.

## Purpose

The repository is a private job-hunt operating workspace. It stores personal
career material, recruiter leads, tracker exports, Gmail reconciliation evidence,
resume variants, and workflow instructions.

The primary goal is accurate, evidence-backed execution. Speed is useful only
when it does not damage tracker integrity, email safety, or resume truthfulness.

## Authority Order

Use this order when sources disagree:

1. Explicit latest user instruction.
2. Live Gmail evidence for sent/received email state.
3. Live Google Sheet for tracker status.
4. Local reconciled workbook/CSV.
5. Older recovered context and memory.

If a fact may have drifted, verify it live before treating it as current.

## Email Policy

- Do not send email unless the user explicitly says to send.
- Drafting is allowed when requested, but drafts must be presented for review.
- `do not send`, `pause`, and `wait` are hard stops.
- Before marking anything sent, verify Gmail sent mail by recipient, subject,
  attachment, date, and message/thread ID.
- For agency outreach, handle one target at a time unless the user explicitly
  requests a batch.

## Tracker Policy

- The live Google Sheet is the source of truth.
- Read metadata before editing a Google Sheet.
- Use exact tab names and bounded ranges.
- Do not overwrite rows based only on company-name guesses.
- Preserve Gmail message IDs and evidence links when available.
- Mirror important reconciliation outputs locally.

## Resume Truth Policy

- Do not invent work, domains, projects, clients, numbers, or outcomes.
- Tailor only from real evidence in the workspace.
- Adjacent experience can be reframed, but it must remain truthful.
- Sector matching is allowed; fabrication is not.
- PDFs and email drafts must match the target role and target organization.

## Repository Policy

- Keep the GitHub repository private.
- Do not commit secrets, tokens, `.env` files, key files, or local credentials.
- Do not commit virtualenvs, dependency caches, or nested Git internals.
- Commit meaningful workspace snapshots with clear messages.
- Avoid destructive Git commands unless explicitly requested by the user.

## Local File Policy

- Do not delete files without explicit user approval.
- When creating generated artifacts, place them in the existing project folders.
- Keep filenames descriptive and stable.
- Avoid unrelated refactors or cleanup while doing job-hunt execution.

## Agent Handoff Policy

Any new agent should read, in order:

1. `README.md`
2. `POLICY.md`
3. `RULES.md`
4. `AGENTS.md`
5. `Job Hunt/AGENTS.md`

Then run:

```powershell
npm run verify
npm run agent:context
```

