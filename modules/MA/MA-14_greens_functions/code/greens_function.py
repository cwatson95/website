"""
MA-14  Green's functions -- the inverse of a differential operator. For L u = f
with homogeneous boundary/initial conditions, G solves L_x G(x,xi) = delta(x-xi)
and then  u(x) = integral G(x,xi) f(xi) dxi.  Boundary-value (Dirichlet) and
causal initial-value (propagator) versions, plus the eigenfunction expansion
G = sum_n phi_n(x) phi_n(xi) / lambda_n.

Part of the physics topic network (modules/topic_network.txt, module MA-14).
Rests on ~MA-15 (delta as the source), ~MA-11 (the spectral sum), ~MA-10 (the
causal G is an inverse Laplace transform), and feeds ~EM-17 (retarded potentials)
and ~QM-19 (the propagator / Feynman path integral).

Pure Python (math), dependency-free. The boundary-value Green's functions are the
closed-form 'two-solution' construction; results are cross-checked against a
direct finite-difference solve and (for the propagator) against RK4.
"""

import math

__all__ = [
    "green_dirichlet", "green_helmholtz", "solve_bvp_greens", "solve_bvp_direct",
    "green_series", "causal_green_oscillator", "solve_oscillator_greens", "rk4_oscillator",
]


# --- boundary-value Green's functions on [0,1], Dirichlet --------------------

def green_dirichlet(x, xi):
    """Green's function for L u = -u'' on [0,1], u(0)=u(1)=0:
        G(x,xi) = x_<(1 - x_>)   (x_< = min, x_> = max).
    Then u(x) = int_0^1 G(x,xi) f(xi) dxi solves -u'' = f."""
    lo, hi = (x, xi) if x <= xi else (xi, x)
    return lo * (1.0 - hi)


def green_helmholtz(x, xi, k):
    """Green's function for L u = -u'' + k^2 u on [0,1], u(0)=u(1)=0, built from
    the two homogeneous solutions y1=sinh(kx) (left BC) and y2=sinh(k(1-x))
    (right BC):  G = sinh(k x_<) sinh(k(1-x_>)) / (k sinh k)."""
    lo, hi = (x, xi) if x <= xi else (xi, x)
    return math.sinh(k * lo) * math.sinh(k * (1.0 - hi)) / (k * math.sinh(k))


def _simpson(f, a, b, N=600):
    if N % 2:
        N += 1
    h = (b - a) / N
    s = f(a) + f(b)
    for i in range(1, N):
        s += (4.0 if i % 2 else 2.0) * f(a + i * h)
    return s * h / 3.0


def solve_bvp_greens(f, xs, k=None):
    """Solve the BVP at the points xs by quadrature against the Green's function:
    u(x) = int_0^1 G(x,xi) f(xi) dxi. k=None uses -u''; k>0 uses -u''+k^2 u."""
    G = (lambda x, xi: green_dirichlet(x, xi)) if k is None else (lambda x, xi: green_helmholtz(x, xi, k))
    return [_simpson(lambda xi: G(x, xi) * f(xi), 0.0, 1.0) for x in xs]


def _thomas(a, b, c, d):
    """Solve a tridiagonal system (sub a, diag b, super c, rhs d)."""
    n = len(d)
    cp = [0.0] * n
    dp = [0.0] * n
    cp[0] = c[0] / b[0]
    dp[0] = d[0] / b[0]
    for i in range(1, n):
        m = b[i] - a[i] * cp[i - 1]
        cp[i] = c[i] / m if i < n - 1 else 0.0
        dp[i] = (d[i] - a[i] * dp[i - 1]) / m
    x = [0.0] * n
    x[-1] = dp[-1]
    for i in range(n - 2, -1, -1):
        x[i] = dp[i] - cp[i] * x[i + 1]
    return x


def solve_bvp_direct(f, N, k=None):
    """Independent check: finite-difference solve of -u'' (+k^2 u) = f on [0,1],
    Dirichlet, N interior points. Returns (xs_interior, us)."""
    h = 1.0 / (N + 1)
    xs = [(i + 1) * h for i in range(N)]
    kk = 0.0 if k is None else k * k
    a = [-1.0 / h ** 2] * N
    b = [2.0 / h ** 2 + kk] * N
    c = [-1.0 / h ** 2] * N
    d = [f(x) for x in xs]
    return xs, _thomas(a, b, c, d)


# --- eigenfunction (spectral) expansion of the Green's function --------------

def green_series(x, xi, nmax):
    """Spectral form for -u'' on [0,1], Dirichlet: eigenpairs phi_n=sqrt2 sin(n pi x),
    lambda_n=(n pi)^2, so
        G(x,xi) = sum_{n>=1} 2 sin(n pi x) sin(n pi xi) / (n pi)^2.
    As nmax -> inf this converges to the closed-form tent green_dirichlet."""
    return sum(2.0 * math.sin(n * math.pi * x) * math.sin(n * math.pi * xi) / (n * math.pi) ** 2
               for n in range(1, nmax + 1))


# --- causal (initial-value) Green's function: the propagator -----------------

def causal_green_oscillator(t, tau, omega):
    """Causal Green's function of  y'' + omega^2 y = delta(t-tau), y(0)=y'(0)=0:
        G(t,tau) = sin(omega (t-tau)) / omega   for t >= tau,   else 0.
    This is the inverse Laplace transform of 1/(s^2+omega^2) shifted to tau
    (~MA-10) -- the 1-D 'retarded propagator'."""
    return math.sin(omega * (t - tau)) / omega if t >= tau else 0.0


def solve_oscillator_greens(f, t, omega, N=800):
    """y(t) = int_0^t G(t,tau) f(tau) dtau  solves y'' + omega^2 y = f(t),
    y(0)=y'(0)=0 -- forcing convolved with the propagator (cf. ~MA-10 convolution)."""
    if t == 0.0:
        return 0.0
    return _simpson(lambda tau: causal_green_oscillator(t, tau, omega) * f(tau), 0.0, t, N)


def rk4_oscillator(f, t, omega, n=4000):
    """Independent RK4 check for y'' + omega^2 y = f(t), y(0)=y'(0)=0."""
    if t == 0.0:
        return 0.0
    h = t / n
    y, v = 0.0, 0.0
    acc = lambda tt, yy: f(tt) - omega * omega * yy
    for i in range(n):
        tt = i * h
        k1y, k1v = v, acc(tt, y)
        k2y, k2v = v + 0.5 * h * k1v, acc(tt + 0.5 * h, y + 0.5 * h * k1y)
        k3y, k3v = v + 0.5 * h * k2v, acc(tt + 0.5 * h, y + 0.5 * h * k2y)
        k4y, k4v = v + h * k3v, acc(tt + h, y + h * k3y)
        y += h / 6.0 * (k1y + 2 * k2y + 2 * k3y + k4y)
        v += h / 6.0 * (k1v + 2 * k2v + 2 * k3v + k4v)
    return y


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-14 Green's functions -- demo")
    print("=" * 33)

    print("\n-u'' = f on [0,1], Dirichlet.  Green integral vs exact:")
    xs = [0.25, 0.5, 0.75]
    f1 = lambda x: math.sin(math.pi * x)                    # exact u = sin(pi x)/pi^2
    ug = solve_bvp_greens(f1, xs)
    for x, u in zip(xs, ug):
        print(f"  x={x}: G-integral {u:.6f}   exact {math.sin(math.pi*x)/math.pi**2:.6f}")

    print("\nGreen integral vs direct finite-difference solve (f = 1):")
    f2 = lambda x: 1.0                                       # exact u = x(1-x)/2
    xd, ud = solve_bvp_direct(f2, 9)
    ug2 = solve_bvp_greens(f2, xd)
    print(f"  max |G - FD| over the grid = {max(abs(a-b) for a,b in zip(ug2, ud)):.2e}")

    print("\nHelmholtz -u''+k^2 u = f (k=3): Green vs direct FD:")
    f3 = lambda x: x
    xd, ud = solve_bvp_direct(f3, 9, k=3.0)
    ug3 = solve_bvp_greens(f3, xd, k=3.0)
    print(f"  max |G - FD| = {max(abs(a-b) for a,b in zip(ug3, ud)):.2e}")

    print("\neigenfunction series  G = sum 2 sin(n pi x) sin(n pi xi)/(n pi)^2:")
    for (x, xi) in [(0.3, 0.7), (0.5, 0.25)]:
        closed = green_dirichlet(x, xi)
        for nmax in (10, 100, 2000):
            print(f"  G({x},{xi})  nmax={nmax:5d}: series {green_series(x, xi, nmax):.6f}   closed {closed:.6f}")

    print("\ncausal propagator: y'' + omega^2 y = f, y(0)=y'(0)=0.  Green vs RK4 (omega=2):")
    fdrive = lambda t: math.cos(0.7 * t)
    for t in (1.0, 3.0, 6.0):
        print(f"  t={t}: Green {solve_oscillator_greens(fdrive, t, 2.0):.6f}   RK4 {rk4_oscillator(fdrive, t, 2.0):.6f}")


if __name__ == "__main__":
    _demo()
