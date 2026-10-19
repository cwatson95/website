#!/usr/bin/env python3
"""Re-run a landed sim's mutation sweep in isolation and report survivors.

    python3 resweep.py <stem> [<stem> ...]

Why: on 2026-09-18 one build agent killed stray `osascript` processes by
matching `_mutant.js`, and at least two of them belonged to OTHER agents'
sweeps. `mutate.py` counts a killed run as a caught mutant, so any sweep that
was live then may hold false kills — which is exactly how a real survivor
hides. This re-runs the sweep from the shipped file, one sim at a time, each
in its own scratch directory (mutate.py writes `_mutant.js` next to the html
it tests, so a private directory is what keeps two sweeps apart).

Prints, per stem, caught/total and every survivor, and compares the count with
the build's own mutation log if one is there.
"""
import io
import os
import re
import shutil
import subprocess
import sys
import time

WT = "/Users/cooper/coding/Agent/.claude/worktrees/phets-revised"
REL = os.path.join("docs", "phets_revised")
MUTATE = os.path.join(WT, "projects", "simulations", "tools", "mutate.py")


def resweep(stem):
    bdir = os.path.join(WT, REL, "build", stem)
    html = os.path.join(WT, REL, stem + ".html")
    muts = os.path.join(bdir, "mutants.json")
    ui = os.path.join(bdir, "ui_drive_%s.js" % stem)
    if not os.path.isfile(ui):
        cands = [f for f in os.listdir(bdir) if f.startswith("ui_drive") and f.endswith(".js")]
        ui = os.path.join(bdir, cands[0]) if len(cands) == 1 else ui
    for p in (html, muts, ui):
        if not os.path.isfile(p):
            print("%-34s SKIP (missing %s)" % (stem, os.path.basename(p)))
            return None
    scratch = os.path.join(bdir, "_out", "resweep")
    shutil.rmtree(scratch, ignore_errors=True)
    os.makedirs(scratch)
    copy = os.path.join(scratch, stem + ".html")
    shutil.copyfile(html, copy)
    t0 = time.time()
    r = subprocess.run([sys.executable, MUTATE, copy, muts, ui],
                       capture_output=True, text=True, timeout=36000)
    out = r.stdout + r.stderr
    io.open(os.path.join(scratch, "resweep.log"), "w", encoding="utf-8").write(out)
    # mutate.py marks a survivor with the word SURVIVED; its closing line reads
    # "<n> caught, <m> survived, <k> skipped" — don't match that as a survivor.
    surv = [l.strip() for l in out.splitlines() if re.search(r"\bSURVIVED\b", l)]
    m = re.search(r"(\d+)\s+caught,\s*(\d+)\s+survived,\s*(\d+)\s+skipped", out)
    print("%-34s %s  (%.0f min, exit %d)" % (stem, m.group(0) if m else "NO SUMMARY LINE",
                                             (time.time() - t0) / 60, r.returncode))
    for s in surv:
        print("      SURVIVOR: " + s[:110])
    old = os.path.join(bdir, "mutation_log.txt")
    if os.path.isfile(old):
        o = io.open(old, encoding="utf-8", errors="replace").read()
        mo = re.search(r"(\d+)\s*/\s*(\d+)\s+caught", o) or re.search(r"caught\s+(\d+)\s*/\s*(\d+)", o)
        print("      build's own log said: %s" % (mo.group(0) if mo else "?"))
    return surv


if __name__ == "__main__":
    bad = 0
    for stem in sys.argv[1:]:
        s = resweep(stem)
        bad += len(s or [])
    print("total survivors across re-swept sims:", bad)
