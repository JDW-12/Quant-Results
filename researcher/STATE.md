# STATE (researcher)

Owned by the Claude researcher: the engine created this file once and never changes it.
Read at the start of every cycle, updated at the end. The engine's own state is engine/STATE.md.

## Current beliefs (2026-11-19)
- 46 trials, 0 Gate 1 passes, holdout untouched. Momentum, trend, reversal fail on costs.
- Low vol is a noisy, mildly positive defensive tilt, not a demonstrated edge: E-000019 (AR 0.71, alpha t 1.4, DSR 0.09) is the top draw of ~17 volatility trials; likely RMW/CMA exposure plus survivorship.
- P-0001 holds utilities + REITs/insurers (+KO since the 2026-11-16 rebalance): a rates/sector bet; outperformance so far is beta to a soft tape.
- First P-0001 rebalance (2026-11-16): 8 trades, 18.1% turnover, ~$5.6 costs. That is about 2.4x a year against 3.06 in the backtest, so it is in line.

## Open questions
- Is there any testable idea outside price-only signals? Quality/value need PIT fundamentals (not available free).
- Does P-0001 track sensibly vs SPY and min-vol after 13 weeks?

## Next cycle
- After the week-ending 2026-11-20 mark (Sunday 2026-11-22 publish): weeks_tracked should be 5, and the Gate 3 turnover/cost checks should no longer show live turnover 0. If they still do, flag it as an engine issue.
- P-0001 now (marked 2026-11-18): +4.42% since start, +4.4% vs SPY, +1.9% vs min-vol, current DD -0.6%. Judge nothing before 13 weeks.
- Propose a card only with new economic logic; do not add low-vol variants.
- Queue items only run on an owner-started manual batch (max 20, provisional).

## Pending queue ids
None (R-0001 to R-0009 all ran).

## Dashboard refresh
2026-11-19: attempted after push; result in the run's final message.
