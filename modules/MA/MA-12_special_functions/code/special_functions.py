"""
MA-12  Special functions -- the orthogonal polynomials and Bessel functions that
are the eigenfunctions of the Sturm-Liouville problems of physics: Legendre P_n
(and associated P_l^m -> spherical harmonics), Hermite H_n, Laguerre L_n, and the
Bessel functions J_n.

Part of the physics topic network (modules/topic_network.txt, module MA-12).
Each family is an ~MA-11 Sturm-Liouville eigenfunction set; they reappear as
~QM-09 (Hermite <-> harmonic oscillator), ~QM-12 (Laguerre <-> hydrogen radial,
Legendre/Y_lm <-> angular part), ~QM-10 (Y_lm <-> angular momentum), and
~EM-05 (Legendre <-> multipole expansion).

Pure Python (math), dependency-free. Polynomials are built from their stable
upward recurrences; J_n from its integral representation. Each evaluator is
cross-checked three ways in the tests: closed-form low orders, the orthogonality
integral with the right weight, and the residual of its own ODE.
"""

import math

__all__ = [
    "legendre", "legendre_deriv", "assoc_legendre",
    "hermite", "laguerre", "bessel_j",
    "legendre_generating", "simpson", "ode_residual",
    "orthogonality_legendre", "orthogonality_hermite", "orthogonality_laguerre",
]


# --- the recurrences ---------------------------------------------------------

def legendre(n, x):
    """Legendre polynomial P_n(x) via (k+1)P_{k+1} = (2k+1)x P_k - k P_{k-1}.
    Eigenfunctions of -((1-x^2)y')' = n(n+1) y on [-1,1]; weight w=1."""
    if n == 0:
        return 1.0
    p0, p1 = 1.0, x
    for k in range(1, n):
        p0, p1 = p1, ((2 * k + 1) * x * p1 - k * p0) / (k + 1)
    return p1


def legendre_deriv(n, x):
    """P_n'(x) from (1-x^2) P_n' = n(P_{n-1} - x P_n)  (x^2 != 1)."""
    if n == 0:
        return 0.0
    return n * (legendre(n - 1, x) - x * legendre(n, x)) / (1.0 - x * x)


def assoc_legendre(l, m, x):
    """Associated Legendre function P_l^m(x), m >= 0, the theta-dependence of the
    spherical harmonics Y_l^m. Built from P_m^m = (-1)^m (2m-1)!! (1-x^2)^{m/2}
    and the upward l-recurrence."""
    if m < 0 or m > l:
        return 0.0
    pmm = 1.0
    if m > 0:
        somx2 = math.sqrt(max(0.0, 1.0 - x * x))
        fact = 1.0
        for _ in range(m):
            pmm *= -fact * somx2
            fact += 2.0                                   # (2m-1)!! with sign (-1)^m
    if l == m:
        return pmm
    pmmp1 = x * (2 * m + 1) * pmm
    if l == m + 1:
        return pmmp1
    pll = 0.0
    for ll in range(m + 2, l + 1):
        pll = ((2 * ll - 1) * x * pmmp1 - (ll + m - 1) * pmm) / (ll - m)
        pmm, pmmp1 = pmmp1, pll
    return pll


def hermite(n, x):
    """Physicists' Hermite polynomial H_n(x) via H_{k+1} = 2x H_k - 2k H_{k-1}.
    Eigenfunctions of the quantum oscillator; weight e^{-x^2} on (-inf, inf)."""
    if n == 0:
        return 1.0
    h0, h1 = 1.0, 2.0 * x
    for k in range(1, n):
        h0, h1 = h1, 2.0 * x * h1 - 2.0 * k * h0
    return h1


def laguerre(n, x):
    """Laguerre polynomial L_n(x) via (k+1)L_{k+1} = (2k+1-x)L_k - k L_{k-1}.
    Eigenfunctions of the hydrogen radial problem; weight e^{-x} on [0, inf)."""
    if n == 0:
        return 1.0
    l0, l1 = 1.0, 1.0 - x
    for k in range(1, n):
        l0, l1 = l1, ((2 * k + 1 - x) * l1 - k * l0) / (k + 1)
    return l1


def bessel_j(n, x, N=2000):
    """Bessel function of the first kind J_n(x) for integer n >= 0, from the
    integral representation  J_n(x) = (1/pi) int_0^pi cos(n tau - x sin tau) dtau.
    Satisfies x^2 y'' + x y' + (x^2 - n^2) y = 0."""
    return simpson(lambda tau: math.cos(n * tau - x * math.sin(tau)), 0.0, math.pi, N) / math.pi


def legendre_generating(x, t, nmax=40):
    """Partial sum of the Legendre generating function
       1/sqrt(1 - 2 x t + t^2) = sum_n P_n(x) t^n   (|t| < 1).
    Returns (series_sum, closed_form) for comparison."""
    s = sum(legendre(n, x) * t ** n for n in range(nmax))
    closed = 1.0 / math.sqrt(1.0 - 2.0 * x * t + t * t)
    return s, closed


# --- quadrature + verification helpers ---------------------------------------

def simpson(f, a, b, N=2000):
    """Composite Simpson's rule for int_a^b f dx."""
    if N % 2:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for k in range(1, N):
        s += (4.0 if k % 2 else 2.0) * f(a + k * h)
    return s * h / 3.0


def ode_residual(family, n, x, eps=1e-4):
    """Residual of the defining ODE at x, with y', y'' by central differences.
    A correct special function returns ~0. `family` in
    {'legendre','hermite','laguerre','bessel'} (Bessel uses n as the order)."""
    fn = {
        "legendre": lambda t: legendre(n, t),
        "hermite": lambda t: hermite(n, t),
        "laguerre": lambda t: laguerre(n, t),
        "bessel": lambda t: bessel_j(n, t),
    }[family]
    y = fn(x)
    yp = (fn(x + eps) - fn(x - eps)) / (2 * eps)
    ypp = (fn(x + eps) - 2 * y + fn(x - eps)) / eps ** 2
    if family == "legendre":
        return (1 - x * x) * ypp - 2 * x * yp + n * (n + 1) * y
    if family == "hermite":
        return ypp - 2 * x * yp + 2 * n * y
    if family == "laguerre":
        return x * ypp + (1 - x) * yp + n * y
    return x * x * ypp + x * yp + (x * x - n * n) * y       # bessel


def orthogonality_legendre(m, n):
    """int_{-1}^1 P_m P_n dx  ( = 2/(2n+1) delta_mn )."""
    return simpson(lambda x: legendre(m, x) * legendre(n, x), -1.0, 1.0, 4000)


def orthogonality_hermite(m, n):
    """int H_m H_n e^{-x^2} dx  ( = 2^n n! sqrt(pi) delta_mn )."""
    return simpson(lambda x: hermite(m, x) * hermite(n, x) * math.exp(-x * x), -8.0, 8.0, 6000)


def orthogonality_laguerre(m, n):
    """int_0^inf L_m L_n e^{-x} dx  ( = delta_mn )."""
    return simpson(lambda x: laguerre(m, x) * laguerre(n, x) * math.exp(-x), 0.0, 45.0, 8000)


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-12 special functions -- demo")
    print("=" * 33)

    print("\nLegendre P_n(0.4) and the ODE residual:")
    for n in range(5):
        print(f"  P_{n}(0.4) = {legendre(n, 0.4): .6f}   ODE residual = {ode_residual('legendre', n, 0.4): .1e}")

    print("\northogonality int_{-1}^1 P_m P_n dx  (expect 2/(2n+1) on the diagonal):")
    for n in range(4):
        diag = orthogonality_legendre(n, n)
        off = orthogonality_legendre(n, (n + 1) % 4 if (n + 1) % 4 != n else n + 2)
        print(f"  n={n}: diag {diag:.6f}  (2/(2n+1)={2/(2*n+1):.6f})   <P_{n},P_other> {off:+.2e}")

    print("\nHermite H_n(0.7) and weighted norm 2^n n! sqrt(pi):")
    for n in range(4):
        norm = orthogonality_hermite(n, n)
        print(f"  H_{n}(0.7) = {hermite(n, 0.7): .4f}   norm {norm:.4f}  (exact {2**n*math.factorial(n)*math.sqrt(math.pi):.4f})")

    print("\nLaguerre L_n(1.5), norm int L_n^2 e^{-x} dx (expect 1):")
    for n in range(4):
        print(f"  L_{n}(1.5) = {laguerre(n, 1.5): .6f}   norm = {orthogonality_laguerre(n, n):.6f}")

    print("\nBessel J_n(x) from the integral rep (J_0(0)=1, J_1(0)=0):")
    for x in (0.0, 1.0, 2.5, 5.0):
        print(f"  x={x}:  J_0={bessel_j(0, x): .6f}  J_1={bessel_j(1, x): .6f}  J_2={bessel_j(2, x): .6f}")

    print("\nLegendre generating function at x=0.3, t=0.5:")
    s, closed = legendre_generating(0.3, 0.5)
    print(f"  sum P_n(0.3)(0.5)^n = {s:.8f}   1/sqrt(1-2xt+t^2) = {closed:.8f}")


if __name__ == "__main__":
    _demo()
