#!/usr/bin/env python3
"""Credit-temperature meter — Marks/Oaktree's cycle thermometer, mechanized.

A METER, NEVER A GATE (Ben adoption 2026-07-23, from the 07-22 Oaktree source study;
same governance as timing_gauge.py and accounting_quality.py). It informs the Regime
read and the funding-fragility watch; it never blocks or triggers a trade by itself.

Market inputs (auto, FRED fredgraph.csv, no API key):
  BAMLH0A0HYM2  ICE BofA US High Yield OAS        (percent; 2.68 = 268bps)
  BAMLH0A1HYBB  ICE BofA BB OAS
  BAMLH0A3HYC   ICE BofA CCC & Lower OAS
Quarterly hand-entered inputs (OCQ / memo data, each with its own as-of date) live in
HAND_INPUTS below — refresh when a new Oaktree Credit Quarterly lands (sweep watches it).

State rules (untuned first cut, documented so /review can grade them):
  COMPLACENT  HY OAS < 330bps AND within 60bps of its 252-trading-day low
              (Marks, Gimme Credit 03-2025: ~290bps = "one of the narrowest spreads on
               record"; his stated normal range 350-550, revised 400-600)
  NORMAL      330-550bps, not within the complacent band
  TIGHTENING  HY OAS has widened >=75bps off its 252d low but remains <550bps,
              OR CCC-BB dispersion >= 700bps while HY < 550 (the OCQ "dispersion"
              regime: index calm, junk-of-the-junk repricing first)
  STRESSED    HY OAS >= 550bps (top of Marks's normal band; distress economics begin)
Trend arrow = 60-trading-day change in HY OAS.

Self-audit (DATA-desk standing rule, 2026-07-10): the meter REFUSES to print a reading
when (a) the credit-quality ordering CCC > HY > BB fails (series mixup), or (b) the
freshest observation is older than 7 calendar days. Hand inputs older than 200 days are
DROPPED from the read with a notice, never silently used (funding_clock freshness rule).

Outputs: stdout table · book/credit_temperature.md (overwrite) ·
book/credit_temperature.csv (append a row only when the state CHANGES — funding_clock
pattern). Manual runs; daily-chain wiring is a plist edit that needs Ben's separate yes.
"""
import csv
import io
import sys
import urllib.request
from datetime import date, datetime, timedelta
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent   # .claude/skills/ai-thesis
BOOK = BASE / "book"
MD_OUT = BOOK / "credit_temperature.md"
CSV_OUT = BOOK / "credit_temperature.csv"

SERIES = {
    "hy": "BAMLH0A0HYM2",
    "bb": "BAMLH0A1HYBB",
    "ccc": "BAMLH0A3HYC",
}

# Quarterly hand-entered block — refresh on each OCQ / memo release. Dates are the
# DATA as-of dates (not our entry date). Sources in the 07-22 Oaktree study.
HAND_INPUTS = [
    # (label, value-as-shown, as-of ISO date, source). Ben reads these labels, so they are
    # written as questions in plain English and every abbreviation is spelled out.
    ("How much of the trouble in company loans is software and IT companies",
     "More than 40%. Software companies on their own are 36.3% of the troubled loans, while "
     "being about 7% of the loan market.",
     "2026-03-03", "Deutsche Bank's default monitor, quoted in Oaktree's Credit Quarterly for "
                   "the first quarter of 2026"),
    ("What lenders think loans are worth when the borrower pays interest in more debt "
     "instead of cash",
     "91 cents on the dollar.",
     "2026-04-13", "Goldman Sachs private-credit monitor, quoted in Oaktree's Credit Quarterly "
                   "for the first quarter of 2026"),
    ("How much of the interest income at listed private-lending funds is paid in more debt "
     "rather than cash",
     "About 10%. At the funds that never wind up, about 4%.",
     "2026-05-01", "Oaktree's Credit Quarterly for the first quarter of 2026"),
    ("How much lenders who are first in line get back when a borrower fails",
     "37.7% to 40% of what they lent, against a 62.3% average over the past 25 years.",
     "2026-04-01", "JPMorgan, quoted in Oaktree's Credit Quarterly for the fourth quarter of "
                   "2025 and the first quarter of 2026"),
    ("How much of each lending market is software companies",
     "20% to 30% of loans made directly by investment funds. 10% to 15% of the big loans banks "
     "arrange and sell on. 4% to 5% of publicly traded high-risk company bonds.",
     "2026-04-09", 'the Howard Marks memo "What\'s Going on in Private Credit?"'),
]
HAND_STALE_DAYS = 200

DISPERSION_TIGHT_BPS = 700
COMPLACENT_LEVEL_BPS = 330
COMPLACENT_OFF_LOW_BPS = 60
TIGHTENING_OFF_LOW_BPS = 75
STRESSED_BPS = 550
TREND_WINDOW_TD = 60
LOW_WINDOW_TD = 252


def pp(bps):
    """Hundredths of a percent, written the way a reader can actually use them.

    The bond market quotes these gaps in "basis points" — 284 means 2.84 percentage
    points of extra interest. Ben reads this report, the abbreviation is banned in
    anything he reads, and the raw number is meaningless without it. Everything the
    report shows goes through here; the CSV history keeps the raw figure."""
    return f"{bps / 100:.2f} percentage points"


def fetch_series(fred_id):
    url = f"https://fred.stlouisfed.org/graph/fredgraph.csv?id={fred_id}"
    with urllib.request.urlopen(url, timeout=45) as r:
        text = r.read().decode()
    rows = []
    for rec in csv.reader(io.StringIO(text)):
        if len(rec) != 2 or rec[0] in ("DATE", "observation_date"):
            continue
        try:
            rows.append((date.fromisoformat(rec[0]), float(rec[1]) * 100))  # % -> bps
        except ValueError:
            continue  # missing obs "."
    if not rows:
        raise RuntimeError(f"{fred_id}: no parseable observations")
    return rows


def main():
    data = {k: fetch_series(v) for k, v in SERIES.items()}
    asof = {k: v[-1][0] for k, v in data.items()}
    latest = {k: v[-1][1] for k, v in data.items()}

    # ---- self-audit ----
    problems = []
    if not (latest["ccc"] > latest["hy"] > latest["bb"]):
        problems.append(
            "the weakest borrowers should always pay more than the average, and the average "
            f"more than the strongest. Today the weakest read {latest['ccc']:.0f}, the average "
            f"{latest['hy']:.0f} and the strongest {latest['bb']:.0f}, which is impossible — "
            "the three data series have been mixed up somewhere")
    stalest = min(asof.values())
    if (date.today() - stalest).days > 7:
        problems.append(f"the newest figure available is from {stalest}, more than a week old")
    if problems:
        print("This reading is not safe to use. Reasons:")
        for p in problems:
            print(" -", p)
        sys.exit(1)

    hy_hist = [v for _, v in data["hy"]]
    hy = latest["hy"]
    hy_low = min(hy_hist[-LOW_WINDOW_TD:])
    hy_chg60 = hy - hy_hist[-TREND_WINDOW_TD] if len(hy_hist) >= TREND_WINDOW_TD else 0.0
    dispersion = latest["ccc"] - latest["bb"]

    # ---- state ----
    # `state` is the machine label, written to the CSV history and never shown to Ben.
    # `headline` and `why` are the plain-English versions that go into the report.
    if hy >= STRESSED_BPS:
        state = "STRESSED"
        headline = "Lenders are frightened, and the weakest borrowers are being cut off"
        why = (f"a typical risky company now pays {pp(hy)} more than the US government to "
               f"borrow, at or above the {pp(STRESSED_BPS)} that marks real distress")
    elif (hy - hy_low) >= TIGHTENING_OFF_LOW_BPS or dispersion >= DISPERSION_TIGHT_BPS:
        state = "TIGHTENING"
        headline = "Lenders are starting to charge more for risk"
        why = ((f"a typical risky company pays {pp(hy)} more than the US government to borrow, "
                f"which is {pp(hy - hy_low)} more than at the cheapest point of the past year "
                f"({pp(hy_low)})")
               if (hy - hy_low) >= TIGHTENING_OFF_LOW_BPS
               else (f"the gap between what the weakest borrowers pay and what the strongest "
                     f"pay has opened to {pp(dispersion)}, past the "
                     f"{DISPERSION_TIGHT_BPS / 100:.2f}-point level that marks a market "
                     "splitting in two, while the average stays calm"))
    elif hy < COMPLACENT_LEVEL_BPS and (hy - hy_low) <= COMPLACENT_OFF_LOW_BPS:
        state = "COMPLACENT"
        headline = "Lenders are charging almost nothing for risk"
        why = (f"a typical risky company pays only {pp(hy)} more than the US government to "
               f"borrow, under {pp(COMPLACENT_LEVEL_BPS)}, and within {pp(COMPLACENT_OFF_LOW_BPS)} "
               "of the cheapest borrowing of the past year")
    else:
        state = "NORMAL"
        headline = "Lenders are charging a normal price for risk"
        why = (f"a typical risky company pays {pp(hy)} more than the US government to borrow, "
               f"inside the ordinary {pp(COMPLACENT_LEVEL_BPS)} to {pp(STRESSED_BPS)} range")
    trend = ("has been getting more expensive" if hy_chg60 > 10
             else ("has been getting cheaper" if hy_chg60 < -10 else "has barely moved"))

    # If BOTH complacent-level and dispersion conditions hold, the read is the split
    # regime itself — surface it rather than letting one rule shadow the other.
    split = hy < COMPLACENT_LEVEL_BPS and dispersion >= DISPERSION_TIGHT_BPS

    today = date.today().isoformat()
    lines = []
    lines.append(f"# How expensive is it right now for a risky company to borrow — {today}")
    lines.append("")
    lines.append("When a company borrows, it pays more interest than the US government pays on "
                 "its own debt. That extra is what lenders charge for the risk of not being "
                 "paid back. When lenders are relaxed the extra is small, and companies can "
                 "raise money to build things. When lenders take fright the extra widens fast, "
                 "and the building stops. Most of the artificial-intelligence data-centre "
                 "construction we invest around is paid for with borrowed money, so this is the "
                 "single best early read on whether that money keeps flowing. It decides "
                 "nothing on its own and never buys or sells anything.")
    lines.append("")
    lines.append(f"**Where we are: {headline}.** In detail, {why}. Over the past three months "
                 f"this extra cost {trend}, a change of {pp(abs(hy_chg60))}.")
    if split:
        lines.append("")
        lines.append("**Two markets at once, and this is the part that matters.** The average "
                     f"risky company pays only {pp(hy)} more than the US government, which is "
                     "the sort of number you see when lenders are relaxed. But the weakest "
                     f"borrowers now pay {pp(dispersion)} more than the strongest ones. So the "
                     "average looks calm while the shakiest companies are already being charged "
                     "much more. Oaktree, the distressed-debt firm founded by Howard Marks, "
                     "reports the same pattern: trouble shows up in the weakest borrowers first "
                     "and in the average last.")
    lines.append("")
    lines.append("| What is measured | Reading | As of | What it means |")
    lines.append("|---|---|---|---|")
    lines.append(f"| Extra interest a typical risky company pays over the US government | "
                 f"{pp(hy)} | {asof['hy']} | The cheapest it got in the past year was "
                 f"{pp(hy_low)}. Howard Marks, who co-founded the distressed-debt firm Oaktree "
                 "in 1995, calls 3.50 to 5.50 percentage points the ordinary range, and has "
                 "since revised that up to 4.00 to 6.00. |")
    lines.append(f"| Extra paid by the strongest of the risky borrowers, those rated BB | "
                 f"{pp(latest['bb'])} | {asof['bb']} | BB is the top rung below investment "
                 "grade: companies lenders consider risky but sound. |")
    lines.append(f"| Extra paid by the weakest, those rated CCC or below | "
                 f"{pp(latest['ccc'])} | {asof['ccc']} | These are companies lenders think may "
                 "not repay at all. |")
    lines.append(f"| Gap between the weakest borrowers and the strongest | {pp(dispersion)} | "
                 f"{asof['ccc']} | Above {DISPERSION_TIGHT_BPS / 100:.2f} points the market has "
                 "split in two: lenders will still fund good companies and are pulling away "
                 "from weak ones. |")
    lines.append(f"| Gap between the weakest borrowers and the average | "
                 f"{pp(latest['ccc'] - hy)} | {asof['ccc']} | This is our early warning on the "
                 "money funding data-centre construction. It is one named input into the "
                 "written re-checks agreed on July 28 2026 for ASML and Taiwan Semiconductor. "
                 "On its own it never triggers anything. |")
    fresh_cut = date.today() - timedelta(days=HAND_STALE_DAYS)
    for label, value, asof_h, src in HAND_INPUTS:
        d = date.fromisoformat(asof_h)
        if d < fresh_cut:
            lines.append(f"| {label} | Dropped: the figure is from {asof_h} and is now too old "
                         f"to rely on | {asof_h} | Refresh it from the next Oaktree Credit "
                         f"Quarterly. Original source: {src}. |")
        else:
            lines.append(f"| {label} | {value} | {asof_h} | Source: {src} |")
    lines.append("")
    lines.append("How to read this page. The three market numbers come from Federal Reserve "
                 "data, updated daily, and describe four possible conditions: lenders charging "
                 "almost nothing for risk, charging a normal price, starting to charge more, or "
                 "frightened. The page refuses to print anything if the three series contradict "
                 "each other or if the newest figure is more than a week old. The hand-entered "
                 f"rows below the market ones are dropped automatically once they are "
                 f"{HAND_STALE_DAYS} days old rather than quietly ageing. Background reading: "
                 "notes/2026-07-22-oaktree-source-study.md.")
    md = "\n".join(lines) + "\n"
    MD_OUT.write_text(md)
    print(md)

    # CSV history: append only on state change
    prev_state = None
    if CSV_OUT.exists():
        rows = CSV_OUT.read_text().strip().splitlines()
        if len(rows) > 1:
            prev_state = rows[-1].split(",")[1]
    if prev_state != state:
        header_needed = not CSV_OUT.exists()
        with CSV_OUT.open("a") as f:
            if header_needed:
                f.write("date,state,hy_oas_bps,bb_oas_bps,ccc_oas_bps,dispersion_bps,hy_12m_low_bps,hy_60d_chg_bps\n")
            f.write(f"{today},{state},{hy:.0f},{latest['bb']:.0f},{latest['ccc']:.0f},{dispersion:.0f},{hy_low:.0f},{hy_chg60:+.0f}\n")
        print(f"[state change recorded: {prev_state} -> {state}]")


if __name__ == "__main__":
    main()
