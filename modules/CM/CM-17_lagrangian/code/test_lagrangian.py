"""Tests for CM-17 Lagrangian mechanics. Reuses MA-13/MA-07 (imported transitively).

Run:  python3 test_lagrangian.py     ->  "All N tests passed."
"""
import math

from lagrangian import el_residual, generalized_momentum, jacobi_energy, integrate_eom


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_el_residual_sho():
    w = 2.0
    L = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q
    N = 400
    ts = [i * (2 * math.pi / w) / N for i in range(N + 1)]
    good = [math.cos(w * t) for t in ts]
    assert max(abs(r) for r in el_residual(L, ts, good)) < 1e-2          # true path -> ~0
    bad = [t * t for t in ts]
    assert max(abs(r) for r in el_residual(L, ts, bad)) > 0.1            # wrong path -> not 0


def test_generalized_momentum():
    m = 2.0
    L = lambda t, q, p: 0.5 * m * p * p - q ** 2
    assert _approx(generalized_momentum(L, 0.0, 1.0, 3.0), m * 3.0)      # p = m qdot


def test_jacobi_energy_is_T_plus_V():
    m, k = 1.5, 4.0
    V = lambda q: 0.5 * k * q * q
    L = lambda t, q, p: 0.5 * m * p * p - V(q)
    q, qd = 0.7, 1.3
    assert _approx(jacobi_energy(L, 0.0, q, qd), 0.5 * m * qd * qd + V(q))


def test_pendulum_trajectory_satisfies_el():
    g, l = 9.81, 1.0
    L = lambda t, q, p: 0.5 * l * l * p * p + g * l * math.cos(q)        # m=1
    ts, ys = integrate_eom(lambda t, q, qd: -(g / l) * math.sin(q), 0.5, 0.0, 0.0, 3.0, 3000)
    res = el_residual(L, ts, [s[0] for s in ys])
    assert max(abs(r) for r in res) < 1e-2                              # integrated path is a true extremal


def test_cyclic_coordinate_conserves_momentum():
    # free particle L = 1/2 qdot^2 has no q-dependence -> p = qdot conserved
    L = lambda t, q, p: 0.5 * p * p
    ts, ys = integrate_eom(lambda t, q, qd: 0.0, 0.0, 2.5, 0.0, 5.0, 1000)
    ps = [generalized_momentum(L, t, s[0], s[1]) for t, s in zip(ts, ys)]
    assert all(_approx(p, 2.5) for p in ps[::100])                      # momentum constant


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
