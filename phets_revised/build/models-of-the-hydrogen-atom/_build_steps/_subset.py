#!/usr/bin/env python3
"""Write _out/mutants_<name>.json holding just the labels given on the command
line, so a survivor can be re-checked in seconds instead of re-running the
whole sweep."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
M = json.load(io.open(os.path.join(HERE, "mutants.json"), encoding="utf-8"))
name = sys.argv[1]
keep = set(sys.argv[2:])
sub = [x for x in M if x[0] in keep]
out = os.path.join(HERE, "_out", "mutants_%s.json" % name)
io.open(out, "w", encoding="utf-8").write(json.dumps(sub, indent=1, ensure_ascii=False))
print("%d mutants -> %s" % (len(sub), out))
missing = keep - {x[0] for x in M}
if missing:
    print("NOT FOUND:", sorted(missing))
    sys.exit(1)
