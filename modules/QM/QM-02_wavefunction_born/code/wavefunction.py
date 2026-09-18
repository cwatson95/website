"""
QM-02  The wavefunction and Born's rule  --  |Psi|^2 as a probability density,
normalization, expectation values, and the move to momentum space, as composable
operations on a 1-D grid that you can evaluate and cross-check against closed forms.

Part of the physics topic network (see modules/topic_network.txt, module QM-02).
Follows ~QM-01 (the de Broglie matter wave is promoted here to the wavefunction
Psi whose squared modulus is a probability density) and feeds ~QM-03 (the
Schrodinger equation governs Psi), ~QM-04 (probability current / continuity) and
~QM-06 (Born -> measurement).  The momentum-space machinery is the Fourier
transform of ~MA-09; the probability theory is ~MA-19.

Born's statistical interpretation (Griffiths 3e Sec.1.2, printed p.17):
    rho(x,t) = |Psi(x,t)|^2  is the probability *density* for finding the
    particle at x.  The probability of finding it in [a,b] is the integral of rho
    (Sec.1.3.2, p.26), the whole-line integral must be 1 (Sec.1.4 normalization,
    p.29), and expectation values are "operator sandwiches" int Psi* Q Psi dx
    (Sec.1.5, pp.32-33) with x -> x and p -> -i hbar d/dx.

Everything below works on a uniform (or non-uniform) numpy grid x and a complex
array psi sampled on it.  Integrals use the trapezoid rule; the momentum operator
is applied either by finite difference (-i hbar d/dx) or by FFT (multiply by hbar*k
in momentum space).  The tests in test_wavefunction.py validate every routine
against the analytic Gaussian wavepacket, whose moments are known in closed form.

Conventions:  hbar defaults to 1 (natural units) but is a keyword everywhere, so
<p> = hbar*k0 etc. hold for any value you pass.
"""

import numpy as np

__all__ = [
    # integration / probability
    "prob_density", "total_probability", "normalize", "prob_between",
    # position moments
    "expectation_x", "expectation_x2", "sigma_x",
    # momentum moments (finite difference)
    "expectation_p", "expectation_p2", "sigma_p",
    # analytic states & momentum space
    "gaussian_packet", "momentum_space", "expectation_p_fft", "free_propagate",
]


# --- trapezoid integration (complex-aware, numpy-version-proof) ---------------

def _trapz(y, x):
    """Trapezoid integral of (possibly complex) samples y on grid x.

    Hand-rolled rather than np.trapz/np.trapezoid so the module is immune to the
    numpy 2.0 rename and so it transparently handles complex integrands."""
    y = np.asarray(y)
    x = np.asarray(x, dtype=float)
    return np.sum(0.5 * (y[1:] + y[:-1]) * np.diff(x))


# --- 1. Born density and probabilities ---------------------------------------

def prob_density(psi):
    """Born probability density  rho(x) = |Psi(x)|^2  (real, >= 0).

    This is the whole content of Born's statistical interpretation: the modulus
    squared of the wavefunction is the probability *density* over position
    (Griffiths 3e Sec.1.2, p.17; Sec.1.3.2, p.26)."""
    return np.abs(np.asarray(psi)) ** 2


def total_probability(psi, x):
    """Total probability  int |Psi|^2 dx  over the whole grid.

    For a physically realizable (normalized) state this is 1; the Schrodinger
    equation keeps it 1 for all time (Griffiths 3e Sec.1.4, p.30)."""
    return _trapz(prob_density(psi), x).real


def normalize(psi, x):
    """Return Psi rescaled so that  int |Psi|^2 dx = 1  on the grid x.

    Multiplies by 1/sqrt(int|Psi|^2 dx).  Square-integrable ( int|Psi|^2 finite,
    Psi -> 0 at the ends ) is required -- non-normalizable solutions cannot
    represent particles (Griffiths 3e Sec.1.4, p.29)."""
    N2 = total_probability(psi, x)
    if N2 <= 0.0:
        raise ValueError("cannot normalize: int|psi|^2 dx is not positive")
    return np.asarray(psi) / np.sqrt(N2)


def prob_between(psi, x, a, b):
    """Born probability of finding the particle in [a, b]:  int_a^b |Psi|^2 dx.

    Griffiths 3e Eq.1.16 (Sec.1.3.2, p.26): probability is the area under the
    |Psi|^2 graph between the limits.  Integrated over the grid points lying in
    [a, b]."""
    if a > b:
        a, b = b, a
    x = np.asarray(x, dtype=float)
    rho = prob_density(psi)
    mask = (x >= a) & (x <= b)
    if mask.sum() < 2:
        return 0.0
    return _trapz(rho[mask], x[mask]).real


# --- 2. position expectation values & spread ---------------------------------

def expectation_x(psi, x):
    """<x> = int x |Psi|^2 dx   (Griffiths 3e Eq.1.28, Sec.1.5, p.32).

    The ensemble average of position measurements on identically-prepared
    systems -- NOT repeated measurements on one system (which collapse the state)."""
    x = np.asarray(x, dtype=float)
    return _trapz(x * prob_density(psi), x).real


def expectation_x2(psi, x):
    """<x^2> = int x^2 |Psi|^2 dx  (the second moment of the Born density)."""
    x = np.asarray(x, dtype=float)
    return _trapz(x ** 2 * prob_density(psi), x).real


def sigma_x(psi, x):
    """Position standard deviation  sigma_x = sqrt(<x^2> - <x>^2).

    The 'useful little theorem' on variances, Griffiths 3e Eq.1.12 (Sec.1.3.1,
    p.24): variance = <x^2> - <x>^2; sigma is its square root, the spread in x.
    A tiny negative argument from round-off is clamped to 0."""
    var = expectation_x2(psi, x) - expectation_x(psi, x) ** 2
    return np.sqrt(var) if var > 0.0 else 0.0


# --- 3. momentum expectation values (operator -i hbar d/dx) -------------------

def expectation_p(psi, x, hbar=1.0):
    """<p> = int Psi* (-i hbar dPsi/dx) dx   (Griffiths 3e Eq.1.33, p.33).

    The momentum operator is p_hat = -i hbar d/dx; the expectation value is the
    'sandwich' Psi* p_hat Psi integrated over x.  dPsi/dx is a 2nd-order central
    finite difference (numpy.gradient); the imaginary part vanishes for a genuine
    state, so we return the real part."""
    psi = np.asarray(psi, dtype=complex)
    x = np.asarray(x, dtype=float)
    dpsi = np.gradient(psi, x)
    integrand = np.conj(psi) * (-1j * hbar) * dpsi
    return _trapz(integrand, x).real


def expectation_p2(psi, x, hbar=1.0):
    """<p^2> = int Psi* (-hbar^2 d^2/dx^2) Psi dx = hbar^2 int |dPsi/dx|^2 dx.

    The second form (integration by parts, boundary terms killed by Psi -> 0)
    needs only the first derivative and is manifestly real and >= 0, so it is the
    numerically robust way to get <p^2>."""
    psi = np.asarray(psi, dtype=complex)
    x = np.asarray(x, dtype=float)
    dpsi = np.gradient(psi, x)
    return (hbar ** 2) * _trapz(np.abs(dpsi) ** 2, x).real


def sigma_p(psi, x, hbar=1.0):
    """Momentum standard deviation  sigma_p = sqrt(<p^2> - <p>^2)."""
    var = expectation_p2(psi, x, hbar) - expectation_p(psi, x, hbar) ** 2
    return np.sqrt(var) if var > 0.0 else 0.0


# --- 4. the analytic Gaussian wavepacket -------------------------------------

def gaussian_packet(x, x0=0.0, sigma=1.0, k0=0.0):
    """Normalized Gaussian wavepacket sampled on grid x:

        Psi(x) = (2 pi sigma^2)^{-1/4} exp(-(x-x0)^2 / (4 sigma^2)) exp(i k0 x).

    Its Born density |Psi|^2 is a normal distribution of mean x0 and standard
    deviation sigma, so (in closed form):
        <x> = x0,   sigma_x = sigma,   <p> = hbar k0,   sigma_p = hbar/(2 sigma),
    and sigma_x sigma_p = hbar/2 -- the Gaussian saturates the uncertainty bound
    (the minimum-uncertainty state, foreshadowing ~QM-07).  Returned already
    normalized to machine precision via the analytic prefactor."""
    x = np.asarray(x, dtype=float)
    pref = (2.0 * np.pi * sigma ** 2) ** (-0.25)
    return pref * np.exp(-(x - x0) ** 2 / (4.0 * sigma ** 2)) * np.exp(1j * k0 * x)


# --- 5. the move to momentum space (Fourier transform, ~MA-09) ---------------

def momentum_space(psi, x, hbar=1.0):
    """Momentum-space wavefunction  Phi(p) = (2 pi hbar)^{-1/2} int Psi(x) e^{-ipx/hbar} dx.

    This is the Fourier transform of the position-space Psi (Griffiths 3e Sec.3.4,
    'the momentum space wave function', p.134; ~MA-09).  |Phi(p)|^2 is the
    probability density over momentum, with int|Phi|^2 dp = 1 (Plancherel).

    Implemented with the FFT: for x_j = x[0] + j*dx the analytic transform on the
    DFT wavenumber grid k = 2 pi * fftfreq(N, dx) is
        Phi~(k) = (dx / sqrt(2 pi)) exp(-i k x[0]) * FFT(psi),
    and Phi(p) = Phi~(k)/sqrt(hbar) with p = hbar k (so dp = hbar dk preserves the
    norm).  Returns (p, Phi) sorted in ascending p."""
    psi = np.asarray(psi, dtype=complex)
    x = np.asarray(x, dtype=float)
    N = len(x)
    dx = x[1] - x[0]
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    phi_k = (dx / np.sqrt(2.0 * np.pi)) * np.exp(-1j * k * x[0]) * np.fft.fft(psi)
    p = hbar * k
    phi_p = phi_k / np.sqrt(hbar)
    order = np.argsort(p)
    return p[order], phi_p[order]


def expectation_p_fft(psi, x, hbar=1.0):
    """<p> computed in momentum space:  int p |Phi(p)|^2 dp.

    A cross-check on expectation_p (the finite-difference route): both must give
    the same <p>.  Uses momentum_space() above."""
    p, phi = momentum_space(psi, x, hbar)
    return _trapz(p * np.abs(phi) ** 2, p).real


# --- 6. free time evolution (preservation of normalization; preview of ~QM-03) -

def free_propagate(psi, x, t, mass=1.0, hbar=1.0):
    """Exact free-particle evolution of Psi by time t, spectrally.

    A free particle's Hamiltonian is diagonal in momentum, so
        Psi(x,t) = IFFT( exp(-i hbar k^2 t / (2 m)) * FFT(Psi(x,0)) ).
    This previews ~QM-03 (the Schrodinger equation) but is included here only to
    *demonstrate* the QM-02 fact that normalization is preserved in time
    (Griffiths 3e Sec.1.4, p.30): int|Psi(x,t)|^2 dx stays 1 while the packet
    spreads.  For a Gaussian the closed-form moments are
        <x>(t) = x0 + (hbar k0 / m) t,   sigma_x(t) = sigma0 sqrt(1+(hbar t/(2 m sigma0^2))^2),
        <p>(t) = hbar k0 (constant),     sigma_p(t) = hbar/(2 sigma0) (constant),
    which the tests check.  Periodic grid: keep the packet away from the edges."""
    psi = np.asarray(psi, dtype=complex)
    x = np.asarray(x, dtype=float)
    N = len(x)
    dx = x[1] - x[0]
    k = 2.0 * np.pi * np.fft.fftfreq(N, d=dx)
    phase = np.exp(-1j * hbar * k ** 2 * t / (2.0 * mass))
    return np.fft.ifft(np.fft.fft(psi) * phase)


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("QM-02  Wavefunction & Born rule -- the Gaussian wavepacket\n")
    x0, sigma, k0, hbar = 2.0, 1.0, 5.0, 1.0
    x = np.linspace(-18.0, 22.0, 4001)
    psi = gaussian_packet(x, x0=x0, sigma=sigma, k0=k0)

    print("Born density |Psi|^2 integrates to 1:")
    print("  int|Psi|^2 dx           = %.6f   (normalize target 1)"
          % total_probability(psi, x))
    print("\nPosition (closed form: <x>=x0=%.1f, sigma_x=sigma=%.1f):" % (x0, sigma))
    print("  <x>   = %.5f      <x^2> = %.5f      sigma_x = %.5f"
          % (expectation_x(psi, x), expectation_x2(psi, x), sigma_x(psi, x)))
    print("\nMomentum (closed form: <p>=hbar*k0=%.1f, sigma_p=hbar/2sigma=%.2f):"
          % (hbar * k0, hbar / (2 * sigma)))
    print("  <p>   = %.5f   (fd)   %.5f (fft)   sigma_p = %.5f"
          % (expectation_p(psi, x, hbar), expectation_p_fft(psi, x, hbar),
             sigma_p(psi, x, hbar)))
    print("  sigma_x * sigma_p = %.5f   (minimum-uncertainty bound hbar/2 = %.3f)"
          % (sigma_x(psi, x) * sigma_p(psi, x, hbar), hbar / 2.0))

    print("\nBorn probabilities (symmetric intervals, closed form erf(L/sqrt2)):")
    for L in (1, 2, 3):
        P = prob_between(psi, x, x0 - L * sigma, x0 + L * sigma)
        print("  P(|x-x0| < %d sigma) = %.5f   (erf(%d/sqrt2) = %.5f)"
              % (L, P, L, math.erf(L / math.sqrt(2.0))))

    print("\nPreservation of normalization in time (free spreading; preview ~QM-03):")
    xx = np.linspace(-40.0, 60.0, 8001)
    p0 = gaussian_packet(xx, x0=0.0, sigma=1.0, k0=4.0)
    for t in (0.0, 1.0, 2.0):
        pt = free_propagate(p0, xx, t, mass=1.0, hbar=1.0)
        sx_cf = 1.0 * math.sqrt(1.0 + (1.0 * t / (2 * 1.0 * 1.0 ** 2)) ** 2)
        print("  t=%.1f:  int|Psi|^2 = %.6f   <x> = %6.3f (cf %6.3f)   sigma_x = %.4f (cf %.4f)"
              % (t, total_probability(pt, xx), expectation_x(pt, xx),
                 0.0 + 4.0 * t, sigma_x(pt, xx), sx_cf))


if __name__ == "__main__":
    _demo()
