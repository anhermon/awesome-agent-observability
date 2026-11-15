# LangSmith client SDK link

`langchain-ai/langsmith-sdk` is archived (GitHub API: `archived: true`; description "This repo was archived on Oct 16, 2026. Python SDK moved to langchain-ai/langsmith-python and JS SDK to langchain-ai/langsmith-javascript.").

```bash
uv venv ls-venv && . ls-venv/bin/activate && uv pip install langsmith
python -c "import langsmith, importlib.metadata as m; print(langsmith.__version__); print([v for k,v in m.metadata('langsmith').items() if k in ('Project-URL','Home-page')])"
npm view langsmith version repository.url
```

```
0.14.17
['Homepage, https://github.com/langchain-ai/langsmith-python', 'Repository, https://github.com/langchain-ai/langsmith-python']
version = '0.12.0'
repository.url = 'git+https://github.com/langchain-ai/langsmith-javascript.git'
```

Both new repositories are MIT, not archived, and had commits on 2026-11-13. The LangSmith entry now links both.
