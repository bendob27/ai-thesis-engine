# /datesweep — find every stale, missing or impossible date in the book

**Read-only. This command changes nothing.** It reports; a human decides. Created
2026-08-03 on Ben's instruction: *"can we pls create a shortcut that triggers a sweep on the
watchlist for this (on latest dates etc)"*.

## Why it exists

The engine's dominant failure is bookkeeping, not analysis, and dates are its worst corner.
Measured instances already on the record: seven watchlist rows carried wrong report dates in
a single sweep and **every one was wrong in the same direction — too late**, because dates
get written when a row is created and never re-verified. A scheduled cloud job was armed for
a Samsung date that did not exist. Nine price conditions sat in prose with nothing watching
them. A gate was set for 2026-08-14 whose own test needed data that does not arrive until
2026-10-29.

A date that has passed and not been replaced is indistinguishable from a date that is being
watched. This command makes them distinguishable.

## What it checks

Run every check. Report each finding with the ticker, the field, the date, and how many days
stale. Never fix silently.

1. **Passed and not replaced.** Any `expiry_date`, gate date, add-gate date or re-read date in
   `book/watchlist.csv`, `book/triggers.csv` or `book/thesis_watch.csv` that is in the past.
   These are the dangerous ones: the row still reads as live coverage and nothing is watching.
2. **Report dates against the company's own filing history.** Read `book/earnings_radar.csv`
   and check every ACTIVE-tier and owned name. A vendor date is not evidence — the rule on
   file is that earnings dates come from the company's filing or investor-relations page.
   Report each as CONFIRMED / VENDOR-ONLY / CONFLICTING / NO DATE. Flag any date that has
   already passed with no result recorded on the row.
3. **Owned positions with no next dated checkpoint at all.** Every holding should have one.
   List the ones that do not.
4. **Dates that cannot settle what they claim.** For each dated gate, name the specific
   disclosure that arrives that day and ask whether it can actually answer the question. A
   date on the calendar is not evidence that the date resolves anything.
5. **Valuation and cap staleness.** Any card in `book/valuations.json` older than 30 days on a
   name we own or are actively considering, and any row in `book/buy_caps.csv` whose `state`
   begins STALE.
6. **Unapplied inbox flags.** `ls book/inbox/*wake-flags.md` — anything without `-applied` in
   the filename, with its age in days.
7. **Orphans.** Run `python3 data/orphan_levels.py` and include its output: price levels that
   exist in prose with no machine row watching them.

## How to report

One table, worst first, with a plain-English "so what" per row. Then a short list of what a
human needs to decide. **Do not fix anything.** If a date is wrong, the fix is a separate,
deliberate act with its own record — that is what `/watchlistsync` is for.

Close with the one line that matters: how many owned positions currently have no live,
future, dated checkpoint.
