# Declined and removed entries

Projects that were proposed and not added, or listed and later removed, with the date and the [CONTRIBUTING](CONTRIBUTING.md#requirements) threshold the decision rests on. Check this file before opening a pull request. A decline is not permanent: when the reason no longer holds (the project is old enough, has docs, or is maintained again), resubmit and say what changed.

## Declined

| Project | Date | Where | Reason |
| --- | --- | --- | --- |
| XiuRouter | 2026-09-28 | [#10](https://github.com/anhermon/awesome-agent-observability/pull/10) | Linked only to hosted product documentation, with no public repository; under thresholds 5 and 8 a hosted-only product needs public docs that back every claim and a hands-on run. |
| agent-watch | 2026-09-28 | [#12](https://github.com/anhermon/awesome-agent-observability/pull/12) | Out of scope (threshold 6): it reports the process state of background coding agents (running, done, failed, stalled) and does not trace model calls, tool calls, or agent steps. |
| Speakeasy | 2026-09-28 | [#13](https://github.com/anhermon/awesome-agent-observability/pull/13) | Linked to a product marketing page rather than a repository or docs that back the description (threshold 5). |
| OpenClaw Monitor | 2026-10-15 | [#27](https://github.com/anhermon/awesome-agent-observability/pull/27) | No commit since 2026-05-14 at review time, a repository made mostly of generated status files rather than install and usage docs, and an endpoint that crashed in the submitter's own run (thresholds 2, 5, and 8). |
| Agent Lightning | 2026-11-16 | [#47](https://github.com/anhermon/awesome-agent-observability/issues/47) | Out of scope (threshold 6): a reinforcement-learning framework for training agents, whose proxy captures agent interactions as training data rather than for observing or evaluating the agent. |

## Removed

| Project | Date | Where | Reason |
| --- | --- | --- | --- |
| UpTrain | 2026-07-28 | [#2](https://github.com/anhermon/awesome-agent-observability/pull/2) | Last push 2024-08-18 (threshold 2). |
| Langtrace | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Dormant (threshold 2). |
| OpenAI Evals | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Dormant (threshold 2). |
| Promptflow | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | End of life announced by the maintainers (threshold 3). |
| lm-evaluation-harness | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Out of scope (threshold 6): scores models on static questions and does not run agents or tools. |
| Lighteval | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Out of scope (threshold 6), for the same reason as lm-evaluation-harness. |
| Agent QA | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Out of scope (threshold 6); source-available under the FSL. |
| YYLO (`yylo-dev/yylo`) | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Claims could not be verified hands-on (threshold 8). The separate YYLO Benchmark repository is listed. |
| Jetty | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Claims could not be verified hands-on and the fit was weak (thresholds 6 and 8). |
| Invariant Guardrails | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | No release in 14 months (threshold 2). |
| Tuskira | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Repository was 3 days old (threshold 4). |
| SandBase Harness | 2026-10-04 | [#21](https://github.com/anhermon/awesome-agent-observability/pull/21) | Too young to judge, and the description did not match the project (thresholds 4 and 10). |
| Helicone | 2026-10-15 | [#29](https://github.com/anhermon/awesome-agent-observability/pull/29) | Maintenance mode only since the March 2026 Mintlify acquisition (threshold 3). |
| sealref | 2026-10-17 | [6f1264c](https://github.com/anhermon/awesome-agent-observability/commit/6f1264ce5a0c826a3c4c939260ffc1e6d4fc4fad) | Under 8 weeks old (threshold 4); the maintainer's own project, eligible to resubmit after 2026-11-26. |
| mcp-trace | 2026-11-16 | [archive notice](https://github.com/anhermon/mcp-trace#readme) | Repository archived on 2026-11-16 (threshold 1); its README says the project is no longer developed (threshold 3). |
| ctxlens (`AgentPostmortem/Ctxlens`) | 2026-11-18 | this pull request | The repository now returns 404 (threshold 1). No successor was found: the owner's organization now hosts an unrelated project, and the `ctxlens-cli` package on PyPI (0.1.1) still points at the missing repository. |

## Closed pull requests whose project is listed

These outside pull requests were closed without merging, but the project is on the list through another change, so they are not declines.

| Project | Closed PR | Listed through |
| --- | --- | --- |
| ClawBench | [#1](https://github.com/anhermon/awesome-agent-observability/pull/1) | [#4](https://github.com/anhermon/awesome-agent-observability/pull/4), the same entry with a more specific description. |
| HermesGate | [#14](https://github.com/anhermon/awesome-agent-observability/pull/14) | Merged by hand in 8070039. |
| Noveum Trace | [#15](https://github.com/anhermon/awesome-agent-observability/pull/15) | [#30](https://github.com/anhermon/awesome-agent-observability/pull/30), linking the SDK repository instead of the docs. |
| Aident Loadout | [#32](https://github.com/anhermon/awesome-agent-observability/pull/32) | [#33](https://github.com/anhermon/awesome-agent-observability/pull/33), the contributor's commit plus a reword to match the docs. |
