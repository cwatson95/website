"""
MA-17  Differential geometry -- differential forms and the exterior derivative
(d^2 = 0, unifying grad/curl/div), and Riemannian curvature: Christoffel symbols,
the Riemann and Ricci tensors, the scalar/Gaussian curvature. The headline
computation: the curvature of a surface FROM ITS METRIC ALONE (2-sphere -> K = 1,
flat plane -> K = 0) -- Gauss's Theorema Egregium, made numerical.

Part of the physics topic network (modules/topic_network.txt, module MA-17 [adv]).
Builds on ~MA-16 (tensors, the metric) and ~MA-02 (grad/curl/div); it IS the math
of ~RE-09..RE-13 (general relativity: curvature = gravity).

Pure Python, dependency-free. Forms are realized concretely in R^3 (d on a
0/1/2-form = grad/curl/div); curvature is computed from a callable metric g(x) by
nested central differences. Tolerances are loose enough to absorb the numerical
differentiation yet tight enough to nail K = 1 on the unit sphere.
"""

import math

__all__ = [
    "partial", "gradient", "curl", "divergence",
    "metric_inverse", "christoffel", "riemann", "ricci", "ricci_scalar",
    "gaussian_curvature_2d", "sphere_metric", "plane_polar_metric",
]


# --- exterior derivative in R^3:  d on 0/1/2-forms = grad / curl / div --------

def partial(f, x, i, eps=1e-6):
    """Partial derivative df/dx_i by central difference."""
    xp, xm = list(x), list(x)
    xp[i] += eps
    xm[i] -= eps
    return (f(xp) - f(xm)) / (2 * eps)


def gradient(f):
    """d of a 0-form: returns the field x -> grad f (a 1-form's components)."""
    return lambda x: [partial(f, x, i) for i in range(len(x))]


def curl(V):
    """d of a 1-form in R^3: returns x -> curl V (a 2-form, via the Hodge dual)."""
    def c(x):
        comp = lambda k, xx: V(xx)[k]
        dV = [[partial(lambda xx: comp(k, xx), x, j) for j in range(3)] for k in range(3)]
        return [dV[2][1] - dV[1][2], dV[0][2] - dV[2][0], dV[1][0] - dV[0][1]]
    return c


def divergence(V):
    """d of a 2-form in R^3: returns x -> div V (a 3-form / scalar density)."""
    return lambda x: sum(partial(lambda xx: V(xx)[k], x, k) for k in range(3))


# --- Riemannian curvature from a metric --------------------------------------

def metric_inverse(g):
    """Inverse of a small square matrix by Gauss-Jordan."""
    n = len(g)
    M = [list(g[i]) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for col in range(n):
        piv = max(range(col, n), key=lambda r: abs(M[r][col]))
        M[col], M[piv] = M[piv], M[col]
        d = M[col][col]
        M[col] = [v / d for v in M[col]]
        for r in range(n):
            if r != col:
                f = M[r][col]
                M[r] = [a - f * b for a, b in zip(M[r], M[col])]
    return [row[n:] for row in M]


def _dg(metric, x, l, eps):
    """d g_ij / d x^l  (a matrix)."""
    xp, xm = list(x), list(x)
    xp[l] += eps
    xm[l] -= eps
    gp, gm = metric(xp), metric(xm)
    n = len(x)
    return [[(gp[i][j] - gm[i][j]) / (2 * eps) for j in range(n)] for i in range(n)]


def christoffel(metric, x, eps=1e-5):
    """Christoffel symbols of the second kind
       Gamma^k_ij = 1/2 g^{kl} (d_i g_jl + d_j g_il - d_l g_ij).
    Returns Gam[k][i][j]."""
    n = len(x)
    gi = metric_inverse(metric(x))
    dg = [_dg(metric, x, l, eps) for l in range(n)]          # dg[l][i][j] = d_l g_ij
    Gam = [[[0.0] * n for _ in range(n)] for _ in range(n)]
    for k in range(n):
        for i in range(n):
            for j in range(n):
                s = 0.0
                for l in range(n):
                    s += gi[k][l] * (dg[i][j][l] + dg[j][i][l] - dg[l][i][j])
                Gam[k][i][j] = 0.5 * s
    return Gam


def _dchristoffel(metric, x, m, eps_out, eps_in):
    xp, xm = list(x), list(x)
    xp[m] += eps_out
    xm[m] -= eps_out
    Gp = christoffel(metric, xp, eps_in)
    Gm = christoffel(metric, xm, eps_in)
    n = len(x)
    return [[[(Gp[k][i][j] - Gm[k][i][j]) / (2 * eps_out)
              for j in range(n)] for i in range(n)] for k in range(n)]


def riemann(metric, x, eps_out=1e-3, eps_in=1e-5):
    """Riemann curvature tensor
       R^rho_{sigma mu nu} = d_mu Gamma^rho_{nu sigma} - d_nu Gamma^rho_{mu sigma}
                             + Gamma^rho_{mu lam} Gamma^lam_{nu sigma}
                             - Gamma^rho_{nu lam} Gamma^lam_{mu sigma}.
    Returns R[rho][sigma][mu][nu]."""
    n = len(x)
    Gam = christoffel(metric, x, eps_in)
    dGam = [_dchristoffel(metric, x, m, eps_out, eps_in) for m in range(n)]   # dGam[m][k][i][j]
    R = [[[[0.0] * n for _ in range(n)] for _ in range(n)] for _ in range(n)]
    for rho in range(n):
        for sig in range(n):
            for mu in range(n):
                for nu in range(n):
                    t = dGam[mu][rho][nu][sig] - dGam[nu][rho][mu][sig]
                    for lam in range(n):
                        t += Gam[rho][mu][lam] * Gam[lam][nu][sig]
                        t -= Gam[rho][nu][lam] * Gam[lam][mu][sig]
                    R[rho][sig][mu][nu] = t
    return R


def ricci(metric, x, **kw):
    """Ricci tensor R_{sigma nu} = R^rho_{sigma rho nu} (contract 1st & 3rd)."""
    n = len(x)
    R = riemann(metric, x, **kw)
    return [[sum(R[rho][sig][rho][nu] for rho in range(n)) for nu in range(n)] for sig in range(n)]


def ricci_scalar(metric, x, **kw):
    """Scalar curvature R = g^{sigma nu} R_{sigma nu}."""
    n = len(x)
    gi = metric_inverse(metric(x))
    Ric = ricci(metric, x, **kw)
    return sum(gi[s][v] * Ric[s][v] for s in range(n) for v in range(n))


def gaussian_curvature_2d(metric, x, **kw):
    """Gaussian curvature of a 2-surface: K = R / 2 (scalar curvature)."""
    return 0.5 * ricci_scalar(metric, x, **kw)


# --- reference metrics -------------------------------------------------------

def sphere_metric(a=1.0):
    """Round 2-sphere of radius a in (theta, phi): g = diag(a^2, a^2 sin^2 theta).
    Constant Gaussian curvature K = 1/a^2."""
    return lambda x: [[a * a, 0.0], [0.0, a * a * math.sin(x[0]) ** 2]]


def plane_polar_metric():
    """The flat plane in polar coordinates: g = diag(1, r^2). K = 0 (it is flat --
    curvature is intrinsic, not an artifact of curvy coordinates)."""
    return lambda x: [[1.0, 0.0], [0.0, x[0] ** 2]]


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-17 differential geometry -- demo")
    print("=" * 37)

    print("\nexterior derivative, d^2 = 0  in R^3:")
    f = lambda x: math.sin(x[0]) * x[1] + x[2] ** 2          # a scalar 0-form
    V = lambda x: [x[1] * x[2], x[0] * x[2], x[0] * x[1]]    # a vector 1-form
    p = [0.6, -0.4, 0.9]
    cg = curl(gradient(f))(p)
    dc = divergence(curl(V))(p)
    print(f"  curl(grad f) = {[round(c,8) for c in cg]}   (= 0:  d(d f) = 0)")
    print(f"  div(curl V)  = {dc:.8f}                       (= 0:  d(d V) = 0)")

    print("\nGaussian curvature from the metric alone (Theorema Egregium):")
    for a in (1.0, 2.0):
        g = sphere_metric(a)
        for th in (0.7, 1.2, 1.9):
            K = gaussian_curvature_2d(g, [th, 0.3])
            print(f"  sphere radius {a}, theta={th}:  K = {K:.5f}   (exact 1/a^2 = {1/a**2:.5f})")
    Kp = gaussian_curvature_2d(plane_polar_metric(), [1.5, 0.0])
    print(f"  flat plane (polar) at r=1.5:    K = {Kp:.5f}   (exact 0)")


if __name__ == "__main__":
    _demo()
