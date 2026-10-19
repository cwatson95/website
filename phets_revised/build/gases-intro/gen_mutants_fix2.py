#!/usr/bin/env python3
"""Second re-run: the three mutants that were still alive after the first round
of added assertions.  Two of them survived because the TEST was written in
terms of the constant it was meant to pin (the lid gaps in units of LID_WIDE,
and the Avogadro check calling the helper rather than the sweep's own call
site); the third was a defensive clamp with nothing asserting what it guards.
Writes _out/mutants_fix2.json."""
import io, json, os
here = os.path.dirname(os.path.abspath(__file__))
KEEP = ['lid blow-off gap 1500 -> 3000',
        'sweep: Avogadro uses the pump again (a clump, not a gas)',
        'sweep: Charles targets not kept inside the container']
mut = {m[0]: m for m in json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))}
out = [mut[k] for k in KEEP]
io.open(os.path.join(here, '_out', 'mutants_fix2.json'), 'w', encoding='utf-8').write(
    json.dumps(out, indent=1, ensure_ascii=False) + '\n')
print('wrote %d' % len(out))
