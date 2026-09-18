"""QM-04  Probability current & the continuity equation.

Physics topic network, module QM-04 (modules/topic_network.txt) -- KEY BRIDGE B2.
Source: Griffiths, *Introduction to Quantum Mechanics* Sect. 1.5 (the continuity
equation); Sakurai, *Modern QM* Sect. 2.4 (probability flux).  Builds on ~QM-02
(rho = |psi|^2, normalization) and ~QM-03 (the Schrodinger equation supplies the
time derivative).

From the time-dependent Schrodinger equation one finds a LOCAL conservation law

    d rho / dt + div j = 0 ,    rho = |psi|^2 ,
    j = (hbar/m) Im(psi* grad psi) = (i hbar / 2m)(psi grad psi* - psi* grad psi),

the *same* continuity equation as mass (~CM-22, j = rho v) and charge
(~EM-14, div J).  Two signatures:
  * a travelling wave e^{ikx} carries j = rho * (hbar k / m) = rho v   (flow = fluid);
  * a real (standing) stationary state has j = 0 everywhere (no net flow).

Working in natural units hbar = m = 1 by default, so j has the clean reading
"probability flows at the de Broglie velocity v = k".
"""

import numpy as np

__all__ = [
    "prob_density", "prob_current", "total_probability", "mean_velocity",
    "plane_wave", "gaussian_packet", "free_step", "continuity_residual",
]


# --- the two local quantities ------------------------------------------------

def prob_density(psi):
    """Born probability density  rho = |psi|^2  (~QM-02)."""
    return np.abs(psi) ** 2


def prob_current(psi, dx, hbar=1.0, m=1.0):
    """Probability current  j = (hbar/m) Im(psi* d psi/dx), by central differences.

    Equivalent to (i hbar / 2m)(psi d psi*/dx - psi* d psi/dx).  Real-valued."""
    grad = np.gradient(psi, dx)
    return (hbar / m) * np.imag(np.conj(psi) * grad)


def total_probability(psi, dx):
    """Global probability  integral |psi|^2 dx  (should be conserved in time)."""
    return float(np.trapezoid(prob_density(psi), dx=dx))


def mean_velocity(psi, dx, hbar=1.0, m=1.0):
    """Probability-weighted mean velocity  <v> = (integral j dx)/(integral rho dx).
    For a free packet this is the group velocity (Ehrenfest, ~QM-07)."""
    num = np.trapezoid(prob_current(psi, dx, hbar, m), dx=dx)
    den = np.trapezoid(prob_density(psi), dx=dx)
    return float(num / den)


# --- model states ------------------------------------------------------------

def plane_wave(x, k, amp=1.0):
    """Travelling de Broglie wave  psi = amp * e^{ikx}  (momentum eigenstate)."""
    return amp * np.exp(1j * k * x)


def gaussian_packet(x, x0=0.0, k0=0.0, sigma=1.0):
    """Normalized minimum-uncertainty wavepacket centred at x0, mean wavenumber k0:
        psi = (2 pi sigma^2)^{-1/4} e^{i k0 x} e^{-(x-x0)^2 / 4 sigma^2}."""
    norm = (2.0 * np.pi * sigma ** 2) ** -0.25
    return norm * np.exp(1j * k0 * x) * np.exp(-((x - x0) ** 2) / (4.0 * sigma ** 2))


# --- exact free-particle time step (spectral) --------------------------------

def free_step(psi, dx, dt, hbar=1.0, m=1.0):
    """One exact free-particle (V = 0) time step via the spectral propagator
        psi(t+dt) = F^{-1} [ exp(-i hbar k^2 dt / 2m) F[psi] ].
    Free evolution is diagonal in k, so this is exact up to the grid's k-cutoff."""
    n = psi.shape[0]
    k = 2.0 * np.pi * np.fft.fftfreq(n, d=dx)
    psi_k = np.fft.fft(psi)
    psi_k = psi_k * np.exp(-1j * hbar * k ** 2 * dt / (2.0 * m))
    return np.fft.ifft(psi_k)


# --- the continuity equation itself ------------------------------------------

def continuity_residual(psi0, psi1, dx, dt, hbar=1.0, m=1.0):
    """Finite-difference residual of  d rho/dt + d j/dx  across one time step.

    Mirrors ~CM-22's `continuity_residual` (same law, different density).  Uses a
    centred time difference for d rho/dt and the midpoint of div j at the two end
    states; returns the residual ARRAY (which should be ~0 wherever the state is
    resolved)."""
    rho0, rho1 = prob_density(psi0), prob_density(psi1)
    drho_dt = (rho1 - rho0) / dt
    j0 = prob_current(psi0, dx, hbar, m)
    j1 = prob_current(psi1, dx, hbar, m)
    div_j = 0.5 * (np.gradient(j0, dx) + np.gradient(j1, dx))
    return drho_dt + div_j


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-04  Probability current & continuity -- demo  (hbar = m = 1)")
    print("=" * 62)

    L, n = 80.0, 2048
    x = np.linspace(-L / 2, L / 2, n, endpoint=False)
    dx = x[1] - x[0]

    # 1) travelling wave: j = rho * v, with v = k
    k = 1.5
    psi = plane_wave(x, k, amp=1.0)
    j = prob_current(psi, dx)
    rho = prob_density(psi)
    print("\n1) plane wave e^{ikx}, k = %.2f :" % k)
    print("   rho = |A|^2 = %.3f (uniform);  j = %.4f;  j/rho = %.4f = v = k"
          % (rho.mean(), j.mean(), j.mean() / rho.mean()))

    # 2) real standing state: j = 0 (no net flow)
    psi_real = np.cos(k * x).astype(complex)
    j_real = prob_current(psi_real, dx)
    print("\n2) real standing wave cos(kx):")
    print("   max|j| = %.2e  ->  no net probability flow (j = 0)" % np.max(np.abs(j_real)))

    # 3) free Gaussian wavepacket: continuity holds, normalization conserved
    sigma, k0, x0 = 2.0, 2.0, -10.0
    psi0 = gaussian_packet(x, x0=x0, k0=k0, sigma=sigma)
    dt = 2e-3
    psi1 = free_step(psi0, dx, dt)
    res = continuity_residual(psi0, psi1, dx, dt)
    drho_dt = (prob_density(psi1) - prob_density(psi0)) / dt
    print("\n3) free Gaussian packet (sigma=%.0f, k0=%.0f), one dt = %.0e step:" % (sigma, k0, dt))
    print("   max|d rho/dt|      = %.3e" % np.max(np.abs(drho_dt)))
    print("   max|d rho/dt+dj/dx| = %.3e   (residual << the term -> continuity holds)"
          % np.max(np.abs(res)))
    print("   total prob: t=0 -> %.6f ,  t=dt -> %.6f  (conserved)"
          % (total_probability(psi0, dx), total_probability(psi1, dx)))
    print("   <v> = integral j / integral rho = %.4f  = group velocity k0 = %.1f"
          % (mean_velocity(psi0, dx), k0))


if __name__ == "__main__":
    _demo()
