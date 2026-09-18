"""
RE-11  Curvature  --  Riemann & Ricci tensors, the Einstein tensor, the
Kretschmann scalar, and geodesic deviation (tidal forces = curvature).

Part of the physics topic network (see modules/topic_network.txt, module RE-11).
Prerequisites: RE-09 (tensor calculus on manifolds), ~MA-17 (Riemann/Ricci).
Feeds into: ~RE-12 (geodesics), ~RE-13 (Einstein field equations), ~RE-14
(Schwarzschild), ~RE-16 (gravitational waves).  This module is the GR-curvature
toolkit the later RE modules import.

THE ONE IDEA.  The connection Γ (RE-09) can be made to vanish at any single point
(the equivalence principle, RE-10) -- so Γ itself is not the gravitational field.
What CANNOT be transformed away is its *derivative*: the Riemann tensor
        R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma}
                              + Gamma^rho_{mu lam}Gamma^lam_{nu sigma}
                              - Gamma^rho_{nu lam}Gamma^lam_{mu sigma}.
R = 0 everywhere  <=>  spacetime is flat  <=>  gravity is a coordinate artefact.
The physical, frame-independent face of curvature is **geodesic deviation**:
nearby free-fallers accelerate relative to one another by
        D^2 xi^a / dtau^2 = -R^a_{bcd} u^b xi^c u^d ,
i.e. **tidal forces ARE the Riemann tensor** (the irreducible field of RE-10 §6).

This module *uses MA-17* (`diffgeo`) for the heavy lifting -- it re-exports
`riemann`/`ricci`/`ricci_scalar` and adds the GR-specific contractions
(`einstein_tensor`, `kretschmann`, `geodesic_deviation`) plus the reference
metrics (`minkowski_metric`, `schwarzschild_metric`).  A metric is a callable
`x -> g(x)` (a matrix), matching MA-17; everything works in any dimension and
signature.  Geometrized units G = c = 1.
"""

import os
import sys
import math

# --- consume MA-17 (differential geometry) by relative path (cf. RE-05->MA-16) -
_MA17 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "MA", "MA-17_differential_geometry", "code")
if _MA17 not in sys.path:
    sys.path.insert(0, _MA17)
import diffgeo  # MA-17: christoffel, riemann, ricci, ricci_scalar, metric_inverse, ...

__all__ = [
    "riemann", "ricci", "ricci_scalar", "gaussian_curvature_2d",
    "einstein_tensor", "kretschmann", "geodesic_deviation",
    "minkowski_metric", "schwarzschild_metric", "sphere_metric",
]

# --- re-exports from MA-17 (the curvature tensors live there) -----------------
riemann = diffgeo.riemann                    # R^rho_{sig mu nu} = R[rho][sig][mu][nu]
ricci = diffgeo.ricci                        # R_{sig nu}
ricci_scalar = diffgeo.ricci_scalar          # R = g^{sig nu} R_{sig nu}
gaussian_curvature_2d = diffgeo.gaussian_curvature_2d   # K = R/2 (2-surfaces)
sphere_metric = diffgeo.sphere_metric        # round 2-sphere, K = 1/a^2


# --- the Einstein tensor ------------------------------------------------------

def einstein_tensor(metric, x, **kw):
    """Einstein tensor  G_{mu nu} = R_{mu nu} - 1/2 R g_{mu nu}  -- the LHS of the
    field equations (RE-13).  Its vanishing is the vacuum equation: Schwarzschild
    has G = 0.  Trace:  g^{mu nu} G_{mu nu} = (1 - n/2) R  in n dimensions."""
    g = metric(x)
    n = len(x)
    Ric = diffgeo.ricci(metric, x, **kw)
    R = diffgeo.ricci_scalar(metric, x, **kw)
    return [[Ric[i][j] - 0.5 * R * g[i][j] for j in range(n)] for i in range(n)]


# --- the Kretschmann curvature invariant -------------------------------------

def kretschmann(metric, x, **kw):
    """Kretschmann scalar  K = R_{abcd} R^{abcd}  -- a coordinate-invariant
    measure of curvature.  For Schwarzschild  K = 48 M^2 / r^6: finite at the
    horizon r = 2M (a coordinate singularity) but divergent at r = 0 (the true
    physical singularity).  This is how you tell the two apart."""
    g = metric(x)
    gi = diffgeo.metric_inverse(g)
    n = len(x)
    Rm = diffgeo.riemann(metric, x, **kw)                    # R^a_{bcd}
    # all-lower  R_{abcd} = g_{ae} R^e_{bcd}
    Rd = [[[[sum(g[a][e] * Rm[e][b][c][d] for e in range(n))
             for d in range(n)] for c in range(n)] for b in range(n)] for a in range(n)]
    # all-upper  R^{abcd} = g^{ae} g^{bf} g^{cg} g^{dh} R_{efgh}
    K = 0.0
    for a in range(n):
        for b in range(n):
            for c in range(n):
                for d in range(n):
                    up = 0.0
                    for e in range(n):
                        for f in range(n):
                            for gg in range(n):
                                for h in range(n):
                                    up += (gi[a][e] * gi[b][f] * gi[c][gg] * gi[d][h]
                                           * Rd[e][f][gg][h])
                    K += Rd[a][b][c][d] * up
    return K


# --- geodesic deviation = tidal forces ---------------------------------------

def geodesic_deviation(metric, x, u, xi, **kw):
    """Relative (tidal) 4-acceleration of a neighbouring geodesic:
        A^a = D^2 xi^a / dtau^2 = - R^a_{bcd} u^b xi^c u^d ,
    where u is the 4-velocity of the fiducial geodesic and xi the separation
    vector.  Flat space => A = 0.  Positive curvature (the 2-sphere) FOCUSES
    neighbouring geodesics (A points back toward the fiducial worldline,
    A . xi < 0); this is the geometric content of RE-10's tidal field."""
    n = len(x)
    Rm = diffgeo.riemann(metric, x, **kw)                    # R^a_{bcd}
    return [-sum(Rm[a][b][c][d] * u[b] * xi[c] * u[d]
                 for b in range(n) for c in range(n) for d in range(n))
            for a in range(n)]


# --- reference metrics --------------------------------------------------------

def minkowski_metric():
    """Flat spacetime eta = diag(-1,+1,+1,+1) as a constant metric field.
    Every curvature here is zero."""
    return lambda x: [[-1.0, 0.0, 0.0, 0.0],
                      [0.0, 1.0, 0.0, 0.0],
                      [0.0, 0.0, 1.0, 0.0],
                      [0.0, 0.0, 0.0, 1.0]]


def schwarzschild_metric(M=1.0):
    """Schwarzschild metric (G = c = 1) in (t, r, theta, phi):
        ds^2 = -(1-2M/r) dt^2 + (1-2M/r)^{-1} dr^2 + r^2 dOmega^2.
    Vacuum solution of Einstein's equations: R_{mu nu} = 0 for r > 2M.
    Horizon at r = 2M; curvature singularity at r = 0."""
    def g(x):
        t, r, th, ph = x
        f = 1.0 - 2.0 * M / r
        return [[-f, 0.0, 0.0, 0.0],
                [0.0, 1.0 / f, 0.0, 0.0],
                [0.0, 0.0, r * r, 0.0],
                [0.0, 0.0, 0.0, r * r * math.sin(th) ** 2]]
    return g


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-11  Curvature -- demo   (curvature tensors via MA-17)")
    print("=" * 56)

    print("\nflat Minkowski -- everything vanishes:")
    mink = minkowski_metric()
    Gm = einstein_tensor(mink, [0.0, 1.0, 1.0, 0.5])
    print("  Einstein tensor max|G| =",
          max(abs(Gm[i][j]) for i in range(4) for j in range(4)),
          " Kretschmann =", kretschmann(mink, [0.0, 1.0, 1.0, 0.5]))

    print("\n2-sphere radius a -- constant curvature R = 2/a^2:")
    for a in (1.0, 2.0):
        s = sphere_metric(a)
        print("  a=%.1f: R = %.4f  (=2/a^2=%.4f),  K_Gauss = %.4f (=1/a^2)"
              % (a, ricci_scalar(s, [1.0, 0.5]), 2.0 / a / a,
                 gaussian_curvature_2d(s, [1.0, 0.5])))

    print("\nSchwarzschild (M=1) -- VACUUM: R_uv = 0, but curvature is real:")
    sch = schwarzschild_metric(1.0)
    for r in (10.0, 6.0, 4.0):
        x = [0.0, r, 1.2, 0.7]
        Ric = ricci(sch, x)
        ricmax = max(abs(Ric[i][j]) for i in range(4) for j in range(4))
        K = kretschmann(sch, x)
        print("  r=%4.1f M: max|R_uv|=%.2e (~0, vacuum)  K=%.4e  (48/r^6=%.4e)"
              % (r, ricmax, K, 48.0 / r ** 6))

    print("\ngeodesic deviation -- the 2-sphere FOCUSES parallel geodesics:")
    s = sphere_metric(1.0)
    x = [1.0, 0.0]                       # (theta, phi)
    u = [0.0, 1.0]                       # moving in phi
    xi = [1.0, 0.0]                      # separated in theta
    A = geodesic_deviation(s, x, u, xi)
    print("  A =", [round(c, 4) for c in A], " A.xi =", round(sum(A[i] * xi[i] for i in range(2)), 4),
          "(<0 => focusing, K>0)")


if __name__ == "__main__":
    _demo()
