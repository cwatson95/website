"""Tests for MA-02 vector calculus. Reuses MA-01 (imported transitively).

Run:  python3 test_vector_calculus.py     ->  "All N tests passed."
"""
import math

from vector_calculus import (
    gradient, divergence, curl, laplacian, directional_derivative,
    line_integral, surface_flux,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_gradient():
    f = lambda x, y, z: x ** 2 + y ** 2 + z ** 2          # grad = (2x,2y,2z)
    g = gradient(f)
    for p in ((1.0, 2.0, 3.0), (-1.0, 0.5, 2.0)):
        assert _vapprox(g(*p), tuple(2.0 * c for c in p), tol=1e-4)


def test_divergence():
    F = lambda x, y, z: (x, y, z)                          # div = 3
    d = divergence(F)
    for p in ((1.0, 1.0, 1.0), (3.0, -2.0, 0.5)):
        assert _approx(d(*p), 3.0, tol=1e-4)


def test_curl():
    F = lambda x, y, z: (-y, x, 0.0)                       # curl = (0,0,2)
    c = curl(F)
    for p in ((1.0, 1.0, 1.0), (2.0, -3.0, 0.5)):
        assert _vapprox(c(*p), (0.0, 0.0, 2.0), tol=1e-4)


def test_laplacian():
    f = lambda x, y, z: x ** 2 + y ** 2 + z ** 2          # lap = 6
    assert _approx(laplacian(f)(1.0, 2.0, 3.0), 6.0, tol=1e-3)
    harmonic = lambda x, y, z: x ** 2 - y ** 2            # lap = 0
    assert _approx(laplacian(harmonic)(2.0, 1.0, 0.0), 0.0, tol=1e-3)


def test_identities():
    f = lambda x, y, z: math.sin(x) * y + z ** 3
    assert _vapprox(curl(gradient(f))(0.4, 1.1, -0.7), (0.0, 0.0, 0.0), tol=1e-3)
    G = lambda x, y, z: (x * y, y * z, z * x)
    assert _approx(divergence(curl(G))(0.7, -0.3, 0.5), 0.0, tol=1e-3)


def test_directional_derivative():
    f = lambda x, y, z: x ** 2 + y ** 2 + z ** 2
    dd = directional_derivative(f, (1.0, 0.0, 0.0))        # = df/dx = 2x
    assert _approx(dd(3.0, 5.0, 1.0), 6.0, tol=1e-4)


def test_stokes_circulation():
    F = lambda x, y, z: (-y, x, 0.0)                       # curl_z = 2
    circle = lambda t: (math.cos(t), math.sin(t), 0.0)
    circ = line_integral(F, circle, 0.0, 2.0 * math.pi)
    assert _approx(circ, 2.0 * math.pi, tol=1e-6)          # = curl_z * (pi r^2) = 2*pi
    assert _approx(circ, 2.0 * (math.pi * 1.0 ** 2), tol=1e-6)


def test_conservative_line_integral():
    # ∫ grad f . dl  from A to B  =  f(B) - f(A)
    f = lambda x, y, z: x * y * z
    F = gradient(f)
    path = lambda t: (t, t, t)                             # (0,0,0) -> (1,1,1)
    val = line_integral(F, path, 0.0, 1.0)
    assert _approx(val, f(1.0, 1.0, 1.0) - f(0.0, 0.0, 0.0), tol=1e-3)


def test_divergence_theorem_flux():
    # flux of F=r through the unit sphere = ∭ div r dV = 3 * (4/3 pi) = 4 pi
    F = lambda x, y, z: (x, y, z)
    sphere = lambda u, v: (math.sin(u) * math.cos(v), math.sin(u) * math.sin(v), math.cos(u))
    flux = surface_flux(F, sphere, 0.0, math.pi, 0.0, 2.0 * math.pi, 60, 60)
    assert _approx(flux, 4.0 * math.pi, tol=1e-2)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
