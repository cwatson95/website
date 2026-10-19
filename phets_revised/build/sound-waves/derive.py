#!/usr/bin/env python3
"""derive.py — the Python twin and the reference values for sound-waves.html.

    python3 derive.py > refvals.txt 2> derive_err.txt

Every value selfTest asserts with the tag (python), (scipy), (twin) or (WI) is a line of the
output of this script, read in full.  It also writes p7_refs.js (the same lines, keyed by label).

WHAT IS REUSED, NOT RE-DERIVED
  The 2-D lattice itself — PhET's 5-point leapfrog at C = 1/2, Mur's second-order absorbing
  edge, the dispersion relation, and the idea of solving the time step from that relation so
  that lambda = v/f is exact along the lattice axes — is proven in
  build/wave-interference/derive.py, and its p2_engine.js is the file this build's engine was
  copied from.  The lines this file needs from that proof are READ from that build's p7_refs.js
  and re-printed under their own labels after the formulas here reproduce them exactly, so the
  two cannot drift apart unnoticed.  The lattice stencil is ALSO falsified independently here,
  by putting an exact lattice plane wave through it (section A).

WHAT IS NEW HERE
  A. the twin: the same lattice at THIS sim's size (231 x 231, 191 visible) with PhET's Sound
     Waves geometry, run for the scenarios the sim shows, cell by cell;
  B. the speed of sound itself: v = sqrt(gamma R T / M) for an ideal gas, the temperature at
     which it equals PhET's 343 m/s, and the fact that it does not depend on pressure;
  C. the calibration at this sim's 100-1000 Hz, against PhET's own fixed time step, and the
     lattice's phase speed, group speed and anisotropy, which is what sets the lattice size;
  D. lambda MEASURED on the lattice by a least-squares fit against the drive's own phase,
     at five frequencies across the slider;
  E. two sources: the hyperbolic nodal lines |r1 - r2| = (m + 1/2) lambda in closed form,
     cross-checked against a brute-force scan, their far-field asymptotes d sin(theta) =
     (m + 1/2) lambda, and the lattice's own nodal lines measured against them;
  F. the reflecting wall as an IMAGE SOURCE: the mirror map, the reflection point, the equality
     of the angles of incidence and reflection, Fermat's shortest path, and the Neumann
     condition du/dn = 0 that the construction enforces on the wall;
  G. the air: what removing it does (the source amplitude scales with the density, exactly, so
     the whole steady field does), the sound intensity and its decibels, and the mean free path
     at which a continuum sound wave stops being a wave at all;
  H. the listener: the path difference and the |cos| interference law, against PhET's own
     hand-tuned 36/f wavelength.
"""
import io
import json
import math
import os
import sys

import numpy as np
from scipy import optimize, special

HERE = os.path.dirname(os.path.abspath(__file__))
WI = os.path.join(HERE, '..', 'wave-interference')
PI = math.pi
TAU = 2 * PI

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
    nums = [float(v) if not isinstance(v, (int, np.integer)) else int(v) for v in vals
            if not isinstance(v, str)]
    assert label not in REFS, 'duplicate reference label: ' + label
    REFS[label] = nums


def jsround(x):
    """JavaScript's Math.round: floor(x + 1/2)"""
    return math.floor(x + 0.5)


# the wave-interference proof, read (not re-derived)
_s = io.open(os.path.join(WI, 'p7_refs.js'), encoding='utf-8').read()
WI_REFS = json.loads(_s[_s.index('const REF=') + len('const REF='):_s.rindex(';')])
assert 'latOmega 0.3 0.0' in WI_REFS and 'MUR1 MUR2A MUR2B' in WI_REFS


def wi(label, i=None):
    v = WI_REFS[label]
    return v if i is None else v[i]


def same(a, b, tol, what):
    assert abs(a - b) <= tol * max(1.0, abs(b)), '%s: %r vs wave-interference %r' % (what, a, b)


# =============================================================================================
# constants.  PhET's, read from docs/phets/sound-waves_en.html (Sound Waves 1.1.11), are marked.
# This sim works in SI: metres and seconds.  PhET's model unit is 1 cm (its ruler is 500 model
# units long and labelled 0..5 m) and its frequency property is per millisecond (its slider
# label is round(1000 f) Hz), so PhET's 1000-unit wave area is 10 m and its 0.1..1 frequency
# range is 100..1000 Hz.
W_AREA = 10.0                      # PhET's WAVE_AREA_WIDTH 1e3 model units = 10 m
V_SOUND = 343.0                    # PhET's 34.3 cm/ms
F_MIN, F_MAX, F_0 = 100.0, 1000.0, 550.0   # PhET's Range(0.1, 1) and initial 0.55, x1000 Hz
AMP_MAX, AMP_0 = 10.0, 5.0         # PhET's AMPLITUDE_RANGE Range(0,10) and initialAmplitude 5
AMP_CAL = 1.2                      # PhET's: the source cell is driven at 1.2 x the amplitude
U_FULL = 2.0                       # PhET's positive full-contrast lattice value (see section C)
PHET_LATTICE, PHET_PAD = 151, 20   # PhET's LATTICE_DIMENSION, LATTICE_PADDING
PHET_SRC_X = 40                    # PhET's SOURCE_POSITION_X, a lattice column
PHET_TIME_SCALE = 2.4187847116091334 * W_AREA * 100 / 500 * 1e-3   # s of model time per s of wall
PHET_EVENT_RATE = 20 * 111 / 61    # PhET's EVENT_RATE, lattice steps per second of wall time
PHET_MAX_SOUND_DIST = 85           # PhET's MAX_SOUND_DISTANCE, in lattice cells
PHET_LISTENER_X = (W_AREA / 3, 8.0)        # PhET's LISTENER_BOUNDS_X Range(1e3/3, 800)
PHET_WALL_X = (W_AREA / 3, 2 * W_AREA / 3)  # PhET's wallPositionXProperty range
PHET_WALL_ANG = (0.1 * PI, 0.5 * PI)        # PhET's wallAngleProperty range
PHET_LISTENER_LAMBDA_K = 36.0      # PhET's updateListenerSound uses lambda = 36/f MODEL UNITS

# this sim's lattice.  PhET's 151 cells give only 3.3 cells per wavelength at 1000 Hz (section
# C); 231 cells with the same 20-cell pad give 6.55, and the source sits where PhET's does.
N_LAT, PAD, VIS = 231, 20, 191
C = 0.5
C2 = C * C
MID = (N_LAT - 1) // 2             # 115: the middle row, at exactly y = W/2
SRC_OFF = 34                       # cells from the left edge of the visible area
SRC_I = PAD + SRC_OFF              # 54
VISIT = 1e-3
MUR1 = (C - 1) / (C + 1)
MUR2A = 2 / (C + 1)
MUR2B = C2 / (2 * (C + 1))
DX = W_AREA / VIS

# the air parcels: a 21 x 21 grid, pushed along grad p, exaggerated so that a full-contrast
# wave moves one PARC_PUSH of the parcel spacing
PARC_N, PARC_PUSH = 20, 0.45

# the measurement lattice of section D (same dx, a shorter tank, the source 5 cells in)
MEAS_N, MEAS_SRC_OFF, MEAS_N0, MEAS_PER, MEAS_R0, MEAS_R1, MEAS_A = 181, 5, 470, 2, 30, 120, 8.0
MEAS_FS = [100.0, 325.0, 550.0, 775.0, 1000.0]

# the gas.  gamma = 7/5 for a diatomic ideal gas; R is the CODATA-2018 exact molar gas constant;
# M is the molar mass of standard dry air (US Standard Atmosphere 1976 / CIPM-2007, 28.96546
# g/mol -- the value quoted to six figures is 28.9647 g/mol and both are carried below).
GAMMA = 1.4
R_GAS = 8.314462618                # J mol^-1 K^-1, exact by the 2019 SI redefinition
M_AIR = 28.9647e-3                 # kg/mol, standard dry air
T_20C = 293.15                     # K
K_B = 1.380649e-23                 # J/K, exact
D_AIR = 3.7e-10                    # m, the usual kinetic-theory collision diameter of air
P_ATM = 101325.0                   # Pa, exact

print('# derive.py for sound-waves.html — every line below is a reference value')
print('# PhET Sound Waves 1.1.11; lattice 231 x 231 (191 visible), C = 1/2, SI units')

# =============================================================================================
print('\n# R. reused from build/wave-interference/ (recomputed here; asserted equal before printing)')


def lat_omega(kx, ky):
    return 2 * math.asin(C * math.sqrt(math.sin(kx / 2) ** 2 + math.sin(ky / 2) ** 2))


def lat_k(Om, th):
    """the wavenumber along direction th carrying Om, by bisection on the monotone branch"""
    c, s = math.cos(th), math.sin(th)
    hi = PI / max(abs(c), abs(s))
    if lat_omega(hi * c, hi * s) < Om:
        return float('nan')
    lo = 0.0
    for _ in range(200):
        m = 0.5 * (lo + hi)
        if lat_omega(m * c, m * s) < Om:
            lo = m
        else:
            hi = m
        if hi - lo <= 1e-15 * max(hi, 1e-300):
            break
    return 0.5 * (lo + hi)


def lat_phase_speed(k, th):
    return lat_omega(k * math.cos(th), k * math.sin(th)) / k


def lat_group_speed(k, th):
    kx, ky = k * math.cos(th), k * math.sin(th)
    return C2 * math.hypot(math.sin(kx), math.sin(ky)) / math.sin(lat_omega(kx, ky))


def omega_step(Nl):
    return 2 * math.asin(C * math.sin(PI / Nl))


def cells_per_wave(f):
    return V_SOUND / f / DX


def step_dt(f):
    return omega_step(cells_per_wave(f)) / (TAU * f)


for a, b in zip([MUR1, MUR2A, MUR2B], wi('MUR1 MUR2A MUR2B')):
    same(a, b, 0, 'Mur')
P('MUR1 MUR2A MUR2B', MUR1, MUR2A, MUR2B)
for kx, ky in [(0.3, 0.0), (0.2, 0.2), (1.0, 0.4), (PI, PI)]:
    lab = 'latOmega %r %r' % (kx, ky)
    same(lat_omega(kx, ky), wi(lab, 0), 0, lab)
    P(lab, lat_omega(kx, ky))
same(PHET_EVENT_RATE, wi('EVENT_RATE', 0), 0, 'EVENT_RATE')
P('EVENT_RATE', PHET_EVENT_RATE)
# the highest frequency the lattice can carry, at C = 1/2: Om = 2 asin(C sqrt 2) = pi/2
P('lattice Omega max', lat_omega(PI, PI))

# =============================================================================================
print('\n# A. the stencil, falsified on an exact lattice plane wave, then the twin')


class Lat:
    """the numpy twin of latStep(): interior, then the left/right edges (tangent y), then the
    top/bottom edges (tangent x), then the four corners -- the same order as the JS."""

    def __init__(self, n, pad=PAD):
        self.nx = self.ny = n
        self.pad = pad
        self.u = np.zeros((n, n))
        self.up = np.zeros((n, n))
        self.un = np.zeros((n, n))
        self.vis = np.zeros((n, n), dtype=bool)
        self.steps = 0

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
        self.steps += 1


# an INDEPENDENT falsification of the interior stencil: a plane wave exp(i(kx i + ky j - Om n))
# with Om = lat_omega(kx, ky) is an exact solution of the update, for any (kx, ky).  Build three
# time levels analytically, take one step, and compare with the analytic next level.
def plane_residual(kx, ky, n=41):
    Om = lat_omega(kx, ky)
    i = np.arange(n)[None, :]
    j = np.arange(n)[:, None]
    ph = kx * i + ky * j
    L = Lat(n, pad=0)
    L.up[:] = np.sin(ph + Om)          # level n-1  (time runs as -Om n)
    L.u[:] = np.sin(ph)                # level n
    want = np.sin(ph - Om)             # level n+1
    L.step()
    return float(np.max(np.abs(L.u[2:-2, 2:-2] - want[2:-2, 2:-2]))), Om


for kx, ky in [(0.4, 0.0), (0.31, 0.77), (PI / 3, PI / 5), (1.1, 1.1)]:
    r, Om = plane_residual(kx, ky)
    P('plane-wave residual of the stencil kx=%r ky=%r' % (kx, ky), r, Om)

# the same statement the calibration rests on: with Nl cells per wavelength along an axis the
# per-step frequency is omega_step(Nl), and inverting it returns exactly Nl
for Nl in [3.3, 6.5513966, 11.911, 65.514, 200.0]:
    Om = omega_step(Nl)
    P('omega_step(%r), and 2 pi / latK back' % Nl, Om, TAU / lat_k(Om, 0.0))


class Run:
    """one lattice with ONE hard point source, the way sound-waves.html drives it.  Every
    picture the sim draws is a shifted or mirrored READ of this one field (which is what PhET
    does): the second speaker is the same field shifted in y, the reflecting wall is the same
    field mirrored in the wall."""

    def __init__(self, f=F_0, n=N_LAT, src_off=SRC_OFF, amp=AMP_0, pressure=1.0):
        self.n = n
        self.src_i = PAD + src_off
        self.mid = (n - 1) // 2
        self.A = amp
        self.pressure = pressure
        self.cont = True
        self.pulse_on = False
        self.pulse_phi = 0.0
        self.set_f(f)
        self.clear()

    def set_f(self, f):
        self.f = min(max(f, F_MIN), F_MAX)
        self.Nl = cells_per_wave(self.f)
        self.Om = omega_step(self.Nl)
        self.dt = step_dt(self.f)

    def clear(self):
        self.lat = Lat(self.n)
        self.phi = 0.0
        self.t = 0.0
        self.steps = 0
        self.pulse_on = False
        self.pulse_phi = 0.0

    def source_value(self):
        amp = self.A * AMP_CAL * self.pressure
        if self.cont:
            return amp * math.sin(self.phi)
        if self.pulse_on:
            self.pulse_phi += self.Om
            if self.pulse_phi < TAU:
                return amp * math.sin(self.pulse_phi)
            self.pulse_on = False
        return None

    def step(self):
        self.lat.step()
        self.phi += self.Om
        v = self.source_value()
        if v is not None:
            self.lat.u[self.mid, self.src_i] = v
        self.t += self.dt
        self.steps += 1


def pin_run(tag, R, steps):
    for _ in range(steps):
        R.step()
    u = R.lat.u
    for (i, j) in [(60, 115), (80, 115), (120, 115), (170, 115), (200, 115),
                   (120, 60), (150, 150), (60, 180), (205, 115), (115, 205)]:
        P('TWIN %s u(%d,%d)' % (tag, i, j), u[j, i])
    vis_u = u[PAD:-PAD, PAD:-PAD]
    P('TWIN %s max|u|, sum u^2, visited cells' % tag, float(np.max(np.abs(vis_u))),
      float(np.sum(vis_u ** 2)), int(np.sum(R.lat.vis[PAD:-PAD, PAD:-PAD])))
    P('TWIN %s t n phi' % tag, R.t, R.steps, R.phi)
    return R


print('\n# the twin runs: continuous at 550 Hz, at 1000 Hz, a pulse, and thin air')
pin_run('mid', Run(F_0), 300)
pin_run('high', Run(F_MAX), 300)
Rp = Run(F_0)
Rp.cont = False
Rp.pulse_on = True
Rp.pulse_phi = 0.0
pin_run('pulse', Rp, 200)
P('TWIN pulse finished', 0 if Rp.pulse_on else 1)
pin_run('thin', Run(F_0, pressure=0.25), 300)

# the air-density law, exactly: the equation is linear and the drive scales with the density,
# so the WHOLE field scales with it, step for step.  Asserted here rather than assumed.
Ra = Run(F_0, pressure=1.0)
Rb = Run(F_0, pressure=0.25)
for _ in range(220):
    Ra.step()
    Rb.step()
P('air density: max |u(p=0.25) - 0.25 u(p=1)| over the lattice after 220 steps',
  float(np.max(np.abs(Rb.lat.u - 0.25 * Ra.lat.u))))
P('air density: max |u| at p = 1 and p = 0.25, and their ratio',
  float(np.max(np.abs(Ra.lat.u))), float(np.max(np.abs(Rb.lat.u))),
  float(np.max(np.abs(Rb.lat.u)) / np.max(np.abs(Ra.lat.u))))

# =============================================================================================
print('\n# B. the speed of sound itself: an ideal gas, and what pressure does to it')
# c = sqrt(gamma p / rho) = sqrt(gamma R T / M).  p and rho both scale with the amount of gas
# at fixed temperature, so the ratio -- and therefore the speed -- does not move at all.
v_ideal = math.sqrt(GAMMA * R_GAS * T_20C / M_AIR)
P('ideal-gas sound speed at 20.00 C, sqrt(gamma R T / M)', v_ideal)
P('the same from sqrt(gamma p / rho) with rho = p M / R T at 1 atm',
  math.sqrt(GAMMA * P_ATM / (P_ATM * M_AIR / (R_GAS * T_20C))))
# the temperature at which the ideal gas gives PhET's 343 m/s exactly
T_343 = V_SOUND ** 2 * M_AIR / (GAMMA * R_GAS)
P('temperature at which the ideal gas gives exactly 343 m/s, K and C', T_343, T_343 - 273.15)
P('PhET 343 m/s against the 20 C ideal gas: ratio - 1', V_SOUND / v_ideal - 1)
# independence of pressure, demonstrated rather than asserted: five pressures, one temperature
for frac in [1.0, 0.5, 0.1, 0.01, 1e-4]:
    p = frac * P_ATM
    rho = p * M_AIR / (R_GAS * T_20C)
    P('  sound speed at p/p0 = %r (T = 20 C): rho, v' % frac, rho, math.sqrt(GAMMA * p / rho))
# the density of air at 20 C, 1 atm, and the decibel drop as the air is removed
RHO_0 = P_ATM * M_AIR / (R_GAS * T_20C)
P('air density at 20 C 1 atm, kg/m^3', RHO_0)
# a piston of fixed velocity radiates p = rho c u, so the pressure amplitude goes as rho and the
# intensity I = p^2 / (rho c) goes as rho as well: both are 20 log10(rho/rho0) dB
for frac in [1.0, 0.5, 0.25, 0.1, 0.01]:
    P('  air at %r atm: pressure amplitude ratio, intensity ratio, dB' % frac,
      frac, frac, 20 * math.log10(frac))
# the mean free path, and the density at which it reaches one wavelength
mfp0 = K_B * T_20C / (math.sqrt(2) * PI * D_AIR ** 2 * P_ATM)
P('mean free path of air at 20 C 1 atm, m', mfp0)
for f in [F_MIN, F_0, F_MAX]:
    lam = V_SOUND / f
    P('  Knudsen 1 at %r Hz: lambda, and the fraction of an atmosphere where mfp = lambda' % f,
      lam, mfp0 / lam)

# =============================================================================================
print('\n# C. the calibration at 100-1000 Hz, PhET\'s own step, and the lattice\'s dispersion')
P('geometry: W, dx, source x, mid y', W_AREA, DX, (SRC_OFF + 0.5) * DX, (MID - PAD + 0.5) * DX)
P('PhET source x (viewToModelX of lattice column 40), m', (PHET_SRC_X - PHET_PAD) / 111 * W_AREA)
P('lattice: N, PAD, VIS, source column', N_LAT, PAD, VIS, SRC_I)


def phet_lambda(f, n_vis=111):
    """the wavelength PhET's own fixed time step gives at frequency f, on its own lattice"""
    dt = PHET_TIME_SCALE / PHET_EVENT_RATE
    Om = TAU * f * dt
    s = math.sin(Om / 2) / C
    if s > 1:
        return float('nan')
    return TAU / (2 * math.asin(s)) * (W_AREA / n_vis)


for f in [F_MIN, 250.0, F_0, 775.0, F_MAX]:
    Nl = cells_per_wave(f)
    Om = omega_step(Nl)
    P('  %r Hz: lambda, cells per wavelength, Omega, dt, steps per period' % f,
      V_SOUND / f, Nl, Om, step_dt(f), TAU / Om)
    # the anisotropy: the wavelength the same Omega has along the diagonal
    kd = lat_k(Om, PI / 4)
    P('  %r Hz: axis lambda in cells, diagonal lambda in cells, diagonal/axis - 1' % f,
      TAU / lat_k(Om, 0.0), TAU / kd, (TAU / kd) / (TAU / lat_k(Om, 0.0)) - 1)
    ka = lat_k(Om, 0.0)
    P('  %r Hz: phase speed and group speed along the axis, in cells per step, against C = 1/2' % f,
      lat_phase_speed(ka, 0.0), lat_group_speed(ka, 0.0), C)
    P('  %r Hz: PhET\'s fixed step on PhET\'s 151 lattice gives lambda, and lambda/(v/f) - 1' % f,
      phet_lambda(f), phet_lambda(f) / (V_SOUND / f) - 1)
    P('  %r Hz: PhET\'s cells per wavelength on its own 111-cell view' % f,
      V_SOUND / f / (W_AREA / 111))
# PhET's own time step, and the slow-motion factor of the clock
P('PhET time scale, s of model time per s of wall time, and the slow-motion factor',
  PHET_TIME_SCALE, 1 / PHET_TIME_SCALE)
P('PhET fixed time step, s', PHET_TIME_SCALE / PHET_EVENT_RATE)
# how many lattice steps a second of wall time is, here, at three frequencies
for f in [F_MIN, F_0, F_MAX]:
    P('  steps per second of wall time at %r Hz' % f, PHET_TIME_SCALE / step_dt(f))
# Mur's reflection at this sim's default: the price of the absorbing edge.  A plane wave
# a(x) e^{-i Om n} arriving at the right-hand edge is e^{ikx} + R e^{-ikx}; putting that into the
# edge update and solving for R gives the exact |R| of the discrete boundary.


def mur_R(kx, ky, order):
    Om = lat_omega(kx, ky)
    z = complex(math.cos(Om), -math.sin(Om))
    ek = complex(math.cos(kx), math.sin(kx))
    if order == 1:                       # a(0)(z + A1) = a(-1)(1 + A1 z)
        Pp, Qq = z + MUR1, 1 + MUR1 * z
    else:                                # a(0)(z - A1/z - B) = a(-1)(-1/z + A1 z + B)
        B = MUR2A - MUR2B * (2 - 2 * math.cos(ky))
        Pp = z - MUR1 / z - B
        Qq = -1 / z + MUR1 * z + B
    return abs(((1 / ek) * Qq - Pp) / (Pp - ek * Qq))


for f, th in [(F_0, 0.0), (F_0, PI / 6), (F_0, PI / 4), (F_0, PI / 3)]:
    k = lat_k(omega_step(cells_per_wave(f)), th)
    P('  Mur |R| at %r Hz, %r rad off normal (order 2, order 1)' % (f, th),
      mur_R(k * math.cos(th), k * math.sin(th), 2), mur_R(k * math.cos(th), k * math.sin(th), 1))

# =============================================================================================
print('\n# D. lambda measured on the lattice, by least squares against the drive\'s own phase')


def measure(f):
    """A fresh run at frequency f on the measurement lattice.  After MEAS_N0 steps the front has
    crossed the tank about 1.3 times; MEAS_PER whole periods are then recorded along the source's
    row, and at every cell the record is fitted by least squares to

         u(n) = a sin(phi_n) + b cos(phi_n) + c + d (n - nbar)

    against the drive's own phase, so the amplitude is hypot(a, b) and the phase atan2(b, a).
    The constant and the drift absorb the wake of the switch-on, which in two dimensions dies
    only as 1/(omega t).  lambda is 2 pi over the slope of the unwrapped phase across cells
    MEAS_R0..MEAS_R1 from the source; the envelope's power is the slope of log amplitude
    against log r over the same cells (-1/2 in two dimensions)."""
    R = Run(f, n=MEAS_N, src_off=MEAS_SRC_OFF, amp=MEAS_A)
    for _ in range(MEAS_N0):
        R.step()
    nc = MEAS_N - PAD - R.src_i
    M = math.ceil(MEAS_PER * TAU / R.Om)
    B = np.zeros((M, 4))
    Y = np.zeros((M, nc))
    for q in range(M):
        R.step()
        B[q] = [math.sin(R.phi), math.cos(R.phi), 1.0, q - (M - 1) / 2]
        Y[q] = R.lat.u[R.mid, R.src_i:R.src_i + nc]
    x, *_ = np.linalg.lstsq(B, Y, rcond=None)
    amp = np.hypot(x[0], x[1])
    ph = np.unwrap(np.arctan2(x[1], x[0]))
    rs = np.arange(nc, dtype=float)
    sl = np.polyfit(rs[MEAS_R0:MEAS_R1 + 1], ph[MEAS_R0:MEAS_R1 + 1], 1)[0]
    lam_cells = TAU / (-sl)
    pexp = np.polyfit(np.log(rs[MEAS_R0:MEAS_R1 + 1]), np.log(amp[MEAS_R0:MEAS_R1 + 1]), 1)[0]
    return dict(f=f, M=M, nc=nc, amp=amp, ph=ph, lam_cells=lam_cells, pexp=float(pexp),
                lam=lam_cells * DX, lam0=V_SOUND / f, Nl=R.Nl, steps=R.steps,
                snap=R.lat.u[R.mid, R.src_i:R.src_i + nc].copy())


P('measurement: lattice, source offset, settling steps, periods, fit window',
  MEAS_N, MEAS_SRC_OFF, MEAS_N0, MEAS_PER, MEAS_R0, MEAS_R1)
MEAS = {}
for f in MEAS_FS:
    m = measure(f)
    MEAS[f] = m
    P('MEAS %r Hz: fit steps M, cells of axis, lambda in cells, v/f in cells, ratio - 1' % f,
      m['M'], m['nc'], m['lam_cells'], m['Nl'], m['lam_cells'] / m['Nl'] - 1)
    P('MEAS %r Hz: lambda measured and v/f, m' % f, m['lam'], m['lam0'])
    P('MEAS %r Hz: envelope power of r (1/sqrt r gives -0.5)' % f, m['pexp'])
    for c in [5, 30, 60, 120]:
        P('MEAS %r Hz: amplitude and unwrapped phase at cell %d' % (f, c), m['amp'][c], m['ph'][c])

# the continuum near field, for the low-frequency reading: the phase of an outgoing 2-D point
# source is arg H0(kr) (which runs as +kr - pi/4 - 1/8kr), not kr, and fitting the SAME cells the
# lattice fit uses shows how much of the reading is the near field rather than the lattice.
# H0^(1) has an increasing phase and the lattice's sin(omega t - kr) a decreasing one, so it is
# the magnitude of the slope that is the wavenumber in both.
for f in [F_MIN, F_0, F_MAX]:
    k = TAU / (V_SOUND / f)
    r = (np.arange(MEAS_R0, MEAS_R1 + 1)) * DX
    phH = np.unwrap(np.angle(special.hankel1(0, k * r)))
    sl = np.polyfit(np.arange(MEAS_R0, MEAS_R1 + 1, dtype=float), phH, 1)[0]
    P('  continuum Hankel phase over the same cells at %r Hz: lambda/(v/f) - 1' % f,
      (TAU / abs(sl)) / (V_SOUND / f / DX) - 1)

# =============================================================================================
print('\n# E. two sources: the hyperbolic nodal lines, and the lattice\'s own')
# Two in-phase point sources on the line x = xs, at y = y1 and y = y2.  Put the origin at their
# midpoint with the sources at y = +/- c, c = d/2.  A point is on a nodal line when
#      | r1 - r2 | = (m + 1/2) lambda = 2a,   a = (m + 1/2) lambda / 2,
# which is the hyperbola  y^2/a^2 - x^2/(c^2 - a^2) = 1  with foci at the sources.  It exists
# only while a < c, i.e. (m + 1/2) lambda < d, which is how many nodal lines there are.
SEP_0 = 2 * W_AREA / 3 - W_AREA / 3         # PhET's speakers at W/3 and 2W/3
SEP_CELLS = jsround(SEP_0 / (2 * DX)) * 2   # the lattice can only put them on whole rows
SEP = SEP_CELLS * DX
P('two sources: PhET\'s separation, the lattice\'s, in cells and m', SEP_0, SEP_CELLS, SEP)


def nodes_of(d, lam):
    out = []
    m = 0
    while (m + 0.5) * lam < d:
        out.append(m)
        m += 1
    return out


def hyperbola_x(m, lam, d, y):
    """the x of the m-th nodal hyperbola at height y (origin at the midpoint of the sources,
    the sources on the y axis): x = sqrt((c^2 - a^2)(y^2/a^2 - 1))"""
    a = (m + 0.5) * lam / 2
    cc = d / 2
    t = y * y / (a * a) - 1
    if t < 0 or a >= cc:
        return float('nan')
    return math.sqrt((cc * cc - a * a) * t)


for f in [F_MIN, F_0, F_MAX]:
    lam = V_SOUND / f
    ms = nodes_of(SEP, lam)
    P('  %r Hz: lambda, d/lambda, number of nodal lines each side' % f, lam, SEP / lam, len(ms))

# the closed form against a brute-force scan: for a sample of heights, find where |r1 - r2|
# equals (m + 1/2) lambda by bisection on x, and compare with the closed form
lam0 = V_SOUND / F_0
worst = 0.0
nchecked = 0
for m in nodes_of(SEP, lam0):
    for y in [0.2, 0.5, 1.0, 2.0, 3.0]:
        xc = hyperbola_x(m, lam0, SEP, y)
        if not math.isfinite(xc):
            continue

        def g(x):
            r1 = math.hypot(x, y - SEP / 2)
            r2 = math.hypot(x, y + SEP / 2)
            return abs(r1 - r2) - (m + 0.5) * lam0
        xb = optimize.brentq(g, 1e-9, 60.0, xtol=1e-14, rtol=1e-15)
        worst = max(worst, abs(xb - xc))
        nchecked += 1
P('two sources: closed-form hyperbola against brentq on |r1-r2|, worst |dx| over %d points'
  % nchecked, worst)
# the far field: the asymptote of the m-th hyperbola is d sin(theta) = (m + 1/2) lambda
for m in nodes_of(SEP, lam0):
    a = (m + 0.5) * lam0 / 2
    cc = SEP / 2
    slope = a / math.sqrt(cc * cc - a * a)              # dy/dx of the asymptote
    th_asym = math.atan(slope)                          # angle from the x axis
    th_far = math.asin((m + 0.5) * lam0 / SEP)          # the two-slit condition, from the axis
    P('  m = %d: asymptote angle from the axis, and asin((m+1/2)lambda/d)' % m, th_asym, th_far)

# the lattice's own nodal lines: run the two-source picture and find, on a line of constant x,
# where the time-averaged square is smallest near each predicted node
def shift_rows(u, s):
    """the field of a source s rows below the lattice's own: u(i, j - s), zero off the lattice
    (the engine's latAt is zero outside, never wrapped)"""
    out = np.zeros_like(u)
    if s >= 0:
        out[s:, :] = u[:u.shape[0] - s, :] if s else u
    else:
        out[:s, :] = u[-s:, :]
    return out


Rt = Run(F_0)
for _ in range(900):
    Rt.step()
per = int(jsround(TAU / Rt.Om))
acc = np.zeros((N_LAT, N_LAT))
one = np.zeros((N_LAT, N_LAT))
for _ in range(per):
    Rt.step()
    # the two speakers are the SAME field read at two shifts in y (PhET's construction)
    sh1, sh2 = SEP_CELLS // 2, -(SEP_CELLS // 2)
    tot = shift_rows(Rt.lat.u, sh1) + shift_rows(Rt.lat.u, sh2)
    acc += tot ** 2
    one += Rt.lat.u ** 2
acc /= per
one_sq = one / per
rms = np.sqrt(acc)
mid_y = (MID - PAD + 0.5) * DX
found = []
for m in nodes_of(SEP, lam0):
    for xcol in [140, 170, 200]:
        x_model = (xcol - PAD + 0.5) * DX - (SRC_OFF + 0.5) * DX      # from the speakers' line
        # the predicted node height above the midpoint at this x
        a = (m + 0.5) * lam0 / 2
        cc = SEP / 2
        ypred = a * math.sqrt(1 + x_model * x_model / (cc * cc - a * a))
        jpred = MID + ypred / DX
        if not (PAD + 3 < jpred < N_LAT - PAD - 3):
            continue
        j0 = int(jpred)
        lo, hi = max(PAD + 1, j0 - 6), min(N_LAT - PAD - 1, j0 + 7)
        seg = rms[lo:hi, xcol]
        jm = lo + int(np.argmin(seg))
        if jm <= lo or jm >= hi - 1:
            continue
        yl, yc, yr = seg[jm - lo - 1], seg[jm - lo], seg[jm - lo + 1]
        sub = 0.5 * (yl - yr) / (yl - 2 * yc + yr)      # parabola-refined minimum
        found.append((m, xcol, jm + sub, jpred, jm + sub - jpred))
for (m, xcol, jmeas, jpred, dj) in found:
    P('  lattice node m = %d at column %d: measured row, hyperbola row, difference in cells'
      % (m, xcol), jmeas, jpred, dj)
P('two sources: worst |measured - hyperbola| over %d nodes, in cells' % len(found),
  max(abs(q[4]) for q in found))

# The drift is not noise: it is the square lattice's ANISOTROPY.  The wave leaving each source
# in a direction theta carries the wavenumber latK(Omega, theta)/dx, and off the axes that is
# smaller (the wavelength is longer), so the phase difference at the continuum node falls short
# of (2m+1) pi and the real node sits further out.  Solving
#      | k(theta1) r1 - k(theta2) r2 | = (2m + 1) pi
# for the height instead reproduces the measured rows to a fraction of a cell.
Om0 = omega_step(cells_per_wave(F_0))


def k_of_dir(dxm, dym):
    th = math.atan2(abs(dym), abs(dxm))
    return lat_k(Om0, th) / DX                      # radians per metre


def dphi(y, x):
    """|k(theta1) r1 - k(theta2) r2| at (x, y) measured from the midpoint of the sources"""
    d1 = (x, y - SEP / 2)
    d2 = (x, y + SEP / 2)
    r1, r2 = math.hypot(*d1), math.hypot(*d2)
    return abs(k_of_dir(*d1) * r1 - k_of_dir(*d2) * r2)


aniso = []
for (m, xcol, jmeas, jpred, dj) in found:
    x_model = (xcol - PAD + 0.5) * DX - (SRC_OFF + 0.5) * DX
    want = (2 * m + 1) * PI
    ylo, yhi = 0.5 * (jpred - MID) * DX, 2.0 * (jpred - MID) * DX
    ysol = optimize.brentq(lambda y: dphi(y, x_model) - want, ylo, yhi, xtol=1e-12)
    jan = MID + ysol / DX
    aniso.append(jmeas - jan)
    P('  node m = %d at column %d with the lattice\'s own k(theta): row, and measured - this'
      % (m, xcol), jan, jmeas - jan)
P('two sources: worst |measured - anisotropic prediction| over %d nodes, in cells' % len(aniso),
  max(abs(q) for q in aniso))

# The interference law at a point, MEASURED on the lattice.  Two sources of amplitudes A1 and A2
# whose waves arrive with a phase difference dphi give sqrt(A1^2 + A2^2 + 2 A1 A2 cos dphi); the
# textbook statement is dphi = 2 pi (r1 - r2)/lambda, and the same statement with the LATTICE's
# own k(theta) is what the lattice really obeys.  A1 and A2 are read off the one-source run, so
# the only thing being tested is the interference, not the spreading.
# Speaker A is the source shifted DOWN by SEP_CELLS/2 (lattice row MID + 32), so its field at a
# cell is u at the row SEP_CELLS/2 ABOVE it; speaker B is the other way about.
hA = SEP_CELLS // 2
sA = ((SRC_OFF + 0.5) * DX, (MID + hA - PAD + 0.5) * DX)
sB = ((SRC_OFF + 0.5) * DX, (MID - hA - PAD + 0.5) * DX)
P('two speakers: the lattice rows and the model y of each', MID + hA, MID - hA, sA[1], sB[1])
worst_iso = worst_ani = 0.0
for (px, py) in [(6.0, 5.0), (7.0, 3.0), (8.0, 6.5), (5.0, 2.0), (9.0, 5.0), (7.5, 7.5), (4.0, 4.5)]:
    i0 = int(PAD - 0.5 + px / DX)
    j0 = int(PAD - 0.5 + py / DX)
    meas = math.sqrt(2.0 * acc[j0, i0])                      # rms over a period -> amplitude
    aA = math.sqrt(2.0 * one_sq[j0 - hA, i0])
    aB = math.sqrt(2.0 * one_sq[j0 + hA, i0])
    dA = (px - sA[0], py - sA[1])
    dB = (px - sB[0], py - sB[1])
    rA, rB = math.hypot(*dA), math.hypot(*dB)
    two = lambda dp: math.sqrt(aA * aA + aB * aB + 2 * aA * aB * math.cos(dp))
    p_iso = two(TAU * (rA - rB) / lam0)
    p_ani = two(k_of_dir(*dA) * rA - k_of_dir(*dB) * rB)
    worst_iso = max(worst_iso, abs(meas - p_iso))
    worst_ani = max(worst_ani, abs(meas - p_ani))
    P('  two speakers at (%r, %r): measured amplitude, textbook lambda, lattice k(theta), dr'
      % (px, py), meas, p_iso, p_ani, rA - rB)
P('two speakers: worst |measured - predicted| over 7 points, textbook and with the lattice k',
  worst_iso, worst_ani)

# =============================================================================================
print('\n# F. the reflecting wall as an image source')
# The wall is a line through A = (xw, W) with direction dhat = (cos th, -sin th) (y runs DOWN,
# as on the lattice), which is PhET's own construction: its wall crosses the bottom edge at
# wallPositionX and leans back at wallAngle.  nhat = (sin th, cos th) is normal to it.  The
# sound lives where (P - A) . nhat < 0, which is exactly PhET's own test
#      x < xw - (y - W)/tan(th).
# For a rigid wall the boundary condition is du/dn = 0, and the field that satisfies it is
#      U(P) = u(P) + u(P'),   P' the mirror image of P in the wall,
# because mirroring is an isometry: |P' - S| = |P - S'|, so u(P') IS the field of the image
# source S'.  Everything below falsifies that one statement.
WALL_X0, WALL_TH0 = W_AREA / 3, PI / 4
SRC_XY = ((SRC_OFF + 0.5) * DX, (MID - PAD + 0.5) * DX)


def wall_basis(xw, th):
    A = np.array([xw, W_AREA])
    d = np.array([math.cos(th), -math.sin(th)])
    n = np.array([math.sin(th), math.cos(th)])
    return A, d, n


def mirror(Pt, xw, th):
    A, d, n = wall_basis(xw, th)
    return Pt - 2 * np.dot(Pt - A, n) * n


def in_front(Pt, xw, th):
    A, d, n = wall_basis(xw, th)
    return float(np.dot(Pt - A, n)) < 0


# (1) the mirror is an involution, preserves distance to the wall, and agrees with PhET's own
#     projection form  P' = P + 2(foot - P)
worst_inv = worst_phet = worst_dist = 0.0
for xw in [W_AREA / 3, 0.5 * W_AREA, 2 * W_AREA / 3]:
    for th in [0.1 * PI, 0.25 * PI, PI / 4, 0.4 * PI, 0.5 * PI]:
        A, d, n = wall_basis(xw, th)
        for Pt in [np.array([1.0, 2.0]), np.array([4.0, 7.0]), np.array([0.5, 5.0]), np.array([3.0, 9.0])]:
            Q = mirror(Pt, xw, th)
            worst_inv = max(worst_inv, float(np.max(np.abs(mirror(Q, xw, th) - Pt))))
            foot = A + np.dot(Pt - A, d) * d
            worst_phet = max(worst_phet, float(np.max(np.abs((Pt + 2 * (foot - Pt)) - Q))))
            worst_dist = max(worst_dist, abs(abs(np.dot(Pt - A, n)) - abs(np.dot(Q - A, n))))
P('wall: mirror involution, PhET\'s projection form, distance to the wall (worst over 60)',
  worst_inv, worst_phet, worst_dist)
# (2) the angles.  The ray from S to P by way of the wall meets it where the straight line from
#     the IMAGE S' to P crosses it; there the angle of incidence equals the angle of reflection,
#     and the path S->Q->P is exactly |S'P| (Fermat).
S = np.array(SRC_XY)
worst_ang = worst_fermat = 0.0
nray = 0
rays = []
for xw, th in [(W_AREA / 3, PI / 4), (0.5 * W_AREA, 0.3 * PI), (2 * W_AREA / 3, 0.15 * PI),
               (W_AREA / 3, 0.5 * PI)]:
    A, d, n = wall_basis(xw, th)
    Sp = mirror(S, xw, th)
    for Pt in [np.array([2.0, 8.5]), np.array([3.0, 7.0]), np.array([1.0, 9.0]), np.array([4.5, 9.5])]:
        if not in_front(Pt, xw, th):
            continue
        # where the segment S'->P crosses the wall
        t = np.dot(A - Sp, n) / np.dot(Pt - Sp, n)
        Q = Sp + t * (Pt - Sp)
        if not (0 < t < 1):
            continue
        inc = (Q - S) / np.linalg.norm(Q - S)
        ref = (Pt - Q) / np.linalg.norm(Pt - Q)
        a_in = math.acos(min(1.0, abs(float(np.dot(inc, n)))))
        a_out = math.acos(min(1.0, abs(float(np.dot(ref, n)))))
        worst_ang = max(worst_ang, abs(a_in - a_out))
        worst_fermat = max(worst_fermat, abs(np.linalg.norm(Q - S) + np.linalg.norm(Pt - Q)
                                             - np.linalg.norm(Pt - Sp)))
        nray += 1
        rays.append((xw, th, tuple(Pt), tuple(Q), a_in, a_out))
P('wall: |angle of incidence - angle of reflection| and |SQ + QP - S\'P| (worst over %d rays)'
  % nray, worst_ang, worst_fermat)
for (xw, th, P_, Q_, a_in, a_out) in rays[:4]:
    P('  ray at xw = %r, th = %r to (%r, %r): wall point, angles from the normal'
      % (xw, th, float(P_[0]), float(P_[1])), Q_[0], Q_[1], a_in, a_out)
# the image source itself, for the four wall settings the sim can show
for xw, th in [(W_AREA / 3, PI / 4), (0.5 * W_AREA, 0.3 * PI), (2 * W_AREA / 3, 0.1 * PI),
               (W_AREA / 3, 0.5 * PI)]:
    Sp = mirror(S, xw, th)
    P('  image source for xw = %r, angle = %r rad' % (xw, th), Sp[0], Sp[1],
      float(np.linalg.norm(Sp - S)))
# (3) the Neumann condition, ON THE LATTICE FIELD the sim actually draws: the normal derivative
#     of u(P) + u(P') vanishes on the wall, by construction, and a finite difference says so.
Rw = Run(F_0)
for _ in range(700):
    Rw.step()


def bilinear(u, X, Y):
    """the engine's probeValue: bilinear in LATTICE coordinates, zero outside"""
    if not (0 <= X <= u.shape[1] - 1 and 0 <= Y <= u.shape[0] - 1):
        return 0.0
    i0 = min(int(math.floor(X)), u.shape[1] - 2)
    j0 = min(int(math.floor(Y)), u.shape[0] - 2)
    fx, fy = X - i0, Y - j0
    return ((1 - fy) * ((1 - fx) * u[j0, i0] + fx * u[j0, i0 + 1])
            + fy * ((1 - fx) * u[j0 + 1, i0] + fx * u[j0 + 1, i0 + 1]))


def total_at(u, Pm, xw, th):
    """the drawn field at a model point: the direct wave plus its image"""
    Q = mirror(np.asarray(Pm), xw, th)
    to_lat = lambda p: (PAD - 0.5 + p[0] / DX, PAD - 0.5 + p[1] / DX)
    a = bilinear(u, *to_lat(Pm))
    b = bilinear(u, *to_lat(Q))
    return a + b


worst_neu = 0.0
for xw, th in [(W_AREA / 3, PI / 4), (0.5 * W_AREA, 0.3 * PI), (2 * W_AREA / 3, 0.15 * PI)]:
    A, d, n = wall_basis(xw, th)
    for s in [-2.0, -1.0, 0.0, 1.0, 2.0]:
        Pw = A + s * d                                   # a point ON the wall
        if not (0 < Pw[0] < W_AREA and 0 < Pw[1] < W_AREA):
            continue
        h = 0.01
        f1 = total_at(Rw.lat.u, Pw - h * n, xw, th)
        f2 = total_at(Rw.lat.u, Pw + h * n, xw, th)
        worst_neu = max(worst_neu, abs(f1 - f2) / (2 * h) / max(1e-9, abs(f1)))
P('wall: worst relative |du/dn| on the wall, from the drawn field (should be 0 by construction)',
  worst_neu)
# (4) the interference the wall makes is the same geometry as two speakers: the direct wave and
#     the image wave are two sources at S and S', so the loud lines are |r - r'| = m lambda
Sp = mirror(S, WALL_X0, WALL_TH0)
dSS = float(np.linalg.norm(Sp - S))
P('wall at xw = W/3, 45 deg: the image source, the S-S\' separation, and d/lambda at 550 Hz',
  Sp[0], Sp[1], dSS, dSS / lam0)

# =============================================================================================
print('\n# F2. the three composed pictures, cell by cell: one speaker, two speakers, the wall')
# Every view draws the SAME lattice field, read straight (one speaker), read at two shifts in y
# (two speakers) or read twice, once direct and once mirrored in the wall (reflection), with
# nothing drawn behind the wall.  These are the pins the JS composition is asserted against.
Rc = Run(F_0)
for _ in range(400):
    Rc.step()
uc = Rc.lat.u
CELLS = [(70, 115), (110, 100), (150, 150), (190, 80), (120, 190), (205, 40)]
for (i, j) in CELLS:
    P('COMP one (%d,%d)' % (i, j), uc[j, i])
hA = SEP_CELLS // 2
for (i, j) in CELLS:
    a = uc[j - hA, i] if 0 <= j - hA < N_LAT else 0.0
    b = uc[j + hA, i] if 0 <= j + hA < N_LAT else 0.0
    P('COMP two (%d,%d)' % (i, j), a + b, a, b)
for (i, j) in CELLS:
    # the model point of the cell centre, then PhET's construction: mirror, round, read
    Pm = np.array([(i - PAD + 0.5) * DX, (j - PAD + 0.5) * DX])
    front = in_front(Pm, WALL_X0, WALL_TH0)
    if not front:
        P('COMP wall (%d,%d)' % (i, j), 0.0, 0.0, 0.0, 0)
        continue
    Q = mirror(Pm, WALL_X0, WALL_TH0)
    qi = jsround(PAD - 0.5 + Q[0] / DX)
    qj = jsround(PAD - 0.5 + Q[1] / DX)
    im = uc[qj, qi] if (0 <= qi < N_LAT and 0 <= qj < N_LAT) else 0.0
    P('COMP wall (%d,%d)' % (i, j), uc[j, i] + im, uc[j, i], im, 1)
# how much of the visible area the wall hides, at the four corners of its two sliders
for xw, th in [(W_AREA / 3, 0.1 * PI), (W_AREA / 3, 0.5 * PI), (2 * W_AREA / 3, 0.1 * PI),
               (2 * W_AREA / 3, 0.5 * PI)]:
    n_front = 0
    for j in range(PAD, N_LAT - PAD):
        for i in range(PAD, N_LAT - PAD):
            if in_front(np.array([(i - PAD + 0.5) * DX, (j - PAD + 0.5) * DX]), xw, th):
                n_front += 1
    P('  wall xw = %r, angle = %r: visible cells in front of it, and the fraction' % (xw, th),
      n_front, n_front / (VIS * VIS))

# =============================================================================================
print('\n# G. the listener')
# PhET's own interference law at the listener is  A |cos(pi dr / lambda)|  with lambda = 36/f in
# MODEL UNITS -- a hand-tuned constant, not v/f.  This sim reads the field the lattice actually
# holds at the listener instead, and prints both so the difference is visible.
P('PhET\'s listener wavelength 36/f model units at 100, 550 and 1000 Hz, m',
  *[PHET_LISTENER_LAMBDA_K / (f / 1000) / 100 for f in [F_MIN, F_0, F_MAX]])
P('the true wavelength v/f at the same three frequencies, m',
  *[V_SOUND / f for f in [F_MIN, F_0, F_MAX]])
P('PhET\'s listener wavelength over v/f', PHET_LISTENER_LAMBDA_K * 10 / V_SOUND)
LIS = (0.5 * W_AREA, 0.5 * W_AREA)
SPK1 = ((SRC_OFF + 0.5) * DX, (MID - 32 - PAD + 0.5) * DX)
SPK2 = ((SRC_OFF + 0.5) * DX, (MID + 32 - PAD + 0.5) * DX)
r1 = math.hypot(LIS[0] - SPK1[0], LIS[1] - SPK1[1])
r2 = math.hypot(LIS[0] - SPK2[0], LIS[1] - SPK2[1])
P('two speakers at the lattice rows 83 and 147, listener at the centre: r1, r2, r1 - r2',
  r1, r2, r1 - r2)
for f in [F_MIN, F_0, F_MAX]:
    P('  listener factor |cos(pi dr/lambda)| at %r Hz' % f,
      abs(math.cos(PI * (r1 - r2) / (V_SOUND / f))))
# a listener moved off the axis of symmetry, where the path difference is not zero
LIS2 = (7.0, 3.0)
q1 = math.hypot(LIS2[0] - SPK1[0], LIS2[1] - SPK1[1])
q2 = math.hypot(LIS2[0] - SPK2[0], LIS2[1] - SPK2[1])
P('listener at (7, 3): r1, r2, dr, and dr/lambda at 550 Hz', q1, q2, q1 - q2, (q1 - q2) / lam0)
for f in [F_MIN, F_0, F_MAX]:
    P('  listener at (7, 3): factor at %r Hz' % f, abs(math.cos(PI * (q1 - q2) / (V_SOUND / f))))

# =============================================================================================
print('\n# H. the pieces the drawing rests on')
# the colour scale, PhET's: its alpha runs linearly from 0.4 at u = 0 to 1 at u = +2, and from
# 0.4 down to 0.03 at u = -1.5; this sim uses a symmetric +/-2 instead, and says so.
P('PhET\'s contrast: full white at u =, full black at u =, this sim\'s symmetric scale', 2.0, -1.5, U_FULL)
P('PhET\'s linear distance taper: it fades the drawn field to zero at this many cells, and metres',
  PHET_MAX_SOUND_DIST, PHET_MAX_SOUND_DIST * W_AREA / 111)
# the parcel displacement: xi = grad p / (rho omega^2) for one frequency, drawn exaggerated
P('parcels: rows and columns, and the fraction of the spacing a full-contrast wave moves one',
  PARC_N + 1, PARC_N + 1, PARC_PUSH)

# =============================================================================================
print('\n# I. the point reads, the parcels, the tone and the wall on the box')
# the listener and the probes read the composed field BILINEARLY, not by rounding: these are the
# pins for that path, in all three compositions, off the run of section F2.


def to_lat(x, y):
    return (PAD - 0.5 + x / DX, PAD - 0.5 + y / DX)


PTS = [(5.0, 5.0), (7.0, 3.0), (3.4, 6.2), (9.1, 8.3)]
for (px, py) in PTS:
    X, Y = to_lat(px, py)
    P('FIELD one at (%r, %r)' % (px, py), bilinear(uc, X, Y))
for (px, py) in PTS:
    X, Y = to_lat(px, py)
    P('FIELD two at (%r, %r)' % (px, py),
      bilinear(uc, X, Y - hA) + bilinear(uc, X, Y + hA))
for (px, py) in PTS:
    X, Y = to_lat(px, py)
    if not in_front(np.array([px, py]), WALL_X0, WALL_TH0):
        P('FIELD wall at (%r, %r)' % (px, py), 0.0)
        continue
    Q = mirror(np.array([px, py]), WALL_X0, WALL_TH0)
    P('FIELD wall at (%r, %r)' % (px, py), bilinear(uc, X, Y) + bilinear(uc, *to_lat(Q[0], Q[1])))

# the air parcels: the same grid, the same 21 x 21 layout, the same exaggeration
R_par = Run(F_0)
for _ in range(400):
    R_par.step()
gv = R_par.lat.u[PAD:N_LAT - PAD, PAD:N_LAT - PAD].copy()
kk = TAU / cells_per_wave(F_0)
KD = PARC_PUSH * (VIS / PARC_N) / (kk * U_FULL)
P('parcels: the exaggeration KD, in cells per unit of gradient', KD)
par = []
for a in range(PARC_N + 1):
    for b in range(PARC_N + 1):
        i = min(max(jsround(a * VIS / PARC_N), 1), VIS - 2)
        j = min(max(jsround(b * VIS / PARC_N), 1), VIS - 2)
        gx = (gv[j, i + 1] - gv[j, i - 1]) / 2
        gy = (gv[j + 1, i] - gv[j - 1, i]) / 2
        par.append((i + KD * gx, j + KD * gy))
for q in [0, 100, 220, 440]:
    P('parcels: number %d at' % q, par[q][0], par[q][1])
push = max(max(abs(par[q][0] - min(max(jsround((q // (PARC_N + 1)) * VIS / PARC_N), 1), VIS - 2)),
               abs(par[q][1] - min(max(jsround((q % (PARC_N + 1)) * VIS / PARC_N), 1), VIS - 2)))
           for q in range(len(par)))
P('parcels: the largest push, in cells and as a fraction of the spacing',
  push, push / (VIS / PARC_N))

# the tone: a buffer of whole cycles, so it loops without a click
TONE_SR, TONE_SECONDS = 44100, 0.5
for hz, level in [(550.0, 0.15), (100.0, 0.3), (1000.0, 0.09)]:
    m = max(1, jsround(hz * TONE_SECONDS))
    L = jsround(m * TONE_SR / hz)
    data = level * np.sin(TAU * m * np.arange(L) / L)
    ups = 0
    for q in range(1, L):
        if data[q - 1] < 0 <= data[q]:
            ups += 1
    P('tone %r Hz at level %r: cycles, samples, looped frequency' % (hz, level), m, L, m * TONE_SR / L)
    P('  tone %r Hz: sample[1], sample[17], sample[1000], upward zero crossings' % hz,
      data[1], data[17], data[1000], ups)

# where the wall line meets the box (what the drawing needs), for four settings
for xw, th in [(W_AREA / 3, PI / 4), (W_AREA / 3, 0.5 * PI), (2 * W_AREA / 3, 0.1 * PI),
               (0.5 * W_AREA, 0.3 * PI)]:
    A, d, n = wall_basis(xw, th)
    pts = []
    for (X, Y) in ([(A[0] + (0 - A[1]) * d[0] / d[1], 0.0), (A[0] + (W_AREA - A[1]) * d[0] / d[1], W_AREA)]
                   if abs(d[1]) > 1e-12 else []):
        if -1e-9 <= X <= W_AREA + 1e-9 and -1e-9 <= Y <= W_AREA + 1e-9:
            pts.append((X, Y))
    if abs(d[0]) > 1e-12:
        for (X, Y) in [(0.0, A[1] + (0 - A[0]) * d[1] / d[0]), (W_AREA, A[1] + (W_AREA - A[0]) * d[1] / d[0])]:
            if -1e-9 <= X <= W_AREA + 1e-9 and -1e-9 <= Y <= W_AREA + 1e-9:
                pts.append((X, Y))
    best, bd = (pts[0], pts[1]), -1.0
    for i in range(len(pts)):
        for j in range(i + 1, len(pts)):
            dd = math.hypot(pts[i][0] - pts[j][0], pts[i][1] - pts[j][1])
            if dd > bd:
                bd, best = dd, (pts[i], pts[j])
    P('  wall xw = %r angle = %r meets the box at' % (xw, th),
      best[0][0], best[0][1], best[1][0], best[1][1])

with io.open(os.path.join(HERE, 'p7_refs.js'), 'w', encoding='utf-8') as fh:
    fh.write('\n/* the reference values: every line derive.py printed (refvals.txt), keyed by its label and\n'
             '   written by derive.py itself, so no number here was typed by hand */\nconst REF=')
    fh.write(json.dumps(REFS, separators=(',', ':')))
    fh.write(';\n')
print('\n# %d reference lines written to p7_refs.js' % len(REFS))
print('# done')
