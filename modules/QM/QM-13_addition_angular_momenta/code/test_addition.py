"""Tests for QM-13 addition of angular momenta.

The operator claims are EXACT in finite dimension and checked to machine
precision; the Clebsch-Gordan coefficients are checked three ways: against the
explicit 1/2(x)1/2 (singlet + triplet) and 1(x)1/2 tables of Griffiths 3e
(Table 4.8, p.226), against orthonormality (the transform must be unitary), and
against an INDEPENDENT library (sympy's Clebsch-Gordan), so the construction is
not graded against itself.

Run directly:   python3 test_addition.py        (-> "All N tests passed.")
Or with pytest: pytest test_addition.py
"""
import math

import numpy as np

from addition import (
    HBAR, dim, commutator,
    multiplet_content, decomposition, dimension_check,
    uncoupled_labels, coupled_labels,
    total_operators, Jz_total, Jminus_total, J_squared,
    J1_squared, J2_squared,
    coupled_basis, cg_coefficient, cg_table,
)

# (j1, j2) pairs exercised across the suite: equal spins, mixed, integer+half.
_PAIRS = [(0.5, 0.5), (1.0, 0.5), (1.0, 1.0), (1.5, 1.0), (2.0, 1.5)]


def _herm(A):
    return np.allclose(A, A.conj().T, atol=1e-12)


# --- multiplet content & dimension -------------------------------------------

def test_multiplet_content_series():
    """j1 (x) j2 yields J = j1+j2 down to |j1-j2| in unit steps, once each
    (Griffiths 3e p.225)."""
    assert multiplet_content(0.5, 0.5) == [1.0, 0.0]
    assert multiplet_content(1.0, 0.5) == [1.5, 0.5]
    assert multiplet_content(2.0, 1.5) == [3.5, 2.5, 1.5, 0.5]
    # Griffiths' own example: spin 3/2 with spin 2 -> 7/2,5/2,3/2,1/2 (p.225)
    assert multiplet_content(1.5, 2.0) == [3.5, 2.5, 1.5, 0.5]
    for (j1, j2) in _PAIRS:
        Js = multiplet_content(j1, j2)
        assert math.isclose(Js[0], j1 + j2)
        assert math.isclose(Js[-1], abs(j1 - j2))
        assert np.allclose(np.diff(Js), -1.0)             # unit steps


def test_dimension_sum_rule():
    """(2j1+1)(2j2+1) = sum_J (2J+1): coupling preserves the dimension."""
    for (j1, j2) in _PAIRS:
        prod, tot = dimension_check(j1, j2)
        assert prod == tot == dim(j1) * dim(j2)
        assert len(coupled_labels(j1, j2)) == len(uncoupled_labels(j1, j2)) == prod


# --- the total operators ------------------------------------------------------

def test_Jz_adds_and_is_diagonal():
    """J_z = J1z + J2z is diagonal with entries M = m1 + m2 (Griffiths p.223:
    'the z-components add')."""
    for (j1, j2) in _PAIRS:
        Jz = Jz_total(j1, j2)
        assert np.allclose(Jz, np.diag(np.diag(Jz)))      # diagonal
        diag = np.diag(Jz).real
        expect = np.array([m1 + m2 for (m1, m2) in uncoupled_labels(j1, j2)])
        assert np.allclose(diag, HBAR * expect)


def test_total_operators_hermitian_and_commuting():
    """J^2 is Hermitian and {J^2, J_z, J1^2, J2^2} is a COMPLETE SET OF COMMUTING
    OBSERVABLES -- so a simultaneous eigenbasis (the coupled basis) exists."""
    for (j1, j2) in _PAIRS:
        ops = total_operators(j1, j2)
        J2, Jz = ops["J^2"], ops["Jz"]
        J1s, J2s = ops["J1^2"], ops["J2^2"]
        for A in (J2, Jz, ops["Jx"], ops["Jy"], J1s, J2s):
            assert _herm(A)
        for A in (Jz, J1s, J2s):
            assert np.allclose(commutator(J2, A), 0.0, atol=1e-12)
        assert np.allclose(commutator(J1s, J2s), 0.0, atol=1e-12)
        assert np.allclose(commutator(Jz, J1s), 0.0, atol=1e-12)


def test_J_squared_two_equivalent_forms():
    """J^2 = Jx^2+Jy^2+Jz^2 must equal J1^2 + J2^2 + 2 J1.J2, where
    J1.J2 = J1z J2z + (1/2)(J1+ J2- + J1- J2+).  (Griffiths Eqs. 4.178-4.179 are
    the spin-1/2 instance of this identity, p.224.)"""
    for (j1, j2) in _PAIRS:
        ops = total_operators(j1, j2)
        from addition import embed_1, embed_2
        from angular_momentum import (Lz, L_plus, L_minus, L_squared)
        J1z, J2z = embed_1(Lz(j1), j2), embed_2(Lz(j2), j1)
        J1p, J2p = embed_1(L_plus(j1), j2), embed_2(L_plus(j2), j1)
        J1m, J2m = embed_1(L_minus(j1), j2), embed_2(L_minus(j2), j1)
        J1s, J2s = embed_1(L_squared(j1), j2), embed_2(L_squared(j2), j1)
        J1dotJ2 = J1z @ J2z + 0.5 * (J1p @ J2m + J1m @ J2p)
        alt = J1s + J2s + 2.0 * J1dotJ2
        assert np.allclose(ops["J^2"], alt, atol=1e-12)


def test_J2_eigenvalues_and_multiplicities():
    """Diagonalizing J^2 gives eigenvalues hbar^2 J(J+1), each with multiplicity
    (2J+1) -- the multiplet content read straight off the spectrum
    (Griffiths 3e p.224-225)."""
    for (j1, j2) in _PAIRS:
        ev = np.linalg.eigvalsh(J_squared(j1, j2)).real
        # bucket eigenvalues by value, count multiplicities
        counts = {}
        for e in ev:
            key = round(e, 6)
            counts[key] = counts.get(key, 0) + 1
        expected = {round(HBAR ** 2 * J * (J + 1), 6): dim(J)
                    for J in multiplet_content(j1, j2)}
        assert counts == expected, (j1, j2, counts, expected)


# --- Clebsch-Gordan: the change of basis -------------------------------------

def test_coupled_basis_is_unitary():
    """The coupled<->uncoupled transform U is unitary: U^dag U = I.  This is the
    Clebsch-Gordan ORTHONORMALITY/completeness -- equivalently 'the sum of the
    squares of each row (and column) of the CG table is 1' (Griffiths p.226)."""
    for (j1, j2) in _PAIRS:
        U, labels, unc = coupled_basis(j1, j2)
        N = len(labels)
        assert np.allclose(U.conj().T @ U, np.eye(N), atol=1e-12)   # columns
        assert np.allclose(U @ U.conj().T, np.eye(N), atol=1e-12)   # rows
        # sum of squares along every row and every column is exactly 1:
        assert np.allclose((np.abs(U) ** 2).sum(axis=0), 1.0, atol=1e-12)
        assert np.allclose((np.abs(U) ** 2).sum(axis=1), 1.0, atol=1e-12)


def test_cg_coefficients_are_real():
    """Clebsch-Gordan coefficients are real in the Condon-Shortley convention."""
    for (j1, j2) in _PAIRS:
        U, _, _ = coupled_basis(j1, j2)
        assert np.max(np.abs(U.imag)) < 1e-12


def test_coupled_states_are_simultaneous_eigenstates():
    """Every coupled state |J,M> is a simultaneous eigenstate of J^2 (eigenvalue
    J(J+1)), J_z (M), J1^2 (j1(j1+1)) and J2^2 (j2(j2+1)) -- the defining property
    of the coupled basis."""
    for (j1, j2) in _PAIRS:
        U, labels, _ = coupled_basis(j1, j2)
        J2, Jz = J_squared(j1, j2), Jz_total(j1, j2)
        J1s, J2s = J1_squared(j1, j2), J2_squared(j1, j2)
        for col, (J, M) in enumerate(labels):
            v = U[:, col]
            assert np.allclose(J2 @ v, HBAR ** 2 * J * (J + 1) * v, atol=1e-10)
            assert np.allclose(Jz @ v, HBAR * M * v, atol=1e-10)
            assert np.allclose(J1s @ v, HBAR ** 2 * j1 * (j1 + 1) * v, atol=1e-10)
            assert np.allclose(J2s @ v, HBAR ** 2 * j2 * (j2 + 1) * v, atol=1e-10)


def test_U_block_diagonalizes_J2_and_Jz():
    """U^dag J^2 U is diagonal with entries J(J+1); U^dag J_z U is diagonal with
    entries M.  (The whole point: the coupled basis diagonalizes J^2, which is NOT
    diagonal in the uncoupled basis.)"""
    for (j1, j2) in _PAIRS:
        U, labels, _ = coupled_basis(j1, j2)
        J2b = U.conj().T @ J_squared(j1, j2) @ U
        Jzb = U.conj().T @ Jz_total(j1, j2) @ U
        d2 = np.array([HBAR ** 2 * J * (J + 1) for (J, M) in labels])
        dz = np.array([HBAR * M for (J, M) in labels])
        assert np.allclose(J2b, np.diag(d2), atol=1e-10)
        assert np.allclose(Jzb, np.diag(dz), atol=1e-10)


def test_J2_not_diagonal_in_uncoupled_basis():
    """Why we need CG at all: J^2 is NOT diagonal in the uncoupled basis (it mixes
    states of equal M), even though J_z, J1^2, J2^2 are.  This is Griffiths
    Problem 4.41, p.227: [J^2, J1z] != 0, so the uncoupled states are not J^2
    eigenstates and a linear recombination (the CG coefficients) is required."""
    for (j1, j2) in _PAIRS:
        J2 = J_squared(j1, j2)
        off = J2 - np.diag(np.diag(J2))
        assert np.max(np.abs(off)) > 1e-9                  # genuinely off-diagonal
        # the explicit Griffiths-4.41 statement:
        J1z = total_operators(j1, j2)["J1z"]
        assert not np.allclose(commutator(J2, J1z), 0.0, atol=1e-9)
        # ... but the TOTAL J_z does commute with J^2 (Griffiths p.227 footnote):
        Jz = Jz_total(j1, j2)
        assert np.allclose(commutator(J2, Jz), 0.0, atol=1e-12)


# --- the named special cases (explicit Griffiths values) ---------------------

def test_singlet_and_triplet_half_half():
    """1/2 (x) 1/2: the triplet (J=1) and singlet (J=0) come out exactly as in
    Griffiths Eqs. 4.175-4.176 (p.223-224).  Uncoupled order: |uu>,|ud>,|du>,|dd>
    with u = +1/2 (particle 1 first)."""
    U, labels, unc = coupled_basis(0.5, 0.5)
    assert unc == [(0.5, 0.5), (0.5, -0.5), (-0.5, 0.5), (-0.5, -0.5)]
    col = {lbl: i for i, lbl in enumerate(labels)}
    r2 = 1.0 / math.sqrt(2.0)
    expect = {
        (1.0, 1.0): [1, 0, 0, 0],                          # |uu>
        (1.0, 0.0): [0, r2, r2, 0],                        # (|ud>+|du>)/sqrt2
        (1.0, -1.0): [0, 0, 0, 1],                         # |dd>
        (0.0, 0.0): [0, r2, -r2, 0],                       # (|ud>-|du>)/sqrt2  SINGLET
    }
    for lbl, vec in expect.items():
        assert np.allclose(U[:, col[lbl]].real, vec, atol=1e-12), lbl
    # the singlet is antisymmetric, the triplet symmetric under particle swap:
    singlet = U[:, col[(0.0, 0.0)]].real
    assert math.isclose(singlet[1], -singlet[2])           # |ud> <-> -|du>
    triplet0 = U[:, col[(1.0, 0.0)]].real
    assert math.isclose(triplet0[1], triplet0[2])          # |ud> <->  |du>


def test_one_times_half_table():
    """1 (x) 1/2 reproduces Griffiths Table 4.8 (p.226) exactly.  Uncoupled order
    for j1=1, j2=1/2: (1,1/2),(1,-1/2),(0,1/2),(0,-1/2),(-1,1/2),(-1,-1/2)."""
    s = math.sqrt
    U, labels, unc = coupled_basis(1.0, 0.5)
    col = {lbl: i for i, lbl in enumerate(labels)}
    expect = {
        (1.5, 1.5): [1, 0, 0, 0, 0, 0],
        (1.5, 0.5): [0, s(1 / 3), s(2 / 3), 0, 0, 0],
        (1.5, -0.5): [0, 0, 0, s(2 / 3), s(1 / 3), 0],
        (1.5, -1.5): [0, 0, 0, 0, 0, 1],
        (0.5, 0.5): [0, s(2 / 3), -s(1 / 3), 0, 0, 0],
        (0.5, -0.5): [0, 0, 0, s(1 / 3), -s(2 / 3), 0],
    }
    for lbl, vec in expect.items():
        assert np.allclose(U[:, col[lbl]].real, vec, atol=1e-12), lbl


def test_cg_selection_rules_and_lookup():
    """cg_coefficient enforces m1+m2=M and the triangle |j1-j2|<=J<=j1+j2, and
    otherwise returns the matrix entry of U (Griffiths Eq. 4.183)."""
    # m1+m2 != M  -> 0
    assert cg_coefficient(0.5, 0.5, 0.5, 0.5, 1.0, 0.0) == 0.0
    # J outside the triangle -> 0
    assert cg_coefficient(0.5, 0.5, 0.5, -0.5, 2.0, 0.0) == 0.0
    # |M| > J -> 0
    assert cg_coefficient(1.0, 1.0, 0.5, 0.5, 0.5, 1.5) == 0.0
    # known values
    assert math.isclose(cg_coefficient(0.5, 0.5, 0.5, 0.5, 1.0, 1.0), 1.0)
    assert math.isclose(cg_coefficient(0.5, 0.5, 0.5, -0.5, 0.0, 0.0),
                        1.0 / math.sqrt(2.0), abs_tol=1e-12)
    assert math.isclose(cg_coefficient(0.5, -0.5, 0.5, 0.5, 0.0, 0.0),
                        -1.0 / math.sqrt(2.0), abs_tol=1e-12)
    # consistency with the full table
    for (j1, j2) in _PAIRS:
        table = cg_table(j1, j2)
        for (J, M), entries in table.items():
            for (m1, m2), c in entries.items():
                assert math.isclose(cg_coefficient(j1, m1, j2, m2, J, M), c,
                                    abs_tol=1e-12)


def test_ladder_normalization_within_a_multiplet():
    """Applying J_- to a coupled state lowers M by one with the standard norm
    J_-|J,M> = hbar sqrt(J(J+1)-M(M-1)) |J,M-1>.  (Griffiths Problem 4.37(a),
    p.226: apply S_- to the top triplet state and recover the next one.)"""
    Jm_cache = {}
    for (j1, j2) in _PAIRS:
        U, labels, _ = coupled_basis(j1, j2)
        col = {lbl: i for i, lbl in enumerate(labels)}
        Jm = Jminus_total(j1, j2)
        for (J, M) in labels:
            if M - 1 < -J - 1e-9:
                continue                                   # bottom rung
            v = U[:, col[(J, M)]]
            w = Jm @ v
            coeff = HBAR * math.sqrt(J * (J + 1) - M * (M - 1))
            assert np.allclose(w, coeff * U[:, col[(J, M - 1)]], atol=1e-10)


def test_cg_matches_sympy():
    """Independent cross-check of every Clebsch-Gordan coefficient against
    sympy.physics.wigner.clebsch_gordan (standard Condon-Shortley convention), so
    the recursion is not validated only against itself."""
    try:
        from sympy import Rational, sqrt, nsimplify
        from sympy.physics.wigner import clebsch_gordan
    except Exception as ex:                                # pragma: no cover
        print("    (skip: sympy unavailable:", ex, ")")
        return

    def R(x):
        return Rational(int(round(2 * x)), 2)

    for (j1, j2) in _PAIRS:
        table = cg_table(j1, j2)
        for (J, M), entries in table.items():
            for (m1, m2), c in entries.items():
                ref = float(clebsch_gordan(R(j1), R(j2), R(J),
                                           R(m1), R(m2), R(M)))
                assert math.isclose(c, ref, abs_tol=1e-9), \
                    ((j1, j2), (m1, m2), (J, M), c, ref)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
