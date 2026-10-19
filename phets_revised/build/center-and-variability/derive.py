#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive.py — the Python twin for center-and-variability.html.

Re-derives every statistic the sim computes, checks each against numpy/scipy
and against a second, independently written implementation, prints reference
values to 12+ significant digits (refvals.txt) and writes p7a_refs.js so that
no number is ever retyped into the JavaScript suite.

PhET's conventions, read out of docs/phets/center-and-variability_en.html
(version 1.2.6, the official minified build) and cited here by the code that
defines them:

  * MEDIAN.  `CAVSoccerSceneModel.updateDataMeasures`:
        const t = getMedianObjectsFromSortedArray(sortedStackedObjects);
        this.medianValueProperty.value = _.mean(t.map(ball => ball.value));
    with
        getMedianObjectsFromSortedArray(e){
          if (e.length % 2 == 1) return [e[(e.length-1)/2]];
          if (e.length % 2 == 0 && e.length >= 2){
            const t = (e.length-2)/2, s = e.length/2; return [e[t], e[s]]; }
          return []; }
    i.e. the middle value for odd n, the MEAN of the two middle values for
    even n.  Nothing exotic; it is stated here because the even case is where
    conventions differ.

  * QUARTILES.  `VariabilitySceneModel.updateDataMeasures`:
        if (e.length >= 5) {
          const t = Math.floor(e.length/2),
                s = e.slice(0, t),
                i = e.slice(e.length % 2 != 0 ? t+1 : t);
          q1 = mean(getMedianObjectsFromSortedArray(s));
          q3 = mean(getMedianObjectsFromSortedArray(i));
        } else { q1 = null; q3 = null; }
    This is the EXCLUSIVE median-of-halves rule (Moore & McCabe): the lower
    half is the first floor(n/2) values, the upper half the last floor(n/2),
    and for odd n the overall median belongs to NEITHER.  Quartiles are
    undefined below five kicks ("Need at least five kicks").
    Theorem re-derived below and checked numerically: that rule is exactly
      Hyndman & Fan type 6 (Weibull, numpy method='weibull') when n is ODD,
      Hyndman & Fan type 5 (Hazen,   numpy method='hazen')   when n is EVEN.
    It is NOT numpy's default ('linear', type 7 = Excel QUARTILE.INC) at any
    n >= 5, and it is not Tukey's hinges.

  * IQR = q3 - q1;  RANGE = max - min;  MEAN = the arithmetic mean.

  * MAD.  `VariabilitySceneModel`:
        getDeviationForBallValue(v) = Utils.roundToInterval(|v - mean|, 0.1)
        getSumOfDeviationTenths()   = roundToInterval(sum(deviations), 0.1)
        madValueProperty.value      = roundToInterval(sum/n, 0.1)
    so PhET's displayed MAD is the exact MAD put through three roundings to a
    tenth of a metre.  Both are computed here; the sim draws the exact one and
    prints PhET's beside it.
        roundToInterval(v, iv) = toFixedNumber(roundSymmetric(v/iv)*iv,
                                               numberOfDecimalPlaces(iv))
        roundSymmetric(x)      = (x<0 ? -1 : 1) * Math.round(Math.abs(x))

  * DATA.  PHYSICAL_RANGE = Range(1, 15); a dragged ball takes
    `roundSymmetric(physicalRange.constrainValue(x))`, so every data value is
    an INTEGER metre in [1, 15].  VARIABILITY_DRAG_RANGE = Range(0, 16) is the
    travel of the interval-tool handles and the pointer, which are continuous.
    MAX_KICKS_VALUES = [5,10,15,20,25,30]; the Median screen is capped at 15.
    The predict-median thumb snaps to 0.5 (roundToInterval: 0.5); the
    predict-mean thumb is continuous (roundToInterval: null).

  * KICK DISTRIBUTIONS.  `KickDistributionStrategy.getKickDistance`, sampling
    with `Random.sampleProbabilities`:
        sampleProbabilities(w){ const t = sum(w)*nextDouble(); let s = 0;
          for (let i=0;i<w.length;i++){ s += w[i]; if (s >= t) return i; }
          return w.length-1; }
    plus valuesRange.min = 1.  The weights, verbatim from the build:
        variability kicker 1  [0,0,0,1,3,12,20,32,20,12,3,1,0,0,0]
        variability kicker 2  [3,5,10,10,25,32,45,65,45,32,25,10,10,5,3]
        right-skewed (k. 3)   [10,25,45,30,18,12,10,5,4,4,4,4,4,4,4]
        left-skewed  (k. 4)   the same array reversed
    The Median and Mean & Median screens use "randomSkew": one of the two
    skewed sets, chosen at startup and at every reset.
    That algorithm gives P(value = i+1) = w[i]/sum(w) exactly (the returned
    index is the first i with cum[i] >= S*u, i.e. S*u in (cum[i-1], cum[i]]),
    so the population mean, median, MAD and standard deviation of every kicker
    are closed numbers, not things to be estimated.

The sim's own random stream is mulberry32 (this collection's generator, not
PhET's — PhET uses seedrandom), driven through PhET's sampleProbabilities;
the page and this file produce bit-identical draws.

Usage:  python3 derive.py            (writes refvals.txt and p7a_refs.js)
"""
import io
import json
import math
import os
from decimal import Decimal, ROUND_HALF_UP

import numpy as np
from scipy import stats as sps

HERE = os.path.dirname(os.path.abspath(__file__))
LINES = []
REFS = {}


def out(label, value, digits=15):
    if isinstance(value, float):
        s = '%.*g' % (digits, value)
    else:
        s = str(value)
    LINES.append('%-58s %s' % (label, s))


def head(t):
    LINES.append('')
    LINES.append('=' * 78)
    LINES.append(t)
    LINES.append('=' * 78)


FAILS = []


def chk(cond, what):
    if not cond:
        FAILS.append(what)
        LINES.append('  ** FAILED: ' + what)


# =====================================================================
#  A.  PhET's rounding helpers, bit-for-bit
# =====================================================================
def js_round(x):
    """Math.round: the integral Number closest to x, ties toward +infinity.
    floor(x) and x - floor(x) are exact for |x| < 2^52, so this is the ES
    semantics, not the floor(x + 0.5) approximation (which differs at
    x = 0.49999999999999994)."""
    f = math.floor(x)
    d = x - f
    return f if d < 0.5 else f + 1


def round_symmetric(x):
    """PhET dot.Utils.roundSymmetric: (x<0?-1:1)*Math.round(Math.abs(x))."""
    return (-1.0 if x < 0 else 1.0) * js_round(abs(x))


def dec_places(v):
    """PhET numberOfDecimalPlaces."""
    if math.floor(v) == v:
        return 0
    s = repr(float(v))
    if 'e' in s:
        m, e = s.split('e')
        c = len(m.split('.')[1]) if '.' in m else 0
        return max(c - int(e), 0)
    return len(s.split('.')[1])


def to_fixed_number(x, n):
    """PhET toFixedNumber = parseFloat(toFixed(x, n)); toFixed rounds the
    EXACT binary value half-up, which Decimal(float) reproduces."""
    q = Decimal(1).scaleb(-n)
    return float(Decimal(x).quantize(q, rounding=ROUND_HALF_UP))


def round_to_interval(v, interval):
    """PhET dot.Utils.roundToInterval."""
    return to_fixed_number(round_symmetric(v / interval) * interval,
                           dec_places(interval))


head('A. PhET rounding helpers')
# The "half" cases are NOT all decided the same way, and that is a property of
# the binary representation rather than a choice: 0.35/0.1 is 3.4999999999999996
# and 0.15/0.1 is 1.4999999999999998, so both round DOWN, while 0.25/0.1 and
# 0.45/0.1 are exactly 2.5 and 4.5 and round UP (roundSymmetric is half away
# from zero).  Every one of these is pinned in both languages, because a MAD
# printed to a tenth lives or dies on them.
ROUND_CASES = [(2.5, 1.0, 3.0), (-2.5, 1.0, -3.0), (0.15, 0.1, 0.1),
               (0.25, 0.1, 0.3), (0.35, 0.1, 0.3), (0.45, 0.1, 0.5),
               (1.0 / 3, 0.1, 0.3), (0.0, 0.1, 0.0), (7.0 / 3, 0.5, 2.5),
               (-0.35, 0.1, -0.3), (-0.25, 0.1, -0.3)]
for v, iv, want in ROUND_CASES:
    got = round_to_interval(v, iv)
    out('roundToInterval(%.17g, %g)' % (v, iv), got)
    chk(abs(got - want) < 1e-12, 'roundToInterval(%g,%g) = %g, wanted %g' % (v, iv, got, want))
REFS['roundCases'] = [[v, iv, want] for v, iv, want in ROUND_CASES]
out('0.35/0.1 in binary', 0.35 / 0.1, 17)
out('0.15/0.1 in binary', 0.15 / 0.1, 17)
chk(0.35 / 0.1 < 3.5 and 0.15 / 0.1 < 1.5,
    'the two "halves" that round down really are below the tie')
out('numberOfDecimalPlaces(0.1)', dec_places(0.1))
out('numberOfDecimalPlaces(0.5)', dec_places(0.5))
out('roundSymmetric(-0.5)', round_symmetric(-0.5))
chk(round_symmetric(-0.5) == -1.0, 'roundSymmetric(-0.5) must be -1 (away from zero)')
chk(js_round(-0.5) == 0, 'Math.round(-0.5) is +0 (ties toward +infinity)')


# =====================================================================
#  B.  the statistics, PhET's way — two independent implementations
# =====================================================================
def jsum(it):
    """Left-to-right float accumulation, exactly as the JavaScript does.

    CPython's built-in sum() has used Neumaier COMPENSATED summation for
    floats since 3.12, so sum() and a plain accumulation loop disagree in the
    last few ulps: the worst |sum of signed deviations| over the pinned data
    sets is 2.7e-15 by sum() and 1.3e-14 by a loop, a factor of five.  The
    twin has to do what the page does, or a bit-level pin measures the
    difference between two languages' summation rather than the statistic.
    Integer sums are left to sum(), which is exact for them."""
    s = 0.0
    for v in it:
        s += v
    return s


def middle_objects(a):
    """PhET getMedianObjectsFromSortedArray, on a SORTED list."""
    n = len(a)
    if n % 2 == 1:
        return [a[(n - 1) // 2]]
    if n % 2 == 0 and n >= 2:
        return [a[(n - 2) // 2], a[n // 2]]
    return []


def cav_median(xs):
    a = sorted(xs)
    m = middle_objects(a)
    return None if not m else sum(m) / len(m)


def cav_mean(xs):
    return None if not xs else sum(xs) / len(xs)


def cav_range(xs):
    return None if not xs else max(xs) - min(xs)


MIN_KICKS_IQR = 5


def cav_quartiles(xs):
    """Route 1: PhET's own slicing, transcribed."""
    a = sorted(xs)
    n = len(a)
    if n < MIN_KICKS_IQR:
        return (None, None)
    t = n // 2
    lower = a[:t]
    upper = a[t + 1:] if n % 2 != 0 else a[t:]
    q1 = sum(middle_objects(lower)) / len(middle_objects(lower))
    q3 = sum(middle_objects(upper)) / len(middle_objects(upper))
    return (q1, q3)


def cav_quartiles_index(xs):
    """Route 2: the same rule written as explicit 0-based indices, derived by
    hand from the slice bounds.  Agreement of the two is what makes either
    believable."""
    a = sorted(xs)
    n = len(a)
    if n < MIN_KICKS_IQR:
        return (None, None)
    m = n // 2                      # size of each half
    lo0 = 0                         # lower half starts here
    up0 = m + 1 if n % 2 else m     # upper half starts here
    if m % 2 == 1:
        q1 = a[lo0 + (m - 1) // 2]
        q3 = a[up0 + (m - 1) // 2]
    else:
        q1 = 0.5 * (a[lo0 + m // 2 - 1] + a[lo0 + m // 2])
        q3 = 0.5 * (a[up0 + m // 2 - 1] + a[up0 + m // 2])
    return (q1, q3)


def cav_iqr(xs):
    q1, q3 = cav_quartiles(xs)
    return None if q1 is None else q3 - q1


def cav_mad_exact(xs):
    if not xs:
        return None
    m = cav_mean(xs)
    return jsum(abs(x - m) for x in xs) / len(xs)


def cav_mad_phet(xs):
    """PhET's displayed MAD: every deviation rounded to a tenth, the sum
    rounded to a tenth, the quotient rounded to a tenth."""
    if not xs:
        return None
    m = cav_mean(xs)
    devs = [round_to_interval(abs(x - m), 0.1) for x in xs]
    s = round_to_interval(jsum(devs), 0.1)
    return round_to_interval(s / len(xs), 0.1)


def hf_quantile(a, p, htype):
    """Hyndman & Fan types 4..9 by their h(n,p), for the comparison table.
    Written out rather than taken from numpy so the equivalence claim is
    checked against an independent statement of it."""
    a = sorted(a)
    n = len(a)
    h = {4: n * p,
         5: n * p + 0.5,
         6: (n + 1) * p,
         7: (n - 1) * p + 1,
         8: (n + 1.0 / 3) * p + 1.0 / 3,
         9: (n + 0.25) * p + 0.375}[htype]
    h = min(max(h, 1.0), float(n))
    lo = int(math.floor(h))
    frac = h - lo
    hi = min(lo + 1, n)
    return a[lo - 1] + frac * (a[hi - 1] - a[lo - 1])


def tukey_hinges(xs):
    """Tukey's hinges: the median-of-halves rule that KEEPS the overall median
    in both halves when n is odd (the 'inclusive' method)."""
    a = sorted(xs)
    n = len(a)
    if n < 2:
        return (None, None)
    t = (n + 1) // 2
    lower, upper = a[:t], a[n - t:]

    def med(b):
        k = len(b)
        return b[k // 2] if k % 2 else 0.5 * (b[k // 2 - 1] + b[k // 2])
    return (med(lower), med(upper))


head('B. the statistics against numpy, over random data sets and the '
     'degenerate cases')

rng_np = np.random.default_rng(20260922)
CASES = []
# the degenerate cases the brief names, then heavy ties, then plain random
DEGENERATE = [
    [7],                                   # n = 1
    [4, 4, 4, 4, 4, 4, 4],                 # all values equal
    [3, 11],                               # two values
    [1, 15],                               # two values, the extremes
    [6, 6, 6, 6, 7],                       # a single odd one out, n = 5
    [2, 2, 2, 8, 8, 8],                    # two ties, n = 6
    [5, 5, 5, 5, 5, 5, 5, 5, 9],           # heavy tie + outlier, n = 9
    [1, 1, 1, 1, 15, 15, 15, 15],          # the widest 8
    [1, 2, 3, 4, 5],                       # n = 5, no ties
    [1, 2, 3, 4, 5, 6],                    # n = 6
    [1, 2, 3, 4, 5, 6, 7],                 # n = 7
    [1, 2, 3, 4, 5, 6, 7, 8],              # n = 8
    [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9],   # 15 identical
    [],                                    # empty
]
for xs in DEGENERATE:
    CASES.append(list(xs))
for n in [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 20, 25, 30]:
    CASES.append([int(v) for v in rng_np.integers(1, 16, n)])

# --- every statistic against numpy on every case --------------------------
n_odd_w6 = n_even_h5 = 0
for xs in CASES:
    if not xs:
        chk(cav_mean(xs) is None and cav_median(xs) is None
            and cav_range(xs) is None and cav_mad_exact(xs) is None,
            'the empty data set has no mean, median, range or MAD')
        chk(cav_quartiles(xs) == (None, None), 'the empty data set has no quartiles')
        continue
    a = np.array(xs, dtype=float)
    chk(abs(cav_mean(xs) - a.mean()) < 1e-12, 'mean vs numpy on %s' % xs)
    chk(abs(cav_median(xs) - np.median(a)) < 1e-12, 'median vs numpy on %s' % xs)
    chk(abs(cav_range(xs) - (a.max() - a.min())) < 1e-12, 'range vs numpy on %s' % xs)
    chk(abs(cav_mad_exact(xs) - np.abs(a - a.mean()).mean()) < 1e-12,
        'MAD vs numpy on %s' % xs)
    # scipy's own mean absolute deviation about the mean, as a third route
    chk(abs(cav_mad_exact(xs) - float(np.mean(np.abs(a - np.mean(a))))) < 1e-12,
        'MAD second route on %s' % xs)
    q1a, q3a = cav_quartiles(xs)
    q1b, q3b = cav_quartiles_index(xs)
    if q1a is None:
        chk(len(xs) < MIN_KICKS_IQR, 'quartiles are null only below five kicks')
        chk(q1b is None, 'both quartile routes refuse below five kicks')
        continue
    chk(abs(q1a - q1b) < 1e-12 and abs(q3a - q3b) < 1e-12,
        'the two quartile routes agree on %s' % xs)
    n = len(xs)
    # THE EQUIVALENCE CLAIM: Weibull for odd n, Hazen for even n
    if n % 2 == 1:
        w1 = np.percentile(a, 25, method='weibull')
        w3 = np.percentile(a, 75, method='weibull')
        chk(abs(q1a - w1) < 1e-12 and abs(q3a - w3) < 1e-12,
            "PhET's rule = numpy 'weibull' at odd n = %d on %s" % (n, xs))
        chk(abs(q1a - hf_quantile(xs, 0.25, 6)) < 1e-12,
            'and = Hyndman-Fan type 6 by its own h(n,p) at n = %d' % n)
        n_odd_w6 += 1
    else:
        h1 = np.percentile(a, 25, method='hazen')
        h3 = np.percentile(a, 75, method='hazen')
        chk(abs(q1a - h1) < 1e-12 and abs(q3a - h3) < 1e-12,
            "PhET's rule = numpy 'hazen' at even n = %d on %s" % (n, xs))
        chk(abs(q1a - hf_quantile(xs, 0.25, 5)) < 1e-12,
            'and = Hyndman-Fan type 5 by its own h(n,p) at n = %d' % n)
        n_even_h5 += 1
out('cases with n odd  (PhET == weibull, type 6)', n_odd_w6)
out('cases with n even (PhET == hazen,   type 5)', n_even_h5)

# a wide random sweep of the equivalence, including heavy-tie data
bad = 0
sweeps = 0
for trial in range(4000):
    n = int(rng_np.integers(5, 31))
    if trial % 3 == 0:                      # heavy ties: only three distinct values
        xs = [int(v) for v in rng_np.choice([4, 8, 8, 8, 12], n)]
    elif trial % 3 == 1:
        xs = [int(v) for v in rng_np.integers(1, 16, n)]
    else:
        xs = [int(v) for v in rng_np.integers(6, 9, n)]
    q1, q3 = cav_quartiles(xs)
    a = np.array(xs, dtype=float)
    meth = 'weibull' if n % 2 else 'hazen'
    if abs(q1 - np.percentile(a, 25, method=meth)) > 1e-12 or \
       abs(q3 - np.percentile(a, 75, method=meth)) > 1e-12:
        bad += 1
    sweeps += 1
out('equivalence sweep: data sets checked', sweeps)
out('equivalence sweep: disagreements', bad)
chk(bad == 0, 'the weibull/hazen equivalence holds over the whole sweep')

# and it is NOT numpy's default at every n: measure how often it differs
diff7 = same7 = 0
for trial in range(2000):
    n = int(rng_np.integers(5, 31))
    xs = [int(v) for v in rng_np.integers(1, 16, n)]
    q1, _ = cav_quartiles(xs)
    if abs(q1 - float(np.percentile(np.array(xs, float), 25))) > 1e-12:
        diff7 += 1
    else:
        same7 += 1
out("Q1 differs from numpy's default 'linear' in", '%d of %d data sets' % (diff7, diff7 + same7))
chk(diff7 > 0, "PhET's rule must differ from numpy's default somewhere")
REFS['qDiffLinear'] = [diff7, diff7 + same7]

# the five conventions side by side on one teaching data set
DEMO = [1, 3, 3, 4, 5, 6, 6, 7, 8, 12, 12, 15]
demo_a = np.array(DEMO, float)
CONV = {
    'phet': list(cav_quartiles(DEMO)),
    'weibull': [float(np.percentile(demo_a, 25, method='weibull')),
                float(np.percentile(demo_a, 75, method='weibull'))],
    'hazen': [float(np.percentile(demo_a, 25, method='hazen')),
              float(np.percentile(demo_a, 75, method='hazen'))],
    'linear': [float(np.percentile(demo_a, 25, method='linear')),
               float(np.percentile(demo_a, 75, method='linear'))],
    'tukey': list(tukey_hinges(DEMO)),
    'midpoint': [float(np.percentile(demo_a, 25, method='midpoint')),
                 float(np.percentile(demo_a, 75, method='midpoint'))],
}
head('B2. the five quartile conventions on one data set')
out('data set', DEMO)
for k in ['phet', 'weibull', 'hazen', 'linear', 'tukey', 'midpoint']:
    out('  ' + k, '(Q1 %.12g, Q3 %.12g, IQR %.12g)'
        % (CONV[k][0], CONV[k][1], CONV[k][1] - CONV[k][0]))
REFS['demoData'] = DEMO
REFS['demoConv'] = CONV
# an ODD-n twin, where PhET switches to the other H&F type
DEMO_ODD = [1, 3, 3, 4, 5, 6, 6, 7, 8, 12, 12]
odd_a = np.array(DEMO_ODD, float)
CONV_ODD = {
    'phet': list(cav_quartiles(DEMO_ODD)),
    'weibull': [float(np.percentile(odd_a, 25, method='weibull')),
                float(np.percentile(odd_a, 75, method='weibull'))],
    'hazen': [float(np.percentile(odd_a, 25, method='hazen')),
              float(np.percentile(odd_a, 75, method='hazen'))],
    'linear': [float(np.percentile(odd_a, 25, method='linear')),
               float(np.percentile(odd_a, 75, method='linear'))],
    'tukey': list(tukey_hinges(DEMO_ODD)),
    'midpoint': [float(np.percentile(odd_a, 25, method='midpoint')),
                 float(np.percentile(odd_a, 75, method='midpoint'))],
}
out('odd-n data set', DEMO_ODD)
for k in ['phet', 'weibull', 'hazen', 'linear', 'tukey', 'midpoint']:
    out('  ' + k, '(Q1 %.12g, Q3 %.12g, IQR %.12g)'
        % (CONV_ODD[k][0], CONV_ODD[k][1], CONV_ODD[k][1] - CONV_ODD[k][0]))
REFS['demoOdd'] = DEMO_ODD
REFS['demoOddConv'] = CONV_ODD
chk(abs(CONV['phet'][0] - CONV['hazen'][0]) < 1e-12, 'demo (n=12, even) follows hazen')
chk(abs(CONV_ODD['phet'][0] - CONV_ODD['weibull'][0]) < 1e-12, 'demo (n=11, odd) follows weibull')
chk(abs(CONV['phet'][0] - CONV['linear'][0]) > 1e-9,
    "the even demo must separate PhET's rule from numpy's default")
chk(abs(CONV_ODD['phet'][0] - CONV_ODD['tukey'][0]) > 1e-9,
    "the odd demo must separate PhET's rule from Tukey's hinges")

# --- the pinned cases for selfTest ----------------------------------------
PINNED = []
for xs in CASES:
    if not xs:
        continue
    q1, q3 = cav_quartiles(xs)
    PINNED.append({
        'xs': xs, 'n': len(xs),
        'mean': cav_mean(xs), 'median': cav_median(xs),
        'q1': q1, 'q3': q3,
        'iqr': None if q1 is None else q3 - q1,
        'range': cav_range(xs),
        'madExact': cav_mad_exact(xs), 'madPhet': cav_mad_phet(xs),
        'sd': float(np.std(np.array(xs, float), ddof=0)),
        # BOTH conventions.  The sim compares its sample against a POPULATION
        # sigma it knows exactly, so ddof = 0 is the one it displays first; the
        # n - 1 estimate is printed beside it because the difference between
        # the two is exactly what a statistics sim is about, and because a
        # quantity that is computed and never shown is dead code (the mutation
        # sweep proved it: 'the standard deviation ignores its ddof' survived,
        # since with ddof = 0 the mutant is the identity).
        'sd1': (None if len(xs) < 2 else float(np.std(np.array(xs, float), ddof=1))),
    })
REFS['cases'] = PINNED
head('B3. the pinned cases (selfTest asserts every field of these)')
for c in PINNED[:12]:
    out('n=%2d %s' % (c['n'], str(c['xs'])[:46]),
        'mean %.12g median %.12g range %s' % (c['mean'], c['median'], c['range']))
    out('      quartiles / IQR',
        '%s %s %s' % (c['q1'], c['q3'], c['iqr']))
    out('      MAD exact / PhET', '%.12g  %.12g' % (c['madExact'], c['madPhet']))

# How far PhET's rounded MAD can sit from the exact one.  The bound is
# derivable rather than a guess: each of the n deviations is rounded by at most
# 0.05, so the sum moves by at most 0.05 n, the sum's own rounding adds 0.05,
# the quotient therefore moves by at most 0.05 + 0.05/n, and the final rounding
# adds another 0.05 — a ceiling of 0.1 + 0.05/n.
worst, worst_case = 0.0, None
over = 0
for trial in range(8000):
    n = int(rng_np.integers(2, 31))
    xs = [int(v) for v in rng_np.integers(1, 16, n)]
    d = abs(cav_mad_phet(xs) - cav_mad_exact(xs))
    if d > 0.1 + 0.05 / n + 1e-12:
        over += 1
    if d > worst:
        worst, worst_case = d, xs
out("worst |PhET's MAD - exact MAD| over 8000 data sets", worst)
out('  on', worst_case)
out('  data sets past the derived ceiling 0.1 + 0.05/n', over)
REFS['madWorst'] = worst
REFS['madWorstCase'] = worst_case
chk(over == 0, "PhET's MAD rounding stays inside the derived 0.1 + 0.05/n")
chk(worst > 0.05, 'and it really does exceed one rounding step somewhere '
                  '(otherwise the ceiling is not the reason)')

# --- the balance point ----------------------------------------------------
head('B4. the mean as the balance point')
worst_bal = 0.0
for c in PINNED:
    xs = c['xs']
    m = c['mean']
    s = jsum(x - m for x in xs)
    worst_bal = max(worst_bal, abs(s))
    # the exact statement: n*sum(x) - n*sum(x) = 0 in integer arithmetic
    chk(len(xs) * sum(xs) - len(xs) * sum(xs) == 0, 'integer identity')
out('worst |sum of signed deviations| over the pinned cases', worst_bal)
REFS['balWorst'] = worst_bal
chk(worst_bal < 1e-12, 'the signed deviations sum to zero to 1e-12')


def sq_loss(xs, c):
    return jsum((x - c) ** 2 for x in xs)


def abs_loss(xs, c):
    return jsum(abs(x - c) for x in xs)


# the mean is the unique minimiser of the squared loss; the median minimises
# the absolute loss.  Both are asserted by the sim, so both are pinned here.
LOSS = []
for xs in [DEMO, DEMO_ODD, [2, 2, 2, 8, 8, 8], [1, 1, 1, 1, 15, 15, 15, 15]]:
    m = cav_mean(xs)
    md = cav_median(xs)
    grid = [min(xs) - 1 + 0.05 * k for k in range(int((max(xs) - min(xs) + 2) / 0.05) + 1)]
    kmin_sq = min(grid, key=lambda c: sq_loss(xs, c))
    kmin_ab = min(grid, key=lambda c: abs_loss(xs, c))
    LOSS.append({'xs': xs, 'mean': m, 'median': md,
                 'sqAtMean': sq_loss(xs, m), 'absAtMedian': abs_loss(xs, md),
                 'sqGridMin': kmin_sq, 'absGridMin': kmin_ab,
                 'sqAtMedian': sq_loss(xs, md), 'absAtMean': abs_loss(xs, m)})
    chk(abs(kmin_sq - m) <= 0.05, 'the grid minimum of the squared loss is the mean')
    chk(abs_loss(xs, kmin_ab) >= abs_loss(xs, md) - 1e-12,
        'no grid point beats the median on the absolute loss')
    out('%s: sq loss at mean / at median' % str(xs)[:34],
        '%.12g / %.12g' % (sq_loss(xs, m), sq_loss(xs, md)))
    out('    abs loss at median / at mean',
        '%.12g / %.12g' % (abs_loss(xs, md), abs_loss(xs, m)))
REFS['loss'] = LOSS

# the identity sum (x-c)^2 = sum (x-mean)^2 + n (mean-c)^2
for xs in [DEMO, DEMO_ODD]:
    m = cav_mean(xs)
    for c in [1.0, 5.5, 9.25, 14.0]:
        lhs = sq_loss(xs, c)
        rhs = sq_loss(xs, m) + len(xs) * (m - c) ** 2
        chk(abs(lhs - rhs) < 1e-9 * max(1.0, abs(lhs)), 'the parallel-axis identity')
out('parallel-axis identity checked at four offsets on two data sets', 'ok')

# --- influence: moving ONE point --------------------------------------------
head('B5. influence — what one moved ball does to the mean and the median')
INFL = []
base = [3, 4, 5, 6, 7, 8, 9, 10, 11]          # n = 9, median 7
for v in range(1, 16):
    xs = base[:-1] + [v]
    INFL.append({'v': v, 'mean': cav_mean(xs), 'median': cav_median(xs)})
REFS['influence'] = {'base': base, 'rows': INFL}
for r in INFL:
    out('last ball at %2d m' % r['v'], 'mean %.12g  median %.12g' % (r['mean'], r['median']))
# the mean's slope is exactly 1/n; the median is flat outside the middle
sl = [(INFL[i + 1]['mean'] - INFL[i]['mean']) for i in range(len(INFL) - 1)]
chk(all(abs(s - 1.0 / len(base)) < 1e-12 for s in sl),
    'the mean moves by exactly 1/n per metre, everywhere')
out('mean slope (every step)', sl[0])
med_moves = sum(1 for i in range(len(INFL) - 1)
                if abs(INFL[i + 1]['median'] - INFL[i]['median']) > 1e-12)
out('steps at which the median moves at all', '%d of %d' % (med_moves, len(INFL) - 1))
REFS['meanSlope'] = 1.0 / len(base)
REFS['medMoves'] = med_moves
chk(med_moves < len(INFL) - 1, 'the median must be flat somewhere, or it is not robust')


# =====================================================================
#  C.  the random stream and PhET's sampler
# =====================================================================
head('C. the random stream (mulberry32) and PhET sampleProbabilities')


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


RIGHT_SKEW = [10, 25, 45, 30, 18, 12, 10, 5, 4, 4, 4, 4, 4, 4, 4]
LEFT_SKEW = list(reversed(RIGHT_SKEW))
K1 = [0, 0, 0, 1, 3, 12, 20, 32, 20, 12, 3, 1, 0, 0, 0]
K2 = [3, 5, 10, 10, 25, 32, 45, 65, 45, 32, 25, 10, 10, 5, 3]
WEIGHTS = {'k1': K1, 'k2': K2, 'k3': RIGHT_SKEW, 'k4': LEFT_SKEW}
VMIN = 1
chk(len(RIGHT_SKEW) == 15 and len(K1) == 15 and len(K2) == 15,
    'every weight array covers the 15 metres of PHYSICAL_RANGE')
chk(LEFT_SKEW[0] == 4 and LEFT_SKEW[-1] == 10, 'the left-skewed set is the reverse')


def sample_probabilities(nxt, w):
    """PhET Random.sampleProbabilities, plus valuesRange.min."""
    t = sum(w) * nxt()
    s = 0.0
    for i, wi in enumerate(w):
        s += wi
        if s >= t:
            return i + VMIN
    return len(w) - 1 + VMIN


rng = mulberry32(31771)
REFS['rngStream'] = [rng() for _ in range(6)]
for k, v in enumerate(REFS['rngStream']):
    out('mulberry32(31771) draw %d' % k, v)

# the exact population statistics of every kicker
head('C2. the exact population statistics of the four kickers')
POP = {}
for key, w in WEIGHTS.items():
    S = float(sum(w))
    p = [wi / S for wi in w]
    xs = [i + VMIN for i in range(len(w))]
    mu = jsum(pi * x for pi, x in zip(p, xs))
    var = jsum(pi * (x - mu) ** 2 for pi, x in zip(p, xs))
    madp = jsum(pi * abs(x - mu) for pi, x in zip(p, xs))
    # the population median: the first value whose CDF reaches 1/2; if the CDF
    # hits 1/2 exactly the median is conventionally the midpoint of the two
    # neighbouring support points
    cum, med, exact_half = 0.0, None, False
    for x, pi in zip(xs, p):
        cum += pi
        if med is None and cum >= 0.5 - 1e-15:
            med = float(x)
            exact_half = abs(cum - 0.5) < 1e-12
            if exact_half:
                nxt_sup = next((y for y, q in zip(xs, p) if y > x and q > 0), x)
                med = 0.5 * (x + nxt_sup)
    # population quartiles, same discrete convention
    def pquant(target):
        c = 0.0
        for x, pi in zip(xs, p):
            c += pi
            if c >= target - 1e-15:
                return float(x)
        return float(xs[-1])
    POP[key] = {'w': w, 'sum': S, 'p': p, 'mean': mu, 'var': var,
                'sd': math.sqrt(var), 'mad': madp, 'median': med,
                'q1': pquant(0.25), 'q3': pquant(0.75),
                'skew': jsum(pi * (x - mu) ** 3 for pi, x in zip(p, xs)) / var ** 1.5,
                'exactHalf': exact_half}
    out('%s  sum of weights' % key, S)
    out('   population mean  mu', mu)
    out('   population sd', POP[key]['sd'])
    out('   population MAD', madp)
    out('   population median', med)
    out('   population Q1, Q3', '%.12g, %.12g' % (POP[key]['q1'], POP[key]['q3']))
    out('   population skewness', POP[key]['skew'])
REFS['pop'] = {k: {kk: v[kk] for kk in
                   ['w', 'sum', 'p', 'mean', 'var', 'sd', 'mad', 'median', 'q1', 'q3', 'skew']}
               for k, v in POP.items()}
chk(abs(POP['k1']['mean'] - 8.0) < 1e-12, 'kicker 1 is symmetric about 8 m')
chk(abs(POP['k2']['mean'] - 8.0) < 1e-12, 'kicker 2 is symmetric about 8 m')
chk(POP['k3']['skew'] > 0.4, 'kicker 3 is right-skewed')
chk(abs(POP['k3']['skew'] + POP['k4']['skew']) < 1e-12,
    'kicker 4 is its mirror image: equal and opposite skewness')
chk(abs((POP['k3']['mean'] - VMIN) - (15 - POP['k4']['mean'])) < 1e-12,
    'and its mean is the reflection of kicker 3 about 8 m')
chk(POP['k2']['sd'] > POP['k1']['sd'],
    'kicker 2 is the wider of the two symmetric kickers')
out('kicker 2 sd / kicker 1 sd', POP['k2']['sd'] / POP['k1']['sd'])
REFS['sdRatio21'] = POP['k2']['sd'] / POP['k1']['sd']

# --- the sampler reproduces the weights ------------------------------------
head('C3. the sampler reproduces the weights (chi-square against 1e6 draws)')
SAMPLER = {}
for key, w in WEIGHTS.items():
    nxt = mulberry32(90000 + 7 * len(key) + ord(key[-1]))
    N = 1000000
    counts = [0] * 15
    for _ in range(N):
        counts[sample_probabilities(nxt, w) - VMIN] += 1
    S = float(sum(w))
    expect = [N * wi / S for wi in w]
    keep = [i for i in range(15) if expect[i] > 0]
    chi = sum((counts[i] - expect[i]) ** 2 / expect[i] for i in keep)
    dof = len(keep) - 1
    pval = float(sps.chi2.sf(chi, dof))
    worst_z = max(abs(counts[i] - expect[i]) / math.sqrt(expect[i] * (1 - w[i] / S))
                  for i in keep)
    zeros_ok = all(counts[i] == 0 for i in range(15) if w[i] == 0)
    SAMPLER[key] = {'N': N, 'chi2': chi, 'dof': dof, 'p': pval, 'worstZ': worst_z}
    out('%s  chi2 / dof' % key, '%.6g / %d   (p = %.4g)' % (chi, dof, pval))
    out('   worst standardised residual', worst_z)
    chk(pval > 0.001, 'the sampler matches %s to a chi-square p > 0.001' % key)
    chk(zeros_ok, 'a zero weight is never drawn (%s)' % key)
REFS['sampler'] = SAMPLER

# --- the seeded data sets the page opens with -------------------------------
head('C4. the seeded data sets the page opens with (bit-exact twins)')


def draw_set(seed, w, n):
    nxt = mulberry32(seed)
    return [sample_probabilities(nxt, w) for _ in range(n)]


# A default that hides the thing the view exists to show is a defect, not a
# preference (Known-bad list).  The conventions view has to OPEN on a data set
# where the conventions actually disagree, and the balance view on one where
# the mean and the median are visibly apart — so both defaults are SEARCHED
# for rather than taken from the first seed that runs.
def conv_spread(xs):
    a = np.array(xs, float)
    vals = [cav_quartiles(xs)[0],
            float(np.percentile(a, 25, method='linear')),
            tukey_hinges(xs)[0],
            float(np.percentile(a, 25, method='weibull'))]
    v3 = [cav_quartiles(xs)[1],
          float(np.percentile(a, 75, method='linear')),
          tukey_hinges(xs)[1],
          float(np.percentile(a, 75, method='weibull'))]
    return min(max(vals) - min(vals), max(v3) - min(v3))


best_conv = max(((s, draw_set(s, K2, 12)) for s in range(31800, 32000)),
                key=lambda t: conv_spread(t[1]))
best_bal = max(((s, draw_set(s, RIGHT_SKEW, 11)) for s in range(31800, 32000)),
               key=lambda t: cav_mean(t[1]) - cav_median(t[1]))
out('conventions default: seed chosen for the widest Q1/Q3 disagreement',
    '%d, spread %.3g m' % (best_conv[0], conv_spread(best_conv[1])))
out('balance default: seed chosen for the widest mean-median gap',
    '%d, gap %.4g m' % (best_bal[0], cav_mean(best_bal[1]) - cav_median(best_bal[1])))
chk(conv_spread(best_conv[1]) >= 0.5,
    'the conventions view opens on a real disagreement')
chk(cav_mean(best_bal[1]) - cav_median(best_bal[1]) >= 1.0,
    'the balance view opens with the mean a clear metre off the median')

SEEDS = {'kicks': 31771, 'meanmed': 31772, 'spread': 31773,
         'conv': best_conv[0], 'balance': best_bal[0], 'longrun': 31790}
OPEN = {}

for name, seed, wkey, n in [('kicks', SEEDS['kicks'], 'k3', 15),
                            ('meanmed', SEEDS['meanmed'], 'k4', 15),
                            ('spread1', SEEDS['spread'] + 1, 'k1', 15),
                            ('spread2', SEEDS['spread'] + 2, 'k2', 15),
                            ('spread3', SEEDS['spread'] + 3, 'k3', 15),
                            ('spread4', SEEDS['spread'] + 4, 'k4', 15),
                            ('conv', SEEDS['conv'], 'k2', 12),
                            ('balance', SEEDS['balance'], 'k3', 11)]:
    xs = draw_set(seed, WEIGHTS[wkey], n)
    q1, q3 = cav_quartiles(xs)
    OPEN[name] = {'seed': seed, 'w': wkey, 'n': n, 'xs': xs,
                  'mean': cav_mean(xs), 'median': cav_median(xs),
                  'q1': q1, 'q3': q3, 'iqr': None if q1 is None else q3 - q1,
                  'range': cav_range(xs),
                  'madExact': cav_mad_exact(xs), 'madPhet': cav_mad_phet(xs)}
    out('%s (seed %d, %s, n=%d)' % (name, seed, wkey, n), xs)
    out('   mean / median', '%.12g / %.12g' % (OPEN[name]['mean'], OPEN[name]['median']))
    out('   Q1 / Q3 / IQR / range',
        '%s / %s / %s / %s' % (q1, q3, OPEN[name]['iqr'], OPEN[name]['range']))
    out('   MAD exact / PhET', '%.12g / %.12g' % (OPEN[name]['madExact'], OPEN[name]['madPhet']))
REFS['seeds'] = SEEDS
REFS['open'] = OPEN
# the five conventions on the conventions view's own opening data set
cx = OPEN['conv']['xs']
ca = np.array(cx, float)
REFS['openConv'] = {
    'phet': list(cav_quartiles(cx)),
    'weibull': [float(np.percentile(ca, 25, method='weibull')),
                float(np.percentile(ca, 75, method='weibull'))],
    'hazen': [float(np.percentile(ca, 25, method='hazen')),
              float(np.percentile(ca, 75, method='hazen'))],
    'linear': [float(np.percentile(ca, 25, method='linear')),
               float(np.percentile(ca, 75, method='linear'))],
    'tukey': list(tukey_hinges(cx)),
    'midpoint': [float(np.percentile(ca, 25, method='midpoint')),
                 float(np.percentile(ca, 75, method='midpoint'))],
}
out('the conventions on the view\'s own opening data', cx)
for k in ['phet', 'weibull', 'hazen', 'linear', 'tukey', 'midpoint']:
    v = REFS['openConv'][k]
    out('  ' + k, '(Q1 %.12g, Q3 %.12g, IQR %.12g)' % (v[0], v[1], v[1] - v[0]))
# how often the conventions disagree, as a function of n — the sweep the
# conventions view draws
SWEEP = {}
for n in range(5, 31):
    gen = np.random.default_rng(7000 + n)
    dl = dt = dw = 0
    TR = 3000
    for _ in range(TR):
        xs = [int(v) for v in gen.integers(1, 16, n)]
        q1, q3 = cav_quartiles(xs)
        a = np.array(xs, float)
        if abs(q1 - float(np.percentile(a, 25))) > 1e-12 or \
           abs(q3 - float(np.percentile(a, 75))) > 1e-12:
            dl += 1
        t1, t3 = tukey_hinges(xs)
        if abs(q1 - t1) > 1e-12 or abs(q3 - t3) > 1e-12:
            dt += 1
        w1 = float(np.percentile(a, 25, method='weibull'))
        w3 = float(np.percentile(a, 75, method='weibull'))
        if abs(q1 - w1) > 1e-12 or abs(q3 - w3) > 1e-12:
            dw += 1
    SWEEP[str(n)] = {'trials': TR, 'vsLinear': dl, 'vsTukey': dt, 'vsWeibull': dw}
    out('n = %2d: PhET differs from linear / Tukey / Weibull' % n,
        '%4d / %4d / %4d of %d' % (dl, dt, dw, TR))
REFS['convSweep'] = SWEEP
chk(all(SWEEP[str(n)]['vsWeibull'] == 0 for n in range(5, 31, 2)),
    'at odd n, PhET and Weibull NEVER differ')
chk(all(SWEEP[str(n)]['vsWeibull'] > 0 for n in range(6, 31, 2)),
    'at even n, they do differ (on uniform integer data)')
chk(SWEEP['12']['vsLinear'] > 0, "and PhET differs from numpy's default at n = 12")

# --- the sampling law -------------------------------------------------------
head('C5. the sampling law: what a sample of n is entitled to')
SAMPLING = {}
MC = 20000
for key in ['k1', 'k2', 'k3', 'k4']:
    w = WEIGHTS[key]
    p = np.array(w, dtype=float)
    p /= p.sum()
    vals = np.arange(1, 16, dtype=float)
    rowd = {}
    for n in [5, 10, 15, 30]:
        gen = np.random.default_rng(5000 + n * 13 + ord(key[-1]))
        draws = gen.choice(vals, size=(MC, n), p=p)
        srt = np.sort(draws, axis=1)
        means = draws.mean(axis=1)
        meds = np.median(draws, axis=1)
        mads = np.abs(draws - means[:, None]).mean(axis=1)
        rngs = srt[:, -1] - srt[:, 0]
        meth = 'weibull' if n % 2 else 'hazen'
        iqrs = (np.percentile(draws, 75, axis=1, method=meth)
                - np.percentile(draws, 25, axis=1, method=meth))
        rowd[str(n)] = {
            'sdMeanExact': POP[key]['sd'] / math.sqrt(n),
            'sdMeanMC': float(means.std(ddof=1)),
            'sdMedian': float(meds.std(ddof=1)), 'meanMedian': float(meds.mean()),
            'sdMad': float(mads.std(ddof=1)), 'meanMad': float(mads.mean()),
            'sdIqr': float(iqrs.std(ddof=1)), 'meanIqr': float(iqrs.mean()),
            'sdRange': float(rngs.std(ddof=1)), 'meanRange': float(rngs.mean()),
        }
        r = rowd[str(n)]
        chk(abs(r['sdMeanMC'] / r['sdMeanExact'] - 1) < 0.03,
            'the measured sd of the mean matches sigma/sqrt(n) at %s, n=%d' % (key, n))
        out('%s n=%2d  sigma/sqrt(n) exact / measured' % (key, n),
            '%.12g / %.12g' % (r['sdMeanExact'], r['sdMeanMC']))
        out('        sd of the sample median / MAD / IQR / range',
            '%.6g / %.6g / %.6g / %.6g' % (r['sdMedian'], r['sdMad'], r['sdIqr'], r['sdRange']))
        # the sample MAD is biased DOWN (it uses the sample mean, not mu)
        out('        E[sample MAD] against the population MAD',
            '%.6g vs %.6g' % (r['meanMad'], POP[key]['mad']))
    SAMPLING[key] = rowd
REFS['sampling'] = SAMPLING
# The sample MAD about the SAMPLE mean is a biased estimator of the population
# MAD, and the sign of the bias is NOT always the same — the first draft of
# this file asserted "biased down at every n" and it is false.  The mechanism:
# g(c) = E|X - c| is convex, so E[g(x-bar)] >= g(mu) by Jensen, and how much
# larger depends on how sharply convex g is at mu.  g'(c) = 2F(c) - 1, which
# JUMPS across an atom, so when mu lands ON a support point (kickers 1 and 2,
# whose mean is exactly 8 m) g has a kink there and the upward push is large;
# when mu is off the lattice (kickers 3 and 4, mean 5.044 and 10.956 m) g is
# locally straight and the downward push from using x-bar inside the
# deviations wins.  Measured, not assumed:
bias = {k: {n: SAMPLING[k][n]['meanMad'] / POP[k]['mad'] - 1 for n in SAMPLING[k]}
        for k in SAMPLING}
REFS['madBias'] = bias
for k in ['k1', 'k2', 'k3', 'k4']:
    out('relative bias of the sample MAD, %s' % k,
        ', '.join('n=%s %+.4f' % (n, bias[k][n]) for n in ['5', '10', '15', '30']))
chk(all(bias[k][n] < 0 for k in ['k3', 'k4'] for n in bias[k]),
    'off-lattice mean (kickers 3, 4): the sample MAD is biased DOWN at every n')
chk(bias['k1']['5'] < 0 and bias['k1']['30'] > 0 and
    bias['k2']['5'] < 0 and bias['k2']['30'] > 0,
    'on-lattice mean (kickers 1, 2): the bias CHANGES SIGN between n = 5 and 30')
# and the Jensen half of it, exactly: g is convex, so E[g(x-bar)] >= g(mu)
def g_of(key, c):
    return jsum(pi * abs(x - c) for pi, x in zip(POP[key]['p'], range(1, 16)))
for key in ['k1', 'k3']:
    mid = g_of(key, POP[key]['mean'])
    for d in [0.1, 0.4, 1.0]:
        chk(0.5 * (g_of(key, POP[key]['mean'] - d) + g_of(key, POP[key]['mean'] + d))
            >= mid - 1e-12, 'g(c) = E|X-c| is convex at mu (%s, +/-%g)' % (key, d))
    out('curvature of g at mu, %s (g(mu+0.5)+g(mu-0.5)-2g(mu))' % key,
        g_of(key, POP[key]['mean'] + 0.5) + g_of(key, POP[key]['mean'] - 0.5) - 2 * mid)
REFS['gKink'] = {k: g_of(k, POP[k]['mean'] + 0.5) + g_of(k, POP[k]['mean'] - 0.5)
                 - 2 * g_of(k, POP[k]['mean']) for k in ['k1', 'k2', 'k3', 'k4']}
chk(REFS['gKink']['k1'] > REFS['gKink']['k3'],
    'the on-lattice mean really is the sharper kink')

# --- the law of large numbers, on the page's own stream ---------------------
head('C6. the long run on the page\'s own stream')
LLN = {}
for key in ['k1', 'k3']:
    w = WEIGHTS[key]
    nxt = mulberry32(SEEDS['longrun'] + ord(key[-1]))
    xs = []
    rows = []
    target = [10, 50, 200, 1000, 5000]
    for i in range(max(target)):
        xs.append(sample_probabilities(nxt, w))
        if len(xs) in target:
            q1, q3 = cav_quartiles(xs)
            rows.append({'n': len(xs), 'mean': cav_mean(xs), 'median': cav_median(xs),
                         'mad': cav_mad_exact(xs), 'iqr': q3 - q1,
                         'range': cav_range(xs),
                         'z': (cav_mean(xs) - POP[key]['mean'])
                              / (POP[key]['sd'] / math.sqrt(len(xs)))})
            out('%s  n=%5d  mean / z' % (key, len(xs)),
                '%.12g / %.4g' % (rows[-1]['mean'], rows[-1]['z']))
    # the empirical frequencies at the largest n, against the weights
    cnt = [0] * 15
    for x in xs:
        cnt[x - 1] += 1
    N = len(xs)
    zs = [abs(cnt[i] - N * POP[key]['p'][i])
          / math.sqrt(max(N * POP[key]['p'][i] * (1 - POP[key]['p'][i]), 1e-12))
          for i in range(15) if POP[key]['p'][i] > 0]
    LLN[key] = {'rows': rows, 'counts': cnt, 'N': N, 'worstZ': max(zs)}
    out('   worst binomial z over the support at n = %d' % N, max(zs))
    chk(max(zs) < 4.0, 'every bin of %s is within 4 binomial sd at n = %d' % (key, N))
    chk(abs(rows[-1]['z']) < 4.0, 'the sample mean of %s is within 4 sigma/sqrt(n)' % key)
REFS['lln'] = LLN

# --- the box plot's whiskers and outliers -----------------------------------
head('C7. the box plot: whiskers and the 1.5 x IQR rule')
BOX = []
for xs in [DEMO, DEMO_ODD, OPEN['spread3']['xs'], OPEN['spread4']['xs'],
           [1, 5, 6, 6, 7, 7, 8, 15], [4, 4, 4, 4, 4, 4, 4, 4, 4, 15]]:
    q1, q3 = cav_quartiles(xs)
    iqr = q3 - q1
    lof, hif = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    inl = [x for x in xs if lof <= x <= hif]
    outs = sorted(x for x in xs if x < lof or x > hif)
    BOX.append({'xs': xs, 'q1': q1, 'q3': q3, 'iqr': iqr,
                'lowFence': lof, 'highFence': hif,
                'whiskLo': min(inl), 'whiskHi': max(inl), 'outliers': outs,
                'min': min(xs), 'max': max(xs)})
    out('%s' % str(xs)[:44],
        'Q1 %g Q3 %g IQR %g fences [%g, %g]' % (q1, q3, iqr, lof, hif))
    out('   whiskers / outliers', '[%g, %g] / %s' % (min(inl), max(inl), outs))
    chk(min(inl) >= min(xs) and max(inl) <= max(xs), 'whiskers stay inside the data')
    chk(all(o < lof or o > hif for o in outs), 'every outlier is past a fence')
REFS['box'] = BOX
chk(any(b['outliers'] for b in BOX), 'at least one pinned case must HAVE an outlier')

# --- the interval tool ------------------------------------------------------
head('C8. the interval tool')
IV = []
for xs, lo, hi in [(DEMO, 3.0, 8.0), (DEMO, 0.0, 16.0), (DEMO, 8.0, 3.0),
                   (OPEN['spread2']['xs'], 5.5, 10.5)]:
    a, b = min(lo, hi), max(lo, hi)
    k = sum(1 for x in xs if a <= x <= b)
    IV.append({'xs': xs, 'lo': lo, 'hi': hi, 'count': k, 'frac': k / len(xs),
               'width': b - a})
    out('interval [%g, %g] on %s' % (lo, hi, str(xs)[:30]),
        '%d of %d = %.12g' % (k, len(xs), k / len(xs)))
REFS['interval'] = IV


# =====================================================================
#  D.  write the artifacts
# =====================================================================
def jsnum(x):
    if x is None:
        return 'null'
    if isinstance(x, bool):
        return 'true' if x else 'false'
    if isinstance(x, (int,)):
        return str(x)
    if isinstance(x, float):
        if x == int(x) and abs(x) < 1e15:
            return '%d.0' % int(x)
        return repr(x)
    if isinstance(x, (list, tuple)):
        return '[' + ','.join(jsnum(v) for v in x) + ']'
    if isinstance(x, dict):
        return '{' + ','.join('%s:%s' % (json.dumps(k), jsnum(v)) for k, v in x.items()) + '}'
    return json.dumps(x)


head('D. summary')
out('reference cases pinned', len(PINNED))
out('checks run in this file', 'see the FAILED lines above (none means all passed)')
out('failures', len(FAILS))

io.open(os.path.join(HERE, 'refvals.txt'), 'w', encoding='utf-8').write(
    '\n'.join(LINES) + '\n')

js = ['/* ================================================================== *',
      ' *  reference values — WRITTEN BY derive.py (build/center-and-        *',
      ' *  variability/derive.py); the same numbers are in refvals.txt.      *',
      ' *  Nothing here is typed by hand.                                    *',
      ' * ================================================================== */',
      'const REF={']
for k in sorted(REFS):
    js.append('  %s:%s,' % (k, jsnum(REFS[k])))
js.append('};')
io.open(os.path.join(HERE, 'p7a_refs.js'), 'w', encoding='utf-8').write(
    '\n'.join(js) + '\n')

print('\n'.join(LINES))
print()
print('wrote refvals.txt (%d lines) and p7a_refs.js' % len(LINES))
if FAILS:
    print('FAILURES: %d' % len(FAILS))
    for f in FAILS:
        print('  - ' + f)
    raise SystemExit(1)
print('all derive.py checks passed')
