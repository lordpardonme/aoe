# Agent Rules

These rules are written for coding agents using this repository.

## Start Here

1. Run `npm run verify`.
2. Run `npm run agent:context`.
3. Read `POLICY.md`.
4. Read `Job Hunt/AGENTS.md` before touching resume or outreach files.

## Do Not Do These

- Do not send email.
- Do not change the live tracker without exact row/range grounding.
- Do not fabricate resume content.
- Do not batch outreach unless asked.
- Do not delete workspace files.
- Do not commit credentials or local dependency folders.
- Do not assume local CSVs are current when live state is available.

## Required Behavior

- State what you verified and what remains uncertain.
- Keep external-state actions explicit and approval-gated.
- Keep Git changes scoped and easy to review.
- When updating tracker state, cite Gmail evidence in the relevant row.
- When making resumes, preserve truthful career evidence.

## Common Commands

```powershell
npm run setup
npm run verify
npm run agent:context
git status -sb
```

## Repository Layout Cheat Sheet

- `Job Hunt/resumes/`: resume variants, PDFs, drafts, scripts.
- `reconciled-tracker-build/`: tracker exports and reconciliation scripts.
- `drive-extraction/`: OCR and extracted lead evidence.
- `.planning/codebase/`: architecture and workspace map.
- `References and Resources/`: supporting reference material.

