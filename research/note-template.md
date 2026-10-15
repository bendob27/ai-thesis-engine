# The research note — one fixed format for every company (adopted 2026-09-21, Ben's instruction)

This is the engine's main deliverable before any purchase and the standing record on every holding.
Same sections, same order, same 14 numbers, every time, so any two companies can be read side by
side and ranked. Written in plain English for a non-engineer; no engine vocabulary. Every number
names its source and date and is graded **filing** / **call commentary** / **press**. Ratios are
computed from raw filed fields, never taken from a price vendor's pre-computed multiples.

Two lengths, one format:
- **Standard note** — about one hour: one analyst pass, then a second pass that re-opens the primary
  source for the two or three figures the recommendation collapses without. No reviewer panel.
- **Deep note** — the same document plus the reviewer panel and the Codex valuation check. Required
  above a set amount or 3% of the account's equity, and for any name entering the concentrated
  roster.

Notes live at `book/notes/<TICKER>.md`. Each results print appends an **Update** (the fixed
four-part reaction) at the bottom; the header's "as of" date moves. The weekly sell check reads
the metric named in section 11.

**Existing holdings and section 10 (Ben's rule of 2026-08-19, unchanged by the template).** A holding gets no new value and no refresh unless Ben names the company or an ADD is proposed. For a note written on an existing holding without such an ask, section 10 states "no value refresh — held under its invalidation" and the size band applies only to new money if an add is ever proposed. A note never produces a sell on price; the sell test is the kill metric in section 11. (The 2026-09-21 ASML note carries a full section 10 as the template's proof; Ben decides whether holdings' notes keep it.)

A **NO** in section 1 is allowed only for a business, balance-sheet, legal-access or fraud fact,
and must name it. Price, crowding and consensus never refuse a name; they set the size band in
section 10.

---

```
# <Company name> (<TICKER>) — <one line: what it sells and to whom>
As of <YYYY-MM-DD> · Price <ccy> <x> (settled close <date>) · Market cap <x> · Our value <x> (<method>, <date>) · Size band: full / half / quarter / zero-until-<level> · Recommendation: <one sentence>
Note type: standard | deep · Author pass: <model> · Fact-check pass: <model> · Panel: yes/no · Codex valuation check: yes/no

## 1. Investment summary (five bullets)
- Why own it:
- Why now:
- What the price already assumes:
- What would prove it wrong (the sentence that goes into the holding's record, no price in it):
- Recommendation and size:

## 2. Key numbers (the same 14 for every company; source and grade beside each)
| Figure | Value | Period / basis | Source, date, grade |
|---|---|---|---|
| Revenue, trailing twelve months | | | |
| Revenue growth, year on year | | | |
| Gross margin | | | |
| Operating margin | | | |
| Free cash flow and margin | | | |
| Capital spending (and as % of operating cash flow) | | | |
| Stock compensation as % of revenue | | | |
| Net cash or net debt | | | |
| Share count and one-year change | | | |
| Price to sales (trailing) | | | |
| Price to free cash flow (trailing) | | | |
| Consensus revenue, next two fiscal years (analyst count, pull date) | | | |
| Consensus earnings per share, next two fiscal years (analyst count, pull date) | | | |
| Next results date (from the company's own notice, never a vendor) | | | |

## 3. Business
What it sells, to whom, how it makes money, unit economics, the constraint it owns or depends on.

## 4. Market and competition
Category growth, share, who is gaining, which layer of the stack captures the economics,
what must become true for the market to be much larger.

## 5. Product evidence (the operator's read)
Is adoption accelerating? What do customers actually use it for? Is pricing power improving?
Is usage leading the reported numbers? One dated, falsifiable paragraph, plus the single
observation that would flip it.

## 6. Management and capital allocation
Founder or management record on hard calls; dilution and incentives; credibility on past
product and financial promises.

## 7. Financials
Five-year table (revenue, growth, gross margin, operating margin, free cash flow, capital
spending, stock compensation, net cash) plus the next two years of consensus with count and
vintage. Any "adjusted", "underlying" or "ex-" figure states its basis and whether the excluded
item is one-off or permanent.

## 8. Balance sheet and financing
Debt maturities, refinancing needs, off-balance-sheet and lease commitments, customer
concentration, contract quality.

## 9. What the price implies
A three-line reverse discounted-cash-flow: the growth, margin and duration the current price
requires. The market's story in two lines; ours in two lines. The trade exists only where they
diverge.

## 10. Our value and the size band
Method v3 (frameworks §11): dated horizon; year-by-year bridge; exit multiple derived from the
company's own trajectory and printed beside today's; scenario odds with a written reason each;
annualised expected return beside the 6.5% index comparison and the 12% / 10% objective.
Then the size band: full (expected return clears the objective), half (clears the index, not
the objective), quarter (positive but below the index), zero-until-<level> (below zero).
The band is a size, never a refusal.

## 11. Risks and the kill case
Ordered: accounting quality · leverage and refinancing · dilution · customer concentration ·
competitive displacement · regulation · capital intensity · contract quality · execution record ·
valuation. End with ONE sentence: the single factor most likely to destroy the case, the exact
metric that would show it (line item, source, threshold, direction), and the earliest date it
could be observed. That metric is the holding's sell test.

## 12. Catalysts and calendar
Next results date; dated events (regulatory, contract, product); what each one tests.

## 13. Portfolio fit
Which belief it expresses; theme exposure across both accounts today against the cap; whether
the other account already holds it and at what weight.

## 14. Five grades, one sentence each (1 = weak, 5 = strong)
Business quality · Growth durability · Balance sheet · Management · Valuation

## 15. Trade card
- Theme room across both accounts:
- Position in the trailing 20-session range and the 5-session run-up:
- Premium or discount to our value → size band:
- Staging room today (15% of equity per day; tranche schedule if a basket):
- The invalidation sentence (from section 1):
- Verdict: place / place in tranches / refuse, because <fact>

## 16. Sources
Every filing, call and article with date and grade. Press-grade claims marked as such.

## Update <YYYY-MM-DD> — results reaction (appended at every print)
1. Objective read, independent of our position:
2. Spillover to other holdings:
3. Our view and action:
4. Anything else relevant:
```
