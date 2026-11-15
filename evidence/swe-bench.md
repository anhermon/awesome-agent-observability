# SWE-bench (SWE-bench/SWE-bench)

Version: `swebench` 5.0.2 from PyPI. Repo created 2023-10-04; last push 2026-09-18. MIT.

```bash
uv venv venv && . venv/bin/activate && uv pip install swebench
swebench eval verified --gold -i sympy__sympy-20590 --run-id validate-gold
```

The first try with the legacy `python -m swebench.harness.run_evaluation --dataset_name princeton-nlp/SWE-bench_Lite ...` form failed with `KeyError: 'image'` under 5.0.2; the v5 CLI above worked. A Hugging Face anonymous rate limit (HTTP 429) also blocked one attempt until the window reset.

```
Instances submitted: 1
Instances completed: 1
Instances resolved: 1
Instances with errors: 0
```

`logs/run_evaluation/validate-gold/gold/sympy__sympy-20590/report.json`:

```
"patch_successfully_applied": true,
"resolved": true,
"tests_status": {
  "FAIL_TO_PASS": {"success": ["test_immutable"], "failure": []},
  "PASS_TO_PASS": {"success": ["test__aresame", "test_structure", "test_equality", ...]}
```

Grading is deterministic: the reference patch is applied inside the per-instance Docker image and the held-out tests decide the result. No model was involved in this run.
