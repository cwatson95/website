"""
MA-21  Dimensional analysis & asymptotics -- the Buckingham Pi theorem (counting
and constructing dimensionless groups), divergent asymptotic series and their
optimal truncation, Stirling's approximation, and regular perturbation series.

Part of the physics topic network (modules/topic_network.txt, module MA-21).
Feeds ~QM-15 (perturbation theory, WKB), ~CM-23/~PK-03 (Reynolds/Knudsen-number
scaling), and the order-of-magnitude habit that underlies every estimate.

Pure Python, dependency-free. The Pi groups are the null space of the dimension
matrix (Gaussian elimination); the asymptotic-series example is benchmarked
against a high-accuracy quadrature so the characteristic 'error shrinks then
grows' of a divergent series is visible; Stirling and the perturbation root are
checked against exact values.
"""

import math

__all__ = [
    "nullspace", "buckingham_pi", "is_dimensionless",
    "exp_integral_scaled_true", "exp_integral_scaled_asymptotic", "optimal_truncation",
    "ln_factorial_stirling", "perturbed_root",
]


# --- Buckingham Pi: dimensionless groups = null space of the dimension matrix -

def nullspace(M, tol=1e-9):
    """Basis of {x : M x = 0} by reduced row echelon form. M is a list of rows."""
    r = len(M)
    c = len(M[0]) if r else 0
    A = [row[:] for row in M]
    pivots = []
    row = 0
    for col in range(c):
        piv = next((rr for rr in range(row, r) if abs(A[rr][col]) > tol), None)
        if piv is None:
            continue
        A[row], A[piv] = A[piv], A[row]
        pv = A[row][col]
        A[row] = [x / pv for x in A[row]]
        for rr in range(r):
            if rr != row and abs(A[rr][col]) > tol:
                f = A[rr][col]
                A[rr] = [a - f * b for a, b in zip(A[rr], A[row])]
        pivots.append(col)
        row += 1
        if row == r:
            break
    pivot_set = set(pivots)
    basis = []
    for fcol in (col for col in range(c) if col not in pivot_set):
        vec = [0.0] * c
        vec[fcol] = 1.0
        for i, pcol in enumerate(pivots):
            vec[pcol] = -A[i][fcol]
        basis.append(vec)
    return basis


def is_dimensionless(dim_matrix, exponents, tol=1e-9):
    """True if the product of variables^exponents has zero net dimension:
    (dim_matrix) @ exponents = 0."""
    for row in dim_matrix:
        if abs(sum(row[j] * exponents[j] for j in range(len(exponents)))) > tol:
            return False
    return True


def buckingham_pi(dim_matrix):
    """Buckingham Pi theorem. `dim_matrix` has one row per base dimension (M,L,T,...)
    and one column per physical variable; entry = exponent of that base dimension in
    that variable. Returns a list of exponent vectors, one per independent
    dimensionless group (their count = n_vars - rank = dim of the null space)."""
    return nullspace(dim_matrix)


# --- asymptotic series: the scaled exponential integral g(x) = x e^x E_1(x) --

def exp_integral_scaled_true(x, N=20000):
    """g(x) = x e^x E_1(x) = int_0^inf e^{-u}/(1 + u/x) du, by composite Simpson --
    the convergent benchmark for the divergent asymptotic series below."""
    U = 60.0
    if N % 2:
        N += 1
    h = U / N
    s = 1.0 + 0.0                                       # integrand at u=0 is 1
    s += math.exp(-U) / (1 + U / x)
    for i in range(1, N):
        u = i * h
        s += (4.0 if i % 2 else 2.0) * math.exp(-u) / (1 + u / x)
    return s * h / 3.0


def exp_integral_scaled_asymptotic(x, N):
    """The divergent asymptotic series  g(x) ~ sum_{k=0}^{N} (-1)^k k! / x^k.
    Accurate for large x only up to its optimal truncation (~N = x terms)."""
    return sum((-1) ** k * math.factorial(k) / x ** k for k in range(N + 1))


def optimal_truncation(x, Nmax=40):
    """Scan truncation order N; return (best_N, best_abs_error, errors_list) of the
    asymptotic series vs the true value. The error shrinks to a minimum near N~x,
    then diverges -- the signature of an asymptotic (non-convergent) series."""
    true = exp_integral_scaled_true(x)
    errs = [abs(exp_integral_scaled_asymptotic(x, N) - true) for N in range(Nmax + 1)]
    best_N = min(range(len(errs)), key=lambda i: errs[i])
    return best_N, errs[best_N], errs


# --- Stirling's approximation ------------------------------------------------

def ln_factorial_stirling(n, terms=2):
    """ln(n!) by Stirling: n ln n - n + (1/2)ln(2 pi n) [+ 1/(12n) - 1/(360 n^3)].
    `terms`=1 keeps the leading n ln n - n; 2 adds (1/2)ln(2 pi n); 3,4 add the
    1/(12n) and -1/(360 n^3) corrections."""
    s = n * math.log(n) - n
    if terms >= 2:
        s += 0.5 * math.log(2 * math.pi * n)
    if terms >= 3:
        s += 1.0 / (12 * n)
    if terms >= 4:
        s -= 1.0 / (360 * n ** 3)
    return s


# --- regular perturbation ----------------------------------------------------

def perturbed_root(eps, order=2):
    """Perturbative root of x^2 + eps x - 1 = 0 near x=1:
    x ~ 1 - eps/2 + eps^2/8 - ...  Returns the series truncated at `order`."""
    coeffs = [1.0, -0.5, 0.125, 0.0]                    # x0, x1, x2, x3 (x3 = 0)
    return sum(coeffs[k] * eps ** k for k in range(order + 1))


def _exact_root(eps):
    return (-eps + math.sqrt(eps * eps + 4.0)) / 2.0


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-21 dimensional analysis & asymptotics -- demo")
    print("=" * 48)

    print("\nBuckingham Pi -- pendulum {period T, length L, gravity g, mass m}")
    print("  base dims rows = (M, L, T); columns = (T_period, L, g, m)")
    D = [[0, 0, 0, 1],          # Mass
         [0, 1, 1, 0],          # Length
         [1, 0, -2, 0]]         # Time
    groups = buckingham_pi(D)
    print(f"  # dimensionless groups = {len(groups)}  (n_vars 4 - rank 3 = 1)")
    for p in groups:
        print(f"  exponents (T,L,g,m) = {[round(e,3) for e in p]}  dimensionless? {is_dimensionless(D, p)}")
    print("  => Pi = g T^2 / L  (so T proportional to sqrt(L/g), the pendulum law)")

    print("\nasymptotic series g(x)=x e^x E_1(x) ~ sum (-1)^k k!/x^k  (DIVERGENT):")
    for x in (5.0, 8.0, 12.0):
        bN, bErr, errs = optimal_truncation(x)
        true = exp_integral_scaled_true(x)
        print(f"  x={x:5}: true={true:.6f}  best N={bN} (~x)  min err={bErr:.2e}  err at N=2x={errs[min(2*int(x),len(errs)-1)]:.2e}")

    print("\nStirling's approximation for ln(n!):")
    for n in (5, 20, 100):
        exact = math.lgamma(n + 1)
        for t in (1, 2, 3):
            err = abs(ln_factorial_stirling(n, t) - exact)
            print(f"  n={n:4d} terms={t}: ln n! approx err = {err:.3e}", end="")
        print(f"   (exact {exact:.4f})")

    print("\nregular perturbation, root of x^2 + eps x - 1 = 0 near x=1:")
    for eps in (0.2, 0.05):
        for order in (1, 2):
            print(f"  eps={eps}: order-{order} series {perturbed_root(eps, order):.6f}  exact {_exact_root(eps):.6f}")


if __name__ == "__main__":
    _demo()
