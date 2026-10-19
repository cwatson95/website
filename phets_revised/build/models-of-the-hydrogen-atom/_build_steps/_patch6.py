#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Layout round 5 — the last three shapes at 560x380.

All three are ordering, not geometry: a MANDATORY label was drawn after an
optional one, so the optional one had nothing to dodge.  The spectrometer title
and the ensemble note now go down first, and the residual panel's rotated
y-axis title is shortened when the panel is too short to hold it (a rotated
title's length runs down the screen, so a 150 px title on a 46 px panel reaches
50 px past the frame and onto the caption).
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
    ("""  const st = M.st, G = boxGeo(ctx, W, H, M), bb = G.bb, s = G.s;
  drawCaption(ctx, G.L);""",
     """  const st = M.st, G = boxGeo(ctx, W, H, M), bb = G.bb, s = G.s;
  drawCaption(ctx, G.L);
  /* the spectrometer's title is mandatory, so it goes down before the gun
     label, which is the one that has to move out of the way */
  if(st.showSpectro) drawSpectrometer(ctx, G.spB, M);"""),
    ("""  /* the spectrometer */
  if(st.showSpectro) drawSpectrometer(ctx, G.spB, M);
}""",
     """}"""),
])

patch("p5_views.js", [
    ("""  axes(ctx, b, lo, hi, 0, yhi, {title: 'this model minus NIST, in parts per 100 000',
    xlab: 'wavelength (nm, log scale)', ylab: '(model − NIST)/NIST, ×10⁻⁵',
    nx: 6, ny: 5, xfmt: t => fmt(Math.pow(10, t), 0), yfmt: t => (t * 1e5).toFixed(1)});""",
     """  axes(ctx, b, lo, hi, 0, yhi, {title: 'this model minus NIST, in parts per 100 000',
    xlab: 'wavelength (nm, log scale)',
    /* a rotated title runs DOWN the screen, so a 150 px one on a 46 px panel
       sticks out 50 px past the frame and lands on the caption */
    ylab: b.h < 120 ? '×10⁻⁵' : '(model − NIST)/NIST, ×10⁻⁵',
    nx: 6, ny: 5, xfmt: t => fmt(Math.pow(10, t), 0), yfmt: t => (t * 1e5).toFixed(1)});"""),
    ("""    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  const bw2 = Math.min(46, b.w / Math.max(1, nF - 1) * 0.3);""",
     """    xticks: cats, xfmt: t => fmt(t, 0), yfmt: t => fmt(t, 1)});
  /* the note is mandatory: it goes down before the optional z labels */
  label(ctx, b.x + 8, b.y1 - 16, 'mean hops per cascade ' + fmt(M.ens.mean, 3)
    + (M.ens.stuck ? '; ' + M.ens.stuck + ' of ' + st.trials + ' ended stuck in 2s' : ''),
    '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');
  const bw2 = Math.min(46, b.w / Math.max(1, nF - 1) * 0.3);"""),
    ("""  label(ctx, b.x + 8, b.y1 - 16, 'mean hops per cascade ' + fmt(M.ens.mean, 3)
    + (M.ens.stuck ? '; ' + M.ens.stuck + ' of ' + st.trials + ' ended stuck in 2s' : ''),
    '#767e92', '10.5px -apple-system, sans-serif', 'left', 'top');
  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);""",
     """  legendAuto(ctx, b, [[COL.live, 'measured'], [COL.ref, 'exact, ±2σ']]);"""),
])
