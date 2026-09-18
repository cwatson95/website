"""Tests for CM-22 continuity equation. Reuses MA-02 (imported transitively).

Run:  python3 test_continuum_mechanics.py     ->  "All N tests passed."
"""
import math

from continuum_mechanics import continuity_residual, material_derivative, divergence_of_velocity


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_travelling_wave_conserves_mass():
    # rho = f(x - c t) advected at uniform velocity c satisfies continuity exactly
    c = 0.5
    rho = lambda x, y, z, t: math.exp(-(x - c * t) ** 2)
    v = lambda x, y, z, t: (c, 0.0, 0.0)
    for (x, t) in ((0.3, 1.0), (1.0, 0.5), (-0.5, 2.0), (2.0, 0.0)):
        assert _approx(continuity_residual(rho, v, x, 0, 0, t), 0.0, tol=1e-4)


def test_incompressible_constant_density():
    rho = lambda x, y, z, t: 2.0                            # constant
    v = lambda x, y, z, t: (-y, x, 0.0)                     # rigid rotation, div v = 0
    for (x, y) in ((1.0, 0.0), (0.5, 2.0), (-1.0, 1.0)):
        assert _approx(continuity_residual(rho, v, x, y, 0, 0), 0.0, tol=1e-4)
        assert _approx(divergence_of_velocity(v, x, y, 0, 0), 0.0, tol=1e-5)


def test_material_form_equals_eulerian():
    # d rho/dt + div(rho v)  ==  D rho/Dt + rho div v   (an identity), for a compressible flow
    rho = lambda x, y, z, t: 2.0 + 0.3 * x + 0.1 * t
    v = lambda x, y, z, t: (0.5 * x, 0.2 * y, 0.0)
    for (x, y, t) in ((1.3, 0.7, 0.4), (-0.5, 1.0, 1.2)):
        euler = continuity_residual(rho, v, x, y, 0, t)
        material = (material_derivative(rho, v, x, y, 0, t)
                    + rho(x, y, 0, t) * divergence_of_velocity(v, x, y, 0, t))
        assert _approx(euler, material, tol=1e-4)


def test_material_derivative_following_flow():
    # for f constant on fluid elements moving with v, Df/Dt = 0
    # take f = x - c t (advected), v = (c,0,0):  df/dt=-c, v.grad f = c  -> Df/Dt = 0
    c = 0.7
    f = lambda x, y, z, t: x - c * t
    v = lambda x, y, z, t: (c, 0.0, 0.0)
    for (x, t) in ((1.0, 0.0), (0.3, 2.0)):
        assert _approx(material_derivative(f, v, x, 0, 0, t), 0.0, tol=1e-5)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
