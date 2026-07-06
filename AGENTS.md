# Agent Instructions

This repository is a private job-hunt workspace. Treat it as live operational
data, not as a toy codebase.

## First Steps

Run:

```powershell
npm run verify
npm run agent:context
```

Read:

1. `README.md`
2. `POLICY.md`
3. `RULES.md`
4. `Job Hunt/AGENTS.md`

## External Actions

External actions need explicit user intent:

- Gmail sends
- Gmail draft creation
- live Google Sheet edits
- GitHub pushes
- file deletions

If the user says `wait`, `pause`, or `do not send`, stop the external action.

## Job-Hunt Defaults

- Verify Gmail before marking sent.
- Verify live Sheets before tracker edits.
- Keep agency outreach one target at a time.
- Use truthful, target-specific resumes.
- Preserve evidence links and Gmail message IDs.

## Git Defaults

- Keep the repo private.
- Do not commit local dependency caches.
- Do not commit nested Git metadata.
- Use clear commits for stable workspace checkpoints.

