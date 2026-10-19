#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Lift PhET's emission-direction rule out of the middle of trySpontaneous into
a function of its own, so it can be asserted.  A quantity computed inside a
step function that nothing reads is invisible to every test, and mutation
testing is how you find out (Known-bad)."""
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


patch("p3_state.js", [
    ("""  const [ex, ey] = electronXY(st);
  let dir;
  if(ATOM.n < 5) dir = ATOM.rng.angle();
  else dir = ATOM.angle + PI + 0.1 * ATOM.rng.sign() * PI;
  emitPhoton(st, lam, ex, ey, adjustEmission(dir));""",
     """  const [ex, ey] = electronXY(st);
  emitPhoton(st, lam, ex, ey, adjustEmission(emissionDirection(ATOM.n, ATOM.angle, ATOM.rng)));"""),
    ("""/* PhET adjustEmissionDirection: never within pi/8 of straight up, so an
   emitted photon is not mistaken for one from the source */""",
     """/* PhET's own rule for which way a spontaneously emitted photon goes: from
   n < 5 any direction at all, and from n >= 5 back along the electron's own
   direction to within a tenth of a turn.  Lifted out of trySpontaneous so the
   suite can assert it — a choice made inside a step function and never read
   back is invisible to every test (Known-bad). */
function emissionDirection(n, angle, rng){
  if(n < 5) return rng.angle();
  return angle + PI + 0.1 * rng.sign() * PI;
}
/* PhET adjustEmissionDirection: never within pi/8 of straight up, so an
   emitted photon is not mistaken for one from the source */"""),
])

patch("p7_test.js", [
    ("""  rel(minOff, PI / 8, 1e-9, 'no emitted photon comes out within pi/8 of the beam (PhET)');""",
     """  rel(minOff, PI / 8, 1e-9, 'no emitted photon comes out within pi/8 of the beam (PhET)');
  /* PhET's emission direction: isotropic below n = 5, backwards along the
     electron above it */
  const rgd = makeRng(1234);
  let cs = 0, sn = 0;
  for(let i = 0; i < 20000; i++){
    const d = emissionDirection(3, 0.7, rgd);
    cs += Math.cos(d); sn += Math.sin(d);
  }
  ok(Math.hypot(cs, sn) / 20000 < 0.02, 'below n = 5 the emission is isotropic (PhET)');
  let worstBack = 0;
  for(let i = 0; i < 2000; i++){
    const ang = rgd.angle();
    const d = emissionDirection(6, ang, rgd);
    let off = d - (ang + PI);
    off = Math.atan2(Math.sin(off), Math.cos(off));
    worstBack = Math.max(worstBack, Math.abs(off));
  }
  rel(worstBack, 0.1 * PI, 1e-9, 'from n >= 5 it comes back along the electron, 0.1 turn either side (PhET)');"""),
])
