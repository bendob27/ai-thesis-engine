#!/usr/bin/env python3
"""The distinct prices a card implies, computed and named (brief §9.1, 2026-08-12).

WHY THIS EXISTS. In one day the same confusion produced three separate false
alarms, each time between two of OUR OWN numbers:

  Constellation  our card said $272.34, an independent lab said $203.47, and it
                 read as a 34% dispute. Discount the card's figure to today and
                 it gives ~$206. The labs agreed to 1.3%.
  Vistra         the rebuilt card says $177.30 and the ceiling on file says
                 $123.32 — apparently 44% apart. Discounted like for like the
                 gap is 9%, and both say the same thing about the price.
  Adobe          the ranking said +1.2%/yr and the card implied +3.7%/yr from
                 identical inputs, because one averages returns and the other
                 returns the average.

None of those was an error in anybody's analysis. Every one was a value at a
FUTURE date being compared with a price TODAY, or an average taken in a
different place. The brief's answer is not "be careful": it is to compute the
distinct prices and give each one a name, so the comparison cannot be made
wrongly by accident.

For each card this computes, all from the card's own scenarios and horizon:

  value_at_horizon        the probability-weighted value at the card's own date
  index_equivalent_today  the most payable NOW to merely match the index over
                          that horizon — value_at_horizon / (1+hurdle)^years.
                          THIS is the number to compare with a price, and the
                          number a buy cap should be.
  target_return_today     the same, at Ben's absolute return targets, which he
                          SET on 2026-08-13: 10% established quality, 12%
                          default, 15% speculative. Read from config/policy.json
                          via data/policy.py — never hardcoded here.
  stress_price_today      index-equivalent computed with the downside case
                          weighted at 40% — the brief's severe stress run.
  market_implied_return   what the CURRENT price implies you earn if the card's
                          value is right; the reverse of the above.

Run: python3 data/price_concepts.py [--replay]   writes book/shadow/price_concepts.csv
"""
import argparse
import csv
import re
import datetime as dt
import glob
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import policy
ROOT = os.environ.get("AI_THESIS_ROOT") or os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "book")
SHADOW = os.path.join(BOOK, "shadow")
# One source for every rate: config/policy.json, read through data/policy.py.
HURDLE = policy.PASSIVE_BENCHMARK
# The three bars Ben approved 2026-08-13. This used to read (0.10, 0.15, 0.20)
# and be labelled illustration; 20% was never a target and 12% was missing.
SENSITIVITY = (policy.ESTABLISHED_QUALITY_TARGET, policy.DEFAULT_TARGET,
               policy.SPECULATIVE_TARGET)
STRESS_DOWNSIDE = 0.40  # brief §9.5's heaviest standardized stress run


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def weighted(scenarios, downside_weight=None):
    """Probability-weighted value. With downside_weight set, the worst case is
    re-weighted to it and the rest scaled down proportionally — the stress run."""
    if not isinstance(scenarios, list) or not scenarios:
        return None
    vals = [(num(s.get("probability")), num(s.get("value_per_share")))
            for s in scenarios if isinstance(s, dict)]
    if any(p is None or v is None for p, v in vals):
        return None
    if downside_weight is None:
        return sum(p * v for p, v in vals)
    worst = min(vals, key=lambda pv: pv[1])
    rest = [pv for pv in vals if pv is not worst]
    rest_total = sum(p for p, _ in rest)
    if rest_total <= 0:
        return None
    scale = (1.0 - downside_weight) / rest_total
    return worst[1] * downside_weight + sum(p * scale * v for p, v in rest)


PV_RE = re.compile(r"present value|discounted (?:back|to today)|pv per share|"
                   r"today'?s value|value today", re.I)
FV_RE = re.compile(r"value at (?:the )?(?:horizon|end)|terminal value|exit value|"
                   r"by fy20\d\d|at fy20\d\d|end-20\d\d", re.I)


def value_basis(card):
    """Is pw_value a value TODAY or a value AT THE HORIZON? — and refuse to guess.

    Found 2026-08-12, and it is the deepest instance of the error this whole file
    exists to prevent, sitting inside this file. `pw_value` is not one concept
    across the 105 rebuilt cards: some analysts wrote a present value already
    discounted at their own required return, others wrote the value they expect
    the shares to fetch at the horizon. Discounting BOTH to get "the most payable
    today" double-discounts the first group and makes those companies look far
    cheaper than their own card says.

    A card may state its basis in a `value_basis` field. Failing that, its prose
    is read — and where the prose says neither or both, the answer is UNKNOWN and
    no index-equivalent price is computed at all. A blank that says "the card does
    not say what its number means" is worth more than a number that is wrong for
    a fifth of the book."""
    stated = str(card.get("value_basis") or "").strip().lower()
    if stated in ("present", "today", "pv"):
        return "present", "stated on the card"
    if stated in ("at_horizon", "horizon", "future", "terminal"):
        return "at_horizon", "stated on the card"
    blob = json.dumps(card)
    pv, fv = bool(PV_RE.search(blob)), bool(FV_RE.search(blob))
    if pv and not fv:
        return "present", "read from the card's own wording"
    if fv and not pv:
        return "at_horizon", "read from the card's own wording"
    return "unknown", ("the card does not say, or says both — no index-equivalent "
                       "price is computed")


def discount_rate(card):
    """The rate a PRESENT-value card was discounted at — stated, never guessed.

    Found 2026-08-12, and it is the same error one layer deeper. A card whose
    value is already a present value was discounted at its OWN required return
    r. That changes two things, both of which were being got wrong:

      the return a buyer earns   is (1+r)·(value/price)^(1/T) − 1, NOT
                                 (value/price)^(1/T) − 1. A card whose value
                                 equals today's price earns r — around 10% —
                                 and the old formula reported 0%.
      the most payable today     to earn merely the index is HIGHER than the
                                 card's value, not equal to it: paying the
                                 card's value earns r, and r is well above the
                                 index hurdle.

    So a present-value card is useless for either purpose unless r is known.
    A regex over the card finds A rate, but these cards carry sensitivity
    tables listing four or five, and the most frequent is not the one used —
    checked on 2026-08-12 against DASH (10%, mode said 8%), Ecolab (8.5%, mode
    said 7%) and Comfort Systems (10.5%, mode said 9%). So the rate is read
    ONLY from a field an analyst wrote deliberately. Absent that, this refuses,
    and the card still yields the one honest comparison that needs no rate:
    price against the card's own value."""
    for k in ("discount_rate", "cost_of_equity", "required_return"):
        r = num(card.get(k))
        if r is not None:
            r = r / 100.0 if r > 1.0 else r
            if 0.02 <= r <= 0.30:
                return r, "stated on the card in `%s`" % k
    return None, ("the card does not state, in a field, the rate its present value "
                  "was discounted at — so neither a buy price nor a return can be "
                  "computed from it")


def concepts(card):
    hz = num(card.get("horizon_years"))
    px = num(card.get("price_at_calc"))
    scen = card.get("scenarios")
    pw = num(card.get("pw_value"))
    if pw is None and scen:
        pw = weighted(scen)
    if not hz or hz <= 0 or pw is None:
        return None
    basis, basis_why = value_basis(card)
    rate, rate_why = discount_rate(card) if basis == "present" else (None, "n/a")
    out = {
        "horizon_years": hz,
        "price_used": px,
        "value_basis": basis,
        "value_basis_source": basis_why,
        # named for what it IS on this card, not for what we wish it were
        "pw_value_as_written": round(pw, 2),
        "card_discount_rate": rate,
        "card_discount_rate_source": rate_why,
    }
    blank = ("index_equivalent_today", "stress_price_today",
             "expected_return_annual", "premium_to_index_equivalent")

    # The one comparison that is always honest for a present-value card and
    # never honest for an at-horizon one: today's price against the card's
    # own number. It needs no rate and no discounting.
    out["premium_to_card_value"] = (round(px / pw - 1.0, 4)
                                    if basis == "present" and px and pw else None)

    if basis == "unknown" or (basis == "present" and rate is None):
        for k in blank:
            out[k] = None
        for t in SENSITIVITY:
            out["target_%d_today" % int(t * 100)] = None
        return out

    # Put every card on ONE footing — a value at its own horizon — then discount
    # once. This is the only place the two conventions are allowed to meet.
    def at_horizon(v):
        return v * (1 + rate) ** hz if basis == "present" else v

    out["index_equivalent_today"] = round(at_horizon(pw) / (1 + HURDLE) ** hz, 2)
    for t in SENSITIVITY:
        out["target_%d_today" % int(t * 100)] = round(at_horizon(pw) / (1 + t) ** hz, 2)
    stressed = weighted(scen, STRESS_DOWNSIDE) if scen else None
    out["stress_price_today"] = (round(at_horizon(stressed) / (1 + HURDLE) ** hz, 2)
                                 if stressed is not None else None)
    if px and px > 0:
        out["expected_return_annual"] = round(
            (at_horizon(pw) / px) ** (1.0 / hz) - 1.0, 4)
        out["premium_to_index_equivalent"] = round(
            px / out["index_equivalent_today"] - 1.0, 4)
    return out


def selftest():
    """The invariant: two cards describing the SAME company in the two different
    conventions must produce the SAME buy price and the SAME expected return.

    This is the check that would have caught every one of the three false alarms
    in this file's opening paragraph, and the deeper one found on 2026-08-12.
    Written as a test rather than as a warning because a warning has failed here
    four times."""
    hz, r, px = 5.0, 0.11, 100.0
    horizon_value = 250.0
    present_value = horizon_value / (1 + r) ** hz          # the same company
    a = concepts({"horizon_years": hz, "price_at_calc": px, "value_basis": "at_horizon",
                  "pw_value": horizon_value})
    b = concepts({"horizon_years": hz, "price_at_calc": px, "value_basis": "present",
                  "discount_rate": r, "pw_value": present_value})
    fails = []
    for k in ("index_equivalent_today", "expected_return_annual",
              "premium_to_index_equivalent"):
        if abs(a[k] - b[k]) > 0.01:
            fails.append("%s: at-horizon card says %s, present-value card says %s"
                         % (k, a[k], b[k]))
    # a present-value card whose value equals the price earns the card's own rate,
    # never zero -- the specific defect fixed on 2026-08-12
    c = concepts({"horizon_years": hz, "price_at_calc": px, "value_basis": "present",
                  "discount_rate": r, "pw_value": px})
    if abs(c["expected_return_annual"] - r) > 0.001:
        fails.append("a present value equal to the price must earn the card's own "
                     "%.1f%%, not %.1f%%" % (r * 100, c["expected_return_annual"] * 100))
    # and it must REFUSE when the rate is missing rather than assume one
    d = concepts({"horizon_years": hz, "price_at_calc": px, "value_basis": "present",
                  "pw_value": px})
    if d["index_equivalent_today"] is not None or d["expected_return_annual"] is not None:
        fails.append("a present-value card with no stated rate must produce no buy "
                     "price and no return, and it produced one")
    if d["premium_to_card_value"] is None:
        fails.append("a present-value card with no stated rate must still report the "
                     "price against its own value, which needs no rate")
    for f in fails:
        print("FAIL " + f)
    print("selftest: %s" % ("PASS — the two conventions agree" if not fails
                            else "%d FAILURES" % len(fails)))
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--replay", action="store_true",
                    help="read the rebuilt cards in book/shadow/replay/ rather than "
                         "the live store")
    ap.add_argument("--selftest", action="store_true",
                    help="prove the two value conventions land on the same answer")
    a = ap.parse_args()
    if a.selftest:
        return selftest()

    cards = {}
    if a.replay:
        for p in glob.glob(os.path.join(SHADOW, "replay", "*.primary.json")):
            tk = os.path.basename(p).replace(".primary.json", "")
            try:
                cards[tk] = json.load(open(p, encoding="utf-8"))
            except ValueError:
                pass
    else:
        d = json.load(open(os.path.join(BOOK, "valuations.json"), encoding="utf-8"))
        cards = {k: v for k, v in d.items()
                 if k != "_meta" and isinstance(v, dict) and v.get("status") == "live"}

    rows, skipped = [], []
    for tk, c in sorted(cards.items()):
        got = concepts(c)
        if got is None:
            skipped.append(tk)
            continue
        rows.append(dict(ticker=tk, ccy=c.get("ccy", ""), **got))

    os.makedirs(SHADOW, exist_ok=True)
    name = "price_concepts_replay.csv" if a.replay else "price_concepts.csv"
    with open(os.path.join(SHADOW, name), "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    print("%d cards priced · %d skipped (no horizon or no value): %s"
          % (len(rows), len(skipped), ", ".join(skipped) or "none"))
    print("wrote book/shadow/%s" % name)
    print("\nThe number to compare with a price is index_equivalent_today, NEVER "
          "value_at_horizon — the second is a figure for a date years away.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
