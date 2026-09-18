"""NE-03 tests -- binding and separation energies against Shultis & Faw §§4.1-4.3
and the measured masses of Appendix B.

Run:  python3 test_binding_energy.py
"""

from binding_energy import (
    M_N_U, M_H_U, M_E_U, U_MEV, MAGIC_NUMBERS,
    load_atomic_masses, atomic_mass, has_nuclide,
    atomic_to_nuclear_mass, mass_excess_mev, mass_defect_u,
    binding_energy, binding_energy_per_nucleon,
    neutron_separation_energy, proton_separation_energy,
    two_neutron_separation_energy, alpha_separation_energy,
    binding_energy_curve, most_bound_nuclide,
    pairing_stagger, electron_binding_fraction,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


TAB = load_atomic_masses()


# --- masses ------------------------------------------------------------------

def test_mass_table_anchors():
    assert _approx(atomic_mass(12, 6, TAB), 12.0)          # defines the scale
    assert _approx(atomic_mass(1, 1, TAB), 1.0078250321, tol=1e-9)
    assert _approx(atomic_mass(235, 92, TAB), 235.0439231, tol=1e-9)
    assert len(TAB) > 2800


def test_atomic_minus_nuclear_is_Z_electrons():
    """S&F Eq. (4.8): M = m + Z m_e - BE_Ze/c^2, the last term dropped."""
    for A, Z in [(1, 1), (56, 26), (238, 92)]:
        assert _approx(atomic_mass(A, Z, TAB) - atomic_to_nuclear_mass(A, Z, TAB),
                       Z * M_E_U)


def test_mass_excess_consistency():
    for A, Z in [(12, 6), (56, 26), (238, 92)]:
        assert _approx(atomic_mass(A, Z, TAB),
                       A + mass_excess_mev(A, Z, TAB) / U_MEV)
    assert _approx(mass_excess_mev(12, 6, TAB), 0.0, tol=1e-9)   # 12C by definition


# --- binding energy  [Eq. (4.12)] -------------------------------------------

def test_binding_energies_match_standard_values():
    assert _approx(binding_energy(2, 1, TAB), 2.2246, tol=1e-3)      # deuteron
    assert _approx(binding_energy(4, 2, TAB), 28.296, tol=1e-3)      # alpha
    assert _approx(binding_energy(12, 6, TAB), 92.162, tol=1e-3)
    assert _approx(binding_energy(16, 8, TAB), 127.62, tol=1e-3)
    assert _approx(binding_energy(56, 26, TAB), 492.25, tol=1e-3)
    assert _approx(binding_energy(208, 82, TAB), 1636.4, tol=1e-3)


def test_binding_energy_is_defect_times_c2():
    for A, Z in [(4, 2), (56, 26), (238, 92)]:
        assert _approx(binding_energy(A, Z, TAB), mass_defect_u(A, Z, TAB) * U_MEV)
        # the nuclide is always lighter than its separated parts
        assert mass_defect_u(A, Z, TAB) > 0


def test_free_nucleons_have_zero_binding_energy():
    """A single free nucleon has nothing to be bound to, so BE = 0 identically."""
    assert abs(binding_energy(1, 1, TAB)) < 1e-8         # a lone proton: exact
    # A lone neutron is *not* exact, and the reason is a book-internal
    # inconsistency rather than a rounding error: Table A.1 (printed p. 555)
    # gives m_n = 1.008 664 915 6 u while Appendix B gives 1.008 664 923 3 u.
    # The gap is 7.7e-9 u = 7.2 eV -- irrelevant beside MeV-scale binding
    # energies, but it is not zero, and it is worth knowing which table a
    # calculation is leaning on.
    lone_neutron = binding_energy(1, 0, TAB)
    assert abs(lone_neutron) < 1e-4                      # MeV
    assert _approx(abs(lone_neutron),
                   abs(M_N_U - atomic_mass(1, 0, TAB)) * U_MEV, tol=1e-6)


def test_binding_energy_per_nucleon_range():
    """Every bound nuclide beyond hydrogen sits between about 1 and 9 MeV/nucleon."""
    for A, Z, b in binding_energy_curve(TAB, z_tolerance=0):
        if A >= 2:
            assert 0.5 < b < 9.0, "A=%d Z=%d has B/A=%.3f" % (A, Z, b)


def test_most_bound_nuclide_is_nickel_62():
    """The peak of the B/A curve is 62Ni at 8.79 MeV/nucleon -- not 56Fe, which
    is the more famous but slightly less bound answer."""
    A, Z, b = most_bound_nuclide(TAB)
    assert (A, Z) == (62, 28)
    assert _approx(b, 8.7945, tol=1e-4)
    assert binding_energy_per_nucleon(56, 26, TAB) < b
    # ... but only just: the top of the curve is very flat
    assert b - binding_energy_per_nucleon(56, 26, TAB) < 0.01


# --- separation energies  [Eqs. (4.13)-(4.14)] ------------------------------

def test_oxygen16_neutron_separation_energy_matches_example_4_3():
    """S&F Example 4.3 (printed p. 87): S_n(16O) = 15.66 MeV."""
    assert _approx(neutron_separation_energy(16, 8, TAB), 15.66, tol=1e-3)
    # "an exceptionally high value for a single nucleon": nearly twice the 7.98
    # MeV/nucleon average, because 16O is doubly magic and removing a neutron
    # breaks the N=8 closure
    assert _approx(binding_energy_per_nucleon(16, 8, TAB), 7.98, tol=1e-3)
    assert neutron_separation_energy(16, 8, TAB) > 1.9 * binding_energy_per_nucleon(16, 8, TAB)
    # the very next neutron is far more loosely held
    assert neutron_separation_energy(17, 8, TAB) < 5.0


def test_separation_energy_two_formulations_agree():
    """Eq. (4.13) via masses and Eq. (4.14) via binding energies must coincide."""
    for A, Z in [(16, 8), (57, 26), (209, 82)]:
        by_mass = (atomic_mass(A - 1, Z, TAB) + M_N_U - atomic_mass(A, Z, TAB)) * U_MEV
        assert _approx(by_mass, neutron_separation_energy(A, Z, TAB), tol=1e-6)


def test_proton_separation_energy_definition():
    for A, Z in [(16, 8), (56, 26)]:
        by_mass = (atomic_mass(A - 1, Z - 1, TAB) + M_H_U - atomic_mass(A, Z, TAB)) * U_MEV
        assert _approx(by_mass, proton_separation_energy(A, Z, TAB), tol=1e-6)


def test_two_neutron_separation_is_the_sum_of_two_one_neutron_steps():
    for A, Z in [(18, 8), (60, 26), (210, 82)]:
        s2 = two_neutron_separation_energy(A, Z, TAB)
        s1 = (neutron_separation_energy(A, Z, TAB)
              + neutron_separation_energy(A - 1, Z, TAB))
        assert _approx(s2, s1, tol=1e-6)


def test_pairing_stagger_in_the_oxygen_chain():
    """S_n alternates: an even-N nuclide is harder to break than its odd-N
    neighbour, by roughly 2 a_p/sqrt(A) ~ 2-4 MeV (the ~NE-02 pairing term)."""
    even = [neutron_separation_energy(A, 8, TAB) for A in (16, 18, 20)]
    odd = [neutron_separation_energy(A, 8, TAB) for A in (17, 19)]
    assert min(even) > max(odd)
    assert pairing_stagger(16, 8, TAB) > 5.0        # S_n(16O) - S_n(17O)
    # the stagger is a real alternation, not a trend
    assert neutron_separation_energy(18, 8, TAB) > neutron_separation_energy(17, 8, TAB)


def test_shell_closure_drops_the_separation_energy():
    """Just past a magic neutron number the next neutron is much less bound."""
    for Z, A_closed in [(82, 208), (58, 140)]:      # N=126 and N=82
        inside = neutron_separation_energy(A_closed, Z, TAB)
        outside = neutron_separation_energy(A_closed + 1, Z, TAB)
        assert inside - outside > 2.5, \
            "no shell drop at Z=%d A=%d (%.2f -> %.2f)" % (Z, A_closed, inside, outside)


def test_alpha_separation_energy_changes_sign_for_heavy_nuclides():
    """S_alpha > 0 means alpha emission costs energy; S_alpha < 0 means the
    nuclide is energetically unstable to it (the Q-value is -S_alpha)."""
    assert alpha_separation_energy(56, 26, TAB) > 0
    assert alpha_separation_energy(120, 50, TAB) > 0
    for A, Z in [(226, 88), (238, 92), (235, 92)]:
        assert alpha_separation_energy(A, Z, TAB) < 0
    # 226Ra: Q_alpha = 4.87 MeV, the textbook value
    assert _approx(-alpha_separation_energy(226, 88, TAB), 4.87, tol=5e-3)


def test_separation_energies_are_positive_for_stable_nuclides():
    for A, Z in [(16, 8), (56, 26), (208, 82), (238, 92)]:
        assert neutron_separation_energy(A, Z, TAB) > 0
        assert proton_separation_energy(A, Z, TAB) > 0


# --- the approximations the derivation makes ---------------------------------

def test_electron_binding_is_negligible():
    """S&F p. 81: 13.6 eV is 1.4e-8 u, negligible against nuclear binding."""
    assert _approx(13.6 / (U_MEV * 1e6), 1.46e-8, tol=1e-2)
    assert electron_binding_fraction(2, 1, 13.6, TAB) < 1e-5
    assert electron_binding_fraction(238, 92, 1e5, TAB) < 1e-4


def test_curve_and_invalid_inputs():
    curve = binding_energy_curve(TAB, z_tolerance=1)
    assert len(curve) > 400
    assert all(a <= b for a, b in zip([r[0] for r in curve], [r[0] for r in curve][1:]))
    for A, Z in [(0, 0), (10, 11), (-1, 1)]:
        try:
            binding_energy(A, Z, TAB)
        except (ValueError, KeyError):
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
