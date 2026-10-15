---
description: Triage article link(s) against my AI investment thesis, validate the core trend with outside research, then surface a trade or confirm strategy
argument-hint: <url> [url2 url3 ...]
---

Analyze the linked article(s) below and tell me whether there's an investment implication for my thesis. Use my ai-thesis skill.

LINKS: $ARGUMENTS

Work in four steps:

1. **Read & extract.** Summarize each piece's core argument in 2–3 sentences, then list every distinct trend or claim it implies. If there are multiple links, merge overlapping trends into one list and note where sources agree or conflict.
   For an X/Twitter link, use the method in `.claude/memory/data-quirks.md` ("Reading tweets", 09-27): the post via fxtwitter, the thread and replies via `bird-x`, images read directly, any video transcribed.

2. **Validate.** For each major trend, research beyond the article (recent data, primary sources, credible counter-views). State whether the evidence supports, weakens, or is mixed on the claim — and how strongly. Cite every source (URL or filing). Flag anything that's opinion dressed up as fact.

3. **Test against my thesis.** For each validated trend: which hypothesis it confirms or weakens and by how much, the affected tickers, and — critically — what is NOT already priced in. Then write the strongest case AGAINST acting.

4. **Conclude with one action:** ignore / watchlist / deep-dive / actionable trade. If actionable, sketch the trade (long or short, rough structure, and what would invalidate it). If it only confirms existing strategy, say so plainly.

5. **Record (governance).** READ-ONLY on the thesis. Add any new name to `book/watchlist.csv` with a `trigger_to_analyze` AND the four decision-display columns per the watchlist-row contract in commands/analyze.md (`decision` enum · `industry` · `what_they_do` · `decision_tldr` — schema since 2026-07-21; the builder warns if missing), then rebuild the page, and journal the change in `book/journal.md`. Append a row to `research/evidence-ledger.md` for each hypothesis a validated trend confirms/weakens (hypothesis · direction · magnitude · weight A/B/C · citation). If a pre-committed falsifier appears to trigger, tag `[FALSIFIER-CANDIDATE]` and flag it loudly. **Never edit research/thesis.md** — that is /review's gated job.

Style: concise, factual, plain English, minimal jargon, no hype. Lead with the bottom line. Keep it under ~400 words. Stamp "data as of <date>" and flag any claim you couldn't verify.

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
