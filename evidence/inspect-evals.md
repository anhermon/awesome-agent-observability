# Inspect Evals (UKGovernmentBEIS/inspect_evals)

Installed from PyPI with `inspect-ai` 0.3.290. Repo created 2024-10-02, last push 2026-11-14, MIT.

```bash
uv venv inspect-venv && . inspect-venv/bin/activate && uv pip install inspect-ai inspect-swe inspect-evals openai anthropic
inspect eval inspect_evals/gsm8k --model mockllm/model --limit 3 --log-dir logs --display plain
```

```
gsm8k (3 samples): mockllm/model
dataset: openai/gsm8k
mockllm/model         6,536 tokens [I: 6,437, O: 99]
match
accuracy  0.000
```

`mockllm/model` returns a fixed string, so the deterministic `match` scorer marks all three wrong, as it should; the run proves the task downloads its dataset, builds prompts, and scores with no model key.
