"""Tests for QM-15 approximations -- every claim checked against a closed form
or an exact diagonalization.

Run directly:   python3 test_approximations.py        (-> "All N tests passed.")
Or with pytest: pytest test_approximations.py

Three pillars, all cross-validated:
  * PERTURBATION THEORY -- the 1st/2nd-order formulae reproduce analytic results
    for the oscillator (H'=x, H'=x^2), and their truncation error scales as
    O(lambda^2) / O(lambda^3) versus exact diagonalization;
  * DEGENERATE PT -- the first-order splitting equals the eigenvalues of H' in
    the degenerate subspace, and the naive diagonal answer is shown to be wrong;
  * VARIATIONAL -- <H> >= E_gs (an upper bound), exact for the Gaussian-on-HO;
  * WKB -- Bohr-Sommerfeld is exact for the oscillator and asymptotically exact
    for the quartic and linear wells; the tunnelling probability shares the EXACT
    exponent of ~QM-08's rectangular barrier (imported here for the cross-check).
"""
import math
import os
import sys

import numpy as np
from scipy.special import ai_zeros

from approximations import (
    HBAR, MASS, OMEGA,
    ho_energies, ho_position, ho_matrix_power,
    first_order_energy, second_order_energy, first_order_correction,
    perturbed_energy, exact_energy, exact_spectrum,
    degenerate_first_order_split,
    gaussian_trial, variational_energy, gaussian_ho_energy,
    gaussian_variational_min, fd_ground_energy, fd_level,
    classical_momentum, action_integral, bohr_sommerfeld_energy,
    barrier_action, tunneling_probability, tunneling_rectangular,
)

# --- cross-link ~QM-08: import its EXACT rectangular-barrier transmission to
# validate the WKB tunnelling exponent.  Relative-path import (same pattern
# QM-09 uses for MA-12).  QM-08 also uses hbar = m = 1, so the comparison is
# apples-to-apples.  Read QM-08/code/one_dim.py for the API: transmission_barrier(E, V0, a).
_HERE = os.path.dirname(os.path.abspath(__file__))
_QM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "QM-08_1d_problems", "code"))
if _QM08 not in sys.path:
    sys.path.insert(0, _QM08)
from one_dim import transmission_barrier  # noqa: E402


# ----------------------------------------------------------------------------
# 1. NONDEGENERATE PERTURBATION THEORY  (oscillator test bed)
# ----------------------------------------------------------------------------

def test_first_order_energy_is_expectation_value():
    """E_n^(1) = <n|H'|n> (Griffiths Eq. 7.9).  For H'=x^2 it equals <n|x^2|n>
    = n+1/2; for the linear (Stark) perturbation H'=x it is 0 by parity."""
    D = 40
    E0 = ho_energies(D)
    X2 = ho_matrix_power(D, 2)
    for n in range(6):
        assert abs(first_order_energy(E0, X2, n) - (n + 0.5)) < 1e-10, n
    X = ho_position(D)
    for n in range(6):
        assert abs(first_order_energy(E0, X, n)) < 1e-12, n


def test_second_order_energy_formula():
    """E_n^(2) = sum_{m!=n} |<m|H'|n>|^2/(E_n-E_m) (Griffiths Eq. 7.15).
    Analytic: for H'=x^2 it is -(n+1/2)/2; for H'=x it is -1/2 for every n."""
    D = 60
    E0 = ho_energies(D)
    X2 = ho_matrix_power(D, 2)
    for n in range(6):
        assert abs(second_order_energy(E0, X2, n) - (-0.5 * (n + 0.5))) < 1e-9, n
    X = ho_position(D)
    for n in range(6):
        assert abs(second_order_energy(E0, X, n) - (-0.5)) < 1e-9, n


def test_second_order_energy_pushes_ground_state_down():
    """For the ground state every denominator E_0 - E_m < 0, so E_0^(2) <= 0:
    second-order PT always LOWERS the ground state (level repulsion)."""
    D = 40
    E0 = ho_energies(D)
    rng = np.random.default_rng(1)
    M = rng.standard_normal((D, D))
    Hp = (M + M.T) / 2.0                      # an arbitrary hermitian perturbation
    assert second_order_energy(E0, Hp, 0) <= 1e-12


def test_first_order_state_correction():
    """psi_n^(1) = sum_{m!=n} <m|H'|n>/(E_n-E_m)|m> (Griffiths Eq. 7.13).  For
    H'=x only m=n+-1 contribute: c_{n-1}=+sqrt(n/2), c_{n+1}=-sqrt((n+1)/2)
    (denominators +1 and -1), and the |n> component is 0."""
    D = 30
    E0 = ho_energies(D)
    X = ho_position(D)
    n = 4
    c = first_order_correction(E0, X, n)
    assert abs(c[n]) < 1e-15                                  # |n> dropped
    assert abs(c[n - 1] - math.sqrt(n / 2.0)) < 1e-12
    assert abs(c[n + 1] - (-math.sqrt((n + 1) / 2.0))) < 1e-12
    others = [m for m in range(D) if m not in (n - 1, n, n + 1)]
    assert np.allclose(c[others], 0.0)


def test_first_order_error_is_order_lambda_squared():
    """E_n^0 + lambda E_n^(1) approximates the exact eigenvalue with error
    O(lambda^2): halving lambda divides the error by ~4."""
    D = 50
    E0 = ho_energies(D)
    X2 = ho_matrix_power(D, 2)
    n = 1
    errs = []
    for lam in (0.04, 0.02, 0.01):
        ex = exact_energy(E0, X2, n, lam)
        errs.append(abs(perturbed_energy(E0, X2, n, lam, order=1) - ex))
    assert abs(errs[0] / errs[1] - 4.0) < 0.3
    assert abs(errs[1] / errs[2] - 4.0) < 0.3


def test_through_second_order_error_is_order_lambda_cubed():
    """E_n^0 + lambda E_n^(1) + lambda^2 E_n^(2) approximates the exact eigenvalue
    with error O(lambda^3): halving lambda divides the error by ~8.  (And the
    2nd-order estimate is much closer than the 1st-order one.)"""
    D = 50
    E0 = ho_energies(D)
    X2 = ho_matrix_power(D, 2)
    n = 1
    errs2, errs1 = [], []
    for lam in (0.04, 0.02, 0.01):
        ex = exact_energy(E0, X2, n, lam)
        errs2.append(abs(perturbed_energy(E0, X2, n, lam, order=2) - ex))
        errs1.append(abs(perturbed_energy(E0, X2, n, lam, order=1) - ex))
    assert abs(errs2[0] / errs2[1] - 8.0) < 0.8
    assert abs(errs2[1] / errs2[2] - 8.0) < 0.8
    assert errs2[0] < errs1[0]                               # 2nd order is better


def test_stark_perturbation_exact_through_second_order():
    """H' = x shifts H = p^2/2 + x^2/2 + lambda x to E_n = (n+1/2) - lambda^2/2
    (complete the square; all higher corrections vanish).  Through-second-order
    PT therefore reproduces the exact spectrum to machine precision."""
    D = 60
    E0 = ho_energies(D)
    X = ho_position(D)
    lam = 0.3
    for n in range(5):
        pt = perturbed_energy(E0, X, n, lam, order=2)
        assert abs(pt - ((n + 0.5) - 0.5 * lam ** 2)) < 1e-9, n
        # and PT matches exact diagonalization
        assert abs(pt - exact_energy(E0, X, n, lam)) < 1e-7, n


# ----------------------------------------------------------------------------
# 1b. DEGENERATE PERTURBATION THEORY
# ----------------------------------------------------------------------------

def test_degenerate_split_equals_subspace_eigenvalues():
    """The first-order splitting of a degenerate level equals the eigenvalues of
    H' restricted to the degenerate subspace (Griffiths Eq. 7.30/7.33).  Verify
    against the exact split (E_exact - E_deg)/lambda as lambda -> 0."""
    E0 = np.array([2.0, 2.0, 5.0, 9.0])       # states 0,1 degenerate at E=2
    Hp = np.array([[0.30, 0.40, 0.10, 0.00],
                   [0.40, -0.20, 0.00, 0.20],
                   [0.10, 0.00, 1.00, 0.00],
                   [0.00, 0.20, 0.00, 2.00]])
    split = degenerate_first_order_split(Hp, [0, 1])
    lam = 1e-6
    ex = np.sort((exact_spectrum(E0, Hp, lam)[:2] - 2.0) / lam)
    assert np.allclose(split, ex, atol=1e-4), (split, ex)


def test_naive_nondegenerate_answer_is_wrong():
    """When the degenerate block of H' has off-diagonal elements, the naive
    diagonal first-order energies {H'_00, H'_11} do NOT give the true splitting --
    you must diagonalize the block.  This is *why* degenerate PT exists."""
    Hp = np.array([[0.30, 0.40, 0.10, 0.00],
                   [0.40, -0.20, 0.00, 0.20],
                   [0.10, 0.00, 1.00, 0.00],
                   [0.00, 0.20, 0.00, 2.00]])
    naive = np.sort([Hp[0, 0], Hp[1, 1]])
    good = degenerate_first_order_split(Hp, [0, 1])
    assert not np.allclose(naive, good)       # the off-diagonal 0.40 matters
    # and the eigenvalues bracket the diagonal entries (eigenvalue interlacing)
    assert good[0] < naive[0] and good[1] > naive[1]


def test_degenerate_diagonal_block_needs_no_rotation():
    """Consistency: if H' is already diagonal in the degenerate subspace, the
    'good' states are the originals and the splitting is just the diagonal."""
    Hp = np.array([[0.7, 0.0, 0.3],
                   [0.0, -0.4, 0.1],
                   [0.3, 0.1, 5.0]])
    split = degenerate_first_order_split(Hp, [0, 1])
    assert np.allclose(split, np.sort([0.7, -0.4]))


# ----------------------------------------------------------------------------
# 2. THE VARIATIONAL PRINCIPLE
# ----------------------------------------------------------------------------

def test_variational_gaussian_recovers_oscillator_exactly():
    """The Gaussian trial family CONTAINS the true oscillator ground state, so
    minimizing <H> hits E_0 = 1/2 hbar omega exactly, at b = 1/2 (Griffiths
    Example 8.1).  Checked both via the closed form and on a grid."""
    # closed form b/2 + 1/(8b), minimized at b=1/2 -> 1/2
    from scipy.optimize import minimize_scalar
    r = minimize_scalar(gaussian_ho_energy, bracket=(0.1, 0.5, 2.0))
    assert abs(r.x - 0.5) < 1e-6 and abs(r.fun - 0.5) < 1e-9
    # grid-based Rayleigh quotient agrees
    x = np.linspace(-12, 12, 6001)
    Emin, b_opt = gaussian_variational_min(lambda t: 0.5 * t ** 2, x)
    assert abs(Emin - 0.5) < 1e-4 and abs(b_opt - 0.5) < 1e-3


def test_variational_numeric_matches_closed_form():
    """The grid Rayleigh quotient variational_energy() equals the analytic
    gaussian_ho_energy(b) for the oscillator, across several widths."""
    x = np.linspace(-14, 14, 7001)
    V = 0.5 * x ** 2
    for b in (0.2, 0.5, 1.0, 2.0):
        num = variational_energy(gaussian_trial(b, x), x, V)
        assert abs(num - gaussian_ho_energy(b)) < 2e-4, b


def test_variational_is_an_upper_bound():
    """<H> >= E_gs for EVERY trial width, not merely at the optimum (Griffiths
    Eq. 8.1).  Check the inequality holds for the quartic well at a range of b,
    with E_gs from exact diagonalization."""
    x = np.linspace(-10, 10, 5001)
    V = lambda t: 0.25 * t ** 4
    Egs = fd_ground_energy(V, np.linspace(-8, 8, 3000))
    Varr = V(x)
    for b in (0.1, 0.3, 0.6, 1.0, 2.0, 4.0):
        assert variational_energy(gaussian_trial(b, x), x, Varr) >= Egs - 1e-6, b


def test_variational_quartic_bound_is_tight_but_above():
    """For the quartic V=x^4/4 the Gaussian is NOT exact (it isn't the true
    ground state), so the minimized bound sits a few % ABOVE E_gs -- a genuine,
    non-trivial upper bound."""
    x = np.linspace(-10, 10, 6001)
    Emin, _ = gaussian_variational_min(lambda t: 0.25 * t ** 4, x)
    Egs = fd_ground_energy(lambda t: 0.25 * t ** 4, np.linspace(-8, 8, 3000))
    assert Emin >= Egs                                   # above the truth
    assert (Emin - Egs) / Egs < 0.05                    # but within 5%
    assert (Emin - Egs) / Egs > 1e-4                    # and strictly above


# ----------------------------------------------------------------------------
# 3. THE WKB APPROXIMATION
# ----------------------------------------------------------------------------

def test_classical_momentum_zero_in_forbidden_region():
    """p(x) = sqrt(2m(E-V)) is real where E>V and clamped to 0 where E<V."""
    V = np.array([-1.0, 0.0, 2.0, 5.0])
    p = classical_momentum(2.0, V)
    assert p[0] > p[1] > p[2] == 0.0 and p[3] == 0.0
    assert abs(p[1] - math.sqrt(2.0 * MASS * 2.0)) < 1e-12


def test_wkb_recovers_oscillator_exactly():
    """Bohr-Sommerfeld with two smooth turning points (n+1/2)pi*hbar gives the
    oscillator spectrum E_n = (n+1/2) hbar omega EXACTLY (Griffiths: WKB is exact
    for the harmonic oscillator).  Action integral for the HO is pi*E, so
    pi*E = (n+1/2)pi -> E = n+1/2."""
    for n in range(6):
        E = bohr_sommerfeld_energy(lambda t: 0.5 * t ** 2, n, -80.0, 80.0)
        assert abs(E - (n + 0.5)) < 1e-6, (n, E)


def test_wkb_action_integral_closed_form():
    """The HO action integral has the closed form  integral p dx = pi E / omega
    (the area of a momentum-space ellipse).  Check directly."""
    for E in (1.0, 3.5, 10.0):
        I = action_integral(lambda t: 0.5 * t ** 2, E, -80.0, 80.0)
        assert abs(I - math.pi * E / OMEGA) < 1e-6, E


def test_wkb_quartic_improves_with_quantum_number():
    """For the quartic well V=x^4/4 WKB is APPROXIMATE; the relative error
    decreases with n (the semiclassical limit), and is already < 1% by n=2."""
    Vq = lambda t: 0.25 * t ** 4
    xfd = np.linspace(-9, 9, 3000)
    rel = []
    for n in range(5):
        E = bohr_sommerfeld_energy(Vq, n, -40.0, 40.0)
        Ef = fd_level(Vq, xfd, n)
        rel.append(abs(E - Ef) / Ef)
    assert rel[0] > rel[1] > rel[2]                      # monotone improvement
    assert rel[2] < 0.01 and rel[4] < 0.005             # excellent at high n


def test_wkb_linear_well_matches_airy():
    """One-vertical-wall WKB (gamma=3/4) for the linear "gravity" well V=Fx
    (x>0, infinite wall at x=0) vs the EXACT energies set by the zeros of the
    Airy function:  E_n = -a_n (hbar^2 F^2/2m)^{1/3}.  Agreement improves with n
    (Griffiths Example 9.3 / Problem 9.7)."""
    F = 1.0
    a_zeros = ai_zeros(5)[0]                              # negative zeros of Ai
    Vlin = lambda t: F * t
    rel = []
    for n in range(4):
        E_wkb = bohr_sommerfeld_energy(Vlin, n, 0.0, 60.0, gamma=0.75)
        E_exact = -a_zeros[n] * (HBAR ** 2 * F ** 2 / (2.0 * MASS)) ** (1.0 / 3.0)
        rel.append(abs(E_wkb - E_exact) / E_exact)
    assert rel[0] < 0.01                                  # <1% even for the ground state
    assert rel[0] > rel[1] > rel[2] > rel[3]             # and improving with n


def test_wkb_tunneling_shares_exact_exponent():
    """WKB tunnelling T_WKB = exp(-2 kappa a) for a rectangular barrier carries
    the SAME exponential as ~QM-08's EXACT transmission_barrier; they differ only
    by an O(1) prefactor.  For a thick barrier the ratio T_exact/T_WKB tends to
    the constant 16 E (V0-E)/V0^2 (independent of a) -- proof of a shared
    exponent."""
    V0, E = 10.0, 2.0
    pref = 16.0 * E * (V0 - E) / V0 ** 2                  # predicted thick-barrier ratio
    ratios = []
    for a in (3.0, 5.0, 8.0):
        T_wkb = tunneling_rectangular(E, V0, a)
        T_ex = transmission_barrier(E, V0, a)             # exact, from ~QM-08
        ratios.append(T_ex / T_wkb)
        assert abs(T_ex / T_wkb - pref) < 1e-3, a         # ratio = prefactor
    # ratio is independent of a (same exponent), to high precision
    assert max(ratios) - min(ratios) < 1e-6


def test_wkb_tunneling_general_matches_rectangular():
    """The general grid-based tunneling_probability() on a rectangular barrier
    reproduces the closed-form tunneling_rectangular(), and T falls off
    exponentially with both width and barrier height."""
    V0, E, a = 8.0, 3.0, 2.0
    Vbar = lambda t: V0 if 0.0 <= t <= a else 0.0
    T_grid = tunneling_probability(Vbar, E, -1.0, a + 1.0)
    assert abs(T_grid - tunneling_rectangular(E, V0, a)) < 1e-9
    # monotone suppression
    assert (tunneling_rectangular(E, V0, 1.0)
            > tunneling_rectangular(E, V0, 2.0)
            > tunneling_rectangular(E, V0, 3.0))
    assert (tunneling_rectangular(E, 6.0, a)
            > tunneling_rectangular(E, 8.0, a)
            > tunneling_rectangular(E, 12.0, a))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
