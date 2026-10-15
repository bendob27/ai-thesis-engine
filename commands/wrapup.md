---
description: End-of-session summary and continuity note
---
**Step 0 — look for another writer before you start (added 2026-10-12, Ben's yes).** Run
`git status --short -- CLAUDE.md .claude/memory .claude/notes .claude/skills/ai-thesis/book/inbox` and
`ls .claude/notes | grep "$(date +%F)"`. If another session's uncommitted edits to CLAUDE.md, `.claude/memory/` or the
flag-file inbox exist, or a session note dated today already exists, tell Ben in one line what you found and stop unless
he says to go on. If he does: make every write to a shared file an append or a guarded single-cell edit, re-read each file
right before writing it, name your note differently (`…-learn-wrapup.md` when `…-session.md` exists) and work only what
the other session left. (2026-10-12: two wrap-ups ran in one hour and collided on CLAUDE.md, failure-modes and the
flag files.)

Summarize this session: what was done, decisions journaled, watchlist changes, thesis
change-log entries, open questions. Save to .claude/notes/YYYY-MM-DD-session.md.
Update CLAUDE.md "What to do next", keeping it to the genuinely live items and moving
resolved detail into `.claude/memory/pending-decisions.md` or `session-history.md`.
Append process learnings to the matching topic file in `.claude/memory/`, never to
CLAUDE.md — CLAUDE.md carries only rules that bind every session plus a short live-state
section. Then run `python3 .claude/skills/ai-thesis/data/check_workspace_docs.py` and fix
anything it reports (a memory file nothing links to, a stale pointer to a moved section).
**The size check BLOCKS above 35k characters (Ben-approved 07-29): file state out of
"What to do next" into its memory/notes home before closing — verify the content landed
at the destination before cutting, leave a one-line pointer. Nothing is deleted, only
refiled; method in `.claude/notes/2026-07-29-claudemd-prune-plan.md`.** Finally, verify every recommendation made this session has a journal entry
in the skill's `book/journal.md` — if any is missing, add it now with the price at the
time of the call. An unjournaled call never happened. Likewise, verify any
hypothesis-level observation this session was logged to `research/evidence-ledger.md`
(never into thesis.md).

Last, run `python3 .claude/dreaming/dream.py status`. If it prints DREAM DUE, put its line
in the wrapup summary as the final item, so Ben knows /dream is due without having to
remember it — transcripts older than about 30 days are deleted automatically and are lost
to review for good. Never run /dream from inside /wrapup; it needs its own session.

## Language (binding — Ben, 2026-07-15)

Everything Ben reads from this command follows CLAUDE.md's communication rules — the full
correction log lives in `.claude/memory/communication-rules.md` (do not trust any count of
it written here); core rules: 07-07 no unexplained jargon · 07-10 short readable sentences · 07-15 engine
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
