# Claude Code monitoring (OpenTelemetry export) and AI Observer

Claude Code 2.1.289 on a local model, exporting all three signals to AI Observer v0.7.0 (`tobilg/ai-observer`, MIT, repo created 2025-12-23, release 2026-11-06) running as the OTLP receiver.

```bash
gh release download v0.7.0 -R tobilg/ai-observer -p 'ai-observer-linux-amd64-v0.7.0.tar.gz' && tar xzf ai-observer-linux-amd64-v0.7.0.tar.gz
AI_OBSERVER_API_PORT=8091 AI_OBSERVER_OTLP_PORT=4328 AI_OBSERVER_DATABASE_PATH=$PWD/db.duckdb ./ai-observer serve &

env ANTHROPIC_BASE_URL=http://localhost:11434 ANTHROPIC_AUTH_TOKEN=ollama ANTHROPIC_API_KEY= \
  CLAUDE_CODE_ENABLE_TELEMETRY=1 CLAUDE_CODE_ENHANCED_TELEMETRY_BETA=1 \
  OTEL_METRICS_EXPORTER=otlp OTEL_LOGS_EXPORTER=otlp OTEL_TRACES_EXPORTER=otlp \
  OTEL_EXPORTER_OTLP_PROTOCOL=http/protobuf OTEL_EXPORTER_OTLP_ENDPOINT=http://127.0.0.1:4328 \
  OTEL_METRIC_EXPORT_INTERVAL=5000 OTEL_LOG_TOOL_DETAILS=1 \
  claude -p "Use the Bash tool to run: echo otel-ok > /tmp/cc-otel/out.txt . Then reply DONE." \
    --model qwen3.5:4b-fast --allowedTools Bash --debug-file /tmp/cc-otel/debug.log
```

Claude Code side (`--debug-file`):

```
[3P telemetry] isTelemetryEnabled=true (CLAUDE_CODE_ENABLE_TELEMETRY=1)
[3P telemetry] getOtlpReaders: types=["otlp"], interval=5000, protocol=http/protobuf, endpoint=http://127.0.0.1:4328
[3P telemetry] Created 1 log exporter(s)
```

The task ran (`/tmp/cc-otel/out.txt` contains `otel-ok`; stdout `DONE`). AI Observer side (`curl localhost:8091/api/...`):

```
/api/stats          {"traceCount":1,"spanCount":6,"logCount":11,"metricCount":12,"services":["claude-code"],"errorRate":0}
/api/metrics/names  ["claude_code.active_time.total","claude_code.cost.usage","claude_code.session.count","claude_code.token.usage"]
/api/traces         root span claude_code.interaction, 6 spans
/api/sessions       1 session, model qwen3.5:4b-fast
/api/logs           user_prompt
                    tool_decision  {tool_name: Bash, decision: accept, source: config}
                    tool_result    {tool_name: Bash, success: true, duration_ms: 99}
                    api_request    {input_tokens: 19323, output_tokens: 68, duration_ms: 270960, cost_usd: 0.078652}
                    api_request    {input_tokens: 19436, output_tokens: 18, duration_ms: 316079, cost_usd: 0.078104}
                    assistant_response
```

Things the run showed that matter when you use this for evals:

- `cost_usd` is Claude Code's own estimate at Claude prices. Against a local model behind `ANTHROPIC_BASE_URL` it reports about $0.08 per call for a call that cost nothing, so treat cost metrics from a non-Anthropic backend as wrong.
- Each turn re-sent about 19.3k input tokens with zero cache reads; Ollama does no prompt caching for this API, so per-turn latency on a CPU-bound 4B model was 4.5 to 5 minutes.
