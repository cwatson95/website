#!/usr/bin/env python3
"""Extract makeShot() — the inline display-list recorder the house selfTests use for their layout
sweeps — BY NAME from projects/simulations/build_buoy/p7_test.js into p7_shot.js.  Nothing retyped."""
import io, os
HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
src = io.open(os.path.join(ROOT, 'projects', 'simulations', 'build_buoy', 'p7_test.js'), encoding='utf-8').read()
i = src.index('function makeShot(')
j = src.index('\n}\n', i) + 3
body = src[i:j]
assert 'ops.push' in body and 'measureText' in body
out = ('\n/* ================================================================== *\n'
       ' *  selfTest — headless verification.  Reference values labelled       *\n'
       ' *  (derive) / (scipy) / (decimal) / (CIE) are lines of                *\n'
       ' *  build/blackbody-spectrum/refvals.txt, the printed output of        *\n'
       ' *  derive.py, read in full.  makeShot() is the house inline recorder, *\n'
       ' *  extracted by name from projects/simulations/build_buoy/p7_test.js. *\n'
       ' * ================================================================== */\n' + body)
io.open(os.path.join(HERE, 'p7_shot.js'), 'w', encoding='utf-8').write(out)
print(out)
