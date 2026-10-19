#!/usr/bin/env python3
"""Re-run only the UI mutants of both sims, after the UI drive gained the
reset-view repaint test (the sims' html is untouched, so the physics mutants
are unaffected; mutate.py reads the drive once at startup, so the earlier
sweep's UI results predate the new test).

Writes _out/mutation_log_ui.txt beside each sim's full sweep log."""
import json
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
    all_m = json.load(open(os.path.join(d, 'mutants.json')))
    # every UI mutant (the drive gained a test) plus the one the new NAMED pin covers
    ui = [m for m in all_m if m[3] == 'u' or m[0].startswith('the bent class is compared')]
    shutil.copyfile(os.path.join(ROOT, stem + '.html'), os.path.join(out, 'sweep.html'))
    sub = os.path.join(out, 'mutants_ui.json')
    json.dump(ui, open(sub, 'w'), indent=1)
    log = os.path.join(out, 'mutation_log_ui.txt')
    print('=== %s: %d UI mutants' % (stem, len(ui)), flush=True)
    with open(log, 'w') as f:
        r = subprocess.run([sys.executable, TOOL, os.path.join(out, 'sweep.html'), sub,
                            os.path.join(d, 'ui_drive_%s.js' % stem)], stdout=f, stderr=subprocess.STDOUT)
    tail = [l for l in open(log).read().splitlines() if 'caught,' in l or l.startswith('   SURV')]
    print('%s: %s' % (stem, ' | '.join(tail) if tail else 'no summary'), flush=True)
    rc = rc or r.returncode
sys.exit(rc)
