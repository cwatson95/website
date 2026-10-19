#!/usr/bin/env python3
"""Re-run only the mutants that survived the first sweep, after the assertions
that were missing have been added.  Reads the survivor labels out of
_out/mutation_log.txt and writes _out/mutants_fix.json; the full sweep stays in
mutants.json."""
import io, json, os, re
here = os.path.dirname(os.path.abspath(__file__))
log = io.open(os.path.join(here, '_out', 'mutation_log.txt'), encoding='utf-8').read()
survived = list(dict.fromkeys(re.findall(r'^SURVIVED\s+\*\*\* (.+?) \*\*\*$', log, re.M)))
mut = {m[0]: m for m in json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))}
out, missing = [], []
for label in survived:
    (out if label in mut else missing).append(mut.get(label, label))
io.open(os.path.join(here, '_out', 'mutants_fix.json'), 'w', encoding='utf-8').write(
    json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print('%d survivors -> %d re-runs%s' % (len(survived), len(out),
      ('; NOT FOUND: ' + ', '.join(map(str, missing))) if missing else ''))
for m in out:
    print('   ' + m[0])
