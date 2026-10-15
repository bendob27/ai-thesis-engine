# Analysis Frameworks & Output Templates

Use these templates exactly — consistency is what makes the journal scoreable.

---

## 1. News triage template (≤150 words total)

```
NEWS TRIAGE — <headline> — Data as of <datetime>
Relevance: <0-5> — <one line why>
Hypotheses: <H# confirm/weaken, magnitude 1-5> (only those affected)
Tickers: <long book / short book / watchlist names affected>
Priced in? <what the market has already discounted; what it hasn't>
Action: ignore | add <ticker> to watchlist | schedule deep-dive | review position <X>
```

Scoring guide: 5 = falsifier or strong confirmer of a hypothesis triggered (rare);
3 = updates an indicator meaningfully; 1 = thematic noise, already priced. Most AI news
is a 1 — the theme is famous. Relevance comes from *surprise relative to expectations*,
not topical match. If action ≠ ignore, append a dated line to `state/journal.md`.

---

## 2. Company analysis template (the 10 steps — none optional)

```
ANALYSIS: <TICKER> — Data as of <datetime> — Sources: <list>

1. BUSINESS  What it does in ≤3 lines; where it sits on the bottleneck map
   (which constraint it owns; what solved constraint it depends on).
2. HYPOTHESIS LINK  Which of H1–H5 this expresses; how pure a play (pure/partial/diluted).
3. LIVE DATA  price, YTD%, mcap, EV/S, fwd P/E, rev growth, gross margin, FCF,
   short interest, 50/200dma — from fetch_market_data.py + web. Timestamped.
   Any comparative claim vs a peer ("cheaper than", "faster-growing than", "same
   socket as") must show BOTH names' live numbers side by side in the output.
   Comparisons are never inherited from a prior note or an agent's assertion
   (rule added 2026-07-07 after the CAMT-vs-ONTO fwd-P/E error).
3b. PRODUCT EVIDENCE (the Fisher step — added 2026-07-29, Ben-approved)
   Is the product actually winning with real customers? Answer from what an OPERATOR
   reads, not from what an accountant reads — see §9 for the method and its limits.
   Output is ONE dated, falsifiable paragraph: "this product is gaining / losing ground
   with its users, because X", plus the single observation that would flip it. It is
   scored at review like any price call. This step INFORMS the verdict and never blocks
   it (§9).
4. EXPECTATIONS AUDIT (the Baker step — most important step)
   Reverse-engineer the price: what revenue growth, margins, and duration does the
   current valuation imply? (Simple reverse DCF or comparable-multiple bridge is fine —
   show the arithmetic.) State the market's implied story in 2 lines.
   Then: my story. The trade only exists where the two diverge.
5. SCENARIOS  Bear / Base / Bull: probability, 12-24mo price, key driver of each.
   Expected value calculation. If EV ≈ current price the SIZE BAND is quarter, or
   zero-until-<level> — a price never refuses a name (2026-09-21, review #3: refusals on
   price cost Palantir +37.7%, ServiceNow +24.5%, SpaceX +33.3%; refusals on the business
   were right). A NO is allowed only for a business, balance-sheet, legal-access or fraud
   fact, named with source and date. The full write-up now follows
   `research/note-template.md` (the standardized research note); these ten steps are its
   working method, the note is its output.
6. PRE-MORTEM (the Dalio step)  "It is July 2028 and this position lost 60%.
   The story of what happened is: ..." Write it as narrative, not bullet hedging.
7. STEELMAN  The strongest current argument on the other side, including what
   Aschenbrenner's/Baker's actual positioning implies about this name. In earnest.
8. TRADE STRUCTURE  Instrument (shares/options — if options: strike, expiry, max loss);
   size per risk-rules.md WITH ARITHMETIC SHOWN; entry approach; invalidation level
   (thesis-based: "if X happens" — plus a price backstop); review trigger; horizon.
   For shorts: borrow cost, short interest, days-to-cover, squeeze scenario. Borrow >3%
   requires explicit justification; >10% use puts or pass.
9. CONFIDENCE  low/med/high + the specific new information that would change it.
10. JOURNAL  Append the dated call to state/journal.md (see journal format below).
```

If steps 4 and 6 feel like they're fighting the conclusion — good. That's the design.

---

## 3. Quarterly review template

```
QUARTERLY REVIEW — <quarter> — Data as of <datetime>

A. PERFORMANCE  Portfolio return vs TWO benchmark classes (split adopted 2026-07-13):
   (1) POLICY benchmark — a blend matching the sleeve structure, which changed on
   2026-08-03 to **50% risky / 25% moderate / 25% safe** (50% QQQ or SMH-tilted risky
   proxy · 25% quality/lower-beta proxy · 25% EUR T-bill/cash index); it was 40/35/25
   until that date, so any comparison spanning the change must state which blend applies
   to which period rather than restating history at the new weights. This is the fair
   test of the whole portfolio; (2) OPPORTUNITY-COST benchmarks — QQQ, SMH,
   and the equal-weight universe basket, the fair test of individual active ideas.
   Attribution: top/bottom 3 contributors + factor-vs-selection split where computable.
   The honest question, answered every quarter: is this process beating its policy
   benchmark, and are the active ideas beating QQQ/SMH? Over a full cycle, if not —
   the rational trade is the index. Currency attribution noted (EUR base).
B. HYPOTHESIS HEALTH  For each H1–H5: current indicator readings → strengthened /
   neutral / weakened / FALSIFIER TRIGGERED. Update conviction scores in thesis.md
   with dated change-log entries.
   H5 dashboard metrics (adopted 2026-07-07, SA-essays deep pass): RLI automation rate
   (remotelabor.ai; 16.1% Jul-26, was 2.5% Oct-25) + METR 50%-success time-horizon
   (14h30m, doubling ~4.3mo). Surgical H5 shorts re-arm ONLY at RLI ≥~30–40% in the
   target vertical or METR ≥ workweek rung; same metrics set the re-entry clock on
   agent-exposed names sold on fear.
   Plus four disclosed seat-stream indicators (adopted 2026-07-07, H5 second-order
   map; baselines in notes/2026-07-07-h5-second-order-map.md): ADP US pays-per-control
   YoY (baseline +1%, was +4% FY23 — first NEGATIVE print = seat contraction live →
   reopen the surgical-short screen); NSP paid worksite employees (guide −1/−2.3%) +
   TNET WSEs; NSP new-client WSEEs (baseline −7%; −15% = firms forming without
   employees, the agent-native-company signal); CDW netted-down GP contribution
   (absolute decline arms the channel WATCH-shorts).
C. JOURNAL SCORING  Grade every journaled call now resolvable: right/wrong on
   direction, and right/wrong for the stated reason (four quadrants — right for the
   wrong reason is luck, log it as luck). Running hit rate and calibration note.
   C0. CALIBRATION LEDGER (adopted 2026-07-13, phased in as calls resolve): for each
   resolved call also score — forecast calibration (did stated-confidence buckets hit
   at their stated rates?), causal accuracy (did the named driver drive it?), valuation
   error vs timing error (right thesis, wrong entry?), and factor-vs-selection (would
   the sleeve's index have done it anyway?). Completing ten analytical sections is not
   calibration; only this scoring is.
   C1. ATTEMPT COUNT  Report hit rate over the SCREEN denominator, not just survivors
   ("8 of 53 screened"), carried forward from the SCREEN journal entries. The more
   names sifted, the more of the winners are luck. A name surfaced by a wide sweep
   carries a HIGHER conviction bar than one reached by a deep dive; state both counts.
   C2a. REFUTATION ORDERING (added 2026-07-14, Ben-approved): the independent refuter
   receives the EVIDENCE (thesis, data, expected path) but NOT the proposed action or
   size, and its verdict is logged BEFORE the operator decides. A refuter that knows
   the analyst wants ENTER 2% is anchored; a refuter that only knows the claim can
   kill it honestly.
   C2. NEGATIVE DECISIONS  Grade every kill, pass, and exit — never against hindsight
   regret ("it went up after we sold"), always against a stated counterfactual:
     · KILL / PASS  → name's total return since the kill date vs the equal-weight
       universe basket over the same window (book/kills.csv holds date + price + reason).
     · EXIT / TRIM  → vs (a) having held, and (b) selling a randomly-chosen other book
       position to raise the same cash. (b) is the real judge: institutional sells
       underperform a random sell by ~100bp/yr — Akepanidtaworn, Di Mascio, Imas &
       Schmidt, "Selling Fast and Buying Slow," Journal of Finance 2023, 4.4M trades.
   Each graded into four boxes: CORRECT (moved our way, for our reason) · LUCK (moved
   our way, wrong reason) · ERROR (moved against us, and the deciding fact was public
   and reachable on the decision date — name the source we failed to check) ·
   UNKNOWABLE (moved against us, and NO public information available that day would
   have changed the call). UNKNOWABLE is a real category and not a mistake, but it is
   also the escape hatch that lets the engine never be wrong: to use it, state the
   specific fact that was missing and why it was unobtainable. Track the UNKNOWABLE
   share of all misses — if it exceeds ~1/3, we are rationalizing, not measuring.
   C3. SALIENCE CHECK (exits)  The same paper's mechanism: bad sells are triggered by a
   big price move, good sells by new information. Any exit must cite the NEW FACT that
   changed the thesis. If the only new fact is that the price moved a lot, it is not an
   exit — it is a rebalance; route it to the §6.4 sizing ladder. NOTE the live tension:
   playbook §7.1's +100%/+25% trailing review is itself a salience trigger. It survives
   only because it demands a written decision rather than a sale; keep it that way.
D. INFLUENCE REFRESH  fetch_13f.py if new filings due; update disagreement register.
E. REGIME CHECK  Capex second derivative; rates; Taiwan/export-control tail; credit
   conditions for neocloud debt.
F. REBALANCE PROPOSAL  Concrete: trims, adds, exits, new positions — each with
   one-line rationale and risk-rule check. Include "do nothing" as a scored option.
G. SLEEVE AUDIT  Actual sleeve weights vs targets (incl. any material external
   correlated exposure); drawdown headroom vs protocol levels.
H. PROCESS SCORECARD + PRUNE (added 2026-07-14, Ben-approved, from the fourth external
   review — the anti-bureaucracy loop): publish counts for the quarter (kills acted on ·
   overrides used/expired · doors opened/blocked by the governor · benchmark defaults
   chosen over ideas · triggers graded fired/mis-specified/stale) AND name at least the
   rules CONSIDERED for deletion, with a keep/delete verdict each. A ruleset that only
   grows becomes decoration; every review must prove the machine is getting simpler or
   say why not.
```

---

## 4. Journal format (state/journal.md — append-only, never edit past entries)

```
## 2026-07-06 | ANALYZE VRT | Rec: PASS (fairly priced) | Px: $XXX.XX
Thesis link: H2. Reason: expectations audit implies 30%+ growth for 5y at 52x fwd —
no divergence from my story. Confidence: med. Review: Q3 earnings (orders growth).
Consensus: EXTREME (above target #1; ≥3 upgrades #2; fwd P/E >2× median #3; viral #4;
 IV elevated #6) — sizes the position, never a veto (2026-08-01). Origin channel: own research.
Lifecycle stage: S3 | Layer: second-order power equipment, profit pool HELD (take-or-pay
 backlog, multiple desperate buyers). Clock: S | Instrument: n/a (PASS — money test fails vs index).
Sequence intended (FP-8): n/a. Validation events so far: 0 new since last look.
Kill condition: orders decelerate 2 quarters (H2/H1 falisifier) OR book-to-bill <1.
Migration-test answers (if shock-driven): n/a.
```

One entry per call. Base fields (always): date, mode, recommendation, price at call,
hypothesis link, one-line reason, confidence, review trigger. **Playbook fields (add for
any entry / watchlist change, per playbook §12.1):** Consensus label (LOW/MODERATE/HIGH/
EXTREME) with indicators cited — it sizes, never gates (2026-08-01); Origin channel
(own research / screen / viral-tracker — disclosed always; the automatic min-score-5
floor was retired 2026-07-29); Lifecycle
stage S0–S4; Layer (first/second-order + profit-pool note); Clock (S structural / T
tactical); Instrument + why this payoff shape (§8, log strike/expiry/premium for options);
Sequence intended (FP-8); Validation events so far; Kill condition; **Product evidence
(§3b/§9 — the dated falsifiable paragraph plus the observation that would flip it; write
"not gathered" if it was not, never leave it blank);** Migration-test answers
(Q1/Q2/Q3 verbatim if the entry is shock-driven, §5); **Edge (falsifiable, §5 rule) and
Expected path (assumptions + thresholds + checkpoint dates) for any entry-candidate or
position**. Scoring happens at quarterly
review — an unjournaled call never happened. **Playbook-rule violations are journaled too**
(§13 anti-patterns): name the rule broken and why.

---

## 5. Screening framework (finding new names)

Long screens, run per theme (see universe.md):
- **Next-bottleneck screen**: lead times rising + order backlog growing + capacity
  additions slow (>2y) + NOT re-rated (multiple vs 3y history) → the H2 sweet spot.
- **Expectations-gap screen**: strong indicator readings + lagging multiple vs theme
  peers → verify it's mispricing, not a broken business.
- **H5 long leg**: post-crash software, usage-based pricing, proprietary data, NRR >110%.

Short screens:
- **H5 surgical short**: per-seat/per-hour revenue + no data moat + agent-replaceable
  tasks + NRR declining + consensus still models recovery. All five or no short.
- **Solved-bottleneck rotation**: H2 names where lead times normalize while multiples
  remain at peak — trim/exit longs first, short only with a catalyst.

**Dual-trigger rule (added 2026-07-07).** Every WATCH verdict must state TWO triggers:
(a) a price trigger, and (b) a non-price trigger — a validation event, a dated catalyst,
or a time-stop. A screen whose every verdict is "buy a −25/30% pullback" is an implicit
market-timing bet: the book earns nothing if the cycle keeps running, and in a real −30%
drawdown the CAUSE of the fall (H1 breaking) may gate the buy anyway. The 2026-07-07
11-name chain screen exhibited exactly this monoculture. Non-price triggers let the
system enter on evidence, not only on crashes; the quarterly review grades trigger
quality (fired / mis-specified / stale).

**Aggregate-decomposition rule (added 2026-07-10, Ben-approved; generalizes the 07-08
trigger-writing rule).** Any reported aggregate that drives a verdict or trigger —
backlog, bookings, contract intake, insider-filing counts, capex commitments, financing
structures — is decomposed BEFORE it is cited: name the largest single component and its
share, date each component (new vs re-announced), and state what the residual is doing.
First reads systematically overstate the exciting interpretation; 07-06→07-10 produced
five same-direction instances (BWMN backlog 85% one contract; QQ.L "record intake" held a
year-old extension; HSAI's trigger had already fired; AMSC "22 insider sales" = tax
withholding; Cerebras customer-prepayment misread as circular financing). A claim built
on an undecomposed aggregate is mis-specified by definition.

**Door-spec checklist (added 2026-07-10, Ben-approved).** Before a trigger/door is written
or honored, check all five — from four mis-specifications in four days (QQ.L's stale
"record intake," AAOI's chased-after-tripling fire, BWMN's misread backlog, the NVDA
segment door NVIDIA made unfireable by restructuring its own disclosure):
1. **Not issuer-redefinable.** A door keyed on a company's own reporting line (a segment
   name, a disclosure category) breaks silently if the company changes how it reports —
   confirm the underlying fact, not just the line item that currently carries it.
2. **Share, not headline** (the aggregate-decomposition rule above).
3. **A no-chase ceiling.** Every price door states the level above which it's no longer
   worth entering, so a fire after a run-up doesn't get bought anyway.
4. **Checked for liveness at every /review.** Does the door still make sense given
   everything learned since it was written, not just whether its condition fired.
5. **Graded fired / mis-specified / stale BEFORE being honored** — never acted on reflexively.

**Edge + expected-path rule (added 2026-07-08, Ben's feedback).** Every ENTRY-CANDIDATE
and every position carries, from its Mode-2 analysis onward:
(a) an **edge statement** — one falsifiable sentence: "the market prices X; we believe Y
because Z; we are wrong if W." Not a description of the company — a claim about the
*mispricing*.
(b) a **pre-registered expected path** — the 2–3 load-bearing assumptions the trade
rests on, each with a numeric threshold and a dated checkpoint (the next 1–2 prints).
Checkpoints are graded when they land: a BEAT is a validation event (feeds the §6.4
add-ladder); a MISS runs the kill-condition test — never silently absorbed.
(c) a **benchmark hurdle** (added 2026-07-13, Ben-approved; closes the gap the external
deep-research review correctly flagged — the 07-12 reply promised this at entry, but only
the review-time policy benchmark had landed). One line of arithmetic answering: why does
this position beat just holding the opportunity-cost benchmark (SMH/QQQ or the sleeve's
index proxy) from HERE, net of the 26% capital-gains tax and expected turnover? The
line must contain numbers (implied vs expected growth, multiple gap, or expected-path
math), not adjectives. If the hurdle cannot be stated numerically, the capital stays with
the benchmark — a weak answer defaults to the index, never to a forced idea. Written at
entry, re-graded with the (b) checkpoints and in the §3.A calibration ledger.
Quantification floor (added 2026-07-14; **SUSPENDED BELOW A MINIMUM BOOK SIZE AND RE-BASED ON THE THESIS
HORIZON 2026-07-29, Ben-approved**): the line states the EXPECTED EXCESS RETURN over the
benchmark, after tax and turnover, **over the horizon the thesis itself claims — not a
fixed 12–24 months** — plus a REVERSION DATE: the specific non-consensus event, and the
date by which, if it has not occurred, the capital returns to the benchmark.

**Two amendments, 2026-07-29, both on Ben's explicit sign-off.**

**(a) The horizon follows the thesis.** A duration entry under playbook §6.1 check 5 states
its excess return over the years it actually claims, evidenced by the five-year
owner's-earnings card above — NOT over 12–24 months. Why: a duration thesis is a claim
about years 3 through 10, so a 24-month hurdle fails it almost by construction. Leaving it
would have capped every duration idea at probe size permanently — the same defect fixed in
the entry gate the same day, one layer down. **Guard: the longer horizon must not become
the easier gate.** A duration case may use the five-year number ONLY if that card survives
its mandatory 30%-lower exit-multiple sensitivity. Failing that, it reverts to the
short-horizon test.

**(b) The ≥2% / ~10-point thresholds are SUSPENDED until the book reaches a minimum size.** Ben,
2026-07-29: *"any position that is very, very significant in our total book needs to earn
its keep. However, that is assuming at scale."* Both
numbers came from an external reviewer on 2026-07-14 and were never tested against this
book's own record — Ben: *"It seems arbitrary… I feel like we need to look at this really
on a case-by-case basis and not come up with these random, arbitrary numbers a priori."*

**What binds while suspended (a suspension, not a deletion):**
1. **Every entry still states an expected excess return with arithmetic shown, and still
   states a reversion date.** The DISCIPLINE of quantifying is untouched; only the two
   fixed thresholds are.
2. **Sizing runs on conviction and the risk-rules.md caps**, which are unchanged and bind
   absolutely.
3. **Every such call is GRADED at review** — did the stated excess return arrive, over the
   stated horizon, for the stated reason? Ben: *"on the basis of empirical data, we can then
   make better decisions. We can always use a rule of thumb that is actually tested and
   tried."* This grading IS the replacement rule being built.
4. **At that size the thresholds are re-derived from our own graded record**, not restored from
   the reviewer's figures. If the record is too thin to derive them, say so plainly and
   extend the suspension — do not quietly reinstate 2% and 10 points.
5. **Standing risk, stated because a suspended hurdle is a removed constraint:** the floor
   existed to stop a weak idea being sized like a strong one. Until the graded record
   replaces it, the panel and the caps are the only things doing that job. A pattern of
   large positions with thin excess-return arithmetic is this suspension failing, and it is
   reported at every review.
Scope guard: WATCH rows do NOT get full expected paths — their non-price trigger already
pre-registers the single assumption that matters, and review-time trigger grading covers
the rest. Track 2–3 assumptions, not "everything": registering happens BEFORE the print,
grading AT the print, action at review/catalyst (cadence guard). This is anti-drift
machinery, not a license to re-litigate names daily — and a deviation is evidence to
process, not an automatic exit (confidence-based selling is the profiled behavioral
risk, not a rule).

**Compounder second yardstick (added 2026-07-29, Ben-approved).** The benchmark hurdle
above is a 12–24 month instrument. Applied ALONE to a durable compounder it reads FAIL
almost by construction, because a compounder's return comes from the DURATION of growth
rather than from a multiple closing inside two years. Not theoretical: all four valuation
cards built 2026-07-28 (ASML, TSM, MBLY, WRT1V) priced a below-benchmark return on a 12–18
month probability-weighted basis, and three of the four are positions Ben took anyway.

So: any name classified a **DURABLE COMPOUNDER** at entry carries TWO valuations, and Ben
sees BOTH, never a blend (same rule as the Fable/Codex disagreement — the gap between them
is the output):
(a) the existing **12–24 month probability-weighted card** — unchanged;
(b) a **five-year owner's-earnings return** — project free cash flow to year 5 from the
    stated growth and margin path, apply an EXIT MULTIPLE written down as an explicit
    assumption with its justification, and state the annualised return after a 26%
    flat tax.

Three binding conditions on (b):
1. **The exit multiple is shown separately and never buried.** A five-year case that only
   works through multiple expansion is a multiple bet wearing a duration costume, and the
   card must say so in those terms.
2. **Sensitivity is mandatory** — state the annualised return at the base exit multiple AND
   at a multiple 30% lower. If the case dies at the lower multiple, the position is a bet
   on sentiment rather than on the business; say that plainly and size it as such.
3. **The compounder label is not self-awarded.** Classification requires the §7 durability
   evidence or equivalent written moat evidence. The label may never be applied to rescue a
   name that the 12–24 month card just failed — that inversion is the whole failure mode
   this yardstick could otherwise create.

Retro-run OWED on the four 2026-07-28 cards.

---

## 6. Believability weighting (when sources conflict)

Rank inputs by skin-in-the-game and track record: audited positioning (13F) > public
fund-manager statements > sell-side research > financial media > social media. A crowded
disclosed position (SA LP's semis puts) is BOTH signal and risk — if the crowd must
unwind, the trade moves against you regardless of who's right. Note crowding explicitly
whenever positioning data informs a recommendation.

**A weight-C number may not drive a decision on its own (added 2026-07-10, Ben-approved).**
A wt-C figure (single unaudited source, self-reported, or a first-pass read of a primary
document) may inform a watchlist row's color but may NOT by itself open/close a door,
set an `engine_says` verdict, or size a position — it must first be checked against a
primary source or upgraded by a second independent read. Six wt-C numbers dissolved on
inspection in four days this week (the Sanhua order rumor, the "2M+ robots" conflation,
the Mega/NVDA robot-count figure, three insider-sale-count overstatements).

## 7. Revenue-durability screen for H5 names (added 2026-07-07, source: Baker Mar-2020 essay)

Baker: "There is no such thing as truly recurring revenue. Some revenue is just more
recurring than other revenue." Apply to every H5 long AND short candidate — score each
software name on which side of each line it falls:

DURABLE (H5 long-survivor traits): system of record (customer cannot operate without it);
enterprise customer base (not SMB); hard-ROI category (security, infrastructure, core
collaboration); low churn / high net revenue retention; high in the customer's stack.
FRAGILE (H5 short-reference traits): SMB-heavy (customers with zero revenue can't pay
anything); seat-based / transactional / workload pricing (revenue reacts instantly to
utilization); discretionary / low in the stack; travel-hospitality-cyclical end markets;
long enterprise sales cycles (new-logo growth stalls first in downturns).

Nuance for AI-disruption analysis (our use, not Baker's): the fragility vectors differ —
Baker's frame is RECESSION sensitivity; H5's is AI SUBSTITUTION. A name can be
recession-fragile but AI-immune (transaction-share models like TOST: revenue follows
customer GMV, not seats) or recession-durable but AI-exposed (per-seat system of record
whose seats AI collapses). Score BOTH axes; only short names fragile on the H5 axis.

## 8. Quarterly kill-first sweep (added 2026-07-07, source: Vanderheiden via Baker)

Vanderheiden began each year asking not "where do I make the most money?" but "roughly
half my positions are wrong — WHICH wrong one costs me the most?" and eliminated it.
Adopt at every quarterly review, before any new-idea work: rank current holdings by
(probability wrong × damage if wrong), write one line each, and propose the kill/trim of
the top item FIRST. Complements §7 exit Darwinism; guards the correlated-factor tail
(power/robotics/AV/space = one factor in a drawdown). Corollary (clocks discipline):
"excessively early is a mistake, not vindication" — being right later doesn't excuse
being sized wrong now.

## 10. Underwriting the long case, the kill case, and the operator's read (added 2026-08-11, upgrade brief §8.2–8.4, Ben-authorized — journal 08-11)

*(Numbered 10, not 9: bare “§9” citations elsewhere in this file — the product-evidence
step 3b — refer to the PLAYBOOK's §9, and this file deliberately leaves 9 unused so
those citations stay unambiguous.)*

Runs at DECISION GRADE: any full analysis, any panel kill/pass, any refusal to honor a
fired pre-registered condition. Triage screen-outs do not owe this (upgrade amendment A2).
The three parts are written by DIFFERENT voices where a panel runs — the analyst who
builds the kill case never writes their own long case (generator ≠ approver).

### 9.1 The strongest investable case (before any rejection is final)

Answer every line, in writing, before a decision-grade NO:
- The credible path to 3x: what has to happen, by when, with what evidence today?
- The credible path to 5x: same discipline — a path, not a hope.
- What does the market underestimate about growth DURATION? (Duration, not next quarter,
  is where long-run mispricing usually lives.)
- What product evidence supports the upside — usage, cohorts, attach rates, pricing power?
- What founder or management capability matters here, shown by past hard calls?
- What adjacent profit pool can this company enter from strength?
- What operating leverage is not yet visible in current margins?
- What financing or dilution does the upside path REQUIRE?
- Which single milestone would justify scaling the position?
- Can a small starter position capture the upside while we learn? (If yes, say what the
  starter teaches and what would scale it — playbook §6.0's uncertainty-sizes-first default.)

### 9.2 The kill case (preserved, sharpened)

Test in order: accounting quality · leverage and refinancing · dilution · customer
concentration · competitive displacement · regulatory risk · capital intensity · contract
quality · execution record · valuation. End with ONE sentence: the single factor most
likely to destroy the long case, and the earliest evidence that would show it happening.

### 9.3 Product, founder and market formation (growth names)

PRODUCT — Is adoption accelerating? What do customers actually use it for? Mission-critical
or discretionary? Retention/replacement cycle? Is pricing power improving? Is usage leading
the reported numbers?
FOUNDER/MANAGEMENT — Is capital allocation rational? Do they make hard strategic
transitions? Does compensation dilute or align? Have they earned credibility on product
and financial promises?
MARKET FORMATION — Is the category expanding? Defining it or following it? Which layer of
the stack captures the economics? Consolidating or fragmenting? What must become true for
the market to be much larger?

### 9.4 The operator's read is structured input, not an afterthought

Ben's product/founder/market judgment enters as a STRUCTURED owner view — his probability
disagreements, his horizon, his falsifier, his review date — recorded beside the house
view before the verdict is adjudicated, never as an informal override after the model is
finished. The house view is never rewritten to match it; the two are graded separately
(upgrade brief §12).

---

## 11. Valuation method — AMENDED 2026-09-02 on Ben's instruction (owner-directed; supersedes the exit-multiple, odds and hurdle practice in §5 and playbook §6.6 for every valuation built from this date)

**Why, in Ben's words (2026-09-02).** On the exit multiple: *"this is terrible, and needs to change ... we can't just randomly assume that investors will always pay less in the future. Companies do grow and improve, and gain in market share ... don't just come up with a random multiple, but actually instantiate it and think about the trajectory of the company."* On the scenario odds: *"That's also bogus. We need to do this on a company by company basis."* On the hurdle: *"I think we're double dipping here. What we should do simply in my view, is come up with the valuation, as per the improved methodology, set a time period, and then compare that against the average return in the market. Ideally it's higher than that, not lower. That needs to be reported."* And the scope: *"let's please not recalculate the 43 valuations, at least not for now. However, let's adopt the valuation methodology changes and make sure any future valuation we calculate uses this approach."*

**What was measured before changing it (2026-09-02, all computed from the book's own files):** 25 of 27 computed maximum prices sat below the market (93%); median headroom −17%; only 6 of 43 live cards stated their exit multiple beside today's; the bear case was weighted at or above the bull case in 35 of 37 cards (median 28% vs 23%); the typical bear case assumed a 45% permanent fall; and the decision grader's early reading showed names declined on price beating their index by 2.0 points on average (33 names, too young to be evidence, direction only). Not a change of view about any company; a change of method.

**Freeze note.** The constitution freeze routes engine improvements to the post-freeze list unless they are a bug or a rule contradiction. This is both: the 29 August rule (print today's multiple beside the exit multiple) was adopted and unenforced in 37 of 43 cards, and the owner has instructed the change directly. Recorded as an owner-directed amendment; the ratifying review confirms or reverses it.

### 11.1 Horizon: state the date, derive the span

Default **3 years** for a growth company, **5 years** for a name held as a compounder; the destination view (§6.6b) stays a separate 10-year document. Every card states the `value_date` and computes `horizon_years` as the span from the pricing date to that date (the 2026-09-01 Reddit card called a 5.33-year span "5.0 years" and overstated every annualised figure). We do not run a discounted-cash-flow model as a second valuation: a DCF's terminal value IS a multiple in another costume and a second number built from the same inputs manufactures false agreement. We take two things from the DCF discipline instead — the year-by-year cash bridge (11.2) and the implied-growth cross-check (11.3).

### 11.2 The bridge, year by year, to the horizon

For each scenario and each year to the horizon: revenue → the company's adjusted profit measure → minus stock pay → minus the payroll taxes on vesting (read the company's own definition of its adjusted measure and put back EVERY named exclusion) → minus depreciation → operating income → minus cash tax at the rate that actually applies that year (tax-loss shields run out on a date; find it) → minus working-capital build → **owner cash earnings**. Interest on cash is never inside the earnings that get multiplied; it accrues to the cash roll-forward, and net cash is added once at the horizon. Stock pay is charged as cash with the share count held flat, OR shares are grown and stock pay is not charged — never both, and buybacks are never also deducted when stock pay is charged. The `cash_bridge` field carries the per-year lines so a reviewer can audit the roll-forward (the Reddit Codex pass could not, and said so).

### 11.3 The exit multiple is DERIVED from the trajectory, never typed

1. **Describe the company at the horizon first:** the revenue growth rate expected in the year AFTER the horizon, the margin, the market-share trend, the reinvestment runway. Write it as one sentence per scenario.
2. **Read the multiple from the ladder** (`data/multiple_ladder.py` → `book/multiple_ladder.md`: a fixed peer set of profitable growth companies, their current multiples computed from raw fields, bucketed by the growth the market expects of them). Take the median for the growth bucket the company will be in after the horizon, then argue it up or down in one sentence (`multiple_rationale`). A company still growing 25% with rising margins gets the 25%-growth multiple, not a fear discount.
3. **Print today's multiple beside it** (`multiple_today`, with its basis named: what is on top, what underneath, which period). Any gap is explained by the trajectory sentence, and a de-rating is allowed only when the growth path itself decays. **Banned: a scenario whose growth after the horizon is 15% or more AND whose exit multiple is below 60% of today's.** Still compounding and the multiple halves is not a scenario, it is a contradiction; the validator rejects it.
4. **The DCF in one line, as a cross-check:** every exit multiple is translated into the perpetual growth it implies at a 10% return (multiple = 1/(r−g) on next-year cash, so g = r − 1/M; a 24x multiple implies 5.8%, a 14x implies 2.9%, a 40x implies 7.5%). Stored as `implied_growth_at_10pct`. A multiple that implies perpetual growth above ~7% needs the trajectory sentence to say why; one that implies growth below inflation for a company described as "still growing 20%" is the contradiction in 3 by another route.
5. **The reverse ladder is mandatory:** the revenue growth rate today's price requires for a market-beating return at 18x, 24x and 30x (`reverse_ladder`). It is the Nomad Costco ladder and it is the most decision-useful line on the card.

### 11.4 Scenario odds: per company, each with a written reason

No house default. Start from the odds the price already implies (§6.6c), then write one sentence per scenario saying why ours differ (`probability_rationale`): the guidance-beat record, cohort or retention data, base rates for the specific question ("how often does a company at this stage keep growing 20%+ for three more years"), the balance sheet's ability to survive the bear. Odds are symmetric unless the evidence says otherwise; a bear weight above the bull weight has to be argued, not assumed. The bear case is a real path for THIS business, sized from its own history and its own balance sheet, not a 45% haircut applied to everything.

### 11.5 Reporting: value → return → comparison, both numbers, every time

The card reports, in this order: the probability-weighted value at the horizon; **the annualised expected return from today's price** (`expected_return_annualised`); **the market comparison** — the passive benchmark return in `config/policy.json` (6.5% a year, set 2026-08-03) — and Ben's absolute-return objective for the company's type (12% a year; 10% for a true compounder held 5+ years; 15% for unprofitable or pre-scale). Both comparisons are printed beside the return; neither is hidden inside a derived price. The "most we may pay" (`data/buy_cap.py`) is the same arithmetic in price form (the price at which the return equals the benchmark) and stays as the order-guard object, but it never replaces the return line in anything Ben reads. What the old practice stacked before this comparison — tilted odds, catastrophic bear values, de-rated multiples — is what 11.3 and 11.4 remove; the comparison itself is a hurdle, not a second risk charge, and is applied once.

### 11.6 Scope and enforcement

Applies to every card whose `as_of` is 2026-09-02 or later. **Existing cards are grandfathered as they stand** — not recalculated (Ben) — and each is rebuilt under this method the next time it is used for a buy decision or a size change, never silently. `data/valuation_validate.py` rejects a new live card that lacks any of: `value_date`, `multiple_today` with `multiple_basis`, per-scenario `exit_multiple` + `growth_after_horizon` + `multiple_rationale` + `probability_rationale`, `implied_growth_at_10pct`, `expected_return_annualised`, `market_comparison`, `cash_bridge`, `reverse_ladder` — and rejects the banned combination in 11.3(3). The Fable-then-Codex second pass and the decision panel are unchanged: the method is what they check, and the Reddit panel is the record of why they are needed.
