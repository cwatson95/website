"""Tests for CM-14 Euler's equations. Reuses MA-07 (imported transitively).

Run:  python3 test_euler_equations.py     ->  "All N tests passed."
"""
from euler_equations import (
    integrate_euler, precession_rate, L_magnitude_sq, rotational_energy,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_torque_free_conserves_L_and_energy():
    I = (1.0, 2.0, 3.0)
    ts, ws = integrate_euler(I, (1.0, 1.0, 1.0), 0.0, 5.0, 5000)
    L0, T0 = L_magnitude_sq(I, ws[0]), rotational_energy(I, ws[0])
    for w in ws[::200]:
        assert _approx(L_magnitude_sq(I, w), L0, tol=1e-4)        # |L| conserved
        assert _approx(rotational_energy(I, w), T0, tol=1e-4)     # T conserved


def test_symmetric_top_precession():
    I = (1.0, 1.0, 2.0)                                           # I1 = I2
    ts, ws = integrate_euler(I, (0.5, 0.0, 3.0), 0.0, 5.0, 5000)
    for w in ws[::200]:
        assert _approx(w[2], 3.0, tol=1e-5)                      # omega3 is constant
        assert _approx(w[0] ** 2 + w[1] ** 2, 0.25, tol=1e-4)    # |omega_perp| constant (it precesses)
    assert _approx(precession_rate(1.0, 2.0, 3.0), 3.0)          # Omega = (I3-I1)/I1 * omega3


def test_steady_rotation_about_each_principal_axis():
    I = (1.0, 2.0, 3.0)
    for axis in [(2.0, 0.0, 0.0), (0.0, 2.0, 0.0), (0.0, 0.0, 2.0)]:
        ts, ws = integrate_euler(I, axis, 0.0, 3.0, 2000)
        for w in ws[::200]:
            assert _vapprox(w, axis, tol=1e-6)                   # spin about a principal axis is steady


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
