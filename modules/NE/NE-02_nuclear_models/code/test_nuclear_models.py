"""NE-02 tests -- the liquid drop model against Shultis & Faw §3.2 and against
the measured masses of Appendix B (../../data_tables/B1_atomic_masses.csv).

Run:  python3 test_nuclear_models.py
"""

import math

from nuclear_models import (
    A_V, A_S, A_C, A_A, A_P, R0_FM, M_H_U, M_N_U, M_P_U, U_MEV, MAGIC_NUMBERS,
    nuclear_radius, nuclear_volume, nucleon_number_density,
    parity_class, pairing_sign, pairing_term,
    semf_terms, semf_binding_energy, semf_binding_energy_per_nucleon,
    semf_nuclear_mass_u, semf_atomic_mass_u, semf_mass_excess_mev,
    most_stable_Z, most_stable_Z_rounded, isobar_masses,
    is_magic, is_doubly_magic, magic_gap,
    load_atomic_masses, measured_binding_energy,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- nuclear size ------------------------------------------------------------

def test_radius_law_and_constant_density():
    """R = 1.1 A^(1/3) fm [Eq. (3.13)] makes the nucleon density independent of A."""
    assert _approx(nuclear_radius(1), R0_FM)
    assert _approx(nuclear_radius(8), 2 * R0_FM)
    rho = [nucleon_number_density(A) for A in (4, 27, 56, 120, 208, 238)]
    for r in rho:
        assert _approx(r, rho[0], tol=1e-12)
    # the book quotes a central nucleon density of roughly 0.16-0.18 per fm^3
    assert 0.15 < rho[0] < 0.20
    # volume is proportional to A -- the "incompressible drop" statement
    assert _approx(nuclear_volume(216) / nuclear_volume(27), 8.0)


# --- pairing sign convention -------------------------------------------------

def test_parity_classes():
    assert parity_class(56, 26) == "even-even"     # N=30 even
    assert parity_class(14, 7) == "odd-odd"        # N=7 odd
    assert parity_class(235, 92) == "odd-even"     # N=143 odd, Z even
    assert parity_class(23, 11) == "odd-even"


def test_pairing_helps_even_even_and_hurts_odd_odd():
    """S&F p. 73: a_p is +11.2 MeV for odd-odd and -11.2 for even-even, entering
    BE as -a_p/sqrt(A).  Even-even therefore gains binding energy."""
    assert pairing_sign(56, 26) == -1.0
    assert pairing_sign(14, 7) == +1.0
    assert pairing_sign(235, 92) == 0.0
    assert pairing_term(56, 26) > 0                 # even-even: more bound
    assert pairing_term(14, 7) < 0                  # odd-odd: less bound
    assert pairing_term(235, 92) == 0.0
    assert _approx(pairing_term(56, 26), A_P / math.sqrt(56))
    # the two parabolas of an isobar are split by 2 a_p / sqrt(A)
    split = pairing_term(110, 46) - pairing_term(110, 45)
    assert _approx(split, 2 * A_P / math.sqrt(110))


# --- the mass formula --------------------------------------------------------

def test_terms_sum_to_binding_energy_and_have_right_signs():
    t = semf_terms(56, 26)
    assert _approx(sum(t.values()), semf_binding_energy(56, 26))
    assert t["volume"] > 0                          # only the bulk term binds
    assert t["surface"] < 0
    assert t["coulomb"] < 0
    assert t["asymmetry"] <= 0
    assert _approx(t["volume"], A_V * 56)
    assert _approx(t["surface"], -A_S * 56 ** (2 / 3))
    assert _approx(t["coulomb"], -A_C * 26 ** 2 / 56 ** (1 / 3))
    assert _approx(t["asymmetry"], -A_A * (56 - 52) ** 2 / 56)


def test_asymmetry_term_vanishes_when_N_equals_Z():
    for A, Z in [(4, 2), (16, 8), (40, 20)]:
        assert _approx(semf_terms(A, Z)["asymmetry"], 0.0)
    assert semf_terms(238, 92)["asymmetry"] < -100.0


def test_binding_energy_per_nucleon_peaks_in_the_iron_region():
    """The B/A curve rises steeply, peaks near A~55-60, then falls slowly."""
    best_A, best = None, -1e9
    for A in range(12, 250):
        Z = most_stable_Z_rounded(A)
        b = semf_binding_energy_per_nucleon(A, Z)
        if b > best:
            best, best_A = b, A
    assert 50 <= best_A <= 70, "peak at A=%d" % best_A
    assert 8.5 < best < 9.0
    # and the ends are lower -- the reason both fission and fusion release energy
    assert semf_binding_energy_per_nucleon(238, 92) < best
    assert semf_binding_energy_per_nucleon(16, 8) < best


def test_nuclear_and_atomic_mass_differ_by_Z_electrons():
    """M_atomic = m_nuclear + Z m_e, to the accuracy at which electron binding
    is neglected [S&F printed pp. 73-74]."""
    for A, Z in [(56, 26), (208, 82), (238, 92)]:
        diff = semf_atomic_mass_u(A, Z) - semf_nuclear_mass_u(A, Z)
        assert _approx(diff, Z * (M_H_U - M_P_U), tol=1e-9)


def test_mass_excess_is_small_relative_to_A():
    for A, Z in [(16, 8), (56, 26), (238, 92)]:
        assert abs(semf_mass_excess_mev(A, Z)) < 100.0
        assert _approx(semf_atomic_mass_u(A, Z),
                       A + semf_mass_excess_mev(A, Z) / U_MEV)


# --- the line of stability ---------------------------------------------------

def test_line_of_stability_bends_neutron_rich():
    """Eq. (3.18): Z/A starts near 1/2 and falls as Coulomb repulsion grows."""
    assert _approx(most_stable_Z(20) / 20, 0.48, tol=0.03)
    assert most_stable_Z(20) / 20 > most_stable_Z(238) / 238
    for A in range(20, 250, 10):
        assert most_stable_Z(A) <= A / 2.0
    # N/Z climbs monotonically with A
    ratios = []
    for A in (40, 80, 120, 160, 200, 238):
        Z = most_stable_Z(A)
        ratios.append((A - Z) / Z)
    assert all(b > a for a, b in zip(ratios, ratios[1:]))
    assert 1.5 < ratios[-1] < 1.6


def test_most_stable_Z_matches_known_stable_nuclides():
    """Rounded Z(A) should land on (or within one of) the real stable nuclide."""
    for A, Z_true in [(56, 26), (27, 13), (40, 20), (120, 50), (208, 82)]:
        assert abs(most_stable_Z_rounded(A) - Z_true) <= 1, \
            "A=%d predicted Z=%d, stable Z=%d" % (A, most_stable_Z_rounded(A), Z_true)


def test_most_stable_Z_minimises_the_isobar_mass():
    """Eq. (3.18) is the stationary point of Eq. (3.16) -- verify numerically,
    holding the parity class fixed so pairing does not confuse the comparison."""
    A = 110
    even = [(Z, m) for Z, m in isobar_masses(A, 40, 55) if Z % 2 == 0]
    zmin = min(even, key=lambda t: t[1])[0]
    assert abs(zmin - most_stable_Z(A)) <= 1.5


def test_isobar_110_reproduces_the_book_figure():
    """S&F Fig. 3.13 (printed p. 75): in the A=110 isobar the two stable nuclides
    lie either side of the predicted stability maximum.  They are 110Pd (Z=46)
    and 110Cd (Z=48), and Z(110) = 47.4 sits between them."""
    z = most_stable_Z(110)
    assert 46 < z < 48
    masses = dict(isobar_masses(110, 43, 51))
    # even-even members lie on the lower curve, odd-odd on the upper one
    for z_even, z_odd in [(46, 45), (48, 47), (44, 43)]:
        assert masses[z_even] < masses[z_odd]


def test_isobar_masses_form_two_curves():
    rows = isobar_masses(64, 26, 34)
    ee = [m for Z, m in rows if parity_class(64, Z) == "even-even"]
    oo = [m for Z, m in rows if parity_class(64, Z) == "odd-odd"]
    assert ee and oo
    assert min(ee) < min(oo)          # the even-even curve lies below


# --- magic numbers -----------------------------------------------------------

def test_magic_number_helpers():
    for m in MAGIC_NUMBERS:
        assert is_magic(m)
    assert not is_magic(1)
    assert not is_magic(100)
    assert is_doubly_magic(4, 2)      # 4He
    assert is_doubly_magic(16, 8)     # 16O
    assert is_doubly_magic(40, 20)    # 40Ca
    assert is_doubly_magic(48, 20)    # 48Ca, N=28
    assert is_doubly_magic(208, 82)   # 208Pb, N=126
    assert not is_doubly_magic(56, 26)
    assert magic_gap(208, 82) == (0, 0)
    assert magic_gap(56, 26) == (2, 2)


# --- against the measured masses of Appendix B -------------------------------

def test_mass_table_loads_and_anchors():
    t = load_atomic_masses()
    assert len(t) > 2800
    assert _approx(t[(6, 12)], 12.0)                  # the definition of u
    assert _approx(t[(92, 235)], 235.0439231, tol=1e-9)
    assert _approx(t[(1, 1)], 1.0078250321, tol=1e-9)


def test_measured_binding_energies_are_right():
    """BE from the measured mass, against values every nuclear text quotes."""
    assert _approx(measured_binding_energy(4, 2), 28.30, tol=2e-3)
    assert _approx(measured_binding_energy(56, 26), 492.25, tol=2e-3)
    assert _approx(measured_binding_energy(208, 82), 1636.4, tol=2e-3)
    assert _approx(measured_binding_energy(235, 92) / 235, 7.591, tol=2e-3)


def test_semf_tracks_measured_masses_for_medium_and_heavy_nuclei():
    """The drop model is a bulk model: it should be good to ~0.2 MeV/nucleon for
    A >= 40 and poor for the lightest nuclei."""
    t = load_atomic_masses()
    worst, worst_n = 0.0, None
    n = 0
    for A in range(40, 240):
        Z = most_stable_Z_rounded(A)
        if (Z, A) not in t:
            continue
        err = abs(semf_binding_energy(A, Z) / A - measured_binding_energy(A, Z, t) / A)
        if err > worst:
            worst, worst_n = err, (A, Z)
        n += 1
    assert n > 150
    assert worst < 0.25, "worst B/A error %.3f MeV at %r" % (worst, worst_n)
    # 4He is where a "drop" of four nucleons is a bad idea
    assert abs(semf_binding_energy(4, 2) / 4 - measured_binding_energy(4, 2) / 4) > 1.0


def test_shell_closures_show_up_as_extra_binding():
    """The liquid drop model is smooth in A and Z, so it must *under*-predict the
    binding of doubly magic nuclei.  That residual is the shell effect (§3.2.7)."""
    for A, Z in [(16, 8), (40, 20), (48, 20), (208, 82)]:
        resid = measured_binding_energy(A, Z) - semf_binding_energy(A, Z)
        assert resid > 3.0, "no shell surplus at A=%d Z=%d (%.2f MeV)" % (A, Z, resid)


def test_invalid_inputs_raise():
    for A, Z in [(0, 0), (-4, 2), (10, 11), (10, -1), (10.5, 5)]:
        try:
            semf_binding_energy(A, Z)
        except ValueError:
            pass
        else:
            raise AssertionError("A=%r Z=%r should be rejected" % (A, Z))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
