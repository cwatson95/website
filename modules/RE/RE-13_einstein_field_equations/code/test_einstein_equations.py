"""Tests for RE-13 Einstein field equations.

Run directly:   python3 test_einstein_equations.py    (-> "All N tests passed.")
Or with pytest: pytest test_einstein_equations.py

Two kinds of check.  The MATTER side (perfect fluid / dust, the trace, the
trace-reversal algebra) is exact and uses tight tolerances.  Anything that touches
the geometry side -- the Einstein tensor / Ricci -- comes from RE-11's
finite-difference curvature, so those checks (Schwarzschild & de Sitter vacua, the
Newtonian limit) use LOOSE tolerances, exactly as RE-11 does.

Headline physics: Schwarzschild solves G = 8 pi T with T = 0; a perfect fluid has
trace -rho + 3p; the trace-reversed form R = 8 pi(T - 1/2 T g) is equivalent to
G = 8 pi T; the weak-field limit gives G_00 = 2 nabla^2 Phi (fixing the 8 pi); and
G + Lambda g = 0 is solved by de Sitter with Lambda = 3/L^2.
"""
import math

from einstein_equations import (
    EIGHT_PI, einstein_tensor, ricci,
    stress_energy_perfect_fluid, stress_energy_dust, rest_four_velocity,
    trace, trace_reversed_ricci,
    field_equation_residual, newtonian_poisson_residual,
    minkowski_metric, schwarzschild_metric, de_sitter_metric,
)

TOL = 1e-12


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _boosted_u(v):
    """A unit timelike 4-velocity boosted at speed v along x in Minkowski:
    U = gamma(1, v, 0, 0), with U.U = -1."""
    g = 1.0 / math.sqrt(1.0 - v * v)
    return [g, g * v, 0.0, 0.0]


# --- vacuum: Schwarzschild solves the field equation -------------------------

def test_schwarzschild_is_a_vacuum_solution():
    """G_{mu nu} = 0 for r > 2M, so Schwarzschild solves G = 8 pi T with T = 0."""
    sch = schwarzschild_metric(1.0)
    for r in (4.0, 6.0, 10.0, 20.0):
        res = field_equation_residual(sch, 0, [0.0, r, 1.2, 0.7])    # T = 0 (vacuum)
        assert all(abs(res[i][j]) <= 1e-4 for i in range(4) for j in range(4))
    # passing the zero tensor explicitly must agree with the 0 shorthand
    Z = [[0.0] * 4 for _ in range(4)]
    r1 = field_equation_residual(sch, 0, [0.0, 8.0, 1.0, 0.9])
    r2 = field_equation_residual(sch, Z, [0.0, 8.0, 1.0, 0.9])
    assert all(_approx(r1[i][j], r2[i][j], 1e-12) for i in range(4) for j in range(4))


# --- the stress-energy tensor ------------------------------------------------

def test_perfect_fluid_is_symmetric():
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    T = stress_energy_perfect_fluid(2.5, 0.4, _boosted_u(0.6), mink, x)
    assert all(_approx(T[i][j], T[j][i], TOL) for i in range(4) for j in range(4))


def test_perfect_fluid_trace_is_minus_rho_plus_3p():
    """g^{mu nu} T_{mu nu} = -rho + 3p (mostly-plus), independent of frame and of
    the background metric (only u.u = -1 matters)."""
    rho, p = 3.0, 0.5
    expect = -rho + 3.0 * p
    # boosted observer in flat space
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    for v in (0.0, 0.4, 0.8):
        T = stress_energy_perfect_fluid(rho, p, _boosted_u(v), mink, x)
        assert _approx(trace(mink, T, x), expect, 1e-12)
    # a curved background (static observer in Schwarzschild) -- same trace
    sch = schwarzschild_metric(1.0)
    xs = [0.0, 8.0, 1.0, 0.5]
    Ts = stress_energy_perfect_fluid(rho, p, rest_four_velocity(sch, xs), sch, xs)
    assert _approx(trace(sch, Ts, xs), expect, 1e-12)


def test_dust_and_radiation_traces():
    """Dust (p = 0): trace = -rho.  Radiation (p = rho/3): trace = 0 (traceless)."""
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    u = _boosted_u(0.3)
    rho = 4.0
    assert _approx(trace(mink, stress_energy_dust(rho, u, mink, x), x), -rho, 1e-12)
    rad = stress_energy_perfect_fluid(rho, rho / 3.0, u, mink, x)
    assert abs(trace(mink, rad, x)) <= 1e-12


def test_perfect_fluid_reduces_to_dust():
    """The p -> 0 perfect fluid IS dust:  T = rho u_mu u_nu."""
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    u = _boosted_u(0.5)
    Tpf = stress_energy_perfect_fluid(2.0, 0.0, u, mink, x)
    Tdust = stress_energy_dust(2.0, u, mink, x)
    assert all(_approx(Tpf[i][j], Tdust[i][j], TOL) for i in range(4) for j in range(4))


def test_rest_frame_gives_energy_density():
    """For an observer at rest the time-time component is the energy density:
    T_00 = -rho g_00  (= rho in Minkowski, where g_00 = -1)."""
    mink = minkowski_metric()
    x = [0.0, 0.0, 0.0, 0.0]
    T = stress_energy_perfect_fluid(2.5, 0.4, rest_four_velocity(mink, x), mink, x)
    assert _approx(T[0][0], 2.5, 1e-12)                       # = rho
    # curved static background: T_00 = -rho g_00
    sch = schwarzschild_metric(1.0)
    xs = [0.0, 8.0, 1.0, 0.5]
    g = sch(xs)
    Ts = stress_energy_perfect_fluid(3.0, 0.5, rest_four_velocity(sch, xs), sch, xs)
    assert _approx(Ts[0][0], -3.0 * g[0][0], 1e-12)


# --- the trace-reversed field equation ---------------------------------------

def test_trace_reversed_equivalent_to_einstein():
    """Pure algebra: take matter T, form R via the trace-reversed equation, then
    rebuild the Einstein tensor G = R - 1/2 R_scalar g from THAT R.  It must equal
    8 pi T -- i.e. R = 8 pi(T - 1/2 T g) <=> G = 8 pi T.  (No curvature here; the
    metric only supplies the index gymnastics.)"""
    metric = schwarzschild_metric(2.0)          # any metric, used only as g_{mu nu}
    x = [0.0, 9.0, 1.0, 0.5]
    g = metric(x)
    T = stress_energy_perfect_fluid(1.2, 0.3, rest_four_velocity(metric, x), metric, x)
    R = trace_reversed_ricci(metric, T, x)
    Rscalar = trace(metric, R, x)               # g^{ab} R_ab
    G = [[R[i][j] - 0.5 * Rscalar * g[i][j] for j in range(4)] for i in range(4)]
    assert all(_approx(G[i][j], EIGHT_PI * T[i][j], 1e-9)
               for i in range(4) for j in range(4))


def test_de_sitter_trace_reversed_reconstructs_ricci():
    """On a real solution (de Sitter), the Ricci tensor reconstructed from the
    sourcing matter T = G/8pi via the trace-reversed equation matches the metric's
    actual Ricci -- and that Ricci is the maximally-symmetric R_uv = (3/L^2) g_uv."""
    L = 10.0
    ds = de_sitter_metric(L)
    Lam = 3.0 / (L * L)
    for r in (2.0, 3.0, 4.0):
        x = [0.0, r, 1.1, 0.7]
        g = ds(x)
        Ric = ricci(ds, x)
        # de Sitter is maximally symmetric: R_uv = (3/L^2) g_uv  (loose, FD curvature)
        assert all(_approx(Ric[i][j], Lam * g[i][j], 1e-3)
                   for i in range(4) for j in range(4))
        # reconstruct Ricci from the matter that sources this geometry
        G = einstein_tensor(ds, x)
        Tsrc = [[G[i][j] / EIGHT_PI for j in range(4)] for i in range(4)]
        Rtr = trace_reversed_ricci(ds, Tsrc, x)
        assert all(abs(Ric[i][j] - Rtr[i][j]) <= 1e-9 * (1.0 + abs(Ric[i][j]))
                   for i in range(4) for j in range(4))


# --- the Newtonian limit fixes the coupling 8 pi -----------------------------

def test_newtonian_limit_fixes_8pi():
    """Weak field: G_00 = 2 nabla^2 Phi (so G_00 = 8 pi rho <=> nabla^2 Phi = 4 pi
    rho).  Use a small Gaussian potential; loose finite-difference tolerance."""
    A, sig = 1e-3, 1.0
    Phi = lambda q: A * math.exp(-(q[0] ** 2 + q[1] ** 2 + q[2] ** 2) / (2.0 * sig * sig))
    for pt in ([0.0, 0.0, 0.0], [0.6, -0.4, 0.5], [1.0, 0.5, -0.8]):
        res = newtonian_poisson_residual(Phi, pt)
        # signal 2 nabla^2 Phi at this point, for a relative comparison
        f0 = Phi(pt)
        lap = 0.0
        for i in range(3):
            qp, qm = list(pt), list(pt)
            qp[i] += 1e-3
            qm[i] -= 1e-3
            lap += (Phi(qp) - 2.0 * f0 + Phi(qm)) / 1e-6
        signal = 2.0 * lap
        assert abs(signal) > 1e-4                              # the lump actually curves space
        assert abs(res) <= 3e-2 * abs(signal)                 # G_00 reproduces 2 nabla^2 Phi


# --- the cosmological constant -----------------------------------------------

def test_cosmological_constant_on_flat_space():
    """With T = 0 the residual G + Lambda g - 8 pi T is exactly Lambda * eta on flat
    space (G = 0) -- the cleanest statement of how Lambda enters the equation."""
    mink = minkowski_metric()
    x = [0.3, 1.0, 1.0, 0.5]
    eta = mink(x)
    for Lam in (0.05, -0.2, 1.5):
        res = field_equation_residual(mink, 0, x, Lambda=Lam)
        assert all(_approx(res[i][j], Lam * eta[i][j], 1e-9)
                   for i in range(4) for j in range(4))


def test_de_sitter_is_a_lambda_vacuum():
    """de Sitter solves G_{mu nu} + Lambda g_{mu nu} = 0 with Lambda = 3/L^2:
    a curved vacuum sourced purely by the cosmological constant."""
    L = 10.0
    ds = de_sitter_metric(L)
    Lam = 3.0 / (L * L)
    for r in (2.0, 3.0, 4.0):
        res = field_equation_residual(ds, 0, [0.0, r, 1.2, 0.6], Lambda=Lam)
        assert all(abs(res[i][j]) <= 1e-4 for i in range(4) for j in range(4))
    # and it is NOT a solution for the wrong Lambda (the equation has real content)
    res_bad = field_equation_residual(ds, 0, [0.0, 3.0, 1.2, 0.6], Lambda=0.0)
    assert max(abs(res_bad[i][j]) for i in range(4) for j in range(4)) > 1e-3


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
