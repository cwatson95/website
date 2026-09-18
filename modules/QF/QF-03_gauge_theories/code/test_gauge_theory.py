"""Tests for QF-03 gauge theories (QED & gauge invariance).

Run:  python3 test_gauge_theory.py     ->  "All N tests passed."
"""
import numpy as np

from gauge_theory import (
    field_strength, gauge_transform, covariant_derivative, yukawa_to_coulomb,
)


def _grid(N=64, L=2.0 * np.pi):
    dx = L / N
    x = np.linspace(0.0, L, N, endpoint=False)
    X0, X1 = np.meshgrid(x, x, indexing="ij")
    return X0, X1, dx


# --- the field strength F_{mu nu} -------------------------------------------

def test_field_strength_antisymmetric():
    X0, X1, dx = _grid()
    A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0)])
    F = field_strength(A, dx)
    assert np.allclose(F, -np.swapaxes(F, 0, 1), atol=1e-12)   # F_{mu nu} = -F_{nu mu}
    assert np.allclose(F[0, 0], 0.0, atol=1e-12)               # diagonal vanishes
    assert np.allclose(F[1, 1], 0.0, atol=1e-12)


def test_constant_field_strength():
    # A = (0, B x0)  =>  uniform F_01 = d0 A1 - d1 A0 = B  (np.gradient exact on linear)
    X0, X1, dx = _grid()
    B = 0.75
    A = np.stack([np.zeros_like(X0), B * X0])
    F = field_strength(A, dx)
    assert np.allclose(F[0, 1], B, atol=1e-10)
    assert np.allclose(F[1, 0], -B, atol=1e-10)


def test_field_strength_gauge_invariant():
    # HEADLINE: F is unchanged by A_mu -> A_mu + d_mu lambda, to machine precision
    X0, X1, dx = _grid()
    A = np.stack([0.4 * np.sin(X1) + 0.1 * X0,
                  0.3 * np.cos(X0) + 0.2 * np.sin(2.0 * X1)])
    lam = 0.7 * np.cos(X0) * np.cos(X1) + 0.5 * np.sin(X0) * np.cos(2.0 * X1)
    F0 = field_strength(A, dx)
    F1 = field_strength(gauge_transform(A, lam, dx), dx)
    assert np.max(np.abs(F1 - F0)) < 1e-10                     # max|Delta F| ~ 0


def test_pure_gauge_has_zero_field_strength():
    # A_mu = d_mu lambda  (pure gauge)  =>  F = 0 identically (curvature of a gradient)
    X0, X1, dx = _grid()
    lam = np.cos(X0) * np.cos(X1) + 0.3 * np.sin(2.0 * X0)
    A_pure = gauge_transform(np.zeros((2,) + X0.shape), lam, dx)
    assert np.max(np.abs(field_strength(A_pure, dx))) < 1e-10


# --- the covariant derivative D_mu = d_mu + i e A_mu -------------------------

def test_covariant_derivative_definition():
    X0, X1, dx = _grid()
    psi = (1.0 + 0.3 * np.cos(X0)) * np.exp(0.6j * np.sin(X1))
    A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0)])
    e = 0.7
    D = covariant_derivative(psi, A, e, dx)
    for mu in range(2):
        expect = np.gradient(psi, dx, axis=mu) + 1j * e * A[mu] * psi
        assert np.allclose(D[mu], expect, atol=1e-14)


def test_covariant_derivative_gauge_invariant():
    # HEADLINE: |D psi| invariant under a local phase, while |d psi| is NOT
    X0, X1, dx = _grid(N=96)
    e = 1.0
    psi = (1.0 + 0.3 * np.cos(X0)) * np.exp(0.6j * np.sin(X1))
    alpha = 0.8 * np.cos(X0) * np.sin(X1)
    psi_g = np.exp(1j * alpha) * psi
    A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0)])
    A_g = gauge_transform(A, -alpha / e, dx)                   # A_mu - (1/e) d_mu alpha
    D0 = covariant_derivative(psi, A, e, dx)
    D1 = covariant_derivative(psi_g, A_g, e, dx)
    g0 = np.stack([np.gradient(psi, dx, axis=mu) for mu in range(2)])
    g1 = np.stack([np.gradient(psi_g, dx, axis=mu) for mu in range(2)])
    sl = (slice(None), slice(1, -1), slice(1, -1))            # interior (drop one-sided edges)
    res_D = np.max(np.abs(np.abs(D1) - np.abs(D0))[sl])
    res_g = np.max(np.abs(np.abs(g1) - np.abs(g0))[sl])
    assert res_g > 0.3                       # ordinary derivative changes by O(1)
    assert res_D < 0.05                      # covariant derivative ~ invariant (O(dx^2))
    assert res_D < 0.1 * res_g               # and dramatically smaller


def test_covariant_derivative_convergence():
    # the |D psi| residual is pure discretization error: ~4x smaller when dx halves
    def residual(N):
        X0, X1, dx = _grid(N=N)
        e = 1.0
        psi = (1.0 + 0.3 * np.cos(X0)) * np.exp(0.6j * np.sin(X1))
        alpha = 0.8 * np.cos(X0) * np.sin(X1)
        A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0)])
        D0 = covariant_derivative(psi, A, e, dx)
        D1 = covariant_derivative(np.exp(1j * alpha) * psi,
                                  gauge_transform(A, -alpha / e, dx), e, dx)
        sl = (slice(None), slice(1, -1), slice(1, -1))
        return np.max(np.abs(np.abs(D1) - np.abs(D0))[sl])
    r1, r2 = residual(48), residual(96)
    assert r2 < 0.4 * r1                     # second order: halving dx ~quarters the error


# --- the photon propagator -> Coulomb potential -----------------------------

def test_yukawa_to_coulomb_limit():
    r = np.array([0.5, 1.0, 2.0, 5.0])
    coul = yukawa_to_coulomb(r, 0.0)
    assert np.allclose(coul, 1.0 / (4.0 * np.pi * r))         # m = 0 is exactly Coulomb
    assert np.all(yukawa_to_coulomb(r, 1.0) < coul)          # m>0 screened: Yukawa < Coulomb
    assert np.allclose(yukawa_to_coulomb(r, 1e-6), coul, atol=1e-4)   # m -> 0 limit
    # at fixed r, V increases monotonically toward Coulomb as m decreases
    vals = [yukawa_to_coulomb(1.0, m) for m in (2.0, 1.0, 0.5, 0.1, 0.0)]
    assert all(vals[i] < vals[i + 1] for i in range(len(vals) - 1))


def test_yukawa_solves_screened_poisson():
    # V = e^{-m r}/(4 pi r) is the Green's function of (-nabla^2 + m^2):
    # for r > 0,  nabla^2 V = (1/r) d^2/dr^2 (r V) = m^2 V   (so (-nabla^2+m^2)V = 0)
    m = 1.3
    r = np.linspace(0.5, 6.0, 4000)
    dr = r[1] - r[0]
    V = yukawa_to_coulomb(r, m)
    rV = r * V
    lap = np.gradient(np.gradient(rV, dr), dr) / r            # nabla^2 V = (rV)'' / r
    inner = slice(5, -5)
    assert np.allclose(lap[inner], m * m * V[inner], rtol=2e-3, atol=1e-6)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
