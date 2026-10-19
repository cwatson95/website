#!/usr/bin/env python3
"""derive.py — the Python twin of gases-intro.html.

Gases Intro is PhET's Ideal screen twice over: the Intro screen without the
Hold Constant panel, the Laws screen with it (read straight out of the
minified original: `class wb extends vb{... hasHoldConstantFeature:!1}` is
IntroScreen, `class Sb extends vb{... hasHoldConstantFeature:!0}` is
LawsScreen, both extending IdealScreen).  The hard-disk engine and its
invariants are already derived in build/gas-properties/derive.py and are not
repeated here; this file derives what THIS sim pins on top of them:

 1. PhET's constants and unit conversions, recomputed from CODATA/SI rather
    than retyped, and compared with the values read out of the minified
    original (cited "PhET's value").
 2. The gas law in PhET's units at specific states, and the four named laws'
    invariants along the sweeps the sim runs (Boyle PV, Charles V/T,
    Gay-Lussac P/T, Avogadro NT), each checked against the state the
    hold-constant controller must reach.
 3. The isotherms the P-against-V view draws, to 17 digits.
 4. The 2-D Maxwell-Boltzmann one-sided flux <vx+> = sqrt(kT2/2 pi m), by
    quadrature and against the closed form, and the identity <vx+> = <v>/pi;
    from it the WALL-HIT RATE that PhET's Collision Counter measures,
    verified three ways: the closed form, a per-particle free-flight argument
    (a disk with speed |vx| in a gap a hits an x-wall at rate |vx|/a), and a
    direct free-flight simulation of 4000 disks.
 5. The contact-density enhancement Z = 1 + B2 n + B3 n^2 for the finite box
    (the contact measure M by quadrature as well as in closed form), which is
    the factor by which collisions raise that hit rate.
 6. PhET's heater as a rate: v -> v (1 + a/800) per 60-fps frame, integrated
    frame by frame and in closed form.
 7. The gauge's noise law and refresh period, and the lid's limits.
"""
import io, math, os
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LINES = []
REFS = {}


def out(label, value, key=None, fmt='%.17g'):
    s = ('%-62s ' + fmt) % (label, value) if not isinstance(value, str) else '%-62s %s' % (label, value)
    print(s)
    OUT_LINES.append(s)
    if key is not None:
        REFS[key] = value


def head(t):
    s = '\n==== ' + t + ' ' + '=' * max(0, 74 - len(t))
    print(s)
    OUT_LINES.append(s)


def check(name, a, b, tol):
    d = abs(a - b) / (abs(b) if b else 1.0)
    out('  check %s' % name, '%.17g vs %.17g  rel %.2e  %s' % (a, b, d, 'OK' if d <= tol else 'FAIL'))
    assert d <= tol, (name, a, b, d)


# ---------------------------------------------------------------------------
head('1. PhET constants, recomputed')
# SI 2019 exact values; u from CODATA 2018.
KB_SI = 1.380649e-23          # J/K, exact by definition
U_SI = 1.66053906660e-27      # kg, CODATA 2018
# 1 pm^2/ps^2 = (1e-12 m)^2 / (1e-12 s)^2 = 1 m^2/s^2, so k/u is already in
# AMU pm^2 ps^-2 K^-1.
K_CODATA = KB_SI / U_SI
K_PHET = 8316.0               # PhET's value (BOLTZMANN, minified build)
out('CODATA k_B/u, AMU pm^2 ps^-2 K^-1', K_CODATA, 'kCodata')
out("PhET's BOLTZMANN", K_PHET, 'kPhET')
out("PhET's k over CODATA, minus one", K_PHET / K_CODATA - 1, 'kRelDiff')
KG_PER_AMU = 1.66e-27         # PhET's value
out("PhET's KG_PER_AMU (rounded u)", KG_PER_AMU, 'kgPerAmu')
out('  … over CODATA u, minus one', KG_PER_AMU / U_SI - 1)
# P in AMU/(pm ps^2) -> Pa: kg/(m s^2) = 1.66e-27/(1e-12 * 1e-24) = 1.66e9 Pa
P_SCALE = KG_PER_AMU / (1e-12 * 1e-24) / 1000.0   # kPa
out('pressure scale, kPa per AMU/(pm ps^2)', P_SCALE, 'pConv')
check('PRESSURE_CONVERSION_SCALE = 1.66e6', P_SCALE, 1.66e6, 1e-15)
ATM_EXACT = 1.0 / 101.325
out('exact atm per kPa (1/101.325)', ATM_EXACT, 'atmPerKpaExact')
out("PhET's ATM_PER_KPA, relative error", 0.00986923 / ATM_EXACT - 1, 'atmRelDiff')

H_BOX, D_BOX = 8750.0, 4000.0
WMIN, WMAX, WDEF = 5000.0, 15000.0, 10000.0
M_HEAVY, R_HEAVY = 28.0, 125.0
M_LIGHT, R_LIGHT = 4.0, 87.5
out('container H x D, pm', '%g x %g' % (H_BOX, D_BOX))
out('width range / default, pm', '%g-%g / %g' % (WMIN, WMAX, WDEF))
out('heavy m, r / light m, r', '%g, %g / %g, %g' % (M_HEAVY, R_HEAVY, M_LIGHT, R_LIGHT))
DT_FRAME = 2.5 / 60.0
out('one 60-fps frame, ps (TimeTransform NORMAL: 1 ps = 0.4 s)', DT_FRAME, 'dtFrame')
out("PhET's step button, ps (MODEL_TIME_STEP)", 0.2, 'stepPs')


# ---------------------------------------------------------------------------
head('2. the gas law in PhET units, and the four named laws')


def volume(w):
    return w * H_BOX * D_BOX


def pressure(N, T, w):
    """P = NkT/V in kPa, PhET's definition."""
    return N * K_PHET * T / volume(w) * P_SCALE


out('V at w = 10 nm, pm^3', volume(WDEF), 'V10')
out('V at w = 10 nm, nm^3', volume(WDEF) / 1e9, 'V10nm')
out('P: 100 disks, 300 K, 10 nm, kPa', pressure(100, 300, WDEF), 'P100kPa')
out('  … in atm', pressure(100, 300, WDEF) * 0.00986923, 'P100atm')
out('P: 200 disks, 300 K, 10 nm, kPa', pressure(200, 300, WDEF), 'P200kPa')
out('P: 100 disks, 600 K, 10 nm, kPa', pressure(100, 600, WDEF), 'P100T600')
out('P: 100 disks, 300 K, 5 nm, kPa', pressure(100, 300, WMIN), 'P100W5')
out('P: 1000 disks, 1000 K, 5 nm, kPa (past the lid limit 20000)',
    pressure(1000, 1000, WMIN), 'PmaxCase')

# The four laws, as the sim sweeps them.  In every case the OTHER quantities
# are held by PhET's controller and the invariant must come back the same.
head('2a. Boyle: hold T, sweep the width')
BOYLE_N, BOYLE_T = 100, 300.0
boyle = [(w, pressure(BOYLE_N, BOYLE_T, w)) for w in (5000.0, 7500.0, 10000.0, 12500.0, 15000.0)]
for w, P in boyle:
    out('  w = %6.0f pm: P' % w, P)
out('Boyle invariant P V (kPa nm^3), 5 widths',
    '%.17g  spread %.3e' % (boyle[0][1] * volume(boyle[0][0]) / 1e9,
                            max(P * volume(w) for w, P in boyle) / min(P * volume(w) for w, P in boyle) - 1))
REFS['boylePV'] = boyle[0][1] * volume(boyle[0][0]) / 1e9
REFS['boyleW'] = [w for w, _ in boyle]
REFS['boyleP'] = [P for _, P in boyle]
check('Boyle: P is exactly proportional to 1/V',
      boyle[0][1] * boyle[0][0], boyle[-1][1] * boyle[-1][0], 1e-15)

head('2b. Charles: hold P, sweep T; the wall walks out')
# At P = 1183.248 kPa and N = 100 the width w = NkT/(P H D) runs over PhET's
# whole 5-15 nm range as T runs over 150-450 K; ask for more and the container
# cannot do it and PhET raises "Volume would be too large/small" (the sim's
# sweep therefore stops at the ends of this range, and says so).
CHARLES_N, CHARLES_P = 100, pressure(100, 300.0, WDEF)
charles = []
for T in (150.0, 225.0, 300.0, 375.0, 450.0):
    w = CHARLES_N * K_PHET * T / (CHARLES_P / P_SCALE) / (H_BOX * D_BOX)
    charles.append((T, w))
    out('  T = %5.0f K: w, pm' % T, w)
REFS['charlesT'] = [T for T, _ in charles]
REFS['charlesW'] = [w for _, w in charles]
out('Charles invariant V/T, nm^3/K', volume(charles[0][1]) / 1e9 / charles[0][0], 'charlesVT')
check('Charles: V/T equal at both ends',
      volume(charles[0][1]) / charles[0][0], volume(charles[-1][1]) / charles[-1][0], 1e-15)
out("PhET rounds the held-P width to 5 decimals (toFixed(5)); at 450 K that is",
    round(charles[-1][1], 5), 'charlesWtopRound')
out('the T that asks for w = WMAX exactly, K',
    CHARLES_P / P_SCALE * volume(WMAX) / (CHARLES_N * K_PHET), 'charlesTmax')
out('the T that asks for w = WMIN exactly, K',
    CHARLES_P / P_SCALE * volume(WMIN) / (CHARLES_N * K_PHET), 'charlesTmin')

head('2c. Gay-Lussac: hold V, sweep T')
gl = [(T, pressure(100, T, WDEF)) for T in (200.0, 300.0, 400.0, 500.0, 600.0)]
for T, P in gl:
    out('  T = %5.0f K: P, kPa' % T, P)
REFS['glT'] = [T for T, _ in gl]
REFS['glP'] = [P for _, P in gl]
out('Gay-Lussac invariant P/T, kPa/K', gl[0][1] / gl[0][0], 'glPT')
check('Gay-Lussac: P/T equal at both ends', gl[0][1] / gl[0][0], gl[-1][1] / gl[-1][0], 1e-15)

head('2d. Avogadro: hold P and V, sweep N; T falls to make room')
AV_P, AV_W = pressure(100, 300.0, WDEF), WDEF
av = []
for N in (50, 100, 150, 200, 250):
    T = (AV_P / P_SCALE) * volume(AV_W) / (N * K_PHET)
    av.append((N, T))
    out('  N = %4d: T, K' % N, T)
REFS['avN'] = [N for N, _ in av]
REFS['avT'] = [T for _, T in av]
out('Avogadro invariant N T, K', av[0][0] * av[0][1], 'avNT')
check('Avogadro: N T equal at both ends', av[0][0] * av[0][1], av[-1][0] * av[-1][1], 1e-15)


# ---------------------------------------------------------------------------
head('3. isotherms for the P-against-V view')
ISO_T = [150.0, 300.0, 600.0, 1000.0]
REFS['isoT'] = ISO_T
iso = []
for T in ISO_T:
    row = [pressure(100, T, w) for w in (WMIN, WDEF, WMAX)]
    iso.append(row)
    out('  T = %6.0f K: P at 5/10/15 nm, kPa' % T, '%.17g  %.17g  %.17g' % tuple(row))
REFS['isoP'] = iso


# ---------------------------------------------------------------------------
head('4. the 2-D Maxwell-Boltzmann flux, and the wall-hit rate')
def kT2(T):
    return 1.5 * K_PHET * T


T0 = 300.0
out('kT2 = (3/2) k T at 300 K, AMU pm^2/ps^2', kT2(T0), 'kT2_300')


def mean_speed_quad(m, kt2):
    f = lambda v: v * (m * v / kt2) * math.exp(-m * v * v / (2 * kt2))
    val, err = integrate.quad(f, 0, np.inf, limit=200)
    return val


def one_sided_quad(m, kt2):
    """<vx+> = int_0^inf vx f(vx) dvx with f the 1-D Gaussian of variance kT2/m."""
    s2 = kt2 / m
    f = lambda vx: vx * math.exp(-vx * vx / (2 * s2)) / math.sqrt(2 * math.pi * s2)
    val, err = integrate.quad(f, 0, np.inf, limit=200)
    return val


for nm, m in (('heavy', M_HEAVY), ('light', M_LIGHT)):
    vbar_c = math.sqrt(math.pi * kT2(T0) / (2 * m))
    vbar_q = mean_speed_quad(m, kT2(T0))
    vx_c = math.sqrt(kT2(T0) / (2 * math.pi * m))
    vx_q = one_sided_quad(m, kT2(T0))
    out('%s <v> closed form, m/s' % nm, vbar_c, 'vMean_' + nm)
    check('%s <v> against quadrature' % nm, vbar_q, vbar_c, 1e-12)
    out('%s <vx+> closed form, m/s' % nm, vx_c, 'vxPlus_' + nm)
    check('%s <vx+> against quadrature' % nm, vx_q, vx_c, 1e-12)
    check('%s <vx+> = <v>/pi exactly' % nm, vx_c * math.pi, vbar_c, 1e-15)
    out('%s rms = PhET injection speed sqrt(3kT/m), m/s' % nm,
        math.sqrt(2 * kT2(T0) / m), 'vRms_' + nm)
out('Graham ratio sqrt(m_heavy/m_light)', math.sqrt(M_HEAVY / M_LIGHT), 'graham')

head('4a. the contact measure and Z (the collisional enhancement)')


def contact_measure(a, b, s):
    """Exact measure of the set of centres within s of the rectangle's edge,
    weighted by the contact perimeter: 2 pi s a b - 4 s^2 (a+b) + 2 s^3."""
    return 2 * math.pi * s * a * b - 4 * s * s * (a + b) + 2 * s ** 3


A_ED, B_ED = WDEF - 2 * R_HEAVY, H_BOX - 2 * R_HEAVY
S_ED = 2 * R_HEAVY
M_closed = contact_measure(A_ED, B_ED, S_ED)
out('contact measure M, closed form (a=9750, b=8500, s=250)', M_closed, 'contactM')

# Term by term, each checked against its own quadrature.  Subtracting the four
# edges' arcs INDEPENDENTLY over-counts where two of them overlap, and they
# overlap exactly on the quarter-disc x^2 + y^2 < s^2 at each corner (the two
# removed arcs are centred a quarter turn apart and have half-widths
# arccos(x/s), arccos(y/s), so they meet when arccos(x/s) + arccos(y/s) > pi/2,
# i.e. x^2 + y^2 < s^2).  That is where the +2 s^3 comes from.
edge_1d, _ = integrate.quad(lambda x: 2 * math.acos(x / S_ED), 0, S_ED, limit=200)
check('one edge: int_0^s 2 arccos(x/s) dx = 2 s', edge_1d, 2 * S_ED, 1e-12)
corner, _ = integrate.dblquad(
    lambda y, x: max(0.0, math.acos(x / S_ED) + math.acos(y / S_ED) - math.pi / 2),
    0, S_ED, 0, S_ED, epsabs=1e-10, epsrel=1e-12)
# the integrand's gradient is square-root singular across the quarter circle
# x^2 + y^2 = s^2, so dblquad reaches ~1e-8 here, not machine precision
check('one corner: the overlap integral = s^2/2 (analytically pi^2/16 + 1/4 twice, '
      'minus pi^2/8)', corner, S_ED ** 2 / 2, 1e-7)
M_terms = 2 * math.pi * S_ED * A_ED * B_ED - S_ED * (2 * edge_1d * B_ED + 2 * edge_1d * A_ED) \
    + 4 * S_ED * corner
check('M rebuilt from the three quadratures', M_terms, M_closed, 1e-11)

# and the whole thing at once, by Monte Carlo over centre AND direction
_rngM = np.random.default_rng(31415)
NMC = 8_000_000
xs = _rngM.uniform(0, A_ED, NMC)
ys = _rngM.uniform(0, B_ED, NMC)
th = _rngM.uniform(0, 2 * math.pi, NMC)
px, py = xs + S_ED * np.cos(th), ys + S_ED * np.sin(th)
frac = np.mean((px >= 0) & (px <= A_ED) & (py >= 0) & (py <= B_ED))
M_mc = 2 * math.pi * S_ED * A_ED * B_ED * frac
out('  Monte Carlo (8e6 samples) of the same measure', M_mc)
check('M against Monte Carlo (1-sigma is 6.6e-5)', M_mc, M_closed, 3e-4)

B2 = math.pi * S_ED ** 2 / 2
B3_RATIO = 4.0 / 3.0 - math.sqrt(3) / math.pi
out('B2 = pi sigma^2/2, pm^2', B2, 'b2')
out('B3/B2^2 for hard disks', B3_RATIO, 'b3ratio')


def hd_z1(N, s, a, b):
    return (N - 1) * s * contact_measure(a, b, s) / (4 * (a * b) ** 2)


def hd_z(N, r, w, h):
    a, b, s = w - 2 * r, h - 2 * r, 2 * r
    z1 = hd_z1(N, s, a, b)
    return 1.0 + z1 * (1.0 + B3_RATIO * (math.pi * s * s / 2) * N / (a * b))


for N in (50, 100, 200):
    z = hd_z(N, R_HEAVY, WDEF, H_BOX)
    eta = N * math.pi * R_HEAVY ** 2 / (WDEF * H_BOX)
    out('Z at N = %3d heavy in the 10 nm box (eta = %.5f)' % (N, eta), z, 'z%d' % N)
check('Z - 1 at N=100 is close to the bulk B2 n = 2 eta',
      hd_z(100, R_HEAVY, WDEF, H_BOX) - 1,
      B2 * 100 / (WDEF * H_BOX) * (1 + B3_RATIO * B2 * 100 / (WDEF * H_BOX)), 0.02)

head('4b. the wall-hit rate PhET s Collision Counter measures')
# The centres of N disks of radius r move in an a x b box, a = W-2r, b = H-2r.
# The one-sided number flux across a wall is n_contact <vx+> per unit length,
# and n_contact = Z n_c with n_c = N/(a b) the mean density of centres, so
#   hits/ps = 2 n_c Z <vx+> (b + a)         (two x-walls and two y-walls,
#                                            <vx+> = <vy+> = <v>/pi).


def hit_rate(N, m, r, w, h, T, use_z=True):
    a, b = w - 2 * r, h - 2 * r
    n_c = N / (a * b)
    vx = math.sqrt(kT2(T) / (2 * math.pi * m))
    z = hd_z(N, r, w, h) if use_z else 1.0
    return 2 * n_c * z * vx * (a + b)


R_ideal = hit_rate(100, M_HEAVY, R_HEAVY, WDEF, H_BOX, T0, use_z=False)
R_with_z = hit_rate(100, M_HEAVY, R_HEAVY, WDEF, H_BOX, T0, use_z=True)
out('100 heavy, 300 K, 10 nm: hits/ps with Z = 1', R_ideal, 'hitRateIdeal')
out('  … with the hard-disk Z', R_with_z, 'hitRateZ')
out('  … over PhET s 10-ps sample period, Z = 1', R_ideal * 10, 'hits10Ideal')
out('  … over 10 ps with Z', R_with_z * 10, 'hits10Z')

# independent form: a free disk with |vx| in a gap a hits an x-wall at |vx|/a
a_, b_ = WDEF - 2 * R_HEAVY, H_BOX - 2 * R_HEAVY
per_particle = 100 * (2 * math.sqrt(kT2(T0) / (2 * math.pi * M_HEAVY))) * (1 / a_ + 1 / b_)
check('hit rate: flux form vs the per-particle free-flight form',
      per_particle, R_ideal, 1e-15)

# and a direct free-flight simulation of the same box
rng = np.random.default_rng(20260921)
NP = 4000
sig = math.sqrt(kT2(T0) / M_HEAVY)
vx = rng.normal(0, sig, NP)
vy = rng.normal(0, sig, NP)
TEND = 400.0
# a point bouncing in [0,a] with speed |vx| crosses a wall every a/|vx|
hits = (np.abs(vx) * TEND / a_).sum() + (np.abs(vy) * TEND / b_).sum()
rate_sim = hits / TEND / NP * 100          # scaled to N = 100
out('free-flight simulation, 4000 disks, 400 ps: hits/ps for N = 100', rate_sim)
check('the simulated free-flight rate (1/sqrt(4000) = 1.6 %)', rate_sim, R_ideal, 0.03)
out('Z raises the rate by, per cent', (R_with_z / R_ideal - 1) * 100)

# the mean free path, so the sim can say how collisional the box is
lam = 1.0 / (math.sqrt(2) * (100 / (WDEF * H_BOX)) * S_ED)
out('mean free path of 100 heavy disks in the 10 nm box, pm', lam, 'mfp100')
out('  … in units of the box width', lam / WDEF)


# ---------------------------------------------------------------------------
head("5. PhET's heater as a rate")
HEAT_COOL = 800.0
step = 1.0 + 1.0 / HEAT_COOL
out('the per-frame speed factor at full heat (a = 1)', step, 'heatStep')
# T ∝ v^2, one factor per 60-fps frame of DT_FRAME ps
n_frames = math.log(1000.0 / 300.0) / (2 * math.log(step))
out('frames from 300 K to 1000 K at full heat', n_frames)
out('  … in ps', n_frames * DT_FRAME, 'heatTime300to1000')
# frame-by-frame, independently
T, f = 300.0, 0
while T < 1000.0:
    T *= step * step
    f += 1
out('  frame-by-frame count (first frame at or past 1000 K)', f)
assert abs(f - math.ceil(n_frames)) <= 1
out('the continuous rate: d lnT/dt, per ps', 2 * math.log(step) / DT_FRAME, 'heatRate')
out('cooling at a = -1: the per-frame factor', 1.0 - 1.0 / HEAT_COOL)
out('  300 K to 100 K, ps', math.log(300.0 / 100.0) / (-2 * math.log(1 - 1 / HEAT_COOL)) * DT_FRAME,
    'coolTime300to100')


# ---------------------------------------------------------------------------
head('6. the gauge, the lid and the limits')
out('gauge refresh period, ps (PressureModel REFRESH_PERIOD)', 0.75, 'pRefresh')
out('maximum pressure before the lid blows, kPa', 2e4, 'pMax')
out('maximum temperature, K', 1e5, 'tMax')
for P in (0.0, 1183.248, 1e4, 2e4):
    out('  noise half-width 50(1 - P/20000) at P = %8.2f kPa' % P, min(50.0, max(0.0, 50 * (1 - P / 2e4))))
REFS['noiseAt0'] = 50.0
REFS['noiseAtP100'] = min(50.0, max(0.0, 50 * (1 - 1183.248 / 2e4)))
out('the noise is scaled to zero below 5 K and full at 50 K: factor at 300 K',
    min(1.0, max(0.0, (300.0 - 5.0) / 45.0)))
out('collision-counter sample periods, ps', '5, 10, 20 (default 10)')
out('lid: thickness / left inset / right inset / blow-off gap, pm', '175 / 1250 / 2000 / 1500')
out('particle entry point, pm', '(-r, H/5) = (-r, %g)' % (H_BOX / 5))
REFS['entryY'] = H_BOX / 5


# ---------------------------------------------------------------------------
head('7. sanity: what one frame of the default box does')
out('a heavy disk at <v> crosses the 10 nm box in, ps', WDEF / 458.18874830809403)
out('frames per ps', 1.0 / DT_FRAME)
out('the pump adds per full stroke', 50)
out('per-species maximum', 1000)

path = os.path.join(HERE, 'refvals.txt')
io.open(path, 'w', encoding='utf-8').write('\n'.join(OUT_LINES) + '\n')


def js(v):
    if isinstance(v, str):
        return '"%s"' % v
    if isinstance(v, (list, tuple)):
        return '[' + ','.join(js(x) for x in v) + ']'
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, int):
        return repr(v)
    return repr(float(v))


lines = ['/* ================================================================== *',
         ' *  reference values — WRITTEN BY derive.py (build/gases-intro);      *',
         ' *  the same numbers are printed in refvals.txt.  Do not edit.        *',
         ' * ================================================================== */',
         'const REF={']
for k in sorted(REFS):
    lines.append('  %s:%s,' % (k, js(REFS[k])))
lines.append('};')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\nwrote refvals.txt (%d lines) and p7a_refs.js (%d refs)' % (len(OUT_LINES), len(REFS)))
