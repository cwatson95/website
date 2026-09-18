"""Tests for QM-22 relativistic QM -- every claim checked numerically.

Griffiths is a non-relativistic text (zero hits for "Klein-Gordon"; the Dirac
equation appears only in passing, p.388/p.415 -- see ../refs.md).  So, exactly as
in ~QM-01_origins, THE VERIFICATION IS THE CODE: the gamma-matrix / Clifford
algebra, both equations' dispersion relations, the spinor solutions, and the g=2
non-relativistic limit are all checked here against closed forms.

The gamma-matrix and spinor identities are exact in finite dimension and checked
to machine precision.  The Klein-Gordon box operator is a finite-difference
operator, so its on-shell residual is checked to the discretization floor (~1e-6).

Run directly:   python3 test_relativistic.py     (-> "All N tests passed.")
Or with pytest: pytest test_relativistic.py
"""
import math
import os
import sys

import numpy as np

from relativistic import (
    I2, I4, metric, minkowski_dot, lower_index, pauli,
    commutator, anticommutator, dagger, sigma_dot,
    dirac_gamma, gamma5, clifford,
    kg_energy, plane_wave, kg_operator_fd, kg_eigenvalue,
    four_momentum, p_slash, dirac_matrix, dirac_determinant, dirac_squared,
    u_spinor, v_spinor, dirac_solutions,
    nonrel_energy, energy_expansion, kinetic_momentum_operators,
    sigma_dot_pi_squared, dirac_g_factor,
)

_RANGE = range(4)                         # the four spacetime indices
_TEST_P = [[0.3, -0.4, 0.5], [0.0, 0.0, 0.0], [1.2, 0.0, -0.7], [0.1, 0.2, 0.3]]
_MASSES = [1.0, 0.5, 2.0]


# --- 0. conventions ----------------------------------------------------------

def test_metric_signature():
    """g = diag(1,-1,-1,-1); g is its own inverse (g g = I) and det g = -1."""
    g = metric()
    assert np.allclose(g, np.diag([1.0, -1.0, -1.0, -1.0]))
    assert np.allclose(g @ g, np.eye(4))            # raising == lowering
    assert math.isclose(np.linalg.det(g), -1.0)
    # the invariant dot uses this signature: p.p = E^2 - |p|^2
    p = [2.0, 1.0, 0.0, 0.0]
    assert math.isclose(minkowski_dot(p, p).real, 4.0 - 1.0)
    assert np.allclose(lower_index(p), [2.0, -1.0, 0.0, 0.0])


def test_pauli_algebra():
    """sigma_i^2 = I, tr = 0, Hermitian; {sigma_i,sigma_j}=2 delta_ij I;
    [sigma_i,sigma_j]=2 i eps_ijk sigma_k -- the su(2) algebra the gammas use."""
    s = [pauli(i) for i in range(4)]
    eps = lambda i, j, k: (i - j) * (j - k) * (k - i) / 2
    for i in (1, 2, 3):
        assert np.allclose(s[i] @ s[i], I2)
        assert np.allclose(s[i], dagger(s[i]))
        assert abs(np.trace(s[i])) < 1e-12
        for j in (1, 2, 3):
            assert np.allclose(anticommutator(s[i], s[j]), 2.0 * (i == j) * I2)
            comm = commutator(s[i], s[j])
            expect = 2j * sum(eps(i, j, k) * s[k] for k in (1, 2, 3))
            assert np.allclose(comm, expect)


def test_pauli_cross_check_MA18():
    """Cross-check our locally-built Pauli matrices against ~MA-18's group-theory
    pauli() (read its API: pauli() -> (sx, sy, sz) as Python lists).  Imported by
    relative path, mirroring how ~QM-10 imports ~MA-12 and ~QM-05 cross-checks
    ~MA-04.  This is the only inter-module import and it is test-only."""
    here = os.path.dirname(os.path.abspath(__file__))
    ma18 = os.path.abspath(os.path.join(here, "..", "..", "..", "MA",
                                        "MA-18_group_theory", "code"))
    if ma18 not in sys.path:
        sys.path.insert(0, ma18)
    from groups import pauli as ma18_pauli           # noqa: E402
    sx, sy, sz = ma18_pauli()
    assert np.allclose(np.array(sx, dtype=complex), pauli(1))
    assert np.allclose(np.array(sy, dtype=complex), pauli(2))
    assert np.allclose(np.array(sz, dtype=complex), pauli(3))


# --- 1. gamma matrices & the Clifford algebra --------------------------------

def test_clifford_algebra_all_pairs():
    """{gamma^mu, gamma^nu} = 2 g^{mu nu} I_4 for ALL 16 (mu,nu) pairs: diagonal
    +2I (00), -2I (11/22/33), zero off-diagonal.  The defining relation."""
    g = metric()
    for mu in _RANGE:
        for nu in _RANGE:
            assert np.allclose(clifford(mu, nu), 2.0 * g[mu, nu] * I4), (mu, nu)
    # in particular (gamma^0)^2 = +I, (gamma^i)^2 = -I
    assert np.allclose(dirac_gamma(0) @ dirac_gamma(0), I4)
    for i in (1, 2, 3):
        assert np.allclose(dirac_gamma(i) @ dirac_gamma(i), -I4)


def test_gamma_hermiticity():
    """(gamma^0)^dagger = gamma^0 (Hermitian); (gamma^i)^dagger = -gamma^i
    (anti-Hermitian); and the unified relation gamma^{mu dagger} = g^0 gamma^mu g^0."""
    g0 = dirac_gamma(0)
    assert np.allclose(dagger(g0), g0)
    for i in (1, 2, 3):
        assert np.allclose(dagger(dirac_gamma(i)), -dirac_gamma(i))
    for mu in _RANGE:
        gm = dirac_gamma(mu)
        assert np.allclose(dagger(gm), g0 @ gm @ g0)


def test_gamma5_properties():
    """gamma^5 = i g^0 g^1 g^2 g^3: (gamma^5)^2 = I, Hermitian, and {gamma^5,gamma^mu}=0
    for every mu (anticommutes with all four)."""
    g5 = gamma5()
    assert np.allclose(g5, np.block([[np.zeros((2, 2)), I2], [I2, np.zeros((2, 2))]]))
    assert np.allclose(g5 @ g5, I4)
    assert np.allclose(dagger(g5), g5)
    for mu in _RANGE:
        assert np.allclose(anticommutator(g5, dirac_gamma(mu)), np.zeros((4, 4))), mu


def test_pslash_squared_is_p_dot_p():
    """p-slash^2 = (p.p) I_4 -- a direct consequence of the Clifford algebra
    (p-slash^2 = p_mu p_nu gamma^mu gamma^nu = p_mu p_nu (1/2){g^mu,g^nu} = p.p I).
    This identity is what makes Dirac the square root of Klein-Gordon."""
    rng = np.random.default_rng(0)
    for _ in range(5):
        p4 = rng.normal(size=4)
        ps = p_slash(p4)
        assert np.allclose(ps @ ps, minkowski_dot(p4, p4) * I4)


# --- 2. Klein-Gordon ---------------------------------------------------------

def test_kg_planewave_on_shell():
    """A plane wave exp(-i p.x) satisfies (box + m^2)phi = 0 iff E^2 = p^2 + m^2.
    Checked for BOTH energy signs (negative-energy solutions exist) at several
    points; on-shell residual is at the finite-difference floor (~1e-6)."""
    x_pts = [[0.11, 0.22, 0.33, 0.44], [1.0, -0.5, 0.7, 0.2], [0.0, 0.0, 0.0, 0.0]]
    for m in _MASSES:
        for p3 in _TEST_P:
            for sign in (+1, -1):
                p4 = four_momentum(p3, m, sign)
                # on shell p.p = m^2 exactly:
                assert abs(minkowski_dot(p4, p4) - m * m) < 1e-10
                for x4 in x_pts:
                    assert abs(kg_operator_fd(p4, m, x4)) < 1e-4, (m, p3, sign, x4)


def test_kg_off_shell_matches_eigenvalue():
    """Off shell, (box+m^2)phi = -(E^2 - p^2 - m^2) phi: the finite-difference
    operator reproduces the closed-form eigenvalue kg_eigenvalue (and it is
    nonzero, i.e. the plane wave is NOT a solution)."""
    m = 1.0
    x4 = [0.2, 0.1, -0.3, 0.05]
    for p3 in _TEST_P:
        for E in (0.4, 1.7, 3.0):                    # arbitrary, off shell
            p4 = np.array([E, p3[0], p3[1], p3[2]])
            lam = kg_eigenvalue(p4, m)
            got = kg_operator_fd(p4, m, x4)
            assert abs(got - lam * plane_wave(p4, x4)) < 1e-3, (p3, E)
            if abs(E * E - (np.dot(p3, p3) + m * m)) > 1e-3:
                assert abs(got) > 1e-6                # genuinely not a solution


def test_kg_negative_energy_exists():
    """The two roots E = +/- sqrt(p^2+m^2) BOTH solve KG -- the indefinite-energy
    spectrum (cured only by reinterpretation in ~QF-01)."""
    m, p3 = 1.0, [0.6, 0.0, 0.8]
    Ep = kg_energy(p3, m, +1)
    En = kg_energy(p3, m, -1)
    assert Ep > 0 and En < 0 and math.isclose(Ep, -En)
    x4 = [0.3, 0.2, 0.1, 0.4]
    assert abs(kg_operator_fd(four_momentum(p3, m, +1), m, x4)) < 1e-4
    assert abs(kg_operator_fd(four_momentum(p3, m, -1), m, x4)) < 1e-4


# --- 3. Dirac ----------------------------------------------------------------

def test_dirac_determinant_closed_form():
    """det(p-slash - m) = (p.p - m^2)^2 for arbitrary p4 (random, off shell), and
    it vanishes exactly on shell -- so nontrivial spinor solutions require
    E^2 = p^2 + m^2."""
    rng = np.random.default_rng(1)
    m = 1.3
    for _ in range(5):
        p4 = rng.normal(size=4) + 0.0j
        expect = (minkowski_dot(p4, p4) - m * m) ** 2
        assert np.allclose(dirac_determinant(p4, m), expect)
    for p3 in _TEST_P:
        p4 = four_momentum(p3, m, +1)               # on shell
        assert abs(dirac_determinant(p4, m)) < 1e-12


def test_dirac_squares_to_klein_gordon():
    """(p-slash - m)(p-slash + m) = (p.p - m^2) I_4: applying the Dirac operator
    twice gives the Klein-Gordon operator -- 'Dirac^2 = Klein-Gordon', and uses
    p-slash^2 = p.p I (the Clifford algebra)."""
    rng = np.random.default_rng(2)
    for m in _MASSES:
        for _ in range(4):
            p4 = rng.normal(size=4) + 0.0j
            lhs = dirac_squared(p4, m)
            assert np.allclose(lhs, (minkowski_dot(p4, p4) - m * m) * I4)
        for p3 in _TEST_P:                           # on shell -> zero
            assert np.allclose(dirac_squared(four_momentum(p3, m, +1), m), 0.0)


def test_dirac_spinors_solve_equation():
    """The 4 plane-wave spinors: u0,u1 (positive energy) solve (p-slash - m)u = 0;
    v0,v1 (negative energy / antiparticle) solve (p-slash + m)v = 0."""
    for m in _MASSES:
        for p3 in _TEST_P:
            p4 = four_momentum(p3, m, +1)
            Dminus = dirac_matrix(p4, m)             # p-slash - m
            Dplus = p_slash(p4) + m * I4             # p-slash + m
            sols = dirac_solutions(p3, m)
            for k in ("u0", "u1"):
                assert np.allclose(Dminus @ sols[k], 0.0, atol=1e-12), (m, p3, k)
            for k in ("v0", "v1"):
                assert np.allclose(Dplus @ sols[k], 0.0, atol=1e-12), (m, p3, k)


def test_dirac_spinor_normalization():
    """Standard spinor relations (normalization N = sqrt(E+m)), with bar(w)=w^dag g^0:
        u-bar^r u^s = +2m delta_rs,   v-bar^r v^s = -2m delta_rs,
        u^{r dag} u^s = v^{r dag} v^s = 2E delta_rs,   u-bar^r v^s = 0.
    The sign of v-bar v is the antiparticle signature; the (-) makes the density
    indefinite -- the Dirac analogue of the KG probability problem (~QF-01)."""
    g0 = dirac_gamma(0)
    m, p3 = 1.0, [0.5, -0.3, 0.9]
    E = kg_energy(p3, m, +1)
    u = [u_spinor(p3, m, s) for s in (0, 1)]
    v = [v_spinor(p3, m, s) for s in (0, 1)]
    for r in (0, 1):
        for s in (0, 1):
            d = 1.0 if r == s else 0.0
            assert abs(dagger(u[r]) @ g0 @ u[s] - 2 * m * d) < 1e-12     # u-bar u
            assert abs(dagger(v[r]) @ g0 @ v[s] + 2 * m * d) < 1e-12     # v-bar v
            assert abs(dagger(u[r]) @ u[s] - 2 * E * d) < 1e-12          # u^dag u
            assert abs(dagger(v[r]) @ v[s] - 2 * E * d) < 1e-12          # v^dag v
            assert abs(dagger(u[r]) @ g0 @ v[s]) < 1e-12                 # u-bar v = 0


# --- 4. non-relativistic limit: spin & g = 2 ---------------------------------

def test_pauli_vector_identity():
    """(sigma.a)(sigma.b) = (a.b) I + i sigma.(a x b) for numeric 3-vectors -- the
    algebraic identity behind (sigma.pi)^2, hence behind g = 2."""
    rng = np.random.default_rng(3)
    for _ in range(6):
        a, b = rng.normal(size=3), rng.normal(size=3)
        lhs = sigma_dot(a) @ sigma_dot(b)
        rhs = np.dot(a, b) * I2 + 1j * sigma_dot(np.cross(a, b))
        assert np.allclose(lhs, rhs)


def test_nonrelativistic_energy_limit():
    """E = sqrt(p^2+m^2) -> m + p^2/2m for |p|<<m, with leading correction -p^4/8m^3.
    Checks E-m against p^2/2m at small p and the full two-term expansion."""
    m = 1.0
    # leading term dominates at small momentum
    for p in (1e-2, 1e-3):
        E_minus_m = nonrel_energy([p, 0.0, 0.0], m)
        assert math.isclose(E_minus_m, p * p / (2 * m), rel_tol=1e-3)
    # the relativistic correction has the right sign and size (E < m + p^2/2m)
    p3 = [0.2, 0.1, 0.0]
    exact = nonrel_energy(p3, m)
    schroedinger = energy_expansion(p3, m, order=1) - m
    with_corr = energy_expansion(p3, m, order=2) - m
    assert with_corr < schroedinger                  # -p^4/8m^3 lowers it
    assert abs(with_corr - exact) < abs(schroedinger - exact)   # 2-term is closer


def test_magnetic_commutator():
    """Minimal coupling realized: [pi_x, pi_y] = i q B on the interior (the gauge-
    invariant magnetic commutator), pi_z = 0.  This is the sole physical input to
    the g-factor extraction."""
    N, q, B = 8, 1.3, 0.7
    pix, piy, piz = kinetic_momentum_operators(N, q, B)
    comm = commutator(pix, piy)
    interior = slice(0, N - 1)
    assert np.allclose(comm[interior, interior],
                       1j * q * B * np.eye(N)[interior, interior])
    assert np.allclose(piz, 0.0)


def test_dirac_g_factor_is_two():
    """The crux: the non-relativistic reduction of the Dirac equation gives the
    Pauli equation with spin g-factor = 2.  (sigma.pi)^2 = pi^2 I - q sigma.B, so
    the spin Zeeman term is -(q/2m) g S.B with g = 2 -- spin and its g=2 emerge
    automatically (no input by hand).  Checked across field strengths."""
    for (q, B) in [(1.0, 0.7), (2.0, 0.3), (0.5, 1.1)]:
        g, residual = dirac_g_factor(N=10, q=q, B=B)
        assert abs(g - 2.0) < 1e-9, (q, B, g)
        assert residual < 1e-9, (q, B, residual)
    # and the operator identity (sigma.pi)^2 - pi^2 = -q sigma.B holds on interior
    N, q, B = 10, 1.0, 0.7
    pix, piy, piz = kinetic_momentum_operators(N, q, B)
    D = sigma_dot_pi_squared(N, q, B)
    O = np.kron(I2, pix @ pix + piy @ piy + piz @ piz)
    target = np.kron(-q * B * pauli(3), np.eye(N))
    idx = [sp * N + o for sp in (0, 1) for o in range(N - 1)]
    sub = np.ix_(idx, idx)
    assert np.allclose((D - O)[sub], target[sub])


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
