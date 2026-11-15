# Inspect SWE (meridianlabs-ai/inspect_swe)

Checked 2026-11-15. Repo: MIT, created 2025-08-29, last push 2026-11-15. Versions: inspect_ai 0.3.290, inspect_swe 0.3.0.

Claim: runs CLI coding agents (here vanilla Claude Code) as an Inspect solver inside a sandbox, then scores the result with any Inspect scorer.

Setup: local Docker sandbox (`python:3.12-slim`), model served by local Ollama (`qwen3.5:4b-fast`, 32k context). No provider API key. Inspect's model proxy hands Claude Code the Ollama model.

Task (`task.py`): one sample, solver `claude_code()`, a deterministic scorer that runs `cat /tmp/hello.txt` in the sandbox and compares it to the target.

```
inspect eval task.py --model ollama/qwen3.5:4b-fast
```

Output:

```
hello_cc (1 sample): ollama/qwen3.5:4b-fast
message_limit: 30, dataset: (samples)
total time:              0:07:10
ollama/qwen3.5:4b-fast   34,598 tokens [I: 34,474, CW: 0, CR: 0, O: 124]
file_check
accuracy    1.000
```

Log transcript (`inspect log dump`): the system prompt carries `cc_version=2.1.311.66b; cc_entrypoint=sdk-cli`, so the Claude Code CLI that inspect_swe installs into the sandbox ran. The model made one `Bash` tool call, and the score is `{'value': 'C', 'answer': 'Hello, world!'}`.

Note: a first run died with "Model proxy process exited unexpectedly ... Killed" because the box ran out of memory with other jobs running at the same time. Running it alone passed.
