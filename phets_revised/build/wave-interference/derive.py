#!/usr/bin/env python3
"""derive.py — the Python twin and the reference values for wave-interference.html.

    python3 derive.py > refvals.txt 2> derive_err.txt

Everything selfTest asserts with the tag (python), (scipy) or (twin) is a line of the output
of this script, read in full.  It also writes p2_cie.js (the CIE 1931 table every 5 nm from
380 to 780 nm, read from the CIE's own file).

What is here:
  A. the lattice: the dispersion relation of the 5-point leapfrog at C = 1/2, phase and group
     speeds, the wavenumber at a given frequency and direction (brentq), the stability bound;
  B. Mur's boundary: the exact plane-wave reflection coefficient (first and second order),
     cross-checked against a brute-force 1-D packet simulation;
  C. the calibration of each medium (water, sound, light): cells per wavelength, radians per
     step, seconds per step, and what PhET's fixed step makes of the same frequency;
  D. the twin: the engine's lattice, sources, plane wave, barrier and screen, operation for
     operation, run for four scenarios (JS rounding reproduced: Math.round = floor(x + 0.5));
  E. the plane wave as an exact lattice solution (axis and diagonal);
  F. two sources: nodal count, hyperbola vs far-field screen positions, intensities;
  G. the slits' theory curves at PhET's default;
  H. the far field: special functions against scipy, the aperture renderer's twin (every
     pixel evaluated, no bounding box) through numpy.fft.fft2, the Dirichlet kernel, the
     sampled Gaussian, the Airy comparison;
  I. colour: the CIE table and the sRGB of eight wavelengths.
"""
import io, math, os, sys
import numpy as np
from scipy import special, optimize

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..', '..', '..'))
PI = math.pi
TAU = PI * 2


def jsround(x):
    return math.floor(x + 0.5)


REFS = {}


def P(label, *vals):
    """print a reference line AND record its numbers under the same label for p7_refs.js,
    so every value selfTest asserts is, character for character, a printed line"""
    def f(v):
        if isinstance(v, str):
            return v
        if isinstance(v, (bool, np.bool_)):
            return str(bool(v))
        if isinstance(v, (int, np.integer)):
            return str(int(v))
        return repr(float(v))
    print(label + ' ' + ' '.join(f(v) for v in vals))
    nums = [float(v) if not isinstance(v, (int, np.integer)) else int(v) for v in vals if not isinstance(v, str)]
    assert label not in REFS, 'duplicate reference label: ' + label
    REFS[label] = nums


# ---------------------------------------------------------------------------------------------
# constants (PhET's values, wave-interference 2.0.22)
N_LAT, PAD, VIS = 151, 20, 111
C = 0.5
C2 = C * C
SRC_I, MID = 25, 75
AMP_CAL, PLANE_MAG = 1.2, 0.21
EVENT_RATE = 20 * 111 / 61
VISIT = 1e-3
MUR1 = (C - 1) / (C + 1)
MUR2A = 2 / (C + 1)
MUR2B = C2 / (2 * (C + 1))
C_NM_FS = 299.792458
SCENES = {
    'water': dict(W=10, v=1.65, fmin=0.25, fmax=1, slitW0=1.5, slitD0=3, phetTimeScale=1),
    'sound': dict(W=500, v=34.3, fmin=0.22, fmax=0.44, slitW0=90, slitD0=200, phetTimeScale=2.4187847116091334),
    'light': dict(W=5000, v=C_NM_FS, fmin=C_NM_FS / 780, fmax=C_NM_FS / 380, slitW0=500, slitD0=1500,
                  phetTimeScale=1416.5 / 511.034),
}
SCREEN_HIST = 180

print('# derive.py for wave-interference.html — every line below is a reference value')
P('EVENT_RATE', EVENT_RATE)
P('MUR1 MUR2A MUR2B', MUR1, MUR2A, MUR2B)

# ---------------------------------------------------------------------------------------------
# A. the dispersion relation
print('\n# A. dispersion: sin^2(Om/2) = C^2 [sin^2(kx/2) + sin^2(ky/2)]')


def lat_omega(kx, ky):
    return 2 * math.asin(C * math.sqrt(math.sin(kx / 2) ** 2 + math.sin(ky / 2) ** 2))


def lat_k(Om, th):
    c, s = math.cos(th), math.sin(th)
    hi = PI / max(abs(c), abs(s))
    return optimize.brentq(lambda k: lat_omega(k * c, k * s) - Om, 1e-12, hi, xtol=1e-15, rtol=1e-15)


def group_speed(k, th):
    kx, ky = k * math.cos(th), k * math.sin(th)
    return C2 * math.hypot(math.sin(kx), math.sin(ky)) / math.sin(lat_omega(kx, ky))


for kx, ky in [(0.3, 0.0), (0.2, 0.2), (1.0, 0.4), (PI, PI)]:
    P('latOmega %r %r' % (kx, ky), lat_omega(kx, ky))
P('max Om (k = (pi, pi)) = 2 asin(C sqrt 2)', 2 * math.asin(C * math.sqrt(2)), ' stability 2C^2 =', 2 * C2)
for Om, thd in [(0.27, 0), (0.27, 45), (0.27, 30), (0.1, 60), (0.36, 45)]:
    th = math.radians(thd)
    k = lat_k(Om, th)
    P('latK Om=%r th=%d' % (Om, thd), k)
    # numeric group speed as a cross-check of the closed form: dOm/dk along th
    h = 1e-6
    num = (lat_omega((k + h) * math.cos(th), (k + h) * math.sin(th)) - lat_omega((k - h) * math.cos(th), (k - h) * math.sin(th))) / (2 * h)
    P('  speeds Om=%r th=%d: phase, |grad Om| (closed), dOm/dk along k (numeric; equals |grad Om| only where v_g is parallel to k, 0 and 45 deg)' % (Om, thd),
      Om / k, group_speed(k, th), num)
for Nl in [8.436, 11.345, 17.316, 29.33, 73.33]:
    k = TAU / Nl
    for thd in [0, 45]:
        th = math.radians(thd)
        P('speeds Nl=%r th=%d vp/C vg/C' % (Nl, thd), lat_omega(k * math.cos(th), k * math.sin(th)) / k / C, group_speed(k, th) / C)
# anisotropy at a fixed frequency: the wavelength along the diagonal vs the axis
for Nl in [8.436, 11.345, 29.33]:
    Om = 2 * math.asin(C * math.sin(PI / Nl))
    P('diagonal wavelength / axial at Nl=%r' % Nl, (TAU / lat_k(Om, PI / 4)) / Nl)

# ---------------------------------------------------------------------------------------------
# B. Mur's boundary: the exact reflection of a plane wave
print('\n# B. Mur reflection |R| (plane-wave ansatz), and a brute-force packet check')


def mur_R(kx, ky, order):
    z = complex(math.cos(lat_omega(kx, ky)), -math.sin(lat_omega(kx, ky)))
    if order == 1:
        Pp, Q = z + MUR1, 1 + MUR1 * z
    else:
        B = MUR2A - MUR2B * (2 - 2 * math.cos(ky))
        Pp, Q = z - MUR1 / z - B, -1 / z + MUR1 * z + B
    ek = complex(math.cos(kx), math.sin(kx))
    return abs((Q / ek - Pp) / (Pp - ek * Q))


for Nl, thd in [(11.345, 0), (11.345, 30), (11.345, 45), (11.345, 60), (29.33, 0), (29.33, 45), (73.33, 0), (8.436, 45)]:
    k = TAU / Nl
    th = math.radians(thd)
    P('murR Nl=%r th=%d order1 order2' % (Nl, thd), mur_R(k * math.cos(th), k * math.sin(th), 1),
      mur_R(k * math.cos(th), k * math.sin(th), 2))
P('continuum Mur-1 at 45 deg |cos-1|/(cos+1)', (1 - math.cos(PI / 4)) / (1 + math.cos(PI / 4)))


def packet_R(kx, ky, order):
    """brute force: a 1-D reduction (transverse mode cos(ky j)) with the same boundary formula"""
    Om = lat_omega(kx, ky)
    Nl = TAU / math.hypot(kx, ky)
    width = 4 * Nl
    kyt = 2 - 2 * math.cos(ky)

    def run(nx, steps):
        x = np.arange(nx, dtype=float)
        env = np.exp(-0.5 * ((x - 300) / width) ** 2)
        u = env * np.cos(kx * (x - 300))
        up = env * np.cos(kx * (x - 300) + Om)
        for n in range(steps):
            un = np.empty_like(u)
            un[1:-1] = 2 * u[1:-1] - up[1:-1] + C2 * (u[2:] + u[:-2] - kyt * u[1:-1] - 2 * u[1:-1])
            e, i = nx - 1, nx - 2
            if order == 1:
                un[e] = u[i] + MUR1 * (un[i] - u[e])
            else:
                un[e] = -up[i] + MUR1 * (un[i] + up[e]) + MUR2A * (u[e] + u[i]) + MUR2B * (-kyt * u[e] - kyt * u[i])
            un[0] = u[1] + MUR1 * (un[1] - u[0])
            up, u = u, un
        return u
    vg = C2 * math.sin(kx) / math.sin(Om)
    steps = int((2 * (700 - 300) - 60) / vg)
    ub = run(700, steps)
    ur = run(3700, steps)[:700]
    ui = run(700, 0)
    return math.sqrt(np.sum((ub - ur)[:695] ** 2) / np.sum(ui ** 2))


for Nl, thd, order in [(11.345, 45, 1), (11.345, 45, 2), (11.345, 30, 1), (8.436, 60, 2)]:
    k = TAU / Nl
    th = math.radians(thd)
    a = mur_R(k * math.cos(th), k * math.sin(th), order)
    b = packet_R(k * math.cos(th), k * math.sin(th), order)
    P('CHECK murR ansatz vs packet Nl=%r th=%d order=%d' % (Nl, thd, order), a, b, ' rel diff', abs(a - b) / a)

# ---------------------------------------------------------------------------------------------
# C. calibration
print('\n# C. calibration: dt solved so the axial wavelength is exactly v/f')


def dx_of(S):
    return S['W'] / VIS


def cells_per_wave(S, f):
    return S['v'] / f / dx_of(S)


def omega_step(Nl):
    return 2 * math.asin(C * math.sin(PI / Nl))


def step_dt(S, f):
    return omega_step(cells_per_wave(S, f)) / (TAU * f)


def phet_lambda(S, f):
    dt = S['phetTimeScale'] / EVENT_RATE
    Om = TAU * f * dt
    s = math.sin(Om / 2) / C
    return TAU / (2 * math.asin(s)) * dx_of(S)


for sid in ['water', 'sound', 'light']:
    S = SCENES[sid]
    f0 = 0.5 * (S['fmin'] + S['fmax'])
    P('%s dx f0 lambda0' % sid, dx_of(S), f0, S['v'] / f0)
    for tag, f in [('fmin', S['fmin']), ('f0', f0), ('fmax', S['fmax'])]:
        Nl = cells_per_wave(S, f)
        Om = omega_step(Nl)
        P('  %s %s f Nl Om dt period_steps' % (sid, tag), f, Nl, Om, step_dt(S, f), TAU / Om)
        P('  %s %s PhET lambda, PhET/true - 1' % (sid, tag), phet_lambda(S, f), phet_lambda(S, f) / (S['v'] / f) - 1)
    P('  %s PhET dt per step, long-wave speed on PhET lattice' % sid, S['phetTimeScale'] / EVENT_RATE,
      C * dx_of(S) / (S['phetTimeScale'] / EVENT_RATE))
print('PhET default light wavelength c/((fmin+fmax)/2):', repr(C_NM_FS / (0.5 * (SCENES['light']['fmin'] + SCENES['light']['fmax']))))

# ---------------------------------------------------------------------------------------------
# D. the twin
print('\n# D. the twin: the engine, operation for operation')


class Lat:
    def __init__(self, n, pad=PAD):
        self.nx = self.ny = n
        self.pad = pad
        self.u = np.zeros((n, n))
        self.up = np.zeros((n, n))
        self.un = np.zeros((n, n))
        self.vis = np.zeros((n, n), dtype=bool)

    def step(self):
        u, up, un = self.u, self.up, self.un
        c = u[1:-1, 1:-1]
        v = 2 * c - up[1:-1, 1:-1] + C2 * (u[1:-1, 2:] + u[1:-1, :-2] + u[2:, 1:-1] + u[:-2, 1:-1] - 4 * c)
        un[1:-1, 1:-1] = v
        self.vis[1:-1, 1:-1] |= (v > VISIT) | (v < -VISIT)
        # left (e col 0, i col 1) and right edges, rows 1..ny-2, tangent = rows
        for e, i in [(0, 1), (-1, -2)]:
            un[1:-1, e] = (-up[1:-1, i] + MUR1 * (un[1:-1, i] + up[1:-1, e]) + MUR2A * (u[1:-1, e] + u[1:-1, i])
                           + MUR2B * (u[2:, e] - 2 * u[1:-1, e] + u[:-2, e] + u[2:, i] - 2 * u[1:-1, i] + u[:-2, i]))
        for e, i in [(0, 1), (-1, -2)]:
            un[e, 1:-1] = (-up[i, 1:-1] + MUR1 * (un[i, 1:-1] + up[e, 1:-1]) + MUR2A * (u[e, 1:-1] + u[i, 1:-1])
                           + MUR2B * (u[e, 2:] - 2 * u[e, 1:-1] + u[e, :-2] + u[i, 2:] - 2 * u[i, 1:-1] + u[i, :-2]))
        for (cj, ci), (aj, ai) in [((0, 0), (0, 1)), ((0, -1), (0, -2)), ((-1, 0), (-1, 1)), ((-1, -1), (-1, -2))]:
            un[cj, ci] = u[aj, ai] + MUR1 * (un[aj, ai] - u[cj, ci])
        self.up, self.u, self.un = u, un, up


class Run:
    def __init__(self, sid, mode='point', nsrc=1, n=N_LAT):
        self.lat = Lat(n)
        self.mode, self.nsrc = mode, nsrc
        self.A = 8.0
        self.src = [True, True]
        self.cont = True
        self.pulse_on, self.pulse_phi = False, 0.0
        self.plane_on, self.m, self.barrier, self.bcol = True, 0, 'one', MID
        self.set_scene(sid)

    def set_scene(self, sid):
        S = SCENES[sid]
        self.sid = sid
        self.sep = S['slitD0']
        self.slitW, self.slitD = S['slitW0'], S['slitD0']
        self.set_f(0.5 * (S['fmin'] + S['fmax']))
        self.clear()

    def set_f(self, f):
        S = SCENES[self.sid]
        self.f = min(max(f, S['fmin']), S['fmax'])
        self.Nl = cells_per_wave(S, self.f)
        self.Om = omega_step(self.Nl)
        self.dt = step_dt(S, self.f)

    def clear(self):
        n = self.lat.nx
        self.lat = Lat(n)
        self.phi = 0.0
        self.t = 0.0
        self.n = 0
        self.m = 0
        self.rows = n - 2 * PAD
        self.buf = np.zeros((SCREEN_HIST, self.rows))
        self.head, self.count = 0, 0

    def source_rows(self):
        h = jsround(self.sep / (2 * dx_of(SCENES[self.sid])))
        mid = (self.lat.ny - 1) / 2
        return [int(mid - h), int(mid + h)] if self.nsrc == 2 else [int(mid)]

    def slit_open(self, j):
        dx = dx_of(SCENES[self.sid])
        mid = (self.lat.ny - 1) / 2
        y = j - mid
        if self.barrier == 'none':
            return True
        a = self.slitW / (2 * dx)
        if self.barrier == 'one':
            return abs(y) < a
        c = self.slitD / (2 * dx)
        return abs(y - c) < a or abs(y + c) < a

    def step(self):
        L = self.lat
        L.step()
        self.phi += self.Om
        if self.mode == 'point':
            self.set_point()
        else:
            self.set_plane()
        self.t += self.dt
        self.n += 1
        col = L.nx - L.pad - 1
        self.buf[self.head, :] = L.u[L.pad:L.pad + self.rows, col]
        self.head = (self.head + 1) % SCREEN_HIST
        self.count = min(self.count + 1, SCREEN_HIST)

    def set_point(self):
        amp = self.A * AMP_CAL
        val = None
        if self.cont:
            val = amp * math.sin(self.phi)
        elif self.pulse_on:
            self.pulse_phi += self.Om
            if self.pulse_phi < TAU:
                val = amp * math.sin(self.pulse_phi)
            else:
                val = 0.0
                self.pulse_on = False
        if val is None:
            return
        ci = self.lat.pad + SRC_I - PAD
        for s, r in enumerate(self.source_rows()):
            if self.src[s]:
                self.lat.u[r, ci] = val

    def set_plane(self):
        L = self.lat
        iR = L.nx - L.pad if self.barrier == 'none' else self.bcol
        k = TAU / self.Nl
        amp = PLANE_MAG * self.A
        front = self.m * self.Om / k if self.plane_on else -1
        blocked = np.array([not self.slit_open(j) for j in range(L.ny)])
        for i in range(L.pad, iR + 1):
            x = i - L.pad
            val = amp * math.sin(self.Om * self.m - k * x) if (self.plane_on and x <= front) else 0.0
            colv = np.full(L.ny, val)
            if i == iR and self.barrier != 'none':
                colv[blocked] = 0.0
            L.u[:, i] = colv
            L.up[:, i] = colv
        if self.plane_on:
            self.m += 1

    def screen_window(self):
        Pp = TAU / self.Om
        m = max(1, jsround(90 / Pp))
        return max(1, min(SCREEN_HIST, jsround(m * Pp)))

    def screen_intensity(self):
        w = min(self.count, self.screen_window())
        acc = np.zeros(self.rows)
        for s in range(1, w + 1):
            v = self.buf[(self.head - s + SCREEN_HIST) % SCREEN_HIST]
            acc += v * v
        return acc / w


def report(tag, R, cells):
    u = R.lat.u
    for (i, j) in cells:
        P('%s u(%d,%d)' % (tag, i, j), u[j, i])
    visu = u[PAD:PAD + VIS, PAD:PAD + VIS]
    P('%s max|u| visible, sum u^2 visible, visited cells' % tag, np.max(np.abs(visu)), np.sum(visu * visu), int(np.sum(R.lat.vis)))
    P('%s t n phi' % tag, R.t, R.n, R.phi)


CELLS = [(22, 75), (10, 75), (45, 75), (60, 75), (90, 75), (60, 50), (100, 100), (130, 40), (140, 75), (75, 140)]
# (a) the ripple tank: water at 0.625 Hz, amplitude 8, one continuous source, 240 steps
Ra = Run('water')
for _ in range(240):
    Ra.step()
report('TWIN tank', Ra, CELLS)
# (b) two sources: sound, amplitude 10, separation 200 cm, 240 steps
Rb = Run('sound', 'point', 2)
Rb.A = 10.0
for _ in range(240):
    Rb.step()
P('TWIN two source rows', *Rb.source_rows())
# the rows at PhET's other default separations: water 3 cm = 16.65 cells, light 1500 nm = 16.65 cells
# (a fraction >= 1/2, where round and floor differ; the sound default 22.2 cannot tell them apart)
P('source rows at the water and light defaults', *(Run('water', 'point', 2).source_rows() + Run('light', 'point', 2).source_rows()))
report('TWIN two', Rb, CELLS)
# (c) the slits: light, plane wave, two slits (500 nm, 1500 nm), barrier at 75, amplitude 10, 400 steps
Rc = Run('light', 'plane', 1)
Rc.A = 10.0
Rc.barrier = 'two'
for _ in range(400):
    Rc.step()
report('TWIN slits', Rc, CELLS + [(76, 75), (76, 58), (76, 92)])
open_rows = [j for j in range(N_LAT) if Rc.slit_open(j)]
P('TWIN slits open rows: count first last', len(open_rows), open_rows[0], open_rows[-1])
Is = Rc.screen_intensity()
P('TWIN slits screen window', Rc.screen_window())
for r in [55, 45, 65, 30, 80, 10]:
    P('TWIN slits screen I[%d]' % r, Is[r])
P('TWIN slits screen argmax, max', int(np.argmax(Is)), np.max(Is))
# (d) a pulse: water, pulse mode fired at the start, amplitude 8, 150 steps
Rd = Run('water')
Rd.cont = False
Rd.pulse_on, Rd.pulse_phi = True, 0.0
for _ in range(150):
    Rd.step()
report('TWIN pulse', Rd, CELLS)
P('TWIN pulse finished', int(not Rd.pulse_on))
# (e) one slit, sound, barrier moved to 60, 300 steps
Re = Run('sound', 'plane', 1)
Re.A = 10.0
Re.barrier = 'one'
Re.bcol = 60
for _ in range(300):
    Re.step()
report('TWIN oneslit', Re, [(61, 75), (61, 60), (100, 75), (120, 90), (40, 75)])
open_rows = [j for j in range(N_LAT) if Re.slit_open(j)]
P('TWIN oneslit open rows: count first last', len(open_rows), open_rows[0], open_rows[-1])

# measured wavelength along the axis in the tank run (zero crossings on row 75, i = 60..128)
row = Ra.lat.u[75, :]
zc = []
for i in range(60, 128):
    if row[i] == 0 or row[i] * row[i + 1] < 0:
        zc.append(i + row[i] / (row[i] - row[i + 1]))
if len(zc) >= 3:
    P('DIAGNOSTIC ONLY (240 steps: transient and near field, not asserted) tank half-wavelengths, mean, Nl/2',
      *np.diff(zc), np.mean(np.diff(zc)), Ra.Nl / 2)

# ---------------------------------------------------------------------------------------------
# E. the plane wave is an exact lattice solution (interior, before the edges can matter)
print('\n# E. analytic plane waves on the lattice')
for thd in [0, 45]:
    th = math.radians(thd)
    Nl = 11.345
    Om = omega_step(Nl)
    k = TAU / Nl if thd == 0 else lat_k(Om, th)
    kx, ky = k * math.cos(th), k * math.sin(th)
    n = 61
    L = Lat(n, 20)
    J, I = np.mgrid[0:n, 0:n]
    L.u[:] = np.sin(kx * I + ky * J)
    L.up[:] = np.sin(kx * I + ky * J + Om)
    for s in range(20):
        L.step()
    ana = np.sin(kx * I + ky * J - 20 * Om)
    err = np.max(np.abs((L.u - ana)[21:40, 21:40]))
    P('plane wave th=%d, 20 steps, max interior error' % thd, err)

# ---------------------------------------------------------------------------------------------
# F. two sources
print('\n# F. two sources: the path difference')


def hyper_y(d, D, L):
    a = D / 2
    return a * math.sqrt(1 + L * L / (d * d / 4 - a * a))


def far_y(d, D, L):
    a = D / 2
    return L * a / math.sqrt(d * d / 4 - a * a)


def nodal_count(x):
    return 2 * max(0, math.ceil(x - 0.5))


for x in [0.3, 0.5, 0.51, 1.0, 1.5, 2.5, 3.2, 7.9]:
    P('nodalCount d/lambda=%r' % x, nodal_count(x))
for d, D, L in [(3.2, 0.5, 10.0), (3.2, 2.5, 10.0), (3.2, 2.5, 100.0), (8.0, 0.5, 4.0)]:
    y1, y2 = hyper_y(d, D, L), far_y(d, D, L)
    r1, r2 = math.hypot(L, y1 + d / 2), math.hypot(L, y1 - d / 2)
    P('hyperY farY d=%r Delta=%r L=%r (and r1-r2 at hyperY)' % (d, D, L), y1, y2, r1 - r2)


def two_I(x, y, d, k):
    r1, r2 = math.hypot(x, y + d / 2), math.hypot(x, y - d / 2)
    return 1 / r1 + 1 / r2 + 2 * math.cos(k * (r1 - r2)) / math.sqrt(r1 * r2)


def two_far(x, y, d, k):
    return math.cos(k * d * y / (2 * math.hypot(x, y))) ** 2


for x, y, d, lam in [(10.0, 0.0, 3.2, 1.0), (10.0, 1.3, 3.2, 1.0), (4.0, 2.0, 2.0, 0.7)]:
    k = TAU / lam
    P('twoSourceI twoSourceFar x=%r y=%r d=%r lam=%r' % (x, y, d, lam), two_I(x, y, d, k), two_far(x, y, d, k))

# does the lattice put its nodal lines on the hyperbolae?  Two light sources (PhET's default),
# steady state, the peak |u| of every cell over two periods; the minima down three columns,
# parabola-refined, against r1 - r2 = (m + 1/2) lambda with the lattice's own source rows.
Rn = Run('light', 'point', 2)
Rn.A = 10.0
for _ in range(600):
    Rn.step()
amp = np.zeros((N_LAT, N_LAT))
for _ in range(2 * int(round(TAU / Rn.Om)) + 2):
    Rn.step()
    amp = np.maximum(amp, np.abs(Rn.lat.u))
sr = Rn.source_rows()
dcell = sr[1] - sr[0]
kc = TAU / Rn.Nl


def minima(a):
    out = []
    for j in range(PAD + 2, PAD + VIS - 2):
        if a[j] < a[j - 1] and a[j] <= a[j + 1]:
            den = a[j - 1] - 2 * a[j] + a[j + 1]
            out.append(j + (0.5 * (a[j - 1] - a[j + 1]) / den if den > 0 else 0.0))
    return out


worst = worst_c = 0.0
nmatch = 0
signed = []
for col in [80, 105, 125]:
    xc = col - (PAD + SRC_I - PAD)
    mins = minima(amp[:, col])
    cmins = minima(np.array([math.sqrt(two_I(xc, j - MID, dcell, kc)) for j in range(N_LAT)]))
    for m in range(0, 20):
        D = (m + 0.5) * Rn.Nl
        if D >= dcell:
            break
        for sg in (1, -1):
            yh = MID + sg * hyper_y(dcell, D, xc)
            if PAD + 3 < yh < PAD + VIS - 3 and mins:
                near = min(mins, key=lambda q: abs(q - yh))
                worst = max(worst, abs(near - yh))
                signed.append(sg * (near - yh))
                worst_c = max(worst_c, abs(min(cmins, key=lambda q: abs(q - yh)) - yh))
                nmatch += 1
P('nodal lines vs the hyperbolae: crossings matched, lattice worst distance (cells), continuum 1/sqrt(r) worst, lattice mean outward shift',
  nmatch, worst, worst_c, float(np.mean(signed)))

# ---------------------------------------------------------------------------------------------
# G. the slits' theory at PhET's default (light, two slits 500/1500 nm, barrier 75)
print('\n# G. slits theory (Rayleigh-Sommerfeld far-zone kernel and Fraunhofer), normalised to peak')
S = SCENES['light']
dx = dx_of(S)
lam = S['v'] / (0.5 * (S['fmin'] + S['fmax']))
k = TAU / lam
X = (130 - 75) * dx
opn = [(j - 75) * dx for j in range(N_LAT) if Rc.slit_open(j)]
hi = [j for j in range(N_LAT) if Rc.slit_open(j) and j > 75]
lo = [j for j in range(N_LAT) if Rc.slit_open(j) and j < 75]
a_eff = len(hi) * dx
d_eff = ((hi[0] + hi[-1]) / 2 - (lo[0] + lo[-1]) / 2) * dx
P('slits effective a (cells) d (cells)', len(hi), (hi[0] + hi[-1]) / 2 - (lo[0] + lo[-1]) / 2)
ex = np.zeros(VIS)
ff = np.zeros(VIS)
for r in range(VIS):
    ys = (PAD + r - 75) * dx
    er = ei = 0.0
    for yj in opn:
        rr = math.hypot(X, ys - yj)
        w = X / (rr * math.sqrt(rr))
        er += w * math.cos(k * rr)
        ei += w * math.sin(k * rr)
    ex[r] = er * er + ei * ei
    sn = ys / math.hypot(X, ys)
    b = k * a_eff * sn / 2
    s2 = 1.0 if abs(b) < 1e-4 else (math.sin(b) / b) ** 2
    ff[r] = s2 * math.cos(k * d_eff * sn / 2) ** 2
ex /= ex.max()
ff /= ff.max()
for r in [55, 45, 65, 30, 80, 10]:
    P('theory exact far [%d]' % r, ex[r], ff[r])
# the lattice at steady state against both curves: how well PhET's screen is predicted
for steps in [400, 900, 1400]:
    Rs = Run('light', 'plane', 1)
    Rs.A = 10.0
    Rs.barrier = 'two'
    for _ in range(steps):
        Rs.step()
    Il = Rs.screen_intensity()
    Il = Il / Il.max()
    P('lattice screen vs Rayleigh-Sommerfeld, vs Fraunhofer after %d steps: max |diff|, rms' % steps,
      np.max(np.abs(Il - ex)), math.sqrt(np.mean((Il - ex) ** 2)), np.max(np.abs(Il - ff)), math.sqrt(np.mean((Il - ff) ** 2)))
# where the first minima fall on the screen: lattice, Rayleigh-Sommerfeld, Fraunhofer (rows from the centre)
def first_min(a):
    c = 55
    for r in range(c + 1, len(a) - 1):
        if a[r] < a[r - 1] and a[r] <= a[r + 1]:
            return r - c
    return -1
P('first minimum (rows above centre): lattice RS Fraunhofer', first_min(Il), first_min(ex), first_min(ff))

# ---------------------------------------------------------------------------------------------
# H. the far field
print('\n# H. the far field')
LAM0 = 2 / (1 / 780 + 1 / 380)
NF = 256
PX = (4 / 3) / NF
SIN_PER_BIN = LAM0 * 1e-6 / (NF * PX)
P('LAM0 PX SIN_PER_BIN', LAM0, PX, SIN_PER_BIN)
for x in [1e-5, 0.5, 3.8317059702075125, 7.015586669815619, 10.0, 16.9, 17.0, 17.1, 25.0, 40.0]:
    P('J1(%r) J0 (scipy)' % x, special.j1(x), special.j0(x))
for v in [5e-5, 1.0, 3.8317059702075125, 5.1356223018406826, 10.0]:
    t = 1.0 if v == 0 else (2 * special.j1(v) / v) ** 2
    P('airy(%r) (scipy)' % v, t)
for b in [5e-5, 0.5, PI / 2, 3.0, 4.493409457909064]:
    P('sinc2(%r)' % b, (math.sin(b) / b) ** 2)
for g, Ng in [(0.4, 2), (0.4, 5), (PI, 3), (1.0 + 1e-7, 1)]:
    sg = math.sin(g)
    P('gratingFactor(%r,%d)' % (g, Ng), 1.0 if Ng <= 1 else (math.sin(Ng * g) / sg) ** 2 / (Ng * Ng))

# the disorder vectors (Park-Miller, seed 20260918)
xs = 20260918 % 2147483647
DV = []
for q in range(16):
    xs = (48271 * xs) % 2147483647
    a = TAU * (xs / 2147483647)
    xs = (48271 * xs) % 2147483647
    r = math.sqrt(xs / 2147483647)
    DV.append((r * math.cos(a), r * math.sin(a)))
P('disorder vector 0', *DV[0])
P('disorder vector 15', *DV[15])
FIG_HEAD = (0, -0.38, 0.12)
FIG_CAPS = [(0, -0.25, 0, 0.1, 0.055), (0, 0.1, -0.12, 0.47, 0.035), (0, 0.1, 0.12, 0.47, 0.035),
            (0, -0.17, -0.2, 0.05, 0.03), (0, -0.17, 0.17, -0.3, 0.03), (0.17, -0.3, 0.22, -0.47, 0.03)]


def seg_d2(px, py, ax, ay, bx, by):
    dx_, dy_ = bx - ax, by - ay
    L2 = dx_ * dx_ + dy_ * dy_
    t = ((px - ax) * dx_ + (py - ay) * dy_) / L2 if L2 > 0 else 0 * px
    t = np.clip(t, 0, 1)
    ex_, ey_ = ax + t * dx_ - px, ay + t * dy_ - py
    return ex_ * ex_ + ey_ * ey_


def render(ap, lam, prm):
    """twin of renderAperture: every pixel, Q = 4 sub-samples, the same arithmetic"""
    N, h, Q = NF, NF // 2, 4
    s = LAM0 / lam
    t = np.zeros((N, N))
    if ap == 'rect':
        iw = jsround(prm['recW'] * s / (2 * PX))
        ih = jsround(prm['recH'] * s / (2 * PX))
        t[h - ih:h + ih, h - iw:h + iw] = 1.0
        return t, iw, ih
    J, I = np.mgrid[0:N, 0:N]
    if ap == 'gauss':
        sx, sy = s * prm['gauSx'], s * prm['gauSy']
        x = (I - h + 0.5) * PX
        y = (J - h + 0.5) * PX
        return np.exp(-(x * x / (2 * sx * sx) + y * y / (2 * sy * sy))), None, None
    cnt = np.zeros((N, N))
    for qy in range(Q):
        for qx in range(Q):
            y = (J - h + (qy + 0.5) / Q) * PX
            x = (I - h + (qx + 0.5) / Q) * PX
            if ap == 'ellipse':
                rx = s * prm['ellD'] / 2
                ry = rx * math.sqrt(1 - prm['ellE'] * prm['ellE'])
                ins = (x / rx) * (x / rx) + (y / ry) * (y / ry) < 1
            elif ap == 'cs':
                c = 26 * PX * s
                r = s * prm['csD'] / 2
                hh = s * prm['csW'] / 2
                ins = ((x + c) * (x + c) + (y + c) * (y + c) < r * r) | ((np.abs(x - c) < hh) & (np.abs(y - c) < hh))
            elif ap == 'disorder':
                p = prm['disP']
                r = s * prm['disD'] / 2
                f = prm['disL'] / 4 * 0.3 * p
                ins = np.zeros((N, N), dtype=bool)
                for a in range(4):
                    for b in range(4):
                        v = DV[4 * a + b]
                        cx, cy = s * ((a - 1.5) * p + f * v[0]), s * ((b - 1.5) * p + f * v[1])
                        ddx, ddy = x - cx, y - cy
                        ins |= ddx * ddx + ddy * ddy < r * r
            elif ap == 'figure':
                H = s * prm['figH']
                rot = prm['figR'] * PI / 180
                co, si = math.cos(rot), math.sin(rot)
                u = (x * co + y * si) / H
                v = (-x * si + y * co) / H
                ins = (u - FIG_HEAD[0]) * (u - FIG_HEAD[0]) + (v - FIG_HEAD[1]) * (v - FIG_HEAD[1]) < FIG_HEAD[2] * FIG_HEAD[2]
                for cp in FIG_CAPS:
                    ins |= seg_d2(u, v, cp[0], cp[1], cp[2], cp[3]) < cp[4] * cp[4]
            elif ap == 'slits':
                n = jsround(prm['sltN'])
                a = s * prm['sltW'] / 2
                d = s * prm['sltD']
                hh = s * 0.3 / 2
                x0 = -(n - 1) / 2 * d
                ins = np.zeros((N, N), dtype=bool)
                for q in range(n):
                    ins |= np.abs(x - (x0 + q * d)) < a
                ins &= ~(np.abs(y) >= hh)
            cnt += ins
    return cnt / (Q * Q), None, None


APS = [
    ('ellipse', 'ellipse_default', LAM0, dict(ellD=0.1, ellE=0.0)),
    ('ellipse', 'ellipse_e08_650', 650.0, dict(ellD=0.2, ellE=0.8)),
    ('rect', 'rect_450', 450.0, dict(recW=0.1, recH=0.2)),
    ('cs', 'cs_default', LAM0, dict(csD=0.05, csW=0.05)),
    ('disorder', 'disorder_L2', LAM0, dict(disD=0.05, disP=0.1, disL=2)),
    ('figure', 'figure_600', 600.0, dict(figH=0.2, figR=30.0)),
    ('gauss', 'gauss_default', LAM0, dict(gauSx=0.03, gauSy=0.02)),
    ('slits', 'slits_2', LAM0, dict(sltN=2, sltW=0.03, sltD=0.1)),
]
BINS = [(0, 0), (3, 0), (0, 5), (7, 4), (-11, 2), (20, -13)]
for ap, name, lam, prm in APS:
    t, iw, ih = render(ap, lam, prm)
    F = np.fft.fft2(t)                        # F[k2, k1] = sum t[j, i] exp(-2 pi i (k1 i + k2 j)/N)
    mag = np.abs(F)
    P('AP %s lam sum(t) max|F|' % name, lam, np.sum(t), mag.max())
    for (k1, k2) in BINS:
        P('AP %s |F|(%d,%d)' % (name, k1, k2), mag[k2 % NF, k1 % NF])
    P('AP %s PhET display at (3,0)' % name, math.log(0.01 * mag[0, 3] + 1) / math.log(0.01 * mag.max() + 1))
    if ap == 'rect':
        M = 2 * iw
        P('AP rect iw ih', iw, ih)
        # at lambda0 the half-height is 19.2 px: round gives 19 where ceil would give 20
        s0 = 1.0
        P('AP rect at LAM0 (0.1 x 0.2 mm): iw ih', jsround(0.1 * s0 / (2 * PX)), jsround(0.2 * s0 / (2 * PX)))
        for k1 in [1, 5, 13, 40, 127]:
            dk = math.sin(PI * k1 * M / NF) / math.sin(PI * k1 / NF)
            P('AP rect Dirichlet k=%d |F|(k,0), 2ih*|D|' % k1, mag[0, k1], 2 * ih * abs(dk))
    if ap == 'gauss':
        s = LAM0 / lam
        sxp, syp = s * prm['gauSx'] / PX, s * prm['gauSy'] / PX      # sigma in pixels
        for k1 in [0, 4, 9, 17]:
            ana = 2 * PI * sxp * syp * math.exp(-2 * PI * PI * sxp * sxp * (k1 / NF) ** 2)
            P('AP gauss k=%d |F|(k,0) vs 2 pi sx sy exp(-2 pi^2 sx^2 f^2)' % k1, mag[0, k1], ana, abs(mag[0, k1] - ana) / ana)
    if ap == 'ellipse' and prm['ellE'] == 0:
        s = LAM0 / lam
        D = prm['ellD']
        dev = 0.0
        for k1 in range(0, 11):
            sinT = k1 * SIN_PER_BIN
            v = PI * D * sinT / (lam * 1e-6)
            ai = 1.0 if v == 0 else (2 * special.j1(v) / v) ** 2
            dev = max(dev, abs((mag[0, k1] / mag[0, 0]) ** 2 - ai))
        P('AP ellipse default: max |FFT cut - Airy| for k <= 10 (intensity)', dev)
        # first dark ring: where the sampled cut is least, around the Airy zero
        zero_bins = 3.8317059702075125 / (PI * D / (lam * 1e-6) * SIN_PER_BIN)
        P('AP ellipse default: Airy first zero at bin', zero_bins)
        cut = (mag[0, :40] / mag[0, 0]) ** 2
        P('AP ellipse default: argmin of the cut over 12..20, its value', 12 + int(np.argmin(cut[12:21])), float(np.min(cut[12:21])))

# a direct DFT of the default ellipse at two bins, as a brute-force check of numpy itself
t, _, _ = render('ellipse', LAM0, dict(ellD=0.1, ellE=0.0))
for (k1, k2) in [(3, 0), (7, 4)]:
    J, I = np.mgrid[0:NF, 0:NF]
    ph = -TAU * ((k1 * I + k2 * J) % NF) / NF
    P('direct DFT |F|(%d,%d)' % (k1, k2), abs(np.sum(t * np.exp(1j * ph))))

# ---------------------------------------------------------------------------------------------
# I. colour
print('\n# I. colour: CIE 1931 2-degree, every 5 nm from 380 to 780 nm (the CIE file, verbatim)')
csv = os.path.join(HERE, '..', 'blackbody-spectrum', 'CIE_xyz_1931_2deg.csv')
rows = {}
for line in io.open(csv, encoding='utf-8'):
    p = line.strip().split(',')
    if len(p) < 4:
        continue
    try:
        nm = int(float(p[0]))
    except ValueError:
        continue
    rows[nm] = (p[1], p[2], p[3])
tab = [(nm,) + rows[nm] for nm in range(380, 781, 5)]
with io.open(os.path.join(HERE, 'p2_cie.js'), 'w', encoding='utf-8') as fh:
    fh.write('\n/* CIE 1931 2-degree colour-matching functions x-bar, y-bar, z-bar, every 5 nm from 380 to 780 nm:\n'
             '   every fifth row of CIE_xyz_1931_2deg.csv exactly as the CIE publishes it (DOI 10.25039/CIE.DS.xvudnb9b,\n'
             '   ISO/CIE 11664-1:2019; the file sits in build/blackbody-spectrum/).  Written by\n'
             '   build/wave-interference/derive.py; no value was typed by hand. */\nconst CIE1931=[\n')
    for q in range(0, len(tab), 3):
        fh.write('  ' + ','.join('[%d,%s,%s,%s]' % r for r in tab[q:q + 3]) + ',\n')
    fh.write('];\n')
P('CIE rows written', len(tab))
M = [[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]]
T = [(r[0], float(r[1]), float(r[2]), float(r[3])) for r in tab]


def cie_at(nm):
    x = min(max((nm - T[0][0]) / 5, 0), len(T) - 1)
    i = min(len(T) - 2, math.floor(x))
    f = x - i
    return [T[i][q] + (T[i + 1][q] - T[i][q]) * f for q in (1, 2, 3)]


def spec_linear(nm):
    c = cie_at(nm)
    if c[0] + c[1] + c[2] < 1e-9:
        return [0, 0, 0]
    r = M[0][0] * c[0] + M[0][1] * c[1] + M[0][2] * c[2]
    g = M[1][0] * c[0] + M[1][1] * c[1] + M[1][2] * c[2]
    b = M[2][0] * c[0] + M[2][1] * c[1] + M[2][2] * c[2]
    lo = min(r, g, b)
    if lo < 0:
        r -= lo
        g -= lo
        b -= lo
    hi = max(r, g, b, 1e-12)
    return [r / hi, g / hi, b / hi]


for nm in [380.0, 450.0, LAM0, 550.0, 600.0, 650.0, 700.0, 780.0]:
    P('specLinear(%r)' % nm, *spec_linear(nm))

import json
with io.open(os.path.join(HERE, 'p7_refs.js'), 'w', encoding='utf-8') as fh:
    fh.write('\n/* the reference values: every line derive.py printed (refvals.txt), keyed by its label and\n'
             '   written by derive.py itself, so no number here was typed by hand */\nconst REF=')
    fh.write(json.dumps(REFS, separators=(',', ':')))
    fh.write(';\n')
print('\n# %d reference lines written to p7_refs.js' % len(REFS))
print('# done')
