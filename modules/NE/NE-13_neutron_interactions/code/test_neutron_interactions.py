"""NE-13 tests -- neutron interactions against Shultis & Faw §7.4, its
Example 7.5, and the extracted Appendices C.1 and C.2.

Run:  python3 test_neutron_interactions.py
"""

import math

from neutron_interactions import (
    AVOGADRO, BARN_CM2, M_N_U, K_BOLTZ_EV_PER_K,
    E_THERMAL_EV, V_THERMAL_CM_S, T_THERMAL_K,
    NUCLIDE_CLASS, RESONANCE_CHARACTER, SECONDARY_NEUTRON_THRESHOLDS,
    load_thermal_cross_sections, load_activation_data,
    absorption_cross_section, scattering_cross_section, total_cross_section,
    fission_cross_section, capture_to_fission_ratio, eta_neutrons_per_absorption,
    neutron_speed, neutron_energy_from_speed, maxwellian_most_probable_energy,
    one_over_v_cross_section, light_nucleus_total_cross_section,
    classify_nuclide, resonance_character,
    macroscopic_cross_section, atom_density, mean_free_path,
    activation_rate, activation_activity, saturation_activity,
    is_fissile, is_fissionable,
)

XS = load_thermal_cross_sections()


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the thermal reference point -------------------------------------------

def test_2200_metres_per_second_is_0_0253_eV():
    """The whole of Appendix C.1 is quoted at one point: 0.0253 eV, 2200 m/s,
    293.6 K.  All three must agree."""
    assert _approx(neutron_speed(E_THERMAL_EV), V_THERMAL_CM_S, tol=2e-3)
    assert _approx(neutron_energy_from_speed(V_THERMAL_CM_S), E_THERMAL_EV, tol=4e-3)
    assert _approx(maxwellian_most_probable_energy(T_THERMAL_K), E_THERMAL_EV, tol=2e-3)
    for e in (1e-3, 0.0253, 1.0, 1e6):
        assert _approx(neutron_energy_from_speed(neutron_speed(e)), e)
    # a 2 MeV fission neutron is eight decades up in energy, four in speed
    assert _approx(neutron_speed(2e6) / V_THERMAL_CM_S, 8890.0, tol=2e-2)
    for fn in (neutron_speed, neutron_energy_from_speed):
        try:
            fn(-1.0)
        except ValueError:
            pass
        else:
            raise AssertionError("%s should reject negatives" % fn.__name__)


# --- the 1/v law  [Eq. (7.40)] --------------------------------------------

def test_one_over_v_law():
    """sigma_a ~ 1/sqrt(E) ~ 1/v.  A slow neutron lingers near the nucleus in
    proportion to 1/v, so capture scales the same way."""
    s0 = absorption_cross_section("1H", XS)
    assert _approx(one_over_v_cross_section(s0, E_THERMAL_EV), s0)
    assert _approx(one_over_v_cross_section(s0, E_THERMAL_EV / 4.0), 2.0 * s0)
    # exactly inverse in SPEED, which is the physical statement.  Note the
    # reference speed must be the one that corresponds to E_THERMAL_EV exactly;
    # the nominal 2200 m/s is 0.02525 eV, 0.2% away, so using it here would
    # compare two slightly different reference points.
    v_ref = neutron_speed(E_THERMAL_EV)
    for e in (1e-4, 1e-2, 1.0, 100.0):
        assert _approx(one_over_v_cross_section(s0, e) / s0, v_ref / neutron_speed(e))
    # and the nominal 2200 m/s is within 0.3% of it
    assert _approx(v_ref, V_THERMAL_CM_S, tol=3e-3)
    # slowing from 1 keV to thermal buys a factor of 199
    assert _approx(one_over_v_cross_section(s0, E_THERMAL_EV)
                   / one_over_v_cross_section(s0, 1000.0), 198.8, tol=1e-2)
    for bad in ((1.0, 0.0), (1.0, -1.0), (-1.0, 1.0)):
        try:
            one_over_v_cross_section(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_light_nucleus_two_term_form():
    """Eq. (7.40): sigma_t = sigma_1 + sigma_2/sqrt(E) -- a flat elastic term
    plus a 1/v capture term, dominating at opposite ends."""
    s1, s2 = 4.0, 0.05
    assert _approx(light_nucleus_total_cross_section(s1, s2, 1000.0), s1, tol=1e-3)
    assert light_nucleus_total_cross_section(s1, s2, 1e-6) > 10 * s1
    prev = float("inf")
    for e in (1e-4, 1e-2, 1.0, 100.0, 999.0):
        v = light_nucleus_total_cross_section(s1, s2, e)
        assert v < prev
        prev = v


def test_eq_7_40_refuses_to_extrapolate_past_its_stated_range():
    """S&F state Eq. (7.40) for E < 1 keV, because resonances appear above that
    and no smooth form describes them.  The function raises rather than
    returning a confident wrong number."""
    light_nucleus_total_cross_section(4.0, 0.05, 999.0)      # inside range
    for e in (1001.0, 1e5, 2e6):
        try:
            light_nucleus_total_cross_section(4.0, 0.05, e)
        except ValueError:
            pass
        else:
            raise AssertionError("%.4g eV is above the stated range" % e)


# --- the tables: erratic where photon cross sections are smooth -----------

def test_cross_sections_vary_wildly_between_neighbouring_isotopes():
    """The organising contrast with ~NE-12.  Photon coefficients follow Z^4, Z
    and Z^2; neutron cross sections follow nothing.  Isotopes of the SAME
    element differ by up to six orders of magnitude."""
    r_h = absorption_cross_section("1H", XS) / absorption_cross_section("2H", XS)
    assert _approx(r_h, 658.0, tol=1e-2), "%.1f" % r_h
    r_b = absorption_cross_section("10B", XS) / absorption_cross_section("11B", XS)
    assert r_b > 1e5, "%.4g" % r_b
    r_u = fission_cross_section("235U", XS) / fission_cross_section("238U", XS)
    assert r_u > 1e7, "%.4g" % r_u
    # no monotone trend with A anywhere in the table -- it should look like noise
    by_a = sorted((v["A"], absorption_cross_section(k, XS)) for k, v in XS.items())
    rises = sum(1 for i in range(1, len(by_a)) if by_a[i][1] > by_a[i - 1][1])
    assert 0.25 < rises / float(len(by_a) - 1) < 0.75


def test_absorption_excludes_scattering():
    """1H scatters 30.5 b and absorbs 0.333 b -- 92x more scattering than
    absorption, exactly the combination a moderator needs (~NE-08)."""
    assert _approx(absorption_cross_section("1H", XS), 0.333)
    assert _approx(scattering_cross_section("1H", XS), 30.5)
    assert _approx(scattering_cross_section("1H", XS)
                   / absorption_cross_section("1H", XS), 91.6, tol=1e-2)
    assert (scattering_cross_section("12C", XS)
            / absorption_cross_section("12C", XS)) > 1000
    assert absorption_cross_section("10B", XS) > 3000
    for n in ("1H", "12C", "16O"):
        assert total_cross_section(n, XS) >= absorption_cross_section(n, XS)


def test_nuclide_classification_boundaries_are_the_books():
    """S&F §7.4.1: light A < 25, heavy A > 150, intermediate between."""
    assert classify_nuclide(1) == "light" and classify_nuclide(24) == "light"
    assert classify_nuclide(25) == "intermediate"
    assert classify_nuclide(150) == "intermediate"
    assert classify_nuclide(151) == "heavy"
    assert NUCLIDE_CLASS["light"][1] == 25 and NUCLIDE_CLASS["heavy"][0] == 150
    try:
        classify_nuclide(0)
    except ValueError:
        pass
    else:
        raise AssertionError("A = 0 should be rejected")


def test_resonances_get_lower_narrower_and_denser_with_mass():
    """Heavier nuclei have denser level schemes, so resonances move down in
    energy and narrow.  Heavy nuclides become unresolvable above a few keV;
    only H and D have none at all."""
    assert resonance_character(1)["energy"] == "keV to MeV"
    assert resonance_character(238)["energy"] == "eV region"
    assert "1 eV or less" in resonance_character(238)["width"]
    assert "unresolved" in resonance_character(238)["note"]
    assert "none at all" in resonance_character(2)["note"]
    for A in (1, 12, 56, 238):
        assert set(resonance_character(A)) == {"energy", "width", "note"}


def test_the_two_anomalous_n2n_thresholds():
    """S&F §7.4.1: (n,2n) usually needs ~8 MeV, but D and Be are anomalously
    low -- 3.3 and 1.84 MeV -- with no inelastic competition.  That is why
    beryllium is a neutron MULTIPLIER in fusion blankets (~NE-10, ~NE-24)."""
    assert SECONDARY_NEUTRON_THRESHOLDS["9Be"] < SECONDARY_NEUTRON_THRESHOLDS["2H"]
    assert SECONDARY_NEUTRON_THRESHOLDS["2H"] < SECONDARY_NEUTRON_THRESHOLDS["typical"]
    assert _approx(SECONDARY_NEUTRON_THRESHOLDS["9Be"], 1.84)
    assert _approx(SECONDARY_NEUTRON_THRESHOLDS["2H"], 3.3)
    # Be sits below the 2 MeV mean fission-neutron energy of ~NE-09; D does not
    assert SECONDARY_NEUTRON_THRESHOLDS["9Be"] < 2.0 < SECONDARY_NEUTRON_THRESHOLDS["2H"]


# --- activation  [Example 7.5] --------------------------------------------

def test_reproduces_example_7_5():
    """S&F Example 7.5 (printed p. 204): 2 g of 55Mn, 1e13 cm^-2 s^-1, 2 min.
    The book gets 2.609e10 Bq using the SHORT-IRRADIATION approximation, which
    it states explicitly ('very small compared to the half-life') and so writes
    A = lambda R t.  The exact form R[1-exp(-lambda t)] gives 2.598e10.

    Both are checked, and their ratio is the leading correction lambda*t/2."""
    act = load_activation_data()
    mn = act["56Mn"]
    assert _approx(mn["sigma_b"], 13.3)
    assert mn["parent"] == "55Mn"
    assert _approx(mn["parent_abundance_pct"], 100.0)

    t_half = 2.579 * 3600.0
    lam = math.log(2.0) / t_half
    assert _approx(lam, 7.466e-5, tol=1e-3)

    r = activation_rate(2.0, 55.0, mn["sigma_b"], 1e13)
    exact = activation_activity(2.0, 55.0, mn["sigma_b"], 1e13, 120.0, t_half)
    book = r * lam * 120.0

    assert _approx(book, 2.609e10, tol=1e-3), "%.4e" % book
    assert _approx(exact, 2.598e10, tol=1e-3), "%.4e" % exact
    assert _approx(1.0 - exact / book, lam * 120.0 / 2.0, tol=1e-2)
    assert 0.004 < (book - exact) / book < 0.005


def test_activation_saturates():
    """Irradiating forever cannot exceed the production rate R (~NE-07).  The
    Mn example reaches only 0.9% of saturation in two minutes, which is why the
    linear approximation is safe there."""
    act = load_activation_data()
    sigma = act["56Mn"]["sigma_b"]
    t_half = 2.579 * 3600.0
    sat = saturation_activity(2.0, 55.0, sigma, 1e13)
    assert _approx(sat, activation_rate(2.0, 55.0, sigma, 1e13))
    short = activation_activity(2.0, 55.0, sigma, 1e13, 120.0, t_half)
    assert short / sat < 0.01
    five = activation_activity(2.0, 55.0, sigma, 1e13, 5 * t_half, t_half)
    ten = activation_activity(2.0, 55.0, sigma, 1e13, 10 * t_half, t_half)
    assert _approx(five / sat, 0.969, tol=1e-2)
    assert _approx(ten / sat, 0.999, tol=1e-2)
    assert ten < sat


def test_activation_activity_demands_an_explicit_half_life():
    """The short-irradiation assumption must be a choice, not a silent default.
    Omitting the half-life raises rather than quietly using the linear form."""
    try:
        activation_activity(2.0, 55.0, 13.3, 1e13, 120.0)
    except ValueError:
        pass
    else:
        raise AssertionError("missing half-life should be rejected")
    for bad in (0.0, -1.0):
        try:
            activation_activity(2.0, 55.0, 13.3, 1e13, 120.0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("half_life=%r should be rejected" % bad)
    try:
        activation_rate(-1.0, 55.0, 13.3, 1e13)
    except ValueError:
        pass
    else:
        raise AssertionError("negative mass should be rejected")


def test_appendix_C2_blanks_are_meaningful():
    """99mTc has no activation cross section in Table C.2, and that is correct
    rather than missing: its parent 99Mo is a FISSION PRODUCT (~NE-09), reached
    by decay rather than neutron capture on a stable target.  The loader
    returns None instead of a zero that would silently give a wrong rate."""
    act = load_activation_data()
    assert len(act) == 31
    assert act["99mTc"]["sigma_b"] is None
    assert act["99mTc"]["parent"] == "99Mo"
    assert act["233Pa"]["parent_abundance_pct"] is None
    assert act["233Pa"]["sigma_b"] is not None
    assert len([k for k, v in act.items() if v["sigma_b"] is not None]) == 30


# --- fission  [§7.4.2] ----------------------------------------------------

def test_fissile_nuclides_stand_four_orders_of_magnitude_clear():
    """S&F §7.4.2 names 233U, 235U and 239Pu.  The thermal fission cross
    sections separate them so sharply that the classifying threshold is
    arbitrary within four decades."""
    for n in ("233U", "235U", "239Pu", "241Pu"):
        assert is_fissile(n, XS), n
        assert fission_cross_section(n, XS) > 500
    for n in ("238U", "232Th", "240Pu", "234U", "236U"):
        assert not is_fissile(n, XS), n
        assert fission_cross_section(n, XS) < 1.0
    for thr in (2.0, 50.0, 100.0, 400.0):
        assert is_fissile("235U", XS, threshold_b=thr)
        assert not is_fissile("238U", XS, threshold_b=thr)
    # fissile implies fissionable, not conversely
    assert is_fissionable("235U", XS) and is_fissionable("238U", XS)
    assert is_fissile("235U", XS) and not is_fissile("238U", XS)


def test_capture_to_fission_ratio_penalises_plutonium():
    """alpha = sigma_gamma/sigma_f.  Every capture is a neutron not causing
    fission AND a heavier actinide created.  239Pu's 0.362 against 235U's 0.169
    is much of why plutonium recycling is harder than it looks."""
    a_u5 = capture_to_fission_ratio("235U", XS)
    a_pu9 = capture_to_fission_ratio("239Pu", XS)
    assert _approx(a_u5, 0.169, tol=2e-2), "%.4f" % a_u5
    assert _approx(a_pu9, 0.362, tol=2e-2), "%.4f" % a_pu9
    assert a_pu9 > 2 * a_u5
    assert capture_to_fission_ratio("233U", XS) < a_u5    # the thorium argument
    try:
        capture_to_fission_ratio("12C", XS)
    except ValueError:
        pass
    else:
        raise AssertionError("a non-fissioning nuclide should be rejected")


def test_eta_is_below_nu_and_above_one():
    """eta = nu sigma_f/sigma_a is neutrons per neutron ABSORBED, and it is what
    must exceed 1 for a chain reaction -- not nu.  The gap is parasitic capture,
    15% even in 235U."""
    for n, nu, expect in (("233U", 2.48, 2.282), ("235U", 2.43, 2.078),
                          ("239Pu", 2.87, 2.107)):
        eta = eta_neutrons_per_absorption(n, nu, XS)
        assert _approx(eta, expect, tol=1e-2), "%s: %.4f" % (n, eta)
        assert 1.0 < eta < nu
    # 233U has the highest eta despite the lowest nu -- purely because its
    # capture-to-fission ratio is lowest.  The whole case for the thorium cycle.
    etas = {n: eta_neutrons_per_absorption(n, nu, XS)
            for n, nu in (("233U", 2.48), ("235U", 2.43), ("239Pu", 2.87))}
    assert max(etas, key=lambda k: etas[k]) == "233U"
    # a moderator returns eta = 0: it absorbs neutrons and gives none back.
    # 12C does absorb (0.0034 b), just never fissions -- so the answer is zero
    # rather than an error, and that is the physically meaningful result.
    assert eta_neutrons_per_absorption("12C", 2.4, XS) == 0.0
    assert eta_neutrons_per_absorption("10B", 2.4, XS) == 0.0


# --- macroscopic quantities ------------------------------------------------

def test_macroscopic_quantities_and_a_graphite_mean_free_path():
    """Same machinery as ~NE-11, restated for neutrons.  Reactor graphite at
    1.7 g/cm3 gives a 2.5 cm mean free path -- with ~NE-08's 115 collisions to
    thermalise, that is why a graphite pile is metres across."""
    n = atom_density(1.7, 12.011)
    assert _approx(n / 1e24, 0.08524, tol=1e-3)
    sig = macroscopic_cross_section(total_cross_section("12C", XS), n)
    assert _approx(sig, 0.404, tol=1e-2)
    assert _approx(mean_free_path(sig), 2.48, tol=1e-2)
    assert _approx(macroscopic_cross_section(1.0, 1e24), 1.0)
    for fn, args in ((atom_density, (1.0, 0.0)),
                     (macroscopic_cross_section, (-1.0, 1e24)),
                     (mean_free_path, (0.0,))):
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def test_table_C1_is_intact():
    """27 nuclides, and the ones every reactor engineer knows."""
    assert len(XS) == 27
    assert _approx(fission_cross_section("235U", XS), 587.0)
    assert absorption_cross_section("10B", XS) > 3800
    assert absorption_cross_section("6Li", XS) > 900
    for bad in ("113Cd", "999Zz"):
        try:
            absorption_cross_section(bad, XS)
        except KeyError:
            pass
        else:
            raise AssertionError("%s should not be in C.1" % bad)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
