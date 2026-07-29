# Tracker Reconciliation Gap — 2026-07-28

## Scope

Gmail scanned for window 2026-07-11 to 2026-07-28. Live tracker read via service
account. This note records what was found and what remains unresolved.

## Live sheet identified

- File name: `Job Tracker`
- ID: `1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI`
- URL: https://docs.google.com/spreadsheets/d/1tkaUbh9iuPs9IzSya1yuJPqNyrvk8BouufIobQgXpwI/edit
- Tabs: Dashboard, Master Job Tracker, Agencies, Direct Employers, LinkedIn
  Search, Phone WhatsApp, Sent By Me, Follow Ups, Needs Manual Check

`README.md` refers to `Master Job Tracker - Reconciled`. That is the name of a
**tab** inside this file, not the file itself. The file is named `Job Tracker`.

## Unresolved: is this the canonical tracker

The live sheet's last application activity is 2026-06-27. Three batches of sends
are absent from every tab:

| Batch | Sends | Present in live sheet |
| --- | --- | --- |
| 2026-07-04 (Nagarro, Cognizant, Marc Ellis, OneThing, others) | ~6 | No |
| 2026-07-07 (Classcard, Techversant, Seventh Contact, Seven Hiring, Aegan, Goldenflitch, The Brink Agency, Aadira Softtech, PinkRoccade) | 9 | No |
| 2026-07-22 and 2026-07-23 | 18 | No |

`2026-07` values that do appear in the sheet are follow-up dates on June
applications, not application dates.

This contradicts `monthly-recap-2026-07-11.md`, which states the live tracker
received eight new rows plus a refreshed Goldenflitch record, and that a report
tab logged all nine July 7 sends. No such rows and no such tab exist here.

Two possible explanations, not distinguished:

1. Those writes went to a different spreadsheet.
2. The writes never landed and the recap overstated the result.

Two spreadsheet IDs recovered from `Job Hunt/resumes/recovered-context/` are
still inaccessible to the service account (HTTP 403). Either could be the real
reconciled tracker:

- `1KXLk48k5XE8pWa8H80mpXsUXBbwUMFjyS7BiaPU1ROY`
- `1m2H2leRva6O7ibudyat_oGx5_j_eESTCytkrcsKx1_k`

Sharing both with `claude-mcp-sheet@claude-sheet-503808.iam.gserviceaccount.com`
resolves this in one read.

The second readable sheet, `Job Application Data Extraction`
(`111LE2oa3HaIkNdNmCw56K3Ffl7a_REIDdsrBYSrcb6g`), contains none of the July
companies and no 2026-07 dates. It is not the missing target.

## Defects found in the live sheet

**`Direct Employers` tab header is broken.** Cell A1 reads `#REF!` and rows 2-3
are empty. 158 data rows sit under a dead formula reference.

**Duplicate rows with contradicting status:**

| Company | Row | Status |
| --- | --- | --- |
| Emirates Net | 45 | Applied, 2026-06-03 |
| Emirates Net | 239 | To Contact |
| Horizon Group | 49 | Applied, 2026-06-03 |
| Horizon Group | 243 | To Contact |

**`Foldr` row 249 is stale and is the highest-value row in the sheet.** It reads
`Applied`, Date Applied 2026-06-12, Follow-up 2026-06-19. Actual state from
Gmail: salary negotiation concluded at a 20% hike for a remote role on
2026-07-20, and an interview ("Conv #1" with Apeksha) was held 2026-07-27
19:00-19:45 IST via Google Meet. Outcome unknown from Gmail alone.

## Gmail findings, 2026-07-11 to 2026-07-28

18 application sends, none recorded in the live tracker. Full detail with Gmail
message IDs and thread IDs is in
`reconciled-tracker-build/gmail-sent-audit-2026-07-28.csv`.

Replies received:

- **Horizon Group**, 2026-07-22 — CV received, under review. Acknowledgement only.
- **Harshita Hiring Desk**, 2026-07-22 — requires three registration links to be
  completed before consideration. Blocked until the user acts.
- **AcceleratorApp**, 2026-07-26 — UX Designer application started but never
  submitted. Open loop.

## Accuracy note on sent material

The Mphasis referral email (`19f88781f9ce6aef`) states "4+ years" of experience.
Every other July send states "6+ years". Already sent; recorded here so tracker
notes match what was actually claimed.

## Not done

No live sheet write was performed. Waiting on confirmation of which spreadsheet
is canonical.
