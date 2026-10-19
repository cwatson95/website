#!/usr/bin/env python3
"""Land verified remakes from the worktree into the main checkout.

    python3 land_one.py <stem> [<stem> ...]

For each stem: copy <stem>.html and build/<stem>/ (minus _out/) from the
worktree to the main checkout's docs/phets_revised/, check every copied file
byte for byte, insert build/<stem>/changelog_entry.md into BOTH checkouts'
CHANGELOG.md above the newest dated entry (never rewriting existing text),
then run verify_one.py FROM THE MAIN CHECKOUT. The first landing also brings
the kit (CHANGELOG.md, build/.gitignore, BRIEF.md, _survey/, _tools/).
Nothing is committed in the main checkout.
"""
import filecmp
import io
import os
import re
import shutil
import subprocess
import sys

WT = "/Users/cooper/coding/Agent/.claude/worktrees/phets-revised"
MAIN = "/Users/cooper/coding/Agent"
REL = os.path.join("docs", "phets_revised")
KIT = ["CHANGELOG.md", "build/.gitignore", "build/BRIEF.md", "build/_survey", "build/_tools"]


SKIP_DIRS = {"_out", "__pycache__"}          # must match the copytree ignore below


def same_tree(a, b):
    for dp, dn, fn in os.walk(a):
        dn[:] = [d for d in dn if d not in SKIP_DIRS]
        for f in fn:
            pa = os.path.join(dp, f)
            pb = os.path.join(b, os.path.relpath(pa, a))
            if not (os.path.isfile(pb) and filecmp.cmp(pa, pb, shallow=False)):
                return False, pa
    return True, None


def copy_path(rel):
    src, dst = os.path.join(WT, REL, rel), os.path.join(MAIN, REL, rel)
    if os.path.isdir(src):
        shutil.copytree(src, dst, dirs_exist_ok=True, ignore=shutil.ignore_patterns("_out", "__pycache__"))
        ok, bad = same_tree(src, dst)
        assert ok, "copy differs: " + bad
    else:
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        assert filecmp.cmp(src, dst, shallow=False), "copy differs: " + rel


def insert_entry(log, entry):
    s = io.open(log, encoding="utf-8").read()
    head = entry.splitlines()[0].strip()
    if head in s:
        return "already there"
    m = re.search(r"^## 20\d\d-\d\d-\d\d", s, flags=re.M)
    assert m, "no dated entry in " + log
    new = s[:m.start()] + entry.rstrip() + "\n\n" + s[m.start():]
    assert new.replace(entry.rstrip() + "\n\n", "", 1) == s
    io.open(log, "w", encoding="utf-8").write(new)
    return "inserted"


def main():
    stems = sys.argv[1:]
    assert stems, __doc__
    if not os.path.exists(os.path.join(MAIN, REL, "CHANGELOG.md")):
        for rel in KIT:
            copy_path(rel)
        print("kit landed:", ", ".join(KIT))
    else:  # keep the landed tools and brief current (only this job edits them)
        copy_path("build/_tools")
        copy_path("build/BRIEF.md")
    for stem in stems:
        html = stem + ".html"
        bdir = os.path.join("build", stem)
        assert os.path.isfile(os.path.join(WT, REL, html)), "not built: " + html
        entry_p = os.path.join(WT, REL, bdir, "changelog_entry.md")
        assert os.path.isfile(entry_p), "no changelog_entry.md for " + stem
        copy_path(html)
        copy_path(bdir)
        entry = io.open(entry_p, encoding="utf-8").read()
        for root in (WT, MAIN):
            print("  %-6s CHANGELOG: %s" % ("wt" if root == WT else "main", insert_entry(os.path.join(root, REL, "CHANGELOG.md"), entry)))
        print("landed", stem)
    r = subprocess.run([sys.executable, os.path.join(WT, REL, "build", "_tools", "verify_one.py"), MAIN] + stems)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
