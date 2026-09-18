"""Tests for CM-19 Hamiltonian mechanics. Reuses MA-07 (imported transitively).

Run:  python3 test_hamiltonian.py     ->  "All N tests passed."
"""
import math

from hamiltonian import hamilton_rhs, integrate_hamilton, hamiltonian_from_potential


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_sho_matches_newton():
    w = 2.0
    H = hamiltonian_from_potential(1.0, lambda q: 0.5 * w * w * q * q)
    ts, ys = integrate_hamilton(H, 1.0, 0.0, 0.0, 2 * math.pi, 8000)
    for t, s in list(zip(ts, ys))[::400]:
        assert _approx(s[0], math.cos(w * t), tol=1e-4)         # q(t) = cos(w t)
        assert _approx(s[1], -w * math.sin(w * t), tol=1e-4)    # p(t) = qdot = -w sin(w t)


def test_energy_conserved():
    w = 1.5
    H = hamiltonian_from_potential(1.0, lambda q: 0.5 * w * w * q * q)
    ts, ys = integrate_hamilton(H, 1.0, 0.5, 0.0, 10.0, 8000)
    E0 = H(*ys[0])
    for s in ys[::400]:
        assert _approx(H(*s), E0, tol=1e-5)                     # H conserved along the flow


def test_phase_orbit_is_closed_ellipse():
    w = 2.0
    H = hamiltonian_from_potential(1.0, lambda q: 0.5 * w * w * q * q)
    ts, ys = integrate_hamilton(H, 1.0, 0.0, 0.0, 2 * math.pi, 8000)
    for s in ys[::400]:
        assert _approx(s[1] ** 2 + w * w * s[0] ** 2, w * w, tol=1e-4)   # p^2 + w^2 q^2 = w^2
    # returns to the start after one period
    assert _approx(ys[-1][0], ys[0][0], tol=1e-3) and _approx(ys[-1][1], ys[0][1], tol=1e-3)


def test_hamilton_rhs_signs():
    # for H = p^2/2 + 1/2 w^2 q^2:  qdot = p,  pdot = -w^2 q
    w = 3.0
    H = hamiltonian_from_potential(1.0, lambda q: 0.5 * w * w * q * q)
    rhs = hamilton_rhs(H)
    qd, pd = rhs(0.0, [2.0, 5.0])
    assert _approx(qd, 5.0, tol=1e-4) and _approx(pd, -w * w * 2.0, tol=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
