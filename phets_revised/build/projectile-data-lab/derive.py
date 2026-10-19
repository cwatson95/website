#!/usr/bin/env python3
"""derive.py — the Python twin of projectile-data-lab.html (and of
projectile-sampling-distributions.html, which runs on the same engine).

Everything the pages' selfTest pins is re-derived here, independently of the
JavaScript, and printed (refvals.txt holds the output, read in full).  The
file also writes p7a_refs.js, the same numbers as a JS object, so no pinned
value is ever retyped by hand.

What is re-derived, and how
---------------------------
 1. PhET's constants, read out of the minified original
    docs/phets/projectile-data-lab_en.html and cited as "PhET's value":
    g = 9.81, the 100 m field, the 12 m raised launcher, the angle-standard-
    deviation range 0.2-5 deg, the three launcher mechanisms (mean speed,
    speed sd), the six mystery launchers, the three projectile types, the
    four launcher orientations, the sample sizes, the bin widths.
 2. The trajectory.  PhET's closed forms for the horizontal range and the
    total flight time from a height h are re-derived from scratch and checked
    three ways: against the root of y(t) = 0 by brentq, against a marched
    trajectory, and (for h = 0) against R = v^2 sin(2 theta)/g.  The
    maximum-range angle from a height is checked against a numerical argmax.
 3. mulberry32 + Box-Muller, bit for bit, so the JS sampler and this file
    draw the SAME numbers and every sample statistic can be pinned value by
    value against numpy.
 4. The EXACT distribution of the landing distance implied by PhET's
    mechanism.  PhET draws the angle as meanAngle + N(0, sd) and re-draws it
    (up to 100 times) while it is outside (0, 90) unless the launcher is the
    raised one; it draws the speed as mult*meanSpeed + N(0, sd) and re-draws
    while it is <= 0.  Both are therefore TRUNCATED normals, and the exact
    moments come from a 96 x 96 Gauss-Legendre product rule over the
    truncated z-ranges whose nodes and weights are emitted into the JS, so
    the page and this file evaluate the same rule.  The rule is checked
    against scipy's adaptive quadrature, against a 2e7-draw Monte Carlo of
    the actual re-draw mechanism, and — for h = 0 — against the closed form
    E[R^k] = E[v^2k] E[sin^k 2theta]/g^k of the UNtruncated model, whose
    difference is the size of the truncation.
 5. The exact probability density of the landing distance, by a 1-D
    quadrature over the launch angle of the speed density pushed through
    R(v, theta); checked by integrating it to 1, to the mean and to the
    second moment, and against the Monte-Carlo histogram.
 6. PhET's own delta-method standard deviation (its SampleSizeThumbnailNode
    sets the thumbnail x-range from it) against the exact standard deviation.
 7. A reference sample: the same PRNG and the same mechanism, 500 launches of
    mystery launcher 1 at 30 deg, with numpy's mean, median, standard
    deviation at ddof = 1 (PhET's convention) and ddof = 0, and the histogram
    counts under PhET's floor(x/w)*w binning at every bin width the sim
    offers.
 8. The central limit theorem: the standard error sigma/sqrt(n) at the four
    sample sizes, the exact sampling distribution of the measured standard
    error used as the tolerance, and a reference sampling experiment.
"""
import io
import math
import os

import numpy as np
from scipy import integrate, optimize, stats

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
head('1. PhET constants (read from docs/phets/projectile-data-lab_en.html)')
# PDLConstants in the minified build:
#   ANGLE_STANDARD_DEVIATION_RANGE: new Range(.2, 5)   (degrees)
#   MAX_FIELD_DISTANCE: 100, RAISED_LAUNCHER_HEIGHT: 12,
#   FREEFALL_ACCELERATION: 9.81, MINIMUM_TIME_BETWEEN_LAUNCHES: .7,
#   MAX_PROJECTILES_VSM_FIELD_DEFAULT: 500, maxSamples: 200
G = 9.81
FIELD = 100.0
RAISED_H = 12.0
ANG_SD = (0.2, 5.0)
SAMPLE_SIZES = [2, 5, 15, 40]
BIN_WIDTHS = [0.5, 1.0, 2.0, 5.0, 10.0]          # PDL; PSD drops the 10
TOTAL_BINS = [10, 20, 50, 100, 200]
ORIENT = [('angle30', 30.0, 0.0), ('angle45', 45.0, 0.0), ('angle60', 60.0, 0.0),
          ('angle0Raised', 0.0, RAISED_H)]
# LauncherMechanism(tandem, speedMean, speedStandardDeviation)
MECH = {'spring': (23.0, 0.5), 'pressure': (24.0, 0.2), 'explosion': (25.0, 1.2),
        'custom': (24.0, 0.5)}
TYPE_MULT = {'cannonball': 1.0, 'pumpkin': 1.1, 'piano': 0.9}
_c = 0.5 * (ANG_SD[0] + ANG_SD[1])                 # Range.getCenter()
_q = ANG_SD[0] + (ANG_SD[1] - ANG_SD[0]) / 4       # min + getLength()/4
# the six mystery launchers, in launcher order: (mechanism, angle sd in deg)
LAUNCHERS = [('spring', _c), ('pressure', ANG_SD[1]), ('explosion', ANG_SD[0]),
             ('spring', _q), ('pressure', ANG_SD[0]), ('explosion', ANG_SD[1])]
out('g, PhET FREEFALL_ACCELERATION (m/s^2)', G, 'G')
out('field length, MAX_FIELD_DISTANCE (m)', FIELD, 'FIELD')
out('raised launcher height, RAISED_LAUNCHER_HEIGHT (m)', RAISED_H, 'RAISED_H')
out('angle sd range min, max (deg)', '%g, %g' % ANG_SD)
out('angle sd centre (launcher 1) (deg)', _c, 'angSdCentre')
out('angle sd min + range/4 (launcher 4) (deg)', _q, 'angSdQuarter')
for k in ('spring', 'pressure', 'explosion', 'custom'):
    out('mechanism %-9s mean speed, sd (m/s)' % k, '%g, %g' % MECH[k])
out('projectile speed multipliers cannonball, pumpkin, piano',
    '%g, %g, %g' % (TYPE_MULT['cannonball'], TYPE_MULT['pumpkin'], TYPE_MULT['piano']))
out('sample sizes', str(SAMPLE_SIZES))
out('bin widths (PDL; PSD drops the 10)', str(BIN_WIDTHS))
out('total-bins choices (bin width = 100/totalBins)', str(TOTAL_BINS))
out('MINIMUM_TIME_BETWEEN_LAUNCHES (s)', 0.7, 'LAUNCH_GAP')
out('MAX_PROJECTILES_VSM_FIELD_DEFAULT', 500, 'MAX_PROJ', '%d')
out('maxSamples', 200, 'MAX_SAMPLES', '%d')
out('SamplingField.totalSampleTime at n = 2, 5, 15, 40 (s)', '0.75, 2, 5, 9')
REFS['SAMPLE_TIME'] = {'2': 0.75, '5': 2.0, '15': 5.0, '40': 9.0}
REFS['NBINS'] = TOTAL_BINS
REFS['MECH'] = {k: list(v) for k, v in MECH.items()}
REFS['LAUNCH_SD'] = [s for _, s in LAUNCHERS]
REFS['LAUNCH_MECH'] = [m for m, _ in LAUNCHERS]
REFS['SAMPLE_SIZES'] = SAMPLE_SIZES
REFS['TYPE_MULT'] = [TYPE_MULT['cannonball'], TYPE_MULT['pumpkin'], TYPE_MULT['piano']]

# ===========================================================================
head('2. the trajectory: PhET closed forms, re-derived and cross-checked')
# y(t) = h + v sin(th) t - g t^2/2 = 0  =>  t = [v s + sqrt(v^2 s^2 + 2 g h)]/g
# x(t) = v cos(th) t  =>  R = v cos(th)/g * (v s + sqrt(v^2 s^2 + 2 g h))


def flight_time(v, th_deg, h):
    s = math.sin(math.radians(th_deg))
    return v * s / G + math.sqrt((v * s / G) ** 2 + 2 * h / G)


def hrange(v, th_deg, h):
    th = math.radians(th_deg)
    s = math.sin(th)
    return v * math.cos(th) / G * (v * s + math.sqrt(v * v * s * s + 2 * G * h))


def range_brentq(v, th_deg, h):
    """independent route 1: the positive root of y(t) = 0 by bisection."""
    th = math.radians(th_deg)

    def y(t):
        return h + v * math.sin(th) * t - 0.5 * G * t * t
    hi = 1.0
    while y(hi) > 0:
        hi *= 2
    lo = 1e-12 if y(1e-12) > 0 else 0.0
    t = optimize.brentq(y, lo, hi, xtol=1e-15, rtol=8.9e-16)
    return v * math.cos(th) * t, t


def range_march(v, th_deg, h, n=400000):
    """independent route 2: march the equations of motion, landing the last
    step exactly on y = 0.  With constant gravity every step is algebraically
    exact, so the only error is the accumulated rounding of n additions."""
    th = math.radians(th_deg)
    vx, vy = v * math.cos(th), v * math.sin(th)
    dt = flight_time(v, th_deg, h) * 1.2 / n
    x, y, t = 0.0, h, 0.0
    for _ in range(n):
        ny = y + vy * dt - 0.5 * G * dt * dt
        if ny <= 0:
            a, b, c = -0.5 * G, vy, y
            tt = (-b - math.sqrt(b * b - 4 * a * c)) / (2 * a)
            return x + vx * tt, t + tt
        x += vx * dt
        y = ny
        vy -= G * dt
        t += dt
    raise RuntimeError('did not land')


for (v, th, h) in [(23.0, 30.0, 0.0), (24.0, 45.0, 0.0), (25.0, 60.0, 0.0),
                   (23.0, 0.0, RAISED_H), (24.0, -7.0, RAISED_H), (20.0, 80.0, 0.0)]:
    R = hrange(v, th, h)
    Rb, tb = range_brentq(v, th, h)
    Rm, tm = range_march(v, th, h)
    out('range  %-22s (m)' % ('v=%g th=%g h=%g' % (v, th, h)), R)
    out('   brentq root of y(t)=0: relative difference', abs(R / Rb - 1))
    out('   marched trajectory:    relative difference', abs(R / Rm - 1))
    out('   flight time (s), vs brentq rel diff',
        '%.17g  %.3e' % (flight_time(v, th, h), abs(flight_time(v, th, h) / tb - 1)))
    assert abs(R / Rb - 1) < 1e-14 and abs(R / Rm - 1) < 2e-10
worst = max(abs(hrange(23.0, th, 0.0) / (23.0 ** 2 * math.sin(2 * math.radians(th)) / G) - 1)
            for th in (5.0, 15.0, 30.0, 45.0, 60.0, 75.0, 85.0))
out('h = 0: R against v^2 sin(2 theta)/g at 7 angles, worst rel diff', worst)
assert worst < 1e-15
REFS['rangeCases'] = [[vv, tt, hh, hrange(vv, tt, hh), flight_time(vv, tt, hh)]
                      for (vv, tt, hh) in [(23.0, 30.0, 0.0), (24.0, 45.0, 0.0), (25.0, 60.0, 0.0),
                                           (23.0, 0.0, RAISED_H), (24.0, -7.0, RAISED_H)]]
# the maximum-range angle from a height: cos(2 th*) = g h/(v^2 + g h)
REFS['maxAngle'] = []
for (v, h) in [(23.0, RAISED_H), (25.0, RAISED_H), (23.0, 0.0)]:
    thstar = 0.5 * math.degrees(math.acos(G * h / (v * v + G * h)))
    num = optimize.minimize_scalar(lambda t: -hrange(v, t, h), bounds=(1.0, 89.0),
                                   method='bounded', options={'xatol': 1e-11})
    out('max-range angle from h=%g at v=%g (deg), closed form' % (h, v), thstar)
    out('   numerical argmax, difference (deg)', abs(thstar - num.x))
    assert abs(thstar - num.x) < 1e-6
    REFS['maxAngle'].append([v, h, thstar])

# ===========================================================================
head('3. mulberry32 + Box-Muller, bit for bit')


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
    """Box-Muller, one pair of uniforms per value (no caching: a draw count
    that does not depend on history keeps the stream reproducible)."""
    u1 = 1.0 - nxt()          # in (0, 1], so the log is finite
    u2 = nxt()
    return math.sqrt(-2.0 * math.log(u1)) * math.cos(2 * math.pi * u2)


rng = mulberry32(20260921)
REFS['rngStream'] = [rng() for _ in range(6)]
for k, v in enumerate(REFS['rngStream']):
    out('mulberry32(20260921) draw %d' % k, v)
rng = mulberry32(20260921)
REFS['gaussStream'] = [gauss_of(rng) for _ in range(6)]
for k, v in enumerate(REFS['gaussStream']):
    out('Box-Muller from the same seed, value %d' % k, v)
r7 = mulberry32(7)
u = np.array([r7() for _ in range(2000000)])
out('mulberry32(7): mean of 2e6 draws (exact 0.5, se 2.04e-4)', float(u.mean()), 'u7mean')
out('   variance (exact 1/12 = 0.08333333)', float(u.var(ddof=1)), 'u7var')
out('   Kolmogorov-Smirnov p against U(0,1)', float(stats.kstest(u, 'uniform').pvalue), 'u7ks')
r7 = mulberry32(7)
z = np.array([gauss_of(r7) for _ in range(1000000)])
out('Box-Muller: mean of 1e6 normals (se 1e-3)', float(z.mean()), 'z7mean')
out('   variance (exact 1)', float(z.var(ddof=1)), 'z7var')
out('   skewness (exact 0), excess kurtosis (exact 0)',
    '%.17g  %.17g' % (float(stats.skew(z)), float(stats.kurtosis(z))))
out('   Kolmogorov-Smirnov p against N(0,1)', float(stats.kstest(z, 'norm').pvalue), 'z7ks')

# ===========================================================================
head('4. the exact distribution of the landing distance (truncated normals)')


def sd_of_stability(stab):
    """PhET: standardDeviationAngle = linear(1, 0, sdMin, sdMax, stability),
    i.e. stability 1 -> the smallest spread, stability 0 -> the largest."""
    return ANG_SD[0] + (ANG_SD[1] - ANG_SD[0]) * (1.0 - stab)


for st_ in (0.0, 0.25, 0.5, 0.75, 1.0):
    out('angle stability %.2f -> angle sd (deg)' % st_, sd_of_stability(st_))
REFS['sdStab'] = [sd_of_stability(s) for s in (0.0, 0.25, 0.5, 0.75, 1.0)]

NGL = 96
NPANEL = 8   # panels for the density's theta integral (see pdf_R)
GL_X, GL_W = np.polynomial.legendre.leggauss(NGL)
REFS['glX'] = [float(x) for x in GL_X]
REFS['glW'] = [float(x) for x in GL_W]
ZCAP = 12.0          # beyond 12 sigma a normal density is below 1e-32
REFS['NGL'] = NGL
REFS['ZCAP'] = ZCAP
out('Gauss-Legendre nodes for the truncated normals', NGL)
out('   sum of the weights (exact 2)', float(GL_W.sum()))
out('   sum w x^2 (exact 2/3)', float((GL_W * GL_X ** 2).sum()))


def phi(z):
    return np.exp(-0.5 * z * z) / math.sqrt(2 * math.pi)


def zrule(a, b):
    """nodes z and weights carrying phi(z) dz over [a, b]; sum(w) = Phi(b)-Phi(a)."""
    z = 0.5 * (b - a) * GL_X + 0.5 * (a + b)
    return z, 0.5 * (b - a) * GL_W * phi(z)


def zrange(mu, sd, lo, hi):
    """the z-interval of N(mu, sd) truncated to (lo, hi), capped at 12 sigma."""
    a = -ZCAP if lo is None else max(-ZCAP, (lo - mu) / sd)
    b = ZCAP if hi is None else min(ZCAP, (hi - mu) / sd)
    return a, b


def grid(mu, sv, m, w, h, raised):
    zv, wv = zrule(*zrange(mu, sv, 0.0, None))
    zt, wt = zrule(*zrange(m, w, None, None)) if raised else zrule(*zrange(m, w, 0.0, 90.0))
    V = mu + sv * zv
    TH = m + w * zt
    thr = np.radians(TH)
    s, c = np.sin(thr), np.cos(thr)
    R = V[:, None] * c[None, :] / G * (V[:, None] * s[None, :]
                                       + np.sqrt(V[:, None] ** 2 * s[None, :] ** 2 + 2 * G * h))
    Wt = np.outer(wv, wt)
    return R, Wt / Wt.sum()


def moments(mu, sv, m, w, h, raised=False, kmax=4):
    R, P = grid(mu, sv, m, w, h, raised)
    return [float((P * R ** k).sum()) for k in range(1, kmax + 1)]


def central(mu, sv, m, w, h, raised=False):
    """TWO passes: the mean, then the central moments about it.  Assembling
    mu3 from the raw moments cancels five to seven digits (m3 ~ 2e5 against
    mu3 ~ 0.02), and the JS and Python sums round that cancellation
    differently — the two-pass form agrees to 1e-15 and is the honest value
    of the quadrature anyway."""
    R, P = grid(mu, sv, m, w, h, raised)
    g = [float((P * R ** k).sum()) for k in (1, 2, 3, 4)]
    D = R - g[0]
    c2 = float((P * D ** 2).sum())
    return dict(m1=g[0], m2=g[1], m3=g[2], m4=g[3], mean=g[0], var=c2, sd=math.sqrt(c2),
                mu3=float((P * D ** 3).sum()), mu4=float((P * D ** 4).sum()))


# ---- the untruncated closed forms, h = 0 -----------------------------------
def v_moments(mu, s):
    return {2: mu * mu + s * s,
            4: mu ** 4 + 6 * mu * mu * s * s + 3 * s ** 4,
            6: mu ** 6 + 15 * mu ** 4 * s ** 2 + 45 * mu ** 2 * s ** 4 + 15 * s ** 6,
            8: mu ** 8 + 28 * mu ** 6 * s ** 2 + 210 * mu ** 4 * s ** 4
               + 420 * mu ** 2 * s ** 6 + 105 * s ** 8}


def sin2_moments(m, w):
    """E[sin^k(2 theta)], k = 1..4, for theta ~ N(m, w) (radians), from
    E[e^{i a theta}] = e^{i a m - a^2 w^2/2}."""
    def C(a):
        return math.cos(a * m) * math.exp(-0.5 * a * a * w * w)

    def S(a):
        return math.sin(a * m) * math.exp(-0.5 * a * a * w * w)
    return {1: S(2), 2: 0.5 * (1 - C(4)), 3: 0.25 * (3 * S(2) - S(6)),
            4: 0.125 * (3 - 4 * C(4) + C(8))}


def moments_closed(mu, s, m_deg, w_deg):
    vm = v_moments(mu, s)
    sm = sin2_moments(math.radians(m_deg), math.radians(w_deg))
    return [vm[2 * k] * sm[k] / G ** k for k in (1, 2, 3, 4)]


def moments_scipy(mu, sv, m, w, h, raised=False, kmax=2):
    """independent route: scipy's adaptive quadrature over the same truncated
    densities."""
    res = []
    vlo = max(0.0, mu - ZCAP * sv)
    tlo, thi = (m - ZCAP * w, m + ZCAP * w) if raised else (0.0, 90.0)
    den = (stats.norm.cdf(min(ZCAP, (thi - m) / w)) - stats.norm.cdf(max(-ZCAP, (tlo - m) / w))) \
        * (stats.norm.cdf(ZCAP) - stats.norm.cdf(max(-ZCAP, (0.0 - mu) / sv)))
    for k in range(1, kmax + 1):
        def f(th, k=k):
            def g(v):
                return hrange(v, th, h) ** k * stats.norm.pdf(v, mu, sv)
            return integrate.quad(g, vlo, mu + ZCAP * sv, epsabs=1e-14, epsrel=1e-14,
                                  limit=300)[0] * stats.norm.pdf(th, m, w)
        res.append(integrate.quad(f, tlo, thi, epsabs=1e-13, epsrel=1e-13, limit=300)[0] / den)
    return res


def mc_sample(mu, sv, m, w, h, raised, n=8000000, seed=4242):
    """Monte Carlo of PhET's ACTUAL mechanism, re-draws and all."""
    rs = np.random.default_rng(seed)
    v = rs.normal(mu, sv, n)
    bad = v <= 0
    while bad.any():
        v[bad] = rs.normal(mu, sv, int(bad.sum()))
        bad = v <= 0
    th = rs.normal(m, w, n)
    if not raised:
        bad = (th <= 0) | (th >= 90)
        while bad.any():
            th[bad] = rs.normal(m, w, int(bad.sum()))
            bad = (th <= 0) | (th >= 90)
    thr = np.radians(th)
    s, c = np.sin(thr), np.cos(thr)
    return v * c / G * (v * s + np.sqrt(v * v * s * s + 2 * G * h))


CASES = [('launcher 1 (spring, sd 2.6 deg) at 30 deg', 23.0, 0.5, 30.0, _c, 0.0, False),
         ('launcher 2 (pressure, sd 5 deg) at 30 deg', 24.0, 0.2, 30.0, 5.0, 0.0, False),
         ('launcher 3 (explosion, sd 0.2 deg) at 30 deg', 25.0, 1.2, 30.0, 0.2, 0.0, False),
         ('launcher 5 (pressure, sd 0.2 deg) at 45 deg', 24.0, 0.2, 45.0, 0.2, 0.0, False),
         ('launcher 6 (explosion, sd 5 deg) at 60 deg', 25.0, 1.2, 60.0, 5.0, 0.0, False),
         ('launcher 1 raised 12 m, mean angle 0', 23.0, 0.5, 0.0, _c, RAISED_H, True)]
EXACT = {}
for (name, mu, sv, m, w, h, raised) in CASES:
    E = central(mu, sv, m, w, h, raised)
    EXACT[name] = E
    out('EXACT  %s' % name, '')
    out('   mean of the landing distance (m)', E['mean'])
    out('   standard deviation (m)', E['sd'])
    out('   skewness  mu3/sd^3', E['mu3'] / E['sd'] ** 3)
    out('   excess kurtosis  mu4/sd^4 - 3', E['mu4'] / E['sd'] ** 4 - 3)
    q = moments_scipy(mu, sv, m, w, h, raised)
    out('   scipy adaptive quadrature: mean rel diff', abs(q[0] / E['m1'] - 1))
    out('   scipy adaptive quadrature: second moment rel diff', abs(q[1] / E['m2'] - 1))
    assert abs(q[0] / E['m1'] - 1) < 1e-12 and abs(q[1] / E['m2'] - 1) < 1e-12
    if not raised:
        cf = moments_closed(mu, sv, m, w)
        out('   UNtruncated closed form mean (m), minus the truncated one',
            '%.17g  %+.3e' % (cf[0], cf[0] - E['m1']))
        out('   UNtruncated closed form sd (m), minus the truncated one',
            '%.17g  %+.3e' % (math.sqrt(cf[1] - cf[0] ** 2), math.sqrt(cf[1] - cf[0] ** 2) - E['sd']))
        out('   P(angle outside 0..90), P(speed <= 0)',
            '%.3e  %.3e' % (stats.norm.cdf(0.0, m, w) + stats.norm.sf(90.0, m, w),
                            stats.norm.cdf(0.0, mu, sv)))
    R = mc_sample(mu, sv, m, w, h, raised)
    se = R.std(ddof=1) / math.sqrt(len(R))
    out('   Monte Carlo of the re-draw mechanism, 8e6: (MC - exact)/se', (R.mean() - E['mean']) / se)
    out('   Monte-Carlo sd / exact sd - 1 (its own se is 2.5e-4)', R.std(ddof=1) / E['sd'] - 1)
    assert abs((R.mean() - E['mean']) / se) < 4.0
REFS['exactCases'] = [[c[1], c[2], c[3], c[4], c[5], 1 if c[6] else 0,
                       EXACT[c[0]]['mean'], EXACT[c[0]]['sd'], EXACT[c[0]]['mu3'], EXACT[c[0]]['mu4']]
                      for c in CASES]
# the closed form for the untruncated model, as its own pin
REFS['closedCases'] = [moments_closed(c[1], c[2], c[3], c[4]) for c in CASES if not c[6]]
REFS['truncGap'] = max(abs(moments_closed(c[1], c[2], c[3], c[4])[0] - EXACT[c[0]]['mean'])
                       for c in CASES if not c[6])
out('the worst truncation shift of the mean over the five flat cases (m)', REFS['truncGap'])

# ---- PhET's own delta-method sd --------------------------------------------
head('4b. PhET calculateRangeStdDev (its delta method) against the exact sd')


def phet_delta_sd(v, sdv, th_deg, sdth_deg):
    """PhET SampleSizeThumbnailNode.calculateRangeStdDev, in maths:
    sqrt((2v/g sin2th)^2 sdv^2 + (2v^2/g cos2th)^2 sdth^2), sdth in radians —
    the first-order (delta-method) propagation through R = v^2 sin(2th)/g."""
    s, r = math.radians(th_deg), math.radians(sdth_deg)
    return math.sqrt((2 * v / G * math.sin(2 * s)) ** 2 * sdv ** 2
                     + (2 * v * v / G * math.cos(2 * s)) ** 2 * r ** 2)


REFS['deltaSd'] = []
REFS['naiveMean'] = []
for (name, mu, sv, m, w, h, raised) in CASES:
    if raised:
        continue
    d = phet_delta_sd(mu, sv, m, w)
    naive = mu * mu * math.sin(2 * math.radians(m)) / G
    ex = EXACT[name]
    out('%s' % name, '')
    out('   PhET delta-method sd (m); delta/exact - 1',
        '%.17g  %+.5f %%' % (d, 100 * (d / ex['sd'] - 1)))
    out('   naive mean v^2 sin2th/g (m); naive/exact - 1',
        '%.17g  %+.5f %%' % (naive, 100 * (naive / ex['mean'] - 1)))
    REFS['deltaSd'].append(d)
    REFS['naiveMean'].append(naive)

# ===========================================================================
head('5. the exact probability density of the landing distance')
# f_R(r) = int f_theta(th) f_v(v*(r,th))/|dR/dv|(v*, th) dth over the accepted
# angles.  R is increasing in v at fixed th (cos th > 0), so v* is unique.


def dR_dv(v, th_deg, h):
    th = math.radians(th_deg)
    s, c = math.sin(th), math.cos(th)
    Q = math.sqrt(v * v * s * s + 2 * G * h)
    return c / G * (2 * v * s + (2 * v * v * s * s + 2 * G * h) / Q)


def v_star(r, th_deg, h):
    """the launch speed landing at r from angle th: closed form when h = 0,
    else Newton from that seed.  R(v) is strictly increasing at fixed theta
    (the derivative below is positive for every v), but for a DOWNWARD launch
    from a height it is bounded: as v grows the path straightens and the range
    tends to h cos/|sin| = h/tan|theta|.  Beyond that no speed reaches r, and
    the answer is None rather than a Newton iteration that divides by a
    vanishing derivative."""
    th = math.radians(th_deg)
    s, c = math.sin(th), math.cos(th)
    if c <= 1e-9 or r <= 0:
        return None
    if h == 0.0:
        return None if s <= 0 else math.sqrt(r * G / math.sin(2 * th))
    if s < 0 and r >= h * c / (-s):
        return None
    v = math.sqrt(r * G / math.sin(2 * th)) if s > 1e-4 else r * math.sqrt(G / (2 * h)) / c
    for _ in range(120):
        d = dR_dv(v, th_deg, h)
        if not (d > 1e-12):
            return None
        step = (hrange(v, th_deg, h) - r) / d
        v = max(1e-9, v - step)
        if abs(step) < 1e-15 * max(1.0, v):
            break
    return v if abs(hrange(v, th_deg, h) - r) < 1e-9 * max(1.0, r) else None


def pdf_R(r, mu, sv, m, w, h, raised, panels=NPANEL):
    """The density of the landing distance at r.

    Unlike the moments, this is a one-dimensional integral over theta at FIXED
    r, and its integrand is a spike: only the angles whose v*(r, theta) lands
    within a few sd of the mean speed contribute at all.  A small speed spread
    beside a large angle spread therefore rings a single 96-node rule (29 % on
    mystery launcher 2, 292 % raised), so the interval is split into `panels`
    equal panels, each carrying the same rule.  The page does exactly this.
    """
    a, b = zrange(m, w, None, None) if raised else zrange(m, w, 0.0, 90.0)
    av, bv = zrange(mu, sv, 0.0, None)
    zv, wv = zrule(av, bv)
    tot = 0.0
    tw = 0.0
    for k in range(panels):
        aa, bb = a + (b - a) * k / panels, a + (b - a) * (k + 1) / panels
        zt, wt = zrule(aa, bb)
        tw += wt.sum()
        for j in range(NGL):
            th = m + w * zt[j]
            vs = v_star(r, th, h)
            if vs is None or vs <= 0:
                continue
            tot += wt[j] * stats.norm.pdf(vs, mu, sv) / dR_dv(vs, th, h)
    return tot / (tw * wv.sum())


REFS['pdfAtMean'] = []
for (name, mu, sv, m, w, h, raised) in CASES:
    E = EXACT[name]
    lo, hi = max(1e-6, E['mean'] - 9 * E['sd']), E['mean'] + 9 * E['sd']
    xs = np.linspace(lo, hi, 1201)
    ps = np.array([pdf_R(float(x), mu, sv, m, w, h, raised) for x in xs])
    I0 = float(np.trapezoid(ps, xs))
    I1 = float(np.trapezoid(ps * xs, xs))
    I2 = float(np.trapezoid(ps * xs ** 2, xs))
    out('pdf  %s' % name, '')
    out('   integral of the density (exact 1; trapezoid on 1201 points)', I0)
    out('   its first moment / the exact mean - 1', I1 / E['mean'] - 1)
    out('   its second moment / the exact one - 1', I2 / E['m2'] - 1)
    out('   the density at the exact mean (1/m)', pdf_R(E['mean'], mu, sv, m, w, h, raised))
    assert abs(I0 - 1) < 1e-6 and abs(I1 / E['mean'] - 1) < 1e-6
    REFS['pdfAtMean'].append(float(pdf_R(E['mean'], mu, sv, m, w, h, raised)))
# against the Monte-Carlo histogram of the mechanism itself
R = mc_sample(23.0, 0.5, 30.0, _c, 0.0, False, n=8000000, seed=99)
E = EXACT[CASES[0][0]]
edges = np.linspace(E['mean'] - 3 * E['sd'], E['mean'] + 3 * E['sd'], 25)
cnt, _ = np.histogram(R, bins=edges)
mid = 0.5 * (edges[1:] + edges[:-1])
dens = cnt / len(R) / (edges[1] - edges[0])
dx = float(edges[1] - edges[0])
# a histogram bin does not sample the density at its midpoint, it AVERAGES it
# over the bin: taking f(mid) instead costs (dx^2/24) f'' ~ 2.6e-3 of f here,
# which is larger than the 1.1e-3 Monte-Carlo noise, so the comparison would
# be measuring the midpoint rule.  Average f over each bin (Simpson, 5 points).
th_dens = np.array([float(np.trapezoid(
    [pdf_R(float(x), 23.0, 0.5, 30.0, _c, 0.0, False) for x in np.linspace(edges[i], edges[i + 1], 9)],
    np.linspace(edges[i], edges[i + 1], 9))) / dx for i in range(len(cnt))])
zsc = (dens - th_dens) * len(R) * dx / np.sqrt(np.maximum(cnt, 1))
out('density vs 8e6 Monte-Carlo histogram, 24 bin averages: worst |z|', float(np.abs(zsc).max()))
out('   (using f at the bin midpoint instead would cost this much of f)', dx * dx / 24 / E['sd'] ** 2)
assert float(np.abs(zsc).max()) < 4.0

# ===========================================================================
head('6. a reference sample: the same PRNG, the same mechanism, numpy')
# The JS draws, per projectile: the angle Gaussian first (with its re-draws),
# then the speed Gaussian (with its re-draws).  This twin does the same, so
# the two produce the SAME landing distances.


def sample_field(seed, n, mech, sd_ang, mean_ang, h, mult=1.0, raised=False):
    nxt = mulberry32(seed)
    mu, sv = MECH[mech]
    mu = mu * mult
    xs = []
    for _ in range(n):
        a = mean_ang + gauss_of(nxt) * sd_ang
        if not raised:
            k = 0
            while k < 100 and (a <= 0 or a >= 90):
                a = mean_ang + gauss_of(nxt) * sd_ang
                k += 1
        v = mu + gauss_of(nxt) * sv
        while v <= 0:
            v = mu + gauss_of(nxt) * sv
        xs.append(hrange(v, a, h))
    return np.array(xs)


SEED_REF = 20260921
X = sample_field(SEED_REF, 500, 'spring', _c, 30.0, 0.0)
REFS['sampleSeed'] = SEED_REF
REFS['sampleN'] = 500
REFS['sampleFirst5'] = [float(v) for v in X[:5]]
REFS['sampleLast'] = float(X[-1])
for k in range(5):
    out('reference sample landing distance #%d (m)' % k, float(X[k]))
out('reference sample landing distance #499 (m)', float(X[-1]))
out('numpy mean (m)', float(X.mean()), 'sMean')
out('numpy median (m)', float(np.median(X)), 'sMedian')
out('numpy std, ddof = 1  (PhET convention) (m)', float(X.std(ddof=1)), 'sSd1')
out('numpy std, ddof = 0  (m)', float(X.std(ddof=0)), 'sSd0')
out('   ddof=1 / ddof=0 (exact sqrt(500/499) = 1.00100200)', float(X.std(ddof=1) / X.std(ddof=0)), 'sSdRatio')
out('numpy min (m)', float(X.min()), 'sMin')
out('numpy max (m)', float(X.max()), 'sMax')
out('standard error sd/sqrt(n) (m)', float(X.std(ddof=1) / math.sqrt(len(X))), 'sSe')
# the sample is 500 draws from the exact law: its mean should sit within
# sigma/sqrt(500) of the exact mean
E1 = EXACT[CASES[0][0]]
out('   (sample mean - exact mean)/(sigma/sqrt 500)',
    (float(X.mean()) - E1['mean']) / (E1['sd'] / math.sqrt(500)))
out('   (sample sd - exact sd)/its own sampling sd',
    (float(X.std(ddof=1)) - E1['sd']) / (E1['sd'] * math.sqrt((E1['mu4'] / E1['sd'] ** 4 - 1) / (4 * 500))))
# PhET's binning: bin(x) = floor(x/w)*w, so bins are [k w, (k+1) w)
BINCOUNTS = {}
for w in BIN_WIDTHS:
    keys = np.floor(X / w).astype(int)
    lo, hi = int(keys.min()), int(keys.max())
    counts = [int((keys == k).sum()) for k in range(lo, hi + 1)]
    BINCOUNTS['%g' % w] = [lo, counts]
    out('bin width %-4g: first bin index, counts' % w, '%d  %s' % (lo, counts))
    assert sum(counts) == len(X)
    nc, _ = np.histogram(X, bins=np.arange(lo, hi + 2) * w)
    assert list(nc) == counts, (w, list(nc), counts)
REFS['binCounts'] = BINCOUNTS
out('numpy.histogram agrees with floor(x/w)*w at every bin width', 'yes')
frac = float(((X >= 40.0) & (X <= 60.0)).sum()) / len(X)
out('interval tool default [40, 60] m: fraction of the sample', frac, 'sFrac4060')
xs = np.linspace(40.0, 60.0, 4001)
ps = np.array([pdf_R(float(x), 23.0, 0.5, 30.0, _c, 0.0, False) for x in xs])
pin = float(np.trapezoid(ps, xs))
out('   P(40 <= R <= 60) from the exact density', pin, 'pIn4060')
out('   the sample fraction is this many binomial sd away',
    (frac - pin) / math.sqrt(pin * (1 - pin) / 500))

# ===========================================================================
head('7. the central limit theorem at PhET sample sizes')
sig, mean1 = E1['sd'], E1['mean']
REFS['clSigma'] = sig
REFS['clMean'] = mean1
REFS['clSe'] = [sig / math.sqrt(n) for n in SAMPLE_SIZES]
for n in SAMPLE_SIZES:
    out('n = %-3d standard error sigma/sqrt(n) (m)' % n, sig / math.sqrt(n))
out('skewness of one landing distance', E1['mu3'] / sig ** 3, 'clSkew')
out('excess kurtosis of one landing distance', E1['mu4'] / sig ** 4 - 3, 'clKurt')
for n in SAMPLE_SIZES:
    out('n = %-3d skewness of the sample mean (skew/sqrt n)' % n, E1['mu3'] / sig ** 3 / math.sqrt(n))
# the sampling sd of a standard error measured over M samples: the delta
# method on s^2 gives sd(s) = sigma sqrt((kurt + 2)/(4 M)) with kurt the
# EXCESS kurtosis of the sample mean, which is the parent's divided by n.
M_SAMPLES = 4000
REFS['clM'] = M_SAMPLES
REFS['clSeTol'] = []
for n in SAMPLE_SIZES:
    kn = (E1['mu4'] / sig ** 4 - 3) / n
    tol = (sig / math.sqrt(n)) * math.sqrt((kn + 2) / (4 * M_SAMPLES))
    REFS['clSeTol'].append(tol)
    out('n = %-3d sd of a standard error measured over %d samples (m)' % (n, M_SAMPLES), tol)
for n in SAMPLE_SIZES:
    X2 = sample_field(4000 + n, n * 2000, 'spring', _c, 30.0, 0.0)
    means = X2.reshape(2000, n).mean(axis=1)
    kn = (E1['mu4'] / sig ** 4 - 3) / n
    tol2 = (sig / math.sqrt(n)) * math.sqrt((kn + 2) / (4 * 2000))
    out('n = %-3d 2000 sample means: mean, sd (m)' % n,
        '%.17g  %.17g' % (float(means.mean()), float(means.std(ddof=1))))
    out('   (measured SE - sigma/sqrt n) in units of its own sd',
        (float(means.std(ddof=1)) - sig / math.sqrt(n)) / tol2)

head('7b. a reference SAMPLING run (the Sampling screen), numpy')
SEED_SAMP = 20260922
NS, NSIZE = 200, 5
XS = sample_field(SEED_SAMP, NS * NSIZE, 'spring', _c, 30.0, 0.0)
MEANS = XS.reshape(NS, NSIZE).mean(axis=1)
REFS['sampSeed'] = SEED_SAMP
REFS['sampN'] = NS
REFS['sampSize'] = NSIZE
REFS['sampFirst3'] = [float(v) for v in MEANS[:3]]
for k in range(3):
    out('sample %d: mean of %d (m)' % (k, NSIZE), float(MEANS[k]))
out('mean of the 200 sample means (m)', float(MEANS.mean()), 'sampMean')
out('sd of the 200 sample means, ddof = 1 (m)', float(MEANS.std(ddof=1)), 'sampSd')
out('   sigma/sqrt(n) for n = 5 (m)', sig / math.sqrt(NSIZE), 'sampSeExact')
out('median of the 200 sample means (m)', float(np.median(MEANS)), 'sampMedian')
keys = np.floor(MEANS / 0.5).astype(int)
lo = int(keys.min())
cnt = [int((keys == k).sum()) for k in range(lo, int(keys.max()) + 1)]
REFS['sampBins'] = [lo, cnt]
out('bin width 0.5 m: first bin index, counts', '%d  %s' % (lo, cnt))

# ===========================================================================
head('8. every launcher, orientation and projectile type')
REFS['launcherStats30'] = []
for i, (mech, sd) in enumerate(LAUNCHERS):
    mu, sv = MECH[mech]
    E = central(mu, sv, 30.0, sd, 0.0)
    out('launcher %d at 30 deg: exact mean, sd (m)' % (i + 1), '%.17g  %.17g' % (E['mean'], E['sd']))
    REFS['launcherStats30'].append([E['mean'], E['sd']])
REFS['orientStats'] = []
for nm, ang, h in ORIENT:
    E = central(23.0, 0.5, ang, _c, h, nm == 'angle0Raised')
    out('launcher 1, orientation %-12s: mean, sd (m)' % nm, '%.17g  %.17g' % (E['mean'], E['sd']))
    REFS['orientStats'].append([E['mean'], E['sd']])
REFS['typeStats'] = []
for nm in ('cannonball', 'pumpkin', 'piano'):
    E = central(23.0 * TYPE_MULT[nm], 0.5, 30.0, _c, 0.0)
    out('launcher 1 with a %-11s: mean, sd (m)' % nm, '%.17g  %.17g' % (E['mean'], E['sd']))
    REFS['typeStats'].append([E['mean'], E['sd']])
E = central(25.0, 1.2, 45.0, 0.2, 0.0)
out('the longest throw the sim can make (explosion, 45 deg, sd 0.2): mean, sd',
    '%.17g  %.17g' % (E['mean'], E['sd']))
out('   (100 m - mean)/sd — how far the field edge is', (100 - E['mean']) / E['sd'])
out('   P(R > 100 m) from the exact density', float(np.trapezoid(
    [pdf_R(float(x), 25.0, 1.2, 45.0, 0.2, 0.0, False) for x in np.linspace(100.0, 130.0, 601)],
    np.linspace(100.0, 130.0, 601))), 'pOver100')

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
         ' *  reference values — WRITTEN BY derive.py (build/projectile-data-   *',
         ' *  lab); the same numbers are printed in refvals.txt.  Do not edit.  *',
         ' * ================================================================== */',
         'const REF={']
for k, v in REFS.items():
    lines.append('  %s:%s,' % (k, js(v)))
lines.append('};\n')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write('\n'.join(lines))
print('\nwrote refvals.txt (%d lines) and p7a_refs.js (%d refs)' % (len(OUT_LINES), len(REFS)))
