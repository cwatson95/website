"""
MA-11  Sturm-Liouville theory -- the self-adjoint eigenvalue problem
    -(p y')' + q y = lambda w y   on [a,b]  with homogeneous boundary conditions,
its real eigenvalues, w-orthogonal eigenfunctions, completeness (eigenfunction
expansions), and the Rayleigh quotient bound.

Part of the physics topic network (modules/topic_network.txt, module MA-11).
Builds on ~MA-04 (the matrix eigenproblem) and ~MA-08 (separation of variables);
its eigenfunctions are the special functions of ~MA-12 (Legendre, Bessel,
Hermite, ...); the framework underlies ~QM-05 (observables) and ~MA-14 (Green's
function as sum over eigenfunctions).

Pure Python, dependency-free. The operator is discretized by finite differences
to a symmetric tridiagonal matrix; eigenvalues come from a **Sturm sequence**
(the very object the theory is named for) plus bisection, and eigenvectors from
inverse iteration. A general weight w(x) is handled by symmetric scaling
M = diag(1/sqrt w) A diag(1/sqrt w), which keeps the matrix tridiagonal.
"""

import math

__all__ = [
    "sl_tridiagonal", "sturm_count", "tridiag_eigenvalues", "tridiag_eigenvector",
    "sl_eigenpairs", "inner_w", "rayleigh_quotient", "expand",
]


# --- discretize the Sturm-Liouville operator ---------------------------------

def _as_fn(c):
    return c if callable(c) else (lambda x, c=c: c)


def sl_tridiagonal(p, q, w, a, b, N):
    """Finite-difference the operator -(p y')' + q y = lambda w y on [a,b] with
    Dirichlet conditions y(a)=y(b)=0 and N interior points. Returns the symmetric
    tridiagonal generalized problem A y = lambda diag(w) y as
    (diag, offdiag, w_vec, xs, h). p,q,w may be constants or callables."""
    P, Q, W = _as_fn(p), _as_fn(q), _as_fn(w)
    h = (b - a) / (N + 1)
    xs = [a + (j + 1) * h for j in range(N)]
    diag, off = [], []
    for j, x in enumerate(xs):
        pl, pr = P(x - h / 2.0), P(x + h / 2.0)            # face-centered p
        diag.append((pl + pr) / h ** 2 + Q(x))
        if j < N - 1:
            off.append(-pr / h ** 2)
    wv = [W(x) for x in xs]
    return diag, off, wv, xs, h


# --- the Sturm sequence: count eigenvalues below mu --------------------------

def sturm_count(d, e, mu):
    """Number of eigenvalues < mu of the symmetric tridiagonal matrix with
    diagonal d and off-diagonal e (len N-1). Uses the ratio form of the
    Sturm/Sylvester sequence  q_k = (d_k - mu) - e_{k-1}^2 / q_{k-1}; the count
    of negative q_k equals the number of eigenvalues below mu. This monotone
    'how many roots so far' count is exactly Sturm's theorem for the
    characteristic polynomial of a tridiagonal matrix."""
    n = len(d)
    q = d[0] - mu
    count = 1 if q < 0.0 else 0
    for k in range(1, n):
        if q == 0.0:
            q = 1e-300
        q = (d[k] - mu) - e[k - 1] * e[k - 1] / q
        if q < 0.0:
            count += 1
    return count


def tridiag_eigenvalues(d, e, which=None):
    """Eigenvalues of a symmetric tridiagonal matrix by Sturm-sequence bisection.
    `which` is a list of 1-based indices (1 = smallest); default = all, ascending.
    The m-th eigenvalue is the threshold mu where sturm_count jumps to m."""
    n = len(d)
    rad = lambda i: (abs(e[i - 1]) if i > 0 else 0.0) + (abs(e[i]) if i < n - 1 else 0.0)
    lo = min(d[i] - rad(i) for i in range(n))             # Gershgorin bracket
    hi = max(d[i] + rad(i) for i in range(n))
    eps = 1e-13 * (abs(lo) + abs(hi) + 1.0)

    def kth(m):
        a, b = lo, hi
        for _ in range(200):
            mid = 0.5 * (a + b)
            if sturm_count(d, e, mid) >= m:
                b = mid
            else:
                a = mid
            if b - a < eps:
                break
        return 0.5 * (a + b)

    idx = which if which is not None else range(1, n + 1)
    return [kth(m) for m in idx]


# --- eigenvectors by inverse iteration ---------------------------------------

def _thomas(d, e, rhs):
    """Solve the tridiagonal system (diag d, off-diag e) x = rhs (Thomas)."""
    n = len(d)
    cp = [0.0] * n
    dp = [0.0] * n
    beta = d[0]
    cp[0] = (e[0] / beta) if n > 1 else 0.0
    dp[0] = rhs[0] / beta
    for i in range(1, n):
        beta = d[i] - e[i - 1] * cp[i - 1]
        cp[i] = (e[i] / beta) if i < n - 1 else 0.0
        dp[i] = (rhs[i] - e[i - 1] * dp[i - 1]) / beta
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def tridiag_eigenvector(d, e, lam, iters=4):
    """Unit eigenvector for eigenvalue lam by inverse iteration on (T - mu I),
    mu shifted just off lam to stay non-singular. The start vector is a generic
    deterministic pattern so it overlaps every mode (a symmetric start would miss
    the antisymmetric modes)."""
    n = len(d)
    shift = lam + 1e-8 * (abs(lam) + 1.0)
    dd = [di - shift for di in d]
    x = [math.sin(1.0 + 2.39996 * j) for j in range(n)]   # broad-spectrum start
    for _ in range(iters):
        x = _thomas(dd, e, x)
        nrm = math.sqrt(sum(v * v for v in x))
        x = [v / nrm for v in x]
    # fix sign: first sizeable component positive
    for v in x:
        if abs(v) > 1e-6:
            if v < 0:
                x = [-v for v in x]
            break
    return x


# --- the Sturm-Liouville eigenproblem (weight included) ----------------------

def sl_eigenpairs(p, q, w, a, b, N, k):
    """Lowest k eigenpairs of -(p y')' + q y = lambda w y, Dirichlet on [a,b].
    The weight is absorbed by the symmetric scaling M = D^{-1} A D^{-1},
    D = diag(sqrt w); eigenvalues of M are the SL eigenvalues and the
    eigenfunction is y = u / sqrt(w). Returns (lambdas, ys, xs, w_vec, h)."""
    d, e, wv, xs, h = sl_tridiagonal(p, q, w, a, b, N)
    sd = [math.sqrt(wi) for wi in wv]
    md = [d[j] / wv[j] for j in range(N)]                 # M = D^-1 A D^-1
    me = [e[j] / (sd[j] * sd[j + 1]) for j in range(N - 1)]
    lams = tridiag_eigenvalues(md, me, which=list(range(1, k + 1)))
    ys = []
    for lam in lams:
        u = tridiag_eigenvector(md, me, lam)              # eigenvector of M
        y = [u[j] / sd[j] for j in range(N)]              # back to the SL function
        ys.append(y)
    return lams, ys, xs, wv, h


# --- inner products, Rayleigh quotient, expansions ---------------------------

def inner_w(f, g, wv, h):
    """Weighted inner product  <f,g>_w = integral f g w dx  (trapezoid-ish, the
    interior-node Riemann sum h * sum f_j g_j w_j)."""
    return h * sum(f[j] * g[j] * wv[j] for j in range(len(f)))


def rayleigh_quotient(p, q, w, y, a, b):
    """Rayleigh quotient  R[y] = [ int p y'^2 + q y^2 ] / [ int w y^2 ]  on the
    grid carrying y (Dirichlet, y=0 at the ends). For any admissible trial y,
    R[y] >= lambda_min, with equality at the ground eigenfunction."""
    P, Q, W = _as_fn(p), _as_fn(q), _as_fn(w)
    N = len(y)
    h = (b - a) / (N + 1)
    xs = [a + (j + 1) * h for j in range(N)]
    yext = [0.0] + list(y) + [0.0]                        # impose Dirichlet ends
    num = 0.0
    for j in range(N + 1):                                # faces between nodes
        xf = a + (j + 0.5) * h
        dy = (yext[j + 1] - yext[j]) / h
        num += P(xf) * dy * dy * h
    num += sum(Q(xs[j]) * y[j] ** 2 for j in range(N)) * h
    den = sum(W(xs[j]) * y[j] ** 2 for j in range(N)) * h
    return num / den


def expand(f, ys, wv, h):
    """Eigenfunction expansion coefficients c_n = <f,y_n>_w / <y_n,y_n>_w. With
    {y_n} the full eigenbasis this reconstructs f exactly (completeness); the
    partial sums converge in the mean (Parseval)."""
    return [inner_w(f, y, wv, h) / inner_w(y, y, wv, h) for y in ys]


def reconstruct(coeffs, ys):
    """Sum_n c_n y_n on the grid."""
    N = len(ys[0])
    return [sum(coeffs[n] * ys[n][j] for n in range(len(ys))) for j in range(N)]


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-11 Sturm-Liouville -- demo")
    print("=" * 31)
    L = math.pi
    N = 120
    print(f"\n-(y')' = lambda y on [0, pi], Dirichlet, N={N} interior points")
    lams, ys, xs, wv, h = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, L, N, 5)
    print("  n   lambda_n (FD)    n^2 (exact continuum)")
    for n in range(5):
        print(f"  {n+1}   {lams[n]:12.6f}    {(n+1)**2:5d}")

    print("\n  eigenvector vs analytic sin(n x):  overlap |<u, sin>|")
    for n in range(3):
        ana = [math.sin((n + 1) * x) for x in xs]
        nrm = math.sqrt(sum(a * a for a in ana))
        ana = [a / nrm for a in ana]
        ov = abs(sum(ys[n][j] * ana[j] for j in range(N))) / math.sqrt(sum(v * v for v in ys[n]))
        print(f"    n={n+1}:  {ov:.6f}")

    print("\nRayleigh quotient with trial y = x(pi - x):")
    trial = [x * (L - x) for x in xs]
    R = rayleigh_quotient(1.0, 0.0, 1.0, trial, 0.0, L)
    print(f"  R[trial] = {R:.6f}   10/pi^2 = {10/math.pi**2:.6f}   lambda_min = {lams[0]:.6f}")
    print(f"  bound satisfied (R >= lambda_min)? {R >= lams[0]}")

    print("\ncompleteness: expand f = x(pi-x) in ALL eigenfunctions, check Parseval")
    lamsA, ysA, xsA, wvA, hA = sl_eigenpairs(1.0, 0.0, 1.0, 0.0, L, 40, 40)
    f = [x * (L - x) for x in xsA]
    c = expand(f, ysA, wvA, hA)
    energy_f = inner_w(f, f, wvA, hA)
    energy_c = sum(c[n] ** 2 * inner_w(ysA[n], ysA[n], wvA, hA) for n in range(len(ysA)))
    print(f"  <f,f>_w = {energy_f:.6f}   sum c_n^2 <y_n,y_n>_w = {energy_c:.6f}")


if __name__ == "__main__":
    _demo()
