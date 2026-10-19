#!/usr/bin/env python3
"""Spot-check the mutation harness on a SAMPLE of mutants, against a COPY of
the html inside this build's own _out/ -- never the shipped file in place,
because mutate.py writes its scratch _mutant.js next to the html it tests and
parallel agents would corrupt each other's kill counts (BRIEF).

    python3 spot_sweep.py            # the default sample
    python3 spot_sweep.py all        # every mutant (the orchestrator's job)
"""
import io
import json
import os
import shutil
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..', '..', '..'))
MUTATE = os.path.join(root, 'projects', 'simulations', 'tools', 'mutate.py')
SIM = os.path.abspath(os.path.join(here, '..', '..', 'molecules-and-light.html'))
UI = os.path.join(here, 'ui_drive_molecules-and-light.js')

SAMPLE = [
    'P_ABSORB 0.5 -> 0.45', "PhET's oxygen mass is carbon's", "CO2's measured bond length",
    'um from cm-1', 'the hysteresis is no longer set after an emission',
    'linear XY2: the symmetric stretch stops being antisymmetric',
    'the emission direction is no longer uniform on the circle',
    'Jacobi: one sweep instead of a hundred',
    'UI: the drag no longer marks the loop dirty', 'UI: resetCam stops resetting the camera',
]
M = json.load(io.open(os.path.join(here, 'mutants.json'), encoding='utf-8'))
if len(sys.argv) > 1 and sys.argv[1] == 'all':
    sub = M
else:
    sub = [m for m in M if m[0] in SAMPLE]
    missing = set(SAMPLE) - set(m[0] for m in sub)
    assert not missing, missing

scratch = os.path.join(here, '_out', 'spot')
shutil.rmtree(scratch, ignore_errors=True)
os.makedirs(scratch)
copy = os.path.join(scratch, 'molecules-and-light.html')
shutil.copyfile(SIM, copy)
sub_path = os.path.join(scratch, 'mutants_sample.json')
io.open(sub_path, 'w', encoding='utf-8').write(json.dumps(sub))
r = subprocess.run([sys.executable, MUTATE, copy, sub_path, UI],
                   capture_output=True, text=True, timeout=36000)
out = r.stdout + r.stderr
io.open(os.path.join(scratch, 'sweep.log'), 'w', encoding='utf-8').write(out)
print(out[-6000:])
print('exit', r.returncode)
