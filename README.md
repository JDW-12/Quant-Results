# quant-results

Written by the research engine (quant-research, `python -m src.export.publish`) and the Claude
researcher (Phase 10). Who owns what:

| path | owner | rule |
|---|---|---|
| `dashboard.json`, `leaderboard.json`, `gates.json`, `paper.json`, `batch_summary.json`, `errors.json` | engine | regenerated on every publish; do not edit |
| `registry_dump.jsonl`, `paper_dump.jsonl` | engine | full text backups of the registry and paper DB; do not edit |
| `engine/STATE.md` | engine | copy of the code repo's STATE.md; do not edit |
| `engine/JOURNAL.md` | engine | latest code-repo JOURNAL.md entries; do not edit |
| `README.md`, `.gitignore` | engine | this file; do not edit |
| `researcher/STATE.md` | researcher | the researcher's state; the engine created it once and never touches it |
| `researcher/JOURNAL.md` | researcher | append-only research journal (`## YYYY-MM-DD title` entries); mirrored into the engine; an `unfreeze: <family> — <justification>` line (justification >= 20 chars) unfreezes a frozen family |
| `queue.yaml` | researcher | queue requests, merged by `python -m src.research.sync_queue` |
| `hypotheses/H-NNNN.yaml` | researcher | new hypothesis cards, validated strictly, copied only as NEW ids |
| `researcher/notes/` | researcher | free; never read by the engine |

Rules: the engine never writes, rewrites or deletes a researcher-owned file (it only creates a
missing `researcher/STATE.md`, `researcher/JOURNAL.md`, `queue.yaml` or `hypotheses/README.md`
once from a template). Edits to engine-owned files are overwritten by the next publish. Invalid
queue items, cards and journal entries are rejected and listed in `errors.json`. Nothing in this
repository is executed by the engine: every file is read as data.
