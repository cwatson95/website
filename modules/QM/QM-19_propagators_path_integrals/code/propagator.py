"""
QM-19  Propagators & path integrals -- the kernel K(x,t;x',0) = <x|exp(-iHt/hbar)|x'>
that evolves any wavefunction, and Feynman's sum-over-paths that builds it.

Part of the physics topic network (modules/topic_network.txt, module QM-19).
Builds on ~QM-03 (time evolution of Psi) and ~MA-14 (Green's functions /
propagators -- IMPORTED below: the propagator IS the time-domain Green's function
of the Schrodinger operator).  Key bridge B1 to ~CM-17 (the classical action
S = integral L dt; NOT built yet -- the stationary-phase hbar->0 limit of the
path integral hands the baton to Lagrangian mechanics).  Forward to ~QF-01 (the
path integral is the starting point of quantum field theory).

The story, each a function group below:

  1. The propagator (kernel).  Psi(x,t) = integral K(x,t;x',0) Psi(x',0) dx'.
     For a time-independent H with stationary states psi_n, energies E_n,
        K(x,t;x',0) = sum_n psi_n(x) psi_n*(x') exp(-i E_n t / hbar).
     (Griffiths 3e Problem 6.30, Eq. 6.79, p.342.)

  2. The free particle.   K0 = sqrt(m/(2 pi i hbar t)) exp(i m (x-x')^2 / (2 hbar t)).
     We verify it (a) reduces to delta(x-x') as t->0, (b) obeys the semigroup
     (composition) law, (c) solves the free Schrodinger equation -- i.e. it is the
     retarded Green's function -- and (d) evolves a Gaussian packet to exactly the
     same state as a direct spectral (split-step FFT) integration of the TDSE.

  3. The harmonic oscillator.   K = sqrt(m omega/(2 pi i hbar sin omega t)) *
        exp{ i m omega/(2 hbar sin omega t) [(x^2+x'^2) cos omega t - 2 x x'] }
     (Mehler's formula; Griffiths Problem 6.30(b)).  Checked by the free limit
     omega->0 and by solving the oscillator Schrodinger equation.

  4. The path integral.   K = integral D[x] exp(i S[x]/hbar),  S = integral L dt,
     L = (1/2) m xdot^2 - V.  Time-sliced: K = lim_{N->inf} (m/2 pi i hbar eps)^{N/2}
     integral prod dx_k exp(i/hbar sum_k S_k).  We (a) reconstruct the FREE K0 by
     the literal real-time sum over 1 and 2 intermediate points, and (b) show
     Trotter convergence to the closed form as N->inf for free AND harmonic in
     IMAGINARY time t = -i tau (Wick rotation: the only numerically stable route,
     since the real-time kernel has constant modulus and does not damp -- the
     "sign problem").  The classical path is the stationary-phase (hbar->0) limit.

  5. Connection to ~MA-14.  The propagator's spectral sum sum_n psi_n psi_n* f(E_n)
     with f = exp(-iE_n t) is the dynamical sibling of MA-14's Green's-function
     eigen-sum with f = 1/lambda_n.  For the particle in a box we IMPORT MA-14's
     green_series / green_dirichlet and show the static (E->0) resolvent
     sum_n psi_n(x) psi_n(x') / E_n equals the box Hamiltonian's Green's function.

UNITS: natural units  hbar = m = 1  throughout (HBAR, MASS kept explicit so the
formulae read in physical form).  numpy supplies the arrays/FFT; every claim is
checked against a closed form in test_propagator.py.
"""

import os
import sys

import numpy as np

# --- cross-link ~MA-14: the propagator is a Green's function. Import MA-14's
# eigenfunction-sum Green's function (green_series) and its closed form
# (green_dirichlet) by relative path -- same pattern QM-09/QM-10 use for MA-12.
# MA-14 API (read before importing): green_series(x, xi, nmax) = sum 2 sin(n pi x)
# sin(n pi xi)/(n pi)^2 ;  green_dirichlet(x, xi) = x_<(1 - x_>).
_HERE = os.path.dirname(os.path.abspath(__file__))
_MA14 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA",
                                     "MA-14_greens_functions", "code"))
if _MA14 not in sys.path:
    sys.path.insert(0, _MA14)
from greens_function import green_series, green_dirichlet, causal_green_oscillator  # noqa: E402

__all__ = [
    "HBAR", "MASS",
    # free particle
    "free_propagator", "free_retarded_propagator",
    # harmonic oscillator
    "harmonic_propagator",
    # evolution
    "propagate", "evolve_free_spectral", "gaussian_packet", "packet_center_width",
    # path integral
    "free_propagator_euclidean", "harmonic_propagator_euclidean",
    "path_integral_realtime_free", "path_integral_euclidean",
    "classical_action_free",
    # eigenfunction sum / particle in a box
    "box_eigenfunction", "box_energy", "box_propagator", "box_resolvent_static",
]

HBAR = 1.0    # natural units; restore SI by setting HBAR = 1.054571817e-34
MASS = 1.0    # particle mass m


# ============================================================================
# 1-2.  THE FREE-PARTICLE PROPAGATOR
# ============================================================================

def free_propagator(x, xp, t, m=MASS, hbar=HBAR):
    """Free-particle propagator (kernel)

        K0(x,t; x',0) = sqrt(m / (2 pi i hbar t)) * exp(i m (x-x')^2 / (2 hbar t)).

    This is <x|exp(-i p^2 t / 2 m hbar)|x'>.  `x` may be an array (`xp`, `t`
    scalars), so K0(grid, x', t) returns a column of the kernel.  The complex
    sqrt uses numpy's principal branch: for t>0 the prefactor is
    (1/sqrt(2 pi hbar t/m)) exp(-i pi/4)."""
    x = np.asarray(x, dtype=float)
    pref = np.sqrt(m / (2j * np.pi * hbar * t))
    return pref * np.exp(1j * m * (x - xp) ** 2 / (2.0 * hbar * t))


def free_retarded_propagator(x, xp, t, m=MASS, hbar=HBAR):
    """The RETARDED propagator  G^R = theta(t) K0(x,t;x',0): zero for t<0, the
    free propagator for t>0.  G^R is the causal Green's function of the
    Schrodinger operator (i hbar d/dt - H): (i hbar d_t - H) G^R = i hbar
    delta(x-x') delta(t) -- the theta-function jump supplies delta(t), exactly as
    MA-14's causal_green_oscillator supplies its delta by a jump in y'.  For t>0
    the kernel itself solves the homogeneous free Schrodinger equation
    (verified in the tests)."""
    if t <= 0.0:
        return np.zeros_like(np.asarray(x, dtype=float), dtype=complex) if np.ndim(x) else 0j
    return free_propagator(x, xp, t, m, hbar)


def classical_action_free(x, xp, t, m=MASS):
    """Classical action of the free straight-line path from x' to x in time t,
        S_cl = m (x-x')^2 / (2 t).
    The free propagator is K0 = sqrt(m/2 pi i hbar t) exp(i S_cl / hbar): the
    phase is exactly the classical action.  This is the seed of the stationary-
    phase (hbar->0) limit -- the classical path dominates (bridge B1 to ~CM-17)."""
    return m * (np.asarray(x, dtype=float) - xp) ** 2 / (2.0 * t)


# ============================================================================
# 3.  THE HARMONIC-OSCILLATOR PROPAGATOR  (Mehler's formula)
# ============================================================================

def harmonic_propagator(x, xp, t, omega=1.0, m=MASS, hbar=HBAR):
    """Harmonic-oscillator propagator (Mehler kernel), valid for 0 < omega t < pi:

        K = sqrt(m omega / (2 pi i hbar sin(omega t)))
            * exp{ i m omega / (2 hbar sin(omega t))
                   * [ (x^2 + x'^2) cos(omega t) - 2 x x' ] }.

    Griffiths 3e Problem 6.30(b).  As omega->0 it reduces to the free K0; like K0
    its phase is the classical action of the oscillator path from x' to x."""
    x = np.asarray(x, dtype=float)
    s = np.sin(omega * t)
    c = np.cos(omega * t)
    pref = np.sqrt(m * omega / (2j * np.pi * hbar * s))
    phase = (m * omega / (2.0 * hbar * s)) * ((x ** 2 + xp ** 2) * c - 2.0 * x * xp)
    return pref * np.exp(1j * phase)


# ============================================================================
# 2d.  EVOLUTION:  propagator  vs  direct (spectral) integration of the TDSE
# ============================================================================

def gaussian_packet(x, x0=0.0, p0=0.0, sigma=1.0):
    """Normalised Gaussian wavepacket at t=0,

        Psi(x,0) = (2 pi sigma^2)^{-1/4} exp(-(x-x0)^2/(4 sigma^2) + i p0 x),

    with <x>=x0, mean momentum p0 and position spread sigma (so |Psi|^2 is a
    Gaussian of standard deviation sigma)."""
    x = np.asarray(x, dtype=float)
    norm = (2.0 * np.pi * sigma ** 2) ** (-0.25)
    return norm * np.exp(-(x - x0) ** 2 / (4.0 * sigma ** 2) + 1j * p0 * x)


def propagate(psi0, xs, t, kernel=free_propagator, **kw):
    """Evolve a state on a grid by the propagator integral

        Psi(x,t) = integral K(x,t; x',0) Psi(x',0) dx'   ~   sum_j K_ij psi0_j dx.

    `psi0` is Psi(x',0) sampled on the uniform grid `xs`; returns Psi(x,t) on the
    same grid.  `kernel(x_array, x'_scalar, t, **kw)` is any propagator above.
    (Because a localised packet damps the integrand, this real-space quadrature
    is accurate -- unlike the bare-kernel composition, whose integrand has
    constant modulus.)"""
    xs = np.asarray(xs, dtype=float)
    dx = xs[1] - xs[0]
    psi0 = np.asarray(psi0, dtype=complex)
    # kernel matrix K[i,j] = K(xs[i], xs[j], t) by broadcasting (x down, x' across)
    K = kernel(xs[:, None], xs[None, :], t, **kw)
    return (K @ psi0) * dx


def evolve_free_spectral(psi0, xs, t, hbar=HBAR, m=MASS):
    """Direct integration of the free TDSE by the split-step (here single-step,
    since V=0) Fourier method: in k-space each mode just rotates,

        Psi(k,t) = exp(-i hbar k^2 t / 2 m) Psi(k,0),

    so Psi(x,t) = IFFT[ exp(-i hbar k^2 t/2m) FFT[Psi(x,0)] ].  This is an
    INDEPENDENT, spectral evolution of Schrodinger's equation (no propagator),
    used to cross-check `propagate`.  Exact for the free particle up to the
    periodic-grid wrap-around, so keep the packet away from the box edges."""
    psi0 = np.asarray(psi0, dtype=complex)
    xs = np.asarray(xs, dtype=float)
    N = len(xs)
    dx = xs[1] - xs[0]
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    phase = np.exp(-1j * hbar * k ** 2 * t / (2.0 * m))
    return np.fft.ifft(phase * np.fft.fft(psi0))


def packet_center_width(psi, xs):
    """Return (<x>, sigma_x) of a (not necessarily normalised) state on grid xs:
    <x> = sum x|psi|^2 / sum|psi|^2,  sigma_x = sqrt(<x^2>-<x>^2).  Used to check
    a free Gaussian's centre drifts as x0+p0 t and its width spreads as
    sigma sqrt(1 + (hbar t / 2 m sigma^2)^2)."""
    xs = np.asarray(xs, dtype=float)
    w = np.abs(np.asarray(psi)) ** 2
    Z = np.sum(w)
    xbar = np.sum(xs * w) / Z
    x2 = np.sum(xs ** 2 * w) / Z
    return float(xbar), float(np.sqrt(max(x2 - xbar ** 2, 0.0)))


# ============================================================================
# 4.  THE PATH INTEGRAL
# ============================================================================

def free_propagator_euclidean(x, xp, tau, m=MASS, hbar=HBAR):
    """Imaginary-time (Wick-rotated t=-i tau) free propagator -- the heat kernel

        K0_E(x; x'; tau) = sqrt(m/(2 pi hbar tau)) exp(-m (x-x')^2 / (2 hbar tau)).

    Real and positive; the analytic continuation of K0 (i t -> tau)."""
    x = np.asarray(x, dtype=float)
    pref = np.sqrt(m / (2.0 * np.pi * hbar * tau))
    return pref * np.exp(-m * (x - xp) ** 2 / (2.0 * hbar * tau))


def harmonic_propagator_euclidean(x, xp, tau, omega=1.0, m=MASS, hbar=HBAR):
    """Imaginary-time harmonic propagator (Mehler with sin->sinh, cos->cosh):

        K_E = sqrt(m omega/(2 pi hbar sinh(omega tau)))
              exp{ -m omega/(2 hbar sinh(omega tau))
                   [(x^2+x'^2) cosh(omega tau) - 2 x x'] }.
    """
    x = np.asarray(x, dtype=float)
    sh = np.sinh(omega * tau)
    ch = np.cosh(omega * tau)
    pref = np.sqrt(m * omega / (2.0 * np.pi * hbar * sh))
    return pref * np.exp(-(m * omega / (2.0 * hbar * sh)) * ((x ** 2 + xp ** 2) * ch - 2.0 * x * xp))


def path_integral_realtime_free(x, xp, t, n_slices, R=50.0, n_grid=100000, m=MASS, hbar=HBAR):
    """The LITERAL real-time time-sliced path integral for the free particle:

        K = integral dx_1 ... dx_{N-1}  prod_{k=0}^{N-1} k_eps(x_{k+1}; x_k),
        k_eps(b; a) = sqrt(m/2 pi i hbar eps) exp(i m (b-a)^2 / 2 hbar eps),

    with x_0 = x', x_N = x, eps = t/N.  Implemented for n_slices = 1, 2, 3
    (0, 1, 2 intermediate integrations) by direct quadrature over [-R, R].  Each
    intermediate integral is Gaussian, so the result equals K0(x,t;x') for EVERY
    N -- the sum over paths reconstructs the closed-form propagator.  n_slices=3
    is a 2-D integral (pass a smaller n_grid); it shows the real-time difficulty
    -- the kernel has CONSTANT modulus, so the integrand never damps and finite-R
    truncation limits accuracy.  Higher N needs the Wick-rotated route below."""
    eps = t / n_slices
    k_eps = lambda b, a: free_propagator(b, a, eps, m, hbar)
    if n_slices == 1:
        return complex(k_eps(np.array([x]), xp)[0])
    ys = np.linspace(-R, R, n_grid)
    dy = ys[1] - ys[0]
    if n_slices == 2:
        integ = k_eps(x, ys) * k_eps(ys, xp)           # K(x;y) K(y;x')
        return complex(np.sum(integ) * dy)
    if n_slices == 3:
        Y1, Y2 = np.meshgrid(ys, ys, indexing="ij")
        integ = free_propagator(x, Y2, eps, m, hbar) * \
            free_propagator(Y2, Y1, eps, m, hbar) * \
            free_propagator(Y1, xp, eps, m, hbar)
        return complex(np.sum(integ) * dy * dy)
    raise ValueError("real-time demo implemented for n_slices in {1,2,3}")


def path_integral_euclidean(xs, tau, n_slices, Vfunc, src_index, m=MASS, hbar=HBAR):
    """Trotter (Strang-split) time-sliced path integral in IMAGINARY time:
    approximate exp(-tau H) on the grid `xs` as ( D_{V/2} F D_{V/2} )^N, where
    F[i,j] = dx * sqrt(m/2 pi hbar eps) exp(-m (x_i-x_j)^2 / 2 hbar eps) is the
    free Euclidean short step (eps = tau/N) and D_{V/2} = diag(exp(-eps V/2)).

    Each matrix product is a sum over the intermediate slice positions -- i.e. the
    discretised sum over paths.  Returns the kernel column K_E(x_i; xs[src_index];
    tau) for all grid points i.  As N->inf this converges to the exact Euclidean
    propagator (Trotter error O(eps^2)); the heat kernel damps, so -- unlike real
    time -- the grid sum is numerically stable."""
    xs = np.asarray(xs, dtype=float)
    dx = xs[1] - xs[0]
    eps = tau / n_slices
    diff = xs[:, None] - xs[None, :]
    F = dx * np.sqrt(m / (2.0 * np.pi * hbar * eps)) * np.exp(-m * diff ** 2 / (2.0 * hbar * eps))
    V = np.asarray(Vfunc(xs), dtype=float)
    dhalf = np.exp(-eps * V / 2.0)
    v = np.zeros(len(xs))
    v[src_index] = 1.0
    for _ in range(n_slices):
        v = dhalf * (F @ (dhalf * v))
    return v / dx


# ============================================================================
# 5.  EIGENFUNCTION-SUM PROPAGATOR  &  the ~MA-14 Green's-function link
#     (particle in a box on [0, L], hbar = m = 1)
# ============================================================================

def box_eigenfunction(n, x, L=1.0):
    """Infinite-square-well eigenfunction on [0,L]:  psi_n(x)=sqrt(2/L) sin(n pi x/L).
    (Griffiths 3e Sec. 2.2.)"""
    return np.sqrt(2.0 / L) * np.sin(n * np.pi * np.asarray(x, dtype=float) / L)


def box_energy(n, L=1.0, m=MASS, hbar=HBAR):
    """Infinite-square-well energy  E_n = n^2 pi^2 hbar^2 / (2 m L^2)."""
    return (n ** 2) * (np.pi ** 2) * (hbar ** 2) / (2.0 * m * L ** 2)


def box_propagator(x, xp, t, nmax, L=1.0, m=MASS, hbar=HBAR):
    """Eigenfunction-sum (spectral) propagator for the box,

        K(x,t; x',0) = sum_{n=1}^{nmax} psi_n(x) psi_n(x') exp(-i E_n t / hbar)

    (Griffiths 3e Eq. 6.79, p.342).  At t=0 it is the completeness sum -> delta;
    applied to an eigenstate psi_m it returns exp(-i E_m t/hbar) psi_m."""
    return sum(box_eigenfunction(n, x, L) * box_eigenfunction(n, xp, L)
               * np.exp(-1j * box_energy(n, L, m, hbar) * t / hbar)
               for n in range(1, nmax + 1))


def box_resolvent_static(x, xp, nmax, L=1.0, m=MASS, hbar=HBAR):
    """The static (E->0) resolvent of the box Hamiltonian -- the Green's function
    of H itself,

        G_H(x,x') = sum_{n=1}^{nmax} psi_n(x) psi_n(x') / E_n  =  <x|H^{-1}|x'>.

    This is the propagator's eigen-sum with exp(-iE_n t) replaced by 1/E_n; it is
    (up to a constant) the time integral of K.  For L=1, H=-(1/2) d^2/dx^2, so
    H = L_op/2 with L_op=-d^2/dx^2 (MA-14's operator) and G_H = 2 * G_{MA-14}.
    The tests import MA-14 and verify G_H = 2 * green_series -> 2 * green_dirichlet."""
    return sum(box_eigenfunction(n, x, L) * box_eigenfunction(n, xp, L)
               / box_energy(n, L, m, hbar)
               for n in range(1, nmax + 1))


# ============================================================================
# demo
# ============================================================================

def _demo():
    print("QM-19  Propagators & path integrals  (natural units hbar = m = 1)")
    print("=" * 66)

    # 1. free propagator: phase = classical action, modulus = 1/sqrt(2 pi t)
    x, xp, t = 1.0, -0.5, 0.8
    K = complex(free_propagator(np.array([x]), xp, t)[0])
    print("\nFree K0(x=1, x'=-0.5, t=0.8):")
    print("   value         = %+.5f %+.5fi" % (K.real, K.imag))
    print("   |K0|          = %.5f   (= 1/sqrt(2 pi t) = %.5f)"
          % (abs(K), 1.0 / np.sqrt(2 * np.pi * t)))
    print("   arg K0 + pi/4 = %.5f   (= S_cl/hbar = %.5f; the prefactor adds -pi/4)"
          % (np.angle(K) + np.pi / 4, classical_action_free(x, xp, t)))

    # 2. composition / semigroup, by the 2-slice real-time path integral
    K2 = path_integral_realtime_free(x, xp, t, n_slices=2)
    print("\nReal-time path integral (1 intermediate point) vs closed form:")
    print("   N=2 sum-over-paths = %+.5f %+.5fi" % (K2.real, K2.imag))
    print("   K0(x,x',t)         = %+.5f %+.5fi" % (K.real, K.imag))

    # 3. Wick-rotated Trotter convergence to the closed form (harmonic)
    print("\nImaginary-time Trotter path integral -> harmonic propagator (tau=1):")
    xs = np.linspace(-6, 6, 601)
    i, j = 350, 250            # x = +1.0, x' = -1.0
    exact = harmonic_propagator_euclidean(xs[i], xs[j], 1.0, omega=1.0)
    for N in (1, 2, 8, 32):
        Kc = path_integral_euclidean(xs, 1.0, N, lambda z: 0.5 * z ** 2, j)[i]
        print("   N=%3d:  |K_path - K_exact| = %.2e" % (N, abs(Kc - exact)))

    # 4. eigen-sum propagator (box) and the MA-14 Green's-function link
    print("\nParticle in a box: eigen-sum propagator carries an eigenstate by a phase:")
    Lx = np.linspace(0, 1, 401)
    psi1 = box_eigenfunction(1, Lx)
    out = np.sum(box_propagator(0.3, Lx, 0.5, nmax=40) * psi1) * (Lx[1] - Lx[0])
    exact = np.exp(-1j * box_energy(1) * 0.5) * box_eigenfunction(1, 0.3)
    print("   integral K(0.3,x',0.5) psi_1(x') dx' = %+.4f %+.4fi" % (out.real, out.imag))
    print("   exp(-i E_1 * 0.5) psi_1(0.3)         = %+.4f %+.4fi" % (exact.real, exact.imag))
    xx, xpp = 0.3, 0.7
    print("\nStatic box resolvent  sum psi_n psi_n/E_n  vs  2 x MA-14 Green's function:")
    print("   sum_{n<=2000} = %.6f" % box_resolvent_static(xx, xpp, 2000))
    print("   2*green_series(2000) = %.6f   2*green_dirichlet = %.6f"
          % (2 * green_series(xx, xpp, 2000), 2 * green_dirichlet(xx, xpp)))

    # retarded structure: G^R = theta(t) K, like MA-14's causal Green's function
    print("\nRetarded structure (theta-function causality), cf. MA-14 causal_green_oscillator:")
    print("   free_retarded_propagator(t=-0.3) = %s  (zero before the source)"
          % np.array2string(np.atleast_1d(free_retarded_propagator(np.array([0.5]), 0.0, -0.3))))
    print("   MA-14 causal_green_oscillator(t=0.3,tau=1.0) = %.4f  (also zero before tau)"
          % causal_green_oscillator(0.3, 1.0, 2.0))


if __name__ == "__main__":
    _demo()
