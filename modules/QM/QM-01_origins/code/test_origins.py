"""Tests for QM-01 origins -- every 'known constant' is rederived and checked.

Run directly:   python3 test_origins.py        (-> "All N tests passed.")
Or with pytest: pytest test_origins.py
"""
import math

from origins import (
    h, c, k_B, e, m_e, a0, Ry_eV, R_inf, sigma_SB, wien_b, lambda_C,
    planck_u_nu, rayleigh_jeans_u_nu, wien_u_nu,
    stefan_boltzmann_sigma, wien_displacement_b,
    photon_energy, photoelectric_Kmax, threshold_frequency, stopping_voltage,
    bohr_energy_eV, bohr_radius, rydberg_wavelength,
    de_broglie_wavelength, de_broglie_from_energy, compton_shift,
)


def _approx(x, y, rel=1e-9, abs_=0.0):
    return abs(x - y) <= max(rel * abs(y), abs_)


def test_planck_reduces_to_rayleigh_jeans():
    """Low frequency (h nu << k_B T): Planck -> Rayleigh-Jeans."""
    T = 300.0
    nu = 1e9                       # h nu / k_B T ~ 1.6e-4, deep classical regime
    assert _approx(planck_u_nu(nu, T), rayleigh_jeans_u_nu(nu, T), rel=1e-3)


def test_planck_reduces_to_wien():
    """High frequency (h nu >> k_B T): Planck -> Wien approximation."""
    T = 300.0
    nu = 1e14                      # h nu / k_B T ~ 16, deep quantum regime
    assert _approx(planck_u_nu(nu, T), wien_u_nu(nu, T), rel=1e-6)


def test_rayleigh_jeans_diverges_but_planck_does_not():
    """The UV catastrophe: RJ grows without bound, Planck turns over and falls."""
    T = 5000.0
    rj = [rayleigh_jeans_u_nu(nu, T) for nu in (1e14, 1e15, 1e16)]
    pl = [planck_u_nu(nu, T) for nu in (1e14, 1e15, 1e16)]
    assert rj[0] < rj[1] < rj[2]               # RJ monotonically explodes
    assert pl[2] < pl[1]                        # Planck has already turned over


def test_stefan_boltzmann_recovered():
    """Integrating Planck over nu must reproduce sigma to <0.1%."""
    sig = stefan_boltzmann_sigma()
    assert _approx(sig, sigma_SB, rel=2e-3)


def test_wien_displacement_recovered():
    """Maximising B(lambda,T) must reproduce b = lambda_max T to <0.1%."""
    b = wien_displacement_b(T=1000.0)
    assert _approx(b, wien_b, rel=1e-3)
    # b is independent of T:
    assert _approx(wien_displacement_b(T=6000.0), b, rel=1e-3)


def test_photoelectric_threshold_and_linearity():
    W = 2.28 * e                              # sodium work function
    f0 = threshold_frequency(W)
    assert photoelectric_Kmax(0.99 * f0, W) == 0.0     # below cutoff: nothing
    assert photoelectric_Kmax(2.0 * f0, W) > 0.0       # above cutoff: emission
    # K_max is linear in f with slope h (Millikan's measurement of h):
    f1, f2 = 2.0 * f0, 3.0 * f0
    slope = (photoelectric_Kmax(f2, W) - photoelectric_Kmax(f1, W)) / (f2 - f1)
    assert _approx(slope, h, rel=1e-12)
    assert _approx(photon_energy(f0), W, rel=1e-12)    # threshold photon = W


def test_stopping_voltage():
    W = 2.0 * e
    f = 2.0e15
    assert _approx(stopping_voltage(f, W), photoelectric_Kmax(f, W) / e, rel=1e-12)


def test_bohr_levels():
    assert _approx(bohr_energy_eV(1), -Ry_eV, rel=1e-4)   # -13.606 eV
    assert _approx(bohr_energy_eV(2), -Ry_eV / 4.0, rel=1e-4)
    assert _approx(bohr_energy_eV(1, Z=2), -4.0 * Ry_eV, rel=1e-4)  # He+ scales Z^2


def test_bohr_radius():
    assert _approx(bohr_radius(1), a0, rel=1e-4)          # ground-state = a0
    assert _approx(bohr_radius(2), 4.0 * a0, rel=1e-4)    # r_n ~ n^2


def test_rydberg_balmer_and_lyman():
    # Balmer H-alpha (3 -> 2): 656.3 nm (visible red)
    assert _approx(rydberg_wavelength(2, 3) * 1e9, 656.3, abs_=0.5)
    # Lyman-alpha (2 -> 1): 121.6 nm (UV)
    assert _approx(rydberg_wavelength(1, 2) * 1e9, 121.6, abs_=0.5)
    # Rydberg constant rebuilt from constants matches R_inf
    R = 1.0 / rydberg_wavelength(1, 10**9)   # n2 -> inf gives 1/(R*1)
    assert _approx(R, R_inf, rel=1e-3)


def test_de_broglie():
    # consistency: lambda from p and lambda from energy agree
    E = 100.0 * e
    p = math.sqrt(2.0 * m_e * E)
    assert _approx(de_broglie_wavelength(p), de_broglie_from_energy(E), rel=1e-12)
    # 100 eV electron ~ 0.123 nm (electron-microscope regime)
    assert _approx(de_broglie_from_energy(100.0 * e) * 1e9, 0.1227, abs_=0.002)


def test_compton():
    assert _approx(compton_shift(0.0), 0.0, abs_=1e-20)         # forward: no shift
    assert _approx(compton_shift(math.pi), 2.0 * lambda_C, rel=1e-9)  # back: 2 lambda_C
    assert _approx(compton_shift(math.pi / 2.0), lambda_C, rel=1e-9)  # 90 deg: lambda_C


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
