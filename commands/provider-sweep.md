# /provider-sweep — monthly research-provider diff

Re-read the 24 research shops in the field guide and report **what changed**, not what they think.
Runs monthly on the 15th as a cloud routine; this command runs the same logic locally on demand.

**The governing rule: a monthly report that restates last month is noise.** Ben's standing
instruction on recurring alerts — they must carry news, not echo. If nothing moved, the honest
output is a short "nothing moved, here is the one thing that came closest" — never a re-dump.

## Inputs

| File | Role |
|---|---|
| `research/provider-baseline.md` | What each shop thought last time. The thing you diff against. |
| `book/provider_tracker.csv` | The numeric series, append-only. One row per metric per reading. |
| `notes/2026-07-28-research-provider-sweep.md` | Month 0 in full, if you need the reasoning behind a baseline position. |

## Cost discipline — do not re-scrape everything

Most of these shops publish on slow clocks. Re-reading all 24 monthly wastes the shared spend
limit for nothing. Tier them:

**TIER A — check every month.** They update monthly or faster, or are irregular-but-high-value.
- Howard Marks memos (`oaktreecapital.com/insights/memos`) — just read the index and note dates. A new memo is the single highest-value event in this whole sweep.
- GMO 7-year asset-class forecast — **updates monthly**, pure number.
- Research Affiliates 10-year expected returns — updates monthly; the site is login-walled, so take the best available secondary and mark it SECONDARY.
- Apollo Daily Spark (`apolloacademy.com`) — grab any AI-capex, hyperscaler-credit or private-credit charts.
- Man Group Views from the Floor — weekly; look for anything on the layer/wave thesis.

**TIER B — check only in the month it publishes.** Skip otherwise and say so.
| Month | Due |
|---|---|
| Jan | AQR Capital Market Assumptions · World Bank GEP · IMF WEO update |
| Feb | NY Fed household debt (Q4) |
| Mar | BIS Quarterly Review |
| Apr | **Stanford AI Index** · IMF WEO + GFSR · Fed Financial Stability Report |
| May | ECB Financial Stability Review · NY Fed household debt (Q1) |
| Jun | **BIS Annual Report** · OECD Outlook · PIMCO Secular Outlook · KKR/BlackRock/Vanguard/PGIM mid-years |
| Jul | **Bank of England FSR** · IMF WEO update |
| Aug | NY Fed household debt (Q2) · NBIM half-year |
| Sep | BIS Quarterly Review |
| Oct | IMF WEO + GFSR |
| Nov | Fed FSR · ECB FSR · NY Fed household debt (Q3) |
| Dec | OECD Outlook · Bank of England FSR · BIS Quarterly Review · Brookfield/KKR outlooks |

**TIER C — the tracked numbers, every month regardless.** These are the actual signal. Re-read
whatever has a fresh value, append a row to the tracker for each, and leave the rest alone. A
metric with no new reading is not a gap — record nothing and move on.

US labour productivity is free and mechanical — pull it from FRED rather than hunting a report:
`curl -s "https://fred.stlouisfed.org/graph/fredgraph.csv?id=OPHNFB"` (output per hour, nonfarm
business; the quarterly annualised series is `PRS85006092`).

## Steps

1. **Read the baseline and the tracker.** Note the last reading date for each metric.
2. **Tier A always; Tier B only if this month is its month.** Check the current month against the
   table above and state explicitly which Tier B sources you skipped and why.
3. **For each source checked, ask only:** is there a publication newer than the baseline date? If
   no — record nothing. If yes — read it at the publisher and extract (a) any tracked number, and
   (b) whether the **wording escalated or softened** on that shop's baseline position. For central
   banks the wording move matters more than the level; they warn every cycle.
4. **Append tracker rows** for every fresh number: `reading_date,metric,value,unit,source,as_of,grade,cite`.
   Grade PRIMARY only if read at the publisher. Never invent a metric name — reuse the existing
   ones so the series stays continuous.
5. **Update `provider-baseline.md`** only where a position genuinely moved, and append the move to
   its change log with old value, new value and the quote.
6. **Check the five convergences and seven disagreements.** For each: intact, weakened, or broken?
   A convergence breaking is the highest-value output this sweep can produce — say so loudly.
7. **Write the report** to `notes/YYYY-MM-DD-provider-sweep.md` and an inbox flag at
   `book/inbox/YYYY-MM-DD-provider-sweep-flags.md`.
8. **Ledger rows** for anything that bears on a hypothesis, appended to `research/evidence-ledger.md`
   in the existing format. Observations only — the sweep never touches `thesis.md` or conviction scores.
9. **Commit explicit paths only.** `git add -A` is banned in this repo.

## Report shape

Lead with the answer to "did anything change". Then, in order:

1. **What moved** — one table: shop, what it said before, what it says now, the quote. Empty is a valid table.
2. **The numbers** — tracker deltas since last reading, with both values and the dates.
3. **Convergences** — the five, each marked intact / weakened / broken.
4. **Disagreements** — the seven, each marked unchanged / narrowed / resolved.
5. **New publications** worth Ben's own time, ranked. A new Marks memo always ranks first.
6. **What it means for the book** — only if something actually bears on a position or a hypothesis.

Write for Ben: plain English, short sentences, no engine jargon. Every company and shop gets its
name plus a short plain descriptor on first mention. Tables for anything comparable. If nothing
moved, say that in the first line and keep the whole thing under a page.

## Rendering the PDF (local only)

The cloud routine cannot render PDFs. To produce one from a monthly report:

```
pandoc notes/<file>.md -f 'gfm-tex_math_dollars' -t html5 -s --embed-resources -o /tmp/sweep.html
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu \
  --no-pdf-header-footer --print-to-pdf=/tmp/sweep.pdf /tmp/sweep.html
```

`-f gfm-tex_math_dollars` is not optional — plain `gfm` reads `$1.4tn` as LaTeX maths and mangles
every dollar figure. Verify with `pdftotext /tmp/sweep.pdf - | grep -c '\*\*'` returning 0.
