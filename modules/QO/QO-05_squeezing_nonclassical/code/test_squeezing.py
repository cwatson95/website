"""Tests for QO-05 squeezing & nonclassical light -- every claim checked against
a closed form (Scully & Zubairy, *Quantum Optics*, Ch. 2-3, 16, 18).

Run:  python3 test_squeezing.py        ->  "All N tests passed."

Conventions (hbar = 1):  X1=(a+a+)/2, X2=(a-a+)/2i;  squeeze operator
S(xi)=exp[1/2(xi* a^2 - xi a+^2)], xi=r e^{i phi}.  For phi=0 the squeezed
vacuum has Var X1 = 1/4 e^{-2r}, Var X2 = 1/4 e^{+2r}, product 1/16, only even
photon numbers, and <n> = sinh^2 r.
"""
import math

import numpy as np

from squeezing import (
    DEFAULT_N, TWO_MODE_N,
    annihilation, creation, quadrature_operators,
    vacuum_state, fock_state, coherent_state,
    squeeze_operator, squeezed_vacuum,
    quadrature_variances, photon_distribution,
    mean_photon, mean_photon_number,
    g2_zero, mandel_q,
    two_mode_squeeze_operator, two_mode_squeezed_vacuum,
    two_mode_photon_distribution, epr_variances,
)


# --- ladder algebra & quadratures -------------------------------------------

def test_ladder_operators_and_commutator():
    """a is the sqrt(n) superdiagonal; a+ its adjoint; [a,a+]=1 on the interior."""
    N = 12
    a, ad = annihilation(N), creation(N)
    assert np.allclose(np.diag(a, k=1), np.sqrt(np.arange(1, N)))
    assert np.allclose(ad, a.conj().T)
    comm = a @ ad - ad @ a
    assert np.allclose(np.diag(comm)[:N - 1], 1.0)          # interior = identity
    assert abs(np.trace(comm)) < 1e-10                       # trace 0 (truncation)


def test_quadrature_commutator_is_i_over_two():
    """[X1, X2] = i/2 on the interior, so Var X1 * Var X2 >= 1/16."""
    N = 12
    X1, X2 = quadrature_operators(N)
    comm = X1 @ X2 - X2 @ X1
    assert np.allclose(np.diag(comm)[:N - 1], 0.5j)


# --- vacuum / coherent sit at the standard quantum limit --------------------

def test_vacuum_and_coherent_are_sql():
    """Vacuum and coherent states have Var X1 = Var X2 = 1/4 (product 1/16)."""
    for state in (vacuum_state(DEFAULT_N), coherent_state(1.5, DEFAULT_N)):
        v1, v2 = quadrature_variances(state)
        assert abs(v1 - 0.25) < 1e-6 and abs(v2 - 0.25) < 1e-6
        assert abs(v1 * v2 - 1.0 / 16.0) < 1e-6


def test_squeeze_operator_zero_is_identity_and_unitary():
    """S(0) = I, and S(xi) is unitary (M anti-Hermitian -> expm unitary)."""
    N = 40
    assert np.allclose(squeeze_operator(0.0, N), np.eye(N))
    S = squeeze_operator(0.9, N, phi=0.7)
    assert np.allclose(S.conj().T @ S, np.eye(N), atol=1e-9)


# --- the headline squeezing result ------------------------------------------

def test_squeezed_vacuum_quadrature_variances():
    """Var X1 = 1/4 e^{-2r} (below 1/4), Var X2 = 1/4 e^{+2r} (above)."""
    for r in (0.2, 0.4, 0.6, 0.8, 1.0):
        v1, v2 = quadrature_variances(squeezed_vacuum(r))
        assert abs(v1 - 0.25 * math.exp(-2 * r)) < 1e-3
        assert abs(v2 - 0.25 * math.exp(+2 * r)) < 1e-3
        assert v1 < 0.25 < v2                                # one below, one above SQL


def test_minimum_uncertainty_product_is_one_sixteenth():
    """The squeezed vacuum stays a minimum-uncertainty state: product = 1/16."""
    for r in (0.0, 0.3, 0.6, 0.9, 1.2):
        v1, v2 = quadrature_variances(squeezed_vacuum(r))
        assert abs(v1 * v2 - 1.0 / 16.0) < 1e-3


def test_phi_rotates_the_squeezed_quadrature():
    """phi = pi swaps which quadrature is squeezed (xi -> -r)."""
    r = 0.7
    v1, v2 = quadrature_variances(squeezed_vacuum(r, phi=math.pi))
    assert abs(v1 - 0.25 * math.exp(+2 * r)) < 1e-3          # X1 now anti-squeezed
    assert abs(v2 - 0.25 * math.exp(-2 * r)) < 1e-3          # X2 now squeezed


# --- photon content: even only, <n> = sinh^2 r ------------------------------

def test_only_even_photon_numbers_populated():
    """The squeezed vacuum is built from photon pairs: P(odd) = 0 exactly
    (S connects |n> only to |n +/- 2>), the even ones are populated."""
    P = photon_distribution(squeezed_vacuum(0.8))
    assert P[1::2].sum() < 1e-12                              # no odd photons
    assert P[0] > 0 and P[2] > 0 and P[4] > 0                # even ones present
    assert abs(P.sum() - 1.0) < 1e-9                          # normalized


def test_photon_distribution_matches_closed_form():
    """P(2m) = (1/cosh r) [ (2m)! / (2^m m!)^2 ] (tanh r)^{2m}  (Scully-Zubairy)."""
    r = 0.7
    P = photon_distribution(squeezed_vacuum(r))
    cr, tr = math.cosh(r), math.tanh(r)
    for m in range(6):
        closed = (1.0 / cr) * (math.factorial(2 * m)
                               / (2.0 ** m * math.factorial(m)) ** 2) * tr ** (2 * m)
        assert abs(P[2 * m] - closed) < 1e-6, (m, P[2 * m], closed)


def test_mean_photon_is_sinh_squared_r():
    """<n> = sinh^2 r, both closed-form and summed from the distribution."""
    for r in (0.0, 0.3, 0.6, 0.9, 1.2):
        assert abs(mean_photon(r) - math.sinh(r) ** 2) < 1e-12
        nbar = mean_photon_number(squeezed_vacuum(r))
        assert abs(nbar - math.sinh(r) ** 2) < 1e-4


def test_r_zero_recovers_vacuum():
    """r = 0: squeezed vacuum IS the vacuum -- |0>, variances 1/4, <n> = 0."""
    sv = squeezed_vacuum(0.0)
    assert np.allclose(sv, vacuum_state(DEFAULT_N))
    v1, v2 = quadrature_variances(sv)
    assert abs(v1 - 0.25) < 1e-9 and abs(v2 - 0.25) < 1e-9
    assert mean_photon_number(sv) < 1e-12


# --- nonclassicality faces: g^(2)(0), Mandel Q ------------------------------

def test_g2_and_mandel_classify_states():
    """Fock |1>: g2=0, Q=-1 (sub-Poissonian/antibunched, nonclassical);
    coherent: g2=1, Q=0 (Poissonian); squeezed vacuum: g2=3+1/sinh^2 r > 1
    (super-Poissonian -- nonclassical but NOT antibunched)."""
    assert abs(g2_zero(fock_state(1)) - 0.0) < 1e-9
    assert abs(mandel_q(fock_state(1)) + 1.0) < 1e-9         # Q = -1
    assert abs(g2_zero(coherent_state(2.0)) - 1.0) < 1e-6
    assert abs(mandel_q(coherent_state(2.0))) < 1e-6         # Q = 0
    r = 0.8
    sv = squeezed_vacuum(r)
    assert abs(g2_zero(sv) - (3.0 + 1.0 / math.sinh(r) ** 2)) < 1e-3
    assert mandel_q(sv) > 0                                   # super-Poissonian


def test_squeezing_pushes_a_quadrature_below_the_vacuum():
    """The defining nonclassical feature: one quadrature variance < 1/4."""
    for r in (0.1, 0.5, 1.0):
        v1, v2 = quadrature_variances(squeezed_vacuum(r))
        assert min(v1, v2) < 0.25


# --- two-mode squeezing & EPR entanglement ----------------------------------

def test_two_mode_squeeze_operator_unitary():
    S2 = two_mode_squeeze_operator(0.6, TWO_MODE_N, phi=0.4)
    assert np.allclose(S2.conj().T @ S2, np.eye(TWO_MODE_N ** 2), atol=1e-8)


def test_two_mode_is_photon_number_correlated():
    """|TMSV> = sech r sum_n tanh^n r |n,n>: only the diagonal n_a = n_b is
    populated, with P(n,n) = (tanh^2 r)^n / cosh^2 r."""
    r = 0.6
    Pab = two_mode_photon_distribution(two_mode_squeezed_vacuum(r))
    off = Pab - np.diag(np.diag(Pab))
    assert np.max(np.abs(off)) < 1e-10                       # nothing off-diagonal
    cr, tr = math.cosh(r), math.tanh(r)
    for n in range(5):
        assert abs(Pab[n, n] - tr ** (2 * n) / cr ** 2) < 1e-6


def test_two_mode_per_mode_mean_photon_is_sinh_squared():
    """Each mode of the TMSV carries <n> = sinh^2 r (a thermal-looking marginal)."""
    for r in (0.3, 0.5, 0.7):
        Pab = two_mode_photon_distribution(two_mode_squeezed_vacuum(r))
        na = float(np.sum(np.arange(Pab.shape[0])[:, None] * Pab))
        assert abs(na - math.sinh(r) ** 2) < 5e-3


def test_epr_joint_quadratures_beat_the_sql():
    """Var(X_a + X_b) = Var(Y_a - Y_b) = (1/2) e^{-2r} < 1/2 -- the continuous-
    variable EPR correlation (the entangled-photon resource, ~QM-21)."""
    for r in (0.3, 0.5, 0.6):
        vx, vy = epr_variances(r)
        assert abs(vx - 0.5 * math.exp(-2 * r)) < 5e-3
        assert abs(vy - 0.5 * math.exp(-2 * r)) < 5e-3
        assert vx < 0.5 and vy < 0.5                          # below the vacuum bound


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
