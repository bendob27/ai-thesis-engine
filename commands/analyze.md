---
description: Full 10-step company analysis against the thesis
---
Use the ai-thesis skill (company-analysis mode) on: $ARGUMENTS

Run the full 10-step template from the skill's `research/frameworks.md` — no steps skipped:
live data (`data/fetch_market_data.py` + web), expectations audit with the arithmetic
shown, scenarios with expected value, pre-mortem, steelman (including what the influence
funds' actual positioning implies), risk-rule-compliant trade structure with invalidation,
confidence, journal entry. Run playbook §6.0's three-layer decision test (eligibility →
money test → rank-and-size) and print the re-homed §6.1 checklist verbatim — each check
with its finding and one line of evidence; only independent refuters (check 6) and the
no-same-day-news rule (check 8) carry a veto of their own, and crowding informs size,
never permission (amended 2026-08-01; wording reconciled 2026-08-11, upgrade brief §7.1).
If a short is
proposed, check borrow cost / short interest / days-to-cover first. If sizing is needed and
`risk/profile.md` is unfilled, run /onboard first.

**Audit gate before the verdict (added 2026-08-11, upgrade brief 7.7).** Run
`python3 data/engine_audit.py --gate --ticker <TICKER>` before writing the verdict: an open
HIGH finding on the name (no valuation card, schema-invalid card, untyped ceiling, missing
identity row, prose contradicting the decision column) is either resolved in this session or
carried as a stated caveat in the output — never silently shipped over.

READ-ONLY on the thesis: journal the call in `book/journal.md`, and if the analysis yields
a hypothesis-level observation (confirms/weakens H#), append a row to
`research/evidence-ledger.md` — **never edit research/thesis.md** (that is /review's gated
job). Save the analysis to `.claude/notes/YYYY-MM-DD-analysis-<ticker>.md`.

**Watchlist-row contract (schema since 2026-07-21).** Every verdict lands as a
`book/watchlist.csv` row (new, or superseding the ticker's old row in place) and MUST fill
the four decision-display columns — the page renders `decision` as the colored status chip
and warns at build time when it's missing:
- `decision` — exactly one of: `BUY APPROVED` (terms set, executes when funded) ·
  `BUY IF` (buy pre-approved if the written condition hits) · `RE-CHECK AT EVENT` (a dated
  event re-opens the decision; not an auto-buy) · `WATCHING` (no committed condition) ·
  `PASSED` (analyzed, declined; reopen condition recorded) · `AVOID` (negative view /
  short-side reference) · `GAUGE` (indicator only, never a candidate).
- `industry` (≤38 chars, "Sector — product") · `what_they_do` (≤110 chars, plain English)
  · `decision_tldr` (≤140 chars: terms/condition first, reason second — no jargon).
`verdict` stays the full written call in plain English (free-form, any length);
`trigger_to_analyze` stays the buy-path text the card renders under "What would make us
buy". The old rule "keep the verdict's leading status token" is retired — the enum column
carries the machine-readable status now.

**An override does not shrink the deliverable (added 2026-07-28, Ben-approved).** If Ben
overrides a pass/kill and takes the position anyway, or backlogs an approved one, the analysis
package is still produced in full — valuation card in `book/valuations.json`, expected return
against the index after the 26% gains tax, exit and invalidation levels, refuters, journal
entry, watchlist row. The package follows from OWNING the position, not from how it was
approved. "No valuation model because it entered by override" is a retired sentence.

**Valuation method v3 (binding from 2026-09-02, Ben's instruction — frameworks §11).** Every new
valuation card: states its value date and derives the horizon (3y growth default, 5y compounder);
builds the cash bridge year by year (stock pay AND its payroll taxes charged, cash tax at the rate
that applies each year, interest never inside the multiplied earnings, net cash added once);
DERIVES each scenario's exit multiple from the company's trajectory after the horizon using
`book/multiple_ladder.md` (re-run `data/multiple_ladder.py` first), prints today's multiple
beside it with a one-sentence rationale, and never pairs "still growing 15%+" with a multiple
below 60% of today's; translates every multiple into the perpetual growth it implies at 10%;
carries the reverse ladder; writes one sentence of reasoning per scenario probability, with no
house default; and reports the annualised expected return from today's price beside the 6.5%
market comparison and Ben's 12%/10% objective. `data/valuation_validate.py` rejects a new live
card missing any of it. Cards dated before 2026-09-02 are grandfathered and rebuilt under §11
the next time they are used for a buy decision.

**Important calculations run twice — Fable, then Codex (added 2026-07-28, Ben-approved).** Any
number that moves money (valuation card, expected return, sizing, cap arithmetic, option payoff
and probability of total loss) is built on Fable and then re-checked by OpenAI Codex with every
load-bearing fact inline, since Codex runs sandboxed and cannot read our files. Exact command in
`.claude/memory/agent-orchestration.md`. Ben sees BOTH numbers when they differ — never a blend.

**Independent refuters are mandatory (added 2026-07-10, Ben-approved)** for any verdict
that writes or updates a door (ENTER, ENTER-ON-TRIGGER, or a change to an existing
position) — 2-3 refuters on distinct lenses, per the generator≠approver rule, empowered
to KILL. A WATCH or PASS verdict does not require a refuter, but still logs to
`book/kills.csv` with the refuter count stated (0 if none ran) — a rule with no
enforcement mechanism just becomes a note nobody checks; this is that mechanism.

**Un-failable-gate check (added 2026-07-22, Ben-approved — repeated generator error, 2 instances
Techwing/KION).** Before recording ANY entry condition ("buy if X"), test it against the company's
pre-announcement surface — its latest guidance, any pre-close/pre-release call, and the
company-hosted consensus. A bar the guided path already clears, or a metric the company has already
printed, is theatre, not a test. Every proposed bar must be one the pre-announced path does NOT
already meet; if you cannot state what would make it fail, it is not a gate. Also verify a multiple
BAND (e.g. "trades 8-15x its history") against computed history like any other number — never assert
it from memory. This runs at the generator step, so the refuter isn't the only thing standing
between a pre-passed bar and the book.

**The same check applies to REOPEN conditions on a pass/kill (extended 2026-07-28, Ben-approved —
KC's two re-look legs were both defective; third sighting of the class).** Before recording any
"look again if X" condition, test three things: (a) would X fire BECAUSE the thesis failed? (a
margin gate a spending pause clears mechanically rings loudest at the exit, not the entry);
(b) is X already met on any published basis? (c) can one accounting-estimate change alone clear
it (a depreciation-life extension, a reclassification)? Any yes → respecify before it enters
triggers.csv.

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
