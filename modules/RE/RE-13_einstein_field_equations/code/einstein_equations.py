"""
RE-13  Einstein field equations  --  the stress-energy tensor, the field equation
G_{mu nu} = 8 pi T_{mu nu}, its trace-reversed form, the cosmological constant,
and the Newtonian (weak-field) limit that fixes the coupling 8 pi.

Part of the physics topic network (see modules/topic_network.txt, module RE-13).
Prerequisites: RE-11 (curvature -- the Einstein tensor G_{mu nu}; IMPORTED here)
and RE-12 (geodesics -- "spacetime tells matter how to move").  Cross-links:
~EM-14 (the electromagnetic stress tensor -- the canonical field T_{mu nu}, NOT
imported here, only forward-referenced).  Feeds ~RE-14 (Schwarzschild = vacuum
solution), ~RE-15 (FLRW cosmology -- Friedmann from a perfect fluid), ~QF-05.

THE ONE IDEA.  Spacetime tells matter how to move (geodesics, RE-12); matter tells
spacetime how to curve.  The second half is one equation,
        G_{mu nu} = 8 pi T_{mu nu}        (geometrized units G = c = 1),
the Einstein tensor G = Ric - 1/2 R g (built in RE-11) sourced by the stress-energy
tensor T.  The left side is FORCED to be G (not just the Ricci tensor) by the
contracted Bianchi identity  nabla_mu G^{mu nu} = 0  (RE-11 sec. 3): it makes
nabla_mu T^{mu nu} = 0 -- local energy-momentum conservation -- automatic.  The
coupling 8 pi is then pinned by demanding the weak-field limit reproduce Newton:
G_00 = 2 nabla^2 Phi = 8 pi rho  <=>  Poisson  nabla^2 Phi = 4 pi rho.

This module IMPORTS RE-11 (`curvature`) for the geometry side (einstein_tensor,
ricci, the reference metrics) and adds the *matter* side: the stress-energy tensor
(perfect fluid / dust), the trace-reversed field equation, the field-equation
residual (with Lambda), and the Newtonian limit.  A metric is a callable
x -> g(x); mostly-plus signature (- + + +).  Pure stdlib beyond RE-11.
"""

import os
import sys
import math

# --- consume RE-11 (curvature) by relative path (cf. RE-11 -> MA-17) ----------
_RE11 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-11_curvature", "code")
if _RE11 not in sys.path:
    sys.path.insert(0, _RE11)
import curvature  # RE-11: einstein_tensor, ricci, ricci_scalar, reference metrics

__all__ = [
    "EIGHT_PI",
    "einstein_tensor", "ricci",
    "stress_energy_perfect_fluid", "stress_energy_dust", "rest_four_velocity",
    "trace", "trace_reversed_ricci",
    "field_equation_residual", "newtonian_poisson_residual",
    "minkowski_metric", "schwarzschild_metric", "de_sitter_metric",
]

EIGHT_PI = 8.0 * math.pi

# convenience re-exports of RE-11 reference metrics (so callers need one import)
minkowski_metric = curvature.minkowski_metric
schwarzschild_metric = curvature.schwarzschild_metric


# --- the LHS: Einstein tensor (thin wrappers of RE-11) -----------------------

def einstein_tensor(metric, x, **kw):
    """Einstein tensor  G_{mu nu} = R_{mu nu} - 1/2 R g_{mu nu}  -- the geometry
    side of the field equation.  Delegates to RE-11 `curvature.einstein_tensor`."""
    return curvature.einstein_tensor(metric, x, **kw)


def ricci(metric, x, **kw):
    """Ricci tensor R_{mu nu} (re-exported from RE-11) -- the quantity the
    trace-reversed field equation solves for."""
    return curvature.ricci(metric, x, **kw)


# --- small linear-algebra helpers (pure stdlib) ------------------------------

def _inverse(M):
    """Inverse g^{mu nu} of a small square matrix by Gauss-Jordan."""
    n = len(M)
    A = [list(M[i]) + [1.0 if i == j else 0.0 for j in range(n)] for i in range(n)]
    for c in range(n):
        piv = max(range(c, n), key=lambda r: abs(A[r][c]))
        A[c], A[piv] = A[piv], A[c]
        d = A[c][c]
        A[c] = [v / d for v in A[c]]
        for r in range(n):
            if r != c:
                f = A[r][c]
                A[r] = [a - f * b for a, b in zip(A[r], A[c])]
    return [row[n:] for row in A]


def _lower(g, u):
    """Lower an index with the metric:  u_mu = g_{mu nu} u^nu."""
    n = len(u)
    return [sum(g[mu][nu] * u[nu] for nu in range(n)) for mu in range(n)]


def _to_matrix(T, x, n):
    """Coerce a stress-energy argument to an n x n matrix.  Accepts a matrix, a
    callable x -> matrix, or 0 / None (vacuum -> the zero tensor)."""
    if T is None or (isinstance(T, (int, float)) and T == 0):
        return [[0.0] * n for _ in range(n)]
    return T(x) if callable(T) else T


# --- the RHS: the stress-energy (energy-momentum) tensor ---------------------

def rest_four_velocity(metric, x):
    """4-velocity of an observer at rest in these coordinates:
        u^mu = (1/sqrt(-g_00), 0, ...),   normalized so g_{mu nu} u^mu u^nu = -1.
    In Minkowski this is just (1, 0, 0, 0)."""
    g = metric(x)
    n = len(g)
    u = [0.0] * n
    u[0] = 1.0 / math.sqrt(-g[0][0])
    return u


def stress_energy_perfect_fluid(rho, p, u, metric, x):
    """Perfect-fluid stress-energy tensor (lower indices):
        T_{mu nu} = (rho + p) u_mu u_nu + p g_{mu nu},
    with rho the rest-frame energy density, p the isotropic pressure, and u the
    fluid 4-velocity (u.u = -1, mostly-plus).  No shear/heat flux -- isotropic in
    the rest frame.  Special cases: dust (p = 0), radiation (p = rho/3, traceless),
    vacuum energy (p = -rho).  The source of the Friedmann equations (RE-15)."""
    g = metric(x)
    n = len(u)
    ul = _lower(g, u)                        # u_mu = g_{mu nu} u^nu
    return [[(rho + p) * ul[mu] * ul[nu] + p * g[mu][nu]
             for nu in range(n)] for mu in range(n)]


def stress_energy_dust(rho, u, metric, x):
    """Pressureless dust, the p -> 0 perfect fluid:  T_{mu nu} = rho u_mu u_nu.
    Models cold non-relativistic matter (galaxies, the matter-dominated era)."""
    return stress_energy_perfect_fluid(rho, 0.0, u, metric, x)


def trace(metric, T, x):
    """Scalar trace  T = g^{mu nu} T_{mu nu}.  For a perfect fluid (4-D) it is
    -rho + 3p; dust -> -rho; radiation (p = rho/3) -> 0."""
    g = metric(x)
    n = len(g)
    Tm = _to_matrix(T, x, n)
    gi = _inverse(g)
    return sum(gi[mu][nu] * Tm[mu][nu] for mu in range(n) for nu in range(n))


# --- the field equation and its trace-reversed form --------------------------

def trace_reversed_ricci(metric, T, x):
    """The Ricci tensor demanded by the field equation, in trace-reversed form
        R_{mu nu} = 8 pi (T_{mu nu} - 1/2 T g_{mu nu}),     T = g^{ab} T_{ab}.
    Algebraically equivalent to G_{mu nu} = 8 pi T_{mu nu}: contracting the latter
    gives R = -8 pi T (in 4-D), and substituting back moves the trace onto the
    source.  This is the form you integrate -- its left side is plain Ricci, so a
    vacuum (T = 0) source gives R_{mu nu} = 0 directly."""
    g = metric(x)
    n = len(g)
    Tm = _to_matrix(T, x, n)
    Tr = trace(metric, Tm, x)
    return [[EIGHT_PI * (Tm[mu][nu] - 0.5 * Tr * g[mu][nu])
             for nu in range(n)] for mu in range(n)]


def field_equation_residual(metric, T, x, Lambda=0.0, **kw):
    """Residual of the Einstein field equation (with cosmological constant)
        G_{mu nu} + Lambda g_{mu nu} - 8 pi T_{mu nu}        (= 0 on a solution).
    T may be a matrix, a callable x -> matrix, or 0/None for vacuum.  Examples:
    Schwarzschild with T = 0, Lambda = 0 -> ~0 (vacuum); de Sitter with T = 0,
    Lambda = 3/L^2 -> ~0.  On FLAT space with T = 0 the residual is exactly
    Lambda * eta (because G = 0) -- the simplest window on how Lambda enters."""
    g = metric(x)
    n = len(g)
    G = curvature.einstein_tensor(metric, x, **kw)
    Tm = _to_matrix(T, x, n)
    return [[G[mu][nu] + Lambda * g[mu][nu] - EIGHT_PI * Tm[mu][nu]
             for nu in range(n)] for mu in range(n)]


# --- the Newtonian (weak-field) limit ----------------------------------------

def _laplacian(f, x, h):
    """Flat-space Laplacian  sum_i d^2 f / d x_i^2  by central 2nd differences."""
    n = len(x)
    f0 = f(x)
    s = 0.0
    for i in range(n):
        xp, xm = list(x), list(x)
        xp[i] += h
        xm[i] -= h
        s += (f(xp) - 2.0 * f0 + f(xm)) / (h * h)
    return s


def _weak_field_metric(Phi):
    """Static, isotropic weak-field (Newtonian-gauge) metric  g = eta + h:
        g_00 = -(1 + 2 Phi),   g_ij = (1 - 2 Phi) delta_ij,   Phi = Phi([x,y,z]).
    The time-time part g_00 alone reproduces the Newtonian FORCE on geodesics
    (Gamma^i_00 = +d_i Phi, RE-12); the isotropic SPATIAL perturbation is what
    promotes that to the field-equation statement G_00 = 2 nabla^2 Phi."""
    def g(X):                                # X = (t, x, y, z)
        ph = Phi([X[1], X[2], X[3]])
        a = 1.0 - 2.0 * ph
        return [[-(1.0 + 2.0 * ph), 0.0, 0.0, 0.0],
                [0.0, a, 0.0, 0.0],
                [0.0, 0.0, a, 0.0],
                [0.0, 0.0, 0.0, a]]
    return g


def newtonian_poisson_residual(Phi, x, eps=1e-3, **kw):
    """Weak-field test that the field equation reduces to Newton/Poisson and so
    FIXES the coupling 8 pi.  Build the static weak-field metric g = eta + h for
    the potential Phi (a function of the spatial point [x,y,z]), form G_00
    numerically via RE-11, and return
        G_00 - 2 nabla^2 Phi.
    In this limit G_00 = 2 nabla^2 Phi, so with G_00 = 8 pi T_00 = 8 pi rho a
    vanishing residual is exactly Poisson's equation nabla^2 Phi = 4 pi rho -- the
    statement that the coupling had to be 8 pi.  Pass a smooth Phi of small
    amplitude (e.g. a Gaussian lump); LOOSE tolerance (finite-difference curvature
    on top of a near-flat metric)."""
    g = _weak_field_metric(Phi)
    X = [0.0, x[0], x[1], x[2]]              # static field: evaluate the point at t = 0
    G = curvature.einstein_tensor(g, X, **kw)
    lap = _laplacian(Phi, list(x), eps)
    return G[0][0] - 2.0 * lap


# --- reference metric: de Sitter (the maximally-symmetric Lambda vacuum) ------

def de_sitter_metric(L=10.0):
    """de Sitter space in static coordinates (G = c = 1):
        ds^2 = -(1 - r^2/L^2) dt^2 + (1 - r^2/L^2)^{-1} dr^2 + r^2 dOmega^2.
    A VACUUM solution WITH a cosmological constant: R_{mu nu} = Lambda g_{mu nu},
    R = 4 Lambda, G_{mu nu} = -Lambda g_{mu nu}, so G_{mu nu} + Lambda g_{mu nu} = 0
    with Lambda = 3/L^2.  Cosmic horizon at r = L (the curvature scale)."""
    def g(X):
        t, r, th, ph = X
        f = 1.0 - (r * r) / (L * L)
        return [[-f, 0.0, 0.0, 0.0],
                [0.0, 1.0 / f, 0.0, 0.0],
                [0.0, 0.0, r * r, 0.0],
                [0.0, 0.0, 0.0, r * r * math.sin(th) ** 2]]
    return g


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-13  Einstein field equations -- demo   (matter <-> curvature)")
    print("=" * 64)

    # 1. vacuum: Schwarzschild solves G = 8 pi T with T = 0
    print("\nVACUUM  G_{mu nu} = 0  (Schwarzschild solves the field equation):")
    sch = schwarzschild_metric(1.0)
    for r in (6.0, 10.0):
        res = field_equation_residual(sch, 0, [0.0, r, 1.1, 0.7])
        m = max(abs(res[i][j]) for i in range(4) for j in range(4))
        print(f"  r={r:4.1f} M:  max|G + 0 - 8pi*0| = {m:.2e}   (~0)")

    # 2. the perfect fluid
    print("\nPERFECT FLUID  T_{mu nu} = (rho+p) u_mu u_nu + p g_{mu nu}:")
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    rho, p = 2.5, 0.4
    u = rest_four_velocity(mink, x)                      # at rest: (1,0,0,0)
    T = stress_energy_perfect_fluid(rho, p, u, mink, x)
    print(f"  rest frame:  T_00 = {T[0][0]:.3f} (= rho = {rho}),   "
          f"T_11 = {T[1][1]:.3f} (= p = {p})")
    print(f"  trace g^uv T_uv = {trace(mink, T, x):+.3f}   (= -rho + 3p = {-rho + 3 * p:+.3f})")

    # 3. trace-reversed form == G = 8 pi T  (reconstruct Ricci two ways) on de Sitter
    print("\nTRACE-REVERSED  R_uv = 8pi(T_uv - 1/2 T g_uv)  ==  G_uv = 8pi T_uv:")
    ds = de_sitter_metric(10.0)
    xd = [0.0, 3.0, 1.2, 0.6]
    G = einstein_tensor(ds, xd)
    Tsrc = [[G[i][j] / EIGHT_PI for j in range(4)] for i in range(4)]   # matter that sources it
    R_direct = ricci(ds, xd)
    R_trev = trace_reversed_ricci(ds, Tsrc, xd)
    dmax = max(abs(R_direct[i][j] - R_trev[i][j]) for i in range(4) for j in range(4))
    print(f"  de Sitter (r=3, L=10):  max|R_direct - R_trace-reversed| = {dmax:.2e}  (~0)")

    # 4. Newtonian limit fixes 8 pi:  G_00 = 2 nabla^2 Phi
    print("\nNEWTONIAN LIMIT  G_00 = 2 nabla^2 Phi  =>  nabla^2 Phi = 4 pi rho:")
    A, sig = 1e-3, 1.0
    Phi = lambda q: A * math.exp(-(q[0] ** 2 + q[1] ** 2 + q[2] ** 2) / (2.0 * sig * sig))
    for pt in ([0.6, -0.4, 0.5], [0.0, 0.0, 0.0]):
        res = newtonian_poisson_residual(Phi, pt)
        lap = _laplacian(Phi, pt, 1e-3)
        print(f"  x={pt}:  G_00 = {2 * lap + res:+.3e}   2 nabla^2 Phi = {2 * lap:+.3e}   "
              f"resid = {res:+.1e}")

    # 5. the cosmological constant
    print("\nCOSMOLOGICAL CONSTANT  G_uv + Lambda g_uv = 8pi T_uv:")
    Lam = 0.05
    res = field_equation_residual(mink, 0, [0.0, 1.0, 1.0, 0.5], Lambda=Lam)
    eta = mink([0, 0, 0, 0])
    dmax = max(abs(res[i][j] - Lam * eta[i][j]) for i in range(4) for j in range(4))
    print(f"  flat space, Lambda = {Lam}:  residual == Lambda*eta? max diff = {dmax:.2e}")
    LdS = 10.0
    res = field_equation_residual(de_sitter_metric(LdS), 0, [0.0, 3.0, 1.2, 0.6],
                                  Lambda=3.0 / LdS ** 2)
    m = max(abs(res[i][j]) for i in range(4) for j in range(4))
    print(f"  de Sitter L = {LdS}, Lambda = 3/L^2 = {3 / LdS ** 2:.3f}:  "
          f"max|G + Lambda g| = {m:.2e}  (~0)")


if __name__ == "__main__":
    _demo()
