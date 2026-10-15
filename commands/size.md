---
description: Position sizing / risk check against the binding rules
---
Use the ai-thesis skill (sizing mode) for: $ARGUMENTS

Apply `risk/risk-rules.md` with `risk/profile.md` and `book/portfolio.csv`. Show all four
numbers: base size (cap × conviction multiplier), theme headroom, sleeve headroom, and the
correlation stress (does a −40% risky-sleeve event breach DERISK_LEVEL?). Count any material
externally-held tech-correlated exposure (employer comp, tech funds) inside the risky sleeve
— same AI-sentiment factor, not diversification. Scope: traditional markets only
(crypto out of scope, per 2026-07-07). Never touches the thesis. If `risk/profile.md` is
unfilled, refuse to size and run /onboard instead.

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
