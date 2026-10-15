#!/usr/bin/env python3
"""The multiple ladder: what do listed growth companies actually trade at, by expected growth?

WHY (2026-09-02, Ben): the exit multiple was the single biggest lever in every valuation and
it was TYPED, not derived — 37 of 43 live cards assumed a lower future multiple with no
argument, and 25 of 27 computed maximum prices sat below the market. Ben: "we can't just
randomly assume that investors will always pay less in the future ... don't just come up
with a random multiple, but actually instantiate it and think about the trajectory of the
company." This file is the instantiation: a fixed peer set of profitable growth companies,
their current multiples computed from raw fields, bucketed by the growth the market expects
of them. A card's exit multiple is READ from this ladder at the growth rate the company is
expected to have in the year after the horizon, then argued up or down in one sentence.

WHAT IT MEASURES (labelled, because the bases differ):
  fwd_pe        price / consensus next-fiscal-year EPS (vendor EPS, usually ADJUSTED — for most
                names that means BEFORE stock pay). Computed locally from the two raw fields.
  trailing_pe   market cap / trailing four quarters of GAAP net income (raw statement rows;
                after stock-pay expense and after tax). The closer cousin of our owner earnings.
  rev_growth_fwd vendor consensus revenue growth, next fiscal year vs current.
  eps_growth_fwd vendor consensus EPS growth, next fiscal year vs current.

HOW TO APPLY: our owner earnings charge stock pay, its payroll taxes, a normal tax rate and
working capital, so they sit BELOW the vendor's adjusted EPS. Reading a forward-P/E ladder
multiple onto our owner earnings is therefore conservative, not generous. Use the trailing
GAAP column when a company's adjusted EPS is far from GAAP (large stock pay, untaxed).

Peer set is fixed on purpose (edit here, never per card): profitable growth companies across
internet, software, semis, consumer and payments. Loss-makers drop out automatically.

Usage: python3 data/multiple_ladder.py            writes book/multiple_ladder.csv and .md
"""
import csv, datetime as dt, os, statistics, sys

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(os.path.dirname(HERE), "book")
OUT_CSV = os.path.join(BOOK, "multiple_ladder.csv")
OUT_MD = os.path.join(BOOK, "multiple_ladder.md")

PEERS = ["META", "GOOGL", "AMZN", "MSFT", "AAPL", "NVDA", "AVGO", "TSM", "ASML", "KLAC", "LRCX",
         "AMAT", "ANET", "NOW", "CRM", "ADBE", "INTU", "ORCL", "PANW", "CRWD", "DDOG", "SHOP",
         "UBER", "DASH", "ABNB", "SPOT", "NFLX", "PINS", "APP", "TTD", "MELI", "COST", "CMG",
         "LULU", "TSLA", "ISRG", "MNST", "BKNG", "ADSK", "CDNS", "SNPS", "MA", "V", "AXON",
         "MDB", "ZS", "FTNT", "MPWR", "CRDO", "ALAB"]

BUCKETS = [(-1.0, 0.10, "under 10%"), (0.10, 0.20, "10-20%"), (0.20, 0.30, "20-30%"),
           (0.30, 0.45, "30-45%"), (0.45, 9.9, "over 45%")]


def one(tk):
    import yfinance as yf
    t = yf.Ticker(tk)
    row = {"ticker": tk}
    try:
        h = t.history(period="5d")["Close"].dropna()
        px = float(h.iloc[-1]); row["price"] = round(px, 2); row["price_date"] = str(h.index[-1].date())
    except Exception as e:
        row["error"] = f"price: {e}"; return row
    info = t.info or {}
    mc = info.get("marketCap")
    try:
        qi = t.quarterly_income_stmt
        ni = qi.loc["Net Income"].dropna()
        ni_ttm = float(ni.iloc[:4].sum()) if len(ni) >= 4 else None
    except Exception:
        ni_ttm = None
    # Currency trap (data-quirks): a vendor's market cap is in the trading currency while its
    # statement rows are in the reporting currency (TSM: USD price, TWD accounts -> a "1.0x" P/E).
    # Only compute the trailing multiple when the two currencies match; otherwise leave it blank.
    fin_ccy = info.get("financialCurrency"); px_ccy = info.get("currency")
    same_ccy = (fin_ccy is None) or (px_ccy is None) or (fin_ccy == px_ccy)
    row["trailing_pe"] = round(mc / ni_ttm, 1) if (mc and ni_ttm and ni_ttm > 0 and same_ccy) else None
    if not same_ccy:
        row["error"] = f"trailing P/E skipped: price in {px_ccy}, accounts in {fin_ccy}"
    try:
        ee = t.earnings_estimate
        eps0 = float(ee.loc["0y", "avg"]); eps1 = float(ee.loc["+1y", "avg"])
        row["fwd_pe"] = round(px / eps1, 1) if eps1 > 0 else None
        row["eps_growth_fwd"] = round(eps1 / eps0 - 1, 3) if eps0 > 0 else None
        row["eps_analysts"] = int(ee.loc["+1y", "numberOfAnalysts"]) if "numberOfAnalysts" in ee.columns else None
    except Exception:
        row["fwd_pe"] = None; row["eps_growth_fwd"] = None; row["eps_analysts"] = None
    try:
        re_ = t.revenue_estimate
        row["rev_growth_fwd"] = round(float(re_.loc["+1y", "growth"]), 3)
    except Exception:
        row["rev_growth_fwd"] = None
    return row


def bucket(g):
    if g is None:
        return None
    for lo, hi, name in BUCKETS:
        if lo <= g < hi:
            return name
    return None


def main():
    rows = []
    for tk in PEERS:
        r = one(tk)
        r["bucket_rev"] = bucket(r.get("rev_growth_fwd"))
        rows.append(r)
        print(f"{tk:6s} px {r.get('price')} fwdPE {r.get('fwd_pe')} trailPE {r.get('trailing_pe')} "
              f"revG {r.get('rev_growth_fwd')} epsG {r.get('eps_growth_fwd')} -> {r.get('bucket_rev')}",
              file=sys.stderr)
    cols = ["ticker", "price", "price_date", "fwd_pe", "trailing_pe", "rev_growth_fwd", "eps_growth_fwd",
            "eps_analysts", "bucket_rev", "error"]
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=cols, extrasaction="ignore"); w.writeheader()
        for r in rows: w.writerow({k: r.get(k, "") for k in cols})

    L = ["# The multiple ladder — what growth companies actually trade at, by expected growth\n"]
    L.append(f"Generated {dt.datetime.now(dt.timezone.utc):%Y-%m-%d %H:%M UTC} from a fixed peer set of "
             f"{len(PEERS)} profitable growth companies. Vendor consensus fields (yfinance) for growth and next-year "
             "earnings, prices and trailing GAAP profit from raw fields. Every multiple here is computed locally; "
             "nothing is a vendor's pre-computed ratio.\n")
    L.append("\nHow to use it: when a valuation needs the multiple a company will command at its horizon, find the "
             "row for the growth rate the company is expected to have in the YEAR AFTER the horizon, take the median, "
             "then argue it up or down in one written sentence (margins, share trend, runway). The forward column is "
             "on the vendor's adjusted earnings (before stock pay for most names); our owner earnings charge stock pay, "
             "so applying these multiples to our figure is conservative. Use the trailing GAAP column for companies "
             "whose adjusted and reported profits differ a lot.\n")
    L.append("\n| Expected revenue growth next year | Companies | Median forward P/E (adjusted EPS) | Median trailing GAAP P/E | Range of forward P/E |")
    L.append("|---|---|---|---|---|")
    for lo, hi, name in BUCKETS:
        grp = [r for r in rows if r.get("bucket_rev") == name and r.get("fwd_pe")]
        if not grp:
            L.append(f"| {name} | 0 | — | — | — |"); continue
        thin = " (THIN — under five names; read the neighbouring bucket too)" if len(grp) < 5 else ""
        name = name + thin
        f = [r["fwd_pe"] for r in grp]; tr = [r["trailing_pe"] for r in grp if r.get("trailing_pe")]
        L.append(f"| {name} | {len(grp)} ({', '.join(r['ticker'] for r in grp)}) | {statistics.median(f):.1f}x | "
                 f"{statistics.median(tr):.1f}x | {min(f):.0f}-{max(f):.0f}x |" if tr else
                 f"| {name} | {len(grp)} ({', '.join(r['ticker'] for r in grp)}) | {statistics.median(f):.1f}x | — | {min(f):.0f}-{max(f):.0f}x |")
    L.append("\n## Every company in the set\n")
    L.append("| Company | Price (date) | Forward P/E | Trailing GAAP P/E | Revenue growth next year | EPS growth next year | Analysts |")
    L.append("|---|---|---|---|---|---|---|")
    for r in sorted(rows, key=lambda x: -(x.get("rev_growth_fwd") or -9)):
        if r.get("error"):
            L.append(f"| {r['ticker']} | error: {r['error']} | | | | | |"); continue
        g = r.get("rev_growth_fwd"); eg = r.get("eps_growth_fwd")
        L.append(f"| {r['ticker']} | {r['price']} ({r['price_date']}) | {r['fwd_pe'] or '—'} | {r['trailing_pe'] or 'loss/—'} | "
                 f"{'' if g is None else f'{100*g:.0f}%'} | {'' if eg is None else f'{100*eg:.0f}%'} | {r.get('eps_analysts') or ''} |")
    L.append("\nShape warning, read before using: the ladder is NOT monotonic. The market currently pays the "
             "highest multiples for 20-30% growers and LOWER multiples for the fastest growers, which are large "
             "semiconductor names priced as cyclical. A card for a 50%-grower that reads 19x off this table is being "
             "conservative, not generous; say so in the rationale rather than silently taking the number.\n")
    L.append("\nCaveats: consensus figures are one vendor's aggregation and carry no analyst names; a company whose "
             "next-year growth is distorted by an acquisition or a one-off sits in the wrong bucket; the set is "
             "US-heavy. Re-run before each new valuation; the numbers move with the market.\n")
    open(OUT_MD, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print(f"wrote {OUT_CSV} and {OUT_MD}")


if __name__ == "__main__":
    main()
