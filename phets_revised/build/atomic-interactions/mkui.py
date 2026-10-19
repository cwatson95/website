#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Assemble ui_drive_atomic-interactions.js = ui_stub.js + ui_body.js.

ui_stub.js is build/coulombs-law/ui_drive_cl.js down to its boot section,
taken verbatim (the recording context, the DOM stub with innerHTML->textContent,
the label/slider/chip/button finders, pumpU and idleU); ui_body.js is this
sim's own harness.  The concatenated file is what the orchestrator runs, so it
is kept in the build dir too — this script only regenerates it.

    python3 mkui.py
"""
import io, os
D = os.path.dirname(os.path.abspath(__file__)) + '/'
stub = io.open(D + 'ui_stub.js', encoding='utf-8').read()
stub = stub.replace(
    """/* ============ UI drive test for coulombs-law.html ========================= *
 * DOM-stub pattern (lineage: build/gravity-force-lab/ui_drive_gfl.js, from
 * projects/simulations/build_buoy).  Two scale screens with their own state,
 * each with three pointer interactions (either charge, the ruler); nothing
 * runs on a clock, so every view must paint NOTHING while idle, and every
 * action must move the picture through the frame loop from a proven-idle
 * baseline.                                                                  */""",
    """/* ====== UI drive test for atomic-interactions.html ======================= *
 * DOM-stub pattern; the stub, the recorder and the finders are taken verbatim
 * from build/coulombs-law/ui_drive_cl.js (lineage build/gravity-force-lab,
 * projects/simulations/build_buoy).  This sim has ONE pointer interaction —
 * dragging the movable atom along the r axis of the two-atoms view — and one
 * clock, which is off unless something releases the atom, so every view must
 * paint NOTHING while idle and every action must move the picture through the
 * frame loop from a proven-idle baseline.                                    *
 *                                                                            *
 * The three sim-specific thresholds the PLAYBOOK warns about are: the chip
 * rows are found by arity (7 pairs, 3 force modes), the panel has 9 groups,
 * and the input count is 9 (five sliders, four checkboxes).                  */""")
assert 'atomic-interactions.html' in stub
body = io.open(D + 'ui_body.js', encoding='utf-8').read()
io.open(D + 'ui_drive_atomic-interactions.js', 'w', encoding='utf-8').write(stub + body)
print('ui_drive_atomic-interactions.js: %d lines'
      % len((stub + body).splitlines()))
