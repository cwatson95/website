#!/usr/bin/env python3
"""derive.py — the Python twin of gravity-force-lab.html.

Re-derives every number the sim's selfTest pins, from scratch:

  * G from CODATA 2022 (scipy.constants), and PhET's own value for parity notes
  * the sphere radius r = (3m / 4 pi rho)^(1/3) at PhET's density 150 kg/m^3
  * PhET's no-overlap rule: centres at least snap(r1 + r2 + 0.1 m) apart on a
    0.1-m grid — enumerated over EVERY mass pair the sliders can reach, in both
    size modes, to prove the snapped rule never lets two spheres touch
  * the push rule (who moves when a sphere grows) on five scenarios
  * the force at the defaults and the extremes, and PhET's two readout formats
  * the free fall if the spheres were let go: the radial two-body closed form
    t(r) = sqrt(r0^3 / 2GM) [ sqrt(x(1-x)) + asin sqrt(1-x) ],  x = r/r0,
    checked against scipy solve_ivp integrating BOTH bodies (Newton's third law
    is then an output, not an input) and against brentq for the inverse r(t)
  * the strongest pull two equal masses can reach, in each size mode

Every value is printed to 13 significant digits; the output is refvals.txt,
which the selfTest pins cite as (derive).  Read it in full, never through
head/tail (Known-bad: a value that never appeared in output you read is not a
reference value).
"""
import math
import scipy
import scipy.constants as C
from scipy.integrate import solve_ivp
from scipy.optimize import brentq

P = lambda *a: print(*a)
def g13(x): return '%.13g' % x

# ------------------------------------------------------------------ constants
G = C.G                                   # CODATA 2022
P('scipy', scipy.__version__)
P('G (CODATA 2022, scipy)', g13(G), 'uncertainty', C.physical_constants['Newtonian constant of gravitation'][2])
G_PHET = 6.67408e-11                      # PhET's PHET_CORE/PhysicalConstants (CODATA 2014)
P('G_PHET', g13(G_PHET), 'G/G_PHET - 1 =', g13(G / G_PHET - 1))

RHO = 150.0      # PhET GravityForceLabConstants.MASS_DENSITY
RC = 0.5         # ISLCConstants.CONSTANT_RADIUS
SEP = 0.1        # ISLCModel minSeparationBetweenObjects
Q = 0.1          # snapObjectsToNearest
IL, IR = -50, 50 # the +-5 m track in 0.1-m counts
MASSES = list(range(10, 1001, 10))

def sym_round(y):
    """JavaScript's Math.round applied symmetrically (PhET's roundSymmetric):
    the nearest integer, halves away from zero.  NOT Python's round()."""
    return int(math.copysign(math.floor(abs(y) + 0.5), y))

def radius(m, cs):
    return RC if cs else math.pow(3 * m / RHO / (4 * math.pi), 1 / 3)

def nmin(m1, m2, cs):
    return sym_round((radius(m1, cs) + radius(m2, cs) + SEP) / Q)

def force(m1, m2, r):
    return G * m1 * m2 / (r * r)

P('\n# radii (mass-scaled, rho = 150)')
for m in (10, 100, 400, 1000):
    P('radius', m, g13(radius(m, False)))
m_half = RHO * 4 / 3 * math.pi * RC ** 3
P('mass whose scaled radius is 0.5 m', g13(m_half))

P('\n# the no-overlap rule over every reachable pair')
for cs in (False, True):
    worst_gap, worst_pair, tie, tie_pair, nmax = 9, None, 9, None, 0
    for m1 in MASSES:
        for m2 in MASSES:
            s = radius(m1, cs) + radius(m2, cs) + SEP
            y = s / Q
            n = sym_round(y)
            gap = n * Q - (radius(m1, cs) + radius(m2, cs))
            if gap < worst_gap:
                worst_gap, worst_pair = gap, (m1, m2)
            fr = abs((y - math.floor(y)) - 0.5)
            if fr < tie:
                tie, tie_pair = fr, (m1, m2)
            nmax = max(nmax, n)
    P('constSize' if cs else 'scaled', 'min surface gap', g13(worst_gap), 'at', worst_pair,
      '| nearest tie |frac-0.5|', g13(tie), 'at', tie_pair, '| max nmin', nmax)
for (m1, m2, cs) in [(100, 400, False), (1000, 1000, False), (10, 10, False), (100, 400, True),
                     (1000, 400, False), (100, 1000, False), (1000, 1000, True),
                     (200, 200, False), (500, 500, False), (140, 940, False)]:
    P('nmin', m1, m2, 'cs' if cs else 'sc', nmin(m1, m2, cs),
      'sum/q', repr((radius(m1, cs) + radius(m2, cs) + SEP) / Q))

P('\n# the push rule: k = the object whose radius changed last')
def settle(i1, i2, n, k):
    if i2 - i1 >= n:
        return i1, i2
    if k == 1:
        if i2 < IR:
            i2 = min(i1 + n, IR)
        if i2 - i1 < n:
            i1 = i2 - n
    else:
        if i1 > IL:
            i1 = max(i2 - n, IL)
        if i2 - i1 < n:
            i2 = i1 + n
    return i1, i2
SCEN = [('a default, m1 -> 1000', -30, 10, 1000, 400, False, 1),
        ('b m2 -> 1000 at 1.5 m', -30, -15, 100, 1000, False, 2),
        ('c m1 on the left wall, m2 -> 1000', -50, -35, 100, 1000, False, 2),
        ('d m2 on the right wall, m1 -> 1000', 35, 50, 1000, 400, False, 1),
        ('e constant size off, 1000/1000 at 1.1 m', -6, 5, 1000, 1000, False, 2)]
for (nm, i1, i2, m1, m2, cs, k) in SCEN:
    n = nmin(m1, m2, cs)
    P('settle', nm, '-> n', n, '->', settle(i1, i2, n, k))

P('\n# forces')
Fdef = force(100, 400, 4.0)
P('F default (100, 400, 4 m)', g13(Fdef))
P('F min (10, 10, 10 m)', g13(force(10, 10, 10.0)))
P('F max scaled (1000, 1000, n=%d)' % nmin(1000, 1000, False), g13(force(1000, 1000, nmin(1000, 1000, False) * Q)))
P('F max constant (1000, 1000, n=%d)' % nmin(1000, 1000, True), g13(force(1000, 1000, nmin(1000, 1000, True) * Q)))
P('F default with PhET G', g13(G_PHET * 100 * 400 / 16))

def dec_group(x, places):
    s = '%.*f' % (places, x)
    i = s.index('.')
    out = s[:i + 4]
    j = i + 4
    while j < len(s):
        out += ' ' + s[j:j + 3]
        j += 3
    return out
def sci(x):
    s = '%.2e' % x
    man, ex = s.split('e')
    return man + ' x 10^' + str(int(ex))
for nm, F in [('default', Fdef), ('min', force(10, 10, 10.0)), ('max scaled', force(1000, 1000, 2.4)), ('7 m', force(100, 400, 7.0))]:
    P('decimal12', nm, repr(dec_group(F, 12)), '| sci', sci(F))

P('\n# the inverse square: F r^2 = G m1 m2 at the default masses')
P('G m1 m2', g13(G * 100 * 400))
for r in (1.5, 2.0, 4.0, 8.0, 10.0):
    P('F(r)', r, g13(force(100, 400, r)))

P('\n# the strongest pull two equal masses can reach')
for m in (10, 100, 500, 1000):
    for cs in (False, True):
        n = nmin(m, m, cs)
        P('Fmax', m, 'cs' if cs else 'sc', 'n', n, g13(force(m, m, n * Q)))
F10, F1000 = force(10, 10, nmin(10, 10, False) * Q), force(1000, 1000, nmin(1000, 1000, False) * Q)
P('scaled log-slope 10 -> 1000 kg', g13(math.log10(F1000 / F10) / 2))
F10c, F1000c = force(10, 10, 1.1), force(1000, 1000, 1.1)
P('constant log-slope 10 -> 1000 kg', g13(math.log10(F1000c / F10c) / 2))
# touching spheres (no gap, no snap): F = G m^2 / (2 r(m))^2 = G m^(4/3) (4 pi rho / 3)^(2/3) / 4
m = 1000.0
P('touching 1000 kg spheres', g13(force(m, m, 2 * radius(m, False))),
  '= G m^(4/3) (4 pi rho/3)^(2/3)/4 =', g13(G * m ** (4 / 3) * (4 * math.pi * RHO / 3) ** (2 / 3) / 4))

P('\n# let them go: radial two-body free fall from rest')
def fall_time(r, r0, GM):
    x = r / r0
    u = (r0 - r) / r0
    return math.sqrt(r0 ** 3 / (2 * GM)) * (math.sqrt(x * u) + math.asin(math.sqrt(u)))
def fall_case(m1, m2, x1, x2, cs, tag):
    M = m1 + m2
    GM = G * M
    r0 = x2 - x1
    rc = radius(m1, cs) + radius(m2, cs)
    tau = math.sqrt(r0 ** 3 / (2 * GM))
    tc = fall_time(rc, r0, GM)
    tff = math.pi / 2 * tau
    P(tag, 'r0', g13(r0), 'r_contact', g13(rc), 'tau', g13(tau), 't_contact', g13(tc), 't_ff (to r=0)', g13(tff))
    vrel = math.sqrt(2 * GM * (1 / rc - 1 / r0))
    P(tag, 'v_rel at contact', g13(vrel), 'v1', g13(m2 / M * vrel), 'v2', g13(-m1 / M * vrel),
      'p1', g13(m1 * m2 / M * vrel))
    xcm = (m1 * x1 + m2 * x2) / M
    P(tag, 'x_cm', g13(xcm))
    # the independent route: integrate both bodies, event at contact
    def rhs(t, y):
        d = y[1] - y[0]
        a = G / (d * d)
        return [y[2], y[3], a * m2, -a * m1]
    ev = lambda t, y: (y[1] - y[0]) - rc
    ev.terminal, ev.direction = True, -1
    sol = solve_ivp(rhs, [0, 2 * tc], [x1, x2, 0.0, 0.0], method='DOP853', rtol=1e-12, atol=1e-14,
                    events=ev, dense_output=True)
    te = sol.t_events[0][0]
    P(tag, 'CHECK solve_ivp contact time', g13(te), 'rel diff', '%.3g' % (te / tc - 1))
    for f in (0.25, 0.5, 0.75, 1.0):
        t = f * tc
        r_bq = rc if f == 1.0 else brentq(lambda r: fall_time(r, r0, GM) - t, rc, r0, xtol=1e-15, rtol=1e-15)
        y = sol.sol(min(t, te))
        P(tag, 'frame %d/600' % int(round(600 * f)), 't', g13(t), 'r (brentq)', g13(r_bq),
          'r (solve_ivp)', g13(y[1] - y[0]), 'x1', g13(y[0]), 'x2', g13(y[1]),
          'v1', g13(y[2]), 'v2', g13(y[3]), 'm1v1+m2v2', '%.3g' % (m1 * y[2] + m2 * y[3]))
    return tc
fall_case(100, 400, -3.0, 1.0, False, 'fall default')
fall_case(100, 400, -3.0, 1.0, True, 'fall constSize')
fall_case(1000, 10, -5.0, 5.0, False, 'fall 1000/10 at 10 m')

P('\n# the arrow scale: 1-2-5 steps; index k -> [1,2,5][k mod 3] * 10^(floor(k/3) + E0)')
def step(k, E0):
    return [1, 2, 5][k % 3] * 10.0 ** (k // 3 + E0)
for k, E0 in ((9, -10), (0, -10), (17, -10), (10, -10)):
    P('step', k, E0, g13(step(k, E0)))
P('inverse-cube comparison at the closest allowed distance (default): F r^3 / d_min', g13(Fdef * 4.0 ** 3 / 1.5))
def ladder(q, room, E0):
    k = 0
    while k < 60 and q / step(k, E0) > room:
        k += 1
    return step(k, E0)
Fc = force(100, 400, radius(100, False) + radius(400, False))
vc = math.sqrt(2 * G * 500 * (1 / (radius(100, False) + radius(400, False)) - 1 / 4.0)) * 400 / 500
P('fall arrow ladders: contact force', g13(Fc), '-> per', g13(ladder(Fc, 4.5, -12)),
  '| fastest speed', g13(vc), '-> per', g13(ladder(vc, 3, -9)))

P('\n# the mass-product view at the defaults and at r = 2.0, 1.5 m')
k4 = G / 16
lv = []
Flo, Fhi = k4 * 100, k4 * 1e6
for e in range(math.floor(math.log10(Flo)), math.ceil(math.log10(Fhi)) + 1):
    for c in (1, 2, 5):
        F = c * 10.0 ** e
        if Flo * 1.0001 < F < Fhi * 0.9999:
            lv.append(F)
P('k = G/r^2 at 4 m', g13(k4), '| levels', len(lv), 'first', g13(lv[0]), 'last', g13(lv[-1]))
for steps_ in (20, 15):
    nb = 0
    edge10 = None
    for m1 in MASSES:
        e = None
        for m2 in MASSES:
            if nmin(m1, m2, False) > steps_:
                e = m2
                break
        if e is not None:
            nb += (1000 - e) // 10 + 1
        if m1 == 1000:
            edge10 = e
    P('blocked pairs at r = %.1f m (scaled):' % (steps_ / 10), nb, '| lightest blocked m2 for m1 = 1000:', edge10)
P('weight equivalent of the default force, micrograms', g13(Fdef / 9.80665 * 1e9))
