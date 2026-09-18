"""Tests for MA-17 differential geometry. Pure stdlib.

Run:  python3 test_diffgeo.py     ->  "All N tests passed."
"""
import math

from diffgeo import (
    gradient, curl, divergence,
    metric_inverse, christoffel, ricci_scalar, gaussian_curvature_2d,
    sphere_metric, plane_polar_metric,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_d_squared_is_zero():
    # curl(grad f) = 0 and div(curl V) = 0  --  the exterior derivative is nilpotent
    fs = [lambda x: math.sin(x[0]) * x[1] + x[2] ** 2,
          lambda x: math.exp(x[0]) * math.cos(x[1]) - x[2],
          lambda x: x[0] * x[1] * x[2]]
    Vs = [lambda x: [x[1] * x[2], x[0] * x[2], x[0] * x[1]],
          lambda x: [math.sin(x[1]), math.cos(x[2]), x[0] ** 2]]
    pts = [[0.6, -0.4, 0.9], [1.0, 0.5, -0.3]]
    for p in pts:
        for f in fs:
            assert all(abs(c) < 1e-4 for c in curl(gradient(f))(p))
        for V in Vs:
            assert abs(divergence(curl(V))(p)) < 1e-4


def test_grad_curl_div_values():
    # grad of x*y*z, curl of a known field, div of a radial field
    f = lambda x: x[0] * x[1] * x[2]
    g = gradient(f)([2.0, 3.0, 4.0])
    assert _approx(g[0], 12.0, tol=1e-4) and _approx(g[1], 8.0, tol=1e-4) and _approx(g[2], 6.0, tol=1e-4)
    # div of r = (x,y,z) is 3
    assert _approx(divergence(lambda x: [x[0], x[1], x[2]])([1.0, 2.0, 3.0]), 3.0, tol=1e-4)
    # curl of (-y, x, 0) is (0, 0, 2)
    c = curl(lambda x: [-x[1], x[0], 0.0])([0.5, 0.5, 0.5])
    assert _approx(c[2], 2.0, tol=1e-4) and abs(c[0]) < 1e-4 and abs(c[1]) < 1e-4


def test_metric_inverse():
    g = [[2.0, 1.0], [1.0, 3.0]]
    gi = metric_inverse(g)
    prod = [[sum(g[i][k] * gi[k][j] for k in range(2)) for j in range(2)] for i in range(2)]
    assert _approx(prod[0][0], 1.0) and _approx(prod[1][1], 1.0)
    assert abs(prod[0][1]) < 1e-9 and abs(prod[1][0]) < 1e-9


def test_christoffel_sphere():
    # unit sphere: Gamma^theta_phiphi = -sin th cos th,  Gamma^phi_thetaphi = cot th
    g = sphere_metric(1.0)
    th = 0.9
    Gam = christoffel(g, [th, 0.3])
    assert _approx(Gam[0][1][1], -math.sin(th) * math.cos(th), tol=1e-4)   # ^theta_phiphi
    assert _approx(Gam[1][0][1], math.cos(th) / math.sin(th), tol=1e-4)    # ^phi_thetaphi
    assert _approx(Gam[1][1][0], math.cos(th) / math.sin(th), tol=1e-4)    # symmetric in lower


def test_sphere_curvature_is_one_over_a2():
    # the showcase: K = 1/a^2 everywhere on the round sphere, from the metric alone
    for a in (1.0, 2.0, 0.5):
        g = sphere_metric(a)
        for th in (0.6, 1.0, 1.5, 2.1):
            K = gaussian_curvature_2d(g, [th, 0.4])
            assert _approx(K, 1.0 / a ** 2, tol=1e-2)
        # scalar curvature R = 2K = 2/a^2
        assert _approx(ricci_scalar(g, [1.0, 0.4]), 2.0 / a ** 2, tol=1e-2)


def test_plane_is_flat():
    # the plane in polar coordinates is FLAT despite the r^2 in the metric
    g = plane_polar_metric()
    for r in (0.8, 1.5, 3.0):
        assert abs(gaussian_curvature_2d(g, [r, 0.0])) < 1e-2


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
