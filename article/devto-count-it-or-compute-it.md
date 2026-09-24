---
title: "Count It or Compute It: Given a Python Tool, a Model Stops Using It as the List Grows"
published: false
description: "A Kaggle benchmark that asks 14 models the same 68 counting questions five ways: count the ids in the prompt, use a Python tool, use it when told to, count the rows a query tool returns, or quote the exact count a query tool returns. Every expected answer is computed by code, and every filter a model sends is graded."
tags: devchallenge, kagglechallenge, ai, machinelearning
cover_image: https://raw.githubusercontent.com/xbill9/devto-kaggle/main/article/devto-cover.d50932c1.jpg
---

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23)*

Ask a model how many ids in a list are 10 or more, and the answer depends on who does the counting. This benchmark asks the same 68 questions five ways, from the model counting by reading to a query tool that returns the exact count.

With a Python tool available, Gemini 2.5 Flash used it on 20 of 26 questions about 11 ids, 2 of 21 about 110 ids and none of 21 about 1,100 ids. It skipped the tool where counting by eye fails. With the query tool, both Gemini Flash models answered all 68 questions correctly.

https://github.com/xbill9/devto-kaggle

PENDING: Kaggle benchmark link

---

#### What I Benchmarked

The itch is eleven ids.

```plaintext
0, 2, 3, 20, 21, 22, 23, 10, 11, 12, 13
```

How many of them are 10 or more? The answer is 8, and Gemini 2.5 Flash gives it every time, which says nothing about eleven hundred ids. Counting, filtering and comparing are work for code, and a model that does them by reading produces a confident number with no way to tell it is wrong.

So the benchmark scales the list and asks the same question five ways:

| Task | What the model gets | Who does the arithmetic |
|---|---|---|
| `count-in-context` | Every id in the prompt | The model, by reading |
| `count-python-tool` | The same prompt, plus `run_python` with `ids` already defined | The model decides |
| `count-python-told` | The same, plus one sentence: use the tool, do not count by reading | The model, if it follows the instruction |
| `count-rows-tool` | No ids; a `list_ids(where)` tool that returns the matching ids | The model counts the rows the tool returns |
| `count-engine` | No ids; a `count_ids(where)` tool that returns the exact count, minimum and maximum | The engine; the model writes the filter |

Each task asks 68 questions: lists of 11, 110 and 330 ids, seven English phrasings of the threshold, three seeds each, and the original eleven ids five times. Every expected answer is computed by code from a filter written beside the phrasing.

---

#### Models Tested

| Vendor | Models |
|---|---|
| Google | Gemini 3.5 Flash-Lite, Gemini 2.5 Flash, Gemini 3.7 Flash, Gemini 3.8 Flash |
| Anthropic | Claude Haiku 4.5, Claude Sonnet 5, Claude Opus 5 |
| OpenAI | GPT-5.4 nano, GPT-5.4 mini, GPT-6 Astra |
| Open weights | Gemma 4 26B A4B, gpt-oss-20b |
| Qwen | Qwen 3 Next 80B Instruct, Qwen 3 Next 80B Thinking |

The lineup takes a small, a mid-sized and a large model from each vendor Kaggle hosts, because the question is whether model size hides the counting problem or fixes it. Two open-weight models show whether the pattern holds outside the hosted frontier. Qwen 3 Next 80B runs twice, with reasoning off and on, to show whether thinking changes how often a model counts by eye instead of reaching for the tool.

---

#### Findings

PENDING: 14-model table, engine results beside Python tool and in-context.

#### 1. When the Engine Counts, the Answer Is Right

Both Gemini Flash models answered all 68 engine questions correctly, and every filter they sent selected the right ids. Writing `id >= 10` for "10 or more" is a task these models do reliably. Counting the matches is the task they do not.

PENDING: engine results for every model, and every wrong-filter or not-quoted answer listed with the filter sent.

#### 2. Given a Python Tool, a Model Stops Using It as the List Grows

On the 1,100-id version of the questions, Gemini 2.5 Flash used the Python tool less as the list grew, in both runs.

| Run | 11 ids | 110 ids | 1,100 ids |
|---|---|---|---|
| Run 1 | 25/26 | 2/21 | 0/17 |
| Run 2 | 20/26 | 2/21 | 0/21 |

When it used the tool it was right every time. When it skipped the tool it answered 30 of 46 questions wrong in run 2, including the original eleven ids twice, answered 7. Its Python-tool score, 38 of 68, came in below its in-context score of 49. Gemini 3.7 Flash used the tool on all 68 questions in every run and answered all 68 correctly.

PENDING: tool use by list size for every model at 11, 110 and 330 ids.

#### 3. Does Telling the Model to Use the Tool Fix It?

`count-python-told` adds one sentence to the Python-tool prompt and changes nothing else.

PENDING: tool use by size, told vs not told, for every model.

#### 4. A Tool That Returns Rows Leaves the Counting to the Model

`count-rows-tool` gets the filter right the same way the engine task does, then hands the model the matching ids to count. A wrong answer is either a wrong filter or a miscount of the right rows, and the benchmark records which.

PENDING: rows tool vs engine for every model, with miscounted-rows and wrong-filter counts.

#### 5. A Reasoning Budget Turns Counting Into Guessing

At 1,100 ids the model counts through the list in its reasoning: Gemini 2.5 Flash and 3.7 Flash spent an average of 9,755 to 19,897 output tokens per question on a prompt of about 6,360 tokens.

With output capped at 8,192 tokens, Gemini 3.7 Flash answered 1 of 21 questions about 1,100 ids correctly, against 19 and 15 of 21 without the cap. It kept answering when the budget ran out, so the cut-off shows up as a wrong number with no error. At 110 ids the cap made no difference: 21 of 21 in all three runs. The benchmark's largest list is 330 ids so that counting fits inside the cap.

#### What It Changed About How I Think About These Models

PENDING: after the 14-model run.

---

#### Compare and Contrast

| | In-context | Python tool | Engine |
|---|---|---|---|
| Who counts | The model, by reading | The model's code, if it writes any | The engine |
| What can go wrong | Miscounts that grow with the list | Skipping the tool | A wrong filter, quoted exactly |
| Cost per question at 1,100 ids, Gemini 3.7 Flash, run 1 | $0.0447 | $0.0150 | $0.0010 |
| Correct, Gemini 2.5 Flash, run 2 | 49/68 | 38/68 | 68/68 |
| Correct, Gemini 3.7 Flash, run 2 | 62/68 | 68/68 | 68/68 |

---

#### So, Which One?

PENDING: after the 14-model run.

---

#### What I'd Measure Next

- **Harder filters.** "At least 10 but under 20", "other than those under 10", "outside 5 to 9". Single thresholds were translated correctly every time; compound and negated ones are where a wrong filter with an exact count would show up.
- **Repeat runs per model.** Gemini 3.7 Flash scored 66 and then 62 of 68 on identical in-context questions, so differences smaller than that need repeats.

---

#### How It Works

**Step 1 — Generate every question in code.** Each phrasing has a filter that means the same thing, and the expected count comes from running it. Every threshold is an id in the list, so `>` and `>=` always give different answers.

| Phrasing | Example | Filter |
|---|---|---|
| or-more | 10 or more | `id >= 10` |
| at-least | at least 10 | `id >= 10` |
| no-less-than | no less than 10 | `id >= 10` |
| more-than | more than 10 | `id > 10` |
| under | under 10 | `id < 10` |
| at-most | at most 10 | `id <= 10` |
| between-inclusive | between 5 and 9 inclusive | `id >= 5 and id <= 9` |

```shell
python3 tasks/check.py
```

```plaintext
ok: 68 rows per task, by size {11: 26, 110: 21, 330: 21}
```

**Step 2 — Grade the filter the model sent.** A wrong filter returns an exact number with a cited source, which is harder to catch than a miscount. `count-engine` and `count-rows-tool` log every filter and checks it by the ids it selects, so `id > 9` counts as right for "10 or more". Each answer lands in one category: `correct`, `quoted-wrong-filter`, `quoted-no-filter` (the table's total), `not-quoted` (had the tool's number, answered something else) or `no-call`.

**Step 3 — Push and run on Kaggle.** Each file is one Kaggle task, and the task name must match the push slug.

```shell
kaggle b t push count-engine -f tasks/count_engine.py --wait
kaggle b t run count-engine -m gemini-2.5-flash -m claude-haiku-4-5-20251001 --wait
kaggle b t download count-engine -o results
```

PENDING: command output

**Step 4 — Score from the run files.** Each row's run file carries the dict the task returned: size, phrasing, answer, category and, for the engine task, every filter sent. Every score here comes from `summarize.py`.

```shell
python3 tasks/summarize.py results
```

PENDING: summary output

---

#### 🔎 Tip: Cap the Output to Stay Inside the Quota

Kaggle's model proxy reserves the worst-case cost of a call, based on the output-token limit, and refuses the call when that exceeds what is left of the day's quota. With no limit set, GPT-6 Astra reserved $6.40 per call and Claude Opus 5 $3.20. Passing a limit keeps the reservation to cents:

```python
llm.prompt(prompt, schema=int, extra_api_params={"max_completion_tokens": 8192})
```

The proxy accepted both `max_tokens` and `max_completion_tokens` on every model checked.

---

#### My Benchmark

- PENDING: Kaggle benchmark (the collection of the three tasks)
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-in-context
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-python-tool
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-engine

---

#### Summary

The goal of this article was to measure whether models count, compute or query when asked how many ids meet a threshold. The key to the solution was generating every question and every expected answer in code, and grading the filter a model sends as well as the number it quotes.

The results were:

- 🟢 PENDING
- ❌ PENDING
- ⚠️ PENDING

PENDING: scope paragraph (one run per model per task, temperature 0, output capped at 8,192 tokens, Kaggle's model proxy, dates).

The strategy for benchmarking counting across 14 models was validated with an incremental step by step approach.

---

#### References

- This benchmark's code: https://github.com/xbill9/devto-kaggle
- Kaggle Benchmarking Challenge: https://dev.to/challenges/kaggle-2026-09-23
- Kaggle Benchmarks: https://www.kaggle.com/benchmarks
- The tasks are built on Kaggle's `kaggle-benchmarks` library: https://github.com/Kaggle/kaggle-benchmarks
- Kaggle's benchmark-writing skill, used as the reference for the CLI workflow: https://github.com/Kaggle/kaggle-skills/blob/main/write-kaggle-benchmarks/SKILL.md
