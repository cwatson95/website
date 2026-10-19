#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two more things the PNGs showed.

  * The standing-wave view scaled its panel to the n = 6 orbit, so at n = 2 on
    the true n^2 ladder the ring was 24 px across and the wave on it — the
    subject of the whole view — was a smudge.  Fit the panel to the ring being
    DRAWN (the house rule: fit each axis to the structure that axis contains),
    let the rest of the ladder run off the panel, and print the scale and the
    fact that it does.
  * The Experiment atom's "?" sat on top of its own proton.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        if s.count(old) == 0 and s.count(new) == 1:
            continue
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p4_views.js", [
    ("""    disc(ctx, px, py, protonR(s), COL.proton);
    label(ctx, px, py - 6, '?', '#cfd4de', 'bold 34px -apple-system, sans-serif', 'center', 'middle');""",
     """    disc(ctx, px, py, protonR(s), COL.proton);
    label(ctx, px, py - 26, '?', '#cfd4de', 'bold 34px -apple-system, sans-serif', 'center', 'middle');"""),
])

patch("p5_views.js", [
    ("""  const rmaxUnits = st.showExact ? trueViewRadius(NMAX) : viewRadius(NMAX);
  const sc = (a.w * 0.42) / rmaxUnits;
  for(let n = 1; n <= NMAX; n++){
    const rr = (st.showExact ? trueViewRadius(n) : viewRadius(n)) * sc;
    ring(ctx, cx, cy, rr, n === nInt ? 'rgba(90,200,224,0.55)' : 'rgba(90,200,224,0.16)', 1, [3, 3]);
  }
  const R = (st.showExact ? trueViewRadius(nInt) : viewRadius(nInt)) * sc;""",
     """  /* the panel is fitted to the ring being DRAWN, not to the n = 6 orbit: on
     the true n^2 ladder n = 2 is a ninth of n = 6 and the wave came out 24 px
     across, which is the one thing this view exists to show.  The rest of the
     ladder is drawn at the same scale and simply runs off the panel, which the
     note below says. */
  const rCur = st.showExact ? trueViewRadius(nInt) : viewRadius(nInt);
  const rmaxUnits = st.showExact ? trueViewRadius(NMAX) : viewRadius(NMAX);
  const sc = (a.w * 0.30) / rCur;
  let offPanel = 0;
  for(let n = 1; n <= NMAX; n++){
    const rr = (st.showExact ? trueViewRadius(n) : viewRadius(n)) * sc;
    if(rr > a.w * 0.49){ offPanel++; continue; }
    ring(ctx, cx, cy, rr, n === nInt ? 'rgba(90,200,224,0.55)' : 'rgba(90,200,224,0.16)', 1, [3, 3]);
  }
  const R = rCur * sc;"""),
    ("""  label(ctx, a.x + 10, a.y1 - 20, 'ν = ' + fmt(nu, 2) + ' wavelengths round the ring', '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');""",
     """  label(ctx, a.x + 10, a.y1 - 20, 'ν = ' + fmt(nu, 2) + ' wavelengths round the ring'
    + (offPanel ? '; ' + offPanel + ' outer orbit' + (offPanel === 1 ? '' : 's') + ' run off the panel' : ''),
    '#767e92', '11px -apple-system, sans-serif', 'left', 'top');"""),
    ("""  label(ctx, a.x + 10, a.y1 - 34, (st.showExact ? 'true radius n²a₀ = ' : 'PhET radius = ')
    + fmt(st.showExact ? trueViewRadius(nInt) : viewRadius(nInt), 0) + ' units', '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');""",
     """  label(ctx, a.x + 10, a.y1 - 34, (st.showExact ? 'true radius n²a₀ = ' : 'PhET radius = ')
    + fmt(rCur, 0) + ' units, drawn at ' + sigf(sc, 3) + ' px per unit', '#767e92',
    '11px -apple-system, sans-serif', 'left', 'top');"""),
])
