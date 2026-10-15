#!/usr/bin/env python3
"""The most we may pay for a company today, computed rather than chosen.

WHY THIS EXISTS (2026-08-01, Ben's question: ceilings and limits for every name,
or only some?). The engine had 15 "no-chase ceilings" across 156 names and the
measured record was damning: 7 of the 15 were more than a fortnight old and had
never been revisited, 4 dated to a single day 24 days earlier, 2 were written
BELOW the market at birth, and 4 were set EQUAL to the order limit -- so every
limit raise mechanically dragged the ceiling up behind it. One name's ceiling
rose four times in about fifteen hours. Not one of 26 order limits was ever
derived from a valuation.

THE TWO OBJECTS, WHICH THE OLD SYSTEM CONFLATED. This file computes the FIRST
and never touches the second.

  1. THE BUY CAP -- the most this company is worth paying today, given what we
     think it will be worth and what the alternative earns. It belongs to the
     COMPANY and to a dated valuation. It moves only when the valuation moves.
  2. THE ORDER LIMIT -- the price typed on a specific order, derived from the
     live quote and the spread at the moment of placing. It belongs to the ORDER.

The rules that follow from keeping them apart:
  * An order limit may never raise a buy cap.
  * A price move may never raise a buy cap. Only new evidence does.
  * An order may never be placed above a valid cap, and never on a stale one.
  * A cap below the market is not a mistake. It means "do not buy", which is a
    real answer and the one the record kept converting into a chase.

HOW THE CAP IS COMPUTED. Not picked off a scale of opinions. The cap is the
highest price at which the probability-weighted outcome still beats simply
holding the index, after a 26% tax on gains:

    cap = (probability-weighted value) / (index multiple over the same horizon)

Worked: a company whose weighted value in ten years is EUR 100 a share, against
an index compounding 6.5% a year over the same ten years (1.88x), is worth paying
at most EUR 53.27 today. Above that the index is the better bet and the position
should not exist.

WHY NOT EVERY NAME. A cap on a company nobody is about to buy is a number nobody
maintains -- which is exactly how 7 of 15 went stale. Caps are computed for names
we OWN or are ACTIVELY considering. A parked name gets one when it is promoted,
before any order can be approved, never after.

Usage:
    python3 data/buy_cap.py                 # compute for owned + actionable
    python3 data/buy_cap.py --all-live      # every name with a live valuation
    python3 data/buy_cap.py --check TICKER 8.50   # may I pay 8.50 for TICKER?
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import policy
SKILL = os.path.dirname(HERE)
BOOK = os.path.join(SKILL, "book")

VALUATIONS = os.path.join(BOOK, "valuations.json")
WATCHLIST = os.path.join(BOOK, "watchlist.csv")
PORTFOLIO = os.path.join(BOOK, "portfolio.csv")
OUT_CSV = os.path.join(BOOK, "buy_caps.csv")
OUT_MD = os.path.join(BOOK, "buy_caps.md")

# The alternative the money always has: what a broad index fund is expected to
# return, before tax, net of the fund's own costs. Every position has to beat it
# to deserve to exist. Stated here once so it can be argued with.
#
# CHANGED 2026-08-03 from 9.0 to 6.5 on Ben's instruction, after the first real
# study of this number. His words: "the hurdle rate should be more accurate not
# purposely harder." What the study found, all computed rather than remembered:
#   * 9.0% was ROUGHLY THE MEDIAN historical outcome, not a conservative one --
#     59% of all 20-year windows returned less than 9.0%, and the median 20-year
#     result is 8.6%.
#   * Worse, 9.0% is unreachable from today's starting valuations. Building it up
#     from the current earnings yield, growth and shareholder yield, and generously
#     assuming NO multiple compression for twelve years, the arithmetic tops out
#     at 7.6%. The old number sat above the ceiling of its own build-up.
#   * Ben's original objection was also right on its own terms: to NET 9% a year
#     after a 26% tax, holding throughout and paying once at the end, you would
#     need 10.87% gross over twelve years (11.03% over ten, 10.66% over fifteen).
# The replacement is built, not chosen: 7.0% gross expected return minus 46 basis
# points of fund-level cost = 6.5%, stated BEFORE tax because the tax cancels on
# both sides (see index_multiple below). Defensible range 6.0-7.5%.
#
# KNOW WHICH WAY THIS CUTS. A lower hurdle is a SMALLER divisor, so every cap goes
# UP and the test gets EASIER to pass. It is not a tightening. Measured effect at
# adoption: +3.5% on a 1.5-year card, +4.7% at two years, +12.3% at five, and
# +26.1% on a ten-year destination case -- the loosening is largest exactly where
# the evidence is thinnest. Ben was shown that and chose accuracy over a carve-out.
#
# THE BIGGEST UNCERTAINTY, named rather than buried: whether today's multiple is
# justified by permanently faster growth. That question is worth 400-600 basis
# points in either direction, against 20-70 for fund costs, currency and tax
# treatment combined. And a second-order problem specific to this book -- the
# index is now ~40% one AI-linked theme, so the hurdle and the portfolio are
# substantially the same bet, and the hurdle falls exactly when the thesis is wrong.
INDEX_RETURN_PCT = policy.PASSIVE_BENCHMARK * 100  # config/policy.json
TAX_RATE = 0.26          # flat on gains, no long-term discount
# NOTE: there is deliberately no DEFAULT_HORIZON_YEARS constant. One existed
# (= 3), was never referenced by any code path, and stated a default that was
# wrong by a factor of two -- the real fallback is 1.5 years and it lives in
# horizon_years() below, next to the logic that uses it. Removed 2026-08-03.

# A cap is executable for this long. Short on purpose: the measured failure was
# ceilings surviving unexamined for a fortnight in a sector that reprices weekly.
# It costs nothing while we are not buying -- an expired cap simply blocks a new
# purchase until someone re-reads the valuation, which is exactly the moment a
# re-read is worth doing.
CAP_VALID_DAYS = 7

# A price move this large voids the cap early, in either direction. Not a
# momentum rule: it says the facts behind the valuation deserve another look
# before anyone acts on a number computed at a very different price.
CAP_VOID_MOVE_PCT = 15.0

csv.field_size_limit(10 ** 9)


def num(v):
    if isinstance(v, (int, float)):
        return float(v)
    if isinstance(v, str):
        m = re.search(r"-?\d[\d,]*\.?\d*", v.replace(",", ""))
        if m:
            try:
                return float(m.group())
            except ValueError:
                return None
    return None


def parse_date(s):
    m = re.search(r"(20\d{2})-(\d{2})-(\d{2})", str(s or ""))
    if not m:
        return None
    try:
        return dt.date(*(int(g) for g in m.groups()))
    except ValueError:
        return None


def index_multiple(years):
    """What the money makes doing nothing clever over `years`.

    BEFORE TAX, DELIBERATELY -- corrected 2026-08-03 (Ben approved).

    THE BUG THIS FIXES. This returned the AFTER-tax index multiple, while the
    value it gets divided into (the probability-weighted price target) is a
    PRE-tax number. So the cap compared a pre-tax stock return against an
    after-tax index return and every cap came out ~10% too HIGH at a five-year
    horizon, ~3% at two years. Caps gate orders in ibkr_order.py, so the effect
    was permissive: it allowed a price the honest comparison rejects. On the
    2026-08-02 big-four cards it flipped Microsoft from fail to pass.

    WHY THE TAX CANCELS. Buy at C, worth V at the horizon, both the stock and the
    index taxed at the same rate t on the gain:

        stock, after tax, per unit invested:  [C + (V - C)(1 - t)] / C
                                           =  1 + (V/C - 1)(1 - t)
        index, after tax, per unit invested:  1 + (gross - 1)(1 - t)

    Set them equal and (1 - t) divides out of both sides:

        V/C - 1 = gross - 1   ->   V/C = gross   ->   C = V / gross

    So the correct divisor is the GROSS index multiple. A flat 26% tax applies
    to both sides of the comparison at the same rate with no holding-period
    discount, so it genuinely cancels. TAX_RATE is kept in this file because the
    valuation cards and the expected-return reporting still use it; it just has
    no place in THIS divisor.

    It would stop cancelling if the two sides were ever taxed differently -- for
    instance an ETF whose gains are taxed as investment income against a share
    whose losses can offset gains. If that asymmetry is ever modelled here, this
    function has to grow a second argument, not quietly regain a tax term.
    """
    return (1 + INDEX_RETURN_PCT / 100.0) ** years


def weighted_value(card):
    """The probability-weighted value per share, and how we got it.

    Prefers an explicitly weighted number already on the card. Falls back to
    computing one from the scenarios. Refuses to invent one."""
    for f in ("probability_weighted", "pw_value"):
        v = num(card.get(f))
        if v:
            return v, f"the card's own probability-weighted value ({f})"

    if card.get("primary_model") or card.get("independent_model"):
        return None, ("two model values await the deciding read — no house number to "
                      "cap from, and the two are never averaged")

    sc = card.get("scenarios")
    if isinstance(sc, list):
        tot = wsum = 0.0
        for leg in sc:
            if not isinstance(leg, dict):
                continue
            p, px = num(leg.get("probability")), num(leg.get("value_per_share"))
            if p and px:
                tot += p
                wsum += p * px
        if tot > 0.5:
            return wsum / tot, ("computed from the card's own scenarios and "
                                "their stated probabilities")
    return None, "the card carries no probability-weighted value and no scenarios"


def horizon_years(card, value_field):
    """The horizon must belong to the VALUE being discounted, never to the card.

    Caught before this file was first used, on a name in the book that carries
    both a 12-18 month weighted value and a ten-year destination case. Taking the
    horizon from the card picked ten years and then discounted the SHORT value by
    a TEN-YEAR index return -- which made the most we may pay look 46% below the
    price instead of roughly at it. Discounting a value by a period it does not
    span is not conservatism, it is a units error.

    So the horizon comes from whichever number we actually used.

    ADDED 2026-08-03. A card may now DECLARE its own horizon, and if it does that
    declaration wins. Why: the four big-four cards written 2026-08-02 carry a
    FIVE-YEAR weighted value in the same `pw_value` field that every older card
    uses for a 12-18 month one. Same field name, two different horizons -- the
    "two objects sharing one shape" failure this engine keeps hitting. Silently
    discounting a 2031 value by eighteen months of index return inflated Meta's
    cap from $485 to $656, which is ABOVE its price, turning a fail into a pass.

    RETIRED 2026-08-11 (upgrade brief 7.3): the 1.5-year fallback for cards with
    no declared horizon. It existed for the pre-08-03 card generation, but a
    default horizon is a guessed horizon, and this exact silence inflated Meta's
    cap from $485 to $656 when a five-year value met the default. A card with no
    numeric `horizon_years` now gets NO cap and a stated reason; the validator
    (valuation_validate.py) flags the card, and the replay owes it a rebuild."""
    if value_field == "destination":
        return 10, "the destination case is a ten-year claim"
    declared = num(card.get("horizon_years"))
    if declared and declared > 0:
        return declared, (f"the card declares its weighted value as a {declared:g}-year "
                          f"figure, so it is compared against {declared:g} years of the index")
    return None, ("the card states no horizon for its weighted value — the old 1.5-year "
                  "default is retired (a defaulted horizon once flipped Meta's verdict), "
                  "so no cap until the card says what period its value spans")


def universe(all_live):
    """Which names get a cap. Owned plus actionable, unless --all-live."""
    want, why = {}, {}
    if os.path.exists(PORTFOLIO):
        for r in csv.DictReader(open(PORTFOLIO, encoding="utf-8")):
            t = (r.get("ticker") or "").strip()
            if t:
                want[t] = "owned"
    if os.path.exists(WATCHLIST):
        for r in csv.DictReader(open(WATCHLIST, encoding="utf-8")):
            t = (r.get("ticker") or "").strip()
            dec = (r.get("decision") or "").strip().upper()
            if not t:
                continue
            if dec in ("OWNED", "BUY APPROVED", "ORDER PLACED", "BUY IF"):
                want.setdefault(t, "actionable" if dec != "OWNED" else "owned")
            elif all_live:
                want.setdefault(t, "tracked (--all-live)")
    return want


def compute(all_live=False):
    if not os.path.exists(VALUATIONS):
        sys.exit(f"no valuation cards at {VALUATIONS}")
    cards = json.load(open(VALUATIONS, encoding="utf-8"))
    wanted = universe(all_live)

    # `status` is a MACHINE FLAG compared by exact string, so anything else written into
    # it makes the card invisible -- and an invisible card reports as "no valuation exists",
    # which reads as "go and do the work" rather than "your status string is wrong".
    # Hit live 2026-08-03: a new TSM card was written with status "live — near-term card,
    # first valuation this position has ever had". It was silently skipped, and the summary
    # line said 15 names needed a valuation when the true number was 14. Same two-objects-
    # one-shape pattern as everything else in this book: prose and a flag sharing one field.
    # The fix is not to be more careful -- it is to fail loudly on a value we do not know.
    # A CARD MAY NOT CARRY ITS OWN `buy_cap`. Added 2026-08-04 after the defect below.
    #
    # The ceiling is DERIVED — weighted value divided by the index multiple — so it moves
    # whenever the hurdle moves. On 2026-08-03 the hurdle went 9.0% -> 6.5% and every
    # ceiling rose 3-6%. This tool recomputed; the number written inside each card did not.
    # Fifteen cards were left asserting a stale ceiling that read exactly like a live one.
    #
    # What made it dangerous rather than untidy: on 2026-08-04 an independent challenger
    # found the two figures disagreeing for Elastic and concluded the LIVE one ($66.00) was
    # a transcription error and the STALE one ($63.39) was correct, because the stale one
    # sat in the workings and looked authoritative. It then built its headline finding on
    # that inversion. A stale number in the right place beats a live number in the wrong one.
    #
    # So the fix is not "remember to update both". It is that a card may not hold this field
    # at all. History goes in `buy_cap_WHEN_WRITTEN`, which no code reads.
    offenders = sorted(k for k, c in cards.items()
                       if isinstance(c, dict) and "buy_cap" in c)
    if offenders:
        raise SystemExit(
            "REFUSING TO RUN — valuation card(s) carry their own `buy_cap`, which this tool "
            "derives and which changes whenever the index hurdle changes:\n  "
            + "\n  ".join(offenders)
            + "\nA stored ceiling goes stale silently and reads as authoritative. Rename it to "
              "`buy_cap_WHEN_WRITTEN`; the live figure belongs only in book/buy_caps.csv.")

    KNOWN_STATUS = {"live", "pending", "declined", "declined_no_permitted_size",
                    "superseded", "retired"}
    unknown = sorted(
        f"{k}: {c.get('status')!r}" for k, c in cards.items()
        if isinstance(c, dict) and "status" in c and c.get("status") not in KNOWN_STATUS)
    if unknown:
        raise SystemExit(
            "REFUSING TO RUN — valuation card(s) carry a status this tool does not "
            "recognise, so they would be silently skipped and reported as missing:\n  "
            + "\n  ".join(unknown)
            + f"\nAllowed values: {', '.join(sorted(KNOWN_STATUS))}. Put prose in a "
              "separate field (status_note), never in the flag.")

    rows, missing = [], []
    for tk, role in sorted(wanted.items()):
        card = None
        for key in (tk, tk.split(".")[0], tk.replace(".", "_")):
            c = cards.get(key)
            if isinstance(c, dict) and c.get("status") == "live":
                card = c
                break
        if card is None:
            missing.append((tk, role, "no live valuation card exists"))
            continue

        pw, basis = weighted_value(card)
        if pw is None:
            missing.append((tk, role, basis))
            continue

        yrs, yrs_why = horizon_years(card, "near")
        if yrs is None:
            missing.append((tk, role, yrs_why))
            continue
        mult = index_multiple(yrs)
        cap = pw / mult
        px = num(card.get("price_at_calc"))
        as_of = parse_date(card.get("as_of"))
        valid_to = (as_of + dt.timedelta(days=CAP_VALID_DAYS)) if as_of else None
        stale = (valid_to is None) or (dt.date.today() > valid_to)

        # ---------------------------------------------------------------------
        # A PASS MUST BE INDEPENDENTLY CHALLENGED. Ben, 2026-08-04: "yes that's
        # sensible", answering the proposal that an independent challenge become
        # mandatory before any valuation is called a pass, not optional.
        #
        # WHY. Two valuations were called passes on 2026-08-03 and both were built
        # and checked by their own author. One inverted the next day: it valued
        # a company that had stopped existing on 2026-03-09, carried three
        # pre-acquisition inputs forward, and its "the profits are clean" check was
        # itself wrong — it compared quarters of tax in DOLLARS and never converted
        # to RATES, so the distorted quarter sat outside the window it chose. The
        # panel that caught it ran only because Ben asked for one. Playbook 6.1
        # check 6 has always said the pitcher may not write its own rebuttal; it
        # was being honoured for panels and skipped for valuations.
        #
        # A FAIL needs no challenge. The asymmetry is deliberate: a wrong fail
        # costs an opportunity, a wrong pass costs money. Only the direction that
        # spends money carries the burden.
        #
        # This does NOT block anything on its own — buy_cap.py reports, it does not
        # transmit. It makes an unchallenged pass IMPOSSIBLE TO MISREAD as a green
        # light, which is what one valuation PDF had already become.
        # HEADROOM AGAINST THE VALUATION-DAY PRICE — historical, and it must never be
        # read as current. `live_headroom_pct` below is the one that answers "may I buy
        # this today". Both are written out; see the live-price block after this loop.
        headroom = (100.0 * (cap / px - 1)) if px else None
        card_challenge = card.get("independent_challenge") or {}
        ch_verdict = str(card_challenge.get("verdict") or "").strip().upper()
        # Only a challenge the case SURVIVED clears the gate. Caught 2026-08-04, minutes
        # after the first real challenge came back: the gate asked "has this been
        # challenged?" and Elastic — which the challenger BROKE — went straight to
        # "usable" because a challenge block existed. A gate that counts reviews rather
        # than reading them is worse than none, because it launders a failure into a pass.
        cleared = bool(card_challenge.get("by") and card_challenge.get("date")
                       and ch_verdict.startswith("SURVIVES"))
        if stale:
            state = "STALE — refresh the valuation before buying"
        elif ch_verdict.startswith("BREAKS"):
            state = ("BROKEN BY CHALLENGE — not actionable at any price on this card. An "
                     "independent reviewer found an error that changes the verdict. Rebuild the "
                     "valuation; do not argue with the reviewer inside the old one.")
        elif ch_verdict.startswith("CANNOT"):
            state = ("CHALLENGE INCONCLUSIVE — not actionable. A load-bearing fact could not be "
                     "established from public sources. The card names it; settle it first.")
        elif headroom is not None and headroom >= 0 and not cleared:
            state = ("PASS, UNCHALLENGED — not actionable. An independent reviewer must "
                     "attack this case and fail before it may fund an order (Ben, 2026-08-04). "
                     "Add `independent_challenge` {by, date, verdict} to the card.")
        else:
            state = "usable"

        # §11.5 (2026-09-02, Ben): the return is reported beside the price, never hidden inside it.
        exp_ret = ((pw / px) ** (1.0 / yrs) - 1) if (px and px > 0) else None
        rows.append({
            "ticker": tk, "role": role,
            "expected_return_pct_at_valuation_price": (100.0 * exp_ret) if exp_ret is not None else None,
            "benchmark_return_pct": INDEX_RETURN_PCT,
            "weighted_value": pw, "value_basis": basis,
            "horizon_years": yrs, "horizon_basis": yrs_why,
            "index_multiple": mult, "buy_cap": cap,
            "price_at_valuation": px,
            "headroom_pct": headroom,
            "valuation_as_of": as_of.isoformat() if as_of else "",
            "valid_until": valid_to.isoformat() if valid_to else "",
            "state": state,
            "ccy": card.get("ccy", ""),
        })
    apply_live_prices(rows)
    return rows, missing


def apply_live_prices(rows):
    """Re-measure every ceiling against the CURRENT price, and say so loudly.

    THE DEFECT THIS FIXES, found 2026-08-04 by an independent challenger and the
    worst of the session. This file printed a rule it did not enforce: "a figure
    expires immediately on results, guidance, a capital raise, or a 15% move in the
    share price." Nothing ever fetched a price. The `headroom_pct` column compared
    the ceiling to `price_at_valuation` — the price on the DAY OF THE VALUATION —
    and every report, every reply to Ben, and every judgement of whether a name was
    buyable was built on it.

    One name shows what it costs. Its ceiling was compared against a price days
    old and reported +6.7% of room. At the live price the true figure was
    MINUS 20.7%. A 27-point error in the direction of "buy", on a name in the
    book, sitting in a column labelled as if it were current.

    The pattern is this book's oldest: one column that looks like current headroom
    and is historical headroom. The fix is not care, it is a second column that
    cannot be confused with the first, plus a state that changes when they diverge.
    """
    if not rows:
        return
    try:
        import yfinance as yf
    except ImportError:
        for r in rows:
            r["live_price"] = ""
            r["live_headroom_pct"] = ""
            r["price_check"] = "NO LIVE PRICE — yfinance unavailable; treat headroom_pct as historical only"
        return
    for r in rows:
        r["live_price"] = ""
        r["live_headroom_pct"] = ""
        r["price_check"] = ""
        try:
            h = yf.Ticker(r["ticker"]).history(period="7d")["Close"].dropna()
            if not len(h):
                r["price_check"] = "NO LIVE PRICE — vendor returned nothing; headroom_pct is historical only"
                continue
            live = float(h.iloc[-1])
            r["live_price"] = live
            r["live_headroom_pct"] = 100.0 * (r["buy_cap"] / live - 1)
            r["expected_return_pct_live"] = 100.0 * ((r["weighted_value"] / live) ** (1.0 / r["horizon_years"]) - 1)
            old = r.get("price_at_valuation")
            move = (100.0 * (live / old - 1)) if old else None
            # The file's own rule: a move this large voids the figure outright.
            if move is not None and abs(move) >= CAP_VOID_MOVE_PCT:
                r["price_check"] = (f"VOID — the price moved {move:+.1f}% since this was valued "
                                    f"({old:,.2f} -> {live:,.2f}), past the {CAP_VOID_MOVE_PCT:.0f}% "
                                    f"threshold this file sets. Re-read the valuation before acting.")
                r["state"] = ("VOID ON A PRICE MOVE — not actionable. " + r["price_check"])
            elif (r.get("headroom_pct") is not None and r["headroom_pct"] >= 0
                  and r["live_headroom_pct"] < 0):
                r["price_check"] = (f"SIGN FLIP — historical headroom {r['headroom_pct']:+.1f}% but live "
                                    f"{r['live_headroom_pct']:+.1f}%. The pass is an artefact of a stale price.")
                r["state"] = ("FAILS AT THE LIVE PRICE — not actionable. " + r["price_check"])
            elif move is not None:
                r["price_check"] = f"live {live:,.2f} vs {old:,.2f} at valuation ({move:+.1f}%)"
        except Exception as e:                                  # noqa: BLE001 — a vendor
            r["price_check"] = f"NO LIVE PRICE — {type(e).__name__}; headroom_pct is historical only"


def write_outputs(rows, missing):
    cols = ["ticker", "role", "buy_cap", "weighted_value", "horizon_years",
            "expected_return_pct_live", "expected_return_pct_at_valuation_price", "benchmark_return_pct",
            "index_multiple", "price_at_valuation", "headroom_pct",
            "live_price", "live_headroom_pct", "price_check",
            "valuation_as_of", "valid_until", "state", "value_basis", "horizon_basis",
            "ccy"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for r in rows:
            w.writerow({k: (f"{r[k]:.4f}" if isinstance(r.get(k), float) else r.get(k, ""))
                        for k in cols})

    L = ["# The most we may pay for each company today\n"]
    L.append(f"Generated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M UTC}.\n")
    L.append("\nThis is not a price we expect to pay and not an order price. It is the "
             "point above which the company stops being worth owning at all, because "
             f"a broad index compounding {INDEX_RETURN_PCT:g}% a year would do better "
             "after a 26% tax on gains.\n")
    L.append("\nIt is computed, never chosen: our probability-weighted value for the "
             "company, divided by what the index turns one euro into over the same "
             "number of years. **A rising share price never raises it. Only new "
             "evidence about the business does.**\n")

    if rows:
        L.append("\n| Company | Why it has one | Most we may pay | Our weighted value | Over | Priced at | Room | Expected return a year from today's price | Market comparison | Good until |")
        L.append("|---|---|---|---|---|---|---|---|---|---|")
        for r in sorted(rows, key=lambda x: x["ticker"]):
            room = f"{r['headroom_pct']:+.1f}%" if r["headroom_pct"] is not None else "—"
            px = f"{r['price_at_valuation']:,.2f}" if r["price_at_valuation"] else "—"
            er = r.get("expected_return_pct_live")
            er_s = f"{er:+.1f}%" if isinstance(er, float) else "—"
            L.append(f"| {r['ticker']} | {r['role']} | **{r['buy_cap']:,.2f}** | "
                     f"{r['weighted_value']:,.2f} | {r['horizon_years']}y | {px} | "
                     f"{room} | {er_s} | {INDEX_RETURN_PCT:g}% | {r['valid_until'] or '—'} |")
        L.append("\n**Reading the return column (added 2026-09-02, Ben's instruction).** The expected return is the "
                 "probability-weighted value divided by today's price, annualised over the card's own horizon. It is "
                 "the number to read; the price columns are the same arithmetic in price form. Ideally it is above the "
                 "market comparison, and above Ben's own objective for the company's type (12% a year; 10% for a true "
                 "compounder held five years or more).\n")
        L.append("\n**Reading the room column.** A negative number means the price when "
                 "we last valued it was already ABOVE the most it is worth paying. That "
                 "is not an error — it is the answer, and it says do not buy.\n")

    stale = [r for r in rows if r["state"].startswith("STALE")]
    if stale:
        L.append(f"\n## {len(stale)} of these are out of date\n")
        L.append(f"A figure here lasts {CAP_VALID_DAYS} days. Past that it blocks a new "
                 "purchase until the valuation behind it is re-read. That costs nothing "
                 "while we are not buying, and it is the check worth doing at the exact "
                 "moment we are: " + ", ".join(sorted(r["ticker"] for r in stale)) + ".\n")

    if missing:
        L.append(f"\n## {len(missing)} names have no figure, and why\n")
        L.append("Each of these would need a valuation before any purchase could be "
                 "approved. Naming them is the point — an absent number must not read "
                 "as permission.\n")
        for tk, role, why in sorted(missing):
            L.append(f"- **{tk}** ({role}): {why}")
        L.append("")

    L.append("\n## The rules this file enforces\n")
    L.append("1. The figure above is the model's answer, and it never moves for an order. "
             "Going above it takes Ben's explicitly approved price, and the order check "
             "prints this figure and the premium beside any such order — the disagreement "
             "is recorded, never erased (amended 2026-08-11; the old absolute ban stopped "
             "matching the code on 2026-08-04).\n")
    L.append("2. Raising the price on an order never raises this figure. They are "
             "separate decisions and were repeatedly confused: four of the old ceilings "
             "were set equal to the order price, so every increase to one dragged the "
             "other up behind it. One company's ceiling rose four times in fifteen hours.\n")
    L.append(f"3. This figure expires after {CAP_VALID_DAYS} days, and immediately on "
             "results, guidance, a capital raise, or a "
             f"{CAP_VOID_MOVE_PCT:.0f}% move in the share price.\n")
    L.append("4. When the price sits above it on something we own: buy no more, cancel "
             "any resting purchase, and put the money into the next-best idea. It is not "
             "a reason to sell — selling crystallises tax, which usually costs more than "
             "the mistake it is trying to fix.\n")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")


def check(ticker, price):
    rows, _ = compute(all_live=True)
    for r in rows:
        if r["ticker"].upper() == ticker.upper():
            cap = r["buy_cap"]
            ok = price <= cap and not r["state"].startswith("STALE")
            print(f"{ticker}: you propose {price:,.2f}; the most it is worth paying is "
                  f"{cap:,.2f} ({r['valuation_as_of']}, good until {r['valid_until']}).")
            if r["state"].startswith("STALE"):
                print("  STALE — that valuation is out of date; the re-read is owed before "
                      "this figure may be cited. Only Ben's own words move an order.")
            elif not ok:
                print(f"  ABOVE THE MODEL'S CEILING — {100*(price/cap-1):.1f}% over the most "
                      f"the model says it is worth paying; on the model's arithmetic the "
                      f"index is the better use of the money. Proceeding takes Ben's "
                      f"explicitly approved price, with this figure and the premium printed "
                      f"beside the order. The figure itself does not move.")
            else:
                print(f"  OK — {100*(1-price/cap):.1f}% below the cap.")
            return 0 if ok else 1
    print(f"{ticker}: no figure on file — nothing to compare against, and the valuation is "
          f"owed. An absent figure is neither permission nor a block; Ben's written "
          f"approval decides, and the gap is logged.")
    return 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--all-live", action="store_true",
                    help="every name with a live valuation, not just owned and actionable")
    ap.add_argument("--check", nargs=2, metavar=("TICKER", "PRICE"),
                    help="ask whether a proposed price is allowed")
    a = ap.parse_args()

    if a.check:
        sys.exit(check(a.check[0], float(a.check[1])))

    rows, missing = compute(a.all_live)
    write_outputs(rows, missing)
    usable = [r for r in rows if not r["state"].startswith("STALE")]
    print(f"Names considered: {len(rows) + len(missing)}  with a figure: {len(rows)}  "
          f"usable today: {len(usable)}  needing a valuation first: {len(missing)}")
    print(f"Wrote {OUT_MD}")


if __name__ == "__main__":
    main()
