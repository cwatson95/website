#!/usr/bin/env python3
"""Pull the shared drawing-helper block out of the landed
models-of-the-hydrogen-atom build (which carries this collection's accumulated
layout fixes: the bottom-up stage layout, the label registry with its
half-pixel overlap rule, the #hint reservation, the axis clearances) into
_out/helpers.js.  Checked by grepping for the functions that must be there --
a cut that silently loses one of them does not fail until a view is drawn."""
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "..", "models-of-the-hydrogen-atom", "p4_views.js")
s = io.open(SRC, encoding="utf-8").read()
i = s.index("/* ==================")
k = s.index("function ring(ctx")
e = s.index("\n}\n", k) + 3
blk = s[i:e]
for want in ["usableW", "layout", "narrowStage", "AXIS_BOT", "nyFor", "drawCaption",
             "stackFit", "panelTitle", "LABEL_RECTS", "labelRect", "rectsHit",
             "label(", "labelIfClear", "disc(", "ring("]:
    if want not in blk:
        print("MISSING " + want, file=sys.stderr)
        sys.exit(1)
out = os.path.join(HERE, "_out", "helpers.js")
io.open(out, "w", encoding="utf-8").write(blk)
print("%d lines extracted from %s" % (len(blk.splitlines()), os.path.relpath(SRC, HERE)))
