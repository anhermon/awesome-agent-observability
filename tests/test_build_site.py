import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, "scripts")
import build_site


README = Path("README.md").read_text(encoding="utf-8")


class Parse(unittest.TestCase):
    def setUp(self):
        self.preamble, self.tagline, self.sections = build_site.parse_readme(README)
        self.by_slug = {s["slug"]: s for s in self.sections}

    def test_expected_sections(self):
        titles = [s["title"] for s in self.sections]
        self.assertEqual(
            titles,
            [
                "Contents",
                "Where to start",
                "Recipes",
                "Standards and instrumentation",
                "Tracing and observability platforms",
                "Trace backends",
                "Coding-agent telemetry",
                "Evaluation and testing",
                "Agent and harness benchmarks",
                "Skill evaluation",
                "Guardrails and security",
                "Gateways and proxies",
                "MCP server testing",
                "Model Context Protocol",
                "Agent frameworks with built-in tracing",
                "Related lists",
                "Contributing",
            ],
        )

    def test_slugify(self):
        self.assertEqual(build_site.slugify("Where to start"), "where-to-start")
        self.assertEqual(
            build_site.slugify("Tracing and observability platforms"),
            "tracing-and-observability-platforms",
        )
        self.assertEqual(build_site.slugify("Model Context Protocol"), "model-context-protocol")

    def test_preamble_has_tagline(self):
        self.assertIn("Tools, standards, and benchmarks", self.preamble)
        self.assertNotIn("# Awesome Agent Observability", self.preamble)

    def test_comparison_table(self):
        body = self.by_slug["tracing-and-observability-platforms"]["body"]
        table = build_site.extract_markdown_table(body)
        self.assertIsNotNone(table)
        self.assertIn("Langfuse", table)
        self.assertIn("Agnost AI", table)
        self.assertIn("OTel GenAI conventions", table)

    def test_link_rewrite(self):
        slugs = {s["slug"] for s in self.sections if s["title"] != "Contents"}
        slugs.update({"contributing", "platform-comparison"})
        self.assertEqual(
            build_site.rewrite_url("CONTRIBUTING.md#requirements", slugs),
            "contributing.md#requirements",
        )
        self.assertEqual(
            build_site.rewrite_url("evidence/comparison-table.md", slugs),
            "platform-comparison.md#sources",
        )
        self.assertEqual(
            build_site.rewrite_url("DECLINED.md", slugs),
            "declined.md",
        )
        self.assertEqual(
            build_site.rewrite_url("evidence/recipes.md", slugs),
            "evidence/recipes.md",
        )
        self.assertEqual(build_site.rewrite_url("#where-to-start", slugs), "where-to-start.md")
        self.assertEqual(
            build_site.rewrite_url("https://github.com/anhermon/awesome-agent-observability", slugs),
            "https://github.com/anhermon/awesome-agent-observability",
        )


class Build(unittest.TestCase):
    def test_build_writes_required_pages(self):
        original_build = build_site.BUILD_DIR
        original_docs = build_site.DOCS_DIR
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            build_site.BUILD_DIR = root / "site-build"
            build_site.DOCS_DIR = build_site.BUILD_DIR / "docs"
            try:
                pages = build_site.build()
            finally:
                build_site.BUILD_DIR = original_build
                build_site.DOCS_DIR = original_docs
        self.assertIn("index.md", pages)
        self.assertIn("where-to-start.md", pages)
        self.assertIn("platform-comparison.md", pages)
        self.assertIn("contributing.md", pages)
        self.assertIn("declined.md", pages)
        self.assertIn("evidence/recipes.md", pages)
        self.assertNotIn("contents.md", pages)
        # Isolation used a temp BUILD_DIR; confirm the pages list is complete
        # even though the temp dir is gone. Re-run into a second temp to read files.
        with tempfile.TemporaryDirectory() as tmp:
            build_site.BUILD_DIR = Path(tmp) / "site-build"
            build_site.DOCS_DIR = build_site.BUILD_DIR / "docs"
            try:
                build_site.build()
                docs = build_site.DOCS_DIR
                home = (docs / "index.md").read_text(encoding="utf-8")
                self.assertIn("title:", home)
                self.assertIn("description:", home)
                comparison = (docs / "platform-comparison.md").read_text(encoding="utf-8")
                self.assertIn("Langfuse", comparison)
                self.assertIn('id="sources"', comparison)
                self.assertIn("Last verified", comparison)
                self.assertIn("`gen_ai.*`", comparison)
                self.assertIn("platform-comparison.md#sources", comparison)
                self.assertNotIn("reading genai.", comparison)
                platforms = (docs / "tracing-and-observability-platforms.md").read_text(
                    encoding="utf-8"
                )
                self.assertIn("platform-comparison.md#sources", platforms)
                contributing = (docs / "contributing.md").read_text(encoding="utf-8")
                self.assertIn("What belongs here", contributing)
                yml = (build_site.BUILD_DIR / "mkdocs.yml").read_text(encoding="utf-8")
                self.assertIn("site_url: https://anhermon.dev/awesome-agent-observability/", yml)
                self.assertIn("platform-comparison.md", yml)
                self.assertIn("proof.md", pages)
                self.assertIn("updates/index.md", pages)
                self.assertIn("updates/2026-11.md", pages)
                proof = (docs / "proof.md").read_text(encoding="utf-8")
                self.assertIn("We evaluated our own agents with tools from this list", proof)
                self.assertIn("2026-11-15", proof)
                self.assertNotIn("anhermon.github.io", proof)
                home = (docs / "index.md").read_text(encoding="utf-8")
                self.assertIn("## Write-ups", home)
                self.assertIn("last verified 2026-11-16", home)
                nov = (docs / "updates" / "2026-11.md").read_text(encoding="utf-8")
                self.assertIn("mcp-trace", nov)
                self.assertIn("Harbor", nov)
            finally:
                build_site.BUILD_DIR = original_build
                build_site.DOCS_DIR = original_docs


class EvidenceDescription(unittest.TestCase):
    def test_skips_version_opener(self):
        body = (
            "Version: `deepeval` 4.3.4.\n\n"
            "```bash\nuv pip install deepeval\n```\n\n"
            "Tool correctness ran in about 2 seconds with no model call.\n"
        )
        desc = build_site.evidence_description("DeepEval", body)
        self.assertNotIn("Version:", desc)
        self.assertIn("Tool correctness ran", desc)

    def test_prefers_claim_paragraph(self):
        body = (
            "Checked 2026-11-15 with promptfoo 0.120.19 from npm.\n\n"
            "Claim in the rewritten line: runs test cases against agent providers.\n"
        )
        desc = build_site.evidence_description("Promptfoo", body)
        self.assertEqual(desc, "Runs test cases against agent providers.")
        self.assertNotIn("Checked 2026-11-15", desc)

    def test_built_evidence_pages_are_not_version_stubs(self):
        import tempfile
        original_build = build_site.BUILD_DIR
        original_docs = build_site.DOCS_DIR
        with tempfile.TemporaryDirectory() as tmp:
            build_site.BUILD_DIR = Path(tmp) / "site-build"
            build_site.DOCS_DIR = build_site.BUILD_DIR / "docs"
            try:
                build_site.build()
                deepeval = (build_site.DOCS_DIR / "evidence" / "deepeval.md").read_text(
                    encoding="utf-8"
                )
                self.assertNotIn('description: "Version:', deepeval)
                self.assertIn("description:", deepeval)
                promptfoo = (build_site.DOCS_DIR / "evidence" / "promptfoo.md").read_text(
                    encoding="utf-8"
                )
                self.assertNotIn('description: "Checked 2026-11-15', promptfoo)
            finally:
                build_site.BUILD_DIR = original_build
                build_site.DOCS_DIR = original_docs


class DescriptionOverrides(unittest.TestCase):
    def test_overrides_name_real_evidence_files_and_fit_the_limit(self):
        for slug, text in build_site.DESCRIPTION_OVERRIDES.items():
            self.assertTrue((Path("evidence") / f"{slug}.md").is_file(), slug)
            self.assertLessEqual(len(text), 160, slug)


if __name__ == "__main__":
    unittest.main()
