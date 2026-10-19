#!/usr/bin/env python3
"""Run both sims' mutation sweeps, one after the other (osascript jobs run one
at a time: other agents share this machine).  Each sweeps a COPY of its html
inside its own _out/, never docs/phets_revised/<stem>.html in place -- mutate.py
writes its scratch _mutant.js next to the file it tests, and parallel sweeps in
the shared directory would corrupt each other's kill counts."""
import os
import shutil
import subprocess
import sys

BUILD = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BUILD)
TOOL = os.path.abspath(os.path.join(ROOT, '..', '..', 'projects', 'simulations', 'tools', 'mutate.py'))

rc = 0
for stem in ('molecule-shapes', 'molecule-shapes-basics'):
    d = os.path.join(BUILD, stem)
    out = os.path.join(d, '_out')
    os.makedirs(out, exist_ok=True)
    copy = os.path.join(out, 'sweep.html')
    shutil.copyfile(os.path.join(ROOT, stem + '.html'), copy)
    log = os.path.join(out, 'mutation_log.txt')
    print('=== %s: sweeping %s' % (stem, copy), flush=True)
    with open(log, 'w') as f:
        r = subprocess.run([sys.executable, TOOL, copy, os.path.join(d, 'mutants.json'),
                            os.path.join(d, 'ui_drive_%s.js' % stem)], stdout=f, stderr=subprocess.STDOUT)
    tail = [l for l in open(log).read().splitlines() if 'caught,' in l or l.startswith('   SURV') or l.startswith('   SKIP')]
    print('%s: %s' % (stem, ' | '.join(tail) if tail else 'no summary'), flush=True)
    rc = rc or r.returncode
sys.exit(rc)
