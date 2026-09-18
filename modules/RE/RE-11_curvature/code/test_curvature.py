"""Tests for RE-11 curvature.

Run directly:   python3 test_curvature.py        (-> "All N tests passed.")
Or with pytest: pytest test_curvature.py

Curvature is computed by MA-17's finite-difference Riemann tensor, so the GR
tests use loose relative tolerances. The headline checks: flat space has zero
curvature; the 2-sphere has constant R = 2/a^2; Schwarzschild is Ricci-flat
(vacuum) yet has Kretschmann K = 48 M^2/r^6 (real curvature); and positive
curvature focuses geodesics.
"""
import math

from curvature import (
    riemann, ricci, ricci_scalar, gaussian_curvature_2d,
    einstein_tensor, kretschmann, geodesic_deviation,
    minkowski_metric, schwarzschild_metric, sphere_metric,
)
import diffgeo  # MA-17 (on sys.path via curvature)

TOL = 1e-9


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _three_sphere(a=1.0):
    """3-sphere of radius a in (chi, theta, phi): scalar curvature R = 6/a^2."""
    return lambda x: [[a * a, 0.0, 0.0],
                      [0.0, a * a * math.sin(x[0]) ** 2, 0.0],
                      [0.0, 0.0, a * a * math.sin(x[0]) ** 2 * math.sin(x[1]) ** 2]]


def test_flat_space_has_zero_curvature():
    mink = minkowski_metric()
    x = [0.3, 1.0, 1.0, 0.5]
    R = riemann(mink, x)
    assert all(abs(R[a][b][c][d]) <= 1e-9
               for a in range(4) for b in range(4) for c in range(4) for d in range(4))
    Ric = ricci(mink, x)
    assert all(abs(Ric[i][j]) <= 1e-9 for i in range(4) for j in range(4))
    assert abs(ricci_scalar(mink, x)) <= 1e-9
    assert abs(kretschmann(mink, x)) <= 1e-9
    G = einstein_tensor(mink, x)
    assert all(abs(G[i][j]) <= 1e-9 for i in range(4) for j in range(4))


def test_sphere_has_constant_curvature():
    for a in (1.0, 2.0, 0.5):
        s = sphere_metric(a)
        for pt in ([0.7, 0.0], [1.3, 2.0], [2.0, 1.0]):
            assert _approx(ricci_scalar(s, pt), 2.0 / (a * a), 1e-2)   # R = 2/a^2
            assert _approx(gaussian_curvature_2d(s, pt), 1.0 / (a * a), 1e-2)  # K = 1/a^2
        # in 2D the Einstein tensor vanishes identically
        G = einstein_tensor(s, [1.1, 0.4])
        assert all(abs(G[i][j]) <= 1e-2 for i in range(2) for j in range(2))


def test_schwarzschild_is_a_vacuum_solution():
    """R_uv = 0 for r > 2M -- Schwarzschild solves the vacuum Einstein equations."""
    sch = schwarzschild_metric(1.0)
    for r in (4.0, 6.0, 10.0, 20.0):
        x = [0.0, r, 1.2, 0.7]
        Ric = ricci(sch, x)
        assert all(abs(Ric[i][j]) <= 1e-4 for i in range(4) for j in range(4))
        assert abs(ricci_scalar(sch, x)) <= 1e-4
        G = einstein_tensor(sch, x)
        assert all(abs(G[i][j]) <= 1e-4 for i in range(4) for j in range(4))


def test_schwarzschild_kretschmann_is_48M2_over_r6():
    """Curvature is REAL even though R_uv = 0: K = 48 M^2/r^6 distinguishes the
    r=0 singularity from the r=2M coordinate horizon."""
    M = 1.0
    sch = schwarzschild_metric(M)
    Ks = []
    for r in (4.0, 6.0, 10.0):
        K = kretschmann(sch, [0.0, r, 1.0, 0.9])
        assert _approx(K, 48.0 * M * M / r ** 6, 2e-2)
        Ks.append((r, K))
    # scales as 1/r^6
    (r1, K1), (r2, K2) = Ks[0], Ks[2]
    assert _approx(K1 / K2, (r2 / r1) ** 6, 3e-2)


def test_einstein_trace_identity():
    """g^{uv} G_{uv} = (1 - n/2) R. In 2D it is 0; in 3D it is -R/2."""
    # 2-sphere (n=2): trace = 0
    s2 = sphere_metric(1.0)
    g2 = s2([1.1, 0.5]); gi2 = diffgeo.metric_inverse(g2)
    G2 = einstein_tensor(s2, [1.1, 0.5])
    tr2 = sum(gi2[i][j] * G2[i][j] for i in range(2) for j in range(2))
    assert abs(tr2) <= 1e-2
    # 3-sphere (n=3): R = 6/a^2, trace = -R/2 = -3
    s3 = _three_sphere(1.0)
    x3 = [1.0, 1.2, 0.6]
    assert _approx(ricci_scalar(s3, x3), 6.0, 2e-2)
    g3 = s3(x3); gi3 = diffgeo.metric_inverse(g3)
    G3 = einstein_tensor(s3, x3)
    tr3 = sum(gi3[i][j] * G3[i][j] for i in range(3) for j in range(3))
    R3 = ricci_scalar(s3, x3)
    assert _approx(tr3, (1.0 - 3.0 / 2.0) * R3, 3e-2)         # = -R/2


def test_geodesic_deviation_flat_and_focusing():
    # flat space: no tidal acceleration
    mink = minkowski_metric()
    A = geodesic_deviation(mink, [0.0, 1.0, 1.0, 0.5], [1.0, 0.2, 0.0, 0.0], [0.0, 0.0, 1.0, 0.0])
    assert all(abs(c) <= 1e-9 for c in A)
    # 2-sphere: positive curvature focuses geodesics (A . xi < 0), with the exact
    # value A^theta = -sin^2(theta) for u=(0,1), xi=(1,0)
    for theta in (0.6, 1.0, 1.4):
        s = sphere_metric(1.0)
        A = geodesic_deviation(s, [theta, 0.0], [0.0, 1.0], [1.0, 0.0])
        assert _approx(A[0], -math.sin(theta) ** 2, 1e-2)
        assert A[0] < 0.0                                     # focusing


def test_riemann_antisymmetry():
    """R^a_{bcd} = -R^a_{bdc} (antisymmetric in the last pair) on the sphere."""
    s = sphere_metric(1.3)
    R = riemann(s, [1.0, 0.7])
    n = 2
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    assert _approx(R[a][b][c][d], -R[a][b][d][c], 1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
