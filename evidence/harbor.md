# Harbor (harbor-framework/harbor)

Version: `harbor` 0.26.0 (`uv tool install harbor`). Repo created 2025-08-04; last push 2026-11-14. Apache-2.0.

Task: `examples/tasks/hello-world` from the repo (instruction: create `/app/hello.txt` with `Hello, world!`; verifier: `tests/test.sh` runs pytest and writes `reward.txt`).

## Built-in reference agents: the grader separates pass from fail

```bash
harbor run -p harbor-src/examples/tasks/hello-world -a oracle -o harbor-jobs --job-name oracle-hello -y
harbor run -p harbor-src/examples/tasks/hello-world -a nop    -o harbor-jobs --job-name nop-hello -y
```

```
oracle__adhoc  reward 1.0   (1 trial, 0 exceptions, 24s)
nop__adhoc     reward 0.0
```

## Vanilla Claude Code as the agent under test, on a local model

```bash
OLLAMA_LOCAL_TOKEN=ollama harbor run -p harbor-src/examples/tasks/hello-world \
  -a claude-code -m anthropic/qwen3.5:4b-fast \
  --base-url http://172.30.0.2:11434 --api-key-name OLLAMA_LOCAL_TOKEN \
  --agent-timeout-multiplier 20 -o harbor-jobs --job-name cc-ollama-hello2 -y
```

Harbor installed Claude Code in the task container, ran it headless, and graded the container state:

```
claude-code.txt: {"type":"tool_use","name":"Write","input":{"file_path":"/app/hello.txt","content":"Hello, world!\n"}}
verifier/test-stdout.txt:
  PASSED ../tests/test_state.py::test_hello_file_exists
  PASSED ../tests/test_state.py::test_hello_file_contents
result.json: "claude-code__qwen3.5:4b-fast__adhoc": mean 1.0, n_errors 0; n_input_tokens 22416, n_output_tokens 37
Total runtime: 19m 13s
```

The first attempt with the default 120 s agent timeout ended in `AgentTimeoutError` (reward 0.0): one Claude Code turn on a CPU-bound 4B model takes several minutes, since every turn sends about 19–22k tokens of system prompt and tools.

`harbor agent list` also lists `codex`, `gemini-cli`, `opencode`, `cursor-cli`, `goose`, `aider`, `openhands`, and others, and `harbor run` accepts `--skill` and `--mcp-config`. `harbor datasets list` includes Terminal-Bench. Those were not run here.
