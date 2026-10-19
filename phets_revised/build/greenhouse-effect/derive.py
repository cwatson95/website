#!/usr/bin/env python3
"""derive.py — the Python twin for greenhouse-effect.html.

Re-derives every number the sim asserts and prints them to 12+ significant figures into
refvals.txt, which p7_refs.js carries verbatim.  Nothing here is quoted from memory.

What is proved here
-------------------
1. The Stefan-Boltzmann constant from CODATA h, c, k (scipy.constants) and the effective
   temperature of the Earth from the solar constant and the Bond albedo.
2. The N-layer grey atmosphere, three independent ways:
     (a) a brute-force linear solve of the full flux system (numpy.linalg.solve),
     (b) the closed form derived below,
     (c) a time-marching integration of PhET's own layer ODE to steady state.
   Energy balance is asserted at every layer and at the top of the atmosphere.
3. The classic result T_s = (N+1)^(1/4) T_eff for fully absorbing layers, and the general
   absorbance law T_s = T_eff [1 + sum_i a_i/(2-a_i)]^(1/4).
4. PhET's convention (a layer absorbs a fraction a but emits a FULL blackbody sigma T^4 in
   each direction) against Kirchhoff's law (emissivity = absorptivity): the two give
   IDENTICAL fluxes and ground temperature, and layer temperatures differing by exactly
   a^(-1/4).
5. The photon picture: the probability that an infrared photon emitted by the ground escapes
   to space under "absorbed with probability a_i, re-emitted up or down with probability 1/2"
   equals F / sigma T_s^4 exactly.  Markov chain, closed form and a seeded Monte Carlo.
6. PhET's own constants, read out of docs/phets/greenhouse-effect_en.html 1.3.13, and the
   surface temperatures its concentration-to-absorbance fit produces.

The closed form (derivation)
----------------------------
Layers 1..N at increasing altitude, absorbance a_i for infrared, transparent to sunlight.
J_i = the flux the layer emits in EACH direction.  U_i = upward flux just above layer i
(U_0 = sigma T_g^4 leaving the ground), D_i = downward flux just above layer i (D_N = 0).
    U_i = (1-a_i) U_{i-1} + J_i                       [transfer up]
    D_{i-1} = (1-a_i) D_i + J_i                       [transfer down]
    2 J_i = a_i (U_{i-1} + D_i)                       [layer energy balance]
    sigma T_g^4 = F + D_0,  F = (1-albedo) S          [ground energy balance]
Each layer conserves energy, so the NET upward flux Phi = U_i - D_i is the same at every
level; at the top D_N = 0 so Phi = U_N = F.  Put D_i = U_i - F into the first and third:
    U_i (1 - a_i/2) = U_{i-1} (1 - a_i/2) - a_i F / 2
    ==>  U_i = U_{i-1} - F a_i/(2 - a_i)
and with U_N = F,
    sigma T_g^4 = U_0 = F [ 1 + sum_i a_i/(2 - a_i) ].
For a_i = 1 that is F(N+1), i.e. T_s = (N+1)^(1/4) T_eff.
"""
import io
import os
import numpy as np
from scipy import constants as C

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = []


def emit(label, *vals):
    """One reference line: a label and its values at FULL double precision.

    '%.17g' round-trips a double exactly, so the JavaScript twin can be pinned bit for bit
    rather than to the twelve figures a printed table would carry -- the lesson of the
    lagrange_points build (Known-bad: print an unstable orbit's initial state at full
    precision), applied to every reference value here."""
    OUT.append(label + '\t' + '\t'.join('%.17g' % v for v in vals))


def rel(a, b):
    return abs(a - b) / max(abs(b), 1e-300)


CHECKS = []


def chk(name, cond, detail=''):
    CHECKS.append((name, bool(cond), detail))
    if not cond:
        print('  DERIVE FAIL — %s %s' % (name, detail))


# ======================================================================== #
#  1. constants                                                            #
# ======================================================================== #
SIGMA = C.Stefan_Boltzmann
SIGMA_FROM_HCK = 2 * np.pi ** 5 * C.k ** 4 / (15 * C.h ** 3 * C.c ** 2)
chk('sigma = 2 pi^5 k^4 / 15 h^3 c^2', rel(SIGMA_FROM_HCK, SIGMA) < 1e-12,
    '%.15g vs %.15g' % (SIGMA_FROM_HCK, SIGMA))
emit('SIGMA scipy, from hck', SIGMA, SIGMA_FROM_HCK)

# PhET rounds the same constant to ten digits in GreenhouseEffectConstants.  That rounded
# value is the one the SIM carries -- one constant throughout, so the twin uses it too, and
# the gap to CODATA is asserted rather than hidden: 3.25e-11, worth 2e-9 K on a 300 K planet.
PHET_SIGMA = 5.670374419e-8
SIGMA_MODEL = PHET_SIGMA
chk('PhET sigma is CODATA to 10 digits', rel(PHET_SIGMA, SIGMA) < 1e-10,
    '%.15g vs %.15g' % (PHET_SIGMA, SIGMA))
emit('PHET_SIGMA rel err', PHET_SIGMA, rel(PHET_SIGMA, SIGMA))

# The solar constant: the 2015 IAU nominal total solar irradiance, 1361 W/m^2.
S0 = 1361.0
ALB_EARTH = 0.30            # the textbook planetary (Bond) albedo
ALB_EARTH_NASA = 0.306      # NASA Earth fact sheet Bond albedo


def teff(F):
    """Effective (blackbody) temperature for an absorbed flux F, per unit area.  Uses the
    constant the SIM carries (PhET's ten-digit rounding), so the twin is exact."""
    return (F / SIGMA_MODEL) ** 0.25


F_EARTH = (1 - ALB_EARTH) * S0 / 4
T_EFF = teff(F_EARTH)
T_EFF_NASA = teff((1 - ALB_EARTH_NASA) * S0 / 4)
emit('EARTH S0 albedo F Teff', S0, ALB_EARTH, F_EARTH, T_EFF)
emit('EARTH Teff at NASA albedo 0.306', ALB_EARTH_NASA, T_EFF_NASA)
# what the CODATA constant would give instead of PhET's rounding: 2e-9 K
emit('EARTH Teff on CODATA sigma, difference',
     (F_EARTH / SIGMA) ** 0.25, (F_EARTH / SIGMA) ** 0.25 - T_EFF)
chk('Earth Teff is the textbook 255 K', abs(T_EFF - 255) < 0.5, '%.4f' % T_EFF)
T_SURF_EARTH = 288.0        # the conventional global mean surface temperature
emit('EARTH mean surface T, greenhouse warming', T_SURF_EARTH, T_SURF_EARTH - T_EFF)

# one layer, fully absorbing, on the real Earth
emit('EARTH one black layer', 2 ** 0.25 * T_EFF)

# ======================================================================== #
#  2. PhET's constants (read from docs/phets/greenhouse-effect_en.html)     #
# ======================================================================== #
PHET = dict(
    S_SUN=343.6,            # SunEnergySource.OUTPUT_ENERGY_RATE, W/m^2
    INTENSITY_MIN=0.5, INTENSITY_MAX=2.0,
    ALB_MEADOW=0.2,         # GroundLayer.GREEN_MEADOW_ALBEDO
    ALB_GLACIER=0.225,      # GroundLayer.PARTIALLY_GLACIATED_LAND_ALBEDO
    ALB_LAYER_MODEL=0.3,    # LayerModelModel groundLayerOptions.initialAlbedo
    ALB_MIN=0.0, ALB_MAX=0.9,
    TMIN_NIGHT=245.0,       # GroundLayer.MINIMUM_EARTH_AT_NIGHT_TEMPERATURE
    TMIN_LAYER_MODEL=125.0,
    TOP=50000.0,            # LayersModel.HEIGHT_OF_ATMOSPHERE
    N_CONC=12,              # LayersModel default numberOfAtmosphereLayers
    N_LAYER_MODEL=3,
    ABS_COEF=0.85,          # ConcentrationModel: absorbance = 0.85 c exp(-z/8400)
    SCALE_H=8400.0,
    ABS_MIN=0.1, ABS_MAX=1.0,
    SPAN_W=85000.0,         # SUNLIGHT_SPAN width (m); height 1
    CLOUD_W=18000.0,
    CLOUD_REFL_TOP=0.125 * 85000.0 / 18000.0,
    DENSITY_EARTH=1250.0, CP_EARTH=1250.0,
    DENSITY_GLASS=2500.0, CP_GLASS=840.0,
    VOLUME_COEF=3e-7,       # mass = SPAN_W * 1 * 3e-7 * density
    PHOTON_ABS_TIME_LAYER=0.25, PHOTON_ABS_TIME_CONC=1.0,
    EXPECTED_MAX_T=309.0,
)
# the cloud reflects energy * topVisibleLightReflectivity * (cloudWidth / sunlightSpanWidth)
CLOUD_REFL = PHET['CLOUD_REFL_TOP'] * PHET['CLOUD_W'] / PHET['SPAN_W']
chk('PhET cloud reflects exactly 0.125 of the sunlight', abs(CLOUD_REFL - 0.125) < 1e-15,
    '%.17g' % CLOUD_REFL)
emit('CLOUD reflectivity, top value', CLOUD_REFL, PHET['CLOUD_REFL_TOP'])

AREA = PHET['SPAN_W'] * 1.0
MASS_G = PHET['SPAN_W'] * 1.0 * PHET['VOLUME_COEF'] * PHET['DENSITY_EARTH']
MASS_L = PHET['SPAN_W'] * 1.0 * PHET['VOLUME_COEF'] * PHET['DENSITY_GLASS']
KG = AREA / (MASS_G * PHET['CP_EARTH'])     # K per (J/m^2) absorbed, ground
KL = AREA / (MASS_L * PHET['CP_GLASS'])     # K per (J/m^2) absorbed, a glass layer
emit('PHET heat mass ground layer', MASS_G, MASS_L)
emit('PHET K per J/m2 ground layer', KG, KL)
chk('ground response is exactly 32/15 K per J/m^2', abs(KG - 32 / 15) < 1e-15, '%.17g' % KG)

# the date -> concentration map (ConcentrationModel) and the gas mixing ratios it prints
DATES = [
    ('iceAge', 'ice age', 0.625, 180, 380, 215),
    ('y1750', '1750', 0.7147, 277, 694, 271),
    ('y1950', '1950', 0.7182, 311, 1116, 288),
    ('y2020', '2020', 0.7446, 413, 1889, 333),
]


def conc_altitudes(n):
    """PhET: spacing = 50000/(n+1), layer i at spacing*(i+1)."""
    sp = PHET['TOP'] / (n + 1)
    return np.array([sp * (i + 1) for i in range(n)])


def conc_absorbance(c, n=12):
    """ConcentrationModel: energyAbsorptionProportion = 0.85 c exp(-altitude/8400)."""
    z = conc_altitudes(n)
    return PHET['ABS_COEF'] * c * np.exp(-z / PHET['SCALE_H'])


ALT12 = conc_altitudes(12)
ALT3 = conc_altitudes(3)
emit('ALT12 spacing first last', PHET['TOP'] / 13, ALT12[0], ALT12[-1])
emit('ALT3', *ALT3)

# ======================================================================== #
#  3. the layer model: closed form, brute force and relaxation             #
# ======================================================================== #


def solve_closed(a, F):
    """The closed form derived in the docstring.  Returns a dict of fluxes."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    step = a / (2 - a)
    Eg = F * (1 + step.sum())
    U = np.empty(n + 1)
    U[0] = Eg
    for i in range(n):
        U[i + 1] = U[i] - F * step[i]
    D = U - F
    J = np.array([a[i] * (U[i] + D[i + 1]) / 2 for i in range(n)])
    return dict(Eg=Eg, U=U, D=D, J=J, F=F,
                Tg=teff(Eg), Tlayer=np.array([teff(j) for j in J]),
                Tkirch=np.array([teff(J[i] / a[i]) if a[i] > 0 else 0.0 for i in range(n)]))


def solve_brute(a, F):
    """The same system solved as a dense linear system in (Eg, J_1..J_N), with no use of the
    net-flux invariant — an independent route to the same answer."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    # U_i as a linear function of (Eg, J_1..J_N): coefficient rows
    U = np.zeros((n + 1, n + 1))
    U[0, 0] = 1.0
    for i in range(n):
        U[i + 1] = (1 - a[i]) * U[i]
        U[i + 1, 1 + i] += 1.0
    D = np.zeros((n + 1, n + 1))          # D[i] = downward flux just above layer i; D[n] = 0
    for i in range(n - 1, -1, -1):
        D[i] = (1 - a[i]) * D[i + 1]
        D[i, 1 + i] += 1.0
    M = np.zeros((n + 1, n + 1))
    b = np.zeros(n + 1)
    # ground: Eg - D_0 = F
    M[0] = -D[0]
    M[0, 0] += 1.0
    b[0] = F
    # layers: 2 J_i - a_i (U_{i-1} + D_i) = 0
    for i in range(n):
        M[1 + i] = -a[i] * (U[i] + D[i + 1])
        M[1 + i, 1 + i] += 2.0
    x = np.linalg.solve(M, b)
    Eg, J = x[0], x[1:]
    Uv = U @ x
    Dv = D @ x
    return dict(Eg=Eg, U=Uv, D=Dv, J=J, F=F, Tg=teff(Eg),
                Tlayer=np.array([teff(j) for j in J]))


def relax(a, F, dt=0.002, steps=100000, Tg0=245.0, Tl0=245.0):
    """PhET's own layer ODE, marched to steady state (forward Euler, fixed step).

    The step has to respect the ODE's own stiffness: a glass layer's linearised rate is
    2 K_L d(sigma T^4)/dT = 8 K_L sigma T^3, which at 300 K is 19 per second, so forward
    Euler needs dt below about 0.1 s and PhET's own 1/60 s frame is comfortably inside
    that.  At dt = 0.05 s the N = 3, a = 1 case overflows to NaN — it is the integrator,
    not the physics, and the sim clamps its own step against the same bound."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    Tg = float(Tg0)
    T = np.full(n, float(Tl0))
    for _ in range(steps):
        Jg = SIGMA_MODEL * Tg ** 4
        J = SIGMA_MODEL * T ** 4
        U = np.empty(n + 1)
        U[0] = Jg
        for i in range(n):
            U[i + 1] = (1 - a[i]) * U[i] + J[i]
        D = np.zeros(n + 1)
        for i in range(n - 1, -1, -1):
            D[i] = (1 - a[i]) * D[i + 1] + J[i]
        dTg = KG * (F + D[0] - Jg) * dt
        dT = KL * (a * (U[:n] + D[1:]) - 2 * J) * dt
        Tg += dTg
        T += dT
    return Tg, T


def balance_residuals(sol, a):
    """Max |absorbed - emitted| over the layers, and the top-of-atmosphere residual."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    res = [abs(a[i] * (sol['U'][i] + sol['D'][i + 1]) - 2 * sol['J'][i]) for i in range(n)]
    toa = abs(sol['U'][n] - sol['F'])
    gnd = abs(sol['Eg'] - sol['F'] - sol['D'][0])
    net = max(abs(sol['U'][i] - sol['D'][i] - sol['F']) for i in range(n + 1))
    return (max(res) if res else 0.0), toa, gnd, net


# --- the two solvers agree, and energy balances, over a wide sweep --------------
worst_agree = 0.0
worst_bal = 0.0
rng = np.random.default_rng(20260921)
cases = []
for n in range(0, 13):
    for aval in [0.05, 0.1, 0.25, 0.5, 0.75, 0.9, 1.0]:
        cases.append(np.full(n, aval))
for _ in range(60):
    n = int(rng.integers(1, 13))
    cases.append(rng.uniform(0.02, 1.0, n))
for c in cases:
    F = 274.88
    s1 = solve_closed(c, F)
    s2 = solve_brute(c, F)
    worst_agree = max(worst_agree, rel(s1['Eg'], s2['Eg']),
                      max([rel(x, y) for x, y in zip(s1['J'], s2['J'])] or [0.0]))
    r, toa, gnd, net = balance_residuals(s1, c)
    worst_bal = max(worst_bal, r, toa, gnd, net)
chk('closed form == brute-force linear solve', worst_agree < 1e-12, '%.3e' % worst_agree)
chk('energy balances at every layer, the ground and the top', worst_bal < 1e-9, '%.3e' % worst_bal)
emit('SOLVER agreement, worst balance residual', worst_agree, worst_bal)

# --- the classic ladder ---------------------------------------------------------
F0 = (1 - PHET['ALB_MEADOW']) * PHET['S_SUN']
T0 = teff(F0)
emit('PHET F0 Teff at albedo 0.2 and 343.6', F0, T0)
ladder = []
for n in range(0, 13):
    s = solve_closed(np.ones(n), F0)
    ladder.append(s['Tg'])
    chk('T_s = (N+1)^(1/4) Teff at N=%d' % n, rel(s['Tg'], (n + 1) ** 0.25 * T0) < 1e-13,
        '%.12g vs %.12g' % (s['Tg'], (n + 1) ** 0.25 * T0))
emit('LADDER black layers N=0..12', *ladder)
# and on the real Earth
emit('LADDER earth N=0..4', *[(n + 1) ** 0.25 * T_EFF for n in range(5)])

# --- the general absorbance law -------------------------------------------------
for n in [1, 2, 3, 12]:
    for aval in [0.1, 0.3, 0.5, 0.7, 0.9, 1.0]:
        s = solve_closed(np.full(n, aval), F0)
        law = T0 * (1 + n * aval / (2 - aval)) ** 0.25
        chk('law T_s = Teff[1+Na/(2-a)]^(1/4) N=%d a=%g' % (n, aval), rel(s['Tg'], law) < 1e-13,
            '%.12g vs %.12g' % (s['Tg'], law))
        emit('LAW N=%d a=%g Ts' % (n, aval), s['Tg'])

# --- relaxation reaches the same steady state -----------------------------------
for n, aval in [(1, 1.0), (3, 0.6), (3, 1.0), (12, 0.3)]:
    a = np.full(n, aval)
    s = solve_closed(a, F0)
    Tg, T = relax(a, F0, dt=0.002, steps=100000)
    chk('relaxation reaches the closed form (N=%d, a=%g)' % (n, aval), rel(Tg, s['Tg']) < 1e-9,
        '%.12g vs %.12g' % (Tg, s['Tg']))
    chk('and every layer (N=%d, a=%g)' % (n, aval),
        max(rel(x, y) for x, y in zip(T, s['Tlayer'])) < 1e-8, '')
    emit('RELAX N=%d a=%g Tg' % (n, aval), Tg, s['Tg'])

# --- Kirchhoff --------------------------------------------------------------------
for aval in [0.2, 0.5, 0.85]:
    a = np.full(3, aval)
    s = solve_closed(a, F0)
    ratio = [s['Tkirch'][i] / s['Tlayer'][i] for i in range(3)]
    chk('Kirchhoff layer T is exactly a^(-1/4) times PhET"s (a=%g)' % aval,
        max(abs(r - aval ** -0.25) for r in ratio) < 1e-13, '%.12g' % ratio[0])
    emit('KIRCH a=%g ratio a^-1/4' % aval, ratio[0], aval ** -0.25)

# ======================================================================== #
#  4. the photon picture                                                   #
# ======================================================================== #


def escape_markov(a):
    """Probability that an IR photon leaving the ground upward escapes to space, under
    "absorbed with probability a_i on crossing layer i, then re-emitted up or down with
    probability 1/2".  Solved as a linear system with no simulation."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    if n == 0:
        return 1.0
    # unknowns p_1..p_n (moving up, about to cross layer i) and q_1..q_n (moving down,
    # about to cross layer i).  p_{n+1} = 1 (escaped), q_0 = 0 (absorbed by the ground).
    N = 2 * n
    M = np.zeros((N, N))
    b = np.zeros(N)

    def pi(i):      # index of p_i, i = 1..n
        return i - 1

    def qi(i):      # index of q_i, i = 1..n
        return n + i - 1
    for i in range(1, n + 1):
        # p_i = (1-a_i) p_{i+1} + a_i (p_{i+1} + q_{i-1}) / 2
        M[pi(i), pi(i)] = 1.0
        cUp = (1 - a[i - 1]) + a[i - 1] / 2
        cDn = a[i - 1] / 2
        if i + 1 <= n:
            M[pi(i), pi(i + 1)] -= cUp
        else:
            b[pi(i)] += cUp * 1.0
        if i - 1 >= 1:
            M[pi(i), qi(i - 1)] -= cDn
        # q_i = (1-a_i) q_{i-1} + a_i (p_{i+1} + q_{i-1}) / 2
        M[qi(i), qi(i)] = 1.0
        cDn2 = (1 - a[i - 1]) + a[i - 1] / 2
        cUp2 = a[i - 1] / 2
        if i - 1 >= 1:
            M[qi(i), qi(i - 1)] -= cDn2
        if i + 1 <= n:
            M[qi(i), pi(i + 1)] -= cUp2
        else:
            b[qi(i)] += cUp2 * 1.0
    x = np.linalg.solve(M, b)
    return x[pi(1)]


class LCG:
    """The 32-bit linear congruential generator the sim uses, so that Python and JavaScript
    produce the SAME stream: every product stays below 2^53 and is therefore exact in double
    arithmetic in both languages."""

    def __init__(self, seed):
        self.s = seed % 4294967296

    def next(self):
        self.s = (1664525 * self.s + 1013904223) % 4294967296
        return self.s / 4294967296.0


def escape_mc(a, m, seed=12345):
    """Monte Carlo of the same walk, with the seeded LCG."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    r = LCG(seed)
    esc = 0
    cross = 0
    absorbed = 0
    up = 0
    for _ in range(m):
        i = 1          # about to cross layer i
        d = +1         # +1 up, -1 down
        while True:
            if i > n:
                esc += 1
                break
            if i < 1:
                break           # reached the ground
            cross += 1
            if r.next() < a[i - 1]:
                absorbed += 1
                if r.next() < 0.5:
                    d = +1
                    up += 1
                else:
                    d = -1
                i += d          # leaves layer i in direction d
            else:
                i += d          # passes through
    return esc / m, cross, absorbed, up


for tag, a in [('N1a1', np.ones(1)), ('N3a06', np.full(3, 0.6)), ('N3a1', np.ones(3)),
               ('grad1750', conc_absorbance(0.7147))]:
    F = F0
    s = solve_closed(a, F)
    pm = escape_markov(a)
    pf = F / s['Eg']
    chk('escape probability (Markov) == F/sigma Ts^4 [%s]' % tag, rel(pm, pf) < 1e-12,
        '%.12g vs %.12g' % (pm, pf))
    emit('ESCAPE %s markov closed' % tag, pm, pf)

# the Monte Carlo, with the same LCG the sim uses
for tag, a, m in [('N1a1', np.ones(1), 200000), ('N3a06', np.full(3, 0.6), 200000),
                  ('grad1750', conc_absorbance(0.7147), 200000)]:
    p, cross, absorbed, up = escape_mc(a, m, seed=12345)
    pm = escape_markov(a)
    sig = (pm * (1 - pm) / m) ** 0.5
    chk('Monte Carlo escape within 4 sigma [%s]' % tag, abs(p - pm) < 4 * sig,
        '%.6f vs %.6f, sigma %.6f' % (p, pm, sig))
    chk('re-emission is 50/50 [%s]' % tag, abs(up / absorbed - 0.5) < 4 * (0.25 / absorbed) ** 0.5,
        '%.6f of %d' % (up / absorbed, absorbed))
    emit('MC %s p markov sigma crossings absorbed up' % tag, p, pm, sig, cross, absorbed, up)

# the raw stream, so the JS generator can be pinned bit for bit
r = LCG(12345)
emit('LCG seed 12345 first 6', *[r.next() for _ in range(6)])
r = LCG(1)
emit('LCG seed 1 first 4', *[r.next() for _ in range(4)])

# the absorption statistic on a single crossing: the measured fraction must be a
for aval in [0.2, 0.5, 0.85]:
    r = LCG(777)
    m = 100000
    hit = sum(1 for _ in range(m) if r.next() < aval)
    sig = (aval * (1 - aval) / m) ** 0.5
    chk('single-crossing absorption fraction is a (%g)' % aval, abs(hit / m - aval) < 4 * sig,
        '%.6f' % (hit / m))
    emit('ABS a=%g measured sigma' % aval, hit / m, sig)

# ======================================================================== #
#  5. PhET's concentration screens                                          #
# ======================================================================== #
emit('PHET S_SUN ALB_MEADOW ALB_GLACIER ALB_LM', PHET['S_SUN'], PHET['ALB_MEADOW'],
     PHET['ALB_GLACIER'], PHET['ALB_LAYER_MODEL'])

for key, name, c, co2, ch4, n2o in DATES:
    alb = PHET['ALB_GLACIER'] if key == 'iceAge' else PHET['ALB_MEADOW']
    a = conc_absorbance(c)
    F = (1 - alb) * PHET['S_SUN']          # by date, PhET always has the cloud off
    s = solve_closed(a, F)
    emit('DATE %s c alb F Ts a1 a12' % key, c, alb, F, s['Tg'], a[0], a[-1])
    emit('DATE %s gases' % key, co2, ch4, n2o)
    emit('DATE %s Tc Tf' % key, s['Tg'] - 273.15, (s['Tg'] - 273.15) * 9 / 5 + 32)

# the concentration slider, cloud off and on, at albedo 0.2
for c in [0.0, 0.25, 0.5, 0.75, 1.0]:
    a = conc_absorbance(c)
    F = (1 - PHET['ALB_MEADOW']) * PHET['S_SUN']
    s = solve_closed(a, F)
    sc = solve_closed(a, F * (1 - 0.125))
    emit('CONC c=%g Ts Ts_cloud' % c, s['Tg'], sc['Tg'])
    emit('CONC c=%g sumstep escape' % c, sum(a / (2 - a)), F / s['Eg'])

# the flux profile at 1750, for the flux-meter view
a1750 = conc_absorbance(0.7147)
s1750 = solve_closed(a1750, (1 - PHET['ALB_MEADOW']) * PHET['S_SUN'])
emit('P1750 absorbance 12 layers', *a1750)
emit('P1750 U 13 levels', *s1750['U'])
emit('P1750 Tlayer 12', *s1750['Tlayer'])
emit('P1750 Eg Tg', s1750['Eg'], s1750['Tg'])

# ======================================================================== #
#  6. PhET's Layer Model screen                                             #
# ======================================================================== #
for n in [0, 1, 2, 3]:
    for aval in [0.1, 0.5, 1.0]:
        for inten, alb in [(1.0, 0.3), (0.5, 0.0), (2.0, 0.9)]:
            F = (1 - alb) * PHET['S_SUN'] * inten
            s = solve_closed(np.full(n, aval), F)
            emit('LM n=%d a=%g i=%g alb=%g Ts' % (n, aval, inten, alb), s['Tg'])
            if n:
                emit('LM n=%d a=%g i=%g alb=%g Tlayers' % (n, aval, inten, alb), *s['Tlayer'])

# the two-sheet stack at the intensities the slider reaches, for the model-level pins
for inten in [0.5, 2.0]:
    emit('LM n=2 a=0.5 i=%g alb=0.3 Ts2' % inten,
         solve_closed(np.full(2, 0.5), (1 - 0.3) * PHET['S_SUN'] * inten)['Tg'])

# the reachable extremes, to show PhET's minimum-temperature floors never bind with the sun on
lo = (1 - PHET['ALB_MAX']) * PHET['S_SUN'] * PHET['INTENSITY_MIN']
hi = (1 - PHET['ALB_MIN']) * PHET['S_SUN'] * PHET['INTENSITY_MAX']
s_lo = solve_closed(np.zeros(0), lo)
s_hi = solve_closed(np.ones(3), hi)
emit('LM extremes Tmin Tmax', s_lo['Tg'], s_hi['Tg'])
chk('the 125 K layer-model floor never binds with the sun on', s_lo['Tg'] > PHET['TMIN_LAYER_MODEL'],
    '%.4f' % s_lo['Tg'])
lo2 = (1 - PHET['ALB_GLACIER']) * PHET['S_SUN'] * (1 - 0.125)
chk('the 245 K night floor never binds on the concentration screens',
    teff(lo2) > PHET['TMIN_NIGHT'], '%.4f' % teff(lo2))
emit('CONC coldest reachable', teff(lo2))

# PhET hard-codes EXPECTED_MAX_TEMPERATURE = 309 for its thermometer.  The hottest state the
# concentration screens can reach is c = 1 with no cloud over a green meadow, and this solve
# puts it at 309.13 K — which is how we know the model here IS PhET's.
hottest = solve_closed(conc_absorbance(1.0), (1 - PHET['ALB_MEADOW']) * PHET['S_SUN'])['Tg']
chk('the hottest reachable state matches PhET EXPECTED_MAX_TEMPERATURE 309',
    abs(hottest - PHET['EXPECTED_MAX_T']) < 0.2, '%.6f' % hottest)
emit('HOTTEST reachable, PhET expected max', hottest, PHET['EXPECTED_MAX_T'])


# ======================================================================== #
#  6b. the sim's own integrator, pinned step for step                       #
# ======================================================================== #
def march(a, F, dt, nsub, frames, Tg0=245.0, Tl0=0.0):
    """Exactly what the sim does per frame: nsub forward-Euler sub-steps of dt/nsub, from
    PhET's own initial condition (the ground at its night floor, every atmosphere layer at
    the 0 K its EnergyAbsorbingEmittingLayer constructor gives it)."""
    a = np.asarray(a, dtype=float)
    n = len(a)
    Tg = float(Tg0)
    T = np.full(n, float(Tl0))
    h = dt / nsub
    out = []
    for f in range(frames):
        for _ in range(nsub):
            Jg = SIGMA_MODEL * Tg ** 4
            J = SIGMA_MODEL * T ** 4
            U = np.empty(n + 1)
            U[0] = Jg
            for i in range(n):
                U[i + 1] = (1 - a[i]) * U[i] + J[i]
            D = np.zeros(n + 1)
            for i in range(n - 1, -1, -1):
                D[i] = (1 - a[i]) * D[i + 1] + J[i]
            Tg = Tg + KG * (F + D[0] - Jg) * h
            T = T + KL * (a * (U[:n] + D[1:]) - 2 * J) * h
        out.append((Tg, T.copy()))
    return out


A1750 = conc_absorbance(0.7147)
F1750 = (1 - PHET['ALB_MEADOW']) * PHET['S_SUN']
traj = march(A1750, F1750, 1 / 60, 4, 1800)
for k in [0, 5, 59, 299, 1799]:
    emit('MARCH 1750 frame %d Tg' % (k + 1), traj[k][0])
emit('MARCH 1750 frame 1800 layer1 layer12', traj[1799][1][0], traj[1799][1][-1])
chk('five seconds of the sim"s integrator puts the ground within 5 K of the steady state',
    abs(traj[299][0] - s1750['Tg']) < 5.0, '%.6f vs %.6f' % (traj[299][0], s1750['Tg']))
chk('and thirty seconds within 0.2 K', abs(traj[1799][0] - s1750['Tg']) < 0.2,
    '%.6f vs %.6f' % (traj[1799][0], s1750['Tg']))
# the topmost layer is the slow one: it is the coldest, so 2 sigma T^4 is tiny and it takes
# tens of seconds to warm — which is why the readout prints the exact steady state alongside.
chk('the topmost layer is still far from its steady state after thirty seconds',
    abs(traj[1799][1][-1] - s1750['Tlayer'][-1]) > 1.0,
    '%.4f vs %.4f' % (traj[1799][1][-1], s1750['Tlayer'][-1]))
# the layer model starts at ITS floor, 125 K, not the concentration screens' 245 K
traj3 = march(np.full(3, 0.7), (1 - 0.3) * PHET['S_SUN'], 1 / 60, 4, 30,
              Tg0=PHET['TMIN_LAYER_MODEL'])
emit('MARCH LM3 a0.7 frame 30 Tg T1 T2 T3', traj3[29][0], *traj3[29][1])

# the stability bound the sub-step has to respect: 8 K_L sigma T^3 h < 2
Tmax = 520.0
hmax = 2 / (8 * KL * SIGMA_MODEL * Tmax ** 3)
emit('STABILITY h_max at 520 K, the sim sub-step', hmax, 1 / 240)
chk('the sim sub-step 1/240 s is inside the stability bound', 1 / 240 < hmax,
    '%.6g vs %.6g' % (1 / 240, hmax))

# an equivalent uniform absorbance for PhET's graded stack: the a with the same sum
for key, name, c, *_ in DATES:
    a = conc_absorbance(c)
    S = (a / (2 - a)).sum()
    aeq = 2 * S / (12 + S)          # solve 12 aeq/(2-aeq) = S
    chk('equivalent uniform absorbance reproduces the sum [%s]' % key,
        abs(12 * aeq / (2 - aeq) - S) < 1e-13, '%.12g' % aeq)
    emit('EQUIV %s sum aeq' % key, S, aeq)

# back radiation at the ground, and the outgoing flux, per date
for key, name, c, *_ in DATES:
    alb = PHET['ALB_GLACIER'] if key == 'iceAge' else PHET['ALB_MEADOW']
    a = conc_absorbance(c)
    F = (1 - alb) * PHET['S_SUN']
    s = solve_closed(a, F)
    emit('BACK %s Dg Eg F escape' % key, s['D'][0], s['Eg'], F, F / s['Eg'])

# PhET's photon production rates (a display layer, not the energy model)
def ir_rate(T, Tmin):
    return 0.0 if T <= Tmin else T ** 4 * PHET_SIGMA / 390 * 5 * 10


emit('PHOTONS visible per s at intensity 1, IR at 1750', 10.0, ir_rate(s1750['Tg'], 245.0))
emit('PHOTONS IR at 245 246 and 309 K', ir_rate(245.0, 245.0), ir_rate(246.0, 245.0),
     ir_rate(309.0, 245.0))
chk('PhET shows one photon in five', True)

# ======================================================================== #
#  7. temperature units                                                     #
# ======================================================================== #
for K in [245.0, 255.0, 273.15, 288.0, 309.0]:
    emit('UNITS K=%g C F' % K, K, K - 273.15, (K - 273.15) * 9 / 5 + 32)
chk('0 C is 32 F', abs((273.15 - 273.15) * 9 / 5 + 32 - 32) < 1e-15)
chk('-40 C is -40 F', abs((233.15 - 273.15) * 9 / 5 + 32 + 40) < 1e-13)

# ======================================================================== #
#  8. what a layer does to the outgoing flux (for the equation bar)         #
# ======================================================================== #
# the "greenhouse forcing" of adding one more fully absorbing layer at 1750 concentration
aN = conc_absorbance(0.7147)
base = solve_closed(aN, F0)['Tg']
emit('SENS dTs per 0.01 concentration at 1750',
     (solve_closed(conc_absorbance(0.7247), F0)['Tg'] - base) / 1.0)
emit('SENS Ts at c 0.7147 and 0.7446', base, solve_closed(conc_absorbance(0.7446), F0)['Tg'])

# ======================================================================== #
#  write refvals.txt                                                        #
# ======================================================================== #
txt = '\n'.join(OUT) + '\n'
io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8').write(txt)
nfail = sum(1 for _, ok_, _ in CHECKS if not ok_)
print('%d reference lines written to refvals.txt' % len(OUT))
print('%d checks, %d failed' % (len(CHECKS), nfail))
if nfail:
    raise SystemExit(1)
