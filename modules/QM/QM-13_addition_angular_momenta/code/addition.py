"""
QM-13  Addition of angular momenta -- coupling two angular momenta j1 and j2,
the coupled (J^2, J_z) basis vs the uncoupled (j1 m1; j2 m2) basis, and the
Clebsch-Gordan coefficients that connect them.

Part of the physics topic network (see modules/topic_network.txt, module QM-13).
Builds directly on ~QM-10 (a single angular momentum: its operators ARE imported
below) and ~QM-11 (spin -- the 1/2 (x) 1/2 case worked here is two spins). Feeds
~QM-17 (L.S spin-orbit coupling / fine structure: J = L + S is this construction)
and ~QM-21 (the singlet (|ud>-|du>)/sqrt2 built here is the Bell state).

The story, each a function group below:
  1. The two spaces      -- each angular momentum lives in a (2j+1)-dim space;
                            the composite lives in the TENSOR PRODUCT, dimension
                            (2j1+1)(2j2+1). J1, J2 act via Kronecker products
                            (J1 = op (x) I, J2 = I (x) op).
  2. Total operators     -- J = J1 + J2 (componentwise); J^2 = (J1+J2)^2 and J_z.
  3. The multiplet content -- diagonalizing J^2 shows the product space splits as
                            j1 (x) j2 = (J=j1+j2) (+) ... (+) (J=|j1-j2|), each J
                            appearing once with (2J+1) states (a dimension check).
  4. Clebsch-Gordan      -- the unitary change of basis coupled<->uncoupled, built
                            from scratch by the highest-weight + ladder recursion
                            with the Condon-Shortley phase convention. Verified for
                            1/2(x)1/2 (singlet + triplet) and 1(x)1/2, against
                            orthonormality (unitarity) and an independent library.

UNITS: natural units  hbar = 1  throughout (inherited from ~QM-10's HBAR). So J^2
has eigenvalues J(J+1) and J_z has eigenvalues M (= m1 + m2). numpy supplies all
linear algebra; the single-angular-momentum matrices come from ~QM-10.

BASIS ORDERING (must match np.kron): for one angular momentum, ~QM-10 orders the
states top rung first, m = j, j-1, ..., -j. The product/uncoupled basis is then
ordered with m1 OUTER and m2 INNER, i.e. index = (j1-m1)*(2j2+1) + (j2-m2), which
is exactly what np.kron(op1, op2) assumes. The coupled basis is ordered by J
descending, and within each J by M = J, J-1, ..., -J.

Reference: Griffiths & Schroeter, Introduction to QM, 3rd ed., Sec. 4.4.3
(Addition of Angular Momenta, p.223-225); Clebsch-Gordan coefficients, the CG
expansion (Eq. 4.183) and Table 4.8, p.225-227. See ../refs.md for page-verified
citations.
"""

import math
import os
import sys
from functools import lru_cache

import numpy as np

# ~QM-10 (a single angular momentum) by relative path -- mirrors how QM-10 itself
# imports ~MA-12.  Once a shared `physkit` package exists this becomes
#     from physkit.angular_momentum import Lz, L_plus, ...
_HERE = os.path.dirname(os.path.abspath(__file__))
_QM10 = os.path.abspath(os.path.join(_HERE, "..", "..",
                                     "QM-10_angular_momentum", "code"))
if _QM10 not in sys.path:
    sys.path.insert(0, _QM10)

# single-j operators (2j+1)x(2j+1), hbar=1, basis m = j..-j.  API read from
# QM-10_angular_momentum/code/angular_momentum.py before importing.
from angular_momentum import (  # noqa: E402
    HBAR, dim, m_values, commutator,
    Lz, L_plus, L_minus, Lx, Ly, L_squared,
)

__all__ = [
    "HBAR", "dim", "commutator",
    # bookkeeping
    "multiplet_content", "decomposition", "dimension_check",
    "uncoupled_labels", "coupled_labels",
    # operators in the product space
    "embed_1", "embed_2", "total_operators",
    "Jz_total", "Jplus_total", "Jminus_total", "J_squared",
    "J1_squared", "J2_squared",
    # Clebsch-Gordan
    "coupled_basis", "cg_coefficient", "cg_table",
]


# --- 0. bookkeeping: the multiplet content -----------------------------------

def multiplet_content(j1, j2):
    """The total-J values produced by coupling j1 and j2:

        J = j1 + j2,  j1 + j2 - 1,  ...,  |j1 - j2|     (integer steps)

    Each value appears exactly ONCE (for two angular momenta).  Returned in
    DESCENDING order.  (Griffiths 3e Sec. 4.4.3, p.225: "you get every spin from
    s1+s2 down to |s1-s2| ... in integer steps".)"""
    j_max = j1 + j2
    j_min = abs(j1 - j2)
    n = int(round(j_max - j_min))
    return [j_max - k for k in range(n + 1)]


def decomposition(j1, j2):
    """Human-readable Clebsch-Gordan series, e.g. '1/2 (x) 1/2 = 1 (+) 0'.
    This is the decomposition of the direct product of two irreps of the rotation
    group into a direct sum of irreps (Griffiths 3e p.226)."""
    lhs = "%s (x) %s" % (_fmt(j1), _fmt(j2))
    rhs = " (+) ".join(_fmt(J) for J in multiplet_content(j1, j2))
    return "%s = %s" % (lhs, rhs)


def dimension_check(j1, j2):
    """Return (product_dim, sum_over_multiplets) where

        product_dim         = (2 j1 + 1)(2 j2 + 1)          [tensor-product dim]
        sum_over_multiplets = sum over J of (2 J + 1)        [coupled-basis dim]

    They must be EQUAL: coupling rearranges the same Hilbert space, it does not
    change its dimension."""
    prod = dim(j1) * dim(j2)
    tot = sum(dim(J) for J in multiplet_content(j1, j2))
    return prod, tot


def uncoupled_labels(j1, j2):
    """The product-basis labels (m1, m2) in the canonical order (m1 outer, m2
    inner) that matches np.kron.  Length (2j1+1)(2j2+1)."""
    return [(float(m1), float(m2))
            for m1 in m_values(j1) for m2 in m_values(j2)]


def coupled_labels(j1, j2):
    """The coupled-basis labels (J, M), J descending and M = J..-J within each J.
    Same length as uncoupled_labels (the two bases span the same space)."""
    out = []
    for J in multiplet_content(j1, j2):
        for M in [J - k for k in range(dim(J))]:
            out.append((float(J), float(M)))
    return out


# --- 1./2. operators in the product space ------------------------------------

def _eye(j):
    return np.eye(dim(j), dtype=complex)


def embed_1(op, j2):
    """Lift an operator that acts on angular momentum 1 to the product space:
    op (x) I_2  (it acts as the identity on space 2)."""
    return np.kron(op, _eye(j2))


def embed_2(op, j1):
    """Lift an operator that acts on angular momentum 2 to the product space:
    I_1 (x) op."""
    return np.kron(_eye(j1), op)


def Jz_total(j1, j2):
    """Total z-component  J_z = J1z + J2z  in the product basis.  Diagonal, with
    entries M = m1 + m2 -- "the z-components just add" (Griffiths 3e p.223)."""
    return embed_1(Lz(j1), j2) + embed_2(Lz(j2), j1)


def Jplus_total(j1, j2):
    """Total raising operator  J_+ = J1+ + J2+ ."""
    return embed_1(L_plus(j1), j2) + embed_2(L_plus(j2), j1)


def Jminus_total(j1, j2):
    """Total lowering operator  J_- = J1- + J2-  (Griffiths uses S_- to build the
    triplet from |1 1> in Eq. 4.175, p.223)."""
    return embed_1(L_minus(j1), j2) + embed_2(L_minus(j2), j1)


def J1_squared(j1, j2):
    """J1^2 in the product space = (j1(j1+1)) I on space 1, tensored with I_2.
    Its single eigenvalue is hbar^2 j1(j1+1)."""
    return embed_1(L_squared(j1), j2)


def J2_squared(j1, j2):
    """J2^2 in the product space.  Single eigenvalue hbar^2 j2(j2+1)."""
    return embed_2(L_squared(j2), j1)


def total_operators(j1, j2):
    """All operators of the coupled problem in the product basis, as a dict:

        'J1x','J1y','J1z','J2x','J2y','J2z'   the two angular momenta (embedded)
        'Jx','Jy','Jz'                        totals  J_i = J1i + J2i
        'J+','J-'                             total ladder operators
        'J1^2','J2^2'                         the two Casimirs (constant on the space)
        'J^2'                                 the total Casimir J^2 = Jx^2+Jy^2+Jz^2

    J^2 is formed directly as Jx@Jx + Jy@Jy + Jz@Jz; that it also equals
    J1^2 + J2^2 + 2 J1.J2 is checked in the tests."""
    I1, I2 = _eye(j1), _eye(j2)
    J1x, J1y, J1z = np.kron(Lx(j1), I2), np.kron(Ly(j1), I2), np.kron(Lz(j1), I2)
    J2x, J2y, J2z = np.kron(I1, Lx(j2)), np.kron(I1, Ly(j2)), np.kron(I1, Lz(j2))
    Jx, Jy, Jz = J1x + J2x, J1y + J2y, J1z + J2z
    Jp = np.kron(L_plus(j1), I2) + np.kron(I1, L_plus(j2))
    Jm = np.kron(L_minus(j1), I2) + np.kron(I1, L_minus(j2))
    J1sq = np.kron(L_squared(j1), I2)
    J2sq = np.kron(I1, L_squared(j2))
    Jsq = Jx @ Jx + Jy @ Jy + Jz @ Jz
    return {"J1x": J1x, "J1y": J1y, "J1z": J1z,
            "J2x": J2x, "J2y": J2y, "J2z": J2z,
            "Jx": Jx, "Jy": Jy, "Jz": Jz, "J+": Jp, "J-": Jm,
            "J1^2": J1sq, "J2^2": J2sq, "J^2": Jsq}


def J_squared(j1, j2):
    """The total Casimir J^2 = (J1 + J2)^2 in the product basis.  Block-diagonal
    once rotated to the coupled basis, with block J carrying eigenvalue
    hbar^2 J(J+1)."""
    return total_operators(j1, j2)["J^2"]


# --- 3./4. the coupled basis and Clebsch-Gordan coefficients -----------------

def _uncoupled_index(j1, j2, m1, m2):
    """Row index of the product state |j1 m1>|j2 m2> in the canonical ordering."""
    i1 = int(round(j1 - m1))
    i2 = int(round(j2 - m2))
    return i1 * dim(j2) + i2


def _unit(n, k):
    v = np.zeros(n, dtype=complex)
    v[k] = 1.0
    return v


@lru_cache(maxsize=None)
def _coupled_basis_cached(j1, j2):
    """Worker for coupled_basis (cached).  Returns (U, coupled_labels_tuple).

    Algorithm (the textbook highest-weight + ladder construction, Condon-Shortley
    convention):
      * For each J from j1+j2 down to |j1-j2|:
          - the top state |J, J> is the unit vector in the M = J sector that is
            orthogonal to the |J', J> already built for J' > J (there is exactly
            one such direction).  Its phase is fixed so the amplitude on the
            product state with the LARGEST m1 (= j1, m2 = J - j1) is real positive
            -- the Condon-Shortley convention.
          - the rest of the multiplet is generated by repeated J_- :
                |J, M-1> = J_- |J, M> / (hbar sqrt(J(J+1) - M(M-1))).
      * The coupled states, stacked as columns in label order, form the unitary
        change-of-basis matrix U whose entries are the Clebsch-Gordan coefficients
        U[(m1,m2), (J,M)] = <j1 m1; j2 m2 | J M>  (Griffiths 3e Eq. 4.183)."""
    N = dim(j1) * dim(j2)
    unc = uncoupled_labels(j1, j2)
    Jm = Jminus_total(j1, j2)

    states = {}                                   # (J, M) -> column vector
    built_Js = []                                 # processed J's (descending)
    for J in multiplet_content(j1, j2):
        # --- top state |J, J> in the M = J sector --------------------------
        M = J
        sub_idx = [k for k, (m1, m2) in enumerate(unc)
                   if abs((m1 + m2) - M) < 1e-9]
        # already-built coupled states living at this M (from larger J'):
        existing = [states[(Jp, M)] for Jp in built_Js if M <= Jp + 1e-9]
        ortho = list(existing)                    # orthonormal set to project out
        survivors = []
        for k in sub_idx:                         # standard basis of the M-sector
            w = _unit(N, k)
            for b in ortho:
                w = w - (np.vdot(b, w)) * b        # Gram-Schmidt
            nrm = np.linalg.norm(w)
            if nrm > 1e-9:
                w = w / nrm
                ortho.append(w)
                survivors.append(w)
        assert len(survivors) == 1, (j1, j2, J, len(survivors))
        top = survivors[0]
        # Condon-Shortley phase: amplitude on (m1 = j1, m2 = J - j1) real positive
        ref = _uncoupled_index(j1, j2, j1, J - j1)
        c = top[ref]
        if abs(c) > 1e-12:
            top = top * (np.conj(c) / abs(c))
        top = top / np.linalg.norm(top)
        states[(J, J)] = top

        # --- ladder down to M = -J -----------------------------------------
        for step in range(dim(J) - 1):
            M = J - step
            v = states[(J, M)]
            w = Jm @ v
            coeff = HBAR * math.sqrt(J * (J + 1) - M * (M - 1))
            states[(J, M - 1)] = w / coeff
        built_Js.append(J)

    labels = []
    cols = []
    for (J, M) in coupled_labels(j1, j2):
        labels.append((J, M))
        cols.append(states[(J, M)])
    U = np.array(cols, dtype=complex).T            # columns = coupled states
    # CG coefficients are real; scrub negligible imaginary parts.
    if np.max(np.abs(U.imag)) < 1e-12:
        U = U.real.astype(complex)
    return U, tuple(labels)


def coupled_basis(j1, j2):
    """Return (U, coupled_labels, uncoupled_labels) for coupling j1 and j2.

    U is the (N x N) unitary change-of-basis matrix: column k is the coupled state
    |J_k, M_k> written in the uncoupled product basis, so

        |J, M> = sum_{m1+m2=M}  <j1 m1; j2 m2 | J M> |j1 m1>|j2 m2>,

    and U[row, col] = <j1 m1; j2 m2 | J M> is the Clebsch-Gordan coefficient
    (Griffiths 3e Eq. 4.183, p.225).  Do not mutate the returned U (it is cached).
    """
    U, labels = _coupled_basis_cached(j1, j2)
    return U, list(labels), uncoupled_labels(j1, j2)


def cg_coefficient(j1, m1, j2, m2, J, M):
    """The Clebsch-Gordan coefficient  <j1 m1; j2 m2 | J M>  (hbar = 1).

    Zero unless m1 + m2 = M (z-components add, Griffiths p.225) AND
    |j1 - j2| <= J <= j1 + j2 (the triangle rule, p.225).  Real, with the
    Condon-Shortley sign convention (matches Griffiths Table 4.8, p.226, and
    sympy.physics.wigner.clebsch_gordan)."""
    if abs((m1 + m2) - M) > 1e-9:
        return 0.0
    if J < abs(j1 - j2) - 1e-9 or J > j1 + j2 + 1e-9:
        return 0.0
    if abs(m1) > j1 + 1e-9 or abs(m2) > j2 + 1e-9 or abs(M) > J + 1e-9:
        return 0.0
    U, labels = _coupled_basis_cached(j1, j2)
    key = (_k(J), _k(M))
    col = next((i for i, (Jj, Mm) in enumerate(labels)
                if (_k(Jj), _k(Mm)) == key), None)
    if col is None:
        return 0.0
    row = _uncoupled_index(j1, j2, m1, m2)
    val = U[row, col]
    return float(val.real)


def cg_table(j1, j2):
    """Clebsch-Gordan coefficients as a nested dict {(J, M): {(m1, m2): coeff}},
    keeping only |coeff| > 1e-12.  This is the content of Griffiths Table 4.8."""
    U, labels, unc = coupled_basis(j1, j2)
    table = {}
    for col, (J, M) in enumerate(labels):
        row_entries = {}
        for row, (m1, m2) in enumerate(unc):
            c = U[row, col].real
            if abs(c) > 1e-12:
                row_entries[(m1, m2)] = float(c)
        table[(J, M)] = row_entries
    return table


# --- small formatting / key helpers ------------------------------------------

def _k(x):
    """Robust integer key for a half-integer (avoids float-equality on labels)."""
    return int(round(2 * x))


def _fmt(j):
    """Format a (possibly half-integer) quantum number: 0.5 -> '1/2', 2.0 -> '2'."""
    if abs(j - round(j)) < 1e-9:
        return str(int(round(j)))
    return "%d/2" % int(round(2 * j))


# --- demo --------------------------------------------------------------------

def _demo():
    np.set_printoptions(precision=3, suppress=True)
    print("QM-13 Addition of angular momenta -- coupled vs uncoupled (hbar = 1)\n")

    for (j1, j2) in [(0.5, 0.5), (1.0, 0.5)]:
        print("=" * 64)
        print("  %s" % decomposition(j1, j2))
        prod, tot = dimension_check(j1, j2)
        print("  dimension check: (2j1+1)(2j2+1) = %d  =  sum_J (2J+1) = %d"
              % (prod, tot))

        J2 = J_squared(j1, j2)
        ev = np.sort(np.round(np.linalg.eigvalsh(J2).real, 6))
        print("  J^2 eigenvalues J(J+1): %s"
              % ", ".join("%.3f" % e for e in ev))
        print("    expected:", ", ".join(
            "%.3f(x%d)" % (J * (J + 1), dim(J)) for J in multiplet_content(j1, j2)))

        print("  Clebsch-Gordan table  <j1 m1; j2 m2 | J M>:")
        table = cg_table(j1, j2)
        for (J, M), entries in table.items():
            terms = "  ".join(
                "%+.3f|%s,%s>" % (c, _fmt(m1), _fmt(m2))
                for (m1, m2), c in sorted(entries.items(), reverse=True))
            print("    |J=%s, M=%s> = %s" % (_fmt(J), _fmt(M), terms))
        print()

    # the headline 1/2 (x) 1/2 result, named:
    print("=" * 64)
    print("  Two spin-1/2  ->  singlet (J=0) + triplet (J=1):")
    table = cg_table(0.5, 0.5)
    names = {(1.0, 1.0): "triplet", (1.0, 0.0): "triplet", (1.0, -1.0): "triplet",
             (0.0, 0.0): "SINGLET  (the ~QM-21 Bell state)"}
    for (J, M), entries in table.items():
        terms = "  ".join("%+.3f|%s%s>"
                          % (c, _arrow(m1), _arrow(m2))
                          for (m1, m2), c in sorted(entries.items(), reverse=True))
        print("    |%s,%s>  %-8s = %s" % (_fmt(J), _fmt(M), names[(J, M)], terms))


def _arrow(m):
    return "u" if m > 0 else "d"


if __name__ == "__main__":
    _demo()
