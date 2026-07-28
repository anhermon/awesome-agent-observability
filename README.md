# Awesome Agent Observability [![Awesome](https://awesome.re/badge.svg)](https://awesome.re)

> Curated tools, standards, and platforms for tracing, evaluating, and governing LLM and AI-agent applications.

Agents fail in ways ordinary services do not: a run is non-deterministic, spans a dozen model and tool calls, and "wrong" is a quality judgement rather than a status code. The projects below cover the resulting stack — OpenTelemetry conventions for GenAI, tracing backends, evaluation harnesses, guardrails, gateways, and Model Context Protocol tooling.

Every entry was checked to resolve and to have been updated within the last 12 months at the time of the last audit (2026-07-28). Descriptions say what a project does, not what it markets.

## Contents

- [Standards and instrumentation](#standards-and-instrumentation)
- [Tracing and observability platforms](#tracing-and-observability-platforms)
- [Trace backends](#trace-backends)
- [Evaluation and testing](#evaluation-and-testing)
- [Guardrails and security](#guardrails-and-security)
- [Gateways and proxies](#gateways-and-proxies)
- [Model Context Protocol](#model-context-protocol)
- [Agent frameworks with built-in tracing](#agent-frameworks-with-built-in-tracing)

## Standards and instrumentation

- [OpenTelemetry GenAI Semantic Conventions](https://github.com/open-telemetry/semantic-conventions-genai) - Repository that now owns the GenAI spans, metrics, and events, moved out of the main semantic-conventions repo.
- [OpenTelemetry Semantic Conventions](https://github.com/open-telemetry/semantic-conventions) - Parent repo for all OTel conventions, including the HTTP, RPC, and database spans an agent stack also emits.
- [OpenTelemetry GenAI Observability SIG](https://github.com/open-telemetry/community/blob/main/projects/gen-ai.md) - Charter and scope of the OTel project group driving GenAI telemetry; the place to track where the conventions are heading.
- [OpenTelemetry Python GenAI instrumentation](https://github.com/open-telemetry/opentelemetry-python-contrib/tree/main/instrumentation-genai) - Upstream instrumentation packages for OpenAI, Anthropic, Google GenAI, VertexAI, LangChain, and the Claude Agent SDK.
- [OpenLLMetry](https://github.com/traceloop/openllmetry) - OpenTelemetry-based auto-instrumentation for Python LLM apps, exporting to any OTel backend.
- [OpenLLMetry-JS](https://github.com/traceloop/openllmetry-js) - The same instrumentation for TypeScript and Node.js applications.
- [OpenInference](https://github.com/Arize-ai/openinference) - OTel-compatible instrumentation spec and libraries from the Phoenix team, spanning Python, JS, and Java.
- [OpenLIT](https://github.com/openlit/openlit) - OTel-native auto-instrumentation SDK for LLM, vector-database, and GPU calls, with a self-hosted UI to read the resulting traces.

## Tracing and observability platforms

- [Langfuse](https://github.com/langfuse/langfuse) - Self-hostable tracing, prompt management, datasets, and evals; ingests OTel as well as its own SDKs.
- [Arize Phoenix](https://github.com/Arize-ai/phoenix) - Self-hostable trace viewer and eval workbench that runs locally in a notebook or as a server.
- [LangSmith](https://docs.langchain.com/langsmith/observability) - Hosted tracing and eval product from LangChain; the [client SDKs](https://github.com/langchain-ai/langsmith-sdk) are open source, the backend is not.
- [Helicone](https://github.com/Helicone/helicone) - Proxy-based observability: point your base URL at it and get request logs, cost, and caching without code changes.
- [Opik](https://github.com/comet-ml/opik) - Comet's open-source tracing and evaluation platform for LLM and agent workflows.
- [LangWatch](https://github.com/langwatch/langwatch) - OTel-based platform pairing production monitoring with pre-deploy agent simulation.
- [Laminar](https://github.com/lmnr-ai/lmnr) - Rust-backed open-source tracing and eval platform aimed specifically at agent runs.
- [Agenta](https://github.com/Agenta-AI/agenta) - Self-hostable workspace for authoring and versioning prompts and agents, with evaluation runs and tracing of each model and tool call.
- [Pydantic Logfire](https://github.com/pydantic/logfire) - OTel-based observability with first-class Python, Pydantic, and agent instrumentation.
- [W&B Weave](https://github.com/wandb/weave) - Weights & Biases toolkit for logging, comparing, and evaluating LLM app versions; [docs](https://docs.wandb.ai/weave).
- [MLflow Tracing](https://mlflow.org/docs/latest/genai/tracing/) - GenAI tracing built into [MLflow](https://github.com/mlflow/mlflow), so agent traces sit next to model runs and registries.
- [Braintrust](https://www.braintrust.dev/docs/instrument) - Hosted eval and tracing platform; the scoring library [autoevals](https://github.com/braintrustdata/autoevals) is open source.
- [AgentOps](https://github.com/AgentOps-AI/agentops) - Python SDK for session replay, cost tracking, and benchmarking across CrewAI, OpenAI Agents, LangChain, and AG2.

## Trace backends

General-purpose OpenTelemetry backends that GenAI spans can be sent to when you do not want an LLM-specific product.

- [OpenTelemetry Collector](https://github.com/open-telemetry/opentelemetry-collector) - Vendor-neutral pipeline to receive, process, filter, and fan out traces before they reach a backend.
- [SigNoz](https://github.com/SigNoz/signoz) - OTel-native, self-hostable traces, metrics, and logs in one UI.
- [Jaeger](https://github.com/jaegertracing/jaeger) - CNCF distributed tracing backend that stores spans and serves trace search and a waterfall UI over them.
- [Grafana Tempo](https://github.com/grafana/tempo) - High-volume trace store backed by object storage, queried from Grafana.

## Evaluation and testing

- [Ragas](https://github.com/vibrantlabsai/ragas) - Metrics and test-set generation for RAG and agent pipelines (repo moved from `explodinggradients/ragas`).
- [DeepEval](https://github.com/confident-ai/deepeval) - Pytest-style eval framework with G-Eval, hallucination, and relevancy metrics.
- [Promptfoo](https://github.com/promptfoo/promptfoo) - Declarative CLI for prompt/model comparison plus LLM red-teaming and vulnerability scanning in CI.
- [TruLens](https://github.com/truera/trulens) - Instrumentation plus feedback functions that score app internals, not just final output.
- [Evidently](https://github.com/evidentlyai/evidently) - Python framework for evals, drift detection, and monitoring across tabular, text, and GenAI systems.
- [Inspect](https://github.com/UKGovernmentBEIS/inspect_ai) - UK AI Security Institute's eval framework, built for agentic tasks, tool use, and sandboxed execution.
- [OpenAI Evals](https://github.com/openai/evals) - Eval framework and benchmark registry from OpenAI; broadly used, but the repo moves slowly.
- [lm-evaluation-harness](https://github.com/EleutherAI/lm-evaluation-harness) - EleutherAI's standard harness for few-shot academic benchmarks across model backends.
- [Lighteval](https://github.com/huggingface/lighteval) - Hugging Face evaluation runner supporting transformers, vLLM, and API backends.
- [Giskard](https://github.com/Giskard-AI/giskard-oss) - Scans LLM agents for hallucination, prompt injection, and bias, and turns findings into test suites.
- [Scenario](https://github.com/langwatch/scenario) - Simulates multi-turn users against an agent so conversations, not single calls, can be asserted on.
- [Promptflow](https://github.com/microsoft/promptflow) - Microsoft's flow authoring, batch evaluation, and tracing toolkit for LLM apps.
- [Autoevals](https://github.com/braintrustdata/autoevals) - Standalone library of model-graded and heuristic scorers usable outside Braintrust.

## Guardrails and security

- [Guardrails AI](https://github.com/guardrails-ai/guardrails) - Runs input/output validators around a model call and enforces structured output.
- [NeMo Guardrails](https://github.com/NVIDIA-NeMo/Guardrails) - NVIDIA toolkit for programmable dialogue rails defined in Colang.
- [garak](https://github.com/NVIDIA/garak) - LLM vulnerability scanner probing for jailbreaks, prompt injection, and data leakage.
- [Presidio](https://github.com/data-privacy-stack/presidio) - PII detection, redaction, and anonymisation for text and images; useful for scrubbing traces before export.

## Gateways and proxies

- [LiteLLM](https://github.com/BerriAI/litellm) - SDK and proxy exposing 100+ providers behind the OpenAI API, with cost tracking, logging, and callbacks to most platforms above.
- [Portkey AI Gateway](https://github.com/Portkey-AI/gateway) - Routing gateway with retries, fallbacks, caching, and inline guardrails.
- [Bifrost](https://github.com/maximhq/bifrost) - Go gateway that fronts multiple LLM providers behind one OpenAI-compatible API, with key load balancing, fallbacks, and plugin hooks for guardrails and telemetry.
- [Traceloop Hub](https://github.com/traceloop/hub) - Small Rust LLM gateway from the OpenLLMetry authors, with OTel emission built in.
- [Kong](https://github.com/Kong/kong) - API gateway whose AI plugins add LLM routing, token metrics, and request logging to an existing gateway deployment.

## Model Context Protocol

- [Model Context Protocol](https://github.com/modelcontextprotocol/modelcontextprotocol) - The specification itself; the source of truth for what a compliant client, server, and transport must do.
- [MCP Inspector](https://github.com/modelcontextprotocol/inspector) - Official UI for calling an MCP server's tools by hand and reading the raw JSON-RPC traffic.
- [mcp-trace](https://github.com/anhermon/mcp-trace) - Small Go proxy that sits in front of an MCP server and emits an OpenTelemetry span per JSON-RPC tool call.
- [ToolHive](https://github.com/stacklok/toolhive) - Runs MCP servers in containers with permission policies, secrets handling, and audit logging.
- [MCPJungle](https://github.com/mcpjungle/MCPJungle) - Self-hosted registry and single proxy endpoint for the MCP servers an organisation runs.
- [Docker MCP Gateway](https://github.com/docker/mcp-gateway) - Docker CLI plugin that fronts multiple MCP servers behind one gateway with container isolation.
- [Snyk agent-scan](https://github.com/snyk/agent-scan) - Security scanner for MCP servers, agents, and skills; formerly Invariant Labs' `mcp-scan`.

## Agent frameworks with built-in tracing

- [OpenAI Agents SDK](https://github.com/openai/openai-agents-python) - Ships a built-in tracing layer with exporters to third-party platforms.
- [Google ADK](https://github.com/google/adk-python) - Agent toolkit with built-in evaluation and OpenTelemetry-based tracing.
- [Pydantic AI](https://github.com/pydantic/pydantic-ai) - Agent framework instrumented with OpenTelemetry out of the box, viewable in Logfire or any OTel backend.

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md). Suggestions and corrections welcome, especially for anything on this list that has gone stale.

To the extent possible under law, Angel Hermon has waived all copyright and related or neighboring rights to this work. CC0 1.0, 2026.
