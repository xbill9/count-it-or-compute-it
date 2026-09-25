# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

Entry for the dev.to Kaggle Benchmarking Challenge (due 2026-10-11, 11:59 PM PDT; the post must link the benchmark on Kaggle). The benchmark is "Count It or Compute It": the same 68 counting questions in five task modes.

## Tasks

- `tasks/count_in_context.py`, `count_python_tool.py`, `count_python_told.py`, `count_rows_tool.py`, `count_engine.py`: one Kaggle task per file, slug = file name with `-` for `_`. Each file must stand alone on Kaggle, so the data, filter parser and scoring code is copied into each one between `# ---- shared:` and `# ---- end shared ----`.
- `count_python_told.py` must differ from `count_python_tool.py` only in its names and the one "use the tool" sentence; `check.py` enforces it.
- **The shared block must be byte-identical in every task file.** Edit it in one file, copy it to the others, then run `python3 tasks/check.py`. That script needs no model calls and no `kaggle_benchmarks`.
- A PostToolUse hook runs `ruff check` (config in `ruff.toml`) and `check.py` after every edit to `tasks/*.py`. A failure comes back as hook feedback; fix it before pushing.
- Ground truth is computed by code from each row's `truth_where` filter. Never hand-write an expected count.
- The engine and rows-tool tasks decide whether a filter is right by checking that it selects the same integers as the true filter, never by comparing strings (`id > 9` is right for "10 or more").

## Kaggle CLI

- `kaggle` is installed in the pyenv Python and is logged in as `xbillwork`. `kaggle_benchmarks` is **not** installed locally, so tasks only run on Kaggle.
- **Never create a venv or `pip install` anything without asking.**
- Pushing and running are pre-approved; no need to confirm each command.
- `kaggle b t push <slug> -f tasks/<file>.py --wait`: the slug must match the outer `@kbench.task(name=...)`: `count-in-context`, `count-python-tool`, `count-python-told`, `count-rows-tool` or `count-engine`.
- `kaggle b t run <slug> -m <model> -m <model> --wait`: repeat `-m`; never space-separate. Model slugs come from `kaggle b t models`.
- `kaggle b t download <slug> -o results` (add `-f` to refresh). Benchmarks (the collection of the five tasks) can only be created in the Kaggle web UI.
- The model proxy key is short-lived: on auth errors run `kaggle b auth -y`.
- Model quota is about $10/day and $100/month (per kaggle-benchmarks issue #76). The proxy refuses a call when its worst-case cost, based on the output-token cap, exceeds what is left. That is why every prompt passes `max_completion_tokens` (`MAX_OUTPUT_TOKENS` in the shared block). `count-in-context` is the expensive task. The largest list is 330 ids because at 1,100 ids the models spend 9k–17k reasoning tokens per row, which costs about $0.04 a row and runs past the cap (v1–v3 used 1,100; those results are kept as evidence, outside the headline).
- `python3 tasks/pending.py results` prints the `kaggle b t run` commands still needed for the lineup at each task's latest version, cheapest task first. Rows that error on quota or 429s are rerun; rows the model answered unreadably are `no-answer` and count as wrong.
- Every `push` also runs the task once on the default model (`gemini-3.7-flash`). If that run errors (for example on an empty quota), `kaggle b t status` shows the task as `Errored` and `kaggle b t run` submits nothing, only printing the stored traceback. Push again once the cause is fixed.
- Library reference: https://github.com/Kaggle/kaggle-benchmarks (branch `ci`).
