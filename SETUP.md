# Setting this project up on another machine

This project is four private repositories plus some state that is deliberately
not in git. Clone them into the layout below — **the layout is load-bearing**,
not a convention: `run_desk.py` resolves the frontend at `../design-system/shell`
relative to the engine repo, so the directories must nest exactly this way.

```
AI Stock/                      <- ai-stock-record  (this repo, clone it first)
├── Stock-Prediction-Models/   <- ai-stock-engine   (gitignored here)
├── design-system/
│   ├── MANIFESTO.md           (tracked here)
│   ├── shell/                 <- ai-stock-shell    (gitignored here)
│   └── references/            (not in git — see "Not in git" below)
├── psa_platform/              (tracked here)
└── *.md, MISSION, roadmaps    (tracked here — the research record)
```

`D:\trading agents v2` is the fourth repo (`trading-desk`) and lives outside
this tree entirely.

## 1. Clone

```bash
git clone https://github.com/onurcelk/ai-stock-record.git "AI Stock"
cd "AI Stock"
git clone https://github.com/onurcelk/ai-stock-engine.git Stock-Prediction-Models
git clone https://github.com/onurcelk/ai-stock-shell.git design-system/shell
git clone https://github.com/onurcelk/trading-desk.git   # wherever you want it
```

Both the engine and the shell have work on branches other than `master`. The
branch the desk was last built from is `engine-sources-owner-directed` in
**both** repos — they are separate histories that move together, so check out
the matching branch in each:

```bash
git -C Stock-Prediction-Models checkout engine-sources-owner-directed
git -C design-system/shell     checkout engine-sources-owner-directed
```

## 2. Python — 3.11 specifically

OpenBB does not support 3.13+, and the pins were generated under 3.11.9. Do not
use a system 3.13/3.14 interpreter.

```bash
cd Stock-Prediction-Models
py -3.11 -m venv venv
venv/Scripts/pip install -r requirements.txt
venv/Scripts/python -m pytest -q        # the fast suite; should pass clean
```

Note: on the old machine there were two virtualenvs, `.venv` and `venv`, and
only `venv` had FastAPI — `launcher/start.ps1` tests for the `fastapi` package
because of it. A single `venv` built from `requirements.txt` has everything;
there is no reason to recreate the second one.

## 3. Frontend

```bash
cd design-system/shell
npm install
npm run build          # without a production build run_desk.py falls back to dev
```

`NEXT_PUBLIC_API_BASE` defaults to `http://localhost:8000`, which is where the
API serves. No `.env` file is needed unless you move the API.

## 4. Run it

```bash
cd Stock-Prediction-Models
python run_desk.py             # API on :8000, Next.js on :3000
python run_desk.py --dev       # Next in dev mode, uvicorn --reload
python run_desk.py --api-only
```

Streamlit is the retained fallback, not the desk: `python run_app.py` (never
`streamlit run app/streamlit_app.py` directly — only the launcher attaches the
ledger backup lifecycle).

## 5. The trading desk MCP server

Needs Python 3.9–3.12 as well. Register it with Claude Code at user scope:

```bash
claude mcp add --scope user --transport http trading-desk http://127.0.0.1:8010/mcp
```

MCP servers load at session start, so restart Claude Code afterwards. Start the
server with `.venv/Scripts/tradingdesk.exe serve` from the desk repo. If the
desk does not live on `D:\` on the new machine, the paths in the root
`CLAUDE.md` need updating to match.

## 6. Ollama models

Re-pull rather than copy (~54 GB):

```bash
ollama pull qwen3-coder:30b
ollama pull qwen3:30b
ollama pull qwen3.5:9b
ollama pull nomic-embed-text
```

Then rebuild the 32k-context variants from the Modelfiles in this repo:

```bash
ollama create qwen3coder-32k -f Modelfile-qwen3coder-32k
ollama create qwen35-32k     -f Modelfile-qwen35-32k
```

Gemini CLI and Codex CLI both need re-authenticating (Codex via ChatGPT login).

## Not in git — what you must carry across by hand

Regenerable things were left out on purpose. These were not, and no clone will
produce them:

| Path | What it is |
|---|---|
| `Stock-Prediction-Models/app/forecast_ledger.sqlite3` | **The prospective forecast record.** Append-only, stamped before outcomes were known. Cannot be reconstructed — a replay is a different claim. Carry this one first. |
| `Stock-Prediction-Models/app/holdings.json`, `transactions.json`, `ledger_backup_state.json` | Book state |
| `Stock-Prediction-Models/app/score_logs/`, `collection_logs/` | Collection and scoring history |
| `D:\trading agents v2\data\desk.sqlite3` | The desk's predictions and scorecard |
| `D:\trading agents v2\artifacts\` | Published reports and briefs |
| `~/ai-orchestration/log.jsonl` | Cost/latency metering history |
| `~/.claude/projects/c--Users-onurc-Desktop-AI-Stock/memory/` | Claude Code's memory: the closure record for V2/V3/V4. The folder name is derived from the project path — rename it if the project lands elsewhere. |
| `~/CLAUDE.md` | The model-delegation policy |
| `design-system/references/` | 41 MB of vendored UI sources (bklit-ui, kokonutui, motion) — re-fetchable from upstream, or copy them |

Deliberately regenerable, do **not** carry: `alpha/edgar/` (6.0 GB, re-downloads
from SEC), `alpha/out/*.pkl`, `alpha/cache/`, `app/replay_study.sqlite3`,
`app/tournament.sqlite3`, `app/cache/`, `app/runs/`, `node_modules/`, `.next/`.
