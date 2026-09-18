"""
MA-20  Numerical methods -- quadrature (trapezoid / Simpson / Gauss-Legendre),
root finding (bisection / Newton / secant), ODE integrators (Euler / RK4),
the dominant-eigenvalue power iteration, and Lagrange interpolation.

Part of the physics topic network (modules/topic_network.txt, module MA-20).
The numerical engine under ~PK-01 (kinetic/Boltzmann solvers), ~MA-10..MA-14
(every quadrature/ODE check there), and ~CM-23 (CFD). Reuses ideas from ~MA-04.

Pure Python, dependency-free. The organizing idea is the **order of accuracy**:
each method's empirical convergence order is measured by halving the step and
reading the error ratio (trapezoid 2, Simpson 4, Euler 1, RK4 4) -- a method that
claims order p must show error ~ h^p, and the tests assert exactly that.
"""

import math

__all__ = [
    "trapezoid", "simpson", "gauss_legendre", "quad_order",
    "bisection", "newton", "secant",
    "euler", "rk4", "ode_order",
    "power_iteration", "lagrange_interp",
]


# --- quadrature --------------------------------------------------------------

def trapezoid(f, a, b, N):
    """Composite trapezoid rule (order 2)."""
    h = (b - a) / N
    s = 0.5 * (f(a) + f(b))
    for i in range(1, N):
        s += f(a + i * h)
    return s * h


def simpson(f, a, b, N):
    """Composite Simpson's rule (order 4). N is rounded up to even."""
    if N % 2:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return s * h / 3.0


# Gauss-Legendre nodes/weights on [-1, 1]
_GL = {
    2: ([-1 / math.sqrt(3), 1 / math.sqrt(3)], [1.0, 1.0]),
    3: ([-math.sqrt(3 / 5), 0.0, math.sqrt(3 / 5)], [5 / 9, 8 / 9, 5 / 9]),
    5: ([-0.906179845938664, -0.538469310105683, 0.0, 0.538469310105683, 0.906179845938664],
        [0.236926885056189, 0.478628670499366, 0.568888888888889, 0.478628670499366, 0.236926885056189]),
}


def gauss_legendre(f, a, b, n_nodes=5, panels=1):
    """Composite Gauss-Legendre quadrature: `panels` sub-intervals, each with an
    n-node rule (exact for polynomials up to degree 2*n_nodes - 1)."""
    nodes, weights = _GL[n_nodes]
    H = (b - a) / panels
    total = 0.0
    for p in range(panels):
        lo = a + p * H
        c0, c1 = (lo + (lo + H)) / 2.0, H / 2.0          # midpoint, half-width
        total += c1 * sum(w * f(c0 + c1 * x) for x, w in zip(nodes, weights))
    return total


def quad_order(method, f, a, b, exact, N=16):
    """Empirical order of accuracy: log2(error(N) / error(2N))."""
    e1 = abs(method(f, a, b, N) - exact)
    e2 = abs(method(f, a, b, 2 * N) - exact)
    return math.log2(e1 / e2) if e2 > 0 else float("inf")


# --- root finding ------------------------------------------------------------

def bisection(f, a, b, tol=1e-12, maxit=200):
    """Bracketing root finder; needs f(a), f(b) of opposite sign. Linear (order 1)."""
    fa, fb = f(a), f(b)
    if fa * fb > 0:
        raise ValueError("f(a) and f(b) must straddle a root")
    for _ in range(maxit):
        m = 0.5 * (a + b)
        fm = f(m)
        if abs(fm) < tol or (b - a) < tol:
            return m
        if fa * fm < 0:
            b, fb = m, fm
        else:
            a, fa = m, fm
    return 0.5 * (a + b)


def newton(f, fp, x0, tol=1e-13, maxit=100):
    """Newton's method x <- x - f/f'. Quadratically convergent near a simple root.
    Returns (root, iterates) where iterates lets the test check the error squares."""
    x = x0
    hist = [x]
    for _ in range(maxit):
        fx = f(x)
        if abs(fx) < tol:
            break
        x = x - fx / fp(x)
        hist.append(x)
    return x, hist


def secant(f, x0, x1, tol=1e-13, maxit=100):
    """Secant method (Newton without an explicit derivative)."""
    f0, f1 = f(x0), f(x1)
    for _ in range(maxit):
        if abs(f1) < tol:
            break
        x2 = x1 - f1 * (x1 - x0) / (f1 - f0)
        x0, f0, x1, f1 = x1, f1, x2, f(x2)
    return x1


# --- ODE integrators  (scalar y' = f(t, y), return y(T)) ---------------------

def euler(f, y0, T, n):
    """Explicit Euler (order 1)."""
    h = T / n
    y = y0
    for i in range(n):
        y += h * f(i * h, y)
    return y


def rk4(f, y0, T, n):
    """Classical 4th-order Runge-Kutta (order 4)."""
    h = T / n
    y = y0
    for i in range(n):
        t = i * h
        k1 = f(t, y)
        k2 = f(t + 0.5 * h, y + 0.5 * h * k1)
        k3 = f(t + 0.5 * h, y + 0.5 * h * k2)
        k4 = f(t + h, y + h * k3)
        y += h / 6.0 * (k1 + 2 * k2 + 2 * k3 + k4)
    return y


def ode_order(integrator, f, y0, T, exact, n=32):
    """Empirical order of an ODE integrator by step halving."""
    e1 = abs(integrator(f, y0, T, n) - exact)
    e2 = abs(integrator(f, y0, T, 2 * n) - exact)
    return math.log2(e1 / e2) if e2 > 0 else float("inf")


# --- linear algebra & interpolation ------------------------------------------

def power_iteration(A, iters=500, tol=1e-14):
    """Dominant eigenvalue (largest |lambda|) and its eigenvector by power
    iteration. Returns (lambda, vector)."""
    n = len(A)
    x = [1.0 / math.sqrt(n)] * n
    lam = 0.0
    for _ in range(iters):
        y = [sum(A[i][j] * x[j] for j in range(n)) for i in range(n)]
        nrm = math.sqrt(sum(v * v for v in y))
        y = [v / nrm for v in y]
        lam_new = sum(y[i] * sum(A[i][j] * y[j] for j in range(n)) for i in range(n))  # Rayleigh
        if abs(lam_new - lam) < tol:
            lam = lam_new
            x = y
            break
        lam, x = lam_new, y
    return lam, x


def lagrange_interp(xs, ys, x):
    """Lagrange interpolating polynomial evaluated at x (exact through the nodes)."""
    total = 0.0
    n = len(xs)
    for i in range(n):
        term = ys[i]
        for j in range(n):
            if j != i:
                term *= (x - xs[j]) / (xs[i] - xs[j])
        total += term
    return total


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-20 numerical methods -- demo")
    print("=" * 33)

    print("\nquadrature of int_0^1 e^x dx = e - 1 = %.10f" % (math.e - 1))
    f = math.exp
    for name, m in [("trapezoid", trapezoid), ("simpson", simpson)]:
        val = m(f, 0, 1, 16)
        print(f"  {name:10s} N=16: {val:.10f}  err {abs(val-(math.e-1)):.2e}  order ~{quad_order(m, f, 0, 1, math.e-1):.2f}")
    g = gauss_legendre(f, 0, 1, 5, 1)
    print(f"  gauss-5    1 panel: {g:.10f}  err {abs(g-(math.e-1)):.2e}")

    print("\nroot finding for x^2 - 2 = 0  (sqrt 2 = %.12f):" % math.sqrt(2))
    r, hist = newton(lambda x: x * x - 2, lambda x: 2 * x, 1.0)
    print(f"  newton:   {r:.12f} in {len(hist)-1} steps (quadratic)")
    print(f"  bisection:{bisection(lambda x: x*x-2, 0, 2):.12f}")
    print(f"  secant:   {secant(lambda x: x*x-2, 1, 2):.12f}")

    print("\nODE y' = y, y(0)=1 -> y(1)=e=%.8f.  order by step halving:" % math.e)
    fode = lambda t, y: y
    for name, integ in [("euler", euler), ("rk4", rk4)]:
        val = integ(fode, 1.0, 1.0, 64)
        print(f"  {name:6s} n=64: {val:.8f}  err {abs(val-math.e):.2e}  order ~{ode_order(integ, fode, 1.0, 1.0, math.e):.2f}")

    print("\npower iteration, dominant eigenvalue of [[2,1,0],[1,2,1],[0,1,2]] (max = 2+sqrt2):")
    lam, vec = power_iteration([[2.0, 1.0, 0.0], [1.0, 2.0, 1.0], [0.0, 1.0, 2.0]])
    print(f"  lambda_max = {lam:.8f}   exact {2+math.sqrt(2):.8f}")

    print("\nLagrange interpolation through (0,0),(1,1),(2,4),(3,9) [the parabola x^2]:")
    print(f"  P(1.5) = {lagrange_interp([0,1,2,3],[0,1,4,9],1.5):.6f}  (= 2.25)")


if __name__ == "__main__":
    _demo()
