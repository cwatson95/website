"""
MA-08  Partial differential equations -- the three classic linear PDEs (heat,
wave, Laplace) by finite differences, checkable against the separation-of-
variables (Fourier-mode) solutions.

Part of the physics topic network (modules/topic_network.txt, module MA-08).
Builds on ~MA-02 (the Laplacian) and ~MA-07 (time stepping); the analytic side
is separation of variables, which feeds ~MA-09 (Fourier) and ~EM-04/~QM-03.

Fields are sampled on a uniform grid (a Python list, or list-of-lists in 2-D)
with Dirichlet boundaries held fixed. Pure stdlib.
"""

import math

__all__ = ["heat_1d", "wave_1d", "laplace_2d", "heat_mode", "wave_mode"]


def heat_1d(u0, alpha, dx, dt, nsteps):
    """Explicit (FTCS) step of the heat equation  u_t = alpha u_xx  on a 1-D grid.
    Endpoints held fixed (Dirichlet). Stable for r = alpha*dt/dx^2 <= 1/2."""
    r = alpha * dt / dx ** 2
    u = list(u0)
    N = len(u)
    for _ in range(nsteps):
        un = list(u)
        for i in range(1, N - 1):
            un[i] = u[i] + r * (u[i + 1] - 2.0 * u[i] + u[i - 1])
        u = un
    return u


def wave_1d(u0, v0, c, dx, dt, nsteps):
    """Explicit leapfrog step of the wave equation  u_tt = c^2 u_xx  on a 1-D grid.
    Initial shape u0 and initial velocity v0; endpoints fixed. Courant C = c*dt/dx <= 1."""
    C2 = (c * dt / dx) ** 2
    N = len(u0)
    u_prev = list(u0)
    # first step from the initial velocity (Taylor): u^1 = u0 + dt v0 + 1/2 C^2 lap(u0)
    u = list(u0)
    for i in range(1, N - 1):
        u[i] = u0[i] + dt * v0[i] + 0.5 * C2 * (u0[i + 1] - 2.0 * u0[i] + u0[i - 1])
    for _ in range(max(0, nsteps - 1)):
        un = list(u)
        for i in range(1, N - 1):
            un[i] = 2.0 * u[i] - u_prev[i] + C2 * (u[i + 1] - 2.0 * u[i] + u[i - 1])
        u_prev, u = u, un
    return u


def laplace_2d(grid, tol=1e-8, maxiter=50000):
    """Solve Laplace's equation u_xx + u_yy = 0 on a rectangle by Gauss-Seidel
    relaxation: interior point -> average of its 4 neighbours. `grid` is a
    list-of-lists whose boundary ring holds the Dirichlet data (interior = guess).
    Returns (solved_grid, iterations)."""
    g = [row[:] for row in grid]
    ny, nx = len(g), len(g[0])
    it = 0
    for it in range(1, maxiter + 1):
        maxdiff = 0.0
        for i in range(1, ny - 1):
            for j in range(1, nx - 1):
                new = 0.25 * (g[i + 1][j] + g[i - 1][j] + g[i][j + 1] + g[i][j - 1])
                maxdiff = max(maxdiff, abs(new - g[i][j]))
                g[i][j] = new
        if maxdiff < tol:
            break
    return g, it


# --- analytic separation-of-variables modes (for verification) ---------------

def heat_mode(L, alpha, n):
    """One separated mode of the heat equation on [0,L] with u(0)=u(L)=0:
       u(x,t) = sin(n pi x/L) exp(-alpha (n pi/L)^2 t)."""
    k = n * math.pi / L
    return lambda x, t: math.sin(k * x) * math.exp(-alpha * k * k * t)


def wave_mode(L, c, n):
    """One separated (standing-wave) mode of the wave equation on [0,L], fixed ends:
       u(x,t) = sin(n pi x/L) cos(c n pi t/L)."""
    k = n * math.pi / L
    return lambda x, t: math.sin(k * x) * math.cos(c * k * t)


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-08 PDEs -- demo")
    print("=" * 32)
    L, N = 1.0, 41
    dx = L / (N - 1)
    xs = [i * dx for i in range(N)]

    print("heat eqn u_t = u_xx, initial sin(pi x):")
    u0 = [math.sin(math.pi * x) for x in xs]
    uf = heat_1d(u0, 1.0, dx, 0.0001, 1000)             # T = 0.1
    exact = heat_mode(L, 1.0, 1)
    mid = N // 2
    print(f"  u(0.5, 0.1): numeric {uf[mid]:.5f}  vs separation-of-vars {exact(0.5, 0.1):.5f}")

    print("\nwave eqn u_tt = u_xx, plucked sin(pi x), c=1:")
    uf = wave_1d(u0, [0.0] * N, 1.0, dx, dx, 8)          # C=1, T = 8 dx = 0.2
    exactw = wave_mode(L, 1.0, 1)
    print(f"  u(0.5, 0.2): numeric {uf[mid]:.5f}  vs standing wave {exactw(0.5, 0.2):.5f}")

    print("\nLaplace eqn on unit square, boundary = x^2 - y^2 (harmonic):")
    n = 21
    h = 1.0 / (n - 1)
    grid = [[(j * h) ** 2 - (i * h) ** 2 for j in range(n)] for i in range(n)]
    for i in range(1, n - 1):                            # wipe interior to a bad guess
        for j in range(1, n - 1):
            grid[i][j] = 0.0
    sol, iters = laplace_2d(grid, tol=1e-9)
    ic = n // 2
    exactL = (ic * h) ** 2 - (ic * h) ** 2
    print(f"  relaxed in {iters} sweeps; u(0.5,0.5) = {sol[ic][ic]:.6f}  (exact x^2-y^2 = {exactL:.6f})")


if __name__ == "__main__":
    _demo()
