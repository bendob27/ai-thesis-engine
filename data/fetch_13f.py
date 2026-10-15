#!/usr/bin/env python3
"""Fetch latest 13F holdings for influence funds from SEC EDGAR.

Usage:
    python fetch_13f.py                     # both default funds
    python fetch_13f.py --cik 0002045724    # any fund by CIK
    python fetch_13f.py --top 25            # show top N by value

Defaults: Situational Awareness LP (Aschenbrenner), Atreides Management (Baker).
Notes: 13Fs lag ~45 days after quarter end; long positions + option notionals only.
No API key needed; SEC requires a User-Agent header.
"""
import argparse
import json
import sys
import urllib.request
from datetime import datetime, timezone
from xml.etree import ElementTree

UA = {"User-Agent": "ai-thesis-skill research contact@example.com"}
FUNDS = {
    "Situational Awareness LP": "0002045724",
    "Atreides Management": "0001777813",
    # Growth managers added 2026-07-29 on Ben's instruction ("let's add lone pine,
    # coatue, viking global, durable capital partners"). Purpose: the register carried
    # no voice whose failure mode is PAYING UP -- Aschenbrenner and Bridgewater are macro
    # and the Burry/Oaktree meters adopted 07-28 are value/credit. Every CIK below was
    # resolved from EDGAR company search and verified to have filed 13F-HR on 2026-05-15
    # (Q1'26) before being added -- not guessed. Note Viking has TWO CIKs: 0001101785
    # ("Viking Global Equities LP") is DEAD, last 13F 2002-11-14. The live filer is
    # 0001103804 ("VIKING GLOBAL INVESTORS LP"), 106 filings.
    "Lone Pine Capital LLC": "0001061165",
    "Coatue Management LLC": "0001135730",
    "Viking Global Investors LP": "0001103804",
    "Durable Capital Partners LP": "0001798849",
}


def get_json(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return json.loads(r.read().decode())


def get_bytes(url):
    req = urllib.request.Request(url, headers=UA)
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read()


def resolve_cik(name):
    """Find a filer CIK via EDGAR full-text search."""
    q = urllib.parse.quote(f'"{name}"')
    url = f"https://efts.sec.gov/LATEST/search-index?q={q}&forms=13F-HR"
    try:
        data = get_json(url)
        hits = data.get("hits", {}).get("hits", [])
        if hits:
            return hits[0]["_source"]["ciks"][0]
    except Exception:
        pass
    return None


def latest_13f_holdings(cik):
    cik10 = str(cik).lstrip("0").zfill(10)
    subs = get_json(f"https://data.sec.gov/submissions/CIK{cik10}.json")
    recent = subs.get("filings", {}).get("recent", {})
    forms = recent.get("form", [])
    idx = next((i for i, f in enumerate(forms) if f in ("13F-HR", "13F-HR/A")), None)
    if idx is None:
        return subs.get("name", cik), None, []
    acc = recent["accessionNumber"][idx].replace("-", "")
    fdate = recent["filingDate"][idx]
    base = f"https://www.sec.gov/Archives/edgar/data/{int(cik10)}/{acc}"
    listing = get_json(f"{base}/index.json")
    xml_files = [f["name"] for f in listing["directory"]["item"]
                 if f["name"].lower().endswith(".xml") and "primary_doc" not in f["name"].lower()]
    holdings = []
    for fn in xml_files:
        try:
            root = ElementTree.fromstring(get_bytes(f"{base}/{fn}"))
            ns = root.tag.split("}")[0] + "}" if "}" in root.tag else ""
            entries = root.findall(f".//{ns}infoTable")
            if not entries:
                continue
            for e in entries:
                def g(tag, el=e):
                    x = el.find(f"{ns}{tag}")
                    return x.text if x is not None else None
                put_call = e.find(f"{ns}putCall")
                holdings.append({
                    "issuer": g("nameOfIssuer"),
                    "class": g("titleOfClass"),
                    "value_usd": int(g("value") or 0),
                    "type": (put_call.text if put_call is not None else "SH"),
                })
            break
        except Exception:
            continue
    return subs.get("name", cik), fdate, holdings


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--cik", help="fetch a specific CIK instead of defaults")
    ap.add_argument("--top", type=int, default=15)
    args = ap.parse_args()

    stamp = datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    print(f"Fetched {stamp} from SEC EDGAR. 13Fs lag ~45 days; longs/options only.\n")

    targets = {}
    if args.cik:
        targets[args.cik] = args.cik
    else:
        import urllib.parse  # noqa: PLC0415
        for name, cik in FUNDS.items():
            targets[name] = cik or resolve_cik(name)

    for label, cik in targets.items():
        if not cik:
            print(f"== {label}: CIK not resolved — search EDGAR manually "
                  f"(https://www.sec.gov/cgi-bin/browse-edgar?action=getcompany"
                  f"&company={label.replace(' ', '+')}&type=13F)\n")
            continue
        try:
            name, fdate, holdings = latest_13f_holdings(cik)
        except Exception as e:  # noqa: BLE001
            print(f"== {label}: fetch failed ({e})\n")
            continue
        if not holdings:
            print(f"== {name}: no 13F holdings parsed\n")
            continue
        # 13F values are USD (values reported in full dollars since 2023)
        agg = {}
        for h in holdings:
            key = (h["issuer"], h["type"])
            agg[key] = agg.get(key, 0) + h["value_usd"]
        total = sum(agg.values())
        print(f"== {name} — 13F filed {fdate} — {len(agg)} lines, "
              f"${total/1e9:.2f}B reported value")
        for (issuer, typ), val in sorted(agg.items(), key=lambda x: -x[1])[: args.top]:
            tag = {"Put": " [PUT]", "Call": " [CALL]"}.get(typ, "")
            print(f"  {val/1e6:>10,.0f}M  {issuer}{tag}")
        print()


if __name__ == "__main__":
    import urllib.parse  # noqa: E402

    try:
        main()
    except KeyboardInterrupt:
        sys.exit(1)
