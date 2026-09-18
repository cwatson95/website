"""Tests for MA-22 topology & dynamical systems. Pure stdlib.

Run:  python3 test_topo_dynamics.py     ->  "All N tests passed."
"""
import math

from topo_dynamics import (
    classify_equilibrium, eigenvalues_2x2,
    logistic, logistic_orbit, lyapunov_logistic, period_of_orbit,
    euler_characteristic, PLATONIC,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_equilibrium_classification():
    assert classify_equilibrium([[1, 0], [0, -1]]) == "saddle"
    assert classify_equilibrium([[-2, 0], [0, -1]]) == "stable node"
    assert classify_equilibrium([[2, 0], [0, 1]]) == "unstable node"
    assert classify_equilibrium([[-1, -2], [2, -1]]) == "stable spiral"
    assert classify_equilibrium([[1, -2], [2, 1]]) == "unstable spiral"
    assert classify_equilibrium([[0, -1], [1, 0]]) == "center"


def test_eigenvalues_2x2():
    # stable spiral -1 +/- 2i
    ev = eigenvalues_2x2([[-1, -2], [2, -1]])
    assert _approx(ev[0].real, -1.0) and _approx(abs(ev[0].imag), 2.0)
    # saddle +1, -1
    ev = sorted(eigenvalues_2x2([[1, 0], [0, -1]]), key=lambda z: z.real)
    assert _approx(ev[0].real, -1.0) and _approx(ev[1].real, 1.0)


def test_logistic_fixed_point():
    # for 1 < r < 3 the orbit converges to the fixed point x* = 1 - 1/r
    for r in (2.0, 2.5, 2.8):
        orbit = logistic_orbit(r, 0.1, 20, skip=5000)
        assert all(_approx(x, 1 - 1 / r, tol=1e-6) for x in orbit)
        assert period_of_orbit(r) == 1


def test_logistic_period_doubling():
    assert period_of_orbit(3.2) == 2          # period-2
    assert period_of_orbit(3.5) == 4          # period-4
    assert period_of_orbit(3.55) == 8         # period-8


def test_lyapunov_exponent():
    # negative on stable cycles, positive in chaos; exactly ln 2 at r = 4
    assert lyapunov_logistic(2.5) < 0
    assert lyapunov_logistic(3.2) < 0
    assert lyapunov_logistic(3.5) < 0
    assert lyapunov_logistic(4.0) > 0
    assert _approx(lyapunov_logistic(4.0, n=400000), math.log(2), tol=2e-2)


def test_lyapunov_sign_matches_period():
    # a detectable finite period <=> non-positive Lyapunov exponent
    for r in (2.5, 3.2, 3.5):
        assert period_of_orbit(r) > 0 and lyapunov_logistic(r) < 0
    assert period_of_orbit(4.0) == -1 and lyapunov_logistic(4.0) > 0


def test_euler_characteristic_polyhedra():
    for name, (V, E, F) in PLATONIC.items():
        assert euler_characteristic(V, E, F) == 2          # all are spheres


def test_euler_genus_formula():
    # chi = 2 - 2g:  sphere (g=0) -> 2,  torus (g=1) -> 0
    assert euler_characteristic(4, 6, 4) == 2 - 2 * 0      # tetrahedron ~ sphere, g=0
    assert euler_characteristic(9, 27, 18) == 2 - 2 * 1    # torus mesh, g=1


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
