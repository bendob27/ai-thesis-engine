---
description: Pre-trade card for a buy Ben intends to place — theme room, range position, price-as-size, staging room, invalidation sentence, verdict (adopted 2026-09-21)
---
Use the ai-thesis skill. Ben intends to BUY: $ARGUMENTS (ticker, then optionally quantity and limit price).

Produce the **trade card** — section 15 of `research/note-template.md` — within the hour, as ONE
reply in plain English. If a research note exists at `book/notes/<TICKER>.md`, read it first and
say when it was last updated; if none exists, say so and offer `/note` (do not build one here).

The six lines, each with its number and its source and date:
1. **Theme room across both accounts.** Run `python3 data/theme_exposure.py` and quote the
   theme's current share of combined equity, its cap, and the EUR room left after this order.
   A breach is stated as one sentence; it does not refuse the trade.
2. **Position in the trailing 20-session range and the 5-session run-up**, from settled closes
   (yfinance `history()`, never `info`). At or above the 80th percentile of the range → say
   plainly that the order guard will require a written reason in Ben's own words
   (`REASON:` in the approval row), and suggest what a legitimate one would be (a results
   print counts).
3. **Premium or discount to our value → size band.** Read `book/valuations.json` / `book/buy_caps.csv`
   for the name. If a value exists: premium or discount in one sentence and the band it implies
   (full / half / quarter / zero-until-level, per note-template §10). If none exists: say "no value
   on file" and give the band as "half until a note exists". A price never refuses a name.
4. **Staging room today.** 15% of the account's equity per day; today's buying so far in that
   account (from `book/preflight_log.jsonl` and `book/fills_broker.csv`); the room left. If the
   order is part of a list above 10% of equity, propose the tranche schedule (three tranches,
   five sessions apart) for `book/tranches.csv`.
5. **The invalidation sentence**: what would prove this purchase wrong about the BUSINESS,
   60–80 words, no price in it. It goes into `portfolio.csv` at fill.
6. **Verdict**: `place` · `place in tranches` · `refuse, because <a business, balance-sheet,
   legal-access or fraud fact, with its source and date>`. Nothing else may refuse.

Then: the approval row Ben would need to write (ticker, side, qty, limit, his quote), and one
line naming which of the two accounts — never inferred.
No panel, no valuation build, no Codex pass here. Journal the card as a dated entry
("CARD <TICKER> | verdict | Px: <close, date>"). Ben decides; nothing is placed by this command.
