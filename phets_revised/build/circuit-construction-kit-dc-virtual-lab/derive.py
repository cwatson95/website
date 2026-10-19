#!/usr/bin/env python3
"""derive.py -- the Python twin of circuit-construction-kit-dc-virtual-lab.html.

Re-derives every number the sim's selfTest pins, by routes independent of the
JavaScript:

  * the JS solves Kirchhoff's laws by Modified Nodal Analysis with EVERY
    branch current kept as an unknown (group-2 MNA), in floating point, by
    Gaussian elimination with partial pivoting and iterative refinement;
  * this file solves the same circuits by classic NODAL analysis
    (conductance stamps, each battery as its Norton equivalent, no current
    unknowns at all) in EXACT rational arithmetic (fractions.Fraction), so
    the reference values carry no rounding error whatever;
  * numpy.linalg.solve on the same nodal system, in floating point, is the
    "(python)" float cross-check, and its departure from the exact answer is
    printed (it is the cancellation a conductance formulation suffers);
  * closed forms where they exist (series, parallel, the Wheatstone bridge,
    Thevenin, maximum power) are checked against the exact solve here.

The real bulb is non-linear (PhET: R = 10 + 3|V| log_(|V|+2) 2... written
out below) and is iterated in 50-digit Decimal arithmetic.

PhET's values are read from the minified 1.5.2 build in
docs/phets/circuit-construction-kit-dc-virtual-lab_en.html (CCKCConstants,
ResistorType, Battery, Fuse, LightBulb, Wire, LinearTransientAnalysis,
ChargeAnimator).  They are marked "PhET" below.

Writes, next to this file:
  refvals.txt   -- everything printed (READ IT IN FULL, never through tail)
  p2_presets.js -- the preset circuits' geometry, emitted (both sides build
                   the same circuits from the same numbers)
  p7_refs.js    -- const REF = {...}: the numbers selfTest asserts
"""
import io
import json
import math
import os
import sys
from decimal import Decimal, getcontext
from fractions import Fraction as Fr

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def P(*a):
    s = ' '.join(str(x) for x in a)
    OUT.append(s)
    print(s)


def f17(x):
    return float(x).__repr__()


# ---------------------------------------------------------------------------
# PhET's values (CCK common, 1.5.2 DC Virtual Lab build)
# ---------------------------------------------------------------------------
RHO_MIN = Fr('1e-10')          # Ohm m   CCKCConstants.WIRE_RESISTIVITY_RANGE.min
RHO_MAX = Fr('0.0168')         # Ohm m   ... .max
LEN_PER_UNIT = Fr('5e-4')      # m of wire per view unit   Wire.update: 5e-4 * distance
AREA = Fr('5e-4')              # m^2    CCKCConstants.WIRE_CROSS_SECTIONAL_AREA
MIN_WIRE_R = Fr('1e-14')       # Ohm    CCKCConstants.MINIMUM_WIRE_RESISTANCE
MIN_R = Fr('1.1e-10')          # Ohm    CCKCConstants.MINIMUM_RESISTANCE (replaces an exact 0)
BATT_R_MIN = Fr('1e-4')        # Ohm    batteryMinimumResistance, the default internal resistance
BATT_R_MAX = Fr(10)            # Ohm
FUSE_K = Fr('0.06')            # Ohm A  Fuse: R = 0.06 / rating
FUSE_DEFAULT = Fr(4)           # A
FUSE_RANGE = (Fr('0.5'), Fr(20))
FIRE_I = Fr(15)                # A      |I| >= 15 and R >= 1e-8 -> fire
FIRE_R = Fr('1e-8')
B_MULT = Fr('0.35')            # LightBulb.BRIGHTNESS_MULTIPLIER
B_PMAX = Fr(2000)              # LightBulb.BRIGHTNESS_MAXIMUM_POWER
REAL_COLD = Fr(10)             # LightBulb.REAL_BULB_COLD_RESISTANCE
CHARGE_SEP = 28                # CCKCConstants.CHARGE_SEPARATION
CHARGE_SPEED = 25              # view units per second per ampere (ChargeAnimator)
CHARGE_CAP = Fr(43, 100) * CHARGE_SEP   # 0.43 * 28 per 1/30 s frame
SNAP = 30                      # view units, Circuit.getDropTarget
SOLDER_R = Fr('11.2')          # SolderNode.SOLDER_RADIUS (voltmeter probe to a vertex)
TAP = 15                       # CCKCConstants.TAP_THRESHOLD (px)

# element types: fixed length (PhET's, view units; the bulbs' 100 is the
# remake's), default value, editable range.  Resistances in Ohm, EMF in V.
TYPES = {
    'wire':      dict(L=None),
    'battery':   dict(L=102, E=9, lo=0, hi=120),
    'xbattery':  dict(L=102, E=1000, lo=100, hi=100000),
    'resistor':  dict(L=110, R=10, lo=0, hi=120),
    'xresistor': dict(L=110, R=1000, lo=100, hi=10000),
    'bulb':      dict(L=100, R=10, lo=0, hi=120),
    'xbulb':     dict(L=100, R=1000, lo=100, hi=10000),
    'rbulb':     dict(L=100, R=10),
    'switch':    dict(L=112),
    'fuse':      dict(L=110),
    'ammeter':   dict(L=121, R=0),
    'coin':      dict(L=85, R=0),
    'clip':      dict(L=75, R=0),
    'pencil':    dict(L=130, R=25),
    'tpencil':   dict(L=130, R=50),
    'eraser':    dict(L=90, R=1000000),
    'bill':      dict(L=140, R=1000000),
}

# ---------------------------------------------------------------------------
# the preset circuits: vertices (x, y) in view units, y DOWN, and elements
# [type, a, b, {value}] in creation order.  Every wire is axis-aligned so its
# length (and so its resistance) is an exact rational.
# ---------------------------------------------------------------------------
PRESETS = {
    'bulb': dict(name='one bulb', verts=[
        [-51, 100], [51, 100], [150, 100], [150, -60], [50, -60], [-50, -60], [-150, -60], [-150, 100]],
        els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['wire', 3, 4, {}],
             ['bulb', 4, 5, {}], ['wire', 5, 6, {}], ['wire', 6, 7, {}], ['wire', 7, 0, {}]]),
    'series': dict(name='series', verts=[
        [-51, 100], [51, 100], [190, 100], [190, -60], [80, -60], [50, -60], [-50, -60], [-190, -60], [-190, 100]],
        els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['resistor', 3, 4, {}],
             ['wire', 4, 5, {}], ['bulb', 5, 6, {}], ['wire', 6, 7, {}], ['wire', 7, 8, {}], ['wire', 8, 0, {}]]),
    'parallel': dict(name='parallel', verts=[
        [-51, 140], [51, 140], [180, 140], [180, 40], [180, -80], [55, 40], [-55, 40], [50, -80], [-50, -80],
        [-180, -80], [-180, 40], [-180, 140]],
        els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['wire', 3, 4, {}], ['wire', 3, 5, {}],
             ['resistor', 5, 6, {}], ['wire', 6, 10, {}], ['wire', 4, 7, {}], ['bulb', 7, 8, {}], ['wire', 8, 9, {}],
             ['wire', 9, 10, {}], ['wire', 10, 11, {}], ['wire', 11, 0, {}]]),
    'bridge': dict(name='Wheatstone bridge', verts=[
        [-220, 20], [-220, -82], [-220, -140], [-120, -140], [-120, -30], [-120, 80], [-220, 80],
        [120, -140], [120, -30], [120, 80], [-60.5, -30], [60.5, -30]],
        els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['resistor', 3, 4, {'R': 10}],
             ['resistor', 4, 5, {'R': 20}], ['wire', 5, 6, {}], ['wire', 6, 0, {}], ['wire', 3, 7, {}],
             ['resistor', 7, 8, {'R': 30}], ['resistor', 8, 9, {'R': 40}], ['wire', 9, 5, {}],
             ['wire', 4, 10, {}], ['ammeter', 10, 11, {}], ['wire', 11, 8, {}]]),
    'twobat': dict(name='two batteries', verts=[
        [-200, 100], [-200, -2], [-200, -120], [-165, -120], [-55, -120], [0, -120], [55, -120], [165, -120],
        [200, -120], [200, -2], [200, 100], [200, 140], [0, 140], [-200, 140], [0, -65], [0, 45]],
        els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['resistor', 3, 4, {'R': 10}],
             ['wire', 4, 5, {}], ['wire', 5, 6, {}], ['resistor', 6, 7, {'R': 20}], ['wire', 7, 8, {}],
             ['wire', 8, 9, {}], ['battery', 10, 9, {'E': 6}], ['wire', 10, 11, {}], ['wire', 11, 12, {}],
             ['wire', 12, 13, {}], ['wire', 13, 0, {}], ['wire', 5, 14, {}], ['resistor', 14, 15, {'R': 30}],
             ['wire', 15, 12, {}]]),
    'short': dict(name='short circuit', verts=[[-51, 60], [51, 60], [51, -40], [-51, -40]],
                  els=[['battery', 0, 1, {}], ['wire', 1, 2, {}], ['wire', 2, 3, {}], ['wire', 3, 0, {}]]),
}
PRESET_ORDER = ['empty', 'bulb', 'series', 'parallel', 'bridge', 'twobat', 'short']


def dist(p, q):
    """exact for axis-aligned segments (all presets are)."""
    dx, dy = Fr(str(q[0])) - Fr(str(p[0])), Fr(str(q[1])) - Fr(str(p[1]))
    if dx == 0:
        return abs(dy)
    if dy == 0:
        return abs(dx)
    return Fr(math.hypot(float(dx), float(dy)))


def wire_R(d, rho):
    """PhET's Wire.update: length = 5e-4 * d metres, R = rho * length / A,
    never below 1e-14 Ohm."""
    return max(MIN_WIRE_R, rho * (LEN_PER_UNIT * d) / AREA)


# ---------------------------------------------------------------------------
# netlists: nodes 0..N-1, branches (a, b, R, E, kind, label).  The branch
# law is  v_a - v_b = R i - E,  i flowing a -> b through the element, so a
# battery's EMF raises the potential from a (its - terminal) to b (+).
# ---------------------------------------------------------------------------
def netlist_from_preset(key, rho=RHO_MIN, rbat=BATT_R_MIN, over=None):
    pr = PRESETS[key]
    over = over or {}
    br = []
    for k, (typ, a, b, par) in enumerate(pr['els']):
        par = dict(par)
        par.update(over.get(k, {}))
        T = TYPES[typ]
        L = T['L']
        if L is not None:
            d = dist(pr['verts'][a], pr['verts'][b])
            assert d == L, (key, k, typ, d, L)
        if typ == 'wire':
            R, E = wire_R(dist(pr['verts'][a], pr['verts'][b]), rho), Fr(0)
        elif typ in ('battery', 'xbattery'):
            R, E = rbat, Fr(str(par.get('E', T['E'])))
        elif typ == 'fuse':
            R, E = FUSE_K / Fr(str(par.get('rating', FUSE_DEFAULT))), Fr(0)
        elif typ == 'switch':
            if not par.get('closed', False):
                continue
            R, E = Fr(0), Fr(0)
        else:
            R, E = Fr(str(par.get('R', T['R']))), Fr(0)
        if R == 0:
            R = MIN_R          # PhET: resistance || MINIMUM_RESISTANCE
        br.append((a, b, R, E, 'B' if typ in ('battery', 'xbattery') else 'R', k))
    return len(pr['verts']), br


def components(N, br):
    par = list(range(N))

    def f(x):
        while par[x] != x:
            par[x] = par[par[x]]
            x = par[x]
        return x
    for a, b, *_ in br:
        ra, rb = f(a), f(b)
        if ra != rb:
            par[max(ra, rb)] = min(ra, rb)
    comp = [f(n) for n in range(N)]
    return comp


def references(N, br, comp):
    """the reference (0 V) node of each component: the - terminal (a) of the
    first battery in branch order in that component, else its lowest node."""
    ref = {}
    for a, b, R, E, kind, lab in br:
        if kind == 'B' and comp[a] not in ref:
            ref[comp[a]] = a
    for n in range(N):
        if comp[n] not in ref:
            ref[comp[n]] = n
    return ref


def solve_exact(N, br, inj=None, zeroE=False, only=None):
    """classic nodal analysis in exact rationals.  inj[n] = current injected
    INTO node n from outside.  zeroE zeroes every EMF (Thevenin resistance);
    only = index of the one battery kept (superposition)."""
    comp = components(N, br)
    ref = references(N, br, comp)
    refs = set(ref.values())
    idx = {}
    for n in range(N):
        if n not in refs:
            idx[n] = len(idx)
    m = len(idx)
    Y = [[Fr(0)] * m for _ in range(m)]
    rhs = [Fr(0)] * m
    if inj:
        for n, J in inj.items():
            if n in idx:
                rhs[idx[n]] += J
    for k, (a, b, R, E, kind, lab) in enumerate(br):
        G = 1 / R
        if zeroE or (only is not None and kind == 'B' and k != only):
            E = Fr(0)
        # i = G (v_a - v_b) + G E leaves a, enters b
        for n, s in ((a, 1), (b, -1)):
            if n not in idx:
                continue
            r = idx[n]
            if a in idx:
                Y[r][idx[a]] += s * G
            if b in idx:
                Y[r][idx[b]] -= s * G
            rhs[r] -= s * G * E
    # Gaussian elimination, exact
    A = [row[:] + [rhs[r]] for r, row in enumerate(Y)]
    for c in range(m):
        p = next(r for r in range(c, m) if A[r][c] != 0)
        A[c], A[p] = A[p], A[c]
        for r in range(m):
            if r != c and A[r][c] != 0:
                f = A[r][c] / A[c][c]
                A[r] = [x - f * y for x, y in zip(A[r], A[c])]
    v = [Fr(0)] * N
    for n, r in idx.items():
        v[n] = A[r][m] / A[r][r]
    cur = []
    for k, (a, b, R, E, kind, lab) in enumerate(br):
        if zeroE or (only is not None and kind == 'B' and k != only):
            E = Fr(0)
        cur.append((v[a] - v[b] + E) / R)
    return v, cur, comp, ref


def solve_numpy(N, br):
    """the same nodal system in floating point: numpy.linalg.solve."""
    comp = components(N, br)
    ref = references(N, br, comp)
    refs = set(ref.values())
    idx = {}
    for n in range(N):
        if n not in refs:
            idx[n] = len(idx)
    m = len(idx)
    Y = np.zeros((m, m))
    rhs = np.zeros(m)
    for a, b, R, E, kind, lab in br:
        G = 1.0 / float(R)
        for n, s in ((a, 1), (b, -1)):
            if n not in idx:
                continue
            r = idx[n]
            if a in idx:
                Y[r, idx[a]] += s * G
            if b in idx:
                Y[r, idx[b]] -= s * G
            rhs[r] -= s * G * float(E)
    x = np.linalg.solve(Y, rhs) if m else np.zeros(0)
    v = np.zeros(N)
    for n, r in idx.items():
        v[n] = x[r]
    cur = [(v[a] - v[b] + float(E)) / float(R) for a, b, R, E, kind, lab in br]
    return v, cur


def kcl_kvl(N, br, v, cur):
    """exact residuals: KCL at every node, KVL (element laws) round every
    fundamental loop of a spanning forest."""
    s = [Fr(0)] * N
    for k, (a, b, *_r) in enumerate(br):
        s[a] += cur[k]
        s[b] -= cur[k]
    kcl = max((abs(x) for x in s), default=Fr(0))
    # spanning forest by BFS; each chord closes one loop
    adj = {n: [] for n in range(N)}
    for k, (a, b, *_r) in enumerate(br):
        adj[a].append((b, k, 1))
        adj[b].append((a, k, -1))
    parent = {}
    tree = set()
    for root in range(N):
        if root in parent:
            continue
        parent[root] = None
        q = [root]
        while q:
            n = q.pop(0)
            for m2, k, sgn in adj[n]:
                if m2 not in parent:
                    parent[m2] = (n, k, sgn)
                    tree.add(k)
                    q.append(m2)
    kvl = Fr(0)
    nloops = 0
    for k, (a, b, R, E, kind, lab) in enumerate(br):
        if k in tree:
            continue
        nloops += 1
        # loop: a -> b through chord k, then b -> ... -> a through the tree
        drop = R * cur[k] - E        # v_a - v_b along the chord
        # path from b up to root and from a up to root; sum tree drops b -> a
        def up(n):
            path = []
            while parent[n] is not None:
                p, kk, sgn = parent[n]
                path.append((n, p, kk))
                n = p
            return path
        pb, pa = up(b), up(a)
        tot = drop
        # going from b to root: step n -> p along branch kk: add (v_n - v_p)
        for n, p, kk in pb:
            aa, bb, RR, EE, *_q = br[kk]
            d = RR * cur[kk] - EE           # v_aa - v_bb
            tot += d if n == aa else -d
        for n, p, kk in pa:                # then root back down to a: minus
            aa, bb, RR, EE, *_q = br[kk]
            d = RR * cur[kk] - EE
            tot -= d if n == aa else -d
        kvl = max(kvl, abs(tot))
    return kcl, kvl, nloops


def brightness(P):
    """PhET LightBulb.computeBrightness: clamp(ln(1+0.35P)/ln(1+0.35*2000), 0, 1)."""
    P = float(P)
    return min(1.0, max(0.0, math.log(1 + P * float(B_MULT)) / math.log(1 + float(B_PMAX) * float(B_MULT))))


def fire(kind, R, I):
    return abs(I) >= FIRE_I and R >= FIRE_R


# ---------------------------------------------------------------------------
P('=' * 78)
P('derive.py -- circuit-construction-kit-dc-virtual-lab: reference values')
P('=' * 78)
P('numpy', np.__version__, '  python', sys.version.split()[0])

REF = {'consts': {}, 'presets': {}, 'nets': {}, 'real': {}, 'misc': {}}
C = REF['consts']
P('\n--- PhET constants and the small laws ---')
for nm, val in [('RHO_MIN', RHO_MIN), ('RHO_MAX', RHO_MAX), ('MIN_WIRE_R', MIN_WIRE_R), ('MIN_R', MIN_R),
                ('BATT_R_MIN', BATT_R_MIN)]:
    C[nm] = float(val)
    P('%-12s %s' % (nm, f17(val)))
# wire resistance at three lengths and both resistivities
C['wireR'] = {}
for d in [0, 1, 100, 250]:
    for rho, rn in [(RHO_MIN, 'min'), (RHO_MAX, 'max')]:
        R = wire_R(Fr(d), rho)
        C['wireR']['%d_%s' % (d, rn)] = float(R)
        P('wire %4d units, rho %-3s : R = %s Ohm' % (d, rn, f17(R)))
P('  (100 units of wire = %s m; at rho_max that is 1.68 Ohm: R = rho L / A = 0.0168 x 0.05 / 5e-4)' % f17(LEN_PER_UNIT * 100))
C['fuseR'] = {}
for rating in ['0.5', '4', '20']:
    R = FUSE_K / Fr(rating)
    C['fuseR'][rating] = float(R)
    P('fuse rated %4s A : R = %s Ohm' % (rating, f17(R)))
C['bright'] = {}
for Pw in ['0', '0.5', '1', '8.1', '100', '2000', '5000']:
    b = brightness(Fr(Pw))
    C['bright'][Pw] = b
    P('brightness at P = %6s W : %s' % (Pw, f17(b)))
den = math.log(1 + 700)
P('  ln(1 + 0.35 x 2000) = ln 701 =', f17(den))
C['brightDen'] = den


def real_R(V):
    """PhET's real bulb: R = 10 + 3|V| / log_2(|V| + 2)  (LinearTransientAnalysis)."""
    V = abs(Decimal(V))
    two = Decimal(2)
    return Decimal(10) + 3 * V / ((V + two).ln() / two.ln())


getcontext().prec = 50
C['realR'] = {}
for V in ['0', '1', '9', '100']:
    R = real_R(Decimal(V))
    C['realR'][V] = float(R)
    P('real bulb at |V| = %4s V : R = %s Ohm' % (V, f17(R)))

# charges
C['charges'] = {}
for L in [20, 28, 40, 100, 102, 110, 250]:
    # PhET Circuit.layoutCharges: o = ceil((L - 28)/28) charges from 14 to L - 14
    s = L - CHARGE_SEP
    o = math.ceil(s / CHARGE_SEP)
    if o <= 1:
        pos = [L / 2]
    else:
        a = s / (o - 1)
        pos = [14 + l * a for l in range(o)]
    C['charges'][str(L)] = pos
    P('charge layout on %3d units: %d at %s' % (L, len(pos), [round(x, 6) for x in pos]))
Icap = float(CHARGE_CAP) * 30 / CHARGE_SPEED
C['Icap'] = Icap
P('charges slow down above I_max = 0.43 x 28 x 30 / 25 = %s A (time scale = I_cap / I_max)' % f17(Icap))

# ---------------------------------------------------------------------------
P('\n--- the preset circuits (exact nodal analysis; numpy nodal as the float check) ---')


def report(tag, N, br, v, cur, comp, ref, extra=None):
    kcl, kvl, nl = kcl_kvl(N, br, v, cur)
    ncomp = len(set(comp))
    P('%s: %d nodes, %d branches, %d components -> %d independent loops; exact KCL %s, KVL %s'
      % (tag, N, len(br), ncomp, len(br) - N + ncomp, kcl, kvl))
    assert kcl == 0 and kvl == 0
    assert nl == len(br) - N + ncomp
    return nl


def preset_ref(key, rho=RHO_MIN, rbat=BATT_R_MIN, over=None, tag=None):
    N, br = netlist_from_preset(key, rho, rbat, over)
    v, cur, comp, ref = solve_exact(N, br)
    tag = tag or key
    nl = report(tag, N, br, v, cur, comp, ref)
    vn, cn = solve_numpy(N, br)
    errv = max((abs(float(v[n]) - vn[n]) / max(1e-300, max(abs(float(x)) for x in v)) for n in range(N)), default=0)
    erri = max((abs(float(cur[k]) - cn[k]) / max(1e-300, max(abs(float(x)) for x in cur)) for k in range(len(br))), default=0)
    P('   numpy nodal vs exact: node voltages %.2e, branch currents %.2e (relative to the largest)' % (errv, erri))
    out = {'v': [float(x) for x in v], 'i': {}, 'P': {}, 'loops': nl, 'comps': len(set(comp)),
           'nodes': N, 'branches': len(br), 'ref': sorted(set(ref.values())), 'numpyErrV': errv, 'numpyErrI': erri}
    pr = PRESETS[key]
    for k, (a, b, R, E, kind, lab) in enumerate(br):
        typ = pr['els'][lab][0]
        out['i'][str(lab)] = float(cur[k])
        if kind == 'B':
            out['P'][str(lab)] = [float(E * cur[k]), float(cur[k] ** 2 * R)]
        else:
            out['P'][str(lab)] = float(cur[k] ** 2 * R)
        line = '   el %2d %-9s %3d->%-3d R=%-22s i=%-24s' % (lab, typ, a, b, f17(R), f17(cur[k]))
        if typ in ('bulb', 'xbulb', 'rbulb'):
            bb = brightness(cur[k] ** 2 * R)
            out.setdefault('bright', {})[str(lab)] = bb
            line += ' P=%s b=%s' % (f17(cur[k] ** 2 * R), f17(bb))
        if kind == 'B' or typ in ('resistor', 'xresistor', 'pencil', 'tpencil', 'eraser', 'bill', 'coin', 'clip'):
            if fire(kind, R, float(cur[k])):
                out.setdefault('fire', []).append(lab)
                line += ' FIRE'
        P(line)
    P('   node voltages: ' + ', '.join('%d:%s' % (n, f17(v[n])) for n in range(N)))
    # Tellegen, exactly
    tel = sum((v[a] - v[b]) * cur[k] for k, (a, b, *_r) in enumerate(br))
    assert tel == 0
    gen = sum(E * cur[k] for k, (a, b, R, E, kind, lab) in enumerate(br))
    dis = sum(R * cur[k] ** 2 for k, (a, b, R, E, kind, lab) in enumerate(br))
    assert gen == dis
    out['Pgen'] = float(gen)
    P('   Tellegen: sum (v_a - v_b) i = %s exactly; EMFs deliver %s W = sum i^2 R' % (tel, f17(gen)))
    return out, N, br, v, cur


def thevenin(N, br, k):
    """the rest of the circuit seen from branch k: open-circuit voltage
    V_oc = v_a - v_b with k removed, and R_th = (v_a - v_b) per ampere
    injected at a and drawn out at b with every EMF zeroed."""
    a, b = br[k][0], br[k][1]
    rest = br[:k] + br[k + 1:]
    comp = components(N, rest)
    if comp[a] != comp[b]:
        return None
    v, cur, _c, _r = solve_exact(N, rest)
    Voc = v[a] - v[b]
    v2, cur2, _c, _r = solve_exact(N, rest, inj={a: Fr(1), b: Fr(-1)}, zeroE=True)
    Rth = v2[a] - v2[b]
    return Voc, Rth


PR = REF['presets']
for key in PRESET_ORDER[1:]:
    out, N, br, v, cur = preset_ref(key)
    PR[key] = out

# Thevenin of chosen elements in the presets, and the check I = (Voc + E)/(R + Rth)
P('\n--- Thevenin: the rest of the circuit seen from one element ---')
REF['thev'] = {}
for key, lab in [('bulb', 4), ('twobat', 15), ('bridge', 12), ('twobat', 0), ('series', 3)]:
    N, br = netlist_from_preset(key)
    k = next(i for i, x in enumerate(br) if x[5] == lab)
    Voc, Rth = thevenin(N, br, k)
    v, cur, comp, ref = solve_exact(N, br)
    a, b, R, E, kind, _l = br[k]
    Ipred = (Voc + E) / (R + Rth)
    assert Ipred == cur[k], (key, lab)
    REF['thev']['%s_%d' % (key, lab)] = {'Voc': float(Voc), 'Rth': float(Rth), 'i': float(cur[k])}
    P('%-7s el %2d: V_oc = %-24s R_th = %-24s i = (V_oc+E)/(R+R_th) = %s  (== the full solve, exactly)'
      % (key, lab, f17(Voc), f17(Rth), f17(cur[k])))
    if kind == 'R':
        Pmax = Voc ** 2 / (4 * Rth)
        REF['thev']['%s_%d' % (key, lab)]['Pmax'] = float(Pmax)
        P('            maximum power V_oc^2/4R_th = %s W at R = R_th' % f17(Pmax))

# superposition in the two-battery preset
P('\n--- superposition: two batteries, each alone (the other EMF zeroed, its r kept) ---')
N, br = netlist_from_preset('twobat')
bats = [k for k, x in enumerate(br) if x[4] == 'B']
v, cur, comp, ref = solve_exact(N, br)
parts = []
for kb in bats:
    vv, cc, _c, _r = solve_exact(N, br, only=kb)
    parts.append(cc)
REF['super'] = {'bats': [br[k][5] for k in bats], 'parts': [[float(x) for x in cc] for cc in parts],
                'labels': [x[5] for x in br]}
for k in range(len(br)):
    s = sum(p[k] for p in parts)
    assert s == cur[k]
for k in [0, 3, 6, 9, 15]:
    kk = next(i for i, x in enumerate(br) if x[5] == k)
    P('   el %2d: %s + %s = %s' % (k, f17(parts[0][kk]), f17(parts[1][kk]), f17(cur[kk])))
P('   every branch: the two contributions sum to the full solution EXACTLY')

# variants of the presets
P('\n--- variants ---')
VAR = REF['variants'] = {}
for tag, key, kw in [('bulb_r2', 'bulb', dict(rbat=Fr(2))), ('bulb_r10', 'bulb', dict(rbat=Fr(10))),
                     ('bulb_rhomax', 'bulb', dict(rho=RHO_MAX)),
                     ('bridge_bal', 'bridge', dict(over={9: {'R': 60}})),
                     ('parallel_r5', 'parallel', dict(rbat=Fr(5)))]:
    out, N, br, v, cur = preset_ref(key, tag=tag, **kw)
    VAR[tag] = out
bb = VAR['bridge_bal']['i']['12']
P('   balanced bridge (R4 = 60 so R1/R2 = R3/R4): the ammeter carries %s A -- not exactly 0, because the'
  ' 2.4e-8-Ohm rails join the dividers\' ends' % f17(bb))

# the bulb preset: closed form I = E / (r + R + sum of wire R)
N, br = netlist_from_preset('bulb')
wires = sum(x[2] for x in br if PRESETS['bulb']['els'][x[5]][0] == 'wire')
I = Fr(9) / (BATT_R_MIN + 10 + wires)
assert I == Fr(str(PR['bulb']['i']['4'])) or abs(float(I) - PR['bulb']['i']['4']) < 1e-16
REF['misc']['bulbWireR'] = float(wires)
REF['misc']['bulbI'] = float(I)
P('\nbulb preset closed form: wires %s Ohm in all, I = 9/(1e-4 + 10 + wires) = %s A' % (f17(wires), f17(I)))

# ---------------------------------------------------------------------------
P('\n--- abstract netlists for the solver pins (nodes, branches [a, b, R, E]) ---')
# kind 'B' = battery (E with internal R), 'R' = resistive
NETS = {}


def net(name, N, brs, note):
    NETS[name] = (N, [(a, b, Fr(str(R)), Fr(str(E)), kind, i) for i, (a, b, R, E, kind) in enumerate(brs)], note)


net('series3', 4, [(0, 1, '0.5', 12, 'B'), (1, 2, 10, 0, 'R'), (2, 3, 20, 0, 'R'), (3, 0, 30, 0, 'R')],
    'I = 12 / (0.5 + 10 + 20 + 30)')
net('parallel3', 4, [(0, 1, '1e-4', 9, 'B'), (1, 2, '1e-8', 0, 'R'), (2, 3, 10, 0, 'R'), (2, 3, 20, 0, 'R'),
                     (2, 3, 40, 0, 'R'), (3, 0, '1e-8', 0, 'R')], 'R1 || R2 || R3 = 40/7')
net('bridge_bal', 4, [(3, 0, '1e-4', 10, 'B'), (0, 1, 100, 0, 'R'), (1, 3, 200, 0, 'R'), (0, 2, 150, 0, 'R'),
                      (2, 3, 300, 0, 'R'), (1, 2, 50, 0, 'R')], 'R1/R2 = R3/R4: no current in R5')
net('bridge_unbal', 4, [(3, 0, '1e-4', 10, 'B'), (0, 1, 100, 0, 'R'), (1, 3, 200, 0, 'R'), (0, 2, 150, 0, 'R'),
                        (2, 3, 250, 0, 'R'), (1, 2, 50, 0, 'R')], 'R4 = 250: current in R5')
net('twobat', 4, [(0, 1, '0.5', 9, 'B'), (1, 2, 10, 0, 'R'), (2, 0, 30, 0, 'R'), (2, 3, 20, 0, 'R'),
                  (0, 3, '0.25', 6, 'B')], 'two sources, three resistors')
net('internal', 2, [(0, 1, 2, 9, 'B'), (1, 0, 7, 0, 'R')], 'terminal voltage E - I r')
net('floating', 9, [(0, 1, '1e-4', 9, 'B'), (1, 2, 10, 0, 'R'), (2, 0, 20, 0, 'R'), (2, 3, 5, 0, 'R'),
                    (4, 5, 10, 0, 'R'), (5, 6, 20, 0, 'R'), (6, 4, 30, 0, 'R'), (7, 8, '1e-4', 6, 'B')],
    'a dangling resistor, a sourceless loop, a lone battery')
net('short', 2, [(0, 1, '1e-4', 9, 'B'), (1, 0, '3.02e-8', 0, 'R')], 'a battery shorted by 302 units of wire')
net('extreme', 3, [(0, 1, '1e-4', 100000, 'B'), (1, 2, 10000, 0, 'R'), (2, 0, '1e-8', 0, 'R')],
    'PhET\'s extreme battery and resistor at their tops')
net('zeroloop', 4, [(0, 1, '1e-4', 9, 'B'), (1, 2, 10, 0, 'R'), (2, 3, '1.1e-10', 0, 'R'), (2, 3, '1.1e-10', 0, 'R'),
                    (3, 0, '1e-8', 0, 'R')], 'a coin and a paper clip side by side (0 Ohm -> 1.1e-10 each)')
net('ladder', 8, [(0, 1, '1e-4', 9, 'B'), (1, 2, '1e-8', 0, 'R'), (2, 3, 25, 0, 'R'), (3, 0, '1e-6', 0, 'R'),
                  (2, 4, 1000000, 0, 'R'), (4, 3, '1.1e-10', 0, 'R'), (4, 5, 120, 0, 'R'), (5, 6, '0.015', 0, 'R'),
                  (6, 7, '2.4e-8', 0, 'R'), (7, 3, 10000, 0, 'R'), (5, 0, 50, 0, 'R'), (6, 1, '0.5', 1000, 'B'),
                  (7, 2, 1, 0, 'R')], 'eight decades of resistance, two sources')
NR = REF['nets']
for name, (N, br, note) in NETS.items():
    v, cur, comp, ref = solve_exact(N, br)
    report(name, N, br, v, cur, comp, ref)
    vn, cn = solve_numpy(N, br)
    scale_v = max(1e-300, max(abs(float(x)) for x in v))
    scale_i = max(1e-300, max(abs(float(x)) for x in cur))
    errv = max(abs(float(v[n]) - vn[n]) for n in range(N)) / scale_v
    erri = max(abs(float(cur[k]) - cn[k]) for k in range(len(br))) / scale_i
    NR[name] = {'N': N, 'br': [[a, b, float(R), float(E), kind] for a, b, R, E, kind, i in br],
                'v': [float(x) for x in v], 'i': [float(x) for x in cur], 'note': note,
                'ref': sorted(set(ref.values())), 'numpyErrV': errv, 'numpyErrI': erri}
    P('   %s -- %s' % (name, note))
    P('   v = [' + ', '.join(f17(x) for x in v) + ']')
    P('   i = [' + ', '.join(f17(x) for x in cur) + ']')
    P('   numpy nodal float vs exact: v %.2e, i %.2e (of the largest)' % (errv, erri))

# closed forms against the exact solve
P('\n--- closed forms (asserted here, exactly) ---')
N, br, _n = NETS['series3']
v, cur, *_ = solve_exact(N, br)
assert cur[0] == Fr(12) / (Fr('0.5') + 60)
P('series3: I = 12/60.5 =', f17(cur[0]))
N, br, _n = NETS['parallel3']
v, cur, *_ = solve_exact(N, br)
Rp = 1 / (Fr(1, 10) + Fr(1, 20) + Fr(1, 40))
Itot = Fr(9) / (Fr('1e-4') + Fr('2e-8') + Rp)
assert cur[0] == Itot and cur[2] == Itot * Rp / 10
P('parallel3: R_par = 40/7, I = 9/(1e-4 + 2e-8 + 40/7) =', f17(Itot), '; I_10 =', f17(cur[2]))
N, br, _n = NETS['bridge_bal']
v, cur, *_ = solve_exact(N, br)
assert cur[5] == 0
P('bridge_bal: I5 = 0 exactly (', cur[5], ')')
N, br, _n = NETS['bridge_unbal']
v, cur, *_ = solve_exact(N, br)
# Thevenin form of the galvanometer current, bridge driven by a source with r
# the exact bridge solution by the "delta" route: solve the 3x3 mesh by hand
Voc, Rth = thevenin(N, br, 5)
I5 = Voc / (Rth + 50)
assert I5 == cur[5]
P('bridge_unbal: I5 = V_oc/(R_th + 50) =', f17(I5), ' V_oc', f17(Voc), 'R_th', f17(Rth))
REF['misc']['bridgeUnbal'] = {'Voc': float(Voc), 'Rth': float(Rth), 'I5': float(I5)}
# ideal source: textbook Wheatstone galvanometer current for r = 0
brI = [(3, 0, Fr('1e-30'), Fr(10), 'B', 0)] + br[1:]
vI, cI, *_ = solve_exact(N, brI)
R1, R2, R3, R4, R5, E = 100, 200, 150, 250, 50, 10
Vth = Fr(E) * (Fr(R2, R1 + R2) - Fr(R4, R3 + R4))
Rth_ideal = Fr(R1 * R2, R1 + R2) + Fr(R3 * R4, R3 + R4)
Ig = Vth / (Rth_ideal + R5)
P('bridge (ideal 10 V source): textbook I_g = E(R2/(R1+R2) - R4/(R3+R4))/(R1||R2 + R3||R4 + R5) =', f17(Ig),
  '; exact solve with r = 1e-30:', f17(cI[5]))
assert abs(float(Ig - cI[5])) < 1e-25
REF['misc']['bridgeIdealIg'] = float(Ig)
N, br, _n = NETS['twobat']
v, cur, *_ = solve_exact(N, br)
parts = [solve_exact(N, br, only=kb)[1] for kb in (0, 4)]
for k in range(len(br)):
    assert parts[0][k] + parts[1][k] == cur[k]
REF['misc']['twobatParts'] = [[float(x) for x in p] for p in parts]
P('twobat superposition parts:', [[f17(x) for x in p] for p in parts])
Voc, Rth = thevenin(N, br, 2)
assert cur[2] == Voc / (Rth + 30)
loads = [Fr(1), Fr(10), Fr(30), Fr(100), Rth]
REF['misc']['twobatThev'] = {'Voc': float(Voc), 'Rth': float(Rth),
                             'loads': [float(x) for x in loads], 'I': [], 'P': []}
for RL in loads:
    br2 = [x if i != 2 else (x[0], x[1], RL, x[3], x[4], x[5]) for i, x in enumerate(br)]
    v2, c2, *_ = solve_exact(N, br2)
    assert c2[2] == Voc / (Rth + RL)
    REF['misc']['twobatThev']['I'].append(float(c2[2]))
    REF['misc']['twobatThev']['P'].append(float(c2[2] ** 2 * RL))
    P('   twobat R3 -> %-22s I = %-22s P = %s' % (f17(RL), f17(c2[2]), f17(c2[2] ** 2 * RL)))
P('   P is largest at R3 = R_th =', f17(Rth), ':', f17(Voc ** 2 / (4 * Rth)), 'W')
N, br, _n = NETS['internal']
REF['misc']['internal'] = []
for r in ['1e-4', '1', '5', '10']:
    for RL in ['1', '5', '10', '20']:
        br2 = [(0, 1, Fr(r), Fr(9), 'B', 0), (1, 0, Fr(RL), Fr(0), 'R', 1)]
        v2, c2, *_ = solve_exact(2, br2)
        I = Fr(9) / (Fr(r) + Fr(RL))
        assert c2[0] == I and v2[1] - v2[0] == 9 - I * Fr(r)
        REF['misc']['internal'].append([float(Fr(r)), float(Fr(RL)), float(I), float(9 - I * Fr(r))])
P('internal resistance: I = E/(r + R_L), terminal voltage E - I r -- 16 cases, exact')
N, br, _n = NETS['floating']
v, cur, *_ = solve_exact(N, br)
assert cur[3] == 0 and cur[4] == cur[5] == cur[6] == 0 and cur[7] == 0 and v[3] == v[2] and v[8] - v[7] == 6
P('floating: dangling i = 0, v3 = v2; sourceless loop all 0; lone battery i = 0 with 6 V across it -- exact')

# ---------------------------------------------------------------------------
P('\n--- the real bulb (non-linear): 50-digit Decimal fixed point ---')


def real_solve(key, lab, extra_over=None):
    """iterate R_bulb <- 10 + 3|V|/log2(|V|+2) to 40 digits (the converged
    fixed point) and also stop after PhET's 10 passes."""
    R = Decimal(10)
    hist = []
    for it in range(200):
        over = {lab: {'R': str(R)}}
        if extra_over:
            over.update(extra_over)
        N, br = netlist_from_preset(key, over=over)
        k = next(i for i, x in enumerate(br) if x[5] == lab)
        v, cur, *_ = solve_exact(N, br)
        V = Decimal(cur[k].numerator) / Decimal(cur[k].denominator) * R
        Rn = real_R(V)
        hist.append((R, cur[k]))
        if abs(Rn - R) < Decimal('1e-40'):
            break
        R = Rn
    phet = hist[10] if len(hist) > 10 else hist[-1]   # cold solve + 10 updates
    return R, cur[k], len(hist), phet


REF['real'] = {}
for key, lab in [('bulb', 4), ('series', 5)]:
    R, I, nit, phet = real_solve(key, lab)
    V = I * Fr(str(R))
    REF['real'][key] = {'R': float(R), 'I': float(I), 'V': float(V), 'iters': nit,
                        'phetR': float(phet[0]), 'phetI': float(phet[1])}
    P('%-6s real bulb: R = %s Ohm, I = %s A, V = %s V after %d passes; PhET\'s 10 passes give R = %s (%.1e off)'
      % (key, f17(R), f17(I), f17(V), nit, f17(phet[0]), abs(float(phet[0] - R)) / float(R)))

# the fuse: the series preset with the bulb swapped for a fuse and the
# resistor set to 1 Ohm (trips) and 3 Ohm (holds); and a 0.5 A fuse in the
# bulb preset
P('\n--- fuses (PhET: R = 0.06/rating, trips when |I| > rating + 1e-6 A) ---')
REF['fuse'] = {}
for Rr in ['1', '3']:
    over = {5: None}
    N0, br0 = netlist_from_preset('series', over={3: {'R': Rr}})
    # swap el 5 (the bulb) for a 4 A fuse: same vertices, R = 0.06/4
    br1 = [x if x[5] != 5 else (x[0], x[1], FUSE_K / 4, Fr(0), 'R', 5) for x in br0]
    v, cur, *_ = solve_exact(N0, br1)
    k = next(i for i, x in enumerate(br1) if x[5] == 5)
    tr = abs(cur[k]) > 4 + Fr('1e-6')
    REF['fuse'][Rr] = {'I': float(cur[k]), 'trips': bool(tr)}
    P('series, resistor %s Ohm, 4 A fuse: I = %s A -> %s' % (Rr, f17(cur[k]), 'TRIPS (then I = 0)' if tr else 'holds'))

# ---------------------------------------------------------------------------
P('\n--- random circuits: 16 decades of resistance, solved exactly ---')
# Park-Miller minimal standard generator: every product stays below 2^53, so
# JavaScript's doubles reproduce it bit for bit.  Values are rounded to six
# significant digits so both languages hold the very same doubles.


def gen_random(count, seed=20260918):
    s = [seed]

    def rnd():
        s[0] = (s[0] * 16807) % 2147483647
        return s[0] / 2147483647
    out = []
    for t in range(count):
        N = 3 + int(rnd() * 9)
        br = []
        for q in range(1, N):
            br.append((q, int(rnd() * q), float('%.6g' % 10 ** (-10 + 16 * rnd())), 0.0, 'R'))
        extra = int(rnd() * N)
        for q in range(extra):
            a, b = int(rnd() * N), int(rnd() * N)
            R = float('%.6g' % 10 ** (-10 + 16 * rnd()))
            if a != b:
                br.append((a, b, R, 0.0, 'R'))
        nb = 1 + int(rnd() * 3)
        for q in range(nb):
            a, b = int(rnd() * N), int(rnd() * N)
            R = float('%.6g' % 10 ** (-4 + 5 * rnd()))
            E = float('%.6g' % (120 * rnd()))
            if a != b:
                br.append((a, b, R, E, 'B'))
        out.append((N, br))
    return out


REF['random'] = []
worst_np = 0.0
for t, (N, brf) in enumerate(gen_random(30)):
    br = [(a, b, Fr(R), Fr(E), kind, k) for k, (a, b, R, E, kind) in enumerate(brf)]
    v, cur, comp, ref = solve_exact(N, br)
    kcl, kvl, nl = kcl_kvl(N, br, v, cur)
    assert kcl == 0 and kvl == 0
    vn, cn = solve_numpy(N, br)
    # numpy's error relative to each piece's current scale
    Isc = {}
    for k, (a, b, *_r) in enumerate(br):
        Isc[comp[a]] = max(Isc.get(comp[a], 0.0), abs(float(cur[k])))
    e = 0.0
    for k, (a, b, *_r) in enumerate(br):
        if Isc[comp[a]] > 0:
            e = max(e, abs(cn[k] - float(cur[k])) / Isc[comp[a]])
    worst_np = max(worst_np, e)
    REF['random'].append({'N': N, 'br': [[a, b, R, E, kind] for (a, b, R, E, kind) in brf],
                          'v': [float(x) for x in v], 'i': [float(x) for x in cur], 'numpyErrI': e})
    if t < 6 or e > 1e-6:
        P('random %2d: %2d nodes %2d branches, %d pieces, %d loops; numpy nodal current error %.2e of the piece\'s largest'
          % (t, N, len(br), len(set(comp)), nl, e))
P('30 random circuits solved exactly; numpy\'s float conductance solve is off by up to %.2e of a piece\'s largest current'
  % worst_np)
REF['misc']['randomNumpyWorst'] = worst_np

# ---------------------------------------------------------------------------
REF['meta'] = {'rho': [float(RHO_MIN), float(RHO_MAX)], 'snap': SNAP, 'solderR': float(SOLDER_R), 'tap': TAP}
P('\nall exact assertions held.')

io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
# the preset geometry, emitted
geo = {k: {'name': PRESETS[k]['name'], 'verts': PRESETS[k]['verts'], 'els': PRESETS[k]['els']} for k in PRESETS}
js = ('/* ================================================================== *\n'
      ' *  the preset circuits -- EMITTED by derive.py (do not edit here):    *\n'
      ' *  vertices in view units (y down), elements [type, a, b, values] in  *\n'
      ' *  creation order.  derive.py solves the very same geometry exactly.  *\n'
      ' * ================================================================== */\n'
      'const PRESET_GEOM=' + json.dumps(geo, separators=(',', ':')) + ';\n'
      'const PRESET_ORDER=' + json.dumps(PRESET_ORDER) + ';\n')
io.open(os.path.join(HERE, 'p2_presets.js'), 'w', encoding='utf-8').write(js)
io.open(os.path.join(HERE, 'p7_refs.js'), 'w', encoding='utf-8').write(
    '/* reference values -- EMITTED by derive.py from exact rational solves (see refvals.txt) */\n'
    'const REF=' + json.dumps(REF, separators=(',', ':')) + ';\n')
print('\nwrote refvals.txt, p2_presets.js, p7_refs.js')
