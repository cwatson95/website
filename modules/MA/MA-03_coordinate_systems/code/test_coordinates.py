"""Tests for MA-03 coordinate systems. Reuses MA-01 (imported transitively).

Run:  python3 test_coordinates.py     ->  "All N tests passed."
"""
import math
import random

from coordinates import (
    cart_to_cyl, cyl_to_cart, cart_to_sph, sph_to_cart,
    cyl_basis, sph_basis, cyl_scale_factors, sph_scale_factors,
    cyl_jacobian, sph_jacobian, vector_to_spherical, vector_from_spherical,
)
from vector_algebra import dot, cross, norm, unit


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_cyl_roundtrip():
    rng = random.Random(0)
    for _ in range(200):
        p = (rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3, 3))
        assert _vapprox(cyl_to_cart(*cart_to_cyl(*p)), p)


def test_sph_roundtrip():
    rng = random.Random(1)
    for _ in range(200):
        p = (rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3, 3))
        assert _vapprox(sph_to_cart(*cart_to_sph(*p)), p)


def test_known_points():
    rho, phi, z = cart_to_cyl(1.0, 1.0, 0.0)
    assert _approx(rho, math.sqrt(2)) and _approx(phi, math.pi / 4) and _approx(z, 0.0)
    r, theta, ph = cart_to_sph(1.0, 1.0, 0.0)
    assert _approx(r, math.sqrt(2)) and _approx(theta, math.pi / 2) and _approx(ph, math.pi / 4)
    # a point on +z: theta = 0
    assert _approx(cart_to_sph(0.0, 0.0, 5.0)[1], 0.0)


def test_cyl_basis_orthonormal_rh():
    for phi in (0.0, 1.0, 2.5, -0.7):
        e_rho, e_phi, e_z = cyl_basis(phi)
        for e in (e_rho, e_phi, e_z):
            assert _approx(norm(e), 1.0)
        assert _approx(dot(e_rho, e_phi), 0.0) and _approx(dot(e_rho, e_z), 0.0) and _approx(dot(e_phi, e_z), 0.0)
        assert _vapprox(cross(e_rho, e_phi), e_z)          # right-handed


def test_sph_basis_orthonormal_rh():
    for theta, phi in ((0.7, 0.4), (1.9, -1.2), (math.pi / 2, 0.0)):
        e_r, e_th, e_ph = sph_basis(theta, phi)
        for e in (e_r, e_th, e_ph):
            assert _approx(norm(e), 1.0)
        assert _approx(dot(e_r, e_th), 0.0) and _approx(dot(e_r, e_ph), 0.0) and _approx(dot(e_th, e_ph), 0.0)
        assert _vapprox(cross(e_r, e_th), e_ph)            # right-handed


def test_e_r_points_along_position():
    rng = random.Random(2)
    for _ in range(100):
        p = (rng.uniform(-3, 3), rng.uniform(-3, 3), rng.uniform(-3, 3))
        r, theta, phi = cart_to_sph(*p)
        if r < 1e-6:
            continue
        e_r = sph_basis(theta, phi)[0]
        assert _vapprox(e_r, unit(p), tol=1e-9)


def test_scale_factors_equal_jacobian():
    for rho in (0.5, 2.0, 4.0):
        h = cyl_scale_factors(rho)
        assert _approx(h[0] * h[1] * h[2], cyl_jacobian(rho))
    for r, theta in ((1.0, 0.5), (2.0, 1.3), (3.0, math.pi / 2)):
        h = sph_scale_factors(r, theta)
        assert _approx(h[0] * h[1] * h[2], sph_jacobian(r, theta))
        assert _approx(sph_jacobian(r, theta), r * r * math.sin(theta))


def test_vector_component_conversion():
    rng = random.Random(3)
    for _ in range(200):
        v = (rng.uniform(-2, 2), rng.uniform(-2, 2), rng.uniform(-2, 2))
        theta, phi = rng.uniform(0.1, math.pi - 0.1), rng.uniform(-math.pi, math.pi)
        vs = vector_to_spherical(*v, theta, phi)
        assert _vapprox(vector_from_spherical(*vs, theta, phi), v)   # round-trip
        assert _approx(norm(vs), norm(v))                            # rotation preserves length


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
