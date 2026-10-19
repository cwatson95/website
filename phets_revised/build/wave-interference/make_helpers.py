#!/usr/bin/env python3
"""Extract the house 2-D drawing helpers BY NAME, unchanged, from
projects/simulations/build_buoy/p4_views.js into p4_helpers.js: the font constants, isNarrow,
worldFitUp, worldCurve, worldFill, worldPoly, seg, dot, arrowW, the label registry (LABELS,
labFits, lab), titleFor, axesR, stageLayout, drawCaption, marker.  The buoyancy-specific
helpers and its DRAG are left behind (this sim declares its own DRAG).  Nothing retyped."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
src = io.open(os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p4_views.js'), encoding='utf-8').read()


def block(name):
    i = src.index('function ' + name + '(')
    first = src[i:].split('\n', 1)[0].rstrip()
    j = (src.index('\n}\n', i) + 3) if first.endswith('{') else (src.index('\n', i) + 1)
    return src[i:j]


out = ('\n/* ================================================================== *\n'
       ' *  drawing helpers (y UP in world maps; layouts built bottom-up from *\n'
       ' *  a measured caption) — from projects/simulations/build_buoy/       *\n'
       ' *  p4_views.js by name, unchanged (make_helpers.py)                  *\n'
       ' * ================================================================== */\n')
for line in ["const CAP_FONT='11.5px -apple-system, sans-serif';\n",
             "const LAB_FONT='11px -apple-system, sans-serif';\n",
             "const SM_FONT='10.5px -apple-system, sans-serif';\n"]:
    assert src.count(line) == 1, line
    out += line
for nm in ['isNarrow', 'worldFitUp', 'worldCurve', 'worldFill', 'worldPoly', 'seg', 'dot', 'arrowW']:
    out += block(nm)
out += "/* the label registry: the audit's half-pixel overlap rule, shift or drop */\nlet LABELS=[];\n"
for nm in ['labFits', 'lab', 'titleFor', 'axesR', 'stageLayout', 'drawCaption', 'marker']:
    out += block(nm)
io.open(os.path.join(HERE, 'p4_helpers.js'), 'w', encoding='utf-8').write(out)
for nm in ['isNarrow', 'worldFitUp', 'lab', 'axesR', 'stageLayout', 'marker', 'arrowW']:
    assert ('function ' + nm + '(') in out, nm
print('p4_helpers.js: %d lines' % len(out.splitlines()))

# the selfTest's recording context, makeShot, from build_buoy/p7_test.js by name, unchanged
tsrc = io.open(os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p7_test.js'), encoding='utf-8').read()
i = tsrc.index('function makeShot(')
j = tsrc.index('\n}\n', i) + 3
shot = ('\n/* ================================================================== *\n'
        ' *  makeShot — the selfTest recording context (text boxes through     *\n'
        ' *  the transform, fill counts), from build_buoy/p7_test.js by name,  *\n'
        ' *  unchanged (make_helpers.py)                                       *\n'
        ' * ================================================================== */\n') + tsrc[i:j]
io.open(os.path.join(HERE, 'p7_shot.js'), 'w', encoding='utf-8').write(shot)
print('p7_shot.js: %d lines' % len(shot.splitlines()))
