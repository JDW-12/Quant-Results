# JOURNAL (researcher)

Owned by the Claude researcher: append only, one `## YYYY-MM-DD title` entry per cycle; never
edit or delete past entries. The engine mirrors new entries into its local copy. To unfreeze a
frozen family write a line `unfreeze: <family> — <justification>` (at least 20 characters of
justification) in a dated entry; nothing else in this file has any effect on the engine.

## 2026-10-13 — First review: low-vol is the only survivor, and it is fragile in breadth

What I learned (first cycle, no earlier entries): 32 trials, 0 failed, 30 failed Gate 1, 2 in research (the two momentum baselines). No holdout use, no data errors in errors.json, nightly and light jobs ok. Paper P-0001 (E-000019) has 0 weeks tracked; first fill is Mon 2026-10-19, so nothing to judge yet (Gate 3 needs 13 weeks).

Patterns: momentum (14 trials), trend (4) and reversal (3) fail after costs, with turnover of 16 to 27x and cost drag of 4 to 6% a year. Slow-rebalanced low vol is the only family with a positive appraisal ratio (E-000019: ar_spy 0.71, E-000018: 0.67) but: alpha t-stat is 1.4, DSR is only 0.09 after 32 trials, and the result is sharp in breadth. With 50 names the same signals fall to 0.47 (252d) and 0.36 (504d), alpha t 0.3 and 0.04. A real premium should degrade smoothly from 25 to 50 names; this drop looks more like a concentration or survivorship effect, plus the known RMW/CMA exposure. I treat E-000019 as a watch item, not evidence.

Queued (9 items, all manual-batch only): H-0013 (low idiosyncratic vol, 252/504d, 25/35 names, 4-weekly; R-0001 to R-0004) and H-0014 (low beta, same grid; R-0005 to R-0008). Both are literature-based, low turnover, and mostly serve as falsification tests of the low-vol story: they are highly correlated with E-000019, so passing is weak evidence and failing is informative. The 35-name points are the plateau check. R-0009 runs the untested liquidity card H-0008 at low priority. 8 trials added to the volatility family: I accept the multiple-testing cost because the aim is to learn whether it is robust.

Deliberately NOT doing: no more momentum/trend/reversal variants (no sign of a cost-surviving edge); no seasonality card H-0009 (weekly turnover will fail on costs); no new low-vol window tuning; nothing touching the holdout; no proposal to loosen any gate.
