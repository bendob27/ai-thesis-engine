# The Thesis — Falsifiable Hypotheses

Owner: Ben. Style: thematic long/short, quarterly/semi-annual cadence, multi-year themes.
Objective: maximize long-run wealth within the risk budget in `risk-rules.md`.

Each hypothesis carries: a claim, current evidence, **monitoring indicators** (check at
every review), **falsification criteria** (if triggered, the hypothesis is downgraded or
killed — no re-rationalizing), a **conviction score** (1–10, update with dated log), and
**what's priced in** as of the last snapshot.

Snapshot date: **2026-07-06**. Assume stale; verify live data every session.

---

## H1 — The AI capex supercycle persists (master regime variable; SPLIT A/B 2026-07-13)

**Claim — split into two propositions (2026-07-13, review #1.5, Ben sign-off; they can
break separately and the book must be able to react to each alone):**
**H1A (spending persists):** hyperscaler + neocloud capital spending keeps compounding
for 3–5 more years — for competitive, geopolitical, or platform-defense reasons if not
economic ones.
**H1B (spending pays the suppliers we can buy):** that spending generates sufficient
economic return to support SUPPLIER and platform equity values — utilization, pricing,
margins, and contract quality hold up, so elevated capex converts into attractive
returns for the layers this book owns. The hardest scenario for this book is H1A intact
while H1B breaks: capex stays high, supplier growth decelerates, margins normalize,
multiples compress — the story survives while most public expressions lose money
(the fiber-bust pattern, P-24/P-26). Exposure REDUCES when H1B weakens even if H1A
is fully intact.

**Evidence (Jul 2026).** Big-four 2026 capex guidance ~$725B, +77% YoY (AMZN ~$200B, MSFT
~$190B, GOOGL ~$175–185B, META ~$115–145B). Goldman projects ~$5.3T 2025–2030. Google
Cloud backlog >$460B. Microsoft AI revenue run-rate >$37B.

**Why it matters.** Every long in this book is directly or indirectly a claim on this
spending. H1 is the shared factor: if it breaks, longs fall together regardless of theme.

**Monitoring indicators.** Quarterly capex guidance (4 hyperscalers, aggregate, YoY and
revisions vs prior guide); NVDA data-center revenue growth; TSMC leading-edge utilization
and CoWoS capacity adds; AI revenue run-rates vs capex (the monetization gap); credit
financing of neocloud buildouts (debt-funded capex is the fragile kind).
**Frontier-lab unit-economics tripwire (added 2026-07-06, from Epoch data):** OpenAI/
Anthropic quarterly GROSS MARGIN (rev − inference compute) and revenue growth rate. Current
read: ~30–40% gross margin (vs 70–80% for normal software), ~−5% operating margin, R&D still
> gross profit — the supercycle is funded by revenue hypergrowth + external capital, NOT
internal cash (capex now exceeds hyperscaler operating cash flow; Alphabet raising $80B
equity). Crack signal: gross margin compressing below ~25–30% OR revenue growth dropping
under ~2×/yr. This is a cleaner, measurable version of the monetization-gap falsifier below.
Also watch the "value-benchmark gap": AI clears bounded tasks but fails long/integrated
high-value work (Remote Labor Index low; GDPval ~mid-70s on 7h tasks) — the measured root of
the enterprise-agent rollback and dying token-pass-through pricing.

**Falsifier-(b) standing monitor (adopted 2026-07-12, review #1, Ben sign-off).** The
audited Funding Clock (`data/funding_clock.py`, capex/OCF TTM per filer, self-auditing
vs the filer's own 12-month facts) is the official read on funding quality: crossing
1.0x = externally-funded buildout. Board 2026-07-10: CRWV 2.77x · ORCL 1.74x · AMZN
1.02x (crossed) vs GOOGL 0.63x · META 0.61x · MSFT 0.57x (self-funded); NVDA = supplier,
watched via DSO (59d vs 54d y/y; flag at +15%). Watch alongside, each review: (i) AI
share of US corp-bond issuance; (ii) foreign net flows into US equities; (iii) regional
electricity prices (all Bridgewater-derived, ledger 2026-07-08); (iv) new-issue demand
on hyperscaler jumbo bonds — cover ratio + concession vs market norm (first live
reading: AMZN Jul'26 $25B — 2.5x peak/1.6x final cover vs ~4x 2026 IG norm, +12–22bps
concession; the buyer-side tell).

**Falsifiers.** H1A (spending): (a) two consecutive quarters of aggregate downward
capex guidance revisions; (b) monetization gap widening two+ quarters while equity/debt
markets tighten for neoclouds; (c) a top-3 hyperscaler explicitly pivots from "supply
constrained" to "digesting capacity." H1B (supplier economics — added 2026-07-13,
review #1.5; these fire on the funding-clock/monitor set above): (d) accelerator rental
prices falling while installed capacity still rises (the P-24 crossover); (e)
utilization or backlog-to-conversion deteriorating at supplier layers while capex
guides hold; (f) material cancellations, renegotiations, or subleasing of contracted
capacity; (g) disclosed AI revenue failing to cover incremental depreciation + energy +
operating cost at a major builder; (h) supplier receivables / vendor financing rising
faster than sales (P-22, NVDA DSO flag +15%); (i) useful-life EXTENSIONS amid
accelerating hardware obsolescence (the accounting-flattery tell, P-23 — Amazon's
SHORTENING is the honest direction). H1B falsifiers can trigger a book-level de-risk
WITHOUT an H1A thesis kill.

**Watch the second derivative.** At +77% YoY, the risk to prices is deceleration, not
decline. Enabler stocks can fall 40% while capex still grows.

**Conviction: H1A 8/10 (spending persists) · H1B 5/10 (spending pays our suppliers).**
Change log: 2026-07-06 initialized (as unitary H1, 7/10).
2026-07-07: three monitoring signals logged, score UNCHANGED — weight together at first
/review. (a) Funding fragility: hyperscaler capex now exceeds operating cash flow
(Alphabet $80B equity raise; Oracle debt+equity; Amazon bonds — Epoch). (b) Demand-side
reckoning at LOW volume: 74% of firms rolled back customer-facing agents; Uber/Meta
capping token spend (Axios May'26). (c) Frontier-lab PRICE WAR opened: Anthropic cut
Jun 30 (Sonnet 5 $2/$10 intro), OpenAI weighing cuts (WSJ), GLM 5.2 open weights at
~1/6th Opus pricing — and BOTH labs filed confidentially for IPOs (Jul'26). The
unit-economics tripwire gains its first direct observable: prospectus gross margins.
Current read MIXED (SemiAnalysis: Anthropic inference margins rose 38%→70% y/y).
Watchlist row FRONTIER-LAB-IPOS carries the triggers.
2026-07-12 (review #1): conviction UNCHANGED at 7. Mixed quarter — build side
steepening (5-hyperscaler capex +72%/yr; TSMC capex guided toward $56B top of range)
while funding QUALITY deteriorates at the margin (3 of 7 clock names crossed capex>OCF
on audited XBRL; ORCL guided FY27 capex $90–95B with ~$40B external funding planned;
AMZN paid the year's weakest jumbo-bond demand, +18–21bps concession, and says no more
2026 debt; CRWV borrowing at 9.625%/8.5%). Falsifier-(b) NOT met — fragility is
narrower than press claims (MSFT/GOOGL/META self-fund at 0.57–0.63x). Adopted the
standing falsifier-(b) monitor block above (Ben sign-off). Next read: hyperscaler Q2
prints Jul 22–30 (falsifier-(a) watch) + TSMC Jul 16. Ledger trail: H1 rows
2026-07-07 → 2026-07-10.
2026-07-13 (review #1.5, Ben sign-off): **H1 SPLIT into H1A/H1B** per the external
merits assessment's strongest recommendation — the unitary claim mixed "spending
continues" with "spending pays our suppliers," and the book's hardest scenario is the
first without the second. Initialization: H1A 7/10 (carries the old H1 score — the
spending-persistence evidence was always the stronger leg); H1B 5/10 (initialized
fresh: build-side strength offset by the funding-quality erosion and pass-through
history already in the ledger — rental-index rebound is the current supporting read,
the AMZN bond concession the current opposing one). Six H1B falsifiers added (d–i),
all wired to EXISTING monitors (funding clock, rental index, DSO, useful-life watch).
Sub-scores move independently at reviews from here. Cite:
notes/2026-07-13-merits-assessment-response.md; AI_Investment_Engine_Document_Merits_Assessment.pdf pp. 5, 12.
2026-08-04 (review #2, Ben's explicit sign-off, span requirement OVERRIDDEN): **H1A 7 → 8.
H1B UNCHANGED at 5.** Evidence trail, all since 2026-07-13, one direction, weight A/B:
(i) **falsifier-(a) is further from firing than at any prior review** — it requires two
consecutive quarters of aggregate DOWNWARD capex guidance revisions, and this quarter three
of the big four revised UP: Alphabet FY26 to $195–205bn from $180–190bn plus "2027 rises
substantially" (07-29), Amazon +$20bn to $220bn (07-31), Meta capex ~doubled to ~$30bn
(07-30). (ii) **The "hyperscalers will abandon rented capacity" fear FAILED every available
test** (07-29, wt A, exhaustive 2026 8-K review): no cancellation or termination in ANY
CoreWeave 2026 filing, every pause on record RESUMED, released Microsoft capacity backfilled
by Google and Meta, Microsoft CFO 04-29 "constrained at least through 2026". (iii) Nine
independent bodies confirm the spending level with zero dissent (07-28) — counted as ONE
research sweep, not nine votes, per Codex's warning that source reliability is not causal
independence. Counter-evidence weighed and rejected as insufficient: compute-efficiency gains
(GPT-5.6 self-rewrote its serving kernels for −20% cost, 07-31, wt B self-reported) and
Chinese open-weight efficiency (07-24/07-28, wt B) point at demand but at lower weight.
**THE SPAN REQUIREMENT WAS NOT MET AND BEN OVERRODE IT** — reviews #1 and #2 are 23 days
apart, and the old wording contradicted itself (see the amended protocol in
evidence-ledger.md). Ben, verbatim: *"Let's do as you suggested and override the rules for
these changes."* Recorded as an override, NOT as the gate having been cleared. Codex reached
HOLD independently on the un-amended rule and named the same strongest counter-argument:
"widespread capex increases and repeated supply constraints make 8 defensible once the clock
matures." Cite: notes/2026-08-04-quarterly-review.md; journal 2026-08-04 REVIEW #2.

2026-09-21 (review #3 build, DRAFT for Ben's signature — no score change): **falsifier-(b)
numeric thresholds PROPOSED**, to be signed before Nvidia's November 10-Q: (i) the credit gauge's
weakest-minus-strongest borrower gap above 7.00 points at two consecutive month-ends (first
reading 9.20 on 2026-09-17); (ii) Nvidia's customer-support commitments (10-Q Note 10: $530.5bn
at 26 Jul 2026, $164.5bn of it customer support) rising again quarter on quarter; (iii) any
rented-capacity provider (CoreWeave, Nebius, IREN, TeraWulf class) failing to refinance a
maturity or issuing equity/converts to repay debt (CoreWeave's $3.7bn 2.875% convert plus a
13.2% at-the-market programme of 17 Sep is the first instance). Any ONE true = a written
de-risk recommendation on the AI-infrastructure basket, never a sale. Ten-week read of the
expressions (backtest 09-19): H1A intact (capex guides up again; Nvidia "twice as many chips
next year", 17 Sep). Cite: notes/2026-09-19-review-3-first-backtest.md §4.

---

## H2 — The bottleneck keeps migrating through the physical stack

**Claim.** As each constraint on AI buildout clears, the binding constraint moves to the
next physical input. Owning the *next* bottleneck early — not the current, priced one —
is the core alpha engine. Sequence so far: GPUs → advanced packaging → power generation →
grid equipment/cooling → **permitting, land, transformers, skilled labor, water (next?)**.

**Evidence (Jul 2026).** The *current* bottleneck names have massively re-rated: GE
Vernova ~+200% in a year (~$1,000, orders +71% organically, one quarter of electrification
DC orders exceeded all of 2025); Vertiv +105% YTD, fwd P/E >52, trading above consensus
target; Bloom Energy +279% YTD (+1,816% over 3y). Baker (June 2026): the bottleneck trade
"has run its course"; power relief visible 2027–28; **permitting and land approvals are
the remaining constraint markets don't clear quickly**. Aschenbrenner's fund disagrees in
part: still heavily long power/DC buildout (Bloom = top long).

**Sharpened claim (the actual edge).** Not "power/grid wins" — that is consensus and
expensive. The edge is: (a) identify the next constraint before it re-rates (candidates:
interconnection/permitting exposure, transformer capacity, gas turbine slots — backlogs
sold out for years, EPC labor, water rights, memory/HBM supply); (b) rotate OUT of solved
bottlenecks at peak multiples even when the story still sounds great — the story is
loudest at the top.

**Monitoring indicators.** Interconnection queue lengths (FERC/regional); transformer and
turbine lead times; PPA prices; equipment book-to-bill for GEV/ETN/VRT/PWR; data-center
vacancy and pre-leasing rates; utility capex plans; HBM/memory contract pricing.

**Falsifiers.** (a) Lead times and queues normalizing broadly (constraint solved and no
successor emerging → whole migration thesis done). (b) Bottleneck names de-rating on
*decelerating orders* rather than multiple compression (demand, not sentiment, breaking —
this is an H1 falsifier too). (c) INTERNALIZATION (added 2026-07-13, review #1.5, from
the 07-12 reply + external assessment): hyperscaler AI spending stays strong for two
quarters while the targeted supplier layer shows weaker organic orders, pricing, backlog
quality, or gross margins — the scarcity is real but the PLATFORM keeps the rent
(custom silicon, self-build, captive financing, procurement leverage), so the public
supplier layer never captures it; downgrade that H2 expression even though "the
bottleneck is real." Physical scarcity ≠ public-equity rent capture. Pre-registration
rule (same date): every next-bottleneck S0 card must state the predicted constraint,
the confirming observable, the refuting observable, the public instrument expected to
capture the rent, the TIME WINDOW, and the scarcity→earnings transmission — a
bottleneck named after the fact is a story, not a hypothesis.

**Conviction: 7/10 on the migration claim — a SINGLE score from 2026-08-04.**

The second score ("4/10 on the current consensus expression") is **DELETED, not moved.** It
measured whether a
PRICE was attractive, not whether we believed a claim, and it was set at 4 when the power and
equipment names were at highs. Those names then fell 25–38% from their late-June highs, and
INNIO (INIO, on-site gas engines for data centres) fell 17% on the day it printed a RECORD
order book (order intake +316% y/y, backlog +279%) — so the number sat still while its meaning
inverted underneath it. A conviction score says how strongly we believe a claim; whether a
price is attractive belongs in each name's own entry test, where it already lives (no-chase
ceilings, entry gates, valuation cards). Deleted at review #2 with Ben's explicit sign-off
("ok agreed"). Nothing about the migration claim changed and the 7 is unmoved.
Change log: 2026-07-06 initialized.
2026-07-06: reinforcing evidence logged (NOT yet scored) — Atreides (Baker) independently
ran the identical migration engine on the compute chain (AMD→Astera→optics→memory) with no
contact with SA LP's power-chain book (playbook §2 v1.2, P-14–P-16). Two independent
discoveries of the same mechanic from opposite worldviews strengthens the *migration-logic*
sub-thesis. Candidate bump 7→8 on migration logic — HELD for the next quarterly review
rather than bumped mid-session (convictions are scored at reviews, not on process insights).
2026-07-07: 11-name chain screen (memory makers → bonding → substrates → metrology → test →
toll-takers, 4 parallel agents, all live-verified): the memory/packaging layer is FULLY
re-rated — zero names pass the §6.1 entry gate; chain +70–150% YTD. Confirms BOTH H2 legs:
the bottleneck did migrate to memory/packaging (migration logic right), and the expression
is now consensus (the rotate-out leg right). Hybrid-bonding transition tracking AHEAD of
the 07-06 timeline (SK Hynix 12-hi hybrid validation + AMAT/Besi pilot order Apr'26;
Samsung weighing hybrid for HBM4). Only pre-consensus expression found: CAMT (entry gate = Q2 report ~Aug 11). Entry triggers for TSM/Disco/Besi/ASML/Onto filed as
watchlist rows. Scores unchanged; the 7→8 migration-logic bump remains HELD for the
quarterly review — now with two independent reinforcements (Atreides convergence 07-06,
layer-migration confirmation 07-07).
2026-07-12 (review #1): scores UNCHANGED (7 migration logic / 4 current expression).
The 7→8 migration-logic bump is formally HELD — five independent instances of the
mechanic (power chain 07-06 · compute chain 07-06 · memory/packaging 07-07 · chip-
internal 07-08 · inside-robotics 07-09) all cluster in ONE WEEK; the sustained-signal
test requires 2+ consecutive quarters or a multi-month trail. The span clock STARTS at
this review: if the signal persists to review #2 with no higher-weight counter-evidence,
the bump qualifies. Same-review reads: WATER downgraded as an S0 candidate layer
(US DCs ≈1/2,000th of agriculture's use; permitting/statutory scarcity stands — the NY
moratorium is a permitting event, not water scarcity); transformer-layer canary rolling
(HD Hyundai Electric ₩851,000, −5.3% since 07-07 designation, below 200d, Q2 order
print ~late Jul); CoWoS/packaging easing (supply-demand gap 20%→10% by end-2026,
TrendForce) narrows the next-layer watch to leading-edge 3nm logic — TSMC Jul 16 print
is the gate. Ledger trail: H2 rows 2026-07-06 → 2026-07-10.
2026-07-13 (review #1.5, Ben sign-off): falsifier-(c) INTERNALIZATION added and the S0
pre-registration rule adopted (constraint · confirmer · refuter · instrument · time
window · earnings transmission). "General law" framing retired in the playbook — the
migration mechanic is a research heuristic that has repeatedly appeared in capital
cycles, strong enough without the overclaim. Scores unchanged (7 logic / 4 current
expression; the 7→8 span clock from review #1 keeps running).
2026-08-04 (review #2, Ben's explicit sign-off): **the SECOND score is DELETED — see the
conviction line above. The migration score stays at 7 and the held 7→8 bump stays HELD.**
Why the bump was not taken even though Ben overrode the span rule for H1A and H5: those two
had pre-registered tests answer in one direction; this one has a genuine higher-weight
counter and a category problem. Four NEW instances since 07-13 take the mechanic to nine —
general-purpose server CPUs (07-16), grid interconnection formalised as a rationed resource
in three jurisdictions in one week (07-30: PJM requires new large loads to bring their own
generation by Jun-2027 or be curtailed first; Israel froze all new >8MW datacenter grid
applications ~140 days against 27GW pending; Ofgem proposed a £237,500–712,500/MW queue
fee), skilled building trades gating construction schedules (07-31), and optics — Lumentum's
CEO says it is undershipping indium-phosphide laser-chip demand by ~30% (08-04) and prepaid
AXT $87M for substrate capacity through 2031 (07-31). Against: Baker (tracked fund) declared
the mechanic priced — "finding the next bottleneck… that game is over" (07-15, wt B mag 3,
[AMENDMENT-CANDIDATE]) — and the frame reached cable television (07-16). Codex's objection,
accepted: nine instances found within weeks demonstrate RECURRENCE, not PERSISTENCE, which is
what the span test exists to distinguish. **NEW MECHANISM logged, not yet a falsifier
(08-04):** Fanuc (6954.T, Japanese industrial-robot and factory-automation leader) reportedly
had its worst one-day fall in about 40 years DESPITE June-quarter orders +37% and a RAISED
full-year profit forecast, attributed to procurement cost and component supply eating the
margin — the first market evidence that component scarcity is a MARGIN SQUEEZE on the machine
builders rather than only a rent for the component makers. Two covered names sit on the
wrong side of that read (Wärtsilä, KION). This is adjacent to falsifier-(c)
INTERNALIZATION but is not it: (c) says the platform keeps the rent, this says the scarcity
DESTROYS value at the assembling layer. Carried to review #3 as a candidate falsifier-(d).
Cite: notes/2026-08-04-quarterly-review.md.

2026-09-21 (review #3 build): the per-layer "is today's expression already priced?" reading
RETURNS as a SIZING input, not a belief score — a table on the timing page
(`book/timing_gauge.md`) per layer (power generation, grid equipment, packaging, memory, optics,
networking, rented compute): consensus temperature, price versus the layer's own history, and
the size band it implies for new money. Why: the 08-04 deletion removed the only warning the
engine had before the loud power/grid names topped in mid-August (GE Vernova −12%,
Vertiv −9%, Siemens Energy −15%, Powell −15%, Ciena −22% by 09-18). Migration score UNCHANGED
at 7. Cite: notes/2026-09-19-review-3-first-backtest.md §4.

---

## H3 — Value migrates from first-order compute to enablers (relative-value, NOT a hedge)

**Claim (made REVERSIBLE 2026-07-13, review #1.5, Ben sign-off).** Value accrues to the
layer with the most favorable expectations-adjusted return — and the book owns THAT
layer, whichever order it is. The standing prior (mega-cap first-order names carry the
highest embedded expectations; enablers out-compound from here) is a rebuttable reading
of today's prices, not a law: when valuation, monetization, and integration make a
first-order name the cheapest durable profit pool, the framework must permit owning it.
Expressed as pairs/relative positioning, not naked shorts of quality.

**Structural honesty required.** The enablers' revenue IS hyperscaler capex. Long
enablers / short hyperscalers is NOT a hedged position — in a capex pause, the high-beta,
thinner-moat enablers fall harder than cash-rich hyperscalers. This trade is a bet on
*value migration within a continuing cycle* (H1 intact). If H1 breaks, close H3
expressions immediately; do not "let the hedge work" — it won't.

**Evidence (Jul 2026).** Aschenbrenner is positioned exactly this way at scale (~$8.5B
notional puts on semis incl. ~$2B SMH / ~$1.6B NVDA, longs in power/DC buildout) — which
also means this expression is crowded and disclosed. Consensus check required before
copying: crowded shorts squeeze.

**Monitoring indicators.** Relative multiples (SMH vs enabler basket); hyperscaler FCF
after capex and buyback capacity; custom-silicon share vs NVDA (merchant vs captive);
enabler margin trajectory (are they gaining pricing power or giving it back?).

**Falsifiers.** (a) Chip backlogs/margins keep beating while enabler orders decelerate —
value NOT migrating. (b) Hyperscaler AI revenue inflects upward faster than capex —
first-order names were cheap all along. (Alphabet paradox: GOOGL is simultaneously a
"first-order overvalued" candidate AND the best AV asset (Waymo, 450k paid rides/week) and
a TPU owner. Do not let the hyperscaler rule exclude the strongest physical-AI assets —
judge each name on embedded expectations, not category.)

**Conviction: 5/10.** Genuinely contested — both influence funds are on opposite sides.
Size accordingly. Change log: 2026-07-06 initialized.
2026-07-07: expression recalibrated, score unchanged. Epoch models data: Nvidia's share
of disclosed frontier training runs is RISING (58%→83%, 2022→2026) — ASIC displacement
is not visible where it matters (disclosure bias noted: in-house TPU/Trainium runs
under-reported). The hyperscaler-short premium has already drained (MSFT ~20x fwd,
−18% YTD) and RELOCATED to accelerators/IP (ARM ~108x fwd, MRVL ~41x). Short-references
now point at perfection-priced accelerators, not clouds. H3 pairs must respect Nvidia's
staying power.
2026-07-12 (review #1): conviction UNCHANGED at 5. Evidence mixed by design (register
below now carries three believable voices, not two — Bridgewater column added with
sign-off): NVDA's frontier-training share still rising; the erosion vector is VERTICAL
(TPU/Trainium/MTIA self-supply), not merchant displacement; the app layer built on
rented models cannot hold price. No sustained one-direction signal. Ledger trail: H3
rows 2026-07-07 → 2026-07-10.
2026-07-13 (review #1.5, Ben sign-off): claim made REVERSIBLE (own the cheapest durable
profit pool, first-order included) and the playbook's "first-order names are never
fresh longs" deleted — the rule was more rigid than our own Alphabet-paradox note and
would exclude a dominant winner exactly when the expectations audit says buy. The
07-13 ledger row (MSFT AI revenue +123% vs capex +77% = falsifier-(b) possibly in
motion) is the live case for why reversibility matters. Score unchanged at 5.

2026-09-21 (review #3 build): claim RESTATED as a falsifiable pair test, in the second lab's
wording of 2026-08-04: *at current prices, do the selected enabler companies offer better
durable free-cash-flow returns than the selected first-order computing companies?* Named pairs,
measured quarterly on filed free cash flow against the price paid for it: TSMC / ASML / SK Hynix /
Lam Research (enablers) vs Microsoft / Alphabet / Meta / Amazon / Nvidia (first order); Vertiv /
GE Vernova / Bloom (power and grid enablers) vs the same first-order set. First reading (09-18,
ten weeks): first-order beat enablers (Meta +17%, AMD +14.5% vs the power/grid names −8% to
−22%). Falsifier: the enablers' free-cash-flow yield at purchase price failing to exceed the
first-order set's at two consecutive scheduled reviews → the enabler tilt is dropped. Score
UNCHANGED at 5. Cite: notes/2026-09-19-review-3-first-backtest.md §4.

---

## H4 — Physical AI (AV, robotics, space, defense autonomy) inflects commercially 2026–2029 — SPLIT into four sub-hypotheses 2026-07-13

**Claim — four separate bets, separately falsifiable, separately budgeted (split
2026-07-13, review #1.5, Ben sign-off: robotaxis, humanoids, defense autonomy and space
have different customers, regulation, adoption clocks, capital intensity, and unit
economics — success in one must never validate exposure to another):**
**H4a Defense autonomy:** drones/USVs, loitering munitions, counter-drone, autonomy
software, military sensing — pulled by structural rearmament (US + EU). Strongest
demand visibility of the four.
**H4b Robotaxi / AV:** autonomous ride networks cross into scaled commercial service.
**H4c Space:** the SpaceX-anchored complex becomes investable at scale post-IPO.
**H4d Humanoid robotics:** general-purpose robots cross from pilots to production.
Weakest evidence of the four; a research theme until customer unit economics exist —
humanoid expressions stay capped at recon size (0.5–1.5%) until a verified unsupervised
deployment exists.
Across all four: autonomy and robotics cross from pilots to revenue at scale within the
horizon; the market underestimates the *duration* of winners' growth. Supply chains and enabling
components are better risk/reward than headline names where the story is already loud —
but (reworded 2026-07-12, review #1) the enabler layer has PARTIALLY re-rated too
(MRCY +51%/75x fwd, DRS +31%; the listed robot-hardware complex +34–200% YTD on ~0–4%
robot revenue), so the edge narrows to the nodes that are genuinely scarce and not yet
priced: **dexterous-hand chokepoints (planetary roller screws, tactile sensing),
reliability (MTBF), and cost-curve ownership** — not "robot hardware" generically.
Avoid humanoid assemblers as longs. And robotics is **data-gated (and dexterous-
hardware-gated), NOT compute-gated** — largest manipulation runs use ~1% of frontier
compute; Tesla names hardware, not compute, as Optimus's blocker while holding
effectively unlimited compute — so H4 is expressed via data/hardware chokepoints and
deployers, never via compute proxies.
**AI-driven defense is a named pillar of H4** (added 2026-07-06): autonomous drones/USVs,
loitering munitions, counter-drone, autonomy software, and military sensing — pulled by a
structural rearmament + autonomy budget shift (US + EU). Same discipline as the rest of the
book: the primes and the loud names (PLTR, Rheinmetall) have largely re-rated; the edge is
in the enablers/sensors/software that haven't, and in post-IPO disgust on defense components.

**Evidence (Jul 2026).** Waymo ~450k paid rides/week (Dec 2025), expanding intl (Tokyo,
London) — but paused 4 cities over weather handling: real, but not solved. Tesla robotaxi
scaling (fleet passing Waymo's ~3k vehicles in months at current pace); Optimus production
start July 2026, public sales targeted end-2027. Humanoids (Figure, 1X, Apptronik,
Agility): paid pilots in manufacturing/logistics, but **no publicly verified unsupervised
deployment yet** — the zero-to-one is uncrossed. SpaceX IPO **filed ~this week** —
watershed: the anchor space asset becomes investable; expect the whole space complex to
re-rate around it (both directions: RKLB/ASTS may de-rate as SpaceX absorbs flows).

**Monitoring indicators.** Waymo/Tesla weekly rides and cities; robotaxi
unit economics disclosures; humanoid pilot→production conversions (verified unsupervised
deployments = the key event); robot component order flow (Harmonic Drive, Nabtesco,
Keyence, Fanuc, Teradyne); SpaceX IPO terms, valuation, and post-IPO capital behavior;
defense autonomy procurement budgets.

**Falsifiers.** Per sub-hypothesis (restructured 2026-07-13; the old (a)/(b)/(c) map to
H4b/H4d/H4c respectively). H4a defense: procurement stays pilot-based with no recurring
production orders for 4+ quarters, OR primes retain all integration economics (enabler
margins never expand). H4b robotaxi: expansion stalls on ECONOMICS (not regulation) for
4+ quarters, OR safety-intervention/remote-assist rates fail to fall city-over-city.
H4c space: launch cadence/pricing collapses margins across the sector post-SpaceX-IPO,
OR replacement capex proves to swamp satellite unit economics. H4d humanoid: pilots
churn without production orders through 2027, OR no verified unsupervised commercial
deployment exists by end-2027 (currently: orders exist with SEC-documented milestone
conditionality; deployments zero — moving, not met).

**Conviction: H4a defense 7/10 dir · 6/10 timing — H4b robotaxi 6/10 · 5/10 — H4c space 5/10 · 4/10 — H4d humanoid 4/10 · 3/10.**
Timing risk is the whole game here — size in the speculative bucket only, budgets per
sub-theme, humanoids recon-capped. Change log: 2026-07-06 initialized (as one combined
H4, 7 direction / 5 timing).
2026-07-12 (review #1): scores UNCHANGED (7 direction / 5 timing). Wording amendments
adopted with sign-off (claim narrowed above): "hardware-gated" → dexterous-hand nodes /
MTBF / cost (PI's own leadership rejects the general claim; Harmonic Drive humanoid
orders ≈4% of sales); "enablers not yet loud" refreshed (several already re-rated;
robot-hardware complex is concept-priced); "data-gated not compute-gated" made explicit.
Dashboard reads at review: Waymo STRENGTHENED (~500k paid rides/wk, 4-city simultaneous
launch 07-08); Tesla robotaxi WEAKENED vs narrative (~20 unsupervised cars, rides
undisclosed, ~3 orders of magnitude behind); falsifier-(b) MOVING NOT MET (zero verified
unsupervised humanoid deployments; production orders exist but now carry SEC-documented
milestone conditionality — Agility Form 425 — and a union blocker at Hyundai). New
public comps to watch: Unitree STAR debut (possibly late Jul) + AGLT SPAC — first
disclosed gross margins referee the private marks (Figure $39B, Apptronik $5.3B).
Ledger trail: H4 rows 2026-07-07 → 2026-07-09 + dashboard refresh
notes/2026-07-12-quarterly-review.md.
2026-07-13 (review #1.5, Ben sign-off): **H4 SPLIT into H4a–H4d** with separate
falsifiers and budgets. Sub-score initializations (from the split of the combined 7/5,
weighted by the review-#1 dashboard evidence): defense 7/6 (strongest demand
visibility: rearmament budgets, recurring EU/US programs); robotaxi 6/5 (Waymo ~500k
rides/wk strengthens; Tesla's ~20-car fleet and the camera-only NHTSA probe cap it);
space 5/4 (SpaceX now public, complex re-rating unresolved); humanoid 4/3 (zero
unsupervised deployments; orders conditional; concept-priced hardware complex) —
humanoids recon-capped until a verified unsupervised deployment. Success in one
sub-theme no longer validates another. Cite: notes/2026-07-13-merits-assessment-response.md.

2026-09-21 (review #3 build): H4a–H4d are SCREENS from this date. The sub-scores above stay as
recorded for continuity, but no capital budget attaches to any of them and no position is sized
on the theme until a unit-economics observable exists (a verified unsupervised humanoid
deployment; robotaxi cost per ride disclosed; a defence-autonomy production order with recurring
revenue). Any position that expresses them is held on its own
research note, not on the theme. Ten-week read: SpaceX, refused at $108, is +33%. Cite: notes/2026-09-19-review-3-first-backtest.md §4.

---

## H5 — Software durability under AI: a SCREEN, not a core hypothesis (reclassified 2026-07-13; short label retired)

**Claim (mechanism unchanged; ROLE reclassified 2026-07-13, review #1.5, Ben sign-off).**
Agents collapse the link between headcount and software seats / offshore labor hours,
structurally impairing per-seat SaaS and BPO/IT-services economics. As of 2026-07-13
this is a SCREENING FRAMEWORK, not one of the core capital-allocation hypotheses: it
sorts software into durable survivors (long candidates when mispriced) and fragile
losers (avoid; short only via the full surgical bar), using the §7 durability screen +
the pricing-model-transition test. Why reclassified: the engine's own record — zero
shortable names found (all crowded at 17–35% short interest), Bridgewater's exit
already public, the mechanism consensus at every bank — makes it a different kind of
tool from H1/H2: a lens on names, not a standing directional bet.

**Evidence — and a warning (Jul 2026).** This already partially played out: ~$2T wiped
off software in 12 months (the Jan-2026 "SaaSpocalypse" — CRM −42% over 12m, WDAY −33%,
NOW/SNOW roughly halved); shorts have already made ~$24B; Goldman calls the selloff
overdone. Staffing (Hays, Page, SThree) sold off on fear with **no clear evidence yet of
structural impairment**. The lazy version of this short is now late and crowded.

**Sharpened claim (surgical only).** Short only names meeting ALL of: per-seat or
per-hour revenue model; no proprietary data/workflow moat; task profile demonstrably
agent-replaceable today; deteriorating net revenue retention; and NOT already priced for
death. Separately: the crash created **long candidates** — software with real data moats
and usage-based pricing thrown out with the bathwater. Run both screens.

**Monitoring indicators.** Net revenue retention and seat-count disclosures; enterprise
agent-adoption surveys; BPO contract renewal pricing; IT-services headcount growth;
pricing-model shifts (seat → usage/outcome).

**Falsifiers.** (a) Seat counts stabilize across 2+ quarters at named short candidates.
(b) Agent adoption plateaus (reliability ceiling). (c) Impaired names successfully
re-price to usage/outcome models with retained revenue AND retained gross margin
(split adopted 2026-07-12, review #1, Ben sign-off: a revenue-only re-price that gives
the margin back is the pass-through trap H5 *predicts* — NOW Q1'26 is the type case,
subscription revenue +22% while non-GAAP subscription GM fell 84.5%→81.5% and GAAP GM
fell monotonically 8 quarters — not a refutation. Governance note: this edits a
falsifier that had begun to fire; the 07-07 FIVN/FRSH "partially active" reads are
therefore RESET to unresolved pending a gross-margin re-check under the new wording.)

**Conviction: 5/10 on the mechanism, applied as a screen — the generic-shorts sub-score is RETIRED with the short label (was 3/10; the held 3→2 span clock closes as moot).**
Change log: 2026-07-06 initialized.
2026-07-07: falsifier (c) PARTIALLY ACTIVE — FIVN/FRSH repriced to usage/AI with
stable-to-rising net revenue retention; the 07-06 five-agent fan-out found ZERO surgical
short candidates (every impaired name already at 17–35% short interest = shorting exit
liquidity); the edge rotated to the LONG leg (KVYO/TOST/ESTC/BRZE screen). CANDIDATE
cut: generic-shorts 3→2, HELD for the first quarterly review per discipline. Mechanism
score untouched.
2026-07-12 (review #1): scores UNCHANGED (6 mechanism / 3 generic shorts). The 3→2
generic-shorts cut is formally HELD — the same-direction evidence (07-07 → 07-10: zero
surgical candidates, Bridgewater's full enterprise-software liquidation, IT-services
de-rated 37–69% pricing disruption the financials don't yet show) spans one week, not
the required multi-month trail; span clock starts at this review. Falsifier-(c) SPLIT
adopted with sign-off (see falsifier box); FIVN/FRSH re-check under the new wording
queued for review #2. Dashboard: RLI 16.1% (re-arm bar ~30–40% — far), METR horizon
~17.4h (above the suite's 16h reliability ceiling; doubling ~4.3mo intact; workweek
re-arm rung not reached). Mechanism keeps confirming in audited filings (DUOL +190bps
then guided back — Jevons); the LONG leg is now a consensus idea — edge is
stock-selection only. Ledger trail: H5 rows 2026-07-07 → 2026-07-10.
2026-07-13 (review #1.5, Ben sign-off): **H5 RECLASSIFIED from core hypothesis to
screening framework; the short label and its 3/10 generic-shorts sub-score are
RETIRED** (the review-#1 span clock on the 3→2 cut closes as moot — the score no
longer exists rather than moving). Mechanism score 6/10 stays and still gates the
screen; existing H5-tagged watchlist rows (KVYO/TOST/ESTC/BRZE longs, INFY surgical
reference) keep their tags — the screen produced them and still governs them. Staged
in the 07-12 reply, endorsed by the external assessment, signed today.
2026-08-04 (review #2, Ben's explicit sign-off, span requirement OVERRIDDEN): **mechanism
6 → 5.** Evidence trail — two wt A mag-3 weakeners inside eight days, both at tests this
engine chose IN ADVANCE. (i) **The pre-registered test case answered NO.** RELX Legal printed
+10% UNDERLYING revenue growth (£900m→£959m) and +13% underlying operating profit at its H1
6-K of 07-23, full-year outlook REAFFIRMED — "underlying" being RELX's own
acquisition-excluding basis, exactly what the condition specified. The price leg of the alert
had already fired (+36.2% off the low vs +25% required) while the fundamental leg said no; a
rebound with the fundamentals intact is the opposite of the short's premise.
(ii) **The security-software version was priced, then refuted** (08-04): Palo Alto (PANW) and
CrowdStrike (CRWD) bottomed on the SAME DAY, 2026-02-24 — the signature of a sector thesis
being priced and unwound rather than two company stories — and are +138% and +124% since.
**There is no hard displacement evidence anywhere in this book: not one named enterprise
account.** Confirming evidence weighed and judged insufficient to hold the 6: an Indian
IT-services major named "AI deflation" on renewals with headcount down two consecutive
quarters (07-24, wt A mag 2), and the finding that the damage relocated to PRIVATE CREDIT
rather than public equity (07-28, wt A mag 3) — the latter confirms a mechanism this book has
no instrument to express, which argues for keeping the screen, not the score. **The screen
itself is NOT retired**; it still governs the existing long-leg rows (KVYO/TOST/ESTC/BRZE)
and the surgical-short bar. **THE SPAN REQUIREMENT WAS NOT MET AND BEN OVERRODE IT** — same
verbatim instruction as H1A above. Codex reached HOLD independently on the un-amended rule
and named the same counter: RELX plus PANW/CRWD without a named displaced customer
"support 5". Falsifier-(c) FIVN/FRSH re-check queued at review #1 for review #2 is STILL NOT
DONE and carries to review #3. Cite: notes/2026-08-04-quarterly-review.md.

2026-09-21 (review #3 build): confirmed as a screen; any remaining capital-budget language is
retired. Ten-week read of the expressions: the "AI-fear discount" long idea (Klaviyo, KVYO) −15.7%
on business facts; the security-software long leg
(CrowdStrike +28.5%, Fortinet +8.9%) won; Salesforce +7.6%. Mechanism score UNCHANGED at 5.
Cite: notes/2026-09-19-review-3-first-backtest.md §4.

---

## Opportunistic sleeve (≤10% of portfolio, same journaling discipline)

Event-driven and special situations adjacent to the thesis: the SpaceX IPO; forced-seller
dislocations in thesis names; post-crash quality software (H5 long leg). Scope note
(2026-07-07): this book trades traditional markets only.

---

## Live disagreement register (update every review)

| Question | Aschenbrenner (via 13F) | Baker (public + 13F) | Bridgewater (13F + public) | Resolution rule |
|---|---|---|---|---|
| Bottleneck trade from here | Still long power/DC buildout | "Nearing its end" — a ROTATION call, not an exit (Jun 16, refined vs the blunter press version; reaffirmed Jun 26) | Long first-order compute AT SCALE: AI silicon 10.4%→18.3% of book, TSM new #1 (Q1'26 13F) | Underwrite name-by-name on embedded expectations; prefer next-bottleneck over current |
| Mega-cap semis | ~$8.5B notional puts | Wafer discipline prevents bubble; TSMC central; largest single position = 16.2% notional QQQ put (hedged, not all-clear) | Third voice AGAINST semi-shorts (KKT: "no one's hurt Nvidia"); no put wall | Express H3 small; pairs not naked shorts |
| What's scarce next | (undisclosed) | Permitting, land | (systematic macro fund — single-name reads weak; SLEEVE rotation is the signal) | Research permitting/land winners — least priced |
| Enterprise software (H5) | (no disclosed position) | (no public call) | LIQUIDATED: 5.5%→0.04% of book, CRM was #5 holding (Q1'26) | Mechanism confirmed AND crowded — long-leg selection only, no new shorts |

*Bridgewater column added 2026-07-12 (review #1, sign-off). Weight its sleeve rotations,
never its single names (systematic fund; Q1'26 filed 05-15, zero putCall rows).*

When believable people disagree, the Dalio rule applies: reduce size, prefer structures
that profit in both worlds, or do nothing. Doing nothing is a position.

**Filings lead words (playbook §10, P-20).** When a manager's public statement and their
disclosed 13F disagree, weight the FILING. Baker's Q1'26 filing rotated optics→interconnect
a month before his public "trade is over" call. The live power/semis disagreement is now a
tracked constraint-fork with pre-committed sizing in `state/phase-map.md` (FORK-1) — resolve
it on the observables named there, updated at the Q2'26 13Fs (~Aug 14).

---

## Sources (snapshot basis, 2026-07-06)

- SA LP Q1'26 13F: 13f.info/13f/000204572426000008 (puts disclosure via Yahoo Finance,
  May 2026); Insider Monkey fund page
- Baker: Invest Like the Best "Watts and Wafers" (2026); "bottleneck trade run its
  course" coverage (Jun 16, 2026); TBPN interview on SpaceX IPO/token path (Jun 15, 2026)
- Capex: hyperscaler 2026 guidance aggregation (~$725B, +77% YoY); Goldman $5.3T 25–30
- Power names: GEV/VRT/BE price and orders data (May–Jun 2026 coverage)
- SaaSpocalypse: CNBC/Forbes (Feb 2026), ~$2T drawdown, short profits ~$24B
- Physical AI: TechCrunch Mobility (May 2026), ARK robotaxi notes, CES 2026 physical-AI
  coverage; SpaceX IPO filing reports (Jul 2026)
