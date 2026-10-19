#!/usr/bin/env python3
"""derive.py -- the Python twin of blackbody-spectrum.html.

Re-derives every closed form the sim implements and prints reference values
to 12-17 significant digits for selfTest() to assert against.  Nothing here is
typed from memory:

  * h, c, k are the exact SI 2019 defining constants, read from scipy.constants
    (CODATA 2022 in scipy 1.18); sigma, b, the radiation constants and the Wien
    frequency constant are re-derived here and compared with scipy's CODATA
    values.
  * Every Planck value is recomputed in 50-digit decimal arithmetic (Python's
    decimal module: exp and ln to arbitrary precision), independent of float64.
  * The band-fraction integral is evaluated three ways: scipy.integrate.quad,
    the exponential series in decimal, and the Bernoulli head series built from
    EXACT rationals (fractions.Fraction), and the three are compared.
  * Colorimetry uses the CIE 1931 2-degree colour-matching functions as the CIE
    publishes them (CIE_xyz_1931_2deg.csv, 1 nm, 360-830 nm, DOI
    10.25039/CIE.DS.xvudnb9b), read verbatim from the downloaded file, and the
    CIE's own Illuminant A table (CIE_std_illum_A_1nm.csv) as an independent
    check of the Planck-to-chromaticity chain.
  * PhET's constants are read from the minified original (blackbody-spectrum
    1.0.26) and labelled "PhET's value"; their deviation from CODATA is printed.

Run:  python3 derive.py > refvals.txt      (then READ refvals.txt IN FULL)
It also writes p2_cie.js (the 5-nm subsample of the CIE table as a JS literal),
so no table value is ever hand-typed into the sim.
"""
import io, os, math
from decimal import Decimal, getcontext
from fractions import Fraction
import numpy as np
import scipy.constants as sc
from scipy import integrate, special, optimize

getcontext().prec = 50
HERE = os.path.dirname(os.path.abspath(__file__))

def P(name, val, fmt='%.17g'):
    print(('%-46s ' + fmt) % (name, val))

# ------------------------------------------------------------------ constants
h, c, k = sc.h, sc.c, sc.k
print('# exact SI defining constants (scipy.constants, CODATA %s)' % getattr(sc, '_codata_version', '2022'))
P('h', h); P('c', c); P('k', k)
C1 = 2 * math.pi * h * c * c                 # first radiation constant 2 pi h c^2, W m^2
C2 = h * c / k                               # second radiation constant hc/k, m K
SIGMA = 2 * math.pi**5 * k**4 / (15 * h**3 * c**2)
P('C1 = 2 pi h c^2 (W m^2)', C1)
P('scipy first radiation constant', sc.physical_constants['first radiation constant'][0])
P('C2 = hc/k (m K)', C2)
P('scipy second radiation constant', sc.physical_constants['second radiation constant'][0])
P('SIGMA = 2 pi^5 k^4/(15 h^3 c^2)', SIGMA)
P('scipy Stefan_Boltzmann', sc.Stefan_Boltzmann)
P('rel diff SIGMA vs scipy', SIGMA / sc.Stefan_Boltzmann - 1, '%.3e')

# Wien roots: x = n (1 - e^-x);  x_n = n + W0(-n e^-n)
X5 = float(5 + special.lambertw(-5 * math.exp(-5)).real)
X3 = float(3 + special.lambertw(-3 * math.exp(-3)).real)
X4 = float(4 + special.lambertw(-4 * math.exp(-4)).real)
# the same roots by Newton in 50-digit decimal (independent route)
def wien_dec(n):
    n = Decimal(n); x = n
    for _ in range(60):
        f = x - n * (1 - (-x).exp()); fp = 1 - n * (-x).exp()
        x = x - f / fp
    return x
X5d = wien_dec(5); X3d = wien_dec(3)
P('X5 (lambertw)', X5); P('X5 (decimal Newton)', float(X5d))
P('X3 (lambertw)', X3); P('X3 (decimal Newton)', float(X3d))
P('X4 (lambertw, photon-count peak)', X4)
B_WIEN = C2 / X5
P('b = C2/X5 (m K)', B_WIEN)
P('scipy Wien wavelength displacement', sc.physical_constants['Wien wavelength displacement law constant'][0])
NU_PER_T = X3 * k / h
P('nu_max/T = X3 k/h (Hz/K)', NU_PER_T)
P('scipy Wien frequency displacement', sc.physical_constants['Wien frequency displacement law constant'][0])
P('X3/X5 = lam_max nu_max / c', X3 / X5)

# PhET's constants (BlackbodyBodyModel / BlackbodyConstants, v1.0.26)
print('\n# PhET\'s values (read from the minified original) and their deviation from CODATA')
PHET_C1_NM = 3.74192e-16        # W m^2 used with lambda in nm and a 1e33 view factor
PHET_C2_NM = 14387700.0         # nm K
PHET_SIGMA = 5.670373e-8
PHET_B_NM = 2897773.0           # nm K
P('PhET c1 / (2 pi h c^2) - 1', PHET_C1_NM / C1 - 1, '%.4e')
P('PhET c2 / (hc/k) - 1', PHET_C2_NM * 1e-9 / C2 - 1, '%.4e')
P('PhET sigma / sigma - 1', PHET_SIGMA / SIGMA - 1, '%.4e')
P('PhET b / b - 1', PHET_B_NM * 1e-9 / B_WIEN - 1, '%.4e')

# ------------------------------------------------------------------ Planck
def M_si(lam_m, T):                      # spectral exitance pi*B_lambda, W m^-2 m^-1
    x = C2 / (lam_m * T)
    if x > 700: return 0.0
    return C1 / lam_m**5 / math.expm1(x)
def bose3(t):                            # t^3/(e^t - 1), overflow-safe
    return t**3 * math.exp(-t) / (-math.expm1(-t)) if t > 0 else 0.0
def M_disp(lam_nm, T):                   # MW m^-2 um^-1 (PhET's axis unit)
    return M_si(lam_nm * 1e-9, T) * 1e-12

Dh, Dc, Dk = Decimal(repr(h)), Decimal(repr(c)), Decimal(repr(k))
DPI = Decimal('3.14159265358979323846264338327950288419716939937510')
def M_dec(lam_nm, T):                    # 50-digit reference, MW m^-2 um^-1
    lam = Decimal(lam_nm) * Decimal('1e-9'); T = Decimal(T)
    x = Dh * Dc / (Dk * lam * T)
    return (2 * DPI * Dh * Dc * Dc / lam**5 / (x.exp() - 1)) * Decimal('1e-12')

print('\n# PLANCK: M_lambda (MW m^-2 um^-1) -- float64 vs 50-digit decimal')
LAMS = [10, 100, 380, 450, 500, 550, 650, 780, 1000, 3000, 10000, 48000, 100000]
TS = [200, 250, 3000, 5800, 9950, 11000]
worst = 0.0
rows = []
for T in TS:
    for L in LAMS:
        d = M_dec(L, T); f = M_disp(L, T)
        dv = float(d)
        if dv > 1e-300:
            worst = max(worst, abs(f / dv - 1))
        rows.append((L, T, dv))
        print('M %6d nm %5d K  %.17g   (float64 %.17g)' % (L, T, dv, f))
P('worst float64/decimal rel diff (non-underflow)', worst, '%.3e')

# ------------------------------------------------------------------ Wien
print('\n# WIEN: peak wavelength (nm) and peak height (MW m^-2 um^-1)')
PRESETS = [('Earth', 250), ('Light Bulb', 3000), ('Sun', 5800), ('Sirius A', 9950), ('min', 200), ('max', 11000)]
for nm, T in PRESETS:
    lm = B_WIEN / T
    print('peak %-10s T=%5d  lam_max %.17g nm   M_peak %.17g   (dec %.17g)' % (nm, T, lm * 1e9, M_si(lm, T) * 1e-12, float(M_dec(Decimal(repr(lm * 1e9)), T))))
# M_peak / T^5 in closed form
KPEAK = 2 * math.pi * k**5 * X5**5 / (h**4 * c**3 * math.expm1(X5))   # W m^-3 K^-5
P('M_peak/T^5 closed form (W m^-3 K^-5)', KPEAK)
P('M_peak/T^5 display (MW m^-2 um^-1 K^-5)', KPEAK * 1e-12)
P('M(lam_max,5800)/5800^5 (display)', M_si(B_WIEN / 5800, 5800) * 1e-12 / 5800**5)
# the peak really is the maximum: brute force at 5800 K
res = optimize.minimize_scalar(lambda L: -M_si(L, 5800), bounds=(3e-7, 8e-7), method='bounded', options={'xatol': 1e-16})
P('argmax M at 5800 K by minimize_scalar (m)', res.x)
P('b/5800 (m)', B_WIEN / 5800)
# frequency peak
for nm, T in [('Sun', 5800)]:
    nu = NU_PER_T * T
    P('nu_max at 5800 K (Hz)', nu); P('c/nu_max at 5800 K (nm)', c / nu * 1e9); P('lam_max at 5800 K (nm)', B_WIEN / T * 1e9)

# universal curve: M/M_peak as a function of y = lam T / b; half maximum roots
def shape(y):   # M(lam)/M(lam_max) with lam = y*lam_max: (1/y^5) (e^X5 - 1)/(e^(X5/y) - 1)
    return (1 / y**5) * math.expm1(X5) / math.expm1(X5 / y)
yl = optimize.brentq(lambda y: shape(y) - 0.5, 0.3, 1.0, xtol=1e-15)
yr = optimize.brentq(lambda y: shape(y) - 0.5, 1.0, 5.0, xtol=1e-15)
P('half max, y_low = lam/lam_max', yl); P('half max, y_high', yr)
P('half max lam T low (um K)', yl * B_WIEN * 1e6); P('half max lam T high (um K)', yr * B_WIEN * 1e6)
P('FWHM in lam T (um K)', (yr - yl) * B_WIEN * 1e6)

# ------------------------------------------------------------------ Stefan-Boltzmann
print('\n# STEFAN-BOLTZMANN: sigma T^4 (W m^-2) vs scipy quad of M over lambda')
for nm, T in PRESETS:
    lm = B_WIEN / T
    f = lambda L: M_si(L, T)
    # split at the peak and at decades so quad sees the structure
    edges = [lm / 64, lm / 8, lm / 2, lm, 2 * lm, 8 * lm, 64 * lm, 1e4 * lm]
    q = 0.0; qe = 0.0
    for a, b2 in zip([0.0] + edges[:-1], edges):
        v, e = integrate.quad(f, a, b2, epsabs=0, epsrel=1.2e-14, limit=400); q += v; qe += e
    v, e = integrate.quad(f, edges[-1], np.inf, epsabs=0, epsrel=1.2e-14, limit=400); q += v; qe += e
    print('I %-10s T=%5d  sigma T^4 %.17g   quad %.17g  rel %.2e' % (nm, T, SIGMA * T**4, q, q / (SIGMA * T**4) - 1))
P('pi^4/15', math.pi**4 / 15)
v, e = integrate.quad(bose3, 0, np.inf, epsabs=0, epsrel=1.2e-14, limit=400)
P('quad int_0^inf t^3/(e^t-1) dt', v)

# ------------------------------------------------------------------ band fractions
print('\n# BAND FRACTIONS: tail(x) = int_x^inf t^3/(e^t-1) dt ; head(x) = int_0^x')
# exact Bernoulli-series coefficients a_k = B_k/k! from power-series division, in rationals
NA = 60
a = [Fraction(1)]
for kk in range(1, NA + 1):
    s = Fraction(0)
    for j in range(1, kk + 1):
        s += a[kk - j] / math.factorial(j + 1)
    a.append(-s)
print('a_k = B_k/k! (exact rationals, first ten):', ', '.join(str(a[i]) for i in range(11)))
# the same recurrence in float64, as the JS builds it
af = [1.0]
for kk in range(1, NA + 1):
    s = 0.0
    for j in range(1, kk + 1):
        s += af[kk - j] / math.factorial(j + 1)
    af.append(-s)
worst_a = max(abs(af[i] - float(a[i])) / max(abs(float(a[i])), 1e-300) for i in range(NA + 1) if a[i] != 0)
worst_odd = max(abs(af[i]) for i in range(3, NA + 1, 2))
P('float recurrence vs exact a_k (worst rel, even k)', worst_a, '%.3e')
P('float recurrence odd k>=3 (worst abs; exact 0)', worst_odd, '%.3e')
for i in (2, 4, 6, 8, 10, 20, 40):
    print('a_%-2d = %s = %.17g' % (i, a[i], float(a[i])))

def head_exact(x, K=NA):                   # sum a_k x^(k+3)/(k+3), exact rationals -> float
    X = Fraction(x)
    s = sum(a[kk] * X**(kk + 3) / (kk + 3) for kk in range(K + 1))
    return float(s)
def tail_dec(x, N=None):                   # sum_n e^-nx (x^3/n + 3x^2/n^2 + 6x/n^3 + 6/n^4), decimal
    X = Decimal(repr(x)); s = Decimal(0)
    if N is None: N = int(110 / x) + 20        # e^-(N x) < 1e-47: the term count follows x
    for n in range(1, N + 1):
        e = (-n * X).exp()
        term = e * (X**3 / n + 3 * X**2 / n**2 + 6 * X / n**3 + Decimal(6) / n**4)
        s += term
        if term < Decimal('1e-45') * s: break
    return s
PI4_15 = Decimal(DPI)**4 / 15
XS = [0.001, 0.01, 0.1, 0.5, 1.0, 1.5, 1.999, 2.0, 2.001, 3.0, 5.0, 10.0, 20.0, 50.0, 100.0, 300.0, 700.0]
for x in XS:
    td = tail_dec(x)
    hd = PI4_15 - td
    q1, _ = integrate.quad(bose3, 0, x, epsabs=0, epsrel=1.2e-14, limit=400) if x < 50 else (float(hd), 0)
    hx = head_exact(x) if x <= 3.0 else float('nan')
    print('F x=%-7g tail %.17g  head %.17g  frac_below %.17g  | head(rational series) %.17g  quad head %.17g'
          % (x, float(td), float(hd), float(td / PI4_15), hx, q1))

# band edges (PhET's values): X-ray < 10 nm < UV < 380 nm < visible < 780 nm < IR < 100 um < beyond
EDGES_NM = [10, 380, 780, 100000]
def frac_below_dec(lam_nm, T):          # 50-digit Decimal: subtract BEFORE converting to float
    x = C2 / (lam_nm * 1e-9 * T)
    return tail_dec(x) / PI4_15 if x < 745 else Decimal(0)
def frac_below(lam_nm, T):
    return float(frac_below_dec(lam_nm, T))
print('\n# band budget: fraction of sigma T^4 per band (X-ray, UV, visible, IR, beyond 100 um)')
for nm, T in PRESETS:
    Fs = [frac_below_dec(L, T) for L in EDGES_NM]
    bands = [Fs[0], Fs[1] - Fs[0], Fs[2] - Fs[1], Fs[3] - Fs[2], 1 - Fs[3]]
    print('B %-10s T=%5d  ' % (nm, T) + '  '.join('%.17g' % float(v) for v in bands))
    # the thin long-wavelength band, independently: the exact-rational head series over pi^4/15
    xf = C2 / (1e5 * 1e-9 * T)
    print('B %-10s T=%5d  beyond 100 um by the rational head series: %.17g' % (nm, T, head_exact(xf) / float(PI4_15)))
# the visible band by direct quad (cross-check)
for T in (3000, 5800):
    v, e = integrate.quad(lambda L: M_si(L, T), 380e-9, 780e-9, epsabs=0, epsrel=1.2e-14)
    P('visible fraction by quad at %d K' % T, v / (SIGMA * T**4))
print('\n# window: fraction of sigma T^4 inside [0, lam_axis] at the zoom levels')
ZX = [750, 1500, 3000, 6000, 12000, 24000, 48000]
for T in (250, 3000, 5800, 9950):
    print('W T=%5d  ' % T + '  '.join('%d:%.15g' % (z, frac_below(z, T)) for z in ZX))

# ------------------------------------------------------------------ colorimetry
print('\n# COLORIMETRY: CIE 1931 2-degree CMFs, as published (1 nm, 360-830 nm)')
cmf = []
for line in io.open(os.path.join(HERE, 'CIE_xyz_1931_2deg.csv'), encoding='utf-8'):
    p = line.strip().split(',')
    if len(p) == 4: cmf.append((int(p[0]), p[1], p[2], p[3]))
assert cmf[0][0] == 360 and cmf[-1][0] == 830 and len(cmf) == 471
lam1 = np.array([r[0] for r in cmf], float)
X1 = np.array([float(r[1]) for r in cmf]); Y1 = np.array([float(r[2]) for r in cmf]); Z1 = np.array([float(r[3]) for r in cmf])
sub = [r for r in cmf if r[0] % 5 == 0]
assert len(sub) == 95
# write the JS literal: verbatim strings, never retyped
with io.open(os.path.join(HERE, 'p2_cie.js'), 'w', encoding='utf-8') as f:
    f.write('/* CIE 1931 2-degree colour-matching functions x-bar, y-bar, z-bar, every 5 nm from 360 to 830 nm:\n'
            '   every fifth row of CIE_xyz_1931_2deg.csv exactly as the CIE publishes it (DOI 10.25039/CIE.DS.xvudnb9b,\n'
            '   ISO/CIE 11664-1:2019).  Written by build/blackbody-spectrum/derive.py from the downloaded file;\n'
            '   no value was typed by hand. */\n')
    f.write('const CIE1931=[\n')
    for i in range(0, 95, 3):
        f.write('  ' + ','.join('[%d,%s,%s,%s]' % r for r in sub[i:i + 3]) + ',\n')
    f.write('];\n')
lam5 = np.array([r[0] for r in sub], float)
X5c = np.array([float(r[1]) for r in sub]); Y5c = np.array([float(r[2]) for r in sub]); Z5c = np.array([float(r[3]) for r in sub])
P('sum xbar (5 nm) * 5', X5c.sum() * 5); P('sum ybar (5 nm) * 5', Y5c.sum() * 5); P('sum zbar (5 nm) * 5', Z5c.sum() * 5)
P('sum ybar (1 nm)', Y1.sum())

SRGB = np.array([[3.2406, -1.5372, -0.4986], [-0.9689, 1.8758, 0.0415], [0.0557, -0.2040, 1.0570]])
P('sRGB matrix x D65 (0.95047,1,1.08883): r', (SRGB @ np.array([0.95047, 1.0, 1.08883]))[0])
def srgb_gamma(u):
    u = min(max(u, 0.0), 1.0)
    return 12.92 * u if u <= 0.0031308 else 1.055 * u**(1 / 2.4) - 0.055
def xyz_of_T(T, step=5):
    lam = lam5 if step == 5 else lam1
    XX, YY, ZZ = (X5c, Y5c, Z5c) if step == 5 else (X1, Y1, Z1)
    m = np.array([M_si(L * 1e-9, T) for L in lam])
    d = step * 1e-9
    return (m * XX).sum() * d, (m * YY).sum() * d, (m * ZZ).sum() * d
def rgb_bytes(XYZ):
    X, Y, Z = XYZ
    v = SRGB @ np.array([X / Y, 1.0, Z / Y])
    v = np.maximum(v, 0.0); v = v / v.max()
    return [int(round(255 * srgb_gamma(u))) for u in v], v
print('# chromaticity of a blackbody (5-nm sums, as the JS does) and the 1-nm sums for comparison')
TC = [800, 1000, 1500, 2000, 2500, 3000, 4000, 5000, 5800, 6500, 8000, 9950, 11000]
for T in TC:
    X, Y, Z = xyz_of_T(T); s = X + Y + Z
    X_, Y_, Z_ = xyz_of_T(T, 1); s_ = X_ + Y_ + Z_
    byt, lin = rgb_bytes((X, Y, Z))
    print('C T=%5d  x %.15g  y %.15g  | 1nm x %.10g y %.10g  dx %.1e dy %.1e | Y %.15g | rgb %s  lin %.12g %.12g %.12g'
          % (T, X / s, Y / s, X_ / s_, Y_ / s_, X / s - X_ / s_, Y / s - Y_ / s_, Y, byt, lin[0], lin[1], lin[2]))
# luminous efficacy K_cd * int M ybar / sigma T^4
KCD = 683.0
print('# luminous efficacy 683 * int M ybar dlam / (sigma T^4)  (lm/W)')
for nm, T in PRESETS + [('6500', 6500)]:
    X, Y, Z = xyz_of_T(T)
    print('E %-10s T=%5d  %.15g   (1nm %.10g)' % (nm, T, KCD * Y / (SIGMA * T**4), KCD * xyz_of_T(T, 1)[1] / (SIGMA * T**4)))
res = optimize.minimize_scalar(lambda T: -KCD * xyz_of_T(T)[1] / (SIGMA * T**4), bounds=(4000, 9000), method='bounded', options={'xatol': 1e-6})
print('# log10 of the luminance ratio Y(T)/Y(6500) (5 nm), for the log-compressed glow')
Y65 = xyz_of_T(6500)[1]
for T in (800, 1000, 2000, 3000, 5800, 11000):
    print('LY T=%5d  %.15g' % (T, math.log10(xyz_of_T(T)[1] / Y65)))
P('max efficacy (5 nm) at T (K)', res.x); P('max efficacy (lm/W)', -res.fun)

# Illuminant A: fit the Planck temperature to the CIE's own table, then compare chromaticities
print('\n# ILLUMINANT A (CIE_std_illum_A_1nm.csv) against this file\'s Planck function')
A = []
for line in io.open(os.path.join(HERE, 'CIE_std_illum_A_1nm.csv'), encoding='utf-8'):
    p = line.strip().split(',')
    if len(p) == 2: A.append((int(p[0]), float(p[1])))
lamA = np.array([r[0] for r in A], float); SA = np.array([r[1] for r in A])
assert abs(SA[lamA == 560][0] - 100) < 1e-12
def relspd(T):
    return np.array([M_si(L * 1e-9, T) for L in lamA]) / M_si(560e-9, T) * 100
Tfit = optimize.minimize_scalar(lambda T: float(np.sum((relspd(T) / SA - 1)**2)), bounds=(2800, 2900), method='bounded', options={'xatol': 1e-9}).x
P('Planck T that reproduces Illuminant A (K)', Tfit)
P('same, predicted 2848 * C2 / 1.435e-2', 2848 * C2 / 1.435e-2)
P('worst rel residual of the fit over 300-830 nm', float(np.max(np.abs(relspd(Tfit) / SA - 1))), '%.3e')
# chromaticity of the TABLE (1 nm, 360-830) vs Planck at Tfit
m = (lamA >= 360) & (lamA <= 830)
XA = (SA[m] * X1).sum(); YA = (SA[m] * Y1).sum(); ZA = (SA[m] * Z1).sum()
P('Illuminant A table: x (1 nm)', XA / (XA + YA + ZA)); P('Illuminant A table: y (1 nm)', YA / (XA + YA + ZA))
X_, Y_, Z_ = xyz_of_T(Tfit, 1); P('Planck at Tfit: x (1 nm)', X_ / (X_ + Y_ + Z_)); P('Planck at Tfit: y (1 nm)', Y_ / (X_ + Y_ + Z_))
X_, Y_, Z_ = xyz_of_T(2848 * C2 / 1.435e-2); P('Planck at 2848*C2/1.435e-2: x (5 nm, as JS)', X_ / (X_ + Y_ + Z_)); P('  y (5 nm, as JS)', Y_ / (X_ + Y_ + Z_))

# the Wyman-Sloan-Shirley fit the house sims use, for the record
def wss(nm):
    g = lambda x, mu, s1, s2: math.exp(-0.5 * ((x - mu) / (s1 if x < mu else s2))**2)
    X = 1.056 * g(nm, 599.8, 37.9, 31.0) + 0.362 * g(nm, 442.0, 16.0, 26.7) - 0.065 * g(nm, 501.1, 20.4, 26.2)
    Y = 0.821 * g(nm, 568.8, 46.9, 40.5) + 0.286 * g(nm, 530.9, 16.3, 31.1)
    Z = 1.217 * g(nm, 437.0, 11.8, 36.0) + 0.681 * g(nm, 459.0, 26.0, 13.8)
    return X, Y, Z
print('\n# the house Wyman-Sloan-Shirley CMF fit vs the CIE table (finding, not used by the sim)')
for L in (700, 750, 780):
    xw, yw, zw = wss(L); i = int(np.where(lam1 == L)[0][0])
    print('CMF %d nm: fit xbar/ybar %.4g   table xbar/ybar %.4g' % (L, xw / yw, X1[i] / Y1[i]))
for T in (800, 1000, 1500, 2000, 3000, 5800):
    mm = np.array([M_si(L * 1e-9, T) for L in lam1])
    W = np.array([wss(L) for L in lam1])
    Xw, Yw, Zw = (mm * W[:, 0]).sum(), (mm * W[:, 1]).sum(), (mm * W[:, 2]).sum()
    X_, Y_, Z_ = xyz_of_T(T, 1)
    print('WSS T=%5d  fit x %.4f y %.4f   table x %.4f y %.4f   dx %+.4f dy %+.4f'
          % (T, Xw / (Xw + Yw + Zw), Yw / (Xw + Yw + Zw), X_ / (X_ + Y_ + Z_), Y_ / (X_ + Y_ + Z_),
             Xw / (Xw + Yw + Zw) - X_ / (X_ + Y_ + Z_), Yw / (Xw + Yw + Zw) - Y_ / (X_ + Y_ + Z_)))

# spectral colours (monochromatic) for the rainbow band: linear sRGB, desaturated
print('\n# monochromatic colours (5-nm table rows): linear sRGB desaturated toward white, max-normalised')
for L in (450, 460, 550, 580, 640, 700):
    i = int(np.where(lam5 == L)[0][0])
    v = SRGB @ np.array([X5c[i], Y5c[i], Z5c[i]])
    lo = v.min()
    if lo < 0: v = v - lo
    v = v / v.max()
    print('S %d nm  lin %.12g %.12g %.12g' % (L, v[0], v[1], v[2]))

# ------------------------------------------------------------------ PhET's photometer
print('\n# PHET PHOTOMETER (PhET\'s model, CODATA constants): R,G,B = floor(255 min(1,0.02 sqrt(T-798)) M(650|550|450)/max)')
def renorm(T): return 0.02 * math.sqrt(max(T, 798) - 798)
for T in (200, 798, 800, 1000, 2000, 3000, 3298, 4000, 5800, 9950, 11000):
    mv = [M_disp(L, T) for L in (650, 550, 450)]
    mx = max(mv); a_ = min(renorm(T), 1)
    ch = [math.floor(255 * a_ * v / mx) for v in mv]
    raw = [255 * a_ * v / mx for v in mv]
    print('PH T=%5d  renorm %.15g  RGB %s  raw %.10g %.10g %.10g  halo r %.12g alpha %.12g'
          % (T, renorm(T), ch, raw[0], raw[1], raw[2], 5 + 47.5 * renorm(T), 0.3 * renorm(T)))

# ------------------------------------------------------------------ classical limits
print('\n# LIMITS: RJ/Planck = (e^x - 1)/x, Wien/Planck = 1 - e^-x, x = hc/(lam k T)')
for x in (1e-3, 1e-2, 0.1, 1.0, X5, 10.0, 30.0):
    print('L x=%-10.6g RJ/P %.17g  W/P %.17g' % (x, math.expm1(x) / x, -math.expm1(-x)))
x1 = optimize.brentq(lambda x: math.expm1(x) / x - 1.01, 1e-6, 1, xtol=1e-16)
P('RJ within 1% for x below', x1); P('Wien within 1% for x above (ln 100)', math.log(100))
P('Wien/Planck at the peak x5', -math.expm1(-X5))
P('RJ/Planck at the peak x5', math.expm1(X5) / X5)
for T in (5800,):
    P('lam where RJ is 1% off at 5800 K (um)', C2 / (x1 * T) * 1e6)
    P('lam where Wien is 1% off at 5800 K (um)', C2 / (math.log(100) * T) * 1e6)

# zoom ladders (PhET's values: x 750..48000 nm in factors of 2, y 1.024e-5..2500 in factors of 5)
print('\n# zoom ladders')
print('ZX', [750 * 2**i for i in range(7)])
print('ZY', ['%.17g' % (100 * 5.0**i) for i in range(-10, 3)])
