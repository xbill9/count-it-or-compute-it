# %% [markdown]
# # Probe: which output-token cap does the model proxy accept?
#
# One tiny prompt per parameter name. The result records the answer or the
# exception, so a single run per model shows which name works.

# %%
import kaggle_benchmarks as kbench

# %%
@kbench.task(name="probe-max-tokens")
def probe_max_tokens(llm) -> dict:
    out = {}
    for param in ["max_tokens", "max_completion_tokens"]:
        try:
            with kbench.chats.new(param):
                answer = llm.prompt("Reply with the number 7.", schema=int,
                                    extra_api_params={param: 8192})
            out[param] = f"ok: {answer}"
        except Exception as e:
            out[param] = f"{type(e).__name__}: {str(e)[:300]}"
    print(out)
    return out


probe_max_tokens.run(kbench.llm)
