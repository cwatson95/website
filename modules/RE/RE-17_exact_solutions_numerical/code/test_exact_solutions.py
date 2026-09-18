"""Tests for RE-17 exact solutions & numerical relativity.

Run directly:   python3 test_exact_solutions.py     (-> "All N tests passed.")
Or with pytest: pytest test_exact_solutions.py

Curvature is computed by RE-11's finite-difference Riemann tensor, so the field-
equation tests use LOOSE absolute tolerances (FD noise ~ 1e-6 at these radii).
The strongest checks are the field equations themselves, evaluated by handing
each hand-written metric back to RE-11:

  * Kerr is Ricci-flat (vacuum)          -- a wrong component would FAIL this
  * de Sitter solves G + Lambda g = 0, R = 4 Lambda
  * Reissner-Nordstrom is NOT Ricci-flat (EM-sourced) but is scalar-flat
  * a -> 0 / Q -> 0 recover Schwarzschild componentwise
  * Kerr horizons / ergosphere; ADM split of Minkowski; Hamiltonian constraint.
"""
import math

from exact_solutions import (
    kerr_metric, reissner_nordstrom_metric, de_sitter_metric,
    verify_vacuum, verify_einstein_lambda,
    kerr_horizons, kerr_ergosphere,
    adm_decompose, spatial_slice_metric, hamiltonian_constraint_flat,
)
import curvature   # RE-11 (on sys.path via exact_solutions)
import diffgeo     # MA-17 (on sys.path via curvature)

# field-equation residuals from finite-difference curvature: loose absolute tol
TOL_FD = 1e-3
# the EM / Lambda source signals are O(1e-2 .. 1e-1) -- comfortably above noise
TOL_SRC = 1e-3


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _maxabs(A):
    return max(abs(A[i][j]) for i in range(len(A)) for j in range(len(A[0])))


# --- Kerr: rotating VACUUM solution ------------------------------------------

def test_kerr_is_ricci_flat_vacuum():
    """Kerr solves the VACUUM equations R_{mu nu} = 0.  This is the correctness
    gate on the metric components: a wrong term makes Ricci non-zero."""
    for a in (0.0, 0.3, 0.5, 0.9):
        kerr = kerr_metric(1.0, a)
        for x in ([0.0, 8.0, 1.0, 0.7], [0.0, 12.0, 1.3, 2.0]):
            assert verify_vacuum(kerr, x) < TOL_FD
    # the full Einstein tensor also vanishes (vacuum, Lambda = 0)
    G = curvature.einstein_tensor(kerr_metric(1.0, 0.5), [0.0, 9.0, 1.1, 0.5])
    assert _maxabs(G) < TOL_FD


def test_kerr_reduces_to_schwarzschild():
    """a -> 0 recovers Schwarzschild componentwise (frame dragging g_{t phi} -> 0)."""
    kerr = kerr_metric(1.0, 0.0)
    sch = curvature.schwarzschild_metric(1.0)
    for x in ([0.0, 5.0, 1.0, 0.7], [0.0, 8.0, 0.6, 2.1], [0.0, 3.0, 1.4, 0.2]):
        gk, gs = kerr(x), sch(x)
        for i in range(4):
            for j in range(4):
                assert abs(gk[i][j] - gs[i][j]) <= 1e-10 * (1.0 + abs(gs[i][j]))


def test_kerr_frame_dragging_is_present():
    """For a > 0 the off-diagonal g_{t phi} (frame dragging) is non-zero, and it
    vanishes when a = 0."""
    g_spin = kerr_metric(1.0, 0.7)([0.0, 6.0, 1.0, 0.3])
    g_static = kerr_metric(1.0, 0.0)([0.0, 6.0, 1.0, 0.3])
    assert abs(g_spin[0][3]) > 1e-3
    assert abs(g_static[0][3]) == 0.0


# --- de Sitter: Lambda-vacuum, constant curvature ----------------------------

def test_de_sitter_solves_lambda_vacuum():
    """de Sitter solves G_{mu nu} + Lambda g_{mu nu} = 0 and has R = 4 Lambda."""
    for Lam in (0.01, 0.03, 0.05):
        ds = de_sitter_metric(Lam)
        for x in ([0.0, 2.0, 1.0, 0.7], [0.0, 3.5, 1.2, 2.0]):
            assert verify_einstein_lambda(ds, x, Lam) < TOL_FD
            assert _approx(curvature.ricci_scalar(ds, x), 4.0 * Lam, 1e-2)


def test_de_sitter_is_not_plain_vacuum():
    """Without the Lambda term de Sitter is NOT Ricci-flat: R_{mu nu} = Lambda g."""
    Lam = 0.05
    ds = de_sitter_metric(Lam)
    assert verify_vacuum(ds, [0.0, 3.0, 1.0, 0.7]) > TOL_SRC


# --- Reissner-Nordstrom: charged, EM-sourced ---------------------------------

def test_reissner_nordstrom_is_not_ricci_flat():
    """Q != 0 is sourced by the EM stress-energy: R_{mu nu} != 0 -- but the EM
    field is trace-free, so the Ricci SCALAR vanishes, R = 0."""
    for Q in (0.5, 0.9):
        rn = reissner_nordstrom_metric(1.0, Q)
        x = [0.0, 3.0, 1.0, 0.7]
        assert verify_vacuum(rn, x) > TOL_SRC                 # NOT Ricci-flat
        assert abs(curvature.ricci_scalar(rn, x)) < TOL_FD    # trace-free: R = 0
    # the source grows with charge
    r0 = [0.0, 3.0, 1.0, 0.7]
    assert (verify_vacuum(reissner_nordstrom_metric(1.0, 0.9), r0)
            > verify_vacuum(reissner_nordstrom_metric(1.0, 0.5), r0))


def test_reissner_nordstrom_reduces_to_schwarzschild():
    """Q -> 0 recovers Schwarzschild componentwise and becomes Ricci-flat again."""
    rn = reissner_nordstrom_metric(1.0, 0.0)
    sch = curvature.schwarzschild_metric(1.0)
    for x in ([0.0, 5.0, 1.0, 0.7], [0.0, 8.0, 0.6, 2.1]):
        gr, gs = rn(x), sch(x)
        for i in range(4):
            for j in range(4):
                assert abs(gr[i][j] - gs[i][j]) <= 1e-12 * (1.0 + abs(gs[i][j]))
    assert verify_vacuum(rn, [0.0, 8.0, 1.0, 0.7]) < TOL_FD


# --- Kerr horizons and ergosphere --------------------------------------------

def test_kerr_horizons():
    """r_pm = M +- sqrt(M^2 - a^2): sum = 2M, product = a^2; extremal at a = M."""
    M = 1.0
    for a in (0.0, 0.3, 0.6, 0.9):
        rminus, rplus = kerr_horizons(M, a)
        assert _approx(rplus, M + math.sqrt(M * M - a * a), 1e-12)
        assert _approx(rminus, M - math.sqrt(M * M - a * a), 1e-12)
        assert _approx(rplus + rminus, 2.0 * M, 1e-12)        # sum of roots
        assert _approx(rplus * rminus, a * a, 1e-12)          # product of roots
        assert rplus >= rminus
    # extremal Kerr a = M: the two horizons merge at r = M
    rm, rp = kerr_horizons(1.0, 1.0)
    assert _approx(rp, 1.0, 1e-9) and _approx(rm, 1.0, 1e-9)
    # a > M is a naked singularity -- no real horizon
    try:
        kerr_horizons(1.0, 1.5)
        raised = False
    except ValueError:
        raised = True
    assert raised


def test_kerr_ergosphere_outside_horizon():
    """At the equator the static-limit surface is at r = 2M, strictly OUTSIDE the
    outer horizon r_plus for a > 0 (the ergoregion)."""
    M = 1.0
    for a in (0.3, 0.6, 0.9):
        _, rplus = kerr_horizons(M, a)
        r_eq = kerr_ergosphere(M, a, math.pi / 2.0)
        assert _approx(r_eq, 2.0 * M, 1e-12)                  # = 2M at the equator
        assert r_eq > rplus                                   # ergosphere outside
    # at the pole the ergosphere touches the horizon
    a = 0.6
    _, rplus = kerr_horizons(M, a)
    assert _approx(kerr_ergosphere(M, a, 0.0), rplus, 1e-12)


# --- ADM 3+1 decomposition ----------------------------------------------------

def test_adm_minkowski_slice():
    """Inertial Minkowski: lapse alpha = 1, shift beta = 0, gamma = delta_ij,
    and the (vacuum, K = 0) Hamiltonian constraint vanishes."""
    mink = curvature.minkowski_metric()
    x = [0.0, 1.0, 1.0, 0.5]
    alpha, beta, gamma = adm_decompose(mink, x)
    assert _approx(alpha, 1.0, 1e-12)
    assert all(abs(b) <= 1e-12 for b in beta)
    for i in range(3):
        for j in range(3):
            assert abs(gamma[i][j] - (1.0 if i == j else 0.0)) <= 1e-12
    assert abs(hamiltonian_constraint_flat(mink, x)) <= 1e-9


def test_adm_lapse_from_inverse_metric():
    """The lapse reads off the time-time INVERSE component: alpha = 1/sqrt(-g^{tt}).
    For a static diagonal metric g_{tt} = -f, that is alpha = sqrt(f)."""
    for f_metric, x, f in (
        (curvature.schwarzschild_metric(1.0), [0.0, 8.0, 1.0, 0.7], 1.0 - 2.0 / 8.0),
        (de_sitter_metric(0.03), [0.0, 3.0, 1.0, 0.7], 1.0 - 0.03 * 9.0 / 3.0),
    ):
        alpha, beta, gamma = adm_decompose(f_metric, x)
        assert _approx(alpha, math.sqrt(f), 1e-9)
        assert all(abs(b) <= 1e-12 for b in beta)             # static: no shift


def test_schwarzschild_slice_is_scalar_flat():
    """The t = const Schwarzschild slice is curved but SCALAR-flat: its intrinsic
    R^(3) = 0, so a time-symmetric (K = 0) slice satisfies the Hamiltonian
    constraint -- as any vacuum slice must.  This validates the constraint code
    on a non-trivial (non-flat) 3-geometry."""
    sch = curvature.schwarzschild_metric(1.0)
    for r in (4.0, 6.0, 10.0):
        H = hamiltonian_constraint_flat(sch, [0.0, r, 1.0, 0.7])
        assert abs(H) < 1e-4
    # the slice is genuinely curved: its spatial metric is not delta_ij
    gamma = spatial_slice_metric(sch, 0.0)([6.0, 1.0, 0.7])
    assert abs(gamma[0][0] - 1.0) > 0.1                       # g_rr = 1/(1-2M/r) > 1


def test_hamiltonian_constraint_extrinsic_terms():
    """The K^2 - K_ij K^ij algebra: on a flat slice (R^(3) = 0) with isotropic
    K_ij = k delta_ij, H = (3k)^2 - 3k^2 = 6 k^2, and a source rho shifts it by
    -16 pi rho."""
    mink = curvature.minkowski_metric()
    x = [0.0, 1.0, 1.0, 0.5]
    k = 0.4
    K = [[k if i == j else 0.0 for j in range(3)] for i in range(3)]
    H = hamiltonian_constraint_flat(mink, x, K_ij=K)
    assert _approx(H, 6.0 * k * k, 1e-9)
    rho = 0.05
    Hrho = hamiltonian_constraint_flat(mink, x, K_ij=K, rho=rho)
    assert _approx(Hrho, 6.0 * k * k - 16.0 * math.pi * rho, 1e-9)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
