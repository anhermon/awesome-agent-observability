# Evidence for the 2026-11-15 evals expansion

One file per entry added, rewritten, or removed in this change. Each file lists the exact commands that were run and the relevant output, trimmed only for length.

Setup used for every run:

- Box: Debian 13 (trixie), x86_64, 8 vCPU, 16 GB RAM, Docker Engine 29.1.4.
- Models: **local only**, through Ollama 0.40.11 (`qwen3.5:4b-fast`, `qwen2.5:3b-instruct`). No LLM provider API key was used anywhere. Where a tool insists on a key variable, it was set to a dummy string that Ollama ignores.
- Vanilla Claude Code 2.1.289 was pointed at Ollama's Anthropic-compatible endpoint with `ANTHROPIC_BASE_URL=http://<host>:11434` and a dummy `ANTHROPIC_AUTH_TOKEN`. That is how "Claude Code as the harness under test" was exercised without a Claude subscription login on the box.
- Small local models fail many tasks. These runs prove that each tool installs, runs the subject, and grades it as described; they are not quality numbers for the models.
