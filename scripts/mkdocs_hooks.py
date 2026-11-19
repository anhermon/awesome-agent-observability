"""MkDocs hooks for the generated site."""

from __future__ import annotations

import re

TABLE_RE = re.compile(r"<table>.*?</table>", re.S)


def on_page_content(html: str, **_kwargs) -> str:
    # Keep wide comparison tables usable on a 390px viewport.
    def wrap(match: re.Match[str]) -> str:
        table = match.group(0)
        wide = table.lower().count("<th") >= 4
        cls = "table-wrap table-wrap-wide" if wide else "table-wrap"
        hint = (
            '<p class="table-hint">This table scrolls sideways on a narrow screen.</p>'
            if wide
            else ""
        )
        return f'{hint}<div class="{cls}">{table}</div>'

    return TABLE_RE.sub(wrap, html)
