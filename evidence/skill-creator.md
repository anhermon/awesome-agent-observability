# skill-creator (anthropics/skills, skills/skill-creator)

Checked 2026-11-15. Repo created 2025-09-22, last push 2026-11-14. GitHub reports no repo-level license, but `skills/skill-creator/LICENSE.txt` is Apache-2.0, so the entry says "Apache-2.0 per the skill's LICENSE.txt".

Claim: its scripts run `claude -p` on should-trigger and should-not-trigger queries to measure how often a skill's description makes Claude load it, and they aggregate with-skill and baseline runs into pass-rate, time, and token deltas.

Setup: vanilla Claude Code 2.1.289 pointed at local Ollama (`qwen3.5:4b-fast`), with a dummy auth token and no provider key. The demo skill is `demo-skill/conventional-commit/SKILL.md`. `evals.json` has one should-trigger and one should-not-trigger query.

## Validation (deterministic)

```
python3 -m scripts.quick_validate ../demo-skill/conventional-commit
Skill is valid!
```

## Trigger eval (`run_eval`, real `claude -p` runs)

```
env ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
  python3 -m scripts.run_eval --eval-set ../evals.json --skill-path ../demo-skill/conventional-commit \
  --num-workers 1 --runs-per-query 1 --timeout 1200 --model qwen3.5:4b-fast --verbose
Results: 1/2 passed
  [FAIL] rate=0/1 expected=True: write me a commit message for the change I just staged
  [PASS] rate=0/1 expected=False: what is the capital of France?
```

The JSON output includes `trigger_rate`, `triggers`, `runs`, and `pass` per query, plus a summary of `{"total": 2, "passed": 1, "failed": 1}`. The 4B local model never loaded the skill, so the should-trigger query failed and the should-not-trigger query passed. The script measured exactly what it claims to.

## Aggregation (`aggregate_benchmark`) on a fixture

Fixture: `eval-1/{with_skill,without_skill}/run-1/grading.json` plus `timing.json`.

```
python3 -m scripts.aggregate_benchmark bench --skill-name conventional-commit
Generated: bench/benchmark.json
Generated: bench/benchmark.md
  With Skill: 100.0% pass rate
  Without Skill: 0.0% pass rate
  Delta:         +1.00
```

Quirks seen: `benchmark.md` says "3 runs each per configuration" when there was 1. Tokens show 0 when `grading.json` carries timing, because `timing.json` tokens are read only when grading has no duration.
