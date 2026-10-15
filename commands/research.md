---
description: Deep research engine — crunch heterogeneous/multimodal inputs; findings to notes + evidence ledger; reads the thesis, never writes it
argument-hint: [light|heavy] <topic or corpus>
---
RESEARCH desk (analyst) — the highest-leverage stage; everything downstream inherits its
quality (garbage in, garbage out). It OBSERVES the thesis and NEVER edits it.

Topic / corpus: $ARGUMENTS

**0. Declare the run (no silent degradation).** Open with one line:
`/research · model:<actual model> · reasoning:<effort> · intensity:<light|heavy>`. If you
cannot confirm you are on the intended tier — the heavy pass wants the strongest available
model (fable preferred) at extended/maximum reasoning — SAY SO and either escalate or stop.
Model choice is set at the session/subagent layer; this command's duty is to state what it
is actually running and refuse to pretend.

**Two intensities:**
- **light ("stay current")** — a focused sweep of current sources to refresh monitoring
  indicators and surface what changed since last look. Cite everything.
- **heavy ("crunch this corpus")** — invoke the deep-research harness: fan-out searches,
  fetch primary sources, **ADVERSARIALLY VERIFY** each load-bearing claim, then synthesize.
  Extended/maximum reasoning. This is the mode for dense papers, large unstructured data
  dumps, and imagery.

**Assume inputs are messy, heterogeneous, high-volume, incomplete** — papers, data dumps,
satellite/other imagery, mixed sources.

**Imagery honesty.** Distinguish genuine image analysis (a vision-capable model actually
reading a supplied image) from text synthesis ABOUT imagery (search/reporting). State which
you did and the limits of what imagery alone can support. Never let a text summary
masquerade as image analysis.

**Output — high-density, insight-first, and faithful (faithfulness beats density):**
- Anchor every insight to its source input. Label observation vs. inference. Flag gaps and
  anything you could not process rather than smoothing over them. A polished summary with
  invented connective tissue is the WORST possible output — everything downstream trusts it.
- Land structured, tagged rows in `research/evidence-ledger.md` (hypothesis · confirms/
  weakens · magnitude · believability weight A/B/C · source citation), plus a short synthesis.
- Save full findings to `.claude/notes/YYYY-MM-DD-<topic>.md`.

**Routing (governance):**
1. Process learnings (data sources, mechanics, quirks) → append to the matching topic file
   in `.claude/memory/` (see the index in CLAUDE.md), NOT to CLAUDE.md itself.
2. Anything bearing on a hypothesis → an evidence-ledger row. If it could eventually move a
   conviction score, tag it `[AMENDMENT-CANDIDATE]` — surfaced for /review, NEVER applied
   here. **Do NOT edit research/thesis.md or research/playbook.md.** If a pre-committed
   falsifier appears to trigger, tag `[FALSIFIER-CANDIDATE]` and flag it loudly.
3. New tickers worth tracking → `book/watchlist.csv` with a `trigger_to_analyze`, then
   rebuild the page (`data/build_watchlist.py`) and journal the change.

## Language (binding — Ben, 2026-07-15)

Everything Ben reads from this command follows CLAUDE.md's communication rules — FIVE
corrections now: 07-07 no unexplained jargon · 07-10 short readable sentences · 07-15 engine
vocabulary is jargon too · 07-17 naming (every company/source gets NAME (TICKER) + a ≤8-word
plain descriptor on first mention) · 07-17 self-containment (every paragraph stands alone: no
coined concept-labels — re-explain concepts in a clause each time; no stat-stacking — each
number gets a sentence saying what it means; no cross-section references; name what a rule does,
not that it exists).
The engine's OWN terms are jargon: gate, door, wake, leg, tier, re-gate, ledger row,
weight A/B/C, §-references, tier names, S0–S4, and bare H1–H5. Translate or replace on
first use — "the re-check condition we pre-set on Talen came true", not "TLN's non-price
door fired". Keep every number, date, and caveat: precision stays, coding goes.
Send-test: a smart friend who has never opened the skill files follows every sentence.
Internal state files (journal, ledger, CSVs) keep the shorthand.
