#!/usr/bin/env python3
"""derive.py — the Python twin of wave-on-a-string.html.

Everything the page asserts is re-derived here, independently of the JS, and
printed to 13+ significant digits.  The JS selfTest pins these lines; the
labels there say (derive) and point at the line printed below.  Run:

    python3 derive.py > refvals.txt       (read the WHOLE file, never head/tail)

THE MODEL (PhET's, read out of wave-on-a-string_en.html v1.2.4 and its
doc/model.md; the remake keeps the scheme and the constants):
  61 beads, 60 intervals of dx = 0.125 cm (PhET: 10 model units at 80 per cm),
  the leapfrog update
      (1+b) y_i^{n+1} = (b-1) y_i^{n-1} + 2(1-a^2) y_i^n + a^2 (y_{i+1}^n + y_{i-1}^n)
  with Courant number a = v dt/dx = 1 always (tension sets the CLOCK, dt = dx/v,
  never the stencil) and b = 0.1 x (damping slider in [0,1]).
  Ends: fixed y_N = 0; loose y_N = y_{N-1}; none y_N^{n+1} = y_{N-1}^n.
  Driver at bead 0: oscillator A sin(phi), phi += 2 pi f dt per step; pulse = a
  triangle of height A lasting w seconds; manual = the wrench.
  Speed: PhET maps its relative tension T in [0.2, 0.8] AFFINELY in sqrt(T) onto
  10..50 steps/s.  The remake keeps PhET's speed range 1.25..6.25 cm/s but makes
  it the physical law v = v_max sqrt(T / T_max): T in [0.032, 0.8].
"""
import math
import cmath
import numpy as np
from scipy import optimize

np.set_printoptions(precision=16)

# ---------------------------------------------------------------- constants
NSEG = 60                  # intervals (PhET: 61 beads, indices 0..60)
DX = 10.0 / 80.0           # cm between beads (PhET: 10 model units, 80 per cm)
L = NSEG * DX              # 7.5 cm, bead 0 to bead 60
LLOOSE = (NSEG - 0.5) * DX # the loose end reflects about bead 59.5 (derived below)
TMAX, TMIN = 0.8, 0.8 / 25.0
VMAX = 50.0 * DX           # 6.25 cm/s: PhET steps 50 times a second at full tension
BETA_PER_DAMP = 0.1        # PhET: e = 0.2 * damping; beta = e / 2


def P(label, x):
    """print a reference value to 16 significant digits, one per line"""
    if isinstance(x, complex):
        print('%-58s %.16g %+.16gj' % (label, x.real, x.imag))
    else:
        print('%-58s %.16g' % (label, x))


def speed(T):
    return VMAX * math.sqrt(T / TMAX)


def dt_of(T):
    return DX / speed(T)


def phet_rate(T):
    """PhET's own map (steps per second): linear in sqrt(T) from sqrt(.2)->.2 to sqrt(.8)->1, times 50"""
    s = math.sqrt(T)
    return 50.0 * (0.2 + (1.0 - 0.2) * (s - math.sqrt(0.2)) / (math.sqrt(0.8) - math.sqrt(0.2)))


def tri(u):
    return 1.0 - abs(2.0 * u - 1.0) if 0.0 <= u <= 1.0 else 0.0


def pulse(t, A, w, t0=0.0):
    return A * tri((t - t0) / w)


# ---------------------------------------------------------------- the lattice (plain Python floats,
# the SAME operation order as the JS so the two agree to the last bit where libm does)
def step(prev, cur, a, b, end, yleft):
    n = len(cur) - 1
    if end == 'fixed':
        cur[n] = 0.0
    elif end == 'loose':
        cur[n] = cur[n - 1]
    else:
        cur[n] = prev[n - 1]
    a2 = a * a
    c = 2.0 * (1.0 - a2)
    inv = 1.0 / (1.0 + b)
    nxt = [0.0] * (n + 1)
    for i in range(1, n):
        nxt[i] = inv * ((b - 1.0) * prev[i] + c * cur[i] + a2 * (cur[i + 1] + cur[i - 1]))
    nxt[0] = yleft
    if end == 'fixed':
        nxt[n] = 0.0
    elif end == 'loose':
        nxt[n] = nxt[n - 1]
    else:
        nxt[n] = cur[n - 1]
    return cur, nxt


def run_pulse(end, A, w, T, nsteps, a=1.0, b=0.0, nseg=NSEG):
    """drive one triangle pulse from bead 0 starting at t = 0; return levels 0..nsteps"""
    dt = a * DX / speed(T)
    prev = [0.0] * (nseg + 1)
    cur = [0.0] * (nseg + 1)
    levels = [cur[:]]
    for k in range(1, nsteps + 1):
        prev, cur = step(prev, cur, a, b, end, pulse(k * dt, A, w))
        levels.append(cur[:])
    return levels, dt


def image_series(end, A, w, T, n, i):
    """d'Alembert with images: the lattice is EXACT for a = 1, b = 0"""
    v, dt = speed(T), dt_of(T)
    t, x = n * dt, i * DX
    f = lambda tau: pulse(tau, A, w)
    s = 0.0
    if end == 'none':
        return f(t - x / v)
    Lr = L if end == 'fixed' else LLOOSE
    sgn_right = -1.0 if end == 'fixed' else 1.0
    m = 0
    while True:
        t1 = t - (2 * m * Lr + x) / v
        if t1 <= 0 and t - (2 * (m + 1) * Lr - x) / v <= 0:
            break
        # each round trip: reflect at the right (sgn_right) and at the driven left end (-1)
        rt = (sgn_right * -1.0) ** m
        s += rt * (f(t1) + sgn_right * f(t - (2 * (m + 1) * Lr - x) / v))
        m += 1
    return s


print('# ============ wave-on-a-string derive.py ============')
P('dx (cm)', DX)
P('L (cm)', L)
P('L_loose (cm)', LLOOSE)
P('v_max (cm/s)', VMAX)

# ---------------------------------------------------------------- 1. tension -> speed
print('\n# ---- 1. tension -> speed (v = v_max sqrt(T/T_max)) and PhET\'s own map')
for T in (0.8, 0.5, 0.2, 0.032, 0.29, 0.53):
    P('v(T=%g) cm/s' % T, speed(T))
    P('dt(T=%g) s' % T, dt_of(T))
for T in (0.8, 0.5, 0.2):
    P('PhET rate(T=%g) steps/s' % T, phet_rate(T))
    P('PhET v(T=%g) cm/s' % T, phet_rate(T) * DX)
P('PhET v ratio max/min', phet_rate(0.8) / phet_rate(0.2))
P('sqrt-law v ratio over PhET\'s 0.2..0.8', speed(0.8) / speed(0.2))

# ---------------------------------------------------------------- 2. d'Alembert exactness
print("\n# ---- 2. the lattice (a=1, b=0) against d'Alembert with images")
for (A, w, T, nst) in ((0.75, 0.5, 0.8, 170), (1.1, 0.37, 0.29, 200)):
    for end in ('fixed', 'loose', 'none'):
        lev, dt = run_pulse(end, A, w, T, nst)
        dev = 0.0
        for n in range(nst + 1):
            for i in range(NSEG + 1):
                if end == 'loose' and i == NSEG:
                    ex = image_series(end, A, w, T, n, NSEG - 1)   # the ring bead copies bead 59
                else:
                    ex = image_series(end, A, w, T, n, i)
                dev = max(dev, abs(lev[n][i] - ex))
        P('max|lattice - images| %s A=%g w=%g T=%g' % (end, A, w, T), dev)
    # the WRONG mirror for the loose end: 7.5 cm instead of 7.4375
    lev, dt = run_pulse('loose', A, w, T, nst)
    bad = 0.0
    v = speed(T)
    for n in range(nst + 1):
        for i in range(NSEG):
            t, x = n * dt, i * DX
            ex = pulse(t - x / v, A, w) + pulse(t - (2 * L - x) / v, A, w)
            if t < 2 * L / v:
                bad = max(bad, abs(lev[n][i] - ex))
    P('loose end with the mirror at 7.5 cm: max dev A=%g' % A, bad)

lev, dt = run_pulse('fixed', 0.75, 0.5, 0.8, 170)
P('fixed y[45] at step 60', lev[60][45])
P('fixed y[30] at step 40', lev[40][30])
P('fixed y[57] at step 70', lev[70][57])
P('fixed reflected min y[30], steps 95..130', min(lev[n][30] for n in range(95, 131)))
levL, _ = run_pulse('loose', 0.75, 0.5, 0.8, 170)
P('loose y[60] at step 72', levL[72][60])
P('loose max y[60] over all steps', max(levL[n][60] for n in range(171)))
P('loose reflected max y[30], steps 95..130', max(levL[n][30] for n in range(95, 131)))
levN, _ = run_pulse('none', 0.75, 0.5, 0.8, 170)
P('none max|y| over all beads, steps 90..170', max(abs(levN[n][i]) for n in range(90, 171) for i in range(61)))
P('pulse sampled apex f(12 dt) (A=.75,w=.5,T=.8)', pulse(12 * 0.02, 0.75, 0.5))
lev2, dt2 = run_pulse('fixed', 1.1, 0.37, 0.29, 200)
P('incommensurate fixed y[20] at step 31', lev2[31][20])
P('incommensurate fixed y[51] at step 75', lev2[75][51])
lev2L, _ = run_pulse('loose', 1.1, 0.37, 0.29, 200)
P('incommensurate loose y[60] at step 66', lev2L[66][60])

# switching the end type mid-run: fixed for 70 steps (the pulse is reflecting), then loose.
# PhET re-asserts the end rule on the CURRENT level before each update, which matters
# exactly once, on the first step after the switch.
prev = [0.0] * (NSEG + 1); cur = [0.0] * (NSEG + 1)
for k in range(1, 91):
    prev, cur = step(prev, cur, 1.0, 0.0, 'fixed' if k <= 70 else 'loose', pulse(k * 0.02, 0.75, 0.5))
    if k == 71:
        P('switch fixed->loose at 70: y[59] at step 71', cur[59])
P('switch fixed->loose at 70: y[59] at step 90', cur[59])
P('switch fixed->loose at 70: y[40] at step 90', cur[40])
# the same run WITHOUT the pre-update, to show it is load-bearing
def step_nopre(prev, cur, a, b, end, yleft):
    n = len(cur) - 1
    a2 = a * a; c = 2.0 * (1.0 - a2); inv = 1.0 / (1.0 + b)
    nxt = [0.0] * (n + 1)
    for i in range(1, n):
        nxt[i] = inv * ((b - 1.0) * prev[i] + c * cur[i] + a2 * (cur[i + 1] + cur[i - 1]))
    nxt[0] = yleft
    nxt[n] = 0.0 if end == 'fixed' else (nxt[n - 1] if end == 'loose' else cur[n - 1])
    return cur, nxt
prev = [0.0] * (NSEG + 1); cur = [0.0] * (NSEG + 1)
for k in range(1, 91):
    prev, cur = step_nopre(prev, cur, 1.0, 0.0, 'fixed' if k <= 70 else 'loose', pulse(k * 0.02, 0.75, 0.5))
P('   (without the pre-update: y[59] at step 90)', cur[59])

# the centroid of the incident pulse moves at exactly v (a=1): between steps 30 and 50, T=0.5
levc, dtc = run_pulse('none', 0.75, 0.5, 0.5, 60)
def centroid(y):
    s = sum(y); return sum(i * DX * yi for i, yi in enumerate(y)) / s
P('centroid speed steps 30->50, T=0.5 (cm/s)', (centroid(levc[50]) - centroid(levc[30])) / (20 * dtc))
P('first step with y[40] != 0 (pulse arrival)', next(n for n in range(61) if levc[n][40] != 0.0))

# ---------------------------------------------------------------- 3. damped eigenmodes
print('\n# ---- 3. damping: a fixed-fixed lattice eigenmode')
def mode_run(m, a, b, nmax, g0, gm1):
    """y_i = sin(m pi i / N) g_n on a lattice with y_0 = y_N = 0"""
    kap = m * math.pi / NSEG
    prev = [math.sin(kap * i) * gm1 for i in range(NSEG + 1)]
    cur = [math.sin(kap * i) * g0 for i in range(NSEG + 1)]
    prev[0] = cur[0] = prev[NSEG] = cur[NSEG] = 0.0
    out = {0: cur[:]}
    for n in range(1, nmax + 1):
        prev, cur = step(prev, cur, a, b, 'fixed', 0.0)
        out[n] = cur[:]
    return out, kap

for (m, a, b, g0, gm1, ns, ibead) in ((3, 1.0, 0.02, 1.0, 1.0, (1, 10, 100, 500), 10),
                                      (17, 0.6, 0.05, 1.0, 1.0, (1, 7, 60, 250), 13),
                                      (41, 1.0, 0.0, 1.0, 0.0, (1, 33, 400), 9)):
    out, kap = mode_run(m, a, b, max(ns), g0, gm1)
    cth = (1.0 - 2.0 * a * a * math.sin(kap / 2) ** 2) / math.sqrt(1.0 - b * b)
    # closed form: g_n = Re(C z^n), z = r e^{i th}, r = sqrt((1-b)/(1+b)); fit C from g_0, g_{-1}
    r = math.sqrt((1 - b) / (1 + b))
    th = math.acos(cth)
    z = r * cmath.exp(1j * th)
    zb = z.conjugate()
    # g_n = c1 z^n + c2 zbar^n with g_0 = c1 + c2, g_{-1} = c1/z + c2/zbar
    Mx = np.array([[1, 1], [1 / z, 1 / zb]], dtype=complex)
    c1, c2 = np.linalg.solve(Mx, np.array([g0, gm1], dtype=complex))
    for n in ns:
        g_closed = (c1 * z ** n + c2 * zb ** n).real
        g_latt = out[n][ibead] / math.sin(kap * ibead)
        P('mode m=%d a=%g b=%g: g_%d lattice' % (m, a, b, n), g_latt)
        P('mode m=%d a=%g b=%g: g_%d closed form' % (m, a, b, n), g_closed)
    P('mode m=%d: theta (rad/step)' % m, th)
    P('mode m=%d: |z| per step' % m, r)
P('amplitude kept per step, b=0.02', math.sqrt(0.98 / 1.02))
P('exp(-atanh(0.02))', math.exp(-math.atanh(0.02)))
P('decay length dx/atanh(b), b=0.02 (cm)', DX / math.atanh(0.02))
P('decay length dx/atanh(b), b=0.1 (cm)', DX / math.atanh(0.1))
P('damping rate 2b/dt (1/s), b=0.02, T=0.8', 2 * 0.02 / dt_of(0.8))

# ---------------------------------------------------------------- 4. dispersion
print('\n# ---- 4. the lattice dispersion  (1+b) z^2 - 2(1 - 2a^2 sin^2(k/2)) z + (1-b) = 0')
def theta_of(kap, a, b):
    c = (1.0 - 2.0 * a * a * math.sin(kap / 2) ** 2) / math.sqrt(1.0 - b * b)
    return math.acos(max(-1.0, min(1.0, c)))
def vg_over_v(kap, a, b):
    th = theta_of(kap, a, b)
    return a * math.sin(kap) / (math.sqrt(1 - b * b) * math.sin(th))
for (kap, a, b) in ((1.0, 1.0, 0.0), (2.0, 0.5, 0.0), (1.5, 0.8, 0.05), (0.3, 1.0, 0.02), (2.9, 0.35, 0.0), (0.02, 1.0, 0.1)):
    roots = np.roots([1 + b, -2 * (1 - 2 * a * a * math.sin(kap / 2) ** 2), 1 - b])
    th_np = abs(np.angle(roots[0]))
    P('theta(k=%g,a=%g,b=%g)' % (kap, a, b), theta_of(kap, a, b))
    P('  np.roots angle', th_np)
    P('  |root|', abs(roots[0]))
    # omega dx / v = theta / a  (since dt = a dx / v)
    P('  omega dx/v = theta/a', theta_of(kap, a, b) / a)
    if abs(math.sin(theta_of(kap, a, b))) > 1e-9:
        h = 1e-6
        num = (theta_of(kap + h, a, b) - theta_of(kap - h, a, b)) / (2 * h) / a
        P('  v_g/v closed form', vg_over_v(kap, a, b))
        P('  v_g/v numerical', num)
        P('  v_p/v', theta_of(kap, a, b) / a / kap)
P('bead chain omega dx/v at k=2 (2 sin(k/2))', 2 * math.sin(1.0))
for a in (0.02, 0.002):
    P('lattice omega dx/v at k=2, a=%g' % a, theta_of(2.0, a, 0.0) / a)
d1 = theta_of(2.0, 0.02, 0.0) / 0.02 - 2 * math.sin(1.0)
d2 = theta_of(2.0, 0.002, 0.0) / 0.002 - 2 * math.sin(1.0)
P('chain-limit error ratio a=0.02 vs 0.002 (O(a^2) -> 100)', d1 / d2)
P('overdamped cutoff k dx = asin(b), b=0.02', math.asin(0.02))

# a pure cosine: g_n = cos(n theta) exactly on the lattice (a=0.6, b=0, m=17)
out, kap = mode_run(17, 0.6, 0.0, 300, 1.0, math.cos(theta_of(17 * math.pi / NSEG, 0.6, 0.0)))
th = theta_of(kap, 0.6, 0.0)
P('cosine mode a=0.6 m=17: g_300 lattice', out[300][13] / math.sin(kap * 13))
P('cosine mode a=0.6 m=17: cos(300 theta)', math.cos(300 * th))

# ---------------------------------------------------------------- 5. the driven steady state
print('\n# ---- 5. the driven steady state (oscillator at bead 0)')
def steady_closed(f, A, b, T, end, nseg=NSEG):
    """Y_i with y_i^n = Im(Y_i z^n), z = e^{i theta}; recurrence Y_{i+1} + Y_{i-1} = 2C Y_i"""
    th = 2 * math.pi * f * dt_of(T)
    C = complex(math.cos(th), b * math.sin(th))
    z = cmath.exp(1j * th)
    lam = C - cmath.sqrt(C * C - 1)
    if abs(lam) > 1:
        lam = 1 / lam
    N = nseg
    # Y_i = p lam^i + q lam^(N-i)
    def row(i):
        return (lam ** i, lam ** (N - i))
    r0 = row(0)
    if end == 'fixed':
        r1 = row(N)
        rhs1 = 0
    elif end == 'loose':
        a1, b1 = row(N)
        a2, b2 = row(N - 1)
        r1 = (a1 - a2, b1 - b2)
        rhs1 = 0
    else:
        a1, b1 = row(N)
        a2, b2 = row(N - 1)
        r1 = (z * a1 - a2, z * b1 - b2)
        rhs1 = 0
    Mx = np.array([[r0[0], r0[1]], [r1[0], r1[1]]], dtype=complex)
    p, q = np.linalg.solve(Mx, np.array([A, rhs1], dtype=complex))
    Y = [p * lam ** i + q * lam ** (N - i) for i in range(N + 1)]
    return Y, lam, p, q, z


def steady_tridiag(f, A, b, T, end, nseg=NSEG):
    """the same Y by a dense linear solve (independent route)"""
    th = 2 * math.pi * f * dt_of(T)
    C = complex(math.cos(th), b * math.sin(th))
    z = cmath.exp(1j * th)
    N = nseg
    Mx = np.zeros((N + 1, N + 1), dtype=complex)
    rhs = np.zeros(N + 1, dtype=complex)
    Mx[0, 0] = 1; rhs[0] = A
    for i in range(1, N):
        Mx[i, i - 1] = 1; Mx[i, i] = -2 * C; Mx[i, i + 1] = 1
    if end == 'fixed':
        Mx[N, N] = 1
    elif end == 'loose':
        Mx[N, N] = 1; Mx[N, N - 1] = -1
    else:
        Mx[N, N] = z; Mx[N, N - 1] = -1
    return list(np.linalg.solve(Mx, rhs))


def steady_bruteforce(f, A, b, T, end, nsteps):
    """run the lattice from rest with the oscillator; return the last two levels and theta"""
    dt = dt_of(T)
    th = 2 * math.pi * f * dt
    a = np.zeros(NSEG + 1); prev = np.zeros(NSEG + 1); cur = np.zeros(NSEG + 1)
    phi = 0.0
    for k in range(1, nsteps + 1):
        phi = phi + 2 * math.pi * f * dt
        prev, cur = step_np(prev, cur, b, end, A * math.sin(phi))
    return prev, cur, phi


def step_np(prev, cur, b, end, yleft):
    n = NSEG
    cur = cur.copy()
    if end == 'fixed':
        cur[n] = 0.0
    elif end == 'loose':
        cur[n] = cur[n - 1]
    else:
        cur[n] = prev[n - 1]
    nxt = np.empty(n + 1)
    inv = 1.0 / (1.0 + b)
    nxt[1:n] = inv * ((b - 1.0) * prev[1:n] + 0.0 * cur[1:n] + 1.0 * (cur[2:n + 1] + cur[0:n - 1]))
    nxt[0] = yleft
    if end == 'fixed':
        nxt[n] = 0.0
    elif end == 'loose':
        nxt[n] = nxt[n - 1]
    else:
        nxt[n] = cur[n - 1]
    return cur, nxt


CASES = [('fixed', 1.5, 0.75, 0.02, 0.8, 4000),
         ('fixed', 1.25, 0.75, 0.002, 0.8, 30000),
         ('loose', 7 * VMAX / (4 * LLOOSE), 0.75, 0.005, 0.8, 16000),
         ('none', 1.5, 0.75, 0.02, 0.8, 4000),
         ('loose', 2.37, 1.1, 0.013, 0.53, 8000),
         ('fixed', 0.6, 0.5, 0.1, 0.2, 3000)]
for (end, f, A, b, T, nbf) in CASES:
    tag = '%s f=%.12g A=%g b=%g T=%g' % (end, f, A, b, T)
    Y, lam, p, q, z = steady_closed(f, A, b, T, end)
    Y2 = steady_tridiag(f, A, b, T, end)
    P('steady ' + tag + ': max_i|Y_i|', max(abs(y) for y in Y))
    for i in (10, 30, 59, 60):
        P('steady ' + tag + ': |Y_%d|' % i, abs(Y[i]))
    P('steady ' + tag + ': Y_30', Y[30])
    P('  closed vs dense solve max diff', max(abs(Y[i] - Y2[i]) for i in range(NSEG + 1)))
    prev, cur, phi = steady_bruteforce(f, A, b, T, end, nbf)
    # at level n the steady state is Im(Y_i e^{i phi_n}) (y_0 = A sin phi_n)
    ss = [(Y[i] * cmath.exp(1j * phi)).imag for i in range(NSEG + 1)]
    P('  brute force (%d steps) max|y - Im(Y e^{i phi})|' % nbf, max(abs(cur[i] - ss[i]) for i in range(NSEG + 1)))
    if end == 'none':
        # the reflection the absorbing end leaves: q lam^0 against p lam^N at the boundary
        P('  no-end reflection |q / (p lam^N)|', abs(q / (p * lam ** NSEG)))

# the no-end reflection coefficient, closed form at the boundary: r = -(z lamR - 1)/(z lamL - 1)
th = 2 * math.pi * 1.5 * dt_of(0.8)
C = complex(math.cos(th), 0.02 * math.sin(th))
lamR = C - cmath.sqrt(C * C - 1)
if abs(lamR) > 1:
    lamR = 1 / lamR
lamL = 1 / lamR
z = cmath.exp(1j * th)
# BC z Y_N = Y_{N-1} with Y_i = p lamR^i + q lamR^(N-i):  q/(p lamR^N) = (z lamR - 1)/(lamR (lamR - z))
P('no-end reflection at bead N, closed form f=1.5 b=0.02', abs((z * lamR - 1) / (lamR * (lamR - z))))
P('   (b=0 would give exactly 0; lamR = e^{-i theta})', abs(z * cmath.exp(-1j * th) - 1))

# resonances
print('\n# ---- resonances: fixed f_n = n v/(2L), loose f_n = (2n-1) v/(4 L_loose)')
for T in (0.8, 0.2):
    v = speed(T)
    P('fixed f_1 T=%g (Hz)' % T, v / (2 * L))
    P('loose f_1 T=%g (Hz)' % T, v / (4 * LLOOSE))
# the response peaks sit at f_n as b -> 0: locate the max of max_i|Y_i| near f_3 (fixed) numerically
for (end, fn, b) in (('fixed', 3 * VMAX / (2 * L), 0.002), ('loose', 7 * VMAX / (4 * LLOOSE), 0.005), ('fixed', 3 * VMAX / (2 * L), 0.0002)):
    g = lambda f: -max(abs(y) for y in steady_closed(f, 0.75, b, 0.8, end)[0])
    res = optimize.minimize_scalar(g, bracket=(fn * 0.99, fn, fn * 1.01), tol=1e-12)
    P('peak of the response near f_n (%s b=%g)' % (end, b), res.x)
    P('  f_n closed form', fn)
    P('  peak height max|Y|/A', -res.fun / 0.75)
# undamped: at f_n the fixed-end response diverges as b -> 0 like 1/(N b) ... measure
for b in (1e-4, 1e-5):
    Y = steady_closed(3 * VMAX / (2 * L), 0.75, b, 0.8, 'fixed')[0]
    P('fixed at f_3 exactly, b=%g: max|Y|/A' % b, max(abs(y) for y in Y) / 0.75)

# ---------------------------------------------------------------- 6. the pulse after crossing (dispersion view)
print('\n# ---- 6. a triangle pulse after crossing the string on a LONG lattice (a < 1 disperses)')
def long_pulse(a, b, A, w, T, xcen_target, nseg=160):
    """drive the pulse at bead 0 of a long lattice (no end far away); stop when the exact
    pulse centre reaches xcen_target (cm).  Returns the final level and the time."""
    v = speed(T)
    dt = a * DX / v
    tstop = xcen_target / v + w / 2
    nsteps = int(math.floor(tstop / dt + 1e-9))
    prev = [0.0] * (nseg + 1); cur = [0.0] * (nseg + 1)
    for k in range(1, nsteps + 1):
        prev, cur = step(prev, cur, a, b, 'none', pulse(k * dt, A, w))
    return cur, nsteps * dt, nsteps
for (a, T) in ((1.0, 0.8), (0.5, 0.8), (0.5, 0.2), (0.05, 0.8)):
    y, t, ns = long_pulse(a, 0.0, 0.75, 0.5, T, 0.75 * L)
    v = speed(T)
    ex = [pulse(t - i * DX / v, 0.75, 0.5) for i in range(len(y))]
    P('long pulse a=%g T=%g: steps' % (a, T), ns)
    P('  max|lattice - exact| over the first 61 beads', max(abs(y[i] - ex[i]) for i in range(61)))
    P('  lattice min over beads 0..60 (ripple)', min(y[:61]))
    P('  lattice max over beads 0..60', max(y[:61]))
    P('  y[30]', y[30])

print('\n# ---- 7. the oscillator and the pulse generator')
P('oscillator: A sin(phi) after 7 steps, f=1.5, T=0.8, A=0.75', 0.75 * math.sin(7 * 2 * math.pi * 1.5 * dt_of(0.8)))
P('triangle at u=0.3', tri(0.3))
P('triangle at u=0.5', tri(0.5))
P('triangle at u=0.8', tri(0.8))
