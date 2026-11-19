#!/usr/bin/env python3
"""Generate the GitHub Pages site from README.md and evidence/.

The README is the single source for list content. Write-ups come from
PROOF.md, evidence/, DECLINED.md, and the git history of the README. Do not hand-edit files
under site-build/; this script recreates that directory on every run.
"""

from __future__ import annotations

import argparse
import re
import shutil
from pathlib import Path

import list_updates

ROOT = Path(__file__).resolve().parents[1]
README_PATH = ROOT / "README.md"
EVIDENCE_DIR = ROOT / "evidence"
CONTRIBUTING_PATH = ROOT / "CONTRIBUTING.md"
BUILD_DIR = ROOT / "site-build"
DOCS_DIR = BUILD_DIR / "docs"
SITE_DIR = BUILD_DIR / "site"
THEME_DIR = ROOT / "site-theme"
HOOKS_PATH = Path(__file__).resolve().parent / "mkdocs_hooks.py"

SITE_NAME = "Awesome Agent Observability"
SITE_URL = "https://anhermon.dev/awesome-agent-observability/"
REPO_URL = "https://github.com/anhermon/awesome-agent-observability"
SITE_TAGLINE = (
    "Tools, standards, and benchmarks for tracing and evaluating AI products "
    "(LLM apps, agents, coding-agent harnesses, Agent Skills, and MCP servers), "
    "with evaluations graded by LLM judges or deterministic checks."
)

SKIP_SECTION_PAGES = {"Contents"}
COMPARISON_SLUG = "platform-comparison"
COMPARISON_TITLE = "Platform comparison"
COMPARISON_INSERT_AFTER = "tracing-and-observability-platforms"
H1_BADGE_RE = re.compile(r"\s*\[!\[Awesome\]\([^)]+\)\]\([^)]+\)")
HEADING_RE = re.compile(r"^## (.+)$", re.M)
LINK_RE = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")
ENTRY_RE = re.compile(r"^- \[([^\]]+)\]", re.M)
SLUG_RE = re.compile(r"[^\w\s-]")
SPACE_RE = re.compile(r"[-\s]+")


def slugify(title: str) -> str:
    slug = SLUG_RE.sub("", title.lower().strip())
    return SPACE_RE.sub("-", slug).strip("-")


def yaml_quote(value: str) -> str:
    return '"' + value.replace("\\", "\\\\").replace('"', '\\"') + '"'


def strip_markdown(text: str) -> str:
    text = LINK_RE.sub(r"\1", text)
    text = re.sub(r"\*\*(.+?)\*\*", r"\1", text)
    text = re.sub(r"[*`]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def first_paragraph(body: str) -> str:
    for para in body.split("\n\n"):
        piece = para.strip()
        if not piece or piece.startswith(("- ", "|", "#", ">")):
            continue
        return piece
    return ""


def first_prose(body: str) -> str | None:
    for para in body.split("\n\n"):
        piece = para.strip()
        if not piece or piece.startswith(("- ", "|", "#", ">", "```")):
            continue
        # A paragraph that is only a bold heading plus text is still prose.
        return strip_markdown(piece)
    return None


SETUP_PROSE_RE = re.compile(
    r"^(Version\b|Checked \d{4}-\d{2}-\d{2}|Metadata:|Commit [0-9a-f]{7}|"
    r"Installed from |Setup:|Auth:|Model:)",
    re.I,
)
CLAIM_PREFIX_RE = re.compile(
    r"^Claim(?: in the (?:list|rewritten) line)?:\s*",
    re.I,
)


def is_setup_prose(text: str) -> bool:
    """True for version, date-checked, and other metadata openers."""
    stripped = text.strip()
    if SETUP_PROSE_RE.match(stripped):
        return True
    # Labels such as "Run:", "Output:", "Script (abridged):"
    if len(stripped) <= 40 and stripped.endswith(":"):
        return True
    if re.match(
        r"^Claims? in the list line, and where each comes from:$",
        stripped,
        re.I,
    ):
        return True
    return False


def evidence_description(title: str, body: str) -> str:
    """Meta description from a meaningful sentence, not 'Version: 1.2.3.'"""
    paras: list[str] = []
    for para in body.split("\n\n"):
        piece = para.strip()
        if not piece or piece.startswith(("- ", "|", "#", ">", "```")):
            continue
        paras.append(strip_markdown(piece))
    for piece in paras:
        if CLAIM_PREFIX_RE.match(piece):
            cleaned = CLAIM_PREFIX_RE.sub("", piece).strip()
            if cleaned:
                if cleaned[0].islower():
                    cleaned = cleaned[0].upper() + cleaned[1:]
                return shorten(cleaned)
    for piece in paras:
        if not is_setup_prose(piece):
            return shorten(piece)
    return f"Hands-on evidence for {title} in {SITE_NAME}."


# Evidence pages whose first paragraphs would give a stale, partial, or
# over-broad description. Each text is stated on the evidence page itself.
DESCRIPTION_OVERRIDES = {
    "bfcl": "Ran bfcl evaluate on a two-item fixture (accuracy 50%, 1 of 2); live generation against a model was not run.",
    "ccusage": "ccusage run on real Claude Code session logs and cross-checked against OpenTelemetry events: it misses output tokens the transcript records as zero.",
    "coder-eval": "One coder-eval task run with Claude Code on a local 4B model; both deterministic criteria failed correctly, from the small model, not the harness.",
    "mcp-atlas": "Smoke run of MCP-Atlas in Docker with a local model: 13 of 20 default servers online; claim-level scoring was not run.",
    "mcp-conformance": "Run log of the MCP conformance suite against the mcp-trace proxy, which was archived on 2026-11-16 and is no longer on this list.",
    "mcpmark": "Hands-on run of MCPMark's filesystem service with a local 3B model; the GitHub, Notion, Playwright, Postgres and Supabase services were not exercised.",
    "promptfoo": "Ran promptfoo against the Claude Agent SDK provider with deterministic assertions; the OpenAI Codex SDK provider was not run (Codex CLI not installed).",
    "swe-bench": "Grading is deterministic: the reference patch is applied inside the per-instance Docker image and the held-out tests decide the result. No model was involved.",
    "tau2-bench": "One tau2 mock-domain trial with a local 3B model reached max_steps (reward 0.000); the orchestrator, user simulator, tools and scorer all ran.",
}


def entry_names(body: str) -> list[str]:
    return ENTRY_RE.findall(body)


def shorten(text: str, limit: int = 160) -> str:
    text = text.strip()
    if len(text) <= limit:
        return text
    cut = text[: limit - 1].rsplit(" ", 1)[0].rstrip(".,;:")
    return cut + "…"


def description_for(title: str, body: str) -> str:
    prose = first_prose(body)
    if prose:
        return shorten(prose)
    names = entry_names(body)
    if names:
        if len(names) <= 3:
            listed = ", ".join(names)
        else:
            listed = f"{', '.join(names[:3])}, and more"
        return f"{title} in {SITE_NAME}, including {listed}."
    return (
        f"{title} from {SITE_NAME}, a curated list of LLM and AI agent "
        "observability and evaluation tools."
    )


def parse_readme(text: str) -> tuple[str, str, list[dict[str, str]]]:
    heading_matches = list(HEADING_RE.finditer(text))
    if not heading_matches:
        raise SystemExit("README.md has no ## sections")
    preamble = text[: heading_matches[0].start()].strip()
    # Drop the H1; the theme renders the site name.
    preamble = re.sub(r"^# .+\n+", "", preamble)
    sections: list[dict[str, str]] = []
    for i, match in enumerate(heading_matches):
        title = match.group(1).strip()
        end = heading_matches[i + 1].start() if i + 1 < len(heading_matches) else len(text)
        body = text[match.end() : end].strip()
        sections.append({"title": title, "slug": slugify(title), "body": body})
    return preamble, SITE_TAGLINE, sections


def extract_markdown_table(body: str) -> str | None:
    lines = body.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.startswith("|") and i + 1 < len(lines) and re.match(r"^\|\s*[-:| ]+$", lines[i + 1]):
            start = i
            break
    if start is None:
        return None
    end = start
    while end < len(lines) and lines[end].startswith("|"):
        end += 1
    return "\n".join(lines[start:end])


def rewrite_url(url: str, section_slugs: set[str]) -> str:
    if url.startswith(("http://", "https://", "mailto:", "//")):
        return url
    path, fragment = url, ""
    if "#" in url:
        path, fragment = url.split("#", 1)
        fragment = "#" + fragment
    if path in {"", "."}:
        if fragment[1:] in section_slugs:
            return f"{fragment[1:]}.md"
        return url
    if path == "CONTRIBUTING.md":
        return "contributing.md" + fragment
    if path == "DECLINED.md":
        return "declined.md" + fragment
    if path == "PROOF.md":
        return "proof.md" + fragment
    if path == "RELEASING.md":
        return f"{REPO_URL}/blob/main/RELEASING.md" + fragment
    if path in {"evidence", "evidence/"}:
        return "evidence/index.md" + fragment
    if path.startswith("evidence/"):
        name = path[len("evidence/") :]
        if name in {"comparison-table.md", "comparison-table"}:
            return f"{COMPARISON_SLUG}.md" + (fragment or "#sources")
        if name.endswith(".md"):
            return f"evidence/{name}{fragment}"
        return f"evidence/{name}{fragment}"
    if path.endswith(".md") and slugify(path[:-3]) in section_slugs:
        return f"{slugify(path[:-3])}.md{fragment}"
    return url


def rewrite_links(markdown: str, section_slugs: set[str]) -> str:
    def repl(match: re.Match[str]) -> str:
        text, url = match.group(1), match.group(2)
        return f"[{text}]({rewrite_url(url, section_slugs)})"

    return LINK_RE.sub(repl, markdown)


def front_matter(title: str, description: str) -> str:
    return (
        "---\n"
        f"title: {yaml_quote(title)}\n"
        f"description: {yaml_quote(description)}\n"
        "---\n\n"
    )


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def contributing_page(readme_body: str, section_slugs: set[str]) -> tuple[str, str]:
    contributing = CONTRIBUTING_PATH.read_text(encoding="utf-8")
    contributing = re.sub(r"^# .+\n+", "", contributing).strip()
    contributing = rewrite_links(contributing, section_slugs)
    intro = rewrite_links(readme_body, section_slugs).strip()
    # The README points at CONTRIBUTING.md; the full file is on this page.
    intro = re.sub(
        r"See \[CONTRIBUTING\.md\]\([^)]+\)\.\s*",
        "",
        intro,
    )
    body = intro + "\n\n" + contributing + "\n"
    return body, description_for("Contributing", contributing)


def declined_page(section_slugs: set[str]) -> tuple[str, str, str]:
    declined = (ROOT / "DECLINED.md").read_text(encoding="utf-8")
    heading = "Declined and removed entries"
    match = re.match(r"^# (.+)$", declined, re.M)
    if match:
        heading = match.group(1).strip()
        declined = declined[match.end() :].lstrip()
    body = rewrite_links(declined, section_slugs).strip() + "\n"
    return heading, body, description_for(heading, body)


def comparison_page(platforms_body: str, section_slugs: set[str]) -> tuple[str, str]:
    table = extract_markdown_table(platforms_body)
    if not table:
        raise SystemExit("could not find the platform comparison table in the README")
    intro = first_paragraph(platforms_body)
    evidence = (EVIDENCE_DIR / "comparison-table.md").read_text(encoding="utf-8")
    evidence = re.sub(r"^# .+\n+", "", evidence).strip()
    evidence = rewrite_links(evidence, section_slugs)
    # The evidence file restates the table with source links; keep that as Sources.
    parts = [
        rewrite_links(intro, section_slugs),
        "",
        table,
        "",
        f'<h2 id="sources">Sources</h2>',
        "",
        evidence,
        "",
    ]
    desc = description_for(COMPARISON_TITLE, platforms_body)
    return "\n".join(parts), desc


def evidence_pages() -> list[tuple[str, Path, str, str]]:
    pages = []
    for path in sorted(EVIDENCE_DIR.glob("*.md")):
        if path.name == "comparison-table.md":
            continue
        text = path.read_text(encoding="utf-8").strip()
        heading = path.stem.replace("-", " ")
        match = re.match(r"^# (.+)$", text, re.M)
        if match:
            heading = match.group(1).strip()
            text = text[match.end() :].lstrip()
        slug = path.stem if path.name != "README.md" else "index"
        dest = DOCS_DIR / "evidence" / f"{slug}.md"
        desc = DESCRIPTION_OVERRIDES.get(path.stem) or evidence_description(heading, text)
        pages.append((heading, dest, text, desc))
    return pages



PROOF_TITLE = "We evaluated our own agents with tools from this list"
PROOF_SLUG = "proof"


def proof_page(section_slugs: set[str]) -> tuple[str, str, str]:
    path = ROOT / "PROOF.md"
    if not path.is_file():
        raise SystemExit(f"missing {path}")
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^# .+\n+", "", text).lstrip()
    body = rewrite_links(text, section_slugs).strip() + "\n"
    # Python-Markdown's slug drops the em dash; GitHub's link used a double hyphen.
    body = body.replace(
        "](#round-2-angels-mac-real-subscriptions--2026-11-15)",
        "](#round-2-angels-mac-real-subscriptions-2026-11-15)",
    )
    desc = (
        "Dated record of the 2026-11-15 proof rounds: evaluating and observing "
        "the maintainer's own agents with tools from this list."
    )
    return PROOF_TITLE, body, desc


def write_ups_section(verified: str) -> str:
    date = f" (last verified {verified})" if verified else ""
    return (
        "## Write-ups\n\n"
        f"- [Platform comparison]({COMPARISON_SLUG}.md){date}. "
        "Every cell is sourced in [`evidence/comparison-table.md`](platform-comparison.md#sources).\n"
        f"- [{PROOF_TITLE}]({PROOF_SLUG}.md) (2026-11-15). "
        "Source: [PROOF.md](proof.md).\n"
        "- [List updates](updates/index.md): adds and removals from each month, "
        "generated from the git history of the README, [DECLINED.md](declined.md), "
        "and [`evidence/`](evidence/index.md).\n"
    )


def comparison_verified_date(platforms_body: str) -> str:
    match = re.search(r"Last verified (\d{4}-\d{2}-\d{2})", platforms_body)
    return match.group(1) if match else ""


def nav_yaml(items: list[tuple[str, str]]) -> str:
    lines = ["nav:"]
    for title, filename in items:
        lines.append(f"  - {yaml_quote(title)}: {filename}")
    return "\n".join(lines)


def write_mkdocs_yml(nav_items: list[tuple[str, str]], site_description: str) -> None:
    # Paths in this file are relative to site-build/.
    content = f"""site_name: {yaml_quote(SITE_NAME)}
site_url: {SITE_URL}
site_description: {yaml_quote(site_description)}
repo_url: {REPO_URL}
repo_name: anhermon/awesome-agent-observability
docs_dir: docs
site_dir: site
use_directory_urls: true
plugins: []
theme:
  name: null
  custom_dir: ../site-theme
hooks:
  - ../scripts/mkdocs_hooks.py
not_in_nav: |
  evidence/**
  updates/2*
markdown_extensions:
  - tables
  - smarty
  - toc:
      permalink: false
      toc_depth: 2
{nav_yaml(nav_items)}
"""
    write(BUILD_DIR / "mkdocs.yml", content)


def build() -> list[str]:
    readme = README_PATH.read_text(encoding="utf-8")
    preamble, tagline, sections = parse_readme(readme)
    section_slugs = {s["slug"] for s in sections if s["title"] not in SKIP_SECTION_PAGES}
    section_slugs.add("contributing")
    section_slugs.add(COMPARISON_SLUG)
    section_slugs.add("proof")

    if BUILD_DIR.exists():
        shutil.rmtree(BUILD_DIR)
    DOCS_DIR.mkdir(parents=True)

    homepage_desc = shorten(strip_markdown(tagline))
    home_body = rewrite_links(preamble, section_slugs).strip() + "\n\n"
    home_body += "## Sections\n\n"
    nav_items: list[tuple[str, str]] = [("Home", "index.md")]
    generated: list[str] = ["index.md"]

    platforms_body = None
    for section in sections:
        if section["title"] in SKIP_SECTION_PAGES:
            continue
        title, slug, body = section["title"], section["slug"], section["body"]
        if slug == "tracing-and-observability-platforms":
            platforms_body = body
        if slug == "contributing":
            page_body, desc = contributing_page(body, section_slugs)
        else:
            page_body = rewrite_links(body, section_slugs).strip() + "\n"
            desc = description_for(title, body)
        write(
            DOCS_DIR / f"{slug}.md",
            front_matter(title, desc) + f"# {title}\n\n" + page_body,
        )
        nav_items.append((title, f"{slug}.md"))
        generated.append(f"{slug}.md")
        home_body += f"- [{title}]({slug}.md)\n"
        if slug == COMPARISON_INSERT_AFTER:
            if platforms_body is None:
                raise SystemExit("platforms section body missing")
            cmp_body, cmp_desc = comparison_page(platforms_body, section_slugs)
            write(
                DOCS_DIR / f"{COMPARISON_SLUG}.md",
                front_matter(COMPARISON_TITLE, cmp_desc)
                + f"# {COMPARISON_TITLE}\n\n"
                + cmp_body,
            )
            nav_items.append((COMPARISON_TITLE, f"{COMPARISON_SLUG}.md"))
            generated.append(f"{COMPARISON_SLUG}.md")
            verified = comparison_verified_date(platforms_body)
            date_note = f" (last verified {verified})" if verified else ""
            home_body += f"- [{COMPARISON_TITLE}]({COMPARISON_SLUG}.md){date_note}\n"

    declined_title, declined_body, declined_desc = declined_page(section_slugs)
    write(
        DOCS_DIR / "declined.md",
        front_matter(declined_title, declined_desc) + f"# {declined_title}\n\n" + declined_body,
    )
    nav_items.append(("Declined", "declined.md"))
    generated.append("declined.md")
    section_slugs.add("declined")

    for heading, dest, text, desc in evidence_pages():
        page = front_matter(heading, desc) + f"# {heading}\n\n" + text + "\n"
        write(dest, page)
        generated.append(str(dest.relative_to(DOCS_DIR)))

    proof_title, proof_body, proof_desc = proof_page(section_slugs)
    write(
        DOCS_DIR / f"{PROOF_SLUG}.md",
        front_matter(proof_title, proof_desc) + f"# {proof_title}\n\n" + proof_body,
    )
    nav_items.append(("Proof", f"{PROOF_SLUG}.md"))
    generated.append(f"{PROOF_SLUG}.md")
    section_slugs.add(PROOF_SLUG)

    months = list_updates.collect()
    write(
        DOCS_DIR / "updates" / "index.md",
        front_matter(
            "List updates",
            "Adds and removals of list entries, generated from git history, DECLINED.md, and evidence/.",
        )
        + list_updates.index_markdown(months),
    )
    generated.append("updates/index.md")
    for month_id, month in months.items():
        dest = DOCS_DIR / "updates" / f"{month_id}.md"
        write(
            dest,
            front_matter(
                f"List updates, {month.title}",
                f"Entry adds and removals in {month.title}, from the README git history and DECLINED.md.",
            )
            + list_updates.month_markdown(month),
        )
        generated.append(f"updates/{month_id}.md")
    nav_items.append(("Updates", "updates/index.md"))

    verified = comparison_verified_date(platforms_body or "")
    home_body += "\n" + write_ups_section(verified)
    write(DOCS_DIR / "index.md", front_matter(SITE_NAME, homepage_desc) + home_body + "\n")

    write_mkdocs_yml(nav_items, homepage_desc)
    return generated


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    if not README_PATH.is_file():
        raise SystemExit(f"missing {README_PATH}")
    pages = build()
    print(f"Wrote {len(pages)} pages under {DOCS_DIR.relative_to(ROOT)}/")
    for name in pages:
        print(f"  {name}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
