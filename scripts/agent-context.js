#!/usr/bin/env node

console.log(`
Job Hunt Workspace Agent Context

Purpose:
  Private operating workspace for resume tailoring, tracker reconciliation,
  Gmail evidence checks, and job-hunt execution.

Source of truth order:
  1. Latest user instruction
  2. Live Gmail for sent/received email evidence
  3. Live Google Sheet for tracker state
  4. Local reconciled workbook/CSV
  5. Older recovered context

Hard rules:
  - Do not send emails without explicit approval.
  - Do not edit the live sheet without exact row/range grounding.
  - Do not invent resume facts.
  - Treat pause, wait, and do not send as hard stops.
  - Keep this repository private.

Start by reading:
  README.md
  POLICY.md
  RULES.md
  AGENTS.md
  Job Hunt/AGENTS.md

Useful local files:
  reconciled-tracker-build/current_tracker.xlsx
  reconciled-tracker-build/gmail-sent-audit-2026-07-06.csv
  Job Hunt/resumes/
  drive-extraction/
`);

