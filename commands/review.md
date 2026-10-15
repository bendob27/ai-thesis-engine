---
description: Quarterly portfolio review — performance, hypothesis health, GATED thesis amendments, rebalance
---
Use the ai-thesis skill (quarterly-review mode). $ARGUMENTS

**This is the ONLY command that may amend `research/thesis.md` or `research/playbook.md`.**
Follow the quarterly-review template in `research/frameworks.md` fully:

- Performance vs QQQ / SMH / equal-weight universe basket (all live data); attribution.
- Hypothesis health dashboard (indicator readings per H1–H5).
- **Thesis-amendment gate — the whole point of the system.** Start at
  `book/evidence_index.md` — it is rebuilt daily and lists every ledger entry under every
  hypothesis it names, INCLUDING entries physically filed in the Playbook/Regime sections
  (between 07-24 and 08-04 that misfiling ran 122-to-1 and review #2 nearly missed twelve
  days of evidence; adopted 08-04, Ben's yes). Then read
  `research/evidence-ledger.md` in full and run the sustained-signal test per hypothesis: a
  pre-committed falsifier met across **2+ consecutive quarters**, OR a **persistent
  believability-weighted directional signal** over multiple months/quarters (a higher-weight
  A/13F row is not outvoted by lower-weight C/media rows). For any hypothesis that clears the
  bar, show the **full dated ledger trail** and a proposed conviction / playbook-threshold
  change, and get my **EXPLICIT sign-off BEFORE** writing it into the file's Change Log. No
  sustained signal → no change, however loud the quarter. Surface every `[FALSIFIER-CANDIDATE]`
  loudly for my decision. Append a resolution note to the ledger for whatever is decided.
- Journal scoring: grade every resolvable call (right/wrong × right-reason/wrong-reason).
- Influence 13F refresh (`data/fetch_13f.py`) and disagreement-register update.
- Regime check (capex second derivative, rates, Taiwan/export controls, neocloud credit).
- **Market-temperature checklist** (adopted 2026-07-23 from the Oaktree/Marks study; the
  frameworks-§3 codification queues for the post-freeze review): run
  `data/credit_temperature.py` (a meter, never a gate) and answer ten qualitative questions,
  one line each: (1) lenders eager or reticent? (2) new-deal terms loose or tight — covenants,
  pay-in-kind interest, spreads vs history? (3) capital abundant or scarce for WEAK borrowers?
  (4) sellers eager or absent — any forced sellers visible? (5) crowds chasing or fleeing our
  themes? (6) has the recent market rewarded caution or aggression? (7) media tone euphoric or
  fearful? (8) IPO/new-issue window wide open or shut? (9) our own watchlist: more names at
  silly prices or at disgust prices? (10) Oaktree deployment pace + any new distressed-fund
  raise (read the latest Brookfield quarterly — deployment ACCELERATION at the reference
  distressed buyer is the strongest bottom marker they emit; 2008 precedent $400M/week).
- **State the offense-defense dial** (adopted 2026-07-23, Marks INVESTCON-style label — it
  changes no sizing rule by itself): one sentence per review — "the book's stance is N on a
  6-to-1 scale (6 = stop buying, 1 = go short), because X" — derived from the sleeves, the
  drawdown ladder, and the temperature checklist above; track N review-over-review.
- Playbook review sweep per SKILL.md Mode 3: watchlist trigger sweep, §8 kill-first sweep,
  §2 phase-map refresh + §2.4 scouting loop, §7 exit/kill sweep, §9 hedge-dial review.
- Concrete rebalance proposal with risk-rule checks — "do nothing" is a scored option.

Save the full review to `.claude/notes/YYYY-MM-DD-quarterly-review.md` and update CLAUDE.md
"What to do next".

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
