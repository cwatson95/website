#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""audit.py found one collision the inline sweep missed (its threshold is
0.5 px against the inline 3 px — the audit's is the real one, Known-bad):
"n=5" on top of "n=6" on the TRUE ladder of the Experiment model.

Root cause: the label thinner exempted the level the electron is on
(`|| n === M.n`), and for Experiment there IS no visible electron, so the
exemption forced a label that had nowhere to go.  The labels now go down in one
pass through labelIfClear, with the occupied level first so that it wins the
space, and nothing is exempt from the collision test."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "p4_views.js")
s = io.open(p, encoding="utf-8").read()

old = """    if(Math.abs(y - lastLabY) >= 12 || n === M.n){
      label(ctx, x1 + 1, y, 'n=' + n, n === M.n ? COL.pos : '#6f7789',
        '10.5px -apple-system, sans-serif', 'right', 'middle');
      lastLabY = y; labelled++;
    }
    /* below 150 px of panel there is no room between the energy axis and the
       level lines for a value, and it lands on the rotated axis title */
    if(trueAxis && b.w >= 150) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');
  }
"""
new = """  }
  /* The labels go down in ONE pass through labelIfClear, occupied level first
     so that it wins the space.  Nothing is exempt: exempting the electron's own
     level put "n=6" on top of "n=5" on the true ladder of the Experiment model,
     which has no visible electron at all. */
  const labOrder = [];
  if(st.model !== 'experiment') labOrder.push(M.n);
  for(let n = 1; n <= NMAX; n++) if(labOrder.indexOf(n) < 0) labOrder.push(n);
  for(const n of labOrder){
    const y = yOf(n);
    const live = (n === M.n && st.model !== 'experiment');
    if(labelIfClear(ctx, x1 + 1, y, 'n=' + n, live ? COL.pos : '#6f7789',
        '10.5px -apple-system, sans-serif', 'right', 'middle')){
      lastLabY = y; labelled++;
    }
    /* below 150 px of panel there is no room between the energy axis and the
       level lines for a value, and it lands on the rotated axis title */
    if(trueAxis && b.w >= 150) labelIfClear(ctx, x0 - 5, y, fmt(energyEV(n), 2), '#6f7789',
      '9.5px -apple-system, sans-serif', 'right', 'middle');
  }
"""
assert s.count(old) == 1
s = s.replace(old, new)
io.open(p, "w", encoding="utf-8").write(s)
print("p4_views.js patched")
