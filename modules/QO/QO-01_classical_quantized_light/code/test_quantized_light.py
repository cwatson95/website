"""Tests for QO-01 classical & quantized light -- every claim checked against a
closed form (Scully & Zubairy, *Quantum Optics*).

Run:  python3 test_quantized_light.py     ->  "All N tests passed."

Three groups:
  * the MODE-as-oscillator algebra (ladder commutator, number operator, ladder
    relations, Fock orthonormality, spectrum) -- the ~QM-09 bridge B6;
  * COHERENT states: eigenstate-of-a property, Poisson statistics, <n> = |alpha|^2,
    Delta n = sqrt<n>, Mandel Q = 0;
  * QUADRATURES: [X,P]=i/2, vacuum/coherent minimum-uncertainty Delta X Delta P = 1/4,
    and the Fock (2n+1)/4 noise.
"""
import math

import numpy as np

from quantized_light import (
    HBAR, OMEGA, energy, zero_point_energy,
    annihilation, creation, number, commutator, fock_state, expectation,
    coherent_state, photon_distribution, mean_n, var_n, mandel_q,
    quadrature_x, quadrature_p, quadrature_variance,
)


# ----------------------------------------------------------------------------
# 1. The quantized mode = a quantum SHO (ladder algebra)
# ----------------------------------------------------------------------------

def test_ladder_commutator_interior_is_identity():
    """[a, a+] = 1 on the interior (Scully & Zubairy Sec. 1.1)."""
    N = 12
    comm = commutator(annihilation(N), creation(N))
    interior = comm[:N - 1, :N - 1]
    assert np.allclose(interior, np.eye(N - 1))
    # truncation is honest: trace must be 0, defect parked in the corner
    assert abs(np.trace(comm)) < 1e-12
    assert abs(comm[N - 1, N - 1] - (-(N - 1))) < 1e-12


def test_number_operator_and_spectrum():
    """n = a+a = diag(0..N-1); H = hbar*omega*(n+1/2) gives E_n = (n+1/2),
    with vacuum zero-point energy 1/2."""
    N = 12
    assert np.allclose(number(N), np.diag(np.arange(N)))
    assert abs(zero_point_energy() - 0.5 * HBAR * OMEGA) < 1e-12
    for n in range(N):
        assert abs(energy(n) - HBAR * OMEGA * (n + 0.5)) < 1e-12


def test_ladder_relations():
    """a|n> = sqrt(n)|n-1>,  a+|n> = sqrt(n+1)|n+1>,  a|0> = 0
    (Scully & Zubairy Sec. 1.2)."""
    N = 12
    a, ad = annihilation(N), creation(N)
    assert np.allclose(a @ fock_state(0, N), 0.0)
    for n in range(1, N):
        assert np.allclose(a @ fock_state(n, N), math.sqrt(n) * fock_state(n - 1, N))
    for n in range(N - 1):
        assert np.allclose(ad @ fock_state(n, N), math.sqrt(n + 1) * fock_state(n + 1, N))


def test_fock_states_orthonormal():
    """<m|n> = delta_{mn}: the number states form an orthonormal basis."""
    N = 10
    for m in range(N):
        for n in range(N):
            val = np.vdot(fock_state(m, N), fock_state(n, N))
            assert abs(val - (1.0 if m == n else 0.0)) < 1e-12


def test_fock_photon_statistics_are_sharp():
    """A Fock state |n> has exactly n photons: <n> = n and Delta n = 0
    (sub-Poissonian, the antithesis of classical light)."""
    N = 30
    for n in (0, 1, 5, 12):
        st = fock_state(n, N)
        assert abs(mean_n(st) - n) < 1e-12
        assert abs(var_n(st)) < 1e-12
        assert expectation(number(N), st) == mean_n(st) or abs(expectation(number(N), st) - n) < 1e-12


# ----------------------------------------------------------------------------
# 2. Coherent states -- eigenstates of a, Poissonian
# ----------------------------------------------------------------------------

def test_coherent_is_eigenstate_of_annihilation():
    """a|alpha> = alpha|alpha> away from the truncation, for real and complex alpha
    (Scully & Zubairy Sec. 2.2)."""
    N = 60
    for alpha in (2.0, 1.5 + 0.8j, -1.0j):
        coh = coherent_state(alpha, N)
        assert abs(np.vdot(coh, coh) - 1.0) < 1e-12            # normalized
        resid = np.linalg.norm(annihilation(N) @ coh - alpha * coh)
        assert resid < 1e-9, (alpha, resid)


def test_coherent_photon_distribution_is_poisson():
    """P(n) = |<n|alpha>|^2 = e^{-|alpha|^2} |alpha|^{2n} / n!  (Poisson)."""
    N = 60
    alpha = 1.7 + 0.6j
    nbar = abs(alpha) ** 2
    P = photon_distribution(coherent_state(alpha, N))
    poisson = np.array([math.exp(-nbar) * nbar ** n / math.factorial(n) for n in range(15)])
    assert np.allclose(P[:15], poisson, atol=1e-9)


def test_coherent_mean_and_variance():
    """<n> = |alpha|^2 and (Delta n)^2 = <n> (Delta n = sqrt<n> = |alpha|):
    the Poissonian signature."""
    N = 60
    for alpha in (0.5, 2.0, 2.5 + 1.0j):
        coh = coherent_state(alpha, N)
        nbar = abs(alpha) ** 2
        assert abs(mean_n(coh) - nbar) < 1e-9
        assert abs(var_n(coh) - nbar) < 1e-9                   # Delta n^2 = <n>
        assert abs(math.sqrt(var_n(coh)) - abs(alpha)) < 1e-6  # Delta n = |alpha|


def test_coherent_mandel_q_is_zero():
    """Mandel Q = ((Delta n)^2 - <n>)/<n> = 0 for coherent light (Poissonian)."""
    N = 60
    for alpha in (1.0, 2.0, 1.2 + 1.2j):
        assert abs(mandel_q(coherent_state(alpha, N))) < 1e-9
    # a Fock state is sub-Poissonian: Q = -1
    assert abs(mandel_q(fock_state(4, N)) - (-1.0)) < 1e-12


# ----------------------------------------------------------------------------
# 3. Quadratures and vacuum fluctuations
# ----------------------------------------------------------------------------

def test_quadrature_commutator_interior():
    """[X, P] = i/2 on the interior, with X=(a+a+)/2, P=(a-a+)/2i."""
    N = 12
    xp = commutator(quadrature_x(N), quadrature_p(N))
    interior = xp[:N - 1, :N - 1]
    assert np.allclose(interior, 0.5j * np.eye(N - 1))
    assert abs(np.trace(xp)) < 1e-12


def test_vacuum_minimum_uncertainty():
    """Vacuum |0>: Var X = Var P = 1/4, so Delta X Delta P = 1/4 -- the Heisenberg
    floor and the irreducible zero-point fluctuation of the field."""
    N = 40
    vac = fock_state(0, N)
    vx, vp = quadrature_variance(vac)
    assert abs(vx - 0.25) < 1e-12 and abs(vp - 0.25) < 1e-12
    assert abs(math.sqrt(vx * vp) - 0.25) < 1e-12


def test_coherent_is_minimum_uncertainty_like_vacuum():
    """Every coherent state has the SAME vacuum-level noise Var X = Var P = 1/4
    (it is a displaced vacuum) -- equal-quadrature minimum uncertainty, the
    'most classical' field.  A Fock |n> instead has (2n+1)/4."""
    N = 60
    for alpha in (1.5, 2.0 + 1.0j):
        vx, vp = quadrature_variance(coherent_state(alpha, N))
        assert abs(vx - 0.25) < 1e-6 and abs(vp - 0.25) < 1e-6
    for n in (1, 3, 6):
        vx, vp = quadrature_variance(fock_state(n, N))
        assert abs(vx - (2 * n + 1) / 4) < 1e-9
        assert abs(vp - (2 * n + 1) / 4) < 1e-9


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
