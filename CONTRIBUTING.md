# Contributing

Thanks for helping keep this list accurate.

## What belongs here

A project qualifies if it helps you observe, evaluate, or govern an LLM or
agent application, or the parts agents are built from: instrumentation,
tracing, evals, guardrails, gateways that emit telemetry, or MCP-specific
tooling. Model frameworks belong here only if tracing or evaluation is a
first-class part of them.

Evaluation is in scope for any of these subjects, with LLM-as-judge or
deterministic grading (exact match, regex, schema checks, tests):

- LLM, prompt, and RAG applications.
- Agents, including agents built on a framework or SDK.
- Agent harnesses, including CLI coding agents such as Claude Code, Codex CLI,
  Gemini CLI, and OpenCode, run as the thing under test, and benchmark
  harnesses that run them on tasks in a sandbox and grade the result.
- Agent Skills: whether a skill triggers when it should and whether it
  improves results over running without it.
- MCP servers and clients: protocol conformance and how well agents complete
  tasks with a server's tools.
- Telemetry and usage data from coding agents.

Out of scope: general model-capability leaderboards and benchmark runners that
only score a model on static questions (for example lm-evaluation-harness),
unless they also run agents or tools; prompt libraries; and agent frameworks
whose tracing or evaluation is an add-on rather than built in.

Rules for recurring scope questions, one line each:

- Red-teaming frameworks that send attacks to a model, app, or agent and score the responses are in scope, under Guardrails and security.
- Guardrail and safety-classifier models are in scope when the project ships code that runs them as a check on inputs or outputs; a model card alone is not.
- Agent training and fine-tuning frameworks are out of scope even when they capture traces or run benchmarks, because the traces feed training rather than observing or evaluating the agent.

Projects that were declined or removed, and why, are in [DECLINED.md](DECLINED.md).

## Requirements

These are the thresholds every entry is held to, at submission and at each audit.

| # | Threshold | Test | Action when it fails |
|---|-----------|------|----------------------|
| 1 | Alive | The link resolves (HTTP 200, or a redirect to the same project), points at the canonical repo or docs page, and the repository is not archived or disabled. | Fix the link if the project moved; remove if gone or archived. |
| 2 | Maintained | Last commit on the default branch is within 12 months. At 9 months without a commit it goes on the watch list. | Remove past 12 months unless the project is a stable specification or standard that is still the reference. |
| 3 | Not end-of-life | No retirement, sunset, or maintenance-mode-only notice from the maintainers, even if commits continue. | Remove, citing the notice. |
| 4 | Old enough to judge | The project is at least 8 weeks old, counted from repository creation or first public release. | Decline; the author can resubmit once it passes. |
| 5 | Real docs | A README or docs site with install or usage steps. Hosted-only products need public docs that back every claim in the description. | Decline or remove. |
| 6 | In scope | It helps you observe, evaluate, or govern an LLM or agent application, or evaluate an agent, harness, skill, or MCP server (see "What belongs here"). | Decline, recategorize, or remove. |
| 7 | License stated | Stated in the description when not plainly open source: open-core (any `ee/` or `enterprise/` directory under a separate license), source-available, AGPL, or a hosted backend. | Fix the description. |
| 8 | Hands-on | You installed or built it and exercised the claim in the description, and the PR says what you ran. Running against a local model or a mock is fine when the claim does not depend on a specific provider; say so in the PR. Projects that are only a README or mostly generated boilerplate do not make the list. | Decline. |
| 9 | One entry, one place | Each project appears once, in the category it best fits. | Merge or move. |
| 10 | Format | `- [Name](link) - What it actually does.` Sentence case, one line, one sentence, ends with a period, describes behaviour rather than positioning. No "revolutionary", no "next-gen", no feature lists copied from a landing page. | Reword. |

Alphabetical order is not required; entries are roughly ordered by how central they are to the category.

## How the list is maintained

A weekly workflow (`scripts/audit.py`) opens or updates one tracking issue listing entries whose repository is gone, archived, renamed, or past the 12-month bar, and non-GitHub links that are dead, erroring, or permanently redirected, with the new URL (thresholds 1 and 2). It closes the issue when a run finds nothing to act on. A monthly hands-on pass re-runs entries and re-checks descriptions against the project (thresholds 3 to 10), which the script cannot do: maintenance-mode announcements, open-core licensing, scope, and whether the description is still true.

The GitHub Pages site is generated from the README, `evidence/`, `DECLINED.md`, and the git history of the README at build time (`scripts/build_site.py`). Do not hand-edit files under `site-build/`. After a monthly hands-on pass, create one GitHub Release from the generated notes; see [RELEASING.md](RELEASING.md).

## Removals

Open a pull request or issue if an entry is archived, renamed, dead, or the
description no longer matches the project. Include the evidence (last commit
date, archive banner, redirect target).

## Self-promotion

Allowed and stated up front. The maintainer's own projects are held to the same bar.
Submit your own project if it meets the bar above, and write the description
the same way you would for someone else's.

## Process

1. Check [DECLINED.md](DECLINED.md) first; if the project is there, say what has changed since.
2. Fork, add your entry, run `npx awesome-lint`.
3. Open a pull request describing what the project does and why it belongs.
