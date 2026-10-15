#!/usr/bin/env python3
"""Grade every decision the engine has ever made against what the money would
otherwise have earned.

WHY THIS EXISTS (2026-08-01, Ben). The rulebook has always required that a
decline be scored against a counterfactual. That scoring ran once, on three
names, and returned "too early". Meanwhile 98 of 156 names sat in a waiting
state that was never eligible for scoring at all, because only explicit kills
were logged. So the engine could not answer the only question that matters --
"when did we say no and should have said yes?" -- and nobody noticed.

WHAT IT DOES. For every name the engine declined, parked, or bought, it takes
the price on the DECISION DATE, fetches the price now, and compares the result
to the index the money would otherwise have sat in. It then reports the score
BY STATED REASON, because the useful finding is not "we were wrong" but "the
reasons of this type are the ones that cost us."

THIS IS A REPORTING TOOL. It places no order, cancels no order, alters no
order, and writes to nothing except book/decision_grades.csv and
book/decision_grades.md.

HONESTY RULES BAKED IN, each one from a real error in this book's record:
  * A call younger than the scoring window is reported as TOO EARLY BY WINDOW,
    never as right or wrong. Ben's standing rule: say "too early by window",
    never "unmeasurable".
  * Rows we cannot grade are SKIPPED AND COUNTED in the output, with the reason
    named. Silent truncation reads as "we covered everything" when we did not.
  * Returns are computed in the name's own currency. Exchange-rate moves are a
    separate attribution and mixing them in would flatter or punish the call
    for something the analyst never decided.
  * Prices come from settled closes, never from an intraday or after-hours
    print. Five logged errors in this book came from that exact confusion.

FIXED 2026-08-01 after an independent adversarial review. Six defects, each of
which had already produced or could produce a large, confident, wrong number:

  D1  THE WRONG DECISION WAS BEING GRADED. The old code paired price_at_add
      (the price on the day a name was ADDED to the watchlist) with
      verdict_date (the day it was DECIDED). Those are different instants. A
      name added at 10 in January and declined at 20 in June, now 22, was
      reported as +120% when the return since the decision was +10%. A row is
      now graded only when the record proves the price and the decision date
      describe the same day, AND the stored price matches a settled close near
      that date. Everything else is dropped and counted.
  D2  THE BENCHMARK WAS ALWAYS SMH. The docstring promised the chip index for
      hardware names and the Nasdaq index for the rest; every table used SMH. A
      software name up 5% against a Nasdaq up 3% was labelled a good refusal at
      -25 points instead of a costly one at +2. Each row now carries one
      benchmark, assigned from its own industry, used everywhere, and written
      into both outputs.
  D3  SPLITS DESTROYED THE RETURN. The provider's history is split-adjusted;
      the stored decision price is not. A 4-for-1 split read as roughly -75%.
      Splits between the decision date and today are now detected and the
      stored price is converted into post-split terms before anything is
      computed.
  D4  --weekly-only COULD CORRUPT ITS OWN HISTORY: an empty file appended rows
      with no header, a future timestamp made it skip forever, two overlapping
      runs both appended a full batch, and a failed report still recorded the
      job as done. Header validated, dates rejected loudly, append under an
      exclusive lock, report written before completion is recorded.
  D5  Duplicate kill rows were counted twice; the de-duplication set was built
      once and never updated.
  D6  The report claimed causation from as few as eight observations. It now
      reports the count and the spread, and says plainly that overlapping dates
      and shared industries make the independent sample smaller than the count.

Usage:
    python3 data/decision_grader.py                # grade everything, write both outputs
    python3 data/decision_grader.py --dry-run      # print, write nothing
    python3 data/decision_grader.py --window 90    # change the scoring window in days
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import fcntl
import io
import os
import re
import statistics
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BOOK = os.path.join(SKILL, "book")

WATCHLIST = os.path.join(BOOK, "watchlist.csv")
KILLS = os.path.join(BOOK, "kills.csv")
OUT_CSV = os.path.join(BOOK, "decision_grades.csv")
OUT_MD = os.path.join(BOOK, "decision_grades.md")

# ---------------------------------------------------------------------------
# D2. The money's alternative home. ONE of these is chosen per row, from that
# row's own industry, and then used everywhere for that row. Mixing them is the
# defect this replaces.
# ---------------------------------------------------------------------------
BENCH_CHIPS = "SMH"
BENCH_BROAD = "QQQ"
BENCHMARKS = [BENCH_CHIPS, BENCH_BROAD]

BENCH_LONG = {
    BENCH_CHIPS: "the VanEck Semiconductor fund (SMH), which holds the largest "
                 "listed chipmakers and chip-equipment makers",
    BENCH_BROAD: "the Invesco QQQ fund (QQQ), which holds the hundred largest "
                 "non-financial companies on the Nasdaq",
}
BENCH_SHORT = {
    BENCH_CHIPS: "the chip fund (SMH)",
    BENCH_BROAD: "the Nasdaq fund (QQQ)",
}

# An industry is graded against the chip fund only if the company sells into
# the semiconductor supply chain. Everything else, including AI cloud renters,
# power equipment and software, is graded against the Nasdaq fund. Anything we
# cannot place goes to the Nasdaq fund and says so.
CHIP_INDUSTRY_PATTERNS = [
    r"\bsemiconductor", r"\bsemi equipment\b", r"\bchip\b", r"\bchips\b",
    r"\bmemory\b", r"\bdram\b", r"\bhbm\b", r"\bwafer", r"\bfoundry\b",
    r"\bsubstrate", r"\blithograph", r"\bprobe card", r"\basic\b",
]

# Below this age a call is reported but never scored. 90 days is one quarter --
# the shortest window over which a fundamental call can honestly be judged.
DEFAULT_WINDOW_DAYS = 90

# D1/D3 proof rules. A stored decision price is accepted only if it matches a
# settled close within this many calendar days of the decision date, to within
# this percentage. The tolerance is self-calibrating: a date error the tolerance
# lets through is one where the price barely moved, so it cannot move the answer.
PRICE_PROOF_WINDOW_DAYS = 3
PRICE_PROOF_TOLERANCE_PCT = 2.0

csv.field_size_limit(10 ** 9)


# --------------------------------------------------------------------------
# Reason classification. The whole point of the report is this split, so the
# patterns are explicit and auditable rather than clever.
# --------------------------------------------------------------------------

REASON_PATTERNS = [
    ("legal or access barrier", [
        r"\bnot listed\b", r"\bprivate\b", r"\bpre-ipo\b", r"\bcannot trade\b",
        r"\bshort selling is (switched )?off\b", r"\bblocked\b", r"\bsanction",
        r"\bprofessional investors\b", r"\baccess\b.{0,20}\bbarrier\b",
    ]),
    ("the business itself", [
        r"\bcompetiti", r"\bmarket share\b", r"\bchurn\b", r"\bproduct\b",
        r"\bmanagement\b", r"\bgovernance\b", r"\bloss-making\b",
        r"\bdo(es)? not earn\b", r"\bgrowth rate must fall\b", r"\bdecelerat",
    ]),
    ("balance sheet or dilution", [
        r"\bdilut", r"\bshare count\b", r"\bprints? shares\b", r"\bnet debt\b",
        r"\bleverage\b", r"\bgoing concern\b", r"\baccounting\b", r"\brestat",
    ]),
    ("price or valuation", [
        r"\balready priced\b", r"\bconsensus price\b", r"\bexpensive\b",
        r"\brich\b", r"\btimes (last|next) year", r"\bno gap\b", r"\bfully priced\b",
        r"\bvaluation\b", r"\bp/e\b", r"\bev/s", r"\bmultiple\b",
    ]),
    ("crowding or popularity", [
        r"\bcrowd", r"\bconsensus\b", r"\bpopular\b", r"\balready discovered\b",
        r"\banalysts covering\b", r"\bhighest band\b",
    ]),
    ("wrong part of the supply chain", [
        r"\bwrong layer\b", r"\btwo steps away\b", r"\bprofit pool\b",
        r"\bdiluted (play|exposure)\b", r"\bonly \d+% of\b",
    ]),
    ("too early or not enough evidence", [
        r"\bnothing proven\b", r"\buntested\b", r"\btoo early\b",
        r"\bneeds? (more|two) \w+ (quarters|reports)\b", r"\bresearch entry\b",
    ]),
]


def classify_reason(text: str) -> str:
    """Assign one reason group. Order matters: access and business quality are
    checked before price, because a row that says both is really the former."""
    t = (text or "").lower()
    if not t.strip():
        return "reason not recorded"
    for label, pats in REASON_PATTERNS:
        for p in pats:
            if re.search(p, t):
                return label
    return "other"


# --------------------------------------------------------------------------
# D2. Benchmark assignment
# --------------------------------------------------------------------------

def assign_benchmark(industry: str, theme: str):
    """Return (benchmark_code, how_it_was_chosen).

    Industry decides on its own when it is recorded, because the theme field
    carries second-order labels -- a PC maker themed "memory-cost-victim" is not
    a chip company and must not be graded against the chip fund."""
    ind = (industry or "").strip()
    th = (theme or "").strip()
    if ind:
        for p in CHIP_INDUSTRY_PATTERNS:
            if re.search(p, ind.lower()):
                return BENCH_CHIPS, "industry names the chip supply chain"
        return BENCH_BROAD, "industry is outside the chip supply chain"
    if th:
        for p in CHIP_INDUSTRY_PATTERNS:
            if re.search(p, th.lower()):
                return BENCH_CHIPS, "no industry recorded; theme names the chip supply chain"
        return BENCH_BROAD, "no industry recorded; theme is outside the chip supply chain"
    return BENCH_BROAD, "no industry or theme recorded; defaulted to the broad index"


# --------------------------------------------------------------------------
# Parsing helpers
# --------------------------------------------------------------------------

def parse_price(raw):
    """Return a float price, or None. Refuses obvious non-prices."""
    if raw is None:
        return None
    s = str(raw).strip()
    if not s or s.lower() in {"n/a", "na", "none", "-", "tbd", "unknown"}:
        return None
    s = s.replace(",", "")
    m = re.search(r"-?\d+\.?\d*", s)
    if not m:
        return None
    try:
        v = float(m.group())
    except ValueError:
        return None
    return v if v > 0 else None


def parse_date(raw):
    if not raw:
        return None
    m = re.search(r"(20\d{2})-(\d{2})-(\d{2})", str(raw))
    if not m:
        return None
    try:
        return dt.date(int(m.group(1)), int(m.group(2)), int(m.group(3)))
    except ValueError:
        return None


DANGLING = {"and", "or", "the", "a", "an", "to", "for", "of", "in", "on", "with",
            "that", "which", "its", "their", "by", "at", "as", "from", "but", "plus"}

# Only these openers are lower-cased when a description is folded into a
# sentence. Anything else keeps its capital, so "Swiss maker of pumps" and
# "World's only producer" are not mangled into nonsense.
LEAD_VERBS = {"makes", "sells", "builds", "owns", "runs", "rents", "designs",
              "mines", "does", "resells", "launches", "rebuilds", "tracks",
              "consults", "advises", "provides", "supplies", "operates", "helps",
              "develops", "manufactures", "produces", "licenses"}


def eight_words(text: str) -> str:
    """At most eight words of plain description, house rule for anything Ben reads."""
    w = " ".join((text or "").split())
    w = re.split(r"[.;|]", w)[0].strip()
    parts = w.split()[:8]
    while parts and parts[-1].strip(",").lower() in DANGLING:
        parts.pop()
    if not parts:
        return ""
    parts[-1] = parts[-1].rstrip(",")
    if parts[0].lower() in LEAD_VERBS:
        parts[0] = parts[0].lower()
    return " ".join(parts)


# --------------------------------------------------------------------------
# Price history
# --------------------------------------------------------------------------

def load_history(tickers, start):
    """Settled daily closes, quoted currency and splits per ticker.

    Returns {ticker: {"closes": {isodate: close}, "splits": {isodate: factor},
                      "currency": str or None}}.

    The provider's close series is split-adjusted throughout, so it is
    internally consistent. The STORED decision price is not, which is what D3
    is about, so the splits are carried out of here for that adjustment."""
    try:
        import yfinance as yf
    except ImportError:
        sys.exit("yfinance not installed. Run: pip3 install --user yfinance")

    out = {}
    for t in sorted(set(tickers)):
        try:
            tk = yf.Ticker(t)
            h = tk.history(start=start.isoformat(), auto_adjust=False, actions=True)
        except Exception:
            continue
        if h is None or len(h) == 0:
            continue
        closes = {
            d.date().isoformat(): float(c)
            for d, c in zip(h.index, h["Close"])
            if c == c and float(c) > 0  # drop NaN bars; a NaN is missing data, not a zero
        }
        if not closes:
            continue
        splits = {}
        if "Stock Splits" in h.columns:
            for d, v in zip(h.index, h["Stock Splits"]):
                try:
                    v = float(v)
                except (TypeError, ValueError):
                    continue
                if v == v and v > 0 and abs(v - 1.0) > 1e-9:
                    splits[d.date().isoformat()] = v
        try:
            ccy = (tk.history_metadata or {}).get("currency")
        except Exception:
            ccy = None
        out[t] = {"closes": closes, "splits": splits, "currency": ccy}
    return out


def price_on_or_after(series, iso):
    if not series:
        return None
    ks = [k for k in series if k >= iso]
    return series[min(ks)] if ks else None


def price_on_or_before(series, iso):
    if not series:
        return None
    ks = [k for k in series if k <= iso]
    return series[max(ks)] if ks else None


def latest(series):
    if not series:
        return None, None
    k = max(series)
    return series[k], k


def closes_near(closes, when, days):
    """Every settled close within `days` calendar days either side of `when`."""
    lo = (when - dt.timedelta(days=days)).isoformat()
    hi = (when + dt.timedelta(days=days)).isoformat()
    return [(k, v) for k, v in closes.items() if lo <= k <= hi]


def split_factor_after(splits, when):
    """D3. Cumulative split factor for every split strictly after the decision.

    A 4-for-1 split returns 4.0, meaning the stored pre-split price must be
    divided by 4 to be comparable with today's split-adjusted price."""
    f = 1.0
    iso = when.isoformat()
    for k, v in splits.items():
        if k > iso:
            f *= v
    return f


def currency_conflict(recorded, quoted):
    """True when the record and the feed disagree about the currency.

    GBp (pence) and GBP (pounds) differ by a factor of one hundred, so they are
    a conflict even though they look like the same word."""
    a = (recorded or "").strip()
    b = (quoted or "").strip()
    if not a or not b:
        return False
    if a == b:
        return False
    if a.upper() == "GBP" and b.upper() == "GBP":
        return True  # one is pence, the other pounds
    return a.upper() != b.upper()


# --------------------------------------------------------------------------
# Gathering the decisions
# --------------------------------------------------------------------------

DECLINED = {"PASSED", "AVOID", "PASS", "KILL", "BLOCKED-ACCESS", "UNSCREENED"}
WAITING = {"WATCHING", "RE-CHECK AT EVENT", "WATCH", "RE-CHECK"}
BOUGHT = {"OWNED", "BUY APPROVED", "ORDER PLACED", "BUY IF"}

# D1. Named so the report can count each cause separately.
DROP_NO_PRICE = "the record holds no usable price"
DROP_NO_DATE = "the record holds no usable decision date"
DROP_PAIR = "the recorded price is from a different day than the decision"
DROP_PRICE_UNDATED = "the record never says which day the price belongs to"
DROP_PAIR_CONTRADICTS = "the record gives the price two different dates"
DROP_NOT_TRADEABLE = "the row is a pair or a theme, not one tradeable line"
DROP_NO_FEED = "no market data came back for the ticker"
DROP_CCY = "the record and the price feed disagree about the currency"
DROP_UNPROVEN = "the stored price matches no settled close near the decision date"


def decision_pair(r):
    """D1. Establish a price and a date that provably describe the same day.

    Returns (date, price, how_we_know) or (None, None, why_not).

    price_at_add is, by the column's own meaning, the price on date_added.
    verdict_date is when the call was made. The pair is accepted only when the
    record itself places the price on the decision day: either the price is
    stamped with a date that equals the decision date, or there is no stamp and
    the name was added and decided on the same day. Anything else is dropped --
    guessing which instant a number belongs to is what produced the defect."""
    added = parse_date(r.get("date_added"))
    decided = parse_date(r.get("verdict_date")) or added
    px = parse_price(r.get("price_at_add"))
    stamp = parse_date(r.get("price_at_add"))   # e.g. "$9.93 (2026-07-27 close)"
    asof = parse_date(r.get("price_asof"))

    if px is None:
        return None, None, DROP_NO_PRICE
    if decided is None:
        return None, None, DROP_NO_DATE
    if stamp and asof and stamp != asof:
        return None, None, DROP_PAIR_CONTRADICTS
    price_day = stamp or asof or added
    if price_day is None:
        return None, None, DROP_PRICE_UNDATED
    # A STAMP ONE DAY BEFORE THE DECISION IS THE HOUSE CONVENTION, NOT A MISMATCH
    # (added 2026-08-01). CLAUDE.md's standing rule is "price at call = the PRIOR
    # day's close" — when a call is made during a session, the last settled close
    # is yesterday's. Requiring an exact date match therefore threw away rows the
    # record had got RIGHT: seven names were dropped for obeying the convention.
    # Up to four calendar days is allowed so a Monday decision can pair with the
    # previous Friday's close, or Tuesday's with a Friday before a holiday.
    if price_day != decided:
        gap = (decided - price_day).days
        if 0 < gap <= 4:
            return decided, px, ("the price is the last settled close before the "
                                 "decision, which is how this book records a price "
                                 "at the moment of a call")
        return None, None, DROP_PAIR
    if stamp or asof:
        return decided, px, "the price carries the decision date as its own stamp"
    return decided, px, "the name was added and decided on the same day"


def gather():
    """Every decision we can honestly try to grade, plus the ones we dropped."""
    rows, skipped = [], []
    names = {}

    if os.path.exists(WATCHLIST):
        for r in csv.DictReader(open(WATCHLIST, encoding="utf-8")):
            tk = (r.get("ticker") or "").strip()
            dec = (r.get("decision") or "").strip().upper()
            if not tk:
                continue
            names[tk] = ((r.get("name") or "").strip(),
                         (r.get("what_they_do") or "").strip(),
                         (r.get("industry") or "").strip(),
                         (r.get("theme") or "").strip())
            if dec == "GAUGE":
                continue  # a measuring instrument was never a candidate
            when, px, basis = decision_pair(r)
            reason_text = " ".join(filter(None, [
                r.get("decision_tldr"), r.get("verdict"), r.get("why")]))
            if when is None:
                skipped.append((tk, dec, basis))
                continue
            bench, bench_basis = assign_benchmark(r.get("industry"), r.get("theme"))
            rows.append({
                "ticker": tk,
                "name": (r.get("name") or "").strip(),
                "what": (r.get("what_they_do") or "").strip(),
                "decision": dec,
                "group": ("declined" if dec in DECLINED else
                          "waiting" if dec in WAITING else
                          "bought" if dec in BOUGHT else "other"),
                "date": when,
                "price": px,
                "pair_basis": basis,
                "ccy": (r.get("price_ccy") or "").strip(),
                "benchmark": bench,
                "bench_basis": bench_basis,
                "reason": classify_reason(reason_text),
                "source": "watchlist",
            })

    if os.path.exists(KILLS):
        seen = {(x["ticker"], x["date"]) for x in rows}
        for r in csv.DictReader(open(KILLS, encoding="utf-8")):
            tk = (r.get("ticker") or "").strip()
            dec = (r.get("decision") or "").strip().upper()
            # Some kill rows record a PAIR or a theme rather than one tradeable
            # line ("000660.KS+MU (pair)", "CN-A-SHARE-AI"). Those are real
            # decisions but they have no single price series, so they are
            # counted as skipped rather than silently dropped.
            if not tk:
                continue
            if "+" in tk or " " in tk or (tk.isupper() and "-" in tk and "." not in tk):
                skipped.append((tk, dec, DROP_NOT_TRADEABLE))
                continue
            when = parse_date(r.get("date"))
            px = parse_price(r.get("price_at_decision"))
            if when is None or px is None:
                skipped.append((tk, dec, DROP_NO_PRICE if px is None else DROP_NO_DATE))
                continue
            if (tk, when) in seen:
                continue
            seen.add((tk, when))  # D5: without this, a duplicate kill row counts twice
            nm, what, ind, th = names.get(tk, ("", "", "", ""))
            bench, bench_basis = assign_benchmark(ind, th)
            rows.append({
                "ticker": tk, "name": nm, "what": what,
                "decision": dec,
                "group": ("declined" if dec in DECLINED else
                          "waiting" if dec in WAITING else
                          "bought" if dec in BOUGHT else "declined"),
                "date": when, "price": px,
                "pair_basis": "the kill log records the price taken at the decision",
                "ccy": (r.get("ccy") or "").strip(),
                "benchmark": bench,
                "bench_basis": bench_basis,
                "reason": classify_reason(r.get("reason")),
                "source": "kills",
            })
    return rows, skipped


# --------------------------------------------------------------------------
# Scoring
# --------------------------------------------------------------------------

def grade(rows, window_days):
    """Return (graded, dropped). Everything dropped here carries its reason."""
    today = dt.date.today()
    if not rows:
        return [], []
    earliest = min(r["date"] for r in rows) - dt.timedelta(days=5)
    hist = load_history([r["ticker"] for r in rows] + BENCHMARKS, earliest)

    graded, dropped = [], []
    for r in rows:
        h = hist.get(r["ticker"])
        if not h or not h["closes"]:
            dropped.append((r["ticker"], r["decision"], DROP_NO_FEED))
            continue

        if currency_conflict(r["ccy"], h["currency"]):
            dropped.append((r["ticker"], r["decision"], DROP_CCY))
            continue

        # D3. Convert the stored price into today's split-adjusted terms before
        # anything is computed from it.
        factor = split_factor_after(h["splits"], r["date"])
        px = r["price"] / factor

        # D1/D3 proof. The record's own claim is only accepted once the market's
        # settled closes agree with it. This is also what catches a wrong
        # currency, a mistyped figure, and a split we failed to detect.
        near = closes_near(h["closes"], r["date"], PRICE_PROOF_WINDOW_DAYS)
        if not near:
            dropped.append((r["ticker"], r["decision"], DROP_UNPROVEN))
            continue
        best_day, best_close = min(near, key=lambda kv: abs(kv[1] - px))
        gap = 100.0 * abs(best_close - px) / best_close
        if gap > PRICE_PROOF_TOLERANCE_PCT:
            dropped.append((r["ticker"], r["decision"], DROP_UNPROVEN))
            continue

        now, now_asof = latest(h["closes"])
        ret = 100.0 * (now / px - 1.0)

        # D2. One benchmark for this row, measured over exactly the same window
        # as the name, so a stale foreign close is not compared to a fresh index.
        bser = hist.get(r["benchmark"], {}).get("closes", {})
        b0 = price_on_or_after(bser, r["date"].isoformat())
        b1 = price_on_or_before(bser, now_asof)
        bench_ret = (100.0 * (b1 / b0 - 1.0)) if (b0 and b1) else None

        rec = dict(r)
        rec.update({
            "price_used": px,
            "split_factor": factor,
            "proof_close": best_close,
            "proof_day": best_day,
            "proof_gap_pct": gap,
            "price_now": now,
            "price_now_asof": now_asof,
            "quote_ccy": h["currency"] or r["ccy"] or "",
            "ret_pct": ret,
            "bench_ret_pct": bench_ret,
            "excess_pts": (ret - bench_ret) if bench_ret is not None else None,
            "age_days": (today - r["date"]).days,
        })
        rec["scored"] = rec["age_days"] >= window_days
        graded.append(rec)
    return graded, dropped


def outcome_line(rec):
    """What happened, stated without claiming why.

    D6: this used to say "correct so far" and "costly so far", which asserts
    that the reason drove the outcome. It reports the comparison only."""
    ex = rec.get("excess_pts")
    if ex is None:
        return "no index comparison available"
    if not rec["scored"]:
        return "too early by window"
    beat = ex > 0
    if rec["group"] in ("declined", "waiting"):
        return "declined; it then beat the index" if beat else "declined; it then lagged the index"
    if rec["group"] == "bought":
        return "held; it then beat the index" if beat else "held; it then lagged the index"
    return "no decision type recorded"


# --------------------------------------------------------------------------
# The accumulating record. D4 lives in this block.
# --------------------------------------------------------------------------

CSV_COLS = [
    "run_utc", "ticker", "name", "decision", "group", "reason",
    "decision_date", "age_days", "price_pair_basis",
    "price_at_decision_recorded", "split_factor_applied",
    "price_at_decision_used", "matched_close", "matched_close_date",
    "matched_gap_pct", "price_ccy", "price_now", "price_now_asof",
    "ret_pct", "benchmark", "benchmark_basis", "bench_ret_pct", "excess_pts",
    "scored", "outcome",
]

# The schema written before the 2026-08-01 fixes. Every row under it was
# computed with the wrong decision price, the wrong benchmark, and no split
# handling, so those rows cannot be compared with anything written since.
LEGACY_COLS = [
    "run_utc", "ticker", "name", "decision", "group", "reason",
    "decision_date", "age_days", "price_at_decision", "ccy",
    "price_now", "price_asof", "ret_pct", "bench_SMH", "excess_SMH",
    "bench_QQQ", "excess_QQQ", "scored", "verdict",
]


def _inspect_header(body):
    """Return (needs_header, needs_legacy_reset). Raises loudly on anything else.

    D4(a): a file that exists but is empty used to be appended to with no
    header, after which every later run read the first data row as the header,
    never found run_utc, and appended forever."""
    if not body.strip():
        return True, False
    first = body.splitlines()[0]
    try:
        cols = next(csv.reader([first]))
    except Exception:
        cols = []
    if cols == CSV_COLS:
        return False, False
    if cols == LEGACY_COLS:
        return True, True
    raise SystemExit(
        "REFUSING TO WRITE. The first line of\n  " + OUT_CSV + "\nis not a header "
        "this script recognises. It reads:\n  " + first[:200] + "\nThat usually means "
        "rows were once appended without a header, or the file was edited by hand. "
        "Nothing has been appended. Move that file aside and run again to start a "
        "clean record.")


def _last_run_date(body):
    """Latest run date in the history. Raises loudly on malformed or future dates.

    D4(b): a future timestamp made (today - last).days negative, which is less
    than seven, so --weekly-only skipped forever and nobody was told."""
    if not body.strip():
        return None
    rdr = csv.DictReader(io.StringIO(body))
    if not rdr.fieldnames or "run_utc" not in rdr.fieldnames:
        raise SystemExit(
            "REFUSING TO WRITE. " + OUT_CSV + " has no run_utc column, so the "
            "date of the last run cannot be read. Nothing has been appended.")
    today = dt.date.today()
    last, bad = None, []
    for i, row in enumerate(rdr, start=2):
        raw = (row.get("run_utc") or "").strip()
        d = parse_date(raw)
        if d is None:
            bad.append((i, raw or "(empty)"))
            continue
        if d > today:
            raise SystemExit(
                "REFUSING TO RUN. " + OUT_CSV + " line " + str(i) + " says this job "
                "last ran on " + d.isoformat() + ", which is in the future (today is "
                + today.isoformat() + "). Left alone, the weekly check would skip this "
                "job forever. Correct that row by hand, then run again.")
        if last is None or d > last:
            last = d
    if bad:
        raise SystemExit(
            "REFUSING TO RUN. " + OUT_CSV + " holds " + str(len(bad)) + " run "
            "timestamp(s) that cannot be read as a date, first at line "
            + str(bad[0][0]) + ": " + str(bad[0][1]) + ". Correct them by hand, then "
            "run again.")
    return last


def read_history_state():
    """Validate the record and return the date it was last written. Read lock only."""
    if not os.path.exists(OUT_CSV):
        return None
    with open(OUT_CSV, "r", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_SH)
        try:
            body = f.read()
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    _inspect_header(body)
    return _last_run_date(body)


def _row_values(r, run_utc):
    def num(v, nd=2):
        return "" if v is None else ("%." + str(nd) + "f") % v
    return [
        run_utc, r["ticker"], r["name"], r["decision"], r["group"], r["reason"],
        r["date"].isoformat(), r["age_days"], r["pair_basis"],
        num(r["price"], 4), num(r["split_factor"], 6),
        num(r["price_used"], 4), num(r["proof_close"], 4), r["proof_day"],
        num(r["proof_gap_pct"]), r["quote_ccy"], num(r["price_now"], 4),
        r["price_now_asof"], num(r["ret_pct"]), r["benchmark"], r["bench_basis"],
        num(r["bench_ret_pct"]), num(r["excess_pts"]),
        "yes" if r["scored"] else "no", outcome_line(r),
    ]


def append_csv(graded, run_utc, weekly_only):
    """Append this run under an exclusive lock, re-checking the last run inside it.

    D4(c): two overlapping invocations both read the old date outside any lock
    and both appended a full batch. The check that decides whether to append now
    happens inside the same lock as the append."""
    fd = os.open(OUT_CSV, os.O_RDWR | os.O_CREAT, 0o644)
    with os.fdopen(fd, "r+", newline="", encoding="utf-8") as f:
        fcntl.flock(f.fileno(), fcntl.LOCK_EX)
        try:
            f.seek(0)
            body = f.read()
            needs_header, legacy = _inspect_header(body)
            if legacy:
                print("NOTE: " + OUT_CSV + " was written by the version with the "
                      "wrong decision price, the wrong benchmark and no split "
                      "handling. Those rows cannot be compared with anything "
                      "written since, so the record is being started again from "
                      "this run.")
                f.seek(0)
                f.truncate(0)
                body = ""
            last = _last_run_date(body)
            if weekly_only and last and (dt.date.today() - last).days < 7:
                print("Another run recorded " + last.isoformat() +
                      " while this one was working. Nothing appended.")
                return False
            f.seek(0, os.SEEK_END)
            if body and not body.endswith("\n"):
                f.write("\n")
            w = csv.writer(f)
            if needs_header:
                w.writerow(CSV_COLS)
            for r in graded:
                w.writerow(_row_values(r, run_utc))
            f.flush()
            os.fsync(f.fileno())
        finally:
            fcntl.flock(f.fileno(), fcntl.LOCK_UN)
    return True


# --------------------------------------------------------------------------
# The report Ben reads
# --------------------------------------------------------------------------

def describe(r):
    """A name the way Ben should read it: what it is, in eight words or fewer."""
    label = r["name"] or r["ticker"]
    what = eight_words(r["what"])
    if not what:
        return label + " (" + r["ticker"] + "), no description in the record"
    return label + " (" + r["ticker"] + "), " + what


def spread_line(vals, with_count=True):
    """Count, average, middle and range -- never the average on its own."""
    n = len(vals)
    if n == 0:
        return "no names"
    if n == 1:
        return "one name, at %+.1f points" % vals[0]
    head = ("%d names, " % n) if with_count else ""
    return (head + "average %+.1f, middle %+.1f, worst %+.1f, best %+.1f"
            % (statistics.mean(vals), statistics.median(vals), min(vals), max(vals)))


def write_md(graded, skipped, window_days, run_utc, total_candidates):
    scored = [r for r in graded if r["scored"] and r.get("excess_pts") is not None]
    early = [r for r in graded if not r["scored"]]
    declines = [r for r in scored if r["group"] in ("declined", "waiting")]

    L = []
    L.append("# Did the names we turned down go on to do well?\n")
    L.append("Generated " + run_utc + ". This file answers one question: when the "
             "engine said no or said wait, what did that name do afterwards, "
             "compared with simply holding an index fund instead.\n")

    L.append("\n## How to read every number here\n")
    L.append("- A **percentage point** is the difference between two percentages. "
             "If a name rose 12% and the index rose 5%, the name beat the index by "
             "7 percentage points.\n")
    L.append("- Each name is compared with **one** index fund, chosen from that "
             "company's own industry and never changed afterwards. Chip and "
             "chip-equipment companies are compared with " + BENCH_LONG[BENCH_CHIPS] +
             ". Everything else, including AI cloud landlords, power equipment and "
             "software, is compared with " + BENCH_LONG[BENCH_BROAD] + ". Which fund "
             "was used is written next to every name, and in the file "
             "`decision_grades.csv`.\n")
    L.append("- A company's return is measured **in its own currency**; the two "
             "index funds are priced in US dollars. For a company that trades "
             "outside the United States, the comparison therefore leaves out the "
             "exchange-rate move between the two. That is deliberate: the analyst "
             "decided the company, not the currency.\n")
    L.append("- Every price is a **settled closing price**. No intraday quote and "
             "no after-hours print is used anywhere.\n")
    L.append("- A decision is only given a result once it is at least " +
             str(window_days) + " days old. Younger ones are listed and marked too "
             "early to judge.\n")

    L.append("\n## The headline\n")
    if not declines:
        L.append("Nothing is old enough to judge yet. " + str(len(early)) + " decisions "
                 "are being tracked and none of them has reached " + str(window_days) +
                 " days. That is a real answer, not a missing one: the engine is "
                 "younger than the shortest window over which a call can fairly be "
                 "measured.\n")
    else:
        beat = sum(1 for r in declines if r["excess_pts"] > 0)
        vals = [r["excess_pts"] for r in declines]
        L.append("We declined or parked " + str(len(declines)) + " names that are now "
                 "old enough to judge. Of those, **" + str(beat) + " went on to beat "
                 "the index fund each is compared with**, and " +
                 str(len(declines) - beat) + " did not.\n")
        L.append("\nAcross all " + str(len(declines)) + ": " + spread_line(vals, False) +
                 " percentage points against their own index. Read that against the "
                 "alternative, not against zero -- a name that fell while its index "
                 "fell further was still the right thing to avoid.\n")
        L.append("\nThese " + str(len(declines)) + " results are not " +
                 str(len(declines)) + " independent pieces of evidence. Most were "
                 "measured over overlapping periods and many sit in the same few "
                 "industries, so one sector-wide move shows up many times over. The "
                 "number of genuinely independent observations is smaller than the "
                 "count, and this file cannot say how much smaller.\n")

    if declines:
        L.append("\n## The same results, grouped by the reason we gave\n")
        L.append("This is the table worth reading, once there is enough in it. It "
                 "shows how names fared after each kind of objection. It does not "
                 "show that the objection caused the outcome -- nothing here "
                 "separates the reason from whatever else moved the sector that "
                 "month.\n")
        L.append("\n| Why we declined | Names | Average gap vs its index | Range, worst to best | What can be read from it |")
        L.append("|---|---|---|---|---|")
        groups = {}
        for r in declines:
            groups.setdefault(r["reason"], []).append(r["excess_pts"])
        for reason, vals in sorted(groups.items(), key=lambda kv: statistics.mean(kv[1])):
            m = statistics.mean(vals)
            rng = "%+.1f to %+.1f points" % (min(vals), max(vals)) if len(vals) > 1 else "single name"
            if len(vals) < 8:
                note = "still too few to read anything into"
            else:
                note = ("eight or more calls, but overlapping periods and shared "
                        "industries mean fewer than " + str(len(vals)) + " independent "
                        "observations; a direction to investigate, not evidence")
            L.append("| " + reason + " | " + str(len(vals)) + " | " +
                     ("%+.1f points" % m) + " | " + rng + " | " + note + " |")
        L.append("\nA group needs at least eight results before anything is said "
                 "about it at all, and eight is still too few to read anything into. "
                 "It is a floor below which the number is noise wearing a decimal "
                 "point, not a threshold at which the number becomes evidence.\n")

        risers = sorted([r for r in declines if r["excess_pts"] > 0],
                        key=lambda r: -r["excess_pts"])[:10]
        if risers:
            L.append("\n## The names we turned down that have risen most since\n")
            L.append("These are worth re-reading. Each was declined or parked, and "
                     "each has since outrun the index fund it is measured against. "
                     "Whether the original objection was wrong is a separate "
                     "question this file cannot answer.\n")
            L.append("\n| Company | Decided on | Price then | Price now | Currency | Compared with | Ahead by |")
            L.append("|---|---|---|---|---|---|---|")
            for r in risers:
                L.append("| " + describe(r) + " | " + r["date"].isoformat() + " | " +
                         "{:,.2f}".format(r["price_used"]) + " | " +
                         "{:,.2f}".format(r["price_now"]) + " | " +
                         (r["quote_ccy"] or "not recorded") + " | " +
                         BENCH_SHORT[r["benchmark"]] + " | " +
                         ("%+.1f points" % r["excess_pts"]) + " |")
            L.append("\nPrices then and now are settled closes in the currency named "
                     "in the row. The most recent close used is dated " +
                     max(r["price_now_asof"] for r in risers) + ".\n")

    if early:
        L.append("\n## Too early to judge -- " + str(len(early)) + " decisions\n")
        L.append("These are younger than " + str(window_days) + " days. They are "
                 "tracked and will be given a result automatically once they reach "
                 "that age.\n")

        interim = [r for r in early
                   if r["group"] in ("declined", "waiting")
                   and r.get("excess_pts") is not None]
        if interim:
            beat = sum(1 for r in interim if r["excess_pts"] > 0)
            vals = [r["excess_pts"] for r in interim]
            L.append("\n### An early reading, which is not a result\n")
            L.append("Over a few weeks this measures which way the market went, not "
                     "whether our judgement was any good. Use it to notice a "
                     "direction. Do not use it to change a rule.\n")
            L.append("\nOf " + str(len(interim)) + " names we declined or parked, **" +
                     str(beat) + " have since risen more than the index fund each is "
                     "measured against** and " + str(len(interim) - beat) + " have "
                     "not. Across all of them: " + spread_line(vals, False) +
                     " percentage points.\n")
            groups = {}
            for r in interim:
                groups.setdefault(r["reason"], []).append(r["excess_pts"])
            L.append("\n| Why we declined | Names | Average gap so far | Range, worst to best |")
            L.append("|---|---|---|---|")
            for reason, vals in sorted(groups.items(), key=lambda kv: statistics.mean(kv[1])):
                rng = ("%+.1f to %+.1f points" % (min(vals), max(vals))) if len(vals) > 1 else "single name"
                L.append("| " + reason + " | " + str(len(vals)) + " | " +
                         ("%+.1f points" % statistics.mean(vals)) + " | " + rng + " |")
            L.append("\nEvery group above is below the eight-name floor, below the "
                     "age floor, or both. The averages sit inside their own ranges "
                     "with room to spare, which is another way of saying the spread "
                     "is wider than the signal. Read the direction, ignore the "
                     "decimals.\n")

    if graded:
        bench_counts = {}
        for r in graded:
            bench_counts[r["benchmark"]] = bench_counts.get(r["benchmark"], 0) + 1
        L.append("\n## Which index each name is measured against\n")
        L.append("Each name is fixed to one index for the whole of its life in this "
                 "file. Before 2026-08-01 every name was compared with the chip "
                 "fund, including software and power-equipment companies, which "
                 "flattered or punished them by whatever the chip cycle happened to "
                 "be doing.\n\n")
        for b in BENCHMARKS:
            if bench_counts.get(b):
                L.append("- " + str(bench_counts[b]) + " names are compared with " +
                         BENCH_LONG[b] + ".\n")

    L.append("\n## What this report could not see\n")
    total = total_candidates
    L.append("Of " + str(total) + " decisions in the record, " + str(len(graded)) +
             " could be measured and " + str(len(skipped)) + " could not. The gap is "
             "a bookkeeping problem, not an absence of decisions.\n")
    if skipped:
        by, who = {}, {}
        for tk, dec, why in skipped:
            by[why] = by.get(why, 0) + 1
            who.setdefault(why, []).append(tk)
        L.append("\n| Why it could not be measured | Decisions |")
        L.append("|---|---|")
        for why, n in sorted(by.items(), key=lambda kv: -kv[1]):
            L.append("| " + why + " | " + str(n) + " |")
        L.append("\nThe rows behind each line, so they can be found and repaired:\n")
        measured = {r["ticker"] for r in graded}
        starred = False
        for why, n in sorted(by.items(), key=lambda kv: -kv[1]):
            out = []
            for tk in sorted(who[why]):
                if tk in measured:
                    out.append(tk + " \\*")
                    starred = True
                else:
                    out.append(tk)
            L.append("- *" + why + "* — " + ", ".join(out) + "\n")
        if starred:
            L.append("\nA star means the company IS measured in this file, from a "
                     "different record of the same decision -- usually its entry in "
                     "the kill log, which stores a price and a date together by "
                     "design. It is the watchlist row for that company that cannot "
                     "be paired, and it is the watchlist row that needs repairing.\n")
        dropped_pair = by.get(DROP_PAIR, 0) + by.get(DROP_PAIR_CONTRADICTS, 0) + by.get(DROP_PRICE_UNDATED, 0)
        if dropped_pair:
            L.append("\n**" + str(dropped_pair) + " of those were dropped for one "
                     "specific reason and it is the important one.** For each of "
                     "them the record holds a price and a decision date that come "
                     "from different days -- typically a price captured when the "
                     "name was first written down, weeks before the call was "
                     "actually made. Measuring from the earlier price would credit "
                     "or blame the decision for a move that happened before anyone "
                     "decided anything. Until each of those rows carries the price "
                     "on the day of the call, those decisions cannot be graded at "
                     "all, and no estimate is offered in their place.\n")
        unproven = by.get(DROP_UNPROVEN, 0)
        if unproven:
            L.append("\n" + str(unproven) + " more were dropped because the stored "
                     "price does not match any settled close within " +
                     str(PRICE_PROOF_WINDOW_DAYS) + " days of the decision date, to "
                     "within " + ("%.1f" % PRICE_PROOF_TOLERANCE_PCT) + "%. That "
                     "catches a price recorded in the wrong currency, a mistyped "
                     "figure, and a share split the feed knows about but the record "
                     "does not.\n")

    L.append("\n## What accumulates, and what it is not\n")
    L.append("Every run appends one row per measurable decision to "
             "`decision_grades.csv`. That file therefore holds one row per "
             "decision **per run**, so its row count is not a count of decisions "
             "and must never be read as a sample size. The same decision "
             "re-measured next week is the same decision, not a second "
             "observation.\n")
    L.append("\nWhat the accumulating file is genuinely good for is watching a "
             "single decision's result move over time, and seeing when a group of "
             "reasons finally has enough separate calls in it to be worth looking "
             "at. It is not a growing body of evidence about whether the reasons "
             "are any good; that would need calls made at different times, in "
             "different industries, under different market conditions, and this "
             "book is a few weeks old.\n")

    with open(OUT_MD, "w", encoding="utf-8") as f:
        f.write("\n".join(L) + "\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--window", type=int, default=DEFAULT_WINDOW_DAYS,
                    help="days before a decision is given a result (default 90)")
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--weekly-only", action="store_true",
                    help="exit quietly if this already ran within the last 7 days. "
                         "Lets the scheduled chain call it every run while it "
                         "actually works once a week.")
    a = ap.parse_args()

    # D4. The record is validated before any work is done, so a corrupt or
    # future-dated history fails loudly and immediately instead of being
    # swallowed. This used to sit inside a bare `except Exception: pass`.
    last = read_history_state()
    if a.weekly_only and last and (dt.date.today() - last).days < 7:
        due = 7 - (dt.date.today() - last).days
        print("Last graded " + last.isoformat() + "; next run due in " + str(due) +
              " day(s). Skipping.")
        return

    run_utc = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rows, unpairable = gather()
    graded, dropped = grade(rows, a.window)
    # `rows` are the candidates that survived pairing; `dropped` are the ones the
    # market data then refused to confirm. Every decision is in exactly one of
    # graded / unpairable / dropped, so the total counts each decision once.
    skipped = unpairable + dropped
    total_candidates = len(graded) + len(skipped)

    scored = [r for r in graded if r["scored"] and r.get("excess_pts") is not None]
    print("Decisions in the record: " + str(total_candidates) +
          "  measurable: " + str(len(graded)) +
          "  old enough for a result: " + str(len(scored)) +
          "  could not be measured: " + str(len(skipped)))
    by = {}
    for tk, dec, why in skipped:
        by[why] = by.get(why, 0) + 1
    for why, n in sorted(by.items(), key=lambda kv: -kv[1]):
        print("    " + str(n) + "  " + why)
    if scored:
        d = [r for r in scored if r["group"] in ("declined", "waiting")]
        if d:
            vals = [r["excess_pts"] for r in d]
            print("Declined or parked and old enough: " + str(len(d)) +
                  "; beat their own index: " + str(sum(1 for v in vals if v > 0)) +
                  "; " + spread_line(vals) + " percentage points")
    else:
        print("Nothing has aged past the scoring window yet -- too early by window.")

    if a.dry_run:
        print("(dry run -- nothing written)")
        return

    # D4(d). The report Ben reads is written FIRST. Completion is recorded only
    # by the CSV append, so a failure here leaves the job un-recorded and the
    # next run repairs it, instead of the timestamp claiming success while the
    # human-readable report sits stale for a week.
    write_md(graded, skipped, a.window, run_utc, total_candidates)
    print("Wrote " + OUT_MD)
    if append_csv(graded, run_utc, a.weekly_only):
        print("Wrote " + OUT_CSV)


if __name__ == "__main__":
    main()
