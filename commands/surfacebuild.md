# /surfacebuild — put the five tools onto the page, then hand the look to Claude Design

Created 2026-08-03. This file exists so the next session starts with the full context instead
of rediscovering it. Ben: *"For the watchlist rebuild, can you give me a code word so the next
run has all the context?"*

## The problem, measured 2026-08-03

Five tools were built in the week to 2026-08-02. **Four of them surface nowhere a human
looks, and the fifth surfaces only half of itself.** Verified by grep, not assumed:

| Tool | File | On the page? |
|---|---|---|
| Six-voice valuation scale | `data/valuation_scale.py` → `book/valuation_scale.md` | **No.** Nothing reads that file. |
| Destination card + the inversion | `book/valuations.json` → `<TICKER>.destination_card` | **No.** Zero references in either page builder. |
| Scenario builder | — | **Does not exist.** Probabilities are hand-typed JSON. |
| Buy cap | `data/buy_cap.py` → `book/buy_caps.csv` | **No.** It gates orders in code and is invisible to Ben. |
| Decision grader | `data/decision_grader.py` → `book/decision_grades.md` | **No.** |
| The three-layer test | playbook §6.0 | **Only as a glossary entry.** No row shows its own result. |

What *does* render is the near-term half of the valuation card: the bear/base/bull table, the
weighted value and the hurdle sentence, via `valcard_html()` in `data/build_watchlist.py`.

## What to build, in Ben's approved order

He approved the recommendation on 2026-08-03 and set the division of labour: **build the logic
and decide WHAT is displayed; Claude Design owns only how it looks.**

1. **One "what we think it's worth" panel per name.** A horizontal scale from the most
   cautious voice to the most optimistic, with **today's price marked on it** and **the buy
   cap marked as a line**. All six voices named — our model, the second lab, our cautious
   case, our optimistic case, the analysts with their count, and the destination case.
   **Never average them.** This surfaces the scale and the buy cap together and is the
   highest value per unit of work.
2. **The destination card as a separate, visually distinct panel**, only on names that have
   one, **led by the inversion sentence** — "the price implies X%, we say Y%". That is the
   sentence Ben actually argues with, and today nobody sees it. Include the stresses.
3. **All three test results as chips at the top of every row.** Eligibility, the money test
   with its percentage margin, ranking. **One valuation on 2026-08-03 is the reason this must be all
   three or none:** it passed the money test, that got read as a buy, and it had to be
   corrected in writing the same day. A row showing one green result and nothing else invites
   exactly that inference.
4. **The decision grader as one line on any declined or parked row**: what it has done against
   its own index since we said no, and whether it is old enough to judge (90 days).
5. **The scenario builder last**, because it is the only one requiring something new rather
   than displaying something that exists. Sliders on the three probabilities, recomputing the
   weighted value and the pass-or-fail live. **It recomputes and displays; it never writes.**
   A probability is a defended judgement, not a dial.

## Constraints that are not negotiable

- **The plain-English standard binds every string**: `research/watchlist-writing-standard.md`.
  A bare score is jargon. A test label is jargon. Say what was measured, which parts fired,
  and what it means for action, in the same breath. `data/language_check.py` runs on deploy
  and must pass.
- **Never show a number without its basis.** Every multiple carries numerator, denominator,
  period and price date. Every price carries its date and whether it is a settled close.
- **An absent figure must never render as permission.** A name with no valuation says so
  plainly; it does not show a blank where a cap should be.
- **One source of truth.** The page is generated FROM `valuations.json`, `buy_caps.csv` and
  `decision_grades.csv` — never from numbers copied into the builder.

## The handover file for Claude Design

Write it to `.claude/notes/YYYY-MM-DD-watchlist-design-handover.md` and keep it strictly to
look and feel: the panels and their content in order, the states each must handle (present /
absent / stale), what must never be visually de-emphasised (the absent-figure case, the
failing test), responsive behaviour, and light/dark. **It states what each panel MEANS so the
design does not mislead — it does not invite changes to which numbers appear.** Ben:
*"claude design should only focus on the UI/UX not the numbers and what is displayed."*

## Related work queued alongside this

`/lifecyclecards` adds per-holding fields that will want to render in the same panel area.
Read that file before designing the layout so the two are built once, not twice.
