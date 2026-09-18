"""Tests for SM-04 quantum statistics. Reuses SM-03 (K_B, HBAR).

Run:  python3 test_quantum_statistics.py     ->  "All N tests passed."
"""
import math

# own module first: chains SM-03 (and SM-01/MA-19) onto sys.path
from quantum_statistics import (
    K_B, HBAR, C_LIGHT,
    bose_einstein, fermi_dirac, maxwell_boltzmann, fermi_dirac_T0,
    planck_energy_density, rayleigh_jeans, wien_peak_x,
    radiation_energy_density, stefan_boltzmann_constant,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_fermi_dirac_bounds_and_half_filling():
    T, mu = 300.0, 1e-20
    # FD is always in [0,1] (Pauli), and exactly 1/2 at eps = mu
    assert _approx(fermi_dirac(mu, mu, T), 0.5)
    for d in (-5.0, -1.0, 0.0, 1.0, 5.0):
        n = fermi_dirac(mu + d * K_B * T, mu, T)
        assert 0.0 <= n <= 1.0
    # below mu -> nearly full, above -> nearly empty
    assert fermi_dirac(mu - 5 * K_B * T, mu, T) > 0.99
    assert fermi_dirac(mu + 5 * K_B * T, mu, T) < 0.01


def test_fermi_dirac_T0_step():
    eF = 5.0 * 1.602e-19
    assert fermi_dirac_T0(0.5 * eF, eF) == 1.0
    assert fermi_dirac_T0(1.5 * eF, eF) == 0.0
    assert fermi_dirac_T0(eF, eF) == 0.5


def test_bose_einstein_diverges_near_mu():
    T, mu = 300.0, 1e-20
    # BE grows without bound as eps -> mu+ (macroscopic ground-state occupation)
    n_close = bose_einstein(mu + 0.001 * K_B * T, mu, T)
    n_far = bose_einstein(mu + 1.0 * K_B * T, mu, T)
    assert n_close > n_far > 0
    assert n_close > 100.0


def test_classical_limit_agreement():
    # (eps - mu) >> kT: BE, FD, MB all coincide
    T, mu = 300.0, 0.0
    eps = mu + 10.0 * K_B * T
    be, fd, mb = bose_einstein(eps, mu, T), fermi_dirac(eps, mu, T), maxwell_boltzmann(eps, mu, T)
    assert _approx(be, mb, tol=1e-3)
    assert _approx(fd, mb, tol=1e-3)
    # and the ordering BE > MB > FD always holds for finite occupancy
    eps2 = mu + 0.5 * K_B * T
    assert bose_einstein(eps2, mu, T) > maxwell_boltzmann(eps2, mu, T) > fermi_dirac(eps2, mu, T)


def test_planck_reduces_to_rayleigh_jeans_at_low_freq():
    T = 5778.0
    for w in (1e10, 1e11, 1e12):
        assert _approx(planck_energy_density(w, T), rayleigh_jeans(w, T), tol=1e-2)


def test_wien_peak_location():
    # wien_peak_x solves 3(1 - e^{-x}) = x  -> x ~ 2.8214
    x = wien_peak_x()
    assert _approx(x, 2.8214393721, tol=1e-6)
    assert _approx(3.0 * (1.0 - math.exp(-x)), x, tol=1e-9)
    # it really is the maximum of the Planck spectrum: scan omega, find the peak
    T = 5778.0
    w_peak = x * K_B * T / HBAR
    u_peak = planck_energy_density(w_peak, T)
    assert u_peak > planck_energy_density(0.7 * w_peak, T)
    assert u_peak > planck_energy_density(1.4 * w_peak, T)


def test_stefan_boltzmann_T4_and_constant():
    # energy density scales as T^4
    assert _approx(radiation_energy_density(2 * 300.0) / radiation_energy_density(300.0), 16.0)
    # sigma matches CODATA 5.670374e-8 W/m^2/K^4
    assert _approx(stefan_boltzmann_constant(), 5.670374419e-8, tol=1e-4)
    # sigma = a c / 4
    a = radiation_energy_density(1.0)                  # = a * 1^4
    assert _approx(stefan_boltzmann_constant(), a * C_LIGHT / 4.0, tol=1e-9)


def test_planck_integral_gives_energy_density():
    # integral of u(omega) d(omega) over the spectrum = a T^4
    T = 1000.0
    x_peak = wien_peak_x()
    w_peak = x_peak * K_B * T / HBAR
    wmax = 30.0 * w_peak
    n = 6000
    dw = wmax / n
    total = sum(planck_energy_density((i + 0.5) * dw, T) * dw for i in range(n))
    assert _approx(total, radiation_energy_density(T), tol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
