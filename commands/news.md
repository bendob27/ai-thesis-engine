---
description: Fast ≤150-word news triage against the thesis (read-only; feeds the ledger + watchlist)
---
Use the ai-thesis skill (news-triage mode) on: $ARGUMENTS

Fetch the article content and live prices for affected tickers first, then follow the triage
template in the skill's `research/frameworks.md` exactly (≤150 words: relevance 0-5,
hypotheses affected, what's priced in, action). Relevance comes from surprise vs
expectations, not topical match — most AI news is a 1. If action ≠ ignore: journal it
(`book/journal.md`), update `book/watchlist.csv` (then rebuild the page), and append an
evidence-ledger row for each hypothesis it confirms/weakens. READ-ONLY on the thesis; a
pre-committed falsifier that appears to trigger is tagged `[FALSIFIER-CANDIDATE]` and flagged
loudly, never suppressed. For relevance ≥3, also save the triage to
`.claude/notes/YYYY-MM-DD-news-<slug>.md`.

(For a heavier pass — outside validation + trade sketch — use /tradescan.)

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
