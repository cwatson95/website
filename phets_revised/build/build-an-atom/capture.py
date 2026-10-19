#!/usr/bin/env python3
"""Build _out/cap_run.js and run it under osascript, then audit and rasterise.
Never pipe osascript through head/tail: a closed pipe kills it before it writes
display.json and the next audit silently reports the STALE file (Known-bad)."""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out")
TOOLS = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..", "projects", "simulations", "tools"))

body = io.open(os.path.join(OUT, "run.js"), encoding="utf-8").read()
body += io.open(os.path.join(TOOLS, "recorder.js"), encoding="utf-8").read()
body += io.open(os.path.join(HERE, "capture_tail_build-an-atom.js"), encoding="utf-8").read()
io.open(os.path.join(OUT, "cap_run.js"), "w", encoding="utf-8").write(body)

r = subprocess.run(["osascript", "-l", "JavaScript", "cap_run.js"], cwd=OUT,
                   capture_output=True, text=True, timeout=3600)
io.open(os.path.join(OUT, "cap.log"), "w", encoding="utf-8").write(r.stdout + r.stderr)
print(r.stdout[-2000:])
if r.returncode != 0:
    print(r.stderr[-3000:], file=sys.stderr)
    sys.exit(1)
for f in ["display.json", "display_narrow.json", "display_tiny.json"]:
    p = os.path.join(OUT, f)
    print(f, os.path.getsize(p), "bytes")
