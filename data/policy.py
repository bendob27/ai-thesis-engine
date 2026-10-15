#!/usr/bin/env python3
"""The approved return policy — one source, read by everything (2026-08-19).

Ben set the targets on 2026-08-13 ("Yes approved") against this proposal, verbatim:
"Set 12% a year for everything, with two exceptions: 15% for anything unprofitable
or pre-scale, 10% for the true compounders you intend to hold 5+ years."

They were written into risk/profile.md and then read by nothing. `ranking.py`
hardcoded the 6.5% index bar, `buy_cap.py` carried its own copy, and
`price_concepts.py` still said the targets were "UNSET until he ratifies them" and
showed 10/15/20% as illustration — six days after he ratified 10/12/15. This module
is the one place the numbers live; the values themselves are data
(config/policy.json), not code.

TWO DIFFERENT QUESTIONS, AND THEY MUST NEVER BE PRESENTED AS ONE NUMBER
(this is what the brief means by naming them separately):

  1. IS IT WORTH BUYING?  A BAR — yes or no.
     Compare a name's expected annual return against ITS OWN required return
     (10%, 12% or 15% by what kind of name it is). Nothing else enters. This is
     `required_return()` and `clears_bar()`.

  2. IF SEVERAL CLEAR THE BAR, WHICH FIRST?  An ORDERING — never a yes or no.
     Rank by the certainty-equivalent return: expected return MINUS a penalty for
     how bad the bad cases are. A name can rank last and still be worth buying; a
     name can rank first and still fail its bar. The penalty weight is assumed at
     1.0 and is NOT approved — it cannot be derived until Ben sets the maximum
     acceptable chance of permanent loss, so every output that uses it prints it.

Using the ranking score as a bar, or the bar as a ranking, is the error this
separation exists to prevent. --selftest fails on either.

WHICH BAR A NAME GETS:
  10% established quality — its strategy book is `compounder`. That book is defined
      as names underwritten on growth DURATION and intended as long holds, which is
      the same set Ben described as "the true compounders you intend to hold 5+
      years". A large fall in one of these is a reason to buy more.
  15% speculative — unprofitable on its own latest filed annual accounts (net income
      or operating income at or below zero), or pre-scale (no revenue reported).
      Read from book/fin/<TICKER>.json, which is built from filings.
  12% default — everything else, and every name whose accounts we do not hold. The
      fallback is NAMED in the output, never silent: "no financial card on file" is
      a different statement from "profitable".

Run: python3 data/policy.py                which bar each name gets, and why
     python3 data/policy.py --selftest
     python3 data/policy.py --lint          find rates hardcoded outside this file
"""
import argparse
import csv
import glob
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.environ.get("AI_THESIS_ROOT") or os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "book")
POLICY_FILE = os.path.join(ROOT, "config", "policy.json")

_REQUIRED_RATES = ("passive_benchmark_return", "default_target",
                   "established_quality_target", "speculative_target")


def _load():
    with open(POLICY_FILE, encoding="utf-8") as fh:
        p = json.load(fh)
    for k in _REQUIRED_RATES:
        v = p.get(k)
        if not isinstance(v, (int, float)) or not 0 < v < 1:
            raise SystemExit(f"config/policy.json: {k} is {v!r} — every rate must be "
                             f"a fraction between 0 and 1 (0.12, not 12).")
    if not (p["passive_benchmark_return"] < p["established_quality_target"]
            <= p["default_target"] <= p["speculative_target"]):
        raise SystemExit(
            "config/policy.json: the bars are out of order. The index bar must be "
            "the lowest, then established quality, then the default, then "
            "speculative — otherwise a safer name is being asked to earn more than "
            "a riskier one.")
    return p


POLICY = _load()

PASSIVE_BENCHMARK = POLICY["passive_benchmark_return"]
DEFAULT_TARGET = POLICY["default_target"]
ESTABLISHED_QUALITY_TARGET = POLICY["established_quality_target"]
SPECULATIVE_TARGET = POLICY["speculative_target"]
DOWNSIDE_AVERSION_LAMBDA = POLICY.get("downside_aversion_lambda", 1.0)
LAMBDA_IS_APPROVED = POLICY.get("maximum_acceptable_permanent_loss_probability") is not None
APPROVED_ON = POLICY["approved_on"]


def lambda_caveat():
    """The sentence every ranking output must carry until Ben sets the input."""
    if LAMBDA_IS_APPROVED:
        return f"downside penalty weight {DOWNSIDE_AVERSION_LAMBDA:g} (derived from policy)"
    return (f"downside penalty weight {DOWNSIDE_AVERSION_LAMBDA:g} — ASSUMED, not "
            f"approved; it can only be derived once the maximum acceptable chance of "
            f"permanent loss is set")


def _profitability(ticker):
    """(state, evidence) from the company's own filed accounts. Never guessed."""
    p = os.path.join(BOOK, "fin", f"{ticker}.json")
    if not os.path.exists(p):
        return "unknown", "no financial card on file"
    try:
        with open(p, encoding="utf-8") as fh:
            d = json.load(fh)
    except (OSError, ValueError):
        return "unknown", "financial card unreadable"
    annual = d.get("annual") or []
    if not isinstance(annual, list) or not annual:
        return "unknown", "financial card has no annual periods"
    latest = annual[0]
    for a in annual:
        if (a.get("end") or "") > (latest.get("end") or ""):
            latest = a
    end = latest.get("end") or "undated"
    rev, ni, oi = latest.get("revenue"), latest.get("net_income"), latest.get("operating_income")
    if rev in (None, 0):
        return "pre-scale", f"no revenue reported for the year ending {end}"
    nums = [x for x in (ni, oi) if isinstance(x, (int, float))]
    if not nums:
        return "unknown", f"no profit line in the accounts for the year ending {end}"
    if min(nums) <= 0:
        which = "net income" if isinstance(ni, (int, float)) and ni <= 0 else "operating income"
        return "unprofitable", f"{which} at or below zero for the year ending {end}"
    return "profitable", f"profitable on the accounts for the year ending {end}"


class Target:
    __slots__ = ("rate", "name", "why")

    def __init__(self, rate, name, why):
        self.rate, self.name, self.why = rate, name, why

    def __repr__(self):
        return f"Target({self.rate:.0%} {self.name}: {self.why})"

    def __eq__(self, o):
        return isinstance(o, Target) and (self.rate, self.name) == (o.rate, o.name)


def required_return(ticker=None, strategy_book=None):
    """The BAR this name must clear to be worth buying. Question 1, never question 2."""
    book = (strategy_book or "").strip().lower()
    if book == "compounder":
        return Target(ESTABLISHED_QUALITY_TARGET, "established quality",
                      "filed in the compounder book — bought for growth duration and "
                      "intended as a long hold, which is the lower bar Ben set for "
                      "exactly that kind of name")
    state, evidence = _profitability(ticker) if ticker else ("unknown", "no ticker given")
    if state in ("unprofitable", "pre-scale"):
        return Target(SPECULATIVE_TARGET, "speculative",
                      f"{state} on its own filings — {evidence}")
    if state == "unknown":
        return Target(DEFAULT_TARGET, "default",
                      f"the default bar, and the reason is named rather than assumed: "
                      f"{evidence}, so neither exception could be established")
    return Target(DEFAULT_TARGET, "default", f"the default bar — {evidence}")


def clears_bar(expected_annual_return, ticker=None, strategy_book=None):
    """Question 1. Returns (bool, Target). Never takes a ranking score."""
    t = required_return(ticker, strategy_book)
    if expected_annual_return is None:
        return None, t
    return expected_annual_return > t.rate, t


def certainty_equivalent(expected_annual_return, expected_shortfall_annual,
                         lam=None):
    """Question 2 — an ORDERING. Never compare this with a target."""
    if expected_annual_return is None or expected_shortfall_annual is None:
        return None
    lam = DOWNSIDE_AVERSION_LAMBDA if lam is None else lam
    return expected_annual_return - lam * abs(expected_shortfall_annual)


# ---------------------------------------------------------------- reporting --
def _rows():
    out = []
    for f in ("portfolio.csv", "watchlist.csv"):
        p = os.path.join(BOOK, f)
        if os.path.exists(p):
            with open(p, encoding="utf-8") as fh:
                for r in csv.DictReader(fh):
                    out.append((f, r.get("ticker"), r.get("strategy_book")))
    return out


def report():
    seen, counts = {}, {}
    for _, tk, bk in _rows():
        if not tk or tk in seen:
            continue
        t = required_return(tk, bk)
        seen[tk] = t
        counts[t.name] = counts.get(t.name, 0) + 1
    print(f"APPROVED RETURN POLICY (set {APPROVED_ON} by {POLICY['approved_by']}: "
          f"\"{POLICY['approval_quote']}\")\n")
    print(f"  index bar (beat a tracker fund) {PASSIVE_BENCHMARK:.1%}")
    print(f"  established quality             {ESTABLISHED_QUALITY_TARGET:.0%}")
    print(f"  default                         {DEFAULT_TARGET:.0%}")
    print(f"  speculative                     {SPECULATIVE_TARGET:.0%}")
    print(f"\n  ranking penalty: {lambda_caveat()}")
    print(f"\nWhich bar each of {len(seen)} names gets:")
    for k, v in sorted(counts.items(), key=lambda x: -x[1]):
        print(f"  {v:4d}  {k}")
    spec = sorted(t for t, v in seen.items() if v.name == "speculative")
    if spec:
        print(f"\n  the {len(spec)} on the 15% bar, and why:")
        for t in spec[:40]:
            print(f"    {t:<12} {seen[t].why}")
    return 0


def lint():
    """Find return rates hardcoded outside this module — the defect that let
    ranking.py and buy_cap.py drift apart from the approved policy."""
    # Only flag a rate where it is being USED AS a return bar. Sleep intervals,
    # test fixtures and unrelated thresholds are not policy, and a lint that
    # cries wolf gets switched off.
    rate = r"(?<![\w.])(?:0\.(?:065|10|12|15)|6\.5|12\.0?|15\.0?|10\.0?)(?![\d])"
    ctx = r"(hurdle|target|benchmark|index_return|required_return|bar\b|sensitivity)"
    pat = re.compile(rf"{ctx}[^=<>!]*[=<>]+[^=]*{rate}|{rate}[^=]*#[^#]*{ctx}",
                     re.IGNORECASE)
    hits = []
    for p in sorted(glob.glob(os.path.join(HERE, "*.py"))):
        if os.path.basename(p) in ("policy.py",):
            continue
        for i, line in enumerate(open(p, encoding="utf-8"), 1):
            t = line.strip()
            if t.startswith("#") or "policy." in t or "check(" in t:
                continue
            if pat.search(line):
                hits.append((os.path.basename(p), i, t[:110]))
    print(f"HARDCODED RATE LINT — {len(hits)} line(s) outside data/policy.py")
    for f, i, l in hits:
        print(f"  {f}:{i}  {l}")
    if not hits:
        print("  clean — every rate comes from config/policy.json")
    return 1 if hits else 0


def selftest():
    fails = []

    def check(name, got, want):
        ok = got == want
        if not ok:
            fails.append(f"{name}: got {got!r}, wanted {want!r}")
        print(f"  {'ok  ' if ok else 'FAIL'} {name}: {got!r}")

    print("1. the approved numbers are the ones in use")
    check("index bar", PASSIVE_BENCHMARK, 0.065)
    check("established quality", ESTABLISHED_QUALITY_TARGET, 0.10)
    check("default", DEFAULT_TARGET, 0.12)
    check("speculative", SPECULATIVE_TARGET, 0.15)
    check("20% is not a target", 0.20 in (ESTABLISHED_QUALITY_TARGET, DEFAULT_TARGET,
                                          SPECULATIVE_TARGET), False)

    print("2. a compounder gets the lower bar, and it is a real difference")
    a = required_return("ADBE", "compounder")
    check("compounder bar", a.rate, ESTABLISHED_QUALITY_TARGET)
    check("compounder bar is below the default", a.rate < DEFAULT_TARGET, True)

    print("3. the bar and the ranking are never the same number")
    ce = certainty_equivalent(0.14, 0.06)
    passes, t = clears_bar(0.14, "SOMETHING", "")
    check("expected return clears the 12% bar", passes, True)
    check("its ranking score is lower than its expected return", ce < 0.14, True)
    check("the ranking score would FAIL the bar it just passed", ce > t.rate, False)
    # ^ the whole point: judging on the ranking score would reject a name that
    #   passes on the measure the policy actually names.

    print("4. a higher bar can never turn a fail into a pass")
    lo, _ = clears_bar(0.11, "X", "compounder")     # 10% bar
    hi, _ = clears_bar(0.11, "X", "")               # 12% bar
    check("clears the 10% bar", lo, True)
    check("fails the 12% bar", hi, False)
    check("monotonic", not (hi and not lo), True)

    print("5. every caller gets the SAME bar for the same name")
    check("stable across calls",
          required_return("ADBE", "compounder") == required_return("ADBE", "compounder"),
          True)

    print("6. an unknown name falls back to the default with the reason NAMED")
    u = required_return("ZZZZ-NOT-A-TICKER", "")
    check("falls back to the default", u.rate, DEFAULT_TARGET)
    check("says why", "no financial card on file" in u.why, True)

    print("7. the bars stay in order")
    check("order", PASSIVE_BENCHMARK < ESTABLISHED_QUALITY_TARGET <= DEFAULT_TARGET
          <= SPECULATIVE_TARGET, True)

    print("8. the unapproved penalty weight announces itself")
    check("caveat present", "ASSUMED" in lambda_caveat(), True)

    print(f"\n{'SELFTEST PASSED' if not fails else 'SELFTEST FAILED'} — {len(fails)} failure(s)")
    for f in fails:
        print("  -", f)
    return 1 if fails else 0


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--lint", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if a.lint:
        return lint()
    return report()


if __name__ == "__main__":
    sys.exit(main())
