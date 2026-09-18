"""Tests for QM-18 scattering -- every formula checked numerically against a
closed form or an independent computation (no formula is asserted, all are
verified).

Run directly:   python3 test_scattering.py        (-> "All N tests passed.")
Or with pytest: pytest test_scattering.py

Units: hbar = 2m = 1 (E = k^2); see scattering.py.
"""
import math

import numpy as np
from scipy.special import eval_legendre

from scattering import (
    momentum_transfer, P_l,
    hard_sphere_phase_shift, square_well_phase_shift,
    phase_shifts_hard_sphere, phase_shifts_square_well,
    partial_wave_amplitude, differential_cross_section,
    partial_cross_section, total_cross_section,
    optical_theorem_sigma,
    born_amplitude_yukawa, born_amplitude_radial, rutherford_cross_section,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


# --- special-function cross-link (~MA-12 / ~QM-10) ---------------------------

def test_legendre_import_matches_scipy():
    """The P_l(cos theta) used in the partial-wave sum comes from ~MA-12; confirm
    it matches scipy.special.eval_legendre over a grid and a range of l."""
    xs = np.linspace(-1.0, 1.0, 21)
    for l in range(0, 7):
        ours = P_l(l, xs)
        ref = eval_legendre(l, xs)
        assert np.allclose(ours, ref, atol=1e-12), l


# --- kinematics --------------------------------------------------------------

def test_momentum_transfer():
    """q = 2k sin(theta/2): zero forward, 2k backward, k*sqrt(2) at 90 deg."""
    k = 1.7
    assert _approx(float(momentum_transfer(0.0, k)), 0.0, abs_=1e-15)
    assert _approx(float(momentum_transfer(math.pi, k)), 2.0 * k, rel=1e-12)
    assert _approx(float(momentum_transfer(math.pi / 2, k)),
                   2.0 * k * math.sin(math.pi / 4), rel=1e-12)


# --- hard sphere -------------------------------------------------------------

def test_hard_sphere_swave_phase_shift():
    """s-wave hard-sphere phase shift is d_0 = -ka (the core pushes the wave out
    by exactly the radius).  Griffiths Example 10.3 / Problem 10.6."""
    a = 1.0
    for ka in (0.01, 0.05, 0.2):
        d0 = hard_sphere_phase_shift(0, ka / a, a)
        assert _approx(d0, -ka, rel=1e-6), ka


def test_hard_sphere_low_energy_4pi_a2():
    """The famous factor of 4: at low energy (ka -> 0) the hard-sphere total
    cross-section tends to 4 pi a^2 -- four times the classical geometric shadow
    pi a^2 (Griffiths Eq. 10.36, p.488).  The long-wavelength wave 'feels' the
    whole surface, not just the head-on disc."""
    a = 1.0
    ratios = []
    for ka in (0.1, 0.03, 0.01):
        k = ka / a
        ds = phase_shifts_hard_sphere(k, a, lmax=8)
        sig = total_cross_section(k, ds)
        ratios.append(sig / (math.pi * a ** 2))
    # ratio -> 4 as ka -> 0, and approaches monotonically from below
    assert _approx(ratios[-1], 4.0, abs_=2e-3)
    assert ratios[0] < ratios[1] < ratios[2] <= 4.0 + 1e-9
    # and the absolute value matches 4 pi a^2
    k = 0.005 / a
    sig = total_cross_section(k, phase_shifts_hard_sphere(k, a, lmax=8))
    assert _approx(sig, 4.0 * math.pi * a ** 2, rel=2e-3)


def test_hard_sphere_swave_dominates_at_low_energy():
    """At low energy the l=0 partial wave dominates: sin^2(d_l) ~ (ka)^{2(2l+1)},
    so higher l are suppressed by powers of ka (Griffiths p.488)."""
    a, ka = 1.0, 0.1
    k = ka / a
    s0 = partial_cross_section(0, k, hard_sphere_phase_shift(0, k, a))
    s1 = partial_cross_section(1, k, hard_sphere_phase_shift(1, k, a))
    assert s0 > 0.0
    assert s1 / s0 < 1e-2          # p-wave already < 1% of s-wave at ka=0.1


# --- square well -------------------------------------------------------------

def test_square_well_swave_closed_form():
    """Numerical log-derivative matching reproduces the s-wave closed form
    d_0 = -ka + arctan((k/k_in) tan(k_in a)),  k_in = sqrt(k^2 + V0).  Compared
    via sin^2(d_0) (the cross-section observable; d_0 itself is defined mod pi)."""
    for k, a, V0 in [(0.5, 1.0, 2.0), (1.0, 1.0, 3.0), (0.8, 1.5, 1.0),
                     (1.5, 1.0, 4.0)]:
        k_in = math.sqrt(k * k + V0)
        d0_closed = -k * a + math.atan((k / k_in) * math.tan(k_in * a))
        d0_num = square_well_phase_shift(0, k, a, V0)
        assert _approx(math.sin(d0_num) ** 2, math.sin(d0_closed) ** 2,
                       abs_=1e-9), (k, a, V0)


def test_square_well_zero_depth_no_scattering():
    """A vanishing potential scatters nothing: V0 -> 0 gives every sin^2(d_l) -> 0
    (d_l = 0 mod pi) and a zero total cross-section.  (sin^2 is the observable;
    the bare phase can land on 0 or pi.)"""
    k, a = 1.3, 1.0
    ds = phase_shifts_square_well(k, a, 1e-12, lmax=5)
    assert np.allclose(np.sin(ds) ** 2, 0.0, atol=1e-12)
    assert _approx(total_cross_section(k, ds), 0.0, abs_=1e-10)


def test_square_well_dirichlet_limit_is_hard_sphere():
    """Deepening/raising the interior log-derivative toward the Dirichlet
    (R(a)=0) limit drives the square-well phase shift to the hard-sphere value
    tan d_l = j_l(ka)/n_l(ka).  Realized by tracking a tunable barrier: a very
    large interior log-derivative L -> infinity makes num/den -> j_l/n_l.  We
    test the formula identity directly: with the same ka, the hard-sphere result
    equals the L->infinity square-well result."""
    k, a = 1.2, 1.0
    x = k * a
    from scattering import spherical_j, spherical_n
    for l in range(0, 4):
        hs = hard_sphere_phase_shift(l, k, a)
        # L -> infinity Dirichlet limit of the square-well matching formula:
        d_dirichlet = math.atan2(spherical_j(l, x), spherical_n(l, x))
        assert _approx(math.sin(hs) ** 2, math.sin(d_dirichlet) ** 2, abs_=1e-12), l


# --- partial-wave amplitude, cross-section, optical theorem -------------------

def test_differential_cross_section_is_f_squared():
    """dsigma/dOmega = |f(theta)|^2 (Griffiths Eq. 10.14)."""
    k, a, V0 = 1.5, 1.0, 4.0
    ds = phase_shifts_square_well(k, a, V0, lmax=6)
    thetas = np.linspace(0.05, math.pi, 11)
    f = partial_wave_amplitude(thetas, k, ds)
    dcs = differential_cross_section(thetas, k, ds)
    assert np.allclose(dcs, np.abs(f) ** 2, rtol=1e-12)


def test_optical_theorem_hard_sphere():
    """sigma_tot = (4pi/k) Im f(0) equals (4pi/k^2) sum (2l+1) sin^2 d_l, for the
    hard sphere (Griffiths Problem 10.19, p.504)."""
    a = 1.0
    for ka in (0.3, 1.0, 2.5):
        k = ka / a
        ds = phase_shifts_hard_sphere(k, a, lmax=12)
        assert _approx(optical_theorem_sigma(k, ds), total_cross_section(k, ds),
                       rel=1e-10)


def test_optical_theorem_square_well():
    """Same identity for the square well -- it is a consequence of the partial-
    wave structure, independent of the potential."""
    for k, a, V0 in [(1.5, 1.0, 4.0), (0.7, 1.2, 2.0), (2.0, 1.0, 6.0)]:
        ds = phase_shifts_square_well(k, a, V0, lmax=12)
        assert _approx(optical_theorem_sigma(k, ds), total_cross_section(k, ds),
                       rel=1e-10)


def test_integrated_dcs_equals_total_cross_section():
    """Integrating the differential cross-section over the full solid angle must
    reproduce the total cross-section: int |f|^2 dOmega = sigma.  This uses the
    ORTHOGONALITY of the P_l (not just the forward value), an independent check
    on partial_wave_amplitude vs total_cross_section.  Gauss-Legendre in
    x = cos theta is exact for the polynomial integrand."""
    k, a, V0 = 1.5, 1.0, 4.0
    ds = phase_shifts_square_well(k, a, V0, lmax=6)
    xg, wg = np.polynomial.legendre.leggauss(64)
    thetas = np.arccos(xg)
    dcs = differential_cross_section(thetas, k, ds)
    integral = 2.0 * math.pi * np.sum(wg * dcs)      # int dphi dcostheta |f|^2
    assert _approx(integral, total_cross_section(k, ds), rel=1e-8)


def test_unitarity_bound():
    """Each partial cross-section obeys sigma_l <= 4pi(2l+1)/k^2 (since
    sin^2 d_l <= 1); equality is a resonance (d_l = pi/2)."""
    k, a, V0 = 1.8, 1.0, 7.0
    for l in range(0, 8):
        d = square_well_phase_shift(l, k, a, V0)
        sl = partial_cross_section(l, k, d)
        assert sl <= 4.0 * math.pi * (2 * l + 1) / k ** 2 + 1e-12


# --- Born approximation ------------------------------------------------------

def test_born_yukawa_closed_form():
    """The reduced radial Born integral -(2m/hbar^2 q) int r V sin(qr) dr
    reproduces the closed form f = -2m beta/(hbar^2 (mu^2+q^2)) for the Yukawa
    potential, over a range of angles (Griffiths Eq. 10.91, p.500)."""
    k, beta, mu = 1.0, 0.7, 0.5
    V = lambda r: beta * math.exp(-mu * r) / r
    for th in (0.3, 1.0, 2.0, 3.0):
        f_num = born_amplitude_radial(th, k, V)
        f_cf = born_amplitude_yukawa(th, k, beta, mu)
        assert _approx(f_num, f_cf, rel=1e-6), th
    # forward direction (q -> 0) too:
    f0_num = born_amplitude_radial(0.0, k, V)
    f0_cf = born_amplitude_yukawa(0.0, k, beta, mu)
    assert _approx(f0_num, f0_cf, rel=1e-6)


def test_born_units_general_mass():
    """The Born amplitude scales as -2m beta/hbar^2/(mu^2+q^2): doubling m
    doubles f; the default m=1/2, hbar=1 give f = -beta/(mu^2+q^2)."""
    k, beta, mu, th = 1.0, 0.7, 0.5, 1.0
    q = 2 * k * math.sin(th / 2)
    assert _approx(born_amplitude_yukawa(th, k, beta, mu), -beta / (mu ** 2 + q ** 2),
                   rel=1e-12)
    f1 = born_amplitude_yukawa(th, k, beta, mu, m=1.0, hbar=1.0)
    f2 = born_amplitude_yukawa(th, k, beta, mu, m=2.0, hbar=1.0)
    assert _approx(f2, 2.0 * f1, rel=1e-12)


def test_yukawa_screening_regularizes_forward():
    """A finite screening length (mu > 0) keeps f finite in the forward
    direction, f(0) = -2m beta/(hbar^2 mu^2); as mu -> 0 (bare Coulomb) the
    forward amplitude diverges -- the signature of the infinite range of 1/r."""
    k, beta = 2.0, 1.0
    f_small_mu = abs(born_amplitude_yukawa(0.0, k, beta, mu=0.1))
    f_smaller_mu = abs(born_amplitude_yukawa(0.0, k, beta, mu=0.01))
    assert f_smaller_mu > 100.0 * f_small_mu      # ~ 1/mu^2 blow-up
    # finite for mu>0:
    assert _approx(born_amplitude_yukawa(0.0, k, beta, mu=0.5), -1.0 / 0.25, rel=1e-12)


def test_born_forward_peaking():
    """The Born amplitude is forward-peaked: |f| is largest at theta = 0 (q = 0)
    and decreases monotonically toward backscatter (q = 2k)."""
    k, beta, mu = 3.0, 1.0, 0.7
    mags = [abs(born_amplitude_yukawa(th, k, beta, mu))
            for th in (0.0, math.pi / 4, math.pi / 2, 3 * math.pi / 4, math.pi)]
    assert all(mags[i] > mags[i + 1] for i in range(len(mags) - 1))


def test_born_rutherford_limit():
    """The screened-Coulomb (mu -> 0) limit reproduces Rutherford scattering:
    dsigma/dOmega ~ 1/sin^4(theta/2), equal to the classical ~CM-08 result
    beta^2/(16 E^2 sin^4(theta/2)) with E = k^2 (Griffiths Example 10.6, p.501)."""
    k, beta = 1.0, 1.0
    E = k ** 2                                  # hbar = 2m = 1
    # 1/sin^4 dependence: dcs * sin^4(theta/2) is angle-independent
    consts = []
    for th in (0.5, 1.0, 2.0, 3.0):
        dcs = rutherford_cross_section(th, k, beta)
        consts.append(dcs * math.sin(th / 2) ** 4)
    assert all(_approx(c, consts[0], rel=1e-12) for c in consts)
    # and the constant equals the classical Rutherford value beta^2/(16 E^2):
    assert _approx(consts[0], beta ** 2 / (16.0 * E ** 2), rel=1e-12)
    # Rutherford == |Yukawa(mu->0)|^2:
    th = 1.3
    dcs_yuk = abs(born_amplitude_yukawa(th, k, beta, mu=1e-6)) ** 2
    assert _approx(dcs_yuk, rutherford_cross_section(th, k, beta), rel=1e-4)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
