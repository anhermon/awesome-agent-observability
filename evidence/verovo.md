# Verovo, formerly AgentMeasure (roy-tong/Verovo)

`https://github.com/roy-tong/AgentMeasure` now answers `HTTP/2 301` with `location: https://github.com/roy-tong/Verovo`: the same repository, renamed (created 2026-08-16, 219 stars, MIT, last push 2026-11-15). Its README now leads with AI vendor-bill audits ("AI financial audit and task economics"), so the question was whether the session-log analysis the list described still exists.

```bash
uv venv verovo-venv && . verovo-venv/bin/activate && uv pip install "verovo==0.13.0"
verovo --help        # 45 subcommands; "check  check local agent logs (default)"
verovo check --help  # --runtime {auto,codex,claude}, --days, --all, --json, --export-otel ...
verovo check --runtime claude --all --no-history --html r.html --json r.json
```

```
reading 415 Claude Code session file(s)…
Verovo Healthcheck v0.13.0 · own-data · run #1
Coverage
  sessions 415 · files 415 · lines 7,893 · corrupt 0 (0.00%)
Activity
  turns 415 · command executions 0 (ok 0 · failed 0 · unknown 0)
  tokens: UNPROVABLE (missing in 415 session(s))
Checks
  [FINDING ] HC-01 — Duplicate records
         identical lines: 414; repeated call_ids: 0; ...
  [UNPROVABLE ] HC-02 — Retry amplification
  [UNPROVABLE ] HC-03 — Tool error runs
```

Decision: keep, with the link and name updated to Verovo and the description rewritten to say that `check` is one part of a tool that is now mostly about vendor bills. Threshold 1 (redirect to the same project) and threshold 6 (in scope: it still reads agent session logs) pass. Moved to Coding-agent telemetry.
