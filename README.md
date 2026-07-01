# Awesome Agent Observability

[![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

A curated list of open-source tools, standards, and platforms for observing, tracing, evaluating, and governing LLM and AI-agent applications.

## Contents

- [Standards & instrumentation](#standards--instrumentation)
- [Tracing & observability platforms](#tracing--observability-platforms)
- [Eval & testing](#eval--testing)
- [Gateways & proxies](#gateways--proxies)
- [Governance & guardrails](#governance--guardrails)
- [MCP-specific](#mcp-specific)

## Standards & instrumentation

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai) — Official OpenTelemetry repo defining GenAI spans, metrics, and events for LLM clients, MCP, and provider-specific conventions.
- [OpenLLMetry (Traceloop)](https://github.com/traceloop/openllmetry) — Open-source OpenTelemetry-based instrumentation for LLM apps, auto-tracing providers and vector DBs to any OTel backend.
- [OpenLIT](https://github.com/openlit/openlit) — OpenTelemetry-native observability platform covering LLM tracing, GPU monitoring, evaluations, guardrails, and prompt management.

## Tracing & observability platforms

- [Langfuse](https://github.com/langfuse/langfuse) — Open-source LLM engineering platform for tracing, prompt management, evaluation, and debugging of AI applications.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) — Open-source AI observability and evaluation platform for tracing, benchmarking, datasets, and prompt experimentation.
- [LangSmith](https://github.com/langchain-ai/langsmith-sdk) — Platform (with SDK) to debug, evaluate, and monitor LLM applications and agents, with native LangChain integration.
- [Helicone](https://github.com/Helicone/helicone) — Open-source LLM observability platform and AI gateway to monitor, evaluate, and route requests across many models.
- [Opik (Comet)](https://github.com/comet-ml/opik) — Open-source platform for tracing, evaluating, and optimizing LLM and agentic applications from prototype to production.
- [LangWatch](https://github.com/langwatch/langwatch) — OpenTelemetry-based platform for testing, simulating, evaluating, and monitoring AI agents before and after deployment.
- [Laminar (lmnr)](https://github.com/lmnr-ai/lmnr) — Open-source observability platform purpose-built for AI agents, providing tracing, monitoring, and evaluation.
- [Agenta](https://github.com/Agenta-AI/agenta) — Open-source LLMOps platform combining prompt management, evaluation, and OpenTelemetry-native observability.
- [Pydantic Logfire](https://github.com/pydantic/logfire) — OpenTelemetry-based observability platform from the Pydantic team with deep Python and LLM/agent tracing.
- [W&B Weave](https://github.com/wandb/weave) — Weights & Biases toolkit to log, debug, and evaluate LLM/GenAI applications across experimentation and production.

## Eval & testing

- [Ragas](https://github.com/explodinggradients/ragas) — Python toolkit for evaluating and optimizing LLM applications with objective metrics and test-set generation.
- [DeepEval](https://github.com/confident-ai/deepeval) — Open-source, Pytest-like LLM evaluation framework with research-backed metrics such as G-Eval and answer relevancy.
- [Promptfoo](https://github.com/promptfoo/promptfoo) — CLI and library for evaluating and red-teaming LLM apps by testing prompts and comparing models.
- [TruLens](https://github.com/truera/trulens) — Evaluation and tracking framework for LLM apps and agents using instrumentation and feedback functions.
- [UpTrain](https://github.com/uptrain-ai/uptrain) — Open-source platform to evaluate and improve LLM applications with 20+ pre-built checks and root-cause analysis.
- [Evidently](https://github.com/evidentlyai/evidently) — Open-source Python framework to evaluate, test, and monitor ML and LLM systems across tabular, text, and GenAI data.

## Gateways & proxies

- [LiteLLM](https://github.com/BerriAI/litellm) — Python SDK and proxy/AI gateway calling 100+ LLM APIs in OpenAI format with cost tracking, logging, and guardrails.
- [Portkey AI Gateway](https://github.com/Portkey-AI/gateway) — Open-source AI gateway routing to many LLM providers with integrated guardrails, retries, fallbacks, and caching.
- [Traceloop Hub](https://github.com/traceloop/hub) — Open-source, high-performance LLM gateway in Rust providing a unified provider API with built-in observability.

## Governance & guardrails

- [Guardrails AI](https://github.com/guardrails-ai/guardrails) — Python framework running input/output guards on LLMs to detect risks and generate validated structured output.

## MCP-specific

- [mcp-trace](https://github.com/anhermon/mcp-trace) — Transparent Go proxy for MCP servers that emits OpenTelemetry spans for every JSON-RPC tool call.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) — Official developer tool for interactively testing and debugging Model Context Protocol servers via a web UI and proxy.

## Contributing

Contributions are welcome — open an issue or pull request to suggest a tool. Please keep entries open-source and observability-focused, and include a one-line description.

Curated by Angel Hermon ([anhermon](https://github.com/anhermon)).
