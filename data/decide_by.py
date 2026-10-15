#!/usr/bin/env python3
"""Forced decision dates — nothing sits in "watching" forever, and nothing declined is forgotten.

Adopted 2026-08-04 (review #2, Ben's sign-off) after the decision record showed that
deferrals, not refusals, are what cost this book: names we said no to came out at a median
-0.90 points against their own industry, names we said "not yet" to came out at +3.45, and
81 of 120 gradable decisions were "not yet". Saying no is roughly free. Not deciding is not.

THE RULE THIS ENFORCES, in two halves:

  A. A name on the live shelf must carry BOTH a date by which we decide AND the named thing
     we are waiting for. When the date arrives there are exactly three outcomes -- BUY, KILL,
     or RE-UNDERWRITE. "Keep watching" is not one of them. It may become one only by naming a
     NEW dated thing to wait for, which resets the clock and is visible as having done so.

  B. A name we declined must carry a written condition that would bring it back. Ben,
     2026-08-04: "it would be good to keep a memory of the players that we've declined, so
     that at a future date we may actually invest in them again in case they become more
     relevant." A declined name with no way back is not a decision, it is a deletion.

This script decides nothing and buys nothing. It reports what is out of time and what has
been forgotten, and it exits non-zero when either is true.
"""
import csv, os, sys, datetime, collections

HERE = os.path.dirname(os.path.abspath(__file__))
BOOK = os.path.join(os.path.dirname(HERE), "book")
WATCHLIST = os.path.join(BOOK, "watchlist.csv")
TRIGGERS = os.path.join(BOOK, "triggers.csv")
KILLS = os.path.join(BOOK, "kills.csv")
PORTFOLIO = os.path.join(BOOK, "portfolio.csv")
OUT = os.path.join(BOOK, "decide_by.md")

LIVE_TIERS = ("ACTIVE", "QUEUE", "MONITOR")
DECLINED_TIERS = ("ARCHIVE",)
# A trigger of one of these types is a machine watching the name.
WATCHER_TYPES = {"WAKE", "EVENT", "DOOR", "BACKSTOP", "REUNDERWRITE", "EXTERNAL"}
# The uniform stamp applied to 110 rows on 2026-08-01. Real, but not a per-name judgement.
BLANKET = "default: 90 days from the verdict date"


def load():
    wl = list(csv.DictReader(open(WATCHLIST)))
    # Companies we already OWN are governed by their life-cycle card (book/lifecycle.md), which
    # carries a generated re-read date. They are not pending decisions and must not be flagged
    # here -- a page that cries wolf about eleven holdings is a page nobody reads.
    owned = {p["ticker"] for p in csv.DictReader(open(PORTFOLIO))}
    watchers = collections.defaultdict(set)
    for t in csv.DictReader(open(TRIGGERS)):
        if t["type"] in WATCHER_TYPES:
            watchers[t["ticker"]].add(t["type"])
    reopen = {k["ticker"]: k["reopen_on"].strip()
              for k in csv.DictReader(open(KILLS)) if k["reopen_on"].strip()}
    return wl, watchers, reopen, owned


def main():
    today = datetime.date.today()
    wl, watchers, reopen, owned = load()

    overdue, undated, no_waiting_for, forgotten = [], [], [], []
    cliff = collections.Counter()

    for r in wl:
        tier = (r.get("tier") or "").strip().upper()
        tkr = r["ticker"]
        if tkr in owned:
            continue  # governed by its life-cycle card, not by a decision date
        exp = (r.get("expiry_date") or "").strip()
        basis = (r.get("expiry_basis") or "").strip()
        waiting = (r.get("trigger_to_analyze") or "").strip()

        if tier in LIVE_TIERS:
            if not exp:
                undated.append(r)
            else:
                if exp < today.isoformat():
                    overdue.append((r, (today - datetime.date.fromisoformat(exp)).days))
                if basis.startswith(BLANKET):
                    cliff[exp] += 1
            if not waiting:
                no_waiting_for.append(r)

        elif tier in DECLINED_TIERS:
            if not watchers.get(tkr) and not reopen.get(tkr):
                forgotten.append(r)

    live = sum(1 for r in wl
               if (r.get("tier") or "").strip().upper() in LIVE_TIERS and r["ticker"] not in owned)
    declined = sum(1 for r in wl if (r.get("tier") or "").strip().upper() in DECLINED_TIERS)

    L = [f"# What has run out of time, and what we have forgotten — {today.isoformat()}", "",
         "Every company we are still considering has to carry two things: a date by which we "
         "decide, and the specific thing we are waiting for. When the date arrives there are "
         "three answers — buy it, kill it, or read it again from scratch. **\"Keep watching\" "
         "is not an answer.** It becomes one only by naming a new dated thing to wait for, "
         "which restarts the clock and shows on this page as having done so.", "",
         "Every company we declined has to carry a written condition that would bring it back. "
         "A company we said no to and cannot ever reconsider was not declined, it was deleted.",
         "", "This page decides nothing and buys nothing.", "",
         f"**{live} companies are still being considered. {declined} have been set aside.** "
         f"The {len(owned)} companies we already own are not on this page — each has its own "
         "card in book/lifecycle.md with a re-read date generated from the earnings calendar.", ""]

    def block(title, rows, fmt, why):
        L.append(f"## {title}")
        L.append("")
        if not rows:
            L.append("None.")
            L.append("")
            return
        L.append(why)
        L.append("")
        for x in rows:
            L.append(fmt(x))
        L.append("")

    block(f"{len(overdue)} have passed their decision date",
          sorted(overdue, key=lambda p: -p[1]),
          lambda p: f"- **{p[0]['name'] or p[0]['ticker']} ({p[0]['ticker']})** — due "
                    f"{p[0]['expiry_date']}, **{p[1]} days ago**. Buy, kill, or read it again.",
          "These need one of the three answers now.")

    block(f"{len(undated)} are being considered with no decision date at all",
          undated,
          lambda r: f"- **{r['name'] or r['ticker']} ({r['ticker']})** — on the "
                    f"{r['tier'].lower()} shelf, no date. Nothing will ever force this one.",
          "A name with no date can sit here forever, which is the thing this rule exists to stop.")

    block(f"{len(no_waiting_for)} do not say what they are waiting FOR",
          no_waiting_for,
          lambda r: f"- **{r['name'] or r['ticker']} ({r['ticker']})** — {r['tier'].lower()} "
                    "shelf, no stated thing being waited for.",
          "Waiting is legitimate when it names a disclosure, a filing, a ruling or a price test. "
          "Waiting for nothing in particular is indecision with a date stapled to it.")

    block(f"{len(forgotten)} set-aside companies have NO way back",
          forgotten,
          lambda r: f"- **{r['name'] or r['ticker']} ({r['ticker']})** — set aside, and nothing "
                    "is watching it and no written condition would revive it.",
          "Each of these was passed over for a reason that may stop being true. Nothing would "
          "tell us if it did.")

    if cliff:
        L.append("## A note on dates that were stamped in bulk")
        L.append("")
        L.append("On 1 August 2026 a uniform 90-day date was applied to every row that had no "
                 "better one. Those are real dates, but none of them is a judgement about that "
                 "particular company, and they all fall due together:")
        L.append("")
        for d, n in sorted(cliff.items()):
            L.append(f"- **{n} companies all come due on {d}.**")
        L.append("")
        L.append("Deciding that many names in one day is not a forcing function, it is a queue. "
                 "Each should get a real date — anchored to its own next disclosure — the next "
                 "time anyone touches the row. They are not being re-stamped in bulk a second "
                 "time, because that is the same mistake twice.")
        L.append("")

    open(OUT, "w").write("\n".join(L) + "\n")
    work = len(overdue) + len(undated) + len(forgotten)
    print(f"wrote {OUT} — {len(overdue)} overdue, {len(undated)} undated, "
          f"{len(no_waiting_for)} with no stated wait, {len(forgotten)} set aside with no way back")
    return 1 if work else 0


if __name__ == "__main__":
    sys.exit(main())
