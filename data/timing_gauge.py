#!/usr/bin/env python3
"""Timing gauge — trend/break state per name. READ-ONLY decision support, NEVER a gate.

Approved by Ben 2026-07-21 (staged in notes/2026-07-20-short-timing-and-unlock-design.md
Q2; valuation-card precedent: informs, never blocks). Mechanizes playbook §9.2 H-2
("size shorts only after overextension evidence, into established breaks") and the trim
side of P-06/P-15 (hold a crowded winner while the trend is intact; trim when it breaks).

DESIGN CONSTRAINT (anti-quant guard, Ben's condition): five checkable states with
conventional, untuned thresholds — no fitted parameters, no backtests, no blending
beyond a Thermometer-style flag tally. If it ever needs a regression it has left scope.

The five structural checks (each a plain fact, documented convention in parens):
  1. price below its 50-day moving average
  2. price below its 200-day moving average
  3. 50-day average below 200-day average ("death cross" — standard convention)
  4. lower high AND lower low: last-60-trading-day max AND min both below the prior
     60-day window's (the simplest swing-structure read; 60d ≈ one quarter)
  5. volatility expansion: 20-day realized vol > 1.5x 60-day realized vol
     (transitions tend to arrive with vol; 1.5x is a convention, not a fit)

Label from the tally: 0-1 INTACT · 2-3 WEAKENING · 4-5 BROKEN. The label is always
reported WITH the fired flags (Thermometer output convention, playbook §3 v1.4).

Reported alongside but NOT in the tally (different questions):
  - % off 52-week high (context, not a flag — every uptrend sits near its high)
  - deterioration_printed: has weakness reached the FILINGS yet? (latest quarterly
    revenue YoY negative, OR gross margin down ≥2pts quarter-over-quarter — computed
    from raw quarterly statements per the ratio-pipe rule; n/a when data is missing,
    never 0). "Expensive" is not deterioration; this column is what separates a
    short candidate from a mere dip.
    KNOWN QUIRK (07-21 first run): Yahoo's "Gross Profit" line for services
    companies can map to something closer to operating profit (CACI printed 9.7%
    "GM" vs its real ~33%). The QoQ-drop test is robust to a consistently-shifted
    line; the LEVEL is not — never cite gm_now_pct as a company's gross margin
    without checking the filing. Also: statements lag — a same-day report (WRT1V
    07-21) is NOT in these columns until Yahoo ingests it; rev_yoy reads the PRIOR
    quarter on report day.
  - short-side cost, US names only, INDICATIVE: sharesShort (raw Yahoo field) +
    days-to-cover computed locally as sharesShort / 30d avg volume. Standing rule:
    second-source at FINRA before ANY decision uses these.

Usage (from the skill dir):  python3 data/timing_gauge.py [--all]
  default universe: ACTIVE + MONITOR tiers of book/watchlist.csv; --all = every row.
Outputs: book/timing_gauge.csv (machine) + book/timing_gauge.md (human), timestamped.
"""
import csv, math, re, sys, datetime, os

import yfinance as yf

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from currency_units import format_money  # noqa: E402  shared: see data/currency_units.py

SKILL = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WATCHLIST = os.path.join(SKILL, "book", "watchlist.csv")
OUT_CSV = os.path.join(SKILL, "book", "timing_gauge.csv")
OUT_MD = os.path.join(SKILL, "book", "timing_gauge.md")

# --------------------------------------------------------------- plain English
# Ben reads book/timing_gauge.md. A bare ticker tells him nothing — "6488.TWO" is
# GlobalWafers, which makes blank silicon wafers — and the internal flag names
# ("below50;death_cross;LH+LL") tell him less than nothing. Everything below turns
# the machine columns into sentences. The CSV keeps the raw values untouched.

_DESCRIPTIONS = None
_PRICE_CCY = {}      # {TICKER: recorded currency code} from watchlist.csv `price_ccy`
_CCY_DISAGREE = {}   # {TICKER: (vendor code, watchlist code)} when the two disagree
_TRAILING_WORDS = {
    "and", "or", "the", "a", "an", "of", "to", "for", "with", "in", "on", "at", "that",
    "which", "who", "its", "their", "from", "by", "plus", "into", "as", "it", "is",
    "are", "this", "these", "but", "than", "then", "now", "also", "including",
}


def _short_business(text, max_words=9):
    """The opening of a company description, cut to about eight words and left
    reading as English rather than stopping mid-phrase."""
    t = (text or "").strip()
    if not t:
        return ""
    parts = [p.strip() for p in re.split(r"(?<=[a-z0-9)])\.(?:\s+|$)", t) if p.strip()]
    if not parts:
        return ""
    first = parts[0]
    if len(first.split()) < 4 and len(parts) > 1:
        first = first + ". " + parts[1]
    words = first.split()
    if len(words) <= max_words:
        return first.rstrip(",;:.")
    words = words[:max_words]
    while words and re.sub(r"[^\w]", "", words[-1]).lower() in _TRAILING_WORDS:
        words.pop()
    return " ".join(words).rstrip(",;:.") + "…"


def _load_descriptions():
    """{TICKER: (company name, what it does)} read from book/watchlist.csv at run
    time, so a name added to the watchlist is described here the same day. The
    same pass collects each row's RECORDED currency (`price_ccy`), which is what
    price_text uses — see the note on that function."""
    global _DESCRIPTIONS
    if _DESCRIPTIONS is None:
        found = {}
        try:
            csv.field_size_limit(10_000_000)  # 851KB file with long quoted cells
            with open(WATCHLIST, newline="", encoding="utf-8") as fh:
                for row in csv.DictReader(fh):
                    t = (row.get("ticker") or "").strip().upper()
                    if t:
                        found[t] = (
                            re.sub(r"\s*\([A-Z0-9.\-]{1,7}\)\s*$", "",
                                   (row.get("name") or "").strip()).strip() or t,
                            _short_business(row.get("what_they_do")))
                        # case preserved: 'GBp' is pence, 'GBP' is pounds
                        c = (row.get("price_ccy") or "").strip()
                        if c:
                            _PRICE_CCY[t] = c
        except Exception:
            pass
        _DESCRIPTIONS = found
    return _DESCRIPTIONS


def describe(ticker):
    """'**GlobalWafers (6488.TWO)** — makes blank silicon wafers'."""
    t = (ticker or "").strip()
    entry = _load_descriptions().get(t.upper()) or _load_descriptions().get(t.split(".")[0].upper())
    if not entry:
        return f"**{t}**"
    name, business = entry
    return f"**{name} ({t})** — {business}" if business else f"**{name} ({t})**"


def ccy_of(ticker, vendor_ccy=""):
    """The currency a price is quoted in, READ rather than guessed.

    REPLACES A TICKER-SUFFIX TABLE (2026-08-01). This file used to derive the
    currency from the bit after the dot — '.L' meant pence, everything unknown
    meant dollars. Both halves of that are unsound. The London exchange lists
    instruments quoted in pence, in pounds and in dollars, and the suffix does not
    say which; SGLN.L and QQ.L share a suffix and only one of them is a British
    company. An unknown suffix silently printing a dollar sign is the same guess
    in the other direction.

    Two recorded sources, in this order:
      1. the currency the price vendor returns BESIDE the price series
         (history_metadata) — the exchange's own field, and the only one
         guaranteed to describe THE VERY NUMBER being printed.
      2. `price_ccy` on the company's own watchlist row, as a fallback for when
         the vendor returns nothing.
    Neither available means the number prints bare. A missing symbol is
    recoverable; a wrong one is a hundredfold error nobody catches.

    THE VENDOR WINS ON PURPOSE, and finding out why is what set the order
    (2026-08-01). watchlist.csv records `price_ccy=HKD` for TCEHY, the US-listed
    Tencent receipt, which trades in DOLLARS — the Hong Kong line is a different
    instrument. Labelling this run's $61.43 close as
    HK$61.43 would attach one instrument's currency to another's price. A price
    and its currency have to come out of the same fetch, or they are two objects
    of the same shape again. A disagreement is printed rather than swallowed, so
    the wrong watchlist value gets fixed instead of hidden.
    """
    _load_descriptions()
    t = (ticker or "").strip().upper()
    vendor = (vendor_ccy or "").strip()
    recorded = _PRICE_CCY.get(t) or _PRICE_CCY.get(t.split(".")[0]) or ""
    if vendor and recorded and vendor != recorded and t not in _CCY_DISAGREE:
        _CCY_DISAGREE[t] = (vendor, recorded)
    return vendor or recorded


def price_text(px, ticker, day, ccy=""):
    """'₩41,450, its closing price on 2026-07-31' — currency always named."""
    return f"{format_money(px, ccy_of(ticker, ccy))}, its closing price on {day}"


# How closely we are watching a name. The internal words for these are ACTIVE,
# MONITOR, QUEUE and ARCHIVE, which mean nothing outside these files.
_WATCH_LEVEL = {"ACTIVE": "watching closely", "MONITOR": "watching",
                "QUEUE": "on the list", "ARCHIVE": "put aside for now"}

# The five price checks, in the words to use with Ben. The keys are the internal
# names written to the CSV; only the sentences reach the report.
_CHECK_WORDS = {
    "below50": "It trades below its average price over the last 50 trading days.",
    "below200": "It trades below its average price over the last 200 trading days.",
    "death_cross": "Its 50-day average price has fallen below its 200-day average.",
    "LH+LL": "Over the last three months it made both a lower peak and a lower trough "
             "than in the three months before.",
    "vol_expansion": "Its day-to-day swings this past month are more than half again as "
                     "wide as over the last three months.",
}
_TREND_WORDS = {"INTACT": "Trend still intact", "WEAKENING": "Weakening", "BROKEN": "Broken"}
_COUNT_WORDS = {0: "None", 1: "One", 2: "Two", 3: "Three", 4: "Four", 5: "Five"}


def trend_sentence(g):
    """'**Broken.** Four of the five checks are true. It trades below ...'"""
    fired = [k for k in _CHECK_WORDS if k in (g.get("flags_fired") or "").split(";")]
    n = g.get("n_flags", 0)
    head = f"**{_TREND_WORDS.get(g.get('label'), g.get('label'))}.** "
    if not fired:
        return head + "None of the five checks is true."
    return head + f"{_COUNT_WORDS.get(n, n)} of the five checks are true. " + \
        " ".join(_CHECK_WORDS[k] for k in fired)

# Rows that are topics/baskets/pre-registrations, not fetchable tickers.
PSEUDO = {"FRONTIER-LAB-IPOS", "MEM-PEAK-SHORT", "FERC-REPORTS"}

VOL_EXPANSION_X = 1.5   # convention, documented above
SWING_WIN = 60          # trading days ≈ one quarter
GM_DROP_PTS = 2.0       # gross-margin QoQ drop that counts as "printed"


def realized_vol(closes):
    rets = [math.log(closes[i] / closes[i - 1]) for i in range(1, len(closes))]
    if len(rets) < 2:
        return None
    m = sum(rets) / len(rets)
    var = sum((r - m) ** 2 for r in rets) / (len(rets) - 1)
    return math.sqrt(var) * math.sqrt(252)


def fundamentals(tk):
    """(rev_yoy_pct, gm_now_pct, gm_prev_pct) — each None when not computable."""
    rev_yoy = gm_now = gm_prev = None
    try:
        q = tk.quarterly_income_stmt
        if q is not None and not q.empty:
            cols = list(q.columns)  # newest first
            def row(name, i):
                try:
                    v = q.loc[name].iloc[i]
                    return float(v) if v == v else None
                except Exception:
                    return None
            r0 = row("Total Revenue", 0)
            if r0 and len(cols) >= 5:
                r4 = row("Total Revenue", 4)
                if r4:
                    rev_yoy = (r0 / r4 - 1) * 100
            g0 = row("Gross Profit", 0)
            if g0 and r0:
                gm_now = g0 / r0 * 100
            r1, g1 = row("Total Revenue", 1), row("Gross Profit", 1)
            if g1 and r1:
                gm_prev = g1 / r1 * 100
    except Exception:
        pass
    return rev_yoy, gm_now, gm_prev


def short_fields(tk, ticker, closes_vol):
    """US names only; INDICATIVE — second-source at FINRA before any decision."""
    if "." in ticker:
        return None, None
    try:
        info = tk.info or {}
        ss = info.get("sharesShort")
        if not ss:
            return None, None
        adv = sum(closes_vol[-30:]) / min(30, len(closes_vol)) if closes_vol else None
        dtc = ss / adv if adv else None
        return int(ss), (round(dtc, 1) if dtc else None)
    except Exception:
        return None, None


def gauge_one(ticker):
    tk = yf.Ticker(ticker)
    h = tk.history(period="2y", auto_adjust=True)
    # The exchange's own currency for this line, returned alongside the price
    # series at no extra cost. Used only when the watchlist row has no recorded
    # `price_ccy`; never inferred from the ticker. Yahoo returns 'GBp' for a
    # London line quoted in pence, so the case of this string matters.
    try:
        vendor_ccy = (getattr(tk, "history_metadata", None) or {}).get("currency") or ""
    except Exception:
        vendor_ccy = ""
    # A vendor gap used to read as calm. yfinance returns the CURRENT day's row with a NaN
    # Close when data is missing; every comparison against NaN is False, so zero flags fired
    # and the name printed INTACT. On 2026-07-24 that turned Techwing from BROKEN (4/5) into
    # INTACT (1/5) on no data at all. Drop unpriced rows first, then refuse to label at all
    # if what remains is too short: "we don't know" is a state, "nothing moved" is a claim.
    if h is not None and "Close" in h:
        h = h[h["Close"].notna()]
    if h is None or len(h) < 210:
        n = 0 if h is None else len(h)
        return {"ticker": ticker, "label": "NO-DATA" if n == 0 else "INSUFFICIENT-HISTORY",
                "note": (f"Only {n} trading days with a price came back, and this reading needs "
                         "210. Either the company has not been listed long enough, or the data "
                         "provider has gaps. Nothing is claimed about its trend either way.")}
    closes = [float(x) for x in h["Close"]]
    vols = [float(x) for x in h["Volume"]] if "Volume" in h else []
    px = closes[-1]
    asof = str(h.index[-1].date())
    dma50 = sum(closes[-50:]) / 50
    dma200 = sum(closes[-200:]) / 200
    f_b50 = px < dma50
    f_b200 = px < dma200
    f_cross = dma50 < dma200
    last, prior = closes[-SWING_WIN:], closes[-2 * SWING_WIN:-SWING_WIN]
    f_lhll = max(last) < max(prior) and min(last) < min(prior)
    v20, v60 = realized_vol(closes[-21:]), realized_vol(closes[-61:])
    f_vol = bool(v20 and v60 and v20 > VOL_EXPANSION_X * v60)
    flags = {"below50": f_b50, "below200": f_b200, "death_cross": f_cross,
             "LH+LL": f_lhll, "vol_expansion": f_vol}
    n = sum(flags.values())
    label = "INTACT" if n <= 1 else ("WEAKENING" if n <= 3 else "BROKEN")
    off_hi = (px / max(closes[-252:]) - 1) * 100

    rev_yoy, gm_now, gm_prev = fundamentals(tk)
    det = None
    if rev_yoy is not None or (gm_now is not None and gm_prev is not None):
        det = (rev_yoy is not None and rev_yoy < 0) or \
              (gm_now is not None and gm_prev is not None and gm_prev - gm_now >= GM_DROP_PTS)
    ss, dtc = short_fields(tk, ticker, vols)

    # `ccy` is deliberately NOT one of the CSV columns below — the DictWriter is
    # built with extrasaction="ignore", so the machine file keeps exactly the
    # columns it has always had. This value only reaches the human report.
    return {"ticker": ticker, "asof": asof, "px": round(px, 2), "ccy": vendor_ccy,
            "dma50": round(dma50, 2), "dma200": round(dma200, 2),
            "off_52wk_high_pct": round(off_hi, 1),
            "flags_fired": ";".join(k for k, v in flags.items() if v) or "none",
            "n_flags": n, "label": label,
            "rev_yoy_pct": (round(rev_yoy, 1) if rev_yoy is not None else "n/a"),
            "gm_now_pct": (round(gm_now, 1) if gm_now is not None else "n/a"),
            "gm_prev_pct": (round(gm_prev, 1) if gm_prev is not None else "n/a"),
            "deterioration_printed": ("n/a" if det is None else ("YES" if det else "no")),
            "shares_short_INDICATIVE": (ss if ss else "n/a"),
            "days_to_cover_INDICATIVE": (dtc if dtc else "n/a"), "note": ""}


def main():
    take_all = "--all" in sys.argv
    rows = list(csv.DictReader(open(WATCHLIST)))
    todo = []
    for r in rows:
        t = (r.get("ticker") or "").strip()
        tier = (r.get("tier") or "").strip().upper()
        status = (r.get("status") or "").strip().lower()
        if not t or t.upper() in PSEUDO or status in ("private", "pre-ipo", "topic"):
            continue
        if take_all or tier in ("ACTIVE", "MONITOR"):
            todo.append((t, tier))
    stamp = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    results = []
    for t, tier in todo:
        try:
            g = gauge_one(t)
        except Exception as e:
            g = {"ticker": t, "label": "FETCH-ERROR", "note": str(e)[:80]}
        g["tier"] = tier
        results.append(g)
        print(f"  {t:12s} {g.get('label','?'):22s} {g.get('flags_fired','')}")

    cols = ["ticker", "tier", "asof", "px", "dma50", "dma200", "off_52wk_high_pct",
            "flags_fired", "n_flags", "label", "rev_yoy_pct", "gm_now_pct",
            "gm_prev_pct", "deterioration_printed", "shares_short_INDICATIVE",
            "days_to_cover_INDICATIVE", "note"]
    with open(OUT_CSV, "w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        for g in results:
            w.writerow(g)

    order = {"BROKEN": 0, "WEAKENING": 1, "INTACT": 2, "NO-DATA": 3, "INSUFFICIENT-HISTORY": 4}
    results.sort(key=lambda g: (order.get(g.get("label"), 3), g["ticker"]))
    with open(OUT_MD, "w") as f:
        f.write(f"# Has the share price actually broken down? — {stamp}\n\n")
        f.write("This page answers two questions about every company we follow. Has its share "
                "price genuinely broken down, rather than just dipped? And has that weakness "
                "shown up yet in the company's own published results? It is background for "
                "judging when to act. It never buys or sells anything, it never blocks a "
                "decision, and Ben decides.\n\n")
        f.write("**How each reading is made.** We check five plain facts about the price. Each "
                "is simply true or false, and none of them is tuned or fitted to past data. "
                "One: the price is below its average over the last 50 trading days. Two: the "
                "price is below its average over the last 200 trading days. Three: the 50-day "
                "average has itself fallen below the 200-day average. Four: over the last three "
                "months the price made both a lower peak and a lower trough than in the three "
                "months before. Five: day-to-day swings over the last month are more than half "
                "again as wide as over the last three months. None or one true means the trend "
                "is still intact. Two or three means it is weakening. Four or five means it has "
                "broken.\n\n")
        f.write("**What the last column means.** A falling share price is not the same as a "
                "deteriorating business. That column says yes only when the company's own most "
                "recent quarterly figures show sales lower than a year earlier, or a gross "
                "margin at least 2 percentage points lower than the quarter before. An "
                "expensive share price is not deterioration. This is what separates a company "
                "in trouble from one that has merely fallen.\n\n")
        f.write("| Company | What the price is doing | Last close | Below its highest close of "
                "the past year | Sales versus a year earlier | Has the weakness reached its "
                "published results? |\n")
        f.write("|---|---|---|---|---|---|\n")
        for g in results:
            watch = _WATCH_LEVEL.get((g.get("tier") or "").upper(), "on the list")
            who = f"{describe(g['ticker'])} ({watch})"
            if g.get("label") in ("INSUFFICIENT-HISTORY", "NO-DATA", "FETCH-ERROR"):
                if g.get("label") == "FETCH-ERROR":
                    why = ("No reading. The price data could not be fetched at all today. The "
                           f"provider reported: {g.get('note', 'no reason given')}.")
                else:
                    why = g.get("note", "No reading is possible for this one.")
                f.write(f"| {who} | {why} | — | — | — | — |\n")
                continue
            off = g["off_52wk_high_pct"]
            off_txt = (f"{abs(off):.1f}% below" if off < -0.05
                       else "at its highest close of the past year")
            rev = g["rev_yoy_pct"]
            rev_txt = ("Not available" if rev == "n/a"
                       else (f"{rev}% higher" if float(rev) >= 0 else f"{abs(float(rev))}% lower"))
            det = {"YES": "Yes, in its latest published quarter",
                   "no": "Not yet",
                   "n/a": "Cannot tell — the figures are not available"}.get(
                       g["deterioration_printed"], g["deterioration_printed"])
            f.write(f"| {who} | {trend_sentence(g)} "
                    f"| {price_text(g['px'], g['ticker'], g['asof'], g.get('ccy', ''))} "
                    f"| {off_txt} | {rev_txt} | {det} |\n")
        f.write("\n*A broken price trend is a timing observation and nothing more. It is never "
                "an instruction to do anything. Betting against a company additionally needs it "
                "to pass the written screen, to be affordable to borrow, to be paired against "
                "something we own, and Ben's yes. The report also collects how many shares are "
                "being borrowed to bet against each US company, which is written to the "
                "spreadsheet beside this file rather than shown here, because that figure has "
                "to be checked against the industry regulator's own data before anyone relies "
                "on it.*\n")
    print(f"\nwrote {OUT_CSV}\nwrote {OUT_MD}\n({len(results)} names, {stamp})")
    # Not written into the report Ben reads — it is a defect in watchlist.csv, and
    # the person who can fix it reads this log. The price shown is labelled with the
    # exchange's own currency either way.
    for t, (vendor, recorded) in sorted(_CCY_DISAGREE.items()):
        print(f"  CURRENCY MISMATCH {t}: the price vendor quotes this line in {vendor}, "
              f"watchlist.csv price_ccy says {recorded}. Used {vendor} (it belongs to the "
              f"price being shown). Fix the watchlist row.")


if __name__ == "__main__":
    main()
