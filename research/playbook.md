# The Bottleneck Playbook — Behavioral & Structural Operating Rules
### Aschenbrenner-derived methodology, codified for the ai-thesis skill

Version 1.5 · 2026-08-04 (§6.7 amended at review #2 — enforcement + the declined-names clause)
Version 1.5.2 · 2026-08-11 (§6.0 LAYER 2 gains the uncertainty-sizes-first default and the
six enumerated refusal grounds — upgrade brief §8.5, Ben-authorized outside cycle, journal
08-11; §6.6d cap-hierarchy language same date)
Version 1.5.1 · 2026-08-11 (gate-language reconciliation across §0/§2.1/§3/§6/§7.1/§12.3:
no rule changed — the 08-01 three-layer decision test is now stated consistently everywhere
it is referenced. Authorized outside the review cycle by the research-analyst upgrade brief
§4.3; governance record in book/journal.md 2026-08-11. The instruction-layer scan in
data/engine_audit.py now guards this class of drift.)

Source basis: forensic reconstruction of Situational Awareness LP's six 13F filings
(Q4 2024 → Q1 2026, SEC CIK 2045724), parsed from raw EDGAR XML — plus (v1.2) a
cross-reference of 26 quarters of Atreides Management (Baker) 13Fs onto this same
framework. Every rule below carries its **why** and, where applicable, a **precedent tag**
(P-xx, defined in §11) so analyses can cite evidence, not vibes. This file encodes
*behavior and structure*; the market *views* live in `references/thesis.md` (H1–H5) and
must not be duplicated here.

**v1.2 fusion note (Atreides cross-reference).** Baker ran the *identical* migration engine
(§2) independently on the compute chain — AMD (Trade 1, own the queue) → Astera Labs
(Trade 2, the interconnect bypass) → optics (Ciena/Coherent/Lumentum) → storage/memory
(Pure Storage/Micron) — with zero contact with Leo's power-chain book. Two independent
discoveries of the same mechanic from opposite worldviews (expectations-mispricing
generalist vs AGI-timeline researcher) is strong evidence §2 is a repeatedly-observed capital-cycle heuristic (v1.4: "general
law" retired — two managers and one week of instances support a strong prior, not a
law), not a power-buildout quirk (reinforces FP-5). Added: precedents P-14–P-20
(§11); the pricing-power kill (§7.2); filings-lead-words (§10); the index-vs-single-name
put question (§9, H-7). **Import the mechanic — NOT Atreides' breadth (40–58 names),
turnover (3-qtr median hold), or calls-on-everything; those would dilute a concentrated
book and violate anti-pattern #8 (clock-blending) and §8's selective-convexity rule.**

**v1.3 amendments (2026-07-12, review #1, Ben sign-off).** Four changes, each with a
ledger trail: (1) §6.1 gains step 0 — the Thermometer runs as a cheap PRE-filter before
any deep analysis, and every screen reports its ENTER/TRIGGER/KILL split (the zero-kill
fix: 108 watchlist rows had produced 0 kills because crowdedness was checked LAST);
(2) §6.1-6 the devil's advocate is written by independent refuters empowered to KILL,
and §7.2 gains the new-fact exit rule (both already operative in SKILL.md/frameworks —
the playbook now agrees); (3) §2.2 gains the marginal-buyer funding-window detector
ahead of book-to-bill (P-26); (4) §11 gains the fiber-bust precedent set P-21..P-27
(notes/2026-07-07-dotcom-fiber-precedents.md, ratified).

**v1.4 amendments (2026-07-13, review #1.5 — the reply's + external merits assessment's
signed queue).** (1) §3 Thermometer output becomes a LABEL (LOW/MODERATE/HIGH/EXTREME);
the numeric score survives ONLY as the internal step-0 pre-filter input — no verdict,
door, or size may cite a bare number as evidence; (2) §4.1 "never fresh longs" DELETED —
first-order names may be longs with a quantified expectations gap + durability pass
(H3 made reversible); (3) §6.1 check 5 now requires the gap QUANTIFIED; (4) new §6.5
door-board governor; (5) §7.2 backstop-breach exception to the new-fact rule; (6) §2.3
coverage tiers (15 active / 25 queue / archive); (7) "general law" framing retired —
the migration mechanic is a repeatedly-observed capital-cycle heuristic, not a law.
Scope note: the prime directive below binds the RISKY sleeve (the edge engine); the
MODERATE sleeve runs the quality mandate in risk-rules.md (consensus allowed, its own
written test — added same date).

**Prime directive (AMENDED 2026-08-01, Ben sign-off — this paragraph reconciled
2026-08-11 per the upgrade brief; SKILL.md's twin was amended on 08-01 and this one was
missed): prefer pre-consensus entry, and make crowding a price of admission, never a
veto.** Every risky-sleeve entry runs the §3 Consensus Thermometer and the §6.0
three-layer decision test; a crowded name enters smaller, with a higher evidence bar and
the check-8 cadence guard — it is not blocked for crowding alone. A great thesis at a
consensus price is usually a donation to whoever entered pre-consensus; the answer is the
size discount and the "what do we know that the crowd does not" line, not a ban. (The
moderate sleeve's quality mandate stays its own separately-tested lane: risk-rules.md,
2026-07-13.)

**Status:** decision support. Ben decides. Risk limits in `references/risk-rules.md`
override anything here. All numeric defaults marked ⚙️ are tunable; risk-rules wins on
conflict.

---

## 0. Wiring instructions (one-time integration — HISTORICAL, July 2026. Where any line
below conflicts with the §6.0 three-layer decision test of 2026-08-01, §6.0 wins.)

1. Save this file as `references/playbook.md`.
2. In `SKILL.md`, add to Mode 1 (news triage): "Also classify the item against
   `references/playbook.md` §2 (lifecycle stage) and §5 (noise vs migration)."
3. Add to Mode 2 (company analysis): "Run the §3 Consensus Thermometer, §4 layer test,
   and §6 entry gate before any sizing; select instruments per §8."
4. Add to Mode 3 (portfolio review): "Run the §2 phase-map refresh, §7 exit/kill sweep,
   and §9 hedge-dial review; diff influence-fund 13Fs per §10."
5. Add to Mode 5 (thesis maintenance): "Behavioral-rule violations are journaled like
   thesis changes."
6. Create `state/phase-map.md` from the template in §12 on first run.
7. Extend `state/journal.md` entries with the fields in §12 (consensus score at entry,
   lifecycle stage, layer, clock, instrument rationale, kill condition).

---

## 1. First principles (the WHY layer under every rule)

These are the load-bearing beliefs. If one breaks, the rules downstream of it break too —
flag it, don't keep executing.

- **FP-1 · Physical bottlenecks, not ideas, gate the AI buildout.** Compute is congealed
  electricity; scaling laws are secretly megawatt laws. Whatever input takes years to add
  (power, interconnection, transformers, land, labor, water) is where scarcity premia —
  and returns — concentrate. (Feeds H2.)
- **FP-2 · Capex is a cost, not a moat.** First-order names (chips, clouds) get bid as if
  spending confers advantage; the returns on that spending accrue to the layers that
  *supply* the scarce inputs. This is the engine of the first-order/second-order divide
  (§4).
- **FP-3 · Bottlenecks migrate.** Solving one constraint exposes the next. Alpha = owning
  the *next* constraint before the market names it, and leaving the solved one while the
  story is loudest. (This is H2's claim; §2 operationalizes it.)
- **FP-4 · The market prices stories late and all at once.** Re-ratings are step
  functions (Baker lens: expectations, not outcomes). Therefore: entries belong in the
  disgust phase, exits in the euphoria phase, and the middle is for sizing up on
  validation.
- **FP-5 · A thesis is not a ticker.** The same view should rotate instruments as the
  bottleneck moves (IPPs → onsite power → energized land). Marrying tickers loses the
  thesis; repeating the thesis without updating instruments loses the returns. (P-04)
- **FP-6 · Discontinuity is the base case.** In an AGI-timeline worldview, outcomes are
  fat-tailed in both directions. Prefer payoff shapes that are paid for extremity
  (convexity, §8) and processes that survive being early.
- **FP-7 · Timing is a separate skill from direction — run them on separate clocks.**
  Structural views (quarters–years) and tactical positioning (weeks–quarters) must be
  bookkept, sized, and judged separately (§9). Blending them is how hedges become
  identity and losses become "conviction."
- **FP-8 · Sequence creates the return; snapshots hide it.** Long-first-unhedged, then
  short-after-the-stretch earns; the same end-state entered in the wrong order bleeds.
  Every recommendation must state its intended *sequence*, not just its end-state.

---

## 2. The Bottleneck Migration Engine (Trade 1 / Trade 2, generalized)

The core pattern, abstracted from the power trade:

> A constraint appears → **Trade 1: own what the queue protects** (incumbents holding
> the scarce asset re-rate; the queue is their moat) → the buyer's problem becomes
> *time*, not price → **Trade 2: own what sells the way around the queue** (the bypass:
> speed itself becomes the product) → the bypass scales, the constraint clears, scarcity
> moves to the next input → repeat.

Crypto-native mnemonic: L1 congestion → own blockspace (Trade 1) → own the rollup stack
(Trade 2) → value migrates again.

### 2.1 Lifecycle stages (state machine — every watchlist name gets a stage)

| Stage | Definition | Correct action |
|---|---|---|
| **S0 · Latent** | Constraint identifiable from physics/lead-times, market hasn't named it | Research; build the instrument list; recon entries allowed |
| **S1 · Recognition** | First deals/backlogs/queue data confirm; specialist coverage only | Primary entry window. Probe → add on validation |
| **S2 · Re-rating** | Multiple expansion underway; generalist money arriving | Hold; average UP on validation events; a new initiation runs the §6.0 three-layer test — crowding sizes it, never permits it (2026-08-01) |
| **S3 · Consensus** | "Default vehicle" status; viral posts; price above mean target; the story explains the market | Trims enter mandatory review. **A new entry runs the §6.0 three-layer test (2026-08-01; the 07-29 three-condition rule and its crowding ≤6 bar are deleted with the rest of the score-keyed gates). The presumption stays against a consensus-stage entry; rebutting it takes a durability screen, a quantified expectations gap, and a smaller size — argued in the analysis, not gated by a score** |
| **S4 · Migration** | The constraint visibly clearing (lead times normalizing, queues shortening) OR premium relocating to next layer | Exit remainder; redeploy to the next constraint's S0/S1 |

### 2.2 Stage-transition detectors (check at every review; log stage changes)

- S0→S1: first anchor contracts/PPAs/backlog disclosures; lead-time data published.
- S1→S2: sell-side initiations cluster; multiple expands faster than estimates.
- S2→S3: price > mean analyst target; index/ETF inclusion effects; mainstream/viral
  coverage; "picks and shovels" listicles include the name; IV elevated.
- S3→S4 — **earliest tell first (v1.3, P-26): the marginal buyer's funding window
  closes.** High-yield/private-credit access for the layer's CUSTOMERS shuts or reprices
  while backlogs still look record — in the fiber bust this led the book-to-bill roll by
  1–3 quarters (CLEC funding shut spring 2000; orders rolled Q4'00). Then the lagging
  confirmations: order book-to-bill rolls over while story still loud; lead times/queues
  shorten; bypass capacity scaling visibly; incumbents guide "normalization."

### 2.3 Phase map (live state) + coverage tiers (v1.4)

Maintain `state/phase-map.md`: current constraint chain, each layer's stage, candidate
next constraints with monitoring indicators (align with H2's indicator list), and dated
stage-change log. Refresh every review; a stage change is journal-worthy.

**Coverage tiers (v1.4 — attention is the binding constraint; one operator cannot give
108 rows live fundamental coverage):** **ACTIVE ≤21 names ⚙️ — SET 2026-08-03 on Ben's
sign-off, and it is now the ONLY cap for this shelf.** History: 15 → 16 on 2026-07-15
(Ben-directed, resolving a fired-wake-promotion versus cap contradiction), then a SECOND and
different cap of "10–15" appeared in §6.7 on 2026-08-01 without the first being retired — so
for three days the rulebook stated two caps for one shelf while the shelf actually held 21,
which meant neither number bound anything. Ben chose 21 and gave the reason: he has not yet
read every name, and forcing names off a list before they have been judged is worse than a
list that is honestly too long. **The cap now BINDS: adding a name to ACTIVE requires moving
another one off it, in the same edit.** A cap nobody enforces is not a cap, it is a wish —
that was the actual defect here, not the number. (live triggers, current
valuation, active thesis work — the trigger board draws only from here) · RESEARCH
QUEUE ≤25 ⚙️ (periodic research, no automatic capital deployment) · ARCHIVE (unlimited;
no live triggers; reactivates only on a defined event) · plus a small MONITOR tag for
instrumentation rows (canaries and tripwire topics — gauges, not candidates; they don't
consume coverage slots and can never receive entry doors). Every watchlist row carries
a tier; tier changes are journaled.
**Wake-up cadence (2026-07-13, Ben-directed; upgraded monthly → WEEKLY same day):**
shelved names are checked, not forgotten. Three layers: (1) DAILY — QUEUE rows with
clean price levels carry WAKE rows in triggers.csv, watched by the automated sweep;
(2) WEEKLY, every Monday — `data/wake_check.py` runs inside the 08:00 deploy chain and
scans ALL public QUEUE + ARCHIVE names for wake behavior (±15% weekly moves, 200-day
reclaims, new 52-week lows = §6.2 disgust watches, new 52-week highs = wake-spec
re-checks, plus QUEUE earnings within 8 days) → `book/wake_report.md`; the Monday
session reads the report and does the event/news layer for topics and private names;
(3) EVERY /review — full pass over all shelved rows. Any /news or /tradescan hit on a
shelved name triggers an automatic wake-check of that row regardless of day. A fired
wake-up PROMOTES the row one tier for a fresh look through the normal gates — it never
buys, and it never skips the re-gate.

### 2.4 Next-bottleneck hypothesis procedure (the phase-3 scouting loop)

The prime directive forbids buying the current bottleneck at consensus — so the engine's
fuel is a steady supply of S0 candidates. Generate them from four sources, every review:

1. **Physics chain:** ask "what input does the *current bypass* consume and who supplies
   it with multi-year lead times?" (Onsite power consumes gas connections, gensets,
   transformers, permits, land, skilled labor, water — each is a candidate layer.)
2. **Reservation behavior in the wild:** earnings-call and procurement language showing
   prepayment/take-or-pay/multi-year reservations for an input nobody's equity expresses
   yet — the §4.2-#2 signal appearing *before* a pure-play exists.
3. **Lead-time and queue datasets:** transformer/turbine lead times, interconnection and
   permitting queue statistics, EPC labor and vocational wage data, water rights pricing.
4. **Influence-fund recon lines (§10):** their new sub-1% positions are *their* S0
   hypotheses, disclosed 45 days late but still early in absolute terms.

Each candidate gets an S0 card in the phase map: the claim, the first S0→S1 detector to
watch, one falsifier, and (if investable) the purest instrument list. A candidate with no
detector defined is a narrative, not a hypothesis — don't card it.

**Why this section exists:** the fund's entire return sequence — IPPs (Trade 1, entered
S2, exited S3) → onsite power/energized land (Trade 2, entered S0–S1) — is this machine
run once. (P-04, P-05, P-06)

**Independent confirmation (v1.2):** Atreides ran the *same* engine on the compute chain —
AMD → Astera Labs → optics → memory (P-14, P-15, P-16) — with no contact with Leo's book.
The engine is not Leo-specific; treat §2 as a strong, repeatedly-confirmed heuristic of
capex supercycles (v1.4: not a "law" — it must keep earning its keep per-cycle). The
discipline that travels is the *mechanic* (own the queue, rotate to the bypass, trim to
consensus), NOT Atreides' breadth/turnover (§3 of the fusion notes; see header).

---

## 3. The Consensus Thermometer (the prime-directive instrument)

Score 0–10, one point per indicator that is TRUE. Measure, don't feel. Cite evidence for
each point in the analysis output.

| # | Indicator (1 pt each) | How Claude Code measures it |
|---|---|---|
| 1 | Price above mean sell-side target | fetch_market_data + latest targets via search |
| 2 | ≥3 major-bank initiations/upgrades in last 2 quarters | search |
| 3 | Multiple re-rated (fwd P/E or P/S > 2× its own 3y median) | fetch_market_data + history |
| 4 | Featured in viral/mainstream content (LinkedIn slop, YouTube, top podcasts) in last 90 days | search; **if the idea's origin is such content → automatic point + note** |
| 5 | 13F-tracker celebrity: highlighted as a "guru" holding | search trackers |
| 6 | Retail flow signals: options volume/IV elevated vs 1y norm; meme-ticker status | data/search |
| 7 | Index/ETF inclusion or weight-driven flows in last 2 quarters | search |
| 8 | The theme (not just the name) is the *default explanation* in financial media | judgment, cite examples |
| 9 | Insiders/anchor holders distributing into strength | filings/search |
| 10 | The stage-2→3 detectors (§2.2) fire | phase map |

**Output convention (v1.4): the Thermometer REPORTS a label, not a number.** LOW (0–3) ·
MODERATE (4–5) · HIGH (6–7) · EXTREME (8–10). The numeric score is computed internally
(it feeds LAYER 3 sizing under §6.0; the step-0 pre-filter and the score-keyed gates it
once drove are deleted, 2026-08-01) but every human-facing output —
verdicts, watchlist rows, journal entries — states the LABEL plus the indicators that
fired, never a bare number as if it were a measurement. Ten judgmental inputs summed do
not make a precision instrument; the conclusion and the evidence matter, the decimal
does not.

**Gates — DELETED 2026-08-01.** A crowding score no longer permits, burdens or forbids a
purchase; §6.0 LAYER 1 is the only absolute block and the money test is the only economic
one. Two uses survive and are unchanged: a heavily-crowded name already HELD enters a
trim-review, and crowding sizes a new position at LAYER 3. The old bands — buy freely below
one score, three written conditions in a middle band, blocked above another, a tighter bar
for adding than for starting — are gone. They gave two different answers in three places
for most of July.

- **Origin test (REWRITTEN 2026-07-29, Ben-approved — the penalty moves from the SOURCE to
  the SPEED).** If an idea arrived via X, a podcast, a newsletter, a tracker or a headline:
  1. **It is never blocked from research on account of its origin.** Ben, 2026-07-29:
     *"X and podcasts and news and anything in the news cycle, as long as it's signal
     rather than noise, is interesting for research purposes and should never be blocked
     from entering our research pipeline… X is a representation of the wisdom of the
     masses, and sometimes the wisdom of the masses can be right."*
  2. **The origin is DISCLOSED at the top of the analysis** — where it came from, when, and
     who said it. Unchanged.
  3. **Indicator 4 fires on the evidence, not on the origin.** Viral or mainstream coverage
     in the last 90 days scores its point when it is TRUE. What is RETIRED is the automatic
     floor of 5 applied for the discovery channel alone, which was a rule about where Ben
     looks rather than about what is true. (Both the floor and the score-keyed buying bars
     that made it bite are deleted as of 2026-08-01 — crowding now only sizes a position.)
  4. **THE HARD RULE, and it is where the real risk lives: NO SAME-DAY ACTION.** An idea
     from the news cycle cannot be bought on the day it surfaces, ever. It goes through the
     full analysis first and enters at a review or a pre-defined catalyst under the §6.1
     check 8 cadence guard. Ben, same date: *"making fast and quick decisions on the basis
     of news and X and trading on clickbait is really, really bad and should under all
     circumstances be avoided. I guess that's maybe the most important point I'd mention."*
  5. **One extra written line for news-sourced ideas: what do we know that the person who
     posted this does not?** A source, a document, a computation, or a piece of judgement.
     If there is no answer, we are buying their exit — say so and stop.
  Record on both sides: the meta-precedent stands (this playbook exists because a LinkedIn
  post about the fund went viral, so the disclosed book was already at consensus when
  studied — P-12), and so does the engine's scorecard on news-sourced ideas: the All-In
  podcast copper idea was killed 3–0 and the tracker-sourced warehouse-automation name was
  killed 3–0. The full analysis is what caught both. That is the protection — not refusing
  to look.
- Thermometer applies **per name AND per layer**: a pre-consensus name in a consensus
  layer inherits the layer's crowding risk (note it explicitly).
- **Scope guard: a high score is NOT a short signal.** The Thermometer sizes entries
  (LAYER 3, since 2026-08-01) and triggers trims on names already held — nothing more.
  Consensus names can keep re-rating for quarters (the IPPs did,
  post-exit). Fading a crowded name additionally requires §9's overextension evidence and
  runs on the tactical clock — crowding tells you *not to buy*; it never alone tells you
  to short.

**Why:** the fund's realized winners were entered at maximum disgust (S0–S1) and
distributed into S3. Its copiers, buying disclosed positions at 2× the marks, structurally
occupy the other side of that trade. The Thermometer is the mechanical guarantee Ben is
on the correct side.

---

## 4. Layer analysis: first-order / second-order / profit-pool test

Before any long, classify the layer and locate the profit pool. Being right about the
theme in the wrong layer returns ~0 (P-08: EQT — "gas powers AI" was TRUE; upstream
commodity producers captured none of it; four restructurings, a year, ~flat).

**4.1 Order classification.** First-order = the obvious, headline beneficiary the crowd
reaches for (chips, megacap cloud). Second-order = the input suppliers and bypass sellers
the buildout *requires* (power, memory, optics, energized land, equipment, labor).
First-order names are where FP-2 bites (capex priced as moat) — they are short/hedge
candidates at S3, and (v1.4, H3 made reversible) they MAY be fresh longs only when the
expectations audit shows a QUANTIFIED gap and the durability screen passes: own the
cheapest durable profit pool, whichever order it is. The presumption stays against
first-order longs; the audit can rebut it.

**4.2 Profit-pool location test (all five must be argued, not asserted):**
1. **Pricing power at the scarcity point** — can this layer *charge* the premium, or does
   it *pay* it? (Commodity producers pay; queue-bypass sellers charge.)
2. **Reservation behavior** — are customers prepaying / signing take-or-pay / reserving
   capacity years out? (Strongest single signal a layer holds the bottleneck.)
3. **Backlog vs spot** — multi-year contracted backlog beats spot exposure.
4. **Substitute distance** — how quickly can buyers route around THIS layer? (The bypass
   you own today is someone's queue tomorrow.)
5. **Who competes for the asset** — multiple desperate, time-constrained buyers (hyper-
   scalers vs one) = premium durability.

**4.3 Asset-reclassification screen (highest-alpha entry class).** Look for companies the
market files under a dying category whose *assets* belong to the scarce layer:
ex-bankrupt miners = energized land with substations (P-05); spinoffs = pure-play on the
scarce input hiding in a conglomerate's multiple (P-09: SNDK). Test: "What is the
replacement cost / strategic value of the physical assets if re-labeled to the bottleneck
category, vs EV today?" The edge is *classification*, not information.

---

## 5. Noise vs migration (the shock-response algorithm)

On any adverse shock to a held thesis, answer three questions **in writing** before
acting:

1. Does the shock change total demand for the bottleneck resource? (Efficiency scares
   usually don't — gains get reinvested into scale; Jevons. DeepSeek test, P-03.)
2. Does it change *which asset is scarce*? (The interconnection-queue insight did —
   that's migration, P-04.)
3. Does it change *who captures the premium*? (Layer shift.)

- **No / No / No → NOISE.** Action: hold; if Thermometer ≤3 and price broke, this is a
  §6.2 disgust entry/add window. (The fund *added generators through DeepSeek*.)
- **Yes on 2 or 3 → MIGRATION.** Action: rotate instruments within the thesis (exit the
  old layer even at a loss/flat; enter the new layer at its S0–S1). Do NOT average down
  in the old layer.
- **Yes on 1 → THESIS FALSIFIER territory.** Route to H1/H2 falsification review; the
  playbook does not override thesis kills.

Journal the three answers verbatim. This test is the single best defense against both
panic-selling noise and loyalty-holding through migration.

---

## 6. Entry playbook

### 6.0 THE DECISION TEST — three layers, not one AND-chain (ADDED 2026-08-01, Ben sign-off; supersedes §6.1's "ALL must pass" framing)

**Why this replaces the eight-check AND-chain.** Measured 2026-08-01 across the engine's
whole record: 156 watchlist rows produced 14 affirmative verdicts, **7 of which carry
explicit override language** — so the engine unaided said buy roughly 3 times in 156.
Outright declines were only 14%; **63% of the book sat in a waiting state** attached to a
price condition needing a median **17.6% fall**, with no expiry and no grading. Of 141
written conditions only 17 have ever fired, and **none of the 51 multi-part conditions has
ever passed**. The reasons given for declining ran **3.1 : 1** in favour of "the price or the
crowd" over "the business is not good." An eight-way AND-chain of subtractive checks cannot
produce a buy; it can only withhold permission. Ben, 2026-08-01: *"the question is, are we
saying no for the right or the wrong reasons though?"* and *"if we just sit still and don't
invest at all, that's just inertia."*

**The three layers. Every candidate passes through all three, in order.**

**LAYER 1 — ELIGIBILITY. The only absolute vetoes.** Ratified by Ben 2026-07-24 and now
binding on the entry test, not just on reviewers: fraud · illegality · cannot be traded in
this account · a hard risk limit in risk-rules.md already breached · a load-bearing fact
simply wrong. **Nothing else blocks.** Valuation, crowding, story-maturity and timing
objections argue and may shrink size; they never veto. A name that is merely *not yet
listed* is NOT an eligibility failure — it goes to the pre-IPO watch list with the listing
itself as its event (10 of the 16 recorded "cannot trade" declines were private companies
mis-filed here).

**LAYER 2 — THE MONEY TEST. Blocks the RECOMMENDATION on economics, never the ORDER
TOOL, and never popularity.** Corrected 2026-08-04 after `data/ibkr_order.py`'s BUYCAP
check silently enforced this layer as a hard stop on order SUBMISSION for three days —
Ben: *"it's not allowed to block, I hope you know that now."* What this layer blocks is
the ANALYSIS saying buy; it is not authority for a script to refuse an order Ben has
decided on. `ibkr_order.py` now shows the gap loudly and does not abort on it — see that
file's BUYCAP comment. Does the
probability-weighted expected return, after the 26% tax, beat simply holding the index
over the horizon the thesis itself claims? **Below the index → no position.** This is the
one veto that survives, and it is where the financial work and the company-prospects work
BOTH FEED THE SAME DECISION rather than sitting in separate steps: the near valuation
(§6.6a) and the destination valuation (§6.6b) answer the same question — what is this worth —
over two different horizons. **They are read side by side and NEVER arithmetically combined**
(§6.6b condition 1 shows why: merging them let a 2% assumed probability turn a marginal hold
into a buy). Two numbers, both shown, exactly like the two labs. Ben's definition of the
valuation gap, given 2026-08-01: *the amount by which our probability-weighted return, after
tax, beats just buying the index.* A tiny bad bet is still a bad bet.

**AMENDED 2026-08-04, Ben's sign-off — two changes, both narrowing what a single typed
number is allowed to do.**

**(a) ONE PROBABILITY MAY NOT VETO. Test the range, and let "we do not know" be an
answer.** The scenario probabilities on every card are hand-authored judgements. Until now
one of them could refuse a purchase outright. From now the test is run three times — the
downside case weighted at 20%, at 30% and at 40%, holding every scenario VALUE unchanged —
and the outcome is read like this:

| What the three runs show | The answer |
|---|---|
| Fails at every weighting | A real NO. The veto stands. |
| Passes at every weighting | A real YES, on economics. |
| **Flips somewhere in between** | **INDETERMINATE — not a failure.** Take a smaller position and write the dated, checkable thing that would settle it. |

**ADDED 2026-08-11 (upgrade brief §8.5, Ben-authorized outside cycle — journal 08-11):
uncertainty is a SIZING input before it is ever a refusal.** The default answer to
"positive expected value with an unresolved question" is a smaller starter position plus a
dated scaling condition — never "open question, therefore wait." A refusal is reserved for
exactly six grounds: (1) expected return inadequate even under the best evidence-based
probabilities; (2) unacceptable risk of permanent loss; (3) the line cannot be traded in
this account; (4) a capital structure that makes survival doubtful; (5) a load-bearing fact
that cannot be established; (6) a price that already requires the optimistic case to be
true. An ANSWERABLE open question shrinks size and sets its dated condition; only an
UNANSWERABLE one is a reason to stand aside (Ben's 07-24 reviewer rule, now written into
the entry test itself).

The third row is the whole point: it is an outcome the engine could not previously express,
so an unresolved question and a proven failure produced the same output, which is a refusal.
This is also already Ben's ratified rule for open-but-answerable questions (2026-07-24, rule
2 of the three that replaced vote-counting) — it was simply never wired into the money test.
**Report which of the three runs were tested and what each returned; never state a pass or a
fail without them.** Worked precedent: CACI on 2026-08-03 failed at every weighting, so its
NO was real — and it failed for a reason no probability captured (the interest on debt that
bought its growth), which is the standing reminder that this test governs confidence in the
probabilities, never confidence in the inputs.

**(b) THE COMPARISON DEPENDS ON THE DECISION. Two different questions, two benchmarks.**
Measured 2026-08-03: the index used as the hurdle is now roughly 40% a single AI-linked
theme — substantially the same bet this book makes. So the hurdle FALLS exactly when our
thesis is wrong, and the rule flatters the portfolio at the precise moment it should be
hardest on it.

- **Buying, adding, or ranking a candidate → compare to the equity index.** It is a genuine
  alternative use of the money and stays as written above.
- **Deciding whether to REDUCE or stand aside → compare to short-dated government paper**
  (the safe sleeve), not to the index. Worked example: our holdings fall 40% and the index
  falls 35%. Against the index the position still "wins" and the engine says hold. Against
  cash-equivalent paper it plainly does not, which is the honest question in a general fall —
  not *did we beat the index*, but *should this money have been at risk at all*.

Both benchmarks are stated whenever the two would give different answers, and the reason for
choosing one is named. Not adopted: blending them into a single number, which would recreate
the averaging error §6.6a exists to prevent.

**LAYER 3 — RANKING. What does this displace?** Every candidate competes against cash,
against the index, against the weakest position already held, and against the extra
single-factor risk it adds. Crowding (§3) and influence-fund positioning (§10) live HERE, as
size modifiers and information — never as blocks. Every buy states its probability-weighted
after-tax return, its permanent-loss case, and **exactly what funds it**. A ranking need not
be a fake decimal score, but "reports only" is abdication: the engine must say why A gets the
money and B does not.

**What §6.1's eight checks become.** They are not deleted — they are re-homed. Check 0
(research pre-filter) and checks 1–2 (crowding, stage) move to LAYER 3 as size inputs and
lose their blocking power. Checks 3 (layer/profit pool), 5 (expectations gap) and 7 (sizing,
kill condition) serve LAYER 2. Check 6 (independent refuters) and check 8 (no same-day news
action) survive unchanged and bind everywhere. Check 4 (hypothesis link) is informational.

**The standing danger of this amendment, recorded at adoption.** Loosening the entry test
raises junk risk, and the protection removed is exactly the one that kept this book out of
expensive popular names. The replacement protection is economic rather than sociological,
which suits a growth investor, but it only works if LAYER 2 is genuinely capable of returning
NO. The 2026-08-01 worked examples are the proof it can: at $123.06 Palantir and at $190.41
Nebius both FAILED layer 2 while passing layer 1 — declined on arithmetic rather than on
popularity. If a quarter passes in which layer 2 never once returns NO, this amendment has
failed and the response is to tighten it, not to argue about it.

**Every decline and every parked name is now GRADED, automatically.**
`data/decision_grader.py` runs weekly inside the deploy chain, prices every declined and
parked name against the index from its decision date, and reports the score **by stated
reason** to `book/decision_grades.md`. This exists because the counterfactual grading the
rulebook has always demanded had run exactly once, on three names. Until a reason-bucket
holds at least eight calls aged 90+ days the report refuses to draw a conclusion from it.

**And what this does NOT yet do, stated plainly:** the grader's own floors — eight calls, a
three-point spread — were chosen by hand on 2026-08-01, not derived from the record, because
the record is 25 days old and holds nothing scoreable yet. They are placeholders to be
replaced by measured values once calls resolve, and the report says so rather than implying
evidence it does not have.

---

**6.1 Entry checklist (re-homed by §6.0 — checks 6 and 8 still bind absolutely; the rest
now inform LAYER 2 and LAYER 3 rather than each holding a veto). Print it in every Mode-2 output:**
0. **Crowding pre-screen — DELETED 2026-08-01.** It used to stop a name being
   analysed at all when the crowd was heavy. §6.0 replaced it: crowding is measured,
   reported, and used to size a position. It never blocks research and never blocks a
   purchase. What survives is one reporting duty — every screen still states how its names
   split across buy, buy-on-a-condition, watch and declined, because a screen that declines
   nothing is broken.

1. **Crowding — SCORED, NEVER A BLOCK (rewritten 2026-08-01, replacing the 4-6 band and
   the ≥7 block).** Measure it with evidence cited per indicator and report the label. It
   feeds position size at LAYER 3 and nothing else. The bands that used to permit, burden
   and forbid a purchase at different scores are deleted. Why: measured across the engine's
   record, declines ran 3.1 to 1 in favour of price and crowd over business quality, and of
   97 scored names the old bar was blocking 8. **The honest counterweight, recorded because
   it argues against this change:** on the first corrected reading of the decision grader,
   names declined on crowding went on to LAG their own index by about 4 points — four names,
   far too few to mean anything, and reported anyway. If that holds as the sample grows,
   this rule is wrong and gets tightened.
2. **Lifecycle stage — SCORED, NEVER A BLOCK (rewritten 2026-08-01).** Record which stage
   the story has reached, because it tells you who the marginal buyer is. It does not permit
   or forbid a purchase. The three written conditions that used to rebut a presumption
   against a well-known name are deleted along with the presumption. Only §6.0 LAYER 1 blocks.
3. Layer test passed: second-order, profit pool located here (§4.2).
4. Maps to a live hypothesis (H1–H5) with stated conviction ≥ its floor.
5. "What's priced in" line (skill guardrail) shows a QUANTIFIED expectations gap
   (v1.4: state what growth/margin/duration the price implies, what we believe, and
   the numeric distance between them — "cheap vs story" is not a gap), not just story.
   **DURATION is a SUFFICIENT source of that gap (added 2026-07-29, Ben sign-off).** A
   complete duration case states: the market prices N years of this growth rate at this
   margin; we believe M years; here is the evidence for M; here is what would make us
   wrong. It does NOT additionally need a multiple that looks low — a duration gap and a
   multiple gap are alternative sources of the same required number and either alone
   qualifies. Duration was already named in this check's own text and had never once been
   the source of a buy case in the engine's record; that is the hole this closes.
   **Holding-period spec (Ben verbatim 2026-07-29): "the goal is long term: at least 1-3
   years, however, in some cases up to 10 or more, the ultimate holding period is
   determined by market factors and business durability (which is all measurable prior to
   (to a degree) and during the holding period)."** Binding consequences:
   (a) The base assumption on a duration entry is a **1–3 year minimum hold**. An entry
       whose case has to be right inside 12 months is not a duration case, it is a trade —
       label it as one and do not claim this path.
   (b) The holding period is an **OUTPUT of measured durability, never a calendar figure
       fixed at entry**. Name at entry the 2–3 durability measures that get re-read during
       the hold — pricing power, share, unit economics, reinvestment runway, ease of
       competitive entry — each with its reading on the entry date.
   (c) **The frameworks §5 REVERSION DATE still applies, but on a duration entry it fires a
       DURABILITY RE-READ rather than an automatic return to the benchmark.** The named
       measures from (b) are re-read and written down: holding up → the position continues
       and the next re-read is dated; deteriorating → the capital returns to the benchmark.
       Same date, two outcomes, the evidence decides — the same shape as the two-key
       advantage test in risk-rules.md, and it carries the identical danger: **the re-read
       must be capable of failing.** An un-failable durability re-read converts a ten-year
       thesis into a permanent excuse, which is the documented mechanism by which growth
       investors become bagholders.
6. Devil's advocate written by 2–3 INDEPENDENT refuters empowered to KILL — never by
   the pitching analyst; distinct lenses (claim false / wrong layer / already priced);
   majority KILL = no door, no row (v1.3; operative in SKILL.md since 07-09) + pre-mortem.
7. Sized per §6.4 ladder and risk-rules.md; kill condition (§7.2) pre-written.
8. Cadence guard respected: entries execute at review/catalyst, never same-day-news.

**6.2 Preferred entry conditions (any one is a green flag, not a requirement):**
- **Maximum disgust within the thesis:** panic quarters, deal-breaks, broken IPOs,
  category-wide selloffs that fail the migration test (§5). Precedents: DeepSeek-quarter
  planting (P-03), CORZ post-vote-rejection add (P-05), CRWV broken-IPO buy (P-07).
- **Asset reclassification** (§4.3) at crypto-trash / conglomerate-discount prices.
- **Spinoff/pure-play emergence** on the scarce input (P-09).
- **S0 physics call:** lead-time/queue data implies scarcity the tape hasn't priced.
- **Strategic inevitability:** a state actor or national-security logic puts a floor
  under an asset the market prices as roadkill ("the US cannot run this race without X").
  Rare; requires the P-02 documentation standard and defined-risk expression (options),
  because the downside case is bankruptcy-shaped even when the strategic logic holds.

**6.3 Validation events (the only license to scale up):** anchor contracts (an
IREN-Microsoft-class deal), take-or-pay/backlog inflections, regulatory/strategic
confirmation (an Intel-government-class event), the S0→S1 detectors firing on a recon
name. Price appreciation alone is NOT validation.

**6.4 Sizing ladder (⚙️ defaults; risk-rules.md caps override):**
- **Recon: 0.5–1.5%.** Purpose = information and forced attention. Basket entries
  allowed (buy the shelf: 2–4 adjacent instruments at recon size when the layer is right
  but the champion is unclear — P-09).
- **Validated: 2–4%** after ≥1 validation event; **champion selection mandatory** when a
  basket exists (keep the purest instrument, kill the rest — do not carry the basket).
- **Conviction: 5–8%** after ≥2 independent validations AND Thermometer still ≤5.
- **Flagship: risk-rules max** — reserved for the rare strategic-asymmetry case; must be
  documented against P-02 (Intel) standards: state actor / structural inevitability
  logic, expressed with defined-risk instruments where possible.
- **Averaging rule: UP on validation, never DOWN on a broken probe.** Down-averaging is
  permitted ONLY when §5 returns NOISE and the entry gate re-passes in full.

**6.5 Door-board governor (v1.4 — correlated-trigger risk; the reply's staged design
with the assessment's numbers).** The board carries ~13 price-gated entry doors ≈12% of
intended book = 30% of the risky sleeve, all one factor, all capable of firing in the
same correlated week. Binding rules:
1. **Count cap:** max 2 H1-correlated door EXECUTIONS per rolling 10 trading days ⚙️.
2. **Capital cap:** max 3% of total portfolio deployed into new H1-correlated exposure
   per rolling 20 trading days ⚙️.
3. **Regime switch:** ALL price-only doors close automatically while any H1 funding /
   utilization / monetization alarm is live (an H1A/H1B falsifier-candidate, a
   funding-clock stage jump, the rental-index crossover) — when the CAUSE of the
   cheapness is the thesis breaking, cheap is not a door.
4. **Reopen path:** a closed door reopens only on non-price validation reviewed by an
   independent refuter (never the analyst who wants to buy).
Doors deferred by the governor queue in Thermometer-label order (LOW first), and the
deferral is journaled — the governor slows correlated buying; it must not silently
cancel the plan (that would recreate the zero-kill bias on the buy side).

### 6.6 Valuation: a scale of voices, a destination card, and the inversion (ADDED 2026-08-01, Ben sign-off)

**6.6a — Never one fair value. A SCALE of voices, never averaged.** Two independent builds
of the same company disagreed by **41% on Nebius ($150.41 vs $212.00)** and **61% on IREN
($24.89 vs $40.00)** on 2026-07-30, and in both cases the cause was identical: one build
valued the whole enterprise and never subtracted the debt funding the build-out. A single
number hides that. Ben, 2026-08-01: *"we should always report valuations on the basis of two
models (Fable and Codex), analysts, bulls and bears; and then I decide which voice is
probably closest to my view today."*

Every live card therefore reports, ordered most cautious to most optimistic, with the live
price marked in its place on that line: **our model (Fable) · the independent second lab
(Codex) · analyst consensus with its analyst count · our explicit cautious case · our
explicit optimistic case · the destination (§6.6b)**. Rendered by
`data/valuation_scale.py`. **They are never averaged** — averaging a right number with a
wrong one produces a third wrong number, and the disagreement was the finding. Where the
voices differ sharply the card states WHY in one sentence. Ben chooses the voice; the engine
supplies the spread and the reason for it.

**6.6b — The destination card. Separate document, separate horizon, never blended in.**
Ben, 2026-08-01: *"we're only looking at the next 12 months which is fine for a fashion
brand, but not fine for a high growth high tech business."* Method, after Andreessen
(*SpaceX & the Sentient Sun*, 2026-06-15, verified verbatim): *"start at the destination and
work backward."* State the terminal outcome in OPERATIONAL units — units sold, share of a
named market, price per unit — then work backward through the preconditions with dates, then
value it.

**Binding requirements, each from a failure mode found at adoption:**
1. **It is its OWN card on its OWN horizon, printed beside the near card, never merged into
   it.** Demonstrated 2026-08-01 on Mobileye: adding the destination as a fourth scenario
   inside the 12-18 month card turned a marginal hold into "buy more" **at a 2% assumed
   probability**, and at 15% it implied +202%. The least reliable number in the analysis would
   have set the entire answer. Same rule as the two-lab disagreement — Ben sees both, never a blend.
2. **Probability-weighted, never conditional.** The conditional return is the easiest number
   in finance to manufacture. A 5x-in-ten-years destination at 20% odds with a 0.2x failure
   case is worth 1.16x — about 1.5% a year, which FAILS. State the odds and the failure value
   explicitly.
3. **Terminal value is PER SHARE, after the dilution and financing the build requires.** All
   four cards built 2026-07-28 made the same error in the other direction — an
   enterprise-level multiple quoted as if it were already an equity value.
4. **Milestones are scored JOINTLY.** Five preconditions each 75% likely are ~24% likely together.
5. **Mandatory stresses:** a two-year delay, a one-third lower exit multiple, lower margins,
   material dilution.
6. **The comparison set must contain failures and mediocrities from the same starting stage.**
   Nvidia, Tesla, Meta and Google are not a reference class, they are a victory montage.
7. **Shadow mode until it earns authority.** A destination card informs but may not authorise
   a larger position until its forecasts have been scored across two reporting cycles.

**6.6c — THE INVERSION, and it is the most useful output.** Rather than asserting our number,
compute **what probability of the destination today's price already implies** to match the
index. Worked 2026-08-01: Mobileye's price implies ~14% against our 15% (we agree with the
market) · Palantir's implies **~43% against our 20%** · Nebius's implies **~95%**. This
converts a verdict into an inspectable disagreement about odds and directly answers the
standing question *"why do prominent funds hold this if they see the same data?"* — usually
because they assign materially different odds, which is arguable, rather than because they
know a different fact. Print the implied probability next to ours on every destination card.

### 6.6d The most we may pay, and the price on an order, are TWO objects (ADDED 2026-08-01, Ben sign-off)

The record that forced this: 15 no-chase ceilings across 156 names, of which 7 were over a
fortnight old and never revisited, 2 were written BELOW the market at birth, and 4 were set
EQUAL to the approved order limit — so every limit raise dragged the ceiling up behind it,
and one name's ceiling rose four times in about fifteen hours. Not one of 26 order limits was
ever derived from a valuation.

**THE BUY CAP** belongs to the COMPANY and to a dated valuation. It is the most the business
is worth paying at all. Computed, never chosen: the probability-weighted value divided by
what an index returns over the SAME horizon, after the 26% tax. Above that price the
index is the better use of the money. `data/buy_cap.py` writes it; `book/buy_caps.md` is the
readable form. **The horizon must belong to the value being discounted** — discounting a
12-18 month value by a ten-year index return is a units error, and it made Mobileye's cap
read 46% below the price instead of 2.5% below on the day this was built.

**THE ORDER LIMIT** belongs to ONE ORDER and comes from the live quote and the spread at the
moment of placing.

**What may never happen:** an order limit raising a cap · a rising share price raising a cap ·
a missing cap read as permission · Ben's approval of a price mutating the cap itself. Only new
evidence about the business moves a cap. **An order ABOVE a valid cap (amended 2026-08-11,
upgrade brief §7.2 — the 08-04 warn-only code and this text finally agree):** it may proceed
only on Ben's explicit approved price, and the preflight prints the cap beside it with the
premium stated. Every no-chase ceiling in triggers.csv is now TYPED by whose number it is —
`authority` = model | owner | analyst. An owner override adds or raises an OWNER row to
exactly his number; it never edits a model row, so the model's ceiling survives on the record
and in the preflight print even when his instruction governs the order.

**Scope: owned and actively-considered names only.** A cap on a company nobody is about to
buy is a number nobody maintains, which is exactly how 7 of 15 went stale. A parked name gets
one when it is promoted, BEFORE an order can be approved, never after.

**Expiry: 7 days, and immediately on results, guidance, a capital raise, or a 15% price move.**
This costs nothing while we are not buying — an expired figure is flagged loudly and cannot be
cited as current; the re-read is owed before the next approval is sought (since 08-04 only
Ben's own words stop a transmit, so the expiry warns rather than blocks).

**When the price sits above the cap on something we own:** buy no more, cancel any resting
purchase, put the money into the next-best idea. It is NOT a reason to sell — selling
crystallises tax, which usually costs more than the mistake it is trying to fix.

`data/ibkr_order.py` runs all of this as a BUYCAP check that WARNS with the premium printed
(since 2026-08-04, Ben's correction: only his own words stop a transmit). What blocks: his
approval row matching the exact order, the typed no-chase ceiling, the exit backstop, real
settled cash, and the sanity cap. Every preflight — blocked, dry-run or transmitted — is
frozen to `book/preflight_log.jsonl` (added 2026-08-11).

### 6.7 No open-ended waiting (ADDED 2026-08-01, Ben sign-off)

**Every parked name carries an expiry date.** At expiry it resolves to owned, declined and
logged for grading, or re-underwritten ONCE — one extension only, requiring a NEW FACT, with
the original decision date preserved. Then it is archived. The active queue is capped at what
one operator can actually cover — **see §2.3 for the number, which is 21 as of 2026-08-03.**
This sentence deliberately does NOT restate the figure. It said "10–15" from 2026-08-01 while
§2.3 said "≤16", and two numbers for one shelf meant neither bound anything. One cap, one home.

**A price condition requiring a large fall is a crash shopping list, not a pipeline** — it
lives on a separate list so it stops impersonating live coverage. The distance is expressed
as an expected return or normalised for the name's own volatility, never as a flat percentage:
a 15% move means completely different things for Tencent and for a small AI-infrastructure name.

**And undeployed money is not free.** risk-rules.md already holds that uninvested risky-sleeve
capital sits in the index proxy rather than cash, because an empty book waiting in cash is
itself an active bet against the benchmark. That rule is what gives every "not yet" a visible
price, and it is the structural answer to inertia.

**AMENDED 2026-08-04 (review #2, Ben's sign-off). The rule above was adopted on 08-01 and
three days later nothing was enforcing it.** Measured, not remembered, at review #2: of the
89 non-owned names on the live shelves, **26 carried no expiry date at all** and **5 did not
say what they were waiting FOR**; and of the 110 rows that did carry a date, every one was a
uniform 90-day stamp applied in bulk on 08-01, so **110 names all fall due on 2026-10-30**.
A date that lands on the same day as 109 others is a queue, not a forcing function. Three
corrections, all now in code (`data/decide_by.py`, in the daily chain, exits non-zero when
there is work; renders `book/decide_by.md`):

1. **A live-shelf row needs BOTH a date and a NAMED thing it is waiting for.** Waiting is
   legitimate when it names a disclosure, a filing, a ruling or a price test. Waiting for
   nothing in particular is indecision with a date stapled to it, and the check now separates
   the two. The three outcomes at expiry are unchanged: owned · declined-and-logged ·
   re-underwritten ONCE on a new fact.
2. **Bulk-stamped dates are reported as bulk-stamped and are NOT re-stamped in bulk again.**
   Each gets a real date, anchored to that name's own next disclosure, the next time anyone
   touches the row. Re-stamping 110 rows a second time is the same mistake twice.
3. **A DECLINED name must carry a written condition that would bring it back — Ben's
   addition, 2026-08-04:** *"it would be good to keep a memory of the players that we've
   declined, so that at a future date we may actually invest in them again in case they
   become more relevant."* `kills.csv` already does this properly — 26 of 26 killed names
   carry a reopen condition. The **ARCHIVE shelf does not**: at review #2, **67 of 82
   set-aside names had nothing watching them and no written condition that would revive
   them.** A name declined with no way back was not declined, it was deleted, and the reason
   it was set aside may stop being true without anyone noticing. Archiving a name now requires
   a reopen condition the same way killing one does.

Why this is enforcement and not a new rule: the engine's own record says prose rules with
nothing checking them are the dominant failure class, and this is a clean specimen — the rule
was right, signed, three days old, and silently unobserved. The generalisable form: **a rule
adopted without a check is a rule adopted without a date of death.**

---

## 7. Exit playbook & Darwinism

**7.1 Sell-to-consensus (structural exits):**
- Thermometer ≥7 → trim review; ≥8 + vertical → mandatory trim proposal (§3's surviving
  trim-review use; its entry gates were deleted 2026-08-01).
- Stage S3 reached → **open a written distribution DECISION, not an automatic sale
  (amended 2026-07-29, Ben sign-off; previously "begin distribution regardless of how good
  the story sounds").** The default remains distribute — the story is loudest at the top
  (H2's own language), and the precedents stand: CEG/VST sold to consensus (P-04), LITE
  pressed through the double then fully exited (P-10), CRWV sold into post-IPO euphoria
  (P-07). **The exception, and it is narrow:** a name carrying a live DURATION thesis under
  §6.1 check 5 and passing its durability re-read may HOLD at S3, with the decision written
  and dated. This aligns the rule with the §3 trim band, which already said "a durable
  compounder whose earnings outpace expectations may HOLD at S3 with the decision written",
  and with check 2's amended entry conditions — before today this line said sell, §3 said a
  compounder may hold, and check 2 said never buy. Three clauses, three answers, one
  situation.
  **The guard: "it's a compounder" must not become the universal reason never to
  distribute.** The hold requires the durability re-read to have been RUN and PASSED on a
  dated basis, not asserted. A held S3 position with no dated re-read on file is
  distributed at the next review, no argument.
- **Never round-trip a winner:** once a position is +100% from blended entry ⚙️, a
  standing trailing-review triggers on each further +25% leg — decide *in writing* to
  hold or trim; silence is not a decision.
- Accept the BE tension consciously (P-06): disciplined trims will sometimes leave
  spectacular upside on the table. The process is the asset; hindsight P&L on single
  names is not the judge.

**7.2 Kill rules (tactical hygiene):**
- Every position carries a pre-written kill condition at entry (thesis-based, not only
  price-based).
- **Probe timer:** recon positions with zero validation events after 2 review cycles ⚙️
  → exit by default; keeping requires a written exception. (ONTO one-quarter kill, P-11;
  Galaxy, KRC, LBRT one-to-two-quarter kills.)
- **Wrong-layer exit (EQT rule, P-08):** if the §4.2 test now locates the profit pool in
  a different layer, exit even at flat/loss and even though "the thesis is fine." Time is
  the loss.
- **Pricing-power kill (Ajinomoto tell, P-17):** for any position whose thesis rests on a
  supplier's ability to charge a scarcity premium (the §4.2-#1 test), the position is
  reviewed the day that supplier has a clear opportunity to raise prices and *declines to*.
  Declining to raise when it could = the pricing power the thesis assumed isn't there.
  Sharper than most triggers because it's a single observable fact, not a judgment call.
  (Baker's own stated rule; import verified against §4.2-#1 — consistent, not contradictory.)
- **New-fact rule (v1.3) — with the backstop exception (v1.4):** every exit or trim
  cites the NEW FACT that changed the thesis. "The price moved a lot" is not an exit —
  it is a rebalance; route it to the §6.4 sizing ladder (frameworks §3.C3 salience
  check: bad sells are triggered by price moves, good sells by new information —
  Selling Fast and Buying Slow, JF 2023). **EXCEPTION AMENDED 2026-07-29 (Ben, stated
  twice; risk-rules.md's NO AUTONOMOUS SELLING clause governs and this line restates it):
  a breached pre-written price backstop fires the WRITTEN CHECK — is the business still
  sound on its named measures, and is this a market-wide selloff? — and produces a
  RECOMMENDATION to Ben. It does not exit by itself, and no order is placed without a fresh
  instruction from him quoting the number.** The previous wording read "EXITS, full stop —
  no new-fact test, no debate, no override in the moment", which made a level
  self-executing; Ben closed that reading on 2026-07-29. The pre-commitment logic that
  produced it still holds and is preserved in the check: the level decides WHEN to look,
  calmly and in advance — the check decides what to do. Re-entry stays allowed through the
  normal gate once the §5 test returns NOISE.
  (From the 07-12 reply: the engine had answered a paper about selling being hard by
  adding friction to selling; this removes the friction exactly where the decision was
  already made in advance.)
- **Sleeve Darwinism:** at each review, force-rank sleeve members; feed the top on
  validation, kill the bottom on the timer. A sleeve is a competition, not a museum.

---

## 8. Instrument selection (payoff-shape matrix)

| Situation | Instrument | Why (shape logic) |
|---|---|---|
| Durable thesis residence | **Common stock** | No clock, no decay; survives being early (FP-7) |
| Regime-change moment expected (catalyst, crash-reentry) | **Calls** | Convexity: prepaid max loss, multiplied jump capture; leverage that cannot be liquidated — survives interim wicks that would stop out linear leverage (P-07 crash-buy) |
| Re-entering a loved name at post-run prices | **Collar** (stock + puts + calls) | Thesis exposure with a crash floor; the puts fund nerve (P-07 Q3'25) |
| Expect violence, can't call direction | **Straddle-family (own puts AND calls)** | Paid for magnitude; expresses fat-tail worldview (P-13: MU/TSM) |
| Crowded first-order name at S3, overextension evidence in hand | **Puts** (tactical book only, §9) | Defined-risk fade; never naked-short structurally |
| After the jump lands | **Convert calls → stock** | Options are the vehicle for transitions, stock for residence; de-lever into the new regime (P-07 Q1'26) |

**Convexity budget (⚙️):** total option premium at risk ≤ a fixed % of book (set in
risk-rules; suggest 2–4%/yr theta budget). Convexity is *rented* — time decay is the
rent; going sideways loses. Buy it where IV is cheap relative to the expected violence;
avoid paying up for obvious melt-ups (indicator #6 on the Thermometer doubles as an
IV-crowding check).

**Prohibitions:** no undefined-risk shorts; no options positions without written strike/
expiry/premium logged (we suffered this opacity reading 13Fs — don't recreate it in our
own journal); no leverage whose worst case violates the drawdown budget in profile.md.

---

## 9. Two clocks & the hedge dial

**9.1 Two books, bookkept separately.** Tag every position in `state/portfolio.csv`:
- **S (structural):** multi-quarter/multi-year thesis residences. Judged on thesis milestones.
- **T (tactical):** timing expressions — the hedge overlay, catalyst options, fades.
  Judged on entry/exit quality over weeks–quarters.
Blending the clocks is how a bleeding hedge becomes "long-term conviction" (FP-7).

**9.2 The hedge dial (states, not habits):** OFF → PILOT (small index puts, recon-sized)
→ FULL (sized overlay). The overlay is **a view with a P&L, not insurance** — the moment
it moves, Ben is claiming timing skill and is exposed to being wrong twice (exit and
re-entry). Own that in the journal or leave the dial at OFF.

**Dial rules:**
- **H-1 · Never hedge into strength.** The urge to buy protection peaks exactly when
  momentum still pays; separate the *feeling* "too high" from *evidence* of setup
  (breadth rolling, book-to-bill cracks, S3→S4 detectors). The fund carried ZERO overlay
  through the melt-up quarter and re-armed after (P-01).
- **H-2 · Early = wrong on the short side.** Being right eventually while paying carry is
  indistinguishable from being wrong. The mid-2025 overlay bled for two quarters (P-01
  cost leg). Size shorts only after overextension evidence, into established breaks if
  need be (the fund's ORCL puts came *after* a ~50% decline).
- **H-3 · PILOT before FULL.** A small standing line (the fund's INFY put) keeps the
  thesis instrumented without the carry bill.
- **H-4 · Whipsaw budget (⚙️):** max 2 dial flips per year; each flip journaled with the
  evidence that fired. Exceeding it = the dial has become mood.
- **H-5 · Hedge the *layer*, not the world:** overlay targets the crowded first-order
  complex (relative-value per H3), not the whole book's beta — Dalio-lens ballast is a
  separate allocation.
- **H-6 · Every dial change states the intended sequence (FP-8)** — what must happen,
  in what order, for the flip to pay.
- **H-7 · Instrument choice is unresolved — decide it deliberately each time (P-19).**
  Baker runs his tactical hedge via broad **index** puts (0%→46%→20%, 2024–26); Leo runs
  his via **single-name semi** puts. These are different bets — systemic beta vs relative
  first-order overextension (H-5). Neither is the settled default for this book; size the
  overlay by naming which one the specific thesis calls for, not by habit. (Open question,
  flagged for the next overlay-sizing decision, not auto-resolved.)

---

## 10. 13F intelligence protocol (upgrades `fetch_13f.py` usage)

Influence funds (Situational Awareness LP CIK 0002045724; Atreides) are **idea flow and
disagreement signal, never trade instructions**.

**Mechanics to enforce when parsing:**
- 13Fs show long stock + long option legs at **notional** (underlying value), never
  premium, strikes, expiries, short stock, written options, cash, non-US, or privates.
  → Never infer position "size" or returns from option notionals; never infer *net*
  direction when both puts and calls appear (that's a long-vol structure, not confusion).
- **Dust filter:** ignore lines <0.2% of filing value sitting beside a large derivative
  on the same name (lifecycle residue/placeholders — the 1-share-Intel class). Signal =
  what is *sized*.
- Growth in disclosed value ≠ returns (inflows + notional accounting; the "+2,065%" and
  "$225M→$13.7B" fallacies).
- Expect filer errors (the BE Q3'25 value/share mismatch); sanity-check implied prices
  against the same filing's option lines.
- **Diff, don't snapshot:** the information is in quarter-over-quarter *changes* —
  weight shifts, flips, basket→champion moves, dial states — read as behavior. The
  weight is the decision, not the ticker.
- **Recon-line surveillance (the highest-value read):** the fund's *future* book has
  historically been visible in its 2% lines three quarters early (miners/neocloud
  entered at 2–4% in Q1'25 while Intel was 46%; they *were* the book by Q4'25). So every
  diff must surface NEW small positions as a named list and route them into §2.4 source
  #4. Live examples from Q1'26: T1 Energy (a suspiciously round 10M-share block —
  US battery/solar manufacturing), SharonAI, HIVE. Their large consensus positions are
  their past; their small fresh lines are their hypotheses.
- **Staleness:** filings land ~45 days late; assume the book has changed; NEVER buy a
  disclosed name trading >25% ⚙️ above its filing-date mark without a full independent
  entry gate (that's copy-trading the exit liquidity).
- **Filings lead words (P-20):** when a manager's disclosed 13F and their public statements
  disagree, WEIGHT THE FILING — every time, no exceptions. Atreides' Q1'26 13F (filed May 18)
  showed the optics→interconnect rotation a full month before Baker's public "bottleneck
  trade is over" call (Jun 16). The filing is the earlier and more honest signal; the
  interview is marketing. Applies to any influence fund, including one you're positioned
  against. (Monitoring discipline, not a trading rule — low-risk to adopt wholesale.)

**Standing calendar:** quarterly, ~Feb/May/Aug/Nov 14. Next: **Q2 2026 due ~Aug 14** —
the live question is the hedge dial: did the Q1 put wall roll (conviction short), expand,
or vanish (tactical dial again)? And did BE keep being distributed into the $200–300s?
Each outcome updates the H2/H3 read and the §9 dial evidence base — pre-write the three
branches at the next review.

---

## 11. Precedent library (cite as P-xx in analyses)

- **P-01 · The hedge dial.** Overlay ON (27% Q2'25) → bled vs rising underlyings → OFF
  entirely for the Q4'25 melt-up → ON at ~5× / 62% Q1'26. Lesson: hedge = timed view;
  never into strength; removal captured the melt-up naked.
- **P-02 · Intel calls.** 46% position via calls at ~$22 at maximum pessimism; strategic
  logic (state can't lose domestic fabs); held 4 quarters; catalyst delivered (gov stake
  8/25); flipped to puts once catalyst spent. Lesson: strategic inevitability + defined-
  risk expression + exit when the reason dies.
- **P-03 · DeepSeek response.** Book -20-30% shock; migration test said NOISE; sold the
  weak legs (MRVL, VRT), *added* generators. Lesson: noise = buy window within thesis.
- **P-04 · IPP rotation.** VST/CEG/TLNE from day one; ridden ~+40–55%; exited at
  consensus while the story stayed loud; capital moved to the bypass (Trade 1 → Trade 2).
  Lesson: the same thesis, next instrument; sell to consensus, IPPs kept grinding — and
  that was fine, torque > residual grind.
- **P-05 · Asset reclassification (miners).** CORZ $7 / IREN $6 / APLD $5.6 entries when
  categorized as crypto trash; the asset was energized land. Added on every validation;
  CORZ added through the deal-break. +100–460% on marks. Lesson: classification edge +
  average-up + nerve at panic.
- **P-06 · BE trim.** Tripled at ~$87 (15.9%), trimmed 36% into $135 (+56% quarter);
  stock later ~$300. Lesson: process-correct trims can cost hindsight P&L; take the
  tension consciously, keep the core.
- **P-07 · CRWV lifecycle.** Broken-IPO buy $37 → sold ALL into euphoria (~$187 peak) →
  re-entered 10× as a collar at $137 → halved; collar floor + calls-into-the-crash
  (10.8M underlying) → converted calls to stock on recovery. Lesson: no relationship
  with the ticker; instruments per regime; convexity as knife-glove.
- **P-08 · EQT (wrong layer).** "Gas powers AI" true; upstream captured nothing; ~flat
  over ~1 year, 3 restructurings, then killed. Lesson: profit-pool location test; exit
  wrong layers regardless of narrative fit; time is the loss.
- **P-09 · Storage basket → champion.** WDC+STX+SNDK probed ~$13M each; champion (SNDK,
  the pure spinoff) kept and 10×'d; parents sold. SNDK $112→$635 marks. Lesson: buy the
  shelf when the layer is right, then concentrate fast.
- **P-10 · LITE.** Entered $163 → added into a double → exited fully near the cycle top,
  then leaned on the laggard (GLW puts). Lesson: press validation, exit the *cycle*, not
  just the name.
- **P-11 · Probe kills.** ONTO, Galaxy, KRC, LBRT, HUT, TSEM: one-two quarters, no
  validation → gone. Lesson: Darwinism keeps the book honest; small probes are cheap
  questions, not commitments.
- **P-12 · The copier's trap (meta).** The fund was discovered via a viral LinkedIn post;
  by then BE traded ~2.2× the filing marks *while the filer had been selling*. Lesson:
  discovery channel sets the consensus floor; disclosed books are exit liquidity for
  their authors.
- **P-13 · MU/TSM straddles.** Puts AND calls owned on both names simultaneously.
  Lesson: when the view is "violence, direction unclear," buy the shape, don't force a
  direction.

### Atreides cross-reference (v1.2 — Baker's compute-chain run of the same engine)
- **P-14 · Astera Labs, double-into-weakness (Q1 2026).** Added +109% to the position
  while the stock fell ~34% intra-quarter; +271% three months later. Bought at IPO (S0/S1),
  added on a mid-stage pullback (NOT an S3→S4 migration). Lesson: the §5 noise-vs-migration
  test, run correctly by a different manager — the test generalizes.
- **P-15 · AMD, full-cycle exit before the continuation.** Held Q3'22→Q3'25 (+155%), exited
  ~$200 at S3 consensus ("the AI chip trade, fully priced") — then AMD ran to $518. Lesson:
  a second independent instance of P-06 (BE trim): process-correct trims cost hindsight P&L.
  Two managers, two occurrences → it's a structural tax of the discipline, not a misread.
- **P-16 · Optics sleeve trimmed into strength (Q1'26).** After multi-quarter runs (Ciena
  ≈+377%, Coherent ≈+121%), Atreides cut Ciena 53% / Coherent 49% / Lumentum 30% the same
  quarter he doubled Astera. Lesson: §7.2 sleeve Darwinism executed across a whole sleeve —
  feed the top (Astera), trim the run (optics).
- **P-17 · The pricing-power falsifier (Ajinomoto tell, Jun 2026).** Baker's rule: a
  bottleneck-long dies the day the scarce-input supplier can raise prices and declines to.
  Imported as a named kill type in §7.2 — a single observable trigger, not a judgment call.
- **P-18 · ACV Auctions / Wayfair, no-falsifier trap.** Held 21 quarters, −88% / −76%, both
  still held — legacy names that never got a kill condition attached. Direct confirmation of
  anti-pattern #9 and §7.2's "every position carries a pre-written kill condition."
- **P-19 · Index-put hedge dial (0%→46%→20%, 2024–26).** Independent confirmation of P-01
  (hedge = timed view, cycles with sentiment, never static) via a different instrument
  (broad index puts vs Leo's single-name semi puts). Strengthens FP-7/§9's two-clock
  separation; opens the H-7 instrument question.
- **P-20 · Filings lead words.** Atreides' Q1'26 13F (May 18) showed the optics→interconnect
  rotation a month before Baker's public "bottleneck trade is over" call (Jun 16). Imported
  as the §10 "filings lead words" discipline — weight the disclosure over the interview.

### Fiber-bust cross-reference (v1.3 — the 1996–2005 telecom overbuild, ratified
### 2026-07-12; full evidence in notes/2026-07-07-dotcom-fiber-precedents.md)
- **P-21 · The traffic myth.** Real ~2x/yr demand was marketed as "2x/100 days" by the
  party SELLING capacity (WorldCom/UUNET), justified 6+ parallel builds; supply grew
  +186,000x vs demand ~128x. Lesson: a demand claim from a capacity seller is marketing
  until confirmed by someone who loses money if it's wrong — anchor H1 evidence to
  measured third-party volumes (OpenRouter/Epoch/AI Index), and treat capex plans citing
  each other's projections circularly as an alarm.
- **P-22 · Vendor financing peak.** $25.6B of supplier loans to customers by end-2000
  (Lucent $8.1B); "revenue" was the supplier's balance sheet round-tripping; Lucent's
  receivables warning (Jan 6, 2000, −28%) led the Nasdaq top by two months. Lesson: when
  the supplier funds the buyer, demand is capex reflux — track the most aggressive
  financier's receivables/DSO and investee-revenue share as the top-of-cycle gauge
  (live: NVDA DSO 59d, investee commitments, CRWV backstop).
- **P-23 · Round-trip revenue & invented metrics.** Capacity swaps = 32% of Global
  Crossing's "cash revenue"; Qwest booked $3.8B sham revenue; pro-forma metrics
  proliferated exactly at the top. Lesson: circular deals + novel non-GAAP metrics +
  peer-counterparty concentration = manufactured story (live: single-counterparty RPO
  concentration, useful-life extensions, any new "adjusted capacity" metric).
- **P-24 · The demand paradox.** Traffic kept doubling THROUGH the bust; per-bit price
  fell faster (−55%/yr); 97.3% of fiber sat dark; commodity capacity sellers were wiped
  out while volume exploded. Lesson: volume ≠ profit — profit = volume × scarcity ×
  contract; never hold the spot-priced commodity layer into the capacity crossover
  (live detector: GPU rental index rolling while shipments still grow).
- **P-25 · Survivor anatomy.** AMT at $1.10 with full towers (5–10yr leases, credit
  tenants, escalators) → ~100x; Equinix near-death → >100x on interconnection network
  effects; Exodus, the SAME "datacenter" label → $32B→0 (commodity hosting, short
  contracts, startup tenants, leverage). Lesson: within one layer label, contract
  duration + tenant credit + asset non-replicability separate 100-baggers from zeros —
  and even the right assets drew down 90%+ when levered; the fortune was the DISGUST
  entry (live: CRWV contracts = Equinix-shaped; spec shells on private credit =
  Exodus-shaped; tenant-credit = what % of leases sit on cash-burning counterparties).
- **P-26 · Stocks top before orders; the funding window is the tell.** Equipment stocks
  peaked Mar–Sep 2000; orders confirmed the top only Q4'00–Q1'01 (Cisco's $2.25B
  write-off Apr'01). The on-time tells: CLEC high-yield window shut spring 2000; Lucent
  receivables warning Jan 2000. Lesson: book-to-bill is the LAST confirmation — the
  marginal buyer's funding access breaks FIRST (→ §2.2 detector, added v1.3; live: AI
  private-credit spreads, neocloud coupons, hyperscaler jumbo-bond demand).
- **P-27 · The applier harvest.** Google bought bankrupt carriers' fiber for pennies
  (2002–05); AWS/YouTube/Netflix were built on collapsed bandwidth costs. Lesson: the
  bust is the setup for the next decade's best trade — pre-write the distress shopping
  list (energized land, powered shells, PPAs, interconnection positions, secondhand
  accelerators); standing trigger = first Ch.11 of a levered neocloud/DC with real
  assets. Maintain the list at each review.

---

## 12. Templates

**12.1 Journal entry — additional fields (append to existing format):**
```
Consensus score: X/10 (indicators cited)
Origin channel: [own research / screen / viral-tracker (→min 5)]
Lifecycle stage: S0–S4 | Layer: first/second-order + profit-pool note
Clock: S / T | Instrument + why this shape (§8)
Sequence intended (FP-8): ...
Validation events so far: ...
Kill condition: ...
Migration-test answers (if shock-driven): Q1/Q2/Q3 ...
```

**12.2 `state/phase-map.md` starter:**
```
# Phase Map — bottleneck chain (update every review)
Snapshot: YYYY-MM-DD
| Layer/constraint | Stage (S0–S4) | Evidence | Next detector to watch |
|---|---|---|---|
| Grid-scale generation (IPPs) | S3–S4 | ... | book-to-bill, queue normalization |
| Speed-to-power / onsite (bypass) | S2–S3 | ... | §2.2 S2→S3 list |
| Energized-land conversions | S2 | ... | contract cadence |
| CANDIDATES (next): transformers, turbine slots, permitting/land, EPC labor, water, HBM | S0? | lead-time data | first anchor deals |
| INTAKE (from §2.4 #4): influence-fund recon lines — currently T1 Energy, SharonAI, HIVE | S0 cards pending | Q1'26 13F diff | next filing ~Aug 14 |
Stage-change log: ...
```

**12.3 Decision test — print verbatim in Mode-2 outputs:** the §6.0 three-layer result
(eligibility · money test at the 20/30/40% downside weightings · rank-and-size), then the
re-homed §6.1 checklist with each check's finding + one-line evidence. Only checks 6
(independent refuters) and 8 (no same-day action on news) carry a veto of their own;
the old PASS/FAIL-per-check AND-chain framing is retired (2026-08-01).

---

## 13. Anti-patterns (extends SKILL.md failure modes; violations are journaled)

1. **Buying without the money test** (rewritten 2026-08-01, replacing "consensus entry").
   The anti-pattern is no longer buying something popular — it is buying anything whose
   probability-weighted after-tax return does not beat simply holding the index. Popularity
   is an input to size. The arithmetic is the discipline.
2. **Copy-trading** — buying stale disclosures above filing marks without a full gate.
3. **Hedging into strength / early shorting** — H-1/H-2 violations.
4. **Averaging down on broken probes** — down-adds without a NOISE verdict + re-gate.
5. **Marrying tickers** (FP-5) or **staying in the wrong layer because the thesis is
   right** (P-08).
6. **Confusing notional/AUM growth with returns** — in others' filings or our own
   accounting.
7. **Options without logged strike/expiry/premium** or beyond the convexity budget.
8. **Clock-blending** — reclassifying a bleeding T position as S "conviction."
9. **Trimming winners by reflex / letting probes ride by neglect** — the exact inverse
   of §6.4/§7.2 (validation sizes up; timers kill).
10. **Narrative sizing** — position size tracking story quality instead of validation
    count + Thermometer + risk rules.

---

## 14. Falsification of the playbook itself

This playbook inherits H1–H5's falsifiers (a dead thesis makes behavioral excellence
irrelevant). Additionally, the playbook is *itself* downgraded if its scored calls (via
the journal) show: disgust entries systematically caught falling knives that stayed
broken (migration test miscalibrated), or sell-to-consensus exits systematically forfeited
>2× subsequent upside (thermometer thresholds too tight ⚙️ — tune, don't abandon). The
August 13F and each quarterly diff also test the source: if the fund's own dial-timing
degrades into whipsaw, weight the Aschenbrenner lens down accordingly — believability is
earned per Dalio, not granted.

*Decision-support methodology. Ben makes all final decisions. Nothing here is financial
advice; risk-rules.md and profile.md constraints override every default in this file.*
