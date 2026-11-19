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


if __name__ == "__main__":
    unittest.main()
