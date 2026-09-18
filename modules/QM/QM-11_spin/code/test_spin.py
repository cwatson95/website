"""Tests for QM-11 spin & two-level systems.

The 2x2 algebra is EXACT in finite dimension, so the Pauli/spin identities are
checked to machine precision.  The eigenstate, precession, and Rabi claims are
checked against their closed forms; the dynamics is verified two independent ways
(matrix exponential `evolve` vs `solve_ivp` integration of the Schrodinger eq.).
One test cross-imports ~QM-10 (the j=1/2 angular-momentum rep) and ~MA-18 (su(2)
Pauli matrices) to confirm spin really is the half-integer rung of QM-10.

Run directly:   python3 test_spin.py        (-> "All N tests passed.")
Or with pytest: pytest test_spin.py
"""
import math
import os
import sys

import numpy as np

from spin import (
    HBAR, S_VALUE, I2, sigma_x, sigma_y, sigma_z, sigma, levi_civita,
    commutator, anticommutator, Sx, Sy, Sz, S, S_squared,
    n_hat, spin_operator_along, spin_eigenstate, up_z, down_z,
    expectation, prob_up_z, born_probabilities,
    hamiltonian_field, larmor_frequency, propagator, evolve,
    spin_expectations, schrodinger_solve,
    rabi_hamiltonian, rabi_frequency, rabi_probability, rotation,
)

_ANGLES = [(0.0, 0.0), (np.pi, 0.0), (np.pi / 2, 0.0), (np.pi / 2, np.pi / 2),
           (0.7, 1.1), (2.1, 4.3), (1.3, -0.6)]   # (theta, phi) test directions


def _herm(A):
    return np.allclose(A, A.conj().T, atol=1e-12)


# --- 1. Pauli matrices: the defining 2x2 algebra -----------------------------

def test_pauli_hermitian_traceless_unitary():
    """Each sigma_i is Hermitian, traceless, det = -1, and sigma_i^2 = I
    (Griffiths 3e Eq. 4.147-4.148, p.215)."""
    for s in sigma:
        assert _herm(s)
        assert abs(np.trace(s)) < 1e-12
        assert abs(np.linalg.det(s) + 1.0) < 1e-12
        assert np.allclose(s @ s, I2, atol=1e-12)


def test_pauli_product_identity():
    """The master identity  sigma_i sigma_j = delta_ij I + i eps_ijk sigma_k
    (all nine i,j), which packs sigma^2=I, the anticommutator, and the
    commutator into one statement."""
    for i in range(3):
        for j in range(3):
            lhs = sigma[i] @ sigma[j]
            rhs = (1.0 if i == j else 0.0) * I2
            for k in range(3):
                rhs = rhs + 1j * levi_civita(i, j, k) * sigma[k]
            assert np.allclose(lhs, rhs, atol=1e-12), (i, j)


def test_pauli_anticommutator():
    """{sigma_i, sigma_j} = 2 delta_ij I -- the Pauli matrices anticommute for
    i != j and square to I."""
    for i in range(3):
        for j in range(3):
            expected = 2.0 * (1.0 if i == j else 0.0) * I2
            assert np.allclose(anticommutator(sigma[i], sigma[j]), expected, atol=1e-12)


def test_pauli_commutator():
    """[sigma_i, sigma_j] = 2 i eps_ijk sigma_k (the su(2) structure constants)."""
    for i in range(3):
        for j in range(3):
            rhs = np.zeros((2, 2), dtype=complex)
            for k in range(3):
                rhs = rhs + 2j * levi_civita(i, j, k) * sigma[k]
            assert np.allclose(commutator(sigma[i], sigma[j]), rhs, atol=1e-12), (i, j)


# --- 2. spin-1/2 operators ---------------------------------------------------

def test_spin_algebra():
    """[S_i, S_j] = i hbar eps_ijk S_k (cyclic) -- the SAME angular-momentum
    algebra as ~QM-10, now in the 2-dimensional s=1/2 rep (Griffiths Eq. 4.134)."""
    assert np.allclose(commutator(Sx, Sy), 1j * HBAR * Sz, atol=1e-12)
    assert np.allclose(commutator(Sy, Sz), 1j * HBAR * Sx, atol=1e-12)
    assert np.allclose(commutator(Sz, Sx), 1j * HBAR * Sy, atol=1e-12)


def test_spin_operators_are_half_sigma_and_hermitian():
    """S_i = (hbar/2) sigma_i, Hermitian (observables); S_z eigenvalues +-hbar/2."""
    assert np.allclose(Sx, 0.5 * HBAR * sigma_x)
    assert np.allclose(Sy, 0.5 * HBAR * sigma_y)
    assert np.allclose(Sz, 0.5 * HBAR * sigma_z)
    for A in (Sx, Sy, Sz):
        assert _herm(A)
    assert np.allclose(np.sort(np.linalg.eigvalsh(Sz)), [-0.5 * HBAR, 0.5 * HBAR])


def test_S_squared_is_three_quarter():
    """S^2 = (3/4) hbar^2 I = hbar^2 s(s+1) I with s=1/2 (Griffiths Eq. 4.135)."""
    assert np.allclose(S_squared(), 0.75 * HBAR ** 2 * I2, atol=1e-12)
    assert math.isclose(S_VALUE * (S_VALUE + 1), 0.75)
    # the single eigenvalue is hbar^2 s(s+1):
    assert np.allclose(np.linalg.eigvalsh(S_squared()), HBAR ** 2 * 0.75)


# --- 3. eigenstates of n.S, and the Born probabilities -----------------------

def test_n_dot_S_eigenstate():
    """chi_+(theta,phi) is the +hbar/2 eigenstate of n.S, chi_- the -hbar/2 one;
    they are normalized and orthogonal (Griffiths 3e Prob. 4.33, p.218)."""
    for th, ph in _ANGLES:
        nS = spin_operator_along(th, ph)
        cp = spin_eigenstate(th, ph, +1)
        cm = spin_eigenstate(th, ph, -1)
        assert np.allclose(nS @ cp, +0.5 * HBAR * cp, atol=1e-12)
        assert np.allclose(nS @ cm, -0.5 * HBAR * cm, atol=1e-12)
        assert math.isclose(np.vdot(cp, cp).real, 1.0, abs_tol=1e-12)
        assert math.isclose(np.vdot(cm, cm).real, 1.0, abs_tol=1e-12)
        assert abs(np.vdot(cp, cm)) < 1e-12


def test_expectation_is_half_n():
    """On chi_+ the spin expectation points exactly along n-hat:
    <S> = (hbar/2) n-hat, and <n.S> = +hbar/2."""
    for th, ph in _ANGLES:
        chi = spin_eigenstate(th, ph, +1)
        svec = np.array([expectation(o, chi) for o in S])
        assert np.allclose(svec, 0.5 * HBAR * n_hat(th, ph), atol=1e-12)
        assert math.isclose(expectation(spin_operator_along(th, ph), chi),
                            0.5 * HBAR, abs_tol=1e-12)


def test_probability_cos_squared():
    """|<up_z|chi_+>|^2 = cos^2(theta/2) and |<down_z|chi_+>|^2 = sin^2(theta/2),
    independent of phi; they sum to 1 (Griffiths 3e p.215)."""
    for th, ph in _ANGLES:
        chi = spin_eigenstate(th, ph, +1)
        p_up = prob_up_z(chi)
        p_dn = abs(np.vdot(down_z, chi)) ** 2
        assert math.isclose(p_up, np.cos(th / 2) ** 2, abs_tol=1e-12)
        assert math.isclose(p_dn, np.sin(th / 2) ** 2, abs_tol=1e-12)
        assert math.isclose(p_up + p_dn, 1.0, abs_tol=1e-12)


def test_stern_gerlach_born_probabilities():
    """Measuring S_z (a Stern-Gerlach magnet) on chi_+(theta) gives outcomes
    +-hbar/2 with probabilities cos^2(theta/2), sin^2(theta/2): the 2s+1=2 beams
    (Griffiths 3e Example 4.4, p.221; generalized statistical interp. ~QM-06)."""
    th, ph = 1.0, 2.0
    probs = born_probabilities(Sz, spin_eigenstate(th, ph, +1))
    assert math.isclose(probs[round(0.5 * HBAR, 12)], np.cos(th / 2) ** 2, abs_tol=1e-12)
    assert math.isclose(probs[round(-0.5 * HBAR, 12)], np.sin(th / 2) ** 2, abs_tol=1e-12)
    assert math.isclose(sum(probs.values()), 1.0, abs_tol=1e-12)


# --- 4. Larmor precession ----------------------------------------------------

def test_larmor_precession_closed_form():
    """For H = -gamma B0 S_z and chi(0) tilted at angle alpha to z:
        <S_x> = (hbar/2) sin a cos(w t),  <S_y> = -(hbar/2) sin a sin(w t),
        <S_z> = (hbar/2) cos a  (constant),   w = gamma B0
    (Griffiths 3e Eq. 4.163-4.167, p.220)."""
    gamma, B0, alpha = 1.7, 2.3, 0.9
    w = larmor_frequency(gamma, B0)
    H = hamiltonian_field(gamma, [0, 0, B0])
    chi0 = spin_eigenstate(alpha, 0.0)
    for t in np.linspace(0, 3.0, 11):
        sx, sy, sz = spin_expectations(H, chi0, t)
        assert math.isclose(sx, 0.5 * HBAR * np.sin(alpha) * np.cos(w * t), abs_tol=1e-10)
        assert math.isclose(sy, -0.5 * HBAR * np.sin(alpha) * np.sin(w * t), abs_tol=1e-10)
        assert math.isclose(sz, 0.5 * HBAR * np.cos(alpha), abs_tol=1e-10)


def test_larmor_cone_and_period():
    """<S_z> is constant, the transverse spin traces a circle of radius
    (hbar/2) sin a, and everything is periodic with the Larmor period 2 pi / w."""
    gamma, B0, alpha = 1.0, 4.0, 1.2
    w = larmor_frequency(gamma, B0)
    H = hamiltonian_field(gamma, [0, 0, B0])
    chi0 = spin_eigenstate(alpha, 0.3)
    r2 = (0.5 * HBAR * np.sin(alpha)) ** 2
    sz0 = 0.5 * HBAR * np.cos(alpha)
    for t in np.linspace(0, 2.0, 9):
        sx, sy, sz = spin_expectations(H, chi0, t)
        assert math.isclose(sx ** 2 + sy ** 2, r2, abs_tol=1e-10)   # fixed cone
        assert math.isclose(sz, sz0, abs_tol=1e-10)                  # constant
    # one Larmor period returns <S> to its start
    T = 2 * np.pi / w
    assert np.allclose(spin_expectations(H, chi0, T),
                       spin_expectations(H, chi0, 0.0), atol=1e-9)


def test_evolution_is_unitary_and_matches_ode():
    """The matrix-exponential propagator conserves the norm, and agrees with an
    independent solve_ivp integration of i hbar d|chi>/dt = H|chi>."""
    gamma, B0, alpha = 1.3, 2.0, 1.0
    H = hamiltonian_field(gamma, [0.5, 0.0, B0])   # tilted field, generic dynamics
    chi0 = spin_eigenstate(alpha, 0.6)
    for t in (0.4, 1.1, 2.7):
        chi_exp = evolve(H, chi0, t)
        assert math.isclose(np.vdot(chi_exp, chi_exp).real, 1.0, abs_tol=1e-9)
        chi_ode = schrodinger_solve(H, chi0, t)
        assert np.allclose(chi_exp, chi_ode, atol=1e-6)


# --- 5. driven two-level (Rabi) ---------------------------------------------

def test_rabi_resonant_full_inversion():
    """On resonance (Delta=0): P(t) = sin^2(Omega t/2) -> reaches 1 (complete
    population inversion) at t = pi/Omega, and returns to 0 at t = 2 pi/Omega."""
    Omega = 1.4
    assert math.isclose(rabi_probability(0.0, Omega, 0.0), 0.0, abs_tol=1e-12)
    assert math.isclose(rabi_probability(np.pi / Omega, Omega, 0.0), 1.0, abs_tol=1e-12)
    assert math.isclose(rabi_probability(2 * np.pi / Omega, Omega, 0.0), 0.0, abs_tol=1e-12)
    for t in np.linspace(0, 5, 13):
        assert math.isclose(rabi_probability(t, Omega, 0.0),
                            np.sin(Omega * t / 2) ** 2, abs_tol=1e-12)


def test_rabi_detuned_amplitude():
    """Off resonance the flop never completes: the maximum transfer is
    Omega^2 / (Omega^2 + Delta^2) < 1, reached at Omega_R t = pi."""
    Omega, Delta = 1.0, 1.5
    OmR = rabi_frequency(Omega, Delta)
    pmax = Omega ** 2 / OmR ** 2
    assert math.isclose(rabi_probability(np.pi / OmR, Omega, Delta), pmax, abs_tol=1e-12)
    # never exceeds pmax over a dense scan
    ts = np.linspace(0, 20, 2001)
    assert max(rabi_probability(t, Omega, Delta) for t in ts) <= pmax + 1e-9


def test_rabi_matches_time_evolution():
    """The closed-form Rabi formula equals the true upper-level population from
    evolving |down> under the rotating-frame H = Delta S_z + Omega S_x."""
    for Omega, Delta in [(1.0, 0.0), (1.0, 0.8), (2.0, -1.3)]:
        H = rabi_hamiltonian(Omega, Delta)
        for t in np.linspace(0.0, 4.0, 9):
            chi = evolve(H, down_z, t)        # start in the lower (down) level
            p_up = abs(np.vdot(up_z, chi)) ** 2
            assert math.isclose(p_up, rabi_probability(t, Omega, Delta), abs_tol=1e-9)


# --- rotations: spin-1/2 double cover ----------------------------------------

def test_rotation_double_cover():
    """R_n(theta) = exp(-i theta n.sigma/2): a 2pi rotation gives -I (spinor sign
    flip), only 4pi gives +I -- the SU(2)->SO(3) double cover (~MA-18)."""
    for _, (th, ph) in enumerate(_ANGLES):
        n = n_hat(th, ph)
        assert np.allclose(rotation(2 * np.pi, n), -I2, atol=1e-10)
        assert np.allclose(rotation(4 * np.pi, n), I2, atol=1e-10)
    # a pi rotation about z swaps the relative phase of up/down by exp(-/+ i pi/2)
    assert np.allclose(rotation(np.pi, [0, 0, 1]) @ up_z, -1j * up_z, atol=1e-10)


# --- cross-check: spin == the j=1/2 rung of ~QM-10, sigma == ~MA-18 su(2) -----

def test_cross_check_QM10_angular_momentum_and_MA18():
    """Spin-1/2 is literally ~QM-10's l=1/2 angular-momentum representation, and
    the Pauli matrices are ~MA-18's su(2) generators.  Import both built modules
    and assert exact agreement (documents the cross-links concretely)."""
    here = os.path.dirname(os.path.abspath(__file__))
    qm10 = os.path.abspath(os.path.join(here, "..", "..",
                                        "QM-10_angular_momentum", "code"))
    ma18 = os.path.abspath(os.path.join(here, "..", "..", "..", "MA",
                                        "MA-18_group_theory", "code"))
    for p in (qm10, ma18):
        if p not in sys.path:
            sys.path.insert(0, p)

    import angular_momentum as am            # ~QM-10
    import groups as grp                      # ~MA-18

    # ~QM-10's l=1/2 matrices equal our spin operators S_i = (hbar/2) sigma_i.
    # (QM-10 uses HBAR=1; rescale by our HBAR to compare.)
    assert np.allclose(am.Lx(0.5) * HBAR / am.HBAR, Sx, atol=1e-12)
    assert np.allclose(am.Ly(0.5) * HBAR / am.HBAR, Sy, atol=1e-12)
    assert np.allclose(am.Lz(0.5) * HBAR / am.HBAR, Sz, atol=1e-12)
    # and QM-10's Casimir l(l+1) at l=1/2 is our 3/4:
    assert math.isclose(am.casimir_eigenvalue(0.5) / am.HBAR ** 2, 0.75)

    # ~MA-18's pauli() (plain nested lists) equals our Pauli arrays.
    sx18, sy18, sz18 = (np.array(m, dtype=complex) for m in grp.pauli())
    assert np.allclose(sx18, sigma_x) and np.allclose(sy18, sigma_y) \
        and np.allclose(sz18, sigma_z)
    # MA-18's su(2) relation [sx,sy] = 2 i sz matches ours:
    assert np.allclose(commutator(sx18, sy18), 2j * sz18, atol=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
