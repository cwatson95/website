#!/usr/bin/env python3
"""One mutant on its own: the P-V isotherm label's leftward fallback.  It
survived the full sweep because at the DEFAULT axis the label fits whichever
way it hangs — the fallback only bites when the hottest isotherm enters within
its own width of the right edge, which needs the gas a little below 300 K.
Writes _out/mutants_iso.json so that one can be re-run without the other 74."""
import io, json, os
here = os.path.dirname(os.path.abspath(__file__))
LABEL = 'the P-V isotherm label falls back to the wrong side'
m = [x for x in json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8')) if x[0] == LABEL]
assert len(m) == 1, m
io.open(os.path.join(here, '_out', 'mutants_iso.json'), 'w', encoding='utf-8').write(
    json.dumps(m, indent=1, ensure_ascii=False) + '\n')
print('wrote 1')
