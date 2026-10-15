---
description: Run the risk-profile onboarding (required before any position sizing)
---
Run the onboarding elicitation from the ai-thesis skill's `risk/risk-rules.md`,
conversationally and one question at a time: portfolio size, drawdown pain point framed in
money (not percent), existing correlated exposure (employer-linked comp, tech-heavy funds —
traditional markets only), cash needs under 3 years, tax jurisdiction, and the sleeve
confirmation including the 2022-scenario walkthrough and the Taleb-barbell-vs-aggressive-book
distinction. Write the results to the skill's `risk/profile.md` with MAX_DD and DERISK_LEVEL
derived, and journal (`book/journal.md`) that onboarding was completed.

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
