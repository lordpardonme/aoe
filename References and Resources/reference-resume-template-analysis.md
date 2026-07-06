# Reference Resume Template Analysis

Reference image: `WhatsApp Image 2026-06-07 at 01.32.45.jpeg`

## Template Verdict

Estimated ATS/template score: 91/100.

This is a strong ATS-friendly visual template because it uses a simple single-column resume structure, plain text sections, standard headings, clear dates, measurable bullets, and minimal decorative styling. It is designed like a recruiter-readable document first, not a portfolio poster.

## Layout Pattern To Match

- One page, single column.
- Name top-left, large serif/bold style.
- Title and contact line directly below name.
- Portfolio and LinkedIn top-right.
- Short 2-line italic/compact summary under header.
- Thin horizontal rule under each major section heading.
- Standard section order:
  - Professional Experience
  - Education
  - Awards/Achievements
  - Skills and Tools
- Role line format: `Role - Company`
- Date range right-aligned on the same line.
- Bullets indented consistently, with strong action verbs and measurable results.
- No tables, sidebars, icons, profile image, charts, badges, colored boxes, or decorative panels.

## Why It Scores Well

- ATS parsers can read the structure in normal order.
- Section names are standard and predictable.
- Dates are explicit and attached to roles.
- Bullets are outcome-heavy, not responsibility-heavy.
- Metrics are dense: project counts, user counts, revenue/business impact, percentages, followers, impressions.
- Skills are plain text at the bottom, separated into `Skills:` and `Tools:`.
- The design looks clean because spacing and horizontal rules create hierarchy without breaking parsing.

## Risks In The Reference

- Screenshot quality is not the resume file itself; the actual PDF/DOCX may score differently.
- Some percentages are blurred, so those values cannot be copied or inferred.
- The resume uses a dense one-page format; weak bullets will look exposed.
- It works because the content is metric-rich. Layout alone will not compensate for vague experience.

## Current Inspire Resume Gap

The current generated PDF is cleaner than the first version, but it still does not match this reference. Main differences:

- It uses a modern colored header and skill grid; the reference uses black text, rules, and no grid.
- It has `PROFILE`; reference uses a short summary without an obvious boxed/modern feel.
- It includes too many skill categories; reference compresses skills into two simple lines.
- It lacks an `Awards/Achievements` section, which the reference uses to add proof and credibility.
- It should use right-aligned dates for roles and education.
- It should reduce visual styling and increase metric density.

## Build Rule For Next Resume

Use the reference as the master template:

- Generate a plain one-page PDF from structured text.
- Use black/gray only.
- Use a serif-style name and section headings if available.
- Keep all text selectable.
- Avoid tables unless used only for invisible date alignment and verified by extraction.
- Prefer paragraph and bullet flowables over text boxes.
- Keep skills as simple text lines.
- Add `Selected Achievements` only if the claims are truthful from the evidence bank.

