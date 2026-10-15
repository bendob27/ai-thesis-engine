# /watchlistsync — bring every watchlist row into line with the decisions actually taken

**This command WRITES.** It is the deliberate counterpart to `/datesweep`, which only reports.
Created 2026-08-03 on Ben's instruction: *"as well as a manual update for the watchlist in
accordance with all the latest decisions? (Note these are two different functionalities)"*.

## Why it exists

The single most embarrassing defect this engine has produced: **Ben's own decision came back
to him as undecided, on the page he reads.** A buy was approved, the approval file had his
verbatim yes, the order card existed — and the watchlist row still said "awaiting Ben" a day
later. Same class: a name graded FAIL whose row still read "re-check at event"; rows quoting
retired earnings bars as live; two different limits on one name; "the four long positions we
hold" written while the book held none.

The decisions are right. The record lags them. This command closes that gap on purpose,
rather than waiting for Ben to spot it.

## The authority order — never invert this

When two files disagree, the one further UP this list wins, and the row is corrected to match
it. The row never wins.

1. **`book/approved_orders.csv`** — what Ben actually approved, in his words. Absolute.
2. **`book/broker_positions.csv` + `book/fills.csv`** — what is actually owned. Judge the
   broker file by its `generated` stamp, never by when it was fetched.
3. **`book/journal.md`** — the dated verdict. The most recent entry on a ticker governs.
4. **`book/valuations.json` + `book/buy_caps.csv`** — the economics.
5. **`book/triggers.csv`** — the machine-watched levels.
6. **`book/watchlist.csv`** — the row. This is the thing being corrected.

## What to do

1. **Read the last two weeks of `book/journal.md` in full.** Every verdict since the row was
   last touched. This is the input; skipping it makes the command decorative.
2. **For every ticker with a decision newer than its row, rewrite the row** so that
   `decision`, `verdict`, `decision_tldr`, `trigger_to_analyze`, `position_status` and
   `expiry_date` all state the same thing the journal states.
3. **Run the reconcilers rather than eyeballing:** `approval_drift_check()` inside
   `data/build_watchlist.py` (every open approval must have a matching row), and
   `python3 data/engine_audit.py --csv` (rows still carrying rules repealed on 2026-08-01).
4. **Retire levels whose basis has died.** A price condition attached to a withdrawn valuation
   must be removed, not reinstated — a level that outlives its reasoning is how a stale number
   survives. Say so in the row rather than deleting quietly.
5. **Obey the writing standard**: `research/watchlist-writing-standard.md`. One action state
   per row from the fixed list. Never confuse a total-position target with an additional
   order. A missing result is not a failure. Two contradicting numbers may not both stand —
   write "unresolved, do not act". Process history stays out of anything Ben reads.
6. **Enforce the shelf cap.** ACTIVE is capped at 21 (playbook §2.3, Ben 2026-08-03) and it
   binds: adding a name requires moving one off, in the same edit.

## Safety

- **Write by re-reading immediately before the edit.** Other sessions commit to this repo
  constantly. Never write from a copy read earlier in the task.
- **Never truncate a book-of-record file.** Write to a temp file and rename.
- **Refuse and report rather than guess.** If a row's correct state is genuinely ambiguous,
  leave it and list it as needing Ben.
- Rebuild the pages at the end: `python3 data/build_watchlist.py --deploy`.

## Report

What changed, ticker by ticker, in one line each: what the row said, what it says now, and
which file was the authority. Then what remains ambiguous and needs Ben.
