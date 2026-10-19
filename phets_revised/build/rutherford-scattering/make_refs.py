#!/usr/bin/env python3
"""Turn refvals.txt into p7_refs.js — a JS map from the label derive.py printed
to the value it printed.  Nothing is transcribed by hand: hand-typing a table
is the same failure as quoting one from memory (Known-bad list), so the numbers
the suite asserts against are emitted by the arithmetic that produced them."""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
src = io.open(os.path.join(HERE, "refvals.txt"), encoding="utf-8").read()

NUM = re.compile(r"^(.*\S)\s{2,}(\S.*)$")
ref = {}
sect = ""
ctx = ""
for line in src.splitlines():
    if line.startswith("====="):
        sect = line.strip("= ").strip()
        ctx = ""
        continue
    m = NUM.match(line)
    if not m:
        continue
    key, val = m.group(1).rstrip(), m.group(2).strip()
    # derive.py indents a line that belongs to the one above it; make that
    # relationship part of the key, or '  emissions 2->1' collides eight times
    if key.startswith("  "):
        key = ctx + " :: " + key.strip()
    else:
        ctx = key
    try:
        v = float(val)
        if v != v or v in (float("inf"), float("-inf")):
            v = val                      # 'inf' / 'nan' stay as the printed word
        elif v == int(v) and abs(v) < 1e15 and "." not in val and "e" not in val:
            v = int(v)
    except ValueError:
        v = val
    if key in ref and ref[key] != v:
        key = key + " #2"
        n = 2
        while key in ref:
            n += 1
            key = m.group(1).rstrip() + " #%d" % n
    ref[key] = v

out = ["/* p7_refs.js — every reference value the suite asserts against, emitted",
       "   verbatim from build/rutherford-scattering/refvals.txt by",
       "   make_refs.py.  Labelled (derive) in the assertions; refvals.txt is the",
       "   printed output of derive.py (scipy.constants CODATA 2022,",
       "   scipy.integrate.quad and solve_ivp, scipy.optimize.brentq and",
       "   minimize_scalar, and a bit-for-bit Python mulberry32).",
       "   Do not edit by hand. */",
       "const REF = " + json.dumps(ref, indent=0, ensure_ascii=False).replace("\n", "\n") + ";",
       "function R(k){ if(!(k in REF)) throw new Error('no reference value: ' + k); return REF[k]; }",
       ""]
io.open(os.path.join(HERE, "p7_refs.js"), "w", encoding="utf-8").write("\n".join(out))
print("%d reference values" % len(ref))
