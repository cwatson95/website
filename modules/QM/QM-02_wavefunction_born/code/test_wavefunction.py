"""Tests for QM-02 wavefunction & Born rule -- every routine is checked against
the CLOSED-FORM moments of the analytic Gaussian wavepacket

    Psi(x) = (2 pi sigma^2)^{-1/4} exp(-(x-x0)^2/(4 sigma^2)) exp(i k0 x),

for which   int|Psi|^2 = 1,  <x>=x0,  sigma_x=sigma,  <x^2>=x0^2+sigma^2,
            <p>=hbar k0,  sigma_p=hbar/(2 sigma),  <p^2>=hbar^2(k0^2+1/(4 sigma^2)),
            sigma_x sigma_p = hbar/2  (minimum-uncertainty state),
and the Born probability over a symmetric interval is the error function
            P(|x-x0| < L sigma) = erf(L/sqrt(2)).
The free-particle evolution adds the closed-form moment laws
            <x>(t)=x0+(hbar k0/m) t,  sigma_x(t)=sigma0 sqrt(1+(hbar t/(2 m sigma0^2))^2),
            <p>(t)=hbar k0,  sigma_p(t)=hbar/(2 sigma0)  (both constant),  norm(t)=1.

Run directly:   python3 test_wavefunction.py        (-> "All N tests passed.")
Or with pytest: pytest test_wavefunction.py
"""
import math

import numpy as np

from wavefunction import (
    prob_density, total_probability, normalize, prob_between,
    expectation_x, expectation_x2, sigma_x,
    expectation_p, expectation_p2, sigma_p,
    gaussian_packet, momentum_space, expectation_p_fft, free_propagate,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# fixed analytic packet used by most tests (fine grid, packet well inside box)
X0, SIGMA, K0, HBAR = 2.0, 1.0, 5.0, 1.0
X = np.linspace(-18.0, 22.0, 4001)            # dx = 0.01
PSI = gaussian_packet(X, x0=X0, sigma=SIGMA, k0=K0)


# --- normalization & the Born density ----------------------------------------

def test_gaussian_prefactor_is_normalized():
    """The analytic (2 pi sigma^2)^{-1/4} prefactor gives int|Psi|^2 dx = 1."""
    assert _approx(total_probability(PSI, X), 1.0, abs_=1e-9)


def test_normalize_makes_unit_integral():
    """normalize() rescales an arbitrary state to int|psi|^2 dx = 1."""
    raw = 7.3 * np.exp(-(X - 1.0) ** 2 / 2.0) * np.exp(0.4j * X)   # un-normalized
    psi = normalize(raw, X)
    assert _approx(total_probability(psi, X), 1.0, abs_=1e-9)


def test_normalize_is_idempotent():
    """Normalizing an already-normalized state changes nothing (factor 1)."""
    once = normalize(PSI, X)
    twice = normalize(once, X)
    assert _approx(float(np.max(np.abs(twice - once))), 0.0, abs_=1e-12)


def test_prob_density_is_real_nonnegative():
    rho = prob_density(PSI)
    assert rho.dtype == np.float64
    assert float(rho.min()) >= 0.0


# --- Born probabilities (areas under |Psi|^2) --------------------------------

def test_prob_over_whole_line_is_one():
    """int_{-inf}^{inf} |Psi|^2 dx = 1 (whole grid)."""
    assert _approx(prob_between(PSI, X, X[0], X[-1]), 1.0, abs_=1e-9)


def test_prob_symmetric_interval_is_erf():
    """P(|x-x0| < L sigma) = erf(L/sqrt 2): 0.6827 (1s), 0.9545 (2s), 0.9973 (3s).

    The tiny +-1e-9 padding makes the symmetric endpoints land inside the mask
    regardless of float round-off on the grid."""
    for L in (1, 2, 3):
        a, b = X0 - L * SIGMA - 1e-9, X0 + L * SIGMA + 1e-9
        P = prob_between(PSI, X, a, b)
        assert _approx(P, math.erf(L / math.sqrt(2.0)), abs_=2e-4)


def test_prob_left_half_is_one_half():
    """By symmetry of |Psi|^2 about x0, P(x < x0) = 1/2."""
    assert _approx(prob_between(PSI, X, X[0], X0), 0.5, abs_=1e-4)


def test_prob_between_orders_limits():
    """prob_between is symmetric in its limits a,b."""
    assert _approx(prob_between(PSI, X, 1.0, 3.0),
                   prob_between(PSI, X, 3.0, 1.0), abs_=1e-12)


# --- position expectation values ---------------------------------------------

def test_expectation_x():
    """<x> = x0 (mean of the Born density)."""
    assert _approx(expectation_x(PSI, X), X0, abs_=1e-6)


def test_expectation_x2():
    """<x^2> = x0^2 + sigma^2."""
    assert _approx(expectation_x2(PSI, X), X0 ** 2 + SIGMA ** 2, rel=1e-6)


def test_sigma_x():
    """sigma_x = sqrt(<x^2>-<x>^2) = sigma."""
    assert _approx(sigma_x(PSI, X), SIGMA, rel=1e-6)


# --- momentum expectation values ---------------------------------------------

def test_expectation_p_finite_difference():
    """<p> = hbar k0 via p_hat = -i hbar d/dx (central difference).

    The residual ~4e-4 is the expected O((k0 dx)^2) discretization of the
    derivative of e^{i k0 x}, k0*sinc(k0 dx); the FFT route below is exact."""
    assert _approx(expectation_p(PSI, X, HBAR), HBAR * K0, rel=5e-3)


def test_expectation_p_fft_is_exact():
    """<p> = hbar k0 via the momentum-space density (FFT) -- exact for the packet."""
    assert _approx(expectation_p_fft(PSI, X, HBAR), HBAR * K0, rel=1e-6)


def test_p_finite_difference_agrees_with_fft():
    assert _approx(expectation_p(PSI, X, HBAR),
                   expectation_p_fft(PSI, X, HBAR), rel=5e-3)


def test_expectation_p2():
    """<p^2> = hbar^2 (k0^2 + 1/(4 sigma^2))."""
    want = HBAR ** 2 * (K0 ** 2 + 1.0 / (4.0 * SIGMA ** 2))
    assert _approx(expectation_p2(PSI, X, HBAR), want, rel=5e-3)


def test_sigma_p():
    """sigma_p = hbar/(2 sigma)."""
    assert _approx(sigma_p(PSI, X, HBAR), HBAR / (2.0 * SIGMA), rel=5e-3)


def test_real_gaussian_has_zero_momentum():
    """A purely real Gaussian (k0=0) has <p> = 0 (no net momentum)."""
    psi0 = gaussian_packet(X, x0=X0, sigma=SIGMA, k0=0.0)
    assert _approx(expectation_p(psi0, X, HBAR), 0.0, abs_=1e-9)
    assert _approx(expectation_p_fft(psi0, X, HBAR), 0.0, abs_=1e-9)


def test_minimum_uncertainty_product():
    """The Gaussian saturates the bound: sigma_x sigma_p = hbar/2 (preview ~QM-07)."""
    prod = sigma_x(PSI, X) * sigma_p(PSI, X, HBAR)
    assert _approx(prod, HBAR / 2.0, rel=5e-3)
    assert prod >= HBAR / 2.0 - 1e-3          # never below the Heisenberg floor


def test_hbar_scaling():
    """<p> and sigma_p scale linearly with hbar (operator -i hbar d/dx)."""
    hb = 2.5
    assert _approx(expectation_p_fft(PSI, X, hb), hb * K0, rel=1e-6)
    assert _approx(sigma_p(PSI, X, hb), hb / (2.0 * SIGMA), rel=5e-3)


# --- the move to momentum space (Fourier transform) --------------------------

def test_momentum_space_is_normalized():
    """Plancherel: int|Phi(p)|^2 dp = 1 (probability conserved by the FT)."""
    p, phi = momentum_space(PSI, X, HBAR)
    integ = np.sum(0.5 * (np.abs(phi[1:]) ** 2 + np.abs(phi[:-1]) ** 2) * np.diff(p))
    assert _approx(float(integ.real), 1.0, abs_=1e-4)


def test_momentum_space_density_matches_closed_form_gaussian():
    """|Phi(p)|^2 is the Gaussian centred at p0=hbar k0 with width sigma_p=hbar/(2 sigma)."""
    p, phi = momentum_space(PSI, X, HBAR)
    p0 = HBAR * K0
    sp = HBAR / (2.0 * SIGMA)
    want = (1.0 / (sp * math.sqrt(2.0 * math.pi))) * np.exp(-(p - p0) ** 2 / (2.0 * sp ** 2))
    # compare where the density is appreciable
    near = np.abs(p - p0) < 4.0 * sp
    assert _approx(float(np.max(np.abs(np.abs(phi[near]) ** 2 - want[near]))),
                   0.0, abs_=2e-3)


# --- preservation of normalization in time (free spreading; preview ~QM-03) --

# free-evolution grid: packet starts at 0, drifts right, stays inside the box
XX = np.linspace(-40.0, 60.0, 8001)           # dx = 0.0125
SIG0, KK0, MASS = 1.0, 4.0, 1.0
P0 = gaussian_packet(XX, x0=0.0, sigma=SIG0, k0=KK0)


def test_free_evolution_preserves_normalization():
    """int|Psi(x,t)|^2 dx stays 1 as the packet spreads (Griffiths Sec.1.4, p.30)."""
    for t in (0.0, 0.5, 1.0, 2.0):
        pt = free_propagate(P0, XX, t, mass=MASS, hbar=HBAR)
        assert _approx(total_probability(pt, XX), 1.0, abs_=1e-6)


def test_free_evolution_group_velocity():
    """<x>(t) = x0 + (hbar k0 / m) t  -- the packet centre moves at the group velocity."""
    for t in (0.5, 1.0, 2.0):
        pt = free_propagate(P0, XX, t, mass=MASS, hbar=HBAR)
        assert _approx(expectation_x(pt, XX), 0.0 + HBAR * KK0 / MASS * t, abs_=2e-3)


def test_free_evolution_spreading_law():
    """sigma_x(t) = sigma0 sqrt(1 + (hbar t/(2 m sigma0^2))^2)  -- closed-form spread."""
    for t in (0.5, 1.0, 2.0):
        pt = free_propagate(P0, XX, t, mass=MASS, hbar=HBAR)
        want = SIG0 * math.sqrt(1.0 + (HBAR * t / (2.0 * MASS * SIG0 ** 2)) ** 2)
        assert _approx(sigma_x(pt, XX), want, rel=2e-3)


def test_free_evolution_conserves_momentum():
    """Free evolution multiplies Phi(k) by a pure phase, so <p> and sigma_p are
    constant in time (= the t=0 closed-form values hbar k0 and hbar/(2 sigma0))."""
    p_ref = expectation_p_fft(P0, XX, HBAR)
    s_ref = sigma_p(P0, XX, HBAR)
    assert _approx(p_ref, HBAR * KK0, rel=1e-6)            # t=0 vs closed form
    assert _approx(s_ref, HBAR / (2.0 * SIG0), rel=5e-3)
    for t in (0.5, 1.0, 2.0):
        pt = free_propagate(P0, XX, t, mass=MASS, hbar=HBAR)
        assert _approx(expectation_p_fft(pt, XX, HBAR), p_ref, rel=1e-6)
        assert _approx(sigma_p(pt, XX, HBAR), s_ref, rel=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
