"""Tests for MA-08 PDEs. Pure stdlib.

Run:  python3 test_pde.py     ->  "All N tests passed."
"""
import math

from pde import heat_1d, wave_1d, laplace_2d, heat_mode, wave_mode


def test_heat_matches_separation_of_variables():
    L, N = 1.0, 41
    dx = L / (N - 1)
    xs = [i * dx for i in range(N)]
    alpha, dt, nsteps = 1.0, 1e-4, 1000
    T = nsteps * dt
    u0 = [math.sin(math.pi * x) for x in xs]              # the n=1 mode
    uf = heat_1d(u0, alpha, dx, dt, nsteps)
    exact = heat_mode(L, alpha, 1)
    for i in range(1, N - 1):
        assert abs(uf[i] - exact(xs[i], T)) < 1.5e-2      # FTCS ~ separation-of-vars solution


def test_heat_diffuses():
    L, N = 1.0, 21
    dx = L / (N - 1)
    u0 = [math.sin(math.pi * (i * dx)) for i in range(N)]
    uf = heat_1d(u0, 1.0, dx, 1e-4, 500)
    assert max(uf) < max(u0)                              # peak decays
    assert min(uf) > -1e-9                                # nonneg IC stays nonneg


def test_wave_matches_standing_wave():
    L, N = 1.0, 41
    dx = L / (N - 1)
    xs = [i * dx for i in range(N)]
    c, dt, nsteps = 1.0, None, 8
    dt = dx                                               # Courant C = 1
    T = nsteps * dt
    u0 = [math.sin(math.pi * x) for x in xs]
    uf = wave_1d(u0, [0.0] * N, c, dx, dt, nsteps)
    exact = wave_mode(L, c, 1)
    for i in range(1, N - 1):
        assert abs(uf[i] - exact(xs[i], T)) < 1e-2        # standing wave sin(pi x) cos(pi t)


def test_laplace_harmonic_is_exact():
    # x^2 - y^2 is harmonic and the 5-point stencil is exact for quadratics
    n = 15
    h = 1.0 / (n - 1)
    g = [[(j * h) ** 2 - (i * h) ** 2 for j in range(n)] for i in range(n)]
    for i in range(1, n - 1):                             # erase interior to a bad guess
        for j in range(1, n - 1):
            g[i][j] = 0.0
    sol, _ = laplace_2d(g, tol=1e-9, maxiter=50000)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            assert abs(sol[i][j] - ((j * h) ** 2 - (i * h) ** 2)) < 1e-4


def test_laplace_residual_vanishes():
    n = 12
    g = [[0.0] * n for _ in range(n)]
    for j in range(n):
        g[0][j] = 1.0                                     # top edge held at 1, rest 0
    sol, _ = laplace_2d(g, tol=1e-9, maxiter=50000)
    for i in range(1, n - 1):
        for j in range(1, n - 1):
            res = sol[i + 1][j] + sol[i - 1][j] + sol[i][j + 1] + sol[i][j - 1] - 4.0 * sol[i][j]
            assert abs(res) < 1e-6                        # discrete Laplacian ~ 0
    assert all(0.0 <= sol[i][j] <= 1.0 for i in range(n) for j in range(n))   # max principle


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
