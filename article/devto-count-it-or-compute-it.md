---
title: "Count It or Compute It: Given a Python Tool, a Model Stops Using It as the List Grows"
published: false
description: "A Kaggle benchmark that asks 14 models the same 68 counting questions three ways: count the ids in the prompt, use a Python tool, or quote an exact count from a query tool. Every expected answer is computed by code, and the query tool's filters are graded as well as its numbers."
tags: devchallenge, kagglechallenge, ai, machinelearning
cover_image: PENDING
---

*This is a submission for the [Kaggle Benchmarking Challenge](https://dev.to/challenges/kaggle-2026-09-23)*

This article provides a step by step guide to building a Kaggle benchmark that asks a model how many ids in a list meet a threshold, and runs it three ways: the model counts by reading, the model gets a Python tool, and the model gets a query tool that returns the exact count. Every expected answer is computed by code, and the query tool's filter is graded as well as the number the model quotes.

With a Python tool available, Gemini 2.5 Flash used it on 20 of 26 questions about 11 ids, 2 of 21 about 110 ids and none of 21 about 1,100 ids. It skipped the tool where counting by eye fails. With the query tool, both Gemini Flash models answered all 68 questions correctly.

https://github.com/xbill9/count-it-or-compute-it

PENDING: Kaggle benchmark link

---

#### What I Benchmarked

The question is the smallest one that exposes a model doing arithmetic it should hand to code: here is a list of ids, how many of them are 10 or more?

It started with eleven ids.

```plaintext
0, 2, 3, 20, 21, 22, 23, 10, 11, 12, 13
```

The answer is 8, and Gemini 2.5 Flash gives it every time, which says nothing about eleven hundred ids. The benchmark scales the list, varies the English used for the threshold, and asks the same question three ways, so the result shows where counting by reading breaks and whether a model reaches for a tool when it does.

---

#### At This Point You Should Have…

- A Kaggle account, with the Kaggle CLI installed and logged in: `kaggle auth login`
- The task files: `count_in_context.py`, `count_python_tool.py` and `count_engine.py`
- Python 3 for the local checks; they need no model calls and no `kaggle_benchmarks`

---

#### Step 1 — Generate Every Question in Code

Each question has an English phrase and a filter that means the same thing. The filter is the ground truth, and the expected count comes from running it.

| Phrasing | Example | Filter |
|---|---|---|
| or-more | 10 or more | `id >= 10` |
| at-least | at least 10 | `id >= 10` |
| no-less-than | no less than 10 | `id >= 10` |
| more-than | more than 10 | `id > 10` |
| under | under 10 | `id < 10` |
| at-most | at most 10 | `id <= 10` |
| between-inclusive | between 5 and 9 inclusive | `id >= 5 and id <= 9` |

Lists of 11, 110 and 330 ids each get all seven phrasings with three seeds, and the original eleven ids are asked five times. That is 68 questions per task. Every threshold is an id that appears in the list, so `>` and `>=` always give different answers.

```shell
python3 tasks/check.py
```

```plaintext
ok: 68 rows per task, by size {11: 26, 110: 21, 330: 21}
```

---

#### Step 2 — Ask the Same Question Three Ways

| Task | What the model gets | What it has to do |
|---|---|---|
| `count-in-context` | Every id in the prompt | Count them |
| `count-python-tool` | The same prompt, plus `run_python` with `ids` already defined | Decide whether to compute the count |
| `count-engine` | No ids; a `count_ids(where)` tool that returns the exact count, minimum and maximum | Write the filter and quote the number |

The first task is the diagnostic. The third is the setup this benchmark argues for: the engine does the arithmetic, and the model does the reasoning.

---

#### Step 3 — Grade the Filter the Model Sent

A wrong filter returns an exact number with a cited source, which is harder to catch than a miscount. So `count-engine` logs every filter and checks it against the question by the ids it selects: `id > 9` counts as right for "10 or more".

Each answer lands in one category:

| Category | Meaning |
|---|---|
| `correct` | Quoted the count of a right filter |
| `quoted-wrong-filter` | Quoted the exact count of a wrong filter, such as `id > 10` for "10 or more" |
| `quoted-no-filter` | Sent no filter and quoted the table's total |
| `not-quoted` | Had the tool's number and answered something else |
| `no-call` | Never used the tool |

---

#### Step 4 — Push and Run on Kaggle

Each file is one Kaggle task, and the task name must match the push slug.

```shell
kaggle b t push count-engine -f tasks/count_engine.py --wait
kaggle b t run count-engine -m gemini-2.5-flash -m claude-haiku-4-5-20251001 --wait
kaggle b t download count-engine -o results
```

PENDING: v4 command output

---

#### Step 5 — Score From the Run Files

Every score in this article is computed by `summarize.py` from the downloaded run files. Each row's run file carries the dict the task returned: size, phrasing, answer, category and, for the engine task, every filter sent.

```shell
python3 tasks/summarize.py results
```

PENDING: v4 summary output

---

#### Models Tested

| Vendor | Models |
|---|---|
| Google | Gemini 3.5 Flash-Lite, Gemini 2.5 Flash, Gemini 3.7 Flash, Gemini 3.8 Flash |
| Anthropic | Claude Haiku 4.5, Claude Sonnet 5, Claude Opus 5 |
| OpenAI | GPT-5.4 nano, GPT-5.4 mini, GPT-6 Astra |
| Open weights | Gemma 4 26B A4B, gpt-oss-20b |
| Qwen | Qwen 3 Next 80B Instruct, Qwen 3 Next 80B Thinking |

Each vendor contributes a small, a mid-sized and a large model where Kaggle hosts them. Qwen 3 Next 80B runs twice, with reasoning off and on, to show whether thinking changes how often the model counts by eye.

---

#### Findings

PENDING: 14-model table, engine results as the headline, Python tool and in-context beside it.

#### How Often Does the Model Reach for Python?

On the 1,100-id version of the questions, Gemini 2.5 Flash used the Python tool less as the list grew, in both runs.

| Run | 11 ids | 110 ids | 1,100 ids |
|---|---|---|---|
| Run 1 | 25/26 | 2/21 | 0/17 |
| Run 2 | 20/26 | 2/21 | 0/21 |

When it used the tool it was right every time. When it skipped the tool it answered 30 of 46 questions wrong in run 2, including the original eleven ids twice, answered 7. Gemini 3.7 Flash used the tool on all 68 questions in every run and answered all 68 correctly.

PENDING: the same table for every model at 11, 110 and 330 ids.

#### What a Reasoning Budget Does to Counting by Eye

At 1,100 ids the in-context task is expensive in a specific way. The prompt is about 6,360 tokens, and Gemini 2.5 Flash and 3.7 Flash then spend an average of 9,755 to 19,897 output tokens per question counting through the list.

With output capped at 8,192 tokens, Gemini 3.7 Flash answered 1 of 21 questions about 1,100 ids correctly, against 19 and 15 of 21 without the cap. It kept answering when the budget ran out, so the cut-off shows up as a wrong number with no error. At 110 ids the cap made no difference: 21 of 21 in all three runs.

That is why the benchmark's largest list is 330 ids, where counting fits inside the cap.

---

#### 🔎 Tip: Cap the Output to Stay Inside the Quota

Kaggle's model proxy reserves the worst-case cost of a call, based on the output-token limit, and refuses the call when that exceeds what is left of the day's quota. With no limit set, GPT-6 Astra reserved $6.40 per call and Claude Opus 5 $3.20. Passing a limit keeps the reservation to cents:

```python
llm.prompt(prompt, schema=int, extra_api_params={"max_completion_tokens": 8192})
```

The proxy accepted both `max_tokens` and `max_completion_tokens` on every model checked.

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

#### My Benchmark

- PENDING: Kaggle benchmark (the collection of the three tasks)
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-in-context
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-python-tool
- https://www.kaggle.com/benchmarks/tasks/xbillwork/count-engine

---

#### Summary

The goal of this article was to measure whether models count, compute or query when asked how many ids meet a threshold. The key to the solution was generating every question and every expected answer in code, and grading the filter a model sends as well as the number it quotes.

The results were:

🟢 PENDING
❌ PENDING
⚠️ PENDING

PENDING: scope paragraph (one run per model per task, temperature 0, output capped at 8,192 tokens, Kaggle's model proxy, dates).

The strategy for benchmarking counting across 14 models was validated with an incremental step by step approach.

---

#### References

- This benchmark's code: https://github.com/xbill9/count-it-or-compute-it
- Kaggle Benchmarking Challenge: https://dev.to/challenges/kaggle-2026-09-23
- Kaggle Benchmarks: https://www.kaggle.com/benchmarks
- kaggle-benchmarks Python library: https://github.com/Kaggle/kaggle-benchmarks
- Kaggle's benchmark-writing skill: https://github.com/Kaggle/kaggle-skills/blob/main/write-kaggle-benchmarks/SKILL.md
