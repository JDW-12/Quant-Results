"""Turn the engine's published files into the small row tables the dashboard reads.

Run from the results repo root:  python3 researcher/tools/build_dashboard_tables.py
Reads dashboard.json, paper.json and batch_summary.json (engine-owned) and writes
researcher/dash/*.json (arrays of row objects). It only reshapes: no number is
computed here except unit conversions, counts and the per-portfolio return series
rebased to 1.0, so every figure on the dashboard traces back to an engine file.
"""

from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "researcher" / "dash"

# Experiments whose equity curves are shown: the best by appraisal ratio vs SPY plus the baselines.
EQUITY_TOP = 6


def _load(name: str) -> dict:
    p = ROOT / name
    return json.loads(p.read_text()) if p.exists() else {}


def _num(x):
    return x if isinstance(x, (int, float)) and x == x else None


def _passes(checks: list) -> tuple[int, int]:
    known = [c for c in checks or [] if c.get("pass") is not None]
    return sum(1 for c in known if c["pass"]), len(checks or [])


def build() -> dict[str, list]:
    dash, paper, batch = _load("dashboard.json"), _load("paper.json"), _load("batch_summary.json")
    exps = dash.get("experiments", [])

    experiments = []
    for e in exps:
        m = e.get("metrics") or {}
        passed, total = _passes(e.get("gate1_checks"))
        experiments.append({
            "id": e["id"], "name": e.get("name"), "family": e.get("family"),
            "hypothesis": e.get("hypothesis_id"), "stage": e.get("stage"), "status": e.get("status"),
            "provisional": bool(e.get("provisional")), "universe": e.get("universe_mode") or "current",
            "baseline": (e.get("name") or "").startswith("baseline_"),
            "created": (e.get("created_at") or "")[:10],
            "ann_return": _num(m.get("ann_return")), "sharpe": _num(m.get("sharpe")),
            "beta_spy": _num(m.get("beta_spy")), "ar_spy": _num(m.get("ar_spy")), "ar_ew": _num(m.get("ar_ew")),
            "max_dd": _num(m.get("max_dd")), "turnover": _num(m.get("turnover")),
            "alpha_t": _num(m.get("alpha_t")), "dsr": _num(m.get("dsr")), "pbo": _num(m.get("pbo")),
            "composite": _num(m.get("composite")),
            "gate1_passed": passed, "gate1_checks": total,
        })

    families = [{"family": f, "trials": n} for f, n in sorted((dash.get("counters") or {}).get("by_family", {}).items(),
                                                              key=lambda kv: -kv[1])]

    gate1_checks = []
    for e in exps:
        for c in e.get("gate1_checks") or []:
            gate1_checks.append({"id": e["id"], "check": c.get("name"), "value": _num(c.get("value")),
                                 "threshold": c.get("threshold"),
                                 "result": {True: "pass", False: "fail"}.get(c.get("pass"), "unknown"),
                                 "reason": c.get("reason")})

    # Equity curves: best experiments by AR vs SPY that carry a curve, the PIT 12-1 baseline, plus SPY/EW.
    with_eq = [e for e in exps if (e.get("equity") or {}).get("dates")]
    ranked = sorted((e for e in with_eq if not (e.get("name") or "").startswith("baseline_")),
                    key=lambda e: -((e.get("metrics") or {}).get("ar_spy") or -9))[:EQUITY_TOP]
    pit_base = [e for e in with_eq if (e.get("name") or "").startswith("baseline_")
                and e.get("universe_mode") == "pit_sp500"][-1:]
    equity = []
    for e in ranked + pit_base:
        q = e["equity"]
        for i, day in enumerate(q["dates"]):
            equity.append({"id": e["id"], "date": day, "value": _num(q["strategy"][i])})
    ref = (pit_base or ranked)[:1]
    for e in ref:
        q = e["equity"]
        for key, label in (("spy", "SPY"), ("equal_weight", "Equal weight")):
            for i, day in enumerate(q["dates"]):
                if i < len(q.get(key) or []):
                    equity.append({"id": label, "date": day, "value": _num(q[key][i])})

    portfolios, paper_curve, positions = [], [], []
    for po in paper.get("portfolios", []):
        g3, kill = po.get("gate3") or {}, po.get("kill") or {}
        portfolios.append({
            "id": po["id"], "experiment": po.get("experiment_id"), "label": po.get("label"),
            "kind": po.get("kind"), "status": po.get("status"), "start": po.get("start_date"),
            "first_fill": po.get("first_fill_date"), "last_mark": po.get("last_mark_date"),
            "weeks": po.get("weeks_tracked"), "min_weeks": po.get("min_weeks"), "target_weeks": po.get("target_weeks"),
            "value_gbp": _num(po.get("value_gbp")), "return": _num(po.get("return_since_start")),
            "vs_spy": _num(po.get("vs_spy")), "vs_minvol": _num(po.get("vs_minvol")),
            "max_dd": _num(po.get("max_dd")), "drawdown_limit": _num(po.get("drawdown_limit")),
            "rolling_ir": _num(po.get("rolling_ir")), "rolling_ar": _num(po.get("rolling_ar")),
            "gate3": (f"pending ({po.get('weeks_tracked') or 0}/{po.get('min_weeks') or 13} weeks)"
                      if (po.get("weeks_tracked") or 0) < (po.get("min_weeks") or 13)
                      else g3.get("status") or ("passed" if g3.get("passed") else "not passed")),
            "kill": kill.get("status"),
        })
        eq = po.get("equity") or {}
        dates = eq.get("dates") or []
        series = [("Strategy", eq.get("strategy") or [])]
        bms = eq.get("benchmarks") or {}
        series += [(k.upper() if k == "spy" else ("Min vol ETF" if k == "minvol" else k), v)
                   for k, v in (bms.items() if isinstance(bms, dict) else [])]
        for name, vals in series:
            for i, day in enumerate(dates):
                if i < len(vals) and _num(vals[i]) is not None:
                    paper_curve.append({"portfolio": po["id"], "series": name, "date": day, "value_gbp": vals[i]})
        if not dates and po.get("start_date"):
            # Before the first fill the book is GBP cash at its starting capital: one honest point per series.
            names = ["Strategy"] + [("SPY" if b.get("id") == "spy" else "Min vol ETF" if b.get("id") == "minvol" else b.get("id"))
                                    for b in po.get("benchmarks") or [] if isinstance(b, dict)]
            for name in names:
                paper_curve.append({"portfolio": po["id"], "series": name, "date": po["start_date"],
                                    "value_gbp": po.get("capital_gbp") or 10000.0})
        for pos in po.get("positions") or []:
            positions.append({"portfolio": po["id"], "ticker": pos.get("ticker"), "weight": _num(pos.get("weight"))})

    lock = batch.get("lock") or {}
    last = batch.get("last_nightly_job") or {}
    counters = dash.get("counters") or {}
    status = [{
        "generated": dash.get("generated_at"), "free_data": bool(dash.get("free_data")),
        "banner": dash.get("banner"), "lock": lock.get("autonomous_batches", "unknown"),
        "total_trials": counters.get("total_trials"), "failed_trials": counters.get("failed_trials"),
        "families": len(counters.get("by_family") or {}),
        "holdout_uses": (dash.get("holdout") or {}).get("uses"),
        "gate1_passes": sum(1 for e in exps if e.get("stage") in ("gate1", "holdout", "paper", "eligible")),
        "paper_portfolios": len(paper.get("portfolios", [])),
        "data_version": dash.get("data_version"),
        "coverage": (dash.get("universe") or {}).get("coverage_pct"),
        "last_nightly": last.get("local_date"),
        "last_nightly_ok": all(s.get("status") in ("ok", "skipped") for s in last.get("steps") or []),
    }]

    journal = [{"date": j.get("date"), "title": j.get("title"), "body": j.get("body")}
               for j in dash.get("journal", [])]
    rj = ROOT / "researcher" / "JOURNAL.md"
    if rj.exists():
        cur = None
        for line in rj.read_text().splitlines():
            if line.startswith("## "):
                head = line[3:].strip()
                date, _, title = head.partition(" ")
                cur = {"date": date, "title": title.strip(" —-") or "Researcher entry", "body": ""}
                journal.append(cur)
            elif cur is not None:
                cur["body"] += line + "\n"
    journal.sort(key=lambda j: j.get("date") or "", reverse=True)

    return {"status": status, "experiments": experiments, "families": families, "gate1_checks": gate1_checks,
            "equity": equity, "paper": portfolios, "paper_curve": paper_curve, "positions": positions,
            "journal": journal[:20]}


def main() -> None:
    OUT.mkdir(parents=True, exist_ok=True)
    for name, rows in build().items():
        (OUT / f"{name}.json").write_text(json.dumps(rows, separators=(",", ":")))
        print(f"{name}: {len(rows)} rows")


if __name__ == "__main__":
    main()
