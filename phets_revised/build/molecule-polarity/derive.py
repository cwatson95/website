#!/usr/bin/env python3
"""Python twin of molecule-polarity.html.

Re-derives every closed form the sim implements, checks limits, signs and
dimensions, cross-checks each clever form against a brute-force version, and
prints reference values to 15 digits.  gen_ref.py copies the printed JSON into
p7a_ref.js, where selfTest asserts against it and labels the assertions
"(python)" / "(scipy)" / "(exact)".

Contents
  1  PhET's 2-D model: bond dipole, molecular dipole, partial charges
  2  the vector sum: closed form vs componentwise, the exact cancellation
  3  the surfaces: PhET's gradient stops, widths and colours
  4  the bond-character bands and the dipole reference length
  5  the field: PhET's kinematic rule, and the damped rotor (RK4 + scipy)
  6  the real molecules: PhET's table, basic and advanced bond dipoles
  7  measured dipole moments (NIST CCCBDB) and the atlas statistics

Run:  python3 derive.py            (prints a report)
      python3 derive.py --json     (prints refvals.json only)
"""
import io
import json
import math
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
try:
    import numpy as np
except ImportError:                                            # pragma: no cover
    np = None
try:
    from scipy.integrate import solve_ivp
    from scipy.optimize import brentq
    HAVE_SCIPY = True
except ImportError:                                            # pragma: no cover
    HAVE_SCIPY = False

REF = {}
LOG = []


def say(*a):
    s = ' '.join(str(x) for x in a)
    LOG.append(s)
    if '--json' not in sys.argv:
        print(s)


def put(key, val):
    REF[key] = val
    return val


# ====================================================================== #
#  1.  PhET's 2-D model                                                  #
#  MPConstants (build 2.0.2): ELECTRONEGATIVITY_RANGE = (2, 4, default 2),
#  ELECTRONEGATIVITY_TICK_SPACING = 0.2, ATOM_DIAMETER = 100,
#  BOND_LENGTH = 150, ANGLE_RANGE = (-pi, pi),
#  SURFACE_GRADIENT_WIDTH_MULTIPLIER = 5.
#  Bond.dipoleProperty: deltaEN = EN2 - EN1; angle = bond angle, + pi when
#  deltaEN < 0; magnitude = |deltaEN|.  Both branches together are exactly
#  mu = deltaEN * unit(atom1 -> atom2), which is how this file writes it.
# ====================================================================== #
EN_MIN, EN_MAX, EN_STEP = 2.0, 4.0, 0.2
ATOM_DIAMETER = 100.0
BOND_LENGTH = 150.0
SURF_MULT = 5.0
DIPOLE_REF_MAG = EN_MAX - EN_MIN          # PhET: referenceMagnitude = range length = 2
DIPOLE_REF_LEN = 135.0                    # PhET: referenceLength = 135 px
BOND_CHARACTER_BAR = 415.0                # PhET: BondCharacterNode's bar width
EFIELD_K = 0.17                           # PhET: linear(0, 2, 0, 0.17, |mu|) rad per frame


def unit(a):
    return (math.cos(a), math.sin(a))


def bond_dipole(en1, en2, ang12):
    """PhET's bond dipole: magnitude |dEN|, along the atom1 -> atom2 direction
    ang12 when dEN > 0, reversed when dEN < 0.  Equivalently dEN * unit(ang12)."""
    d = en2 - en1
    m = abs(d)
    a = ang12 + (math.pi if d < 0 else 0.0)
    return (m * math.cos(a), m * math.sin(a))


def bond_dipole_signed(en1, en2, ang12):
    d = en2 - en1
    return (d * math.cos(ang12), d * math.sin(ang12))


def diatomic(enA, enB, theta):
    """PhET's DiatomicMolecule at molecule angle theta: A at theta+pi, B at
    theta, each BOND_LENGTH/2 from the centre; partial charges qA = +dEN,
    qB = -dEN with dEN = EN_B - EN_A."""
    r = BOND_LENGTH / 2.0
    A = (r * math.cos(theta + math.pi), r * math.sin(theta + math.pi))
    B = (r * math.cos(theta), r * math.sin(theta))
    d = enB - enA
    mu = bond_dipole(enA, enB, theta)          # A -> B direction is theta
    return dict(A=A, B=B, dEN=d, qA=d, qB=-d, mu=mu, mumag=math.hypot(*mu),
                muang=math.atan2(mu[1], mu[0]))


def triatomic(enA, enB, enC, angAB, angBC, theta=0.0):
    """PhET's TriatomicMolecule: B at the centre, A at theta+angAB and C at
    theta+angBC, both BOND_LENGTH away.  Bond AB runs A -> B (direction
    theta+angAB+pi), bond BC runs B -> C (direction theta+angBC)."""
    A = (BOND_LENGTH * math.cos(theta + angAB), BOND_LENGTH * math.sin(theta + angAB))
    C = (BOND_LENGTH * math.cos(theta + angBC), BOND_LENGTH * math.sin(theta + angBC))
    muAB = bond_dipole(enA, enB, theta + angAB + math.pi)
    muBC = bond_dipole(enB, enC, theta + angBC)
    mu = (muAB[0] + muBC[0], muAB[1] + muBC[1])
    qA = enB - enA
    qC = enB - enC
    qB = (enA - enB) + (enC - enB)
    bondangle = norm_angle(angAB - angBC, -math.pi)
    return dict(A=A, B=(0.0, 0.0), C=C, muAB=muAB, muBC=muBC, mu=mu,
                mumag=math.hypot(*mu), muang=math.atan2(mu[1], mu[0]),
                qA=qA, qB=qB, qC=qC, bondangle=bondangle,
                dAB=enB - enA, dBC=enC - enB)


def norm_angle(a, lo=0.0):
    TAU = 2 * math.pi
    x = (a - lo) % TAU
    if x < 0:
        x += TAU
    if x == TAU:
        x = 0.0
    return x + lo


def section1():
    say('')
    say('== 1. PhET\'s 2-D model =========================================')
    say('EN range %.1f..%.1f, tick %.1f; ATOM_DIAMETER %g, BOND_LENGTH %g' %
        (EN_MIN, EN_MAX, EN_STEP, ATOM_DIAMETER, BOND_LENGTH))
    # the two branches of PhET's constructor agree with the signed form everywhere
    worst = 0.0
    for i in range(11):
        for j in range(11):
            for k in range(13):
                e1 = EN_MIN + 0.2 * i
                e2 = EN_MIN + 0.2 * j
                a = -math.pi + 2 * math.pi * k / 12.0
                p = bond_dipole(e1, e2, a)
                q = bond_dipole_signed(e1, e2, a)
                worst = max(worst, math.hypot(p[0] - q[0], p[1] - q[1]))
    say('PhET\'s two-branch bond dipole == dEN * unit(1->2) to %.3e over 1573 cases' % worst)
    put('bondDipoleBranchMax', worst)

    d = diatomic(2.0, 3.0, 0.0)
    say('diatomic defaults (EN_A 2, EN_B 3, angle 0): |mu| = %.15f, angle = %.15f' %
        (d['mumag'], d['muang']))
    put('diatomicDefault', dict(mumag=d['mumag'], muang=d['muang'], qA=d['qA'], qB=d['qB'],
                                Ax=d['A'][0], Ay=d['A'][1], Bx=d['B'][0], By=d['B'][1]))
    # PhET's opening triatomic: bond angles 5pi/6 and pi/6, EN 2 / 3 / 2
    t = triatomic(2.0, 3.0, 2.0, 5 * math.pi / 6, math.pi / 6)
    say('triatomic defaults: bond angle %.15f deg, |mu| = %.15f, angle = %.15f' %
        (math.degrees(t['bondangle']), t['mumag'], t['muang']))
    say('  partial charges qA %.15f  qB %.15f  qC %.15f   (sum %.3e)' %
        (t['qA'], t['qB'], t['qC'], t['qA'] + t['qB'] + t['qC']))
    put('triatomicDefault', dict(bondangleDeg=math.degrees(t['bondangle']), mumag=t['mumag'],
                                 muang=t['muang'], qA=t['qA'], qB=t['qB'], qC=t['qC'],
                                 muABx=t['muAB'][0], muABy=t['muAB'][1],
                                 muBCx=t['muBC'][0], muBCy=t['muBC'][1],
                                 Ax=t['A'][0], Ay=t['A'][1], Cx=t['C'][0], Cy=t['C'][1]))
    # charge neutrality is an identity, not a coincidence: check it over the grid
    worstq = 0.0
    for i in range(11):
        for j in range(11):
            for k in range(11):
                tt = triatomic(EN_MIN + 0.2 * i, EN_MIN + 0.2 * j, EN_MIN + 0.2 * k,
                               5 * math.pi / 6, math.pi / 6)
                worstq = max(worstq, abs(tt['qA'] + tt['qB'] + tt['qC']))
    say('triatomic charge neutrality over the whole 11^3 EN grid: max |sum q| = %.3e' % worstq)
    put('chargeSumMax', worstq)
    # the diatomic's own neutrality
    put('diatomicChargeSumMax', max(abs(diatomic(EN_MIN + 0.2 * i, EN_MIN + 0.2 * j, 0.0)['qA'] +
                                        diatomic(EN_MIN + 0.2 * i, EN_MIN + 0.2 * j, 0.0)['qB'])
                                    for i in range(11) for j in range(11)))


# ====================================================================== #
#  2.  the vector sum                                                    #
# ====================================================================== #
def mumag_closed(dAB, dBC, bondangle):
    """|mu_AB + mu_BC| from the signed delta-ENs and the A-B-C angle.
    u(A->B) . u(B->C) = -cos(theta), so |mu|^2 = dAB^2 + dBC^2 - 2 dAB dBC cos theta."""
    return math.sqrt(max(0.0, dAB * dAB + dBC * dBC - 2 * dAB * dBC * math.cos(bondangle)))


def section2():
    say('')
    say('== 2. the vector sum ===========================================')
    worst = 0.0
    worst_at = None
    n = 0
    for i in range(11):
        for j in range(11):
            for k in range(11):
                for m in range(36):
                    enA = EN_MIN + 0.2 * i
                    enB = EN_MIN + 0.2 * j
                    enC = EN_MIN + 0.2 * k
                    th = math.pi * (m + 0.5) / 36.0
                    # put the bond angle th between the bonds, C fixed along +x
                    t = triatomic(enA, enB, enC, th, 0.0)
                    cf = mumag_closed(t['dAB'], t['dBC'], th)
                    e = abs(cf - t['mumag'])
                    n += 1
                    if e > worst:
                        worst, worst_at = e, (enA, enB, enC, math.degrees(th))
    say('closed form vs componentwise sum over %d (EN,EN,EN,theta): max |diff| = %.3e at %s'
        % (n, worst, worst_at))
    put('closedFormMax', worst)

    # the exact cancellation of a symmetric triatomic at 180 deg
    zeros = []
    for i in range(11):
        for j in range(11):
            enA = enC = EN_MIN + 0.2 * i
            enB = EN_MIN + 0.2 * j
            t = triatomic(enA, enB, enC, math.pi, 0.0)
            zeros.append(t['mumag'])
    say('symmetric triatomic at theta = 180 deg over the 121 EN pairs: max |mu| = %.3e'
        % max(zeros))
    put('cancelMax', max(zeros))
    # ... and the symmetric law 2|dEN| |cos(theta/2)|
    worst = 0.0
    for i in range(11):
        for j in range(11):
            for m in range(181):
                enA = enC = EN_MIN + 0.2 * i
                enB = EN_MIN + 0.2 * j
                th = math.radians(m)
                t = triatomic(enA, enB, enC, th, 0.0)
                law = 2 * abs(enB - enA) * abs(math.cos(th / 2))
                worst = max(worst, abs(law - t['mumag']))
    say('symmetric law |mu| = 2|dEN| |cos(theta/2)| : max |diff| = %.3e' % worst)
    put('symLawMax', worst)

    # the curve the view draws: EN 2 / 3.4 / 2, theta 0..180
    curve = []
    for m in range(0, 181, 10):
        th = math.radians(m)
        t = triatomic(2.0, 3.4, 2.0, th, 0.0)
        curve.append([m, t['mumag']])
    put('sumCurve_2_34_2', curve)
    say('curve EN 2/3.4/2: |mu|(0) = %.15f, |mu|(90) = %.15f, |mu|(180) = %.3e' %
        (curve[0][1], curve[9][1], curve[18][1]))
    # an asymmetric one, whose minimum is NOT at 180 and is NOT zero
    t120 = triatomic(2.0, 3.4, 2.6, math.radians(120), 0.0)
    put('asym_2_34_26_120', dict(mumag=t120['mumag'], dAB=t120['dAB'], dBC=t120['dBC']))
    lo = min(((mumag_closed(t120['dAB'], t120['dBC'], math.radians(m)), m) for m in range(0, 361)))
    say('asymmetric EN 2/3.4/2.6: |mu|(120 deg) = %.15f; over theta the minimum is %.15f at %d deg'
        % (t120['mumag'], lo[0], lo[1]))
    put('asymMin', dict(mumag=lo[0], deg=lo[1]))
    if HAVE_SCIPY:
        # the minimum of |mu|(theta) for unequal bonds is at theta = 180 too, with
        # value |dAB + dBC| -- check by brute force on a fine grid
        fine = min(mumag_closed(t120['dAB'], t120['dBC'], math.radians(m / 100.0))
                   for m in range(0, 36001))
        say('  fine grid (0.01 deg): min = %.15f;  |dAB + dBC| = %.15f'
            % (fine, abs(t120['dAB'] + t120['dBC'])))
        put('asymMinFine', fine)
        put('asymMinLaw', abs(t120['dAB'] + t120['dBC']))


# ====================================================================== #
#  3.  the surfaces                                                      #
# ====================================================================== #
RGB_BLACK = (0, 0, 0)
RGB_WHITE = (255, 255, 255)
RGB_RED = (255, 0, 0)
RGB_BLUE = (0, 0, 255)
RGB_NEUTRAL_GRAY = (128, 128, 128)
SURF_ALPHA = 0.72
ROYGB = ['#FF0000', '#FF2000', '#FF4000', '#FF6000', '#FF8000', '#FFA000', '#FFC000',
         '#FFE000', '#FFF000', '#FFFF00', '#F0F000', '#E0FF00', '#C0FF00', '#A0FF00',
         '#80FF00', '#60FF00', '#40FF00', '#20FF00', '#00FF00', '#00FF20', '#00FF40',
         '#00FF60', '#00FF80', '#00FFA0', '#00FFC0', '#00FFE0', '#00FFFF', '#00E0FF',
         '#00C0FF', '#00A0FF', '#0080FF', '#0060FF', '#0040FF', '#0020FF', '#0000FF']


def linear(a1, a2, b1, b2, x):
    """PhET's Utils.linear."""
    return (b2 - b1) / (a2 - a1) * (x - a1) + b1


def surface_width():
    """PhET: bond length + 2.25 * rA + 2.25 * rB, with r = ATOM_DIAMETER/2."""
    return BOND_LENGTH + 2.25 * (ATOM_DIAMETER / 2) + 2.25 * (ATOM_DIAMETER / 2)


def lerp3(c0, c1, t):
    return tuple(c0[i] + (c1[i] - c0[i]) * t for i in range(3))


def surface_colour(kind, dEN, p):
    """The colour PhET's gradient paints at model-x = p along the bond axis."""
    W = surface_width()
    if kind == 'density':
        if dEN == 0:
            return RGB_NEUTRAL_GRAY
        t = abs(dEN) / (EN_MAX - EN_MIN)
        n = linear(1, 0, W, W * SURF_MULT, t)
        s = min(1.0, max(0.0, (p + n / 2) / n))
        c0 = RGB_WHITE if dEN > 0 else RGB_BLACK
        c1 = RGB_BLACK if dEN > 0 else RGB_WHITE
        return lerp3(c0, c1, s)
    if dEN == 0:
        return RGB_WHITE
    t = abs(dEN) / (EN_MAX - EN_MIN)
    n = linear(1, 0, W / 2, W * SURF_MULT, t)
    s = min(1.0, max(0.0, (p + n / 2) / n))
    a = RGB_BLUE if dEN > 0 else RGB_RED
    l = RGB_RED if dEN > 0 else RGB_BLUE
    return lerp3(a, RGB_WHITE, 2 * s) if s < 0.5 else lerp3(RGB_WHITE, l, 2 * s - 1)


def roygb(e):
    """PhET's rainbow mapping of an electrostatic-potential value e."""
    t = min(1.0, max(0.0, (8 * e + 1) / 2)) * (len(ROYGB) - 1)
    i = int(math.floor(t))
    n = t - i
    lo = ROYGB[max(0, min(i, len(ROYGB) - 1))]
    hi = ROYGB[max(0, min(i + 1, len(ROYGB) - 1))]
    c0 = tuple(int(lo[1 + 2 * k:3 + 2 * k], 16) for k in range(3))
    c1 = tuple(int(hi[1 + 2 * k:3 + 2 * k], 16) for k in range(3))
    return lerp3(c0, c1, n)


def section3():
    say('')
    say('== 3. the surfaces =============================================')
    W = surface_width()
    say('surface width = %g + 2.25*%g + 2.25*%g = %g' %
        (BOND_LENGTH, ATOM_DIAMETER / 2, ATOM_DIAMETER / 2, W))
    put('surfaceWidth', W)
    widths = {}
    for dEN in (0.4, 1.0, 2.0):
        t = dEN / 2
        widths['density_%.1f' % dEN] = linear(1, 0, W, W * SURF_MULT, t)
        widths['potential_%.1f' % dEN] = linear(1, 0, W / 2, W * SURF_MULT, t)
    put('gradientWidths', widths)
    say('gradient widths: density dEN=2 -> %g (= the surface width), dEN=0 -> %g' %
        (widths['density_2.0'], linear(1, 0, W, W * SURF_MULT, 0)))
    say('                 potential dEN=2 -> %g (= half the width), dEN=0 -> %g' %
        (widths['potential_2.0'], linear(1, 0, W / 2, W * SURF_MULT, 0)))
    samples = {}
    for kind in ('density', 'potential'):
        for dEN in (-2.0, -1.0, 0.0, 1.0, 2.0):
            for p in (-W / 2, -W / 4, 0.0, W / 4, W / 2):
                samples['%s|%+.1f|%+.2f' % (kind, dEN, p)] = list(surface_colour(kind, dEN, p))
    put('surfaceSamples', samples)
    say('potential dEN=+2 at the A end (x=-W/2): rgb%s; at the B end: rgb%s' %
        (tuple(round(v, 6) for v in surface_colour('potential', 2.0, -W / 2)),
         tuple(round(v, 6) for v in surface_colour('potential', 2.0, W / 2))))
    say('  -> the more electronegative atom (B, dEN>0) is RED: PhET\'s key labels red "negative"')
    say('density  dEN=+2 at the A end: rgb%s; at the B end: rgb%s (black = more density)' %
        (tuple(round(v, 6) for v in surface_colour('density', 2.0, -W / 2)),
         tuple(round(v, 6) for v in surface_colour('density', 2.0, W / 2))))
    # the mid-point is the neutral colour for every dEN, by construction
    mids = [surface_colour('potential', d / 10.0, 0.0) for d in range(-20, 21)]
    say('potential at x = 0 is white for every dEN: max deviation %.3e' %
        max(max(abs(c[i] - 255) for i in range(3)) for c in mids))
    put('potentialMidMax', max(max(abs(c[i] - 255) for i in range(3)) for c in mids))
    put('roygbSamples', {('%+.3f' % e): [round(v, 9) for v in roygb(e)]
                         for e in (-0.5, -0.25, -0.125, 0.0, 0.125, 0.25, 0.5)})
    say('ROYGB: e=-0.125 -> rgb%s (red end), e=0 -> rgb%s, e=+0.125 -> rgb%s (blue end)' %
        (tuple(round(v, 3) for v in roygb(-0.125)), tuple(round(v, 3) for v in roygb(0.0)),
         tuple(round(v, 3) for v in roygb(0.125))))
    put('surfaceAlpha', SURF_ALPHA)
    put('roygbStops', ROYGB)


# ====================================================================== #
#  4.  bond character and the dipole reference length                     #
# ====================================================================== #
BANDS = [(0.05, 'nonpolar covalent'), (0.4, 'nearly nonpolar covalent'),
         (0.8, 'slightly polar covalent'), (1.2, 'polar covalent'),
         (1.6, 'slightly ionic'), (1e9, 'mostly ionic')]


def bond_character(dEN):
    x = round(abs(dEN), 2)
    for lim, name in BANDS:
        if x <= lim:
            return name
    return BANDS[-1][1]


def dipole_px(mag):
    """PhET's DipoleNode: referenceLength 135 px for referenceMagnitude 2."""
    return DIPOLE_REF_LEN * mag / DIPOLE_REF_MAG


def section4():
    say('')
    say('== 4. bond character, arrow lengths ============================')
    edges = {}
    for d in (0.0, 0.05, 0.051, 0.4, 0.41, 0.8, 0.81, 1.2, 1.21, 1.6, 1.61, 2.0):
        edges['%.3f' % d] = bond_character(d)
    put('bondCharacter', edges)
    say('bands: ' + '; '.join('%s -> %s' % (k, v) for k, v in sorted(edges.items(), key=lambda p: float(p[0]))))
    # PhET rounds to 2 dp BEFORE the comparison, so 0.404 is still "nearly nonpolar covalent"
    say('PhET rounds |dEN| to 2 dp first: 0.404 -> %s, 0.405 -> %s'
        % (bond_character(0.404), bond_character(0.405)))
    put('bondCharacterRounding', [bond_character(0.404), bond_character(0.405)])
    put('bondCharacterFraction', {('%.2f' % d): d / (EN_MAX - EN_MIN) for d in (0.0, 0.5, 1.0, 1.5, 2.0)})
    put('dipolePx', {('%.2f' % m): dipole_px(m) for m in (0.0, 0.2, 1.0, 2.0)})
    say('arrow length: |mu| = 2 -> %g px (PhET\'s reference), |mu| = 1 -> %g px'
        % (dipole_px(2.0), dipole_px(1.0)))
    put('bondCharacterBar', BOND_CHARACTER_BAR)


# ====================================================================== #
#  5.  the field                                                          #
# ====================================================================== #
def phet_align_steps(mu0, psi0, maxsteps=100000):
    """PhET's MoleculePolarityModel.step, verbatim in structure: each frame the
    dipole angle moves |linear(0, 2, 0, 0.17, |mu|)| radians toward 0, taking the
    short way round, and is clamped at the target."""
    step = abs(linear(0, EN_MAX - EN_MIN, 0, EFIELD_K, mu0))
    psi = norm_angle(psi0)
    n = 0
    hist = [psi]
    while n < maxsteps:
        if psi == 0:
            break
        if 0 < psi < math.pi:
            nxt = psi - step
            if nxt < 0:
                nxt = 0.0
        else:
            nxt = psi + step
            if nxt > 2 * math.pi:
                nxt = 0.0
        psi = nxt
        n += 1
        hist.append(psi)
        if step == 0:
            break
    return n, hist


def rotor_rhs(psi, w, muE, b, I=1.0):
    return w, (-muE * math.sin(psi) - b * w) / I


def rotor_rk4(psi0, w0, muE, b, dt, nsteps, I=1.0):
    """Fixed-step RK4 on I psi'' = -muE sin psi - b psi'."""
    psi, w = psi0, w0
    out = [(0.0, psi, w)]
    for k in range(nsteps):
        k1 = rotor_rhs(psi, w, muE, b, I)
        k2 = rotor_rhs(psi + dt / 2 * k1[0], w + dt / 2 * k1[1], muE, b, I)
        k3 = rotor_rhs(psi + dt / 2 * k2[0], w + dt / 2 * k2[1], muE, b, I)
        k4 = rotor_rhs(psi + dt * k3[0], w + dt * k3[1], muE, b, I)
        psi += dt / 6 * (k1[0] + 2 * k2[0] + 2 * k3[0] + k4[0])
        w += dt / 6 * (k1[1] + 2 * k2[1] + 2 * k3[1] + k4[1])
        out.append(((k + 1) * dt, psi, w))
    return out


def rotor_energy(psi, w, muE, I=1.0):
    """E = 1/2 I w^2 + muE (1 - cos psi);  dE/dt = -b w^2 <= 0."""
    return 0.5 * I * w * w + muE * (1 - math.cos(psi))


def section5():
    say('')
    say('== 5. the field ================================================')
    say('PhET\'s rule: dpsi per frame = linear(0, 2, 0, 0.17, |mu|) = 0.085 |mu| rad')
    for mu0 in (0.4, 1.0, 2.0):
        n, hist = phet_align_steps(mu0, math.radians(150))
        say('  |mu| = %.1f: step %.15f rad, %d frames from 150 deg (%.4f s at 60 fps)'
            % (mu0, abs(linear(0, 2, 0, EFIELD_K, mu0)), n, n / 60.0))
        put('phetSteps_%.1f' % mu0, n)
        put('phetStepSize_%.1f' % mu0, abs(linear(0, 2, 0, EFIELD_K, mu0)))
    # the short way round: from 210 deg it goes UP to 360, not down through 180
    n2, h2 = phet_align_steps(2.0, math.radians(210))
    say('  from 210 deg, |mu| = 2: %d frames, and psi INCREASES (%.4f -> %.4f rad) -- the short way'
        % (n2, h2[0], h2[1]))
    put('phetSteps_210', n2)
    put('phetDir_210', 1 if h2[1] > h2[0] else -1)

    say('')
    say('the damped rotor: I psi\'\' = -mu E sin psi - b psi\',  b = 2 zeta sqrt(I mu E)')
    I = 1.0
    muE = 1.0
    w0 = math.sqrt(muE / I)
    say('  mu E = %g, I = %g -> omega_0 = %.15f, critical b_c = %.15f' % (muE, I, w0, 2 * math.sqrt(I * muE)))
    put('rotorOmega0', w0)
    put('rotorBcrit', 2 * math.sqrt(I * muE))
    traces = {}
    for zeta in (0.2, 0.7, 1.0, 2.0):
        b = 2 * zeta * math.sqrt(I * muE)
        tr = rotor_rk4(math.radians(150), 0.0, muE, b, 0.002, 15000, I)
        # the energy never rises
        worst_rise = 0.0
        Eprev = rotor_energy(tr[0][1], tr[0][2], muE, I)
        for (t, p, w) in tr[1:]:
            E = rotor_energy(p, w, muE, I)
            worst_rise = max(worst_rise, E - Eprev)
            Eprev = E
        settle = None
        for idx in range(len(tr)):
            if all(abs(tr[j][1]) < 0.01 for j in range(idx, min(len(tr), idx + 500))):
                settle = tr[idx][0]
                break
        say('  zeta = %.1f: b = %.15f, psi(30 s) = %.3e rad, max energy rise %.3e, settle(|psi|<0.01) %.15f s'
            % (zeta, b, tr[-1][1], worst_rise, settle if settle is not None else float('nan')))
        traces['%.1f' % zeta] = dict(b=b, psiEnd=tr[-1][1], wEnd=tr[-1][2],
                                     energyRise=worst_rise, settle=settle,
                                     psi_at_1s=tr[500][1], psi_at_3s=tr[1500][1])
    put('rotorTraces', traces)
    # overshoot: only zeta < 1 crosses zero
    for zeta in (0.2, 0.7, 1.0, 2.0):
        b = 2 * zeta * math.sqrt(I * muE)
        tr = rotor_rk4(math.radians(150), 0.0, muE, b, 0.002, 15000, I)
        crossings = sum(1 for k in range(1, len(tr)) if tr[k - 1][1] * tr[k][1] < 0)
        say('  zeta = %.1f: %d zero crossings from 150 deg' % (zeta, crossings))
        put('rotorCrossings_%.1f' % zeta, crossings)
    # the unstable equilibrium: starting exactly at pi it never moves
    tr = rotor_rk4(math.pi, 0.0, muE, 2 * math.sqrt(muE), 0.002, 2000, I)
    say('  from psi = pi exactly (the unstable equilibrium): psi(4 s) - pi = %.3e' % (tr[-1][1] - math.pi))
    put('rotorUnstable', tr[-1][1] - math.pi)
    tr = rotor_rk4(math.pi - 1e-3, 0.0, muE, 2 * math.sqrt(muE), 0.002, 15000, I)
    say('  from psi = pi - 1e-3: psi(30 s) = %.3e -- it falls to the stable one' % tr[-1][1])
    put('rotorNearUnstable', tr[-1][1])
    if HAVE_SCIPY:
        for zeta in (0.2, 1.0):
            b = 2 * zeta * math.sqrt(I * muE)
            sol = solve_ivp(lambda t, y: [y[1], (-muE * math.sin(y[0]) - b * y[1]) / I],
                            [0, 3], [math.radians(150), 0.0], rtol=1e-11, atol=1e-13,
                            dense_output=True)
            mine = rotor_rk4(math.radians(150), 0.0, muE, b, 0.002, 1500, I)[-1]
            say('  scipy vs RK4 at t = 3 s, zeta %.1f: %.15f vs %.15f (diff %.3e)'
                % (zeta, sol.sol(3.0)[0], mine[1], abs(sol.sol(3.0)[0] - mine[1])))
            put('rotorScipy_%.1f' % zeta, dict(scipy=sol.sol(3.0)[0], rk4=mine[1],
                                               diff=abs(sol.sol(3.0)[0] - mine[1])))
    # the linearised solution, for the small-angle check
    zeta = 0.2
    b = 2 * zeta * math.sqrt(I * muE)
    wd = w0 * math.sqrt(1 - zeta * zeta)
    psi0 = 1e-4
    lin = [psi0 * math.exp(-zeta * w0 * t) * (math.cos(wd * t) + zeta / math.sqrt(1 - zeta * zeta) * math.sin(wd * t))
           for t in (0.5, 1.0, 2.0)]
    tr = rotor_rk4(psi0, 0.0, muE, b, 0.0005, 4000, I)
    num = [tr[1000][1], tr[2000][1], tr[4000][1]]
    say('  small-angle: linear solution vs RK4 at 0.5/1/2 s: %s vs %s'
        % (['%.12e' % v for v in lin], ['%.12e' % v for v in num]))
    put('rotorLinear', dict(lin=lin, num=num, wd=wd,
                            relmax=max(abs(a - c) / abs(a) for a, c in zip(lin, num))))


# ====================================================================== #
#  6.  the real molecules                                                 #
# ====================================================================== #
PAULING = {'H': 2.20, 'B': 2.04, 'C': 2.55, 'N': 3.04, 'O': 3.44, 'F': 3.98, 'Cl': 3.16}
VDW_PM = {'H': 120, 'B': 192, 'C': 170, 'N': 155, 'O': 152, 'F': 147, 'Cl': 175}
DEBYE_PER_EA = 0.208194        # PhET's constant: mu[D] = q[e] * d[A] / 0.208194
NAMES = {'H2': 'hydrogen', 'N2': 'nitrogen', 'O2': 'oxygen', 'F2': 'fluorine',
         'HF': 'hydrogen fluoride', 'H2O': 'water', 'CO2': 'carbon dioxide',
         'HCN': 'hydrogen cyanide', 'O3': 'ozone', 'NH3': 'ammonia', 'BH3': 'borane',
         'BF3': 'boron trifluoride', 'CH2O': 'formaldehyde', 'CH4': 'methane',
         'CH3F': 'fluoromethane', 'CH2F2': 'difluoromethane', 'CHF3': 'trifluoromethane',
         'CHCl3': 'chloroform', 'CF4': 'tetrafluoromethane'}
ORDER = ['H2', 'N2', 'O2', 'F2', 'HF', 'H2O', 'CO2', 'HCN', 'O3', 'NH3', 'BH3', 'BF3',
         'CH2O', 'CH4', 'CH3F', 'CH2F2', 'CHF3', 'CHCl3', 'CF4']
# NIST CCCBDB, "Experimental Dipole Moments" (cccbdb.nist.gov/diplistx.asp),
# retrieved 2026-09-22.  Value in debye exactly as printed, with CCCBDB's own
# source code for that row.  BH3 is absent from the table.
MEASURED = {
    'H2O': (1.857, '1991Sho/Ebe:5875-5882'), 'NH3': (1.476, '1970Shi:3572-3576'),
    'HF': (1.827, 'NISTDiatomic'), 'HCN': (2.980, 'NSRDS-NBS10'),
    'CH2O': (2.332, '2003The/Cal:8910-8915'), 'CH3F': (1.847, '1974Hel/Hel(II/6)'),
    'CH2F2': (1.970, 'NSRDS-NBS10'), 'CHF3': (1.645, '1951Sho/Sha:95'),
    'CHCl3': (1.040, '1970Rei/Wil:1418-1421'), 'O3': (0.530, 'NSRDS-NBS10'),
    'CO2': (0.000, 'NSRDS-NBS10'), 'CH4': (0.000, 'NSRDS-NBS10'),
    'CF4': (0.000, 'NSRDS-NBS10'), 'BF3': (0.000, 'NSRDS-NBS10'),
    'H2': (0.000, 'NSRDS-NBS10'), 'N2': (0.000, 'NSRDS-NBS10'),
    'O2': (0.000, 'NSRDS-NBS10'), 'F2': (0.000, 'NSRDS-NBS10'),
}


def load_real():
    with io.open(os.path.join(HERE, '_out', 'real_molecules.json'), encoding='utf-8') as f:
        return json.load(f)


def origin_offset(m):
    """PhET's RealMolecule.computeOriginOffset: the midpoint for a homonuclear
    diatomic, the F for a heteronuclear one, otherwise the most-bonded atom."""
    atoms = m['atoms']
    if len(atoms) == 2:
        if atoms[0]['symbol'] == atoms[1]['symbol']:
            return [(atoms[0][k] + atoms[1][k]) / 2 for k in 'xyz']
        f = [a for a in atoms if a['symbol'] == 'F'][0]
        return [f[k] for k in 'xyz']
    best, bn = None, -1
    for i, a in enumerate(atoms):
        n = sum(1 for b in m['bonds'] if b['indexA'] == i or b['indexB'] == i)
        if n > bn:
            bn, best = n, i
    return [atoms[best][k] for k in 'xyz']


def real_molecule(sym, data):
    m = data[sym]
    off = origin_offset(m)
    pos = [[a[k] - off[j] for j, k in enumerate('xyz')] for a in m['atoms']]
    syms = [a['symbol'] for a in m['atoms']]
    q = m['hirshfeld']
    out = dict(symbol=sym, name=NAMES[sym], syms=syms, pos=pos, q=q,
               simplified=m.get('charges'),
               bonds=[[b['indexA'], b['indexB'], b['bondType']] for b in m['bonds']],
               realDipole=m['molecularDipole'],
               realDipoleMag=math.sqrt(sum(v * v for v in m['molecularDipole'])))
    bd_basic, bd_adv = [], []
    for b in m['bonds']:
        ia, ib = b['indexA'], b['indexB']
        d = [pos[ib][k] - pos[ia][k] for k in range(3)]
        L = math.sqrt(sum(v * v for v in d))
        u = [v / L for v in d]
        # basic: |dEN| along the positive -> negative direction (Pauling EN)
        enA, enB = PAULING[syms[ia]], PAULING[syms[ib]]
        mb = abs(enB - enA)
        ub = u if enB - enA >= 0 else [-v for v in u]
        bd_basic.append([mb * v for v in ub])
        # advanced: |(qA - qB)/2| * d / 0.208194, direction by the Hirshfeld charges
        ma = abs((q[ia] - q[ib]) / 2 * (L / DEBYE_PER_EA))
        ua = u if q[ia] - q[ib] >= 0 else [-v for v in u]
        bd_adv.append([ma * v for v in ua])
        out.setdefault('lengths', []).append(L)
    out['bondDipolesBasic'] = bd_basic
    out['bondDipolesAdv'] = bd_adv
    out['sumBasic'] = [sum(v[k] for v in bd_basic) for k in range(3)]
    out['sumAdv'] = [sum(v[k] for v in bd_adv) for k in range(3)]
    out['sumBasicMag'] = math.sqrt(sum(v * v for v in out['sumBasic']))
    out['sumAdvMag'] = math.sqrt(sum(v * v for v in out['sumAdv']))
    # PhET's getDipoleArrowScale: advanced arrows are rescaled so the drawn
    # molecular dipole carries the REAL (Psi4) magnitude
    out['arrowScaleAdv'] = 0.25 if out['sumAdvMag'] <= 1e-5 else \
        out['realDipoleMag'] / out['sumAdvMag'] * 3 * 0.25
    out['arrowScaleBasic'] = 0.75
    out['radii'] = [0.25 * VDW_PM[s] / 100.0 for s in syms]
    return out


def section6():
    say('')
    say('== 6. the real molecules =======================================')
    data = load_real()
    rows = {}
    for sym in ORDER:
        r = real_molecule(sym, data)
        rows[sym] = r
        say('%-6s %-20s atoms %d  |mu| Psi4 %.6f D  sum(basic) %.6f  sum(adv) %.6f D  scale %.6f'
            % (sym, r['name'], len(r['syms']), r['realDipoleMag'], r['sumBasicMag'],
               r['sumAdvMag'], r['arrowScaleAdv']))
    # charge neutrality of the Hirshfeld sets
    worst = max(abs(sum(rows[s]['q'])) for s in ORDER)
    say('Hirshfeld charges sum to zero: max |sum q| = %.3e' % worst)
    put('hirshfeldSumMax', worst)
    # the symmetric molecules' vector sums vanish
    sym0 = ['H2', 'N2', 'O2', 'F2', 'CO2', 'CH4', 'CF4', 'BF3', 'BH3']
    say('symmetric set, |sum of advanced bond dipoles|: ' +
        ', '.join('%s %.2e' % (s, rows[s]['sumAdvMag']) for s in sym0))
    put('symmetricSumAdv', {s: rows[s]['sumAdvMag'] for s in sym0})
    put('symmetricSumBasic', {s: rows[s]['sumBasicMag'] for s in sym0})
    put('symmetricPsi4', {s: rows[s]['realDipoleMag'] for s in sym0})
    # --- a geometry audit.  PhET takes its coordinates from PubChem, whose 3-D
    # conformers are force-field optimised, not experimental.  Check the bond
    # angles the data really carry against the textbook ones before trusting the
    # dipoles computed on them.
    say('')
    say('bond angles in PhET\'s stored geometry (central atom, all pairs):')
    # measured: NIST CCCBDB "Experimental bond angles" (cccbdb.nist.gov/expangle2x.asp),
    # release 22, May 2022, retrieved 2026-09-22, to the 2 decimals it prints.
    # symmetry: fixed by the point group, so no measurement is needed.
    KNOWN = {'H2O': ('H-O-H', 104.48, 'CCCBDB'), 'NH3': ('H-N-H', 106.67, 'CCCBDB'),
             'O3': ('O-O-O', 116.80, 'CCCBDB'), 'CH2O': ('H-C-H', 116.13, 'CCCBDB'),
             'CH4': ('H-C-H', 109.47, 'CCCBDB'),
             'CO2': ('O-C-O', 180.0, 'symmetry'), 'HCN': ('H-C-N', 180.0, 'symmetry'),
             'BF3': ('F-B-F', 120.0, 'symmetry'), 'BH3': ('H-B-H', 120.0, 'symmetry'),
             'CF4': ('F-C-F', math.degrees(math.acos(-1 / 3.0)), 'symmetry')}
    audit = {}
    for sym in ORDER:
        r = rows[sym]
        if len(r['syms']) < 3:
            continue
        deg = [sum(1 for b in r['bonds'] if b[0] == i or b[1] == i) for i in range(len(r['syms']))]
        c = deg.index(max(deg))
        nb = [b[1] if b[0] == c else b[0] for b in r['bonds'] if c in (b[0], b[1])]
        angs = sorted(round(angle_deg(r['pos'][c], r['pos'][i], r['pos'][j]), 6)
                      for a, i in enumerate(nb) for j in nb[a + 1:])
        audit[sym] = angs
        note = ''
        if sym in KNOWN:
            nm, kv, src = KNOWN[sym]
            near = min(angs, key=lambda v: abs(v - kv))
            note = '   %s: stored %.3f vs %.3f %s (%+.3f)' % (nm, near, kv, src, near - kv)
        say('  %-6s %s%s' % (sym, ', '.join('%.3f' % v for v in angs), note))
    put('realAngles', audit)
    put('realAnglesKnown', {k: list(v) for k, v in KNOWN.items()})
    gaps = {}
    for sym, (nm, kv, src) in KNOWN.items():
        near = min(audit[sym], key=lambda v: abs(v - kv))
        gaps[sym] = dict(name=nm, stored=near, known=kv, src=src, diff=near - kv)
    put('realAngleGaps', gaps)
    bad = sorted(gaps.items(), key=lambda p: -abs(p[1]['diff']))[:3]
    say('  worst three: ' + ', '.join('%s %+.2f deg' % (k, v['diff']) for k, v in bad))

    # water, in detail, since it is the one everybody knows
    w = rows['H2O']
    ang = angle_deg(w['pos'][0], w['pos'][1], w['pos'][2])
    say('water: O-H %.9f A, H-O-H %.9f deg, Hirshfeld q(O) %.6f q(H) %.6f'
        % (w['lengths'][0], ang, w['q'][0], w['q'][1]))
    say('  advanced bond dipole %.9f D each; their sum %.9f D; Psi4 %.9f D; scale %.9f'
        % (math.sqrt(sum(v * v for v in w['bondDipolesAdv'][0])), w['sumAdvMag'],
           w['realDipoleMag'], w['arrowScaleAdv']))
    say('  2 mu_bond cos(theta/2) = %.9f (identity check)'
        % (2 * math.sqrt(sum(v * v for v in w['bondDipolesAdv'][0])) * math.cos(math.radians(ang) / 2)))
    put('waterDetail', dict(bondLength=w['lengths'][0], angleDeg=ang, qO=w['q'][0], qH=w['q'][1],
                            bondDipoleAdv=math.sqrt(sum(v * v for v in w['bondDipolesAdv'][0])),
                            sumAdv=w['sumAdvMag'], psi4=w['realDipoleMag'],
                            scale=w['arrowScaleAdv'],
                            law=2 * math.sqrt(sum(v * v for v in w['bondDipolesAdv'][0])) *
                            math.cos(math.radians(ang) / 2)))
    # what the JS table needs, trimmed to what the sim draws
    table = {}
    for sym in ORDER:
        r = rows[sym]
        table[sym] = dict(name=r['name'], syms=r['syms'], pos=r['pos'],
                          bonds=r['bonds'], q=r['q'], psi4=r['realDipole'])
    put('realTable', table)
    put('realDerived', {s: dict(psi4mag=rows[s]['realDipoleMag'],
                                basic=rows[s]['sumBasicMag'], adv=rows[s]['sumAdvMag'],
                                scale=rows[s]['arrowScaleAdv'],
                                lengths=rows[s]['lengths']) for s in ORDER})
    return rows


def angle_deg(centre, a, b):
    u = [a[k] - centre[k] for k in range(3)]
    v = [b[k] - centre[k] for k in range(3)]
    nu = math.sqrt(sum(x * x for x in u))
    nv = math.sqrt(sum(x * x for x in v))
    c = sum(u[k] * v[k] for k in range(3)) / (nu * nv)
    return math.degrees(math.acos(max(-1.0, min(1.0, c))))


# ====================================================================== #
#  7.  the atlas                                                          #
# ====================================================================== #
def section7(rows):
    say('')
    say('== 7. the atlas: computed against measured =====================')
    say('%-6s %-20s %10s %10s %10s   %s' % ('', '', 'Psi4 D', 'meas D', 'diff', 'CCCBDB source'))
    diffs = []
    for sym in ORDER:
        r = rows[sym]
        if sym in MEASURED:
            mv, src = MEASURED[sym]
            d = r['realDipoleMag'] - mv
            diffs.append(abs(d))
            say('%-6s %-20s %10.3f %10.3f %+10.3f   %s'
                % (sym, r['name'], r['realDipoleMag'], mv, d, src))
        else:
            say('%-6s %-20s %10.3f %10s %10s   %s'
                % (sym, r['name'], r['realDipoleMag'], '--', '--', 'absent from CCCBDB'))
    mae = sum(diffs) / len(diffs)
    say('mean |Psi4 - measured| over the %d measured molecules: %.6f D; worst %.6f D'
        % (len(diffs), mae, max(diffs)))
    put('atlasMAE', mae)
    put('atlasWorst', max(diffs))
    put('measured', {k: list(v) for k, v in MEASURED.items()})
    # the basic model has no debye scale at all -- only an ORDERING.  Check the
    # rank correlation between sum(basic) and the measured value on the polar set.
    polar = [s for s in ORDER if s in MEASURED and MEASURED[s][0] > 0]
    xs = [rows[s]['sumBasicMag'] for s in polar]
    ys = [MEASURED[s][0] for s in polar]
    rho = spearman(xs, ys)
    say('basic mode (sum of |dEN| vectors) vs measured on the %d polar molecules: Spearman rho = %.9f'
        % (len(polar), rho))
    put('spearmanBasic', rho)
    xs2 = [rows[s]['realDipoleMag'] for s in polar]
    say('advanced (Psi4) vs measured on the same set: Spearman rho = %.9f' % spearman(xs2, ys))
    put('spearmanAdv', spearman(xs2, ys))
    put('polarSet', polar)
    # the zero set: exactly which molecules PhET's data makes non-polar
    zeros = [s for s in ORDER if rows[s]['realDipoleMag'] < 1e-3]
    say('Psi4 |mu| < 1e-3 D: ' + ', '.join(zeros))
    put('zeroSet', zeros)


def spearman(x, y):
    def rank(v):
        order = sorted(range(len(v)), key=lambda i: v[i])
        r = [0.0] * len(v)
        i = 0
        while i < len(order):
            j = i
            while j + 1 < len(order) and v[order[j + 1]] == v[order[i]]:
                j += 1
            avg = (i + j) / 2.0 + 1
            for k in range(i, j + 1):
                r[order[k]] = avg
            i = j + 1
        return r
    rx, ry = rank(x), rank(y)
    n = len(x)
    mx = sum(rx) / n
    my = sum(ry) / n
    num = sum((rx[i] - mx) * (ry[i] - my) for i in range(n))
    den = math.sqrt(sum((rx[i] - mx) ** 2 for i in range(n)) * sum((ry[i] - my) ** 2 for i in range(n)))
    return num / den


# ====================================================================== #
def main():
    section1()
    section2()
    section3()
    section4()
    section5()
    rows = section6()
    section7(rows)
    put('_scipy', HAVE_SCIPY)
    out = json.dumps(REF, indent=1, sort_keys=True)
    with io.open(os.path.join(HERE, 'refvals.json'), 'w', encoding='utf-8') as f:
        f.write(out)
    with io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8') as f:
        f.write('\n'.join(LOG) + '\n')
    if '--json' in sys.argv:
        print(out)
    else:
        say('')
        say('refvals.json: %d keys, %d bytes' % (len(REF), len(out)))


if __name__ == '__main__':
    main()
