#!/usr/bin/env python3
"""Every mutant's `old` must occur exactly once in the extracted script (mutate.py skips the rest)."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
js = io.open(os.path.join(HERE, '_out', 'run.js'), encoding='utf-8').read()
ms = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
bad = 0
for lab, old, new, suite in ms:
    n = js.count(old)
    if n != 1:
        bad += 1
        print('COUNT %d  %s' % (n, lab))
print('%d mutants (%d physics, %d UI), %d with a bad pattern' % (len(ms), sum(m[3] == 'p' for m in ms), sum(m[3] == 'u' for m in ms), bad))
