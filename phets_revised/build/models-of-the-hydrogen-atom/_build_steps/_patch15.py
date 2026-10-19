#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The narrow-stage audit findings.

  * The label registry tolerated a 2 px overlap while tools/audit.py fails on
    half a pixel — and the audit's threshold is the real one, because a 2 px
    graze IS visible antialiased smear on canvas (Known-bad).  Tightened to
    0.5 px, which is what let "2->1" sit on "3->1" in the Lyman crowd at 820 px.
  * The branching bars' value labels went through label(), not labelIfClear(),
    so two adjacent bars printed "0.19" on top of "0.13".
  * The caption ran the full width of the stage and therefore under the
    floating readout at every size below 1400 px.  It is now capped at the
    usable width, which is exactly the part of the stage the readout does not
    cover.
"""
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


patch("p4_views.js", [
    ("""function rectsHit(a, b){
  return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > 2
      && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > 2;
}""",
     """/* half a pixel, which is tools/audit.py's threshold.  A 2 px tolerance passed
   the inline sweep and failed the audit on the same picture (Known-bad), and a
   2 px graze is visible antialiased smear on canvas. */
function rectsHit(a, b){
  return Math.min(a.x + a.w, b.x + b.w) - Math.max(a.x, b.x) > 0.5
      && Math.min(a.y + a.h, b.y + b.h) - Math.max(a.y, b.y) > 0.5;
}"""),
    ("""  const f = fitCaption(ctx, W, H - HINT_H, full, short, W - 40,
                       stageTop() + (narrowStage(W) ? 300 : 120));""",
     """  /* the caption is capped at the USABLE width, which is the part of the stage
     the floating readout does not cover; at the full stage width it ran under
     the readout at every size below 1400 px */
  const f = fitCaption(ctx, W, H - HINT_H, full, short, usableW(W),
                       stageTop() + (narrowStage(W) ? 300 : 120));"""),
])

patch("p5_views.js", [
    ("""  label(ctx, X, y, fmt(f, 2), col, '9.5px -apple-system, sans-serif', 'center',
    above ? 'bottom' : 'top');""",
     """  labelIfClear(ctx, X, y, fmt(f, 2), col, '9.5px -apple-system, sans-serif', 'center',
    above ? 'bottom' : 'top');"""),
])

patch("p7_test.js", [
    # the inline sweep now uses the audit's own half-pixel rule
    ("""      if(ox > 3 && oy > 3){ hit = '"' + texts[i2].t.slice(0, 22) + '" vs "' + texts[j2].t.slice(0, 22) + '"'; break; }""",
     """      /* half a pixel, the same rule tools/audit.py applies: a 3 px tolerance
         passed here and failed the audit on the same picture (Known-bad) */
      if(ox > 0.5 && oy > 0.5){ hit = '"' + texts[i2].t.slice(0, 22) + '" vs "' + texts[j2].t.slice(0, 22) + '"'; break; }"""),
])
