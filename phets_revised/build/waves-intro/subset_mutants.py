#!/usr/bin/env python3
"""Write _out/mutants_osa.json: every UI mutant (they need ObjC.import, so only osascript can
run them) plus a physics cross-section — one from each layer of the file, and all three mutants
that survived the first sweep.  The whole set of 98 is swept under jsc by sweep_jsc.py; this is
what tools/mutate.py runs on a shared machine, and it is also the check that the two runners
agree on their verdicts."""
import io, json, os
HERE = os.path.dirname(os.path.abspath(__file__))
PHYS = [
    'Courant number C', 'Mur 2/(C+1)', 'Laplacian -4u', 'dispersion: the ky term',
    'calibration: pi/Nl', 'calibration: dt = Om/(2 pi f)', 'dx = W/111', 'water speed 1.65 cm/s',
    'light red end 780 nm', 'the source cell: 1.2 A sin(phi)', 'a pulse lasts one period',
    'switching a source on restarts the phase', 'a new medium restarts the clock',
    'the clock: slow is half', 'PhET’s colour scale 2.14', 'the parcels move along +grad p',
    'PhET’s screen window, 40 rows', 'PhET’s brightness knot 0.4', 'the 3-row smoothing',
    'one source on the screen: 1/r', 'the fit window starts at 30 cells', 'the unwrap step',
    'the unwrap step, the other way', 'solve4’s pivot search', 'lambda = 2 pi / k',
    'the tone is 1000 f Hz', 'the tone buffer’s length', 'light’s nanometre',
    'the exponent of a power of ten',
]
allm = json.load(io.open(os.path.join(HERE, 'mutants.json'), encoding='utf-8'))
by = {m[0]: m for m in allm}
missing = [p for p in PHYS if p not in by]
assert not missing, 'no such mutants: %s' % missing
# UI first: only osascript can run them (ObjC.import), while every physics mutant is also swept
# under jsc — so if a shared machine makes the run too slow to finish, what is lost is the part
# that is covered twice, not the part that is covered once.
sel = [m for m in allm if m[3] == 'u'] + [by[p] for p in PHYS]
io.open(os.path.join(HERE, '_out', 'mutants_osa.json'), 'w', encoding='utf-8').write(json.dumps(sel, indent=1, ensure_ascii=False))
print('%d mutants for osascript (%d physics, %d UI) of %d in all' %
      (len(sel), len(PHYS), len(sel) - len(PHYS), len(allm)))
