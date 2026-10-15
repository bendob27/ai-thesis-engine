---
description: Standardized research note on a company (research/note-template.md) — the main deliverable before any purchase and the standing record on every holding (adopted 2026-09-21)
---
Use the ai-thesis skill. Write or update the research note for: $ARGUMENTS (ticker; add "deep" for the deep version).

Follow `research/note-template.md` exactly — every section, in order, the same 14 numbers —
and write it to `book/notes/<TICKER>.md` (append an **Update** block if the note already exists
and the ask is a results reaction). Plain English throughout; every company on first mention gets
NAME (TICKER) plus a short descriptor; every figure names its source, date and grade
(filing / call commentary / press); ratios computed from raw filed fields, never vendor multiples;
the results date comes from the company's own notice.

**Standard note (default, about one hour):** one analyst pass, then a second pass that lists the
two or three figures the recommendation collapses without and re-opens the primary source for each
(EDGAR via `curl` with a User-Agent, or the company's own investor page), correcting the note
in place — never a note plus a corrections list.

**Deep note ("deep", required above a set amount or 3% of the account's equity, or for any name
entering the concentrated roster):** the standard note, then the reviewer panel
(`.claude/workflows/decision-panel.js`) on the recommendation, then the Codex second pass on the
valuation arithmetic with every load-bearing fact inline; both numbers shown to Ben when they
differ.

Rules that bind the note:
- A **NO** (section 1) is allowed only for a business, balance-sheet, legal-access or fraud
  fact, named with its source and date. Price, crowding and consensus set the size band in
  section 10 and never refuse a name.
- Section 11 ends with the single kill metric (line item, source, threshold, direction, earliest
  observable date); it is copied into `book/sell_tests.csv` as the holding's sell test.
- Section 1's "what would prove it wrong" sentence has no price in it and is the text that goes
  into `portfolio.csv` at fill.
- Section 13 quotes `python3 data/theme_exposure.py` for the theme's share of combined equity.
- No score in the note is left unexplained; every grade in section 14 carries its sentence.

Finish with the journal entry ("NOTE <TICKER> | standard/deep | recommendation and size band |
Px: <close, date>") and one line to Ben: the recommendation, the size band, and the kill metric.
Ben decides; nothing is placed by this command.
