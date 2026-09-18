"""Tests for QM-12 hydrogen atom -- every claim checked against a closed form.

Run directly:   python3 test_hydrogen.py        (-> "All N tests passed.")
Or with pytest: pytest test_hydrogen.py

Two independent solutions of the Coulomb problem are cross-validated: the
finite-difference radial eigensolver must reproduce the analytic Bohr spectrum
E_n = -1/(2 n^2) AND the analytic radial functions r R_nl(r); the closed-form
R_nl are checked for normalization, the n-l-1 node count, and <r>.  The
associated Laguerre polynomial used for R_nl is checked, at order 0, against the
ordinary Laguerre polynomial that ~MA-12 builds from its recurrence.

Atomic units (hbar = m = e = 4 pi eps0 = 1) throughout, as in hydrogen.py.
"""
import math
import os
import sys

import numpy as np

from hydrogen import (
    HARTREE_EV,
    coulomb_energy, coulomb_energy_eV,
    allowed_l, m_values, degeneracy, count_states,
    effective_potential, radial_solve,
    generalized_laguerre, radial_wavefunction, radial_probability,
    radial_norm, count_radial_nodes, expectation_r, expectation_r_closed,
)

# ~MA-12 (ordinary Laguerre) by relative path -- the same pattern QM-10 uses to
# reach MA-12's assoc_legendre.  Used only to cross-check that scipy's generalized
# Laguerre at alpha=0 equals MA-12's recurrence-built L_n.
_HERE = os.path.dirname(os.path.abspath(__file__))
_MA12 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-12_special_functions", "code"))
if _MA12 not in sys.path:
    sys.path.insert(0, _MA12)
from special_functions import laguerre as ma12_laguerre  # noqa: E402


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


def _trapz(y, x):
    f = getattr(np, "trapezoid", None) or np.trapz
    return f(y, x)


# --- 1. the Coulomb spectrum -------------------------------------------------

def test_energy_levels():
    """E_n = -1/(2 n^2) Ha;  E_1 = -0.5 Ha = -13.606 eV (the ionization energy)."""
    assert _approx(coulomb_energy(1), -0.5, rel=1e-12)
    assert _approx(coulomb_energy(2), -0.125, rel=1e-12)
    assert _approx(coulomb_energy(3), -1.0 / 18.0, rel=1e-12)
    assert _approx(coulomb_energy_eV(1), -13.605693, abs_=1e-4)   # -13.6 eV
    # the levels scale as 1/n^2 and converge to 0 (the ionization threshold)
    for n in (2, 3, 4, 5):
        assert _approx(coulomb_energy(n), coulomb_energy(1) / n ** 2, rel=1e-12)
    assert coulomb_energy(100) < 0.0 and coulomb_energy(100) > -1e-3


# --- 2. quantum numbers and the n^2 degeneracy -------------------------------

def test_allowed_l_and_m():
    """l = 0..n-1 (so l < n), and each l has 2l+1 values m = -l..l."""
    for n in range(1, 7):
        ls = allowed_l(n)
        assert ls == list(range(n))           # l < n, exactly n of them
        assert max(ls) == n - 1
    for l in range(0, 5):
        ms = m_values(l)
        assert ms == list(range(-l, l + 1))
        assert len(ms) == 2 * l + 1


def test_degeneracy_is_n_squared():
    """sum_{l=0}^{n-1} (2l+1) = n^2 -- the explicit sum equals the closed form
    (Griffiths 3e p.191).  This is the n^2-fold degeneracy of each level."""
    for n in range(1, 9):
        assert count_states(n) == degeneracy(n) == n * n
        # built bottom-up from the (2l+1) m-multiplets:
        assert count_states(n) == sum(len(m_values(l)) for l in allowed_l(n))


# --- 3. the radial equation: finite difference vs the Bohr spectrum ----------

def test_effective_potential_centrifugal_barrier():
    """V_eff = -1/r + l(l+1)/2r^2: pure Coulomb for l=0; a positive centrifugal
    barrier for l>0 that dominates (V_eff>0) at small r (Griffiths 3e p.180)."""
    r = np.array([0.1, 0.5, 1.0, 2.0, 5.0])
    assert np.allclose(effective_potential(r, 0), -1.0 / r)        # l=0: Coulomb
    for l in (1, 2, 3):
        Veff = effective_potential(r, l)
        assert np.allclose(Veff, -1.0 / r + l * (l + 1) / (2.0 * r ** 2))
        assert effective_potential(0.01, l) > 0.0                  # barrier wins near 0
    # higher l raises the barrier at fixed small r
    assert effective_potential(0.1, 2) > effective_potential(0.1, 1) > effective_potential(0.1, 0)


def test_radial_solve_recovers_bohr_spectrum():
    """The finite-difference radial solver recovers E_n = -1/(2 n^2) to <0.5% for
    n = 1, 2, 3.  For orbital l the k-th state has n = l+1+k (Griffiths Eq.4.70)."""
    for l in (0, 1, 2):
        E, r, U = radial_solve(l, n_states=3)
        for k in range(3):
            n = l + 1 + k
            assert _approx(E[k], coulomb_energy(n), rel=5e-3), (l, n, E[k])
    # the ground state really is -0.5 Ha = -13.6 eV
    E0 = radial_solve(0, n_states=1)[0][0]
    assert _approx(E0 * HARTREE_EV, -13.6057, abs_=0.1)


def test_radial_solve_eigenfunction_matches_analytic():
    """The FD radial eigenfunction equals the analytic u_nl(r) = r R_nl(r)
    (up to sign): two independent constructions of the same state."""
    for (l, k) in [(0, 0), (0, 1), (0, 2), (1, 0), (1, 1), (2, 0)]:
        n = l + 1 + k
        E, r, U = radial_solve(l, n_states=k + 1)
        u_fd = U[k]
        u_an = r * radial_wavefunction(n, l, r)
        u_an = u_an / np.sqrt(_trapz(u_an ** 2, r))    # match normalization
        if np.dot(u_fd, u_an) < 0.0:                   # fix the global sign
            u_fd = -u_fd
        l2 = np.sqrt(_trapz((u_fd - u_an) ** 2, r))
        assert l2 < 5e-3, (n, l, l2)


# --- 4. the closed-form radial wave functions R_nl ---------------------------

def test_ground_state_is_two_exp():
    """R_10(r) = 2 e^{-r} exactly; R_20 = (1/(2 sqrt2))(2 - r) e^{-r/2}
    (Griffiths 3e Eq. 4.80 and Table 4.7)."""
    r = np.array([0.0, 0.3, 1.0, 2.0, 4.0])
    assert np.allclose(radial_wavefunction(1, 0, r), 2.0 * np.exp(-r))
    R20 = (1.0 / (2.0 * math.sqrt(2.0))) * (2.0 - r) * np.exp(-r / 2.0)
    assert np.allclose(radial_wavefunction(2, 0, r), R20)


def test_radial_normalization():
    """int_0^inf |R_nl|^2 r^2 dr = 1 for every orbital (Griffiths 3e Eq. 4.31):
    the closed-form normalization constant in R_nl is correct."""
    for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 1)]:
        assert _approx(radial_norm(n, l), 1.0, abs_=1e-4), (n, l)


def test_radial_node_count():
    """R_nl has exactly n - l - 1 radial nodes (Griffiths 3e p.195)."""
    for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2),
                   (4, 0), (4, 1), (4, 2), (4, 3), (5, 1)]:
        assert count_radial_nodes(n, l) == n - l - 1, (n, l)


def test_expectation_r_ground_state():
    """<r> for the ground state = 3/2 a0 (Griffiths 3e Problem 4.15a) -- larger
    than the Bohr radius a0=1, which is only the *most probable* radius."""
    assert _approx(expectation_r(1, 0), 1.5, abs_=2e-3)


def test_expectation_r_matches_closed_form():
    """<r>_nl = (1/2)(3 n^2 - l(l+1)) a0, by numeric integration vs closed form."""
    for (n, l) in [(1, 0), (2, 0), (2, 1), (3, 0), (3, 1), (3, 2), (4, 2)]:
        num = expectation_r(n, l)
        closed = expectation_r_closed(n, l)
        assert _approx(num, closed, rel=2e-3), (n, l, num, closed)
    assert expectation_r_closed(1, 0) == 1.5      # ground state exactly 3/2


def test_radial_probability_peaks_at_bohr_radius():
    """The radial density P(r) = r^2 |R_10|^2 peaks at r = a0 = 1: the Bohr radius
    is the MOST PROBABLE electron radius (Griffiths 3e Problem 4.16)."""
    r = np.linspace(1e-4, 6.0, 60001)
    P = radial_probability(1, 0, r)
    assert _approx(r[np.argmax(P)], 1.0, abs_=1e-3)


def test_radial_functions_orthogonal():
    """Radial functions of the same l but different n are orthogonal:
    int R_nl R_n'l r^2 dr = delta_nn' (Griffiths 3e Eq. 4.90)."""
    r = np.linspace(1e-6, 160.0, 400001)
    for l in (0, 1):
        for n1 in range(l + 1, l + 4):
            for n2 in range(l + 1, l + 4):
                overlap = _trapz(radial_wavefunction(n1, l, r)
                                 * radial_wavefunction(n2, l, r) * r * r, r)
                assert _approx(overlap, 1.0 if n1 == n2 else 0.0, abs_=2e-3), (l, n1, n2, overlap)


def test_generalized_laguerre_reduces_to_MA12():
    """The associated Laguerre L_k^{(alpha)} used for R_nl reduces, at alpha=0, to
    the ordinary Laguerre L_k that ~MA-12 builds from its recurrence -- tying this
    module's special function to MA-12 and verifying its API."""
    for k in range(6):
        for x in (0.0, 0.3, 1.5, 4.0, 9.0):
            assert _approx(generalized_laguerre(k, 0, x), ma12_laguerre(k, x), abs_=1e-9), (k, x)
    # and the hydrogen one (alpha = 2l+1) is a genuine polynomial of degree n-l-1:
    # L_0^{(alpha)} = 1 for any alpha (the n = l+1 states, no radial node)
    for alpha in (1, 3, 5):
        assert _approx(generalized_laguerre(0, alpha, 2.34), 1.0, rel=1e-12)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
