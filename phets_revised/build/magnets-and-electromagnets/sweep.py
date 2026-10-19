#!/usr/bin/env python3
"""sweep.py -- run tools/mutate.py over a COPY of the page inside this build's _out/.

    python3 sweep.py [stem] [p|u]

mutate.py writes its scratch `_mutant.js` NEXT TO the html it tests, so sweeping
docs/phets_revised/<stem>.html in place would have parallel builds share one scratch file
and corrupt each other's kill counts (Known-bad).  The copy is byte-identical and is
checked to be so before the sweep starts.
"""
import filecmp
import io
import os
import shutil
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
BUILD = os.path.dirname(HERE)
OUT = os.path.dirname(BUILD)
ROOT = os.path.abspath(os.path.join(OUT, '..', '..'))
TOOLS = os.path.join(ROOT, 'projects', 'simulations', 'tools')
stem = sys.argv[1] if len(sys.argv) > 1 else 'magnets-and-electromagnets'
only = sys.argv[2] if len(sys.argv) > 2 else None
sdir = os.path.join(BUILD, stem)
src = os.path.join(OUT, stem + '.html')
dst = os.path.join(sdir, '_out', stem + '_sweep.html')
os.makedirs(os.path.dirname(dst), exist_ok=True)
shutil.copyfile(src, dst)
assert filecmp.cmp(src, dst, shallow=False), 'the sweep copy differs from the page'
ui = os.path.join(sdir, 'ui_drive_%s.js' % stem)
cmd = [sys.executable, os.path.join(TOOLS, 'mutate.py'), dst, os.path.join(sdir, 'mutants.json'), ui]
if only:
    cmd.append(only)
log = os.path.join(sdir, '_out', 'mutation_log%s.txt' % ('_' + only if only else ''))
with io.open(log, 'w', encoding='utf-8') as f:
    r = subprocess.run(cmd, stdout=f, stderr=subprocess.STDOUT)
txt = io.open(log, encoding='utf-8').read()
print(txt[-2500:])
print('log: ' + log)
sys.exit(r.returncode)
