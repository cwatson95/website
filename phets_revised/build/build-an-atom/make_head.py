#!/usr/bin/env python3
"""Build p1_head.html: the house scaffold taken verbatim from the landed
rutherford-scattering build (CSS, site nav, body markup) with only the header
comment, the <title>, the <h1>, the .sub tagline and the role-colour block
replaced.  The PLAYBOOK's rule: extract the aesthetic, do not retype it."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.normpath(os.path.join(HERE, "..", "rutherford-scattering", "p1_head.html"))

HEAD = u"""<!doctype html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Build an atom &mdash; three integers and one table</title>
<!--
  ===================================================================
  build-an-atom.html — a remake of PhET's Build an Atom: drop protons,
  neutrons and electrons into a nucleus and watch the element, the
  mass number, the charge and the stability follow
  ===================================================================

  Remake of PhET Interactive Simulations' Build an Atom (University of
  Colorado Boulder, phet.colorado.edu, CC-BY 4.0).  New code; no PhET
  code or assets.  Built against PhET's build-an-atom 1.9.3: all three
  of its screens (Atom, Symbol, Game), its three buckets of 10 protons,
  13 neutrons and 10 electrons, its orbits/cloud model switch, its
  Element Name / Neutral Atom or Ion / Nuclear Stability displays, its
  periodic table, its two charge-sign conventions, and its four game
  levels of five challenges scored 2 and 1 — with its data tables and
  its view constants read out of the minified original.

  SIX VIEWS.  THE ATOM is PhET's first screen: the buckets, the
  nucleus, the shells or the cloud, and the four things the counts
  determine.  THE SYMBOL is its second: the same atom written as a
  nuclear symbol, mass number over atomic number with the charge on
  the shoulder.  THE GAME is its third: four levels, five challenges,
  seeded so a level can be replayed exactly.  THE COUNTING is the
  whole space the buckets can reach — 1694 configurations — with the
  census that makes the three rules checkable rather than merely
  stated.  THE CHART OF NUCLIDES puts PhET's whole stability table on
  the (N, Z) plane beside an independent one.  MASS AND BINDING is the
  measured data: isotope masses, natural abundances, the standard
  atomic weight as their mean, and the binding energy those masses
  imply.

  WHAT IS EXACT HERE
  ------------------
  The three rules are arithmetic on three integers and are exact by
  construction: the element IS the proton count, A = Z + N, q = Z - e.
  selfTest walks all 11 x 14 x 11 = 1694 configurations the buckets
  allow and checks every one of them against an independently written
  expression, so "exact across the whole range the sim allows" is a
  measurement and not a claim.  The charge strings, the ion wording,
  the shell filling (2 then 8), PhET's cloud radius
  r(e) = 42.5 + 8.75 e and its ten electron slots are pinned against
  the values read out of the original.  The game's generator is a
  seeded mulberry32 reproduced bit for bit in Python, and 16 000
  generated levels are checked for solvability, for the no-repeat rule
  and for PhET's Z ranges; the scoring is integer arithmetic and is
  asserted on every path through a level.

  WHAT IS MEASURED, AND BY WHOM
  -----------------------------
  Stability is NOT a formula.  Which (Z, N) combinations are stable is
  a table, and the one this file uses is PhET's own
  stableElementTable — 244 nuclides, Z = 1 to 82 — read out of
  SHRED's AtomIdentifier.  It is cross-checked here against an
  independent table (NUBASE half-lives and NIST isotopic compositions,
  by way of this repo's own periodic_table.html), whose criterion is
  "occurs in nature and has never been observed to decay": 253
  nuclides.  The two agree on 243.  PhET alone calls germanium-76
  stable, which has a measured double-beta half-life of 1.9e21 yr; the
  independent table alone calls ten more stable (Cr-50, Zn-70, Te-123,
  Xe-124, Xe-134, Ba-132, Ce-138, Ce-142, W-183, Pb-204), every one of
  them a nuclide whose predicted decay has never been seen.  Below
  Z = 24 the two are IDENTICAL, so over everything this sim can build
  the stability data is not in dispute.  Both stop at lead: neither
  calls bismuth-209 stable, and its 2.0e19 yr alpha decay is why.
  Both give technetium and promethium no stable isotope at all.

  Isotope atomic masses and natural abundances are PhET's own tables
  (Z = 1 to 18), which come from AME/NIST; they agree with the
  independent mass excesses to 1.6e-6 u and with the NIST abundances
  to 3.2e-3 percentage points, and the resulting binding energies per
  nucleon agree to 1.6e-4 MeV, which is why B/A is quoted to three
  decimals.  Standard atomic weights are PhET's standardMassTable;
  Sigma(abundance x mass) reproduces them to 1.4e-4 relative, worst at
  lithium, whose isotopic composition genuinely varies between natural
  sources.  The neutron mass and the u-to-MeV conversion are CODATA
  2022 through scipy.constants.  The atomic radii used for the scale
  note are PhET's own (the Clementi calculated radii: hydrogen's is
  the Bohr radius), and the nuclear radius is the textbook
  1.2 A^(1/3) fm; every exaggeration factor is printed on the canvas
  for the nuclide on screen.

  The game's fallback is PhET's: when the filtered pool of atoms is
  empty it reuses one already posed.  That path is reachable exactly
  once in 16 000 generated levels — level 2 at seed 2691, whose five
  all-schematic challenges exhaust the four charged atoms with Z < 3 —
  and the suite asserts that RATE rather than forbidding the
  behaviour.

  NOT MODELLED
  ------------
  No nuclear physics: nothing here computes why a nuclide is stable,
  and the file says so on the canvas — the binding-energy curve is
  drawn FROM the measured masses, not from a mass formula.  No
  chemistry: the electron shells are PhET's two-then-eight cartoon,
  not orbitals, and nothing decides whether an ion is one a chemist
  would meet.  No decay: an unstable nucleus here sits there being
  unstable.  No electron binding energy in the mass arithmetic (it is
  eV-scale against MeV-scale nuclear binding, which is why B/A is
  quoted to three decimals).  PhET's particle animation, its sound and
  its accessibility layer are not reproduced.

  WHERE THE NUMBERS COME FROM
  ---------------------------
  PhET's tables and constants: build/build-an-atom/extract_phet.py
  reads them out of docs/phets/build-an-atom_en.html (1.9.3) —
  stableElementTable, numNeutronsInMostCommonIsotope,
  standardMassTable, the isotope table, the symbol and element-name
  strings, the atomic radii, the bucket sizes, the shell radii and the
  ten slots, the cloud law, the two capture radii, the four
  AtomValuePool challenge pools and the scoring constants.  The
  independent nuclide table and the periodic-table layout come from
  projects/simulations/periodic_table.html (NUBASE via mendeleev/IAEA;
  NIST Atomic Weights and Isotopic Compositions).  Every reference
  number selfTest asserts against is a line of
  build/build-an-atom/_out/refvals.txt, emitted into p7_refs.js by
  make_refs.py from derive.py — nothing is transcribed by hand.
-->
"""

ROLE = u"""    /* role colours.  PhET's own three particles keep their identities:
       proton orange, neutron grey, electron cyan (PhET draws them
       orange-red, grey and blue).  On top of the house scheme: green =
       the thing this file computes and the word "stable", orange = the
       warning ("unstable") and the reference value, magenta = the live
       marker (the nuclide you have built, the held particle), cyan =
       structure (shells, axes, the periodic-table grid). */
"""


def main():
    src = io.open(SRC, encoding="utf-8").read()
    body = src[src.index("<style>"):]
    # replace the role-colour comment block inside :root
    i = body.index("    /* role colours:")
    j = body.index("    --pos:", i)
    body = body[:i] + ROLE + body[j:]
    body = body.replace(
        "--pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4; --wplus:#5ac8e0; --wminus:#e8843a;",
        "--pos:#b8ec4c; --ref:#e8843a; --live:#cd35c4;\n"
        "    --proton:#e8843a; --neutron:#8b93a6; --electron:#5ac8e0;")
    body = body.replace("<h1>Rutherford scattering</h1>", "<h1>Build an atom</h1>")
    k = body.index('<span class="sub" id="sub">')
    e = body.index("</span>", k)
    body = body[:k] + ('<span class="sub" id="sub">A remake of PhET&rsquo;s Build an Atom: '
                       'the element is the proton count, A = Z + N, q = Z &minus; e '
                       '&mdash; and whether the nucleus is stable is a table, not a formula'
                       ) + body[e:]
    out = HEAD + body
    io.open(os.path.join(HERE, "p1_head.html"), "w", encoding="utf-8").write(out)
    print("p1_head.html  %d lines" % len(out.splitlines()))
    for must in ["site-nav-css", "cooper-watson.net/cv.html", 'aria-current="page"',
                 "#eqbar", "#readout", "<script>", "Build an atom"]:
        assert must in out, must
    print("  scaffold checks pass")


if __name__ == "__main__":
    main()
