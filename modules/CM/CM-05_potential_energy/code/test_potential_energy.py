"""Tests for CM-05 potential energy. Reuses MA-01/MA-02 (imported transitively).

Run:  python3 test_potential_energy.py     ->  "All N tests passed."
"""
import math

from potential_energy import (
    force_from_potential, is_conservative, total_energy, is_equilibrium, is_stable,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_force_from_potential():
    k = 3.0
    U = lambda x, y, z: 0.5 * k * (x * x + y * y + z * z)             # -> F = -k r
    F = force_from_potential(U)
    for p in ((1.0, 2.0, 3.0), (-1.0, 0.5, 2.0)):
        assert _vapprox(F(*p), tuple(-k * c for c in p), tol=1e-3)


def test_is_conservative():
    k = 2.0
    U = lambda x, y, z: 0.5 * k * (x * x + y * y + z * z)
    assert is_conservative(force_from_potential(U))                  # gradient field -> curl 0
    assert not is_conservative(lambda x, y, z: (-y, x, 0.0))         # rotational -> curl != 0


def test_energy_conserved_for_oscillator():
    m, k, A = 1.0, 4.0, 1.0
    w = math.sqrt(k / m)
    U = lambda x, y, z: 0.5 * k * (x * x + y * y + z * z)
    E0 = 0.5 * k * A * A
    for t in (0.0, 0.25, 0.7, 1.3, 2.1):
        r = (A * math.cos(w * t), 0.0, 0.0)
        v = (-A * w * math.sin(w * t), 0.0, 0.0)
        assert _approx(total_energy(m, v, U, r), E0, tol=1e-9)        # E = 1/2 k A^2, constant


def test_double_well_equilibria():
    U = lambda x: x ** 4 - 2.0 * x ** 2                              # minima at +/-1, max at 0
    assert is_equilibrium(U, 1.0) and is_equilibrium(U, -1.0) and is_equilibrium(U, 0.0)
    assert not is_equilibrium(U, 0.5)
    assert is_stable(U, 1.0) and is_stable(U, -1.0)                  # wells are stable
    assert not is_stable(U, 0.0)                                     # hilltop is unstable


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
