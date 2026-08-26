# Setting this project up on another machine

Covers **Windows and macOS**. Where the two differ, both are given — the macOS
path is additional, never a replacement. Steps without a platform heading are
identical on both.

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

The fourth repo (`trading-desk`) lives outside this tree entirely — it was at
`D:\trading agents v2` on the Windows machine. On macOS put it anywhere and
update the "Trading Desk" section of `~/CLAUDE.md` to match; see step 5.

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

### Windows

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

### macOS

Use `requirements-macos.txt`, **not** `requirements.txt`. The Windows file was
produced by `pip freeze` on Windows and carries two wheels that have no macOS
build at all — `pywinpty` and `tensorflow-intel` — so installing it fails
before it reaches anything interesting. The macOS file is the same pin minus
five lines; see its header for exactly which and why.

Get a 3.11 interpreter with `brew install python@3.11` or pyenv, then:

```bash
cd Stock-Prediction-Models
python3.11 -m venv venv
venv/bin/pip install -r requirements-macos.txt
venv/bin/python -m pytest -q            # the fast suite; should pass clean
```

Note `venv/bin/`, not `venv/Scripts/`. The two-virtualenv history above is a
Windows artefact and does not apply — build one `venv` and be done.

### TensorFlow is optional, and on Apple Silicon it needs its own step

**You do not need TensorFlow to bring the desk up.** `app/core/forecast.py`
imports it lazily, inside the projection function rather than at module scope,
because the import costs several seconds and nothing else in the module wants
it. Verified by import rather than assumed: `import api.main` and
`import app.core.forecast_ledger` both complete with `tensorflow` absent from
`sys.modules`. So the API, the frontend, the ledger, the scan router and the
whole UI run against `requirements-macos.txt` exactly as it stands.

TensorFlow loads only when the LSTM projection is actually called — in
practice the headless daily freeze (`python -m core.collector`) and the model
registered at `app.core.forecast.project`. Install it when you reach that
point, not before:

```bash
venv/bin/pip install tensorflow-macos==2.15.0    # Apple Silicon
venv/bin/pip install tensorflow-metal            # optional, GPU plugin
```

Apple Silicon needs `tensorflow-macos` specifically: the 2.15 generation
predates the unified macOS wheel, so there is no arm64 `tensorflow==2.15.1` to
install. On Intel Macs the plain `tensorflow` wheel does exist. `keras` and
`tensorboard` are already pinned at matching 2.15 versions in
`requirements-macos.txt`, so this does not need a second pass.

The macOS pin has not been verified by an actual macOS install — it was
written on the Windows machine and its removals are reasoned from wheel
availability. If a pin turns out to have no macOS wheel either, drop it and
note it in that file's header.

## 3. Frontend

Identical on both platforms. Next 16.3.2 / React 19.2.8, so Node 20+ (the
Windows machine ran Node 24).

```bash
cd design-system/shell
npm install
npm run build          # without a production build run_desk.py falls back to dev
```

`NEXT_PUBLIC_API_BASE` defaults to `http://localhost:8000`, which is where the
API serves. No `.env` file is needed unless you move the API.

## 4. Run it

`run_desk.py` is the launcher on every platform. It invokes the API through
`sys.executable`, finds npm with `shutil.which`, and its one platform branch
(`os.name == "nt"`, for killing the `next start` process tree) falls through to
`process.terminate()` on POSIX. Nothing about it is Windows-specific.

```bash
cd Stock-Prediction-Models
python run_desk.py             # API on :8000, Next.js on :3000
python run_desk.py --dev       # Next in dev mode, uvicorn --reload
python run_desk.py --api-only
```

On macOS call it through the venv: `venv/bin/python run_desk.py`.

Streamlit is the retained fallback, not the desk: `python run_app.py` (never
`streamlit run app/streamlit_app.py` directly — only the launcher attaches the
ledger backup lifecycle).

**macOS: ignore `launcher/`.** `start.ps1`, `stop.ps1` and the two `.vbs`
files are Windows shortcuts for the desktop icon. They have no macOS
equivalent and no macOS purpose — `run_desk.py` is what they call anyway.

## 5. The trading desk MCP server

Needs Python 3.9–3.12 as well. Register it with Claude Code at user scope:

```bash
claude mcp add --scope user --transport http trading-desk http://127.0.0.1:8010/mcp
```

MCP servers load at session start, so restart Claude Code afterwards. Start the
server from the desk repo:

```bash
.venv/Scripts/tradingdesk.exe serve     # Windows
.venv/bin/tradingdesk serve             # macOS — no .exe
```

If the desk does not live on `D:\` on the new machine, the paths in the root
`CLAUDE.md` need updating to match. **On macOS there is no `D:` drive at all**,
so this is not optional: put the `trading-desk` clone wherever you like and
edit the "Trading Desk" section of `CLAUDE.md` to point at it. The desk's own
`pyproject.toml` requires `>=3.9.21,<3.13` and neither repo has a hardcoded
Windows path in tracked Python, so nothing else needs changing.

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

All of it is in the state bundle — `ai-stock-state-2026-08-26.zip`, 176 files,
1.03 MB — whose `RESTORE.md` gives the exact destination for each entry and
the commands to verify it landed. That file is the authority; the table here
is the summary.

| Path | What it is |
|---|---|
| `Stock-Prediction-Models/app/forecast_ledger.sqlite3` | **The prospective forecast record.** 371 forecasts, 93 resolved outcomes. Append-only, stamped before outcomes were known. Cannot be reconstructed — a replay is a different claim. Carry this one first. |
| `Stock-Prediction-Models/app/holdings.json`, `transactions.json`, `ledger_backup_state.json` | Book state |
| `Stock-Prediction-Models/app/score_logs/`, `collection_logs/` | Collection and scoring history |
| `Stock-Prediction-Models/app/runs/` | 117 timestamped run outputs. Listed under a "local data" line in `.gitignore` beside genuine caches, but each is a snapshot against the data of its day, so re-running produces different files, not the same ones. In the bundle for that reason. |
| `<desk>/data/desk.sqlite3` | The desk's predictions and scorecard |
| `<desk>/artifacts/` | Published reports and briefs |
| `~/ai-orchestration/` | **The whole directory, not just the log.** `orchestrator.py` and `generate_dashboard.py` are source in no repository anywhere; `log.jsonl` is accumulated metering history. |
| `~/.claude/projects/<derived-name>/memory/` | Claude Code's memory: the closure record for V2/V3/V4 — which questions are settled and may not be re-litigated. |
| `~/CLAUDE.md` | The model-delegation policy, and the trading-desk section with its `D:\` paths |
| `design-system/references/` | 41 MB of vendored UI sources (bklit-ui, kokonutui, motion). Not in the bundle — re-fetch from upstream, or copy them. |

### The memory folder name, on macOS

`<derived-name>` comes from the project's absolute path with the separators
replaced by hyphens: `c:\Users\onurc\Desktop\AI Stock` became
`c--Users-onurc-Desktop-AI-Stock`. A macOS path has no drive letter and will
not encode the same way.

Do not hand-build the folder and guess. Start Claude Code once inside the
project directory, let it create its own project folder, then copy the 22
`.md` files from the bundle's `claude-config/memory/` into the `memory/`
directory that appears. That removes the guess entirely.

### Regenerable — do not carry

`alpha/edgar/` (6.0 GB, re-downloads from SEC), `alpha/out/*.pkl`,
`alpha/cache/`, `app/replay_study.sqlite3` (163 MB), `app/replay_ledger.sqlite3`,
`app/tournament.sqlite3` (94 MB — `python -m core.tournament`, and its result
is in the tracked `reports/HT1_TOURNAMENT_RESULT.md`), `app/cache/`,
`node_modules/`, `.next/`, and both virtualenvs. A venv especially: it is full
of absolute paths and platform binaries, and copying a Windows one to a Mac
produces something that cannot run.
