#!/usr/bin/env python3
"""Insert a changelog entry file into BOTH checkouts' docs/phets_revised/CHANGELOG.md.

    python3 insert_entry.py <entry.md>

Same guarded insertion land_one.py uses: above the newest dated entry, never
rewriting existing text, and a no-op if the heading is already there.
"""
import io
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from land_one import MAIN, REL, WT, insert_entry  # noqa: E402

entry = io.open(os.path.abspath(sys.argv[1]), encoding="utf-8").read()
for root in (WT, MAIN):
    log = os.path.join(root, REL, "CHANGELOG.md")
    print("%-6s %s: %s" % ("wt" if root == WT else "main", os.path.basename(log),
                           insert_entry(log, entry)))
