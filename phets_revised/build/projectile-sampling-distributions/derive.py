#!/usr/bin/env python3
"""derive.py — the Python twin of projectile-sampling-distributions.html.

The sim runs the same engine as projectile-data-lab.html, so the trajectory,
the mechanism and the exact law are re-derived the same way (and checked here
against the same independent routes).  What is NEW is everything the Sampling
screen needs and the data lab does not:

 1. PhET's PSD-specific constants, read out of
    docs/phets/projectile-sampling-distributions_en.html: its bin widths are
    [0.5, 1, 2, 5] with 0.5 the default (the data lab adds a 10 and defaults
    to 1), its histogram has no total-bins strategy at all, its zoom ladder
    runs to 250 samples rather than 500 projectiles, and its launcher
    mechanisms carry a speed-mean range floor of 20 m/s rather than 15.
 2. Reference SAMPLING runs at every one of PhET's four sample sizes, drawn
    from the same bit-exact mulberry32 + Box-Muller stream the page uses, with
    numpy's mean, standard deviation (ddof 1 and 0), median and the histogram
    counts of the sample MEANS under PhET's floor(x/w)*w binning.
 3. The exact law of one launch for all six mystery launchers at PhET's fixed
    30 deg orientation (the Sampling screen has no orientation control), by a
    96 x 96 Gauss-Legendre product rule over the truncated normals, checked
    against scipy's adaptive quadrature and a Monte Carlo of the actual
    re-draw mechanism.
 4. The central limit theorem at those four sizes: sigma/sqrt(n) exactly, the
    skewness and excess kurtosis of the sample mean, and the sampling spread
    of a MEASURED standard error, which is the tolerance the page asserts
    with.
"""
import io
import math
import os

import numpy as np
from scipy import integrate, stats

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
    s = '\n==== ' + t + ' ' + '=' * max(0, 72 - len(t))
    print(s)
    OUT_LINES.append(s)


# ===========================================================================
head('1. PhET constants (projectile-sampling-distributions_en.html)')
G = 9.81
FIELD = 100.0
ANG_SD = (0.2, 5.0)
SAMPLE_SIZES = [2, 5, 15, 40]
BIN_WIDTHS = [0.5, 1.0, 2.0, 5.0]          # PSD: no 10, and 0.5 is the default
ZOOM_MAX = [250, 200, 150, 100, 75, 50, 25]
MECH = {'spring': (23.0, 0.5), 'pressure': (24.0, 0.2), 'explosion': (25.0, 1.2)}
_c = 0.5 * (ANG_SD[0] + ANG_SD[1])
_q = ANG_SD[0] + (ANG_SD[1] - ANG_SD[0]) / 4
LAUNCHERS = [('spring', _c), ('pressure', ANG_SD[1]), ('explosion', ANG_SD[0]),
             ('spring', _q), ('pressure', ANG_SD[0]), ('explosion', ANG_SD[1])]
MEAN_ANGLE = 30.0                          # the Sampling screen fixes angle30
MAX_SAMPLES = 200
out('g (m/s^2)', G, 'G')
out('the field (m)', FIELD, 'FIELD')
out('the mean launch angle, fixed (deg)', MEAN_ANGLE, 'MEAN_ANGLE')
out('bin widths (PSD)', str(BIN_WIDTHS))
out('default bin width (PSD 0.5; the data lab 1)', 0.5, 'BINW_DEFAULT')
out('histogram zoom ladder, max samples per bin', str(ZOOM_MAX))
out('sample sizes', str(SAMPLE_SIZES))
out('at most this many samples a field', MAX_SAMPLES, 'MAX_SAMPLES')
out('MAX_PROJECTILES_VSM_FIELD_DEFAULT', 500, 'MAX_PROJ', '%d')
out('SamplingField.totalSampleTime at n = 2, 5, 15, 40 (s)', '0.75, 2, 5, 9')
REFS['SAMPLE_TIME'] = {'2': 0.75, '5': 2.0, '15': 5.0, '40': 9.0}
REFS['BINW'] = BIN_WIDTHS
REFS['ZOOM_MAX'] = ZOOM_MAX
REFS['SAMPLE_SIZES'] = SAMPLE_SIZES
REFS['MECH'] = {k: list(v) for k, v in MECH.items()}
REFS['LAUNCH_SD'] = [s for _, s in LAUNCHERS]
REFS['LAUNCH_MECH'] = [m for m, _ in LAUNCHERS]

# ===========================================================================
head('2. the engine, re-derived (the same closed forms the data lab uses)')


def hrange(v, th_deg, h=0.0):
    th = math.radians(th_deg)
    s = math.sin(th)
    return v * math.cos(th) / G * (v * s + math.sqrt(v * v * s * s + 2 * G * h))


def flight_time(v, th_deg, h=0.0):
    s = math.sin(math.radians(th_deg))
    return v * s / G + math.sqrt((v * s / G) ** 2 + 2 * h / G)


worst = max(abs(hrange(23.0, th) / (23.0 ** 2 * math.sin(2 * math.radians(th)) / G) - 1)
            for th in (5.0, 15.0, 30.0, 45.0, 60.0, 75.0, 85.0))
out('h = 0: the range against v^2 sin2theta/g, worst rel diff', worst)
assert worst < 1e-15
for v, th in [(23.0, 30.0), (24.0, 30.0), (25.0, 30.0)]:
    out('range and flight time at v = %g, 30 deg' % v, '%.17g  %.17g' % (hrange(v, th), flight_time(v, th)))
REFS['rangeCases'] = [[v, MEAN_ANGLE, 0.0, hrange(v, MEAN_ANGLE), flight_time(v, MEAN_ANGLE)]
                      for v in (23.0, 24.0, 25.0)]


def mulberry32(seed):
    st = [seed & 0xFFFFFFFF]

    def imul(x, y):
        return ((x & 0xFFFFFFFF) * (y & 0xFFFFFFFF)) & 0xFFFFFFFF

    def nxt():
        a = (st[0] + 0x6D2B79F5) & 0xFFFFFFFF
        st[0] = a
        t = imul(a ^ (a >> 15), a | 1)
        t = ((t + imul(t ^ (t >> 7), t | 61)) & 0xFFFFFFFF) ^ t
        return ((t ^ (t >> 14)) & 0xFFFFFFFF) / 4294967296.0
    return nxt


def gauss_of(nxt):
    u1 = 1.0 - nxt()
    u2 = nxt()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)


rng = mulberry32(20260923)
REFS['rngStream'] = [rng() for _ in range(6)]
for k, v in enumerate(REFS['rngStream']):
    out('mulberry32(20260923) draw %d' % k, v)
rng = mulberry32(20260923)
REFS['gaussStream'] = [gauss_of(rng) for _ in range(6)]
for k, v in enumerate(REFS['gaussStream']):
    out('Box-Muller from the same seed, value %d' % k, v)

# ===========================================================================
head('3. the exact law of one launch, all six launchers at 30 deg')
NGL = 96
GL_X, GL_W = np.polynomial.legendre.leggauss(NGL)
ZCAP = 12.0
REFS['glX'] = [float(x) for x in GL_X]
REFS['glW'] = [float(x) for x in GL_W]
REFS['NGL'] = NGL
REFS['ZCAP'] = ZCAP
out('Gauss-Legendre nodes', NGL)
out('   sum of the weights (exact 2)', float(GL_W.sum()))


def phi(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def zrule(a, b):
    z = 0.5 * (b - a) * GL_X + 0.5 * (a + b)
    return z, 0.5 * (b - a) * GL_W * phi(z)


def zrange(mu, sd, lo, hi):
    a = -ZCAP if lo is None else max(-ZCAP, (lo - mu) / sd)
    b = ZCAP if hi is None else min(ZCAP, (hi - mu) / sd)
    return a, b


def central(mu, sv, m, w):
    """TWO passes: the mean, then the central moments about it — mu3 cancels
    five digits or more out of the raw moments, and the two languages round
    that cancellation differently."""
    zv, wv = zrule(*zrange(mu, sv, 0.0, None))
    zt, wt = zrule(*zrange(m, w, 0.0, 90.0))
    V = mu + sv * zv
    thr = np.radians(m + w * zt)
    s, c = np.sin(thr), np.cos(thr)
    R = V[:, None] * c[None, :] / G * (V[:, None] * s[None, :]
                                       + np.sqrt(V[:, None] ** 2 * s[None, :] ** 2))
    P = np.outer(wv, wt)
    P = P / P.sum()
    g1 = float((P * R).sum())
    D = R - g1
    return dict(mean=g1, var=float((P * D ** 2).sum()), sd=math.sqrt(float((P * D ** 2).sum())),
                mu3=float((P * D ** 3).sum()), mu4=float((P * D ** 4).sum()),
                m2=float((P * R ** 2).sum()))


def moments_scipy(mu, sv, m, w):
    vlo = max(0.0, mu - ZCAP * sv)
    den = (stats.norm.cdf(min(ZCAP, (90 - m) / w)) - stats.norm.cdf(max(-ZCAP, (0 - m) / w))) \
        * (stats.norm.cdf(ZCAP) - stats.norm.cdf(max(-ZCAP, -mu / sv)))

    def f(th):
        def g(v):
            return hrange(v, th) * stats.norm.pdf(v, mu, sv)
        return integrate.quad(g, vlo, mu + ZCAP * sv, epsabs=1e-14, epsrel=1e-14,
                              limit=300)[0] * stats.norm.pdf(th, m, w)
    return integrate.quad(f, 0.0, 90.0, epsabs=1e-13, epsrel=1e-13, limit=300)[0] / den


def mc_sample(mu, sv, m, w, n=6000000, seed=606):
    rs = np.random.default_rng(seed)
    v = rs.normal(mu, sv, n)
    bad = v <= 0
    while bad.any():
        v[bad] = rs.normal(mu, sv, int(bad.sum()))
        bad = v <= 0
    th = rs.normal(m, w, n)
    bad = (th <= 0) | (th >= 90)
    while bad.any():
        th[bad] = rs.normal(m, w, int(bad.sum()))
        bad = (th <= 0) | (th >= 90)
    thr = np.radians(th)
    s, c = np.sin(thr), np.cos(thr)
    return v * c / G * (v * s + np.sqrt(v * v * s * s))


EX = []
for i, (mech, sd) in enumerate(LAUNCHERS):
    mu, sv = MECH[mech]
    E = central(mu, sv, MEAN_ANGLE, sd)
    EX.append(E)
    out('launcher %d (%s, angle sd %g deg)' % (i + 1, mech, sd), '')
    out('   exact mean (m)', E['mean'])
    out('   exact standard deviation (m)', E['sd'])
    out('   skewness, excess kurtosis', '%.17g  %.17g' % (E['mu3'] / E['sd'] ** 3, E['mu4'] / E['sd'] ** 4 - 3))
    q = moments_scipy(mu, sv, MEAN_ANGLE, sd)
    out('   scipy adaptive quadrature, rel diff', abs(q / E['mean'] - 1))
    assert abs(q / E['mean'] - 1) < 1e-12
    R = mc_sample(mu, sv, MEAN_ANGLE, sd)
    se = R.std(ddof=1) / math.sqrt(len(R))
    out('   Monte Carlo of the re-draw mechanism, 6e6: (MC - exact)/se', (R.mean() - E['mean']) / se)
    assert abs((R.mean() - E['mean']) / se) < 4.0
REFS['launcherStats'] = [[E['mean'], E['sd'], E['mu3'], E['mu4']] for E in EX]

# ===========================================================================
head('3b. the engine still carries the general case, so pin it there too')
# The Sampling screen fixes 30 deg, where the (0, 90) re-draw window sits six
# standard deviations out and nothing can see it.  The ENGINE is the general
# one, and at 60 deg with a 5 deg spread the window is only four sigma out --
# which is where a test of it actually bites.


def closed(mu, sv, m_deg, w_deg):
    """the UNtruncated closed form: R = v^2 sin2th/g, and both factors have
    exact Gaussian moments."""
    m, w = math.radians(m_deg), math.radians(w_deg)

    def C(a):
        return math.cos(a * m) * math.exp(-0.5 * a * a * w * w)

    def S(a):
        return math.sin(a * m) * math.exp(-0.5 * a * a * w * w)
    v2 = mu * mu + sv * sv
    v4 = mu ** 4 + 6 * mu * mu * sv * sv + 3 * sv ** 4
    return [v2 * S(2) / G, v4 * 0.5 * (1 - C(4)) / G ** 2]


GEN = []
for (mu, sv, m, w) in [(24.0, 0.2, 60.0, 5.0), (23.0, 0.5, 45.0, 2.6), (25.0, 1.2, 75.0, 5.0)]:
    E = central(mu, sv, m, w)
    cf = closed(mu, sv, m, w)
    out('general case v=%g+-%g, th=%g+-%g: exact mean, sd (m)' % (mu, sv, m, w),
        '%.17g  %.17g' % (E['mean'], E['sd']))
    out('   the UNtruncated closed form mean, and the gap (m)',
        '%.17g  %+.3e' % (cf[0], cf[0] - E['mean']))
    out('   its second moment, and the gap',
        '%.17g  %+.3e' % (cf[1], cf[1] - E['m2']))
    out('   P(angle > 90) at this setting', stats.norm.sf(90.0, m, w))
    GEN.append([mu, sv, m, w, E['mean'], E['sd'], cf[0], cf[1]])
REFS['generalCases'] = GEN

head('3c. the exact density at each launcher mean, and the standard error')
NGL_ = NGL
NPANEL = 8   # panels for the density's theta integral (see pdf_R)


def dR_dv(v, th_deg):
    th = math.radians(th_deg)
    s, c = math.sin(th), math.cos(th)
    return c / G * (2 * v * s + (2 * v * v * s * s) / (v * s))


def pdf_R(r, mu, sv, m, w, panels=NPANEL):
    """The density of the landing distance at r.

    Unlike the moments this is a one-dimensional integral over theta at FIXED
    r, and its integrand is a spike: only the angles whose v*(r, theta) lands
    within a few sd of the mean speed contribute.  Launcher 2 (a 0.2 m/s speed
    spread beside a 5 deg angle spread) rings a single 96-node rule by 29 %,
    so the interval is split into `panels` equal panels each carrying that
    rule.  The page does exactly the same, and its selfTest asserts the
    convergence rather than assuming it.
    """
    a, b = zrange(m, w, 0.0, 90.0)
    zv, wv = zrule(*zrange(mu, sv, 0.0, None))
    tot = 0.0
    tw = 0.0
    for k in range(panels):
        aa, bb = a + (b - a) * k / panels, a + (b - a) * (k + 1) / panels
        zt, wt = zrule(aa, bb)
        tw += wt.sum()
        for j in range(NGL_):
            th = m + w * zt[j]
            if not (0 < th < 90):
                continue
            vs = math.sqrt(r * G / math.sin(2 * math.radians(th)))
            tot += wt[j] * stats.norm.pdf(vs, mu, sv) / dR_dv(vs, th)
    return tot / (tw * wv.sum())


REFS['pdfAtMean'] = []
for i, (mech, sd) in enumerate(LAUNCHERS):
    mu, sv = MECH[mech]
    f = pdf_R(EX[i]['mean'], mu, sv, MEAN_ANGLE, sd)
    out('launcher %d: the exact density at its own mean (1/m)' % (i + 1), f)
    REFS['pdfAtMean'].append(float(f))

# ===========================================================================
head('4. reference sampling runs at every sample size, against numpy')


def sample_means(seed, mech, sd_ang, size, count):
    nxt = mulberry32(seed)
    mu, sv = MECH[mech]
    means = []
    for _ in range(count):
        xs = []
        for _ in range(size):
            a = MEAN_ANGLE + gauss_of(nxt) * sd_ang
            k = 0
            while k < 100 and (a <= 0 or a >= 90):
                a = MEAN_ANGLE + gauss_of(nxt) * sd_ang
                k += 1
            v = mu + gauss_of(nxt) * sv
            while v <= 0:
                v = mu + gauss_of(nxt) * sv
            xs.append(hrange(v, a))
        means.append(sum(xs) / size)
    return np.array(means)


SEED = 20260923
REFS['sampSeed'] = SEED
REFS['sampCount'] = 200
REFS['sampRuns'] = []
E1 = EX[0]
for size in SAMPLE_SIZES:
    M = sample_means(SEED + size, 'spring', _c, size, 200)
    out('n = %-3d  first three sample means (m)' % size,
        '%.17g  %.17g  %.17g' % (M[0], M[1], M[2]))
    out('   numpy mean of the 200 (m)', float(M.mean()))
    out('   numpy sd, ddof = 1 (m)', float(M.std(ddof=1)))
    out('   numpy sd, ddof = 0 (m)', float(M.std(ddof=0)))
    out('   numpy median (m)', float(np.median(M)))
    out('   numpy standard error, sd(ddof=1)/sqrt(200) (m)', float(M.std(ddof=1)) / math.sqrt(200))
    out('   sigma/sqrt(n) from the exact law (m)', E1['sd'] / math.sqrt(size))
    tol = (E1['sd'] / math.sqrt(size)) * math.sqrt((((E1['mu4'] / E1['sd'] ** 4 - 3) / size) + 2) / (4 * 200))
    out('   (measured SE - sigma/sqrt n) in units of its own sd',
        (float(M.std(ddof=1)) - E1['sd'] / math.sqrt(size)) / tol)
    keys = np.floor(M / 0.5).astype(int)
    lo = int(keys.min())
    cnt = [int((keys == k).sum()) for k in range(lo, int(keys.max()) + 1)]
    nc, _ = np.histogram(M, bins=np.arange(lo, int(keys.max()) + 2) * 0.5)
    assert list(nc) == cnt
    out('   bin width 0.5: first bin index, counts', '%d  %s' % (lo, cnt))
    REFS['sampRuns'].append({'n': size, 'first3': [float(x) for x in M[:3]],
                             'mean': float(M.mean()), 'sd1': float(M.std(ddof=1)),
                             'sd0': float(M.std(ddof=0)), 'median': float(np.median(M)),
                             'se': float(M.std(ddof=1)) / math.sqrt(200),
                             'binLo': lo, 'bins': cnt})
out('numpy.histogram agrees with floor(x/w)*w at every sample size', 'yes')

# ===========================================================================
head('5. the central limit theorem at PhET sample sizes')
REFS['clSigma'] = E1['sd']
REFS['clMean'] = E1['mean']
REFS['clSkew'] = E1['mu3'] / E1['sd'] ** 3
REFS['clKurt'] = E1['mu4'] / E1['sd'] ** 4 - 3
REFS['clSe'] = [E1['sd'] / math.sqrt(n) for n in SAMPLE_SIZES]
for n in SAMPLE_SIZES:
    out('n = %-3d sigma/sqrt(n) (m)' % n, E1['sd'] / math.sqrt(n))
out('the skewness of one launch', REFS['clSkew'])
out('the excess kurtosis of one launch', REFS['clKurt'])
for n in SAMPLE_SIZES:
    out('n = %-3d skewness of the sample mean' % n, REFS['clSkew'] / math.sqrt(n))
M_SAMPLES = 2000
REFS['clM'] = M_SAMPLES
REFS['clSeTol'] = []
for n in SAMPLE_SIZES:
    tol = (E1['sd'] / math.sqrt(n)) * math.sqrt(((REFS['clKurt'] / n) + 2) / (4 * M_SAMPLES))
    REFS['clSeTol'].append(tol)
    out('n = %-3d sd of a standard error measured over %d samples (m)' % (n, M_SAMPLES), tol)
for n in SAMPLE_SIZES:
    M = sample_means(7000 + n, 'spring', _c, n, M_SAMPLES)
    tol = (E1['sd'] / math.sqrt(n)) * math.sqrt(((REFS['clKurt'] / n) + 2) / (4 * M_SAMPLES))
    out('n = %-3d %d sample means: mean, sd (m)' % (n, M_SAMPLES),
        '%.17g  %.17g' % (float(M.mean()), float(M.std(ddof=1))))
    out('   (measured SE - sigma/sqrt n) in units of its own sd',
        (float(M.std(ddof=1)) - E1['sd'] / math.sqrt(n)) / tol)

# ===========================================================================
path = os.path.join(HERE, 'refvals.txt')
io.open(path, 'w', encoding='utf-8').write('\n'.join(OUT_LINES) + '\n')


def js(v):
    if isinstance(v, bool):
        return 'true' if v else 'false'
    if isinstance(v, (float, np.floating)):
        return repr(float(v))
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (list, tuple)):
        return '[' + ','.join(js(x) for x in v) + ']'
    if isinstance(v, dict):
        return '{' + ','.join("'%s':%s" % (k, js(x)) for k, x in v.items()) + '}'
    if isinstance(v, str):
        return "'" + v + "'"
    raise TypeError(type(v))


lines = ['/* ================================================================== *',
         ' *  reference values — WRITTEN BY derive.py (build/projectile-        *',
         ' *  sampling-distributions); the same numbers are in refvals.txt.     *',
         ' * ================================================================== */',
         'const REF={']
for k, v in REFS.items():
    lines.append('  %s:%s,' % (k, js(v)))
lines.append('};\n')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write('\n'.join(lines))
print('\nwrote refvals.txt (%d lines) and p7a_refs.js (%d refs)' % (len(OUT_LINES), len(REFS)))
