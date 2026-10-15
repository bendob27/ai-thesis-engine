# Research-provider baseline — the positions the monthly sweep diffs against

**Purpose.** This file holds what each research shop currently thinks, so that next month's
sweep reports **what changed** rather than re-stating the world. A monthly report that repeats
last month's findings is noise; the whole value is the delta.

**Owned by:** `/provider-sweep` (local) and the monthly cloud routine (15th, 06:00 UTC).
**Numeric companion:** `book/provider_tracker.csv` — append-only, one row per metric per reading.
**Full month-0 writeup:** `notes/2026-07-28-research-provider-sweep.md` and the 10-page PDF
`notes/Research-Provider-Sweep-2026-07-28.pdf`.

**How to update:** overwrite the POSITION column when a shop's view genuinely moves, and log the
move in the change log at the bottom with the date, the old value, the new value and the quote
that justifies it. Never overwrite silently — the change log is the memory.

---

## Month 0 — established 2026-07-28

### The five convergences (what everyone agreed on at baseline)

| # | Convergence | Strength at baseline | What would break it |
|---|---|---|---|
| C1 | AI capital spending is real and macro-scale | **9 sources, zero dissent** | A hyperscaler cutting guided capex; tech capex share of investment falling two quarters |
| C2 | The productivity payoff is not visible in aggregate data | **9 sources** | US productivity sustaining >3% for two quarters; a TFP regime probability above ~50% at the SF Fed |
| C3 | Financing has shifted from cash flow to debt | **6 bodies** | Hyperscaler free cash flow rising again; AI share of IG issuance falling back toward its share of stock |
| C4 | Revenue circularity is real and now measured | **4 sources** | The two-counterparty share of cloud backlog falling materially, or their revenue compounding into the commitments |
| C5 | Concentration at a record, and broader than AI | **4 sources** | The excess CAPE yield normalising, especially the ex-top-30 version |

### Per-shop positions at baseline

| Shop | What it is | Position at 2026-07-28 | Next scheduled publication |
|---|---|---|---|
| **BIS** | The central banks' own bank, Basel | Most alarmed official body. First to model the sector's net economic surplus turning **negative**. "Shadow borrowing" via joint ventures. Direct lenders quadrupled AI/IT exposure to ~15% of portfolios | Quarterly Review: Sep · Annual Report: Jun |
| **IMF** | Emergency lender to governments | Two-sided, tilted down. Stability impact "modest currently" — but needs **~30% S&P / ~35% Nasdaq EPS growth** to normalise valuations. Baseline assumes **no** productivity boost | WEO update: Oct · GFSR: Oct |
| **Bank of England** | UK central bank | **The sharpest document in the set.** Leverage language escalated hard: prime brokerage at record levels, **+40% y/y**, concentrated in semiconductors. Says the valuation stretch is **broader than AI** | FSR: Dec |
| **US Federal Reserve** | US central bank | Equity premium near a **20-year low**; private credit **$1.4tn**. Says dealers report **no change** in hedge fund leverage — contradicts the BoE | FSR: ~Nov · NY Fed household debt: Aug |
| **ECB** | Euro-area central bank | Dovish outlier on private credit — euro-area exposure "limited", risks second-round | FSR: Nov |
| **OECD** | Rich-countries research body | Growth cut; AI a named **corporate-credit amplifier**. **2,500 GW** stalled in grid queues. **No** widespread labour displacement, US excepted | Outlook: Dec |
| **World Bank** | Development lender | First edition to use the word **"bubble"**. Productivity gains "so-far-limited" | GEP: Jan |
| **Stanford HAI** | Stanford's AI institute | Adoption **79%** (its own highlight says 70 and is wrong). **Dropped token pricing entirely** — AI unit economics no longer computable from public sources | AI Index: Apr |
| **NBER** | US academic economics clearinghouse | Key result: AI lifts code **+180%** but shipped releases only **+30%**. Exposure indices explain just **14%** of adoption variance | Weekly, un-refereed |
| **NBIM** | Norway's sovereign fund, owns ~1.5% of everything | Concentration "never seen before in the fund's history"; 10% of returns from seven US tech names | Half-year: 12 Aug |
| **Oaktree / Marks** | Distressed-credit investor | Splits the bubble question five ways. Hyperscaler equity "unlikely ruinously excessive"; startups are "lottery tickets". **The bubble he describes is in the debt.** Dates the software tipping point to **early Feb 2026** | Irregular, 6–10/yr. **Only 2 in 2026** |
| **PIMCO** | Best-known bond manager | "**The credit loss cycle is upon us**" — but with **zero** default rates, PIK shares or recovery rates. Assertion with named mechanisms, not measurement | Secular: Jun · Cyclical: ~3x/yr |
| **GMO** | Grantham's value shop | **−8.1%/yr** real on US large-cap. Software is **40% of recent buyouts**, a full quality decile below small caps. Its own equity fund is long TSMC/Broadcom/Microsoft/Alphabet — a split house | Quarterly letter · **7-yr forecast updates MONTHLY** |
| **AQR** | Quantitative manager | **+3.9%/yr** real on US large-cap — 12 points above GMO. Refuses to call a bubble at the 75th percentile. Private equity at 4.2% is the outlier claim | CMA: Jan · Perspectives: irregular |
| **Research Affiliates** | Index designer | Hardware "**becomes economically obsolete before it is physically obsolete**" — capital churn, not deepening. **The most falsifiable bear claim in the sweep** | 10-yr tool updates MONTHLY (login-walled) |
| **Man Group** | Largest listed hedge-fund firm | The wave model: chips → infrastructure → software last. Calls it "**the bubble everyone can see and no one wants to leave**". Pressure point **2027** lock-ups. Model fitted to **mobile internet 2010–16** only | Weekly notes · outlooks semi-annual |
| **Apollo** | Private-credit manager | **Most decision-useful funding data, published against its own book.** Cover ratios **~5x Feb → below 2x Jul**. Only house linking the AI trade to the **dollar** | Daily |
| **KKR** | Private markets | Inflation **above** consensus (3.6% vs 3.3%). Tech capex **+18.4%** while other capex is **−3.5%**. "Less good about the supply/demand setup for equities than a year ago" | Mid-year: Jun · outlook: Dec |
| **BlackRock** | Largest asset manager | **Overweight US equities** as breadth insurance — "we do not need to know which AI model wins". Trigger to change: a **margin/earnings miss**, not a valuation level | Midyear: Jun · outlook: Dec |
| **Vanguard** | Index funds | **Most credible on the adverse-interest test** — an index house forecasting ~5% US equity returns. Fed **on hold**, no cut, no hike | Rolling updates |
| **PGIM** | Multi-asset manager | **The outlier: three Fed HIKES in 2026.** Private credit "defying headlines". Tech capex at **0.83pp vs the 0.93pp dot-com peak** | Mid-year: Jun |
| **Brookfield** | Real assets, owns Westinghouse | Loudest power supercycle — 17%/yr datacenter growth, **106 GW by 2035**. Sells exactly this | Outlook: Dec |
| **PIIE** | Trade-policy think tank | Tariffs average **~12%** from 2.5%; **$189bn** collected = 3.4% of federal revenue; borne "almost entirely by US households and businesses" | Several briefs/month |
| **a16z** | Venture firm | Idea source only, **grade C**. Big Ideas set published **Dec 2025** and re-marketed through 2026 — date-check anything that looks like news | Irregular |

### The seven live disagreements at baseline

| # | Question | Split | Resolves when |
|---|---|---|---|
| D1 | US large-cap real return | GMO −8.1% vs AQR +3.9% | Never cleanly — watch whether the **gap** widens or closes |
| D2 | Is AI credit systemic | BIS/PIMCO yes vs IMF/ECB no | IMF Oct GFSR · ECB Nov FSR |
| D3 | Hedge-fund equity leverage | Fed "no change" vs BoE "+40%, record" | Fed FSR Nov · BoE FSR Dec |
| D4 | Which layer gets paid | Man Group waves vs RA capital-churn | Watch software de-rating vs infrastructure |
| D5 | Next Fed move | PGIM 3 hikes vs Vanguard hold | Each FOMC |
| D6 | Private credit health | PGIM "improving" vs Apollo "stress real" | Apollo publishes continuously |
| D7 | Labour displacement | OECD "none" vs Stanford/BIS "visible" | OECD Dec · AI Index Apr |

### Open questions carried forward

1. **RA's depreciation claim** — hardware obsoletes before it earns back. Most falsifiable bear
   claim found; owed a dedicated test.
2. **Our software durability screen** is built on exposure-style reasoning, which NBER says
   explains only 14% of actual adoption. Owed a rebuild on comparative advantage.
3. **ASML installed-base service revenue by country** — never disclosed; every services-ban
   estimate is an assumption. Watch each quarterly report for a country split.
4. **AI unit economics are no longer computable** from public sources. Watch whether any
   credible substitute series appears.

---

## Change log

Append one line per genuine position move. Format:
`YYYY-MM-DD · SHOP · axis · OLD -> NEW · the quote that justifies it · cite`

- 2026-07-28 · BASELINE ESTABLISHED · 24 shops read at publisher sites by 8 parallel agents · no prior state to diff against · notes/2026-07-28-research-provider-sweep.md
- 2026-09-15 · SWEEP RUN, NO POSITION CHANGED · all 24 shops carried at baseline · this session's browsing tool was blocked from reaching nearly every publisher site (Oaktree, FRED, BIS, Wikipedia and others all returned "blocked by the network's outbound filter"); only web search worked, and one search summary falsely suggested a new Howard Marks memo that turned out to be from 2022 · only fresh figure found: US Q2 2026 productivity 1.4% annualised (was 0.29% Q1), SECONDARY grade · notes/2026-09-15-provider-sweep.md
