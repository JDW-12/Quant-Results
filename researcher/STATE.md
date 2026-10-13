# STATE (researcher)

Owned by the Claude researcher: the engine created this file once and never changes it.
Read at the start of every cycle, updated at the end. The engine's own state is engine/STATE.md.

## Current focus
Test whether the slow low-vol result is robust or an artefact. Evidence so far (2026-10-13): 32 trials, 0 Gate 1 passes. Best: E-000019 low vol 252d, 25 names, 4-weekly (appraisal vs SPY 0.71, alpha t 1.38, DSR 0.09), paper-tracked as P-0001 (first fill 2026-10-19). Same signal with 50 names is much weaker (0.47, t 0.3): sharp in breadth, so suspect concentration/survivorship/RMW-CMA exposure. Momentum, trend and reversal fail on costs; do not revisit them.

## Open questions
- Does low idio-vol or low beta (H-0013, H-0014) reproduce low vol at 25 AND 35 names? A failure at 35 means the low-vol result is fragile.
- Is any of it independent of known quality/defensive factors (alpha t stays below 2)?
- Liquidity (H-0008) and seasonality (H-0009) are untested; H-0009 judged too high-turnover.

## Next cycle
- Check whether the owner ran a manual batch for R-0001 to R-0009; compare 25 vs 35 name results.
- Check P-0001 after its first fill (2026-10-19); Gate 3 needs 13 weeks, so judge nothing early.
- Do not add more low-vol variants unless a result demands it; look at under-explored families if any.

## Pending queue ids
R-0001 to R-0009 (owner must start a manual batch; max 20).
