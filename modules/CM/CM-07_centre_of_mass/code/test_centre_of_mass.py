"""Tests for CM-07 centre of mass. Pure stdlib.

Run:  python3 test_centre_of_mass.py     ->  "All N tests passed."
"""
from centre_of_mass import (
    centre_of_mass, cm_velocity, reduced_mass, relative_coordinate, two_body_decompose,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_centre_of_mass_symmetric():
    assert _vapprox(centre_of_mass([1, 1], [[0, 0, 0], [2, 0, 0]]), [1.0, 0.0, 0.0])
    assert _vapprox(centre_of_mass([1, 1, 1], [[0, 0, 0], [3, 0, 0], [0, 3, 0]]), [1.0, 1.0, 0.0])


def test_centre_of_mass_weighted():
    # 3:1 -> CM at 1/4 of the way to the heavy mass from... it sits closer to heavy mass
    assert _vapprox(centre_of_mass([3, 1], [[0, 0, 0], [4, 0, 0]]), [1.0, 0.0, 0.0])


def test_cm_velocity():
    assert _vapprox(cm_velocity([2, 1], [[3, 0, 0], [0, 0, 0]]), [2.0, 0.0, 0.0])


def test_reduced_mass():
    assert _approx(reduced_mass(2.0, 2.0), 1.0)                      # equal masses -> m/2
    assert _approx(reduced_mass(3.0, 6.0), 2.0)
    assert _approx(reduced_mass(1.0, 1e12), 1.0, tol=1e-6)           # heavy partner -> lighter mass
    assert _approx(reduced_mass(2.0, 3.0), reduced_mass(3.0, 2.0))   # symmetric


def test_relative_and_decompose():
    assert _vapprox(relative_coordinate([5, 2, 1], [1, 2, 0]), [4.0, 0.0, 1.0])
    R, r = two_body_decompose(1.0, 1.0, [0, 0, 0], [2, 0, 0])
    assert _vapprox(R, [1.0, 0.0, 0.0]) and _vapprox(r, [-2.0, 0.0, 0.0])


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
