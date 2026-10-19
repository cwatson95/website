#!/usr/bin/env python3
"""The Python twin of molecule-shapes-basics.html.

Basics is the same model as molecule-shapes.html with the lone pairs taken out,
so it has the same twin: build/molecule-shapes/derive.py.  Rather than keep a
second copy that could drift, this runs that one and then regenerates THIS
sim's reference table (p7a_ref.js) from its printed output.

    python3 derive.py        # re-derives everything and refreshes p7a_ref.js

What it checks, in full, is documented at the top of the shared file; the parts
Basics leans on are the ideal geometries and their closed-form energies, the
relaxation against scipy's BFGS, the seeded random starts (100 of 100 reach the
ideal shape for five and for six equal pairs), PhET's real-molecule table and
the AXE names.  Its printed output is ../molecule-shapes/refvals.txt."""
import os
import subprocess
import sys

here = os.path.dirname(os.path.abspath(__file__))
full = os.path.abspath(os.path.join(here, '..', 'molecule-shapes'))
for cmd in (['derive.py'], ['gen_ref.py', 'basics']):
    r = subprocess.run([sys.executable] + [os.path.join(full, cmd[0])] + cmd[1:], cwd=full)
    if r.returncode:
        sys.exit(r.returncode)
print('the shared twin ran in %s; this directory\'s p7a_ref.js is up to date' % full)
