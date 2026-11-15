# coder-eval (UiPath/coder_eval)

Checked 2026-11-15. Repo: Apache-2.0, created 2026-07-09 (18 weeks old), last push 2026-11-14, 160 stars. Installed `coder-eval` 0.12.18 with `uv tool install coder-eval`. Docs: `docs/` (task guide, A/B experiments, per-agent pages for Claude Code, Codex, OpenCode, Antigravity, Pi).

Claim: runs CLI coding agents on YAML-defined tasks and grades the resulting workspace and trajectory with deterministic criteria (`file_contains`, `run_command`, `skill_triggered`, and more) or LLM judges, with A/B variants across agents, models, and plugins/skills.

Setup: local only. Claude Code (the SDK-bundled CLI) is routed to Ollama `qwen3.5:4b-fast` through coder-eval's `litellm` backend, with `LITELLM_BASE_URL` pointed at Ollama and a dummy token. No provider key.

## 1. Agentless smoke task (deterministic, no model)

```
coder-eval run coder_eval-src/tasks/agentless_smoke_test.yaml
...
Task finished: status=SUCCESS duration=2.0s score=1.000 iterations=1
Results: 1/1 succeeded
```

## 2. Vanilla Claude Code, skill offered, graded on outcome and skill activation

`task.yaml`: agent `claude-code`, model `qwen3.5:4b-fast`, a local plugin offering skill `greeting-file`, and the prompt "Create a greeting file named hello.txt in the current directory." The criteria are `file_contains hello.txt "Hello, world!"` and `skill_triggered greeting-file`.

```
API_BACKEND=litellm LITELLM_BASE_URL=http://localhost:11434 LITELLM_AUTH_TOKEN=ollama \
LITELLM_MODEL=qwen3.5:4b-fast coder-eval run task.yaml
```

Output (task.log):

```
API routing: litellm (model: qwen3.5:4b-fast)
Criterion 'file_contains' FAILED (score=0.00, threshold=0.90): Includes: 0/1 found; Score: 0.00
Criterion 'skill_triggered' FAILED (score=0.00, threshold=0.90): observed='no', expected='yes' (skill_name='greeting-file')
Success criteria: 0/2 passed, weighted score: 0.000
Task finished: status=FAILURE duration=1328.2s score=0.000 iterations=1
```

experiment.md: 4 assistant turns, 49,681 tokens. task.json shows one `Write` tool call and no Skill call. The file the model wrote is "Hello! 👋 Welcome to this project directory...", so both criteria failed correctly: the model ignored the skill and wrote the wrong text. That was the small model's fault, not the harness's. The run took 22 min because another job on the box was using the same Ollama instance.

## 3. Positive control for the grader

```
coder-eval evaluate task-fileonly.yaml ./good     # ./good/hello.txt = "Hello, world!\n"
Passed: 1/1
All criteria passed! ✓
```

Not exercised: the Codex, OpenCode, Antigravity and Pi agents (no logins on this box), a positive `skill_triggered` (the model never loaded the skill), and LLM-judge criteria.
