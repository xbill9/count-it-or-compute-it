## Engine, rows tool and Python tool, every model with all three runs

| Model | Engine | Rows tool | Rows tool, 330 ids | Python tool | Python tool used, 110 / 330 ids |
|---|---|---|---|---|---|
| Gemini 3.7 Flash | 68/68 | 68/68 | 21/21 | 68/68 | 21/21 / 21/21 |
| Gemini 3.8 Flash | 68/68 | 68/68 | 21/21 | 68/68 | 21/21 / 21/21 |
| Gemma 4 26B A4B | 68/68 | 67/68 | 21/21 | 68/68 | 21/21 / 21/21 |
| Claude Sonnet 5 | 68/68 | 57/68 | 10/21 | 68/68 | 21/21 / 21/21 |
| Claude Opus 5 | 68/68 | 56/68 | 9/21 | 68/68 | 21/21 / 21/21 |
| gpt-oss-20b | 56/68 | 56/68 | 17/21 | 58/68 (1 errored) | 15/21 / 14/20 |
| Claude Haiku 4.5 | 68/68 | 52/68 | 5/21 | 68/68 | 21/21 / 21/21 |
| GPT-5.4 mini | 68/68 | 49/68 | 3/21 | 61/68 | 21/21 / 21/21 |
| Gemini 2.5 Flash | 68/68 | 43/68 | 2/21 | 36/68 (1 errored) | 3/21 / 0/20 |
| GPT-5.4 nano | 68/68 | 28/68 | 0/21 | 68/68 | 21/21 / 21/21 |

## Rows tool by list size

| Model | 11 ids | 110 ids | 330 ids |
|---|---|---|---|
| Gemini 3.7 Flash | 26/26 | 21/21 | 21/21 |
| Gemini 3.8 Flash | 26/26 | 21/21 | 21/21 |
| Gemma 4 26B A4B | 26/26 | 20/21 | 21/21 |
| Claude Sonnet 5 | 26/26 | 21/21 | 10/21 |
| Claude Opus 5 | 26/26 | 21/21 | 9/21 |
| gpt-oss-20b | 23/26 | 16/21 | 17/21 |
| Claude Haiku 4.5 | 26/26 | 21/21 | 5/21 |
| GPT-5.4 mini | 26/26 | 20/21 | 3/21 |
| Gemini 2.5 Flash | 26/26 | 15/21 | 2/21 |
| GPT-5.4 nano | 26/26 | 2/21 | 0/21 |

## Categories

- count-engine: correct 668, not-quoted 12
- count-rows-tool: correct 536, miscounted-rows 134, correct-no-filter 8, no-call 2
- count-python-tool: correct-tool 599, miscount-no-tool 33, correct-no-tool 32, wrong-tool 14

## Filters sent by rows-tool and engine answers that were wrong

- count-engine: 0 answers built on a wrong filter
- count-rows-tool: 0 answers built on a wrong filter

## Left out (no complete run of all three tasks)

- Gemini 3.5 Flash-Lite: complete in count-python-tool
- GPT-6 Astra: complete in none
- Qwen 3 Next 80B Instruct: complete in none
- Qwen 3 Next 80B Thinking: complete in count-python-tool
