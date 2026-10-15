#!/usr/bin/env python3
"""fact_pack.py -- an SEC fact-pack puller that cannot print a stale number.

Usage:
    python3 data/fact_pack.py TICKER [TICKER ...] [--json out.json] [--md out.md]

For each ticker it prints one block. Every figure carries value, period_end (or as_of),
source (XBRL tag / filing form + date / "vendor") and grade ("filing-xbrl", "filing-text",
"vendor"). Anything that cannot be established prints `n/a` plus a flag, never 0 or blank.

THE SELF-AUDIT IS THE POINT. Market value and enterprise value are printed only when cash,
debt and shares each belong to the filer's latest 10-Q/10-K period (shares: the latest cover
date) and no blocking flag is open. Otherwise the block says
    MARKET VALUE: REFUSED -- <reasons>      EV: REFUSED -- <reasons>
instead of a number. A request that fails is a step not taken: flag FETCH_FAILED:<what>.

Where the numbers come from (and why):
  * Balance sheet = the FACE of the latest periodic filing (its R-page, via FilingSummary.xml),
    not the companyfacts API. The API drops dimensional facts, keeps abandoned tags alive
    (Illumina's cash tag ends 2018) and lags the filing (Avantor, IQVIA). The face is what the
    filer actually printed, line by line, so a disclosure-only tag (AST SpaceMobile's $2.3bn
    "short-term investments", money-market funds already inside cash) cannot be double counted.
  * Shares = cover-page counts by class from the filing's own inline XBRL (text parse as a
    fallback), because dei in the API is one class only or stale (Bruker).
  * Everything is live. Nothing is cached between runs. Companyfacts/submissions are cached
    per process only.

Flags (BLOCK = stops market value / EV; WARN = printed, does not stop):
  STALE_CASH STALE_DEBT STALE_SHARES STALE_QUARTER FOREIGN_FILER_NO_QUARTERLY_XBRL
  SHARES_MAY_BE_STALE_POST_OFFERING  DEI_STALE_IN_XBRL_API  PREFERRED_AS_CONVERTED_UNKNOWN
  FETCH_FAILED:<what>  FACE_UNAVAILABLE  REPORTING_CURRENCY_NOT_USD  CIK_UNRESOLVED ...
"""
from __future__ import annotations

import argparse
import datetime as dt
import gzip
import html
import json
import os
import re
import sys
import threading
import time
import urllib.error
import urllib.request
from concurrent.futures import ThreadPoolExecutor

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from funding_clock import quarters, ttm  # noqa: E402  (engine's shared SEC helpers)

UA = os.environ.get("SEC_UA", "ai-thesis-skill research contact@example.com")  # same placeholder as funding_clock.py
TICKER_MAP = "https://www.sec.gov/files/company_tickers.json"
MATERIAL_ITEMS = ("1.01", "1.02", "2.01", "2.05", "2.06", "3.02", "4.01", "4.02", "5.02", "7.01", "8.01")
PERIODIC_FORMS = ("10-K", "10-Q", "10-K/A", "10-Q/A", "10-KT", "10-QT")
FOREIGN_FORMS = ("20-F", "40-F", "20-F/A", "40-F/A", "6-K", "6-K/A")
OFFERING_FORMS = ("424B2", "424B3", "424B4", "424B5", "424B7")


def today():
    return dt.date.fromisoformat(os.environ["FACT_PACK_TODAY"]) if os.environ.get("FACT_PACK_TODAY") else dt.date.today()


def d(s):
    return dt.date.fromisoformat(s)


# --------------------------------------------------------------------------------------
# SEC client: User-Agent on every request, <= ~7 requests/s across all threads, retry with
# backoff, per-process cache. A failure is recorded, never papered over.
# --------------------------------------------------------------------------------------
class Sec:
    def __init__(self, ua=None, rps=7.0):
        self.ua = ua or UA
        self.min_gap = 1.0 / rps
        self._pace_lock = threading.Lock()
        self._next = 0.0
        self._cache = {}
        self._cache_lock = threading.Lock()
        self.n_requests = 0
        self.failures = []  # (url, error)

    def _pace(self):
        with self._pace_lock:
            now = time.monotonic()
            if self._next > now:
                time.sleep(self._next - now)
                now = self._next
            self._next = now + self.min_gap

    def fetch(self, url, as_json=False, tries=4):
        key = (url, as_json)
        with self._cache_lock:
            if key in self._cache:
                return self._cache[key]
        data, err = None, None
        for i in range(tries):
            self._pace()
            self.n_requests += 1
            try:
                req = urllib.request.Request(url, headers={"User-Agent": self.ua, "Accept-Encoding": "gzip"})
                with urllib.request.urlopen(req, timeout=90) as r:
                    raw = r.read()
                    if r.headers.get("Content-Encoding") == "gzip" or raw[:2] == b"\x1f\x8b":
                        raw = gzip.decompress(raw)
                text = raw.decode("utf-8", "ignore")
                data = json.loads(text) if as_json else text
                err = None
                break
            except urllib.error.HTTPError as e:
                err = f"HTTP {e.code}"
                if e.code == 404:
                    break
                time.sleep(2.0 * (2 ** i) if e.code in (403, 429, 503) else 1.0 * (i + 1))
            except Exception as e:  # noqa: BLE001
                err = f"{type(e).__name__}: {str(e)[:80]}"
                time.sleep(1.0 * (2 ** i))
        if data is None:
            self.failures.append((url, err))
        with self._cache_lock:
            self._cache[key] = data
        return data


# --------------------------------------------------------------------------------------
# small helpers
# --------------------------------------------------------------------------------------
def fig(value, period_end=None, source="", grade="filing-xbrl", **extra):
    out = {"value": value, "period_end": period_end, "source": source, "grade": grade}
    out.update(extra)
    return out


def na(reason, **extra):
    return fig(None, None, "", "n/a", note=reason, **extra)


class Pack(dict):
    """Result for one ticker. Flags are dicts: code, detail, block, scope."""

    def flag(self, code, detail="", block=False, scope=None):
        fl = self.setdefault("flags", [])
        if not any(f["code"] == code and f["detail"] == detail for f in fl):
            fl.append({"code": code, "detail": detail, "block": bool(block), "scope": scope})


def vis_text(t):
    x = re.sub(r"<ix:header>.*?</ix:header>", " ", t, flags=re.S)
    x = re.sub(r"<script.*?</script>|<style.*?</style>", " ", x, flags=re.S)
    x = re.sub(r"<[^>]+>", " ", x)
    x = html.unescape(x).replace("\xa0", " ")
    return re.sub(r"\s+", " ", x).strip()


def money(v, unit="USD"):
    if v is None:
        return "n/a"
    a = abs(v)
    sgn = "-" if v < 0 else ""
    if a >= 1e9:
        return f"{sgn}${a/1e9:,.3f}bn"
    if a >= 1e6:
        return f"{sgn}${a/1e6:,.1f}m"
    return f"{sgn}${a:,.0f}"


def px(v):
    """Share prices keep cents; money() is for company-size figures."""
    return "n/a" if v is None else f"${v:,.2f}"


def num(v, dec=0):
    return "n/a" if v is None else f"{v:,.{dec}f}"


# --------------------------------------------------------------------------------------
# submissions / filings list
# --------------------------------------------------------------------------------------
def _rows(cols):
    n = len(cols.get("form", []))
    rows = []
    for i in range(n):
        rows.append({
            "form": cols["form"][i], "filed": cols["filingDate"][i], "report": cols["reportDate"][i] or None,
            "acc": cols["accessionNumber"][i], "doc": cols["primaryDocument"][i],
            "items": [s.strip() for s in (cols["items"][i] or "").split(",") if s.strip()],
            "xbrl": bool(cols["isXBRL"][i]) if "isXBRL" in cols else False,
            "desc": cols.get("primaryDocDescription", [""] * n)[i],
        })
    return rows


def load_filings(sec, cik, since):
    sub = sec.fetch(f"https://data.sec.gov/submissions/CIK{cik}.json", as_json=True)
    if not sub:
        return None, []
    rows = _rows(sub["filings"]["recent"])
    oldest = min((r["filed"] for r in rows), default="9999")
    if oldest > since:  # the 1000-row "recent" window does not reach back far enough: page in older files
        for f in sub["filings"].get("files", []):
            page = sec.fetch(f"https://data.sec.gov/submissions/{f['name']}", as_json=True)
            if page:
                rows += _rows(page)
                if min(r["filed"] for r in rows) <= since:
                    break
    return sub, rows


def base_url(cik, acc):
    return f"https://www.sec.gov/Archives/edgar/data/{int(cik)}/{acc.replace('-', '')}/"


# --------------------------------------------------------------------------------------
# R-pages (the rendered XBRL statements of one filing)
# --------------------------------------------------------------------------------------
MONTHS = {m: i + 1 for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"])}


def parse_hdr_date(s):
    m = re.search(r"([A-Za-z]{3})[a-z]*\.?\s+(\d{1,2}),\s+(\d{4})", s)
    if not m or m.group(1).lower() not in MONTHS:
        return None
    return dt.date(int(m.group(3)), MONTHS[m.group(1).lower()], int(m.group(2))).isoformat()


def parse_val(s):
    s = s.replace("$", "").replace("€", "").replace("£", "").replace(",", "").strip()
    if s in ("—", "–", "-"):
        return 0.0
    neg = s.startswith("(") and s.endswith(")")
    s = s.strip("()").strip()
    try:
        v = float(s)
    except ValueError:
        return None
    return -v if neg else v


def rpage_list(sec, cik, acc):
    fs = sec.fetch(base_url(cik, acc) + "FilingSummary.xml")
    if not fs:
        return None
    return re.findall(r"<Report[^>]*>.*?<HtmlFileName>([^<]*)</HtmlFileName>.*?<ShortName>([^<]*)</ShortName>.*?<MenuCategory>([^<]*)</MenuCategory>", fs, re.S)


def find_report(reps, kind):
    pats = {
        "bs": (r"balance sheets?|financial position|financial condition|assets and liabilities", r"parenthetical"),
        "is": (r"statements? of (consolidated )?(operations|income|earnings|loss|profit)|income statements?|results of operations", r"parenthetical|comprehensive (income|loss)\s*\(?(unaudited)?\)?\s*$"),
        "cf": (r"cash flows?", r"parenthetical"),
    }
    inc, exc = pats[kind]
    for f, n, c in reps:
        if c.lower().startswith("statement") and re.search(inc, n, re.I) and not re.search(exc, n, re.I):
            return f
    return None


def parse_rpage(t):
    """-> {title, ccy, mscale, sscale, cols:[{end, months}], rows:[{tag,label,vals,abstract}]}"""
    title_m = re.search(r"<th[^>]*class=\"tl\"[^>]*>(.*?)</th>", t, re.S)
    title = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", title_m.group(1)))).strip() if title_m else ""
    ccy_m = re.search(r"-\s*([A-Z]{3})\s*\(", title)
    ccy = ccy_m.group(1) if ccy_m else None

    def scale_of(pat):
        m = re.search(pat + r"\s+in\s+(Thousands|Millions|Billions)", title, re.I)
        return {"thousands": 1e3, "millions": 1e6, "billions": 1e9}[m.group(1).lower()] if m else 1.0

    mscale = scale_of(r"(?:\$|USD|€|EUR|£|GBP)?")
    sscale = scale_of(r"shares")
    hdr_rows, body_rows = [], []
    for m in re.finditer(r"<tr[^>]*>(.*?)</tr>", t, re.S):
        row = m.group(1)
        if "defref_" in row:
            tag = re.search(r"defref_([A-Za-z0-9\-]+)_([A-Za-z0-9_\-]+)", row)
            tds = re.findall(r"<td([^>]*)>(.*?)</td>", row, re.S)
            cells = []
            for attrs, inner in tds:
                cls = (_attr(attrs, "class") or "").split()
                txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
                # value cells are nump/num/text; a footnote marker cell (class "th", e.g. "[1]") must not shift the columns
                if not cells or any(c in ("nump", "num", "text") for c in cls):
                    cells.append(txt)
            if tag and cells:
                body_rows.append({"tag": tag.group(1) + ":" + tag.group(2), "label": cells[0], "raw": cells[1:]})
        elif "<th" in row:
            cells = []
            for attrs, inner in re.findall(r"<th([^>]*)>(.*?)</th>", row, re.S):
                span = re.search(r"colspan=\"(\d+)\"", attrs)
                txt = re.sub(r"\s+", " ", html.unescape(re.sub(r"<[^>]+>", " ", inner))).strip()
                cells.append((txt, int(span.group(1)) if span else 1, "tl" in attrs))
            hdr_rows.append(cells)
    cols = []
    date_row = None
    for hr in hdr_rows:
        ds = [parse_hdr_date(c[0]) for c in hr if not c[2]]
        if ds and all(ds):
            date_row = hr
            break
    if date_row:
        group_row = hdr_rows[0] if hdr_rows and hdr_rows[0] is not date_row else None
        groups = []
        if group_row:
            for txt, span, is_tl in group_row:
                if not is_tl:
                    groups += [txt] * span
        dates = [parse_hdr_date(c[0]) for c in date_row if not c[2]]
        for i, dd in enumerate(dates):
            g = groups[i] if len(groups) == len(dates) else ""
            mm = re.search(r"(\d+)\s+Months", g)
            cols.append({"end": dd, "months": int(mm.group(1)) if mm else None})
    rows = []
    for r in body_rows:
        vals = [parse_val(c) for c in r["raw"]]
        abstract = r["tag"].endswith("Abstract") or (not any(v is not None for v in vals) and not any(c for c in r["raw"]))
        is_shares = bool(re.search(r"shares|ShareS", r["tag"] + " " + r["label"])) and not re.search(r"per share|PerShare", r["tag"] + r["label"])
        sc = sscale if is_shares else mscale
        rows.append({"tag": r["tag"], "label": r["label"], "vals": [None if v is None else v * sc for v in vals], "abstract": abstract})
    return {"title": title, "ccy": ccy, "cols": cols, "rows": rows}


# --------------------------------------------------------------------------------------
# inline XBRL of the main document (contexts + facts, INCLUDING dimensional ones)
# --------------------------------------------------------------------------------------
CTX_RE = re.compile(r"<xbrli:context\b[^>]*\bid=\"([^\"]+)\"[^>]*>(.*?)</xbrli:context>", re.S)
FACT_RE = re.compile(r"<ix:nonFraction\b([^>]*)>(.*?)</ix:nonFraction>", re.S)


def _attr(a, name):
    m = re.search(r"\b" + name + r"=\"([^\"]*)\"", a)
    return m.group(1) if m else None


def parse_ixbrl(t):
    ctx = {}
    for cid, body in CTX_RE.findall(t):
        inst = re.search(r"<xbrli:instant>\s*([^<\s]+)\s*</xbrli:instant>", body)
        st = re.search(r"<xbrli:startDate>\s*([^<\s]+)\s*</xbrli:startDate>", body)
        en = re.search(r"<xbrli:endDate>\s*([^<\s]+)\s*</xbrli:endDate>", body)
        dims = re.findall(r"<xbrldi:explicitMember[^>]*dimension=\"([^\"]+)\"[^>]*>\s*([^<\s]+)\s*</xbrldi:explicitMember>", body)
        ctx[cid] = {"instant": inst.group(1) if inst else None, "start": st.group(1) if st else None,
                    "end": en.group(1) if en else None, "dims": [(a.split(":")[-1], m.split(":")[-1]) for a, m in dims]}
    facts = []
    for a, inner in FACT_RE.findall(t):
        name, cref = _attr(a, "name"), _attr(a, "contextRef")
        if not name or cref not in ctx:
            continue
        txt = html.unescape(re.sub(r"<[^>]+>", "", inner)).strip()
        fmt = _attr(a, "format") or ""
        scale = int(_attr(a, "scale") or 0)
        sign = -1 if _attr(a, "sign") == "-" else 1
        if "zerodash" in fmt or txt in ("-", "—", "–"):
            v = 0.0
        else:
            s = txt.replace(" ", "")
            s = s.replace(".", "").replace(",", ".") if ("comma-decimal" in fmt or "numcommadecimal" in fmt) else s.replace(",", "")
            try:
                v = float(s)
            except ValueError:
                continue
        c = ctx[cref]
        facts.append({"name": name.split(":")[-1], "ns": name.split(":")[0], "val": sign * v * (10 ** scale),
                      "instant": c["instant"], "start": c["start"], "end": c["end"], "dims": c["dims"], "unit": _attr(a, "unitRef")})
    return facts


# --------------------------------------------------------------------------------------
# balance-sheet face: classify lines
# --------------------------------------------------------------------------------------
def face_sections(rows):
    sec = "ca"
    out = []
    for r in rows:
        tag = r["tag"].split(":")[-1]
        if tag == "AssetsCurrentAbstract":
            sec = "ca"
        elif tag == "AssetsNoncurrentAbstract":
            sec = "nca"
        elif tag == "LiabilitiesCurrentAbstract":
            sec = "cl"
        elif tag == "LiabilitiesNoncurrentAbstract":
            sec = "ncl"
        elif tag in ("StockholdersEquityAbstract", "LiabilitiesAndStockholdersEquityAbstract"):
            sec = "eq"
        elif tag == "AssetsCurrent":
            out.append((sec, r))
            sec = "nca"
            continue
        elif tag == "Assets":
            out.append((sec, r))
            sec = "cl"
            continue
        elif tag == "LiabilitiesCurrent":
            out.append((sec, r))
            sec = "ncl"
            continue
        elif tag == "Liabilities":
            out.append((sec, r))
            sec = "eq"
            continue
        out.append((sec, r))
    return out


NONCUR = re.compile(r"non-?\s?current|long[- ]term|noncurrent", re.I)
DEBT_LABEL = re.compile(r"\b(debt|notes?|borrowings?|loans?|credit (facility|facilities|agreement|lines?)|lines? of credit|term loan|convertible|bonds?|debentures?|commercial paper|revolv\w*|bridge|financing obligations?)\b", re.I)
DEBT_NOT = re.compile(r"receivable|accounts payable|trade payable|interest payable|accrued|dividend|warrant|derivative|deferred|operating lease|related party receivable|contract liabilit|pension|retirement|asset retirement|income tax|tax payable|payable to|payables?\b(?!.*(note|loan|debt))", re.I)
DEBT_TAGS = {"LongTermDebt", "LongTermDebtCurrent", "LongTermDebtNoncurrent", "DebtCurrent", "ShortTermBorrowings", "NotesPayableCurrent",
             "NotesPayable", "NotesPayableNoncurrent", "LongTermNotesPayable", "ConvertibleNotesPayable", "ConvertibleNotesPayableCurrent",
             "ConvertibleDebtNoncurrent", "ConvertibleDebtCurrent", "ConvertibleDebt", "ConvertibleLongTermNotesPayable", "SeniorNotes",
             "SeniorLongTermNotes", "LongTermLineOfCredit", "LinesOfCreditCurrent", "LineOfCredit", "SecuredDebt", "UnsecuredDebt",
             "CommercialPaper", "LongTermDebtAndCapitalLeaseObligations", "LongTermDebtAndCapitalLeaseObligationsCurrent",
             "OtherLongTermDebt", "SubordinatedDebt", "LoansPayable", "LoansPayableCurrent", "LoansPayableNoncurrent", "DebtAndCapitalLeaseObligations",
             "ConvertibleNotesPayableNoncurrent", "NotesPayableRelatedPartiesClassifiedCurrent", "SecuredLongTermDebt", "ShortTermBankLoansAndNotesPayable",
             "LongTermDebtAndCapitalLeaseObligationsIncludingCurrentMaturities", "DebtLongtermAndShorttermCombinedAmount"}


def classify_cash(tag, label, sec):
    tg = tag.split(":")[-1]
    lb = label.lower()
    if re.match(r"\s*total\b", lb) or tg == "CashCashEquivalentsAndShortTermInvestments":
        return "subtotal" if re.search(r"cash|invest|securit", lb) else None
    if re.search(r"non-?\s?marketable", lb):
        return None
    if "restricted" in lb and re.search(r"cash|deposit|equivalent", lb):
        return "restricted_noncurrent" if (sec in ("nca",) or NONCUR.search(lb) or tg.endswith("Noncurrent")) else "restricted_current"
    if tg.startswith("RestrictedCash"):
        return "restricted_noncurrent" if tg.endswith("Noncurrent") or sec == "nca" else "restricted_current"
    if re.search(r"equity securities|equity investments?|equity method", lb) or "EquitySecurities" in tg:
        return "equity_securities" if re.search(r"marketable|securities", lb) else None
    if re.match(r"\s*cash\b", lb) and not re.search(r"flows?|provided|used|paid|received", lb):
        if re.search(r"(marketable|short[- ]term investments?|securities)", lb):
            return "cash_combined"
        return "cash"
    if tg in ("CashAndCashEquivalentsAtCarryingValue", "Cash", "CashAndDueFromBanks", "CashEquivalentsAtCarryingValue") and sec in ("ca", None):
        return "cash"
    if re.search(r"short[- ]term (investments?|deposits?|securities)|marketable (debt )?securities|available[- ]for[- ]sale|time deposits|certificates? of deposit|treasury (bills|securities)|investments? in (debt )?securities|marketable", lb) \
            or tg in ("ShortTermInvestments", "MarketableSecuritiesCurrent", "MarketableSecurities", "AvailableForSaleSecuritiesDebtSecuritiesCurrent",
                      "AvailableForSaleSecuritiesDebtSecurities", "DebtSecuritiesCurrent", "HeldToMaturitySecuritiesCurrent", "AvailableForSaleSecuritiesCurrent"):
        if sec == "nca" or NONCUR.search(lb) or tg.endswith("Noncurrent"):
            return "securities_noncurrent"
        return "securities_current"
    return None


def classify_debt(tag, label, sec):
    tg = tag.split(":")[-1]
    lb = label.lower()
    if "lease" in lb or "Lease" in tg:
        return ("finance_lease" if re.search(r"finance|capital", lb) or "FinanceLease" in tg else None)
    if re.match(r"\s*total\b", lb):
        return "debt_subtotal" if re.search(r"debt|borrowing|notes|loan", lb) else None
    if tg in DEBT_TAGS or (DEBT_LABEL.search(lb) and not DEBT_NOT.search(lb)):
        if sec in ("ca", "nca", "eq"):
            return None  # an asset (e.g. notes receivable) or equity line, not a liability
        if re.search(r"warrant|derivative", lb):
            return None
        return "debt_current" if (sec == "cl" or re.search(r"current portion|current maturit|short[- ]term", lb) or tg.endswith("Current")) and not tg.endswith("Noncurrent") \
            and not NONCUR.search(lb.replace("current portion", "")) else "debt_noncurrent"
    return None


def pick_col(cols, period_end):
    for i, c in enumerate(cols):
        if c["end"] == period_end:
            return i
    return None


def read_face(rp, period_end):
    """Return dict with cash/debt components from a parsed balance-sheet R page, or None."""
    ci = pick_col(rp["cols"], period_end)
    if ci is None:
        return None
    comp = {"cash": [], "restricted_current": [], "restricted_noncurrent": [], "securities_current": [], "securities_noncurrent": [],
            "equity_securities": [], "subtotal": [], "cash_combined": [], "debt_current": [], "debt_noncurrent": [], "finance_lease": [], "debt_subtotal": []}
    for sec, r in face_sections(rp["rows"]):
        if r["abstract"] or ci >= len(r["vals"]) or r["vals"][ci] is None:
            continue
        item = {"tag": r["tag"], "label": r["label"], "value": r["vals"][ci], "section": sec}
        if sec in ("ca", "nca", "eq"):
            k = classify_cash(r["tag"], r["label"], sec)
            if k:
                comp[k].append(item)
        if sec in ("cl", "ncl", "l"):
            k = classify_debt(r["tag"], r["label"], sec)
            if k:
                comp[k].append(item)
    # subtotal debt lines: drop when the other lines already sum to it (no double count)
    lines = comp["debt_current"] + comp["debt_noncurrent"]
    for sub in comp["debt_subtotal"]:
        if lines and abs(sum(x["value"] for x in lines) - sub["value"]) <= 0.01 * max(1.0, abs(sub["value"])):
            continue
    return comp


# --------------------------------------------------------------------------------------
# per-ticker build
# --------------------------------------------------------------------------------------
def latest_periodic(filings):
    cands = [f for f in filings if f["form"] in PERIODIC_FORMS and f["report"]]
    if not cands:
        return []
    best = max(f["report"] for f in cands)
    return sorted([f for f in cands if f["report"] == best], key=lambda f: f["filed"], reverse=True)


def foreign_latest(filings, pack):
    """Foreign private issuer: newest filing that carries XBRL financials (20-F/40-F or an XBRL 6-K with a period end)."""
    x = [f for f in filings if f["form"] in FOREIGN_FORMS and f["report"] and f["xbrl"]
         and (f["form"].startswith(("20-F", "40-F")) or 5 <= (d(f["filed"]) - d(f["report"])).days <= 150)]
    if not x:
        return []
    best = max(f["report"] for f in x)
    return sorted([f for f in x if f["report"] == best], key=lambda f: f["filed"], reverse=True)


def build_cash_debt(sec, pack, cik, cand):
    """Try the candidate filings (latest first) until a balance-sheet face parses."""
    for f in cand:
        reps = rpage_list(sec, cik, f["acc"])
        if not reps:
            pack.flag("FETCH_FAILED:FilingSummary", f"{f['form']} {f['acc']}", False, "filing")
            continue
        r = find_report(reps, "bs")
        if not r:
            continue
        t = sec.fetch(base_url(cik, f["acc"]) + r)
        if not t:
            pack.flag("FETCH_FAILED:balance-sheet R page", f"{f['acc']} {r}", False, "filing")
            continue
        rp = parse_rpage(t)
        comp = read_face(rp, f["report"])
        if comp is None:
            continue
        return f, rp, comp
    return None, None, None


def assemble_cash(pack, f, rp, comp):
    pe = f["report"]
    src = f"{f['form']} {f['filed']} balance-sheet face ({f['acc']})"
    cash_lines = comp["cash"] + comp["cash_combined"]
    out = {"period_end": pe}
    if not cash_lines:
        out["cash_and_equivalents"] = na("no cash line on the balance-sheet face")
        pack.flag("STALE_CASH", f"no cash line found on the {f['form']} face for {pe}", True, "cash")
    else:
        v = sum(x["value"] for x in cash_lines)
        tags = "+".join(x["tag"] for x in cash_lines)
        extra = {}
        if any("RestrictedCash" in x["tag"] for x in cash_lines):
            extra["note"] = "face cash line is tagged cash+restricted cash; restricted portion not separable in XBRL"
        out["cash_and_equivalents"] = fig(v, pe, f"{tags}; {src}", "filing-xbrl", **extra)
    sti = comp["securities_current"]
    out["short_term_investments"] = fig(sum(x["value"] for x in sti), pe, "+".join(x["tag"] for x in sti) + "; " + src) if sti else fig(0.0, pe, "no short-term investment line on the face", "filing-xbrl", note="none on face")
    lti = comp["securities_noncurrent"]
    out["noncurrent_securities_apart"] = fig(sum(x["value"] for x in lti), pe, "+".join(x["tag"] for x in lti) + "; " + src) if lti else None
    eq = comp["equity_securities"]
    out["equity_securities_apart"] = fig(sum(x["value"] for x in eq), pe, "+".join(x["tag"] for x in eq) + "; " + src) if eq else None
    rc, rn = comp["restricted_current"], comp["restricted_noncurrent"]
    out["restricted_cash_current"] = fig(sum(x["value"] for x in rc), pe, "+".join(x["tag"] for x in rc) + "; " + src) if rc else None
    out["restricted_cash_noncurrent"] = fig(sum(x["value"] for x in rn), pe, "+".join(x["tag"] for x in rn) + "; " + src) if rn else None
    base = out["cash_and_equivalents"]["value"]
    if base is not None:
        out["cash_plus_current_investments"] = fig(base + out["short_term_investments"]["value"], pe, "cash line + current investments; " + src)
    # cross-check against the filer's own "total cash and investments" line when present
    for st in comp["subtotal"]:
        if base is not None and abs(base + out["short_term_investments"]["value"] + (out["noncurrent_securities_apart"]["value"] if out["noncurrent_securities_apart"] else 0) - st["value"]) > 0.005 * max(1.0, st["value"]):
            pack.flag("CASH_SUBTOTAL_MISMATCH", f"face line '{st['label']}' = {money(st['value'])} differs from components", False, "cash")
    pack["cash"] = out


def assemble_debt(pack, f, rp, comp):
    pe = f["report"]
    src = f"{f['form']} {f['filed']} balance-sheet face ({f['acc']})"
    lines = comp["debt_current"] + comp["debt_noncurrent"]
    out = {"period_end": pe, "lines": [{"tag": x["tag"], "label": x["label"], "value": x["value"], "section": x["section"]} for x in lines]}
    cur = sum(x["value"] for x in comp["debt_current"])
    non = sum(x["value"] for x in comp["debt_noncurrent"])
    if lines:
        out["carrying"] = fig(cur + non, pe, "+".join(x["tag"] for x in lines) + "; " + src, "filing-xbrl")
        out["current_portion"] = fig(cur, pe, src)
        out["noncurrent_portion"] = fig(non, pe, src)
    else:
        out["carrying"] = fig(0.0, pe, "no borrowing line on the balance-sheet face; " + src, "filing-xbrl", note="face shows no debt")
    fl = comp["finance_lease"]
    out["finance_leases_apart"] = fig(sum(x["value"] for x in fl), pe, "+".join(x["tag"] for x in fl) + "; " + src) if fl else None
    pack["debt"] = out


def run_ticker(sec, ticker, args):
    pack = Pack({"ticker": ticker, "run_utc": dt.datetime.utcnow().strftime("%Y-%m-%dT%H:%MZ"), "flags": []})
    tm = sec.fetch(TICKER_MAP, as_json=True) or {}
    cik = None
    for row in tm.values():
        if row.get("ticker", "").upper() == ticker.upper().replace(".", "-") or row.get("ticker", "").upper() == ticker.upper():
            cik = str(row["cik_str"]).zfill(10)
            break
    if not cik:
        pack.flag("CIK_UNRESOLVED", ticker, True, "filing")
        return pack
    pack["cik"] = cik
    since = (today() - dt.timedelta(days=372)).isoformat()
    sub, filings = load_filings(sec, cik, since)
    if not sub:
        pack.flag("FETCH_FAILED:submissions", cik, True, "filing")
        return pack
    pack["name"] = sub.get("name")
    pack["fiscal_year_end"] = sub.get("fiscalYearEnd")
    pack["filings_seen"] = len(filings)
    recent_dom = [f for f in filings if f["form"] in ("10-K", "10-Q") and f["filed"] >= (today() - dt.timedelta(days=620)).isoformat()]
    foreign = not recent_dom and any(f["form"] in FOREIGN_FORMS for f in filings)
    pack["filer_type"] = "foreign_private_issuer" if foreign else "domestic"
    cand = foreign_latest(filings, pack) if foreign else latest_periodic(filings)
    if not cand:
        pack.flag("NO_PERIODIC_FILING", "no 10-K/10-Q (or XBRL 6-K/20-F) found", True, "filing")
        return pack
    f0, rp, comp = build_cash_debt(sec, pack, cik, cand)
    latest_end = cand[0]["report"]
    if foreign:
        # interim results published without XBRL (Qiagen) make any older XBRL balance sheet stale
        interim = [f for f in filings if f["form"].startswith("6-K") and f["report"] and not f["xbrl"]
                   and 10 <= (d(f["filed"]) - d(f["report"])).days <= 120]
        newest_interim = max((f["report"] for f in interim), default=None)
        if newest_interim and newest_interim > latest_end and (d(newest_interim) - d(latest_end)).days > 30:
            pack.flag("FOREIGN_FILER_NO_QUARTERLY_XBRL", f"latest XBRL balance sheet is {latest_end}; interim results for {newest_interim} were filed on 6-K without XBRL", True, "filing")
            latest_end = newest_interim
    pack["filing"] = {"form": cand[0]["form"], "filed": cand[0]["filed"], "period_end": latest_end, "acc": cand[0]["acc"]}
    if f0 is None:
        pack.flag("FACE_UNAVAILABLE", "could not read a balance-sheet face for the latest periodic filing", True, "cash")
        pack["cash"] = {"cash_and_equivalents": na("balance-sheet face unavailable")}
        pack["debt"] = {"carrying": na("balance-sheet face unavailable")}
    else:
        pack["balance_sheet_filing"] = {"form": f0["form"], "filed": f0["filed"], "period_end": f0["report"], "acc": f0["acc"]}
        if rp["ccy"] and rp["ccy"] != "USD":
            pack.flag("REPORTING_CURRENCY_NOT_USD", rp["ccy"], True, "cash")
        assemble_cash(pack, f0, rp, comp)
        assemble_debt(pack, f0, rp, comp)
        if latest_end and f0["report"] < latest_end:
            why = f"the last XBRL balance sheet is {f0['report']}; a later period ({latest_end}) was reported without XBRL, so no figure is printed as current"
            pack["cash"] = {"period_end": f0["report"], "cash_and_equivalents": na(why), "short_term_investments": na(why)}
            pack["debt"] = {"period_end": f0["report"], "carrying": na(why), "lines": []}
            pack.flag("STALE_CASH", why, True, "cash")
            pack.flag("STALE_DEBT", why, True, "debt")
    return pack



# --------------------------------------------------------------------------------------
# debt principal (face) -- from the debt note's inline XBRL, cross-checked two ways
# --------------------------------------------------------------------------------------
S1_COMBINED = "DebtInstrumentUnamortizedDiscountPremiumAndDebtIssuanceCostsNet"
S1_DISC = ("DebtInstrumentUnamortizedDiscountNet", "DebtInstrumentUnamortizedDiscount", "UnamortizedDebtIssuanceExpense", "DebtIssuanceCostsNet")
S1_PREM = ("DebtInstrumentUnamortizedPremium",)


def tag_total(facts, name, pe, fv_ok=False):
    """Value of one concept at pe: the non-dimensional total if the filer gave one, else the sum over distinct
    member sets (fair-value-table duplicates ignored unless nothing else exists). None when absent."""
    xs = [x for x in facts if x["name"] == name and x["instant"] == pe]
    if not xs:
        return None
    nodim = [x for x in xs if not x["dims"]]
    if nodim:
        return nodim[0]["val"]
    seen, tot, n = set(), 0.0, 0
    for x in xs:
        fv = any(("FairValue" in m or "Level" in m) for a, m in x["dims"])
        if fv and not fv_ok:
            continue
        k = tuple(x["dims"])
        if k in seen:
            continue
        seen.add(k)
        tot += x["val"]
        n += 1
    if n == 0 and not fv_ok:
        return tag_total(facts, name, pe, True)
    return tot


def assemble_principal(pack, facts, pe, f):
    dbt = pack.get("debt") or {}
    carrying = (dbt.get("carrying") or {}).get("value")
    if not carrying:
        return
    src = f"{f['form']} {f['filed']} debt-note inline XBRL ({f['acc']})"
    if not facts:
        pack.flag("PRINCIPAL_NOT_ESTABLISHED", "the filing's inline XBRL could not be read", False, "debt")
        dbt["principal"] = na("inline XBRL unavailable")
        return
    # instrument-level face amounts (e.g. AAOI's $125m convertible notes), shown for reference
    inst, seen = [], set()
    for x in facts:
        if x["name"] == "DebtInstrumentFaceAmount" and x["instant"] == pe and x["dims"]:
            k = (tuple(x["dims"]), x["val"])
            if k not in seen:
                seen.add(k)
                inst.append({"member": " / ".join(m for a, m in x["dims"]), "face": x["val"]})
    dbt["instrument_face_amounts"] = inst
    comb = tag_total(facts, S1_COMBINED, pe)
    if comb is not None:
        disc = comb
    else:
        disc = sum(v for v in (tag_total(facts, n, pe) for n in S1_DISC) if v)
    prem = sum(v for v in (tag_total(facts, n, pe) for n in S1_PREM) if v)
    p_s1 = carrying + disc - prem if (disc or prem) else None
    if p_s1 is not None and not (0.9 <= p_s1 / carrying <= 1.25):
        p_s1 = None
    gross = []
    for n in ("DebtInstrumentFaceAmount", "LongTermDebtGross", "DebtLongtermAndShorttermCombinedAmount", "DebtInstrumentCarryingAmount"):
        v = tag_total(facts, n, pe)
        if v and 0.97 <= v / carrying <= 1.15:
            gross.append((n, v))
    pg = gross[0] if gross else None
    val, how, parts = None, "", {}
    if p_s1 is not None and pg and abs(p_s1 - pg[1]) <= 0.005 * carrying:
        val, how = pg[1], f"corroborated: {pg[0]} = carrying + unamortized discount/costs"
    elif pg and (p_s1 is None):
        val, how = pg[1], f"debt-note total ({pg[0]})"
    elif p_s1 is not None and not pg:
        val, how = p_s1, "carrying + unamortized discount/issuance costs - premium"
    elif p_s1 is not None and pg:
        val, how = pg[1], f"debt-note total ({pg[0]}); carrying + unamortized costs gives {money(p_s1)} (differs)"
        pack.flag("PRINCIPAL_CONFLICT", f"{pg[0]} {money(pg[1])} vs carrying+costs {money(p_s1)}", False, "debt")
    parts = {"carrying": carrying, "unamortized_discount_and_costs": disc or None, "unamortized_premium": prem or None}
    if val is None:
        pack.flag("PRINCIPAL_NOT_ESTABLISHED", "no machine-readable principal for the borrowings in the debt note (no face-amount total, no unamortized-cost facts)", False, "debt")
        dbt["principal"] = na("not machine-readable in the filing's inline XBRL")
        return
    dbt["principal"] = fig(val, pe, f"{how}; {src}", "filing-xbrl", differs_from_carrying_pct=(val / carrying - 1) * 100, parts=parts)

# --------------------------------------------------------------------------------------
# shares: cover counts by class (inline XBRL of the filing itself), preferred, post-cover events
# --------------------------------------------------------------------------------------
def cover_from_ixbrl(facts):
    cov = [x for x in facts if x["name"] == "EntityCommonStockSharesOutstanding" and x["instant"]]
    if not cov:
        return None, []
    date = max(x["instant"] for x in cov)
    seen, classes = set(), []
    for x in cov:
        if x["instant"] != date:
            continue
        key = tuple(x["dims"])
        if key in seen:
            continue
        seen.add(key)
        member = "+".join(m for a, m in x["dims"]) or "Common"
        classes.append({"class": member, "value": x["val"], "preferred": any("Preferred" in m for a, m in x["dims"])})
    return date, classes


def cover_from_text(text):
    """Fallback when the cover carries no machine-readable count: read the cover paragraph itself."""
    head = text[:30000]
    months = "January|February|March|April|May|June|July|August|September|October|November|December"
    out, date = [], None
    for m in re.finditer(r"([\d]{1,3}(?:,\d{3}){2,})\s+(?:shares|ordinary shares)", head):
        ctx = head[max(0, m.start() - 260): m.end() + 140]
        if not re.search(r"outstanding", ctx, re.I):
            continue
        dm = re.search(r"(?:as of|at)\s+((?:%s)\s+\d{1,2},\s+\d{4})" % months, ctx, re.I)
        if dm and not date:
            date = dt.datetime.strptime(dm.group(1), "%B %d, %Y").date().isoformat()
        out.append({"class": re.sub(r"\s+", " ", ctx[max(0, ctx.find(m.group(1)) - 80): ctx.find(m.group(1))]).strip()[-60:] or "Common",
                    "value": float(m.group(1).replace(",", "")), "preferred": bool(re.search(r"preferred", ctx[:ctx.find(m.group(1))][-120:], re.I))})
    return date, out


def share_signal(text):
    """A short evidence snippet if an 8-K/prospectus text reports a sale/issuance of shares, else None.
    Sentences about NOTES/debentures are not share sales (a convertible-notes offering does not change the cover count)."""
    t = text[:60000]
    pats = [
        r"((?:completed|closed|priced|announced|entered into)[^.]{0,200}(?:public offering|underwritten offering|registered direct|private placement|at[- ]the[- ]market|underwriting agreement|sales agreement)[^.]{0,200}(?:shares|common stock|ordinary shares)[^.]*\.)",
        r"((?:issued|issuance|sold|sale of|issue|delivered)[^.]{0,200}(?:\d{1,3}(?:,\d{3}){2,}|[\d.]+\s+million)\s+(?:additional\s+)?(?:shares|ordinary shares|Class [A-Z] (?:common )?shares)[^.]*\.)",
        r"(proposed public offering of[^.]{0,200}(?:common stock|ordinary shares|shares)[^.]*\.)",
        r"((?:public offering|offering)[^.]{0,80}of\s+[^.]{0,60}(?:shares of (?:its |our )?(?:Class [A-Z] )?common stock)[^.]*\.)",
        r"((?:stock consideration|shares of [A-Za-z ]{0,40}common stock)[^.]{0,200}(?:issued|issuable)[^.]*\.)",
        r"(\d\.\d+\s+shares of [A-Za-z ]{0,40}common stock[^.]{0,120}(?:for each|per)\s+[^.]{0,80}share[^.]*\.)",
        r"((?:received|right to receive)[^.]{0,200}\d\.\d+\s+(?:validly issued,? fully paid and nonassessable\s+)?shares of [A-Za-z ]{0,40}common stock[^.]*\.)",
    ]
    for pat in pats:
        for m in re.finditer(pat, t, re.I):
            sn = m.group(1)
            if re.search(r"\bnotes\b|debentures|principal amount", sn, re.I) and not re.search(r"upon (?:the )?conversion|conversion of", sn, re.I):
                continue
            return re.sub(r"\s+", " ", sn)[:300]
    return None


def _num(sx):
    return float(sx.replace(",", ""))


def preferred_ratio(text):
    """Common shares per preferred share, from the filing's own words. -> dict(ratio|total_million, how, snippet) or dict(unknown=reason)."""
    wins = []
    for m in re.finditer(r"preferred stock|preferred shares", text, re.I):
        lo, hi = max(0, m.start() - 600), m.end() + 900
        if wins and lo <= wins[-1][1]:
            wins[-1] = (wins[-1][0], hi)
        else:
            wins.append((lo, hi))
    mandatory = False
    best = None
    for lo, hi in wins:
        w = text[lo:hi]
        if not re.search(r"convert", w, re.I):
            continue
        if re.search(r"mandatory convertible", w, re.I):
            mandatory = True
        sv = re.search(r"stated value of (?:\$|US\$)\s?([\d,]+(?:\.\d+)?)", w, re.I)
        cp = re.search(r"conversion price of (?:approximately )?(?:\$|US\$)\s?([\d,]+(?:\.\d+)?)", w, re.I)
        if sv and cp and _num(cp.group(1)) > 0:
            return {"ratio": _num(sv.group(1)) / _num(cp.group(1)), "how": "stated value / conversion price", "snippet": re.sub(r"\s+", " ", w[max(0, sv.start() - 120): cp.end() + 80])}
        m1 = re.search(r"one[- ]for[- ]one|1[- ]for[- ]1|one share of (?:the Company.s |our )?common stock for each share", w, re.I)
        if m1 and not best:
            best = {"ratio": 1.0, "how": "filing states one-for-one", "snippet": re.sub(r"\s+", " ", w[max(0, m1.start() - 150): m1.end() + 100])}
        m4 = re.search(r"exchange[^.]{0,260}?([\d,]{6,})\s+shares of (?:the Company.s )?common stock\s+(?:into|for)\s+([\d,]{6,})\s+shares of (?:the Company.s )?[^.]{0,60}?Preferred Stock", w, re.I)
        if m4 and abs(_num(m4.group(1)) - _num(m4.group(2))) < 0.5 and not best:
            best = {"ratio": 1.0, "how": "common exchanged share-for-share into the preferred", "snippet": re.sub(r"\s+", " ", w[m4.start(): m4.end()])[:260]}
        m3 = re.search(r"into an aggregate (?:maximum )?of (?:approximately )?([\d.,]+)\s+million shares of (?:the Company.s |our )?common stock", w, re.I)
        if m3 and not best:
            best = {"total_million": _num(m3.group(1)), "how": "filing states the aggregate share count (rounded)", "snippet": re.sub(r"\s+", " ", w[max(0, m3.start() - 120): m3.end()])}
    if best:
        return best
    if mandatory:
        return {"unknown": "mandatory convertible preferred: the common shares it converts into depend on the share price at conversion; the filing gives no fixed rate"}
    if any(re.search(r"convert", text[lo:hi], re.I) for lo, hi in wins):
        return {"unknown": "convertible preferred: no conversion rate stated in this filing"}
    return {"nonconvertible": True}


def resolve_preferred(pack, prefs, text, ents):
    out = []
    if not prefs:
        return out
    pr = preferred_ratio(text or "")
    for row in prefs:
        r = dict(row)
        n = r["shares"]
        # exact count from an Item 3.02/5.03 8-K when the statement figure is rounded (reported in millions)
        if n >= 1e6 and n % 100000 == 0:
            for e in ents or []:
                c = e.get("pref_count")
                if c and abs(c - n) / n <= 0.03:
                    r["shares_rounded_in_statement"] = n
                    r["shares"] = n = c
                    r["count_source"] = f"8-K {e['filed']} Items {','.join(e['items'])} ({e['acc']}): exact count; the statement rounds to {r['shares_rounded_in_statement']:,.0f}"
                    break
        if "ratio" in pr:
            r.update(ratio=pr["ratio"], as_converted=n * pr["ratio"], ratio_source=pr["how"], evidence=pr["snippet"])
        elif "total_million" in pr:
            r.update(ratio=None, as_converted=pr["total_million"] * 1e6, ratio_source=pr["how"], evidence=pr["snippet"])
        elif pr.get("nonconvertible"):
            r.update(ratio=0.0, as_converted=0.0, ratio_source="no conversion feature found in the filing text", evidence="")
            pack.flag("NONCONVERTIBLE_PREFERRED_NOT_ADDED", f"{r['series']} {n:,.0f} preferred shares outstanding, no conversion feature found", False, "shares")
        else:
            r.update(ratio=None, as_converted=None, ratio_source=pr["unknown"], evidence="")
            pack.flag("PREFERRED_AS_CONVERTED_UNKNOWN", f"{r['series']} {n:,.0f} preferred shares outstanding; {pr['unknown']}", True, "shares")
        out.append(r)
    return out


def build_shares(sec, pack, cik, f, facts, text, ents=None):
    pe = f["report"]
    src_f = f"{f['form']} {f['filed']} cover ({f['acc']})"
    cover_date, classes = cover_from_ixbrl(facts) if facts else (None, [])
    grade, how = "filing-xbrl", "inline XBRL dei:EntityCommonStockSharesOutstanding by class"
    if not classes and text:
        cover_date, classes = cover_from_text(text)
        grade, how = "filing-text", "cover page text"
        if classes:
            pack.flag("COVER_FROM_TEXT", "no machine-readable cover count in the filing; read from cover text", False, "shares")
    out = {"cover_date": cover_date, "classes": classes, "method": how}
    commons = [c for c in classes if not c["preferred"]]
    prefs_cover = [c for c in classes if c["preferred"]]
    if commons and cover_date:
        out["common_total"] = fig(sum(c["value"] for c in commons), cover_date, f"{how}; {src_f}", grade)
    else:
        out["common_total"] = na("no cover share count could be read from the filing")
        pack.flag("STALE_SHARES", "no cover share count could be read from the latest filing", True, "shares")
    out["preferred_on_cover"] = prefs_cover
    # the API's dei value is a separate witness: flag when it is older than the filing's own cover
    cf = sec.fetch(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", as_json=True)
    if cf:
        node = cf["facts"].get("dei", {}).get("EntityCommonStockSharesOutstanding", {}).get("units", {}).get("shares", [])
        if node:
            api_latest = max(u["end"] for u in node)
            out["dei_api_latest"] = api_latest
            if cover_date and api_latest < cover_date:
                pack.flag("DEI_STALE_IN_XBRL_API", f"SEC companyfacts dei share count is dated {api_latest}; the filing's own cover is {cover_date} (API drops dimensional cover facts)", False, "shares")
        pack["_companyfacts_ok"] = True
    else:
        pack.flag("FETCH_FAILED:companyfacts", cik, False, "shares")
    # convertible preferred on the balance sheet (count only in v0)
    prefs = []
    if facts:
        pf = [x for x in facts if x["name"] == "PreferredStockSharesOutstanding" and x["instant"] == pe and x["val"] > 0]
        if not pf:  # some filers (Lumentum) tag only the issued count on the face
            pf = [x for x in facts if x["name"] == "PreferredStockSharesIssued" and x["instant"] == pe and x["val"] > 0]
        nodim = [x for x in pf if not x["dims"]]
        seen, rows = set(), []
        for x in (nodim or pf):
            k = tuple(x["dims"])
            if k not in seen:
                seen.add(k)
                rows.append({"series": "+".join(m for a, m in x["dims"]) or "all preferred", "shares": x["val"]})
        prefs = rows
    out["preferred_outstanding"] = resolve_preferred(pack, prefs, text, ents)
    pack["shares"] = out
    return cover_date


def classify_prospectus(sec, cik, fl):
    """424B prospectus -> shares | debt | resale | unknown (read the first ~7k characters of the document)."""
    raw = sec.fetch(base_url(cik, fl["acc"]) + fl["doc"])
    if raw is None:
        return {"kind": "unknown", "evidence": "FETCH_FAILED: could not open the prospectus", "fetch_failed": True}
    head = vis_text(raw[:260000])[:7000]
    top = head[:1800]
    hint = re.search(r"([\d,]{6,})\s+shares of (?:our |the Company.s )?(?:Class [A-Z] )?(?:common stock|ordinary shares)", head, re.I)
    ev = re.sub(r"\s+", " ", head[:260])
    sells_shares = re.search(r"(?:we are offering|are offering|offering|offer(?:ing)? and sell|sell)[^.]{0,90}\b[\d,]{5,}\s+(?:shares|ordinary shares|Class [A-Z] (?:common )?shares)", head, re.I) \
        or re.search(r"\$\s?[\d.,]+\s+(?:million|billion)\s+of\s+(?:shares of\s+)?(?:our\s+)?(?:Class [A-Z]\s+)?(?:common stock|ordinary shares)", head, re.I) \
        or re.search(r"at[- ]the[- ]market", top, re.I)
    if re.search(r"selling (?:stockholders?|shareholders?|securityholders?)", head, re.I) and re.search(r"will not receive any|not receive any proceeds", head, re.I):
        kind = "resale"
    elif re.search(r"\bnotes? due\b|\bdebentures\b|aggregate principal amount of|\d\.\d+%\s+(?:senior\s+)?notes", top, re.I) and not sells_shares:
        kind = "debt"
    elif sells_shares or re.search(r"shares of (?:our )?(?:Class [A-Z] )?(?:common stock|ordinary shares)", top, re.I):
        kind = "shares"
    else:
        kind = "unknown"
    return {"kind": kind, "evidence": ev, "offered_hint": hint.group(1) if hint else None}


def post_cover_events(sec, pack, cik, filings, cover_date, period_end, eightk):
    """Shares: anything filed after the cover date that sold/issued shares -> SHARES_MAY_BE_STALE_POST_OFFERING (blocks).
    Debt: a debt prospectus or Item 2.03 8-K filed after the balance-sheet date -> DEBT_MAY_BE_STALE_POST_FINANCING (warns)."""
    lo = min(x for x in (cover_date, period_end) if x) if (cover_date or period_end) else None
    if not lo:
        return
    pro = sorted([fl for fl in filings if fl["form"] in OFFERING_FORMS and fl["filed"] > lo], key=lambda f: f["filed"])[:10]
    with ThreadPoolExecutor(max_workers=4) as ex:
        cls = list(ex.map(lambda fl: classify_prospectus(sec, cik, fl), pro))
    ev, dev, info = [], [], []
    for fl, c in zip(pro, cls):
        item = {"filed": fl["filed"], "form": fl["form"], "acc": fl["acc"], "kind": c["kind"], "evidence": c["evidence"], "offered_hint": c.get("offered_hint")}
        if c.get("fetch_failed"):
            pack.flag("FETCH_FAILED:prospectus", f"{fl['form']} {fl['filed']} {fl['acc']}", False, "shares")
        if c["kind"] in ("shares", "unknown") and cover_date and fl["filed"] > cover_date:
            ev.append(item)
        elif c["kind"] == "debt":
            dev.append(item)
        else:
            info.append(item)
    for e in eightk:
        if cover_date and e["filed"] > cover_date and e.get("share_signal"):
            ev.append({"filed": e["filed"], "form": e["form"], "acc": e["acc"], "kind": "8-K", "items": e["items"], "evidence": e["share_signal"]})
    ev.sort(key=lambda x: x["filed"])
    pack["shares"]["post_cover_events"] = ev
    pack["shares"]["post_cover_other_prospectuses"] = info
    if ev:
        pack.flag("SHARES_MAY_BE_STALE_POST_OFFERING", f"cover date {cover_date}; {len(ev)} later filing(s) report/prepare a sale or issuance of shares, first on {ev[0]['filed']} ({ev[0]['form']})", True, "shares")
    dpost = [f for f in filings if f["form"] in ("8-K", "8-K/A") and period_end and f["filed"] > period_end and "2.03" in f["items"]]
    by_acc = {e["acc"]: e for e in eightk}
    dsig = [(e["filed"], e["debt_signal"]) for e in eightk if period_end and e["filed"] > period_end and e.get("debt_signal")]
    if dev or dpost or dsig:
        dates = sorted({x["filed"] for x in dev} | {f["filed"] for f in dpost} | {x[0] for x in dsig})
        pack["debt"]["post_period_financing"] = {"debt_prospectuses": dev, "item_2_03_8ks": [{"filed": f["filed"], "acc": f["acc"]} for f in dpost],
                                                 "sentences": [{"filed": a, "text": b} for a, b in dsig]}
        what = "; ".join(f"{a}: {b[:150]}" for a, b in dsig[:2])
        if not what and dev:
            what = "; ".join(f"{x['filed']}: debt prospectus ({x['evidence'][:70]})" for x in dev[:2])
        pack.flag("DEBT_MAY_BE_STALE_POST_FINANCING", f"balance sheet is {period_end}; later debt filings {', '.join(dates[:4])}" + (f" -- {what}" if what else ""), False, "debt")
    asig = [(e["filed"], e["acq_signal"]) for e in eightk if period_end and e["filed"] > period_end and e.get("acq_signal")]
    if asig:
        pack["cash"]["post_period_acquisitions"] = [{"filed": a, "text": b} for a, b in asig]
        pack.flag("CASH_MAY_BE_STALE_POST_ACQUISITION", f"balance sheet is {period_end}; " + "; ".join(f"{a}: {b[:170]}" for a, b in asig[:2]), False, "cash")


# --------------------------------------------------------------------------------------
# 8-K scan (12 months, material items): headline from Ex 99.x, else body after the Item text
# --------------------------------------------------------------------------------------
ITEM_TITLES = {
    "1.01": r"Entry\s+into\s+a\s+Material\s+Definitive\s+Agreement", "1.02": r"Termination\s+of\s+a\s+Material\s+Definitive\s+Agreement",
    "2.01": r"Completion\s+of\s+Acquisition\s+or\s+Disposition\s+of\s+Assets", "2.05": r"Costs\s+Associated\s+with\s+Exit\s+or\s+Disposal\s+Activities",
    "2.06": r"Material\s+Impairments", "3.02": r"Unregistered\s+Sales\s+of\s+Equity\s+Securities",
    "4.01": r"Changes\s+in\s+Registrant.{1,3}s\s+Certifying\s+Accountant",
    "4.02": r"Non-?\s?Reliance\s+on\s+Previously\s+Issued\s+Financial\s+Statements[^.]{0,80}?(?:Review|Report)",
    "5.02": r"Departure\s+of\s+Directors\s+or\s+Certain\s+Officers;?\s*Election\s+of\s+Directors;?\s*Appointment\s+of\s+Certain\s+Officers;?\s*Compensatory\s+Arrangements\s+of\s+Certain\s+Officers",
    "7.01": r"Regulation\s+FD\s+Disclosure", "8.01": r"Other\s+Events",
}
EX_TOKEN = re.compile(r"^\s*(?:EX-\d+(?:\.\d+)?|\d{1,3}\s+\S+\.htm|(?:EXHIBIT|Exhibit)\s+\d+(?:\.\d+)?|PRESS RELEASE|NEWS RELEASE|FOR IMMEDIATE RELEASE)\b[:.]?\s*", re.S)


def ex99_links(raw):
    out = []
    for m in re.finditer(r'href="([^"#]+)"', raw, re.I):
        h = m.group(1)
        if re.search(r"ex[\-_]?99", h, re.I) and h not in out:
            out.append(h)

    def key(h):
        m = re.search(r"99[_\-.]?(\d+)", h)
        return int(m.group(1)) if m else 99
    return sorted(out, key=key)


def clean_exhibit(x):
    for _ in range(12):
        y = EX_TOKEN.sub("", x, count=1)
        if y == x:
            break
        x = y
    # drop a letterhead address block (street ... ZIP) sitting in front of the headline
    m = re.match(r"^(.{0,200}?\b\d{1,5}\s+[A-Z][\w .#,]{3,60}?(?:Street|Avenue|Road|Drive|Boulevard|Way|Parkway|Suite|Floor)\b.{0,80}?\b\d{5}(?:-\d{4})?\)?)\s+(?=\S)", x)
    if m and len(m.group(1)) < 220:
        x = x[m.end():]
    return x.strip()


def body_after_item(x, items):
    best = None
    for it in items:
        pat = ITEM_TITLES.get(it)
        if not pat:
            continue
        m = re.search(r"Item\s+" + re.escape(it) + r"\.?\s*" + pat + r"\.?", x, re.I)
        if m and (best is None or m.start() < best.start()):
            best = m
    if best is None:
        m = re.search(r"Item\s+\d\.\d\d\.?\s+[A-Z]", x)
        return x[m.end() - 1:] if m else x
    return x[best.end():].strip()


def detail_sentence(x):
    trig = re.compile(r"warrant|preferred|convertible|offering|issued|issuance|purchase agreement|merger|acquisition|acquire|consideration|exchange|placement|shares", re.I)
    big = re.compile(r"\d{1,3}(?:,\d{3}){2,}|\$\s?[\d.,]+\s*(?:million|billion)|[\d.]+\s+million\s+shares")
    for s in re.split(r"(?<=[.!?])\s+(?=[A-Z“\"(])", x[:6000]):
        if trig.search(s) and big.search(s):
            return s[:320]
    return None


BAD_EXHIBIT_START = re.compile(r"^(index to|table of contents|unaudited|condensed|financial statements|consolidated|report of independent)", re.I)


DEBT_SENT = [r"increased the principal amount[^.]{0,160}\$[\d,.]+", r"(?:entered into|executed)[^.]{0,120}(?:credit agreement|credit facility|term loan|indenture|note purchase)[^.]{0,160}\$[\d,.]+",
             r"(?:issued|priced|completed|closed)[^.]{0,100}(?:senior|convertible|term|floating rate) notes[^.]{0,200}\$[\d,.]+", r"aggregate principal amount[^.]{0,120}(?:notes|loans?)[^.]{0,80}\$?[\d,.]+",
             r"\$[\d,.]+\s+(?:million|billion)[^.]{0,80}(?:term loan|revolving credit facility|credit facility)"]
ACQ_SENT = [r"(?:completed|closed|consummated)[^.]{0,80}acquisition of[^.]{0,200}\$[\d,.]+\s*(?:million|billion)", r"(?:completed|closed|consummated)[^.]{0,80}acquisition of[^.]{0,200}(?:cash|stock)"]


def sentence_matching(text, pats):
    for sn in re.split(r"(?<=[.!?])\s+(?=[A-Z\u201c\"(])", text[:80000]):
        for pt in pats:
            if re.search(pt, sn, re.I):
                return re.sub(r"\s+", " ", sn)[:260]
    return None


def eightk_entry(sec, cik, fl):
    base = base_url(cik, fl["acc"])
    raw = sec.fetch(base + fl["doc"])
    ent = {"filed": fl["filed"], "form": fl["form"], "items": fl["items"], "acc": fl["acc"], "doc": fl["doc"]}
    if raw is None:
        ent.update(headline="n/a", source="FETCH_FAILED", detail=None, share_signal=None, fetch_failed=True)
        return ent
    body = body_after_item(vis_text(raw), [i for i in fl["items"] if i in ITEM_TITLES])
    headline, src, ex_text = None, "body", ""
    for h in ex99_links(raw)[:2]:
        url = h if h.startswith("http") else (("https://www.sec.gov" + h) if h.startswith("/") else base + h)
        exr = sec.fetch(url)
        if exr:
            ex_text = clean_exhibit(vis_text(exr))
            if ex_text and not BAD_EXHIBIT_START.match(ex_text):
                headline, src = ex_text[:300], "Ex " + h.split("/")[-1]
                break
    if headline is None:
        headline = body[:300]
    pm = re.search(r"(?:issuance and sale of|issued and sold|sale and issuance of|sold|issued)\s+(?:approximately\s+)?([\d,]{6,})\s+shares of[^.]{0,90}?Preferred Stock", body, re.I)
    full = vis_text(raw)
    ent.update(headline=headline, source=src, detail=detail_sentence(body), share_signal=share_signal(body + " " + ex_text[:20000]),
               debt_signal=sentence_matching(full, DEBT_SENT), acq_signal=sentence_matching(full, ACQ_SENT),
               pref_count=float(pm.group(1).replace(",", "")) if pm else None)
    return ent


def scan_8ks(sec, pack, cik, filings):
    since = (today() - dt.timedelta(days=365)).isoformat()
    sel = [f for f in filings if f["form"] in ("8-K", "8-K/A") and f["filed"] >= since and set(f["items"]) & set(MATERIAL_ITEMS)]
    sel.sort(key=lambda f: f["filed"], reverse=True)
    with ThreadPoolExecutor(max_workers=4) as ex:
        ents = list(ex.map(lambda fl: eightk_entry(sec, cik, fl), sel))
    for e in ents:
        if e.get("fetch_failed"):
            pack.flag("FETCH_FAILED:8-K", f"{e['filed']} {e['acc']}", False, "8k")
    pack["eightk"] = ents
    pack["eightk_window"] = {"since": since, "material_items": list(MATERIAL_ITEMS), "count": len(ents)}
    return ents


# --------------------------------------------------------------------------------------
# latest quarter, TTM and the TTM audit
# --------------------------------------------------------------------------------------
REV_TAGS = ["RevenueFromContractWithCustomerExcludingAssessedTax", "Revenues", "RevenueFromContractWithCustomerIncludingAssessedTax",
            "SalesRevenueNet", "SalesRevenueGoodsNet", "SalesRevenueServicesNet", "RevenuesNetOfInterestExpense"]
COST_TAGS = ["CostOfRevenue", "CostOfGoodsAndServicesSold", "CostOfGoodsSold", "CostOfGoodsAndServiceExcludingDepreciationDepletionAndAmortization"]
OPINC_TAGS = ["OperatingIncomeLoss"]
OCF_TAGS = ["NetCashProvidedByUsedInOperatingActivities", "NetCashProvidedByUsedInOperatingActivitiesContinuingOperations"]
CAPEX_TAGS = ["PaymentsToAcquirePropertyPlantAndEquipment", "PaymentsToAcquireProductiveAssets", "PaymentsToAcquirePropertyPlantAndEquipmentAndIntangibleAssets"]
SBC_TAGS = ["ShareBasedCompensation", "AllocatedShareBasedCompensationExpense"]
DILUTED_TAGS = ["WeightedAverageNumberOfDilutedSharesOutstanding"]


def latest_filed(units):
    """One fact per (start, end): the most recently filed (a restatement/amendment beats the original)."""
    best = {}
    for u in units:
        if u.get("val") is None:
            continue
        k = (u.get("start"), u.get("end"))
        if k not in best or u.get("filed", "") >= best[k].get("filed", ""):
            best[k] = u
    return list(best.values())


def cf_series(cf, tags, unit="USD"):
    """The FRESHEST tag (not the first that parses): filers abandon concepts without deleting history."""
    best = None
    for tag in tags:
        node = (cf or {}).get("facts", {}).get("us-gaap", {}).get(tag)
        if not node or unit not in node["units"]:
            continue
        units = latest_filed(node["units"][unit])
        q, twelve = quarters(units)
        if len(q) < 2:
            continue
        latest = max(q)
        if best is None or latest > best["latest"]:
            best = {"tag": tag, "q": q, "twelve": twelve, "latest": latest, "units": units}
    return best


def native_quarters(cf, tag, unit="shares"):
    node = (cf or {}).get("facts", {}).get("us-gaap", {}).get(tag)
    if not node or unit not in node["units"]:
        return {}
    out = {}
    for u in latest_filed(node["units"][unit]):
        if u.get("start") and u.get("end") and 80 <= (d(u["end"]) - d(u["start"])).days <= 100:
            out[u["end"]] = float(u["val"])
    return dict(sorted(out.items()))


def year_ago(series, end):
    for e in sorted(series, reverse=True):
        if 350 <= (d(end) - d(e)).days <= 380:
            return e, series[e]
    return None, None


def contiguous(ends):
    return all(75 <= (d(b) - d(a)).days <= 110 for a, b in zip(ends, ends[1:]))


def ttm_of(q, offset=0):
    ends = list(q)
    hi = len(ends) - offset
    if hi < 4:
        return None, []
    w = ends[hi - 4:hi]
    return (sum(q[e] for e in w), w) if contiguous(w) else (None, w)


def audit_ttm(ser, window, q_sum, label):
    """Compare a summed TTM with the filer's own twelve-month figure(s). -> (ok|None, text)."""
    if not window or q_sum is None:
        return None, "no TTM to audit"
    end = window[-1]
    tw = ser["twelve"]
    if end in tw:
        ref, how = tw[end], f"filer's own 12-month fact ending {end}"
    else:
        # FY(last fiscal year end) + YTD(current) - YTD(prior), all filer-reported
        fys = sorted(e for e in tw if (d(end) - d(e)).days > 20)
        if not fys:
            return None, "no 12-month fact and no fiscal-year anchor: TTM unaudited"
        fy_end = fys[-1]
        cur = [u for u in ser["units"] if u.get("start") and u["end"] == end and 80 <= (d(u["end"]) - d(u["start"])).days <= 290 and abs((d(u["start"]) - d(fy_end)).days) <= 8]
        pri = [u for u in ser["units"] if u.get("start") and abs((d(end) - d(u["end"])).days - 365) <= 12 and 80 <= (d(u["end"]) - d(u["start"])).days <= 290 and abs((d(u["start"]) - d(fy_end)).days + 365) <= 12]
        if not cur or not pri:
            return None, "no FY+YTD path in the filer's own facts: TTM unaudited"
        ref, how = tw[fy_end] + cur[0]["val"] - pri[0]["val"], f"filer's FY {fy_end} + YTD {end} - prior YTD"
    if not ref:
        return None, "reference is zero: TTM unaudited"
    dev = (q_sum / ref - 1) * 100
    return (abs(dev) <= 2.0), f"summed {money(q_sum)} vs {how} {money(ref)} ({dev:+.2f}%)"


def pick_row(rp, tags=None, label_re=None, col=0, mode="max"):
    cands = []
    for r in rp["rows"]:
        if r["abstract"] or col >= len(r["vals"]) or r["vals"][col] is None:
            continue
        if (tags and r["tag"].split(":")[-1] in tags) or (label_re and re.search(label_re, r["label"], re.I)):
            cands.append(r)
    if not cands:
        return None
    if tags:
        tagged = [r for r in cands if r["tag"].split(":")[-1] in tags]
        cands = tagged or cands
    return max(cands, key=lambda r: r["vals"][col]) if mode == "max" else cands[0]


def col_for(rp, end, months):
    for i, c in enumerate(rp["cols"]):
        if c["end"] == end and c["months"] == months:
            return i
    return None


def quarter_from_filing(sec, pack, cik, f, cf):
    """STALE_QUARTER path: read the latest 10-Q's own income statement and cash-flow statement."""
    reps = rpage_list(sec, cik, f["acc"])
    if not reps:
        pack.flag("FETCH_FAILED:FilingSummary(quarter)", f["acc"], False, "quarter")
        return None
    pe = f["report"]
    src = f"{f['form']} {f['filed']} statements ({f['acc']})"
    is_name, cf_name = find_report(reps, "is"), find_report(reps, "cf")
    out = {"period_end": pe, "months": 3, "origin": "filing statements (SEC XBRL API lags this filing)"}
    if not is_name:
        return None
    is_rp = parse_rpage(sec.fetch(base_url(cik, f["acc"]) + is_name) or "")
    c0 = col_for(is_rp, pe, 3)
    if c0 is None:
        pack.flag("QUARTER_COLUMN_NOT_FOUND", f"no 3-month column ending {pe} in {is_name} (10-K or odd layout)", False, "quarter")
        return None
    pe_prev = next((c["end"] for c in is_rp["cols"] if c["months"] == 3 and 350 <= (d(pe) - d(c["end"])).days <= 380), None)
    c1 = col_for(is_rp, pe_prev, 3) if pe_prev else None
    rev = pick_row(is_rp, REV_TAGS, r"^(total )?(net )?(revenues?|sales)( net)?\b", c0)
    if not rev:
        pack.flag("QUARTER_REVENUE_NOT_FOUND", f"no revenue row in {is_name}", False, "quarter")
        return None
    out["revenue"] = fig(rev["vals"][c0], pe, f"{rev['tag']} in {is_name}; {src}", "filing-text")
    if c1 is not None and rev["vals"][c1]:
        out["revenue_year_ago"] = fig(rev["vals"][c1], pe_prev, f"{rev['tag']} in {is_name}; {src}", "filing-text")
        out["revenue_yoy_pct"] = fig((rev["vals"][c0] / rev["vals"][c1] - 1) * 100, pe, "computed from the two printed revenue figures", "filing-text")
    gp = pick_row(is_rp, ["GrossProfit"], r"^gross (profit|margin)", c0)
    cost = None if gp else pick_row(is_rp, COST_TAGS, r"^cost of (revenues?|sales|goods sold)", c0)
    if gp:
        out["gross_profit"] = fig(gp["vals"][c0], pe, f"{gp['tag']}; {src}", "filing-text")
    elif cost:
        out["gross_profit"] = fig(rev["vals"][c0] - abs(cost["vals"][c0]), pe, f"revenue minus {cost['tag']}; {src}", "filing-text", note="derived: revenue minus cost of revenue")
    op = pick_row(is_rp, OPINC_TAGS, r"^(operating (income|loss|\(loss\) income|income \(loss\))|(income|loss|\(loss\) income|income \(loss\)) from operations)", c0, "first")
    if op:
        out["operating_income"] = fig(op["vals"][c0], pe, f"{op['tag']}; {src}", "filing-text")
    dl = pick_row(is_rp, DILUTED_TAGS, r"^diluted$", c0, "first")
    if dl and c1 is not None and dl["vals"][c1]:
        out["diluted_shares"] = fig(dl["vals"][c0], pe, f"{dl['tag']}; {src}", "filing-text")
        out["diluted_shares_year_ago"] = fig(dl["vals"][c1], pe_prev, f"{dl['tag']}; {src}", "filing-text")
    # YTD cash flow -> quarter (subtract the previous YTD from the filer's own earlier facts)
    if cf_name:
        cf_rp = parse_rpage(sec.fetch(base_url(cik, f["acc"]) + cf_name) or "")
        ycol = next((i for i, c in enumerate(cf_rp["cols"]) if c["end"] == pe and c["months"]), None)
        if ycol is not None:
            m = cf_rp["cols"][ycol]["months"]
            for key, tags, lre in (("ocf", OCF_TAGS, r"^net cash (provided by|used in|\(used in\) provided by|provided by \(used in\)).*operating"),
                                   ("capex", CAPEX_TAGS, r"(purchases?|acquisitions?|additions?|payments?|expenditures?).{0,40}(property|equipment|plant|software)|capital expenditures")):
                row = pick_row(cf_rp, tags, lre, ycol, "first")
                if not row:
                    continue
                ytd = abs(row["vals"][ycol]) if key == "capex" else row["vals"][ycol]
                prior = 0.0
                if m > 3:
                    ser = cf_series(cf, tags)
                    prev = None
                    if ser:
                        for u in ser["units"]:
                            if u.get("start") and abs((d(u["end"]) - d(pe)).days + 91) <= 12 and abs((d(u["start"]) - (d(pe) - dt.timedelta(days=int(m * 30.4)))).days) <= 15:
                                prev = float(u["val"])
                    if prev is None:
                        pack.flag("QUARTER_CASHFLOW_NOT_DERIVABLE", f"{key}: no earlier YTD fact to subtract from the {m}-month figure", False, "quarter")
                        continue
                    prior = prev
                out[key] = fig(ytd - prior, pe, f"{m}-month YTD in {cf_name}" + (" minus the prior YTD" if m > 3 else "") + f"; {src}", "filing-text")
                out[key + "_ytd"] = {"months": m, "value": ytd, "prior_ytd": prior}
    return out


def build_quarter(sec, pack, cik, f0):
    cf = sec.fetch(f"https://data.sec.gov/api/xbrl/companyfacts/CIK{cik}.json", as_json=True)
    pe = f0["report"]
    rev = cf_series(cf, REV_TAGS)
    q = {"period_end": pe}
    stale = rev is None or (d(pe) - d(rev["latest"])).days > 30
    if stale:
        last = rev["latest"] if rev else "none"
        pack.flag("STALE_QUARTER", f"the SEC XBRL feed's last revenue quarter is {last}; the latest {f0['form']} is {pe} (filed {f0['filed']}): reading the filing's own statements", False, "quarter")
        fq = quarter_from_filing(sec, pack, cik, f0, cf)
        if fq:
            q.update(fq)
            q["status"] = "STALE_QUARTER: read from the filing"
        else:
            q["status"] = "n/a"
            q["revenue"] = na("XBRL feed stale and the filing's statements could not be read")
            pack.flag("QUARTER_UNAVAILABLE", "no current quarter could be established", False, "quarter")
    else:
        sec_src = f"companyfacts {rev['tag']} (SEC XBRL API)"
        e = rev["latest"]
        q.update(status="xbrl", months=3, origin=sec_src)
        q["revenue"] = fig(rev["q"][e], e, sec_src, "filing-xbrl")
        ye, yv = year_ago(rev["q"], e)
        if yv:
            q["revenue_year_ago"] = fig(yv, ye, sec_src, "filing-xbrl")
            q["revenue_yoy_pct"] = fig((rev["q"][e] / yv - 1) * 100, e, "computed from the two printed revenue figures", "filing-xbrl")
        gp = cf_series(cf, ["GrossProfit"])
        if gp and e in gp["q"]:
            q["gross_profit"] = fig(gp["q"][e], e, "companyfacts GrossProfit", "filing-xbrl")
        else:
            cost = cf_series(cf, COST_TAGS)
            if cost and e in cost["q"]:
                q["gross_profit"] = fig(rev["q"][e] - cost["q"][e], e, f"revenue minus companyfacts {cost['tag']}", "filing-xbrl", note="derived: revenue minus cost of revenue")
        op = cf_series(cf, OPINC_TAGS)
        if op and e in op["q"]:
            q["operating_income"] = fig(op["q"][e], e, "companyfacts OperatingIncomeLoss", "filing-xbrl")
        for key, tags in (("ocf", OCF_TAGS), ("capex", CAPEX_TAGS)):
            ser = cf_series(cf, tags)
            if ser and e in ser["q"]:
                q[key] = fig(abs(ser["q"][e]) if key == "capex" else ser["q"][e], e, f"companyfacts {ser['tag']}", "filing-xbrl")
    if q.get("revenue", {}).get("value"):
        r = q["revenue"]["value"]
        if q.get("gross_profit"):
            q["gross_margin_pct"] = fig(q["gross_profit"]["value"] / r * 100, q["revenue"]["period_end"], "computed from printed gross profit / revenue", q["revenue"]["grade"])
        if q.get("operating_income"):
            q["operating_margin_pct"] = fig(q["operating_income"]["value"] / r * 100, q["revenue"]["period_end"], "computed GAAP operating income / revenue", q["revenue"]["grade"])
    pack["quarter"] = q
    # ---------------- TTM (revenue, free cash flow, stock compensation) with the audit
    ttm_out = {}
    for key, tags in (("revenue", REV_TAGS), ("ocf", OCF_TAGS), ("capex", CAPEX_TAGS), ("sbc", SBC_TAGS)):
        ser = cf_series(cf, tags)
        if not ser:
            ttm_out[key] = na(f"no {key} series in the SEC XBRL feed")
            continue
        qq = dict(ser["q"])
        origin = f"companyfacts {ser['tag']}"
        # append the quarter read from the filing when the feed is stale and it is the very next quarter
        if stale and q.get("status", "").startswith("STALE") and key in ("revenue", "ocf", "capex") and q.get(key, {}).get("value") is not None:
            if 75 <= (d(pe) - d(ser["latest"])).days <= 110:
                qq[pe] = abs(q[key]["value"]) if key == "capex" else q[key]["value"]
                origin += f" + {pe} quarter read from the filing"
        qq = dict(sorted(qq.items()))
        s_, w = ttm_of(qq)
        if s_ is None:
            ttm_out[key] = na("four consecutive quarters not available (gap in the feed)" if w else "fewer than four quarters")
            pack.flag("TTM_GAP", f"{key}: no four contiguous quarters", False, "ttm")
            continue
        if w[-1] != pe and (d(pe) - d(w[-1])).days > 30:
            pack.flag("TTM_STALE", f"{key} TTM ends {w[-1]}, latest period is {pe}", False, "ttm")
        ok, txt = audit_ttm({"twelve": ser["twelve"], "units": ser["units"]}, w, s_, key)
        if ok is False:
            ttm_out[key] = fig(None, w[-1], origin, "filing-xbrl", note=f"REFUSED: TTM audit failed: {txt}", audit=txt, window=w)
            pack.flag("TTM_AUDIT_FAILED", f"{key}: {txt}", False, "ttm")
        else:
            ttm_out[key] = fig(s_, w[-1], origin + f"; four quarters {w[0]}..{w[-1]}", "filing-xbrl", audit=(txt if ok else f"unaudited: {txt}"), window=w)
    if ttm_out.get("ocf", {}).get("value") is not None and ttm_out.get("capex", {}).get("value") is not None and ttm_out["ocf"]["period_end"] == ttm_out["capex"]["period_end"]:
        ttm_out["free_cash_flow"] = fig(ttm_out["ocf"]["value"] - abs(ttm_out["capex"]["value"]), ttm_out["ocf"]["period_end"], "TTM operating cash flow minus TTM capital spending", "filing-xbrl")
    else:
        ttm_out["free_cash_flow"] = na("operating cash flow and capex TTM windows do not both exist/align")
    pack["ttm"] = ttm_out
    # ---------------- diluted share change YoY (native 3-month facts only: weighted averages cannot be differenced)
    dil = {}
    if q.get("diluted_shares"):
        a, b = q["diluted_shares"]["value"], q["diluted_shares_year_ago"]["value"]
        if b and 0.2 <= a / b <= 5:
            dil = {"latest": q["diluted_shares"], "year_ago": q["diluted_shares_year_ago"], "change_yoy_pct": fig((a / b - 1) * 100, q["diluted_shares"]["period_end"], "computed from the two printed weighted diluted share counts", "filing-text")}
        else:
            pack.flag("DILUTED_SHARES_SCALE_MISMATCH", f"{a} vs {b}: refusing to compute (unit scale differs)", False, "ttm")
    else:
        ds = native_quarters(cf, DILUTED_TAGS[0])
        if ds:
            e = max(ds)
            ye, yv = year_ago(ds, e)
            if yv and (d(pe) - d(e)).days <= 40:
                if 0.2 <= ds[e] / yv <= 5:
                    dil = {"latest": fig(ds[e], e, "companyfacts WeightedAverageNumberOfDilutedSharesOutstanding", "filing-xbrl"), "year_ago": fig(yv, ye, "same tag", "filing-xbrl"),
                           "change_yoy_pct": fig((ds[e] / yv - 1) * 100, e, "computed from the two printed weighted diluted share counts", "filing-xbrl")}
                else:
                    pack.flag("DILUTED_SHARES_SCALE_MISMATCH", f"{ds[e]} vs {yv}: refusing to compute (unit scale differs)", False, "ttm")
    pack["dilution"] = dil or {"change_yoy_pct": na("no comparable native-quarter diluted share counts (e.g. Q4 is not reported as a discrete quarter)")}
    return cf


# --------------------------------------------------------------------------------------
# price (yfinance history() only -- never .info)
# --------------------------------------------------------------------------------------
def get_price(pack, ticker):
    try:
        import warnings
        warnings.filterwarnings("ignore")
        import yfinance as yf
        h = yf.Ticker(ticker).history(period="2y", auto_adjust=False)
    except Exception as e:  # noqa: BLE001
        pack.flag("FETCH_FAILED:yfinance history", str(e)[:100], True, "market")
        return
    if h is None or len(h) == 0:
        pack.flag("FETCH_FAILED:yfinance history", "empty", True, "market")
        return
    rows = [(ix.date().isoformat(), float(c)) for ix, c in zip(h.index, h["Close"])]
    if rows and rows[-1][1] != rows[-1][1]:
        pack.flag("LAST_CLOSE_NAN", f"vendor returned NaN for {rows[-1][0]}; using the previous valid close", False, "market")
    rows = [r for r in rows if r[1] == r[1]]
    if not rows:
        pack.flag("FETCH_FAILED:yfinance history", "no valid closes", True, "market")
        return
    try:
        from zoneinfo import ZoneInfo
        now_et = dt.datetime.now(ZoneInfo("America/New_York"))
        if rows[-1][0] == now_et.date().isoformat() and now_et.hour * 60 + now_et.minute < 16 * 60 + 5:
            rows = rows[:-1]  # today's bar is not a close yet
    except Exception:  # noqa: BLE001
        pass
    last_d, last_c = rows[-1]
    cut = (d(last_d) - dt.timedelta(days=365)).isoformat()
    one_y = [r for r in rows if r[0] <= cut]
    win = [r for r in rows if r[0] > cut]
    m = {"close": fig(last_c, last_d, "yfinance history() close", "vendor")}
    if one_y:
        m["close_one_year_ago"] = fig(one_y[-1][1], one_y[-1][0], "yfinance history() close", "vendor")
        m["change_1y_pct"] = fig((last_c / one_y[-1][1] - 1) * 100, last_d, "computed from the two printed closes", "vendor")
    hi, lo = max(win, key=lambda r: r[1]), min(win, key=lambda r: r[1])
    m["high_52w_close"] = fig(hi[1], hi[0], "yfinance history() closing high", "vendor")
    m["low_52w_close"] = fig(lo[1], lo[0], "yfinance history() closing low", "vendor")
    if (today() - d(last_d)).days > 10:
        pack.flag("STALE_CLOSE", f"last close is {last_d}", True, "market")
    elif (today() - d(last_d)).days > 4:
        pack.flag("OLD_CLOSE", f"last close is {last_d}", False, "market")
    pack["market"] = m


# --------------------------------------------------------------------------------------
# the self-audit: pure function of the pack, so it can be unit-tested with a stale input
# --------------------------------------------------------------------------------------
def audit_pack(pack):
    latest = (pack.get("filing") or {}).get("period_end")
    filed = (pack.get("filing") or {}).get("filed")
    reasons = []

    def older(fg, label):
        if not fg or fg.get("value") is None:
            reasons.append(f"{label}: n/a (could not be established)")
            return
        pe = fg.get("period_end")
        if not pe:
            reasons.append(f"{label}: no period/date attached")
        elif latest and pe < latest:
            reasons.append(f"{label}: period {pe} is older than the latest 10-Q/10-K period end {latest}")

    cash = pack.get("cash") or {}
    older(cash.get("cash_and_equivalents"), "cash")
    if cash.get("short_term_investments") and cash["short_term_investments"].get("value"):
        older(cash["short_term_investments"], "short-term investments")
    older((pack.get("debt") or {}).get("carrying"), "debt")
    sh = ((pack.get("shares") or {}).get("common_total")) or {}
    if not sh or sh.get("value") is None:
        reasons.append("shares: n/a (no cover count)")
    else:
        if filed and sh["period_end"] and (d(filed) - d(sh["period_end"])).days > 45:
            reasons.append(f"shares: cover date {sh['period_end']} is more than 45 days before the filing date {filed}")
    for f in pack.get("flags", []):
        if f["block"]:
            reasons.append(f"flag {f['code']}" + (f" ({f['detail']})" if f["detail"] else ""))
    px = ((pack.get("market") or {}).get("close")) or {}
    if px.get("value") is None:
        reasons.append("price: no close")
    # drop duplicate wording
    seen, uniq = set(), []
    for r in reasons:
        if r not in seen:
            seen.add(r)
            uniq.append(r)
    out = {"market_value": {"status": "REFUSED", "reasons": uniq}, "ev": {"status": "REFUSED", "reasons": uniq}}
    if not uniq:
        prefs_unknown = [p for p in ((pack.get("shares") or {}).get("preferred_outstanding") or []) if p.get("as_converted") is None]
        if prefs_unknown:
            r = [f"preferred stock outstanding ({', '.join(p['series'] + ' ' + format(p['shares'], ',.0f') for p in prefs_unknown)}); as-converted common shares not established"]
            out = {"market_value": {"status": "REFUSED", "reasons": r}, "ev": {"status": "REFUSED", "reasons": r}}
            pack.flag("PREFERRED_AS_CONVERTED_UNKNOWN", r[0], True, "shares")
            return out
        total = sh["value"] + sum(p["as_converted"] for p in (pack["shares"].get("preferred_outstanding") or []))
        mv = px["value"] * total
        mv_cav = [f for f in pack.get("flags", []) if not f["block"] and f["code"] in ("OLD_CLOSE", "COVER_FROM_TEXT", "LAST_CLOSE_NAN", "NONCONVERTIBLE_PREFERRED_NOT_ADDED")]
        ev_cav = mv_cav + [f for f in pack.get("flags", []) if not f["block"] and f["code"] in ("DEBT_MAY_BE_STALE_POST_FINANCING", "CASH_MAY_BE_STALE_POST_ACQUISITION", "CASH_SUBTOTAL_MISMATCH")]
        out["market_value"] = {"status": "OK", "value": mv, "shares_used": total, "close": px["value"], "close_date": px["period_end"], "reasons": [],
                               "caveats": [{"code": f["code"], "detail": f["detail"]} for f in mv_cav]}
        debt = pack["debt"]["carrying"]["value"]
        liq = cash["cash_and_equivalents"]["value"] + (cash["short_term_investments"]["value"] or 0)
        out["ev"] = {"status": "OK", "value": mv + debt - liq, "formula": "market value + debt (carrying) - cash and equivalents - current investments", "reasons": [],
                     "balance_sheet_date": latest, "current": not ev_cav, "caveats": [{"code": f["code"], "detail": f["detail"]} for f in ev_cav]}
    return out


# --------------------------------------------------------------------------------------
# rendering
# --------------------------------------------------------------------------------------
def fline(label, fg, extra="", fmt=None):
    if not fg:
        return f"  {label}: n/a"
    if fg.get("value") is None:
        return f"  {label}: n/a  [{fg.get('note', '')}]"
    return f"  {label}: {(fmt or money)(fg['value'])}  | as of {fg.get('period_end')} | {fg.get('source')} | grade {fg.get('grade')}{extra}"


def render_block(p):
    L = [f"=== {p['ticker']} -- {p.get('name', '?')} (CIK {p.get('cik', '?')}) | {p.get('filer_type', '')} | run {p['run_utc']}"]
    fl = p.get("flags", [])
    L.append("FLAGS: " + ("; ".join(f"{f['code']}{'*' if f['block'] else ''}" + (f" [{f['detail']}]" if f["detail"] else "") for f in fl) if fl else "none"))
    if "filing" in p:
        L.append(f"LATEST PERIODIC: {p['filing']['form']} period end {p['filing']['period_end']} filed {p['filing']['filed']} ({p['filing']['acc']})")
    mk = p.get("market")
    if mk:
        L.append(fline("CLOSE", mk["close"], fmt=px))
        if mk.get("change_1y_pct"):
            L.append(f"  1y change: {mk['change_1y_pct']['value']:+.1f}% (vs {px(mk['close_one_year_ago']['value'])} on {mk['close_one_year_ago']['period_end']})")
        L.append(f"  52w closing high {px(mk['high_52w_close']['value'])} ({mk['high_52w_close']['period_end']}) / low {px(mk['low_52w_close']['value'])} ({mk['low_52w_close']['period_end']})")
    c = p.get("cash") or {}
    L.append("CASH:")
    for k, lab in (("cash_and_equivalents", "cash and equivalents"), ("short_term_investments", "current investments"), ("cash_plus_current_investments", "cash + current investments"),
                   ("noncurrent_securities_apart", "noncurrent securities (apart, not added)"), ("equity_securities_apart", "equity securities (apart, not added)"),
                   ("restricted_cash_current", "restricted cash current (apart)"), ("restricted_cash_noncurrent", "restricted cash noncurrent (apart)")):
        if c.get(k):
            L.append(fline(lab, c[k]))
    dbt = p.get("debt") or {}
    L.append("DEBT:")
    if dbt.get("carrying"):
        L.append(fline("carrying value (current + noncurrent borrowings + convertibles)", dbt["carrying"]))
    for ln in dbt.get("lines", []):
        L.append(f"    - {ln['label'][:60]} [{ln['tag']}] {money(ln['value'])} ({ln['section']})")
    pr = dbt.get("principal")
    if pr and pr.get("value") is not None:
        diff = pr.get("differs_from_carrying_pct")
        L.append(fline("principal (face)", pr, extra=f" | {diff:+.2f}% vs carrying" if diff is not None else ""))
    elif pr:
        L.append(f"  principal (face): n/a  [{pr.get('note', '')}]")
    for inf in dbt.get("instrument_face_amounts", []):
        L.append(f"    - instrument face {money(inf['face'])}: {inf['member'][:90]}")
    if dbt.get("finance_leases_apart"):
        L.append(fline("finance leases (apart, not added)", dbt["finance_leases_apart"]))
    s = p.get("shares") or {}
    L.append("SHARES:")
    if s.get("common_total"):
        L.append(fline("cover total (classes summed)", {**s["common_total"], "value": s["common_total"]["value"]}).replace("$", "").replace("bn", "").replace("m  |", "m  |"))
    for cl in s.get("classes", []):
        L.append(f"    - {cl['class']}: {cl['value']:,.0f}" + ("  (preferred class on cover)" if cl["preferred"] else ""))
    for pf in s.get("preferred_outstanding", []):
        L.append(f"    - preferred outstanding at period end: {pf['series']} {pf['shares']:,.0f}")
    for e in s.get("post_cover_events", []):
        L.append(f"    ! after cover date: {e['filed']} {e['form']}: {e['evidence'][:160]}")
    q = p.get("quarter")
    if q:
        L.append(f"LATEST QUARTER ({q.get('status', 'n/a')}; period end {q.get('period_end')}):")
        for k, lab in (("revenue", "revenue"), ("revenue_year_ago", "revenue, year-ago quarter"), ("gross_profit", "gross profit"),
                       ("operating_income", "GAAP operating income"), ("ocf", "operating cash flow"), ("capex", "capital spending")):
            if q.get(k):
                L.append(fline(lab, q[k]))
        for k, lab, sg in (("revenue_yoy_pct", "revenue growth YoY", "+"), ("gross_margin_pct", "gross margin", ""), ("operating_margin_pct", "GAAP operating margin", "")):
            if q.get(k) and q[k].get("value") is not None:
                L.append(f"  {lab}: {q[k]['value']:{sg}.1f}%  | {q[k]['source']} | grade {q[k]['grade']}")
    t = p.get("ttm")
    if t:
        L.append("TRAILING TWELVE MONTHS (four contiguous quarters, audited against the filer's own 12-month fact where one exists):")
        for k, lab in (("revenue", "revenue"), ("free_cash_flow", "free cash flow (operating cash flow - capex)"), ("sbc", "stock compensation")):
            fg = t.get(k)
            if fg and fg.get("value") is not None:
                L.append(fline("TTM " + lab, fg, extra=f" | audit: {fg.get('audit', 'n/a')}" if fg.get("audit") else ""))
            elif fg:
                L.append(f"  TTM {lab}: n/a  [{fg.get('note', '')}]")
    dl = p.get("dilution") or {}
    if dl.get("change_yoy_pct") and dl["change_yoy_pct"].get("value") is not None:
        L.append(f"DILUTED SHARES YoY: {dl['change_yoy_pct']['value']:+.1f}%  ({num(dl['latest']['value'])} on {dl['latest']['period_end']} vs {num(dl['year_ago']['value'])} on {dl['year_ago']['period_end']}) | grade {dl['change_yoy_pct']['grade']}")
    a = p.get("audit") or {}
    for key, lab in (("market_value", "MARKET VALUE"), ("ev", "EV")):
        r = a.get(key)
        if not r:
            continue
        if r["status"] == "OK":
            cav = "; ".join(f"{c['code']} [{c['detail']}]" for c in r.get("caveats", []))
            tag = ""
            if key == "ev" and r.get("caveats"):
                tag = f" (balance sheet {r['balance_sheet_date']} basis -- NOT CURRENT: {cav})"
            elif cav:
                tag = f" (CAVEAT: {cav})"
            L.append(f"{lab}{tag}: {money(r['value'])}" + (f"  (close {px(r['close'])} on {r['close_date']} x {r['shares_used']:,.0f} shares)" if key == "market_value" else f"  ({r['formula']})"))
        else:
            L.append(f"{lab}: REFUSED -- " + "; ".join(r["reasons"]))
    e8 = p.get("eightk")
    if e8 is not None:
        L.append(f"8-K SCAN since {p['eightk_window']['since']} (items {','.join(MATERIAL_ITEMS)}): {len(e8)} filing(s)")
        for e in e8:
            L.append(f"  {e['filed']} {e['form']} items {','.join(e['items'])} | {e['source']} | {e['headline'][:300]}")
            if e.get("detail"):
                L.append(f"      detail: {e['detail']}")
    return "\n".join(L)


# --------------------------------------------------------------------------------------
# orchestration
# --------------------------------------------------------------------------------------
def build(sec, ticker, args=None):
    t0 = time.time()
    pack = run_ticker(sec, ticker, args)
    if "filing" in pack and pack.get("cik"):
        cik = pack["cik"]
        since = (today() - dt.timedelta(days=372)).isoformat()
        _, filings = load_filings(sec, cik, since)
        cand = latest_periodic(filings) if pack["filer_type"] == "domestic" else foreign_latest(filings, pack)
        f0 = None
        if pack.get("balance_sheet_filing"):
            f0 = next((f for f in cand if f["acc"] == pack["balance_sheet_filing"]["acc"]), cand[0] if cand else None)
        facts, text = None, ""
        if f0 and pack["filer_type"] == "domestic":
            raw = sec.fetch(base_url(cik, f0["acc"]) + f0["doc"])
            if raw is None:
                pack.flag("FETCH_FAILED:main document", f0["acc"], True, "shares")
            else:
                facts, text = parse_ixbrl(raw), vis_text(raw)
        if f0 and pack["filer_type"] == "domestic":
            ents = scan_8ks(sec, pack, cik, filings)
            cover_date = build_shares(sec, pack, cik, f0, facts, text, ents)
            assemble_principal(pack, facts, f0['report'], f0)
            post_cover_events(sec, pack, cik, filings, cover_date, pack['filing']['period_end'], ents)
            build_quarter(sec, pack, cik, f0)
        else:
            pack["shares"] = {"common_total": na("foreign filer: no cover count read in this version"), "classes": []}
            pack.flag("STALE_SHARES", "foreign filer: no current share count established", True, "shares")
            scan_8ks(sec, pack, cik, filings)
    if "market" not in pack:
        get_price(pack, ticker)
    pack["audit"] = audit_pack(pack)
    pack["seconds"] = round(time.time() - t0, 1)
    return pack


def main(argv=None):
    ap = argparse.ArgumentParser(description="SEC fact-pack puller that cannot print a stale number")
    ap.add_argument("tickers", nargs="+")
    ap.add_argument("--json", dest="json_out")
    ap.add_argument("--md", dest="md_out")
    args = ap.parse_args(argv)
    sec = Sec()
    t0 = time.time()
    packs = []
    for tk in args.tickers:
        p = build(sec, tk.upper(), args)
        packs.append(p)
        print(render_block(p))
        print()
        sys.stdout.flush()
    print(f"[{len(packs)} ticker(s), {sec.n_requests} SEC requests, {time.time() - t0:.1f}s]")
    if args.json_out:
        json.dump(packs, open(args.json_out, "w"), indent=1, default=str)
    if args.md_out:
        with open(args.md_out, "w") as fh:
            for p in packs:
                fh.write("```\n" + render_block(p) + "\n```\n\n")
    return packs


if __name__ == "__main__":
    main()
