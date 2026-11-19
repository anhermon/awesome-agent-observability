#!/usr/bin/env python3
"""Print Markdown notes for a monthly GitHub Release from git history and DECLINED.md."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import list_updates


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("month", help="Pass month as YYYY-MM, for example 2026-11")
    args = parser.parse_args()
    if not list_updates.DATE_RE.match(args.month + "-01"):
        # YYYY-MM only
        if not __import__("re").fullmatch(r"\d{4}-\d{2}", args.month):
            raise SystemExit("month must be YYYY-MM")
    print(list_updates.release_notes(args.month), end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
