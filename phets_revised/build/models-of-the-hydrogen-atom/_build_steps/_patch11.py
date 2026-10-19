#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""derive.py side of the choose_l / choose_m consolidation: the Python twin has
to draw from the same ordered distributions and consume the same number of
random draws, or the bit-for-bit cascade pins stop meaning anything."""
import io
import os

HERE = os.path.dirname(os.path.abspath(__file__))
p = os.path.join(HERE, "derive.py")
s = io.open(p, encoding="utf-8").read()


def sub(old, new):
    global s
    assert s.count(old) == 1, ("%r appears %d times" % (old[:70], s.count(old)))
    s = s.replace(old, new)


# the distributions become ORDERED LISTS, in exactly the JS order
sub('''def phet_choose_l_dist(l, n_new):
    """choose_l: 0 -> 1; l == n_new or l == n_new-1 -> l-1; else 50/50 l+-1."""
    if l == 0:
        return {1: 1.0}
    if l == n_new or l == n_new - 1:
        return {l - 1: 1.0}
    return {l + 1: 0.5, l - 1: 0.5}


def phet_choose_m_dist(m, l_new):
    if l_new == 0:
        return {0: 1.0}
    if m > l_new:
        return {l_new: 1.0}
    if m < -l_new:
        return {-l_new: 1.0}
    if m == l_new:
        return {m: 0.5, m - 1: 0.5}
    if m == -l_new:
        return {m: 0.5, m + 1: 0.5}
    return {m + 1: 1.0 / 3, m - 1: 1.0 / 3, m: 1.0 / 3}''',
    '''def phet_choose_l_list(l, n_new):
    """choose_l: 0 -> 1; l == n_new or l == n_new-1 -> l-1; else 50/50 l+-1.
    An ORDERED list, matching the JS exactly: both sides feed it to the same
    weighted() and must therefore agree on the order as well as the weights."""
    if l == 0:
        return [(1, 1.0)]
    if l == n_new or l == n_new - 1:
        return [(l - 1, 1.0)]
    return [(l + 1, 0.5), (l - 1, 0.5)]


def phet_choose_m_list(m, l_new):
    if l_new == 0:
        return [(0, 1.0)]
    if m > l_new:
        return [(l_new, 1.0)]
    if m < -l_new:
        return [(-l_new, 1.0)]
    if m == l_new:
        return [(m, 0.5), (m - 1, 0.5)]
    if m == -l_new:
        return [(m, 0.5), (m + 1, 0.5)]
    return [(m + 1, 1.0 / 3), (m - 1, 1.0 / 3), (m, 1.0 / 3)]


def phet_choose_l_dist(l, n_new):
    return dict(phet_choose_l_list(l, n_new))


def phet_choose_m_dist(m, l_new):
    return dict(phet_choose_m_list(m, l_new))''')

sub('''    out = {}
    for lp, pl in phet_choose_l_dist(l, n_new).items():
        for mp, pm in phet_choose_m_dist(m, lp).items():''',
    '''    out = {}
    for lp, pl in phet_choose_l_list(l, n_new):
        for mp, pm in phet_choose_m_list(m, lp):''')

# the cascade draws from the lists, one weighted() call per choice
sub('''        nn = rng.weighted(sorted(d.items()))
        # choose_l
        if l == 0:
            lp = 1
        elif l == nn or l == nn - 1:
            lp = l - 1
        else:
            lp = l + 1 if rng.next() < 0.5 else l - 1
        # choose_m
        if lp == 0:
            mp = 0
        elif m > lp:
            mp = lp
        elif m < -lp:
            mp = -lp
        elif m == lp:
            mp = m if rng.int_below(2) == 0 else m - 1
        elif m == -lp:
            mp = m if rng.int_below(2) == 0 else m + 1
        else:
            k = rng.int_below(3)
            mp = m + 1 if k == 0 else (m - 1 if k == 1 else m)
        ok = (valid_state(n, l, m) and valid_state(nn, lp, mp) and n != nn''',
    '''        nn = rng.weighted(sorted(d.items()))
        lp = rng.weighted(phet_choose_l_list(l, nn))
        mp = rng.weighted(phet_choose_m_list(m, lp))
        ok = (valid_state(n, l, m) and valid_state(nn, lp, mp) and n != nn''')

# the printed distributions follow the lists
sub('''for (l, nn) in [(0, 3), (1, 3), (2, 3), (1, 2), (2, 4), (3, 5)]:
    P("PhET P(l'|l=%d, n'=%d)" % (l, nn), phet_choose_l_dist(l, nn))
for (m, ln) in [(0, 0), (0, 1), (1, 1), (-1, 1), (2, 1), (-2, 1), (0, 2), (1, 2), (2, 2), (-2, 2)]:
    P("PhET P(m'|m=%d, l'=%d)" % (m, ln), {k: round(v, 10) for k, v in phet_choose_m_dist(m, ln).items()})''',
    '''for (l, nn) in [(0, 3), (1, 3), (2, 3), (1, 2), (2, 4), (3, 5)]:
    P("PhET P(l'|l=%d, n'=%d)" % (l, nn), phet_choose_l_list(l, nn))
for (m, ln) in [(0, 0), (0, 1), (1, 1), (-1, 1), (2, 1), (-2, 1), (0, 2), (1, 2), (2, 2), (-2, 2)]:
    P("PhET P(m'|m=%d, l'=%d)" % (m, ln), [(k, round(v, 10)) for k, v in phet_choose_m_list(m, ln)])''')

# the lower-n floor, written once (matches the JS after patch 10)
sub('''    lo = max(l, 1)
    if l == 0:
        lo = 2''',
    '''    lo = 2 if l == 0 else l''')

io.open(p, "w", encoding="utf-8").write(s)
print("derive.py patched")
