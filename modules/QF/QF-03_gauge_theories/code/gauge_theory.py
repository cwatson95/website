"""QF-03  Gauge theories -- QED & gauge invariance.

Physics topic network, module QF-03 (modules/topic_network.txt) -- KEY BRIDGE B8
(symmetry -> conservation / interaction:  MA-18 groups -> CM-18 Noether -> QF-03
gauge).  Source: Peskin & Schroeder, *An Introduction to Quantum Field Theory*,
Ch. 4 (the QED Lagrangian, minimal coupling, local gauge invariance) and Ch. 7
(the Ward-Takahashi identity); cross-cf. Zee, *QFT in a Nutshell*, Sect. III.4
("Gauge invariance: a photon can find no rest").  Builds on ~EM-09 (the classical
abelian gauge freedom A -> A + grad(lambda)).

The gauge principle in one line: promoting the GLOBAL phase symmetry of the Dirac
field, psi -> e^{i alpha} psi, to a LOCAL one, psi -> e^{i alpha(x)} psi, forces a
connection field A_mu coupled through the covariant derivative

    D_mu = d_mu + i e A_mu ,      A_mu -> A_mu - (1/e) d_mu alpha ,

so that D_mu psi -> e^{i alpha(x)} D_mu psi transforms like psi itself ("minimal
coupling").  The field strength F_{mu nu} = d_mu A_nu - d_nu A_mu is then gauge
INVARIANT, and the QED Lagrangian

    L = psibar (i gamma^mu D_mu - m) psi - (1/4) F_{mu nu} F^{mu nu}

follows.  Gauge symmetry forbids a photon mass term (1/2) m^2 A_mu A^mu, so the
photon is massless and electrostatics is Coulombic, V(r) = 1/(4 pi r) -- the m -> 0
limit of the Yukawa potential e^{-m r}/(4 pi r) read off the (massive) boson
propagator.

This module works numerically on a small lattice:
  * field_strength + gauge_transform  -> demonstrate  max|Delta F| ~ 0  (F is gauge
                                         invariant to machine precision);
  * covariant_derivative              -> |D psi| is gauge invariant while |d psi|
                                         is not;
  * yukawa_to_coulomb                 -> e^{-m r}/(4 pi r)  ->  1/(4 pi r) as m -> 0.

Conventions: natural units; the lattice index mu runs over the spacetime components
stored as axis 0 of the field arrays, and d_mu is a centred finite difference
(numpy.gradient).  e is the gauge coupling (charge).  See refs.md for citations.
"""

import numpy as np

__all__ = [
    "field_strength", "gauge_transform", "covariant_derivative",
    "yukawa_to_coulomb",
]


# --- the gauge field: strength tensor and gauge transformation ---------------

def field_strength(A, dx):
    """Abelian field-strength tensor  F_{mu nu} = d_mu A_nu - d_nu A_mu.

    `A` is the gauge potential sampled on a D-dimensional lattice with shape
    (D,) + grid_shape, so `A[mu]` is the mu-component field and carries D spatial
    axes; `dx` is the (uniform) lattice spacing.  Returns `F` of shape
    (D, D) + grid_shape, antisymmetric in (mu, nu), built from centred finite
    differences (numpy.gradient).

    F_{mu nu} is GAUGE INVARIANT: under A_mu -> A_mu + d_mu lambda it picks up only
    d_mu d_nu lambda - d_nu d_mu lambda, which vanishes because finite-difference
    partials along distinct axes commute exactly.  Equivalently F_{mu nu} is the
    curvature of the connection, i e F_{mu nu} = [D_mu, D_nu]  (Peskin Sect. 4.1)."""
    A = np.asarray(A, dtype=float)
    D = A.shape[0]
    grid = A.shape[1:]
    if len(grid) != D:
        raise ValueError("A must have shape (D,)+grid with len(grid)==D "
                         "(one spatial axis per spacetime component)")
    dA = np.empty((D, D) + grid, dtype=float)
    for mu in range(D):
        for nu in range(D):
            dA[mu, nu] = np.gradient(A[nu], dx, axis=mu)   # d_mu A_nu
    return dA - np.swapaxes(dA, 0, 1)                       # F = d_mu A_nu - d_nu A_mu


def gauge_transform(A, lambda_field, dx):
    """Abelian gauge transformation  A_mu -> A_mu + d_mu lambda.

    This is the classical gauge freedom of ~EM-09 (A -> A + grad lambda); the QED
    convention A_mu -> A_mu - (1/e) d_mu alpha is the special case lambda = -alpha/e.
    It leaves F_{mu nu} unchanged (see `field_strength`).  `lambda_field` has shape
    grid_shape; returns the shifted potential, same shape as `A`."""
    A = np.asarray(A, dtype=float)
    D = A.shape[0]
    out = np.array(A, dtype=float)
    for mu in range(D):
        out[mu] = A[mu] + np.gradient(lambda_field, dx, axis=mu)
    return out


# --- the matter field: minimal coupling -------------------------------------

def covariant_derivative(psi, A, e, dx):
    """Gauge-covariant derivative  (D_mu psi) = d_mu psi + i e A_mu psi.

    `psi` is a complex matter field on the lattice (shape grid_shape); `A` is the
    gauge potential (shape (D,)+grid_shape); `e` the coupling.  Returns `D psi` of
    shape (D,) + grid_shape.

    Under the COMBINED gauge transformation  psi -> e^{i alpha(x)} psi,
    A_mu -> A_mu - (1/e) d_mu alpha,  it transforms covariantly,
    D_mu psi -> e^{i alpha} D_mu psi, so |D_mu psi| is gauge INVARIANT -- unlike the
    ordinary derivative d_mu psi, whose modulus changes because d_mu(e^{i alpha}psi)
    = e^{i alpha}(d_mu psi + i (d_mu alpha) psi) carries the stray gradient of the
    phase (Peskin Sect. 4.1).  (Numerically |D psi| is invariant up to the O(dx^2)
    finite-difference error in the discrete Leibniz rule.)"""
    psi = np.asarray(psi, dtype=complex)
    A = np.asarray(A, dtype=float)
    D = A.shape[0]
    out = np.empty((D,) + psi.shape, dtype=complex)
    for mu in range(D):
        out[mu] = np.gradient(psi, dx, axis=mu) + 1j * e * A[mu] * psi
    return out


# --- the photon: propagator -> static potential ------------------------------

def yukawa_to_coulomb(r, m):
    """Static potential from one-boson exchange:  V(r) = e^{-m r} / (4 pi r).

    This is the spatial Fourier transform of the (massive) boson propagator
    1/(q^2 + m^2) -- the Green's function of the operator (-nabla^2 + m^2):
        integral d^3q/(2 pi)^3  e^{i q.r}/(q^2 + m^2)  =  e^{-m r}/(4 pi r).
    For m > 0 it is the short-range YUKAWA potential; as m -> 0 the exponential -> 1
    and it becomes the long-range COULOMB potential 1/(4 pi r).  Because gauge
    invariance forbids a photon mass, the photon is massless and electrostatics is
    Coulombic (Peskin Sect. 4.7).  `r` may be a scalar or array; `m` a non-negative
    scalar (m = 0 returns the Coulomb potential exactly)."""
    r = np.asarray(r, dtype=float)
    return np.exp(-m * r) / (4.0 * np.pi * r)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QF-03  Gauge theories -- QED & gauge invariance  (demo)")
    print("=" * 58)

    # a small 2-D lattice (spacetime index mu = 0, 1)
    N, L = 64, 2.0 * np.pi
    dx = L / N
    x = np.linspace(0.0, L, N, endpoint=False)
    X0, X1 = np.meshgrid(x, x, indexing="ij")

    # a generic (non-pure-gauge) potential and a coupling
    A = np.stack([0.4 * np.sin(X1), 0.3 * np.cos(X0) + 0.2 * np.sin(2.0 * X1)])
    e = 1.0

    # 1) F_{mu nu} is gauge invariant ------------------------------------
    F0 = field_strength(A, dx)
    lam = 0.7 * np.cos(X0) * np.cos(X1) + 0.5 * np.sin(X0)
    F1 = field_strength(gauge_transform(A, lam, dx), dx)
    A_pure = gauge_transform(np.zeros_like(A), lam, dx)        # A_mu = d_mu lambda
    print("\n1) field strength under  A_mu -> A_mu + d_mu lambda :")
    print("   F antisymmetric:           max|F + F^T| = %.2e" %
          np.max(np.abs(F0 + np.swapaxes(F0, 0, 1))))
    print("   GAUGE-INVARIANCE residual: max|Delta F| = %.2e   (-> 0)" %
          np.max(np.abs(F1 - F0)))
    print("   pure gauge A=d(lambda):    max|F|       = %.2e   (-> 0)" %
          np.max(np.abs(field_strength(A_pure, dx))))

    # 2) covariant derivative: |D psi| invariant, |d psi| not -------------
    psi = (1.0 + 0.3 * np.cos(X0)) * np.exp(0.6j * np.sin(X1))
    alpha = 0.8 * np.cos(X0) * np.sin(X1)
    psi_g = np.exp(1j * alpha) * psi
    A_g = gauge_transform(A, -alpha / e, dx)                   # A_mu - (1/e) d_mu alpha
    D0 = covariant_derivative(psi, A, e, dx)
    D1 = covariant_derivative(psi_g, A_g, e, dx)
    g0 = np.stack([np.gradient(psi, dx, axis=mu) for mu in range(2)])
    g1 = np.stack([np.gradient(psi_g, dx, axis=mu) for mu in range(2)])
    sl = (slice(None), slice(1, -1), slice(1, -1))            # interior
    res_D = np.max(np.abs(np.abs(D1) - np.abs(D0))[sl])
    res_g = np.max(np.abs(np.abs(g1) - np.abs(g0))[sl])
    print("\n2) local phase  psi -> e^{i alpha(x)} psi,  A_mu -> A_mu - (1/e) d_mu alpha :")
    print("   |d_mu psi|  changes by  max = %.3e   (ordinary derivative NOT invariant)"
          % res_g)
    print("   |D_mu psi|  changes by  max = %.3e   (covariant derivative invariant, O(dx^2))"
          % res_D)

    # 3) Yukawa -> Coulomb as m -> 0 --------------------------------------
    r = 1.0
    coul = yukawa_to_coulomb(r, 0.0)
    print("\n3) one-boson-exchange potential  V(r=%.0f) = e^{-m r}/(4 pi r) :" % r)
    for m in (2.0, 1.0, 0.5, 0.1, 0.0):
        V = yukawa_to_coulomb(r, m)
        tag = "  <- Coulomb 1/(4 pi r)" if m == 0.0 else ""
        print("   m = %4.1f :  V = %.6f   (V / V_Coulomb = %.4f)%s" %
              (m, V, V / coul, tag))


if __name__ == "__main__":
    _demo()
