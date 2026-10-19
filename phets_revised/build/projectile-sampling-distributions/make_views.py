#!/usr/bin/env python3
"""Extract p4b_shared.js — the picture layer this sim shares with the data lab
remake — rather than retyping it (PLAYBOOK section 4: the aesthetic is
extracted, not restyled).  The cut runs from the top of
build/projectile-data-lab/p4_views.js to the end of drawField(), which is
everything up to the data lab's own landing-distance histogram, measures
overlay and interval tool: the caption/panel layout, the field map and its
true-aspect rule, PhET's ground markers, the launcher and its spread fan, and
the trajectories.  The histogram is NOT taken, because this sim's histogram is
of sample MEANS and of densities, and dead code is equivalent-mutant country.

The cut is made on the END of drawField rather than on the banner comment that
follows it, and every function the sim depends on is asserted present.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(os.path.dirname(HERE), 'projectile-data-lab', 'p4_views.js')
s = io.open(SRC, encoding='utf-8').read()
k = s.index('function drawField(')
e = s.index('\n}\n', k) + 3
head = s[:e]
head = head.replace(
    """/* ================================================================== *
 *  the shared picture: a 100 m field with a launcher on it, and the   *
 *  histogram of landing distance under it on the SAME x axis — which  *
 *  is PhET's layout and the whole point of the screen                 *
 * ================================================================== */""",
    """/* ================================================================== *
 *  the shared picture layer — EXTRACTED from                          *
 *  build/projectile-data-lab/p4_views.js by make_views.py, unchanged: *
 *  the stage layout, the field map (true aspect wherever it fits),    *
 *  PhET's 10 m markers, the launcher and its spread fan, the          *
 *  trajectories.                                                      *
 * ================================================================== */""", 1)
for want in ['const HINT_H=18;', 'function axesT(', 'function legendReg(', 'function logTicks125(',
             'function labStage(', 'function fieldWantH(', 'function fieldMap(', 'function drawGround(',
             'function drawLauncher(', 'function drawPath(', 'function drawField(']:
    assert want in head, want
for unwanted in ['function drawHist(', 'function drawMeasures(', 'function intervalGeo(', 'function aspectNote(']:
    assert unwanted not in head, unwanted
io.open(os.path.join(HERE, 'p4b_shared.js'), 'w', encoding='utf-8').write(head)
print('p4b_shared.js: %d lines extracted from build/projectile-data-lab/p4_views.js'
      % len(head.splitlines()))
