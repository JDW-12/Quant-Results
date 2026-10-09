# JOURNAL (latest entries, newest first)

_Engine-generated mirror of the latest 10 entries of the code repo's JOURNAL.md. Do not edit here._

## 2026-10-08 Owner decision: objective is risk-adjusted; Gate 1 v2 pre-registered before further testing

Recorded by the engineer on the owner's instruction. This is the OWNER'S DECISION about what the
system optimises, not a research conclusion; no new result motivated a specific threshold.

Context (first research batch on the VPS, PIT S&P 500 universe, free survivorship-biased data,
all trials PROVISIONAL): every strategy lost to the equal-weight universe after costs; turnover is
the dominant driver (about 0.25-0.3% round trip per trade, of which FX at 15 bps per trade is about
60%); 252-day low volatility had the best Sharpe (0.93 vs equal weight 0.73 and SPY 0.69) but an IR
vs SPY of -0.13 because it is a low-beta book. Gate 1 v1 asked for active return vs SPY, which a
low-beta book cannot deliver in a bull market however good its risk-adjusted return.

Decisions:
1. Objective: RISK-ADJUSTED performance. Gate 1 becomes version 2 (`config/gates.yaml`
   `version: 2`), fixed now, BEFORE any further testing, and every evaluation records its version.
2. Broker: Trading 212 (commission free, 0.15% FX on every foreign trade): keep `fx.mode: per_trade`
   at 15 bps and `fees_bps: 2` as a conservative allowance. US dividends are taxed at the 15%
   W-8BEN treaty rate: `dividend_withholding: 0.15` in `config/costs.yaml`.
3. A rebalance-frequency option (`rebalance_every_weeks`, 1-4) is added so slow signals can be
   traded less often.

Gate 1 v2, exact checks (all on walk-forward OOS daily USD returns after costs; AR = CAPM appraisal
ratio = annualised alpha / annualised residual volatility from regressing daily strategy excess
returns over the Fama-French rf on the benchmark's excess returns; unknown inputs fail):
- ar_vs_spy: AR vs SPY > 0.3
- ar_vs_equal_weight: AR vs the equal-weight universe > 0
- beats_momentum_12_1: AR vs the registered plain 12-1 momentum baseline > 0 (fails with the reason
  when no baseline returns are available)
- dsr_beta_adj_vs_spy and dsr_beta_adj_vs_equal_weight: deflated Sharpe of the beta-adjusted active
  returns ((r - rf) - beta (b - rf) = alpha + residual) > 0.95 against each, deflated by the family
  and the global trial counts (the stricter one), trial variance from the other trials' ARs
- pbo_family: family PBO < 0.3, CSCV over the family's completed trials ranked on their beta-adjusted
  active returns vs SPY (null below 10 trials -> fail)
- years_positive_ar_share: share of calendar years (>= 20 days) with AR vs SPY > 0 >= 0.6
- positive_at_2x_costs: AR vs SPY at 2x costs > 0
- sensitivity_loss_20: <= 30% Sharpe loss at +-20% parameter perturbation (unchanged)
- factor_alpha_t: FF5 + momentum alpha t-stat (Newey-West) > 2 (unchanged). Caveat: FF5 + MOM has no
  low-volatility / betting-against-beta factor, so for volatility-family strategies part of that
  alpha is the known low-vol anomaly itself.

The IR-based numbers stay in every scorecard as informational fields. All existing experiments are
to be re-evaluated under v2 with `python -m src.gates gate1 --all` (evaluations are appended; the
v1 evaluations stay in the registry). Gate 2 (holdout: IR vs SPY > 0 and Sharpe >= 50% of research)
is NOT changed by this decision.
