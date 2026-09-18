"""
RE-17  Exact solutions & numerical relativity  --  the exact-solution landscape
*beyond* Schwarzschild (Kerr, Reissner-Nordstrom, de Sitter), validated as
solutions of the field equations by feeding each metric back to RE-11's
curvature engine, plus the 3+1 / ADM split that begins numerical relativity.

Part of the physics topic network (see modules/topic_network.txt, module RE-17
[adv]).  Prerequisites: RE-11 (curvature -- imported here), RE-13 (Einstein
equations), RE-14 (Schwarzschild).  Capstone of the GR portion of the RE trunk.

THE ONE IDEA.  An "exact solution" is a metric g(x) for which the Einstein
equations hold *identically*.  We do not solve them here -- we WRITE DOWN three
famous metrics and CHECK them, by handing each to RE-11's finite-difference
`ricci` / `einstein_tensor`:

  * Kerr (rotating, vacuum)            R_{mu nu} = 0          (verify_vacuum ~ 0)
  * de Sitter (Lambda-vacuum)          G_{mu nu} + Lambda g_{mu nu} = 0
  * Reissner-Nordstrom (charged)       R_{mu nu} != 0  (sourced by the EM field)

The vacuum check is the validator: if a Kerr component were wrong, R_{mu nu}
would NOT vanish and the test would fail.  Then the move to NUMERICAL relativity:
most spacetimes (a binary merger) have no closed form, so we foliate spacetime
into spatial slices -- the 3+1 / ADM decomposition (lapse alpha, shift beta^i,
spatial metric gamma_ij, extrinsic curvature K_ij) -- and split Einstein's
equations into CONSTRAINTS on each slice and EVOLUTION forward in time.  Initial
data must satisfy the Hamiltonian constraint R^(3) + K^2 - K_ij K^ij = 16 pi rho.

This module *imports RE-11* (`curvature`, which itself pulls in MA-17 `diffgeo`)
and adds nothing to the curvature machinery -- it only supplies metrics and the
3+1 algebra.  A metric is a callable `x -> g(x)` (a matrix), matching RE-11.
Geometrized units G = c = 1; signature mostly-plus (-,+,+,+).
"""

import os
import sys
import math

# --- consume RE-11 (curvature) by relative path (cf. RE-11 -> MA-17) ----------
_RE11 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-11_curvature", "code")
if _RE11 not in sys.path:
    sys.path.insert(0, _RE11)
import curvature                  # RE-11: ricci, einstein_tensor, ricci_scalar, ...
import diffgeo                    # MA-17: metric_inverse (on sys.path via curvature)

__all__ = [
    "kerr_metric", "reissner_nordstrom_metric", "de_sitter_metric",
    "verify_vacuum", "verify_einstein_lambda",
    "kerr_horizons", "kerr_ergosphere",
    "adm_decompose", "spatial_slice_metric", "hamiltonian_constraint_flat",
]


# =============================================================================
# 1.  Exact vacuum / electrovac / Lambda-vacuum metrics (Boyer-Lindquist etc.)
# =============================================================================

def kerr_metric(M=1.0, a=0.0):
    """Kerr metric (rotating, uncharged black hole) in Boyer-Lindquist
    coordinates x = (t, r, theta, phi), G = c = 1, signature (-,+,+,+):

        Sigma = r^2 + a^2 cos^2(theta),   Delta = r^2 - 2 M r + a^2,
        ds^2 = -(1 - 2 M r / Sigma) dt^2
               - (4 M a r sin^2(theta) / Sigma) dt dphi
               + (Sigma / Delta) dr^2 + Sigma dtheta^2
               + (r^2 + a^2 + 2 M a^2 r sin^2(theta)/Sigma) sin^2(theta) dphi^2 .

    a = J/M is the spin per unit mass.  This is a VACUUM solution: R_{mu nu} = 0
    (checked by `verify_vacuum`).  a -> 0 recovers Schwarzschild exactly; a > M
    is a naked singularity (no horizon -- see `kerr_horizons`).  The g_{t phi}
    cross term is frame dragging; g_{tt} changes sign at the ergosphere."""
    def g(x):
        t, r, th, ph = x
        s2 = math.sin(th) ** 2
        Sigma = r * r + a * a * math.cos(th) ** 2
        Delta = r * r - 2.0 * M * r + a * a
        g_tt = -(1.0 - 2.0 * M * r / Sigma)
        g_tph = -2.0 * M * a * r * s2 / Sigma
        g_rr = Sigma / Delta
        g_thth = Sigma
        g_phph = (r * r + a * a + 2.0 * M * a * a * r * s2 / Sigma) * s2
        return [[g_tt, 0.0, 0.0, g_tph],
                [0.0,  g_rr, 0.0, 0.0],
                [0.0,  0.0,  g_thth, 0.0],
                [g_tph, 0.0, 0.0, g_phph]]
    return g


def reissner_nordstrom_metric(M=1.0, Q=0.0):
    """Reissner-Nordstrom metric (a static, charged black hole) in (t,r,theta,phi):

        f(r) = 1 - 2 M / r + Q^2 / r^2,
        ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 (dtheta^2 + sin^2 theta dphi^2).

    NOT a vacuum solution: it is sourced by the electromagnetic stress-energy of
    the central charge Q (forward-ref EM-14), so R_{mu nu} != 0 -- but the EM
    stress-energy is trace-free, so the Ricci SCALAR R = 0.  Q -> 0 recovers
    Schwarzschild.  Horizons where f = 0: r_pm = M +- sqrt(M^2 - Q^2)."""
    def g(x):
        t, r, th, ph = x
        f = 1.0 - 2.0 * M / r + Q * Q / (r * r)
        return [[-f, 0.0, 0.0, 0.0],
                [0.0, 1.0 / f, 0.0, 0.0],
                [0.0, 0.0, r * r, 0.0],
                [0.0, 0.0, 0.0, r * r * math.sin(th) ** 2]]
    return g


def de_sitter_metric(Lambda):
    """de Sitter spacetime (the maximally symmetric Lambda-vacuum) in the static
    patch, coordinates (t, r, theta, phi):

        f(r) = 1 - Lambda r^2 / 3,
        ds^2 = -f dt^2 + f^{-1} dr^2 + r^2 (dtheta^2 + sin^2 theta dphi^2).

    Solves G_{mu nu} + Lambda g_{mu nu} = 0 (the vacuum equations WITH a
    cosmological constant) -- checked by `verify_einstein_lambda`.  It has
    constant curvature: R_{mu nu} = Lambda g_{mu nu} and Ricci scalar R = 4 Lambda
    in 4-D.  A cosmological horizon sits at r = sqrt(3/Lambda) (where f = 0);
    Lambda < 0 (anti-de Sitter) has no horizon."""
    def g(x):
        t, r, th, ph = x
        f = 1.0 - Lambda * r * r / 3.0
        return [[-f, 0.0, 0.0, 0.0],
                [0.0, 1.0 / f, 0.0, 0.0],
                [0.0, 0.0, r * r, 0.0],
                [0.0, 0.0, 0.0, r * r * math.sin(th) ** 2]]
    return g


# =============================================================================
# 2.  Validators -- feed a metric to RE-11 and read off the field equation
# =============================================================================

def verify_vacuum(metric, x, **kw):
    """max |R_{mu nu}| at x via RE-11's `ricci`.  ~ 0 for a vacuum solution
    (Kerr, Schwarzschild).  THIS is the correctness gate on `kerr_metric`: a
    wrong component makes the Ricci tensor non-zero and the test fails."""
    Ric = curvature.ricci(metric, x, **kw)
    n = len(x)
    return max(abs(Ric[i][j]) for i in range(n) for j in range(n))


def verify_einstein_lambda(metric, x, Lambda, **kw):
    """max |G_{mu nu} + Lambda g_{mu nu}| at x.  ~ 0 for a Lambda-vacuum solution
    (de Sitter), i.e. it solves G_{mu nu} + Lambda g_{mu nu} = 0."""
    G = curvature.einstein_tensor(metric, x, **kw)
    g = metric(x)
    n = len(x)
    return max(abs(G[i][j] + Lambda * g[i][j]) for i in range(n) for j in range(n))


# =============================================================================
# 3.  Kerr structure -- horizons, ergosphere
# =============================================================================

def kerr_horizons(M, a):
    """Boyer-Lindquist horizons of Kerr (roots of Delta = r^2 - 2Mr + a^2 = 0):
        r_minus = M - sqrt(M^2 - a^2),   r_plus = M + sqrt(M^2 - a^2).
    Returns (r_minus, r_plus).  Real iff a <= M (a = M is extremal); for a > M
    there is no horizon -- a naked ring singularity -- and we raise ValueError."""
    disc = M * M - a * a
    if disc < 0.0:
        raise ValueError("a > M: no horizon (naked singularity); Delta has no real root")
    root = math.sqrt(disc)
    return (M - root, M + root)


def kerr_ergosphere(M, a, theta):
    """Outer boundary of the ergosphere (the static limit surface, where
    g_{tt} = 0):  r_E(theta) = M + sqrt(M^2 - a^2 cos^2(theta)).
    At the equator (theta = pi/2) r_E = 2M, strictly OUTSIDE the horizon r_plus
    for a > 0 -- the gap between them is the ergoregion, where no observer can
    remain static (frame dragging is total) yet escape is still possible."""
    return M + math.sqrt(M * M - a * a * math.cos(theta) ** 2)


# =============================================================================
# 4.  The 3+1 / ADM decomposition  (Baumgarte-Shapiro Ch.2)
# =============================================================================

def adm_decompose(metric, x):
    """Split a 4-metric at a point into ADM (3+1) pieces, foliating on x[0]=t:

        g_{mu nu} = [ -alpha^2 + beta_k beta^k    beta_j ]
                    [        beta_i               gamma_ij ]

    Returns (alpha, beta_up, gamma):
      * alpha  = 1 / sqrt(-g^{00})   -- the LAPSE (proper time per coord time),
                 read from the time-time component of the INVERSE metric;
      * beta_up[i] = gamma^{ij} g_{0j}   -- the SHIFT vector beta^i;
      * gamma  = g_{ij}  (the spatial i,j block)  -- the SPATIAL METRIC.

    For Minkowski in inertial coordinates: alpha = 1, beta = 0, gamma = delta_ij."""
    g = metric(x)
    n = len(x)
    gi = diffgeo.metric_inverse(g)
    alpha = 1.0 / math.sqrt(-gi[0][0])
    gamma = [[g[i][j] for j in range(1, n)] for i in range(1, n)]
    gamma_inv = diffgeo.metric_inverse(gamma)
    beta_low = [g[0][i] for i in range(1, n)]               # beta_i = g_{0i}
    beta_up = [sum(gamma_inv[i][j] * beta_low[j] for j in range(n - 1))
               for i in range(n - 1)]
    return alpha, beta_up, gamma


def spatial_slice_metric(metric, t=0.0):
    """The spatial 3-metric gamma_ij(y) of the t = const slice as a *callable* of
    the spatial coordinates y = x[1:], so RE-11's curvature engine can act on it
    (e.g. to get the intrinsic 3-curvature R^(3) of the slice)."""
    def gamma(y):
        x = [t] + list(y)
        g = metric(x)
        n = len(g)
        return [[g[i][j] for j in range(1, n)] for i in range(1, n)]
    return gamma


def hamiltonian_constraint_flat(metric, x, K_ij=None, rho=0.0, **kw):
    """Hamiltonian-constraint residual on the t = const slice through x:

        H = R^(3) + K^2 - K_ij K^ij - 16 pi rho ,

    where R^(3) is the INTRINSIC scalar curvature of the spatial metric gamma_ij
    (RE-11 `ricci_scalar` on `spatial_slice_metric`), K = gamma^{ij} K_ij is the
    mean curvature, and rho is the energy density.  Initial data are admissible
    only if H = 0.  K_ij defaults to None = the time-symmetric (moment-of-time-
    symmetry) case K_ij = 0, for which H reduces to R^(3) - 16 pi rho.

    H ~ 0 for a flat Minkowski slice (R^(3) = 0, K = 0).  It also vanishes for the
    t = const Schwarzschild slice: that 3-geometry is curved but SCALAR-FLAT
    (R^(3) = 0), exactly as a time-symmetric vacuum slice must be."""
    t = x[0]
    y = list(x[1:])
    gamma = spatial_slice_metric(metric, t)
    R3 = curvature.ricci_scalar(gamma, y, **kw)
    m = len(y)
    if K_ij is None:
        Ktr = 0.0
        KK = 0.0
    else:
        gi = diffgeo.metric_inverse(gamma(y))
        Ktr = sum(gi[i][j] * K_ij[i][j] for i in range(m) for j in range(m))
        KK = sum(gi[i][k] * gi[j][l] * K_ij[i][j] * K_ij[k][l]
                 for i in range(m) for j in range(m)
                 for k in range(m) for l in range(m))
    return R3 + Ktr * Ktr - KK - 16.0 * math.pi * rho


# =============================================================================
# demo
# =============================================================================

def _maxabs(A):
    return max(abs(A[i][j]) for i in range(len(A)) for j in range(len(A[0])))


def _demo():
    print("RE-17  Exact solutions & numerical relativity -- demo")
    print("=" * 56)
    print("(every field equation below is CHECKED by RE-11's curvature engine)")

    print("\n[1] Kerr (M=1) -- VACUUM (R_uv = 0), rotating: a -> 0 = Schwarzschild")
    for a in (0.0, 0.5, 0.9):
        kerr = kerr_metric(1.0, a)
        x = [0.0, 8.0, 1.0, 0.7]
        rm, rp = kerr_horizons(1.0, a)
        print("  a=%.1f: max|R_uv|(r=8) = %.2e   horizons r-=%.3f r+=%.3f   "
              "ergo(eq)=%.3f" % (a, verify_vacuum(kerr, x), rm, rp,
                                 kerr_ergosphere(1.0, a, math.pi / 2)))

    print("\n[2] de Sitter -- Lambda-vacuum: G_uv + Lambda g_uv = 0, R = 4 Lambda")
    for Lam in (0.01, 0.03):
        ds = de_sitter_metric(Lam)
        x = [0.0, 3.0, 1.0, 0.7]
        print("  Lambda=%.2f: max|G+Lg| = %.2e   R = %.5f   (4 Lambda = %.5f)"
              % (Lam, verify_einstein_lambda(ds, x, Lam),
                 curvature.ricci_scalar(ds, x), 4.0 * Lam))

    print("\n[3] Reissner-Nordstrom (M=1) -- NOT vacuum (EM-sourced), R = 0 (trace-free)")
    for Q in (0.0, 0.5, 0.9):
        rn = reissner_nordstrom_metric(1.0, Q)
        x = [0.0, 3.0, 1.0, 0.7]
        Ric = curvature.ricci(rn, x)
        print("  Q=%.1f: max|R_uv| = %.3e   R(scalar) = %.3e"
              % (Q, _maxabs(Ric), curvature.ricci_scalar(rn, x)))

    print("\n[4] ADM 3+1 split")
    mink = curvature.minkowski_metric()
    alpha, beta, gamma = adm_decompose(mink, [0.0, 1.0, 1.0, 0.5])
    print("  Minkowski (inertial): alpha = %.4f, beta = %s, gamma diag = %s"
          % (alpha, [round(b, 3) for b in beta],
             [round(gamma[i][i], 3) for i in range(3)]))
    H = hamiltonian_constraint_flat(mink, [0.0, 1.0, 1.0, 0.5])
    print("  Hamiltonian constraint (flat slice, K=0):   H = %.2e" % H)
    sch = curvature.schwarzschild_metric(1.0)
    Hs = hamiltonian_constraint_flat(sch, [0.0, 6.0, 1.0, 0.7])
    print("  Hamiltonian constraint (Schwarzschild slice, K=0): H = %.2e"
          "   (R^(3) ~ 0: curved but SCALAR-flat)" % Hs)


if __name__ == "__main__":
    _demo()
