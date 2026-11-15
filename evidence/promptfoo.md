# Promptfoo (rewording)

Checked 2026-11-15 with promptfoo 0.120.19 from npm.

Claim in the rewritten line: runs test cases against agent providers, including the Claude Agent SDK and the OpenAI Codex SDK, and grades them with deterministic and model-graded assertions.

## Claude Agent SDK provider, deterministic assertions, local model

`promptfooconfig.yaml`:

```yaml
providers:
  - id: anthropic:claude-agent-sdk
    config:
      model: qwen3.5:4b-fast
      working_dir: ./work
      append_allowed_tools: ["Write", "Bash"]
tests:
  - vars: {task: "Reply with exactly the word PONG and nothing else."}
    assert:
      - {type: icontains, value: PONG}
      - {type: not-icontains, value: PING}
```

```
ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY=ollama-dummy \
  npx promptfoo eval -c promptfooconfig.yaml -o out.json --no-cache
...
Using unknown model for Claude Agent SDK: qwen3.5:4b-fast
Total Tokens: 12,311
  Eval: 12,311 (12,273 prompt, 38 completion)
Results: ✓ 1 passed, 0 failed, 0 errors (100%)
Duration: 10m 21s
```

`out.json`: provider `anthropic:claude-agent-sdk`, output `'PONG'`, assertions `icontains` passed and `not-icontains` passed.

A first attempt with `permission_mode: bypassPermissions` failed with: "permission_mode 'bypassPermissions' requires allow_dangerously_skip_permissions: true as a safety measure". That is a guard in the provider, not a bug.

## OpenAI Codex SDK provider

Not run, because Codex CLI is not installed or logged in on this box. The installed package ships the `openai:codex-sdk` provider (`dist/src/codex-sdk-*.js`), and the docs page https://www.promptfoo.dev/docs/providers/openai-codex-sdk/ returns 200.
