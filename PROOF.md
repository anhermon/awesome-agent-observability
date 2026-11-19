# Proof run: using awesome-agent-observability to evaluate and observe Angel's own tools and agents

This file is the dated record of the 2026-11-15 proof rounds. The raw run artifacts are not in this repository; the numbers and caveats below are this written record. Every GitHub pull request cited here is an upstream source. **mcp-trace**, which appears in round 1, was later archived and removed from the list; see [DECLINED.md](DECLINED.md).

Run: 2026-11-15, 15:30–17:45 Asia/Jerusalem, on the shared Grok Bot box (8 CPUs, 15 GB RAM, partial GPU offload, shared with a parallel job).
Scope: only tools that are on the list (README `main` @ 599e0eb) or in the list PR being prepared in parallel (#41: Harbor, inspect_swe, MCP Conformance, MCP-Universe/MCPMark, skill-creator evals, Claude Code OTel, ccusage).
Auth: no provider API keys. `claude` and `codex` are **not logged in on the box**, and all of Angel's computers were offline, so every model call went to local Ollama models (qwen2.5:3b-instruct, granite4.2:3b, qwen3.5:4b-fast). Claude Code itself ran as the harness, pointed at Ollama through LiteLLM. That added up to 7 Claude Code CLI invocations (`claude -p`, all on local models) and 0 Codex calls.

Round 2 ran later the same day on Angel's Mac with his Claude Code and Codex subscriptions; that write-up is [Round 2 (Angel's Mac, real subscriptions)](#round-2-angels-mac-real-subscriptions--2026-11-15). It was written from existing artifacts only, with no further model calls.

## Headline

| # | Fix (where it lives) | Eval tool from the list | Before | After |
|---|---|---|---|---|
| 1 | **mcp-trace** Streamable HTTP proxy buffered server→client requests, so sampling/elicitation deadlocked → [mcp-trace#23](https://github.com/anhermon/mcp-trace/pull/23) | MCP Conformance (official suite) + MCP Inspector CLI + mcp-trace's own spans | 27 pass / 5 fail, 242 s (direct to server: 40/40, 3 s) | **39 pass / 1 fail, 3 s**; sampling/elicitation spans 60 s → 10–12 ms |
| 2 | **local-harness-router** sent system-scale coding prompts to a 3B model with `confidence: high` → [local-harness-router#12](https://github.com/anhermon/local-harness-router/pull/12) | Promptfoo (exec provider + deterministic JS asserts) | tuning set 10/14, holdout 5/9 | **14/14, holdout 7/9**, 0 false rejects; `npm test` 32 → 34 pass |
| 3 | **harness-arena** `--lean-prompt` did nothing for `claude` cells → [harness-arena#25](https://github.com/anhermon/harness-arena/pull/25) | LiteLLM proxy → OTel → OpenTelemetry Collector (token spans); Claude Code OTel | 13,497 input tokens per request for a one-line prompt | **2,883 (−79%)** with tool/MCP/skill trimming; **242 (−98%)** with the lean system prompt too |
| 4 | **cos-paperclip-bridge** skill description under-triggered (live file updated, backup kept) | skill-creator-style trigger evals (`query`/`should_trigger` evals.json) on a local router model through LiteLLM | 8/12, recall 2/6, 0 false triggers | **10/12, recall 4/6, 0 false triggers** |

Nothing was merged or force-pushed, and nothing went to `main`/`master`. All three PRs are open and waiting for Dogfooding review.

## Matrix: target × eval type × list tool × result

| Target | Eval type | List tool(s) used | Result |
|---|---|---|---|
| mcp-trace (MCP proxy) | Spec conformance, deterministic | **MCP Conformance** `server` suite against the suite's reference everything-server, direct vs through the proxy | main 665cf07: 27/32 checks in 242 s, with 4 timeouts (sampling, elicitation ×3) plus dns-rebinding. Fixed branch: 39/40 in 3 s |
| mcp-trace | Behavior (span correctness) | **mcp-trace** `--otel-stdout`, **MCP Inspector** CLI (`tools/list`, `tools/call`) | 14 tools listed, one call traced with the right tool name and client name. Bug: deadlocked calls were exported `status=Ok, duration=1m0s` while the client saw `-32001 Request timed out` |
| harness-arena MCP server (hand-rolled stdio JSON-RPC) | Conformance | **MCP Conformance** over **mcp-trace `--stdio`** as the HTTP bridge | initialize, ping, tools-list pass. `logging/setLevel` and the json-schema scenario fail, but neither is advertised (`capabilities: {tools:{}}`), so they don't apply |
| harness-arena | Regression (deterministic) | repo selftests (`test-runner.mjs`, `test-confinement.mjs`) | all checks pass (158 s); +1 new check in #25 |
| local-harness-router | Routing correctness (deterministic) | **Promptfoo** exec provider over `local-route --dry-run` | see Headline #2 |
| Agent harnesses: OpenCode, Pi, vanilla Claude Code (same local model) | Coding task with hidden tests (deterministic) **and** LLM-as-judge | **Inspect AI** task: solver shells out to each CLI; scorers = visible+hidden unittest + `model_graded_qa` judge (qwen2.5:3b via LiteLLM) | capable-setup T1 (slugify), qwen2.5:3b-instruct: OpenCode FAIL (429 s, Edit `oldString` mismatch), Pi FAIL (39 s, emitted the tool call as text), Claude Code FAIL (0.9 s: the request carried `thinking`, which qwen2.5 rejects; fixed with `MAX_THINKING_TOKENS=0`). The judge agreed with the hidden tests on 3/3 (all I). Claude vs claude-lean rerun: see "Harness rerun" |
| Claude Code harness overhead | Token/latency observability | **LiteLLM** (gateway) `callbacks: otel` → **OpenTelemetry Collector** file exporter; **Claude Code OTel** (`CLAUDE_CODE_ENABLE_TELEMETRY`) → same Collector | default 13,497 input tokens per request vs OpenCode ~6.6k, Pi ~1.5–2.3k, bare chat 13. See Headline #3 |
| Skills: cos-paperclip-bridge (user-created), adapter-mind (plugin) | Trigger eval (should / shouldn't trigger) | **skill-creator** evals.json schema and metric. Its `run_eval.py` needs a logged-in `claude -p`, so the same eval ran on a local router model through **LiteLLM** | cos-paperclip-bridge 8/12 → 10/12. adapter-mind 6/8 → 5/8 (its description didn't change; one query flipped under the changed catalog, which shows a 3B router's noise floor). granite4.2:3b returned empty answers, so that run is marked invalid (`skills/invalid/`) |
| Session archive (Claude Code, OpenCode, Pi, Grok Bot sessions on the box) | Session health / waste | **AgentsView** (`sync`, `health --json`, `export sessions`) | 933 sessions (claude 419, opencode 435, pi 64, grokbot 15). Median peak context on small one-shot tasks: Claude Code ~10.7k (19.3k on the parallel job's `echo` run), Pi 2.6k. Tool failures: opencode 20. Retries: pi 13. Grok Bot sessions all grade "A" because the transcripts carry no timestamps or tokens, so the health signals are blind there |
| Grok Bot (Cos) transcripts | Waste: oversized tool outputs, repeated calls | AgentsView ingests them (fork); the waste metrics come from a small script, `obs/grokbot_waste.py`, because no listed tool computes them for this format (gap) | 15 sessions, 229 tool calls, 12 duplicate calls (all in the first-run session), 533 KB of tool results. The **Morning digest** routine normally reads ~12 KB of tool output (median of 13 runs). 2 runs read 78 KB and 97 KB because they listed the **whole plugin catalog (283–287 plugins, ~68 KB)** to find the Calendar tools |

## Observability findings
- **One tap covers every harness.** LiteLLM's proxy with the `otel` callback, writing into the OTel Collector, gave per-request `gen_ai.usage.input_tokens/output_tokens`, model, latency and user-agent (`claude-cli/2.1.289`, opencode, pi) for all three harnesses, with no harness-specific setup. This is the most useful pattern the list enables, but no single entry says so.
- **Claude Code on a small local model:** 13.5k input tokens on the first request and 366 s for "pong". Most of that is tool schemas, MCP and skills, not the task. The parallel job measured ~19k uncached input tokens per turn and a phantom ~$0.078/call cost in Claude Code's own OTel, even on local models.
- **Runaway output:** with the lean system prompt, qwen2.5:3b produced 6,482 output tokens in 900 s against Claude Code's `max_tokens` 32000. Only the gateway spans caught this. Claude Code's own OTel exported just `session.count`/`active_time` metrics and `user_prompt`/`api_error` events for the local-model runs.
- **mcp-trace reports deadlocked calls as successes.** Its spans for the timed-out sampling/elicitation calls said `status=Ok, duration=1m0s`. Conformance, not tracing, found the bug. `clientName` is also proxy-global rather than per-session, so concurrent clients would be mislabeled (not fixed).
- **mcp-trace accepts any Host/Origin and listens on all interfaces.** Go rewrites `Host` to the target, so the upstream's DNS-rebinding guard never sees the attacker's Host. Left for a design decision (described in #23).
- **mcp-trace `dev` has a stray 20 MB `mcp-trace` binary committed** that `main` doesn't have (`git diff origin/main origin/dev`). It should be cleaned before the next promote.

## Inefficiencies → fixes → before/after
1. **mcp-trace deadlock** (code): `io.Copy` into an unflushed `ResponseWriter` → a flush-per-write writer on both forwarding paths. Conformance 27/5 in 242 s → 39/1 in 3 s. The new regression test fails on main and passes on the branch. `go test -race ./...` passes. PR #23.
2. **lhr misroutes** (code): a scope guard for code task types. Promptfoo 10/14 → 14/14 on the tuning set. The holdout was written before the fix and its markers were not fitted to it: 5/9 → 7/9. The two misses are kept honestly. PR #12.
3. **Claude Code prompt bloat in arena lean cells** (config/argv): 13,497 → 2,883 → 242 input tokens per request. PR #25. The runaway-output risk is noted there.
4. **cos-paperclip-bridge triggering** (skill description, live file): recall 2/6 → 4/6 with no new false triggers. Backup: `skills/SKILL.md.before`.
5. **Cos Morning digest catalog dump** (routine prompt, *not applied*): the routine belongs to the Cos bot, and editing another bot's routine needs Angel's go-ahead. The proposed wording is in "Proposed, not applied". It's a projection, not a re-run: from 2 of 13 runs at 78–97 KB down to the ~12 KB median, about 150 KB less tool output across those two runs.

## Harness rerun (claude vs claude-lean on T1, Inspect AI)
Inspect AI ran the same T1 task with `MAX_THINKING_TOKENS=0`, through LiteLLM, with Claude Code OTel on. Token counts from Claude Code's own `api_request` events and from the LiteLLM spans match exactly.

| Cell | Requests | Input tokens (total) | Wall | Claude Code OTel `cost_usd` | Hidden tests | Judge |
|---|---|---|---|---|---|---|
| claude (vanilla) | 1 | 13,708 | 189 s | $0.084 (phantom: the model is local) | FAIL | I |
| claude-lean (`--tools Read,Edit,Bash --strict-mcp-config --disable-slash-commands`) | 2 | 6,368 (3,099 + 3,269) | **30 s (−84%)** | $0.039 | FAIL | I |

Neither cell changed the file: qwen2.5:3b answered in prose instead of calling Edit. The pass rate is therefore 0/2 on both, and the model is too weak to say anything about quality. What the run does show is cost and latency: lean is 2.2× fewer input tokens per run and 6× faster to a final answer. The judge (`model_graded_qa`) agreed with the hidden tests on 5/5 harness runs in this proof (all incorrect). That is agreement on easy negatives only, so it doesn't validate the judge on positives.

## List gaps found while doing this
1. **No entry tells you how to trace any CLI harness through a gateway.** LiteLLM + OTel Collector did it, but neither line says so. The Gateways section should mention "point Claude Code/OpenCode/Pi at the gateway to get per-request token spans."
2. **skill-creator's trigger eval is hard-wired to a logged-in `claude -p`.** Nothing on the list runs a skill-trigger eval on another model or harness. I had to write a small runner (`skills/run_trigger_eval.py`) using its evals.json format.
3. **Nothing computes waste signals (oversized tool output, duplicate calls) for a custom agent transcript format.** AgentsView's `health` only grades sessions that have timestamps and tokens. Inspect Scout could scan transcripts, but it needs a model and an adapter. I wrote `obs/grokbot_waste.py`.
4. **No harness-agnostic eval runner that works without Docker or a cloud key.** Harbor and inspect_swe both need Docker sandboxes. On this box, Inspect with a custom subprocess solver was the practical route. A "local subprocess" recipe would help, or mention Inspect's `local` sandbox on its line.
5. **The MCP Conformance suite tests servers over HTTP only.** Testing a stdio server needed a bridge; mcp-trace `--stdio` worked, which the list could note. Most scenarios also assume the reference server's tool names, so third-party servers get many not-applicable failures, and the suite can't tell those apart from real failures without an expected-failures file.
6. **No listed tool flags a Streamable HTTP proxy that buffers SSE.** Only end-to-end conformance through the proxy found it. Worth a sentence in the MCP section: "run the conformance suite through any proxy or gateway you put in front of a server."
7. **Promptfoo needs Node ≥ 22.22.** The box default (22.20) failed, so I used a bundled Node 24. Small, but it blocks "npx promptfoo" on many machines.
8. **Grok Bot transcripts carry no tokens or latency at all.** No list tool can cost them. This gap is on the platform side, not the list's.

## Proposed, not applied (needs Angel)
- **Cos "Morning digest" routine**, replacing "Look up the current Google Calendar tools each run rather than assuming names" with: "Get the current Google Calendar tool schemas with GetDynamicTools on namespace `user-Google-calendar` (don't list or search the whole plugin catalog)."
- **mcp-trace:** validate Host/Origin on its own listener or bind to 127.0.0.1 by default; per-session client info; remove the stray binary from `dev`.
- **Arena local claude cells:** cap `CLAUDE_CODE_MAX_OUTPUT_TOKENS`.

## Files
- `mcp/`: conformance outputs (`direct.txt`, `proxy-*.txt`, `proxy-fixed.txt`, `out-*`), proxy span logs, arena-MCP conformance (`out-arena/`).
- `router/pf/`: Promptfoo configs, holdout, before/after JSON.
- `harness/`: Inspect task `harness_eval.py`, hidden tests, logs (`logs-before/`, `logs-claude/`), Claude Code overhead runs (`cc_overhead.sh`, `cc-*.json`).
- `skills/`: evals.json files, catalog, runner, before/after results.
- `obs/`: Collector and LiteLLM configs, `traces.jsonl` / `metrics.jsonl` / `logs.jsonl`, `llm_spans.py`, AgentsView exports, `grokbot_waste.py` and its output.

## Process cleanup (17:4x Asia/Jerusalem)
These were stopped: LiteLLM proxy, OpenTelemetry Collector, the AgentsView daemon (started by `agentsview projects`), the MCP reference server, both mcp-trace proxies, the arena MCP bridge, and the parallel job's AI Observer (8091/4328) and MCP server-everything (3001). The conformance reference server on 3002 was already gone. Afterwards, `pgrep -af "litellm|otelcol|agentsview|ai-observer|server-everything|everything-server|mcp-trace|conformance|inspect eval|claude -p|opencode run|pi -p"` returned nothing, `docker ps` was empty, and none of ports 3001/3002/3311/4000/4317/4318/4328/8080/8091/8311–8313 were listening. dockerd and `ollama serve` (pid 1623698, started by the parallel job and not by this run) were left running as instructed.

## Round 2 (Angel's Mac, real subscriptions) — 2026-11-15

Offline write-up only. Angel's instruction was "Don't spend more calls; write up round 2 from what we have." No model calls, no subscription use, and no access to the Mac went into this section. Figures come from the artifacts under `round2/` plus local re-runs of `bundle/grade.sh` on the box (no model). Claude Code costs below are the CLI's **list-price** `costUSD` / `total_cost_usd` (`costBasis: list` in the overhead JSON). They are not a subscription invoice.

Run window, Asia/Jerusalem: phase 1 19:24:32–19:59:23 (`round2/p1/out-p1.log`), phase 2 20:02:03–20:17:04 (`round2/p2/out-p2.log`). First recorded call 19:24:33, last `take()` 20:16:53 (`round2/p2/out/calls.jsonl`). The Mac went offline around 20:26 while a planned third phase (`round2/bundle/plan3.json`, `round2/bundle-p3.tgz`) was packed but not started.

Host from Claude Code OTel resource attributes (`round2/p2/out/obs-p2/logs.jsonl`): darwin arm64, `os.version` 25.3.0, `claude-code` 2.1.325. Model for Claude Code cells: `claude-fable-5-2` (`round2/p1/out/model.txt`; also every `modelUsage` block and every OTel `api_request`). Phase 2 additionally passed `--settings {"model": "fable", "effortLevel": "high"}` from the user's `~/.claude/settings.json` (`round2/p2/out/runs/p2-cc-lean2-t1-r1/meta.json`).

### What ran

Phase 1 (`round2/bundle/plan1.json`, runner `round2/bundle-p1.tgz`): four one-shot Claude Code overhead "pong" probes, then a harness matrix, then LLM-judge v1, then skill-trigger evals (before).

| Cell | Argv extras | Tasks × reps | Planned model / notes |
|---|---|---|---|
| `cc` | none (vanilla `claude -p`) | T1, T2, T3 × 2 | `claude-fable-5-2`. T2 and T3 also spawned `savvy-flow` subagents on `claude-sonnet-5-5` (`round2/p2/out/analysis-runs.json`, OTel `skill_activated`) |
| `cc-lean` | `--tools Read,Edit,Write,Bash --strict-mcp-config --disable-slash-commands` | T1, T2, T3 × 2 | `claude-fable-5-2` only |
| `codex` | `codex exec --json -s workspace-write --skip-git-repo-check` | T1, T2, T3 × 2 | **No model flag is passed** (`bundle/run.py` `harness_cmd`). Usage is recorded as `codex default`. The plan's `codex_model: gpt-6.1-sol` is used only when choosing an OpenCode model |
| `gemini` | `gemini -p --yolo --skip-trust --output-format json` | T1, T2, T3 × 1 | Did not authenticate (see below) |
| `opencode` | `opencode run --format json -m openai/gpt-6.1-sol` | T1, T2, T3 × 1 | Model chosen in `round2/p1/out/opencode-models.txt`; every run failed with `Token refresh failed: 401` |

Tasks (prompts in `plan1.json` / `plan2.json`): T1 fix `src/textkit/slug.py`; T2 implement a small reportkit from `SPEC.md`; T3 implement `src/limiter/bucket.py`, write `REVIEW.md` from an adversarial review, and leave `tests/` untouched. Hidden tests plus that process check are in `round2/bundle/grade.sh` and `round2/bundle/fixtures/score.sh`.

Phase 2 (`round2/bundle/plan2.json`, runner `round2/bundle-p2.tgz`): no overhead probes. New cells, both lean plus `--setting-sources project` and the user's model/effort settings:

| Cell | Tasks × reps | Extra |
|---|---|---|
| `cc-lean2` | T1, T2, T3 × 2 | same tool trim as `cc-lean`, plus `--setting-sources project` and `effortLevel: high` |
| `cc-lean2-p` | T3 × 2 only | same argv; T3 prompt also says do not add/edit/delete anything under `tests/` and to stop after a review round with no valid issues (`plan2.json` `prompt_overrides`) |

Then judge v2 over phase-1 and phase-2 diffs (excluding `gemini` / `opencode`) plus 8 fixture seeds, then skill-trigger evals (after) with the wording in `round2/desc-after-r2.txt`.

`traces.jsonl` is empty in both phases (0 bytes). The Collector is configured to export traces (`round2/bundle/otelcol.yaml`), but Claude Code was started with `OTEL_METRICS_EXPORTER` and `OTEL_LOGS_EXPORTER` only (`run.py` `cc_env`), so token and latency figures below come from log `api_request` events and from each run's `stdout` / `analysis-runs.json`.

List tools actually used in this round: **Claude Code OTel** into an **OpenTelemetry Collector** file exporter (tokens, list cost, latency, `api_error`, tool and skill events); **skill-creator** `scripts.run_eval` for the trigger evals; Claude Code's own JSON usage (`costBasis: list`, ccusage-adjacent). Hidden tests and the LLM judge were a custom `grade.sh` / `run.py` harness, not Inspect AI (round 1 used Inspect). MCP Conformance, Promptfoo, and the LiteLLM gateway path from round 1 were not re-run.

### Hidden-test pass rates

Authoritative grades are the box re-grades in `round2/p2/out/analysis-runs.json` (script `round2/analysis/analyze.py`, which applies each `diff.patch` to a fresh fixture and runs `bundle/grade.sh`). I re-ran `grade.sh` on the box this write-up for the T3 disagreements and for all 8 seeds; the saved box grades matched.

**Phase 1, box grades** (24 runs):

| Cell | T1 | T2 | T3 | All |
|---|---|---|---|---|
| `cc` | 2/2 | 2/2 | 1/2 | 5/6 |
| `cc-lean` | 2/2 | 2/2 | 0/2 | 4/6 |
| `codex` | 2/2 | 2/2 | 2/2 | 6/6 |
| `gemini` | 0/1 | 0/1 | 0/1 | 0/3 |
| `opencode` | 0/1 | 0/1 | 0/1 | 0/3 |

T3 box failures that are about the agent's change, not the scorer: `p1-cc-lean-t3-r1` (timeout 900 s, `REVIEW.md` missing, `TESTS-MODIFIED:tests/test_review.py`), `p1-cc-lean-t3-r2` (`TESTS-MODIFIED:tests/test_edge.py`), `p1-cc-t3-r2` (timeout 900 s, `TESTS-MODIFIED:tests/test_spec.py`). Visible and hidden tests were OK on those diffs once re-graded; they fail the frozen-`tests/` and/or `REVIEW.md` checks. `p1-cc-t3-r1` and both Codex T3 runs are box **PASS**.

**Mac vs box on T3.** Every phase-1 T3 Mac grade, including the empty-diff Gemini and OpenCode runs, ends `hidden:[ModuleNotFoundError: No module named 'bpy']` (`round2/p1/out/runs/*/meta.json`, `out-p1.log`). That is a scorer-environment bug, not the agents' code. Phase 1's `score.sh` copied the hidden test to `/tmp/test_hidden_$$.py`, which puts `/tmp` on `sys.path`. Phase 2 changed this to a fresh `mktemp -d` (`diff` of `bundle-p1.tgz` vs `bundle-p2.tgz` `fixtures/score.sh`). After that change, completed T3 hidden scores are `OK` or, on empty trees, `No module named 'limiter.bucket'`. So Mac `truth_pass` for phase-1 T3, including `seed-t3-ref`, is not reliable. Box re-grade of `bundle/seeds/t3-ref` is PASS.

Gemini 0/3: stderr `IneligibleTierError` / `UNSUPPORTED_CLIENT`, "This client is no longer supported for Gemini Code Assist for individuals… migrate to the Antigravity suite" (`round2/p1/out/runs/p1-gemini-t1-r1/stderr.txt`). Empty diffs, ~3.0–3.5 s, rc 1. This is not a quality result.

OpenCode 0/3: stdout `Token refresh failed: 401` (`round2/p1/out/runs/p1-opencode-t1-r1/stdout.txt`). Empty diffs, ~3.2–3.6 s, rc 1. Also not a quality result.

**Phase 2, box grades** (8 runs):

| Cell | T1 | T2 | T3 | All |
|---|---|---|---|---|
| `cc-lean2` | 1/2 | 1/2 | 0/2 | 2/6 |
| `cc-lean2-p` | — | — | 1/2 | 1/2 |

The four second-rep runs (`p2-cc-lean2-t1-r2`, `t2-r2`, `t3-r2`, `p2-cc-lean2-p-t3-r2`) are not real attempts. Each `stdout.txt` has `terminal_reason: "api_error"`, `api_error_status: 429`, `api_error: "usage_limit_reached"`, `result: "You've hit your 5-hour limit · resets 10:20pm (Asia/Jerusalem)"`, all token fields 0, `duration_ms` 530–634, wall 1.4–1.5 s. That is **4** such runs.

The four first-rep runs did real work. `t1-r1` and `t2-r1` PASS. `t3-r1` has hidden tests OK but fails `REVIEW.md:MISSING`. `p-t3-r1` is a full PASS (hidden OK, `REVIEW.md:yes`, tests untouched). Both T3 first-reps also ended with the same 5-hour-limit 429 after that work (`is_error: true` in `p2-cc-lean2-t3-r1/stdout.txt` and `p2-cc-lean2-p-t3-r1/stdout.txt`; one OTel `api_error` each). Counting only those completed first reps: `cc-lean2` 2/3, `cc-lean2-p` 1/1. Phase-2 pass rates over all 8 cells are not a fair before/after against phase 1.

### LLM-judge agreement

**Judge v1** (`round2/p1/out/judge-p1.jsonl`, prompt `round2/bundle/judge-v1.txt`, 32 items: 24 runs + 8 seeds). Every item parsed as `CORRECT` or `INCORRECT` (19 / 13). No `PARSE_ERROR`. All rc 0.

- Versus the Mac `truth_pass` stored in the JSONL: 27/32 agree (TP 14, TN 13, FP 5, FN 0). All five disagreements are T3 false positives, whose Mac truth is contaminated by the `bpy` hidden-test failure.
- Versus box grades on the 24 harness runs (`analysis-runs.json`): 22/24 agree (TP 15, TN 7, FP 2). The two remaining false positives are `p1-cc-lean-t3-r2` and `p1-cc-t3-r2`, which edited `tests/`. Judge v1 asked not to "modify or delete anything under tests/" but still called those diffs `CORRECT`.
- Versus box `grade.sh` on the 8 seeds: 7/8. The miss is `seed-t3-ref` (box PASS, judge `INCORRECT`). The judge's reason complains that `refill_per_sec` accepts NaN because it only checks `< 0` — a robustness nit the v2 prompt later tells the judge not to fail on. Combined with the runs: **29/32** against box truth.

**Judge v2** (`round2/p2/out/judge-p2.jsonl`, prompt `round2/bundle/judge-v2.txt`): **34/34 `PARSE_ERROR`**. Every record has rc 1, 0 input and 0 output tokens, wall 1.2–1.8 s, and `result` exactly `You've hit your 5-hour limit · resets 10:20pm (Asia/Jerusalem)`. Matching OTel: each of the 34 `p2-judge-v2-*` tags has a user_prompt and an `api_error` (status 429, "This request would exceed your account's rate limit. Please try again later.") and **no** `api_request`. The v2 prompt was never answered. This is not a JSON-schema or prompt-format failure, and it does not evaluate v2's tighter `tests/` and "don't fail on NaN" rules.

The p2 runner (`bundle-p2.tgz` `run.py`) has no usage-limit detector. It classifies any reply without `"grade": "CORRECT"|"INCORRECT"` as `PARSE_ERROR`, so all 34 limit messages were stored that way and the remaining judge jobs were not cancelled. A circuit breaker (`limited()`, `VOID_LIMIT`, skip later stages) was added later in `round2/bundle/run.py` / `bundle-p3.tgz` (20:25 Asia/Jerusalem), after phase 2 had finished. It did not protect this run. I did not edit the historical p1/p2 runners.

### Claude Code phase-2 `api_error` / zero-token runs

- **4** runs ended `terminal_reason: "api_error"` with zero tokens, all second reps, all the same 429 `usage_limit_reached` / 5-hour limit message, listed above. Evidence: each run's `stdout.txt` under `round2/p2/out/runs/`.
- **2** further completed T3 first-reps (`p2-cc-lean2-t3-r1`, `p2-cc-lean2-p-t3-r1`) hit the same 429 at the end of a long session (789.6 s and 838.8 s, non-zero usage) and still wrote diffs that could be graded.
- **34** judge-v2 calls hit the same limit with zero tokens (previous section).
- Those 4 + 2 + 34 = **40** OTel `api_error` events in `round2/p2/out/obs-p2/logs.jsonl`, and there are no leftover untagged `api_error`s. The message in the CLI result is the 5-hour usage cap resetting at 22:20 Asia/Jerusalem; OTel's wording is the generic 429 rate-limit string. I am not treating those as two different causes.

### Tokens and latency

Overhead, one "Reply with exactly: pong" turn, four argv variants in this order: `cc`, `cc-src`, `cc-lean`, `cc-lean-src` (`plan1.json` `overhead_order`). Prompt size = uncached input + cache read + cache write on the single `api_request` (OTel `round2/p1/out/obs-p1/logs.jsonl`, also `round2/p1/out/overhead/*.json`):

| Variant | Prompt tokens | Cache write / read | Output | List cost | API ms | Wall s (`out-p1.log`) |
|---|---|---|---|---|---|---|
| `cc` (vanilla, cold: cache read 0) | 50,003 | 50,001 / 0 | 4 | $0.800 | 956 | 7.4 |
| `cc-src` (`--setting-sources project`) | 19,207 | 7,862 / 11,343 | 4 | $0.128 | 844 | 2.1 |
| `cc-lean` (tool/MCP/slash trim, cold) | 22,431 | 22,429 / 0 | 4 | $0.359 | 778 | 7.1 |
| `cc-lean-src` (lean + project sources) | 7,467 | 3,879 / 3,586 | 4 | $0.063 | 1,157 | 2.3 |

Same split on the first API request of a real T1 or T2 run (OTel): vanilla T1 r1 50,174; `cc-lean` T1 r1 22,648. The `cc-lean2` T1 r1 first request is 7,686, and T2 first requests are 50,186 / 22,657 / 7,698 — but the lean2 first requests are **not cold** (3,586 cache-read tokens, the same cache leftover seen on the lean-src pong). The cold comparison remains the overhead pair: 50,003 vs 22,431.

Per-run totals, box metadata in `analysis-runs.json` except the two timeouts, whose `modelUsage` is missing from stdout and whose tokens come from OTel `api_request` sums:

| Set | Uncached in | Cache read | Cache write | Output | List cost | Wall s (sum) |
|---|---|---|---|---|---|---|
| p1 `cc` (6 runs; T3 r2 timeout from OTel) | 237 | 7,721,419 | 811,165 | 160,013 | $11.028 (T3 r2 $2.689 of that) | 1,925.4 |
| p1 `cc-lean` (6 runs; T3 r1 timeout from OTel) | 76 | 1,114,531 | 145,482 | 53,128 | $4.676 (T3 r1 $1.977 of that) | 1,470.2 |
| p1 `codex` (6 runs; Codex JSON usage, no list cost parsed) | 143,365 | 2,685,952 | 0 | 25,313 | — | 870.7 |
| p2 `cc-lean2` completed r1 only (3 runs) | 30 | 189,281 | 61,573 | 40,570 | $2.646 | 862.4 |
| p2 `cc-lean2-p` completed r1 only (T3) | 18 | 182,333 | 45,417 | 37,519 | $2.264 | 838.8 |

Notable single runs (`analysis-runs.json` unless noted): vanilla T2 r1 / r2 cost $1.510 / $1.677, 62.0 / 82.3 s, models `claude-fable-5-2+claude-sonnet-5-5`, subagents `savvy-flow:savvy-light` × 2. Vanilla T3 r1 cost $3.661, 854.5 s, 83,038 output tokens, `savvy-flow:savvy-careful` × 1, 24 of 38 API requests on `claude-sonnet-5-5` (OTel). Lean T2 is cheaper and faster at the same 2/2 box pass ($0.431 / $0.429, 36.6 / 35.0 s) with no subagent. Judge v1: 32 calls, list cost $2.541, 274,376 API ms, 299.2 s wall (`judge-p1.jsonl`). Judge v2: $0 and 0 tokens (`judge-p2.jsonl`).

Why vanilla is large, from the same OTel log: a vanilla overhead request loads 26 plugins, 42 hook registrations, and 25 MCP server connections. `cc-lean` alone still loads 25 plugins and 42 hooks; it only drops MCP connections to 7, which is the 50,003 → 22,431 cut. The drop to 4 plugins and 0 hook events is `--setting-sources project` (`cc-src` and `cc-lean-src`); `cc-lean-src` also has no `mcp_server_connection` events. Vanilla T2/T3 each emit `skill_activated` for `savvy-flow:savvy-flow` (plugin). Lean cells do not.

Codex has no Claude Code OTel and does not name a model in its JSONL. Wall and tokens above are from `turn.completed.usage` as parsed into `analysis-runs.json` (uncached in = `input_tokens - cached_input_tokens`).

### Skill trigger evals, before vs after

Results: `round2/p1/out/skills/p1-*-before.json` and `round2/p2/out/skills/p2-*-after.json`. Logs: p1 before 19:59:01 cos-paperclip-bridge **11/12** (35.9 s) and 19:59:19 adapter-mind **5/8** (17.4 s); p2 after 20:16:53 **6/12** (9.0 s) and 20:17:00 **4/8** (6.3 s).

What `round2/desc-after-r2.txt` changed, versus the "before" `description` fields:

- **cos-paperclip-bridge:** one clause. Before: "checking whether Claude replied". After: "checking whether Claude replied or answered (on a cos-bridge issue or thread)". The only before miss was the should-trigger query "Did Claude reply on the cos-bridge thread about the hosting study?" (trigger_rate 0). All other 11 before queries passed (5/6 recall, 0 false triggers).
- **adapter-mind:** the before description was the plugin default ("Use when a task may have prior context, when the user asks what was decided or done before, or when finishing work worth keeping."). After is the longer wording with examples ("what did we decide about X", "have we already tried Y", "did we do this last time"), an explicit remember/save clause, and "Not for email, calendar, Dropbox files, or GitHub work." Before: 1/4 recall (only "Save the key findings from this study to my Adapter workspace" triggered), 0 false triggers, 5/8. The after description was proposed only for the eval (`plan2.json`); it was not applied to the live plugin skill.

The after scores are **not** a valid before/after of that wording. Every after query has `trigger_rate: 0`. All six / four should-not-trigger cases therefore "pass", and all should-trigger cases fail — including the one adapter-mind query that triggered in phase 1. The after runs also started immediately after judge v2 had already hit the 5-hour limit, and they finished in 9.0 s and 6.3 s versus 35.9 s and 17.4 s before. Skill evals were not given `cc_env()`, so they have no OTel tags; I cannot show a 429 for them the way I can for the judge. The all-zero trigger pattern plus the timing is enough to treat 6/12 and 4/8 as inconclusive, not as a regression caused by the new descriptions. Phase 2's runner also did not stop the skill stage when the limit was already hit (that skip exists only in the later p3 `run.py`).

### Inefficiencies — supported vs inconclusive

Supported by this run's data:

1. **Vanilla Claude Code prompt bloat.** A one-line "pong" is 50,003 prompt tokens vanilla vs 22,431 lean vs 7,467 lean+`--setting-sources project`. The same ratio appears on the first request of T1/T2. The extra tokens coincide with loading the full plugin/hook/MCP surface. This is the same class of finding as round 1 on local models, now measured on the subscription CLI with `claude-fable-5-2`.
2. **Vanilla cells pull in `savvy-flow` and Sonnet subagents on T2/T3**, which lean cells do not. On T2 that did not improve the hidden-test result (both 2/2) and it did increase cost and wall time (about $1.51–$1.68 / 62–82 s vs $0.43 / 35–37 s).
3. **T3 process discipline is the hard part for lean Claude Code.** Hidden tests can be OK while the run still fails for a missing `REVIEW.md` or a modified file under `tests/`. The phase-2 prompt override that forbids touching `tests/` and says to stop after a clean review is the only lean T3 box PASS (`p2-cc-lean2-p-t3-r1`). One data point, but it is a real pass, not a scorer artifact.
4. **The harness did not stop on a subscription cap.** After the 5-hour limit, phase 2 still launched 4 zero-token harness reps, 34 judge calls, and 20 skill-trigger calls (58 of the 142 total). Those calls produced no usable grades.

Inconclusive or not a quality comparison:

- Phase-2 vs phase-1 pass rates as a whole (half of the phase-2 cells never started).
- Judge v2 vs hidden tests (never answered).
- Skill-trigger after vs before (all-zero triggers under a cap).
- Gemini and OpenCode 0/3 (authentication, empty diffs).
- Whether `effortLevel: high` helped or hurt; it is confounded with `--setting-sources project` and with the cap.
- Codex vs Claude Code cost (no comparable list-cost field in the Codex JSON).

### Calls used: 142

`round2/p2/out/calls.jsonl` has 142 lines; `out-p2.log` ends `CALLS phase 62 total 142`. Phase 1 used 80 (`out-p1.log`, `round2/p1/out/calls.jsonl`). Breakdown:

| Phase | overhead | harness | judge | skill-trigger | Total |
|---|---|---|---|---|---|
| p1 | 4 | 24 | 32 | 20 | 80 |
| p2 | 0 | 8 | 34 | 20 | 62 |
| Total | 4 | 32 | 66 | 40 | **142** |

The cap was 150 for phases 1–2 (`plan1.json` / `plan2.json` `max_calls_total`). Phase 3 was planned at a raised cap of 200 and was not run.

### Not verified

- Judge v2 agreement with hidden tests, and whether its tighter `tests/` / NaN wording would have caught the two v1 false positives or graded `seed-t3-ref` correctly.
- Skill-trigger rates with the `desc-after-r2.txt` wording under a working model.
- Phase-2 second reps, and any phase-3 reruns (`plan3.json`).
- Gemini CLI on a supported client / Antigravity; OpenCode once token refresh works.
- The model Codex actually used (not named in its JSON events).
- Claude Code traces (none exported).
- Live application of the adapter-mind after-description to the plugin skill (eval-only).
- A release of mcp-trace `dev` (held until this round; this write-up does not add new mcp-trace measurements).

### Next if resumed

No further calls without a new go-ahead. If the round is ever continued after the 5-hour window:

- Use the p3 runner, whose circuit breaker records `VOID_LIMIT` and skips later stages on `usage_limit_reached`. Consider also tagging skill evals with `cc_env()` and treating an all-zero trigger set after a known cap as void.
- Re-run judge v2 only, and the after skill evals, before any new harness cells.
- Re-run the four voided `cc-lean2` / `cc-lean2-p` second reps if a fair after-fix matrix is still wanted.
- Keep box `grade.sh` as the T3 source of truth; do not copy hidden tests into `/tmp` itself.
- Gemini and OpenCode need working auth before they belong in the matrix again.

### Does this meet the 'done' bar?

No. Angel's bar was to evaluate and observe our own tools and agents, then self-inspect and fix inefficiencies with proof. Round 2 did the first half on real subscriptions: hidden-test pass rates for Claude Code and Codex, a usable judge-v1 agreement figure (29/32 against box truth), Claude Code OTel token/cost/latency, and confirmation that lean flags — and, separately, `--setting-sources project` — cut a large fraction of list-cost tokens without lowering T1/T2 pass rates. It did not complete the second half. The after-fix measurements that were supposed to close the loop — judge v2, the skill-description rerun, a fair lean2 / lean2-p comparison, phase 3 — either never ran, or ran only after the 5-hour limit and are not evidence. The runner also kept spending calls once the limit was hit, which is itself an inefficiency this write-up can only describe, not re-test.

### Process cleanup (this write-up, box only)

`pgrep -af 'otelcol|litellm|run\.py'` on the box returned no matching processes. This write-up did not start any. The Mac was not contacted, so this is not a check of leftover processes there.
