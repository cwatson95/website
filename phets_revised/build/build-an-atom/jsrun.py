#!/usr/bin/env python3
"""jsrun.py — concatenate part files (plus an optional inline tail) and run them
under jsc (fast, for iterating) or osascript (the final pass).

    python3 jsrun.py jsc  p2_physics.js  _out/tail.js
    python3 jsrun.py osa  p2_physics.js  _out/tail.js

Always prepends a tiny prelude (jsc has no console.log) and the shared helpers
the parts assume (clamp, TAU, PI come from p1_utils.js).
"""
import io
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out")
JSC = "/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc"


def main():
    engine = sys.argv[1]
    parts = sys.argv[2:]
    body = "var console={log:print};\n" if engine == "jsc" else ""
    for p in parts:
        path = p if os.path.isabs(p) else os.path.join(HERE, p)
        body += io.open(path, encoding="utf-8").read() + "\n"
    tmp = os.path.join(OUT, "_jsrun.js")
    io.open(tmp, "w", encoding="utf-8").write(body)
    if engine == "jsc":
        r = subprocess.run([JSC, tmp], capture_output=True, text=True, timeout=1800)
    else:
        r = subprocess.run(["osascript", "-l", "JavaScript", tmp], capture_output=True,
                           text=True, timeout=1800)
    sys.stdout.write(r.stdout)
    sys.stderr.write(r.stderr)
    sys.exit(r.returncode)


if __name__ == "__main__":
    main()
