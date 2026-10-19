#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""One implementation of PhET's choose_l / choose_m, not three.

They were written out three times — as a declarative distribution in
p2_physics.js, inline in setNLM (the live atom) and inline again in
cascadeSchrodinger (the ensemble) — which is the group-velocity-written-
out-three-times shape on the Known-bad list: a mutant on the declarative copy
changed nothing any test could see, because nothing the sim draws went through
it.  Both callers now DRAW from the distribution, so there is one statement of
the rule and every mutant on it is live.

That changes how many random numbers a decay consumes (one weighted draw per
choice instead of a bare next()/int()), so derive.py's cascade references move
with it — both sides are changed together and the bit-for-bit pins still hold.
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


patch("p3_state.js", [
    ("""function setNLM(st, nNew){
  const l = ATOM.l, m = ATOM.m;
  let lp;
  if(l === 0) lp = 1;
  else if(l === nNew || l === nNew - 1) lp = l - 1;
  else lp = ATOM.rng.next() < 0.5 ? l + 1 : l - 1;
  let mp;
  if(lp === 0) mp = 0;
  else if(m > lp) mp = lp;
  else if(m < -lp) mp = -lp;
  else if(m === lp) mp = ATOM.rng.int(2) === 0 ? m : m - 1;
  else if(m === -lp) mp = ATOM.rng.int(2) === 0 ? m : m + 1;
  else { const k = ATOM.rng.int(3); mp = k === 0 ? m + 1 : (k === 1 ? m - 1 : m); }
  if(!phetTransitionAllowed(ATOM.n, l, m, nNew, lp, mp)){ ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; return; }
  ATOM.n = nNew; ATOM.l = lp; ATOM.m = mp;
}""",
     """function setNLM(st, nNew){
  const l = ATOM.l, m = ATOM.m;
  const lp = ATOM.rng.weighted(phetChooseL(l, nNew));
  const mp = ATOM.rng.weighted(phetChooseM(m, lp));
  if(!phetTransitionAllowed(ATOM.n, l, m, nNew, lp, mp)){ ATOM.n = 1; ATOM.l = 0; ATOM.m = 0; return; }
  ATOM.n = nNew; ATOM.l = lp; ATOM.m = mp;
}"""),
])

patch("p2_physics.js", [
    ("""    const nn = rng.weighted(d);
    let lp;
    if(l === 0) lp = 1;
    else if(l === nn || l === nn - 1) lp = l - 1;
    else lp = rng.next() < 0.5 ? l + 1 : l - 1;
    let mp;
    if(lp === 0) mp = 0;
    else if(m > lp) mp = lp;
    else if(m < -lp) mp = -lp;
    else if(m === lp) mp = rng.int(2) === 0 ? m : m - 1;
    else if(m === -lp) mp = rng.int(2) === 0 ? m : m + 1;
    else { const k = rng.int(3); mp = k === 0 ? m + 1 : (k === 1 ? m - 1 : m); }
    let tn = nn, tl = lp, tm = mp;""",
     """    const nn = rng.weighted(d);
    const lp = rng.weighted(phetChooseL(l, nn));
    const mp = rng.weighted(phetChooseM(m, lp));
    let tn = nn, tl = lp, tm = mp;"""),
])
