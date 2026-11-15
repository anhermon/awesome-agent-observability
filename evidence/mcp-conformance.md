# MCP Conformance (modelcontextprotocol/conformance)

Version: `@modelcontextprotocol/conformance` 0.1.16 (npx). Repo created 2025-07-10; last push 2026-11-11. License file: Apache-2.0, with MIT for contributions not yet relicensed.

## Reference server: all scenarios pass

```bash
git clone --depth 1 https://github.com/modelcontextprotocol/conformance
cd conformance/examples/servers/typescript && npm ci && PORT=3002 npx tsx everything-server.ts &
npx @modelcontextprotocol/conformance server --url http://localhost:3002/mcp
```

```
=== SUMMARY ===
✓ server-initialize: 1 passed, 0 failed
✓ tools-call-image: 1 passed, 0 failed
✓ tools-call-sampling: 1 passed, 0 failed
✓ tools-call-elicitation: 1 passed, 0 failed
✓ elicitation-sep1034-defaults: 5 passed, 0 failed
✓ dns-rebinding-protection: 2 passed, 0 failed
... (30 scenarios)
Total: 40 passed, 0 failed
```

## A server that does not implement the fixtures fails the right scenarios

```bash
PORT=3001 npx @modelcontextprotocol/server-everything streamableHttp &
npx @modelcontextprotocol/conformance server --url http://localhost:3001/mcp
```

```
✓ tools-list: 1 passed, 0 failed
✗ tools-call-image: 0 passed, 1 failed
✗ prompts-get-simple: 0 passed, 1 failed
✗ dns-rebinding-protection: 1 passed, 1 failed
Total: 13 passed, 19 failed
```

## Used on our own tool: mcp-trace in front of the passing server

The list's own `mcp-trace` proxy was put between the suite and the reference server, so any new failure is the proxy's.

```bash
mcp-trace --transport streamable --target http://localhost:3002/mcp --port 8014 --otel-stdout &   # v2.0.4 release binary
npx @modelcontextprotocol/conformance server --url http://localhost:8014/mcp --scenario tools-call-sampling
npx @modelcontextprotocol/conformance server --url http://localhost:8014/mcp --scenario tools-call-elicitation
npx @modelcontextprotocol/conformance server --url http://localhost:8014/mcp --scenario dns-rebinding-protection
```

```
tools-call-sampling      Passed: 0/1   Error: MCP error -32001: Request timed out
tools-call-elicitation   Passed: 0/1   Error: MCP error -32001: Request timed out
dns-rebinding-protection Passed: 1/2   Error: Expected HTTP 4xx for invalid Host/Origin headers, got 200
tools-call-simple-text   Passed: 1/1
```

Full run through v2.0.3 (the binary installed on the box): 27 passed, 5 failed, the same five scenarios. These are findings for mcp-trace itself, to be fixed in that repo: server-to-client requests (sampling, elicitation) do not make it back through the proxy, and the proxy accepts any `Host`/`Origin`. A separate check showed that v2.0.3 emitted no span for a Streamable HTTP `tools/call` answered with `text/event-stream`, while v2.0.4 emitted `SPAN: mcp tools/call test_simple_text ... status=Ok`, so the list line's claim holds for the current release only.
