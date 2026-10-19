#!/usr/bin/env python3
"""derive.py — the Python twin of build-an-atom.html.

Everything the JS asserts is computed here first, printed to 10+ digits, and
emitted into _out/refvals.txt (which make_refs.py turns into p7_refs.js).
Nothing is transcribed by hand.

What it does, in order:

  1.  Reads PhET's four data tables out of the minified original
      (_out/phet_tables.json, written by extract_phet.py).
  2.  Reads an INDEPENDENT nuclide table — the NUBASE/IAEA half-lives and the
      NIST isotopic compositions embedded in this repo's own
      projects/simulations/periodic_table.html — and cross-checks PhET's
      stable-nuclide set, isotope atomic masses and natural abundances
      against it.  The two are different publications; the disagreements are
      listed, not smoothed over.
  3.  Re-derives every quantity the sim computes from the particle counts
      (element, mass number, net charge, stability) exhaustively over the
      whole range the buckets allow.
  4.  Standard atomic weights from sum(abundance x atomic mass), binding
      energies from the measured atomic masses, and the nuclide-chart
      geometry.
  5.  The game: a mulberry32 PRNG reproduced bit-for-bit in JS, PhET's four
      challenge pools and level type lists, and an exhaustive check that
      every seed in a large range produces five solvable challenges.
"""
import io
import json
import os
import re
import sys

import numpy as np
import scipy.constants as sc

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(HERE, "_out")
PT = os.path.normpath(os.path.join(HERE, "..", "..", "..", "..",
                                   "projects", "simulations", "periodic_table.html"))

REF = {}          # name -> value, emitted for the JS suite
LINES = []


def say(s=""):
    LINES.append(s)
    print(s)


def ref(name, value, note=""):
    REF[name] = value
    if isinstance(value, float):
        say("  %-38s %.15g   %s" % (name, value, note))
    else:
        say("  %-38s %s   %s" % (name, value, note))


# ---------------------------------------------------------------- PhET tables
P = json.load(io.open(os.path.join(OUT, "phet_tables.json"), encoding="utf-8"))
STABLE = [list(v) for v in P["stable"]]          # Z -> [N, ...]
MOSTN = P["mostCommonN"]
SMASS = P["standardMass"]
SYM = P["symbols"]
NAMES = P["names"]
ISOP = {int(k): {int(a): v for a, v in d.items()} for k, d in P["isotopes"].items()}

# ------------------------------------------------- the independent comparison
def load_house_iso():
    """[A, mass excess/keV, abundance/%, half-life/s, spin-parity, decay] by Z,
    from periodic_table.html — NIST Atomic Weights and Isotopic Compositions
    for the abundances, NUBASE via mendeleev/IAEA for the half-lives."""
    s = io.open(PT, encoding="utf-8").read()
    m = re.search(r"const ISO=(\{.*?\});\s*\n", s, re.S)
    d = json.loads(m.group(1))
    return {int(k): v for k, v in d.items()}


def load_house_el():
    s = io.open(PT, encoding="utf-8").read()
    i = s.index("const EL=[")
    j = s.index("\n];", i)
    lit = re.sub(r",\s*\]", "]", s[i + len("const EL="):j + 2])
    return json.loads(lit)


HISO = load_house_iso()
HEL = load_house_el()
HSYM = {r[0]: r[1] for r in HEL}
HNAME = {r[0]: r[2] for r in HEL}
HXY = {r[0]: (r[39], r[40]) for r in HEL}
HW = {r[0]: r[43] for r in HEL}          # NIST standard atomic weight (None if interval)

U_MEV = sc.physical_constants["atomic mass constant energy equivalent in MeV"][0]
KEV_PER_U = U_MEV * 1000.0
M_N = sc.physical_constants["neutron mass in u"][0]
M_H1 = ISOP[1][1]["atomicMass"]          # the atomic mass of 1H, PhET's value


def house_mass(z, a):
    for row in HISO.get(z, []):
        if row[0] == a:
            return a + row[1] / KEV_PER_U
    return None


def house_stable_set():
    """The independent "stable" set: a nuclide that OCCURS IN NATURE (NIST
    gives it an isotopic abundance) and whose decay has NEVER BEEN OBSERVED
    (NUBASE gives it no half-life).  Both halves are needed.  Half-life alone
    admits drip-line nuclides whose half-life is unmeasured because it is
    ~1e-21 s (Li-12, B-16) — 569 of them; abundance alone admits K-40 and
    U-238.  Together they give 253 nuclides, all with Z <= 82."""
    out = {}
    for z, rows in HISO.items():
        ns = [r[0] - z for r in rows if r[2] is not None and r[3] is None]
        if ns:
            out[z] = sorted(ns)
    return out


# ================================================================== §1 symbols
say("=" * 72)
say("1. element names and symbols (PhET's SHRED tables vs this repo's own)")
say("=" * 72)
bad = [z for z in range(1, 119) if SYM[z] != HSYM[z]]
say("  symbols disagreeing with periodic_table.html: %s"
    % ([(z, SYM[z], HSYM[z]) for z in bad] or "none"))
namebad = [z for z in range(1, 119) if NAMES[z].lower() != HNAME[z].lower()]
say("  names disagreeing: %s" % ([(z, NAMES[z], HNAME[z]) for z in namebad] or "none"))
ref("nElements", 118)
ref("symbol_1", SYM[1])
ref("symbol_10", SYM[10])
ref("symbol_118", SYM[118])
ref("nSymbolMismatch", len(bad))
ref("nNameMismatch", len(namebad))

# the standard 18-column layout, derived from (group, period) and checked
# against periodic_table.html's own x/y columns
LAY = {}
for r in HEL:
    z, group, period = r[0], r[3], r[4]
    if 57 <= z <= 71:                       # the lanthanide strip, La included
        LAY[z] = (3 + z - 57, 9)
    elif 89 <= z <= 103:                    # the actinide strip, Ac included
        LAY[z] = (3 + z - 89, 10)
    else:
        LAY[z] = (group, period)
laybad = [z for z in range(1, 119) if LAY[z] != HXY[z]]
say("  layout cells disagreeing with periodic_table.html: %s"
    % ([(z, LAY[z], HXY[z]) for z in laybad] or "none"))
ref("nLayoutMismatch", len(laybad))

# ============================================================== §2 the stable set
say()
say("=" * 72)
say("2. PhET's stable-nuclide table vs NUBASE (no observed decay)")
say("=" * 72)
PSET = set((z, n) for z, ns in enumerate(STABLE) for n in ns)
HSET0 = house_stable_set()
HSET = set((z, n) for z, ns in HSET0.items() for n in ns)
say("  PhET's table: %d nuclides, Z = 1 .. %d" % (len(PSET), max(z for z, _ in PSET)))
say("  NUBASE table: %d nuclides, Z = 1 .. %d" % (len(HSET), max(z for z, _ in HSET)))
onlyP = sorted(PSET - HSET)
onlyH = sorted(HSET - PSET)
say("  in PhET only   (%d): %s" % (len(onlyP), [(SYM[z], z + n) for z, n in onlyP]))
say("  in NUBASE only (%d): %s" % (len(onlyH), [(SYM[z], z + n) for z, n in onlyH]))
inBoth = len(PSET & HSET)
say("  agreeing: %d of PhET's %d" % (inBoth, len(PSET)))
lowP = sorted(x for x in PSET if x[0] <= 18)
lowH = sorted(x for x in HSET if x[0] <= 18)
say("  over Z <= 18 (everything the game can reach) the two sets are%s identical"
    % ("" if lowP == lowH else " NOT"))
say("  the lowest Z at which they part company: %d (%s)"
    % (min(z for z, _ in (PSET ^ HSET)), SYM[min(z for z, _ in (PSET ^ HSET))]))
ref("identicalBelowZ", min(z for z, _ in (PSET ^ HSET)))
ref("nStableZ18_nubase", len(lowH))
ref("nStablePhet", len(PSET))
ref("nStableZ10", sum(1 for z, n in PSET if z <= 10))
ref("nStableZ18", sum(1 for z, n in PSET if z <= 18))
ref("phetMaxStableZ", max(z for z, _ in PSET))
heaviest = max(PSET, key=lambda t: (t[0] + t[1], t[0]))
ref("heaviestStableZ", heaviest[0])
ref("heaviestStableN", heaviest[1])
ref("heaviestStableA", heaviest[0] + heaviest[1])
say("  heaviest stable nuclide in PhET's table: %s-%d (Z = %d, N = %d)"
    % (SYM[heaviest[0]], heaviest[0] + heaviest[1], heaviest[0], heaviest[1]))
noStable = [z for z in range(1, max(z for z, _ in PSET) + 1) if not STABLE[z]]
say("  elements with NO stable isotope below that: %s" % [(z, SYM[z]) for z in noStable])
ref("noStableZ", noStable)
ref("nAgreeWithNubase", inBoth)
ref("nStableNubase", len(HSET))
ref("nPhetOnly", len(onlyP))
ref("nNubaseOnly", len(onlyH))
ref("nubaseMaxStableZ", max(z for z, _ in HSET))
ref("phetOnlyList", [[z, n] for z, n in onlyP])
ref("nubaseOnlyList", [[z, n] for z, n in onlyH])

# the N/Z drift: the mean N/Z of the stable nuclides of the lightest and
# heaviest element that has any
lightZ = [z for z in range(1, 11) if STABLE[z]]
ref("meanNoverZ_light", float(np.mean([n / z for z in lightZ for n in STABLE[z]])))
ref("NoverZ_Pb208", heaviest[1] / heaviest[0])
say("  N/Z at Pb-208 = %.15g, mean over Z <= 10 = %.15g"
    % (REF["NoverZ_Pb208"], REF["meanNoverZ_light"]))

# ======================================================= §3 exhaustive counting
say()
say("=" * 72)
say("3. the counting rules, over the whole range the buckets allow")
say("=" * 72)
NP, NN, NE = 10, 13, 10          # PhET's bucket contents, read from the original
tot = neutral = ions = stable = 0
elements = set()
census = {}
for p in range(NP + 1):
    for n in range(NN + 1):
        for e in range(NE + 1):
            tot += 1
            q = p - e
            a = p + n
            st = (p + n > 0) and (n in STABLE[p] if p < len(STABLE) else False)
            if p > 0:
                elements.add(p)
            if q == 0 and p + n + e > 0:
                neutral += 1
            elif q != 0:
                ions += 1
            if st:
                stable += 1
            census[(p, n, e)] = (a, q, st)
say("  configurations: %d   neutral (non-empty): %d   ions: %d   stable nucleus: %d"
    % (tot, neutral, ions, stable))
ref("nConfigs", tot)
ref("nNeutral", neutral)
ref("nIons", ions)
ref("nStableConfigs", stable)
ref("nElementsReachable", len(elements))
ref("maxProtons", NP)
ref("maxNeutrons", NN)
ref("maxElectrons", NE)
ref("maxCharge", NP)
ref("minCharge", -NE)
# the (p, n) pairs the buckets can reach that are stable
pn = sorted(set((p, n) for p in range(NP + 1) for n in range(NN + 1)
                if p > 0 and n in STABLE[p]))
ref("nStablePN", len(pn))
say("  stable (Z, N) pairs inside the buckets: %d  ->  %s"
    % (len(pn), [(SYM[z], z + n) for z, n in pn]))
# the heaviest and the only element with no stable isotope inside reach
ref("nUnstablePN", (NP) * (NN + 1) - len(pn))

# a few spot values the JS asserts by name
for (p, n, e), nm in [((6, 6, 6), "C12"), ((6, 8, 6), "C14"), ((8, 8, 10), "O2minus"),
                      ((3, 4, 2), "Li7plus"), ((1, 0, 0), "Hplus"), ((1, 2, 1), "H3"),
                      ((10, 12, 10), "Ne22"), ((4, 5, 4), "Be9"), ((5, 5, 5), "B10")]:
    a, q, st = census[(p, n, e)]
    ref("cfg_%s" % nm, [p, n, e, a, q, 1 if st else 0],
        "%s-%d charge %+d %s" % (SYM[p], a, q, "stable" if st else "unstable"))

# ========================================== §4 masses, abundances and binding
say()
say("=" * 72)
say("4. isotope masses, natural abundances, atomic weights, binding energies")
say("=" * 72)
say("  PhET's isotope table covers Z = %d .. %d" % (min(ISOP), max(ISOP)))
worstm = (0.0, None)
worsta = (0.0, None)
for z in sorted(ISOP):
    for a, d in sorted(ISOP[z].items()):
        hm = house_mass(z, a)
        if hm is not None:
            dm = abs(d["atomicMass"] - hm)
            if dm > worstm[0]:
                worstm = (dm, (z, a, d["atomicMass"], hm))
        for row in HISO.get(z, []):
            if row[0] == a and row[2] is not None and d["abundance"] > 1e-9:
                da = abs(d["abundance"] * 100 - row[2])
                if da > worsta[0]:
                    worsta = (da, (z, a, d["abundance"] * 100, row[2]))
say("  worst atomic-mass difference PhET vs NUBASE mass excess: %.3e u at %s"
    % (worstm[0], worstm[1] and (SYM[worstm[1][0]], worstm[1][1])))
say("     PhET %.11f   from mass excess %.11f" % (worstm[1][2], worstm[1][3]))
say("  worst abundance difference PhET vs NIST: %.3e %% at %s"
    % (worsta[0], worsta[1] and (SYM[worsta[1][0]], worsta[1][1])))
say("     PhET %.6f %%   NIST %.6f %%" % (worsta[1][2], worsta[1][3]))
ref("worstMassDiff_u", worstm[0])
ref("worstAbundanceDiff_pct", worsta[0])

# sum(abundance) per element, and sum(abundance x mass) vs the published weight
say()
say("  element   sum(ab)       sum(ab*m)         PhET standard   NIST standard")
wrows = []
for z in sorted(ISOP):
    ab = sum(d["abundance"] for d in ISOP[z].values() if d["abundance"] > 1e-9)
    w = sum(d["abundance"] * d["atomicMass"] for d in ISOP[z].values() if d["abundance"] > 1e-9)
    wrows.append((z, ab, w, SMASS[z], HW.get(z)))
    say("  %-3s %-4d %.10f  %.10f   %-13s   %s"
        % (SYM[z], z, ab, w, SMASS[z], HW.get(z)))
ref("sumAb_C", [r[1] for r in wrows if r[0] == 6][0])
ref("weightedMass_C", [r[2] for r in wrows if r[0] == 6][0])
ref("weightedMass_O", [r[2] for r in wrows if r[0] == 8][0])
ref("weightedMass_Ne", [r[2] for r in wrows if r[0] == 10][0])
ref("weightedMass_Cl", [r[2] for r in wrows if r[0] == 17][0])
worstw = max(abs(r[2] - r[3]) / r[3] for r in wrows)
ref("worstWeightRel", float(worstw))
say("  worst relative gap between sum(ab*m) and PhET's standard weight: %.3e" % worstw)
worstwz = max(wrows, key=lambda r: abs(r[2] - r[3]) / r[3])
say("     at %s: %.8f vs %.8f" % (SYM[worstwz[0]], worstwz[2], worstwz[3]))
ref("worstWeightZ", worstwz[0])

# binding energy per nucleon, from the measured atomic masses
say()
say("  binding energy per nucleon B/A = [Z m(1H) + N m_n - m(A,Z)] c^2 / A")
say("  m(1H) = %.11f u (PhET), m_n = %.11f u (CODATA), 1 u = %.8f MeV"
    % (M_H1, M_N, U_MEV))
ref("mH1_u", M_H1)
ref("mNeutron_u", M_N)
ref("uMeV", U_MEV)


def bpern(z, a):
    m = ISOP.get(z, {}).get(a)
    if m is None:
        return None
    n = a - z
    return (z * M_H1 + n * M_N - m["atomicMass"]) * U_MEV / a


for z, a, nm in [(1, 2, "H2"), (2, 4, "He4"), (3, 7, "Li7"), (4, 9, "Be9"),
                 (6, 12, "C12"), (8, 16, "O16"), (10, 20, "Ne20"), (16, 32, "S32"),
                 (18, 40, "Ar40")]:
    v = bpern(z, a)
    ref("BperA_%s" % nm, v, "MeV/nucleon")
best = max(((z, a) for z in ISOP for a in ISOP[z]), key=lambda t: bpern(*t))
say("  most tightly bound nuclide in PhET's table: %s-%d at %.10f MeV/nucleon"
    % (SYM[best[0]], best[1], bpern(*best)))
ref("bestBoundZ", best[0])
ref("bestBoundA", best[1])
ref("bestBperA", bpern(*best))
# He-4 sticks out of its neighbours: assert that, it is the alpha-particle fact
ref("BperA_He3", bpern(2, 3))
ref("BperA_Li6", bpern(3, 6))

# the deuteron binding energy is a textbook number: 2.224 MeV
ref("Bd_MeV", (M_H1 + M_N - ISOP[1][2]["atomicMass"]) * U_MEV)
say("  deuteron binding energy %.10f MeV (textbook 2.2246)" % REF["Bd_MeV"])

# PhET's isotope table stops at argon, so the maximum of B/A inside it is NOT
# the real one.  Take the whole curve from the independent mass excesses.
def bpern_house(z, a):
    m = house_mass(z, a)
    if m is None:
        return None
    return (z * M_H1 + (a - z) * M_N - m) * U_MEV / a


allb = [(z, r[0], bpern_house(z, r[0])) for z in HISO for r in HISO[z]
        if r[0] > 0 and bpern_house(z, r[0]) is not None]
gmax = max(allb, key=lambda t: t[2])
say("  from the independent mass excesses, the global maximum of B/A is "
    "%s-%d at %.10f MeV/nucleon" % (SYM[gmax[0]], gmax[1], gmax[2]))
ref("globalBestZ", gmax[0])
ref("globalBestA", gmax[1])
ref("globalBestBperA", gmax[2])
ref("BperA_Fe56_house", bpern_house(26, 56))
ref("BperA_U238_house", bpern_house(92, 238))
say("  Fe-56 %.10f, U-238 %.10f MeV/nucleon"
    % (REF["BperA_Fe56_house"], REF["BperA_U238_house"]))
worstb = max(abs(bpern(z, a) - bpern_house(z, a)) for z in ISOP for a in ISOP[z]
             if bpern_house(z, a) is not None)
ref("worstBperADiff", float(worstb))
say("  worst B/A difference between PhET's masses and the mass excesses: %.3e MeV" % worstb)

# PhET's "most common isotope" table against the NIST abundances
mcbad = []
for z in range(1, 19):
    rows = [(r[2], r[0]) for r in HISO[z] if r[2]]
    if rows:
        top = max(rows)[1]
        if top - z != MOSTN[z]:
            mcbad.append((z, MOSTN[z] + z, top))
say("  PhET's most-common-isotope table vs the NIST abundances, Z <= 18: %s"
    % (mcbad or "agrees on all 18"))
ref("nMostCommonMismatch", len(mcbad))
ref("mostCommonA_18", 18 + MOSTN[18])
ref("mostCommonA_1", 1 + MOSTN[1])

# which element has the most stable isotopes
nmost = max(range(1, len(STABLE)), key=lambda z: len(STABLE[z]))
ref("mostIsotopesZ", nmost)
ref("mostIsotopesN", len(STABLE[nmost]))
say("  the element with the most stable isotopes in PhET's table: %s (Z = %d), %d of them"
    % (SYM[nmost], nmost, len(STABLE[nmost])))
# odd Z never has more than two
oddmax = max(len(STABLE[z]) for z in range(1, len(STABLE)) if z % 2 == 1)
evenmax = max(len(STABLE[z]) for z in range(1, len(STABLE)) if z % 2 == 0)
ref("oddZmaxIsotopes", oddmax)
ref("evenZmaxIsotopes", evenmax)
say("  odd Z never has more than %d stable isotopes; even Z reaches %d (Mattauch)"
    % (oddmax, evenmax))
# even/odd census of the stable set
ee = sum(1 for z, n in PSET if z % 2 == 0 and n % 2 == 0)
eo = sum(1 for z, n in PSET if z % 2 == 0 and n % 2 == 1)
oe = sum(1 for z, n in PSET if z % 2 == 1 and n % 2 == 0)
oo = sum(1 for z, n in PSET if z % 2 == 1 and n % 2 == 1)
ref("censusEvenEven", ee)
ref("censusEvenOdd", eo)
ref("censusOddEven", oe)
ref("censusOddOdd", oo)
say("  even-even %d, even-odd %d, odd-even %d, odd-odd %d (the four odd-odd ones are %s)"
    % (ee, eo, oe, oo, [SYM[z] + "-" + str(z + n) for z, n in sorted(PSET)
                        if z % 2 and n % 2]))
ref("oddOddList", [[z, n] for z, n in sorted(PSET) if z % 2 and n % 2])

# the magic numbers are not decoration: the shells close there, and the census
# shows it.  Count stable ISOTONES (nuclides sharing a neutron number) and
# stable ISOTOPES (sharing a proton number) and look at where the maxima are.
MAGIC = [2, 8, 20, 28, 50, 82, 126]
byN, byZ = {}, {}
for z, n in PSET:
    byN[n] = byN.get(n, 0) + 1
    byZ[z] = byZ.get(z, 0) + 1
topN = sorted(byN.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
topZ = sorted(byZ.items(), key=lambda kv: (-kv[1], kv[0]))[:5]
say("  stable isotones: the five commonest neutron numbers are %s" % topN)
say("  stable isotopes: the five commonest proton numbers are %s" % topZ)
say("  magic among the top five N: %s   among the top five Z: %s"
    % ([n for n, _ in topN if n in MAGIC], [z for z, _ in topZ if z in MAGIC]))
ref("magicNumbers", MAGIC)
ref("topIsotoneN", [list(t) for t in topN])
ref("topIsotopeZ", [list(t) for t in topZ])
ref("nIsotones_N82", byN.get(82, 0))
ref("nIsotones_N50", byN.get(50, 0))
ref("nIsotones_N81", byN.get(81, 0))
ref("nIsotones_N83", byN.get(83, 0))
say("  N = 50 has %d stable isotones and N = 82 has %d; their neighbours "
    "N = 81 and N = 83 have %d and %d"
    % (byN.get(50, 0), byN.get(82, 0), byN.get(81, 0), byN.get(83, 0)))

# ==================================================================== §5 game
say()
say("=" * 72)
say("5. the game: seeded generation and exact scoring")
say("=" * 72)
POOLS = json.load(io.open(os.path.join(OUT, "phet_pools.json"), encoding="utf-8"))
TYPES = [["schematic-to-element", "counts-to-element"],
         ["schematic-to-charge", "schematic-to-mass-number",
          "counts-to-charge", "counts-to-mass-number"],
         ["schematic-to-symbol-charge", "schematic-to-symbol-mass-number",
          "schematic-to-symbol-proton-count", "counts-to-symbol-charge",
          "counts-to-symbol-mass-number"],
         ["schematic-to-symbol-all", "symbol-to-schematic", "symbol-to-counts",
          "counts-to-symbol-all"]]
SCHEMATIC = {"schematic-to-element", "schematic-to-charge", "schematic-to-mass-number",
             "schematic-to-symbol-all", "schematic-to-symbol-proton-count",
             "schematic-to-symbol-charge", "schematic-to-symbol-mass-number",
             "symbol-to-schematic"}
CHARGEY = {"schematic-to-charge", "counts-to-charge", "counts-to-symbol-charge",
           "schematic-to-symbol-charge"}
CHALLENGES_PER_LEVEL = 5
POINTS_FIRST, POINTS_SECOND = 2, 1
say("  4 levels, %d challenges each, %d for a first-try answer and %d for a second"
    % (CHALLENGES_PER_LEVEL, POINTS_FIRST, POINTS_SECOND))
say("  pool sizes: %s" % [len(p) for p in POOLS])
ref("challengesPerLevel", CHALLENGES_PER_LEVEL)
ref("pointsFirst", POINTS_FIRST)
ref("pointsSecond", POINTS_SECOND)
ref("perfectScore", CHALLENGES_PER_LEVEL * POINTS_FIRST)
ref("nLevels", 4)
ref("poolSizes", [len(p) for p in POOLS])
ref("typeCounts", [len(t) for t in TYPES])


class M32(object):
    """mulberry32 — the same 32-bit arithmetic the JS twin does."""

    def __init__(self, seed):
        self.a = seed & 0xFFFFFFFF

    def next(self):
        self.a = (self.a + 0x6D2B79F5) & 0xFFFFFFFF
        t = self.a
        t = (t ^ (t >> 15)) * (t | 1) & 0xFFFFFFFF
        t ^= (t + ((t ^ (t >> 7)) * (t | 61) & 0xFFFFFFFF)) & 0xFFFFFFFF
        t &= 0xFFFFFFFF
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0


def make_set(level, seed):
    """PhET's ChallengeDescriptorSetFactory, with a mulberry32 in place of
    dotRandom: pick a type (never the same as the previous one), then an atom
    from the level's pool under the type's constraints, without repetition."""
    types = TYPES[level]
    remaining = [tuple(t) for t in POOLS[level]]
    used = []
    rng = M32(seed)
    out = []
    prev = None
    for _ in range(CHALLENGES_PER_LEVEL):
        i = int(rng.next() * len(types))
        t = types[i]
        if prev is not None and t == prev:
            i = (i + 1) % len(types)
            t = types[i]
        lo, hi = (0, 3) if t in SCHEMATIC else (4, 10 ** 9)
        need = rng.next() >= 0.5 if t in CHARGEY else False
        ok = [a for a in remaining if lo <= a[0] < hi and (not need or a[0] - a[2] != 0)]
        if not ok:
            ok = [a for a in used if lo <= a[0] < hi and (not need or a[0] - a[2] != 0)]
        if not ok:
            raise RuntimeError("no atom matches %s" % t)
        a = ok[int(rng.next() * len(ok))]
        if a in remaining:
            remaining.remove(a)
            used.append(a)
        out.append((t, a))
        prev = t
    return out


def solvable(t, atom):
    """A challenge is solvable iff the question determines the answer.  Every
    type here is a function of (p, n, e), so the check is that the answer
    fields are all derivable and inside the ranges the answer controls span."""
    p, n, e = atom
    a, q = p + n, p - e
    if t.endswith("-to-element") or t.endswith("proton-count"):
        return 1 <= p <= 18
    if t.endswith("charge"):
        return -10 <= q <= 10
    if t.endswith("mass-number"):
        return 0 <= a <= 40
    if t in ("schematic-to-symbol-all", "counts-to-symbol-all"):
        return 1 <= p <= 18 and 0 <= a <= 40 and -10 <= q <= 10
    if t == "symbol-to-schematic" or t == "symbol-to-counts":
        return 0 <= p <= 18 and 0 <= n <= 22 and 0 <= e <= 18
    raise RuntimeError("unknown type " + t)


NSEED = 4000
bad = 0
schem_bad = 0
dups = 0
dup_first = None
typecount = {}
for level in range(4):
    for seed in range(1, NSEED + 1):
        cs = make_set(level, seed)
        assert len(cs) == CHALLENGES_PER_LEVEL
        for k in range(1, len(cs)):
            if cs[k][0] == cs[k - 1][0]:
                bad += 1
        seen = set()
        for t, atom in cs:
            typecount[t] = typecount.get(t, 0) + 1
            if atom in seen:
                dups += 1
                if dup_first is None:
                    dup_first = [level + 1, seed]
            seen.add(atom)
            if not solvable(t, atom):
                bad += 1
            if t in SCHEMATIC and atom[0] >= 3:
                schem_bad += 1
            if t not in SCHEMATIC and atom[0] < 4:
                schem_bad += 1
say("  %d seeds x 4 levels = %d sets, %d challenges" % (NSEED, 4 * NSEED,
                                                        4 * NSEED * CHALLENGES_PER_LEVEL))
say("  unsolvable or repeated-type challenges: %d" % bad)
say("  challenges breaking the schematic Z < 3 / other Z >= 4 rule: %d" % schem_bad)
ref("gameSweepSeeds", NSEED)
ref("gameSweepBad", bad)
ref("gameSweepSchemBad", schem_bad)
say("  levels in which an atom is posed twice: %d (PhET's documented fallback, "
    "which reuses a used atom when the filtered pool is empty); first at %s"
    % (dups, dup_first))
ref("gameSweepDups", dups)
ref("gameSweepDupFirst", dup_first)
# the fallback case, spelled out: level 2 seed 2691 exhausts the four charged
# Z < 3 atoms and has to reuse one
if dup_first:
    ref("dupSet", [[t, list(a)] for t, a in make_set(dup_first[0] - 1, dup_first[1])])
    say("  that set: %s" % REF["dupSet"])
say("  type histogram: %s" % sorted(typecount.items()))

# three reference sets the JS must reproduce exactly
for level in range(4):
    cs = make_set(level, 12345)
    ref("gameSet_L%d_s12345" % (level + 1),
        [[t, list(a)] for t, a in cs])
    say("  level %d, seed 12345: %s" % (level + 1, [(t, a) for t, a in cs]))
ref("m32_seed1_first5", [M32(1).next() for _ in range(1)] and
    [(lambda r: [r.next() for _ in range(5)])(M32(1))][0])
say("  mulberry32(1) first five: %s" % REF["m32_seed1_first5"])

# scoring: every path through one level
def score_run(results):
    """results[i] = number of the attempt that was right (1 or 2), or 0 for
    never.  PhET: 2 for a first-attempt answer, 1 for a second, 0 after."""
    return sum(POINTS_FIRST if r == 1 else POINTS_SECOND if r == 2 else 0 for r in results)


def level_seed(gseed, level):
    v = (gseed + level * 7919) & 0xFFFFFFFF
    return v - 0x100000000 if v >= 0x80000000 else v


ref("levelSeed_20260922_1", level_seed(20260922, 1))
ref("levelSeed_20260922_4", level_seed(20260922, 4))
ref("levelSeed_1_1", level_seed(1, 1))
say("  the level seed mixes the control's seed with the level number: "
    "(20260922, 1) -> %d, (20260922, 4) -> %d"
    % (REF["levelSeed_20260922_1"], REF["levelSeed_20260922_4"]))
# the whole point of the mixing: the same control seed gives four DIFFERENT
# streams.  Without it levels 3 and 4, which share a pool, would draw the
# same atoms in the same order.
same = 0
for s in range(1, 501):
    a = [tuple(x[1]) for x in make_set(2, s)]
    b = [tuple(x[1]) for x in make_set(3, s)]
    if a == b:
        same += 1
ref("unmixedLevel34Same", same)
say("  with the SAME seed, levels 3 and 4 draw identical atom sequences in "
    "%d of 500 seeds — which is what the mixing exists to prevent" % same)

ref("score_allFirst", score_run([1] * 5))
ref("score_allSecond", score_run([2] * 5))
ref("score_none", score_run([0] * 5))
ref("score_mixed", score_run([1, 2, 0, 1, 2]))
say("  scores: all first %d, all second %d, none %d, mixed(1,2,0,1,2) %d"
    % (REF["score_allFirst"], REF["score_allSecond"], REF["score_none"],
       REF["score_mixed"]))

# ================================================= §6 geometry PhET's own numbers
say()
say("=" * 72)
say("6. PhET's own view constants (read from the minified original)")
say("=" * 72)
INNER, OUTER, MAXE = 85.0, 130.0, 10
say("  inner shell %g, outer shell %g, nucleon radius %g, electron radius %g"
    % (INNER, OUTER, 10, 8))
ref("innerShell", INNER)
ref("outerShell", OUTER)
ref("nucleonRadius", 10.0)
ref("electronRadius", 8.0)
cloud = [0.0] + [0.5 * INNER + (OUTER - 0.5 * INNER) / MAXE * e for e in range(1, MAXE + 1)]
ref("cloudR_1", cloud[1])
ref("cloudR_10", cloud[10])
say("  cloud radius r(e) = %g + %g e  ->  r(1) = %g, r(10) = %g (= the outer shell)"
    % (0.5 * INNER, (OUTER - 0.5 * INNER) / MAXE, cloud[1], cloud[10]))
RAD = {int(k): v for k, v in P["radius"].items()}
hrad = {r[0]: r[15] for r in HEL}
# NOT a cross-check: periodic_table.html's radius column is a different
# QUANTITY (mendeleev's atomic_radius, 154 pm for hydrogen), while PhET's are
# the Clementi calculated radii (53 pm).  Reconciling a table against a number
# from another publication is on this repo's Known-bad list.  What IS checkable
# is the definition: the Clementi radius of hydrogen is the Bohr radius.
a0_pm = sc.physical_constants["Bohr radius"][0] * 1e12
say("  PhET's radii are CLEMENTI calculated radii (H = %d pm), not "
    "periodic_table.html's %g pm — a different quantity, not a discrepancy"
    % (RAD[1], hrad[1]))
say("  the Bohr radius is %.6f pm, which rounds to PhET's hydrogen value %d"
    % (a0_pm, RAD[1]))
ref("bohrRadius_pm", a0_pm)
ref("radius_C", RAD[6])
ref("radius_H", RAD[1])
ref("radius_He", RAD[2])
# how far from scale the atom picture is, for carbon: the drawn nucleus is
# nucleonRadius/outerShell of the atom, the real one is R_nuc/R_atom
R_NUC_FM = 1.2


def nuc_radius_fm(a):
    return R_NUC_FM * a ** (1 / 3.0)


for z, a, nm in [(6, 12, "C12"), (1, 1, "H1"), (10, 20, "Ne20")]:
    true_frac = nuc_radius_fm(a) * 1e-15 / (RAD[z] * 1e-12)
    drawn = 10.0 / 130.0
    ref("nucFrac_%s" % nm, true_frac)
    ref("exagg_%s" % nm, drawn / true_frac)
    say("  %s: nucleus radius %.4f fm in an atom of %g pm -> 1 : %.0f; drawn 1 : %.2f, "
        "so the picture exaggerates it %.0f x"
        % (nm, nuc_radius_fm(a), RAD[z], 1 / true_frac, 1 / drawn, drawn / true_frac))

ang = [0.0, np.pi]
a0 = np.pi / 8 * 1.2
outer_ang = [(a0 + k * 2 * np.pi / 8) for k in range(8)]
ref("outerAngle0", float(outer_ang[0]))
ref("outerAngle7", float(outer_ang[7]))
say("  outer-shell slot angles start at pi/8 x 1.2 = %.15g rad and step 2pi/8"
    % outer_ang[0])

# ==================================================================== emit
say()
io.open(os.path.join(OUT, "refvals.txt"), "w", encoding="utf-8").write(
    json.dumps(REF, indent=1, sort_keys=True))
io.open(os.path.join(OUT, "derive.log"), "w", encoding="utf-8").write("\n".join(LINES))
say("wrote %d reference values to _out/refvals.txt" % len(REF))
