"""Tests for MA-18 group theory & symmetry. Pure stdlib.

Run:  python3 test_groups.py     ->  "All N tests passed."
"""
import math

from groups import (
    FiniteGroup, cyclic_group, symmetric_group, dihedral_group, compose_perm,
    matmul, commutator, rotation_matrix, cyclic_rep, so3_generators, pauli, scalar,
)


def _mat_eq(A, B, tol=1e-9):
    return all(abs(A[i][j] - B[i][j]) < tol for i in range(len(A)) for j in range(len(A[0])))


def test_cyclic_is_abelian_group():
    for n in (1, 2, 5, 6, 12):
        G = cyclic_group(n)
        assert G.is_group() and G.is_abelian()
        assert G.order() == n
        # every element order divides n (Lagrange)
        for a in G.elements:
            assert n % G.element_order(a) == 0


def test_symmetric_group_structure():
    G = symmetric_group(3)
    assert G.is_group()
    assert G.order() == 6
    assert not G.is_abelian()                      # S_3 is the smallest non-abelian group
    # element orders are 1, 2, 3 (and all divide 6)
    orders = sorted(set(G.element_order(a) for a in G.elements))
    assert orders == [1, 2, 3]


def test_lagrange_theorem():
    for G in (cyclic_group(12), symmetric_group(3), symmetric_group(4), dihedral_group(5)):
        for d in G.subgroup_orders():
            assert G.order() % d == 0              # subgroup order divides |G|


def test_dihedral_equals_symmetric_for_3():
    assert set(dihedral_group(3).elements) == set(symmetric_group(3).elements)
    # D_4 has order 8 and is non-abelian, but is NOT all of S_4 (order 24)
    D4 = dihedral_group(4)
    assert D4.order() == 8 and D4.is_group() and not D4.is_abelian()
    assert set(D4.elements) < set(symmetric_group(4).elements)


def test_permutation_composition():
    # (0 1 2) cycle composed with itself = (0 2 1)
    p = (1, 2, 0)
    assert compose_perm(p, p) == (2, 0, 1)
    assert compose_perm(p, compose_perm(p, p)) == (0, 1, 2)   # order 3


def test_cyclic_representation_homomorphism():
    for n in (3, 4, 6):
        rep = cyclic_rep(n)
        for a in range(n):
            for b in range(n):
                assert _mat_eq(matmul(rep[a], rep[b]), rep[(a + b) % n])
        # the generator is a rotation by 2 pi / n
        assert _mat_eq(rep[1], rotation_matrix(2 * math.pi / n))


def test_so3_lie_algebra():
    Lx, Ly, Lz = so3_generators()
    assert _mat_eq(commutator(Lx, Ly), Lz)
    assert _mat_eq(commutator(Ly, Lz), Lx)
    assert _mat_eq(commutator(Lz, Lx), Ly)
    # antisymmetry of the bracket
    assert _mat_eq(commutator(Ly, Lx), scalar(-1, Lz))


def test_su2_pauli_algebra():
    sx, sy, sz = pauli()
    I2 = [[1, 0], [0, 1]]
    # squares to the identity
    for s in (sx, sy, sz):
        assert _mat_eq(matmul(s, s), I2)
    # [sigma_i, sigma_j] = 2 i eps_ijk sigma_k
    assert _mat_eq(commutator(sx, sy), scalar(2j, sz))
    assert _mat_eq(commutator(sy, sz), scalar(2j, sx))
    assert _mat_eq(commutator(sz, sx), scalar(2j, sy))
    # anticommute: sx sy + sy sx = 0
    s = matmul(sx, sy)
    t = matmul(sy, sx)
    assert _mat_eq([[s[i][j] + t[i][j] for j in range(2)] for i in range(2)], [[0, 0], [0, 0]])


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
