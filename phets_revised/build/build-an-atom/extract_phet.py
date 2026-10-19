#!/usr/bin/env python3
"""Pull PhET's data tables out of the minified build-an-atom_en.html (1.9.3).

Four tables, all from SHRED's AtomIdentifier:
  Pq  stableElementTable   Z -> [neutron numbers that give a stable nuclide]
  Sq  numNeutronsInMostCommonIsotope   Z -> N
  _q  standardMassTable    Z -> standard atomic weight / u
  wq  ISOTOPE_INFO_TABLE   Z -> {A: {atomicMass, abundance}}
  fq  symbols              Z -> symbol   ("-" at Z = 0)
  bq  non-localized names  Z -> lower-case name

Written to _out/phet_tables.json.  Nothing here is retyped by hand.
"""
import io
import json
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
ORIG = os.path.normpath(os.path.join(HERE, "..", "..", "..", "phets", "build-an-atom_en.html"))
OUT = os.path.join(HERE, "_out")


def slice_array(s, start, open_ch, close_ch):
    """Return the literal starting at s[start] (which must be open_ch), balanced."""
    assert s[start] == open_ch, (s[start], start)
    d = 0
    i = start
    while i < len(s):
        c = s[i]
        if c == '"' or c == "'":
            q = c
            i += 1
            while s[i] != q:
                i += 2 if s[i] == "\\" else 1
        elif c == open_ch:
            d += 1
        elif c == close_ch:
            d -= 1
            if d == 0:
                return s[start:i + 1]
        i += 1
    raise ValueError("unbalanced")


def grab(s, name, open_ch="[", close_ch="]"):
    m = re.search(re.escape(name) + r"\s*=\s*(?=\%s)" % open_ch, s)
    if not m:
        raise KeyError(name)
    return slice_array(s, m.end(), open_ch, close_ch)


def jsobj_to_json(t):
    """Minified object literals use bare keys, numeric keys and leading-dot
    numbers; none of the three is legal JSON."""
    t = re.sub(r"([{,])\s*([A-Za-z_$][A-Za-z0-9_$]*)\s*:", r'\1"\2":', t)
    t = re.sub(r"([{,])\s*(\d+)\s*:", r'\1"\2":', t)
    t = re.sub(r"([:\[,])\s*\.(\d)", r"\g<1>0.\2", t)
    return t


def main():
    s = io.open(ORIG, encoding="utf-8", errors="replace").read()
    out = {}
    out["stable"] = json.loads(grab(s, "Pq"))
    out["mostCommonN"] = json.loads(grab(s, "Sq"))
    out["standardMass"] = json.loads(grab(s, "_q"))
    out["symbols"] = json.loads(jsobj_to_json(grab(s, "fq")))
    out["names"] = json.loads(jsobj_to_json(grab(s, "bq")))
    out["isotopes"] = json.loads(jsobj_to_json(grab(s, "wq", "{", "}")))
    out["radius"] = json.loads(jsobj_to_json(grab(s, "Vq", "{", "}")))
    if not os.path.isdir(OUT):
        os.makedirs(OUT)
    io.open(os.path.join(OUT, "phet_tables.json"), "w", encoding="utf-8").write(
        json.dumps(out, indent=0, sort_keys=True))
    print("stable        len %d   empty at Z = %s" % (
        len(out["stable"]), [i for i, v in enumerate(out["stable"]) if not v and i > 0]))
    print("mostCommonN   len %d" % len(out["mostCommonN"]))
    print("standardMass  len %d  (last Z = %d, %s)" % (
        len(out["standardMass"]), len(out["standardMass"]) - 1, out["standardMass"][-1]))
    print("symbols       len %d   [0] = %r  [1] = %r  [118] = %r" % (
        len(out["symbols"]), out["symbols"][0], out["symbols"][1], out["symbols"][118]))
    print("names         len %d" % len(out["names"]))
    print("isotopes      %d elements, Z = %s .. %s" % (
        len(out["isotopes"]), min(int(k) for k in out["isotopes"]),
        max(int(k) for k in out["isotopes"])))
    print("radius        %d entries" % len(out["radius"]))
    # the heaviest stable nuclide PhET believes in
    best = None
    for z, ns in enumerate(out["stable"]):
        for n in ns:
            if best is None or z + n > best[0] + best[1]:
                best = (z, n)
    print("heaviest stable in PhET's table: Z = %d, N = %d, A = %d (%s)" % (
        best[0], best[1], best[0] + best[1], out["symbols"][best[0]]))


if __name__ == "__main__":
    main()
