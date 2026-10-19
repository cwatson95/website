#!/usr/bin/env python3
"""Per-stem finishing status: sweep summary, changelog entry, captured PNGs.

    python3 status.py <stem> [<stem> ...]
"""
import os
import re
import sys

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SUM = re.compile(r"^(\d+) caught, (\d+) survived, (\d+) skipped", re.M)
PLACEHOLDER = re.compile(r"\b(TODO|TBD|FIXME|XXX|PLACEHOLDER)\b")

for stem in sys.argv[1:]:
    d = os.path.join(BUILD, stem)
    if not os.path.isdir(d):
        print("%-36s NO BUILD DIR" % stem)
        continue
    best, pngs = None, 0
    for dp, dn, fn in os.walk(d):
        for f in fn:
            p = os.path.join(dp, f)
            if f.endswith(".png"):
                pngs += 1
            elif f.endswith((".txt", ".log", ".md")) and os.path.getsize(p) < 4_000_000:
                try:
                    hits = SUM.findall(open(p, encoding="utf-8", errors="replace").read())
                except OSError:
                    continue
                if hits:
                    best = hits[-1]          # last summary in that file
    cl = os.path.join(d, "changelog_entry.md")
    if os.path.isfile(cl):
        txt = open(cl, encoding="utf-8").read()
        head = txt.splitlines()[0][:60] if txt.strip() else "(empty)"
        ph = "PLACEHOLDERS" if PLACEHOLDER.search(txt) else "clean"
        entry = "%d lines, %s, %s" % (len(txt.splitlines()), ph, head)
    else:
        entry = "MISSING"
    sweep = ("%s caught / %s survived / %s skipped" % best) if best else "NONE FOUND"
    print("%-36s %-40s png:%-4d %s" % (stem, sweep, pngs, entry))
