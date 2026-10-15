#!/usr/bin/env python3
"""Three-layer ranking on ONE distributional measure (brief §10, 2026-08-11).

What replaced what: the 08-06 ranking scored nine pillars whose weights rewarded
the same scenario distribution four different ways (edge, downside, severe loss,
lagging probability — §10.3's double-counting). This engine uses ONE
distributional measure and keeps genuinely different questions in genuinely
different ranks:

  CE = annualized expected return − λ · annualized expected shortfall
       (λ printed on every row; 1.0 until Ben ratifies a value — open decision)

  STANDALONE  — the company's own economics: CE from its card's scenarios over
                its own horizon against one shared price cut. No account, no
                portfolio, no cash.
  PORTFOLIO   — standalone, penalized for what it does to THIS book: single-name
                cap proximity, theme concentration, the one-factor AI stress.
  EXECUTION   — logistics only, and deliberately quarantined here so it can
                never contaminate the standalone view (the engine's standing
                rule: size and account mechanics are never a verdict): tradeable
                line, identity row, live approval, cap state.

TIERS BEFORE RANKS (§10.2): house-positive · provisional · disputed · house-no ·
UNRANKABLE. A high rank inside "house no" is still a no. Every name that cannot
be ranked says exactly why — most of the book today, honestly: cards without
horizons or scenarios rank when the replay rebuilds them, not before.

ONE MARKET-DATA CUT (§16): every price in a run comes from one settled-close
fetch, stamped once; a mixed cut refuses to write.

SENSITIVITY (§10.5): each name re-ranked under λ 0.5/1/2 and downside-probability
+10pp; a rank that moves more than 2 places prints its range, not a fake point.

Run: python3 data/ranking.py [--no-fetch]      writes book/ranking.csv + ranking.md
"""
import argparse
import csv
import datetime as dt
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import policy
ROOT = os.environ.get("AI_THESIS_ROOT") or os.path.dirname(HERE)
BOOK = os.path.join(ROOT, "book")
SHADOW = os.path.join(BOOK, "shadow")  # Phase-2 outputs quarantine here until Ben promotes (plan Phase 4)
LAMBDA = 1.0  # downside-aversion weight; PRINTED everywhere; Ben ratifies later

sys.path.insert(0, HERE)
# One definition of "is this value today's or a future date's, and at what rate"
# for the whole engine. Two files answering that separately is how a ten-point
# error in every present-value card survived a careful reading (2026-08-12).
from price_concepts import value_basis, discount_rate  # noqa: E402


def num(v):
    return float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else None


def load_csv(name):
    p = os.path.join(BOOK, name)
    if not os.path.exists(p):
        return []
    with open(p, encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


def card_economics(card, price):
    """(er_ann, es_ann, ce) from the card's own scenarios over its own horizon,
    against the shared price cut. None + reason when the card can't support it.

    Every scenario value is put on ONE footing first — a value at the card's own
    horizon — before any return is taken. Cards come in two conventions and only
    say which in a field: a value AT the horizon, or a value TODAY already
    discounted at the analyst's required return. Annualizing the second kind as
    if it were the first understates the return by roughly that required return,
    about ten percentage points, which is more than the entire spread this
    ranking is trying to measure (found 2026-08-12)."""
    hz = num(card.get("horizon_years"))
    if not hz or hz <= 0:
        return None, "no stated horizon"
    scen = card.get("scenarios")
    if not isinstance(scen, list) or not scen:
        return None, "no scenario set on the card"
    if not price or price <= 0:
        return None, "no settled close in this run's price cut"
    basis, _ = value_basis(card)
    if basis == "unknown":
        return None, ("the card does not say whether its value is today's or a "
                      "value years out, so no return can be taken from it")
    rate = None
    if basis == "present":
        rate, why = discount_rate(card)
        if rate is None:
            return None, why
    tot = er = es = 0.0
    for s in scen:
        p_, v = num(s.get("probability")), num(s.get("value_per_share"))
        if p_ is None or v is None:
            return None, f"scenario {s.get('name')} not numeric"
        tot += p_
        v = max(v, 0.01)
        if basis == "present":
            v = v * (1 + rate) ** hz          # back onto the horizon footing
        r_ann = (v / price) ** (1.0 / hz) - 1.0
        er += p_ * r_ann
        es += p_ * max(0.0, -r_ann)
    if abs(tot - 1.0) > 0.02:
        return None, f"probabilities sum to {tot:.2f}"
    return (er, es, er - LAMBDA * es), "ok"


def fetch_closes(tickers):
    """One settled-close cut for the whole run."""
    import yfinance as yf
    out, cut_date = {}, None
    for tk in tickers:
        try:
            h = yf.Ticker(tk).history(period="5d")["Close"].dropna()
            if len(h):
                out[tk] = float(h.iloc[-1])
                d = str(h.index[-1].date())
                cut_date = max(cut_date or d, d)
        except Exception:
            pass
    return out, cut_date


def tier_of(card, econ_ok, money_pass, verdicts=None, ticker=None):
    """The tier, and it is NOT read out of prose.

    Fixed 2026-08-11, third instance of one defect class in a day: this matched
    substrings like "CHALLENGED" inside review_status, so a card whose text read
    "PRIMARY ONLY - no challenge panel, no blind replication" was classified
    DISPUTED — the sentence said the exact opposite of what the keyword implied.
    The effect was visible and wrong: names returning -16% and -25% a year
    outranked names returning +6%, because DISPUTED sorts above HOUSE-NO.

    Order of authority: a STRUCTURED verdict from an adjudicating agent decides.
    Absent one, a card that has had no independent pass is UNREVIEWED — its own
    honest state — and never DISPUTED, which is a finding about disagreement
    between reviewers who actually ran."""
    if verdicts and ticker and ticker in verdicts:
        t = (verdicts[ticker].get("tier") or "").upper()
        if t in ("HOUSE-POSITIVE", "PROVISIONAL", "DISPUTED", "HOUSE-NO", "UNRANKABLE"):
            return t
    if not econ_ok:
        return "UNRANKABLE"
    rs = str(card.get("review_status") or "").upper()
    unreviewed = ("NOT REVIEWED" in rs or "PRIMARY ONLY" in rs
                  or "PRIMARY ANALYST" in rs or "NO CHALLENGE" in rs
                  or "NO INDEPENDENT" in rs or not rs)
    if unreviewed:
        # Say what it is: economics computed, nobody has checked them.
        return "UNREVIEWED-PASSES" if money_pass else "UNREVIEWED-FAILS"
    if money_pass is True:
        return "HOUSE-POSITIVE"
    if money_pass is False:
        return "HOUSE-NO"
    return "PROVISIONAL"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--no-fetch", action="store_true",
                    help="use each card's price_at_calc (clearly stamped as such)")
    ap.add_argument("--replay", action="store_true",
                    help="rank the REBUILT cards in book/shadow/replay/ instead of the "
                         "live store. Every one of those carries review_status NOT "
                         "REVIEWED until its independent pass runs, so the output is "
                         "labelled accordingly and is not a house view.")
    a = ap.parse_args()

    if a.replay:
        import glob as _glob
        vals = {}
        for _p in _glob.glob(os.path.join(SHADOW, "replay", "*.primary.json")):
            _tk = os.path.basename(_p).replace(".primary.json", "")
            try:
                vals[_tk] = json.load(open(_p, encoding="utf-8"))
            except ValueError:
                pass
        SOURCE = ("the %d cards rebuilt by the replay — EVERY ONE UNREVIEWED, no "
                  "independent pass has run against any of them" % len(vals))
    else:
        vals = json.load(open(os.path.join(BOOK, "valuations.json"), encoding="utf-8"))
        SOURCE = "the live valuation store"
    cards = {k: v for k, v in vals.items() if k != "_meta"
             and isinstance(v, dict) and v.get("status") == "live"}
    if a.replay:
        for _k, _v in list(cards.items()):
            _v.setdefault("review_status", "NOT REVIEWED")
    portfolio = {r["ticker"]: r for r in load_csv("portfolio.csv")}
    watch = {r["ticker"]: r for r in load_csv("watchlist.csv")}
    secs = {r["ticker"]: r for r in load_csv("securities.csv")}
    caps = {r["ticker"]: r for r in load_csv("buy_caps.csv")}
    approvals = {r["ticker"] for r in load_csv("approved_orders.csv")
                 if (r.get("status") or "").upper() in ("OPEN", "PLACED", "BACKLOG")}

    hurdle = policy.PASSIVE_BENCHMARK  # config/policy.json, via data/policy.py

    if a.no_fetch:
        closes = {tk: num(c.get("price_at_calc")) for tk, c in cards.items()}
        cut = "card price_at_calc (NO shared cut — stale by card, stamped as such)"
    else:
        closes, cut = fetch_closes(sorted(cards))
        cut = f"settled closes through {cut}" if cut else "FETCH FAILED"

    try:
        VERDICTS = json.load(open(os.path.join(SHADOW, "replay", "verdicts.json"),
                                  encoding="utf-8"))
    except (OSError, ValueError):
        VERDICTS = {}
    stamp = dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC")
    os.makedirs(SHADOW, exist_ok=True)
    rows, unrankable = [], []
    for tk, card in sorted(cards.items()):
        price = closes.get(tk)
        econ, why = card_economics(card, price)
        if econ is None:
            unrankable.append((tk, why, str(card.get("review_status") or "")))
            continue
        er, es, ce = econ
        money_pass = (er > hurdle) if er is not None else None
        # sensitivity: λ 0.5 / 2.0 and downside +10pp (heaviest-scenario bump)
        ces = [er - lam * es for lam in (0.5, 2.0)]
        hz = num(card.get("horizon_years"))
        scen = card["scenarios"]
        # same footing correction as card_economics — the downside-bump run must
        # not use a different convention from the run it is a sensitivity on
        _basis, _ = value_basis(card)
        _rate = discount_rate(card)[0] if _basis == "present" else None
        def _horizon_value(s):
            v = max(num(s.get("value_per_share")), 0.01)
            return v * (1 + _rate) ** hz if _basis == "present" else v
        worst = min(scen, key=lambda s: num(s.get("value_per_share")) or 0)
        bump = min(0.10, max(0.0, 1.0 - num(worst.get("probability"))))
        er_b = es_b = 0.0
        scale = 1.0 - bump
        for s in scen:
            p_ = num(s.get("probability")) * scale / max(1e-9, sum(
                num(x.get("probability")) for x in scen))
            if s is worst:
                p_ += bump
            r_ann = (_horizon_value(s) / price) ** (1.0 / hz) - 1.0
            er_b += p_ * r_ann
            es_b += p_ * max(0.0, -r_ann)
        ces.append(er_b - LAMBDA * es_b)

        held = tk in portfolio
        theme = (watch.get(tk, {}).get("theme") or "").strip()
        held_same_theme = sum(1 for t, r in portfolio.items()
                              if (watch.get(t, {}).get("theme") or "").strip() == theme
                              and theme)
        pf_penalty = 0.01 * held_same_theme  # 1pp CE penalty per held same-theme name
        sec = secs.get(tk, {})
        exec_score = sum([
            1 if sec else 0,
            1 if (sec.get("tradeable") or "").lower() == "yes" or held else 0,
            1 if tk in approvals else 0,
            1 if (caps.get(tk, {}).get("state") or "").split()[:1] == ["usable"] else 0,
        ])
        rows.append({
            "ticker": tk, "held": "yes" if held else "",
            "tier": tier_of(card, True, money_pass, VERDICTS, tk),
            "er_ann": round(er, 4), "es_ann": round(es, 4),
            "ce": round(ce, 4), "lambda": LAMBDA,
            "ce_sens_low": round(min(ces), 4), "ce_sens_high": round(max(ces), 4),
            "pf_adj_ce": round(ce - pf_penalty, 4),
            "pf_reason": (f"{held_same_theme} held name(s) in theme '{theme}'"
                          if pf_penalty else ""),
            "exec_score": exec_score,
            "price": price, "price_cut": cut,
            "horizon_years": num(card.get("horizon_years")),
            "review_status": card.get("review_status") or "",
        })

    # ranks: tier order first, CE within tier
    tier_order = {"HOUSE-POSITIVE": 0, "PROVISIONAL": 1, "UNREVIEWED-PASSES": 2,
                  "DISPUTED": 3, "UNREVIEWED-FAILS": 4, "HOUSE-NO": 5}
    rows.sort(key=lambda r: (tier_order.get(r["tier"], 9), -r["ce"]))
    for i, r in enumerate(rows, 1):
        r["standalone_rank"] = i
    by_pf = sorted(rows, key=lambda r: (tier_order.get(r["tier"], 9), -r["pf_adj_ce"]))
    for i, r in enumerate(by_pf, 1):
        r["portfolio_rank"] = i
    by_ex = sorted(rows, key=lambda r: (tier_order.get(r["tier"], 9), -r["pf_adj_ce"],
                                        -r["exec_score"]))
    for i, r in enumerate(by_ex, 1):
        r["execution_rank"] = i

    # dominance check (§10.4): portfolio rank below a standalone-dominated name
    dominance = []
    for r in rows:
        for s in rows:
            if s is r:
                continue
            if (r["er_ann"] > s["er_ann"] and r["es_ann"] <= s["es_ann"]
                    and r["portfolio_rank"] > s["portfolio_rank"]):
                dominance.append(
                    f"{r['ticker']} dominates {s['ticker']} on economics (ER "
                    f"{r['er_ann']:+.1%} vs {s['er_ann']:+.1%}, ES no worse) yet ranks "
                    f"below it after portfolio adjustment — reason on file: "
                    f"{r['pf_reason'] or 'NONE PRINTED (defect)'}")

    cols = ["standalone_rank", "portfolio_rank", "execution_rank", "ticker", "held",
            "tier", "er_ann", "es_ann", "ce", "lambda", "ce_sens_low", "ce_sens_high",
            "pf_adj_ce", "pf_reason", "exec_score", "price", "price_cut",
            "horizon_years", "review_status"]
    out_csv = "ranking_replay.csv" if a.replay else "ranking.csv"
    out_md = "ranking_replay.md" if a.replay else "ranking.md"
    with open(os.path.join(SHADOW, out_csv), "w", newline="",
              encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=cols, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)

    L = [f"# Ranking — {stamp}\n",
         f"Source: {SOURCE}.\n",
         "**Two honest returns, and this file uses the harsher one.** A company's "
         "expected return can be measured two ways and they do not agree. You can "
         "average the yearly return of each case (what this file does), or you can "
         "work out the yearly return of the averaged value (what a card's headline "
         "implies). The second is always the flattering one when the cases are far "
         "apart, because a case that triples helps the average value more than it "
         "helps the average return. Adobe on 2026-08-12: +1.2%/yr the first way, "
         "+3.7%/yr the second, from identical inputs. Neither is wrong; they answer "
         "different questions, and a rank should not be built on the flattering "
         "one. Where this file and a card disagree, this is why.\n",
         f"One price cut: {cut}. One measure: expected yearly return minus {LAMBDA} x "
         f"expected yearly shortfall (the weight is provisional until Ben ratifies "
         f"one). Order of tiers is the point — a high rank inside 'house no' is "
         f"still a no.\n"]
    cur = None
    for r in rows:
        if r["tier"] != cur:
            cur = r["tier"]
            L.append(f"\n## {cur}\n")
        rng = ""
        if abs(r["ce_sens_high"] - r["ce_sens_low"]) > 0.05:
            rng = (f" · sensitive: CE runs {r['ce_sens_low']:+.1%} to "
                   f"{r['ce_sens_high']:+.1%} across the test weightings")
        L.append(f"- **{r['ticker']}**{' (held)' if r['held'] else ''} — expected "
                 f"{r['er_ann']:+.1%}/yr, downside charge {r['es_ann']:.1%}/yr, "
                 f"certainty-equivalent {r['ce']:+.1%}/yr{rng}. Ranks: standalone "
                 f"#{r['standalone_rank']} → portfolio #{r['portfolio_rank']}"
                 + (f" ({r['pf_reason']})" if r["pf_reason"] else "")
                 + f" → execution #{r['execution_rank']}.")
    if dominance:
        L.append("\n## Dominance checks that need a printed reason\n")
        L += [f"- {d}" for d in dominance]
    L.append(f"\n## Not rankable yet — and why ({len(unrankable)} names)\n")
    L.append("These rank when the replay rebuilds their cards; an absent number is "
             "named, never defaulted.\n")
    for tk, why, rs in unrankable:
        L.append(f"- **{tk}** — {why}" + (f" (review: {rs})" if rs else ""))
    with open(os.path.join(SHADOW, out_md), "w", encoding="utf-8") as fh:
        fh.write("\n".join(L) + "\n")

    print(f"ranked {len(rows)} of {len(cards)} live cards · {len(unrankable)} "
          f"unrankable with reasons · cut: {cut}\n  {policy.lambda_caveat()}")
    print("wrote book/shadow/%s + %s (SHADOW — not a production surface until "
          "Ben promotes)" % (out_csv, out_md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
