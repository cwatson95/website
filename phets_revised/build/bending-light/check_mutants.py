#!/usr/bin/env python3
"""Every mutant's `old` must appear EXACTLY ONCE in the extracted script, or
mutate.py skips it (and a skipped mutant is one you think you ran and did not).
Also checks that `new` differs from `old` and does not already appear."""
import io
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, '..', '..', 'bending-light.html'))
s = io.open(SIM, encoding='utf-8').read()
js = s.split('<script>', 1)[1].rsplit('</script>', 1)[0]
M = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
bad = 0
seen = set()
for label, old, new, suite in M:
    n = js.count(old)
    if n != 1:
        print('%-4s %-62s old appears %d times' % ('BAD', label[:60], n))
        bad += 1
    if old == new:
        print('%-4s %-62s old == new' % ('BAD', label[:60]))
        bad += 1
    if label in seen:
        print('%-4s %-62s duplicate label' % ('BAD', label[:60]))
        bad += 1
    seen.add(label)
    if suite not in ('p', 'u'):
        print('%-4s %-62s suite %r' % ('BAD', label[:60], suite))
        bad += 1
print('%d mutants, %d physics, %d ui, %d problems'
      % (len(M), sum(1 for m in M if m[3] == 'p'), sum(1 for m in M if m[3] == 'u'), bad))
sys.exit(1 if bad else 0)
