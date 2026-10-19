#!/usr/bin/env python3
"""derive.py — the Python twin of gas-properties.html.

Everything the page's selfTest pins is re-derived here, independently of the
JavaScript, and printed (refvals.txt holds the output, read in full).  The
file also writes p7a_refs.js, the same numbers as a JS object, so no pinned
value is ever retyped by hand.

What is re-derived, and how
---------------------------
 1. PhET's constants and unit conversions (read out of the minified original,
    docs/phets/gas-properties_en.html, cited "PhET's value"), against CODATA.
 2. The collision-time algebra, in EXACT rational arithmetic (fractions):
    the contact time of two disks is the smaller root of a quadratic, the
    elastic impulse conserves momentum and energy exactly, the moving wall's
    reflection 2u - v and its work 2mu(u - v), PhET's rule u - v and its
    work mu(u/2 - v).  No sympy on this machine; exact rationals are the
    stronger check anyway (every identity is tested with == on Fractions).
 3. A brute-force, O(N^2), exactly-ordered event-driven molecular dynamics
    (no grid, no substeps: an independent algorithm from the JS engine's) for
    small configurations in PhET's box: final positions, velocities, event
    counts, the work done by a moving wall and the virial ledger.
 4. mulberry32 and Box-Muller, bit-for-bit, so PhET's injection (Gaussian
    temperatures with the mean restored, a pi/2 fan pointing left) can be
    pinned value by value.
 5. The 2-D Maxwell-Boltzmann laws in PhET's units (kT2 = (3/2) k T: PhET
    applies the 3-D equipartition to 2-D motion), PhET's histogram bins, the
    mean speed; the finite-N microcanonical laws (Dirichlet), and the exact
    sampling moments used as the selfTest's tolerances; the chi-square
    statistic's sampling distribution by Monte Carlo over the exact ensemble.
 6. Hard disks: B2 = pi s^2/2, B3 = (4/3 - sqrt3/pi) B2^2 checked by
    quadrature of the three-disk Mayer integral; the finite-rectangle contact
    measure M = 2 pi s a b - 4 s^2 (a + b) + 2 s^3 checked by quadrature; the
    low-density collisional virial it implies.
 7. PhET's heater rate, the 2-D adiabat T A = const (gamma = 2) and PhET's
    rule's T A^(1/2) = const, the effusion flux and Graham's ratio.
"""
import io, math, os, sys
from fractions import Fraction as Fr
import numpy as np
from scipy import integrate, special, stats

HERE = os.path.dirname(os.path.abspath(__file__))
OUT_LINES = []
REFS = {}


def out(label, value, key=None, fmt='%.17g'):
    s = ('%-58s ' + fmt) % (label, value) if not isinstance(value, str) else '%-58s %s' % (label, value)
    print(s)
    OUT_LINES.append(s)
    if key is not None:
        REFS[key] = value


def head(t):
    s = '\n==== ' + t + ' ' + '=' * max(0, 70 - len(t))
    print(s)
    OUT_LINES.append(s)


# ---------------------------------------------------------------------------
head('1. PhET constants (read from docs/phets/gas-properties_en.html)')
K_PHET = 8316.0            # BOLTZMANN, AMU pm^2 / (ps^2 K)
KG_PER_AMU = 1.66e-27      # KG_PER_AMU
ATM_PER_KPA = 0.00986923   # ATM_PER_KPA
P_SCALE = 1.66e6           # PRESSURE_CONVERSION_SCALE, kPa per AMU/(pm ps^2)
HEIGHT, DEPTH, WALL = 8750.0, 4000.0, 75.0
HEAVY = (28.0, 125.0)
LIGHT = (4.0, 87.5)
out('PhET k (AMU pm^2 ps^-2 K^-1)', K_PHET, 'kPhET')
# CODATA 2018/2022 exact k_B and the 2022 atomic mass constant
kB = 1.380649e-23
u_amu = 1.66053906892e-27
k_codata = kB / u_amu            # (kg m^2 s^-2 K^-1)/kg -> m^2 s^-2 K^-1 = pm^2 ps^-2 K^-1 per AMU
out('CODATA k in these units (k_B / u)', k_codata, 'kCodata')
out('PhET k / CODATA k - 1', K_PHET / k_codata - 1, 'kRelDiff')
out('k_B / PhET KG_PER_AMU (what 1.66e-27 would give)', kB / KG_PER_AMU, 'kFromPhetAmu')
# pressure conversion: 1 AMU/(pm ps^2) = KG_PER_AMU kg / (1e-12 m * 1e-24 s^2) Pa
pconv = KG_PER_AMU / (1e-12 * 1e-24) / 1e3
out('1 AMU/(pm ps^2) in kPa (from KG_PER_AMU)', pconv, 'pConv')
out('PhET PRESSURE_CONVERSION_SCALE / that', P_SCALE / pconv, 'pConvRatio')
out('exact atm per kPa (1/101.325)', 1 / 101.325, 'atmPerKpaExact')
out('PhET ATM_PER_KPA / exact - 1', ATM_PER_KPA * 101.325 - 1, 'atmRelDiff')
# PhET's default state: 100 heavy at 300 K in the 10 nm box
V0 = 10000.0 * HEIGHT * DEPTH
P100 = 100 * K_PHET * 300 / V0 * P_SCALE
out('P for N=100, T=300 K, W=10000 pm (kPa)', P100, 'P100kPa')
out('  ... in atm', P100 * ATM_PER_KPA, 'P100atm')
Pmax_N = 1000 * K_PHET * 1000 / (5000 * HEIGHT * DEPTH) * P_SCALE
out('P for N=1000, T=1000 K, W=5000 (kPa) > 2e4 blows the lid', Pmax_N, 'PmaxCase')
# speeds: 1 pm/ps = 1 m/s exactly
kT2_300 = 1.5 * K_PHET * 300
out('kT2 = (3/2) k T at 300 K (AMU pm^2/ps^2)', kT2_300, 'kT2_300')
for nm, (m, r) in (('heavy', HEAVY), ('light', LIGHT)):
    out('%s injection speed sqrt(3kT/m) at 300 K (pm/ps)' % nm, math.sqrt(3 * K_PHET * 300 / m), 'vInj_' + nm)
    out('%s mean speed sqrt(pi kT2/(2m)) at 300 K' % nm, math.sqrt(math.pi * kT2_300 / (2 * m)), 'vMean_' + nm)
    out('%s most probable speed sqrt(kT2/m) at 300 K' % nm, math.sqrt(kT2_300 / m), 'vMode_' + nm)
out('KE of one AMU pm^2/ps^2 in zJ (PhET KG_PER_AMU)', KG_PER_AMU * 1e21, 'zJperUnit')

# ---------------------------------------------------------------------------
head('2. collision-time algebra, in exact rational arithmetic')
# (a) the contact time.  Two disks, centres p_i, p_j, velocities v_i, v_j,
# sum of radii s.  |dp + t dv|^2 = s^2  ->  a t^2 + 2 b t + c = 0 with
# a = dv.dv, b = dp.dv, c = dp.dp - s^2.  Approaching (b < 0) and apart
# (c > 0): the earlier root t = (-b - sqrt(b^2 - a c))/a, written stably as
# t = c / (-b + sqrt(b^2 - a c)) (the product of the roots is c/a).
# Pick rationals with a perfect-square discriminant so t is rational:
dp = (Fr(-900), Fr(-300))           # p_i - p_j
dv = (Fr(300), Fr(40))              # v_i - v_j  (approaching: b < 0)
s = Fr(250)
a = dv[0] ** 2 + dv[1] ** 2
b = dp[0] * dv[0] + dp[1] * dv[1]
c = dp[0] ** 2 + dp[1] ** 2 - s * s
disc = b * b - a * c
root = Fr(math.isqrt(disc.numerator), math.isqrt(disc.denominator))
assert root * root == disc, 'choose a perfect square'
t1 = (-b - root) / a
t2 = c / (-b + root)
assert t1 == t2
contact = (dp[0] + t1 * dv[0], dp[1] + t1 * dv[1])
assert contact[0] ** 2 + contact[1] ** 2 == s * s        # exactly at contact
out('exact contact time (rational)', float(t1), 'tContactExact')
out('  numerator/denominator', '%d/%d' % (t1.numerator, t1.denominator))
# (b) the elastic impulse along the line of centres
mi, mj = Fr(28), Fr(4)
vi, vj = (Fr(250), Fr(40)), (Fr(-50), Fr(0))           # dv = (300, 40) as above
n_ = (contact[0] / s, contact[1] / s)                    # unit normal (exact: |contact| = s)
g = (vi[0] - vj[0]) * n_[0] + (vi[1] - vj[1]) * n_[1]    # normal relative speed (< 0)
vi2 = (vi[0] - 2 * mj / (mi + mj) * g * n_[0], vi[1] - 2 * mj / (mi + mj) * g * n_[1])
vj2 = (vj[0] + 2 * mi / (mi + mj) * g * n_[0], vj[1] + 2 * mi / (mi + mj) * g * n_[1])
P0 = (mi * vi[0] + mj * vj[0], mi * vi[1] + mj * vj[1])
P1 = (mi * vi2[0] + mj * vj2[0], mi * vi2[1] + mj * vj2[1])
E0 = (mi * (vi[0] ** 2 + vi[1] ** 2) + mj * (vj[0] ** 2 + vj[1] ** 2)) / 2
E1 = (mi * (vi2[0] ** 2 + vi2[1] ** 2) + mj * (vj2[0] ** 2 + vj2[1] ** 2)) / 2
assert P0 == P1 and E0 == E1, 'elastic impulse conserves momentum and energy exactly'
g2 = (vi2[0] - vj2[0]) * n_[0] + (vi2[1] - vj2[1]) * n_[1]
assert g2 == -g, 'the normal relative velocity reverses exactly'
t_i = ((vi2[0] - vj2[0]) * (-n_[1]) + (vi2[1] - vj2[1]) * n_[0])
t_0 = ((vi[0] - vj[0]) * (-n_[1]) + (vi[1] - vj[1]) * n_[0])
assert t_i == t_0, 'the tangential relative velocity is unchanged'
out('exact post-collision vi', '(%s, %s)' % (vi2[0], vi2[1]))
out('exact post-collision vj', '(%s, %s)' % (vj2[0], vj2[1]))
REFS['pair1'] = dict(mi=28, mj=4, ri=125, rj=125, pi=[-900.0, -300.0], pj=[0.0, 0.0],
                     vi=[250.0, 40.0], vj=[-50.0, 0.0], t=float(t1),
                     vi2=[float(vi2[0]), float(vi2[1])], vj2=[float(vj2[0]), float(vj2[1])])
out('pair1 vi2x (float of the exact rational)', float(vi2[0]))
out('pair1 vi2y', float(vi2[1]))
out('pair1 vj2x', float(vj2[0]))
out('pair1 vj2y', float(vj2[1]))
# (c) the moving wall.  Left wall at x_w(t) = x_w0 + u t, particle at x0 with
# vx, radius r: contact when x0 + vx t - r = x_w0 + u t, t = (x_w0 + r - x0)/(vx - u),
# needs vx < u.  Elastic (the wall is infinitely heavy): in the wall's frame
# vx - u -> -(vx - u), so vx' = 2u - vx; the work is m/2 (vx'^2 - vx^2) = 2 m u (u - vx).
m, r, x0, vx, xw0, u = Fr(28), Fr(125), Fr(-9000), Fr(-400), Fr(-10000), Fr(150)
tc = (xw0 + r - x0) / (vx - u)
assert x0 + vx * tc - r == xw0 + u * tc
vx2 = 2 * u - vx
work = m * (vx2 ** 2 - vx ** 2) / 2
assert work == 2 * m * u * (u - vx)
out('moving wall: contact time (rational)', float(tc), 'wallTc')
out('moving wall: vx after (2u - vx)', float(vx2), 'wallVx2')
out('moving wall: work 2 m u (u - vx)', float(work), 'wallWork')
# PhET's rule, -(vx - u) = u - vx: in the wall's frame the particle leaves
# at -vx, not -(vx - u); the work is m/2 ((u - vx)^2 - vx^2) = m u (u/2 - vx)
vxp = u - vx
workp = m * (vxp ** 2 - vx ** 2) / 2
assert workp == m * u * (u / 2 - vx)
out('PhET rule: vx after (u - vx)', float(vxp), 'phetVx2')
out('PhET rule: work m u (u/2 - vx)', float(workp), 'phetWork')
out('PhET work / elastic work (first order in u -> 1/2)', float(workp / work), 'phetWorkRatio')
# ratio to first order: (mu(-vx))/(2mu(-vx)) = 1/2 exactly as u -> 0
for uu in (Fr(1), Fr(1, 100), Fr(1, 10000)):
    wr = (m * uu * (uu / 2 - vx)) / (2 * m * uu * (uu - vx))
    out('  ratio at u = %s' % uu, float(wr))

# ---------------------------------------------------------------------------
head('3. brute-force event-driven reference runs (O(N^2), exact ordering)')


def ed_run(parts, left0, H, T_end, u=0.0, t_stop=0.0, collisions=True):
    """parts: [m, r, x, y, vx, vy].  Box x in [left(t), 0], y in [0, H], the
    left wall at left0 + u*min(t, t_stop).  Returns the final state and the
    ledgers.  Every event is found by scanning all pairs and all walls."""
    P = [list(p) for p in parts]
    n = len(P)
    t = 0.0
    st = dict(pair=0, wall=0, work=0.0, kin=0.0, vir_wall=0.0, vir_pair=0.0)
    G0 = sum(p[0] * (p[2] * p[4] + p[3] * p[5]) for p in P)

    def lwall(tt):
        return left0 + u * min(tt, t_stop)
    while True:
        u_now = u if t < t_stop else 0.0
        best = [T_end - t, 'end', -1, -1]
        if t < t_stop and t_stop - t < best[0]:
            best = [t_stop - t, 'stop', -1, -1]
        xw = lwall(t)
        for i in range(n):
            m, r, x, y, vx, vy = P[i]
            # left wall (moving with u_now)
            if vx < u_now:
                tt = (xw + r - x) / (vx - u_now)
                if tt >= 0 and tt < best[0]:
                    best = [tt, 'L', i, -1]
            if vx > 0:
                tt = (-r - x) / vx
                if tt >= 0 and tt < best[0]:
                    best = [tt, 'R', i, -1]
            if vy < 0:
                tt = (r - y) / vy
                if tt >= 0 and tt < best[0]:
                    best = [tt, 'B', i, -1]
            if vy > 0:
                tt = (H - r - y) / vy
                if tt >= 0 and tt < best[0]:
                    best = [tt, 'T', i, -1]
        if collisions:
            for i in range(n):
                for j in range(i + 1, n):
                    dx, dy = P[i][2] - P[j][2], P[i][3] - P[j][3]
                    dvx, dvy = P[i][4] - P[j][4], P[i][5] - P[j][5]
                    s = P[i][1] + P[j][1]
                    c = dx * dx + dy * dy - s * s
                    b = dx * dvx + dy * dvy
                    if c < 0 or b >= 0:
                        continue
                    a = dvx * dvx + dvy * dvy
                    d = b * b - a * c
                    if d < 0:
                        continue
                    tt = c / (-b + math.sqrt(d))
                    if tt < best[0]:
                        best = [tt, 'P', i, j]
        dt, kind, i, j = best
        KE = sum(0.5 * p[0] * (p[4] ** 2 + p[5] ** 2) for p in P)
        st['kin'] += 2 * KE * dt
        for p in P:
            p[2] += p[4] * dt
            p[3] += p[5] * dt
        t += dt
        if kind == 'end':
            break
        if kind == 'stop':
            t = t_stop
            continue
        if kind == 'P':
            pi, pj = P[i], P[j]
            dx, dy = pi[2] - pj[2], pi[3] - pj[3]
            dd = math.sqrt(dx * dx + dy * dy)
            nx, ny = dx / dd, dy / dd
            gg = (pi[4] - pj[4]) * nx + (pi[5] - pj[5]) * ny
            M = pi[0] + pj[0]
            ci, cj = 2 * pj[0] / M * gg, 2 * pi[0] / M * gg
            Jx, Jy = -pi[0] * ci * nx, -pi[0] * ci * ny        # impulse on i
            pi[4] -= ci * nx
            pi[5] -= ci * ny
            pj[4] += cj * nx
            pj[5] += cj * ny
            st['pair'] += 1
            st['vir_pair'] += dx * Jx + dy * Jy               # r_ij . J_i = sigma |J| > 0
        else:
            p = P[i]
            m = p[0]
            if kind == 'L':
                vx_new = 2 * u_now - p[4]
                st['work'] += 0.5 * m * (vx_new ** 2 - p[4] ** 2)
                Jx, Jy = m * (vx_new - p[4]), 0.0
                p[4] = vx_new
            elif kind == 'R':
                Jx, Jy = -2 * m * p[4], 0.0
                p[4] = -p[4]
            elif kind == 'B':
                Jx, Jy = 0.0, -2 * m * p[5]
                p[5] = -p[5]
            else:
                Jx, Jy = 0.0, -2 * m * p[5]
                p[5] = -p[5]
            st['wall'] += 1
            st['vir_wall'] += p[2] * Jx + p[3] * Jy
    G1 = sum(p[0] * (p[2] * p[4] + p[3] * p[5]) for p in P)
    st['G0'], st['G1'] = G0, G1
    st['resid'] = (G1 - G0) - (st['kin'] + st['vir_wall'] + st['vir_pair'])
    return P, st


# R1: five disks in PhET's 10 nm box, static walls
R1 = [[28, 125, -6000, 4000, 300, 120],
      [28, 125, -4200, 4300, -250, -80],
      [4, 87.5, -5000, 2000, -600, 900],
      [4, 87.5, -3000, 6000, 800, -500],
      [28, 125, -8000, 7000, 150, -400]]
Pf, st = ed_run(R1, -10000.0, HEIGHT, 25.0)
out('R1 pair collisions in 25 ps', st['pair'], 'R1pairs', '%d')
out('R1 wall collisions in 25 ps', st['wall'], 'R1walls', '%d')
REFS['R1init'] = R1
REFS['R1final'] = [[p[2], p[3], p[4], p[5]] for p in Pf]
for k, p in enumerate(Pf):
    out('R1 particle %d x' % k, p[2])
    out('R1 particle %d y' % k, p[3])
    out('R1 particle %d vx' % k, p[4])
    out('R1 particle %d vy' % k, p[5])
out('R1 kinetic virial int 2KE dt', st['kin'], 'R1kin')
out('R1 wall virial sum r.J', st['vir_wall'], 'R1virWall')
out('R1 pair virial sum sigma|J|', st['vir_pair'], 'R1virPair')
out('R1 G1 - G0 (sum m r.v)', st['G1'] - st['G0'], 'R1dG')
out('R1 virial ledger residual', st['resid'], 'R1resid')
E_R1 = sum(0.5 * p[0] * (p[4] ** 2 + p[5] ** 2) for p in R1)
out('R1 total KE (conserved)', E_R1, 'R1E')

# R2: disks near the left wall, which is pushed in at u = +300 pm/ps for 5 ps
R2 = [[28, 125, -9300, 3000, -200, 60],
      [4, 87.5, -8800, 5000, -900, -300],
      [28, 125, -7000, 4500, -400, 150],
      [4, 87.5, -6000, 2500, 500, 650],
      [28, 125, -5200, 6500, -300, -250],
      [28, 125, -3000, 4000, 200, -100]]
REFS['R2init'] = R2
Pf2, st2 = ed_run(R2, -10000.0, HEIGHT, 25.0, u=300.0, t_stop=5.0)
out('R2 pair collisions', st2['pair'], 'R2pairs', '%d')
out('R2 wall collisions', st2['wall'], 'R2walls', '%d')
REFS['R2final'] = [[p[2], p[3], p[4], p[5]] for p in Pf2]
for k, p in enumerate(Pf2):
    out('R2 particle %d x' % k, p[2])
    out('R2 particle %d vx' % k, p[4])
out('R2 work done by the wall', st2['work'], 'R2work')
E2 = sum(0.5 * p[0] * (p[4] ** 2 + p[5] ** 2) for p in Pf2)
E_R2 = sum(0.5 * p[0] * (p[4] ** 2 + p[5] ** 2) for p in R2)
out('R2 initial KE', E_R2, 'R2E0')
out('R2 final KE', E2, 'R2E')
out('R2 KE - KE0 - work (ledger)', E2 - E_R2 - st2['work'], 'R2ledger')
out('R2 virial ledger residual', st2['resid'], 'R2resid')

# R4: twelve disks, a mixture, 30 ps: more collisions per disk
R4 = []
rs4 = np.random.RandomState(11)
for k in range(12):
    m, r = (HEAVY if k % 3 else LIGHT)
    R4.append([m, r, float(-9400 + 780 * k + rs4.uniform(-60, 60)), float(700 + (k % 4) * 2000 + rs4.uniform(-200, 200)),
               float(rs4.uniform(-700, 700)), float(rs4.uniform(-700, 700))])
Pf4, st4 = ed_run(R4, -10000.0, HEIGHT, 30.0)
out('R4 pair collisions in 30 ps', st4['pair'], 'R4pairs', '%d')
out('R4 wall collisions in 30 ps', st4['wall'], 'R4walls', '%d')
REFS['R4init'] = R4
REFS['R4final'] = [[p[2], p[3], p[4], p[5]] for p in Pf4]
out('R4 pair virial', st4['vir_pair'], 'R4virPair')
out('R4 wall virial', st4['vir_wall'], 'R4virWall')
out('R4 kinetic virial', st4['kin'], 'R4kin')
out('R4 G1 - G0', st4['G1'] - st4['G0'], 'R4dG')
out('R4 virial ledger residual', st4['resid'])
for k in (0, 5, 11):
    out('R4 particle %d x' % k, Pf4[k][2])
    out('R4 particle %d vy' % k, Pf4[k][5])

# R5: stale predictions, the case the JS engine's stamps exist for.  An event
# is predicted, then one of its disks is struck by something else first; the
# old prediction must be skipped.  Three groups, 1 ps, every stale event inside
# the first substep:
#  g1 (disks 0-2): A creeps at 100 m/s toward B (contact due at 0.010 ps); K
#      strikes B head-on from below at 0.0005 ps and B leaves upward, A misses
#      (closest approach 250.93 pm).  The A-B event (pushed by A, the lower
#      index) is stale in its PARTNER only.
#  g2 (disks 3-5): the same with B the lower index: stale in its OWNER.
#  g3 (disks 6-7): B2 creeps at 200 m/s toward the right wall (due at 0.005
#      ps); K2 strikes it obliquely at 0.0005 ps, B2 reaches the wall early and
#      is heading away when the stale wall event comes due.
# Processing any of the three flips or kicks a disk that is not touching
# anything, and the run leaves the brute force by ~100 pm.
off3 = math.sqrt(250.0 ** 2 - 100.0 ** 2)          # K2 hits B2 100 pm off-centre
R5 = [[28, 125, -7250.8, 2990.0, 100.0, 0.0],        # g1: A
      [28, 125, -7000.0, 3000.0, 0.0, 0.0],          #     B
      [28, 125, -7000.0, 2749.0, 0.0, 2000.0],       #     K
      [28, 125, -3500.0, 3000.0, 0.0, 0.0],          # g2: B
      [28, 125, -3750.8, 2990.0, 100.0, 0.0],        #     A
      [28, 125, -3500.0, 2749.0, 0.0, 2000.0],       #     K
      [28, 125, -126.0, 5000.0, 200.0, 0.0],         # g3: B2
      [28, 125, -226.0, 5000.0 - off3 - 1.0, 0.0, 2000.0]]   # K2
Pf5, st5 = ed_run(R5, -10000.0, HEIGHT, 1.0)
out('R5 pair collisions in 1 ps (the three strikes)', st5['pair'], 'R5pairs', '%d')
out('R5 wall collisions in 1 ps (B2, once)', st5['wall'], 'R5walls', '%d')
REFS['R5init'] = R5
REFS['R5final'] = [[p[2], p[3], p[4], p[5]] for p in Pf5]
for k, p in enumerate(Pf5):
    out('R5 particle %d x' % k, p[2])
    out('R5 particle %d y' % k, p[3])
    out('R5 particle %d vx' % k, p[4])
    out('R5 particle %d vy' % k, p[5])
out('R5 virial ledger residual', st5['resid'])
# the misses the design relies on: A passes B at >= 250.93 pm (g1, g2)
tau = 5075.0 / 4.01e6
out('R5 A-B closest approach after the strike, pm', math.hypot(250.75 - 100 * tau, 10 + 2000 * tau))

# R3: collisions off (a 12-disk ideal gas): every |vx|, |vy| is a constant
R3 = []
rs = np.random.RandomState(7)
for k in range(12):
    m, r = (HEAVY if k % 2 == 0 else LIGHT)
    R3.append([m, r, -10000 + 400 + 800 * k, 1000 + 550 * k, float(rs.uniform(-900, 900)), float(rs.uniform(-900, 900))])
Pf3, st3 = ed_run(R3, -10000.0, HEIGHT, 40.0, collisions=False)
out('R3 (collisions off) wall collisions in 40 ps', st3['wall'], 'R3walls', '%d')
REFS['R3init'] = R3
REFS['R3final'] = [[p[2], p[3], p[4], p[5]] for p in Pf3]

# ---------------------------------------------------------------------------
head('4. mulberry32 + Box-Muller, bit for bit; PhET injection')


def mulberry32(seed):
    st_ = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        a_ = (st_[0] + 0x6D2B79F5) & 0xFFFFFFFF
        st_[0] = a_
        t_ = imul(a_ ^ (a_ >> 15), a_ | 1)
        t_ = ((t_ + imul(t_ ^ (t_ >> 7), t_ | 61)) & 0xFFFFFFFF) ^ t_
        return ((t_ ^ (t_ >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return nxt


rng = mulberry32(12345)
first = [rng() for _ in range(5)]
for k, v in enumerate(first):
    out('mulberry32(12345) draw %d' % k, v)
REFS['rng12345'] = first


def gauss(nxt):
    u1 = 1.0 - nxt()                     # (0, 1]
    u2 = nxt()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)


def phet_inject(seed, n, T, m, r, collisions=True):
    """PhET's addParticles: temperatures Gaussian (sd 0.2T) with the mean
    restored exactly (getGaussianValues), speed sqrt(3kT_i/m), direction
    uniform in [3pi/4, 5pi/4] (the pump's pi/2 fan, pointing left), all at
    (-r, H/5).  The JS draws the n Gaussians first, then the n angles."""
    nxt = mulberry32(seed)
    if n != 1 and collisions:
        Ts = [T + 0.2 * T * gauss(nxt) for _ in range(n)]
        shift = T - sum(Ts) / n
        Ts = [Ti + shift for Ti in Ts]
    else:
        Ts = [T] * n
    res = []
    for Ti in Ts:
        th = math.pi - (math.pi / 2) / 2 + nxt() * (math.pi / 2)
        sp = math.sqrt(3 * K_PHET * Ti / m)
        res.append([-r, HEIGHT / 5, sp * math.cos(th), sp * math.sin(th), Ti])
    return res


inj = phet_inject(2024, 6, 300.0, 28.0, 125.0)
REFS['inject2024'] = inj
for k, p in enumerate(inj):
    out('inject(seed 2024, 6 heavy, 300 K) #%d T_i' % k, p[4])
    out('   vx', p[2])
    out('   vy', p[3])
out('inject mean T (restored exactly)', sum(p[4] for p in inj) / 6, 'injMeanT')
KEm = sum(0.5 * 28 * (p[2] ** 2 + p[3] ** 2) for p in inj) / 6
out('inject mean KE -> T = (2/3)<KE>/k', (2 / 3) * KEm / K_PHET, 'injT')

# ---------------------------------------------------------------------------
head('5. 2-D Maxwell-Boltzmann in PhET units; PhET histogram bins')
# speed pdf f(v) = (m v / kT2) exp(-m v^2 / 2kT2), cdf 1 - exp(-m v^2/2kT2)
# energy pdf (1/kT2) exp(-e/kT2): exponential with mean kT2 (2 quadratic dof)
NB, SBIN, EBIN = 19, 170.0, 8e5
for nm, (m, r) in (('heavy', HEAVY), ('light', LIGHT)):
    F = lambda v: 1 - math.exp(-m * v * v / (2 * kT2_300))
    pb = [F((k + 1) * SBIN) - F(k * SBIN) for k in range(NB)]
    REFS['sbins_' + nm] = pb
    out('%s P(speed bin 0), 300 K' % nm, pb[0])
    out('%s P(speed bin 2)' % nm, pb[2])
    out('%s P(speed beyond the 19 bins)' % nm, 1 - F(NB * SBIN), 'sTail_' + nm)
    # check the pdf integrates to the cdf (scipy quad, independent route)
    q, _ = integrate.quad(lambda v: m * v / kT2_300 * math.exp(-m * v * v / (2 * kT2_300)), 2 * SBIN, 3 * SBIN)
    out('%s quad of the pdf over bin 2 (check)' % nm, q)
    # mean speed by quadrature against the closed form
    q2, _ = integrate.quad(lambda v: v * m * v / kT2_300 * math.exp(-m * v * v / (2 * kT2_300)), 0, np.inf)
    out('%s <v> by quad (check)' % nm, q2)
Fe = lambda e: 1 - math.exp(-e / kT2_300)
pe = [Fe((k + 1) * EBIN) - Fe(k * EBIN) for k in range(NB)]
REFS['ebins'] = pe
out('P(KE bin 0), any mass, 300 K', pe[0], 'ebin0')
out('P(KE bin 4)', pe[4], 'ebin4')
out('P(KE beyond the 19 bins)', 1 - Fe(NB * EBIN), 'eTail')
out('Var(v)/(kT2/m) for 2-D MB = 2 - pi/2', 2 - math.pi / 2, 'varVfac')

# ---------------------------------------------------------------------------
head('6. the finite-N microcanonical laws (Dirichlet) and the test tolerances')
# In a closed box the total kinetic energy E is exactly conserved and hard
# disks have no potential energy, so the momenta are uniform on the energy
# shell.  Each disk carries 2 quadratic dof, so the energy FRACTIONS
# x_i = e_i/E are Dirichlet(1,...,1): uniform on the simplex, whatever the
# masses.  One disk: x ~ Beta(1, N-1), F(e) = 1 - (1 - e/E)^(N-1).
lg = special.gammaln


def dir_moment(N, a, b):
    """E[x1^a x2^b] for Dirichlet(1^N)"""
    return math.exp(lg(N) + lg(1 + a) + lg(1 + b) - lg(N + a + b))


def dir_moment_exact(N, a, b):
    """E[x1^a x2^b] for Dirichlet(1^N), integer a, b: (N-1)! a! b! / (N-1+a+b)!"""
    return Fr(math.factorial(N - 1) * math.factorial(a) * math.factorial(b), math.factorial(N - 1 + a + b))


def q_stats(N):
    """Q = N sum x_i^2 (= <e^2>/<e>^2 in one snapshot): mean and variance, exact"""
    Esum = N * dir_moment_exact(N, 2, 0)
    Esum2 = N * dir_moment_exact(N, 4, 0) + N * (N - 1) * dir_moment_exact(N, 2, 2)
    return float(N * Esum), float(N * N * (Esum2 - Esum * Esum))


def vbar_stats(N):
    """V = (1/N) sum sqrt(x_i) (the snapshot mean speed / sqrt(2E/m)): mean, var"""
    E1 = dir_moment(N, 0.5, 0)
    Ex = 1.0 / N
    E12 = dir_moment(N, 0.5, 0.5)
    var = (Ex - E1 * E1) / N + (1 - 1.0 / N) * (E12 - E1 * E1)
    return E1, var


for N in (60,):
    mQ, vQ = q_stats(N)
    out('N=%d: E[Q] = 2N/(N+1)' % N, mQ, 'EQ%d' % N)
    out('N=%d: 2N/(N+1) closed form' % N, 2 * N / (N + 1))
    out('N=%d: SD(Q) one snapshot' % N, math.sqrt(vQ), 'sdQ%d' % N)
    mV, vV = vbar_stats(N)
    out('N=%d: E[mean sqrt(x)] = G(3/2)G(N)/G(N+1/2)' % N, mV, 'EV%d' % N)
    out('N=%d: SD(mean sqrt(x)) one snapshot' % N, math.sqrt(vV), 'sdV%d' % N)
    out('N=%d: canonical limit sqrt(pi/(4N))' % N, math.sqrt(math.pi / (4 * N)))
    # species split: S = sum over the first N/2 of x ~ Beta(N/2, N/2);
    # D = (mean e_heavy - mean e_light)/(E/N) = 2(2S - 1), Var(D) = 4/(N+1)
    out('N=%d: SD(D) heavy-light equipartition, one snapshot' % N, math.sqrt(4 / (N + 1)), 'sdD%d' % N)
# Monte Carlo over the exact ensemble: check the closed-form moments, and
# the sampling law of the pooled chi-square statistic used in selfTest:
# R independent snapshots of N disks, energies pooled, K equal-probability
# bins of the exact marginal Beta(1, N-1).
N, R, K = 60, 40, 12
edges = [1 - (1 - k / K) ** (1 / (N - 1)) for k in range(K + 1)]   # quantiles of Beta(1,N-1)
edges[-1] = 1.0
REFS['chiEdges'] = edges[1:-1]
rsx = np.random.default_rng(99)
reps = 20000
X2 = np.empty(reps)
Qs = np.empty(reps)
Vs = np.empty(reps)
for rep in range(reps):
    x = rsx.dirichlet(np.ones(N), size=R)          # R x N
    cnt = np.histogram(x.ravel(), bins=edges)[0]
    Eexp = R * N / K
    X2[rep] = ((cnt - Eexp) ** 2 / Eexp).sum()
    Qs[rep] = (N * (x ** 2).sum(axis=1)).mean()
    Vs[rep] = np.sqrt(x).mean()
mQ, vQ = q_stats(N)
mV, vV = vbar_stats(N)
out('MC: mean of Qbar over %d reps (vs E[Q])' % reps, Qs.mean())
out('MC: SD of Qbar (vs SD(Q)/sqrt(R))', Qs.std(ddof=1))
out('  closed form SD(Q)/sqrt(R)', math.sqrt(vQ / R), 'sdQbar')
out('MC: mean of Vbar', Vs.mean())
out('MC: SD of Vbar', Vs.std(ddof=1))
out('  closed form SD(V)/sqrt(R)', math.sqrt(vV / R), 'sdVbar')
out('MC: chi-square mean (K-1 = %d for multinomial)' % (K - 1), X2.mean(), 'chiMean')
out('MC: chi-square variance (2(K-1) = %d for multinomial)' % (2 * (K - 1)), X2.var(ddof=1), 'chiVar')
q999 = np.quantile(X2, 0.999)
out('MC: chi-square 99.9th percentile', q999, 'chi999')
# the 1e-4 tail: the chi-square law with the MC mean, scaled to the MC variance
scale = X2.var(ddof=1) / (2 * X2.mean())
dof = X2.mean() / scale
q9999 = scale * stats.chi2.ppf(0.9999, dof)
out('scaled chi-square 99.99th percentile (the selfTest bound)', q9999, 'chi9999')
out('  multinomial chi2(K-1) 99.99th percentile, for comparison', stats.chi2.ppf(0.9999, K - 1))

# ---------------------------------------------------------------------------
head('7. hard disks: B2, B3, the finite-box contact measure')
sig = 250.0
B2 = math.pi * sig ** 2 / 2
out('B2 = pi sigma^2 / 2, heavy (pm^2)', B2, 'B2heavy')


def lens(d, s_):
    return 2 * s_ * s_ * math.acos(d / (2 * s_)) - (d / 2) * math.sqrt(4 * s_ * s_ - d * d)


# B3 = (1/3) int over r2 in the disk |r2| < s of the lens area (r3 within s
# of both the origin and r2)  -- the three-disk Mayer integral
B3q, _ = integrate.quad(lambda rr: 2 * math.pi * rr * lens(rr, 1.0), 0, 1.0, epsabs=1e-14, epsrel=1e-14)
B3q /= 3.0
B3c = (4.0 / 3 - math.sqrt(3) / math.pi) * (math.pi / 2) ** 2
out('B3 / sigma^4 by quadrature', B3q, 'B3q')
out('B3 / sigma^4 closed form (4/3 - sqrt3/pi) (pi/2)^2', B3c, 'B3c')
out('B3 / B2^2 = 4/3 - sqrt3/pi', 4.0 / 3 - math.sqrt(3) / math.pi, 'B3overB2sq')


def contact_measure(a_, b_, s_):
    return 2 * math.pi * s_ * a_ * b_ - 4 * s_ * s_ * (a_ + b_) + 2 * s_ ** 3


def contact_measure_quad(a_, b_, s_):
    # s * int_0^2pi (a - s|cos|)(b - s|sin|) dtheta, integrated numerically
    f = lambda th: (a_ - s_ * abs(math.cos(th))) * (b_ - s_ * abs(math.sin(th)))
    val = 0.0
    for k in range(4):
        v, _ = integrate.quad(f, k * math.pi / 2, (k + 1) * math.pi / 2, epsabs=1e-9, epsrel=1e-14)
        val += v
    return s_ * val


a_, b_ = 10000 - 250.0, HEIGHT - 250.0
out('contact measure M, heavy in the 10 nm box (closed form)', contact_measure(a_, b_, sig), 'Mbox')
out('   by quadrature', contact_measure_quad(a_, b_, sig))
out('   M / (2 pi sigma a b) (the wall deficit)', contact_measure(a_, b_, sig) / (2 * math.pi * sig * a_ * b_), 'Mratio')
# the low-density collisional virial for one species of N disks in a x b:
# per pair the virial rate is sigma kT2 M / (ab)^2 (derivation in the header
# comment of the page), so Z - 1 = C/(2E) = (N - 1) sigma M / (4 (a b)^2) at
# first order, times (1 + (B3/B2) rho) at second (bulk).  Brute-force check of
# the per-pair contact-rate formula by Monte Carlo is in section 7b.
for Nv in (90,):
    z1 = (Nv - 1) * sig * contact_measure(a_, b_, sig) / (4 * (a_ * b_) ** 2)
    rho = Nv / (a_ * b_)
    z2 = z1 * (1 + (4.0 / 3 - math.sqrt(3) / math.pi) * B2 * rho)
    out('N=%d heavy, 10 nm box: (Z-1) first order' % Nv, z1, 'Z1_%d' % Nv)
    out('N=%d: (Z-1) with the bulk B3 correction' % Nv, z2, 'Z2_%d' % Nv)
    out('N=%d: area fraction eta' % Nv, Nv * math.pi * 125.0 ** 2 / (10000 * HEIGHT), 'eta_%d' % Nv)
    out('N=%d: bulk B2 rho for comparison' % Nv, B2 * rho)

head('7b. Monte Carlo check of the pair contact measure')
# two points uniform in a x b: P(|r1 - r2| in [s, s+ds]) = M(s) ds / (ab)^2
rsm = np.random.default_rng(5)
aa, bb, ss = 3.0, 2.0, 0.4
nmc = 4_000_000
p1 = rsm.random((nmc, 2)) * [aa, bb]
p2 = rsm.random((nmc, 2)) * [aa, bb]
d = np.hypot(*(p1 - p2).T)
ds = 0.01
frac = np.mean((d >= ss - ds / 2) & (d < ss + ds / 2))
out('MC P(|r1-r2| in shell) / ds * (ab)^2', frac / ds * (aa * bb) ** 2)
out('   closed form M(s) (to O(ds^2))', contact_measure(aa, bb, ss))

# ---------------------------------------------------------------------------
head('8. heater, adiabat, effusion')
DT_PHET = 2.5 / 60
out('PhET frame, 60 fps at 1 ps = 0.4 s (ps)', DT_PHET, 'dtFrame')
f1 = (1 + 1 / 800) ** (1 / DT_PHET)
out('speed factor per ps at full heat (1 + 1/800)^24', f1, 'heatPerPs')
out('KE factor per ps at full heat', f1 ** 2, 'heatKEPerPs')
out('ps to heat 300 K -> 1000 K at full heat', math.log(1000 / 300) / (2 * math.log(1 + 1 / 800)) * DT_PHET, 'heatTime')
out('ps to cool 300 K -> 100 K at full cool', math.log(100 / 300) / (2 * math.log(1 - 1 / 800)) * DT_PHET, 'coolTime')
# the adiabat: 2-D ideal gas E = N kT2, P2 A = E; dE = -P2 dA -> E A = const
# (gamma = 1 + 2/f with f = 2).  PhET's rule does half the work: E A^(1/2) = const.
out('2-D gamma = 1 + 2/f, f = 2', 1 + 2 / 2, 'gamma2d')
out('T after squeezing 15 -> 5 nm from 300 K (elastic, T V = const)', 300 * 15 / 5, 'Tsqueeze')
out('... with PhET rule (T V^(1/2) = const)', 300 * math.sqrt(15 / 5), 'TsqueezePhet')
out('... a real monatomic 3-D gas (T V^(2/3) = const)', 300 * (15 / 5) ** (2 / 3), 'Tsqueeze3d')
# effusion: 2-D flux per unit length Phi = n sqrt(kT2/(2 pi m)); Graham: rate ~ 1/sqrt(m)
for nm, (m, r) in (('heavy', HEAVY), ('light', LIGHT)):
    out('%s <v_x+> = sqrt(kT2/(2 pi m)) at 300 K' % nm, math.sqrt(kT2_300 / (2 * math.pi * m)), 'vxplus_' + nm)
out('Graham ratio light/heavy sqrt(28/4)', math.sqrt(28 / 4), 'graham')
# wall-hit rate for collisions-off: particle i hits the x-walls |vx|/(W-2r) per ps
out('PhET pressure noise at P = 1183 kPa, T = 300 K (max, kPa)', 50 * (1 - 1183.0 / 20000), 'noiseMax')

# ---------------------------------------------------------------------------
head('9. the quasi-static adiabat of hard disks; the sound speed')
# Pushed slowly, the gas stays in equilibrium: dE = -F_x dW, and the virial
# split (isotropic to 1e-4 here) gives F_x (W - 2r) = E Z(W).  With T ~ E:
#   ln(T1/T0) = int_{W1}^{W0} Z(W) dW / (W - 2r),
#   Z(W) = 1 + z1 (1 + (B3/B2^2) B2 N/(a b)),  z1 = (N-1) s M(a,b,s) / (4 (a b)^2),
#   a = W - 2r, b = H - 2r.  Points (r -> 0, Z -> 1): T W = const.
def hd_adiabat_ratio(N, r, W0, W1, Hh, b3=True):
    sg = 2 * r
    def Z(W):
        a_ = W - sg
        b_ = Hh - sg
        z1 = (N - 1) * sg * contact_measure(a_, b_, sg) / (4 * (a_ * b_) ** 2)
        if b3:
            z1 *= 1 + (4.0 / 3 - math.sqrt(3) / math.pi) * (math.pi * sg * sg / 2) * N / (a_ * b_)
        return 1 + z1
    val, _ = integrate.quad(lambda W: Z(W) / (W - sg), W1, W0, epsabs=0, epsrel=1e-13)
    return math.exp(val)


for b3 in (False, True):
    rr = hd_adiabat_ratio(100, 125.0, 10000.0, 7000.0, HEIGHT, b3)
    out('100 heavy, 10 -> 7 nm: T1/T0 hard disks (%s)' % ('B2+B3' if b3 else 'first order'), rr, 'adHD' if b3 else 'adHD1')
    out('   T1 W1 / T0 W0', rr * 0.7, 'adHDtw' if b3 else 'adHD1tw')
out('points in the accessible width: (W0-2r)/(W1-2r) * W1/W0', (10000 - 250.0) / (7000 - 250.0) * 0.7, 'adPointsTw')
out('100 light, 10 -> 7 nm: T1 W1 / T0 W0 (B2+B3)', hd_adiabat_ratio(100, 87.5, 10000.0, 7000.0, HEIGHT) * 0.7, 'adHDlight')
# sound in a 2-D ideal gas: c^2 = gamma P/rho = 2 kT2/m -- equal to the rms speed
for nm, (m, r) in (('heavy', HEAVY), ('light', LIGHT)):
    c = math.sqrt(2 * kT2_300 / m)
    out('%s sound speed sqrt(2 kT2/m) at 300 K (m/s)' % nm, c, 'cSound_' + nm)
    out('   PhET wall limit 800 m/s as a Mach number', 800 / c, 'mach800_' + nm)

# ---------------------------------------------------------------------------
path = os.path.join(HERE, 'refvals.txt')
io.open(path, 'w', encoding='utf-8').write('\n'.join(OUT_LINES) + '\n')


def js(v):
    if isinstance(v, (float, np.floating)):
        return repr(float(v))
    if isinstance(v, int):
        return str(v)
    if isinstance(v, (list, tuple)):
        return '[' + ','.join(js(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ','.join('%s:%s' % (k, js(x)) for k, x in v.items()) + '}'
    if isinstance(v, str):
        return "'" + v + "'"
    if isinstance(v, (np.floating,)):
        return repr(float(v))
    if isinstance(v, (np.integer,)):
        return str(int(v))
    raise TypeError(type(v))


lines = ['/* ================================================================== *',
         ' *  reference values — WRITTEN BY derive.py (build/gas-properties);   *',
         ' *  the same numbers are printed in refvals.txt.  Do not edit.        *',
         ' * ================================================================== */',
         'const REF={']
for k, v in REFS.items():
    lines.append('  %s:%s,' % (k, js(v)))
lines.append('};\n')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write('\n'.join(lines))
print('\nwrote refvals.txt (%d lines) and p7a_refs.js (%d refs)' % (len(OUT_LINES), len(REFS)))
