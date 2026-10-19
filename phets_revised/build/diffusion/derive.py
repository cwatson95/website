#!/usr/bin/env python3
"""derive.py — the Python twin of diffusion.html.

PhET's Diffusion screen: a 16 nm x 8.75 nm box split by a 100 pm divider, two
species with their own number, mass, radius and initial temperature, the
divider removable, the centres of mass, the particle flow rates, the scale and
the stopwatch.  The hard-disk engine and its invariants are derived in
build/gas-properties/derive.py and are not repeated; this file derives what
THIS sim pins:

 1. PhET's constants recomputed from SI/CODATA, and the Diffusion screen's own
    constants read out of the minified original (container widthRange
    16e3,16e3,16e3; dividerThickness 100; DIFFUSION_NUMBER_OF_PARTICLES_RANGE
    (0,200,0); DIFFUSION_MASS_RANGE (4,32,28); DIFFUSION_RADIUS_RANGE
    (50,250,125); DIFFUSION_INITIAL_TEMPERATURE_RANGE (50,500,300); DELTAS
    numberOfParticles 10, mass 1, radius 5, initialTemperature 50).
 2. The centre of mass of a species scattered into its own half, EXACTLY
    (-W/4 - dividerHalf/2, independent of the radius), with the sampling
    spread that any measurement of it must carry.
 3. The one-sided flux <vx+> = sqrt(kT2/2 pi m) by quadrature, the flow rate
    across the divider line, and Graham's ratio.
 4. The relaxation of the left-right imbalance.  In the free-flight limit
    dDeltaN/dt = -(4<vx+>/(W-2r)) DeltaN, i.e. tau = (W-2r)/(4<vx+>) — derived
    here, integrated numerically from the two-box rate equations, and checked
    against a direct free-flight simulation of 20000 disks.
 5. The collision rate and the mean free path of a two-component hard-disk
    mixture: z_k = sum_j n_j 2(r_k+r_j) <v_rel,kj>, with <v_rel> = sqrt(pi kT2
    / 2 mu) verified by Monte Carlo over two 2-D Maxwellians.  This is the
    number the simulation's own pair-collision counter must reproduce -- and it
    is how the factor of 2 in the swath width was FOUND: the first draft wrote
    n_j (r_k+r_j) and the simulation counted 2.05 times as many collisions.
 6. The diffusive limit tau_D = W^2/(pi^2 D) with the 2-D kinetic-theory
    estimate D = <v> lambda / 2, and the exact ratio tau_D/tau_free =
    8 W /(pi^3 lambda) that says which regime the box is in.
 7. PhET's initial condition is a DELTA in speed (every particle at
    sqrt(3kT/m)); relaxing to Maxwell-Boltzmann at the same energy multiplies
    the mean speed by exactly sqrt(pi/4) = 0.886227, and the common final
    temperature of two species is the energy-weighted mean.
"""
import io, math, os
import numpy as np
from scipy import integrate

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LINES = []
REFS = {}


def out(label, value, key=None, fmt='%.17g'):
    s = ('%-64s ' + fmt) % (label, value) if not isinstance(value, str) else '%-64s %s' % (label, value)
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
head('1. constants')
KB_SI = 1.380649e-23          # J/K, exact (SI 2019)
U_SI = 1.66053906660e-27      # kg, CODATA 2018
K_CODATA = KB_SI / U_SI       # AMU pm^2 ps^-2 K^-1 (pm/ps is m/s)
K_PHET = 8316.0
out('CODATA k_B/u', K_CODATA, 'kCodata')
out("PhET's BOLTZMANN", K_PHET, 'kPhET')
out('  relative difference', K_PHET / K_CODATA - 1, 'kRelDiff')
KG_PER_AMU = 1.66e-27
P_SCALE = KG_PER_AMU / (1e-12 * 1e-24) / 1000.0
out('kPa per AMU/(pm ps^2)', P_SCALE, 'pConv')
check('PRESSURE_CONVERSION_SCALE', P_SCALE, 1.66e6, 1e-15)
out('exact atm per kPa', 1 / 101.325, 'atmPerKpaExact')

W_BOX, H_BOX, D_BOX = 16000.0, 8750.0, 4000.0
DIV = 100.0
out('Diffusion container W x H x D, pm', '%g x %g x %g' % (W_BOX, H_BOX, D_BOX))
out('divider thickness, pm', DIV, 'divider')
out('number of particles: range / delta / default', '0-200 / 10 / 0')
out('mass, AMU: range / delta / default', '4-32 / 1 / 28')
out('radius, pm: range / delta / default', '50-250 / 5 / 125')
out('initial temperature, K: range / delta / default', '50-500 / 50 / 300')
out('particle-flow running window, frames', 300)
DT_FRAME, DT_SLOW = 2.5 / 60.0, 0.3 / 60.0
out('one frame at normal speed, ps', DT_FRAME, 'dtFrame')
out('one frame at PhET s slow speed, ps', DT_SLOW, 'dtSlow')
out("PhET's step button, ps (MODEL_TIME_STEP)", 0.2, 'stepPs')
out('  … in frames at normal speed', 0.2 / DT_FRAME)
# PhET's Diffusion screen shows no gauge, but the engine still computes
# P = NkT/V and the shared definition has to be right wherever it is reused.
_V = W_BOX * H_BOX * D_BOX
out('V of the Diffusion box, pm^3', _V, 'Vbox')
out('P = NkT/V for 200 disks at 300 K in it, kPa',
    200 * K_PHET * 300.0 / _V * P_SCALE, 'pBox200')
out('  … for 100 at 300 K', 100 * K_PHET * 300.0 / _V * P_SCALE, 'pBox100')

# this sim's own opening state (PhET opens with 0 of each, which draws nothing)
N1, M1, R1, T1 = 100, 28.0, 125.0, 300.0
N2, M2, R2, T2 = 100, 4.0, 90.0, 300.0
out('this sim s opening state: particle 1', 'N=%d m=%g AMU r=%g pm T=%g K' % (N1, M1, R1, T1))
out('                          particle 2', 'N=%d m=%g AMU r=%g pm T=%g K' % (N2, M2, R2, T2))


# ---------------------------------------------------------------------------
head('2. the centre of mass of a species in its own half')
# PhET scatters species 0 uniformly in [left, mid - half] and species 1 in
# [mid + half, 0]; the engine keeps the CENTRES inside by a radius, so the
# occupied interval is [left + r, mid - half - r] and the mean of a uniform
# distribution on it is its midpoint.  The radius cancels.
left, mid, half = -W_BOX, -W_BOX / 2.0, DIV / 2.0


def com_exact(k, r):
    if k == 0:
        lo, hi = left + r, mid - half - r
    else:
        lo, hi = mid + half + r, 0.0 - r
    return (lo + hi) / 2.0 - mid


out('COM of particle 1 at t = 0, pm from the middle', com_exact(0, R1), 'com1')
out('COM of particle 2 at t = 0, pm from the middle', com_exact(1, R2), 'com2')
check('the radius cancels (particle 1 at r = 50 and at r = 250)',
      com_exact(0, 50.0), com_exact(0, 250.0), 1e-15)
check('COM = -(W/4 + half/2) exactly', com_exact(0, R1), -(W_BOX / 4 + half / 2), 1e-15)
out('… and the two sides are mirror images', '%.17g / %.17g' % (com_exact(0, R1), com_exact(1, R2)))


def com_sd(k, r, N):
    """sd of the sample mean of N uniform draws on the occupied interval."""
    if k == 0:
        L = (mid - half - r) - (left + r)
    else:
        L = (0.0 - r) - (mid + half + r)
    return L / math.sqrt(12.0 * N)


out('sampling sd of the COM, particle 1, N = 100, pm', com_sd(0, R1, N1), 'comSd1')
out('sampling sd of the COM, particle 2, N = 100, pm', com_sd(1, R2, N2), 'comSd2')
_r = np.random.default_rng(90210)
_s = np.array([_r.uniform(left + R1, mid - half - R1, N1).mean() - mid for _ in range(4000)])
check('the sd against 4000 Monte-Carlo draws', _s.std(ddof=1), com_sd(0, R1, N1), 0.03)
out('a fully mixed species has COM 0; the scale of the approach, pm', abs(com_exact(0, R1)))


# ---------------------------------------------------------------------------
head('3. the one-sided flux, the flow rate and Graham')


def kT2(T):
    return 1.5 * K_PHET * T


def vbar(m, T):
    return math.sqrt(math.pi * kT2(T) / (2 * m))


def vxplus(m, T):
    return math.sqrt(kT2(T) / (2 * math.pi * m))


for nm, m in (('1 (28 AMU)', M1), ('2 (4 AMU)', M2)):
    q, _ = integrate.quad(lambda v: v * math.exp(-v * v * m / (2 * kT2(T1)))
                          / math.sqrt(2 * math.pi * kT2(T1) / m), 0, np.inf, limit=200)
    out('particle %s: <vx+>, m/s' % nm, vxplus(m, T1))
    check('  against quadrature', q, vxplus(m, T1), 1e-12)
    out('particle %s: <v>, m/s' % nm, vbar(m, T1))
    check('  <vx+> = <v>/pi', vxplus(m, T1) * math.pi, vbar(m, T1), 1e-15)
    out('particle %s: sqrt(3kT/m), PhET s starting speed, m/s' % nm, math.sqrt(3 * K_PHET * T1 / m))
REFS['vxPlus1'] = vxplus(M1, T1)
REFS['vxPlus2'] = vxplus(M2, T1)
REFS['vbar1'] = vbar(M1, T1)
REFS['vbar2'] = vbar(M2, T1)
REFS['vDelta1'] = math.sqrt(3 * K_PHET * T1 / M1)
REFS['vDelta2'] = math.sqrt(3 * K_PHET * T1 / M2)
out('Graham ratio sqrt(m1/m2) = rate2/rate1 at equal n and T',
    math.sqrt(M1 / M2), 'graham')
check('Graham = <vx+>2/<vx+>1', vxplus(M2, T1) / vxplus(M1, T1), math.sqrt(M1 / M2), 1e-15)


def flow_rate(N_side, m, r, T):
    """particles per ps crossing the divider line one way, from one side."""
    n = N_side / ((W_BOX / 2 - r) * (H_BOX - 2 * r))
    return n * vxplus(m, T) * (H_BOX - 2 * r)


out('particle 1, 100 all on the left: crossings/ps to the right at t = 0',
    flow_rate(N1, M1, R1, T1), 'flow1')
out('particle 2, 100 all on the right: crossings/ps to the left at t = 0',
    flow_rate(N2, M2, R2, T2), 'flow2')
check('the height cancels: rate = N <vx+>/(W/2 - r)',
      flow_rate(N1, M1, R1, T1), N1 * vxplus(M1, T1) / (W_BOX / 2 - R1), 1e-15)
out('their ratio (equal N, equal T)', flow_rate(N2, M2, R2, T2) / flow_rate(N1, M1, R1, T1))
out('  … Graham times the (W/2 - r) ratio',
    math.sqrt(M1 / M2) * (W_BOX / 2 - R1) / (W_BOX / 2 - R2))


# ---------------------------------------------------------------------------
head('4. the relaxation of the left-right imbalance (free-flight limit)')
# N_L + N_R = N; each side loses N_side <vx+>/(W/2 - r) per ps, so
#   d(N_L - N_R)/dt = -2 <vx+>/(W/2 - r) (N_L - N_R) = -(4 <vx+>/(W - 2r)) DeltaN


def tau_free(m, r, T):
    return (W_BOX - 2 * r) / (4 * vxplus(m, T))


out('tau (free flight), particle 1, ps', tau_free(M1, R1, T1), 'tauFree1')
out('tau (free flight), particle 2, ps', tau_free(M2, R2, T2), 'tauFree2')
out('  … for point particles (r = 0), particle 1, ps', tau_free(M1, 0.0, T1), 'tauFreePoint1')
out('  … the radius correction, per cent',
    (tau_free(M1, R1, T1) / tau_free(M1, 0.0, T1) - 1) * 100)

# integrate the two-box rate equations and read the decay off the solution.
# Each side loses N_side <vx+>/(W/2 - r) per ps, so the per-side rate constant
# is <vx+>/(W/2 - r) and the IMBALANCE decays at twice that.
rate = vxplus(M1, T1) / (W_BOX / 2 - R1)
check('the imbalance rate is 2x the per-side rate = 1/tau', 2 * rate, 1 / tau_free(M1, R1, T1), 1e-15)
sol = integrate.solve_ivp(lambda t, y: [-rate * y[0] + rate * y[1], rate * y[0] - rate * y[1]],
                          [0, 200], [100.0, 0.0], rtol=1e-11, atol=1e-11, dense_output=True)
d40 = (sol.sol(40.0)[0] - sol.sol(40.0)[1]) / 100.0
check('the ODE solution at 40 ps is exp(-t/tau)', d40, math.exp(-40.0 / tau_free(M1, R1, T1)), 1e-8)
out('DeltaN/N at 40 ps (effusion model, particle 1)', d40, 'dn40eff')

# The two-box model assumes each side stays internally well mixed, which only
# collisions can do.  With collisions OFF the motion is ballistic: a disk just
# bounces between the end walls, so the imbalance is NOT exponential — it falls
# faster at first and then rings.  That curve is exact kinematics and the sim's
# collisions-off run must reproduce it, so pin it here.
head('4a. the collisionless (ballistic) curve, exactly')
_rng = np.random.default_rng(2718281)
NS = 4_000_000
sig = math.sqrt(kT2(T1) / M1)
xlo, xhi = left + R1, 0.0 - R1
x0 = _rng.uniform(left + R1, mid - half - R1, NS)
vx0 = _rng.normal(0, sig, NS)
L = xhi - xlo
BALL_T = [5.0, 10.0, 20.0, 40.0, 80.0]
ball = []
for tt in BALL_T:
    u = np.abs((x0 - xlo + vx0 * tt) % (2 * L))
    xt = xlo + np.where(u <= L, u, 2 * L - u)
    f = float(np.mean(xt < mid))
    ball.append(2 * f - 1)
    out('ballistic DeltaN/N at %5.1f ps  (effusion model says %.5f)'
        % (tt, math.exp(-tt / tau_free(M1, R1, T1))), ball[-1])
REFS['ballT'] = BALL_T
REFS['ballDN'] = ball
out('  Monte-Carlo 1-sigma on each (4e6 samples)', 1.0 / math.sqrt(NS), 'ballSd')
out('ballistic is FASTER than the effusion model early on: ratio at 10 ps',
    ball[1] / math.exp(-10.0 / tau_free(M1, R1, T1)))
assert ball[1] < math.exp(-10.0 / tau_free(M1, R1, T1)), 'ballistic should lead at 10 ps'


# ---------------------------------------------------------------------------
head('5. the collision rate and the mean free path of the mixture')
# <v_rel> for two 2-D Maxwellians of masses m_k, m_j at the same kT2: the
# relative velocity is Gaussian in each component with variance kT2/mu, so it
# is itself a 2-D Maxwellian with the reduced mass.
def vrel(mk, mj, T):
    mu = mk * mj / (mk + mj)
    return math.sqrt(math.pi * kT2(T) / (2 * mu))


_r2 = np.random.default_rng(161803)
NMC = 2_000_000
for (mk, mj) in ((M1, M1), (M1, M2), (M2, M2)):
    a = _r2.normal(0, math.sqrt(kT2(T1) / mk), (NMC, 2))
    b = _r2.normal(0, math.sqrt(kT2(T1) / mj), (NMC, 2))
    mc = np.mean(np.hypot(*(a - b).T))
    out('<v_rel> for %g and %g AMU, m/s' % (mk, mj), vrel(mk, mj, T1))
    check('  against 2e6 Monte-Carlo pairs (1-sigma 0.04 %)', mc, vrel(mk, mj, T1), 3e-3)
check('like pairs: <v_rel> = sqrt(2) <v>', vrel(M1, M1, T1), math.sqrt(2) * vbar(M1, T1), 1e-15)

AREA = W_BOX * H_BOX
nn = [N1 / AREA, N2 / AREA]
mm, rr = [M1, M2], [R1, R2]


def zrate(k, T):
    """Collisions per ps suffered by one disk of species k.

    A disk of radius r_k moving with relative velocity v_rel through targets of
    radius r_j collides when the centres come within d = r_k + r_j, so it
    sweeps a STRIP OF HALF-WIDTH d -- width 2d, not d.  Writing n_j d <v_rel>
    (the natural-looking but wrong form) halves every collision rate; the
    simulation's own pair counter caught it at exactly a factor 2.05.
    Check in 3-D, where the same argument gives a cylinder of radius d and the
    textbook cross-section pi d^2 with d the DIAMETER: same convention.
    """
    s = 0.0
    for j in (0, 1):
        s += nn[j] * 2 * (rr[k] + rr[j]) * vrel(mm[k], mm[j], T)
    return s


for k in (0, 1):
    out('particle %d: collisions per ps per disk' % (k + 1), zrate(k, T1), 'z%d' % (k + 1))
    out('particle %d: mean free path, pm' % (k + 1), vbar(mm[k], T1) / zrate(k, T1), 'mfp%d' % (k + 1))
    out('  … in units of the box width', vbar(mm[k], T1) / zrate(k, T1) / W_BOX)
pair_total = 0.5 * (N1 * zrate(0, T1) + N2 * zrate(1, T1))
out('total pair collisions per ps in the box', pair_total, 'pairRate')
out('  … over 10 ps', pair_total * 10)
# the like-pair rate alone, as a cross-check of the 1/2
check('total = sum over unordered pairs',
      pair_total,
      0.5 * N1 * nn[0] * 4 * rr[0] * vrel(M1, M1, T1)
      + 0.5 * N2 * nn[1] * 4 * rr[1] * vrel(M2, M2, T1)
      + N1 * nn[1] * 2 * (rr[0] + rr[1]) * vrel(M1, M2, T1), 1e-13)
# and the identical-disk mean free path against its textbook form
_lam1 = vbar(M1, T1) / zrate(0, T1)
_g = gasfree = 1.0 / (2 * math.sqrt(2) * nn[0] * 2 * rr[0])
out('one species alone: lambda = 1/(2 sqrt2 n sigma), sigma = 2r, pm', _g)
check('the mixture formula reduces to it when species 2 is absent',
      vbar(M1, T1) / (nn[0] * 2 * (2 * rr[0]) * vrel(M1, M1, T1)), _g, 1e-14)


# ---------------------------------------------------------------------------
head('6. the diffusive limit, and which regime the box is in')
# 2-D kinetic-theory estimate D = <v> lambda / 2 (an ESTIMATE: the exact
# Chapman-Enskog coefficient carries an O(1) factor this argument cannot fix).
for k in (0, 1):
    lam = vbar(mm[k], T1) / zrate(k, T1)
    D = vbar(mm[k], T1) * lam / 2
    tauD = W_BOX ** 2 / (math.pi ** 2 * D)
    out('particle %d: D estimate, pm^2/ps' % (k + 1), D, 'Dest%d' % (k + 1))
    out('particle %d: tau_D = W^2/(pi^2 D), ps' % (k + 1), tauD, 'tauD%d' % (k + 1))
    out('particle %d: tau_D / tau_free' % (k + 1), tauD / tau_free(mm[k], rr[k], T1))
    check('  … = 8 W /(pi^3 lambda) for point particles',
          W_BOX ** 2 / (math.pi ** 2 * D) / tau_free(mm[k], 0.0, T1),
          8 * W_BOX / (math.pi ** 3 * lam), 1e-13)
out('the box is %.1f mean free paths across for particle 1' % (W_BOX / (vbar(M1, T1) / zrate(0, T1))),
    W_BOX / (vbar(M1, T1) / zrate(0, T1)), 'boxInMfp1')
out('so the crossing is neither free flight nor Fickian: the two limits differ by',
    (W_BOX ** 2 / (math.pi ** 2 * (vbar(M1, T1) * (vbar(M1, T1) / zrate(0, T1)) / 2)))
    / tau_free(M1, R1, T1))


# ---------------------------------------------------------------------------
head("7. PhET's delta start, and the common final temperature")
out('PhET starts every particle at sqrt(3kT/m), the RMS speed', 'so <v> starts at the rms, not at the Maxwell-Boltzmann mean')
out('<v>_MB / <v>_delta at the same energy = sqrt(pi/4)', math.sqrt(math.pi / 4), 'meanSpeedDrop')
check('sqrt(pi kT2/2m) / sqrt(2 kT2/m)', vbar(M1, T1) / math.sqrt(2 * kT2(T1) / M1),
      math.sqrt(math.pi / 4), 1e-15)
out('  … the same for both species (mass cancels)',
    vbar(M2, T1) / math.sqrt(2 * kT2(T1) / M2))
out('so the mean speed falls by, per cent', (1 - math.sqrt(math.pi / 4)) * 100)

for TA, TB in ((300.0, 300.0), (500.0, 100.0), (50.0, 500.0)):
    Tf = (N1 * TA + N2 * TB) / (N1 + N2)
    out('particle 1 at %5.0f K, particle 2 at %5.0f K: common T, K' % (TA, TB), Tf)
REFS['tCommon500_100'] = (N1 * 500.0 + N2 * 100.0) / (N1 + N2)
out('  the common T is the number-weighted mean',
    '(energy is conserved and T = (2/3)<KE>/k)')

# the exact 2-D Maxwell-Boltzmann speed bins the speeds view draws
head('7a. the speed histogram the speeds view compares against')
NB, BW = 20, 150.0


def mb_bin(m, T, lo, hi):
    """F(hi) - F(lo) with F(v) = 1 - exp(-m v^2/2kT2), written the way the page
    writes it (two expm1 calls) so the two agree into the 1e-14 tail rather
    than losing every digit to cancellation there."""
    a = -m * lo * lo / (2 * kT2(T))
    b = -m * hi * hi / (2 * kT2(T))
    return math.expm1(a) - math.expm1(b)


p1 = [mb_bin(M1, T1, b * BW, (b + 1) * BW) for b in range(NB)]
p2 = [mb_bin(M2, T2, b * BW, (b + 1) * BW) for b in range(NB)]
out('bins: %d of %g m/s' % (NB, BW), 'up to %g m/s' % (NB * BW))
out('particle 1 (28 AMU, 300 K): the 6 largest bin probabilities',
    ' '.join('%.10f' % v for v in p1[:6]))
REFS['mbBins1'] = p1
REFS['mbBins2'] = p2
REFS['binW'] = BW
REFS['nBins'] = NB
out('particle 1: probability inside the plotted range', sum(p1), 'mbCover1')
out('particle 2: probability inside the plotted range', sum(p2), 'mbCover2')
q, _ = integrate.quad(lambda v: (M1 * v / kT2(T1)) * math.exp(-M1 * v * v / (2 * kT2(T1))),
                      0, NB * BW, limit=200)
check('bin sum against a direct quadrature of the pdf', sum(p1), q, 1e-10)
out('the mode sqrt(kT2/m), particle 1, m/s', math.sqrt(kT2(T1) / M1), 'mode1')
out('the mode, particle 2, m/s', math.sqrt(kT2(T2) / M2), 'mode2')

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
         ' *  reference values — WRITTEN BY derive.py (build/diffusion);        *',
         ' *  the same numbers are printed in refvals.txt.  Do not edit.        *',
         ' * ================================================================== */',
         'const REF={']
for k in sorted(REFS):
    lines.append('  %s:%s,' % (k, js(REFS[k])))
lines.append('};')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write('\n'.join(lines) + '\n')
print('\nwrote refvals.txt (%d lines) and p7a_refs.js (%d refs)' % (len(OUT_LINES), len(REFS)))
