#!/usr/bin/env python3
"""p4_helpers.js = the house view helpers, verbatim from
projects/simulations/build_buoy/p4_views.js (itself "extracted from
build_cycloid/p4_views.js, unchanged"): fonts, worldFitUp, worldCurve,
worldFill, worldPoly, seg, circleW, dot, arrowW, the label registry and lab(),
titleFor, axesR, stageLayout, drawCaption, marker.  Cut just before the first
buoyancy-specific helper (fluidRect); every function we use is asserted."""
import io
import os

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
src = io.open(os.path.join(root, 'projects', 'simulations', 'build_buoy', 'p4_views.js'), encoding='utf-8').read()
k = src.index('/* the fluid: a translucent slab')
out = src[:k].rstrip('\n') + '\n'
out = out.replace(' *  — extracted from build_cycloid/p4_views.js, unchanged              *',
                  ' *  — verbatim from build_buoy/p4_views.js (build_cycloid lineage)     *')
for fn in ['const CAP_FONT=', 'const LAB_FONT=', 'const SM_FONT=', 'function isNarrow(', 'const DRAG=',
           'function worldFitUp(', 'function worldPoly(', 'function seg(', 'function circleW(', 'function dot(',
           'function arrowW(', 'let LABELS=', 'function labFits(', 'function lab(', 'function titleFor(',
           'function axesR(', 'function stageLayout(', 'function drawCaption(', 'function marker(']:
    assert out.count(fn) == 1, fn
assert 'fluidRect' not in out and 'forceArrow' not in out
io.open(os.path.join(here, 'p4_helpers.js'), 'w', encoding='utf-8').write(out)
print('p4_helpers.js: %d lines' % len(out.splitlines()))
