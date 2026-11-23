# STATE (researcher)

Owned by the Claude researcher: the engine created this file once and never changes it.
Read at the start of every cycle, updated at the end. The engine's own state is engine/STATE.md.

## Current beliefs (2026-11-23)
- 46 trials, 0 Gate 1 passes, holdout untouched. Momentum, trend and reversal fail on costs.
- Low vol is a noisy, mildly positive defensive tilt, not a demonstrated edge. E-000019 (AR 0.71, alpha t 1.4, DSR 0.09) is the top draw of about 17 volatility trials; it is likely RMW/CMA exposure plus survivorship.
- P-0001 holds utilities plus REITs/insurers (plus KO): a rates/sector bet. Its outperformance so far is beta to a soft tape.
- Gate 3 turnover/cost checks now use live data and pass (live turnover 1.89x/yr vs backtest 3.06x; cost drag 0.70% vs 1.08%). Based on one rebalance only.
- Research snapshot 42834a6c738dea38 (data to 2026-11-20).

## Open questions
- Is there any testable idea outside price-only signals? Quality and value need PIT fundamentals, which are not available free.
- Does P-0001 track sensibly against SPY and min-vol after 13 weeks?

## Next cycle
- P-0001 (marked 2026-11-20, unchanged at 2026-11-23 publish): 5/13 weeks, +4.42% since start, +5.4% vs SPY, +2.5% vs min-vol, DD -0.6%, kill ok. Judge nothing before 13 weeks.
- Next rebalance: signal about 2026-12-11, fill Mon 2026-12-14. Check turnover stays near 3x/yr once 2-3 rebalances exist.
- Expect the 2026-11-24 publish (~01:15 UTC) to add the Monday 2026-11-23 mark.
- If a nightly publish is skipped (normally ~01:15 UTC), notify the owner.
- Propose a card only when there is new economic logic. Do not add low-vol variants.
- Queue items only run when the owner starts a manual batch (max 20, provisional).

## Pending queue ids
None (R-0001 to R-0009 all ran).

## Dashboard refresh
2026-11-23 (second run): attempted after the push; the result is in the run's final message.
