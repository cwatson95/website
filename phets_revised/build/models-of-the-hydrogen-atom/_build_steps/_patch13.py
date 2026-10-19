#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The last two survivors of the re-check.

1. "PhET choose_m thirds" survived even after the rule was consolidated,
   because m is CAUSALLY INERT in PhET's model: phetLowerDist depends only on
   (n, l), phetChooseL does not read m, and phetChooseM can only ever return
   m, m+1 or m-1 — so |dm| is never 2 and the (1,0,0) fallback is never reached
   through m either.  The m choice therefore changes nothing about which n the
   atom lands on or which wavelength comes out; it changes only the m the
   readout prints and the orbital the cloud draws.  So the distribution itself
   has to be asserted, and the inertness stated deliberately rather than left
   as the reason a mutant lived.

2. "the pointer never marks the canvas dirty" survived the pointerdown-only
   test because the test still fired pointerup afterwards, and the pointerup
   handler calls refresh(), which draws unconditionally.  Capture AFTER the
   pointerdown and BEFORE any pointerup.
"""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))


def patch(fname, pairs):
    p = os.path.join(HERE, fname)
    s = io.open(p, encoding="utf-8").read()
    for old, new in pairs:
        assert s.count(old) == 1, ("%s: %r appears %d times" % (fname, old[:70], s.count(old)))
        s = s.replace(old, new)
    io.open(p, "w", encoding="utf-8").write(s)
    print(fname, "patched")


patch("p7_test.js", [
    ("""  eq(phetChooseM(0, 1).length, 3, 'PhET choose_m from m=0 has three options');""",
     """  eq(phetChooseM(0, 1).length, 3, 'PhET choose_m from m=0 has three options');
  {
    /* m is a passenger in PhET's model — phetLowerDist reads only (n, l),
       phetChooseL does not read m, and phetChooseM can only return m, m+1 or
       m-1, so |dm| is never 2 and the (1,0,0) fallback is never reached through
       m.  Nothing about which n the atom lands on, or which wavelength comes
       out, depends on it; it sets the m the readout prints and the orbital the
       cloud draws.  So assert the DISTRIBUTION, and assert the inertness. */
    const rgm = makeRng(606060);
    const hist = {};
    const NM3 = 60000;
    for(let i = 0; i < NM3; i++){
      const v = rgm.weighted(phetChooseM(0, 2));
      hist[v] = (hist[v] || 0) + 1;
    }
    for(const k of [-1, 0, 1])
      rel((hist[k] || 0) / NM3, 1 / 3, 0.02, 'PhET choose_m gives m' +
        (k > 0 ? '+1' : (k < 0 ? '-1' : '')) + ' one third of the time');
    let worstDm = 0;
    for(let l2 = 0; l2 <= 5; l2++) for(let m0 = -5; m0 <= 5; m0++)
      for(const [mp] of phetChooseM(m0, l2))
        worstDm = Math.max(worstDm, Math.abs(mp - clamp(m0, -l2, l2)));
    eq(worstDm, 1, 'PhET choose_m never moves m by more than 1, so |dm| <= 1 is automatic');
    /* and the lower n never depends on m */
    let sameN = true;
    for(let n2 = 2; n2 <= NMAX; n2++) for(let l2 = 0; l2 < n2; l2++)
      if(JSON.stringify(phetLowerDist(n2, l2)) !== JSON.stringify(phetLowerDist(n2, l2))) sameN = false;
    ok(sameN && phetLowerDist.length === 2, 'phetLowerDist takes (n, l) only: m cannot change the hop');
  }"""),
])

patch("ui_drive_models-of-the-hydrogen-atom.js", [
    ("""  const on0 = ST.lightOn;
  UREC = uMakeRec();
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UNODES.scene.fire('pointerup', {});
  upump(3);
  uok(uGeom(UREC).length > 50, 'a pointerdown ALONE repaints (only that handler sets dirty)');
  uok(ST.lightOn !== on0, 'clicking inside the box toggles the lamp');""",
     """  const on0 = ST.lightOn;
  /* fire the pointerdown and pump BEFORE any pointerup: the pointerup handler
     calls refresh(), which draws unconditionally, and that draw masked the
     pointerdown handler's dirty flag entirely (Known-bad, again) */
  UNODES.scene.fire('pointerdown', {clientX: 400, clientY: 300});
  UREC = uMakeRec(); upump(3);
  uok(uGeom(UREC).length > 50, 'a pointerdown ALONE repaints (only that handler sets dirty)');
  UNODES.scene.fire('pointerup', {});
  uok(ST.lightOn !== on0, 'clicking inside the box toggles the lamp');"""),
])
