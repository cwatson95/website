"""Tests for QM-09 oscillator -- every claim checked against a closed form.

Run directly:   python3 test_oscillator.py        (-> "All N tests passed.")
Or with pytest: pytest test_oscillator.py

Two methods, one spectrum:
  * the ALGEBRAIC tests verify the ladder algebra ([a,a+]=1, N=diag, the
    raising/lowering relations, E_n = n+1/2) and HANDLE the truncation artifact
    in the last row/col honestly;
  * the ANALYTIC tests verify orthonormality of the Hermite-Gaussians and that
    each one solves the finite-difference TISE;
  * the final test cross-checks that both routes give E_n = hbar*omega*(n+1/2).
"""
import math

import numpy as np

from oscillator import (
    HBAR, OMEGA, energy, zero_point_energy,
    annihilation, creation, number_operator, hamiltonian_matrix,
    position_operator, momentum_operator, hamiltonian_from_xp,
    commutator, basis_vector, algebraic_spectrum,
    psi, ground_state, overlap, fd_spectrum, fd_residual,
)


# ----------------------------------------------------------------------------
# ALGEBRAIC METHOD
# ----------------------------------------------------------------------------

def test_ladder_commutator_interior_is_identity():
    """[a, a+] = 1 on the interior (Griffiths Eq. 2.51-ish, p.60)."""
    D = 10
    comm = commutator(annihilation(D), creation(D))
    interior = comm[:D - 1, :D - 1]
    assert np.allclose(interior, np.eye(D - 1)), "interior of [a,a+] must be I"


def test_truncation_artifact_is_honest():
    """The price of a finite basis: tr([a,a+]) = 0 (true of ANY finite matrices),
    so [a,a+] cannot be I everywhere -- the whole defect sits in one corner,
    [a,a+][D-1,D-1] = -(D-1).  We assert exactly that, not a fudged 1."""
    D = 10
    comm = commutator(annihilation(D), creation(D))
    assert abs(np.trace(comm)) < 1e-12                       # trace is exactly 0
    assert abs(comm[D - 1, D - 1] - (-(D - 1))) < 1e-12      # corner = -(D-1)
    diag = np.diag(comm).real
    assert np.allclose(diag[:D - 1], 1.0)                    # first D-1 entries = 1


def test_number_operator_is_diagonal_count():
    """N = a+ a = diag(0, 1, 2, ..., D-1) -- exact even under truncation, since
    a+a never needs the rung above the top."""
    D = 12
    N = number_operator(D)
    assert np.allclose(N, np.diag(np.arange(D)))


def test_hamiltonian_spectrum_is_n_plus_half():
    """H = hbar*omega*(N + 1/2) has eigenvalues E_n = hbar*omega*(n + 1/2)."""
    D = 15
    ev = algebraic_spectrum(D)
    assert np.allclose(ev, [energy(n) for n in range(D)])
    assert abs(ev[0] - zero_point_energy()) < 1e-12          # zero-point energy
    assert abs(zero_point_energy() - 0.5 * HBAR * OMEGA) < 1e-12


def test_raising_lowering_relations():
    """a+|n> = sqrt(n+1)|n+1>,  a|n> = sqrt(n)|n-1>,  a|0> = 0
    (Griffiths Eq. 2.66/2.68, pp.63-64)."""
    D = 12
    a, ad = annihilation(D), creation(D)
    # a|0> = 0
    assert np.allclose(a @ basis_vector(0, D), 0.0)
    for n in range(D - 1):                                   # raising, n -> n+1
        got = ad @ basis_vector(n, D)
        assert np.allclose(got, math.sqrt(n + 1) * basis_vector(n + 1, D))
    for n in range(1, D):                                    # lowering, n -> n-1
        got = a @ basis_vector(n, D)
        assert np.allclose(got, math.sqrt(n) * basis_vector(n - 1, D))


def test_canonical_commutation_relation():
    """[x, p] = i*hbar on the interior, from x=sqrt(hbar/2mw)(a+a+),
    p=i sqrt(hbar m w/2)(a+-a).  (The corner carries the truncation artifact;
    trace is still 0.)"""
    D = 12
    xp = commutator(position_operator(D), momentum_operator(D))
    interior = xp[:D - 1, :D - 1]
    assert np.allclose(interior, 1j * HBAR * np.eye(D - 1))
    assert abs(np.trace(xp)) < 1e-12


def test_hamiltonian_from_xp_matches_ladder_form():
    """H = p^2/2m + (1/2) m w^2 x^2 equals hbar*omega*(N+1/2) on the interior."""
    D = 12
    H1 = hamiltonian_from_xp(D)
    H2 = hamiltonian_matrix(D)
    assert np.allclose(H1[:D - 1, :D - 1], H2[:D - 1, :D - 1])


# ----------------------------------------------------------------------------
# ANALYTIC METHOD
# ----------------------------------------------------------------------------

def test_eigenfunctions_orthonormal():
    """<psi_m|psi_n> = delta_{mn} for the Hermite-Gaussians (Griffiths p.64)."""
    nmax = 6
    for m in range(nmax):
        for n in range(nmax):
            val = overlap(m, n)
            assert abs(val - (1.0 if m == n else 0.0)) < 1e-6, (m, n, val)


def test_ground_state_is_normalised_gaussian():
    """psi_0 is the pure Gaussian (m w/pi hbar)^{1/4} e^{-xi^2/2}, and psi(0,.)
    agrees with the closed form."""
    x = np.linspace(-12, 12, 4001)
    assert np.allclose(psi(0, x), ground_state(x))
    from scipy.integrate import simpson
    assert abs(simpson(ground_state(x) ** 2, x=x) - 1.0) < 1e-6


def test_eigenfunctions_solve_fd_tise():
    """Each analytic psi_n satisfies the finite-difference TISE with E_n=n+1/2:
    the relative residual ||H psi_n - E_n psi_n|| / ||psi_n|| is tiny."""
    for n in range(5):
        assert fd_residual(n) < 2e-3, (n, fd_residual(n))


def test_psi_scalar_and_vector_agree():
    """psi accepts a scalar or an array and is consistent between them."""
    xs = [-1.3, 0.0, 0.7, 2.1]
    for n in range(4):
        arr = psi(n, np.array(xs))
        for x, a in zip(xs, arr):
            assert abs(psi(n, x) - a) < 1e-12


def test_parity_of_eigenfunctions():
    """psi_n has parity (-1)^n: even n symmetric, odd n antisymmetric."""
    x = np.linspace(0.1, 6.0, 50)
    for n in range(6):
        sign = (-1) ** n
        assert np.allclose(psi(n, -x), sign * psi(n, x))


# ----------------------------------------------------------------------------
# CROSS-CHECK: both methods, one spectrum
# ----------------------------------------------------------------------------

def test_two_methods_same_spectrum():
    """The ladder (algebraic) spectrum and the finite-difference (analytic)
    spectrum agree, and both equal E_n = hbar*omega*(n + 1/2)."""
    k = 6
    alg = algebraic_spectrum(20)[:k]
    ana = fd_spectrum(L=10.0, N=801, k=k)
    target = np.array([energy(n) for n in range(k)])
    assert np.allclose(alg, target, atol=1e-12)             # algebraic is exact
    assert np.allclose(ana, target, atol=5e-3)              # FD converges to it
    assert np.allclose(alg, ana, atol=5e-3)                 # so the two agree


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
