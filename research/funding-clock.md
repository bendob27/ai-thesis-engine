# The Funding Clock — read 2026-10-12 11:09 UTC

A meter, not a hypothesis. Source: SEC XBRL companyconcept (audited filings).
Trailing-twelve-month capex vs operating cash flow, de-cumulated from filed
year-to-date facts. **Detection is automated; judgment is not.** This file never
amends the thesis — `/review` adjudicates, with Ben's sign-off.

| co | stage | capex TTM | OCF TTM | capex/OCF | +leases | capex YoY | OCF YoY | net ext. funding TTM | as of |
|---|---|---|---|---|---|---|---|---|---|
| CRWV | S2 EXTERNAL | $21B | $7B | 2.98x | — | +140% | +984% | $17B | 2026-06-30 |
| ORCL | S2 EXTERNAL | $76B | $47B | 1.61x | 1.75x | +176% | +118% | $47B | 2026-08-31 |
| AMZN | S2 EXTERNAL | $173B | $161B | 1.07x | 1.10x | +61% | +33% | $77B | 2026-06-30 |
| GOOGL | S1 SELF-FUNDED | $132B | $186B | 0.71x | 0.72x | +98% | +39% | n/a | 2026-06-30 |
| META | S1 SELF-FUNDED | $89B | $130B | 0.69x | 0.69x | +71% | +27% | $42B | 2026-06-30 |
| MSFT | S1 SELF-FUNDED | $116B | $183B | 0.63x | 0.77x | +80% | +34% | $2B | 2026-06-30 |
| NVDA | n/a (supplier — watched for S3 only) | $7B | $134B | 0.05x | — | +47% | +74% | $0B | 2026-07-26 |

## Signals

- `CROSSED` — AMZN (Amazon)
- `CROSSED` — ORCL (Oracle)
- `S3 DSO-RISING(vendor-credit tell)` — NVDA (Nvidia)
- `CROSSED` — CRWV (CoreWeave)
- `OCF-REINFLECTING(watch)` — CRWV (CoreWeave)

## Notes and caveats

- MSFT: OCF TTM cross-checks against the filer's own 12-month fact ($182.9B, 2026-06-30)
- MSFT: capex TTM cross-checks against the filer's own 12-month fact ($115.9B, 2026-06-30)
- GOOGL: issuance concepts absent — external funding unmeasured (n/a, not zero)
- AMZN: OCF TTM cross-checks against the filer's own 12-month fact ($161.4B, 2026-06-30)
- AMZN: capex TTM cross-checks against the filer's own 12-month fact ($173.0B, 2026-06-30)
- AMZN: net external funding $77B covers >=50% of the $12B capex-over-cash-flow gap
- META: repayment concept absent — external funding is GROSS, overstated
- ORCL: net external funding $47B covers >=50% of the $29B capex-over-cash-flow gap
- NVDA: DSO 76d vs 61d a year ago (Lucent/Nortel tell: supplier extending credit to customers)
- CRWV: net external funding $17B covers >=50% of the $14B capex-over-cash-flow gap
- NBIS: NOT MEASURED — foreign private issuer (IFRS/20-F); convert terms tracked by hand
- S4/S5/S6 are not computable from XBRL alone. S4/S5 use `--fulltext` as a READ-THIS prompt; S6 is the NBIS convert/ABS term check, done by hand.
- Cash-flow quarters are differenced from year-to-date facts. Run `--verbose` to print the four quarters behind each TTM before citing a number.
- **`capex` is cash purchases of property and equipment.** It EXCLUDES datacenter capacity taken via finance lease, which never touches investing cash flow. The `+leases` column adds `RightOfUseAssetObtainedInExchangeForFinanceLeaseLiability`; the STAGE is set on the unadjusted ratio so this ladder stays comparable to how Epoch and the street measure it. Where the two disagree about crossing, the meter says so.
- `net ext. funding` = debt proceeds − debt repayments + equity issuance. Gross proceeds are mostly refinancing and would badly overstate the number.

## Suggested ledger row (paste into research/evidence-ledger.md under H1 — requires a command's judgment, not this script's)

```
- 2026-10-12 · weakens · mag 3 · wt A · src:/research · Q4'26 · Funding Clock (XBRL, audited): capex>OCF at AMZN, ORCL, CRWV. · cite: book/funding_clock.csv 2026-10-12
```
