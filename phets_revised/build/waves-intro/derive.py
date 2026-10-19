#!/usr/bin/env python3
"""derive.py — the Python twin and the reference values for waves-intro.html.

    python3 derive.py > refvals.txt 2> derive_err.txt

Every value selfTest asserts with the tag (python), (scipy), (twin) or (WI) is a line of the
output of this script, read in full.  It also writes p7_refs.js (the same lines, keyed by label).

What is REUSED, not re-derived.  The lattice (PhET's 5-point leapfrog at C = 1/2 on 151 x 151
cells), its dispersion relation, Mur's boundary, the calibration of the three media and the
engine's twin are proven in build/wave-interference/derive.py.  The lines this file needs from
that proof are READ from build/wave-interference/refvals.txt and re-printed here under their own
labels, after checking that the one-line formulas below reproduce them exactly (so the two
files cannot drift apart unnoticed).  The engine itself (build/wave-interference/p2_engine.js)
is included in waves-intro.html unchanged.

What is NEW here:
  A. a compact twin of the engine's point-source path (lattice, Mur edge, hard source, pulse,
     on/off with the phase restart), checked against wave-interference's own twin pins, then
     run for the scenarios this sim adds;
  B. PhET's light screen as Waves Intro 1.1.24 draws it (read from docs/phets/waves-intro_en.html:
     lightScreenAveragingWindowSize 40, piecewiseLinearBrightness true): 3-row smoothing, a
     +/-39-row box average, and PhET's piecewise-linear brightness table;
  C. the steady-state measurement: at each cell of the axis a least-squares fit against the
     drive's own phase; the wavelength from the slope of the phase, against v/f; the envelope's
     power law against 1/sqrt(r); the continuum 2-D near field (scipy's Hankel function) for
     comparison;
  D. the single-source screen: the lattice's time-averaged intensity against 1/r;
  E. PhET's tone: 1000 f Hz at output level 0.3 A/10, as a looped buffer of whole cycles.
"""
import io, json, math, os, re, sys
import numpy as np
from scipy import special

HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')
PI = math.pi
TAU = 2 * PI


def jsround(x):
    """JavaScript's Math.round: floor(x + 1/2)"""
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
# the wave-interference proof, read (not re-derived): its p7_refs.js is refvals.txt keyed by label
# (a printed line cannot be split back into label and values when the label ends in numbers)
_s = io.open(os.path.join(WI, 'p7_refs.js'), encoding='utf-8').read()
WI_REFS = json.loads(_s[_s.index('const REF=') + len('const REF='):_s.rindex(';')])
assert 'TWIN tank u(22,75)' in WI_REFS and 'latOmega 0.3 0.0' in WI_REFS


def wi(label, i=None):
    v = WI_REFS[label]
    return v if i is None else v[i]


def same(a, b, tol, what):
    assert abs(a - b) <= tol * max(1.0, abs(b)), '%s: %r vs wave-interference %r' % (what, a, b)


# ---------------------------------------------------------------------------------------------
# constants: PhET's values (waves-intro 1.1.24 = wave-interference 2.0.22 for everything below;
# the scene definitions were compared line by line in the minified original)
N_LAT, PAD, VIS = 151, 20, 111
C = 0.5
C2 = C * C
SRC_I, MID = 25, 75
AMP_CAL = 1.2
EVENT_RATE = 20 * 111 / 61
VISIT = 1e-3
MUR1 = (C - 1) / (C + 1)
MUR2A = 2 / (C + 1)
MUR2B = C2 / (2 * (C + 1))
C_NM_FS = 299.792458
SCENES = {
    'water': dict(W=10, v=1.65, fmin=0.25, fmax=1, phetTimeScale=1),
    'sound': dict(W=500, v=34.3, fmin=0.22, fmax=0.44, phetTimeScale=2.4187847116091334),
    'light': dict(W=5000, v=C_NM_FS, fmin=C_NM_FS / 780, fmax=C_NM_FS / 380, phetTimeScale=1416.5 / 511.034),
}
# SI conversions of each medium's units (cm/s, cm/ms, nm/fs)
SI_LEN = {'water': 1e-2, 'sound': 1e-2, 'light': 1e-9}
SI_TIME = {'water': 1.0, 'sound': 1e-3, 'light': 1e-15}
SCREEN_HIST = 180
# PhET's light screen in Waves Intro (read from the minified original, class sp / tp)
SCREEN_AVG = 40
PHET_BRIGHT = [0, 0, .002237089269640335, .4, .008937089269640335, .5, .05372277438413573, .64,
               .13422634397144692, .74, .2096934692889395, .8, 1, 1]
# the steady-state measurement
MEAS_N0, MEAS_PER, MEAS_R0, MEAS_R1, MEAS_A = 400, 2, 30, 100, 8.0
# the tone
TONE_SR, TONE_SECONDS = 44100, 0.5

print('# derive.py for waves-intro.html — every line below is a reference value')

# ---------------------------------------------------------------------------------------------
print('\n# R. reused from build/wave-interference/refvals.txt (recomputed here; asserted equal before printing)')


def lat_omega(kx, ky):
    return 2 * math.asin(C * math.sqrt(math.sin(kx / 2) ** 2 + math.sin(ky / 2) ** 2))


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


same(EVENT_RATE, wi('EVENT_RATE', 0), 0, 'EVENT_RATE')
P('EVENT_RATE', EVENT_RATE)
for a, b in zip([MUR1, MUR2A, MUR2B], wi('MUR1 MUR2A MUR2B')):
    same(a, b, 0, 'Mur')
P('MUR1 MUR2A MUR2B', MUR1, MUR2A, MUR2B)
for kx, ky in [(0.3, 0.0), (0.2, 0.2), (1.0, 0.4), (PI, PI)]:
    lab = 'latOmega %r %r' % (kx, ky)
    same(lat_omega(kx, ky), wi(lab, 0), 0, lab)
    P(lab, lat_omega(kx, ky))
for sid in ['water', 'sound', 'light']:
    S = SCENES[sid]
    f0 = 0.5 * (S['fmin'] + S['fmax'])
    lab = '%s dx f0 lambda0' % sid
    for a, b in zip([dx_of(S), f0, S['v'] / f0], wi(lab)):
        same(a, b, 0, lab)
    P(lab, dx_of(S), f0, S['v'] / f0)
    for tag, f in [('fmin', S['fmin']), ('f0', f0), ('fmax', S['fmax'])]:
        Nl = cells_per_wave(S, f)
        Om = omega_step(Nl)
        lab = '  %s %s f Nl Om dt period_steps' % (sid, tag)
        vals = [f, Nl, Om, step_dt(S, f), TAU / Om]
        for a, b in zip(vals, wi(lab)):
            same(a, b, 0, lab)
        P(lab, *vals)
        lab = '  %s %s PhET lambda, PhET/true - 1' % (sid, tag)
        vals = [phet_lambda(S, f), phet_lambda(S, f) / (S['v'] / f) - 1]
        for a, b in zip(vals, wi(lab)):
            same(a, b, 0, lab)
        P(lab, *vals)
# the SI speeds: the unit conversions of the three media
for sid in ['water', 'sound', 'light']:
    P('SI speed m/s %s' % sid, SCENES[sid]['v'] * SI_LEN[sid] / SI_TIME[sid])

# ---------------------------------------------------------------------------------------------
# A. the twin (the point-source path of build/wave-interference/p2_engine.js, operation for
#    operation; the lattice step is wave-interference derive.py's own)
print('\n# A. the twin: the engine\'s point-source path, checked against wave-interference\'s twin pins')


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
    """one medium, one hard point source at (25, 75): makeRun(sid, 'point', 1)"""

    def __init__(self, sid, n=N_LAT):
        self.lat = Lat(n)
        self.A = 8.0
        self.src0 = True
        self.cont = True
        self.pulse_on, self.pulse_phi = False, 0.0
        self.sid = sid
        S = SCENES[sid]
        self.set_f(0.5 * (S['fmin'] + S['fmax']))
        self.t, self.n, self.watch = 0.0, 0, 0.0
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
        self.pulse_on, self.pulse_phi = False, 0.0
        self.rows = n - 2 * PAD
        self.buf = np.zeros((SCREEN_HIST, self.rows))
        self.head, self.count = 0, 0

    # runSetSource(R, 0, on) for one source: switching on restarts the phase
    def set_source(self, on):
        if on and not self.src0:
            self.phi = 0.0
        self.src0 = on

    # runSetWave(R, cont): a new disturbance type stops everything; pulse mode keeps the cell armed
    def set_wave(self, cont):
        if self.cont == cont:
            return
        self.cont = cont
        self.pulse_on, self.pulse_phi = False, 0.0
        self.src0 = not cont

    def fire(self):
        if self.cont:
            return False
        self.pulse_on, self.pulse_phi = True, 0.0
        return True

    def step(self):
        L = self.lat
        L.step()
        self.phi += self.Om
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
        if val is not None and self.src0:
            L.u[MID, L.pad + SRC_I - PAD] = val
        self.t += self.dt
        self.n += 1
        col = L.nx - L.pad - 1
        self.buf[self.head, :] = L.u[L.pad:L.pad + self.rows, col]
        self.head = (self.head + 1) % SCREEN_HIST
        self.count = min(self.count + 1, SCREEN_HIST)

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


CELLS = [(22, 75), (10, 75), (45, 75), (60, 75), (90, 75), (60, 50), (100, 100), (130, 40), (140, 75), (75, 140)]


def report(tag, R, cells):
    u = R.lat.u
    for (i, j) in cells:
        P('%s u(%d,%d)' % (tag, i, j), u[j, i])
    visu = u[PAD:PAD + VIS, PAD:PAD + VIS]
    P('%s max|u| visible, sum u^2 visible, visited cells' % tag, np.max(np.abs(visu)), np.sum(visu * visu), int(np.sum(R.lat.vis)))
    P('%s t n phi' % tag, R.t, R.n, R.phi)


# (a) wave-interference's own tank scenario: water, amplitude 8, 240 steps — this twin must
#     reproduce wave-interference's pins exactly (then the engine included here is theirs)
Ra = Run('water')
for _ in range(240):
    Ra.step()
for (i, j) in CELLS:
    same(Ra.lat.u[j, i], wi('TWIN tank u(%d,%d)' % (i, j), 0), 1e-13, 'tank u(%d,%d)' % (i, j))
visu = Ra.lat.u[PAD:PAD + VIS, PAD:PAD + VIS]
same(float(np.sum(visu * visu)), wi('TWIN tank max|u| visible, sum u^2 visible, visited cells', 1), 1e-13, 'tank sum u^2')
report('TWIN tank', Ra, CELLS)
# (b) wave-interference's pulse scenario: water, pulse fired at the start, 150 steps
Rd = Run('water')
Rd.set_wave(False)
Rd.fire()
for _ in range(150):
    Rd.step()
for (i, j) in CELLS:
    same(Rd.lat.u[j, i], wi('TWIN pulse u(%d,%d)' % (i, j), 0), 1e-13, 'pulse u(%d,%d)' % (i, j))
report('TWIN pulse', Rd, CELLS)
P('TWIN pulse finished', int(not Rd.pulse_on))
# (c) new: sound at a non-default frequency and amplitude, 300 steps
Rb = Run('sound')
Rb.set_f(0.2937)
Rb.A = 6.5
for _ in range(300):
    Rb.step()
report('TWIN sound', Rb, CELLS)
# the air parcels on that run: PhET's 21 x 21 grid, each pushed along grad p by
# xi = grad p / (rho omega^2), scaled so that a wave at PhET's full colour (U_FULL) moves a
# parcel 0.3 of the parcel spacing.  Beside the source the field is stronger than full colour,
# so the push there is larger — the number below is what it actually reaches.
U_FULL = 2.14


def parcels(R):
    S = SCENES[R.sid]
    L = R.lat
    k = TAU / R.Nl
    KD = 0.3 * (VIS / 20) / (k * U_FULL)
    dx = dx_of(S)
    out = []
    for a in range(21):
        for b in range(21):
            X = L.pad - 0.5 + (a * S['W'] / 20) / dx
            Y = L.pad - 0.5 + (b * S['W'] / 20) / dx
            i = min(max(jsround(X), 1), L.nx - 2)
            j = min(max(jsround(Y), 1), L.ny - 2)
            gx = (L.u[j, i + 1] - L.u[j, i - 1]) / 2
            gy = (L.u[j + 1, i] - L.u[j - 1, i]) / 2
            out.append((X + KD * gx, Y + KD * gy, X, Y))
    return out


pc = parcels(Rb)
for q in [0, 100, 220, 440]:
    P('TWIN sound parcel[%d] x y' % q, pc[q][0], pc[q][1])
P('TWIN sound parcels: largest push across, up, and as a fraction of the spacing',
  max(abs(p[0] - p[2]) for p in pc), max(abs(p[1] - p[3]) for p in pc),
  max(abs(p[0] - p[2]) for p in pc) / (VIS / 20))
# (d) new: light at its default, the source switched OFF at step 150 and back ON at step 190
#     (the phase restarts at zero), 360 steps in all; then its screen
Rc = Run('light')
for s in range(360):
    if s == 150:
        Rc.set_source(False)
    if s == 190:
        Rc.set_source(True)
    Rc.step()
report('TWIN onoff', Rc, CELLS)
# (e) new: light at its default, amplitude 8, 400 steps undisturbed: the screen
Re = Run('light')
for _ in range(400):
    Re.step()
report('TWIN light', Re, CELLS)

# ---------------------------------------------------------------------------------------------
# B. PhET's light screen (Waves Intro 1.1.24)
print('\n# B. the light screen: whole-period mean square, 3-row smoothing, +/-39-row window, PhET brightness')


def smooth3(I):
    n = len(I)
    out = np.empty(n)
    out[0] = (I[0] + I[1]) / 2
    out[n - 1] = (I[n - 1] + I[n - 2]) / 2
    for r in range(1, n - 1):
        out[r] = (I[r - 1] + I[r] + I[r + 1]) / 3
    return out


def screen_average(I, a):
    n = len(I)
    out = np.empty(n)
    for r in range(n):
        s, c = I[r], 1
        for d in range(1, a):
            if r + d < n:
                s += I[r + d]
                c += 1
            if r - d >= 0:
                s += I[r - d]
                c += 1
        out[r] = s / c
    return out


def phet_brightness(u):
    T = PHET_BRIGHT
    if u <= T[0]:
        b = T[1]
    elif u >= T[-2]:
        b = T[-1]
    else:
        i = 0
        while u > T[i + 2]:
            i += 2
        b = T[i + 1] + (T[i + 3] - T[i + 1]) * (u - T[i]) / (T[i + 2] - T[i])
    return min(max(b, 0.0), 1.0)


# an independent route to PhET's table: numpy's own piecewise-linear interpolation
xs, ys = PHET_BRIGHT[0::2], PHET_BRIGHT[1::2]
for u in [0.0, 0.001, 0.002237089269640335, 0.005, 0.03, 0.1, 0.17, 0.5, 1.0, 1.7]:
    b = phet_brightness(u)
    assert abs(b - float(np.interp(u, xs, ys))) < 1e-15, u
    P('phetBrightness(%r)' % u, b)
Ie = Re.screen_intensity()
P('TWIN light screen window', Re.screen_window())
for r in [0, 10, 30, 55, 80, 100, 110]:
    P('TWIN light screen I[%d]' % r, Ie[r])
S3 = smooth3(Ie)
SA = screen_average(S3, SCREEN_AVG)
BR = np.array([phet_brightness(u) for u in SA])
for r in [0, 10, 30, 55, 80, 100, 110]:
    P('screen smooth3, window40, brightness [%d]' % r, S3[r], SA[r], BR[r])
P('screen brightness min max', float(BR.min()), float(BR.max()))
# the same window, but Wave Interference's default of 3 (as a check that 40 is load-bearing)
P('screen window 3 at row 10 (Wave Interference default)', screen_average(S3, 3)[10])

# ---------------------------------------------------------------------------------------------
# C. the steady-state measurement along the axis
print('\n# C. steady state along the axis: least squares against the drive, lambda from the phase slope')


def solve4(Nm, rhs):
    """Gaussian elimination with partial pivoting, as the JS does (column by column)"""
    A = [row[:] + [rhs[i]] for i, row in enumerate(Nm)]
    n = 4
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(A[r][col]))
        if piv != col:
            A[col], A[piv] = A[piv], A[col]
        for r in range(col + 1, n):
            fct = A[r][col] / A[col][col]
            for c in range(col, n + 1):
                A[r][c] -= fct * A[col][c]
    x = [0.0] * n
    for r in range(n - 1, -1, -1):
        s = A[r][n]
        for c in range(r + 1, n):
            s -= A[r][c] * x[c]
        x[r] = s / A[r][r]
    return x


def measure(sid, f):
    R = Run(sid)
    R.set_f(f)
    R.A = MEAS_A
    for _ in range(MEAS_N0):
        R.step()
    M = int(math.ceil(MEAS_PER * TAU / R.Om))
    ci = R.lat.pad + SRC_I - PAD
    ncell = R.lat.nx - R.lat.pad - ci                  # r = 0 .. 105
    Nm = [[0.0] * 4 for _ in range(4)]
    rhs = np.zeros((4, ncell))
    samples = []
    for q in range(M):
        R.step()
        tq = q - (M - 1) / 2
        b = [math.sin(R.phi), math.cos(R.phi), 1.0, tq]
        row = R.lat.u[MID, ci:ci + ncell].copy()
        samples.append((b, row))
        for i in range(4):
            for j in range(4):
                Nm[i][j] += b[i] * b[j]
            rhs[i] += b[i] * row
    amp = np.zeros(ncell)
    ph = np.zeros(ncell)
    for c in range(ncell):
        x = solve4(Nm, [rhs[0][c], rhs[1][c], rhs[2][c], rhs[3][c]])
        amp[c] = math.hypot(x[0], x[1])
        ph[c] = math.atan2(x[1], x[0])
    # cross-check the elimination against numpy's least squares (SVD)
    Bm = np.array([s[0] for s in samples])
    Um = np.array([s[1] for s in samples])
    coef = np.linalg.lstsq(Bm, Um, rcond=None)[0]
    assert np.max(np.abs(np.hypot(coef[0], coef[1]) - amp)) < 1e-9 * np.max(amp)
    un = np.zeros(ncell)
    un[0] = ph[0]
    for c in range(1, ncell):
        d = ph[c] - ph[c - 1]
        while d > PI:
            d -= TAU
        while d < -PI:
            d += TAU
        un[c] = un[c - 1] + d
    r = np.arange(ncell, dtype=float)
    sel = (r >= MEAS_R0) & (r <= MEAS_R1)
    rs, ps = r[sel], un[sel]
    slope = np.sum((rs - rs.mean()) * (ps - ps.mean())) / np.sum((rs - rs.mean()) ** 2)
    lr, la = np.log(rs), np.log(amp[sel])
    pexp = np.sum((lr - lr.mean()) * (la - la.mean())) / np.sum((lr - lr.mean()) ** 2)
    afit = float(np.mean(amp[sel] * np.sqrt(rs)))
    return dict(R=R, M=M, amp=amp, un=un, k=-slope, lam=TAU / (-slope), pexp=pexp, afit=afit,
                snap=R.lat.u[MID, ci:ci + ncell].copy(), Nl=R.Nl)


def hankel_bias(Nl):
    """the continuum's own answer: fit the phase of H0(kr) over the same cells the same way"""
    k = TAU / Nl
    r = np.arange(MEAS_R0, MEAS_R1 + 1, dtype=float)
    th = np.unwrap(np.angle(special.hankel1(0, k * r)))
    kc = np.sum((r - r.mean()) * (th - th.mean())) / np.sum((r - r.mean()) ** 2)
    return (TAU / kc) / Nl - 1


MEAS_CASES = [('water', 0.625), ('water', 0.25), ('water', 0.8), ('sound', 0.33), ('light', 0.5866384130904184),
              ('light', SCENES['light']['fmax'])]
for sid, f in MEAS_CASES:
    m = measure(sid, f)
    S = SCENES[sid]
    lab = 'MEAS %s f=%r' % (sid, f)
    P(lab + ': fit steps M, lambda cells, v/f cells, lambda/(v/f) - 1', m['M'], m['lam'], m['Nl'], m['lam'] / m['Nl'] - 1)
    P(lab + ': lambda in the medium unit, v/f', m['lam'] * dx_of(S), S['v'] / f)
    P(lab + ': envelope exponent, amp*sqrt(r) mean over the window', m['pexp'], m['afit'])
    for c in [0, 5, 30, 55, 100]:
        P(lab + ': amp phase snapshot at r=%d' % c, m['amp'][c], m['un'][c], m['snap'][c])
    P(lab + ': continuum Hankel phase fit over the same cells, lambda/(v/f) - 1', hankel_bias(m['Nl']))

# ---------------------------------------------------------------------------------------------
# D. one source on the screen: the intensity falls as 1/r
print('\n# D. single-source screen theory: I proportional to 1/r, normalised to its peak')
dxl = dx_of(SCENES['light'])
Xs = (N_LAT - PAD - 1 - SRC_I) * dxl
th = np.array([1 / math.hypot(Xs, (PAD + r - MID) * dxl) for r in range(VIS)])
th /= th.max()
for r in [0, 10, 30, 55, 80, 110]:
    P('screen 1/r theory [%d]' % r, th[r])
Il = Ie / Ie.max()
P('lattice screen vs 1/r after 400 steps: max |diff|, rms', float(np.max(np.abs(Il - th))), float(math.sqrt(np.mean((Il - th) ** 2))))
# the steady state (1400 steps) as well
Rs = Run('light')
for _ in range(1400):
    Rs.step()
Is = Rs.screen_intensity()
Is = Is / Is.max()
P('lattice screen vs 1/r after 1400 steps: max |diff|, rms', float(np.max(np.abs(Is - th))), float(math.sqrt(np.mean((Is - th) ** 2))))

# ---------------------------------------------------------------------------------------------
# E. the tone
print('\n# E. PhET\'s tone: 1000 f Hz, output level 0.3 A/10; a looped buffer of whole cycles')


def tone_buffer(hz, level, sr):
    m = max(1, jsround(hz * TONE_SECONDS))
    L = jsround(m * sr / hz)
    i = np.arange(L)
    data = (level * np.sin(TAU * m * i / L)).astype(np.float32)
    return m, L, m * sr / L, data


# 0.301 per ms is here on purpose: 301 Hz needs 150.5 cycles in half a second and 22123.25
# samples to hold them, so BOTH roundings have a fraction below one half and a mutant that
# rounds either of them the other way is caught.  At 0.33 and 0.44 the arithmetic is exact and
# at 0.2937 the fractions are above one half (wave-interference's Known-bad rounding trap).
for f, A in [(0.33, 8.0), (0.2937, 6.5), (0.44, 10.0), (0.301, 4.0)]:
    hz, level = 1000 * f, 0.3 * A / 10
    m, L, act, data = tone_buffer(hz, level, TONE_SR)
    P('tone f=%r A=%r: hz level' % (f, A), hz, level)
    P('tone f=%r A=%r: cycles, samples, looped frequency' % (f, A), m, L, act)
    for i in [1, 17, 1000]:
        P('tone f=%r A=%r: sample[%d]' % (f, A, i), float(data[i]))
    # the measured frequency from zero crossings over the whole buffer, interpolated
    zc = []
    for i in range(L - 1):
        a, b = float(data[i]), float(data[i + 1])
        if a <= 0 < b:
            zc.append(i + a / (a - b))
    P('tone f=%r A=%r: upward crossings, frequency from their spacing' % (f, A), len(zc),
      TONE_SR * (len(zc) - 1) / (zc[-1] - zc[0]))

# ---------------------------------------------------------------------------------------------
# F. evidence for two claims the page makes (python only; the JS asserts the claims against these)
print('\n# F. evidence: the edges, not the calibration, carry the residuals (a 401-cell lattice, edges far away)')


def measure_big(sid, f, n, n0=MEAS_N0):
    """the same fit (numpy lstsq) on an n x n lattice with the source 5 cells in from the pad"""
    R = Run(sid, n=n)
    R.set_f(f)
    mid = (n - 1) // 2
    ci = PAD + 5
    for _ in range(n0):
        R.lat.step()
        R.phi += R.Om
        R.lat.u[mid, ci] = MEAS_A * AMP_CAL * math.sin(R.phi)
    M = int(math.ceil(MEAS_PER * TAU / R.Om))
    B, U = [], []
    for q in range(M):
        R.lat.step()
        R.phi += R.Om
        R.lat.u[mid, ci] = MEAS_A * AMP_CAL * math.sin(R.phi)
        B.append([math.sin(R.phi), math.cos(R.phi), 1.0, q - (M - 1) / 2])
        U.append(R.lat.u[mid, ci:ci + MEAS_R1 + 1].copy())
    coef = np.linalg.lstsq(np.array(B), np.array(U), rcond=None)[0]
    ph = np.unwrap(np.arctan2(coef[1], coef[0]))
    r = np.arange(MEAS_R1 + 1, dtype=float)
    sel = (r >= MEAS_R0) & (r <= MEAS_R1)
    k = -np.polyfit(r[sel], ph[sel], 1)[0]
    return (TAU / k) / R.Nl - 1


for sid, f in [('water', 0.25), ('water', 0.625), ('sound', 0.33), ('light', 0.5866384130904184)]:
    P('CHECK lambda/(v/f) - 1 at %s f=%r: 151 lattice, 401 lattice, continuum near field' % (sid, f),
      measure_big(sid, f, N_LAT), measure_big(sid, f, 401), hankel_bias(cells_per_wave(SCENES[sid], f)))
# the screen: the same source and screen geometry (screen 105 cells out, +/-55 rows) on lattices of
# 151, 401 and 601 cells.  The ripple (the profile minus its own 11-row running mean) shrinks as the
# edges move away — it is the waves the edges reflect; the smooth part that is left departs from 1/r
# by a few per cent at +/-27 degrees — the square lattice's own slight anisotropy.
def screen_profile(n, steps=1400):
    R = Run('light', n=n)
    mid = (n - 1) // 2
    ci = PAD + 5
    w = R.screen_window()
    buf = []
    for s in range(steps):
        R.lat.step()
        R.phi += R.Om
        R.lat.u[mid, ci] = 8 * AMP_CAL * math.sin(R.phi)
        if s >= steps - w:
            buf.append(R.lat.u[mid - 55:mid + 56, ci + 105].copy())
    I = np.mean(np.array(buf) ** 2, axis=0)
    return I / I.max()


def ripple(a):
    sm = np.convolve(np.pad(a, 5, mode='edge'), np.ones(11) / 11, mode='valid')
    return float(math.sqrt(np.mean((a - sm)[6:-6] ** 2))), sm


profs = [screen_profile(n) for n in (151, 401, 601)]
assert np.max(np.abs(profs[0] - Is)) < 1e-12          # the 151 run is the engine's own screen
rp = [ripple(a) for a in profs]
P('CHECK screen ripple rms (profile minus its 11-row mean) on 151, 401, 601 lattices', *[q[0] for q in rp])
# the smooth part: mean of rows 0-10 over mean of rows 50-60 (the edge of the screen against its centre)
edge = lambda a: float(np.mean(a[0:11]) / np.mean(a[50:61]))
P('CHECK screen edge/centre (rows 0-10 over 50-60): 151, 401, 601 lattices, 1/r', edge(profs[0]), edge(profs[1]),
  edge(profs[2]), edge(th))

with io.open(os.path.join(HERE, 'p7_refs.js'), 'w', encoding='utf-8') as fh:
    fh.write('\n/* the reference values: every line derive.py printed (refvals.txt), keyed by its label and\n'
             '   written by derive.py itself, so no number here was typed by hand */\nconst REF=')
    fh.write(json.dumps(REFS, separators=(',', ':')))
    fh.write(';\n')
print('\n# %d reference lines written to p7_refs.js' % len(REFS))
print('# done')
