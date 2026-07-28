# Contributing

Thanks for helping keep this list accurate.

## What belongs here

A project qualifies if it helps you observe, evaluate, or govern an LLM or
agent application: instrumentation, tracing, evals, guardrails, gateways that
emit telemetry, or MCP-specific tooling. Model frameworks belong here only if
tracing or evaluation is a first-class part of them.

## Requirements

- The link resolves and points at the canonical repo or docs page.
- The project has been updated within the last 12 months and is not archived.
- One entry per project, in the category it best fits.
- Format: `- [Name](link) - What it actually does.`
  - Sentence case, one line, ends with a period.
  - Describe behaviour, not positioning. No "revolutionary", no "next-gen", no
    feature lists copied from a landing page.
- Alphabetical order is not required; entries are roughly ordered by how
  central they are to the category.

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
