---
description: Consolidate notes into improved PROCESS instructions; route thesis signals to the ledger (never direct edits)
---
Review everything in `.claude/notes/` plus the skill's `book/journal.md` and
`research/evidence-ledger.md`. Then:

1. Record improved PROCESS instructions and patterns in `.claude/memory/` — one topic file
   per subject, chosen from the index in CLAUDE.md (data-quirks, verification-rules,
   agent-orchestration, concurrency, infra, and so on). Dedupe and prune stale entries in
   the topic file itself. **CLAUDE.md gets at most one line, and only when a rule binds
   every session; it must stay under 50k characters.** If a learning fits no existing topic
   file, create one and add its row to the CLAUDE.md index.
2. Findings that bear on investment hypotheses → append tagged rows to
   `research/evidence-ledger.md` (tag `[AMENDMENT-CANDIDATE]` if they could eventually move a
   score). **Do NOT edit `research/thesis.md` or `research/playbook.md`** — conviction and
   threshold changes happen ONLY at /review, on a sustained signal, with my sign-off. Notes
   must never rewrite the thesis; that is how recency bias gets codified as wisdom.
3. Propose improvements to the engine itself (templates, screens, risk rules, scripts) as
   diffs for approval. If the journal shows a repeated error pattern (consistently early,
   consistently overconfident on timing), say so explicitly — that is the most valuable
   output this command can produce.

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
