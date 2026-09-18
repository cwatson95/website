"""NE-05 tests -- decay energetics against Shultis & Faw §§5.1-5.4, the measured
masses of Appendix B, and the measured emission energies of Appendix D.

The strongest test here is the cross-appendix one: Q_beta- computed from atomic
masses (Appendix B) must equal the beta endpoint measured by spectroscopy
(Appendix D).  They are independent data sets.

Run:  python3 test_decay_modes.py
"""

from decay_modes import (
    M_E_U, U_MEV, TWO_ME_MEV,
    load_atomic_masses, atomic_mass, has_nuclide, daughter_of,
    q_alpha, alpha_kinetic_energy, daughter_recoil_energy,
    q_beta_minus, q_beta_plus, q_electron_capture,
    q_isomeric_transition, q_neutron_emission, q_proton_emission,
    allowed_decay_modes, dominant_decay_mode, beta_endpoint,
    load_decay_radiation, measured_emissions,
)


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


TAB = load_atomic_masses()


# --- bookkeeping -------------------------------------------------------------

def test_daughters():
    assert daughter_of(238, 92, "alpha") == (234, 90)
    assert daughter_of(137, 55, "beta-") == (137, 56)
    assert daughter_of(22, 11, "beta+") == (22, 10)
    assert daughter_of(7, 4, "ec") == (7, 3)
    assert daughter_of(137, 56, "it") == (137, 56)
    try:
        daughter_of(1, 1, "spontaneous-combustion")
    except ValueError:
        pass
    else:
        raise AssertionError("unknown mode should be rejected")


def test_two_electron_mass_penalty_is_1022_keV():
    """The beta-plus correction is 2 m_e c^2 = 1.022 MeV [Eq. (5.18)]."""
    assert _approx(TWO_ME_MEV, 1.02200, tol=1e-4)
    assert _approx(TWO_ME_MEV, 2 * M_E_U * U_MEV)


def test_beta_plus_and_ec_differ_by_exactly_that_penalty():
    """Both connect the same parent and daughter; beta-plus just costs 1.022 MeV
    more [Eqs. (5.18) vs (5.22)].  This is why the two always compete."""
    for A, Z in [(22, 11), (64, 29), (40, 19), (7, 4), (18, 9)]:
        Ad, Zd = daughter_of(A, Z, "ec")
        if not has_nuclide(Ad, Zd, TAB):
            continue
        assert _approx(q_electron_capture(A, Z, TAB) - q_beta_plus(A, Z, TAB),
                       TWO_ME_MEV, tol=1e-9)


# --- alpha decay  [Eqs. (5.7), (5.11), (5.12)] ------------------------------

def test_alpha_q_values_match_known_decays():
    assert _approx(q_alpha(238, 92, TAB), 4.2703, tol=1e-3)
    assert _approx(q_alpha(226, 88, TAB), 4.8706, tol=1e-3)
    assert _approx(q_alpha(222, 86, TAB), 5.5903, tol=1e-3)
    assert _approx(q_alpha(210, 84, TAB), 5.4071, tol=1e-3)


def test_alpha_kinetic_energies_match_measured_line_energies():
    """Two-body kinematics gives the alpha a sharp energy, and it is the one
    tabulated in every chart of the nuclides."""
    assert _approx(alpha_kinetic_energy(238, 92, TAB), 4.198, tol=1e-3)
    assert _approx(alpha_kinetic_energy(226, 88, TAB), 4.784, tol=1e-3)
    assert _approx(alpha_kinetic_energy(210, 84, TAB), 5.304, tol=1e-3)
    # and against Appendix D's measured alpha lines
    rows = measured_emissions("222Rn", "alpha")
    assert rows
    e_meas = max(float(r["E_keV"]) for r in rows) / 1000.0
    assert _approx(alpha_kinetic_energy(222, 86, TAB), e_meas, tol=2e-3)


def test_alpha_energy_split_conserves_energy_and_momentum():
    """E_alpha + E_D = Q, and the split is by inverse mass [Eqs. (5.11)-(5.12)]."""
    for A, Z in [(238, 92), (226, 88), (241, 95)]:
        q = q_alpha(A, Z, TAB)
        ea = alpha_kinetic_energy(A, Z, TAB)
        ed = daughter_recoil_energy(A, Z, TAB)
        assert _approx(ea + ed, q, tol=1e-9)
        Ad, Zd = daughter_of(A, Z, "alpha")
        MD, Ma = atomic_mass(Ad, Zd, TAB), atomic_mass(4, 2, TAB)
        assert _approx(ea, q * MD / (MD + Ma))
        # equal and opposite momenta: p^2 = 2mE must match
        assert _approx(MD * ed, Ma * ea, tol=1e-9)
        # the alpha takes ~98% of the energy
        assert 0.97 < ea / q < 0.99


def test_excited_daughter_reduces_alpha_energy():
    base = q_alpha(226, 88, TAB)
    assert _approx(q_alpha(226, 88, TAB, excitation=0.186), base - 0.186, tol=1e-9)
    assert alpha_kinetic_energy(226, 88, TAB, excitation=0.186) < alpha_kinetic_energy(226, 88, TAB)


# --- beta decay  [Eqs. (5.14), (5.16), (5.18), (5.22)] ---------------------

def test_beta_minus_q_matches_endpoints_for_ground_state_emitters():
    """THE cross-appendix check.  For nuclides that decay essentially entirely
    to the daughter's *ground* state, Q computed from Appendix B atomic masses
    must equal the beta endpoint measured spectroscopically in Appendix D.
    Two independent data sets, so agreement validates both."""
    checks = [(3, 1, "3H", 18.6), (14, 6, "14C", 156.5),
              (32, 15, "32P", 1710.4), (90, 38, "90Sr", 546.0)]
    for A, Z, name, expect in checks:
        rows = [r for r in measured_emissions(name, "beta") if r["E_max_keV"]]
        assert rows, name
        e_meas = max(float(r["E_max_keV"]) for r in rows)
        assert _approx(e_meas, expect, tol=1e-3)
        q_keV = q_beta_minus(A, Z, TAB) * 1000.0
        assert abs(q_keV - e_meas) < 1.0, \
            "%s: Q=%.2f keV vs Appendix D endpoint %.2f keV" % (name, q_keV, e_meas)


def test_total_decay_energy_closes_for_a_cascade():
    """When the beta feeds an excited level, the endpoint alone is *not* Q --
    the gamma cascade carries the rest.  For 60Co the 99.94% branch stops
    2505.7 keV short of the ground state and two gammas make up the difference:

        E_beta,max + E_gamma1 + E_gamma2  ==  Q_beta-

    This is energy conservation checked across Appendices B and D."""
    q_keV = q_beta_minus(60, 27, TAB) * 1000.0
    endpoint = max(float(r["E_max_keV"])
                   for r in measured_emissions("60Co", "beta") if r["E_max_keV"])
    gammas = sorted(float(r["E_keV"])
                    for r in measured_emissions("60Co", "gamma_xray") if r["E_keV"])
    assert _approx(endpoint, 317.9, tol=1e-3)
    assert len(gammas) == 2
    total = endpoint + sum(gammas)
    assert abs(total - q_keV) < 1.0, "60Co: cascade %.1f keV vs Q %.1f keV" % (total, q_keV)


def test_cesium137_shows_a_small_appendix_disagreement():
    """137Cs is the one place this cross-check does *not* close to a keV.

    Appendix D gives the 94.43% branch an endpoint of 511.5 keV feeding the
    661.66 keV level, and the weak ground-state branch an endpoint of 1173.2
    keV -- internally consistent, both implying a total decay energy of
    1173.2 keV.  Appendix B's masses give 1176.5 keV.  The 3.3 keV gap (0.3%)
    is a disagreement between the two evaluations, not an arithmetic error;
    the modern value is 1175.6 keV, between the two.  Recorded here so the
    discrepancy is visible rather than silently absorbed into a loose tolerance."""
    q_keV = q_beta_minus(137, 55, TAB) * 1000.0
    endpoint_gs = max(float(r["E_max_keV"])
                      for r in measured_emissions("137Cs", "beta") if r["E_max_keV"])
    assert _approx(q_keV, 1176.5, tol=1e-3)
    assert _approx(endpoint_gs, 1173.2, tol=1e-3)
    gap = q_keV - endpoint_gs
    assert 3.0 < gap < 3.6, "137Cs B-vs-D gap is now %.2f keV" % gap


def test_beta_endpoint_equals_q():
    """Eq. (5.16): the beta spectrum runs from 0 to Q, because the antineutrino
    takes the rest.  Contrast the sharp alpha line above."""
    for A, Z in [(3, 1), (14, 6), (137, 55)]:
        assert _approx(beta_endpoint(A, Z, "beta-", TAB), q_beta_minus(A, Z, TAB))


def test_beta_minus_needs_no_electron_correction():
    """Eq. (5.14): atomic masses cancel exactly, unlike beta-plus."""
    for A, Z in [(3, 1), (14, 6), (137, 55)]:
        Ad, Zd = daughter_of(A, Z, "beta-")
        raw = (atomic_mass(A, Z, TAB) - atomic_mass(Ad, Zd, TAB)) * U_MEV
        assert _approx(q_beta_minus(A, Z, TAB), raw)


def test_electron_capture_only_window():
    """When 0 < Q_EC < 1.022 MeV, positron emission is forbidden and capture is
    the only open channel.  7Be, 55Fe, 51Cr and 125I all sit in that window and
    all are pure EC emitters."""
    for A, Z, name in [(7, 4, "7Be"), (55, 26, "55Fe"), (51, 24, "51Cr"), (125, 53, "125I")]:
        qec = q_electron_capture(A, Z, TAB)
        qbp = q_beta_plus(A, Z, TAB)
        assert qec > 0, name
        assert qbp < 0, name
        assert 0 < qec < TWO_ME_MEV, name


def test_potassium_40_branches_both_ways():
    """40K is the classic branching nuclide: beta-minus to 40Ca and EC to 40Ar,
    both energetically open.  The 40Ar branch is why potassium-argon dating works."""
    assert q_beta_minus(40, 19, TAB) > 0
    assert q_electron_capture(40, 19, TAB) > 0
    assert _approx(q_beta_minus(40, 19, TAB), 1.311, tol=1e-2)
    assert _approx(q_electron_capture(40, 19, TAB), 1.505, tol=1e-2)


def test_stable_nuclides_have_no_open_beta_channel():
    for A, Z in [(56, 26), (16, 8), (12, 6), (208, 82)]:
        assert q_beta_minus(A, Z, TAB) < 0
        assert q_beta_plus(A, Z, TAB) < 0


# --- other modes -------------------------------------------------------------

def test_isomeric_transition_is_just_the_excitation():
    assert _approx(q_isomeric_transition(0.6616), 0.6616)
    try:
        q_isomeric_transition(-1.0)
    except ValueError:
        pass
    else:
        raise AssertionError("negative excitation should be rejected")


def test_nucleon_emission_is_closed_for_stable_nuclides():
    """Q_n is minus the neutron separation energy, so it is negative wherever
    S_n > 0 -- i.e. everywhere on the valley floor."""
    for A, Z in [(56, 26), (208, 82), (238, 92)]:
        assert q_neutron_emission(A, Z, TAB) < 0
        assert q_proton_emission(A, Z, TAB) < 0


# --- mode prediction ---------------------------------------------------------

def test_dominant_mode_agrees_with_observation():
    """Energetics alone gets the direction right for the standard nuclides."""
    for A, Z, expect in [(3, 1, "beta-"), (14, 6, "beta-"), (137, 55, "beta-"),
                         (60, 27, "beta-"), (90, 38, "beta-"),
                         (238, 92, "alpha"), (226, 88, "alpha"), (210, 84, "alpha"),
                         (7, 4, "ec"), (55, 26, "ec")]:
        got = dominant_decay_mode(A, Z, TAB)
        assert got == expect, "%d/%d predicted %r, expected %r" % (A, Z, got, expect)


def test_allowed_modes_are_energetically_positive():
    modes = allowed_decay_modes(238, 92, TAB)
    assert "alpha" in modes and modes["alpha"] > 0
    for q in modes.values():
        assert q > 0
    assert allowed_decay_modes(56, 26, TAB) == {}      # 56Fe is stable


# --- Appendix D wiring -------------------------------------------------------

def test_appendix_d_loads_and_has_the_famous_lines():
    rows = load_decay_radiation()
    assert len(rows) > 1000
    g60 = [float(r["E_keV"]) for r in measured_emissions("60Co", "gamma_xray") if r["E_keV"]]
    assert any(abs(e - 1173.2) < 0.5 for e in g60)
    assert any(abs(e - 1332.5) < 0.5 for e in g60)
    g137 = [float(r["E_keV"]) for r in measured_emissions("137mBa", "gamma_xray") if r["E_keV"]]
    assert any(abs(e - 661.6) < 0.5 for e in g137)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
