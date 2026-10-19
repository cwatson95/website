#!/usr/bin/env python3
"""p1_utils.js = the house 2-D helper layer, verbatim from
projects/simulations/build_buoy/p1_utils.js (the newest copy carrying the
Known-bad fixes: tag-stripping plain() with the wide entity regex and the
numeric decode inside it, Liang-Barsky polyline() clipping in data space,
axes() sorting its range, the legend registry, the guarded log ticks), plus
the house 3-D camera block (v3, makeCamera, camBasis, project, boxCamera)
verbatim from projects/simulations/build_lagr/p4_views.js.  Each function
we depend on is asserted present, so a cut that loses one fails here."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
sim = os.path.join(root, 'projects', 'simulations')
u = io.open(os.path.join(sim, 'build_buoy', 'p1_utils.js'), encoding='utf-8').read()
for fn in ['function toRgb(', 'function mix(', 'function rgba(', 'function shade(', 'function neon(', 'function h(',
           'function fmt(', 'function sigf(', 'const ENTS=', 'function plain(', 'function wrapText(',
           'function caption(', 'function box(', 'function frame(', 'function ticksFor(', 'function logTicks(',
           'function axes(', 'function polyline(', 'function legendBox(', 'function legendAuto(', 'function fitCaption(']:
    assert u.count(fn) == 1, fn
lp = io.open(os.path.join(sim, 'build_lagr', 'p4_views.js'), encoding='utf-8').read()
i = lp.index('const v3={')
i = lp.rindex('\n', 0, i) + 1
k = lp.index('function boxCamera(')
e = lp.index('\n}\n', k) + 3
cam = lp[i:e]
for fn in ['const v3={', 'function makeCamera(', 'function camBasis(', 'function project(', 'function boxCamera(']:
    assert cam.count(fn) == 1, fn
out = (u.rstrip('\n') + '\n\n'
       '/* ================================================================== *\n'
       ' *  3-vector helpers, orbit camera, perspective projection (z-up)      *\n'
       ' *  — verbatim from build_lagr/p4_views.js (the lattice / steam_carnot *\n'
       ' *  camera), with boxCamera sizing it to a panel                       *\n'
       ' * ================================================================== */\n'
       + cam)
io.open(os.path.join(here, 'p1_utils.js'), 'w', encoding='utf-8').write(out)
print('p1_utils.js: %d lines (%d from build_buoy, camera %d lines from build_lagr)'
      % (len(out.splitlines()), len(u.splitlines()), len(cam.splitlines())))
