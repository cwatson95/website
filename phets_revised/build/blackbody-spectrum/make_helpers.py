#!/usr/bin/env python3
"""Extract the house 2-D drawing helpers BY NAME from projects/simulations/build_buoy/p4_views.js
(the label registry, lab, titleFor, axesR, stageLayout, drawCaption, marker, dot) into
p4_helpers.js.  The world-map and fluid helpers that sim needs are left behind.  Nothing retyped."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
src = io.open(os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p4_views.js'), encoding='utf-8').read()

def block(name):
    i = src.index('function ' + name + '(')
    first = src[i:].split('\n', 1)[0].rstrip()
    j = (src.index('\n}\n', i) + 3) if first.endswith('{') else (src.index('\n', i) + 1)
    return src[i:j]

head = src[:src.index('function worldFitUp(')]
assert head.count("const DRAG={what:null,off:0};\n") == 1
out = head.replace("const DRAG={what:null,off:0};\n", "")
out = out.replace('extracted from build_cycloid/p4_views.js, unchanged',
                  'from projects/simulations/build_buoy/p4_views.js by name,   *\n *  unchanged; its world-map and fluid helpers are left behind')
for nm in ['dot', 'labFits', 'lab', 'titleFor', 'axesR', 'stageLayout', 'drawCaption', 'marker']:
    if nm == 'labFits':
        out += "/* the label registry: the audit's half-pixel overlap rule, shift or drop */\nlet LABELS=[];\n"
    out += block(nm)
io.open(os.path.join(HERE, 'p4_helpers.js'), 'w', encoding='utf-8').write(out)
print(out)
