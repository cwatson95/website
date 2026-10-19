#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Two guards on one path make each other's mutant equivalent (Known-bad).

phetLowerDist opened with `let lo = Math.max(l, 1); if(l === 0) lo = 2;` — the
Math.max only ever differs from a plain `l` when l is 0, and the next line
overwrites lo in exactly that case.  So mutating the 1 to a 0 changed nothing
any harness could see, and the sweep correctly reported a survivor that was a
redundancy.  One guard, written once.
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


patch("p2_physics.js", [
    ("""  let lo = Math.max(l, 1);
  if(l === 0) lo = 2;
  let tot = 0;""",
     """  /* an s state cannot go to n' = 1 (that would be s -> s), so PhET starts it
     at 2; every other l starts at l itself.  Written as ONE decision: the
     Math.max(l,1) that used to stand in front of it could only ever differ at
     l = 0, where the next line overwrote it, so its mutant was equivalent. */
  const lo = (l === 0) ? 2 : l;
  let tot = 0;"""),
])

patch("gen_mutants.py", [
    ("""m("PhET lower-n floor", "let lo = Math.max(l, 1);", "let lo = Math.max(l, 0);")
m("PhET s-state floor", "if(l === 0) lo = 2;", "if(l === 0) lo = 1;")""",
     """m("PhET lower-n floor", "const lo = (l === 0) ? 2 : l;", "const lo = (l === 0) ? 2 : 1;")
m("PhET s-state floor", "const lo = (l === 0) ? 2 : l;", "const lo = (l === 0) ? 1 : l;")"""),
])
