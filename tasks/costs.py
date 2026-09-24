"""Cost and tokens per row by task, model, version and list size, from the run files.

    python3 tasks/costs.py [results]
"""
import collections
import json
import pathlib
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else "results")
cost: dict = collections.defaultdict(float)
n: collections.Counter = collections.Counter()
tok_in: collections.Counter = collections.Counter()
tok_out: collections.Counter = collections.Counter()
for f in ROOT.glob("*/*/*/*/*-row-run_param_id_*.result.json"):
    task, version, model = f.parts[-5], f.parts[-4], f.parts[-3]
    r = json.loads(f.read_text())
    agent = r.get("agent_result") or {}
    rewards = (r.get("verifier_result") or {}).get("rewards") or {}
    if agent.get("cost_usd") is None or "size" not in rewards:
        continue
    k = (task, model, int(version), int(rewards["size"]))
    cost[k] += agent["cost_usd"]
    n[k] += 1
    tok_in[k] += agent.get("n_input_tokens") or 0
    tok_out[k] += agent.get("n_output_tokens") or 0

print(f"{'task':<18} {'model':<28} ver  size  rows   $/row  in/row  out/row")
for k in sorted(cost):
    print(f"{k[0]:<18} {k[1]:<28} v{k[2]:<3} {k[3]:>4} {n[k]:>5}  {cost[k] / n[k]:.4f} {tok_in[k] // n[k]:>7} {tok_out[k] // n[k]:>8}")
