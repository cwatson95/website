"""
MA-18  Group theory & symmetry -- finite groups (cyclic, dihedral, symmetric) via
their Cayley tables and the group axioms, Lagrange's theorem, matrix
representations, and the Lie algebras so(3) and su(2).

Part of the physics topic network (modules/topic_network.txt, module MA-18).
Symmetry is conservation: ~CM-18 (Noether's theorem), ~QF-03 (gauge groups),
~QM-10/~QM-11 (rotation group -> angular momentum & spin), ~MA-04 (reps are
matrices). Network bridge B8 (symmetry -> conservation).

Pure Python (math/cmath), dependency-free. A finite group is its element set plus
a binary operation; the axioms, element orders, and Lagrange's theorem are checked
directly from the Cayley table. Representations and the so(3)/su(2) commutators are
verified as explicit matrix identities.
"""

import cmath
import math
from itertools import permutations

__all__ = [
    "FiniteGroup", "cyclic_group", "symmetric_group", "dihedral_group",
    "compose_perm", "matmul", "commutator", "rotation_matrix", "cyclic_rep",
    "so3_generators", "pauli", "scalar",
]


# --- a finite group from a set + operation -----------------------------------

class FiniteGroup:
    """A finite group: a list of (hashable) elements and a binary operation
    op(a, b). All structural facts are read off the Cayley table."""

    def __init__(self, elements, op, name=""):
        self.elements = list(elements)
        self.op = op
        self.name = name

    def order(self):
        return len(self.elements)

    def closed(self):
        S = set(self.elements)
        return all(self.op(a, b) in S for a in self.elements for b in self.elements)

    def identity(self):
        for e in self.elements:
            if all(self.op(e, a) == a and self.op(a, e) == a for a in self.elements):
                return e
        return None

    def inverse(self, a):
        e = self.identity()
        for b in self.elements:
            if self.op(a, b) == e and self.op(b, a) == e:
                return b
        return None

    def associative(self):
        el = self.elements
        return all(self.op(self.op(a, b), c) == self.op(a, self.op(b, c))
                   for a in el for b in el for c in el)

    def is_group(self):
        if not self.closed() or self.identity() is None:
            return False
        if any(self.inverse(a) is None for a in self.elements):
            return False
        return self.associative()

    def is_abelian(self):
        return all(self.op(a, b) == self.op(b, a) for a in self.elements for b in self.elements)

    def element_order(self, a):
        e = self.identity()
        x = a
        k = 1
        while x != e:
            x = self.op(x, a)
            k += 1
        return k

    def cyclic_subgroup(self, a):
        e = self.identity()
        sub = [e]
        x = a
        while x != e:
            sub.append(x)
            x = self.op(x, a)
        return sub

    def subgroup_orders(self):
        """Orders of all cyclic subgroups <a> -- each must divide |G| (Lagrange)."""
        return sorted(set(len(self.cyclic_subgroup(a)) for a in self.elements))


# --- the standard families ---------------------------------------------------

def cyclic_group(n):
    """Z_n = integers mod n under addition."""
    return FiniteGroup(range(n), lambda a, b: (a + b) % n, name=f"Z_{n}")


def compose_perm(p, q):
    """Permutation composition (p after q): (p o q)[i] = p[q[i]]."""
    return tuple(p[q[i]] for i in range(len(p)))


def symmetric_group(n):
    """S_n = all permutations of {0,...,n-1} under composition."""
    return FiniteGroup(list(permutations(range(n))), compose_perm, name=f"S_{n}")


def dihedral_group(n):
    """D_n = symmetries of a regular n-gon, realized as permutations of its n
    vertices (n rotations + n reflections). D_3 comes out equal to S_3."""
    rot = [tuple((i + k) % n for i in range(n)) for k in range(n)]
    ref = [tuple((k - i) % n for i in range(n)) for k in range(n)]
    return FiniteGroup(rot + ref, compose_perm, name=f"D_{n}")


# --- matrices: representations and Lie algebras ------------------------------

def matmul(A, B):
    k = len(B)
    return [[sum(A[i][p] * B[p][j] for p in range(k)) for j in range(len(B[0]))]
            for i in range(len(A))]


def commutator(A, B):
    """[A, B] = AB - BA."""
    AB, BA = matmul(A, B), matmul(B, A)
    return [[AB[i][j] - BA[i][j] for j in range(len(A))] for i in range(len(A))]


def scalar(c, A):
    return [[c * A[i][j] for j in range(len(A[0]))] for i in range(len(A))]


def rotation_matrix(theta):
    c, s = math.cos(theta), math.sin(theta)
    return [[c, -s], [s, c]]


def cyclic_rep(n):
    """The 2-D rotation representation of Z_n: R(k) = rotation by 2 pi k / n.
    R(a) R(b) = R(a+b) makes it a homomorphism Z_n -> SO(2)."""
    return [rotation_matrix(2 * math.pi * k / n) for k in range(n)]


def so3_generators():
    """Real antisymmetric generators of rotations about x, y, z. They close the
    so(3) Lie algebra  [L_i, L_j] = epsilon_{ijk} L_k  (physics: J = -i L gives
    [J_i, J_j] = i epsilon_{ijk} J_k)."""
    Lx = [[0, 0, 0], [0, 0, -1], [0, 1, 0]]
    Ly = [[0, 0, 1], [0, 0, 0], [-1, 0, 0]]
    Lz = [[0, -1, 0], [1, 0, 0], [0, 0, 0]]
    return Lx, Ly, Lz


def pauli():
    """The Pauli matrices (generators of SU(2)/su(2)). sigma_i^2 = I and
    [sigma_i, sigma_j] = 2 i epsilon_{ijk} sigma_k -- the spin-1/2 rotation algebra."""
    I = 1j
    sx = [[0, 1], [1, 0]]
    sy = [[0, -I], [I, 0]]
    sz = [[1, 0], [0, -1]]
    return sx, sy, sz


# --- demo --------------------------------------------------------------------

def _mat_eq(A, B, tol=1e-9):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(len(A)) for j in range(len(A[0])))


def _demo():
    print("MA-18 group theory & symmetry -- demo")
    print("=" * 39)

    for G in (cyclic_group(6), symmetric_group(3), dihedral_group(3)):
        print(f"\n{G.name}: order {G.order()}  group? {G.is_group()}  abelian? {G.is_abelian()}")
        print(f"  cyclic-subgroup orders {G.subgroup_orders()}  (all divide {G.order()} -- Lagrange)")

    print("\nD_3 == S_3 (same 6 permutations of 3 vertices)?",
          set(dihedral_group(3).elements) == set(symmetric_group(3).elements))

    print("\nrepresentation of Z_4 by rotations: R(a)R(b) = R(a+b)?")
    rep = cyclic_rep(4)
    ok = all(_mat_eq(matmul(rep[a], rep[b]), rep[(a + b) % 4]) for a in range(4) for b in range(4))
    print(f"  homomorphism holds? {ok}")

    print("\nso(3) Lie algebra  [L_i, L_j] = eps_ijk L_k:")
    Lx, Ly, Lz = so3_generators()
    print(f"  [Lx,Ly] == Lz ? {_mat_eq(commutator(Lx, Ly), Lz)}")
    print(f"  [Ly,Lz] == Lx ? {_mat_eq(commutator(Ly, Lz), Lx)}")
    print(f"  [Lz,Lx] == Ly ? {_mat_eq(commutator(Lz, Lx), Ly)}")

    print("\nsu(2) Pauli matrices  [sigma_x, sigma_y] = 2 i sigma_z, sigma_x^2 = I:")
    sx, sy, sz = pauli()
    print(f"  [sx,sy] == 2i sz ? {_mat_eq(commutator(sx, sy), scalar(2j, sz))}")
    print(f"  sx^2 == I ? {_mat_eq(matmul(sx, sx), [[1,0],[0,1]])}")


if __name__ == "__main__":
    _demo()
