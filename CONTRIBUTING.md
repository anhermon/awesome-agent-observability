# Contributing

Thanks for helping keep this list accurate.

## What belongs here

A project qualifies if it helps you observe, evaluate, or govern an LLM or
agent application: instrumentation, tracing, evals, guardrails, gateways that
emit telemetry, or MCP-specific tooling. Model frameworks belong here only if
tracing or evaluation is a first-class part of them.

## Requirements

These are the thresholds every entry is held to, at submission and at each audit.

| # | Threshold | Test | Action when it fails |
|---|-----------|------|----------------------|
| 1 | Alive | The link resolves (HTTP 200, or a redirect to the same project), points at the canonical repo or docs page, and the repository is not archived or disabled. | Fix the link if the project moved; remove if gone or archived. |
| 2 | Maintained | Last commit on the default branch is within 12 months. At 9 months without a commit it goes on the watch list. | Remove past 12 months unless the project is a stable specification or standard that is still the reference. |
| 3 | Not end-of-life | No retirement, sunset, or maintenance-mode-only notice from the maintainers, even if commits continue. | Remove, citing the notice. |
| 4 | Old enough to judge | The project is at least 8 weeks old, counted from repository creation or first public release. | Decline; the author can resubmit once it passes. |
| 5 | Real docs | A README or docs site with install or usage steps. Hosted-only products need public docs that back every claim in the description. | Decline or remove. |
| 6 | In scope | It helps you observe, evaluate, or govern an LLM or agent application (see "What belongs here"). | Decline, recategorize, or remove. |
| 7 | License stated | Stated in the description when not plainly open source: open-core (any `ee/` or `enterprise/` directory under a separate license), source-available, AGPL, or a hosted backend. | Fix the description. |
| 8 | Hands-on | You installed or built it and exercised the claim in the description, and the PR says what you ran. Projects that are only a README or mostly generated boilerplate do not make the list. | Decline. |
| 9 | One entry, one place | Each project appears once, in the category it best fits. | Merge or move. |
| 10 | Format | `- [Name](link) - What it actually does.` Sentence case, one line, one sentence, ends with a period, describes behaviour rather than positioning. No "revolutionary", no "next-gen", no feature lists copied from a landing page. | Reword. |

Alphabetical order is not required; entries are roughly ordered by how central they are to the category.

## How the list is maintained

A weekly workflow (`scripts/audit.py`) opens or updates one tracking issue listing entries whose repository is gone, archived, renamed, or past the 12-month bar (thresholds 1 and 2). A monthly hands-on pass re-runs entries and re-checks descriptions against the project (thresholds 3 to 10), which the script cannot do: maintenance-mode announcements, open-core licensing, scope, and whether the description is still true.

## Removals

Open a pull request or issue if an entry is archived, renamed, dead, or the
description no longer matches the project. Include the evidence (last commit
date, archive banner, redirect target).

## Self-promotion

Allowed and stated up front — the maintainer's own `mcp-trace` is on the list.
Submit your own project if it meets the bar above, and write the description
the same way you would for someone else's.

## Process

1. Fork, add your entry, run `npx awesome-lint`.
2. Open a pull request describing what the project does and why it belongs.
