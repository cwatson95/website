"""Tests for RE-05 Minkowski spacetime.

Run directly:   python3 test_minkowski.py      (-> "All N tests passed.")
Or with pytest: pytest test_minkowski.py

Checks: eta is its own inverse; lower/raise (MA-16) round-trips; the interval and
the Minkowski product are Lorentz-invariant (verified against an inline boost);
classify/causal_relation label the light cone; and proper time obeys the reversed
triangle inequality (the twin paradox).
"""
import math
import random

from minkowski import (
    ETA, ETA_INV, mdot, interval2, classify,
    lower, raise_, is_future_pointing, causal_relation,
    proper_time, four_velocity, three_velocity, four_momentum, invariant_mass,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=TOL):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def _rand_event(rng):
    return [rng.uniform(-3.0, 3.0) for _ in range(4)]


def _rand_beta_vec(rng, hi=0.9):
    while True:
        b = [rng.uniform(-hi, hi) for _ in range(3)]
        if b[0] ** 2 + b[1] ** 2 + b[2] ** 2 < hi * hi:
            return b


def _boost(beta_vec):
    """A general Lorentz boost (inline, so the test doesn't depend on RE-03)."""
    bx, by, bz = beta_vec
    b2 = bx * bx + by * by + bz * bz
    g = 1.0 / math.sqrt(1.0 - b2)
    b = [bx, by, bz]
    L = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    L[0][0] = g
    for i in range(3):
        L[0][i + 1] = L[i + 1][0] = -g * b[i]
        for j in range(3):
            L[i + 1][j + 1] = (1.0 if i == j else 0.0) + (g - 1.0) * b[i] * b[j] / b2
    return L


def _apply(L, x):
    return [sum(L[i][k] * x[k] for k in range(4)) for i in range(4)]


def test_eta_is_its_own_inverse():
    prod = [[sum(ETA[i][k] * ETA_INV[k][j] for k in range(4)) for j in range(4)]
            for i in range(4)]
    ident = [[1.0 if i == j else 0.0 for j in range(4)] for i in range(4)]
    assert all(_approx(prod[i][j], ident[i][j]) for i in range(4) for j in range(4))


def test_interval_matches_formula():
    rng = random.Random(0)
    for _ in range(300):
        x = _rand_event(rng)
        assert _approx(interval2(x), -x[0] ** 2 + x[1] ** 2 + x[2] ** 2 + x[3] ** 2)


def test_lower_raise_roundtrip():
    rng = random.Random(1)
    for _ in range(300):
        v = _rand_event(rng)
        assert _vapprox(raise_(lower(v)), v)
        # lowering flips only the time component's sign
        lo = lower(v)
        assert _approx(lo[0], -v[0]) and _vapprox(lo[1:], v[1:])
        # u.v can be computed as u^mu (v_mu)
        u = _rand_event(rng)
        assert _approx(mdot(u, v), sum(u[i] * lower(v)[i] for i in range(4)))


def test_interval_and_product_are_invariant():
    """The whole point: a Lorentz boost leaves u.v unchanged."""
    rng = random.Random(2)
    for _ in range(400):
        L = _boost(_rand_beta_vec(rng))
        u, v = _rand_event(rng), _rand_event(rng)
        assert _approx(mdot(_apply(L, u), _apply(L, v)), mdot(u, v))
        assert _approx(interval2(_apply(L, u)), interval2(u))


def test_classify_and_causal_structure():
    assert classify([3.0, 1.0, 0.0, 0.0]) == "timelike"
    assert classify([1.0, 1.0, 0.0, 0.0]) == "null"
    assert classify([0.0, 2.0, 0.0, 0.0]) == "spacelike"
    A = [0.0, 0.0, 0.0, 0.0]
    assert causal_relation(A, [3.0, 1.0, 0.0, 0.0]) == "future"
    assert causal_relation(A, [-3.0, 1.0, 0.0, 0.0]) == "past"
    assert causal_relation(A, [0.5, 2.0, 0.0, 0.0]) == "elsewhere"   # spacelike
    assert is_future_pointing([2.0, 1.0, 0.0, 0.0])
    assert not is_future_pointing([-2.0, 1.0, 0.0, 0.0])


def test_causal_order_is_frame_invariant_for_timelike():
    """Timelike order can't be reversed by a boost; spacelike 'order' can."""
    rng = random.Random(3)
    A = [0.0, 0.0, 0.0, 0.0]
    B = [3.0, 1.0, 0.0, 0.0]                       # timelike future of A
    for _ in range(200):
        L = _boost(_rand_beta_vec(rng))
        Bp = _apply(L, B)
        assert Bp[0] > 0.0                          # B still in the future
    # a spacelike-separated event CAN have its time-order flipped
    S = [0.1, 3.0, 0.0, 0.0]                        # spacelike from A
    flipped = any(_apply(_boost(_rand_beta_vec(rng)), S)[0] < 0.0 for _ in range(50))
    assert flipped


def test_proper_time_reversed_triangle_inequality():
    A, B = [0.0, 0.0, 0.0, 0.0], [10.0, 0.0, 0.0, 0.0]
    straight = proper_time([A, B])
    assert _approx(straight, 10.0)                  # = sqrt(-s^2) = 10
    for x in (1.0, 2.0, 4.0):                        # any detour is shorter
        bent = proper_time([A, [5.0, x, 0.0, 0.0], B])
        assert bent < straight
        assert _approx(bent, math.sqrt(100.0 - 4.0 * x * x))
    # proper time is additive along a worldline
    mid = [4.0, 0.0, 0.0, 0.0]
    assert _approx(proper_time([A, mid, B]), proper_time([A, B]))


def test_four_velocity_and_momentum():
    rng = random.Random(4)
    for _ in range(300):
        v = _rand_beta_vec(rng)
        U = four_velocity(v)
        assert _approx(mdot(U, U), -1.0)            # U.U = -1
        assert _vapprox(three_velocity(U), v)
        m = rng.uniform(0.5, 5.0)
        p = four_momentum(m, v)
        assert _approx(mdot(p, p), -m * m)          # mass shell p.p = -m^2
        assert _approx(invariant_mass(p), m)
        # E = gamma m, |p| = gamma m |v|  ->  E^2 - |p|^2 = m^2
        E, px, py, pz = p
        assert _approx(E * E - (px * px + py * py + pz * pz), m * m)


def test_invariant_mass_is_frame_independent():
    rng = random.Random(5)
    for _ in range(200):
        p = four_momentum(3.0, _rand_beta_vec(rng))
        pboosted = _apply(_boost(_rand_beta_vec(rng)), p)
        assert _approx(invariant_mass(pboosted), 3.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
