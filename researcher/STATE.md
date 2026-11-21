# STATE (researcher)

Owned by the Claude researcher: the engine created this file once and never changes it.
Read at the start of every cycle, updated at the end. The engine's own state is engine/STATE.md.

## Current beliefs (2026-11-21)
- 46 trials, 0 Gate 1 passes, holdout untouched. Momentum, trend and reversal fail on costs.
- Low vol is a noisy, mildly positive defensive tilt, not a demonstrated edge. E-000019 (AR 0.71, alpha t 1.4, DSR 0.09) is the top draw of about 17 volatility trials; it is likely RMW/CMA exposure plus survivorship.
- P-0001 holds utilities plus REITs/insurers (plus KO): a rates/sector bet. Its outperformance so far is beta to a soft tape.
- The first P-0001 rebalance (2026-11-16) had 18.1% turnover and about $5.6 in costs, which is in line with the backtest's 3.06x a year.
- Research snapshot rebuilt 2026-11-21: 42834a6c738dea38 (data to 2026-11-20).

## Open questions
- Is there any testable idea outside price-only signals? Quality and value need PIT fundamentals, which are not available free.
- Does P-0001 track sensibly against SPY and min-vol after 13 weeks?

## Next cycle
- The nightly job recovered on 2026-11-21 after skipping 2026-11-20. If another night is skipped, notify the owner.
- After the Sunday 2026-11-22 publish: weeks_tracked should be 5, and Gate 3 turnover/cost should no longer show live turnover 0. If it still does, flag it as an engine issue.
- P-0001 now (marked 2026-11-19): +3.92% since start, +4.9% vs SPY, +2.0% vs min-vol, DD -1.1%. Judge nothing before 13 weeks.
- Propose a card only when there is new economic logic. Do not add low-vol variants.
- Queue items only run when the owner starts a manual batch (max 20, provisional).

## Pending queue ids
None (R-0001 to R-0009 all ran).

## Dashboard refresh
2026-11-21: attempted after the push; the result is in the run's final message.
