# Risk Rules — Binding Constraints

These rules exist because the biggest risk to this portfolio is its owner's conviction.
Every rule binds every recommendation. A great idea that breaks a rule gets the largest
compliant expression, with the breach noted.

This file is the binding authority. `references/playbook.md` (the Bottleneck Playbook)
supplies *behavior and structure* — the sizing ladder (§6.4), instrument payoff-shape
matrix (§8), and convexity/theta budgeting — but every numeric default there is marked ⚙️
and is **overridden by the limits in this file** on any conflict. Where the playbook
proposes a size band or option budget, this file's caps (single-name, options premium,
gross/net, drawdown protocol) are the ceiling.

---

## Onboarding elicitation (run once; store answers in state/profile.md)

Ask conversationally, one at a time. Frame drawdowns in money, not percent — percents
don't hurt, amounts do.

1. **Portfolio size** committed to this strategy (order of magnitude is fine).
2. **Drawdown pain point**: "If this portfolio went from €X to €0.75X in three months,
   would you (a) buy more, (b) hold and sleep fine, (c) hold but check prices daily,
   (d) sell something? What about €0.6X?" The answer where they'd realistically sell or
   suffer = beyond the budget. Set MAX_DD one notch safer.
3. **Existing correlated exposure**: employer-linked equity/compensation, tech-heavy
   index funds, concentrated tech holdings. Get rough % relative to this portfolio.
   If material, it counts inside the risky sleeve (same AI-sentiment factor).
4. **Cash needs**: any chance this money is needed within 3 years? That fraction goes to
   the safe sleeve, non-negotiable.
5. **Tax jurisdiction and constraints** (note for Germany: derivative-loss offset rules
   have shifted repeatedly — verify current treatment before any options-heavy design;
   quarterly turnover has tax drag vs holding).
6. **Sleeve confirmation**: Ben's starting instinct is 60% risky / 15% safe / 25%
   moderate. Show him what that implied in 2022 (speculative tech −50 to −80%: portfolio
   impact ≈ −35 to −50% with moderate sleeve down too) and confirm or adjust. Note this
   is NOT a Taleb barbell (that would be ~85–90% ultra-safe / 10–15% max-aggressive,
   nothing in between, downside capped by construction). Both are legitimate; they are
   different machines. Record which one he actually wants.

Record: MAX_DD, DERISK_LEVEL (= MAX_DD × 0.6, rounded), sleeve targets, portfolio size,
external correlated exposure %, jurisdiction.

## Default limits (apply until profile.md overrides)

| Rule | Limit |
|---|---|
| Single name at cost | ≤8% (established), ≤4% (speculative bucket: SMRs, neoclouds, space, humanoid) |
| Single theme | ≤25% of portfolio |
| Speculative bucket total | ≤20% of risky sleeve |
| Opportunistic sleeve | ≤10% of portfolio |
| Gross exposure | ≤150% of equity (1.5x) — **checked by the order guard from 2026-09-21** (review #3, Ben: "execute 1-10"): a buy that would take holdings above 1.5x net liquidation fails the GROSS-EXPOSURE check unless Ben's verbatim override for that specific order is on file (`--gross-override`). **Until Ben makes the step-3 choice the check WARNS and does not block** (`GROSS_ENFORCE = False` in `data/ibkr_order.py`). Was "≤130%" from 07-06 and never enforced. Ben's choice, pending: keep this cap (then flip the flag), or delete the 30% forced-sale-cushion line and accept the risk in writing — not both. |
| Net exposure | 40–80% |
| Single short | ≤3% at cost; sized at HALF the equivalent long risk |
| Options premium at risk | ≤1% per expression; ≤4% concurrent book-wide; annual realized theta-loss budget ≤2% of book (tightened 2026-07-13 — 6% vs a 40% risky sleeve was 15% of active risk). Every options expression must show the stock-and-cash structure it beat |
| Safe sleeve | Actual T-bills/short-duration (SGOV/BIL-type) — "safe tech" is not safe |

## Idle-capital default (added 2026-07-13, Ben-approved via explicit decision — adopted FULLY)

Undeployed risky-sleeve capital does NOT sit in cash. It sits in the policy benchmark's
risky proxy — EU-UCITS index instruments matching the policy blend (UCITS Nasdaq-100 +
UCITS semiconductor ETF; US-listed QQQ/SMH are PRIIPs-blocked — confirm exact tickers and
IBKR availability at first use, do not guess) — and is sold down as doors open.
EXCEPTION: capital reserved for a door expected to fire within ~20 trading days may wait
in cash. Why: an empty book waiting in cash is itself an active bet against the benchmark
(the book sat in cash through a +71% SMH half-year); the default must be the benchmark,
and stock-picking must displace it only through the gates. Costs accepted at adoption:
an ETF tax asymmetry (fund gains are investment income — taxed, never
offsettable; ETF losses do offset stock gains) and sell-low friction when doors open in
selloffs. The rule interacts with the drawdown ladder: parked index counts inside the
risky sleeve for both drawdown gauges.

## Correlation rule (the one-factor reality)

Power, grid, cooling, neoclouds, robotics, AV, space: assume correlation ≥0.8 in
a drawdown. Stress test every portfolio as if the risky sleeve is ONE position. Theme
count is not diversification; only the safe and (partially) moderate sleeves are.

## Moderate-sleeve quality mandate (added 2026-07-13, Ben sign-off — the deliberate consensus lane)

The **25%** moderate sleeve (cut from 35% on 2026-08-03, Ben's sign-off, to fund the risky
sleeve's rise to 50% — see `profile.md`) holds **quality compounders with real
defensibility — consensus ALLOWED.** This is Ben's risk-mitigation instinct given
structure instead of exceptions; solid-but-known names live here. **Superseded clause,
corrected 2026-08-03:** this paragraph previously said the risky sleeve "keeps its strict
anti-consensus ban." That ban was repealed on 2026-08-01 — under playbook §6.0 crowding
sizes a position and never blocks one, so the moderate sleeve is no longer the only lane
in which a well-known name may be bought. What survives is the quality mandate below,
which is a test of the BUSINESS and is unaffected by that repeal. Entry test (all three, written): (1) durability — passes the
frameworks §7 survivor screen (system of record / hard-ROI / high NRR / enterprise
base) or equivalent moat evidence; (2) valuation sanity — a written "what am I paying
for" line (multiple vs own history and vs growth; no crowding test, but no
any-price buying); (3) sizing — single name ≤5% at cost, sleeve stays ≤35%, turnover
low (holdings reviewed quarterly, not gated on triggers). Guardrails: a name REJECTED
by the risky-sleeve gate cannot be bought as "moderate" in the same month (no backdoor);
moderate-sleeve tech names still count ~fully in the one-factor correlation stress —
this sleeve mitigates single-name and thesis risk, NOT an AI-factor drawdown; and the
sleeve's benchmark honesty line applies (would this beat just holding QQQ after tax?).

## Liquidity rules (added 2026-07-13 — from the reply + external assessment)

- Minimum liquidity for ANY entry: ≥$2M average daily dollar volume (20-day) ⚙️.
- Position size ≤5% of 20-day average daily dollar volume ⚙️ — the position must be
  exitable in ~1 day without being the market.
- Every catalyst/earnings-night entry states a written GAP ASSUMPTION (what an adverse
  earnings gap does to the entry and whether the backstop can realistically execute).
- Foreign listings (Helsinki, Brussels, London, KOSDAQ, Tokyo): 1.5× the ADV minimums,
  local-hours limit orders only, and FX exposure noted in the journal entry (currency
  attribution is tracked — EUR book, USD/KRW/JPY/GBp names).
- **Spreads stated per entry (added 2026-07-14, Ben-approved):** normal bid-ask spread
  AND a stressed-spread assumption (what the spread does on a −10% day) — slippage is
  part of the excess-return arithmetic, not a surprise.
- **Backstop executability (added 2026-07-14):** every price backstop states WHEN it can
  actually execute. A Korean or Japanese backstop cannot fire while Ben sleeps unless an
  order rests at the exchange; if no resting order, the rule is "exit at next local open
  after breach" and the gap assumption must cover the overnight move.

## Drawdown protocol (rewritten 2026-07-13 at Ben's calibration; heading corrected 2026-08-03 — it said "minimum ACTIONS, not proposals," which read as though the engine transacts. It does not, and never has. What is mechanical is the engine's DUTY TO RECOMMEND; every sale is Ben's.)

Tracked on TWO gauges (added 2026-07-13): total portfolio from high-water mark AND the
risky sleeve alone — the safe sleeve must never mask failure inside the active strategy.

**WHAT "−30%" IS MEASURED FROM, because it is not obvious and Ben asked (clarified
2026-08-03): the HIGH-WATER MARK, not the calendar year.** The gauge is the fall from the
highest value the portfolio has ever reached, at any time, not from 1 January and not from
cost. So a book that runs from 100 to 150 and then falls to 105 has fallen
**30%** and has tripped the bottom rung, even though it is up 5% on the year and up 5% on
what was paid in. Contributions are handled the same way: fresh cash raises the high-water
mark, so money paid in cannot disguise a fall in the money already invested.

**AND NOTHING ON THIS LADDER SELLS ANYTHING BY ITSELF (clarified 2026-08-03, Ben: "I would
also want to question that you auto sell on my behalf; this is something that I want to
reserve for myself").** He is right to question it and the answer is that it does not
happen and structurally cannot. Two independent reasons. First, the NO AUTONOMOUS SELLING
clause below explicitly governs every clause in this file that appears to authorise a sale,
and it post-dates this ladder (2026-07-29 versus 2026-07-13). Second, this engine has no
route to the market at all: every order is placed by Ben in Interactive Brokers himself.
The words "MINIMUM ACTION, not proposal" and "forced reduction" on the two lower rungs were
written before that clause existed and read as if the machine acts. They mean: **the engine
must bring Ben a specific, written, sized reduction the same session, and may not soften it
into a suggestion or wait for a better day.** The obligation is on the ENGINE to recommend
without flinching, never on the account to transact without him. That distinction is the
whole point of the rung — it exists so that the recommendation still arrives when it feels
worst, which is exactly when a discretionary engine would go quiet.

- **Risky sleeve −12%** (whatever total is doing): freeze NEW same-factor buying;
  price-only doors close (governor §6.5 regime switch) until the hypothesis health
  check passes.
- **Total −10%**: full hypothesis health check within one session; no adds to losing
  positions until complete; price-only doors stay closed while any H1 alarm is live.
- **Total −DERISK_LEVEL (−18%)**: MINIMUM RECOMMENDATION, not a suggestion — the engine
  must put a written proposal to Ben the same session to cut the speculative bucket by
  half, unless a written per-survivor case is journaled instead; options book marked to
  its floor case. Ben decides; the engine may not omit the proposal or soften it.
- **Total −MAX_DD (−30%)**: the engine must recommend reducing the risky sleeve to 50%
  of target, in writing, with the sizes, and re-put it at every session until a full
  quarterly review passes. This rung exists precisely because it will feel wrong at the
  time — which is why the obligation to RAISE it is mechanical, while the decision to
  ACT on it stays entirely Ben's.
- Deliberately NOT adopted (2026-07-13): the external assessment's mandatory de-gross
  at −10% total — fund logic; Ben is a net buyer (steady yearly contributions, 10–15y
  horizon) whose profile deliberately trades early forced selling for behavioral
  freedom. The early rungs freeze BUYING instead.

## Kill criteria

## NO AUTONOMOUS SELLING — the overriding rule (Ben, 2026-07-29, stated twice in one message)

**This clause sits above every price rule in this file. Where any other clause appears to
authorise a sale, this one governs.**

Ben, verbatim: *"Under no circumstances, however, are you authorized to execute any trades
without my approval when these prices have been met."* And again in the same message:
*"Again, under no circumstances are you authorized to make any trading decisions unless I
tell you to."*

**What a breached level does — in this order, every time:**
1. **It fires a WRITTEN CHECK, not an order.** Two questions, both answered in writing
   before anything else: (a) is the business still sound on the measures named on its own
   position row? (b) is this a market-wide selloff or a sector frenzy rather than something
   specific to this company?
2. **Sound business → HOLD, and consider buying more.** Ben: *"If it's still solid, I think
   we should still hold and, in some cases, maybe even buy a little bit more, unless it's
   really a very, very, very significant decrease."*
3. **Failed check → bring Ben a RECOMMENDATION to sell, with the evidence, and wait.**
4. **No order is placed, amended or cancelled without a fresh instruction from Ben quoting
   the number.** A level he set once is not standing authorisation to act on it later —
   the same distinction as the ceiling-is-not-an-approval incident (governance.md).

**Why this supersedes the 2026-07-13 wording below.** That clause said a breached backstop
exits with "no new-fact test, no in-the-moment override," which reads as self-executing.
Ben has closed that reading. His stated basis: *"We also decided I'm not going to be a
trader who rotates in and out of positions constantly. That's not my style. I'm more of a
growth investor."*

**The counterweight, stated honestly every time this rule is applied — it is not free.**
profile.md records Ben's OWN logged behavioural risk as selling positions he has "lost
confidence in," and the drawdown protocol exists because conviction is the largest risk to
this portfolio. Removing the automatic sell protects against panic selling AND removes the
mechanical protection against holding a broken position too long. **The written check is now
the only thing doing that job, so it must be CAPABLE OF FAILING.** This engine has twice
written tests that could not fail. A check that always concludes "still solid" is not a
check, and a position whose check has never once been at risk of failing gets re-specified
at the next review. The SELL SCORECARD (`data/sell_scorecard.py`, spec `notes/2026-07-29-sell-scorecard-spec.md`; tests in `book/sell_tests.csv`; open recommendations in `book/sell_recommendations.csv`) is the machine-checkable form of
this: six pre-registered numeric tests, three failing produces the recommendation.

---

- Every position carries a thesis-based invalidation ("if X happens") plus a price
  backstop. **A breached price BACKSTOP fires the written check above and produces a
  RECOMMENDATION — it does not exit by itself (amended 2026-07-29; the 2026-07-13 wording
  was "exits — no new-fact test, no in-the-moment override").** Re-entry allowed through
  the normal gate. A thesis-based
  invalidation triggered → exit or journal an explicit, dated override with reasoning.
  **Override accounting REWRITTEN 2026-09-21 (review #3, Ben: "execute 1-10").** The
  two-a-year budget, the "third override blocked in advance" clause (07-13) and the 30-day
  override expiry (07-14) are DELETED: eight override entries in ten weeks against a budget of
  two showed the budget bound nothing. What replaces them: every override sits in
  `book/approved_orders.csv` with Ben's verbatim words in the `ben_quote` column (the check
  that has actually worked — it blocked a live order twice); the monthly scorecard
  (`data/scorecard_monthly.py`) counts and grades every override, split into overrides of an
  engine refusal and overrides above the engine's written maximum, because the first backtest
  showed those two behave differently (conviction overrides won; above-maximum overrides lost
  5 of 5). A count is never a limit; the grade is the discipline.
- **Moderate/quality-sleeve exception — the TWO-KEY LEVEL (added 2026-07-28, Ben-approved;
  resolves a live contradiction, freeze-exempt).** The contradiction: the rule above demands a
  price backstop on *every* position, while the quality mandate says those holdings are
  "reviewed quarterly, not gated on triggers". That second clause is about TURNOVER — don't
  trade in and out on signals — but it got read as "no exit needed", and two quality holdings (07-17,
07-28) were both carried with no exit of any kind. Neither clause was wrong; they were
  answering different questions. **Resolution: quality-sleeve holdings carry a price level, but
  it is NOT a backstop and it sells nothing by itself.** A breach fires a written ADVANTAGE TEST
  recorded on the position row: **passes → BUY MORE at a pre-set size, funded from
  contributions, selling nothing else; fails → SELL.** Same price, opposite actions; the test
  decides, never the price. Three binding conditions: (1) the test is **pre-registered while
  calm and must be capable of failing** — an un-failable test converts this rule into an
  automatic averaging-down machine, which is precisely how quality investors become
  bagholders, and this book has already twice written entry bars a company's own guidance
  already cleared; (2) the level is set **deeper than any drawdown in the name's 10-year
  history**, because the empirical finding behind this rule is that all 11 falls ≥20% across
  the two names studied in 10 years fully recovered, so any shallower level systematically sells the
  bottom; (3) it fires the analysis on a **daily close** — no multi-month confirmation wait,
  which would miss the price. Rows use trigger type `REUNDERWRITE`, deliberately NOT `BACKSTOP`,
  so the two can never be confused by a script or a reader. This exception is available ONLY to
  the moderate/quality sleeve; the risky sleeve keeps the hard backstop above.
- Hypothesis-level: 2+ falsifiers triggered on any H → exit all pure-play expressions
  of that hypothesis within one review cycle.

## Staging rule (adopted 2026-09-21, review #3, Ben: "execute 1-10" — enforced by the order guard's STAGING check)

No single day places more than 15% of an account's equity. Any list of orders whose total exceeds
10% of equity goes in tranches at least five trading sessions apart, per a written schedule in
`book/tranches.csv`. A buy in the top fifth of its trailing 20-session close range requires a
written reason in Ben's own words (`REASON:` in the approval row); a results print counts.
Why: a large share of the capital went in over two days in August 2026, just before the
AI-hardware complex fell 8%; the owner's no-engine-view purchases landed at a median 0.72 of
their 20-session range after a median +2.8% run-up and lost a median 5.1% in the next ten
sessions. Sells are never subject to this rule. Applies to both accounts.

**No-chase maximums (written maximum prices) from the same date:** they BLOCK an
engine-recommended buy, as before; on Ben's own buys they are printed as information and the
staging rule governs. **Sleeve percentages (50/25/25) are RETIRED** in favour of the
cross-account theme caps in `data/theme_exposure.py` (AI infrastructure ≤40% of combined
equity; any other theme ≤10%; any company ≤8%, both accounts summed).

## Position sizing arithmetic (show it every time)

Base size = (portfolio × single-name cap) × conviction multiplier
(high 1.0 / med 0.6 / low 0.3 or pass). Then apply: theme headroom check, sleeve
headroom check, correlation stress (would this position push a −40% risky-sleeve event
past DERISK_LEVEL?). Print all four numbers.

Trimming winners: position >1.5× its cap by appreciation → trim back to cap at next
review (not intra-quarter). Let winners run inside the risk budget, not outside it.

## Shorts & options mechanics (IBKR)

**Unlock condition (AMENDED 2026-07-21, Ben sign-off — freeze exception (d) rule
contradiction; supersedes the 2026-07-14 flat book-value leg):** shorts/options
unlock per-expression, not at a book-size threshold. BOTH must hold:
1. **Affordability test (replaces the book-value gate):** the expression is a defined-risk
   structure (long put or put spread — never an undefined-risk naked short), and ONE
   contract of the intended structure fits inside the ≤1%-per-expression premium cap at
   the CURRENT book value. If one contract does not fit, the trade is not takeable at
   this book size — no exceptions, no "small overshoot." The 4% concurrent and 2%
   annual-theta budgets apply unchanged.
2. **Pair-construction spec ratified at a review (UNCHANGED, still pending — staged
   post-freeze):** shorts must not unlock into a rulebook that has no pair rules. Until
   this leg ratifies, shorts stay locked in practice regardless of leg 1.
Why the swap (priced live 2026-07-20, arithmetic in
notes/2026-07-20-short-timing-and-unlock-design.md): the flat gate contradicted the
book's own caps — at the gate's book value, 1% was a few hundred euros, while one defined-risk contract on plausible short
candidates costs ~$2k (NVDA/ORCL ATM Dec'26) to ~$10–21k (MU), so this file prescribed
structures ("prefer defined-risk," below) its own gate could not pay for. The per-trade
test auto-scales: cheap-premium names clear at a small book; expensive ones stay locked far
above it.

- Before ANY short recommendation: check borrow fee, short interest %, days-to-cover.
  Borrow >3% needs written justification; >10% → puts or pass. Always write the squeeze
  scenario (what −20% against you in a week does to the book).
- Prefer defined-risk structures for shorts of quality/momentum names (put spreads over
  naked shorts) — the H3 short leg is exactly the kind of trade that ruins people via
  timing even when directionally right.
- Options: max loss = premium, defined at entry; no naked short options, no undefined-
  risk structures, period.
- The skill NEVER executes trades. It produces orders for Ben to review and place.

## Cadence rules

Full execution at quarterly reviews or pre-defined catalysts (earnings, filings, IPO
events) only. Between reviews: watchlist and deep-dives, no impulse adds. New position
minimum research: full 10-step analysis, no exceptions — including (especially) for
ideas Ben arrives already loving.
