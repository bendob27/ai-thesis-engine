#!/usr/bin/env python3
"""Fetch live market data for tickers — computed from raw fields, never from the
vendor's own multiples (rebuilt 2026-08-11, upgrade brief 7.4).

Why the rebuild: this tool feeds analysis sessions, so its numbers travel
upstream into verdicts — and until 2026-08-11 it printed exactly the
pre-computed yfinance fields the engine's own standing rules ban from citation
(forwardPE, enterpriseToRevenue, margins, shortPercentOfFloat). Every logged
data failure lives in those fields: ASML EV/S printed 1,159 vs a real ~15-16x,
a fwd P/E of 121.6x vs ~45-70x on guidance, MU YTD +2.1% vs a verified +242%.

Now:
  COMPUTED — price is the last SETTLED CLOSE with its date; share count is
  market cap / close (the house derivation that survives dual-class filers);
  trailing P/E, EV/S and margins are computed here from raw quarterly statement
  rows; revenue growth is latest quarter vs the same quarter a year ago, basis
  stated. If the statements are priced in a different currency than the stock
  (a documented yfinance trap), the mixed ratios print n/a with a loud flag
  instead of a silently wrong number.
  VENDOR CONTEXT — analyst target/count, forward P/E, short % of float — is
  printed in its own clearly-labeled section. Context for a conversation,
  never a decision input; the engine's rules ban citing these as facts.

Usage:
    python3 fetch_market_data.py NVDA VRT GEV
    python3 fetch_market_data.py --json NVDA VRT
Every output is timestamped. If a field is unavailable, it prints n/a — never guess.
"""
import argparse
import json
import sys
from datetime import datetime, timezone


def num(v):
    return v if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def fmt(v, pct=False, money=False):
    if v is None:
        return "n/a"
    try:
        if pct:
            return f"{v * 100:.1f}%"
        if money:
            for unit, div in (("T", 1e12), ("B", 1e9), ("M", 1e6)):
                if abs(v) >= div:
                    return f"{v / div:.2f}{unit}"
            return f"{v:,.0f}"
        return f"{v:,.2f}"
    except (TypeError, ValueError):
        return str(v)


def stmt_row(df, *names):
    """Latest-first list of values for the first matching row label, else None."""
    try:
        if df is None or df.empty:
            return None
        for n in names:
            if n in df.index:
                vals = [num(x) for x in df.loc[n].tolist()]
                return vals if any(v is not None for v in vals) else None
    except Exception:
        pass
    return None


def ttm(vals):
    """Sum of the four most recent quarters, or None if fewer than 4 are real."""
    if not vals:
        return None
    got = [v for v in vals[:4] if v is not None]
    return sum(got) if len(got) == 4 else None


def fetch_ticker(symbol):
    import yfinance as yf

    t = yf.Ticker(symbol)
    info = t.info or {}

    row = {"ticker": symbol, "name": info.get("shortName") or info.get("longName"),
           "currency": info.get("currency"), "flags": [], "computed_basis": {}}

    # --- settled close + return windows + moving averages: all from history() ------
    close = close_date = dma50 = dma200 = None
    try:
        h = t.history(period="1y")["Close"].dropna()
        if len(h) > 0:
            close = float(h.iloc[-1])
            close_date = str(h.index[-1].date())
            if len(h) >= 50:
                dma50 = float(h.tail(50).mean())
            if len(h) >= 200:
                dma200 = float(h.tail(200).mean())
    except Exception:
        pass
    row.update(close=close, close_date=close_date, dma50=dma50, dma200=dma200)
    for key, period in (("ytd_pct", "ytd"), ("w52_pct", "1y")):
        row[key] = None
        try:
            closes = t.history(period=period)["Close"].dropna()
            if len(closes) > 1:
                row[key] = float(closes.iloc[-1] / closes.iloc[0] - 1)
        except Exception:
            pass

    # --- share count and market cap: the house derivation ---------------------------
    mcap = num(info.get("marketCap"))
    shares = (mcap / close) if (mcap and close) else None
    row["market_cap"] = mcap
    row["computed_basis"]["shares"] = ("market cap / last close — survives dual-class "
                                       "filers whose sharesOutstanding returns one class")

    # --- raw statements; refuse mixed currencies rather than mixing them ------------
    fin_ccy = info.get("financialCurrency")
    mixed = bool(fin_ccy and row["currency"] and fin_ccy != row["currency"])
    if mixed:
        row["flags"].append(f"statements are in {fin_ccy}, the stock trades in "
                            f"{row['currency']} — ratio lines withheld rather than "
                            f"mixed (documented vendor trap); convert by hand if needed")

    inc = bal = None
    try:
        inc = t.quarterly_income_stmt
    except Exception:
        pass
    try:
        bal = t.quarterly_balance_sheet
    except Exception:
        pass

    rev = stmt_row(inc, "Total Revenue", "Operating Revenue")
    gp = stmt_row(inc, "Gross Profit")
    op = stmt_row(inc, "Operating Income", "Total Operating Income As Reported")
    ni = stmt_row(inc, "Net Income", "Net Income Common Stockholders")
    debt = stmt_row(bal, "Total Debt")
    cash = stmt_row(bal, "Cash And Cash Equivalents",
                    "Cash Cash Equivalents And Short Term Investments")

    rev_ttm, ni_ttm, gp_ttm, op_ttm = ttm(rev), ttm(ni), ttm(gp), ttm(op)

    row["trailing_pe"] = row["ev_to_sales"] = row["gross_margin"] = None
    row["op_margin"] = row["rev_growth_yoy_q"] = None
    if not mixed:
        if close and shares and ni_ttm and ni_ttm > 0:
            row["trailing_pe"] = (close * shares) / ni_ttm
            row["computed_basis"]["trailing_pe"] = "close x derived shares / TTM net income (4 quarters summed)"
        if mcap and rev_ttm and debt is not None and cash is not None \
                and debt[0] is not None and cash[0] is not None:
            row["ev_to_sales"] = (mcap + debt[0] - cash[0]) / rev_ttm
            row["computed_basis"]["ev_to_sales"] = "(mcap + total debt - cash) / TTM revenue, one currency"
        if gp_ttm and rev_ttm:
            row["gross_margin"] = gp_ttm / rev_ttm
        if op_ttm and rev_ttm:
            row["op_margin"] = op_ttm / rev_ttm
        if rev and len(rev) >= 5 and rev[0] and rev[4]:
            row["rev_growth_yoy_q"] = rev[0] / rev[4] - 1
            row["computed_basis"]["rev_growth"] = "latest quarter vs same quarter a year ago"

    # An EDGAR-auditor-style self-check: summed quarters vs the vendor's own TTM
    # revenue field, when it offers one. >2% apart -> the computed line wins but
    # carries a flag instead of silent confidence.
    v_rev = num(info.get("totalRevenue"))
    if rev_ttm and v_rev and abs(rev_ttm - v_rev) / v_rev > 0.02:
        row["flags"].append(f"summed 4-quarter revenue {fmt(rev_ttm, money=True)} vs "
                            f"vendor TTM {fmt(v_rev, money=True)} — >2% apart, "
                            f"check the filing before citing either")

    # --- vendor context: labeled, quarantined, never decision inputs ----------------
    row["vendor_context"] = {
        "fwd_pe": num(info.get("forwardPE")),
        "analyst_target": num(info.get("targetMeanPrice")),
        "analyst_count": info.get("numberOfAnalystOpinions"),
        "short_pct_float": num(info.get("shortPercentOfFloat")),
    }
    return row


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()

    try:
        import yfinance  # noqa: F401
    except ImportError:
        sys.exit("yfinance not installed. Run: pip3 install --user yfinance")

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    rows, errors = [], {}
    for s in args.tickers:
        try:
            rows.append(fetch_ticker(s.upper()))
        except Exception as e:  # noqa: BLE001
            errors[s.upper()] = str(e)

    if args.json:
        print(json.dumps({"as_of": stamp, "data": rows, "errors": errors}, indent=2))
        return

    print(f"Data as of {stamp} (raw fields via yfinance; every ratio computed here)\n")
    hdr = (f"{'TICKER':<10}{'CLOSE':>10}{'DATE':>12}{'YTD':>9}{'52W':>9}{'MCAP':>8}"
           f"{'P/E ttm':>9}{'EV/S':>7}{'REVq YoY':>9}{'GM ttm':>8}{'OM ttm':>8}{'vs200d':>8}")
    print(hdr)
    print("-" * len(hdr))
    for r in rows:
        vs200 = (r["close"] / r["dma200"] - 1) if (r["close"] and r["dma200"]) else None
        print(f"{r['ticker']:<10}"
              f"{fmt(r['close']):>10}"
              f"{(r['close_date'] or 'n/a'):>12}"
              f"{fmt(r['ytd_pct'], pct=True):>9}"
              f"{fmt(r['w52_pct'], pct=True):>9}"
              f"{fmt(r['market_cap'], money=True):>8}"
              f"{fmt(r['trailing_pe']):>9}"
              f"{fmt(r['ev_to_sales']):>7}"
              f"{fmt(r['rev_growth_yoy_q'], pct=True):>9}"
              f"{fmt(r['gross_margin'], pct=True):>8}"
              f"{fmt(r['op_margin'], pct=True):>8}"
              f"{fmt(vs200, pct=True):>8}")
    print("\nBasis: close = last settled close (dated); shares = mcap/close; P/E, EV/S "
          "and margins from summed quarterly filings; growth = latest Q vs year-ago Q.")

    any_ctx = any(v is not None for r in rows for v in r["vendor_context"].values())
    if any_ctx:
        print("\nVENDOR CONTEXT — conversation context only, NEVER decision inputs "
              "(the engine's rules ban citing these as facts):")
        for r in rows:
            c = r["vendor_context"]
            n = c.get("analyst_count")
            print(f"  {r['ticker']:<10} fwd P/E {fmt(c['fwd_pe'])} · analyst target "
                  f"{fmt(c['analyst_target'])} ({n if n else '?'} analysts) · "
                  f"short {fmt(c['short_pct_float'], pct=True)} of float "
                  f"(second-source at FINRA before any use)")

    for r in rows:
        for f in r.get("flags", []):
            print(f"\nWARNING {r['ticker']}: {f}")
    for s, e in errors.items():
        print(f"\nERROR {s}: {e}")
    print("\nNote: verify surprising values against a second source before using in analysis.")


if __name__ == "__main__":
    main()
