---
name: kaggle-run
description: Push one or more of the five count tasks to Kaggle, run them against named models, download the results and report the scores computed from the run files. Use when asked to push, run, rerun or collect results for count-in-context, count-python-tool, count-python-told, count-rows-tool or count-engine.
---

Arguments: `$ARGUMENTS`: task slugs and model slugs, e.g. `count-engine gemini-2.5-flash claude-haiku-4-5`. With `pending`, download all five tasks and run what `python3 tasks/pending.py results` prints, one task at a time. With no tasks named, use all five. With no models named, ask.

Quota is about $10/day. When rows error with `exceeds your available quota`, stop for the day and rerun the pending pairs after the quota resets.

Pushing and running are pre-approved. Never create a venv or pip install anything.

1. `python3 tasks/check.py` must print `ok`. Stop and fix it if it fails.
2. Check every model slug against `kaggle b t models`. Report any that aren't on the list; don't guess a substitute.
3. For each task: `kaggle b t push <slug> -f tasks/<file>.py --wait`
   (slug → file: `count-in-context` → `count_in_context.py`, and likewise `count-python-tool`, `count-python-told`, `count-rows-tool`, `count-engine`).
4. `kaggle b t run <slug> -m <model> -m <model> --wait`: one `-m` per model.
5. `kaggle b t status <slug>`. For any errored run, `kaggle b t log <slug> -m <model>` and report the final exception line.
6. `kaggle b t download <slug> -o results -f`.
7. Run `python3 tasks/summarize.py results`. It reads each `*-row-run_param_id_*.run.json` (per-row dict at `results[0].dictResult`) and prints everything below. Extend the script rather than counting by hand. Report per task and model:
   - correct out of 68, plus the number of errored rows (errored rows count as wrong)
   - correct by size (11 / 110 / 330) and by phrasing
   - the category counts
   - for `count-engine` and `count-rows-tool`, list every `quoted-wrong-filter` and `quoted-no-filter` row with the filter sent and the true filter. Check the filter the model sent, not just the number it quoted.
8. Headline table: the engine-computed results. Treat in-context counting as the diagnostic.
