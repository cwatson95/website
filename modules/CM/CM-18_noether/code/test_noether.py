"""Tests for CM-18 Noether's theorem. Reuses CM-17 (imported transitively).

Run:  python3 test_noether.py     ->  "All N tests passed."
"""
import math

from noether import noether_charge, symmetry_defect, energy, integrate_eom


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_translation_symmetry_conserves_momentum():
    L = lambda t, q, p: 0.5 * p * p                              # free particle
    assert abs(symmetry_defect(L, lambda q: 1.0, 0.0, 1.0, 2.0)) < 1e-6   # translation symmetric
    ts, ys = integrate_eom(lambda t, q, qd: 0.0, 0.0, 2.5, 0.0, 4.0, 800)
    Q = [noether_charge(L, lambda q: 1.0, t, s[0], s[1]) for t, s in zip(ts, ys)]
    assert all(_approx(x, 2.5) for x in Q[::80])                # momentum conserved


def test_potential_breaks_translation():
    w = 2.0
    L = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q
    assert abs(symmetry_defect(L, lambda q: 1.0, 0.0, 1.0, 0.5)) > 0.1    # not translation symmetric


def test_time_translation_conserves_energy():
    w = 2.0
    L = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q       # no explicit t
    ts, ys = integrate_eom(lambda t, q, qd: -w * w * q, 1.0, 0.0, 0.0, 5.0, 5000)
    E = [energy(L, t, s[0], s[1]) for t, s in zip(ts, ys)]
    for e in E[::200]:
        assert _approx(e, E[0], tol=1e-4)                       # energy conserved
    assert _approx(E[0], 0.5 * w * w, tol=1e-3)                 # 1/2 w^2 A^2 = 2


def test_scaling_is_not_a_symmetry_of_sho():
    w = 2.0
    L = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q
    # delta q = eps q (dilation) changes L, so it is not a symmetry
    assert abs(symmetry_defect(L, lambda q: q, 0.0, 1.0, 1.0)) > 0.1


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
