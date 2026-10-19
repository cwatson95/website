#!/usr/bin/env python3
"""Write _out/mutants_retest.json holding only the named mutants from mutants.json (survivors whose
tests were strengthened), for a targeted re-run:
    python3 retest_mutants.py "label one" "label two" ...
    cd _out && python3 <sim>/tools/mutate.py sim_for_mutants.html mutants_retest.json ../ui_drive_wave-interference.js"""
import io, json, os, sys
HERE = os.path.dirname(os.path.abspath(__file__))
allm = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
want = set(sys.argv[1:])
sel = [m for m in allm if m[0] in want]
missing = want - set(m[0] for m in sel)
assert not missing, 'no such mutants: %s' % sorted(missing)
io.open(os.path.join(HERE, '_out', 'mutants_retest.json'), 'w', encoding='utf-8').write(json.dumps(sel, indent=1, ensure_ascii=False))
print('%d mutants to retest' % len(sel))
