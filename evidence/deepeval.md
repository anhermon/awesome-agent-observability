# DeepEval: tool-correctness and MCP metrics (line reworded)

Version: `deepeval` 4.3.4.

```bash
uv venv venv && . venv/bin/activate && uv pip install deepeval ollama
python - <<'PY'
import deepeval.metrics as m
print([n for n in dir(m) if "MCP" in n])
from deepeval.metrics import ToolCorrectnessMetric
from deepeval.models import OllamaModel
from deepeval.test_case import LLMTestCase, ToolCall
judge = OllamaModel(model="qwen2.5:3b-instruct", base_url="http://localhost:11434")
good = LLMTestCase(input="weather in Paris?", actual_output="18C",
    tools_called=[ToolCall(name="geocode"), ToolCall(name="get_weather")],
    expected_tools=[ToolCall(name="geocode"), ToolCall(name="get_weather")])
bad = LLMTestCase(input="weather in Paris?", actual_output="18C",
    tools_called=[ToolCall(name="web_search")],
    expected_tools=[ToolCall(name="geocode"), ToolCall(name="get_weather")])
for name, t in [("match", good), ("mismatch", bad)]:
    met = ToolCorrectnessMetric(model=judge, should_consider_ordering=True, async_mode=False, include_reason=False)
    met.measure(t); print(name, met.score, met.success)
PY
```

```
['MCPTaskCompletionMetric', 'MCPUseMetric', 'MultiTurnMCPUseMetric']
match 1.0 True
mismatch 0.0 False
```

Tool correctness ran in about 2 seconds with no model call (deterministic name and order comparison; the judge model is only used when you pass `available_tools`). The MCP metrics were confirmed to ship in the package and are documented at https://deepeval.com/docs/metrics-mcp-use; they need a judge model and were not scored here. Without `model=`, DeepEval 4.3.4 raises `OpenAI API key is not configured`, so a local judge has to be passed explicitly.
