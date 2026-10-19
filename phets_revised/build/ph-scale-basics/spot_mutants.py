#!/usr/bin/env python3
"""Spot-check a few of mutants.json by hand, so the list handed over is known to be live.

A baseline that prints "N passed, 0 failed" does NOT prove the runner can see a failure
(Known-bad, waveguides.html): prove it by mutating a constant and checking the process
exits non-zero.  Physics mutants run under jsc, which is ~14x faster than osascript and
enough for this check; the full sweep is run separately with tools/mutate.py.

    python3 spot_mutants.py <index> [<index> ...]      indices into mutants.json
"""
import io
import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
JSC = '/System/Library/Frameworks/JavaScriptCore.framework/Versions/Current/Helpers/jsc'
base = io.open(os.path.join(HERE, '_out', 'run.js'), encoding='utf-8').read()
ui = io.open(os.path.join(HERE, 'ui_drive_ph-scale-basics.js'), encoding='utf-8').read()
mutants = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))

idxs = [int(a) for a in sys.argv[1:]] or [0]
bad = 0
for i in idxs:
    label, old, new, suite = mutants[i]
    assert base.count(old) == 1, label
    body = base.replace(old, new)
    tmp = os.path.join(HERE, '_out', '_spot.js')
    if suite == 'u':
        io.open(tmp, 'w', encoding='utf-8').write(body + '\n' + ui)
        cmd = ['osascript', '-l', 'JavaScript', tmp]
    else:
        io.open(tmp, 'w', encoding='utf-8').write('var console={log:print};\n' + body)
        cmd = [JSC, tmp]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    caught = r.returncode != 0
    if not caught:
        bad += 1
    print('%-8s %-4d %s' % ('caught' if caught else 'SURVIVED', i, label))
print('%d of %d spot mutants caught' % (len(idxs) - bad, len(idxs)))
sys.exit(1 if bad else 0)
