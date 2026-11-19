import sys
import unittest
from pathlib import Path

sys.path.insert(0, "scripts")
import list_updates


SAMPLE_DECLINED = """# Declined and removed entries

## Declined

| Project | Date | Where | Reason |
| --- | --- | --- | --- |
| Speakeasy | 2026-09-28 | [#13](https://github.com/anhermon/awesome-agent-observability/pull/13) | Linked to a product marketing page (threshold 5). |

## Removed

| Project | Date | Where | Reason |
| --- | --- | --- | --- |
| Helicone | 2026-10-15 | [#29](https://github.com/anhermon/awesome-agent-observability/pull/29) | Maintenance mode only (threshold 3). |

## Closed pull requests whose project is listed

| Project | Closed | Reason |
| --- | --- | --- |
| Noveum Trace | [#15](https://example) | listed later |
"""


class ParseDeclined(unittest.TestCase):
    def test_rows_and_kinds(self):
        rows = list_updates.parse_declined(SAMPLE_DECLINED)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0].name, "Speakeasy")
        self.assertEqual(rows[0].kind, "declined")
        self.assertEqual(rows[1].name, "Helicone")
        self.assertEqual(rows[1].kind, "removed")

    def test_real_file_has_dated_rows(self):
        rows = list_updates.parse_declined()
        names = {r.name for r in rows}
        self.assertIn("mcp-trace", names)
        self.assertIn("ctxlens (`AgentPostmortem/Ctxlens`)", names)
        self.assertTrue(all(list_updates.DATE_RE.match(r.date) for r in rows))


class ParseEntries(unittest.TestCase):
    def test_skips_toc_anchors(self):
        text = "- [Where to start](#where-to-start)\n- [Langfuse](https://github.com/langfuse/langfuse) - tracing.\n"
        self.assertEqual(
            list_updates.parse_entries(text),
            {"Langfuse": "https://github.com/langfuse/langfuse"},
        )


class History(unittest.TestCase):
    def test_collect_known_months(self):
        if not list_updates.history_available():
            self.skipTest("git history too shallow")
        months = list_updates.collect()
        self.assertIn("2026-10", months)
        self.assertIn("2026-11", months)
        removed_oct = {c.name for c in months["2026-10"].removed}
        self.assertIn("Helicone", removed_oct)
        added_nov = {c.name for c in months["2026-11"].added}
        self.assertIn("Harbor", added_nov)
        self.assertIn("ranwhat", added_nov)
        removed_nov = {c.name for c in months["2026-11"].removed}
        self.assertIn("mcp-trace", removed_nov)
        self.assertIn("ctxlens", removed_nov)
        self.assertNotIn("AgentMeasure", removed_nov)
        self.assertNotIn("Verovo", added_nov)
        self.assertIn("AgentMeasure -> Verovo", {c.name for c in months["2026-11"].renamed})
        removed_jul = {c.name for c in months["2026-07"].removed}
        self.assertEqual(removed_jul, {"UpTrain"})

    def test_release_notes_mention_sources(self):
        if not list_updates.history_available():
            self.skipTest("git history too shallow")
        notes = list_updates.release_notes("2026-11")
        self.assertIn("Harbor", notes)
        self.assertIn("mcp-trace", notes)
        self.assertIn("DECLINED.md", notes)
        self.assertLessEqual(max(len(line) for line in notes.splitlines() if line.startswith("- ")), 400)


class EvidenceFor(unittest.TestCase):
    def test_known_files(self):
        self.assertEqual(list_updates.evidence_for("Harbor"), "evidence/harbor.md")
        self.assertEqual(list_updates.evidence_for("τ²-bench"), "evidence/tau2-bench.md")
        self.assertIsNone(list_updates.evidence_for("Langfuse"))
        self.assertIsNone(list_updates.evidence_for("Inspect"))


class GoneProjects(unittest.TestCase):
    def test_removed_projects_are_not_linked(self):
        if not list_updates.history_available():
            self.skipTest("git history too shallow")
        months = list_updates.collect()
        text = list_updates.month_markdown(months["2026-11"])
        self.assertNotIn("AgentPostmortem/Ctxlens)", text.split("## Declined")[0])
        self.assertIn("- ctxlens on 2026-11-15", text)


class Renames(unittest.TestCase):
    def test_same_url_and_formerly(self):
        prev = {"Opik (Comet)": "https://github.com/comet-ml/opik", "AgentMeasure": "https://github.com/a/AgentMeasure"}
        cur = {"Opik": "https://github.com/comet-ml/opik/", "Verovo": "https://github.com/a/Verovo"}
        lines = {"Verovo": "- [Verovo](https://github.com/a/Verovo) - Local CLI, formerly AgentMeasure."}
        self.assertEqual(
            list_updates.find_renames(prev, cur, lines),
            {"Opik (Comet)": "Opik", "AgentMeasure": "Verovo"},
        )
        self.assertEqual(list_updates.find_renames({"Gone": "https://x"}, {"New": "https://y"}, {}), {})



class KnownDeadLinks(unittest.TestCase):
    # Hosts/URLs that 404 today. CI's lychee job only checks README.md, so this
    # guards the generated Updates pages against regressing those links.
    KNOWN_DEAD = (
        "https://github.com/AgentPostmortem/Ctxlens",
    )

    def test_updates_pages_do_not_link_known_dead_urls(self):
        if not list_updates.history_available():
            self.skipTest("git history too shallow")
        import re

        months = list_updates.collect()
        pages = [list_updates.index_markdown(months)]
        pages.extend(list_updates.month_markdown(month) for month in months.values())
        hrefs = []
        for text in pages:
            hrefs.extend(re.findall(r"\[[^\]]*\]\((https?://[^)]+)\)", text))
        dead = [
            url
            for url in hrefs
            if any(url.rstrip("/") == dead.rstrip("/") or url.startswith(dead.rstrip("/") + "/")
                   for dead in self.KNOWN_DEAD)
        ]
        self.assertEqual(dead, [])


if __name__ == "__main__":
    unittest.main()
