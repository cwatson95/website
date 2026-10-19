#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Draw the branching legend before the bar labels (so they can dodge it), and
floor 'draws substance' on the TOTAL op count instead of on fills alone — a
view that batches its drawing into strokes emits very few fills and the old
floor punished it for that (Known-bad: floor what the ops carry)."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p5_views.js", [
    ("""    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  const bw = Math.min(42, a.w / (nF - 1) * 0.34);""",
     """    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  /* the legend goes down FIRST so the bar labels can dodge its rectangle */
  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);
  const bw = Math.min(42, a.w / (nF - 1) * 0.34);"""),
    ("""  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);
  /* --- lifetimes (dropped on a narrow stage) --- */""",
     """  /* --- lifetimes (dropped on a narrow stage) --- */"""),
])

patch("p7_test.js", [
    ("""    const texts = c.ops.filter(o => o.op === 'text'), fills = c.ops.filter(o => o.op === 'fill');
    ok(fills.length >= minFills && texts.length >= 3,
      nm + ' ' + W + 'x' + H + ' draws substance (' + fills.length + ' fills, floor ' + minFills + ')');""",
     """    const texts = c.ops.filter(o => o.op === 'text');
    /* floor the TOTAL op count, not the fills: the standing-wave view draws one
       stroked polyline and four discs, and a fill floor tuned on the orbital
       cloud punishes it for batching (Known-bad) */
    ok(c.ops.length >= minFills && texts.length >= 3,
      nm + ' ' + W + 'x' + H + ' draws substance (' + c.ops.length + ' ops, floor ' + minFills + ')');"""),
])
