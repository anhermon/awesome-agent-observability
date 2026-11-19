# Recipes added in this follow-up

> Note (2026-11-16): mcp-trace was archived on 2026-11-16 and is no longer on the list; this record is kept as the run log of that date.

The patterns themselves were exercised during the 2026-11-15 proof run unless noted. This file only records what was re-checked or newly confirmed for the list wording.

## Trace any CLI harness through a gateway

Proof run: LiteLLM (`callbacks: otel`) → OpenTelemetry Collector file exporter. Per-request `gen_ai.usage.input_tokens` / `output_tokens`, model, latency, and user-agent (`claude-cli/2.1.289`, opencode, pi) were recorded for vanilla Claude Code, OpenCode, and Pi pointed at the same proxy, with no harness-specific instrumentation. Claude Code's own OTel (`CLAUDE_CODE_ENABLE_TELEMETRY`) was sent to the same collector; on local models it reported a phantom cost (about $0.08/call) and, for some runs, only session-level metrics. Token counts on the Claude vs claude-lean rerun matched exactly between Claude Code `api_request` events and the LiteLLM spans (vanilla 13,708 input tokens / 189 s; lean 6,368 / 30 s).

## Run MCP Conformance through a proxy, including stdio

Proof run: official MCP Conformance `server` suite against the reference everything-server, direct vs through mcp-trace. Direct: 40/40 in 3 s. Through mcp-trace on main: 27/32 in 242 s (sampling/elicitation timeouts). Through the fixed proxy: 39/40 in 3 s. A stdio MCP server from a private harness was tested by pointing the suite at `mcp-trace --stdio` as the HTTP bridge; initialize, ping, and tools/list passed.

## Run a harness eval without Docker

Proof run: Inspect AI with a custom subprocess solver ran the same hidden-test coding task against OpenCode, Pi, and vanilla Claude Code on `qwen2.5:3b-instruct` via LiteLLM, scored with visible+hidden unittests and `model_graded_qa`. That task set **no sandbox**; its solver called Python `subprocess` directly on the host. Inspect also ships a built-in `local` sandbox (`inspect_ai.util.sandbox.local`, the host file system with no isolation). Dogfooding reproduced `sandbox="local"` on inspect_ai 0.3.290 with `sandbox().exec` in the solver and scorer and mockllm, accuracy 1.0. Harbor and Inspect SWE were already documented in #41 as container sandboxes.

## Promptfoo Node version

Proof run: the box default Node 22.20 failed to run Promptfoo; Node 24 worked. Re-checked 2026-11-15: `npm view promptfoo engines.node` for promptfoo **0.125.1** is `>=22.22.0`. The 0.120.19 tree used in #41 still declared `>=20.0.0`, so the current published requirement is the one the list should mention.
