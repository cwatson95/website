#!/usr/bin/env python3
"""Re-run only the mutants that survived the first sweep, after the assertions
that were missing have been added.  Reads the survivor labels out of
_out/mutation_log.txt, maps the two whose code MOVED (the P-V isotherm went
from the draw call into the model function `pvIsotherm`, per the Known-bad rule
that a number computed inside a draw call cannot be tested), and writes
_out/mutants_fix.json.  The full sweep stays in mutants.json."""
import io, json, os, re
here = os.path.dirname(os.path.abspath(__file__))
log = io.open(os.path.join(here, '_out', 'mutation_log.txt'), encoding='utf-8').read()
survived = re.findall(r'^SURVIVED\s+\*\*\* (.+?) \*\*\*$', log, re.M)
survived = list(dict.fromkeys(survived))
mut = {m[0]: m for m in json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))}
# the isotherm mutant was renamed when its code moved out of the draw call
RENAME = {'the P-V isotherm drawn at 2T': 'the P-V isotherm built at 2T'}
out, missing = [], []
for label in survived:
    key = RENAME.get(label, label)
    if key in mut:
        out.append(mut[key])
    else:
        missing.append(label)
io.open(os.path.join(here, '_out', 'mutants_fix.json'), 'w', encoding='utf-8').write(
    json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print('%d survivors -> %d re-runs%s' % (len(survived), len(out),
      ('; NOT FOUND: ' + ', '.join(missing)) if missing else ''))
for m in out:
    print('   ' + m[0])
