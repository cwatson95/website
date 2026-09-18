"""Tests for RE-09 tensor calculus on manifolds.

Run directly:   python3 test_covariant_derivative.py   (-> "All N tests passed.")
Or with pytest: pytest test_covariant_derivative.py

These are property-based tests of real differential geometry, with LOOSE
tolerances because every quantity is a finite-difference of the metric:
  * flat (Minkowski) Christoffels vanish, so nabla reduces to the plain partial;
  * the sphere Christoffels match their closed forms (and our re-export matches
    MA-17's `diffgeo.christoffel`);
  * the Levi-Civita connection is metric-compatible (nabla g = 0) on the sphere
    AND the (flat-but-curvy-coordinates) plane-polar metric;
  * great circles are geodesics on the sphere, circles of latitude are not;
  * parallel transport round a closed lat-long loop rotates a vector by the
    enclosed area (Gauss-Bonnet holonomy, K=1), reverses sign with the loop
    orientation, vanishes for a zero-area loop, and preserves the vector's
    g-length.
"""
import math

from covariant_derivative import (
    minkowski_metric, christoffel,
    covariant_derivative_vector, covariant_derivative_covector,
    parallel_transport, geodesic_acceleration, metric_compatibility,
)
import diffgeo  # MA-17 (on sys.path via covariant_derivative); reference metrics


def _approx(x, y, tol=1e-4):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _partial(field, x, i, eps=1e-5):
    """Plain (non-covariant) component-wise partial d_i field, central diff."""
    xp, xm = list(x), list(x)
    xp[i] += eps
    xm[i] -= eps
    fp, fm = field(xp), field(xm)
    return [(fp[k] - fm[k]) / (2 * eps) for k in range(len(fp))]


def _ortho_angle(theta0, Vi, Vf):
    """Signed rotation angle between tangent vectors at sphere colatitude theta0,
    in the orthonormal frame (e_theta = d_theta, e_phi = d_phi / sin theta0)."""
    a = (Vi[0], Vi[1] * math.sin(theta0))
    b = (Vf[0], Vf[1] * math.sin(theta0))
    return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])


def _lat_long_loop(theta0, dtheta, dphi):
    """Closed rectangular loop in (theta, phi): east, south, west, north, back."""
    return [[theta0, 0.0], [theta0, dphi],
            [theta0 + dtheta, dphi], [theta0 + dtheta, 0.0], [theta0, 0.0]]


# --- the connection -----------------------------------------------------------

def test_christoffel_reexport_matches_ma17():
    # christoffel() is a thin re-export of MA-17's diffgeo.christoffel
    g = diffgeo.sphere_metric(1.0)
    x = [0.9, 0.3]
    A, B = christoffel(g, x), diffgeo.christoffel(g, x)
    assert all(_approx(A[k][i][j], B[k][i][j], 1e-12)
               for k in range(2) for i in range(2) for j in range(2))


def test_flat_christoffels_vanish():
    # the Minkowski metric is constant -> every Christoffel symbol is zero
    G = christoffel(minkowski_metric(), [0.3, 1.0, -0.5, 2.0])
    assert all(abs(G[k][i][j]) < 1e-9
               for k in range(4) for i in range(4) for j in range(4))


def test_sphere_christoffels_match_closed_form():
    # unit sphere, g = diag(1, sin^2 theta).  Index order Gam[k][i][j] = Gamma^k_ij.
    g = diffgeo.sphere_metric(1.0)
    for th in (0.7, 1.0, 1.9):
        G = christoffel(g, [th, 0.4])
        cot = math.cos(th) / math.sin(th)
        assert _approx(G[0][1][1], -math.sin(th) * math.cos(th))   # Gamma^th_phiphi
        assert _approx(G[1][0][1], cot)                            # Gamma^phi_thetaphi
        assert _approx(G[1][1][0], cot)                            # symmetric in lower pair
        # all other components vanish on the round sphere
        for (k, i, j) in [(0, 0, 0), (0, 0, 1), (0, 1, 0),
                          (1, 0, 0), (1, 1, 1)]:
            assert abs(G[k][i][j]) < 1e-4


# --- the covariant derivative -------------------------------------------------

def test_flat_covariant_derivative_reduces_to_partial():
    # with Gamma = 0, nabla_i V^k = d_i V^k exactly (vector AND covector forms)
    eta = minkowski_metric()
    Vfield = lambda x: [x[1] * x[1], math.sin(x[0]), x[2] * x[3], 2.0]
    Wfield = lambda x: [math.cos(x[3]), x[0] * x[2], x[1] ** 3, x[0] + x[1]]
    x0 = [0.3, 1.0, -0.5, 2.0]
    MV = covariant_derivative_vector(eta, Vfield, x0)
    MW = covariant_derivative_covector(eta, Wfield, x0)
    for i in range(4):
        dV, dW = _partial(Vfield, x0, i), _partial(Wfield, x0, i)
        for k in range(4):
            assert _approx(MV[i][k], dV[k], 1e-6)
            assert _approx(MW[i][k], dW[k], 1e-6)


def test_metric_compatibility_on_sphere_and_plane():
    # nabla g = 0 is the DEFINING property of the Levi-Civita connection
    sph = diffgeo.sphere_metric(1.0)
    pol = diffgeo.plane_polar_metric()
    for x in ([0.7, 1.1], [1.0, 0.4], [1.9, 0.2]):
        assert metric_compatibility(sph, x) < 1e-6
    for x in ([0.8, 2.0], [1.5, 0.0], [3.0, 0.5]):
        assert metric_compatibility(pol, x) < 1e-6
    # ... and on flat Minkowski (trivially, since g is constant)
    assert metric_compatibility(minkowski_metric(), [0.1, 0.2, 0.3, 0.4]) < 1e-9


# --- geodesics ----------------------------------------------------------------

def test_geodesic_great_circle_vs_latitude():
    g = diffgeo.sphere_metric(1.0)
    # equator (theta = pi/2) traversed in phi is a great circle -> zero accel
    eq = geodesic_acceleration(g, [math.pi / 2, 0.0], [0.0, 1.0])
    assert abs(eq[0]) < 1e-6 and abs(eq[1]) < 1e-6
    # a circle of latitude theta != pi/2 is NOT a geodesic:
    #   x_ddot^theta = sin(theta) cos(theta) * phidot^2  (nonzero), x_ddot^phi = 0
    for th in (0.7, 1.0, 1.3):
        for phidot in (1.0, 2.0):
            lat = geodesic_acceleration(g, [th, 0.0], [0.0, phidot])
            assert _approx(lat[0], math.sin(th) * math.cos(th) * phidot ** 2)
            assert abs(lat[1]) < 1e-6
            assert abs(lat[0]) > 0.05            # genuinely nonzero acceleration


# --- parallel transport, holonomy, metric-compatible transport ----------------

def test_holonomy_equals_enclosed_area():
    g = diffgeo.sphere_metric(1.0)
    for (th0, dth, dphi) in [(1.0, 0.3, 0.3), (0.9, 0.4, 0.5), (1.2, 0.25, 0.25)]:
        loop = _lat_long_loop(th0, dth, dphi)
        Vf = parallel_transport(g, [1.0, 0.0], loop, steps=400)
        angle = _ortho_angle(th0, [1.0, 0.0], Vf)
        area = (math.cos(th0) - math.cos(th0 + dth)) * dphi     # int sin(th) dth dphi
        # holonomy angle MAGNITUDE = enclosed area = int K dA (K = 1 here)
        assert abs(abs(angle) - area) < 0.03 * area
        # the angle is a genuine rotation defect, not finite-difference noise
        assert abs(angle) > 0.5 * area


def test_holonomy_sign_flips_with_orientation_and_vanishes_for_zero_area():
    g = diffgeo.sphere_metric(1.0)
    th0, dth, dphi = 1.0, 0.3, 0.3
    fwd = _lat_long_loop(th0, dth, dphi)
    rev = list(reversed(fwd))
    a_fwd = _ortho_angle(th0, [1.0, 0.0], parallel_transport(g, [1.0, 0.0], fwd, steps=400))
    a_rev = _ortho_angle(th0, [1.0, 0.0], parallel_transport(g, [1.0, 0.0], rev, steps=400))
    # reversing the loop negates the holonomy (orientation dependence)
    assert a_fwd * a_rev < 0.0
    assert abs(a_fwd + a_rev) < 0.05 * abs(a_fwd)
    # an out-and-back path along a meridian encloses zero area -> no holonomy,
    # and the vector returns essentially unchanged
    degen = [[th0, 0.0], [th0 + 0.5, 0.0], [th0, 0.0]]
    Vf = parallel_transport(g, [1.0, 0.0], degen, steps=400)
    assert abs(_ortho_angle(th0, [1.0, 0.0], Vf)) < 1e-3
    assert _approx(Vf[0], 1.0, 1e-6) and abs(Vf[1]) < 1e-6


def test_parallel_transport_preserves_g_length():
    # metric-compatible transport keeps the vector's length constant; round a
    # closed loop the base point is unchanged, so compare with the same metric
    g = diffgeo.sphere_metric(1.0)
    th0 = 1.0
    gb = g([th0, 0.0])
    loop = _lat_long_loop(th0, 0.3, 0.3)
    for V0 in ([1.0, 0.0], [0.7, 1.3], [-0.4, 2.0]):
        Vf = parallel_transport(g, V0, loop, steps=400)
        n0 = sum(gb[i][j] * V0[i] * V0[j] for i in range(2) for j in range(2))
        nf = sum(gb[i][j] * Vf[i] * Vf[j] for i in range(2) for j in range(2))
        assert _approx(nf, n0, 1e-2)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
