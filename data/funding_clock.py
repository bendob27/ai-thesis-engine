#!/usr/bin/env python3
"""Funding Clock — an automated measurement device for HOW the AI buildout is financed.

This is a meter, not a hypothesis. It reads audited SEC XBRL facts (EDGAR companyconcept)
and reports, per company, which financing stage the buildout occupies and when it changed.

  S1 SELF-FUNDED      capex <= operating cash flow
  S2 EXTERNAL         capex > OCF; gap covered by debt/equity issuance
  S3 VENDOR-FINANCED  the supplier funds its own customers   (NVDA days-sales-outstanding proxy)
  S4 SECURITIZED      asset-backed / GPU-collateralised debt, SPV/VIE   [semi-auto: --fulltext]
  S5 CIRCULAR         related-party revenue from entities the seller funds [semi-auto: --fulltext]
  S6 CREDIT EVENT     spreads / downgrades / defaults          [manual: NBIS convert terms]

THE METER IS SYMMETRIC BY DESIGN. It reports the bearish reading (external funding rising)
and the bullish one (CLOUD-OUTCOME: operating cash flow re-inflecting faster than capex)
with equal prominence. H1's falsifier-(b) can resolve in EITHER direction and this device
must be able to say "the builders are winning" as loudly as "the funding is getting fragile."

GOVERNANCE. This script never edits thesis.md, playbook.md, or evidence-ledger.md.
Detection is automated; judgment is not. It prints a ready-to-paste ledger row and leaves
the amendment decision to /review with Ben's sign-off.

DATA HONESTY. Cash-flow facts are filed year-to-date, so quarters are de-cumulated by
differencing within a fiscal-year chain. Every reading prints the four quarters it summed
so the arithmetic is auditable. A missing tag reports "n/a", never 0.

Usage:
    python3 data/funding_clock.py              # read the clock; append a row only if it moved
    python3 data/funding_clock.py --fulltext   # + EDGAR full-text scan for S4/S5 language
    python3 data/funding_clock.py --force      # append a row even when nothing changed
    python3 data/funding_clock.py --verbose    # show the de-cumulated quarters per company
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys
import time
import urllib.parse
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUT_CSV = os.path.join(ROOT, "book", "funding_clock.csv")
OUT_MD = os.path.join(ROOT, "research", "funding-clock.md")

UA = {"User-Agent": os.environ.get("SEC_UA", "ai-thesis-skill research contact@example.com")}
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
CONCEPT = "https://data.sec.gov/api/xbrl/companyconcept/CIK{cik}/us-gaap/{tag}.json"
FTS = "https://efts.sec.gov/LATEST/search-index?q={q}&forms={forms}"

# Entities the clock watches. Builders first, then the supplier (S3 tell), then neoclouds.
ENTITIES = [
    ("MSFT", "Microsoft", "builder"),
    ("GOOGL", "Alphabet", "builder"),
    ("AMZN", "Amazon", "builder"),
    ("META", "Meta", "builder"),
    ("ORCL", "Oracle", "builder"),
    ("NVDA", "Nvidia", "supplier"),
    ("CRWV", "CoreWeave", "neocloud"),
]
# NBIS files 20-F under IFRS — us-gaap concepts do not resolve. Tracked manually as the
# H1 funding-fragility canary (convert/ABS terms), per CLAUDE.md standing duty.
MANUAL_ONLY = {"NBIS": "foreign private issuer (IFRS/20-F); convert terms tracked by hand"}

# Tag fallbacks, in priority order. Filers disagree about which concept to use.
TAGS = {
    "ocf": [
        "NetCashProvidedByUsedInOperatingActivities",
        "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations",
    ],
    "capex": [
        "PaymentsToAcquirePropertyPlantAndEquipment",
        "PaymentsToAcquireProductiveAssets",
        "PaymentsToAcquirePropertyPlantAndEquipmentAndIntangibleAssets",
    ],
    "debt_issued": [
        "ProceedsFromIssuanceOfLongTermDebt",
        "ProceedsFromIssuanceOfSeniorLongTermDebt",
        "ProceedsFromNotesPayable",
    ],
    "equity_issued": [
        "ProceedsFromIssuanceOfCommonStock",
        "ProceedsFromIssuanceOrSaleOfEquity",
    ],
    # Gross proceeds mostly refinance maturing paper. Only NET issuance funds a capex gap.
    "debt_repaid": [
        "RepaymentsOfLongTermDebt",
        "RepaymentsOfDebt",
        "RepaymentsOfNotesPayable",
    ],
    "revenue": [
        "RevenueFromContractWithCustomerExcludingAssessedTax",
        "Revenues",
    ],
    # Cash capex understates datacenter buildout: hyperscalers take delivery of capacity via
    # finance leases, which never touch investing cash flow. Informational, not stage-setting.
    "finance_leases": [
        "RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability",
    ],
}
AR_TAGS = ["AccountsReceivableNetCurrent", "AccountsReceivableNet"]

# S4/S5 language. Presence in a 10-K/10-Q is a FLAG to read, never a conclusion.
# Phrases are taken from the language filers ACTUALLY use — journalistic coinages like
# "GPU-backed" return zero hits, while CoreWeave's own collateral language does not.
# Queries must DISCRIMINATE. Bare '"delayed draw term loan"' returns 10,000 hits of generic
# private-credit boilerplate; paired with "GPU" it isolates the AI-collateral structures.
# Anything over FTS_NOISE_CEILING hits is reported as too-broad rather than listed.
FTS_NOISE_CEILING = 100
FTS_QUERIES = {
    "S4": [
        '"depreciable cost of GPU servers"',
        '"pledged contractual cash flows"',
        '"delayed draw term loan" "GPU"',
        '"special purpose vehicle" "GPU"',
    ],
    "S5": [
        '"cloud services agreement" "related party"',
        '"in which we hold an equity interest" "artificial intelligence"',
    ],
}


def get_json(url, tries=3):
    for i in range(tries):
        try:
            req = urllib.request.Request(url, headers=UA)
            with urllib.request.urlopen(req, timeout=30) as r:
                return json.loads(r.read().decode())
        except Exception:
            if i == tries - 1:
                return None
            time.sleep(1.5 * (i + 1))
    return None


def d(s):
    return dt.date.fromisoformat(s)


def resolve_ciks(tickers):
    data = get_json(TICKER_MAP) or {}
    want = {t.upper() for t in tickers}
    found = {}
    for row in data.values():
        t = row.get("ticker", "").upper()
        if t in want:
            found[t] = str(row["cik_str"]).zfill(10)
    return found


def fiscal_year_anchor(units):
    """Infer the fiscal-year start (month, day) from ~12-month facts.

    Needed because a fact's `start` is the only reliable way to tell a fiscal-YTD fact
    (Jan 1 -> Sep 30) from a trailing-twelve-month fact (Apr 1 -> Mar 31). Amazon files
    both, and they share start dates with quarterly facts — differencing them blindly
    produces a $119B "quarter". Fiscal years also drift for 52/53-week filers (NVDA),
    hence the +/-7 day tolerance at the call site.
    """
    starts = {}
    for f in units:
        s, e = f.get("start"), f.get("end")
        if not s or not e:
            continue
        try:
            span = (d(e) - d(s)).days
        except ValueError:
            continue
        if 350 <= span <= 380:
            key = (d(s).month, d(s).day)
            starts[key] = starts.get(key, 0) + (3 if f.get("fp") == "FY" else 1)
    return max(starts, key=starts.get) if starts else None


def _near_anchor(start, anchor, tol=7):
    if not anchor:
        return False
    s = d(start)
    ref = dt.date(s.year, *anchor)
    return min(abs((s - ref).days), abs((s - dt.date(s.year - 1, *anchor)).days),
               abs((s - dt.date(s.year + 1, *anchor)).days)) <= tol


def quarters(units):
    """Discrete quarters -> ({end: value}, ttm_crosscheck).

    Native ~3-month facts are authoritative. Gaps (typically Q4, which many filers report
    only inside the annual total) are filled by differencing the fiscal-YTD chain. Facts
    that are neither native nor FY-anchored — e.g. trailing-twelve-month contexts — are
    discarded rather than differenced.

    Also returns the filer's own 12-month facts keyed by end date, so the caller can audit
    a summed TTM against the number the company itself reported.
    """
    anchor = fiscal_year_anchor(units)
    native, ytd, twelve = {}, {}, {}
    for f in units:
        s, e, v = f.get("start"), f.get("end"), f.get("val")
        if not s or not e or v is None:
            continue
        try:
            span = (d(e) - d(s)).days
        except ValueError:
            continue
        v = float(v)
        if 80 <= span <= 100:
            native[e] = v
        if 350 <= span <= 380:
            twelve[e] = v
        # A native Q1 fact is ALSO the first link of its fiscal-YTD chain. Oracle files
        # exactly one native quarter per year (Q1) and cumulates the rest; omitting it
        # from the chain differences Q2 against zero and double-counts Q1.
        if span >= 80 and _near_anchor(s, anchor):
            ytd.setdefault(s, {})[e] = v

    out = dict(native)
    for s, ends in ytd.items():
        prev = None
        for e, v in sorted(ends.items()):
            span = (d(e) - d(s)).days
            if prev is None:
                # Chain does not start at Q1 — the first quarter is unrecoverable.
                # Emit nothing rather than a cumulative value masquerading as a quarter.
                if span <= 100:
                    out.setdefault(e, v)
            else:
                out.setdefault(e, v - prev)
            prev = v
    return dict(sorted(out.items())), twelve


def fetch_series(cik, tag_list, min_q=4):
    """Pick the tag whose series is FRESHEST, not merely the first that parses.

    Filers abandon concepts without deleting history: Amazon's
    PaymentsToAcquirePropertyPlantAndEquipment stops in 2017 and Nvidia's in 2012, yet both
    still return years of quarters. Selecting on "has >= 4 quarters" silently reads a
    decade-dead tag. Selecting on the latest quarter-end fixes it.

    Returns ({end: quarter_value}, tag_used, twelve_month_facts).
    """
    best = ({}, None, {})
    best_end = None
    for tag in tag_list:
        js = get_json(CONCEPT.format(cik=cik, tag=tag))
        time.sleep(0.15)  # SEC asks for <10 req/s
        if not js:
            continue
        units = js.get("units", {}).get("USD", [])
        if not units:
            continue
        q, twelve = quarters(units)
        if len(q) < min_q:
            continue
        latest = max(q)
        if best_end is None or latest > best_end:
            best, best_end = (q, tag, twelve), latest
    return best


def fetch_instant(cik, tag_list):
    """Point-in-time facts (balance sheet) -> {end: value}."""
    for tag in tag_list:
        js = get_json(CONCEPT.format(cik=cik, tag=tag))
        time.sleep(0.15)
        if not js:
            continue
        units = js.get("units", {}).get("USD", [])
        vals = {u["end"]: float(u["val"]) for u in units if u.get("val") is not None}
        if vals:
            return dict(sorted(vals.items())), tag
    return {}, None


def ttm(series, offset=0):
    """Sum of the 4 quarters ending `offset` quarters back. None if we lack 4."""
    ends = list(series)
    hi = len(ends) - offset
    if hi < 4:
        return None, []
    window = ends[hi - 4:hi]
    return sum(series[e] for e in window), window


def pct(a, b):
    if a is None or b is None or b == 0:
        return None
    return (a / b - 1.0) * 100.0


def audit_ttm(summed, window, twelve, label, notes):
    """Cross-check our summed TTM against the filer's own 12-month fact for the same end.

    When a company reports a trailing-twelve-month context (Amazon does), the meter's
    arithmetic can be validated for free. A silent >2% divergence means the quarter
    reconstruction is wrong and the reading must not be cited.
    """
    if not window or not twelve:
        return
    end = window[-1]
    if end not in twelve or not summed:
        return
    filed = twelve[end]
    if filed and abs(summed / filed - 1.0) > 0.02:
        notes.append(f"**TTM MISMATCH** {label}: summed ${summed/1e9:.1f}B vs filer's own "
                     f"12-month fact ${filed/1e9:.1f}B ({end}) — do not cite this reading")
    else:
        notes.append(f"{label} TTM cross-checks against the filer's own 12-month fact "
                     f"(${filed/1e9:.1f}B, {end})")


def read_entity(ticker, name, role, cik, verbose=False):
    r = {"ticker": ticker, "name": name, "role": role, "cik": cik, "notes": []}

    ocf, ocf_tag, ocf_12 = fetch_series(cik, TAGS["ocf"])
    capex, capex_tag, capex_12 = fetch_series(cik, TAGS["capex"])
    if not ocf or not capex:
        r["stage"] = "NO-DATA"
        r["notes"].append(f"missing {'OCF' if not ocf else 'capex'} concept")
        return r

    r["ocf_ttm"], ocf_w = ttm(ocf)
    r["capex_ttm"], capex_w = ttm(capex)
    r["ocf_ttm_prior"], _ = ttm(ocf, offset=4)
    r["capex_ttm_prior"], _ = ttm(capex, offset=4)
    r["asof"] = min(ocf_w[-1], capex_w[-1]) if ocf_w and capex_w else None
    r["tags"] = f"{ocf_tag}|{capex_tag}"

    # Staleness guard: an abandoned-but-populated tag is the failure mode this catches.
    if r["asof"] and (dt.date.today() - d(r["asof"])).days > 200:
        r["notes"].append(f"**STALE** newest quarter ends {r['asof']} — tag may be abandoned")

    audit_ttm(r["ocf_ttm"], ocf_w, ocf_12, "OCF", r["notes"])
    audit_ttm(r["capex_ttm"], capex_w, capex_12, "capex", r["notes"])
    if verbose:
        r["notes"].append("OCF quarters: " + ", ".join(f"{e}:{ocf[e]/1e9:.2f}B" for e in ocf_w))
        r["notes"].append("capex quarters: " + ", ".join(f"{e}:{capex[e]/1e9:.2f}B" for e in capex_w))

    if r["ocf_ttm"] is None or r["capex_ttm"] is None:
        r["stage"] = "INSUFFICIENT"
        return r

    r["ratio"] = r["capex_ttm"] / r["ocf_ttm"] if r["ocf_ttm"] else None
    r["capex_yoy"] = pct(r["capex_ttm"], r["capex_ttm_prior"])
    r["ocf_yoy"] = pct(r["ocf_ttm"], r["ocf_ttm_prior"])

    # Lease-adjusted view. Informational only — the stage stays on the standard cash-capex
    # definition so the ladder is comparable to how the street and Epoch measure it.
    leases, _, _ = fetch_series(cik, TAGS["finance_leases"])
    r["lease_ttm"] = ttm(leases)[0] if leases else None
    if r["lease_ttm"] and r["ocf_ttm"]:
        r["ratio_adj"] = (r["capex_ttm"] + r["lease_ttm"]) / r["ocf_ttm"]

    # External funding, NET of repayments. Gross proceeds are mostly refinancing: Amazon's
    # $68B of gross issuance against a $2B capex gap says nothing about how the gap is
    # funded. Report n/a when the concept is absent — never impute 0.
    debt, _, _ = fetch_series(cik, TAGS["debt_issued"])
    repaid, _, _ = fetch_series(cik, TAGS["debt_repaid"])
    eq, _, _ = fetch_series(cik, TAGS["equity_issued"])
    dt_ttm = ttm(debt)[0] if debt else None
    rp_ttm = ttm(repaid)[0] if repaid else None
    eq_ttm = ttm(eq)[0] if eq else None
    if dt_ttm is None and eq_ttm is None:
        r["ext_ttm"] = None
        r["notes"].append("issuance concepts absent — external funding unmeasured (n/a, not zero)")
    else:
        r["ext_ttm"] = (dt_ttm or 0) - (rp_ttm or 0) + (eq_ttm or 0)
        if rp_ttm is None and dt_ttm:
            r["notes"].append("repayment concept absent — external funding is GROSS, overstated")

    # ---- Stage assignment ---------------------------------------------------
    # A fabless supplier has no buildout to fund; its capex/OCF ratio is not a stage.
    # Nvidia sits on this board for exactly one reason: the S3 vendor-credit tell.
    if role == "supplier":
        r["stage"] = "n/a (supplier — watched for S3 only)"
        r["signals"] = []
    else:
        gap = r["capex_ttm"] - r["ocf_ttm"]
        if r["ratio"] is not None and r["ratio"] <= 1.0:
            r["stage"] = "S1 SELF-FUNDED"
        else:
            r["stage"] = "S2 EXTERNAL"
            if r["ext_ttm"] and gap > 0 and r["ext_ttm"] >= 0.5 * gap:
                r["notes"].append(
                    f"net external funding ${r['ext_ttm']/1e9:.0f}B covers >=50% of the "
                    f"${gap/1e9:.0f}B capex-over-cash-flow gap")

        # ---- Signals (symmetric) --------------------------------------------
        sig = []
        if r["ratio"] is not None:
            if 0.85 <= r["ratio"] < 1.0:
                sig.append("APPROACHING-CROSSOVER")
            if r["ratio"] > 1.0:
                sig.append("CROSSED")
        # The bullish falsifier: builders out-earning their own buildout.
        if r["ocf_yoy"] is not None and r["capex_yoy"] is not None and r["ratio"]:
            if r["ocf_yoy"] > r["capex_yoy"]:
                sig.append("CLOUD-OUTCOME-CANDIDATE" if r["ratio"] < 1.0
                           else "OCF-REINFLECTING(watch)")
        # Not crossed on cash capex, but crossed once leased capacity is counted.
        if r.get("ratio_adj") and r["ratio"] and r["ratio"] <= 1.0 < r["ratio_adj"]:
            sig.append("CROSSED-ON-LEASE-ADJUSTED-BASIS(watch)")
        r["signals"] = sig

    # ---- S3 vendor-financing tell (supplier only) ---------------------------
    if role == "supplier":
        ar, ar_tag = fetch_instant(cik, AR_TAGS)
        rev, rev_tag, _ = fetch_series(cik, TAGS["revenue"])
        if ar and rev:
            rev_ttm, rev_w = ttm(rev)
            ar_dates = [e for e in ar if e <= rev_w[-1]] if rev_w else []
            if rev_ttm and ar_dates:
                dso = ar[ar_dates[-1]] / rev_ttm * 365.0
                r["dso"] = dso
                prior_rev, prior_w = ttm(rev, offset=4)
                prior_ar = [e for e in ar if e <= prior_w[-1]] if prior_w else []
                if prior_rev and prior_ar:
                    dso_prior = ar[prior_ar[-1]] / prior_rev * 365.0
                    r["dso_prior"] = dso_prior
                    if dso > dso_prior * 1.15:
                        r["signals"].append("S3 DSO-RISING(vendor-credit tell)")
                    r["notes"].append(
                        f"DSO {dso:.0f}d vs {dso_prior:.0f}d a year ago "
                        f"(Lucent/Nortel tell: supplier extending credit to customers)")
    return r


def fulltext_scan():
    """EDGAR full-text search for S4/S5 language. Hits are prompts to read, not evidence."""
    results = {}
    for stage, queries in FTS_QUERIES.items():
        for q in queries:
            url = FTS.format(q=urllib.parse.quote(q), forms="10-K,10-Q")
            js = get_json(url)
            time.sleep(0.3)
            total = (js or {}).get("hits", {}).get("total", {}).get("value", 0)
            names = []
            for h in (js or {}).get("hits", {}).get("hits", [])[:5]:
                src = h.get("_source", {})
                names.append(f"{(src.get('display_names') or ['?'])[0]} ({src.get('file_date','?')})")
            results.setdefault(stage, []).append((q, total, names))
    return results


def load_last_row():
    if not os.path.exists(OUT_CSV):
        return {}
    rows = list(csv.DictReader(open(OUT_CSV)))
    last = {}
    for r in rows:
        last[r["ticker"]] = r
    return last


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fulltext", action="store_true", help="scan EDGAR text for S4/S5 language")
    ap.add_argument("--force", action="store_true", help="append even if no stage changed")
    ap.add_argument("--verbose", action="store_true", help="print the de-cumulated quarters")
    args = ap.parse_args()

    ciks = resolve_ciks([t for t, _, _ in ENTITIES])
    missing = [t for t, _, _ in ENTITIES if t not in ciks]
    readings = []
    for ticker, name, role in ENTITIES:
        if ticker not in ciks:
            continue
        readings.append(read_entity(ticker, name, role, ciks[ticker], verbose=args.verbose))

    prior = load_last_row()
    today = dt.date.today().isoformat()
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")

    changed = [r for r in readings
               if prior.get(r["ticker"], {}).get("stage") not in (None, r.get("stage"))]
    new = [r for r in readings if r["ticker"] not in prior]

    # ---- append the time series --------------------------------------------
    if changed or new or args.force:
        exists = os.path.exists(OUT_CSV)
        with open(OUT_CSV, "a", newline="") as f:
            w = csv.writer(f)
            if not exists:
                w.writerow(["date", "ticker", "name", "role", "stage", "asof",
                            "capex_ttm_usd", "ocf_ttm_usd", "ratio",
                            "finance_leases_ttm_usd", "ratio_incl_leases",
                            "net_ext_funding_ttm_usd",
                            "capex_yoy_pct", "ocf_yoy_pct", "dso_days", "signals", "tags"])
            for r in readings:
                w.writerow([
                    today, r["ticker"], r["name"], r["role"], r.get("stage"), r.get("asof"),
                    f"{r['capex_ttm']:.0f}" if r.get("capex_ttm") else "",
                    f"{r['ocf_ttm']:.0f}" if r.get("ocf_ttm") else "",
                    f"{r['ratio']:.3f}" if r.get("ratio") else "",
                    f"{r['lease_ttm']:.0f}" if r.get("lease_ttm") else "n/a",
                    f"{r['ratio_adj']:.3f}" if r.get("ratio_adj") else "",
                    f"{r['ext_ttm']:.0f}" if r.get("ext_ttm") else "n/a",
                    f"{r['capex_yoy']:.1f}" if r.get("capex_yoy") is not None else "",
                    f"{r['ocf_yoy']:.1f}" if r.get("ocf_yoy") is not None else "",
                    f"{r['dso']:.0f}" if r.get("dso") else "",
                    ";".join(r.get("signals", [])), r.get("tags", ""),
                ])

    fts = fulltext_scan() if args.fulltext else {}

    # ---- the human-readable clock face -------------------------------------
    with open(OUT_MD, "w") as f:
        f.write(f"# The Funding Clock — read {stamp}\n\n")
        f.write("A meter, not a hypothesis. Source: SEC XBRL companyconcept (audited filings).\n"
                "Trailing-twelve-month capex vs operating cash flow, de-cumulated from filed\n"
                "year-to-date facts. **Detection is automated; judgment is not.** This file never\n"
                "amends the thesis — `/review` adjudicates, with Ben's sign-off.\n\n")
        f.write("| co | stage | capex TTM | OCF TTM | capex/OCF | +leases | capex YoY | OCF YoY | net ext. funding TTM | as of |\n")
        f.write("|---|---|---|---|---|---|---|---|---|---|\n")

        def usd(v):
            return f"${v/1e9:.0f}B" if v else "—"

        def ratio_s(v):
            return f"{v:.2f}x" if v else "—"

        def pct_s(v):
            return f"{v:+.0f}%" if v is not None else "—"

        for r in sorted(readings, key=lambda x: -(x.get("ratio") or 0)):
            cells = [
                r["ticker"], r.get("stage", "?"),
                usd(r.get("capex_ttm")), usd(r.get("ocf_ttm")), ratio_s(r.get("ratio")),
                ratio_s(r.get("ratio_adj")),
                pct_s(r.get("capex_yoy")), pct_s(r.get("ocf_yoy")),
                usd(r["ext_ttm"]) if r.get("ext_ttm") else "n/a",
                str(r.get("asof") or "—"),
            ]
            f.write("| " + " | ".join(cells) + " |\n")

        f.write("\n## Signals\n\n")
        any_sig = False
        for r in readings:
            for s in r.get("signals", []):
                any_sig = True
                loud = "**[FALSIFIER-CANDIDATE]** " if "CLOUD-OUTCOME" in s else ""
                f.write(f"- {loud}`{s}` — {r['ticker']} ({r['name']})\n")
        if not any_sig:
            f.write("- none\n")

        f.write("\n## Notes and caveats\n\n")
        for r in readings:
            for n in r.get("notes", []):
                f.write(f"- {r['ticker']}: {n}\n")
        for t, why in MANUAL_ONLY.items():
            f.write(f"- {t}: NOT MEASURED — {why}\n")
        if missing:
            f.write(f"- CIK unresolved (skipped): {', '.join(missing)}\n")
        f.write("- S4/S5/S6 are not computable from XBRL alone. S4/S5 use `--fulltext` as a "
                "READ-THIS prompt; S6 is the NBIS convert/ABS term check, done by hand.\n")
        f.write("- Cash-flow quarters are differenced from year-to-date facts. Run `--verbose` "
                "to print the four quarters behind each TTM before citing a number.\n")
        f.write("- **`capex` is cash purchases of property and equipment.** It EXCLUDES "
                "datacenter capacity taken via finance lease, which never touches investing "
                "cash flow. The `+leases` column adds "
                "`RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability`; the STAGE is set "
                "on the unadjusted ratio so this ladder stays comparable to how Epoch and the "
                "street measure it. Where the two disagree about crossing, the meter says so.\n")
        f.write("- `net ext. funding` = debt proceeds − debt repayments + equity issuance. "
                "Gross proceeds are mostly refinancing and would badly overstate the number.\n")

        if fts:
            f.write("\n## Full-text scan (prompts to read — NOT evidence)\n\n")
            f.write(f"A hit means a filer used the phrase, nothing more. Queries returning over "
                    f"{FTS_NOISE_CEILING} hits are too broad to be a signal and are marked so.\n")
            for stage, rows in fts.items():
                f.write(f"\n### {stage}\n")
                for q, total, names in rows:
                    if total > FTS_NOISE_CEILING:
                        f.write(f"- `{q}` — {total} hits — TOO BROAD, no signal; narrow the phrase\n")
                    elif total == 0:
                        f.write(f"- `{q}` — no filer uses this phrase\n")
                    else:
                        f.write(f"- `{q}` — **{total} hits**: {'; '.join(names)}\n")

        f.write("\n## Suggested ledger row (paste into research/evidence-ledger.md under H1 — "
                "requires a command's judgment, not this script's)\n\n```\n")
        crossed = [r["ticker"] for r in readings if r.get("ratio") and r["ratio"] > 1.0]
        cloud = [r["ticker"] for r in readings if "CLOUD-OUTCOME-CANDIDATE" in r.get("signals", [])]
        direction = "confirms" if cloud and not crossed else "weakens"
        tag = " [FALSIFIER-CANDIDATE]" if cloud else ""
        f.write(f"- {today} · {direction} · mag 3 · wt A · src:/research · "
                f"Q{(dt.date.today().month-1)//3+1}'{str(dt.date.today().year)[2:]} ·{tag} "
                f"Funding Clock (XBRL, audited): capex>OCF at {', '.join(crossed) or 'none'}"
                + (f"; OCF re-inflecting at {', '.join(cloud)}" if cloud else "")
                + f". · cite: book/funding_clock.csv {today}\n```\n")

    n_moved = len(changed) + len(new)
    print(f"funding clock read {len(readings)} entities -> {OUT_MD}")
    for r in sorted(readings, key=lambda x: -(x.get("ratio") or 0)):
        rr = f"{r['ratio']:.2f}x" if r.get("ratio") else "n/a"
        print(f"  {r['ticker']:6s} {r.get('stage','?'):16s} capex/OCF {rr:>7s}  "
              f"{';'.join(r.get('signals', [])) or '-'}")
    if missing:
        print(f"  CIK unresolved: {', '.join(missing)}")
    print(f"{n_moved} stage change(s); csv {'appended' if (n_moved or args.force) else 'unchanged'}")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
