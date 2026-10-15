# Watchlist writing standard

Every word on the watchlist dashboard is written for Ben and nobody else. He is a growth
investor with deep AI, crypto and venture knowledge, and zero patience for this engine's
internal vocabulary. Created 2026-07-30 after he read the Klaviyo, Tencent and SK Hynix rows
and called them ambiguous, then gibberish. His instruction: *"I essentially want to make sure
that there is no ambiguous language in the watchlist."* His benchmark: Bridgewater's insight
reports.

This file is the contract for anything written into `book/watchlist.csv`. It applies to new
rows too, not only the 2026-07-30 rewrite.

---

## 1. The one test that matters

**A single field, read cold, with no other field and no other document, must make complete
sense to a smart reader who has never opened this repo.**

If a sentence needs the reader to know what a gate is, what tier means, what a card is, which
tests were A/B/C/D, what 2/10 measures, or what "armed" implies — it fails. Rewrite it.

## 2. What Bridgewater does that we must copy

1. **Mechanism before conclusion.** Say how the thing works, then what it means. "Memory
   prices are set quarter by quarter, so a shortage shows up in profits within two quarters"
   beats "cyclical torque".
2. **Every number carries its unit, its date and its source in the same sentence.** "76%
   operating margin in the June quarter, from the company's own results release."
3. **Plain declarative sentences.** Subject, verb, object. One idea each.
4. **Define the instrument the first time it appears, every time.** No standing definitions.
5. **State what would prove it wrong.** Bridgewater always says what breaks the view.
6. **No insider shorthand.** They write for allocators who did not build the model.

## 3. Hard rules

- **One idea per sentence.** Two commas plus a dash means split it.
- **At most one dash per sentence, usually none.**
- **Expand every company on first mention inside that field:** NAME (TICKER) plus a plain
  descriptor of eight words or fewer. Do this per field — each field is read alone.
- **Never a bare score.** Not "2 out of 10", not "7/10", not "conviction 4". A score appears
  only with what it measures, which signals produced it, and what the number means for action.
- **Never a bare test label.** Not "test A failed", not "check 5", not "leg (b)". Say what the
  test asked and what the answer was.
- **No engine words.** See the replacement table in §6.
- **No coined labels.** If a concept matters, re-explain it in a clause every time. "the
  contracted-infrastructure case" is banned; write "the case that memory becomes sold under
  long contracts like a utility rather than repriced every quarter".
- **No stat-stacking.** Each number gets its own sentence saying what it is and why it matters.
- **No cross-references.** Never "see the row above", "as noted", "per the card". If a fact
  matters, restate it.
- **Dates in full.** "July 29" or "2026-07-29", never "07-29" alone in the middle of a sentence,
  and never a bare weekday.
- **Currency named every time.** "₩1,401,000 (about €830)". Never a bare number for a non-US
  price.

## 4. The crowd gauge — how to write it

We score how crowded a name is by checking ten specific signs that other investors have already
arrived. Each sign is either true or false, one point each. The bands: **0–3 is LOW (few
investors here yet), 4–5 MODERATE, 6–7 HIGH, 8–10 EXTREME.** The engine's own rules say a score
of 7 or more blocks a new purchase, 4 to 6 allows one only with a bigger measured gap between
price and reality plus a smaller position, and 3 or less passes freely.

The ten signs, in the words to use with Ben:

| # | Sign | Plain wording |
|---|---|---|
| 1 | Price above mean sell-side target | the share price already sits above the average price analysts think it is worth |
| 2 | ≥3 major-bank initiations/upgrades in 2 quarters | at least three big banks started or upgraded coverage in the last six months |
| 3 | Multiple > 2× its own 3y median | the shares cost more than twice what they normally have, measured against their own three-year average |
| 4 | Viral / mainstream content in 90 days | it has been all over podcasts, YouTube or LinkedIn in the last three months |
| 5 | 13F-tracker celebrity holding | famous investors' filings are being passed around as a reason to own it |
| 6 | Retail flow / elevated options / meme status | unusually heavy options trading or small-investor enthusiasm versus its own normal |
| 7 | Index or ETF inclusion in 2 quarters | it was added to an index, so funds had to buy it whether they liked it or not |
| 8 | The theme is the default media explanation | the story behind it is the standard explanation financial media reaches for |
| 9 | Insiders or anchor holders selling into strength | the people who run it, or its earliest backers, are selling into the rally |
| 10 | Our stage-2→3 detectors fire | the signs we watch for a story moving from early to fully understood are showing |

**Required shape whenever a row states a crowd reading:**

> Crowding: LOW. We check ten signs that investors have already piled in, and two are true
> here. One: it joined the Russell index in June 2026, so funds had to buy it. Two: insiders
> sold about $80 million of stock with almost no buying against it, 62 sales per purchase. The
> eight that are false include the ones that matter most — the price is below the average
> analyst target, no wave of bank upgrades, and no viral coverage.

**If the record does not say which signs fired,** do not guess and do not drop the number.
Write: `Crowding: <LABEL>, recorded <date>. Which of the ten signs fired was not written down
at the time, so treat the label as a judgement rather than a measurement.` Then list that row
in your report so the debt is visible.

## 5. The entry checklist — how to write it

A name must clear every item below before it can be bought. When a row claims it passed, name
the items and give this company's reading for each. When a row claims it failed, name which
item failed and what the failing evidence was.

0. **Cheap crowd screen first.** Score 8 or more out of the ten crowd signs and we do not even
   commission the deep work.
1. **Crowding low enough to buy.** 7 or more blocks. 4 to 6 needs a bigger measured gap, a
   written paragraph on who else owns it and what would force them to sell, and a stated cut
   to position size.
2. **How far the story has travelled.** Early and unnoticed passes freely. A name everyone
   already understands can still be bought, but only with three things written down: crowding
   at 6 or below, evidence the business is durable, and a gap between price and reality stated
   as a number.
3. **We are buying the layer that keeps the profit.** Not the loudest name in the chain — the
   place the money actually settles.
4. **It maps to one of our five standing hypotheses about the AI buildout**, with conviction
   above that hypothesis's floor. Say the hypothesis in words, never as "H2".
5. **A gap between what the price implies and what we believe, stated as a number.** Either the
   growth or margin the price implies versus what we expect, or the number of years of growth
   the price implies versus how many we think it gets. "It looks cheap" is not a gap.
6. **Two or three independent people tried to kill it and failed**, each attacking a different
   way: the facts are wrong, we are buying the wrong part of the chain, or it is already priced.
7. **Sized to the rules, with the condition that would end the position written before we buy.**
8. **Never bought on the day the news broke.** Entries happen at a scheduled review or at a
   pre-defined event.

## 6. Word replacements — banned on the left, use the right

| Banned | Write instead |
|---|---|
| gate, re-gate, door | the written condition we set / the conditions that have to be true before we buy |
| wake, wake flag | the price alert that tells us to look again |
| tier, ACTIVE/QUEUE/ARCHIVE | how closely we are watching it: closely / on the list / ruled out |
| leg | part of the position / part of the plan |
| standby | ruled out for now, with conditions that would reopen it |
| armed, armed order, backlog order | approved and waiting on cash, nothing placed with the broker |
| panel-adjudicated, adjudicated 4-1 | reviewed by several independent checkers; four said X, one said Y |
| the card, decision card | the written test we agreed in advance |
| test A / check 5 / leg (b) | the test that asked whether ... |
| override #5 | Ben decided to buy it anyway, against the engine's conclusion |
| no-chase ceiling | the highest price we will ever pay |
| S0/S1/S2/S3/S4 | early and unnoticed / becoming understood / widely understood / the default explanation / visibly clearing |
| H1–H5 | the actual hypothesis in words |
| ADR | US-listed receipts that stand for shares traded in <country> |
| parity, premium to parity | what the same shares cost in their home market, and the extra you pay here |
| NRR | how much existing customers grow their spending, year over year |
| reverse-DCF | working backwards from today's price to the growth it implies |
| thermometer, consensus score | how crowded the name is |
| PASS | we looked and decided not to buy it |
| KILL | ruled out; here is what would change that |
| ENTER | the analysis says buy |
| WATCH | not buying, tracking it with written conditions for a second look |
| ratify | say yes if you agree, or overrule it; nothing happens if you do nothing |
| un-failable | a test written so loosely it could never say no |
| bps | hundredths of a percent, or just write the percentage |

## 6b. The order card — what `decision_tldr` must be

Added 2026-07-30 after an independent review by OpenAI's Codex, run because it had never seen
these rows or written any of them. Its verdict on the first rewrite was **no, not yet safe to buy
from**, and its reason was not vocabulary. It was that a reader *"cannot reliably distinguish a
total-position target from an additional order, a failed test from a missing result, or a current
decision from historical workflow."* Its single highest-effect fix, adopted here:

**`decision_tldr` is a CURRENT-STATE ORDER CARD, and nothing else. Four parts, in this order:**

1. **The state, in exactly one of these eight sentences.** No blending, no second state.
   - *"We own N shares at PRICE, bought DATE."* — a position
   - *"Approved to buy, nothing placed: N shares at LIMIT or better."* — approved and order-ready
   - *"Approved to buy, but no order can exist yet: BLOCKER."* — approved, not order-ready
   - *"An order is live at the broker: N shares at LIMIT, expires DATE."* — submitted
   - *"Not bought. It becomes a buy only if CONDITION."* — a written condition, not yet true
   - *"Not bought, and no condition is set."* — watching only
   - *"We looked and decided not to buy it."* — rejected
   - *"Not a purchase candidate. We read it to tell us WHAT."* — a gauge
2. **The money, with TOTAL and ADDITIONAL never confused.** Say *"bring the TOTAL holding to 2%
   of the book, including the share already owned"*, never *"buy 2%"*. Say what the percentage is
   a percentage OF. A ceiling is stated as the highest price we will ever pay.
3. **What blocks it right now** — the cash transfer, a price Ben has not quoted, a review not yet
   run, a report not yet published. If nothing blocks it, say that.
4. **The next dated event that changes the decision.**

Nothing historical belongs in this field. No vote counts, no superseded tests, no corrections, no
who-asked-whom.

## 6c. Eleven further rules from the same review

Each of these describes a sentence that reads perfectly and still misleads.

1. **A missing result is not a failure.** "Could not be graded" may block an approval, but never
   write it as evidence against the company, and never let it read as "failed".
2. **Two numbers that contradict each other may not both stand.** Writing "both figures are on
   the record" leaves the reader to pick. Write instead: *"the record holds two figures, X and Y,
   and they are not reconciled — do not act on either until they are."*
3. **Every multiple carries four things:** what is on top, what is underneath, the period, and the
   price and date it was computed at. "29 times its trailing figure" is not a multiple.
4. **Every condition carries six:** the thing measured, where the number comes from, the period,
   the exact threshold, what happens when it is met, and what is watching it. Ban "on a pullback",
   "customers shrinking", "a calm day", "about 25-30%".
5. **Process history stays out of anything Ben reads** unless it changes today's decision. Our
   reviewers, our vote counts, our earlier drafts and our corrections are not evidence.
6. **A claim about motive or cause is labelled as inference.** Not "the disclosure stopped because
   the number stopped flattering them" but "the disclosure stopped; we do not know why, and one
   possibility is that the number had turned".
7. **Rhetoric about value needs arithmetic behind it in the same breath.** "Already paid for",
   "the multiple is spent", "a 40% event" — either show the number or cut the phrase.
8. **Peer comparisons use the same measure, period and basis on both sides**, or they are not
   comparisons. Say so when only one side is available.
9. **A private company gets NAME (no public ticker) plus its descriptor** — the ticker rule does
   not get silently dropped because there is no ticker.
10. **No semicolon-packed evidence lists.** If a sentence needs a semicolon to hold three claims,
    it is three sentences.
11. **A score whose components are missing cannot drive an action.** Say how many of the ten
    crowd signs are documented, and treat the reading as a floor. The page does this in code.

**Where this review and Ben disagree, Ben wins.** Codex proposed deleting the crowding label
entirely; Ben asked specifically for the gauge to be EXPLAINED. So the label stays, with what it
measures, which signs fired, and what it means for buying — which is what the page now renders
from the columns rather than from prose.

## 7. Field-by-field contract

Fields are single-line in the CSV. Use ` | ` to separate what should read as separate
paragraphs; the page renderer turns each segment into its own paragraph. A segment beginning
with `• ` renders as a bullet. Never put a raw newline in a cell.

| Field | Job | Length |
|---|---|---|
| `what_they_do` | What the company sells and who pays for it. No thesis, no verdict. | ≤ 130 chars |
| `decision_tldr` | What we are doing and the one number that governs it. Plain enough to act on. | ≤ 320 chars |
| `market_expects` | What today's price implies, in plain terms. Numbers with units and dates. | 1–3 sentences |
| `engine_says` | Our read: the mechanism, the crowd reading in full per §4, the checklist readings per §5, the two or three numbers the case rests on, and what would prove us wrong. Lead with the conclusion. | ≤ 1,800 chars, paragraphs split by ` \| ` |
| `verdict` | The decision in one plain sentence, plus the condition attached to it. | ≤ 400 chars |
| `trigger_to_analyze` | What would have to happen, with prices and dates, before anything is bought, added to or sold. Say who has to approve. | ≤ 900 chars |
| `why` | Why the name is on the list at all: the bottleneck or change it sits on, and how it makes money from it. | ≤ 900 chars |
| `bull_case` / `bear_case` | Each argument as its own sentence with its own number. | ≤ 700 chars |

**Truncation rule:** never lose a number, a date, a price level, a condition or a name while
shortening. Drop adjectives, hedges, history and self-commentary instead. If a field cannot fit
its numbers, keep the numbers and cut the prose.

## 8. Fact discipline — the part that is not about style

1. **Never invent a fact to fill the new structure.** Not a crowd-signal breakdown, not a
   checklist reading, not a date.
2. **Every number kept must already exist in the record** — the row itself, `book/journal.md`,
   `book/kills.csv`, `research/evidence-ledger.md`, or a file in `.claude/notes/`. If a number
   in the old text cannot be traced, keep it and mark it `(source not recorded)`.
3. **Do not change a verdict, a price level, a date or a decision.** This is a translation job.
   If a row's facts look wrong, leave them and report the row.
4. **Do not soften a bear case, a risk or an objection.** Plain English makes risks clearer, it
   never makes them smaller.
5. **A stale row stays stale.** If the text describes something that already happened, keep the
   history but say plainly when it happened and that it is history.

## 9. Worked example

**Before** (Klaviyo, `engine_says` as it read on 2026-07-30):

> It passed all 8 checks on our entry checklist. Our crowdedness gauge reads 2 out of 10 — very
> few investors are here yet. Working backwards from today's price, the market is pricing in only
> about 4-5% growth forever, versus the 23-28% the company is actually delivering. […]

Three failures. The eight checks are never named. The gauge's 2 out of 10 is never explained
and the two signals that fired are never identified. "Working backwards from today's price"
states a method without saying the price or the date.

**After:**

> The finding: the market is paying for a company that grows 4–5% a year forever, and this one
> is growing 23–28%. That is the whole case. | The arithmetic: at $17.22 on July 8 2026 the
> shares cost 2.8 times next year's sales and about 18 times free cash flow. Run that backwards
> and the price implies 4–5% growth in perpetuity. The company grew 23–28% in its last reported
> quarters. | Crowding: LOW. We check ten signs that investors have already piled in, and two
> are true here. One: Klaviyo joined the Russell index in June 2026, so index funds had to buy
> it. Two: insiders sold about $80 million of stock against almost no buying, 62 sales for every
> purchase. The other eight are false, including the three that usually matter most — the price
> sits below the average analyst target, no wave of big-bank upgrades, and no viral coverage. |
> The entry checklist, item by item: crowding low, as above. The story is still early, so most
> investors have not formed a view. We are buying the layer that keeps the profit, because
> Klaviyo raised prices in February 2025 and customers still spent more. […]

## 10. Before you hand work back

Run these greps over anything you wrote. Each must return nothing.

```
grep -nE '\b[0-9]+ ?(/|out of) ?10\b'          # bare scores
grep -niE '\b(gate|re-gate|wake|tier|leg|standby|armed|adjudicat|no-chase|thermometer)\b'
grep -nE '\b[SH][0-9]\b'                        # stage and hypothesis codes
grep -niE 'test [A-D]\b|check [0-9]|leg \([ab]\)'
grep -niE '\b(NRR|ADR|bps|reverse-DCF|EV/S|FCF)\b'   # undefined acronyms
```

A hit is not always wrong — "ARM" contains no banned word, "Stage 3" spelled out is fine — but
every hit must be justified deliberately, not left by accident.
