# MCPMark (eval-sys/mcpmark)

Checked 2026-11-15. Repo: Apache-2.0, created 2025-07-01, last push 2026-06-12 (commit cd45b7f). 473 stars.

Claim: runs an agent against real MCP servers (filesystem, GitHub, Notion, Playwright, Postgres, Supabase) on seeded environments, and grades each task with a per-task verification script that checks the final state.

Setup: local only. LiteLLM route `ollama_chat/qwen2.5:3b-instruct`. The filesystem service starts `@modelcontextprotocol/server-filesystem` over stdio, pinned at 2025.12.18.

```
python -m pipeline --mcp filesystem --task-suite easy --tasks file_context/uppercase \
  --models ollama_chat/qwen2.5:3b-instruct --exp-name aao --k 1
```

Output (trimmed):

```
Discovered 10 Filesystem tasks across all categories (suite=easy)
| ✓ Created backup for task file_context__uppercase: .../.mcpmark_backups/backup_filesystem_file_context_uppercase_1659001
Secure MCP Filesystem Server running on stdio
| list_directory {"path": "uppercase"}
...
🔍 Verifying Uppercase in: .../backup_filesystem_file_context_uppercase_1659001
❌ Directory 'uppercase' not found
❌ File 'file_01.txt' not found in uppercase directory
| Verification Result: ✗ FAILED
✓ Tasks passed: 0/1 (0.0%)
📁 Results: results/aao/ollama_chat/qwen2-5:3b-instruct__filesystem-easy/run-1
```

`meta.json` records `turn_count: 2`, `input_tokens: 4922`, `output_tokens: 492`, along with the verifier output. `messages.json` (12 items) shows the model calling the MCP tools with relative paths. The server answered "Access denied - path outside allowed directories", and the model gave up. So the run fails, as you would expect from a 3B model, and the deterministic verifier scored it correctly. The full loop ran: seeded environment, real MCP server, agent tool calls, state verification, then results files.

Not exercised: the GitHub, Notion, Postgres, Playwright and Supabase services, which need accounts or containers.
