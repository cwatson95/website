#!/usr/bin/env python3
"""derive.py — the Python twin of fourier-making-waves.html.

PLAYBOOK step 3: re-derive every closed form the sim implements, check limits,
signs and dimensions, cross-check anything clever against a brute-force
version, and print reference values to 15+ digits for selfTest() to assert.

Nothing here is copied from the sim.  Where a number is PhET's it is read out
of docs/phets/fourier-making-waves_en.html (build 1.1.5) and named as such.

Sections
  A  PhET's constants, read from the minified original
  B  the preset Fourier coefficients: closed forms vs quad on the waveform
  C  Parseval, exact and truncated
  D  Gibbs: the Wilbraham-Gibbs constant, and the finite-M overshoot
  E  the truncation error, term by term
  F  analysis: the projection integral, direct DFT and a radix-2 FFT
  G  the wave packet: the transform pair, Poisson periodisation, the tail
  H  the wave-game amplitude alphabet
"""
import io
import json
import math
import os
import re

import numpy as np
from scipy import integrate, special, optimize

OUT = []


def emit(name, value, note=''):
    """Record a reference value for selfTest, printed to full double precision."""
    if isinstance(value, (list, tuple, np.ndarray)):
        s = '[' + ', '.join(repr(float(v)) for v in np.asarray(value).ravel()) + ']'
    elif isinstance(value, (bool, np.bool_)):
        s = 'true' if value else 'false'
    elif isinstance(value, (int, np.integer)):
        s = str(int(value))
    else:
        s = repr(float(value))
    OUT.append('%-52s %s%s' % (name, s, ('   # ' + note) if note else ''))
    return value


def head(t):
    OUT.append('')
    OUT.append('=== %s ===' % t)


# ----------------------------------------------------------------------------
# A.  PhET's constants, read out of the shipped build
# ----------------------------------------------------------------------------
head('A  PhET constants (fourier-making-waves 1.1.5)')
PHET = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                    '..', '..', '..', 'phets', 'fourier-making-waves_en.html')
src = io.open(PHET, encoding='utf-8', errors='replace').read()

m = re.search(r'MAX_HARMONICS:(\d+),MAX_AMPLITUDE:([\d.]+),', src)
MAX_HARMONICS, MAX_AMPLITUDE = int(m.group(1)), float(m.group(2))
m2 = re.search(r'NUMBER_OF_GAME_LEVELS:(\d+)', src)
N_LEVELS = int(m2.group(1))
m3 = re.search(r'DISCRETE_AMPLITUDE_STEP:([\d.]+)', src)
D_STEP = float(m3.group(1))
m4 = re.search(r'WAVE_GAME_AMPLITUDE_STEP:([\d.]+)', src)
G_STEP = float(m4.group(1))
m5 = re.search(r'this\.fundamentalFrequency=(\d+),this\.fundamentalPeriod=1e3/this\.fundamentalFrequency,'
               r'this\.fundamentalWavelength=(\d+)', src)
F1, L = float(m5.group(1)), float(m5.group(2))
T = 1e3 / F1
emit('MAX_HARMONICS', MAX_HARMONICS, "PhET's value")
emit('MAX_AMPLITUDE', MAX_AMPLITUDE, "PhET's value")
emit('N_GAME_LEVELS', N_LEVELS, "PhET's value")
emit('DISCRETE_AMPLITUDE_STEP', D_STEP, "PhET's value")
emit('WAVE_GAME_AMPLITUDE_STEP', G_STEP, "PhET's value")
emit('F1_Hz', F1, "PhET's fundamental frequency")
emit('L_m', L, "PhET's fundamental wavelength")
emit('T_ms', T, 'T = 1000/f1, ms')
emit('k1_rad_per_m', 2 * math.pi / L)
emit('omega1_rad_per_ms', 2 * math.pi / T)

# the wave-packet screen's model, also read out of the build
mw = re.search(r'this\.waveNumberRange=new \w+\.A\(0,24\*Math\.PI\)', src)
assert mw, 'wave-number range not found'
KMAX = 24 * math.pi
emit('WP_KMAX', KMAX, "PhET's wave-number range 0..24 pi")
emit('WP_K0_DEFAULT', 12 * math.pi, "PhET's default centre")
emit('WP_K0_MIN', 9 * math.pi)
emit('WP_K0_MAX', 15 * math.pi)
emit('WP_SIGMA_DEFAULT', 3 * math.pi, "PhET's default width")
emit('WP_SIGMA_MIN', math.pi)
emit('WP_SIGMA_MAX', 4 * math.pi)
emit('WP_SPACINGS', [0.0, math.pi / 4, math.pi / 2, math.pi], "PhET's four component spacings")

# ----------------------------------------------------------------------------
# B.  the presets.  Closed forms, and the waveform they belong to.
# ----------------------------------------------------------------------------
head('B  preset coefficients: closed form vs quadrature on the waveform')

# The four classic waveforms, as functions of the phase u = 2 pi x / L.
# square (sin)   : +1 on (0, pi), -1 on (pi, 2pi)      -- odd
# square (cos)   : the same shifted a quarter period    -- even
# triangle (sin) : peak +1 at u = pi/2                  -- odd
# triangle (cos) : peak +1 at u = 0                     -- even
# sawtooth       : 2x/L on (-L/2, L/2), i.e. u/pi       -- odd only


def wrap(u):
    return (u + math.pi) % (2 * math.pi) - math.pi          # into (-pi, pi]


def sq_sin(u):
    return math.copysign(1.0, math.sin(u)) if math.sin(u) != 0 else 0.0


def sq_cos(u):
    return math.copysign(1.0, math.cos(u)) if math.cos(u) != 0 else 0.0


def tri_sin(u):
    return (2 / math.pi) * math.asin(min(1.0, max(-1.0, math.sin(u))))


def tri_cos(u):
    return (2 / math.pi) * math.asin(min(1.0, max(-1.0, math.cos(u))))


def saw(u):
    return wrap(u) / math.pi


def coeff(f, n, kind):
    """b_n (kind='sin') or a_n (kind='cos') of f over one period in u."""
    g = (lambda u: f(u) * math.sin(n * u)) if kind == 'sin' else (lambda u: f(u) * math.cos(n * u))
    tot = 0.0
    # break at the discontinuities/corners so quad is not asked to guess
    brk = np.linspace(-math.pi, math.pi, 4 * n + 5)
    for a, b in zip(brk[:-1], brk[1:]):
        tot += integrate.quad(g, a, b, limit=200, epsabs=1e-14, epsrel=1e-14)[0]
    return tot / math.pi


def preset_closed(name, series, N):
    """The closed forms PhET uses (and every textbook prints)."""
    out = []
    for n in range(1, N + 1):
        if name == 'sinusoid':
            out.append(1.0 if n == 1 else 0.0)
        elif name == 'triangle':
            if n % 2 == 0:
                out.append(0.0)
            elif series == 'sin':
                out.append((-1.0) ** ((n - 1) // 2) * 8.0 / (n * n * math.pi * math.pi))
            else:
                out.append(8.0 / (n * n * math.pi * math.pi))
        elif name == 'square':
            if n % 2 == 0:
                out.append(0.0)
            elif series == 'sin':
                out.append(4.0 / (n * math.pi))
            else:
                out.append((-1.0) ** ((n - 1) // 2) * 4.0 / (n * math.pi))
        elif name == 'sawtooth':
            out.append((-1.0) ** (n - 1) * 2.0 / (n * math.pi))
        elif name == 'wavePacket':
            c, s = (N + 1) / 2.0, N / 5.0
            out.append(math.exp(-((n - c) ** 2) / (2 * s * s)))
        else:
            raise ValueError(name)
    return out


WAVE = {('square', 'sin'): sq_sin, ('square', 'cos'): sq_cos,
        ('triangle', 'sin'): tri_sin, ('triangle', 'cos'): tri_cos,
        ('sawtooth', 'sin'): saw}
worst = 0.0
for (name, series), f in sorted(WAVE.items()):
    cl = preset_closed(name, series, MAX_HARMONICS)
    num = [coeff(f, n, series) for n in range(1, MAX_HARMONICS + 1)]
    d = max(abs(a - b) for a, b in zip(cl, num))
    worst = max(worst, d)
    OUT.append('  %-8s %-3s closed vs quad: max |diff| = %.3e' % (name, series, d))
    # and the coefficients of the OTHER parity must vanish
    other = 'cos' if series == 'sin' else 'sin'
    dz = max(abs(coeff(f, n, other)) for n in range(1, MAX_HARMONICS + 1))
    OUT.append('  %-8s %-3s the %s coefficients vanish: max |a| = %.3e' % (name, series, other, dz))
    assert dz < 1e-12, (name, series, dz)
assert worst < 1e-11, worst
emit('preset_closed_vs_quad_worst', worst, 'closed forms ARE the waveforms')

for name, series in [('square', 'sin'), ('square', 'cos'), ('triangle', 'sin'),
                     ('triangle', 'cos'), ('sawtooth', 'sin'), ('wavePacket', 'sin'),
                     ('sinusoid', 'sin')]:
    emit('A_%s_%s' % (name, series), preset_closed(name, series, MAX_HARMONICS))

# PhET's hard-coded wave-packet table, read straight out of the build
mtab = re.search(r'Gg\.WAVE_PACKET=new Gg\(\{getAmplitudes:\(e,t\)=>(\[\[1\].*?\])\[e-1\]', src, re.S)
tab = json.loads(re.sub(r'(?<=[\[,])\.', '0.', mtab.group(1)))   # JS writes .457833, JSON needs 0.457833
assert len(tab) == MAX_HARMONICS
wp_worst, wp_outliers = 0.0, []
for N in range(1, MAX_HARMONICS + 1):
    mine = preset_closed('wavePacket', 'sin', N)
    for n, (a, b) in enumerate(zip(mine, tab[N - 1]), 1):
        if abs(a - b) > 1e-6:
            wp_outliers.append((N, n, a, b))
        else:
            wp_worst = max(wp_worst, abs(a - b))
    # the width itself, fitted from the table rather than assumed
    if N >= 2:
        num = sum((n - (N + 1) / 2.0) ** 2 for n in range(1, N + 1) if tab[N - 1][n - 1] > 1e-6)
        den = sum(-2 * math.log(tab[N - 1][n - 1]) for n in range(1, N + 1) if tab[N - 1][n - 1] > 1e-6)
        OUT.append('  N=%-3d sigma fitted from PhET\'s own numbers = %.6f   (N/5 = %.6f)'
                   % (N, math.sqrt(num / den), N / 5.0))
        assert abs(math.sqrt(num / den) - N / 5.0) < 2e-5
OUT.append('  PhET wave-packet table vs exp(-(n-c)^2/2s^2), c=(N+1)/2, s=N/5:')
OUT.append('    max |diff| over N = 1..11 = %.3e  (PhET prints 6 decimals)' % wp_worst)
for N, n, a, b in wp_outliers:
    OUT.append('    OUTLIER N=%d n=%d: the Gaussian gives %.6f, PhET\'s table says %.6f '
               '(a transposed digit in PhET\'s table; this sim uses the closed form)' % (N, n, a, b))
assert wp_worst < 6e-7, wp_worst
assert [o[:2] for o in wp_outliers] == [(10, 2), (10, 9)], wp_outliers   # one value, mirrored
emit('wavepacket_table_vs_gaussian', wp_worst, "PhET's table IS that Gaussian, bar one typo")
emit('wavepacket_phet_typo_N10_n2', tab[9][1],
     "PhET's table; the Gaussian is %.6f" % preset_closed('wavePacket', 'sin', 10)[1])
emit('wavepacket_gaussian_N10_n2', preset_closed('wavePacket', 'sin', 10)[1])
emit('wavepacket_sigma_over_N', 1 / 5.0, 'sigma = N/5')

# ----------------------------------------------------------------------------
# C.  Parseval
# ----------------------------------------------------------------------------
head('C  Parseval')


def mean_square_series(A, series):
    """<f^2> over a period for f = sum A_n sin/cos(n u), by quadrature."""
    def f2(u):
        s = 0.0
        for n, a in enumerate(A, 1):
            s += a * (math.sin(n * u) if series == 'sin' else math.cos(n * u))
        return s * s
    tot = 0.0
    br = np.linspace(-math.pi, math.pi, 2 * len(A) + 9)
    for a, b in zip(br[:-1], br[1:]):
        tot += integrate.quad(f2, a, b, limit=300, epsabs=1e-14, epsrel=1e-14)[0]
    return tot / (2 * math.pi)


rng = np.random.default_rng(20260922)
worstP = 0.0
for name, series in [('square', 'sin'), ('triangle', 'cos'), ('sawtooth', 'sin')]:
    A = preset_closed(name, series, MAX_HARMONICS)
    lhs, rhs = mean_square_series(A, series), 0.5 * sum(a * a for a in A)
    worstP = max(worstP, abs(lhs - rhs))
    OUT.append('  %-8s %-3s <f^2> = %.15f   (1/2) sum A^2 = %.15f' % (name, series, lhs, rhs))
for k in range(4):
    A = list(rng.uniform(-MAX_AMPLITUDE, MAX_AMPLITUDE, MAX_HARMONICS))
    for series in ('sin', 'cos'):
        lhs, rhs = mean_square_series(A, series), 0.5 * sum(a * a for a in A)
        worstP = max(worstP, abs(lhs - rhs))
    if k == 0:
        emit('parseval_random_A', A)
        emit('parseval_random_ms', 0.5 * sum(a * a for a in A))
assert worstP < 1e-12, worstP
emit('parseval_worst_residual', worstP, 'quadrature vs (1/2) sum A^2')

# the infinite series: the exact mean square of each waveform
head('C2  Parseval for the complete series (infinite)')
for name, series, f, exact, label in [
        ('square', 'sin', sq_sin, 1.0, '1'),
        ('triangle', 'cos', tri_cos, 1 / 3.0, '1/3'),
        ('sawtooth', 'sin', saw, 1 / 3.0, '1/3')]:
    ms = integrate.quad(lambda u: f(u) ** 2, -math.pi, math.pi,
                        limit=400, epsabs=1e-14, epsrel=1e-14)[0] / (2 * math.pi)
    OUT.append('  %-8s <f^2> = %.15f  (exact %s, diff %.2e)' % (name, ms, label, abs(ms - exact)))
    assert abs(ms - exact) < 1e-12
emit('ms_square_exact', 1.0, 'sum over odd n of (1/2)(4/pi n)^2 = (8/pi^2)(pi^2/8)')
emit('ms_triangle_exact', 1 / 3.0, '(32/pi^4) sum_odd n^-4 = (32/pi^4)(pi^4/96)')
emit('ms_sawtooth_exact', 1 / 3.0, '(2/pi^2) sum n^-2 = (2/pi^2)(pi^2/6)')

# ----------------------------------------------------------------------------
# D.  Gibbs
# ----------------------------------------------------------------------------
head('D  Gibbs')
Si_pi = float(special.sici(math.pi)[0])
GIBBS_PEAK = 2 / math.pi * Si_pi                      # the limit of the partial sum's max
GIBBS_FRAC = GIBBS_PEAK / 2 - 0.5                     # overshoot as a fraction of the JUMP (2)
emit('Si_pi', Si_pi, 'scipy.special.sici')
emit('gibbs_peak', GIBBS_PEAK, '(2/pi) Si(pi): the limit of max S_M for the unit square wave')
emit('gibbs_fraction_of_jump', GIBBS_FRAC, 'the Wilbraham-Gibbs constant, 8.9490 %')


def square_partial_max(M):
    """max of the M-term (odd harmonics 1..2M-1) square-wave partial sum.

    Brute force: dense sampling + a refined bracket, so the closed form below
    is checked rather than assumed."""
    def S(u):
        return sum(4 / (math.pi * (2 * m - 1)) * math.sin((2 * m - 1) * u) for m in range(1, M + 1))
    us = np.linspace(1e-9, math.pi - 1e-9, 40000)      # the whole half period: the FIRST peak is the global one
    vs = np.array([S(u) for u in us])
    i = int(np.argmax(vs))
    lo, hi = us[max(i - 1, 0)], us[min(i + 1, len(us) - 1)]
    r = optimize.minimize_scalar(lambda u: -S(u), bounds=(lo, hi), method='bounded',
                                 options={'xatol': 1e-15})
    return -r.fun, r.x


def square_partial_max_closed(M):
    """The first maximum is at u = pi/(2M) exactly (S' = sin(2Mu)/(2 sin u) * 8/(2pi)),
    and there S_M = sum 4/(pi(2m-1)) sin((2m-1) pi/(2M))."""
    u = math.pi / (2 * M)
    return sum(4 / (math.pi * (2 * m - 1)) * math.sin((2 * m - 1) * u) for m in range(1, M + 1)), u


for M in (1, 2, 3, 6, 12, 50, 400):
    v1, u1 = square_partial_max(M)
    v2, u2 = square_partial_max_closed(M)
    OUT.append('  M=%-4d peak %.15f at u=%.15f   (closed %.15f at %.15f, diff %.2e)'
               % (M, v1, u1, v2, u2, abs(v1 - v2)))
    assert abs(v1 - v2) < 1e-9, (M, v1, v2)
emit('gibbs_peak_M1', square_partial_max_closed(1)[0])
emit('gibbs_peak_M2', square_partial_max_closed(2)[0])
emit('gibbs_peak_M6', square_partial_max_closed(6)[0], '11 harmonics: PhET\'s maximum')
emit('gibbs_peak_M50', square_partial_max_closed(50)[0])
emit('gibbs_peak_M400', square_partial_max_closed(400)[0])
emit('gibbs_x_M6_over_L', 1 / (4.0 * 6), 'the first peak sits at x = L/(4M)')
# the approach to the limit is O(1/M^2)
e6, e12, e24 = (square_partial_max_closed(M)[0] - GIBBS_PEAK for M in (6, 12, 24))
OUT.append('  the peak approaches the limit as 1/M^2: ratios %.4f, %.4f (4 expected)'
           % (e6 / e12, e12 / e24))
emit('gibbs_err_ratio_6_12', e6 / e12, 'O(1/M^2) approach')

# the triangle wave does NOT overshoot (it is continuous) -- a falsifier
tri_over = max(abs(sum(preset_closed('triangle', 'cos', 41)[n - 1] * math.cos(n * u)
                       for n in range(1, 42))) for u in np.linspace(0, math.pi, 4001))
OUT.append('  triangle (41 terms) max |S| = %.15f  <= 1: no Gibbs, it is continuous' % tri_over)
assert tri_over <= 1.0 + 1e-12
emit('triangle_partial_max_41', tri_over, 'continuous: never exceeds 1')

# the sawtooth's jump is 2 as well, so it shows the SAME 8.9 % of the jump
def saw_partial_max(N):
    def S(u):
        return sum((-1) ** (n - 1) * 2 / (math.pi * n) * math.sin(n * u) for n in range(1, N + 1))
    u = math.pi * N / (N + 1)                     # the last extremum before the jump
    return S(u)


for N in (11, 100, 1000):
    v = saw_partial_max(N)
    OUT.append('  sawtooth N=%-5d peak %.15f  -> overshoot/jump = %.10f' % (N, v, (v - 1) / 2))
emit('saw_peak_N11', saw_partial_max(11))
emit('saw_peak_N1000', saw_partial_max(1000), '-> the same Wilbraham-Gibbs fraction')

# ----------------------------------------------------------------------------
# E.  truncation error
# ----------------------------------------------------------------------------
head('E  truncation error: ||f - S_N||^2 = (1/2) sum_{n>N} A_n^2')


MS_EXACT = {('square', 'sin'): 1.0, ('square', 'cos'): 1.0, ('triangle', 'sin'): 1 / 3.0,
            ('triangle', 'cos'): 1 / 3.0, ('sawtooth', 'sin'): 1 / 3.0}


def tail_l2(name, series, N):
    """||f - S_N|| = sqrt(<f^2> - (1/2) sum_{n<=N} A_n^2) -- Parseval, exactly."""
    A = preset_closed(name, series, N)
    return math.sqrt(max(0.0, MS_EXACT[(name, series)] - 0.5 * sum(a * a for a in A)))


# and the same thing the other way round, as a tail sum with its own remainder
for name, series in [('square', 'sin'), ('triangle', 'cos'), ('sawtooth', 'sin')]:
    A = preset_closed(name, series, 60000)
    part = math.sqrt(0.5 * sum(a * a for a in A[11:]))
    OUT.append('  %-8s %-3s N=11: Parseval %.15f, tail sum to n=60000 %.15f (short by %.1e, '
               'the remaining tail)' % (name, series, tail_l2(name, series, 11), part,
                                        tail_l2(name, series, 11) - part))
    for N in (1, 3, 11):
        OUT.append('  %-8s %-3s N=%-3d rms error %.15f' % (name, series, N, tail_l2(name, series, N)))
emit('l2_square_N11', tail_l2('square', 'sin', 11))
emit('l2_triangle_N11', tail_l2('triangle', 'cos', 11))
emit('l2_sawtooth_N11', tail_l2('sawtooth', 'sin', 11))
# cross-check one of them against a direct integral of (f - S_N)^2
A = preset_closed('square', 'sin', 11)


def resid2(u):
    s = sum(A[n - 1] * math.sin(n * u) for n in range(1, 12))
    return (sq_sin(u) - s) ** 2


br = np.linspace(-math.pi, math.pi, 41)
tot = sum(integrate.quad(resid2, a, b, limit=400, epsabs=1e-13, epsrel=1e-13)[0]
          for a, b in zip(br[:-1], br[1:]))
direct = math.sqrt(tot / (2 * math.pi))
OUT.append('  square N=11 rms error by direct integration: %.15f (tail sum %.15f, diff %.2e)'
           % (direct, tail_l2('square', 'sin', 11), abs(direct - tail_l2('square', 'sin', 11))))
assert abs(direct - tail_l2('square', 'sin', 11)) < 1e-9

# ----------------------------------------------------------------------------
# F.  analysis: projection, direct DFT, radix-2 FFT
# ----------------------------------------------------------------------------
head('F  analysis: the coefficients come back out')
NS = 256                                     # samples over one period


def analyse_direct(y, N, series):
    """A_n = (2/NS) sum_j y_j sin/cos(2 pi n j / NS) -- the direct DFT projection."""
    out = []
    for n in range(1, N + 1):
        s = 0.0
        for j in range(NS):
            u = 2 * math.pi * j / NS
            s += y[j] * (math.sin(n * u) if series == 'sin' else math.cos(n * u))
        out.append(2 * s / NS)
    return out


A = list(rng.uniform(-1.5, 1.5, MAX_HARMONICS))
for series in ('sin', 'cos'):
    y = [sum(A[n - 1] * (math.sin(n * 2 * math.pi * j / NS) if series == 'sin'
                         else math.cos(n * 2 * math.pi * j / NS))
             for n in range(1, MAX_HARMONICS + 1)) for j in range(NS)]
    back = analyse_direct(y, MAX_HARMONICS, series)
    d = max(abs(a - b) for a, b in zip(A, back))
    OUT.append('  %s: round trip max |A - analyse(synthesise(A))| = %.3e' % (series, d))
    assert d < 1e-13
    # numpy's FFT, as the third independent implementation
    Y = np.fft.rfft(np.array(y)) / NS
    if series == 'sin':
        fb = [-2 * float(np.imag(Y[n])) for n in range(1, MAX_HARMONICS + 1)]
    else:
        fb = [2 * float(np.real(Y[n])) for n in range(1, MAX_HARMONICS + 1)]
    d2 = max(abs(a - b) for a, b in zip(A, fb))
    OUT.append('  %s: numpy.fft agrees with the projection to %.3e' % (series, d2))
    assert d2 < 1e-13
emit('analysis_A', A)
emit('analysis_NS', NS)

# ----------------------------------------------------------------------------
# G.  the wave packet
# ----------------------------------------------------------------------------
head('G  the wave packet')
K0, SK = 12 * math.pi, 3 * math.pi
SX = 1 / SK


def Ak(k, k0, sk):
    return math.exp(-(k - k0) ** 2 / (2 * sk * sk)) / (sk * math.sqrt(2 * math.pi))


def F_cont(x, k0, sk, series='cos'):
    """The exact transform: int A(k) cos(kx) dk over the whole line."""
    e = math.exp(-sk * sk * x * x / 2)
    return e * (math.cos(k0 * x) if series == 'cos' else math.sin(k0 * x))


# (i) the transform pair, against quadrature over the whole line
worstT = 0.0
for x in (0.0, 0.037, 0.12, -0.25, 0.4):
    for series in ('cos', 'sin'):
        q = integrate.quad(lambda k: Ak(k, K0, SK) * (math.cos(k * x) if series == 'cos' else math.sin(k * x)),
                           K0 - 12 * SK, K0 + 12 * SK, limit=800, epsabs=1e-15, epsrel=1e-14)[0]
        worstT = max(worstT, abs(q - F_cont(x, K0, SK, series)))
OUT.append('  transform pair vs quad: max |diff| = %.3e' % worstT)
assert worstT < 1e-12
emit('wp_transform_residual', worstT, 'exp(-s^2 x^2/2) cos(k0 x) IS the transform of A(k)')
emit('wp_F0', F_cont(0.0, K0, SK), 'the packet at the origin: 1')
emit('wp_F_0p12', F_cont(0.12, K0, SK))
emit('wp_sigma_x', SX, 'sigma_x = 1/sigma_k exactly')
emit('wp_uncertainty_product', SX * SK, 'sigma_x sigma_k = 1')
emit('wp_envelope_at_sigma_x', math.exp(-0.5), 'the envelope is 1/sqrt(e) at x = sigma_x')
emit('wp_width_indicator', 2 * SX, 'full width at 1/sqrt(e)')

# (ii) Poisson: the two-sided discrete sum IS the periodised continuous packet
def discrete_two_sided(x, k1, k0, sk, series='cos'):
    s, n = 0.0, 0
    while True:
        k = n * k1
        a = Ak(k, k0, sk) * k1
        b = Ak(-k, k0, sk) * k1 if n else 0.0
        if n and a < 1e-300 and b < 1e-300 and k > k0 + 40 * sk:
            break
        if series == 'cos':
            s += a * math.cos(k * x) + b * math.cos(k * x)
        else:
            s += a * math.sin(k * x) - b * math.sin(k * x)
        n += 1
        if n > 400000:
            break
    return s


def periodised(x, k1, k0, sk, series='cos'):
    lam = 2 * math.pi / k1
    s = 0.0
    for mm in range(-60, 61):
        s += F_cont(x - mm * lam, k0, sk, series)
    return s


worstPo = 0.0
for k1 in (math.pi, math.pi / 2, math.pi / 4, 2 * math.pi):
    for x in (0.0, 0.07, 0.31, -0.5):
        for series in ('cos', 'sin'):
            worstPo = max(worstPo, abs(discrete_two_sided(x, k1, K0, SK, series)
                                       - periodised(x, k1, K0, SK, series)))
OUT.append('  Poisson summation (two-sided sum == periodised packet): max |diff| = %.3e' % worstPo)
assert worstPo < 1e-12
emit('wp_poisson_residual', worstPo, 'the discrete packet is the continuous one, repeated')

# (iii) PhET's one-sided truncated sum vs the two-sided one: the Gaussian tail
def phet_sum(x, k1, k0, sk, series='cos'):
    n = int(KMAX / k1) + 1
    s = 0.0
    for j in range(n):
        k = j * k1
        s += Ak(k, k0, sk) * k1 * (math.cos(k * x) if series == 'cos' else math.sin(k * x))
    return s


tail = 0.5 * math.erfc((K0 - 0.0) / (SK * math.sqrt(2))) + 0.5 * math.erfc((KMAX - K0) / (SK * math.sqrt(2)))
worstTr = 0.0
for k1 in (math.pi, math.pi / 2, math.pi / 4):
    for x in (0.0, 0.05, 0.2, -0.33):
        worstTr = max(worstTr, abs(phet_sum(x, k1, K0, SK) - discrete_two_sided(x, k1, K0, SK)))
OUT.append('  one-sided truncation vs two-sided: max |diff| = %.3e  (Gaussian tail bound %.3e)'
           % (worstTr, tail))
assert worstTr < tail
emit('wp_tail_bound', tail, 'erfc at k=0 and at k=24pi, sigma = 3 pi')
emit('wp_truncation_residual', worstTr)
emit('wp_n_components_pi', int(KMAX / math.pi) + 1, "PhET's floor(24pi/k1)+1")
emit('wp_n_components_pi_over_4', int(KMAX / (math.pi / 4)) + 1)

# (iv) the discrete sum is EXACTLY periodic with period lambda1 = 2 pi / k1,
#      because every k_n = n k1 is.  So the copies are what separates it from
#      the continuous packet, and they march out to infinity as k1 -> 0.
per = 0.0
for k1 in (math.pi, math.pi / 2, math.pi / 4):
    lam = 2 * math.pi / k1
    for x in (0.0, 0.13, -0.4):
        per = max(per, abs(phet_sum(x + lam, k1, K0, SK) - phet_sum(x, k1, K0, SK)))
OUT.append('  the truncated discrete sum repeats every lambda1 exactly: max |diff| = %.3e' % per)
assert per < 1e-12
emit('wp_periodicity_residual', per, 'every k_n = n k1 has period lambda1')

emit('wp_discrete_k1_list', [math.pi, math.pi / 2, math.pi / 4, math.pi / 8])
WIN = 3.0                       # a fixed window, wider than lambda1 at the coarsest spacing
errs, inner = [], []
for k1 in (math.pi, math.pi / 2, math.pi / 4, math.pi / 8):
    lam = 2 * math.pi / k1
    xs = np.linspace(-WIN, WIN, 1201)
    e = max(abs(phet_sum(x, k1, K0, SK) - F_cont(x, K0, SK)) for x in xs)
    xi = np.linspace(-min(lam / 2, WIN), min(lam / 2, WIN), 601)
    ei = max(abs(phet_sum(x, k1, K0, SK) - F_cont(x, K0, SK)) for x in xi)
    errs.append(e)
    inner.append(ei)
    OUT.append('  k1 = %.6f (lambda1 = %7.4f m): max |discrete - continuous| on |x|<%.0f = %.3e, '
               'inside one period = %.3e' % (k1, lam, WIN, e, ei))
emit('wp_conv_errs_window3', errs, 'the copies leave the window as k1 falls')
emit('wp_conv_errs_one_period', inner, 'inside one period it is only the Gaussian tail')
assert errs[0] > 0.9 and errs[2] < 1e-4, errs     # the copy is full height, then gone
assert max(inner) < tail, inner

# (v) the amplitudes PhET plots: A(k_n) * k1, and their sum -> 1
for k1 in (math.pi, math.pi / 2, math.pi / 4):
    tot = sum(Ak(j * k1, K0, SK) * k1 for j in range(int(KMAX / k1) + 1))
    OUT.append('  sum of the plotted amplitudes at k1 = %.5f : %.15f  (-> 1)' % (k1, tot))
emit('wp_amp_sum_pi', sum(Ak(j * math.pi, K0, SK) * math.pi for j in range(int(KMAX / math.pi) + 1)))
emit('wp_amp_peak_pi', max(Ak(j * math.pi, K0, SK) * math.pi for j in range(int(KMAX / math.pi) + 1)))
emit('wp_Ak_at_k0', Ak(K0, K0, SK), '1/(sigma sqrt(2 pi))')

# ----------------------------------------------------------------------------
# H.  the wave game
# ----------------------------------------------------------------------------
head('H  the wave game')
alphabet = sorted({round(s * v, 10) for v in np.arange(G_STEP, MAX_AMPLITUDE + 1e-9, G_STEP)
                   for s in (-1, 1)})
emit('game_alphabet_size', len(alphabet), 'multiples of 0.1 in [-1.5, 1.5], zero excluded')
emit('game_alphabet_min', min(alphabet))
emit('game_alphabet_max', max(alphabet))
emit('game_levels_harmonics', [1, 2, 3, 4, 5], "level n uses n non-zero harmonics (5 = '5 or more')")

# ----------------------------------------------------------------------------
head('I  a few sum values for the JS to reproduce exactly')
for name, series, xs in [('square', 'sin', [0.1, 0.25, 0.37]),
                         ('triangle', 'cos', [0.0, 0.13]),
                         ('sawtooth', 'sin', [0.2, -0.45])]:
    A = preset_closed(name, series, MAX_HARMONICS)
    vals = []
    for x in xs:
        u = 2 * math.pi * x / L
        vals.append(sum(A[n - 1] * (math.sin(n * u) if series == 'sin' else math.cos(n * u))
                        for n in range(1, MAX_HARMONICS + 1)))
    emit('sum_%s_%s' % (name, series), vals, 'at x = %s m' % xs)
# space & time: the travelling form sin(2 pi n (x/L - t/T))
A = preset_closed('square', 'sin', MAX_HARMONICS)
tms = 0.7
vals = [sum(A[n - 1] * math.sin(2 * math.pi * n * (x / L - tms / T)) for n in range(1, MAX_HARMONICS + 1))
        for x in (0.1, 0.25)]
emit('sum_square_xt_t0p7', vals, 'space & time at t = 0.7 ms')
# the travelling wave moves at L/T m/ms
emit('wave_speed_m_per_ms', L / T, 'L/T = 0.44 m/ms = 440 m/s')

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'refvals.txt')
io.open(path, 'w', encoding='utf-8').write('\n'.join(OUT) + '\n')
print('\n'.join(OUT))
print('\nwrote %s (%d lines)' % (path, len(OUT)))
