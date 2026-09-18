"""Tests for EM-03 electric potential. Reuses EM-01 (fields) and MA-02 (grad/int/lap).

Run:  python3 test_electric_potential.py     ->  "All N tests passed."
"""
import math

# own module first: it chains EM-01 (and MA-01/MA-02) onto sys.path
from electric_potential import (
    potential_of_charge, potential_point_charges,
    potential_from_field, field_from_potential, poisson_residual,
)
from electrostatics import EPS0, K_E, point_charge_field, coulomb_field, field_magnitude


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_point_charge_potential():
    q = 2e-9
    V = potential_of_charge(q)
    for r in (0.1, 0.5, 3.0):
        assert _approx(V(r, 0, 0), K_E * q / r, tol=1e-12)


def test_superposition_and_dipole_antisymmetry():
    q = 1e-9
    Vd = potential_point_charges([(q, (-0.05, 0, 0)), (-q, (0.05, 0, 0))])
    # potential is odd under x -> -x for this antisymmetric pair
    assert _approx(Vd(0.2, 0, 0), -Vd(-0.2, 0, 0), tol=1e-9)
    # midplane x=0 is at zero potential
    assert _approx(Vd(0.0, 0.3, 0.1), 0.0, tol=1e-12)


def test_field_is_minus_grad_V():
    # E = -grad V must reproduce the exact EM-01 Coulomb field
    q = 3e-9
    V = potential_of_charge(q)
    E = field_from_potential(V)
    Eexact = point_charge_field(q)
    for p in ((0.3, 0.2, -0.1), (-0.4, 0.1, 0.25)):
        assert _vapprox(E(*p), Eexact(*p), tol=1e-3)


def test_potential_from_field_round_trip():
    # V(P) - V(ref) = - int_ref^P E.dl  must match the closed-form difference
    q = 2e-9
    Eexact = point_charge_field(q)
    Vclosed = potential_of_charge(q)
    ref = (10.0, 0.0, 0.0)
    Vint = potential_from_field(Eexact, reference=ref)
    for p in ((0.5, 0.0, 0.0), (0.3, 0.4, 0.0), (-0.6, 0.2, 0.1)):
        target = Vclosed(*p) - Vclosed(*ref)
        assert _approx(Vint(*p), target, tol=1e-3)


def test_path_independence():
    # two different references differ only by a constant (the potential of ref)
    q = 1e-9
    E = point_charge_field(q)
    Va = potential_from_field(E, reference=(8.0, 0.0, 0.0))
    Vb = potential_from_field(E, reference=(0.0, 9.0, 0.0))
    p1, p2 = (0.4, 0.1, 0.0), (-0.2, 0.3, 0.2)
    # V(p1)-V(p2) is reference-independent (a genuine potential difference)
    assert _approx(Va(*p1) - Va(*p2), Vb(*p1) - Vb(*p2), tol=1e-3)


def test_laplace_in_vacuum():
    # point-charge potential satisfies grad^2 V = 0 away from the source
    q = 4e-9
    V = potential_of_charge(q)
    for p in ((0.5, 0.2, -0.3), (0.4, -0.4, 0.1)):
        assert abs(poisson_residual(V, 0.0, p)) < 1e-2


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
