"""Tests for EM-04 boundary-value problems. Reuses EM-01/EM-03 and MA-02.

Run:  python3 test_boundary_value.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-01/EM-03 (and MA-01/MA-02) onto sys.path
from boundary_value import (
    image_potential_plane, image_field_plane, induced_surface_charge,
    total_induced_charge, image_force,
    slot_potential_series, slot_potential_closed, solve_laplace_2d,
)
from electrostatics import EPS0, K_E


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_image_grounds_the_plane():
    # V = 0 everywhere on z = 0 (the boundary condition the image enforces)
    q, d = 2e-9, 0.15
    V = image_potential_plane(q, d)
    for (x, y) in [(0.0, 0.0), (0.1, 0.0), (0.05, 0.2), (0.3, -0.4)]:
        assert _approx(V(x, y, 0.0), 0.0, tol=1e-9)


def test_image_force_attractive_and_correct():
    q, d = 3e-9, 0.2
    F = image_force(q, d)
    assert F < 0                                            # toward the plane
    assert _approx(F, -K_E * q ** 2 / (2 * d) ** 2, tol=1e-12)


def test_total_induced_charge_is_minus_q():
    q, d = 1e-9, 0.1
    assert _approx(total_induced_charge(q, d), -q, tol=2e-2)


def test_induced_charge_peaks_under_the_charge():
    # |sigma| is largest directly beneath q (at the origin) and decays outward
    q, d = 1e-9, 0.1
    sigma = induced_surface_charge(q, d)
    assert abs(sigma(0.0, 0.0)) > abs(sigma(0.1, 0.0)) > abs(sigma(0.5, 0.0))
    assert sigma(0.0, 0.0) < 0                              # opposite sign to q


def test_slot_series_matches_closed_form():
    V0, a = 10.0, 1.0
    Vs, Vc = slot_potential_series(V0, a, N=400), slot_potential_closed(V0, a)
    for (x, y) in [(0.3, 0.5), (0.5, 0.25), (0.8, 0.7), (0.4, 0.9)]:
        assert _approx(Vs(x, y), Vc(x, y), tol=1e-4)


def test_slot_boundary_conditions():
    V0, a = 5.0, 2.0
    Vc = slot_potential_closed(V0, a)
    # grounded plates: V = 0 on y = 0 and y = a
    for x in (0.2, 1.0, 3.0):
        assert _approx(Vc(x, 0.0), 0.0, tol=1e-9)
        assert _approx(Vc(x, a), 0.0, tol=1e-9)
    # far down the slot the potential dies away
    assert abs(Vc(10.0, a / 2)) < 1e-6
    # near the mouth it approaches V0
    assert _approx(Vc(1e-4, a / 2), V0, tol=1e-2)


def test_slot_satisfies_laplace():
    # discrete Laplacian of the closed-form solution ~ 0 in the interior
    Vc = slot_potential_closed(10.0, 1.0)
    h = 1e-3
    x, y = 0.4, 0.5
    lap = (Vc(x + h, y) + Vc(x - h, y) + Vc(x, y + h) + Vc(x, y - h) - 4 * Vc(x, y)) / h ** 2
    scale = abs(Vc(x, y)) / 0.4 ** 2
    assert abs(lap) < 1e-3 * scale


def test_uniqueness_relaxation_matches_analytic():
    # boundary V = 10*x forces the unique interior solution V = 10*x (linear, harmonic)
    grid, xs, ys = solve_laplace_2d(lambda x, y: 10.0 * x, nx=25, ny=25, tol=1e-9)
    worst = 0.0
    for i in range(len(xs)):
        for j in range(len(ys)):
            worst = max(worst, abs(grid[i][j] - 10.0 * xs[i]))
    assert worst < 1e-3


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
