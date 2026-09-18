"""Tests for RE-08 covariant formulation of special relativity.

Run directly:   python3 test_covariant_sr.py     (-> "All N tests passed.")
Or with pytest: pytest test_covariant_sr.py

Every transformation law is cross-checked against REAL RE-03 Lorentz boosts
(lorentz.general_boost / lorentz.inverse): the Minkowski product, the contra-/
covariant contraction V^mu W_mu, the trace, eta and the Kronecker delta are all
verified invariant; lower/raise round-trips; the symmetric/antisymmetric split,
its vanishing cross-contraction, and the preservation of symmetry under boost
(Griffiths Prob. 12.50); and the numerical 4-gradient and d'Alembertian against
their exact closed forms (finite-difference tests use loose tolerances).
"""
import math
import os
import random
import sys

# Put MA-16 (kronecker_delta) and RE-03 (boosts) on the path.  covariant_sr also
# does this at import, but mirror it here so the test is robust under any import
# order / runner (pytest, direct).
_HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "..", "MA", "MA-16_tensor_analysis", "code"))
sys.path.insert(0, os.path.join(_HERE, "..", "..", "RE-03_lorentz_transformations", "code"))

from covariant_sr import (
    ETA, ETA_INV, mdot,
    transform_vector, transform_covector, transform_tensor2,
    lower, raise_, trace,
    symmetric_part, antisymmetric_part, double_contract,
    four_gradient, dalembertian,
)
import lorentz   # RE-03
import tensors   # MA-16

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=TOL):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def _mapprox(A, B, tol=TOL):
    return all(_approx(A[i][j], B[i][j], tol) for i in range(4) for j in range(4))


def _rand_vec(rng):
    return [rng.uniform(-3.0, 3.0) for _ in range(4)]


def _rand_tensor(rng):
    return [[rng.uniform(-3.0, 3.0) for _ in range(4)] for _ in range(4)]


def _rand_beta(rng, hi=0.9):
    while True:
        b = [rng.uniform(-hi, hi) for _ in range(3)]
        if b[0] ** 2 + b[1] ** 2 + b[2] ** 2 < hi * hi:
            return b


def _rand_boost(rng):
    """A genuine RE-03 Lorentz boost in a random direction."""
    return lorentz.general_boost(_rand_beta(rng))


def _transform_mixed(L, M):
    """Mixed (1,1) law  M'^mu_nu = Lambda^mu_a (Lambda^{-1})^b_nu M^a_b -- built
    inline (the module's public API only needs the pure contra/covariant laws)."""
    Linv = lorentz.inverse(L)
    return [[sum(L[mu][a] * Linv[b][nu] * M[a][b]
                 for a in range(4) for b in range(4))
             for nu in range(4)] for mu in range(4)]


# --- transformation laws & invariants ----------------------------------------

def test_transform_vector_preserves_minkowski_product():
    """A Lorentz boost leaves the Minkowski product u.v unchanged."""
    rng = random.Random(0)
    for _ in range(400):
        L = _rand_boost(rng)
        V, W = _rand_vec(rng), _rand_vec(rng)
        assert _approx(mdot(transform_vector(L, V), transform_vector(L, W)),
                       mdot(V, W))
        # transform_vector is exactly RE-03's own apply()
        assert _vapprox(transform_vector(L, V), lorentz.apply(L, V))


def test_lower_raise_roundtrip():
    rng = random.Random(1)
    for _ in range(400):
        V = _rand_vec(rng)
        assert _vapprox(raise_(lower(V)), V)
        assert _vapprox(lower(raise_(V)), V)
        # lowering flips only the time component's sign
        lo = lower(V)
        assert _approx(lo[0], -V[0]) and _vapprox(lo[1:], V[1:])
        # u.v can be written as the contraction u^mu v_mu
        U = _rand_vec(rng)
        assert _approx(mdot(U, V), sum(U[i] * lower(V)[i] for i in range(4)))


def test_contra_co_contraction_is_invariant():
    """V^mu W_mu is invariant: the covariant law is inverse-transpose to the
    contravariant one -- this is the entire reason covectors transform that way."""
    rng = random.Random(2)
    for _ in range(400):
        L = _rand_boost(rng)
        V = _rand_vec(rng)            # contravariant
        Wlow = _rand_vec(rng)         # covariant (lower index)
        before = sum(V[i] * Wlow[i] for i in range(4))
        after = sum(transform_vector(L, V)[i] * transform_covector(L, Wlow)[i]
                    for i in range(4))
        assert _approx(after, before)


def test_lowered_vector_transforms_covariantly():
    """Lowering with eta and transforming commute the right way: V_mu = eta V^mu
    must obey the covariant law if V^mu obeys the contravariant one."""
    rng = random.Random(3)
    for _ in range(300):
        L = _rand_boost(rng)
        V = _rand_vec(rng)
        assert _vapprox(transform_covector(L, lower(V)),
                        lower(transform_vector(L, V)))


def test_trace_is_invariant():
    rng = random.Random(4)
    for _ in range(300):
        L = _rand_boost(rng)
        T = _rand_tensor(rng)
        assert _approx(trace(transform_tensor2(L, T)), trace(T))
        # the metric supplies the minus sign on the 00 term
        assert _approx(trace(T), -T[0][0] + T[1][1] + T[2][2] + T[3][3])


def test_eta_is_an_invariant_tensor():
    """Lambda^mu_a Lambda^nu_b eta^{ab} = eta^{mu nu} for every Lorentz boost."""
    rng = random.Random(5)
    for _ in range(300):
        L = _rand_boost(rng)
        assert _mapprox(transform_tensor2(L, ETA), ETA)


def test_kronecker_delta_is_invariant():
    """delta^mu_nu (mixed) is Lambda-invariant: Lambda delta Lambda^{-1} = delta."""
    rng = random.Random(6)
    delta = tensors.kronecker_delta(4)
    for _ in range(300):
        L = _rand_boost(rng)
        assert _mapprox(_transform_mixed(L, delta), delta)


# --- symmetric / antisymmetric structure -------------------------------------

def test_symmetric_antisymmetric_decomposition():
    rng = random.Random(7)
    for _ in range(300):
        T = _rand_tensor(rng)
        S, A = symmetric_part(T), antisymmetric_part(T)
        for i in range(4):
            assert _approx(A[i][i], 0.0)                    # antisym diagonal = 0
            for j in range(4):
                assert _approx(S[i][j], S[j][i])            # symmetric
                assert _approx(A[i][j], -A[j][i])           # antisymmetric
                assert _approx(S[i][j] + A[i][j], T[i][j])  # reconstruct T


def test_double_contract_sym_with_antisym_vanishes():
    """Contracting a symmetric tensor with an antisymmetric one gives 0."""
    rng = random.Random(8)
    for _ in range(300):
        S = symmetric_part(_rand_tensor(rng))
        A = antisymmetric_part(_rand_tensor(rng))
        assert _approx(double_contract(S, A), 0.0)
        assert _approx(double_contract(A, S), 0.0)


def test_symmetry_type_preserved_by_boost():
    """Griffiths Prob. 12.50: a Lorentz transformation preserves symmetry and
    antisymmetry of a rank-2 tensor."""
    rng = random.Random(9)
    for _ in range(200):
        L = _rand_boost(rng)
        S = symmetric_part(_rand_tensor(rng))
        A = antisymmetric_part(_rand_tensor(rng))
        Sp, Ap = transform_tensor2(L, S), transform_tensor2(L, A)
        for i in range(4):
            for j in range(4):
                assert _approx(Sp[i][j], Sp[j][i])
                assert _approx(Ap[i][j], -Ap[j][i])


def test_double_contract_and_trace_on_outer_product():
    """For T^{mu nu} = a^mu b^nu:  eta_{mu nu} T^{mu nu} = trace(T) = a.b."""
    rng = random.Random(10)
    for _ in range(300):
        a, b = _rand_vec(rng), _rand_vec(rng)
        T = [[a[i] * b[j] for j in range(4)] for i in range(4)]
        assert _approx(double_contract(ETA, T), mdot(a, b))
        assert _approx(trace(T), mdot(a, b))


# --- the 4-gradient and the d'Alembertian ------------------------------------

def test_four_gradient_is_two_x_lower():
    """The covariant gradient of x.x is 2 x_mu (index down): the time component
    carries the metric's minus sign,  d_0(x.x) = -2 x^0."""
    rng = random.Random(11)
    f = lambda y: mdot(y, y)
    for _ in range(50):
        x = _rand_vec(rng)
        grad = four_gradient(f, x)
        assert _vapprox(grad, [2.0 * c for c in lower(x)], tol=1e-4)
        assert _approx(grad[0], -2.0 * x[0], tol=1e-4)


def test_four_gradient_of_linear_field_is_constant_covector():
    """For f = k_mu x^mu (k a fixed covector), d_mu f = k_mu everywhere."""
    rng = random.Random(12)
    for _ in range(50):
        k = _rand_vec(rng)
        f = lambda y, k=k: sum(k[i] * y[i] for i in range(4))
        assert _vapprox(four_gradient(f, _rand_vec(rng)), k, tol=1e-4)


def test_dalembertian_known_quadratics():
    x = [1.0, 2.0, -1.0, 0.5]
    assert _approx(dalembertian(lambda y: y[0] ** 2, x), -2.0, tol=1e-3)
    assert _approx(dalembertian(lambda y: y[1] ** 2, x), 2.0, tol=1e-3)
    assert _approx(dalembertian(lambda y: y[2] ** 2, x), 2.0, tol=1e-3)
    assert _approx(dalembertian(lambda y: y[3] ** 2, x), 2.0, tol=1e-3)
    # box(x.x) = -(-2) + 2 + 2 + 2 = 8  (= 2 eta^{mu nu} eta_{mu nu} = 2 * 4)
    assert _approx(dalembertian(lambda y: mdot(y, y), x), 8.0, tol=1e-3)


def test_dalembertian_is_a_lorentz_scalar():
    """box is frame-independent.  Take f(x) = (x^0)^2 (box f = -2); in a boosted
    frame the SAME scalar field looks like a generic quadratic (a.x)^2, yet box
    of it still returns -2 at every point."""
    rng = random.Random(13)
    f = lambda y: y[0] ** 2
    for _ in range(30):
        L = _rand_boost(rng)
        Linv = lorentz.inverse(L)
        phi = lambda yp, Linv=Linv: f(lorentz.apply(Linv, yp))   # field in boosted frame
        assert _approx(dalembertian(phi, _rand_vec(rng)), -2.0, tol=1e-2)


def test_null_plane_wave_solves_wave_equation():
    """A plane wave cos(k_mu x^mu) with NULL wavevector (k.k = 0) satisfies the
    homogeneous wave equation box f = 0, since box cos(k.x) = -(k.k) cos(k.x)."""
    k = [1.0, 1.0, 0.0, 0.0]            # null: -1 + 1 = 0
    assert _approx(mdot(k, k), 0.0)
    klow = lower(k)
    f = lambda y: math.cos(sum(klow[i] * y[i] for i in range(4)))
    for x in ([0.2, -0.3, 0.5, 0.1], [1.0, 0.4, -0.2, 0.7]):
        assert _approx(dalembertian(f, x), 0.0, tol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
