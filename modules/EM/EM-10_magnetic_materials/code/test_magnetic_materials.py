"""Tests for EM-10 magnetic materials. Reuses EM-08 (mu0) and MA-01/MA-02.

Run:  python3 test_magnetic_materials.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-08 (and MA-01/MA-02) onto sys.path
from magnetic_materials import (
    bound_volume_current, bound_surface_current, auxiliary_field_H,
    magnetization_linear, permeability, B_linear, classify_material,
    magnetized_sphere_inner_B, magnetized_sphere_inner_H,
    hysteresis_branches, remanence, coercivity,
)
from magnetostatics import MU0
from vector_algebra import norm


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_bound_volume_current():
    # uniform M -> J_b = 0
    Mu = lambda x, y, z: (0.0, 0.0, 1e4)
    assert _vapprox(bound_volume_current(Mu, (0.1, 0.2, 0.3)), (0, 0, 0), tol=1e-3)
    # swirling M = (-a y, a x, 0) -> curl M = 2a zhat
    a = 5.0
    Mr = lambda x, y, z: (-a * y, a * x, 0.0)
    assert _vapprox(bound_volume_current(Mr, (0.3, 0.1, 0.0)), (0, 0, 2 * a), tol=1e-3)


def test_bound_surface_current_is_solenoidal():
    # M along z, side-surface normal s-hat = x-hat -> K_b = M phi-hat (= +y here)
    Mz = 1e4
    Kb = bound_surface_current((0, 0, Mz), (1, 0, 0))
    assert _vapprox(Kb, (0.0, Mz, 0.0), tol=1e-9)
    assert _approx(norm(Kb), Mz, tol=1e-12)                 # |K_b| = M


def test_auxiliary_field_definition():
    # H = B/mu0 - M, pointwise
    B = lambda x, y, z: (0.0, 0.0, 1.2)
    M = lambda x, y, z: (0.0, 0.0, 5e5)
    H = auxiliary_field_H(B, M)
    assert _vapprox(H(0, 0, 0), (0.0, 0.0, 1.2 / MU0 - 5e5), tol=1e-3)


def test_linear_media_consistency():
    # B = mu H and B = mu0(H + M) with M = chi H must agree
    chi = 600.0
    H = lambda x, y, z: (0.0, 0.0, 100.0)
    M = magnetization_linear(chi, H)
    B = B_linear(chi, H)
    p = (0, 0, 0)
    bx, by, bz = B(*p)
    hx, hy, hz = H(*p)
    mx, my, mz = M(*p)
    assert _approx(bz, MU0 * (hz + mz), tol=1e-9)
    assert _approx(permeability(chi), MU0 * (1 + chi), tol=1e-15)


def test_classification():
    assert classify_material(-1.7e-5) == "diamagnetic"
    assert classify_material(2.5e-4) == "paramagnetic"
    assert classify_material(5500.0) == "ferromagnetic"


def test_magnetized_sphere_fields_consistent():
    M = (0.0, 0.0, 8e5)
    Bin = magnetized_sphere_inner_B(M)
    Hin = magnetized_sphere_inner_H(M)
    # B_in = (2/3) mu0 M and H_in = -M/3
    assert _vapprox(Bin, (0, 0, (2.0 / 3.0) * MU0 * 8e5), tol=1e-9)
    assert _vapprox(Hin, (0, 0, -8e5 / 3.0), tol=1e-6)
    # the defining relation B = mu0 (H + M) holds inside
    assert _approx(Bin[2], MU0 * (Hin[2] + M[2]), tol=1e-9)


def test_hysteresis_has_remanence_and_coercivity():
    Ms, Hc, w = 8e5, 5e3, 2e3
    M_up, M_down = hysteresis_branches(Ms, Hc, w)
    # the two branches differ at H = 0 -> open loop (history dependence)
    assert M_down(0.0) > 0.0 > M_up(0.0)
    # remanence is nonzero and below saturation
    Mr = remanence(Ms, Hc, w)
    assert 0.0 < Mr < Ms
    # descending branch crosses M = 0 at H = -Hc (coercive field)
    assert _approx(M_down(-coercivity(Ms, Hc, w)), 0.0, tol=1e-9)
    # branches saturate to +/- Ms at large |H|
    assert _approx(M_up(1e6), Ms, tol=1e-6) and _approx(M_down(-1e6), -Ms, tol=1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
