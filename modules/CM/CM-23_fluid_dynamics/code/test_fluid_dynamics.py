"""Tests for CM-23 fluid dynamics. Reuses MA-02 (imported transitively).

Run:  python3 test_fluid_dynamics.py     ->  "All N tests passed."
"""
from fluid_dynamics import vorticity, is_incompressible, is_irrotational, bernoulli_constant


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-4):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_rigid_rotation_vorticity():
    Omega = 1.5
    v = lambda x, y, z: (-Omega * y, Omega * x, 0.0)
    for p in ((1, 0, 0), (0.5, 2.0, -1.0)):
        assert _vapprox(vorticity(v)(*p), (0.0, 0.0, 2 * Omega))   # omega = 2 Omega z-hat
    assert is_incompressible(v)                                    # div = 0
    assert not is_irrotational(v)                                  # it rotates


def test_shear_flow_vorticity():
    v = lambda x, y, z: (y, 0.0, 0.0)                              # simple shear
    assert _vapprox(vorticity(v)(0.5, 0.5, 0.0), (0.0, 0.0, -1.0))  # curl_z = -1
    assert is_incompressible(v)


def test_potential_flow_is_irrotational():
    v = lambda x, y, z: (2 * x, -2 * y, 0.0)                       # v = grad(x^2 - y^2)
    assert is_irrotational(v)                                      # curl of a gradient = 0
    assert is_incompressible(v)                                    # Laplacian of x^2-y^2 = 0


def test_source_flow_is_compressible():
    v = lambda x, y, z: (x, y, z)                                  # radial source, div = 3
    assert not is_incompressible(v)
    assert is_irrotational(v)                                      # still curl-free


def test_bernoulli():
    # along a streamline the constant is the same; speed up <-> pressure drop
    g = 9.81
    b1 = bernoulli_constant(2.0, 1.0e5, 1000.0, 0.0, g)
    # if it rises 5 m and pressure adjusts so the constant matches, speed must change
    assert _approx(bernoulli_constant(2.0, 1.0e5, 1000.0, 0.0, g),
                   0.5 * 4.0 + 1.0e5 / 1000.0 + 0.0)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
