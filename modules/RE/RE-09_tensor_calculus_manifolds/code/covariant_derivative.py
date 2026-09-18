"""
RE-09  Tensor calculus on manifolds  --  the metric g_{mu nu}(x) as a
position-dependent inner product, the Levi-Civita connection (Christoffel
symbols), the covariant derivative, parallel transport, holonomy, and the
geodesic equation.

Part of the physics topic network (see modules/topic_network.txt, module RE-09).
Prerequisites: RE-08 (covariant formulation -- tensors in flat SR); **~MA-17**
(differential geometry -- the Christoffel/Riemann machinery this module is built
on).  Feeds into: ~RE-10 (equivalence principle: Gammas vanish in a locally
inertial frame), ~RE-11 (curvature = holonomy density), ~RE-12 (geodesics).

THE ONE IDEA.  On a curved manifold the metric varies from point to point, so the
coordinate basis vectors do too.  The plain partial derivative  d_i V^k  is then
*not* a tensor: it mixes the change in V with the change in the basis.  The cure is
the **covariant derivative**, which adds a correction built from the Christoffel
symbols Gamma^k_{ij} (the Levi-Civita connection) to cancel the basis drift:
        nabla_i V^k = d_i V^k + Gamma^k_{ij} V^j           (contravariant)
        nabla_i W_k = d_i W_k - Gamma^j_{ik} W_j           (covariant).
Gamma is fixed uniquely by demanding the connection be metric-compatible
(nabla g = 0) and torsion-free (Gamma symmetric in i,j):
        Gamma^k_{ij} = 1/2 g^{kl} (d_i g_{jl} + d_j g_{il} - d_l g_{ij}).

This module *uses MA-17* for that formula: `christoffel` here is a thin re-export
of `diffgeo.christoffel`.  Everything else -- covariant differentiation, parallel
transport (delta V^k = -Gamma^k_{ij} V^j dx^i), the geodesic acceleration
(x_ddot^k = -Gamma^k_{ij} x_dot^i x_dot^j), and the metric-compatibility check --
is built on top of it by finite differences.

Conventions: indices run 0..n-1; `metric` is a CALLABLE x -> g (a matrix), as in
MA-17.  Christoffels are returned as Gam[k][i][j] = Gamma^k_{ij}.  Pure stdlib
apart from the MA-17 import.
"""

import os
import sys
import math

# --- consume MA-17 (differential geometry) by relative path, like RE-05/MA-16 ---
_MA17 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-17_differential_geometry", "code")
if _MA17 not in sys.path:
    sys.path.insert(0, _MA17)
import diffgeo  # MA-17: christoffel, riemann, ricci, sphere_metric, plane_polar_metric, ...
# (future: swap for `from physkit.diffgeo import ...` once physkit is packaged.)

__all__ = [
    "minkowski_metric", "christoffel",
    "covariant_derivative_vector", "covariant_derivative_covector",
    "parallel_transport", "geodesic_acceleration", "metric_compatibility",
]


# --- a flat reference metric --------------------------------------------------

def minkowski_metric():
    """The flat Minkowski metric eta = diag(-1,+1,+1,+1) as a CONSTANT field
    x -> eta.  Being constant, all d_l g = 0, so every Christoffel vanishes and
    the covariant derivative reduces to the ordinary partial derivative: flat
    spacetime is the curved formalism with the curvature switched off."""
    return lambda x: [[-1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]


# --- the connection (delegated to MA-17) -------------------------------------

def christoffel(metric, x, eps=1e-5):
    """Levi-Civita connection Gamma^k_{ij} = 1/2 g^{kl}(d_i g_jl + d_j g_il -
    d_l g_ij), returned as Gam[k][i][j].  Thin re-export of MA-17's
    `diffgeo.christoffel` -- the UNIQUE connection that is metric-compatible and
    torsion-free.  Not a tensor: it can be made to vanish at any chosen point
    (locally inertial coordinates -- the math face of the equivalence principle,
    RE-10)."""
    return diffgeo.christoffel(metric, x, eps)


# --- the covariant derivative -------------------------------------------------

def covariant_derivative_vector(metric, Vfield, x, eps=1e-5):
    """Covariant derivative of a contravariant vector field:
            nabla_i V^k = d_i V^k + Gamma^k_{ij} V^j .
    `Vfield` is a callable x -> V (the components V^k).  The partial d_i V^k is a
    central finite difference; the Gamma term corrects for the drift of the
    coordinate basis.  Returns the matrix M[i][k] = nabla_i V^k (lower index i =
    the differentiation direction, upper index k = the vector component)."""
    n = len(x)
    Gam = christoffel(metric, x, eps)
    V0 = Vfield(x)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xp, xm = list(x), list(x)
        xp[i] += eps
        xm[i] -= eps
        Vp, Vm = Vfield(xp), Vfield(xm)
        for k in range(n):
            d_iVk = (Vp[k] - Vm[k]) / (2 * eps)
            M[i][k] = d_iVk + sum(Gam[k][i][j] * V0[j] for j in range(n))
    return M


def covariant_derivative_covector(metric, Wfield, x, eps=1e-5):
    """Covariant derivative of a covariant vector (1-form) field:
            nabla_i W_k = d_i W_k - Gamma^j_{ik} W_j .
    Note the MINUS sign and the contracted lower index (cf. the vector case):
    raising/lowering must commute with nabla, which forces the opposite-sign
    correction.  `Wfield` is a callable x -> W (the components W_k).  Returns
    M[i][k] = nabla_i W_k."""
    n = len(x)
    Gam = christoffel(metric, x, eps)
    W0 = Wfield(x)
    M = [[0.0] * n for _ in range(n)]
    for i in range(n):
        xp, xm = list(x), list(x)
        xp[i] += eps
        xm[i] -= eps
        Wp, Wm = Wfield(xp), Wfield(xm)
        for k in range(n):
            d_iWk = (Wp[k] - Wm[k]) / (2 * eps)
            M[i][k] = d_iWk - sum(Gam[j][i][k] * W0[j] for j in range(n))
    return M


# --- parallel transport and holonomy -----------------------------------------

def parallel_transport(metric, V0, path, steps=1, eps=1e-5):
    """Parallel-transport the vector V0 along `path` (a list of waypoints).  At
    each step the vector is dragged so its covariant derivative along the path
    vanishes:
            delta V^k = -Gamma^k_{ij}(x) V^j dx^i        (forward Euler).
    Each consecutive pair of waypoints is subdivided into `steps` Euler sub-steps
    (so a coarse list of corners + a large `steps` integrates accurately; a
    finely sampled path can use steps=1).  Returns the final vector.

    Around a CLOSED loop the result does not equal V0 on a curved manifold: it is
    rotated by the holonomy angle, which equals the integral of the Gaussian
    curvature over the enclosed area (Gauss-Bonnet).  On the unit sphere (K=1)
    that angle equals the enclosed area itself -- curvature made visible (RE-11).
    Parallel transport is metric-compatible, so it preserves the g-length of V."""
    n = len(V0)
    V = list(V0)
    for a, b in zip(path[:-1], path[1:]):
        dx = [(b[d] - a[d]) / steps for d in range(n)]
        for s in range(steps):
            x = [a[d] + (b[d] - a[d]) * s / steps for d in range(n)]
            Gam = christoffel(metric, x, eps)
            dV = [-sum(Gam[k][i][j] * V[j] * dx[i]
                       for i in range(n) for j in range(n)) for k in range(n)]
            V = [V[k] + dV[k] for k in range(n)]
    return V


# --- the geodesic equation ----------------------------------------------------

def geodesic_acceleration(metric, x, xdot, eps=1e-5):
    """The acceleration that makes a curve a geodesic (a 'straight line' on the
    manifold):  x_ddot^k = -Gamma^k_{ij} x_dot^i x_dot^j.  A geodesic has zero
    covariant acceleration -- it parallel-transports its own tangent.  Feeding
    this to an integrator solves x_ddot^k + Gamma^k_{ij} x_dot^i x_dot^j = 0
    (RE-12: free fall and light bending)."""
    n = len(x)
    Gam = christoffel(metric, x, eps)
    return [-sum(Gam[k][i][j] * xdot[i] * xdot[j]
                 for i in range(n) for j in range(n)) for k in range(n)]


# --- metric compatibility (the defining property of Levi-Civita) -------------

def metric_compatibility(metric, x, eps=1e-5):
    """Numerically evaluate the covariant derivative of the metric tensor,
            nabla_i g_{jk} = d_i g_{jk} - Gamma^l_{ij} g_{lk} - Gamma^l_{ik} g_{jl},
    and return max_|component|.  For the Levi-Civita connection this is ZERO
    everywhere (the connection is built precisely to make it so): lengths and
    angles are preserved by parallel transport.  A nonzero value flags either a
    non-metric connection or finite-difference error."""
    n = len(x)
    Gam = christoffel(metric, x, eps)
    g = metric(x)
    worst = 0.0
    for i in range(n):
        xp, xm = list(x), list(x)
        xp[i] += eps
        xm[i] -= eps
        gp, gm = metric(xp), metric(xm)
        for j in range(n):
            for k in range(n):
                d_igjk = (gp[j][k] - gm[j][k]) / (2 * eps)
                val = (d_igjk
                       - sum(Gam[l][i][j] * g[l][k] for l in range(n))
                       - sum(Gam[l][i][k] * g[j][l] for l in range(n)))
                worst = max(worst, abs(val))
    return worst


# --- demo --------------------------------------------------------------------

def _ortho_angle(theta0, Vi, Vf):
    """Signed rotation angle (radians) between two tangent vectors at sphere
    colatitude theta0, measured in the local orthonormal frame
    (e_theta = d_theta, e_phi = d_phi / sin theta0)."""
    a = (Vi[0], Vi[1] * math.sin(theta0))
    b = (Vf[0], Vf[1] * math.sin(theta0))
    return math.atan2(a[0] * b[1] - a[1] * b[0], a[0] * b[0] + a[1] * b[1])


def _demo():
    print("RE-09  Tensor calculus on manifolds -- demo   (connection via MA-17)")
    print("=" * 67)

    print("\nflat Minkowski: every Christoffel vanishes ->")
    Gflat = christoffel(minkowski_metric(), [0.3, 1.0, -0.5, 2.0])
    print("  max |Gamma^k_ij| = %.2e   (covariant deriv = ordinary partial)"
          % max(abs(Gflat[k][i][j]) for k in range(4) for i in range(4) for j in range(4)))

    print("\nunit 2-sphere Gamma^k_ij at theta=1.0  (g = diag(1, sin^2 theta)):")
    g = diffgeo.sphere_metric(1.0)
    th = 1.0
    Gam = christoffel(g, [th, 0.4])
    print("  Gamma^theta_phiphi = % .5f   (exact -sin cos = % .5f)"
          % (Gam[0][1][1], -math.sin(th) * math.cos(th)))
    print("  Gamma^phi_thetaphi = % .5f   (exact   cot th = % .5f)"
          % (Gam[1][0][1], math.cos(th) / math.sin(th)))

    print("\nmetric compatibility  nabla_i g_jk = 0  (defines Levi-Civita):")
    print("  sphere      max|nabla g| = %.2e" % metric_compatibility(g, [1.0, 0.4]))
    print("  plane-polar max|nabla g| = %.2e"
          % metric_compatibility(diffgeo.plane_polar_metric(), [1.5, 0.0]))

    print("\ngeodesics on the sphere (x_ddot = -Gamma x_dot x_dot, x_dot = d/dphi):")
    eq = geodesic_acceleration(g, [math.pi / 2, 0.0], [0.0, 1.0])
    lat = geodesic_acceleration(g, [1.0, 0.0], [0.0, 1.0])
    print("  equator  theta=pi/2 : accel = [% .4f, % .4f]   (great circle -> 0)" % tuple(eq))
    print("  latitude theta=1.0  : accel = [% .4f, % .4f]   (NOT a geodesic)" % tuple(lat))

    print("\nholonomy: parallel transport round a lat-long loop on the unit sphere")
    th0, dth, dphi = 1.0, 0.3, 0.3
    loop = [[th0, 0.0], [th0, dphi], [th0 + dth, dphi], [th0 + dth, 0.0], [th0, 0.0]]
    Vf = parallel_transport(g, [1.0, 0.0], loop, steps=400)
    angle = _ortho_angle(th0, [1.0, 0.0], Vf)
    area = (math.cos(th0) - math.cos(th0 + dth)) * dphi
    print("  enclosed area (= int K dA, K=1) = %.5f" % area)
    print("  measured holonomy angle         = %.5f   (rotation defect ~ area)" % abs(angle))


if __name__ == "__main__":
    _demo()
