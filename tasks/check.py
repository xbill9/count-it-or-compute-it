"""Local checks for the three count tasks. No model calls, no kaggle_benchmarks.

    python3 tasks/check.py
"""
import json
import pathlib

HERE = pathlib.Path(__file__).parent
FILES = ["count_in_context.py", "count_python_tool.py", "count_engine.py"]
START, END = "# ---- shared:", "# ---- end shared ----"


def shared_block(text: str) -> str:
    return text[text.index(START):text.index(END) + len(END)]


def cell_after(text: str, marker: str) -> str:
    """The code from `marker` up to the next `# %%` cell."""
    start = text.index(marker)
    end = text.find("\n# %%", start)
    return text[start:end if end != -1 else None]


texts = {f: (HERE / f).read_text() for f in FILES}
blocks = {f: shared_block(t) for f, t in texts.items()}
assert len(set(blocks.values())) == 1, "shared block differs between task files"

ns: dict = {}
exec(blocks[FILES[0]], ns)
exec(cell_after(texts["count_engine.py"], "def make_count_ids"), {**ns, "json": json}, ns)
parse_where, count_where, same_filter = ns["parse_where"], ns["count_where"], ns["same_filter"]
make_count_ids, classify, ROWS = ns["make_count_ids"], ns["classify"], ns["ROWS"]

# The original measurement: eleven ids, 10 or more, is 8.
assert count_where(ns["ORIGINAL_IDS"], "id >= 10")["count"] == 8
assert count_where(ns["ORIGINAL_IDS"], "id > 10")["count"] == 7
assert count_where(ns["ORIGINAL_IDS"], "")["count"] == 11

# Parser and filter equivalence.
assert parse_where("id between 5 and 9") == [(">=", 5), ("<=", 9)]
assert parse_where("ID>=3 AND id<7") == [(">=", 3), ("<", 7)]
assert same_filter("id >= 10", "id > 9", list(range(30)))
assert not same_filter("id >= 10", "id > 10", list(range(30)))
assert same_filter("id between 4 and 8", "id >= 4 and id <= 8", list(range(30)))
for bad in ["x >= 3", "id >= three", "id >= 3 or id < 1"]:
    try:
        parse_where(bad)
    except ValueError:
        pass
    else:
        raise AssertionError(f"parsed {bad!r}")

# Rows: every expected count comes from the canonical filter, and every
# threshold is an id in the data, so > and >= give different counts.
expected_rows = ns["ORIGINAL_REPEATS"] + len(ns["SIZES"]) * len(ns["PHRASINGS"]) * ns["SEEDS_PER_CELL"]
assert len(ROWS) == expected_rows, (len(ROWS), expected_rows)
assert len({r["case_id"] for r in ROWS}) == len(ROWS)
assert ROWS == ns["build_rows"](), "rows are not deterministic"
for r in ROWS:
    assert len(r["ids"]) == r["size"] == len(set(r["ids"]))
    assert r["expected"] == sum(1 for x in r["ids"] if ns["matches"](parse_where(r["truth_where"]), x))
    for _, v in parse_where(r["truth_where"]):
        assert v in r["ids"], (r["case_id"], v)

# Engine grading, on the original case.
ids, truth = ns["ORIGINAL_IDS"], "id >= 10"
def graded(wheres, answer):
    log: list = []
    tool = make_count_ids(ids, log)
    for w in wheres:
        json.loads(tool(w))
    return classify(answer, 8, truth, ids, log)

assert graded(["id >= 10"], 8) == "correct"
assert graded(["id > 9"], 8) == "correct"
assert graded(["id > 10"], 7) == "quoted-wrong-filter"
assert graded([""], 11) == "quoted-no-filter"
assert graded([], 8) == "correct-no-call"
assert graded([], 6) == "no-call"
assert graded(["id >= 10"], 6) == "not-quoted"
assert graded(["nonsense", "id >= 10"], 8) == "correct"

sizes = {}
for r in ROWS:
    sizes[r["size"]] = sizes.get(r["size"], 0) + 1
print(f"ok: {len(ROWS)} rows per task, by size {dict(sorted(sizes.items()))}")
