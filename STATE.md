<!-- Engine-generated mirror of the code repo's STATE.md. Do not edit here. -->
# STATE

Current state of the research system. Read at the start of every cycle, updated at the end.

## Build status (2026-10-08, owner decisions: Gate 1 v2 risk-adjusted, rebalance frequency, withholding)

- **Owner decisions 2026-10-08 (built, see JOURNAL.md):**
  **Gate 1 v2** (`config/gates.yaml` `version: 2`, pre-registered before
  further testing): AR vs SPY > 0.3, AR vs EW > 0, AR vs the 12-1 baseline
  > 0, DSR of beta-adjusted active returns > 0.95 vs SPY and vs EW, family
  PBO on beta-adjusted active returns vs SPY < 0.3, share of years with AR
  vs SPY > 0 >= 0.6, AR vs SPY at 2x costs > 0, sensitivity and FF5+MOM
  alpha t unchanged (AR = CAPM appraisal ratio: annualised alpha /
  annualised residual vol of daily excess returns over FF rf). Every
  evaluation and scorecard records its gates version; old IR numbers stay
  as informational fields. `python -m src.gates gate1 --all` re-evaluates
  everything (appended). **Rebalance frequency**
  `rebalance_every_weeks` 1-4 (anchored at the first OOS signal date;
  k = 1 leaves every existing strategy hash unchanged). **Broker** Trading
  212: FX per trade 15 bps and fees 2 bps kept; **US dividend
  withholding** 15% modelled as its own cost line (`dividend_withholding`
  in `config/costs.yaml`). Cards: rebalance [1, 4] added to H-0002, H-0004,
  H-0005, H-0011; new H-0012 (low vol, slow rebalance, risk-adjusted).

- **Phase 1 (data layer): built.** `src/data`. Runs on real data on the VPS
  (902 tickers, S&P 500 + 400 current constituents, yfinance). The build
  sandbox has no market data access.
- **Phase 2 (feature and signal library): built.** `src/features`, 26 registered
  signals (20 cross-sectional, 6 market-level regime features incl. the
  turn-of-month calendar flag). Every one passes the lookahead test and the
  shuffle test on synthetic data. Not yet run on real data.
- **Phase 3 (labels, models, portfolio): built.** `src/labels`, `src/models`,
  `src/portfolio`. Single-signal, rank-average, ridge and LightGBM LambdaRank
  models behind one fit/predict interface; Gaussian HMM regime layer with
  forward-filtered (causal) states; isotonic calibration; inverse-vol top-N
  with 5%/25% iterative caps, hysteresis, quarter-Kelly option, regime
  exposure scaling and a research long/short variant.
  TODO (optional per spec): meta-labelling; switching signal weights by regime.
- **Phase 4 (backtester and validation): built, runs on real data on the VPS.**
  `src/backtest`, `src/validation`, `config/costs.yaml`, `config/validation.yaml`.
  The plain 12-1 momentum baseline runs end to end (signal at the week's last
  close -> next open -> costs -> USD and GBP curves -> purged walk-forward ->
  report) with `python -m src.backtest.pipeline [--synthetic]`.
- **Turnover fix: no-trade band is the default** (`config/backtest.yaml`,
  `min_trade_weight: 0.005`). Held names in the target book are traded only
  when more than 0.5pp from target; entries/exits always trade; the band never
  levers the book. Synthetic baseline: turnover 11.5x -> 10.3x/yr, trades
  -72%, cost drag 2.9% -> 2.6%/yr. Most remaining turnover is names entering
  and leaving the top 25, so expect a modest cut on real data too; the
  portfolio `hysteresis_buffer` is the next lever.
- **Phase 5 (registry and scorecard): built.** `src/registry` (append-only
  SQLite with triggers, crash accounting, counters, artefacts),
  `src/scoring` (full scorecard incl. PSR/DSR, PBO, FF5+mom alpha with
  Newey-West t, capacity, composite score, Gate 1 preview against
  `config/gates.yaml`). Every `run_research` call, including the baseline
  CLI, registers itself before it starts.
- **Dashboard export: built.** `python -m src.export.dashboard --out
  exports/dashboard.json` (schema v1, validated on write).
- **Phase 6 (gates and kill rules): built.** `src/gates`, CLI `python -m
  src.gates status|gate1|gate2`. Stage model as append-only registry
  `stage_events` (+ `gate_evaluations`, `holdout_uses`); Gate 1 runner;
  one-shot Gate 2 holdout with a frozen model; Gate 3 evaluation and kill
  rules as functions (the paper tracker is Phase 9); Gate 4 is a flag only.
  Two methodology fixes after the first real scorecard:
  **A** PSR/DSR now on daily ACTIVE returns vs SPY and vs the equal-weight
  universe (P(true IR > 0), deflated; Gate 1 needs > 0.95 vs both);
  total-return PSR/DSR kept as `psr_total`/`dsr_total`, never gated.
  **B** Gate 1 PBO is CSCV over the active-vs-SPY returns of all completed
  trials in the family; null (FAIL) below 10 trials. The sensitivity-variant
  PBO is now the informational `pbo_local`.
- **Phase 7 (research engine): built, autonomous mode LOCKED.** `src/research`,
  `config/budgets.yaml`, cards `hypotheses/H-0002..H-0011`. Hypothesis cards
  with strict validation and grid expansion; YAML research queue with
  registry de-duplication; Thompson sampling across families (Beta posterior
  on the composite) with a 30% exploration floor, family freeze at 200 trials
  (journal `unfreeze: <family> — <why>`), weekly under-explored quota;
  mutation engine with the 20% diversity rule and near-duplicate flag;
  sensitivity for ANY strategy; pre/post-publication split; failure-pattern
  summary; batch runner `python -m src.research.batch`.
  **Autonomy lock**: the data manifest says `survivorship_free: false`
  (yfinance), so `--autonomous` is refused; manual batches need
  `--allow-biased-data`, are capped at 20 and every entry is PROVISIONAL
  (never promoted past Gate 1). The lock lifts when the store is rebuilt
  from a survivorship-free provider (`MANIFEST.json` `survivorship_free:
  true`).
- **PIT S&P 500 universe (optional, `universe_mode: pit_sp500`): built.**
  `src/data/membership.py` + `config/universe.yaml` `universe_mode`. Free
  historical S&P 500 membership (fja05680/sp500, since 1996) stored as the
  versioned `membership` dataset; prices for every member since 2005; the
  universe at t = members at t (known at t) with prices passing $5/$5m;
  breadth/dispersion over PIT members; coverage report per year in
  `data/reports/coverage_*.json` + manifest + report + export. Default stays
  `current` (no change). Still survivorship biased (dead members missing on
  Yahoo): `survivorship_free: false`, the autonomy lock stays on. Real file
  (upstream commit a2430f2, 2026-09-07): 2720 change rows 1996-01-02 ..
  2026-08-18; 977 tickers ever members since 2005 (906 by 2022); 495 members
  on 2005-01-03, 499 on 2010-01-04, 503 on 2022-12-30. Yahoo coverage not
  measured yet (the sandbox cannot reach Yahoo).
- **Phase 8 (VPS deployment): built, not yet installed on the VPS.**
  `src/ops` (`python -m src.ops run nightly|light|refresh`, `status`),
  `src/data/snapshot.py`, `src/export/publish.py` + `results_repo.py`,
  `src/research/sync_queue.py`, `config/deploy.yaml`, `deploy/` (install /
  uninstall scripts, systemd unit + timer templates, logrotate),
  `docker/` (Dockerfile, compose.yaml), `requirements.lock`.
  Nightly 01:15 UK: guard -> queue sync -> weekly research data refresh (new
  snapshot) -> `--autonomous` batch (LOCKED on biased data => logged
  `skipped: locked (survivorship-biased data)`, exit 0; never
  `--allow-biased-data`) -> `gate1 --all-pending` (only after new
  experiments) -> publish. Light job every 4 h (05:05 .. 21:05, none in
  06:30-09:00): queue sync -> publish. Heavy steps skip when
  MemAvailable+SwapFree < 3 GB or 06:30-09:00 UK; job file lock. Data
  snapshots `data/snapshots/<data_version>/` + `data/current`; prune never
  deletes a snapshot referenced by the registry or the holdout log. Results
  repo `JDW-12/quant-results` gets dashboard, leaderboard, gates, paper
  (placeholder), batch summary (incl. lock status), registry dump, STATE,
  JOURNAL, errors; idempotent; results key only. The researcher's
  `queue.yaml` and `hypotheses/` there are merged/validated into the local
  queue and cards. Daily paper-data refresh: placeholder (Phase 9).
- Phase 9 onward (paper tracker): not started.

## Results so far

First research batch on the VPS (PIT S&P 500 universe, free biased data,
all trials PROVISIONAL, as reported by the owner): every strategy lost to
equal weight after costs; turnover is the dominant driver (~0.25-0.3% per
round trip, FX at 15 bps per trade ~60% of costs); 252d low vol had the best
Sharpe (0.93 vs EW 0.73, SPY 0.69) but IR vs SPY -0.13 because it is low
beta. This led to the owner decisions above. The registry numbers of that
batch were scored under Gate 1 v1 and WITHOUT dividend withholding (their
costs understate the tax drag by roughly 15% of the dividend yield, i.e.
~0.2-0.3%/yr for a ~1.5-2% yielding book; ESTIMATE).

### Real data, VPS, before the no-trade band

First real 12-1 momentum baseline, 2010-2022 out of sample, net of costs,
survivorship biased (current constituents): 21.4%/yr, vol 27.8%, Sharpe 0.82,
max DD -41.9%, turnover 19.3x/yr, cost drag 4.6%/yr (FX 60% of costs).
Equal-weight universe baseline Sharpe also 0.82. IR 0.60 vs SPY, 0.38 vs
equal weight. Not yet registered (pre-dates the registry): rerun it with the
band so it becomes registry trial #1.

## Things the researcher should know

- **Two universes.** `current` (today's S&P 500+400, ~900 names, inflated by
  survivorship AND index-inclusion hindsight) and `pit_sp500` (S&P 500 as it
  was at each date, ~500 names, only survivorship bias left, coverage below
  100% in early years: read the coverage line in every report). Results
  are not comparable across them (different breadth). A strategy run on one
  is NOT de-duplicated against the other (the queue key is strategy +
  universe), but its holdout shot is shared (Gate 2 is keyed on the
  strategy alone), and trials on both count towards the same family and
  global DSR deflation and family budgets. Prefer `pit_sp500` evidence; treat
  a strategy whose edge shrinks sharply from `current` to `pit_sp500` as
  mostly inclusion bias.

- **Nothing can pass Gate 1 until its family has >= 10 completed trials**
  (family PBO). Plan research so that a family is explored before judging
  it; `python -m src.gates gate1 --all-pending` re-evaluates earlier
  failures as the family grows.
- **Gate 1 is version 2 (risk-adjusted) since 2026-10-08**: it asks for
  CAPM alpha per unit of residual risk vs SPY (AR > 0.3), vs EW and vs the
  12-1 baseline (AR > 0), with DSR > 0.95 on BETA-ADJUSTED active returns vs
  both SPY and EW. A low-beta book no longer fails just for being low beta;
  a levered-beta book without alpha no longer passes. FF5 + MOM has no
  low-vol/BAB factor: for volatility strategies the factor alpha is partly
  the known low-vol anomaly. Gate 2 is risk-adjusted as well (holdout AR vs
  SPY > 0, Sharpe >= 50% of research) and keyed on the strategy ignoring its
  name.
- (Gate 1 version 1, retired:) asked whether the strategy beats SPY AND the equal-weight
  universe with DSR > 0.95 on active returns. The real 12-1 baseline
  (E-000001: IR 0.63 vs SPY, 0.45 vs EW over 2010-2022) would get roughly
  0.99 vs SPY and 0.95 vs EW before deflation (ESTIMATE, not computed: no
  real data here); with more trials both fall. Expect IR vs EW to be the
  binding constraint for long-only books.
- Gate 2 is one shot per strategy (strategy hash: signals, model,
  portfolio, regime options). Re-registering the same strategy with another
  seed or cost setting does not buy a second look. Every use counts towards
  the 20-model "holdout is becoming overfit" warning.
- Baselines (`baseline_*`, H-0001) are benchmarks: scored, evaluated for
  reference, never promoted.

- Every `run_research` call is a trial in the registry and counts towards
  the deflated Sharpe ratio, including failures and crashes. Do not run
  throwaway experiments against the production registry; point
  `QR_REGISTRY_DB` elsewhere for debugging.
- DSR uses the trial Sharpe variance with a floor at 1/T per period; with
  fewer than 5 finished trials the floor is used. Early DSRs are therefore
  driven by the number of trials, not their dispersion.
- The sensitivity score (and `pbo_local`) exist only when a run has a
  variant grid (`--sensitivity`; any strategy since Phase 7). Without it
  the Gate 1 sensitivity check FAILS. The composite uses the family PBO
  (0.5 while the family has < 10 trials) and the active-return DSR.
- The composite score ranks; it never promotes. The Gate 1 preview stored
  with each run is informational; `python -m src.gates gate1` decides.

- No signal has been evaluated for predictive power yet. The shuffle test
  only proves the evaluation machinery does not invent signal.
- All momentum/low-vol/reversal signals are published anomalies: test the
  post-publication period separately and expect decay.
- Free data is survivorship biased; momentum and low-vol will look better
  than they are. Sector labels are current-only.
- `resid_mom_12_1` needs about 3 years of history and `same_month_5y` about
  3-5 years, so they start later than the other signals.

- Default FX treatment is `per_trade` (0.15% on every trade's notional). It is
  the largest single cost for a weekly strategy (on the synthetic baseline
  FX was ~58% of all costs). `capital_flows` is the alternative; GBP curves
  are unhedged in both.
- Purging drops the ~4 weekly label rows before each yearly test start; the
  2-week embargo is a no-op in the forward walk-forward (it matters in CSCV).
- The synthetic-store baseline numbers (2009-2022 out of sample, 80 synthetic
  names, planted momentum strength 1.0, seed 0) are a plumbing check only:
  12-1 momentum 11.3%/yr USD, Sharpe 0.48, 11.5x two-way turnover, cost drag
  2.9%/yr, IR +0.47 vs SPY and -0.20 vs equal weight; 3x costs cut the return
  to 4.9%. PBO over the 13 sensitivity variants 0.66. None of this says
  anything about real markets.
- Runtime: about 36 s for a full `run_research` (strategy + SPY + equal weight
  + 2x/3x stress) on 900 synthetic names x 2005-2022, peak memory ~2.2 GB.
  In a research batch (sandbox, 900 synthetic names) later trials take
  12-13 s each (baselines and shared signals cached), a sensitivity trial
  with 8 variants ~100 s.

- Research engine habits (Phase 7): every experiment needs a card; queue
  items for a strategy that is already in the registry are skipped (set
  `rerun: true` + `rerun_reason` to repeat one on purpose). The engine never
  writes JOURNAL.md: a frozen family is unfrozen only by your dated entry
  with `unfreeze: <family> — <justification>`. Read
  `python -m src.research patterns` before writing new cards. Results of
  manual batches on the free data are PROVISIONAL: use them to decide what
  to test on survivorship-free data, not as evidence.
- Every seed literature card except residual momentum (H-0002, 2011) was
  published before the OOS window starts (2009; later for signals that need
  long histories), so its whole OOS window is post-publication and the
  pre-publication column is empty. Only H-0002 gets a real pre/post split.

## Next step

0000. Phase 8 deployment on the VPS (full owner steps: README "Phase 8",
   "Deployment: owner steps on the VPS"). In short:

   ```bash
   cd ~/quant-research && git pull origin main && source .venv/bin/activate && pip install -e .
   # create PRIVATE github.com/JDW-12/quant-results, then its WRITE deploy key:
   ssh-keygen -t ed25519 -N '' -C quant-results-engine -f ~/.ssh/quant_results
   #   add ~/.ssh/quant_results.pub under the repo's Settings -> Deploy keys, "Allow write access"
   GIT_SSH_COMMAND="ssh -i ~/.ssh/quant_results -o IdentitiesOnly=yes" git ls-remote git@github.com:JDW-12/quant-results.git
   python -m src.data.snapshot adopt          # existing store -> first snapshot, no download
   python -m src.ops status
   python -m src.research.sync_queue
   python -m src.export.publish --no-push && python -m src.export.publish
   python -m src.ops run light
   python -m src.ops run nightly              # expect batch "skipped: locked (survivorship-biased data)"
   deploy/install.sh --mode venv --no-enable  # or --mode docker if docker + compose exist
   sudo systemctl start quant-light.service && sudo systemctl start quant-nightly.service
   journalctl -u quant-nightly -n 80 --no-pager
   sudo systemctl enable --now quant-nightly.timer quant-light.timer
   ```

   Then report: snapshot size (`python -m src.data.snapshot list`), whether
   Docker was available, and the first nightly summary
   (`logs/jobs/last_nightly.json`). Phase 10 must decide where the researcher
   writes its own journal/state in the results repo (the engine overwrites
   `STATE.md`/`JOURNAL.md` there with mirrors).


000. On the VPS after pulling the 2026-10-08 owner-decision commits (exact
   commands; the PIT store from step 00 stays, no rebuild needed: dividends
   are already in the store and are read now):

   ```bash
   cd ~/quant-research && git pull origin main
   python -m src.research cards                     # all valid, incl. H-0012
   python -m src.gates gate1 --all                  # re-evaluate every experiment under Gate 1 v2 (appended)
   python -m src.gates status                       # nothing is promoted: all provisional/baselines
   python -m src.research enqueue H-0012 H-0005 H-0011 H-0004 H-0002
   python -m src.research queue
   python -m src.research.batch --allow-biased-data --max-experiments 20 --dry-run
   python -m src.research.batch --allow-biased-data --max-experiments 20
   python -m src.gates status
   python -m src.export.dashboard --out exports/dashboard.json
   ```

   `gate1 --all` reads the store's Fama-French rf for old runs (they have no
   rf column; pass `--root` if the store is not the default) and fails
   `positive_at_2x_costs` as unknown for them (no 2x-cost returns stored).
   Enqueue H-0012 first: its window=252 / 25 names / 4-weekly point is the
   same strategy as H-0005's window=252 / k=4 point, and the later one is
   skipped as a duplicate. The k = 1 grid points of the updated cards are the
   strategies already run (same keys) and are skipped if they ran on the same
   universe. New strategies: H-0012 4, H-0005 2, H-0011 3, H-0004 4,
   H-0002 4 = 17 (plus H-0004's k = 1 points if 6-1 was never run on PIT:
   then 21, capped at 20 per batch; run the batch again for the rest).
   Nothing can pass Gate 1 without `--sensitivity` (sensitivity check) and
   10 family trials (PBO); add `--sensitivity` to the batch once the family
   counts are there (ESTIMATE: ~10-15 min for 17 trials without it on the
   VPS, a few hours with it). Compare the k = 4 trials with their k = 1
   siblings on turnover, cost drag and `ar_spy` / `beta_spy` (dashboard
   metrics), and note the new `withholding` cost line in the reports.

00. On the VPS (PIT universe): `git pull`, then
   `python -m src.data.download --universe-mode pit_sp500` (rebuilds the
   store; ESTIMATE 10-25 min, ~980 tickers of which a few hundred return
   nothing), read the logged COVERAGE line and
   `data/reports/coverage_<version>.csv`, set `universe_mode: pit_sp500` in
   `config/universe.yaml` if it should stay the default, rerun the 12-1
   baseline (`python -m src.backtest.pipeline --sensitivity`) and compare it
   with the current-universe baseline. Refresh membership every couple of
   months with `--membership-only` (new members then need a full download).

0a. On the VPS after pulling Phase 7: `python -m src.research cards` (all
   valid), `python -m src.research status` (should say LOCKED), then
   `python -m src.research enqueue H-0011 H-0010 H-0005 H-0002` and a first
   small manual batch: `python -m src.research.batch --allow-biased-data
   --max-experiments 10 --dry-run`, check the plan, run it without
   `--dry-run` (ESTIMATE: ~5-8 min for 10 trials without sensitivity on the
   VPS; 20 trials ~10-15 min; with `--sensitivity` ~2.5-4 h for 20), then
   `python -m src.gates status` and the dashboard export. Run heavy batches
   when the other memory-hungry processes are idle; `--jobs 2` doubles
   memory (each worker loads the data).

0. On the VPS after pulling Phase 6: `python -m src.gates gate1 --experiment
   E-000001` (it is a baseline: logged for reference, never promoted; old
   runs have no `returns.parquet`, the runner derives returns from
   `equity.parquet`). Expected (ESTIMATE): dsr_active_vs_spy ~0.98-0.99
   PASS, dsr_active_vs_equal_weight ~0.94-0.95 borderline FAIL, pbo_family
   null FAIL (1 trial), beats_momentum_12_1 FAIL (it is the baseline).

1. On the VPS: rerun the baseline with the band and `--sensitivity` so it is
   registered (`python -m src.backtest.pipeline --sensitivity`), compare
   turnover/cost drag with the pre-band 19.3x / 4.6%, then export the
   dashboard. Back up `registry/` (DB is gitignored, never deleted).
2. Consider `capital_flows` FX (FX is 60% of costs) and a hysteresis buffer
   for the baseline-derived research specs.
3. Phase 6: gate runner (Gate 1 from `config/gates.yaml`, one-shot holdout
   with the access log, stage changes as registry `gate_events`).
