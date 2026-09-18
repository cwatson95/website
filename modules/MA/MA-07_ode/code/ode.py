"""
MA-07  Ordinary differential equations -- numerical integrators (Euler, RK4) for
scalar/vector/second-order systems, plus the exact solution of a linear system
by diagonalization (reusing ~MA-04).

Part of the physics topic network (modules/topic_network.txt, module MA-07).
Builds on ~MA-04 (eigen-decomposition); feeds ~CM-02 (Newton's 2nd law is an
ODE), ~CM-15/~CM-16 (oscillations & normal modes), ~QM-03 (Schrodinger eqn).

State y is a list (vector); a scalar ODE uses a length-1 list. The RHS is
f(t, y) -> list. `integrate` returns (ts, ys).

NOTE: MA-04 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA04 = os.path.abspath(os.path.join(_HERE, "..", "..", "MA-04_linear_algebra", "code"))
if _MA04 not in sys.path:
    sys.path.insert(0, _MA04)

from linalg import matvec, eig_symmetric  # noqa: E402

__all__ = [
    "euler_step", "rk4_step", "integrate", "second_order_system",
    "linear_rhs", "linear_evolve_symmetric",
]


def _axpy(y, dy, s):
    return [y[i] + s * dy[i] for i in range(len(y))]


def euler_step(f, t, y, dt):
    """One explicit-Euler step (first order)."""
    return _axpy(y, f(t, y), dt)


def rk4_step(f, t, y, dt):
    """One classical 4th-order Runge-Kutta step."""
    k1 = f(t, y)
    k2 = f(t + dt / 2.0, _axpy(y, k1, dt / 2.0))
    k3 = f(t + dt / 2.0, _axpy(y, k2, dt / 2.0))
    k4 = f(t + dt, _axpy(y, k3, dt))
    return [y[i] + dt / 6.0 * (k1[i] + 2.0 * k2[i] + 2.0 * k3[i] + k4[i]) for i in range(len(y))]


def integrate(f, y0, t0, t1, n, method=rk4_step):
    """Integrate dy/dt = f(t, y) from t0 to t1 in n steps. Returns (ts, ys)."""
    y, t, dt = list(y0), t0, (t1 - t0) / n
    ts, ys = [t0], [list(y0)]
    for _ in range(n):
        y = method(f, t, y, dt)
        t += dt
        ts.append(t)
        ys.append(y)
    return ts, ys


def second_order_system(g):
    """Turn a 2nd-order ODE y'' = g(t, y, y') into a first-order system on
    [y, y']:  d/dt [y, v] = [v, g(t, y, v)]."""
    return lambda t, yv: [yv[1], g(t, yv[0], yv[1])]


def linear_rhs(A):
    """RHS of the linear system  dx/dt = A x  (A a matrix), for use with `integrate`."""
    return lambda t, x: matvec(A, x)


def linear_evolve_symmetric(A, x0, t):
    """Exact solution x(t) = e^{At} x0 for a SYMMETRIC matrix A, via MA-04:
    diagonalize A = Q diag(lambda) Q^T, then
        x(t) = sum_i (v_i . x0) e^{lambda_i t} v_i .
    A clean reuse of the ~MA-04 eigensolver; compare against RK4 of dx/dt=Ax."""
    vals, vecs = eig_symmetric(A)
    x = [0.0] * len(x0)
    for lam, v in zip(vals, vecs):
        c = sum(v[i] * x0[i] for i in range(len(x0)))     # projection v_i . x0
        e = math.exp(lam * t)
        for i in range(len(x0)):
            x[i] += c * e * v[i]
    return x


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-07 ODEs -- demo")
    print("=" * 32)

    # dy/dt = y  ->  e^t
    ts, ys = integrate(lambda t, y: [y[0]], [1.0], 0.0, 1.0, 1000)
    print("dy/dt=y:   y(1) =", round(ys[-1][0], 8), " (e =", round(math.e, 8), ")")

    # SHO  y'' = -y  ->  cos t
    f = second_order_system(lambda t, y, v: -y)
    ts, ys = integrate(f, [1.0, 0.0], 0.0, 2.0 * math.pi, 4000)
    print("SHO y''=-y: y(2pi) =", round(ys[-1][0], 6), " (cos 2pi = 1);  y'(2pi) =", round(ys[-1][1], 6), " (= 0)")

    # damped oscillator  y'' + 0.3 y' + y = 0
    f = second_order_system(lambda t, y, v: -0.3 * v - y)
    ts, ys = integrate(f, [1.0, 0.0], 0.0, 20.0, 4000)
    print("damped:    y(20) =", round(ys[-1][0], 6), " (small, decayed)")

    # linear system dx/dt = A x, A symmetric -- exact (MA-04) vs RK4
    A = [[0.0, 1.0], [1.0, 0.0]]               # eigenvalues +/- 1
    x0 = [1.0, 0.0]
    exact = linear_evolve_symmetric(A, x0, 0.7)
    ts, xs = integrate(linear_rhs(A), x0, 0.0, 0.7, 2000)
    print("linear sys: e^{At}x0 (MA-04) =", [round(c, 6) for c in exact])
    print("            RK4 of dx/dt=Ax  =", [round(c, 6) for c in xs[-1]])


if __name__ == "__main__":
    _demo()
