#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""The assertions the first mutation sweep asked for.

Each one closes a survivor: a constant that no observable depended on, a guard
that no caller could reach, or a self-referential pin that moved with the
mutant instead of failing on it.
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
    # --- delta l = 0 is only REACHABLE through einsteinA when l >= 1, because
    #     lmax = max(lu, ll) is zero for s -> s and kills the rate anyway
    ("""  eq(einsteinA(2, 0, 1, 0), 0, '2s -> 1s is forbidden (delta l = 0)');""",
     """  eq(einsteinA(2, 0, 1, 0), 0, '2s -> 1s is forbidden (delta l = 0)');
  eq(einsteinA(3, 1, 2, 1), 0, '3p -> 2p is forbidden (delta l = 0, and l_max does not hide it)');
  eq(einsteinA(4, 2, 3, 2), 0, '4d -> 3d is forbidden (delta l = 0)');
  eq(einsteinA(4, 3, 3, 1), 0, '4f -> 3p is forbidden (delta l = 2)');"""),
    # --- the Condon-Shortley phase is provably invisible: say so
    ("""  /* the angular part */""",
     """  /* The Condon-Shortley phase (-1)^m in legendreP cancels in |Y|^2, which is
     the only thing this file ever asks for, so a mutant that drops it is
     EQUIVALENT.  That is worth stating rather than leaving as a blind spot
     (Known-bad): assert the invariance deliberately. */
  for(const [l, m] of [[1, 1], [2, 1], [3, 3], [5, 3]]){
    const p1 = legendreP(l, m, 0.42);
    ok(Math.abs(p1) > 1e-6, 'P_' + l + '^' + m + '(0.42) is not zero, so the phase is testable');
    ok(Math.abs(ylmSq(l, m, 0.42) - ylmSq(l, -m, 0.42)) < 1e-15,
      '|Y_' + l + '^' + m + '|^2 does not depend on the sign of m, so the phase cancels');
  }
  /* the angular part */"""),
    # --- PhET's white-light bias, measured off the source itself
    ("""  eq(JSON.stringify(phetGroundAbsorptionLams()), JSON.stringify([122, 103, 97, 95, 94]),
     'the n=1 absorption lines PhET biases white light toward');""",
     """  eq(JSON.stringify(phetGroundAbsorptionLams()), JSON.stringify([122, 103, 97, 95, 94]),
     'the n=1 absorption lines PhET biases white light toward');
  {
    /* PhET aims 0.4 of its white photons at an n = 1 line and scatters the rest
       uniformly over 92-780 nm; measure the fraction off the source */
    Object.assign(ST, DEFAULTS, {light: 'white', lightOn: true, seed: 5150});
    atomReset(ST);
    const gl = phetGroundAbsorptionLams();
    let onLine = 0;
    const NW = 20000;
    for(let k = 0; k < NW; k++){
      ATOM.photons.length = 0;
      firePhoton(ST);
      if(gl.indexOf(ATOM.photons[0].lam) >= 0) onLine++;
    }
    const want = 0.4 + 0.6 * gl.length / (PHET.lamMax - PHET.lamMin + 1);
    rel(onLine / NW, want, 0.04, 'white light is 40 % aimed at the n = 1 lines (PhET)');
    ok(Math.abs(onLine / NW - 0.7) > 0.2, 'and not 70 %');
    let inRange = true;
    for(let k = 0; k < 2000; k++){
      ATOM.photons.length = 0; firePhoton(ST);
      const w = ATOM.photons[0].lam;
      if(w < PHET.lamMin || w > PHET.lamMax || w !== Math.round(w)) inRange = false;
    }
    ok(inRange, 'every white photon is an integer nanometre inside 92-780 nm (PhET)');
  }"""),
    # --- an un-normalised weighted draw: the /tot really is load-bearing
    ("""  ok(lo7 > 0 && hi7 < 1, 'the stream stays inside [0,1)');""",
     """  ok(lo7 > 0 && hi7 < 1, 'the stream stays inside [0,1)');
  {
    /* weighted() normalises; every distribution the sim passes it already sums
       to 1, so the division is invisible unless it is tested with weights that
       do not (Known-bad: a term that cancels in every call is untested) */
    const rgw = makeRng(8888);
    let a3 = 0;
    for(let i = 0; i < 40000; i++) if(rgw.weighted([[1, 3], [2, 1]]) === 1) a3++;
    rel(a3 / 40000, 0.75, 0.02, 'weighted() normalises un-normalised weights (3:1 gives 0.75)');
    ok(makeRng(1).weighted([]) === null, 'an empty distribution returns null');
    ok(makeRng(1).weighted([[7, 0]]) === null, 'an all-zero distribution returns null');
  }"""),
    # --- PhET's state validity, at the boundary the callers never reach
    ("""  ok(phetTransitionAllowed(3, 1, 0, 2, 0, 0), 'dl=1, dm=0 is allowed');""",
     """  ok(validState(2, 1, 1) && validState(2, 1, -1), 'l = n-1 and m = +-l are legal');
  ok(!validState(2, 2, 0), 'l = n is NOT a legal state');
  ok(!validState(2, 1, 2), '|m| > l is not a legal state');
  ok(!validState(7, 0, 0), 'n above PhET\\'s ceiling of 6 is not a legal state');
  ok(phetTransitionAllowed(3, 1, 0, 2, 0, 0), 'dl=1, dm=0 is allowed');"""),
    # --- the tick, the collision radii, the waits and the emission chance
    ("""  /* the classical spiral */""",
     """  /* one tick is 1/60 s of PhET's model: a photon crosses the box in 95 of them */
  eq(Math.round(PHET.boxSide / (PHET.photonSpeed * DT_TICK)), 95,
    'a 300-unit/s photon crosses the 475-unit box in 95 ticks of 1/60 s');
  close(DT_TICK, 1 / 60, 1e-15, 'the tick is 1/60 s');
  {
    Object.assign(ST, DEFAULTS, {model: 'billiard', light: 'mono', lam: 300, lightOn: false});
    atomReset(ST);
    ATOM.photons.push({x: 0, y: -HALF_BOX, dir: PI / 2, lam: 300, emit: false, hit: false, age: 0});
    let k = 0;
    while(ATOM.photons.length && k < 400){ atomTick(ST); k++; }
    eq(k, Math.ceil((PHET.boxSide + 40) / (PHET.photonSpeed * DT_TICK)),
      'and leaves the captured region after ' + k + ' ticks');
  }
  /* the collision geometry: PhET's photon is 15 units and its electron 5 */
  {
    Object.assign(ST, DEFAULTS, {model: 'bohr'});
    atomReset(ST); ATOM.n = 1; ATOM.angle = 0;
    const ee = electronXY(ST);
    ok(quantumCollides(ST, {x: ee[0] + 19.9, y: ee[1], lam: 122}),
      'Bohr: a photon 19.9 units from the electron collides (15 + 5, PhET)');
    ok(!quantumCollides(ST, {x: ee[0] + 20.1, y: ee[1], lam: 122}),
      'and one 20.1 units away does not');
    Object.assign(ST, DEFAULTS, {model: 'debroglie', dbRep: 'radial'});
    atomReset(ST); ATOM.n = 1;
    ok(quantumCollides(ST, {x: viewRadius(1) + 22.9, y: 0, lam: 122}),
      'de Broglie: the whole ring collides out to 23 units (15 + 8, PhET)');
    ok(!quantumCollides(ST, {x: viewRadius(1) + 23.1, y: 0, lam: 122}),
      'and not beyond it');
    ok(quantumCollides(ST, {x: -viewRadius(1), y: 0, lam: 122}),
      'and it collides on the far side too, which a point electron would not');
  }
  /* PhET makes the atom wait 0.75 s before it will absorb */
  function uAbsorbAt(tState){
    Object.assign(ST, DEFAULTS, {model: 'bohr', light: 'mono', lam: 122, lightOn: false});
    atomReset(ST);
    ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; ATOM.tState = tState; ATOM.angle = 0;
    const ee = electronXY(ST);
    return processPhoton(ST, {x: ee[0], y: ee[1], dir: PI / 2, lam: 122, emit: false, hit: false, age: 0});
  }
  ok(!uAbsorbAt(0.70), 'a photon arriving 0.70 s after the last transition is refused (PhET waits 0.75 s)');
  ok(uAbsorbAt(0.80), 'and one arriving at 0.80 s is absorbed');
  /* and 1 s before it will emit, and then a flat 0.5 a tick */
  {
    Object.assign(ST, DEFAULTS, {model: 'bohr', lightOn: false});
    atomReset(ST);
    ATOM.n = 3; ATOM.l = 0; ATOM.m = 0; ATOM.tState = 0;
    let waited = 0;
    while(ATOM.n === 3 && waited < 400){ atomTick(ST); waited++; }
    ok(waited * DT_TICK >= 1.0, 'nothing is emitted before the state is 1 s old ('
      + fmt(waited * DT_TICK, 3) + ' s)');
    let tot = 0, trials = 0;
    for(let k = 0; k < 3000; k++){
      ATOM.n = 3; ATOM.l = 0; ATOM.m = 0; ATOM.tState = PHET.tEmit;
      let t = 0;
      while(ATOM.n === 3 && t < 500){ atomTick(ST); t++; }
      if(ATOM.n !== 3){ tot += t; trials++; }
    }
    ok(trials > 2900, 'every one of the 3000 excited atoms decayed');
    rel(tot / trials, 2, 0.06, 'past 1 s the wait is geometric with mean 2 ticks, i.e. 0.5 a tick (PhET)');
  }
  /* the classical spiral */"""),
    # --- self-referential pins replaced by the literal PhET values
    ("""  rel(ATOM.cls.w / (PHET.classicalOmega0 * DEG), Math.pow(PHET.classicalSpin, ATOM.ticks), 1e-9,
    'the angular speed is multiplied by 1.008 every tick (PhET)');""",
     """  rel(ATOM.cls.w / (600 * DEG), Math.pow(1.008, ATOM.ticks), 1e-9,
    'the angular speed starts at 600 deg/s and is multiplied by 1.008 every tick (PhET)');"""),
    ("""  eq(Object.keys(ATOM.counts).join(','), String(PHET.puddingLam), 'plum pudding emits 150 nm and nothing else');""",
     """  eq(Object.keys(ATOM.counts).join(','), '150', 'plum pudding emits 150 nm and nothing else');"""),
    # --- the emission direction: isotropy has to be tested at n = 4, because
    #     the branch is n < 5 and n = 3 is below either version of it
    ("""    const d = emissionDirection(3, 0.7, rgd);""",
     """    const d = emissionDirection(4, 0.7, rgd);"""),
    ("""  ok(Math.hypot(cs, sn) / 20000 < 0.02, 'below n = 5 the emission is isotropic (PhET)');""",
     """  ok(Math.hypot(cs, sn) / 20000 < 0.02, 'at n = 4 the emission is isotropic: the branch is n < 5 (PhET)');
  {
    let cs5 = 0, sn5 = 0;
    for(let i = 0; i < 20000; i++){
      const d5 = emissionDirection(5, 0.0, rgd);
      cs5 += Math.cos(d5); sn5 += Math.sin(d5);
    }
    ok(Math.hypot(cs5, sn5) / 20000 > 0.9, 'and at n = 5 it is not: it points back along the electron');
  }"""),
])
