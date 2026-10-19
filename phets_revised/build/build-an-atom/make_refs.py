#!/usr/bin/env python3
"""Turn _out/refvals.txt (which derive.py writes as JSON) into p7_refs.js.

Nothing is transcribed by hand: hand-typing a table is the same failure as
quoting one from memory (Known-bad list), so every number the suite asserts
against is emitted by the arithmetic that produced it."""
import io
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
ref = json.load(io.open(os.path.join(HERE, "_out", "refvals.txt"), encoding="utf-8"))

out = ["/* p7_refs.js — every reference value the suite asserts against, emitted",
       "   verbatim from build/build-an-atom/_out/refvals.txt by make_refs.py.",
       "   Labelled (derive) in the assertions; refvals.txt is the printed output",
       "   of derive.py, which reads PhET's tables out of the minified original,",
       "   an independent nuclide table out of projects/simulations/",
       "   periodic_table.html, and its constants from scipy.constants",
       "   (CODATA 2022).  Do not edit by hand. */",
       "const REF = " + json.dumps(ref, indent=0, sort_keys=True, ensure_ascii=False) + ";",
       "function R(k){ if(!(k in REF)) throw new Error('no reference value: ' + k); return REF[k]; }",
       ""]
io.open(os.path.join(HERE, "p7_refs.js"), "w", encoding="utf-8").write("\n".join(out))
print("%d reference values" % len(ref))
