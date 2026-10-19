#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Narrow-stage rates view: the legends sat on the bars.

legendAuto dodges POLY_SEGS, and a bar is a fillRect, which is not in it — so
on an 820 px stage the branching legend landed on the bars it was labelling.
Register each bar's outline before the legend goes down, and keep the order
legend-then-labels so the bar values can still dodge the legend.  Also shorten
the 2s note on a narrow panel, where it ran past its own frame.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "p5_views.js")
s = io.open(p, encoding="utf-8").read()


def sub(old, new):
    global s
    assert s.count(old) == 1, ("%r appears %d times" % (old[:70], s.count(old)))
    s = s.replace(old, new)


# --- the branching panel: register the bars, then the legend, then draw ----
sub("""  /* the legend goes down FIRST so the bar labels can dodge its rectangle */
  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);
  const bw = Math.min(42, a.w / (nF - 1) * 0.34);
  for(let i = 0; i < cats.length; i++){
    const np = cats[i];
    const X = a.x + a.w * (np - 0.5) / (nF - 1);
    const f1 = tb.frac[i], f2 = phetMap[np] || 0;""",
    """  /* the bars are fillRects, which legendAuto cannot see (it dodges POLY_SEGS),
     so their outlines go into POLY_SEGS BEFORE the legend is placed; the
     legend still goes down before the bar VALUES, so those can dodge it */
  const bw = Math.min(42, a.w / (nF - 1) * 0.34);
  for(let i = 0; i < cats.length; i++){
    const np = cats[i];
    const X = a.x + a.w * (np - 0.5) / (nF - 1);
    const f1 = tb.frac[i], f2 = phetMap[np] || 0;
    for(const [xx, ff] of [[X - bw - 2, f1], [X + 2, f2]]){
      if(!(ff > 0)) continue;
      POLY_SEGS.push(xx, a.y1 - a.h * ff, xx + bw, a.y1 - a.h * ff);
      POLY_SEGS.push(xx, a.y1 - a.h * ff, xx, a.y1);
      POLY_SEGS.push(xx + bw, a.y1 - a.h * ff, xx + bw, a.y1);
    }
  }
  legendAuto(ctx, a, [[COL.pos, 'real hydrogen'], [COL.ref, 'PhET’s weights']]);
  for(let i = 0; i < cats.length; i++){
    const np = cats[i];
    const X = a.x + a.w * (np - 0.5) / (nF - 1);
    const f1 = tb.frac[i], f2 = phetMap[np] || 0;""")

# --- the ensemble panel: the same treatment --------------------------------
sub("""  /* the legend goes down before the z labels, so they dodge it rather than
     landing on it (labelIfClear checks LEGEND_RECTS too) */
  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);
  const bw2 = Math.min(46, b.w / Math.max(1, nF - 1) * 0.3);""",
    """  const bw2 = Math.min(46, b.w / Math.max(1, nF - 1) * 0.3);
  for(const r of rows){
    const X = b.x + b.w * (r.n - 0.5) / Math.max(1, nF - 1);
    const hf = b.h * clamp(r.f / yTop, 0, 1);
    POLY_SEGS.push(X - bw2 / 2, b.y1 - hf, X + bw2 / 2, b.y1 - hf);
    POLY_SEGS.push(X - bw2 / 2, b.y1 - hf, X - bw2 / 2, b.y1);
    POLY_SEGS.push(X + bw2 / 2, b.y1 - hf, X + bw2 / 2, b.y1);
  }
  /* the legend goes down before the z labels, so they dodge it rather than
     landing on it (labelIfClear checks LEGEND_RECTS too) */
  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);""")

# --- the 2s note, shortened on a narrow panel ------------------------------
sub("""  label(ctx, c.x + 8, c.y + 5, '2s has no allowed drop: \\u03c4 = \\u221e, plotted on the top rule',
    COL.ref, '10px -apple-system, sans-serif', 'left', 'top');""",
    """  label(ctx, c.x + 8, c.y + 5, c.w < 330 ? '2s: \\u03c4 = \\u221e, on the top rule'
    : '2s has no allowed drop: \\u03c4 = \\u221e, plotted on the top rule',
    COL.ref, '10px -apple-system, sans-serif', 'left', 'top');""")

io.open(p, "w", encoding="utf-8").write(s)
print("p5_views.js patched")
