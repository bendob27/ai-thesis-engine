#!/usr/bin/env python3
"""Fail loudly when a document Ben reads contains jargon he has banned.

WHY THIS EXISTS (2026-08-01). Ben has corrected this engine's writing 17+ times
since 2026-07-07. Exactly one of those corrections had any mechanical
enforcement; the rest relied on a model remembering. Meanwhile eight of the nine
documents he actually reads have their prose emitted by Python, so a rule
written in a markdown file could never reach them at all.

research/watchlist-writing-standard.md already DEFINES five checks that "must
return nothing before work is handed back". Nothing ran them. This runs them.

The repo already knows this pattern works: approval_drift_check and
crowd_drift_check both compare two objects in code and fail loudly, and both
have caught real defects that prose warnings had already failed to prevent.

HOW IT WAS BYPASSED, AND WHAT CHANGED (2026-08-01, outside adversarial review).
Every check in here could be walked straight past, and three of the four ways
were accidents of a too-generous exemption:

  * ANY line containing "<!--" anywhere was exempt, so appending a comment to a
    sentence excused the sentence: `This line is armed <!-- note -->` passed.
    Now only a line that is ENTIRELY a machine comment is exempt.
  * ANY line containing the word "banned" was exempt. That word was meant to
    catch a sentence retiring a term; it excused any line that happened to use
    it. Removed.
  * ANY line matching "corrected <date>" was exempt, so `CORRECTED 2026-08-01:
    tier 3 armed` passed. A retraction is now only exempt where the retired
    wording is actually IN QUOTES on that line — quoting is what makes a
    retraction a retraction rather than a repetition.
  * The checks were CASE-SENSITIVE, so `RE-GATE ARMED` scored zero hits while
    `re-gate armed` was caught. All checks now ignore case.

A missing report is also a finding now. The old code filtered the target list
down to files that exist, so a report that stopped being written was silently
reported as clean — the failure mode this file was built to end.

Exit codes: 0 clean, 1 findings (jargon or a missing report). Prints the file,
line and term so the offending template can be found immediately.

Usage:
    python3 data/language_check.py                 # check every Ben-facing report
    python3 data/language_check.py --warn-only     # report but always exit 0
    python3 data/language_check.py path/to/file.md # check specific files
"""

from __future__ import annotations

import argparse
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
BOOK = os.path.join(SKILL, "book")

# The documents Ben actually reads. Internal state files (journal, ledger, the
# CSVs, triggers.csv) deliberately keep the shorthand and are NOT checked.
TARGETS = [
    "timing_gauge.md", "credit_temperature.md", "accounting_quality.md",
    "standby_alerts.md", "kc_value_door.md", "gas_strip.md",
    "trigger_alerts.md", "thesis_watch.md", "wake_report.md",
    "decision_grades.md", "valuation_scale.md",
    os.path.join("inbox", "eod_report_last.md"),
]

# The five checks from research/watchlist-writing-standard.md, plus the 07-30
# bare-score rule. Each is (label, regex, why it matters).
CHECKS = [
    ("a bare score with no explanation",
     r"\b\d+\s*(?:/|out of)\s*\d+\b",
     "say what it measures and which parts fired, never just the number"),
    ("the engine's own vocabulary",
     r"\b(?:re-gate|no-chase|thermometer|sleeve|clock-blend|door(?:s|-board)?|"
     r"wake(?:s|-up)?|tier(?:s|ed)?|armed|arming|standby|consumed|probe|recon)\b",
     "translate it into what the thing actually does"),
    ("a stage or hypothesis code",
     r"(?<![A-Za-z0-9])[SH]\d(?![A-Za-z0-9])",
     "say what the stage or hypothesis claims, in words"),
    ("an unnamed test label",
     r"\btest [A-D]\b|\bcheck \d+\b|\bleg \([ab]\)\b|\bpart \([ab]\)\b|\bMode-?\d\b",
     "name what the test measures"),
    ("an undefined abbreviation",
     r"\b(?:bps|DSO|SBC|NRR|TTM|EV/S|reverse-DCF|OAS|AMC|BMO|XBRL|GPV|DBNR)\b",
     "spell it out on first use"),
    ("a section reference",
     r"§\s*\d", "say what the rule does rather than citing where it lives"),
]

# EXEMPTION 1 — a line that is ENTIRELY a machine-readable state marker. Anchored
# on purpose: a comment appended to a sentence must not excuse the sentence.
MACHINE_COMMENT = re.compile(r"^\s*<!--.*-->\s*$")

# EXEMPTION 2 — a retraction. Only a line that SAYS it is retiring a wording, and
# only for the occurrences actually inside the quotation marks on that line. A
# retraction that does not quote the term it is retiring is indistinguishable from
# a line that simply uses the term, so it gets no exemption.
RETRACTION = re.compile(
    r"RETRACTED|no longer say|no longer written|the earlier|previously read|"
    r"used to (?:say|read)|was retired|retired \d{4}-\d{2}-\d{2}|"
    r"replaced the wording", re.I)

# Quoted spans: straight quotes, curly quotes, backticks.
QUOTED = re.compile(r"\"[^\"]*\"|'[^']*'|“[^”]*”|‘[^’]*’|`[^`]*`")


def _quoted_spans(line):
    return [m.span() for m in QUOTED.finditer(line)]


def check_file(path):
    """[(line_no, label, term, why)] — every occurrence a reader would trip on."""
    hits = []
    text = open(path, encoding="utf-8").read()   # caller has already established it exists
    for n, line in enumerate(text.splitlines(), 1):
        if MACHINE_COMMENT.match(line):
            continue
        spans = _quoted_spans(line) if RETRACTION.search(line) else []
        for label, pat, why in CHECKS:
            for m in re.finditer(pat, line, re.I):
                if any(a <= m.start() and m.end() <= b for a, b in spans):
                    continue   # properly quoted inside a retraction
                hits.append((n, label, m.group(0).strip(), why))
    return hits


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("files", nargs="*")
    ap.add_argument("--warn-only", action="store_true",
                    help="print findings but always exit 0 (for the scheduled chain)")
    a = ap.parse_args()

    paths = a.files or [os.path.join(BOOK, t) for t in TARGETS]

    # A REPORT THAT IS NOT THERE IS A FINDING, NOT A PASS (2026-08-01). This used
    # to filter the list down to files that exist, so a report whose script had
    # died was counted as clean — the check reported success on prose it never
    # read. A missing file is now named and counted.
    missing = [p for p in paths if not os.path.exists(p)]
    present = [p for p in paths if os.path.exists(p)]

    total, unreadable = 0, []
    for p in present:
        try:
            hits = check_file(p)
        except OSError as exc:
            unreadable.append((p, exc))
            continue
        if not hits:
            continue
        total += len(hits)
        print(f"\n{os.path.relpath(p, SKILL)} — {len(hits)} thing(s) Ben would not follow:")
        seen = set()
        for n, label, term, why in hits:
            key = (label, term.lower())
            if key in seen:
                continue
            seen.add(key)
            print(f"  line {n}: {label} — \"{term}\"")
            print(f"      fix: {why}")

    if missing:
        print(f"\n{len(missing)} report(s) Ben is meant to be able to read were not "
              f"there at all, so nothing in them was checked. Either the script that "
              f"writes each one failed, or it should come off the list in "
              f"data/language_check.py:")
        for p in missing:
            print(f"  MISSING: {os.path.relpath(p, SKILL)}")
    for p, exc in unreadable:
        print(f"  UNREADABLE: {os.path.relpath(p, SKILL)} — {exc}")

    if total == 0 and not missing and not unreadable:
        print(f"Language check clean across {len(present)} report(s) Ben reads.")
        return 0
    if total:
        print(f"\n{total} occurrence(s) across {len(present)} file(s). These are written by "
              "the scripts in data/, so the fix belongs in the template, not the output.")
    return 0 if a.warn_only else 1


if __name__ == "__main__":
    sys.exit(main())
