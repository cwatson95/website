"""Tests for QM-10 angular momentum.

The matrix claims are EXACT in finite dimension, so they are checked to machine
precision (a clean contrast to ~QM-05's x, p, which only close on a truncated
basis).  The spherical-harmonic claims are checked by numerical integration over
the sphere and against the closed forms in Griffiths 3e Table 4.3 (p.178).

Run directly:   python3 test_angular_momentum.py     (-> "All N tests passed.")
Or with pytest: pytest test_angular_momentum.py
"""
import math

import numpy as np

from angular_momentum import (
    HBAR, dim, m_values, ladder_coeff, casimir_eigenvalue,
    Lz, L_plus, L_minus, Lx, Ly, L_squared, commutator,
    spherical_harmonic, sphere_inner_product, Lz_on_Y,
)

_LS = [0.5, 1.0, 1.5, 2.0]                 # the reps to exercise (dispatch list)
_MODES = [(0, 0), (1, -1), (1, 0), (1, 1),
          (2, 0), (2, 1), (2, 2), (3, -2), (3, 3)]   # integer-l spherical harmonics


def _herm(A):
    return np.allclose(A, A.conj().T, atol=1e-12)


# --- matrix representation: the algebra is exact -----------------------------

def test_dimension_and_m_values():
    """dim = 2l+1 and the L_z labels run m = l, l-1, ..., -l."""
    for l in _LS:
        m = m_values(l)
        assert len(m) == dim(l) == round(2 * l + 1)
        assert math.isclose(m[0], l) and math.isclose(m[-1], -l)
        assert np.allclose(np.diff(m), -1.0)            # unit steps


def test_Lz_is_diagonal_spectrum():
    """L_z = hbar*diag(m); its spectrum is exactly {-l,...,+l} (Griffiths Eq.4.119)."""
    for l in _LS:
        z = Lz(l)
        assert np.allclose(z, np.diag(np.diag(z)))      # diagonal
        spec = np.sort(np.linalg.eigvalsh(z).real)
        assert np.allclose(spec, HBAR * np.sort(m_values(l)))


def test_commutators_cyclic():
    """[L_x,L_y]=i hbar L_z and the two cyclic partners -- EXACT (Griffiths Eq.4.99)."""
    for l in _LS:
        X, Y, Z = Lx(l), Ly(l), Lz(l)
        assert np.allclose(commutator(X, Y), 1j * HBAR * Z, atol=1e-12)
        assert np.allclose(commutator(Y, Z), 1j * HBAR * X, atol=1e-12)
        assert np.allclose(commutator(Z, X), 1j * HBAR * Y, atol=1e-12)


def test_casimir_is_l_l_plus_one():
    """L^2 = L_x^2+L_y^2+L_z^2 = hbar^2 l(l+1) * I, exactly (Griffiths Eq.4.118)."""
    for l in _LS:
        L2 = L_squared(l)
        assert np.allclose(L2, casimir_eigenvalue(l) * np.eye(dim(l)), atol=1e-12)
        # so the only eigenvalue of L^2 is hbar^2 l(l+1):
        ev = np.linalg.eigvalsh(L2).real
        assert np.allclose(ev, HBAR ** 2 * l * (l + 1))


def test_ladder_decomposition():
    """L_+ = L_x + i L_y, L_- = L_x - i L_y, and L_+ = (L_-)^dagger."""
    for l in _LS:
        assert np.allclose(L_plus(l), Lx(l) + 1j * Ly(l), atol=1e-12)
        assert np.allclose(L_minus(l), Lx(l) - 1j * Ly(l), atol=1e-12)
        assert np.allclose(L_plus(l), L_minus(l).conj().T, atol=1e-12)


def test_L2_commutes_with_each_component():
    """[L^2, L_i] = 0 for every component -- so L^2 and one L_i share eigenstates
    (Griffiths Eq.4.102-4.103, p.202)."""
    for l in _LS:
        L2 = L_squared(l)
        for A in (Lx(l), Ly(l), Lz(l)):
            assert np.allclose(commutator(L2, A), 0.0, atol=1e-12)


def test_hermiticity():
    """L_x, L_y, L_z, L^2 are Hermitian (observables); L_+, L_- are not."""
    for l in _LS:
        for A in (Lx(l), Ly(l), Lz(l), L_squared(l)):
            assert _herm(A)
        assert not _herm(L_plus(l))


def test_ladder_matrix_elements():
    """L_+ raises m by one with element hbar*sqrt(l(l+1)-m(m+1)); it annihilates
    the top rung and L_- the bottom rung (Griffiths Problem 4.21, p.206)."""
    for l in _LS:
        m = m_values(l)
        Lp, Lm = L_plus(l), L_minus(l)
        # acting on each basis ket |l, m[j]> (column j)
        for j, mm in enumerate(m):
            up = Lp[:, j]
            if j - 1 >= 0:                              # has a rung above
                assert math.isclose(up[j - 1].real, ladder_coeff(l, mm, +1))
                assert np.allclose(np.delete(up, j - 1), 0.0)
            else:                                       # top rung: annihilated
                assert np.allclose(up, 0.0)
        assert np.allclose(Lp[:, 0], 0.0)              # L_+ |l, l> = 0
        assert np.allclose(Lm[:, -1], 0.0)            # L_- |l,-l> = 0


def test_spin_half_is_pauli():
    """For l=1/2, 2*L_x, 2*L_y, 2*L_z are exactly the Pauli matrices -- the bridge
    to ~QM-11 (spin), the simplest half-integer rep (no spatial Y_l^m)."""
    sx = np.array([[0, 1], [1, 0]], dtype=complex)
    sy = np.array([[0, -1j], [1j, 0]], dtype=complex)
    sz = np.array([[1, 0], [0, -1]], dtype=complex)
    assert np.allclose(2 * Lx(0.5) / HBAR, sx)
    assert np.allclose(2 * Ly(0.5) / HBAR, sy)
    assert np.allclose(2 * Lz(0.5) / HBAR, sz)


# --- position space: spherical harmonics -------------------------------------

def test_spherical_harmonics_orthonormal():
    """<Y_l^m | Y_l'^m'> = delta_ll' delta_mm' over the sphere (Griffiths Eq.4.33).
    Checked by Gauss-Legendre x quadrature + uniform phi sum, for many modes."""
    for (l1, m1) in _MODES:
        for (l2, m2) in _MODES:
            ip = sphere_inner_product(l1, m1, l2, m2)
            expected = 1.0 if (l1, m1) == (l2, m2) else 0.0
            assert abs(ip - expected) < 1e-9, ((l1, m1), (l2, m2), ip)


def test_spherical_harmonics_closed_forms():
    """Match the closed forms of Griffiths 3e Table 4.3 (p.178) at a generic point."""
    th, ph = 0.7, 1.1
    s, c = math.sin(th), math.cos(th)
    e1, e2 = np.exp(1j * ph), np.exp(2j * ph)
    cases = {
        (0, 0): math.sqrt(1 / (4 * math.pi)),
        (1, 0): math.sqrt(3 / (4 * math.pi)) * c,
        (1, 1): -math.sqrt(3 / (8 * math.pi)) * s * e1,
        (1, -1): math.sqrt(3 / (8 * math.pi)) * s / e1,
        (2, 0): math.sqrt(5 / (16 * math.pi)) * (3 * c * c - 1),
        (2, 1): -math.sqrt(15 / (8 * math.pi)) * s * c * e1,
        (2, 2): math.sqrt(15 / (32 * math.pi)) * s * s * e2,
        (2, -2): math.sqrt(15 / (32 * math.pi)) * s * s / e2,
    }
    for (l, m), ref in cases.items():
        got = complex(spherical_harmonic(l, m, th, ph))
        assert abs(got - ref) < 1e-12, ((l, m), got, ref)


def test_spherical_harmonics_match_scipy():
    """Independent cross-check against scipy's spherical harmonics (same Condon-
    Shortley convention).  Uses the modern sph_harm_y(l,m,theta,phi) when present,
    else the legacy sph_harm(m,l,phi,theta)."""
    import scipy.special as sp
    if hasattr(sp, "sph_harm_y"):
        ref = lambda l, m, th, ph: sp.sph_harm_y(l, m, th, ph)
    else:                                              # older scipy: swapped args
        ref = lambda l, m, th, ph: sp.sph_harm(m, l, ph, th)
    th, ph = 0.9, 2.3
    for (l, m) in _MODES:
        got = complex(spherical_harmonic(l, m, th, ph))
        assert abs(got - complex(ref(l, m, th, ph))) < 1e-12, ((l, m), got)


def test_spherical_harmonics_are_Lz_eigenfunctions():
    """L_z = -i hbar d/dphi gives Y_l^m the eigenvalue hbar*m (Griffiths Eq.4.129,
    p.208).  Checked numerically at several points."""
    for (l, m) in _MODES:
        for (th, ph) in [(0.6, 0.9), (1.3, 4.0), (2.0, 5.5)]:
            lhs = Lz_on_Y(l, m, th, ph)
            rhs = HBAR * m * spherical_harmonic(l, m, th, ph)
            assert abs(complex(lhs) - complex(rhs)) < 1e-6, ((l, m), th, ph)


def test_spherical_harmonics_parity():
    """Under inversion r -> -r, i.e. (theta,phi) -> (pi-theta, phi+pi):
    Y_l^m -> (-1)^l Y_l^m.  A closed-form property tied to l (eigenvalue of P)."""
    th, ph = 0.7, 1.1
    for (l, m) in _MODES:
        direct = complex(spherical_harmonic(l, m, th, ph))
        inverted = complex(spherical_harmonic(l, m, math.pi - th, ph + math.pi))
        assert abs(inverted - (-1) ** l * direct) < 1e-12, ((l, m), inverted)


def test_spherical_harmonics_require_integer_l():
    """No Y_l^m for half-integer l: e^{im phi} must be single valued -> l integer
    (Griffiths Eq.4.22, p.176).  Half-integer l is spin (~QM-11), matrices only."""
    for l in (0.5, 1.5):
        raised = False
        try:
            spherical_harmonic(l, 0.5, 0.5, 0.5)
        except ValueError:
            raised = True
        assert raised, l


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
