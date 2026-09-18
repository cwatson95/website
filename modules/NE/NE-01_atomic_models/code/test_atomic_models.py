"""NE-01 tests -- the Bohr atom against the numbers printed in Shultis & Faw §3.1.

Run:  python3 test_atomic_models.py
"""

import math

from atomic_models import (
    C, M_E, M_P, H_PLANCK, E_CHARGE, EPS0,
    R_INF, R_H, BOHR_RADIUS, HARTREE_EV,
    reduced_mass, reduced_mass_ratio, rydberg_constant,
    bohr_radius, bohr_velocity, bohr_energy, bohr_angular_momentum,
    bohr_orbital_period, ionization_energy,
    transition_energy, transition_wavelength, rydberg_wavelength,
    series_limit_wavelength, series_name,
    fine_structure_constant, is_nonrelativistic,
    thomson_scattering_probability,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the numbers the book prints --------------------------------------------

def test_book_ground_state_values():
    """r_1 = 5.293e-11 m, v_1 = 2.187e6 m/s, E_1 = -13.606 eV (printed pp. 59-60)."""
    assert _approx(bohr_radius(1), 5.293e-11, tol=2e-4)
    assert _approx(bohr_velocity(1), 2.187e6, tol=5e-4)
    assert _approx(bohr_energy(1), -13.606, tol=1e-4)
    assert _approx(BOHR_RADIUS, bohr_radius(1))
    assert _approx(HARTREE_EV, -bohr_energy(1))


def test_rydberg_constants():
    """R_inf from the constants, and R_H = 10 967 758 m^-1 (printed p. 60)."""
    assert _approx(R_INF, 1.0973732e7, tol=1e-6)
    assert _approx(R_H, 10967758.0, tol=1e-6)
    assert rydberg_constant() == R_INF
    assert _approx(rydberg_constant(M_P), R_H)
    # the finite-mass constant must be the smaller one
    assert R_H < R_INF


def test_reduced_mass_ratio_reproduces_book_R_H():
    """The book prints mu_e/m_e = 0.999445568 on p. 60, but that value does not
    reproduce the R_H printed two lines later.  0.999455679 does."""
    ratio = reduced_mass_ratio()
    assert _approx(ratio, 0.999455679, tol=1e-9)
    assert _approx(R_INF * ratio, 10967758.0, tol=1e-6)
    # the printed ratio misses R_H by ~100 m^-1, far outside its 8 quoted figures
    assert abs(R_INF * 0.999445568 - 10967758.0) > 100.0


def test_helium_ion_ionization_energy():
    """Example 3.1 (printed p. 60): He+ ground state needs 54.4 eV to ionize."""
    assert _approx(ionization_energy(2), 54.42, tol=1e-3)
    # E_n scales as Z^2
    assert _approx(bohr_energy(1, 2), 4.0 * bohr_energy(1, 1))


# --- structure of the model --------------------------------------------------

def test_energy_scales_as_Z2_over_n2():
    for Z in (1, 2, 3):
        for n in (1, 2, 5):
            assert _approx(bohr_energy(n, Z), -HARTREE_EV * Z ** 2 / n ** 2)


def test_radius_and_velocity_scaling():
    """r_n ~ n^2/Z and v_n ~ Z/n [Eq. (3.4)]."""
    for Z in (1, 2):
        for n in (1, 3, 7):
            assert _approx(bohr_radius(n, Z), BOHR_RADIUS * n ** 2 / Z)
            assert _approx(bohr_velocity(n, Z), bohr_velocity(1, 1) * Z / n)


def test_angular_momentum_is_quantized():
    """Postulate 2: L = m_e v_n r_n = n h/2pi [Eq. (3.3)]."""
    for n in (1, 2, 3, 6):
        L = M_E * bohr_velocity(n) * bohr_radius(n)
        assert _approx(L, bohr_angular_momentum(n), tol=1e-12)
        assert _approx(L, n * H_PLANCK / (2 * math.pi), tol=1e-12)


def test_virial_theorem():
    """For a 1/r potential, T = -E and V = 2E, so E = -T [from Eq. (3.5)]."""
    for n in (1, 2, 4):
        T = 0.5 * M_E * bohr_velocity(n) ** 2 / E_CHARGE          # eV
        V = -E_CHARGE / (4 * math.pi * EPS0 * bohr_radius(n))     # eV
        assert _approx(T, -bohr_energy(n), tol=1e-9)
        assert _approx(V, 2.0 * bohr_energy(n), tol=1e-9)
        assert _approx(T + V, bohr_energy(n), tol=1e-9)


def test_coulomb_balances_centripetal_force():
    """Postulate 1, Eq. (3.2): m v^2/r = Z e^2/(4 pi eps0 r^2)."""
    for Z in (1, 2):
        for n in (1, 3):
            r, v = bohr_radius(n, Z), bohr_velocity(n, Z)
            centripetal = M_E * v ** 2 / r
            coulomb = Z * E_CHARGE ** 2 / (4 * math.pi * EPS0 * r ** 2)
            assert _approx(centripetal, coulomb, tol=1e-12)


# --- spectra -----------------------------------------------------------------

def test_transitions_reproduce_the_rydberg_formula():
    """Eq. (3.7): the Bohr energies give exactly 1/lambda = R(1/n_lo^2 - 1/n_hi^2)."""
    for n_lo, n_hi in [(1, 2), (2, 3), (2, 5), (3, 7)]:
        lam_bohr = transition_wavelength(n_lo, n_hi)
        lam_ryd = rydberg_wavelength(n_lo, n_hi, R=R_INF)
        assert _approx(lam_bohr, lam_ryd, tol=1e-9)


def test_balmer_alpha_is_the_red_line():
    """3->2 in hydrogen is 656.3 nm (the book's Fig. 3.4) once the reduced mass
    is used; the infinite-mass value is 0.4 nm short."""
    lam = transition_wavelength(2, 3, nuclear_mass=M_P)
    assert _approx(lam * 1e9, 656.47, tol=1e-3)
    assert transition_wavelength(2, 3) < lam


def test_series_limits_and_names():
    """The series limit is lambda = n_lo^2/R (Table 3.1, printed p. 59)."""
    assert series_name(1) == "Lyman"
    assert series_name(2) == "Balmer"
    assert series_name(5) == "Pfund"
    # Lyman limit 91.2 nm (ultraviolet), Balmer limit 364.7 nm
    assert _approx(series_limit_wavelength(1) * 1e9, 91.18, tol=1e-3)
    assert _approx(series_limit_wavelength(2) * 1e9, 364.7, tol=1e-3)
    # every line in a series is longer than the series limit
    for n in range(3, 12):
        assert transition_wavelength(2, n, nuclear_mass=M_P) > series_limit_wavelength(2)


def test_transition_energy_positive_and_additive():
    """Energies add along a cascade: (5->3) + (3->2) = (5->2)."""
    assert transition_energy(2, 3) > 0
    e53 = transition_energy(3, 5)
    e32 = transition_energy(2, 3)
    e52 = transition_energy(2, 5)
    assert _approx(e53 + e32, e52)


def test_photon_energy_matches_wavelength():
    """E = hc/lambda for every transition."""
    for n_lo, n_hi in [(1, 3), (2, 4)]:
        E = transition_energy(n_lo, n_hi) * E_CHARGE
        lam = transition_wavelength(n_lo, n_hi)
        assert _approx(E * lam, H_PLANCK * C, tol=1e-12)


# --- consistency and history -------------------------------------------------

def test_fine_structure_constant_is_v1_over_c():
    alpha = fine_structure_constant()
    assert _approx(alpha, bohr_velocity(1) / C, tol=1e-12)
    assert _approx(1.0 / alpha, 137.036, tol=1e-5)
    assert is_nonrelativistic(1)
    # a hydrogen-like ion of large Z is no longer safely non-relativistic
    assert not is_nonrelativistic(1, Z=92)


def test_orbital_period_and_reduced_mass_helpers():
    T = bohr_orbital_period(1)
    assert _approx(T, 2 * math.pi * bohr_radius(1) / bohr_velocity(1))
    assert T > 0
    assert _approx(reduced_mass(M_E, M_P), M_E * M_P / (M_E + M_P))
    # a much heavier partner leaves the electron mass essentially unchanged
    assert reduced_mass(M_E, 1e6 * M_P) < M_E
    assert _approx(reduced_mass(M_E, 1e12 * M_P), M_E, tol=1e-9)


def test_thomson_model_fails_by_36_orders_of_magnitude():
    """Printed p. 58: the plum-pudding model gives ~1e-40 for phi > 90 deg,
    while Geiger and Marsden saw 1 in 8000."""
    p = thomson_scattering_probability(90.0)
    assert p < 1e-38
    assert (1.0 / 8000) / p > 1e30
    # monotone decreasing in angle, and unity at zero
    assert _approx(thomson_scattering_probability(0.0), 1.0)
    assert thomson_scattering_probability(5.0) < thomson_scattering_probability(1.0)


def test_invalid_inputs_raise():
    for bad in (0, -1, 1.5):
        try:
            bohr_energy(bad)
        except ValueError:
            pass
        else:
            raise AssertionError("n=%r should be rejected" % (bad,))
    try:
        transition_wavelength(3, 2)          # n_hi must exceed n_lo
    except ValueError:
        pass
    else:
        raise AssertionError("n_hi <= n_lo should be rejected")


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
