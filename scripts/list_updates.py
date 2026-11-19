"""Derive list adds and removals from git history and DECLINED.md.

This is the source for the Updates pages and for monthly release notes.
Do not hand-maintain a second changelog.
"""

from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REPO_URL = "https://github.com/anhermon/awesome-agent-observability"
ENTRY_RE = re.compile(r"^- \[([^\]]+)\]\(([^)]+)\)", re.M)
PR_RE = re.compile(r"#(\d+)")
DATE_RE = re.compile(r"^\d{4}-\d{2}-\d{2}$")


@dataclass
class Change:
    name: str
    url: str
    sha: str
    date: str
    subject: str
    gone: bool = False  # the project was later removed, so do not link its URL

    @property
    def pr(self) -> str | None:
        match = PR_RE.search(self.subject)
        return match.group(1) if match else None

    @property
    def commit_url(self) -> str:
        return f"{REPO_URL}/commit/{self.sha}"

    @property
    def pr_url(self) -> str | None:
        return f"{REPO_URL}/pull/{self.pr}" if self.pr else None


@dataclass
class Decline:
    name: str
    date: str
    where: str
    reason: str
    kind: str  # declined | removed


@dataclass
class Month:
    id: str  # YYYY-MM
    added: list[Change] = field(default_factory=list)
    removed: list[Change] = field(default_factory=list)
    renamed: list[Change] = field(default_factory=list)  # name is "old -> new"
    declined: list[Decline] = field(default_factory=list)

    @property
    def title(self) -> str:
        year, month = self.id.split("-")
        names = (
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December",
        )
        return f"{names[int(month) - 1]} {year}"


def parse_entries(text: str) -> dict[str, str]:
    entries: dict[str, str] = {}
    for match in ENTRY_RE.finditer(text):
        name, url = match.group(1), match.group(2)
        if url.startswith("#"):
            continue
        entries[name] = url
    return entries


def parse_entry_lines(text: str) -> dict[str, str]:
    """Entry name to its full README line, used to spot "formerly X" renames."""
    lines: dict[str, str] = {}
    for line in text.splitlines():
        match = re.match(r"^- \[([^\]]+)\]\(([^)]+)\)", line)
        if match and not match.group(2).startswith("#"):
            lines[match.group(1)] = line
    return lines


def _git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True)


def history_available() -> bool:
    if not (ROOT / ".git").exists():
        return False
    try:
        count = int(_git("rev-list", "--count", "HEAD").strip())
    except (subprocess.CalledProcessError, ValueError):
        return False
    return count >= 2


def read_readme_history() -> list[tuple[str, str, str, dict[str, str], dict[str, str]]]:
    """Oldest-first first-parent snapshots of README entries."""
    log = _git("log", "--first-parent", "--format=%H %ad %s", "--date=short", "--", "README.md")
    rows = []
    for line in log.splitlines():
        sha, date, *rest = line.split(" ", 2)
        subject = rest[0] if rest else ""
        text = _git("show", f"{sha}:README.md")
        rows.append((sha, date, subject, parse_entries(text), parse_entry_lines(text)))
    rows.reverse()
    return rows


def find_renames(prev: dict[str, str], cur: dict[str, str], lines: dict[str, str]) -> dict[str, str]:
    """Map old entry name to new name when the same project was renamed.

    A rename is the same URL under a new name, or a new entry whose README line
    says "formerly <old name>". Everything else that disappears is a removal.
    """
    renamed: dict[str, str] = {}
    for old in set(prev) - set(cur):
        for new in set(cur) - set(prev):
            same_url = prev[old].rstrip("/") == cur[new].rstrip("/")
            formerly = re.search(rf"\bformerly\s+{re.escape(old)}\b", lines.get(new, ""), re.I)
            if same_url or formerly:
                renamed[old] = new
    return renamed


def changes_by_month(snapshots: list[tuple] | None = None) -> dict[str, Month]:
    if snapshots is None:
        snapshots = read_readme_history()
    months: dict[str, Month] = {}
    prev: dict[str, str] = {}
    for sha, date, subject, cur, *rest in snapshots:
        month_id = date[:7]
        month = months.setdefault(month_id, Month(id=month_id))
        renamed = find_renames(prev, cur, rest[0] if rest else {})
        for old, new in sorted(renamed.items()):
            month.renamed.append(Change(f"{old} -> {new}", cur[new], sha, date, subject))
        for name in sorted(set(cur) - set(prev) - set(renamed.values())):
            month.added.append(Change(name, cur[name], sha, date, subject))
        for name in sorted(set(prev) - set(cur) - set(renamed)):
            month.removed.append(Change(name, prev.get(name, ""), sha, date, subject))
        prev = cur
    return months


def parse_declined(text: str | None = None) -> list[Decline]:
    if text is None:
        text = (ROOT / "DECLINED.md").read_text(encoding="utf-8")
    kind = None
    rows: list[Decline] = []
    for line in text.splitlines():
        if line.startswith("## Declined"):
            kind = "declined"
            continue
        if line.startswith("## Removed"):
            kind = "removed"
            continue
        if line.startswith("## "):
            kind = None
            continue
        if kind is None or not line.startswith("|") or line.startswith("| ---") or line.startswith("| Project"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if kind == "declined" and len(cells) >= 4:
            name, date, where, reason = cells[0], cells[1], cells[2], cells[3]
        elif kind == "removed" and len(cells) >= 4:
            name, date, where, reason = cells[0], cells[1], cells[2], cells[3]
        else:
            continue
        if not DATE_RE.match(date):
            continue
        rows.append(Decline(name=name, date=date, where=where, reason=reason, kind=kind))
    return rows


def months_with_declines(months: dict[str, Month], declines: list[Decline] | None = None) -> dict[str, Month]:
    if declines is None:
        declines = parse_declined()
    for item in declines:
        month = months.setdefault(item.date[:7], Month(id=item.date[:7]))
        # Removals already appear in git history when the README dropped them.
        # Still attach the DECLINED row so the reason can be cited.
        month.declined.append(item)
    return months


def evidence_for(name: str) -> str | None:
    """Return an evidence/ path if a matching file exists."""
    ev = ROOT / "evidence"
    if not ev.is_dir():
        return None
    slug = re.sub(r"[^\w]+", "-", name.lower()).strip("-")
    aliases = {
        "claude-code-monitoring": "claude-code-monitoring",
        "inspect-evals": "inspect-evals",
        "inspect-swe": "inspect-swe",
        "mcp-conformance": "mcp-conformance",
        "mcp-universe": "mcp-universe",
        "mcp-atlas": "mcp-atlas",
        "mcpmark": "mcpmark",
        "tau2-bench": "tau2-bench",
        "τ²-bench": "tau2-bench",
        "swe-bench": "swe-bench",
        "ai-observer": "ai-observer",
        "skill-creator": "skill-creator",
        "coder-eval": "coder-eval",
        "ccusage": "ccusage",
        "verovo": "verovo",
        "bfcl": "bfcl",
        "promptfoo": "promptfoo",
        "harbor": "harbor",
        "deepeval": "deepeval",
        "pyrit": "pyrit",
        "purplellama": "purplellama",
        "langsmith": "langsmith",
    }
    key = aliases.get(slug, slug)
    path = ev / f"{key}.md"
    if path.is_file():
        return f"evidence/{path.name}"
    return None


def github_blob(path: str) -> str:
    return f"{REPO_URL}/blob/main/{path}"


def _change_line(change: Change, include_evidence: bool = True, prefix: str = "", link_project: bool = True) -> str:
    # Removed projects often no longer exist upstream, so their lines do not link the project URL.
    label = f"[{change.name}]({change.url})" if link_project and not change.gone else change.name
    parts = [f"- {label} on {change.date}, recorded in [{change.sha[:7]}]({change.commit_url})"]
    if change.pr:
        parts.append(f" ([{'#' + change.pr}]({change.pr_url}))")
    parts.append(".")
    if include_evidence:
        ev = evidence_for(change.name)
        if ev:
            parts.append(f" Hands-on notes: [`{ev}`]({prefix}{ev}).")
    return "".join(parts)


def _decline_line(item: Decline, prefix: str = "") -> str:
    declined = f"{prefix}declined.md"
    where = item.where.rstrip(".")
    return (
        f"- {item.name} ({item.date}), cited in [DECLINED.md]({declined}): {item.reason} "
        f"({where})."
    )


def month_markdown(month: Month, prefix: str = "../") -> str:
    declined = f"{prefix}declined.md"
    evidence_index = f"{prefix}evidence/index.md"
    lines = [
        f"# List updates, {month.title}",
        "",
        "This page is generated from the git history of the README, from "
        f"[DECLINED.md]({declined}), and from [`evidence/`]({evidence_index}). "
        "It lists only entry adds, removals, and renames those sources show. "
        "Description-only edits are omitted.",
        "",
    ]
    if month.added:
        lines.append("## Added")
        lines.append("")
        for change in month.added:
            lines.append(_change_line(change, prefix=prefix))
        lines.append("")
    if month.renamed:
        lines.append("## Renamed")
        lines.append("")
        lines.append("Same project under a new name; these are not removals.")
        lines.append("")
        for change in month.renamed:
            lines.append(f"- {change.name} on {change.date}, recorded in [{change.sha[:7]}]({change.commit_url})"
                         + (f" ([#{change.pr}]({change.pr_url}))" if change.pr else "") + ".")
        lines.append("")
    if month.removed:
        lines.append("## Removed")
        lines.append("")
        for change in month.removed:
            lines.append(_change_line(change, include_evidence=False, prefix=prefix, link_project=False))
        lines.append("")
    declined_only = [d for d in month.declined if d.kind == "declined"]
    removed_reasons = [d for d in month.declined if d.kind == "removed"]
    if declined_only:
        lines.append("## Declined (not added)")
        lines.append("")
        for item in declined_only:
            lines.append(_decline_line(item, prefix=prefix))
        lines.append("")
    if removed_reasons:
        lines.append("## Removal reasons")
        lines.append("")
        lines.append(f"From [DECLINED.md]({declined}):")
        lines.append("")
        for item in removed_reasons:
            lines.append(_decline_line(item, prefix=prefix))
        lines.append("")
    if not (month.added or month.removed or month.renamed or month.declined):
        lines.append("No entry adds or removals are recorded for this month.")
        lines.append("")
    return "\n".join(lines)


def index_markdown(months: dict[str, Month]) -> str:
    lines = [
        "# List updates",
        "",
        "Adds, removals, and renames of list entries, generated from the git history of "
        "the README, from [DECLINED.md](../declined.md), and from "
        "[`evidence/`](../evidence/index.md). "
        "Each month is a dated page. These notes are also the source for a "
        f"monthly GitHub Release; see [RELEASING.md]({github_blob('RELEASING.md')}).",
        "",
    ]
    for month_id in sorted(months, reverse=True):
        month = months[month_id]
        n_add, n_rem = len(month.added), len(month.removed)
        summary = []
        if n_add:
            summary.append(f"{n_add} added")
        if month.renamed:
            summary.append(f"{len(month.renamed)} renamed")
        if n_rem:
            summary.append(f"{n_rem} removed")
        if any(d.kind == "declined" for d in month.declined):
            n_dec = sum(1 for d in month.declined if d.kind == "declined")
            summary.append(f"{n_dec} declined")
        extra = f" ({', '.join(summary)})" if summary else ""
        lines.append(f"- [{month.title}]({month_id}.md){extra}")
    lines.append("")
    return "\n".join(lines)


def release_notes(month_id: str, months: dict[str, Month] | None = None) -> str:
    if months is None:
        if not history_available():
            raise SystemExit("git history is not available; cannot write release notes")
        months = months_with_declines(changes_by_month())
    if month_id not in months:
        raise SystemExit(f"no adds or removals recorded for {month_id}")
    month = months[month_id]
    lines = [
        f"Monthly pass {month.title}.",
        "",
        "Adds and removals below are taken from the git history of the README "
        "and from DECLINED.md. See the list site's updates page for links.",
        "",
    ]
    if month.added:
        lines.append("Added:")
        for change in month.added:
            ref = f"#{change.pr}" if change.pr else change.sha[:7]
            lines.append(f"- {change.name} ({change.date}, {ref})")
        lines.append("")
    if month.renamed:
        lines.append("Renamed:")
        for change in month.renamed:
            ref = f"#{change.pr}" if change.pr else change.sha[:7]
            lines.append(f"- {change.name} ({change.date}, {ref})")
        lines.append("")
    if month.removed:
        lines.append("Removed:")
        for change in month.removed:
            ref = f"#{change.pr}" if change.pr else change.sha[:7]
            lines.append(f"- {change.name} ({change.date}, {ref})")
        lines.append("")
    declined_only = [d for d in month.declined if d.kind == "declined"]
    if declined_only:
        lines.append("Declined (not added):")
        for item in declined_only:
            lines.append(f"- {item.name} ({item.date}): {item.reason}")
        lines.append("")
    lines.append("Sharing outside GitHub stays with the maintainer.")
    lines.append("")
    return "\n".join(lines)


def mark_gone(months: dict[str, Month]) -> dict[str, Month]:
    removed = {c.name for m in months.values() for c in m.removed}
    for m in months.values():
        for c in m.added:
            c.gone = c.name in removed
    return months


def collect() -> dict[str, Month]:
    if not history_available():
        raise SystemExit(
            "git history is too shallow to generate the updates pages; "
            "check out the full history (fetch-depth: 0)"
        )
    return mark_gone(months_with_declines(changes_by_month()))
