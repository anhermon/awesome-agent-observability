# MCP-Universe (SalesforceAIResearch/MCP-Universe)

Commit 0df6c427 (2026-10-08). Repo created 2025-05-02, 604 stars, Apache-2.0.

## End-to-end run: ReAct agent, real MCP server, rule-based grading, local model

The bundled `dummy/benchmark_1.yaml` was copied with the LLM switched from `type: openai` / `gpt-4o-mini` to the built-in `type: ollama` / `qwen2.5:3b-instruct`. Nothing else changed.

```bash
uv venv -p 3.12 venv && . venv/bin/activate && uv pip install -r requirements.txt -e .
sed 's/type: openai/type: ollama/; s/model_name: gpt-4o-mini/model_name: qwen2.5:3b-instruct/' \
  mcpuniverse/benchmark/configs/dummy/benchmark_1.yaml > mcpuniverse/benchmark/configs/dummy/benchmark_ollama.yaml
OLLAMA_URL=http://localhost:11434 python run_aao.py   # BenchmarkRunner("dummy/benchmark_ollama.yaml").run(trace_collector=MemoryCollector())
```

```
Service:weather INFO Starting the MCP server
Processing request of type ListToolsRequest
Benchmark INFO Running task: dummy/tasks/weather_1.json
OllamaModel WARNING Error on attempt 1/4: cannot access local variable 'messages_dict' where it is not associated with a value. Retrying...
ReAct ERROR Failed to parse response: Invalid control character at: line 3 column 18 (char 252)
Benchmark INFO Finished benchmark: Test the agent for weather forecasting
evaluation_results: [EvaluationResult(config=EvaluatorConfig(func='json -> get(city)', op='=', value='San Francisco'),
  response='The tool set does not provide current weather information for San Francisco.',
  passed=False, reason='JSON decoding error')]
```

The 3B model did not produce the required JSON, and the task's evaluator failed it. The `messages_dict` warning is an MCP-Universe bug in the Ollama client's retry path; the call succeeded on a later attempt.

## The same evaluator on known answers

```python
Evaluator({"func": "json -> get(city)", "op": "=", "value": "San Francisco"}).evaluate(x)
```

```
'{"city": "San Francisco", "weather": "Sunny, 64F"}'  -> True
'{"city": "Oakland", "weather": "Sunny"}'             -> False  output is not equal to ground-truth
'The tool set does not provide ...'                    -> False  JSON decoding error
```

Most of the real benchmark domains need third-party keys (Google Maps, SerpAPI, GitHub, Yahoo Finance via MCP servers). Only the keyless weather task was run here.
