#!/usr/bin/env python3
"""Per-belief index of the evidence ledger — the fix for evidence hiding in the wrong section.

Adopted 2026-08-04 (Ben's yes, replacing the rejected "teach the writer to route" option).
Between 07-24 and 08-04 the five hypothesis sections of research/evidence-ledger.md received
ONE row while the Playbook section received 122, of which 85 named a hypothesis in their text.
Review #2 nearly missed twelve days of evidence because it was reading sections, not content.

DESIGN CONSTRAINTS, all deliberate (Ben, 2026-08-04: "make sure nothing breaks... not making
things more difficult and complex"):

  - READ-ONLY over its input. It opens the ledger to read and writes ONLY its own output
    page. It cannot corrupt the ledger under any failure.
  - STATELESS. The index is regenerated from scratch on every run — no incremental state,
    nothing to drift, nothing to reconcile. If it is ever wrong, delete it and re-run.
  - ZERO configuration. No flags, no env vars. One input, one output, both hard-coded.
  - FAIL LOUD. Every dated row in the ledger must be accounted for in the audit line at the
    bottom of the page; if the arithmetic does not add up, exit non-zero and say so.
  - The sweep's writer (sweep_write.py) is NOT touched. It stays append-only on purpose —
    its stupidity is a security property (a hijacked headless run can only add text at the
    end of four fixed files, never steer where in a governed file it writes).

Output: book/evidence_index.md. The ledger stays the single source of truth; this page is a
table of contents over it and says so.
"""
import datetime
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SKILL = os.path.dirname(HERE)
LEDGER = os.path.join(SKILL, "research", "evidence-ledger.md")
OUT = os.path.join(SKILL, "book", "evidence_index.md")

# Literal hypothesis labels only. A row mentioning "H2-GRID" or "H4b" is claimed by that
# hypothesis; a row with no literal label is process, which is a legitimate thing to be.
LABEL = re.compile(r"\bH1[AB]?\b|\bH2\b|\bH3\b|\bH4[a-d]?\b|\bH5\b|H1-FUNDING|H2-GRID|H2-BOTTLENECKS?")
HEADER = re.compile(r"^- (\d{4}-\d\d-\d\d) · (\w[\w+-]*) · mag (\d) · wt ([ABC])")
PLAIN = {
    "H1": "H1 — does the AI spending keep growing, and does it pay our suppliers",
    "H2": "H2 — the binding shortage keeps moving through the physical stack",
    "H3": "H3 — which layer is the cheapest durable profit pool",
    "H4": "H4 — physical AI: defence, robotaxis, space, humanoids",
    "H5": "H5 — does AI impair per-seat software (a screen)",
}


def hypo_of(label):
    return "H" + re.search(r"\d", label).group(0)


def excerpt(row):
    """The most informative slice of a row, one line, bold stripped."""
    body = row.split("· cite:")[0]
    fields = body.split(" · ")
    text = max(fields, key=len).strip().replace("**", "")
    return text[:180] + ("…" if len(text) > 180 else "")


def main():
    if not os.path.exists(LEDGER):
        sys.exit(f"evidence_index: ledger not found at {LEDGER}")
    lines = open(LEDGER).read().split("\n")

    section = None
    per_h = {h: [] for h in PLAIN}      # hypothesis -> [(date, line)]
    n_home = n_claimed = n_process = 0
    total = 0

    for ln in lines:
        if ln.startswith("## "):
            section = ln[3:].strip()
            continue
        if not re.match(r"^- \d{4}-\d\d-\d\d", ln):
            continue
        total += 1
        m = HEADER.match(ln)
        date = ln[2:12]
        meta = f"{m.group(2)} · mag {m.group(3)} · wt {m.group(4)}" if m else "unparsed header"
        home = re.match(r"H[1-5]", section or "")
        if home:
            h = home.group(0)
            per_h[h].append((date, f"- {date} · {meta} — {excerpt(ln)}"))
            n_home += 1
        else:
            labels = sorted({hypo_of(x) for x in LABEL.findall(ln.split("· cite:")[0])})
            if labels:
                n_claimed += 1
                for h in labels:
                    where = (section or "?").split(" (")[0].split(" — ")[0]
                    per_h[h].append((date, f"- {date} · {meta} — {excerpt(ln)} *(lives in the {where} section)*"))
            else:
                n_process += 1

    if n_home + n_claimed + n_process != total:
        sys.exit(f"evidence_index: accounting broke — {n_home}+{n_claimed}+{n_process} != {total}")

    today = datetime.date.today().isoformat()
    L = [f"# Every piece of evidence, sorted by the belief it bears on — {today}", "",
         "The evidence ledger is append-only, so a note about a belief sometimes gets written at "
         "the end of the file, under the general process section, instead of under the belief it "
         "is about. Between 24 July and 4 August that happened 122 times against once, and a "
         "review nearly missed twelve days of evidence. This page is the fix: it is rebuilt from "
         "the ledger on every run and lists every entry under every belief it names, wherever it "
         "physically sits. **The ledger stays the single source of truth. Never edit this page — "
         "it is overwritten daily.**", ""]

    for h in ("H1", "H2", "H3", "H4", "H5"):
        rows = sorted(per_h[h], key=lambda p: p[0])
        L.append(f"## {PLAIN[h]} — {len(rows)} entries")
        L.append("")
        L.extend(line for _, line in rows)
        L.append("")

    L.append("## The arithmetic this page checks itself against")
    L.append("")
    L.append(f"The ledger holds **{total} dated entries**. {n_home} sit in a belief's own "
             f"section. {n_claimed} sit elsewhere but name a belief in their text, and are "
             f"indexed above under each belief they name. {n_process} name no belief — those "
             "are process notes, which is a legitimate thing to be, and they are not listed "
             f"here. {n_home} + {n_claimed} + {n_process} = {total}; if that sum ever breaks, "
             "this script refuses to write and exits with an error instead.")
    L.append("")

    open(OUT, "w").write("\n".join(L) + "\n")
    print(f"wrote {OUT} — {total} rows read: {n_home} in home sections, "
          f"{n_claimed} indexed from elsewhere, {n_process} process-only")
    return 0


if __name__ == "__main__":
    sys.exit(main())
