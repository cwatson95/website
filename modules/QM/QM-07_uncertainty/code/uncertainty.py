"""
QM-07  Uncertainty principle & Ehrenfest's theorem  --  the two faces of the
position-momentum trade-off, computed and verified numerically.

Part of the physics topic network (see modules/topic_network.txt, module QM-07).
Prereqs: ~QM-05 (commutators -- they are the right-hand side of the bound) and
~MA-09 (Fourier: x and p are conjugate variables linked by the transform).
Feeds into ~QM-09 (the SHO ground state IS the minimum-uncertainty packet) and,
classically, into ~CM-19 (Hamilton's equations -- what Ehrenfest reduces to).

Three results, three function groups below:

  1. Position-momentum uncertainty   sigma_x sigma_p >= hbar/2.
     States live on a 1-D grid; p-hat = -i hbar d/dx is applied SPECTRALLY (FFT).
     A Gaussian SATURATES the bound (= hbar/2); everything else exceeds it.

  2. Generalized relation            sigma_A sigma_B >= (1/2)|<[A,B]>|
     for Hermitian A, B (Griffiths 3e Sec.3.5.1).  Verified on finite matrices:
     for spin-1/2, sigma_{Sx} sigma_{Sy} >= (1/2)|<[Sx,Sy]>| = (hbar/2)|<Sz>|.

  3. Ehrenfest's theorem             d<x>/dt = <p>/m,   d<p>/dt = -<V'(x)>
     (Griffiths 3e Sec.1.5).  A wave packet is time-evolved by the split-step
     Fourier method in free space and in a harmonic well; the two rates are
     checked against the recorded expectation values, and the harmonic <x>(t) is
     shown to trace the CLASSICAL oscillation x0 cos(wt) + (p0/mw) sin(wt).

UNITS.  Natural units  hbar = m = 1  throughout (documented at each formula).
In these units the bound is sigma_x sigma_p >= 1/2, momentum p = wavenumber k,
the kinetic operator is k^2/2, and spin operators are S = sigma_Pauli / 2.

Implementation: numpy only.  The momentum operator and the kinetic propagator
both use the FFT, so on a well-resolved grid every continuous result is
spectrally accurate and is checked against a closed form in test_uncertainty.py.
"""

import math
import numpy as np

__all__ = [
    "HBAR", "M",
    # grids & states
    "grid", "normalize", "gaussian_packet", "ho_eigenstate",
    # position-momentum statistics
    "apply_p", "apply_p2", "mean_x", "mean_p", "sigma_x", "sigma_p",
    "uncertainty_product",
    # finite-dimensional / spin
    "PAULI_X", "PAULI_Y", "PAULI_Z", "spin_ops",
    "expval", "variance", "std", "commutator", "generalized_bound",
    # dynamics
    "split_step_evolve", "classical_sho",
]

HBAR = 1.0     # natural units
M = 1.0        # particle mass (natural units)


# --- grids & states ----------------------------------------------------------

def grid(L, N):
    """A periodic 1-D position grid on (-L/2, L/2].

    Returns (x, dx) with N points and spacing dx = L/N.  endpoint=False keeps the
    grid consistent with the discrete Fourier transform (no duplicated endpoint),
    which is what makes the spectral derivative below exact for smooth, decaying
    states.
    """
    x = np.linspace(-L / 2.0, L / 2.0, N, endpoint=False)
    return x, L / N


def normalize(psi, dx):
    """Return psi scaled so that integral |psi|^2 dx = 1 (trapezoid == sum here,
    the grid being periodic)."""
    nrm = math.sqrt(np.sum(np.abs(psi) ** 2) * dx)
    return psi / nrm


def gaussian_packet(x, x0=0.0, sigma=1.0, p0=0.0):
    """Minimum-uncertainty Gaussian wave packet (hbar = 1):

        psi(x) = (2 pi sigma^2)^{-1/4} exp(-(x-x0)^2 / (4 sigma^2)) exp(i p0 x)

    It is normalized and has <x> = x0, <p> = p0, sigma_x = sigma,
    sigma_p = hbar/(2 sigma); hence sigma_x sigma_p = hbar/2 exactly -- it
    SATURATES the uncertainty bound (Griffiths 3e Sec.3.5.2).  This is the same
    object that appears in ~QM-09 as the harmonic-oscillator ground state.
    """
    amp = (2.0 * math.pi * sigma ** 2) ** (-0.25)
    return amp * np.exp(-(x - x0) ** 2 / (4.0 * sigma ** 2)) * np.exp(1j * p0 * x / HBAR)


def _hermite_phys(n, x):
    """Physicists' Hermite polynomial H_n(x) by the recursion
    H_{n+1} = 2x H_n - 2n H_{n-1}."""
    if n == 0:
        return np.ones_like(x)
    Hm1, Hm = np.ones_like(x), 2.0 * x
    for m in range(1, n):
        Hm1, Hm = Hm, 2.0 * x * Hm - 2.0 * m * Hm1
    return Hm


def ho_eigenstate(x, n):
    """The n-th harmonic-oscillator eigenstate for hbar = m = omega = 1:

        psi_n(x) = (2^n n! sqrt(pi))^{-1/2} H_n(x) exp(-x^2/2).

    For these states <x> = <p> = 0 and sigma_x = sigma_p = sqrt(n + 1/2), so
    sigma_x sigma_p = n + 1/2: the ground state (n=0) saturates hbar/2, every
    excited state exceeds it.  Cross-link to ~QM-09 (built there from scratch).
    """
    coeff = 1.0 / math.sqrt(2.0 ** n * math.factorial(n) * math.sqrt(math.pi))
    return coeff * _hermite_phys(n, x) * np.exp(-x ** 2 / 2.0)


# --- position-momentum statistics -------------------------------------------

def _kgrid(N, dx):
    """Angular-wavenumber grid matching numpy's FFT layout."""
    return 2.0 * math.pi * np.fft.fftfreq(N, d=dx)


def apply_p(psi, dx):
    """Apply the momentum operator p-hat = -i hbar d/dx, evaluated spectrally.

    Because  d/dx = IFFT(i k FFT(.))  and  p-hat = -i hbar d/dx, with hbar = 1
    this collapses to  p-hat psi = IFFT(k FFT(psi))  (the two i's cancel).  For
    a plane wave exp(i k0 x) it returns hbar k0 times the wave, as it must.
    """
    N = psi.size
    k = _kgrid(N, dx)
    return HBAR * np.fft.ifft(k * np.fft.fft(psi))


def apply_p2(psi, dx):
    """Apply p-hat^2 = -hbar^2 d^2/dx^2 spectrally: IFFT((hbar k)^2 FFT(psi))."""
    N = psi.size
    k = _kgrid(N, dx)
    return np.fft.ifft((HBAR * k) ** 2 * np.fft.fft(psi))


def mean_x(psi, x, dx):
    """<x> = integral x |psi|^2 dx."""
    p = normalize(psi, dx)
    return float(np.sum(x * np.abs(p) ** 2) * dx)


def mean_p(psi, dx):
    """<p> = integral psi* (p-hat psi) dx  (real for any normalizable state)."""
    p = normalize(psi, dx)
    return float(np.real(np.sum(np.conj(p) * apply_p(p, dx)) * dx))


def sigma_x(psi, x, dx):
    """Position standard deviation sigma_x = sqrt(<x^2> - <x>^2)."""
    p = normalize(psi, dx)
    rho = np.abs(p) ** 2
    m1 = np.sum(x * rho) * dx
    m2 = np.sum(x ** 2 * rho) * dx
    return math.sqrt(max(float(m2 - m1 ** 2), 0.0))


def sigma_p(psi, dx):
    """Momentum standard deviation sigma_p = sqrt(<p^2> - <p>^2), p-hat spectral."""
    p = normalize(psi, dx)
    m1 = np.real(np.sum(np.conj(p) * apply_p(p, dx)) * dx)
    m2 = np.real(np.sum(np.conj(p) * apply_p2(p, dx)) * dx)
    return math.sqrt(max(float(m2 - m1 ** 2), 0.0))


def uncertainty_product(psi, x, dx):
    """The product sigma_x sigma_p; it is >= hbar/2 for every state (= for a
    Gaussian)."""
    return sigma_x(psi, x, dx) * sigma_p(psi, dx)


# --- finite-dimensional (spin) uncertainty ----------------------------------

PAULI_X = np.array([[0, 1], [1, 0]], dtype=complex)
PAULI_Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
PAULI_Z = np.array([[1, 0], [0, -1]], dtype=complex)


def spin_ops():
    """Spin-1/2 operators (hbar = 1): S_i = sigma_i / 2.  They obey
    [Sx, Sy] = i hbar Sz, so the generalized bound for Sx, Sy is
    (1/2)|<[Sx,Sy]>| = (hbar/2)|<Sz>|."""
    return HBAR * PAULI_X / 2.0, HBAR * PAULI_Y / 2.0, HBAR * PAULI_Z / 2.0


def _ket(psi):
    """Column state vector, L2-normalized."""
    v = np.asarray(psi, dtype=complex).reshape(-1)
    return v / math.sqrt(float(np.real(np.vdot(v, v))))


def expval(A, psi):
    """Expectation value <psi|A|psi> for a (not necessarily normalized) state."""
    v = _ket(psi)
    return complex(np.vdot(v, A @ v))


def variance(A, psi):
    """Var(A) = <A^2> - <A>^2.  Real and >= 0 for a Hermitian A."""
    v = _ket(psi)
    a = np.vdot(v, A @ v)
    a2 = np.vdot(v, A @ (A @ v))
    return float(np.real(a2 - a * a))


def std(A, psi):
    """Standard deviation sigma_A = sqrt(Var(A))."""
    return math.sqrt(max(variance(A, psi), 0.0))


def commutator(A, B):
    """The commutator [A, B] = AB - BA (the RHS of the bound; see ~QM-05)."""
    return A @ B - B @ A


def generalized_bound(A, B, psi):
    """The Robertson bound (1/2)|<[A,B]>| that sigma_A sigma_B must not fall
    below (Griffiths 3e Sec.3.5.1, the generalized uncertainty principle)."""
    return 0.5 * abs(expval(commutator(A, B), psi))


# --- the Schwarz inequality (the lemma the bound stands on) -------------------

def inner(f, g, dx=None):
    """The inner product <f|g>.  Pass dx for grid wavefunctions (the Riemann
    weight of Griffiths 3e Eq. 3.6); omit it for finite kets (spin states)."""
    v = complex(np.vdot(np.asarray(f, dtype=complex).reshape(-1),
                        np.asarray(g, dtype=complex).reshape(-1)))
    return v * dx if dx is not None else v


def schwarz_gap(f, g, dx=None):
    """<f|f><g|g> - |<f|g>|^2, the slack in the Schwarz inequality (Griffiths 3e
    Eq. 3.7 / Eq. A.27): >= 0 for every pair of states, and = 0 iff g = c f."""
    ff = inner(f, f, dx).real
    gg = inner(g, g, dx).real
    fg = inner(f, g, dx)
    return ff * gg - abs(fg) ** 2


def schwarz_residual_identity(f, g, dx=None):
    """The single identity that PROVES the Schwarz inequality (Problem A.5's
    hint, notes Sec.2.1): subtract from g its projection along f,

        h = g - (<f|g>/<f|f>) f    (so <f|h> = 0),

    and expanding <h|h> >= 0 gives exactly

        <f|f><g|g> - |<f|g>|^2  =  <f|f><h|h>  >=  0.

    Returns (gap, <f|f><h|h>, <f|h>): the first two agree to round-off and the
    third vanishes -- the whole derivation, in numbers."""
    f = np.asarray(f, dtype=complex).reshape(-1)
    g = np.asarray(g, dtype=complex).reshape(-1)
    ff = inner(f, f, dx).real
    h = g - (inner(f, g, dx) / ff) * f
    return schwarz_gap(f, g, dx), ff * inner(h, h, dx).real, inner(f, h, dx)


# --- Ehrenfest dynamics: split-step Fourier ----------------------------------

def split_step_evolve(psi0, x, V, dt, nsteps, dVdx=None):
    """Evolve psi under i hbar d/dt psi = [p^2/2m + V(x)] psi by the symmetric
    (Strang) split-step Fourier method, recording the Ehrenfest observables.

    One step is the unitary  exp(-iV dt/2hbar) exp(-i T dt/hbar) exp(-iV dt/2hbar)
    with kinetic T = p^2/2m applied as a diagonal multiply in Fourier space.  It
    is norm-conserving and second-order accurate in dt.

    Parameters
    ----------
    psi0   : initial state on the grid x (auto-normalized).
    x      : position grid (from grid()).
    V      : potential, a callable V(x) or a precomputed array on x.
    dt     : time step.
    nsteps : number of steps.
    dVdx   : optional derivative V'(x) (callable or array) so the mean force
             <-V'(x)> can be recorded; defaults to 0 (free particle).

    Returns
    -------
    t   : (nsteps+1,) times.
    xs  : (nsteps+1,) <x>(t).
    ps  : (nsteps+1,) <p>(t).
    Fs  : (nsteps+1,) <-V'(x)>(t)  (the mean force, = d<p>/dt by Ehrenfest).
    psi : final state.
    """
    N = x.size
    dx = x[1] - x[0]
    k = _kgrid(N, dx)

    Varr = V(x) if callable(V) else np.asarray(V, dtype=float)
    if dVdx is None:
        Fx = np.zeros_like(x)
    else:
        Fx = -(dVdx(x) if callable(dVdx) else np.asarray(dVdx, dtype=float))

    expV = np.exp(-0.5j * Varr * dt / HBAR)               # half potential step
    expT = np.exp(-0.5j * HBAR * (k ** 2) * dt / M)       # full kinetic step (T=p^2/2m)

    psi = normalize(np.asarray(psi0, dtype=complex).copy(), dx)

    t = np.empty(nsteps + 1)
    xs = np.empty(nsteps + 1)
    ps = np.empty(nsteps + 1)
    Fs = np.empty(nsteps + 1)

    def record(i, tt):
        rho = np.abs(psi) ** 2
        t[i] = tt
        xs[i] = np.sum(x * rho) * dx
        ps[i] = np.real(np.sum(np.conj(psi) * apply_p(psi, dx)) * dx)
        Fs[i] = np.sum(Fx * rho) * dx

    record(0, 0.0)
    for n in range(nsteps):
        psi = expV * psi
        psi = np.fft.ifft(expT * np.fft.fft(psi))
        psi = expV * psi
        record(n + 1, (n + 1) * dt)
    return t, xs, ps, Fs, psi


def classical_sho(t, x0, p0, omega):
    """Classical harmonic trajectory x(t) = x0 cos(wt) + (p0/(m w)) sin(wt).
    For the harmonic potential Ehrenfest is EXACT (V' is linear, so
    <V'(x)> = V'(<x>)), and the packet centre follows this curve."""
    return x0 * np.cos(omega * t) + (p0 / (M * omega)) * np.sin(omega * t)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-07  Uncertainty principle & Ehrenfest's theorem  (hbar = m = 1)\n")

    x, dx = grid(L=40.0, N=2048)

    print("1. Position-momentum  sigma_x sigma_p >= hbar/2 = 0.5")
    g = gaussian_packet(x, x0=0.0, sigma=1.3, p0=0.7)
    print("   Gaussian (sigma=1.3): sigma_x=%.4f  sigma_p=%.4f  product=%.6f  (saturates)"
          % (sigma_x(g, x, dx), sigma_p(g, dx), uncertainty_product(g, x, dx)))
    for n in (0, 1, 2, 3):
        psi = ho_eigenstate(x, n)
        print("   HO eigenstate n=%d : product=%.6f   (analytic n+1/2 = %.1f)"
              % (n, uncertainty_product(psi, x, dx), n + 0.5))

    print("\n2. Generalized bound  sigma_A sigma_B >= (1/2)|<[A,B]>|   (spin-1/2)")
    Sx, Sy, Sz = spin_ops()
    print("   [Sx,Sy] = i Sz ?  ", np.allclose(commutator(Sx, Sy), 1j * Sz))
    up = [1.0, 0.0]                                   # spin up along z
    print("   state |up_z>: sigma_Sx sigma_Sy = %.4f,  bound (hbar/2)|<Sz>| = %.4f  (saturates)"
          % (std(Sx, up) * std(Sy, up), generalized_bound(Sx, Sy, up)))
    tilt = [math.cos(0.6), math.sin(0.6)]            # a tilted state
    print("   tilted state: sigma_Sx sigma_Sy = %.4f >= bound %.4f"
          % (std(Sx, tilt) * std(Sy, tilt), generalized_bound(Sx, Sy, tilt)))

    print("\n3. Ehrenfest  d<x>/dt = <p>/m,  d<p>/dt = -<V'(x)>")
    xf, dxf = grid(L=120.0, N=2048)
    free = gaussian_packet(xf, x0=0.0, sigma=2.0, p0=1.5)
    t, xs, ps, Fs, _ = split_step_evolve(free, xf, V=0.0, dt=0.02, nsteps=100)
    dxdt = np.gradient(xs, t)
    print("   free particle: d<x>/dt = %.4f,  <p>/m = %.4f  (constant momentum)"
          % (dxdt[50], ps[50] / M))

    xo, dxo = grid(L=40.0, N=1024)
    omega, x0, p0 = 1.0, 3.0, 0.0
    pkt = gaussian_packet(xo, x0=x0, sigma=1.0, p0=p0)
    V = 0.5 * M * omega ** 2 * xo ** 2
    t, xs, ps, Fs, _ = split_step_evolve(pkt, xo, V=V, dt=0.01,
                                         nsteps=int(2 * math.pi / 0.01),
                                         dVdx=lambda xx: M * omega ** 2 * xx)
    xcl = classical_sho(t, x0, p0, omega)
    print("   SHO (one period): max |<x>(t) - classical| = %.2e  (centre follows x0 cos wt)"
          % np.max(np.abs(xs - xcl)))
    dpdt = np.gradient(ps, t)
    j = len(t) // 4
    print("   at t=T/4: d<p>/dt = %.4f,  -<V'(x)> = %.4f" % (dpdt[j], Fs[j]))


if __name__ == "__main__":
    _demo()
