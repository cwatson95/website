"""
RE-12  Geodesics & the variational principle  --  the worldlines of free fall.
The geodesic equation, its derivation as the Euler-Lagrange equation of the
action, maximal-aging (longest proper time), and conserved quantities from
Killing symmetries.

Part of the physics topic network (see modules/topic_network.txt, module RE-12).
Prerequisites: RE-11 (curvature -- Christoffel/Riemann), ~MA-13 (calculus of
variations: Euler-Lagrange), ~MA-17 (differential geometry: christoffel).  Feeds
into: ~RE-14 (Schwarzschild orbits), and is bridge B1's relativity terminus
(MA-13 -> CM-17 -> CM-21 -> RE-12: one variational idea across four trunks).

THE ONE IDEA.  A geodesic is the spacetime version of a straight line, and it has
TWO equivalent faces that coincide for the Levi-Civita connection:
  * STRAIGHTEST -- it parallel-transports its own tangent,  u^nu D_nu u^mu = 0,
    which in an affine parameter is the geodesic equation
        d2x^mu/dlam2  +  Gamma^mu_{nu rho} (dx^nu/dlam)(dx^rho/dlam)  =  0 ;
  * EXTREMAL -- it extremizes the action  delta * integral ds = 0.
Extremizing S = integral (1/2) g_{mu nu} xdot^mu xdot^nu dlam via the
Euler-Lagrange equations (MA-13) REPRODUCES exactly the Christoffel symbols --
the slick way to read off Gamma (`euler_lagrange_gives_christoffel`).

This module *uses MA-17* (`diffgeo.christoffel`) for the geodesic right-hand side
and *uses MA-13* (`variational.euler_lagrange_residual`) to demonstrate the
variational <=> Christoffel equivalence numerically.  A metric is a callable
`x -> g(x)` (a matrix), matching RE-11 / MA-17; everything works in any dimension
and signature.  Geometrized units G = c = 1; signature mostly-plus.
"""

import os
import sys
import math

# --- consume MA-17 (differential geometry) by relative path (cf. RE-11) --------
_MA17 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-17_differential_geometry", "code")
if _MA17 not in sys.path:
    sys.path.insert(0, _MA17)
import diffgeo  # MA-17: christoffel, metric_inverse, sphere_metric, ...

# --- consume MA-13 (calculus of variations) by relative path -------------------
_MA13 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-13_calculus_of_variations", "code")
if _MA13 not in sys.path:
    sys.path.insert(0, _MA13)
import variational  # MA-13: euler_lagrange_residual, functional, beltrami, ...

__all__ = [
    "geodesic_rhs", "integrate_geodesic", "lagrangian", "action_length",
    "euler_lagrange_gives_christoffel", "is_geodesic", "killing_conserved",
    "minkowski_metric", "schwarzschild_metric", "sphere_metric",
]

# the round 2-sphere lives in MA-17 (constant curvature K = 1/a^2)
sphere_metric = diffgeo.sphere_metric


# --- the geodesic equation ----------------------------------------------------

def geodesic_rhs(metric, x, xdot, **kw):
    """Right-hand side of the geodesic equation in an affine parameter:
        xddot^k  =  - Gamma^k_{ij} xdot^i xdot^j
    (the relative acceleration that keeps the tangent parallel-transported).
    Uses MA-17's `christoffel`.  Flat space => Gamma = 0 => xddot = 0 (straight
    lines).  Returns the acceleration vector xddot."""
    n = len(x)
    Gam = diffgeo.christoffel(metric, x, **kw)            # Gam[k][i][j] = Gamma^k_{ij}
    return [-sum(Gam[k][i][j] * xdot[i] * xdot[j]
                 for i in range(n) for j in range(n))
            for k in range(n)]


def integrate_geodesic(metric, x0, xdot0, dtau, steps, **kw):
    """RK4-integrate the geodesic worldline from (x0, xdot0) for `steps` steps of
    affine-parameter size `dtau`.  The second-order geodesic equation is written
    as the first-order system  d/dlam (x, xdot) = (xdot, geodesic_rhs).
    Returns a list of (x, xdot) states (length steps+1, including the start)."""
    n = len(x0)
    x, v = list(x0), list(xdot0)
    traj = [(list(x), list(v))]

    def deriv(xx, vv):
        return list(vv), geodesic_rhs(metric, xx, vv, **kw)

    for _ in range(steps):
        k1x, k1v = deriv(x, v)
        k2x, k2v = deriv([x[i] + 0.5 * dtau * k1x[i] for i in range(n)],
                         [v[i] + 0.5 * dtau * k1v[i] for i in range(n)])
        k3x, k3v = deriv([x[i] + 0.5 * dtau * k2x[i] for i in range(n)],
                         [v[i] + 0.5 * dtau * k2v[i] for i in range(n)])
        k4x, k4v = deriv([x[i] + dtau * k3x[i] for i in range(n)],
                         [v[i] + dtau * k3v[i] for i in range(n)])
        x = [x[i] + dtau / 6.0 * (k1x[i] + 2 * k2x[i] + 2 * k3x[i] + k4x[i]) for i in range(n)]
        v = [v[i] + dtau / 6.0 * (k1v[i] + 2 * k2v[i] + 2 * k3v[i] + k4v[i]) for i in range(n)]
        traj.append((list(x), list(v)))
    return traj


# --- the geodesic Lagrangian and the action / arc length ----------------------

def lagrangian(metric, x, xdot):
    """Affine-parameter geodesic Lagrangian  L = (1/2) g_{mu nu} xdot^mu xdot^nu.
    Its Euler-Lagrange equation (MA-13) IS the geodesic equation -- and along an
    affine geodesic L itself is constant (= -1/2 timelike, 0 null, +1/2 spacelike,
    when xdot is unit-normalised), since 2L = g_{mu nu}xdot^mu xdot^nu = xdot.xdot."""
    g = metric(x)
    n = len(x)
    return 0.5 * sum(g[i][j] * xdot[i] * xdot[j] for i in range(n) for j in range(n))


def action_length(metric, path):
    """Arc length / proper time along a sampled path:
        S = sum_segments sqrt(| g_{mu nu} dx^mu dx^nu |),
    with g taken at each segment midpoint.  For a timelike worldline this is the
    proper time tau (RE-05); the mostly-plus signature makes |.| pick out -ds^2.
    The geodesic EXTREMIZES this -- maximally for timelike paths (`maximal
    aging')."""
    n = len(path[0])
    total = 0.0
    for k in range(len(path) - 1):
        dx = [path[k + 1][i] - path[k][i] for i in range(n)]
        xm = [0.5 * (path[k + 1][i] + path[k][i]) for i in range(n)]
        g = metric(xm)
        s2 = sum(g[i][j] * dx[i] * dx[j] for i in range(n) for j in range(n))
        total += math.sqrt(abs(s2))
    return total


# --- the variational principle reproduces the Christoffel symbols -------------

def euler_lagrange_gives_christoffel(metric, x, xdot, eps=1e-3):
    """The geodesic equation IS the Euler-Lagrange equation of `lagrangian`.

    For each coordinate mu we build the reduced 1-D Lagrangian  L_mu(lam, y, p)
    that equals L with x^mu->y, xdot^mu->p and the OTHER coordinates advanced at
    constant velocity x^nu + xdot^nu lam.  MA-13's `euler_lagrange_residual`,
    evaluated on that constant-velocity (zero-acceleration) trial, returns
        R_mu = dL/dx^mu - d/dlam (dL/dxdot^mu)|_{xddot=0}
             = (1/2) d_mu g_{ab} xdot^a xdot^b - d_a g_{mu b} xdot^a xdot^b
             = g_{mu b} xddot^b              (the Euler-Lagrange equation),
    so contracting with the inverse metric recovers the acceleration
        xddot^lam = g^{lam mu} R_mu  ==  -Gamma^lam_{ab} xdot^a xdot^b  ==  geodesic_rhs.
    This is the variational <=> Christoffel equivalence, computed via MA-13.
    Returns xddot (should equal `geodesic_rhs`)."""
    n = len(x)
    gi = diffgeo.metric_inverse(metric(x))
    R = []
    for mu in range(n):
        def L_mu(lam, y, p, mu=mu):
            pos = [x[nu] + xdot[nu] * lam for nu in range(n)]
            pos[mu] = y
            vel = list(xdot)
            vel[mu] = p
            return lagrangian(metric, pos, vel)
        # 3-node constant-velocity trial centred on the current state; the single
        # interior node (lam = 0) carries the Euler-Lagrange residual R_mu.
        lams = [-eps, 0.0, eps]
        ys = [x[mu] - xdot[mu] * eps, x[mu], x[mu] + xdot[mu] * eps]
        R.append(variational.euler_lagrange_residual(L_mu, lams, ys)[0])
    return [sum(gi[lam][mu] * R[mu] for mu in range(n)) for lam in range(n)]


# --- testing whether a sampled path is a geodesic -----------------------------

def is_geodesic(metric, path, dtau=1.0, tol=1e-2):
    """True if a uniformly-sampled `path` satisfies the geodesic equation
        xddot^k + Gamma^k_{ij} xdot^i xdot^j ~ 0
    at every interior node, with xdot, xddot estimated by central differences in
    the affine parameter (spacing `dtau`).  Loose `tol` absorbs the differencing.
    E.g. the sphere's equator is a geodesic (great circle); a circle of latitude
    theta != pi/2 is NOT."""
    n = len(path[0])
    for k in range(1, len(path) - 1):
        v = [(path[k + 1][i] - path[k - 1][i]) / (2.0 * dtau) for i in range(n)]
        a = [(path[k + 1][i] - 2.0 * path[k][i] + path[k - 1][i]) / (dtau * dtau)
             for i in range(n)]
        rhs = geodesic_rhs(metric, path[k], v)            # = -Gamma v v
        scale = 1.0 + max(abs(c) for c in v) ** 2
        if any(abs(a[i] - rhs[i]) > tol * scale for i in range(n)):
            return False
    return True


# --- conserved quantities from Killing vectors --------------------------------

def killing_conserved(metric, killing_vec, x, xdot):
    """Quantity conserved along a geodesic when xi is a Killing vector (a symmetry
    of the metric):  Q = p . xi = g_{mu nu} xi^mu xdot^nu  (= xi_nu xdot^nu).
    A symmetry direction gives a constant of motion -- on the sphere xi = d_phi
    gives angular momentum L = g_{phi phi} phidot; on Schwarzschild xi = d_t gives
    energy E = g_{tt} tdot.  `killing_vec` may be a constant vector or a callable
    x -> xi(x)."""
    xi = killing_vec(x) if callable(killing_vec) else killing_vec
    g = metric(x)
    n = len(x)
    return sum(g[i][j] * xi[i] * xdot[j] for i in range(n) for j in range(n))


# --- reference metrics (G = c = 1, mostly-plus) -------------------------------

def minkowski_metric():
    """Flat spacetime eta = diag(-1,+1,+1,+1) as a constant metric field.  Every
    Christoffel symbol vanishes, so geodesics are straight lines xdot = const."""
    return lambda x: [[-1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]


def schwarzschild_metric(M=1.0):
    """Schwarzschild metric in (t, r, theta, phi):
        ds^2 = -(1-2M/r) dt^2 + (1-2M/r)^{-1} dr^2 + r^2 dOmega^2.
    Its timelike geodesics are the orbits of RE-14; d_t and d_phi are Killing, so
    energy E = (1-2M/r) tdot and angular momentum L = r^2 sin^2(theta) phidot are
    conserved along them."""
    def g(x):
        t, r, th, ph = x
        f = 1.0 - 2.0 * M / r
        return [[-f, 0.0, 0.0, 0.0],
                [0.0, 1.0 / f, 0.0, 0.0],
                [0.0, 0.0, r * r, 0.0],
                [0.0, 0.0, 0.0, r * r * math.sin(th) ** 2]]
    return g


# --- demo ---------------------------------------------------------------------

def _demo():
    print("RE-12  Geodesics & the variational principle -- demo")
    print("=" * 52)

    print("\nflat Minkowski -- a geodesic is a straight line (xddot = 0):")
    mink = minkowski_metric()
    x0, v0 = [0.0, 0.0, 0.0, 0.0], [1.25, 0.3, -0.2, 0.1]
    traj = integrate_geodesic(mink, x0, v0, dtau=0.5, steps=8)
    xend, vend = traj[-1]
    dv = max(abs(vend[i] - v0[i]) for i in range(4))
    print("  start v =", v0)
    print("  end   v =", [round(c, 6) for c in vend], "  max|dv| = %.2e (velocity constant)" % dv)
    print("  end   x =", [round(c, 4) for c in xend], " (= v*4 exactly)")

    print("\n2-sphere -- the equator is a great-circle geodesic, a latitude is not:")
    s = sphere_metric(1.0)
    equator = [[math.pi / 2, 0.2 * k] for k in range(9)]
    latitude = [[1.0, 0.2 * k] for k in range(9)]          # theta = 1.0 != pi/2
    print("  is_geodesic(equator)  =", is_geodesic(s, equator, dtau=0.2))
    print("  is_geodesic(latitude) =", is_geodesic(s, latitude, dtau=0.2), " (theta=1.0)")
    eq = integrate_geodesic(s, [math.pi / 2, 0.0], [0.0, 1.0], dtau=0.2, steps=10)
    dtheta = max(abs(st[0][0] - math.pi / 2) for st in eq)
    print("  integrate equator: max|theta - pi/2| = %.2e (stays on the great circle)" % dtheta)

    print("\nvariational <=> Christoffel: E-L of the action reproduces -Gamma v v:")
    for name, met, x, v in [
        ("sphere", sphere_metric(1.0), [1.1, 0.5], [0.4, 0.9]),
        ("Schwarzschild", schwarzschild_metric(1.0), [0.0, 8.0, math.pi / 2, 0.3], [1.0, 0.1, 0.05, 0.04]),
    ]:
        a_el = euler_lagrange_gives_christoffel(met, x, v)
        a_g = geodesic_rhs(met, x, v)
        d = max(abs(a_el[i] - a_g[i]) for i in range(len(x)))
        print("  %-13s max|EL - geodesic_rhs| = %.2e" % (name, d))

    print("\nmaximal aging -- the inertial (geodesic) twin ages the most:")
    T = 10.0
    straight = [[T * k / 20, 0.0, 0.0, 0.0] for k in range(21)]
    bent = [[T * k / 20, 3.0 * (1 - abs(1 - k / 10.0)), 0.0, 0.0] for k in range(21)]
    print("  straight (geodesic) proper time tau = %.4f" % action_length(mink, straight))
    print("  bent     (turn-around) proper time  = %.4f  (shorter -> younger)"
          % action_length(mink, bent))

    print("\nKilling conservation along an integrated geodesic:")
    tilt = integrate_geodesic(sphere_metric(1.0), [math.pi / 2, 0.0], [0.35, 1.0], dtau=0.15, steps=40)
    Ls = [killing_conserved(sphere_metric(1.0), [0.0, 1.0], st[0], st[1]) for st in tilt]
    print("  sphere d_phi -> L = sin^2(th) phidot: spread = %.2e (conserved)"
          % (max(Ls) - min(Ls)))
    sch = schwarzschild_metric(1.0)
    orb = integrate_geodesic(sch, [0.0, 10.0, math.pi / 2, 0.0], [1.2, 0.2, 0.0, 0.04], dtau=0.2, steps=60)
    rs = [st[0][1] for st in orb]
    Es = [killing_conserved(sch, [1.0, 0.0, 0.0, 0.0], st[0], st[1]) for st in orb]
    print("  Schwarzschild d_t -> E = -(1-2M/r) tdot: spread = %.2e over r in [%.2f, %.2f]"
          % (max(Es) - min(Es), min(rs), max(rs)))


if __name__ == "__main__":
    _demo()
