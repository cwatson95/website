#!/usr/bin/env python3
"""Stage a named subset of mutants.json into _out/<dir>/ with a private copy of
the shipped html, so a spot check never shares mutate.py's `_mutant.js` scratch
with another agent's sweep (BRIEF: sweep a COPY inside your own _out/)."""
import io, json, os, shutil, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SIM = os.path.abspath(os.path.join(HERE, '..', '..', 'molecule-polarity.html'))
out = os.path.join(HERE, '_out', sys.argv[1])
names = set(sys.argv[2:])
M = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
sub = [m for m in M if m[0] in names] if names else M
missing = names - {m[0] for m in sub}
assert not missing, missing
os.makedirs(out, exist_ok=True)
io.open(os.path.join(out, 'subset.json'), 'w', encoding='utf-8').write(json.dumps(sub, indent=1))
shutil.copyfile(SIM, os.path.join(out, 'molecule-polarity.html'))
print('%d mutants staged in _out/%s' % (len(sub), sys.argv[1]))
