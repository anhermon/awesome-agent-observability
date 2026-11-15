# ccusage (ccusage/ccusage)

Version 20.0.51 via `npx ccusage@latest`. Repo created 2025-05-29, last push 2026-11-15, 19.4k stars. GitHub reports the license as "Other"; the LICENSE file is MIT ("Copyright (c) 2025 ryoppippi").

```bash
npx -y ccusage@latest --help        # daily, weekly, monthly, session, blocks ("grouped by session billing blocks")
npx -y ccusage@latest daily --since 20261101 --offline
```

```
Coding (Agent) CLI Usage Report - Daily
Detected: Claude, OpenCode, pi-agent
│ 2026 11-15 │ - Claude │ - qwen3.5:4b… │ 19,278 │ 0 │ 0 │ 0 │ 19,278 │ $0.00 │
WARN  Missing embedded pricing for qwen3.5:4b-fast; cost excludes this model.
```

It read the box's Claude Code session logs, including runs against a local model.

Cross-check against Claude Code's own OpenTelemetry events for the same session (see [claude-code-monitoring.md](claude-code-monitoring.md)):

```bash
npx -y ccusage@latest session --since 20261115 --offline
```

```
│ 5e685e9… │ Claude │ - qwen3.5:4b… │ 38,732 │ 18 │ 0 │ 0 │ 38,750 │ $0.00 │
```

OTel `api_request` events for session 5e685e97 sum to 38,759 input and 86 output tokens. The transcript (`~/.claude/projects/-tmp-cc-otel/5e685e97….jsonl`) records the first turn only as streaming entries with `"output_tokens":0`, so ccusage, which reads the transcript, misses that turn's 68 output tokens. For exact token accounting of a run, prefer the OTel events; ccusage is accurate to what the transcript contains.
