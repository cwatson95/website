"""NE-25 tests -- direct energy conversion against Shultis & Faw §§12.5-12.11
and Tables 12.1-12.3.

Run:  python3 test_direct_conversion.py
"""

import math

from direct_conversion import (
    CI_TO_BQ, RADIONUCLIDE_SOURCES, MASS_NUMBERS, SNAP_GENERATORS,
    SPACE_REACTORS, CONVERTER_TYPES,
    specific_activity, specific_power, activity_per_watt, power_after,
    fuel_mass_for_power, mission_sizing, carnot_efficiency,
    thermoelectric_efficiency, zt_for_efficiency, richardson_current,
    thermionic_ideal_efficiency, betavoltaic_power, shielding_needed,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- Table 12.2 ----------------------------------------------------------

def test_table_12_2_is_fully_self_consistent():
    """Table 12.2 gives half-life, recoverable energy, specific activity and
    specific power for nine nuclides -- and only two of those four are
    independent.

    Every one of the nine specific powers reproduces from its own activity and
    energy row (to 0.5%), and every one of the nine specific activities
    reproduces from its own half-life and mass number (to 1.3%, 90Sr worst --
    plausibly because its entry is quoted in secular equilibrium with 90Y).
    A table that passes eighteen internal checks is one you can use."""
    for nuc, (t12, mev, ci_g, w_g, ci_w, _, _) in RADIONUCLIDE_SOURCES.items():
        derived_p = specific_power(ci_g, mev)
        assert _rel(derived_p, w_g, 5e-3), \
            "%s power: %.5f vs %.5f" % (nuc, derived_p, w_g)
        derived_a = specific_activity(t12, MASS_NUMBERS[nuc])
        assert _rel(derived_a, ci_g, 1.5e-2), \
            "%s activity: %.1f vs %.1f" % (nuc, derived_a, ci_g)
        # and the Ci/W column follows from the other two
        assert _rel(activity_per_watt(ci_g, mev), ci_w, 5e-3), nuc
    assert len(RADIONUCLIDE_SOURCES) == 9
    # four beta emitters, four alpha, plus 60Co -- as §12.10 says
    emitters = [v[5] for v in RADIONUCLIDE_SOURCES.values()]
    assert emitters.count("alpha") == 4
    assert emitters.count("beta") == 5          # incl. 60Co, which §12.10 sets apart
    for bad in ((0.0, 238), (87.7, 0)):
        try:
            specific_activity(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_specific_power_spans_a_factor_of_1500_and_it_does_not_matter():
    """210Po delivers 144 W/g and 137Cs 0.0966 -- a factor of 1500. And 210Po is
    useless for any mission longer than a year, because its half-life is 138
    days.

    The design variable is not specific power; it is specific power AT END OF
    MISSION, and the ranking inverts as the mission lengthens."""
    powers = [v[3] for v in RADIONUCLIDE_SOURCES.values()]
    assert _rel(max(powers) / min(powers), 1490.0, 0.02)
    assert max(RADIONUCLIDE_SOURCES, key=lambda k: RADIONUCLIDE_SOURCES[k][3]) == "210Po"
    # after a year, 210Po has lost 84% of its power and 238Pu 0.8%
    assert _rel(power_after(1.0, RADIONUCLIDE_SOURCES["210Po"][0]), 0.161, 1e-2)
    assert _rel(power_after(1.0, RADIONUCLIDE_SOURCES["238Pu"][0]), 0.992, 1e-3)
    # the ranking by mass inverts between a 3-month and a 5-year mission
    short = [n for n, _ in mission_sizing(100.0, 0.25)]
    long_ = [n for n, _ in mission_sizing(100.0, 5.0)]
    assert short[0] == "210Po"
    assert long_[0] != "210Po"
    assert long_.index("210Po") > short.index("210Po") + 3
    # 238Pu is never the lightest and is always in contention long
    assert "238Pu" in long_[:4]
    assert _approx(power_after(0.0, 87.7), 1.0)
    for bad in ((-1.0, 10.0), (1.0, 0.0)):
        try:
            power_after(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_why_every_deep_space_mission_flew_plutonium_238():
    """By mass alone the curiums beat 238Pu even on a 30-year mission. They have
    never flown, and Table 12.2 says why in its shielding row: both curium
    isotopes are marked 'neut.' -- strong spontaneous-fission neutron emitters,
    against which lead is useless.

    238Pu wins because it is an almost pure alpha emitter with an 87.7-year
    half-life: 0.558 W/g, negligible shielding, and 67% of its power still there
    after fifty years."""
    m_cm = fuel_mass_for_power(100.0, "244Cm", 0.06, 30.0)
    m_pu = fuel_mass_for_power(100.0, "238Pu", 0.06, 30.0)
    assert m_cm < m_pu                            # by mass the curium wins
    assert shielding_needed("244Cm") is None      # ...and cannot be shielded
    assert shielding_needed("242Cm") is None
    assert shielding_needed("238Pu") is None      # neutron emitter too, but far weaker
    assert shielding_needed("90Sr") == 0.0
    assert shielding_needed("60Co") == 18.0       # the gamma emitter: 18 cm of lead
    # 238Pu's staying power
    assert _rel(power_after(50.0, 87.7), 0.674, 1e-2)
    assert _rel(power_after(47.0, 87.7), 0.689, 1e-2)   # Voyager, launched 1977
    # and 60Co needs the most lead of any of them, by a factor of 2.4
    leads = [(n, v[6]) for n, v in RADIONUCLIDE_SOURCES.items() if v[6]]
    assert max(leads, key=lambda kv: kv[1])[0] == "60Co"
    try:
        shielding_needed("235U")
    except KeyError:
        pass
    else:
        raise AssertionError("an unlisted nuclide should be refused")


def test_sizing_an_rtg():
    """A 100 W(e) RTG at 6% conversion needs 1667 W of thermal power, and the
    fuel mass follows from the specific power at end of mission."""
    g = fuel_mass_for_power(100.0, "238Pu", 0.06, 0.0)
    assert _rel(g, 2987.0, 1e-2), "%.0f g" % g
    assert _rel(g * 0.558, 100.0 / 0.06, 1e-9)
    # the mass grows as the mission lengthens
    masses = [fuel_mass_for_power(100.0, "238Pu", 0.06, y) for y in (0, 10, 30)]
    assert masses == sorted(masses)
    assert _rel(masses[2] / masses[0], 1.267, 1e-2)
    # a better converter buys mass back linearly
    assert _rel(fuel_mass_for_power(100.0, "238Pu", 0.12) / g, 0.5, 1e-9)
    for bad in (("238Pu", 0.0), ("238Pu", 1.0)):
        try:
            fuel_mass_for_power(100.0, bad[0], bad[1])
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))
    try:
        fuel_mass_for_power(100.0, "3H")
    except KeyError:
        pass
    else:
        raise AssertionError("an unlisted nuclide should be refused")


# --- the converters -------------------------------------------------------

def test_everything_here_except_the_betavoltaic_is_still_a_heat_engine():
    """S&F §12.6.1 makes the point for thermionics and it applies to all of
    them: thermoelectric, thermionic, AMTEC and Stirling all take heat in hot
    and reject it cold, so Carnot bounds every one.

    What direct conversion replaces is the TURBINE, not the thermodynamics."""
    engines = [k for k, v in CONVERTER_TYPES.items() if v["heat_engine"]]
    assert len(engines) == 4
    assert CONVERTER_TYPES["betavoltaic"]["heat_engine"] is False
    # only the Stirling has moving parts, and it is the most efficient
    movers = [k for k, v in CONVERTER_TYPES.items() if v["moving_parts"]]
    assert movers == ["Stirling"]
    best = max(engines, key=lambda k: CONVERTER_TYPES[k]["efficiency"][1])
    assert best == "Stirling"
    # AMTEC is the best without moving parts
    still = [k for k in engines if not CONVERTER_TYPES[k]["moving_parts"]]
    assert max(still, key=lambda k: CONVERTER_TYPES[k]["efficiency"][1]) == "AMTEC"
    # and every quoted efficiency is well inside Carnot for its temperatures
    eta_c = carnot_efficiency(1300.0, 500.0)
    for k, v in CONVERTER_TYPES.items():
        assert v["efficiency"][1] < eta_c, k
    for bad in ((300.0, 300.0), (300.0, 400.0), (0.0, 100.0)):
        try:
            carnot_efficiency(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_thermoelectric_penalty_is_ZT():
    """The efficiency S&F quote results from but never write down:

        eta = eta_Carnot (sqrt(1+ZT) - 1)/(sqrt(1+ZT) + T_c/T_h) .

    At ZT = 1 -- what the best materials managed for decades -- the second
    factor is 0.23, so a 61% Carnot limit yields a 14% device, and a real RTG
    with worse temperatures and parasitic losses lands at 6%. That factor is the
    whole reason direct conversion is a niche."""
    th, tc = 1300.0, 500.0
    eta_c = carnot_efficiency(th, tc)
    assert _rel(eta_c, 0.6154, 1e-3)
    e1 = thermoelectric_efficiency(1.0, th, tc)
    assert _rel(e1 / eta_c, 0.230, 1e-2), "%.4f" % (e1 / eta_c)
    # monotone in ZT, and approaching Carnot only as ZT -> infinity
    prev = 0.0
    for zt in (0.1, 0.5, 1.0, 4.0, 20.0, 1000.0):
        e = thermoelectric_efficiency(zt, th, tc)
        assert e > prev
        assert e < eta_c
        prev = e
    assert _rel(thermoelectric_efficiency(1e6, th, tc) / eta_c, 1.0, 1e-2)
    assert _approx(thermoelectric_efficiency(0.0, th, tc), 0.0)
    # what ZT would a 20% device need?
    zt = zt_for_efficiency(0.20, th, tc)
    assert _rel(zt, 1.778, 0.02), "%.3f" % zt
    # and no ZT reaches Carnot
    try:
        zt_for_efficiency(eta_c, th, tc)
    except ValueError as exc:
        assert "Carnot" in str(exc)
    else:
        raise AssertionError("a Carnot-limited target should be refused")
    try:
        thermoelectric_efficiency(-1.0, th, tc)
    except ValueError:
        pass
    else:
        raise AssertionError("a negative ZT should be rejected")


def test_thermionics_need_1400_kelvin_because_of_an_exponential():
    """S&F §12.6.1 says emitter temperatures "typically in excess of 1400 K" are
    needed and does not say why. The Richardson law does:
    J = A T^2 exp(-phi/kT).

    For a 2.5 eV emitter the current density runs 1e-8 A/cm^2 at 800 K and 39 at
    1800 K -- ten orders of magnitude for a factor of 2.25 in temperature. There
    is no low-temperature thermionic converter, and there cannot be."""
    j = [richardson_current(t, 2.5) for t in (800.0, 1000.0, 1400.0, 1800.0)]
    assert j == sorted(j)
    assert j[0] < 1e-7
    assert j[3] > 10.0
    assert j[3] / j[0] > 1e9
    assert _rel(j[2], 0.2358, 1e-2)
    # a lower work function helps enormously -- hence caesium coatings
    assert richardson_current(1400.0, 1.8) / richardson_current(1400.0, 2.5) > 200
    # the ideal efficiency lands in §12.6.1's quoted 1-10% band once the
    # collector is realistic, and can never exceed Carnot
    e = thermionic_ideal_efficiency(1800.0, 800.0)
    assert e <= carnot_efficiency(1800.0, 800.0)
    assert _rel(e, 0.412, 1e-2)
    # the output voltage is a DIFFERENCE of work functions, so this must fail
    try:
        thermionic_ideal_efficiency(1800.0, 800.0, 1.4, 2.6)
    except ValueError:
        pass
    else:
        raise AssertionError("a collector with the higher work function should be refused")
    for bad in ((0.0, 2.5), (1400.0, 0.0)):
        try:
            richardson_current(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_the_betavoltaic_escapes_carnot_and_pays_in_microwatts():
    """§12.9.2's device is the only one here that is not a heat engine: beta
    particles create electron-hole pairs directly, so there is no Carnot bound
    and no temperature difference to maintain.

    The price is scale. A curie of tritium at 5.67 keV mean beta energy and 2%
    conversion yields 0.7 microwatts -- which is why betavoltaics power
    pacemakers and memory backup and nothing else."""
    p = betavoltaic_power(CI_TO_BQ, 5670.0, 0.02)
    assert _rel(p * 1e6, 0.672, 1e-2), "%.3f uW" % (p * 1e6)
    assert p < 1e-5
    # 63Ni's harder beta is worth 3x
    assert _rel(betavoltaic_power(CI_TO_BQ, 17400.0, 0.02) / p, 3.07, 1e-2)
    # linear in everything, having no thermodynamic structure at all
    assert _rel(betavoltaic_power(2 * CI_TO_BQ, 5670.0, 0.02), 2 * p, 1e-12)
    assert _rel(betavoltaic_power(CI_TO_BQ, 5670.0, 0.04), 2 * p, 1e-12)
    # matching one SNAP-3 (2.5 W(e)) would take 3.7 MEGAcuries of tritium --
    # 380 grams of it, and 140 petabecquerels
    curies = 2.5 / p
    assert _rel(curies, 3.72e6, 0.02), "%.3e Ci" % curies
    for bad in ({"efficiency": 0.0}, {"efficiency": 1.0}):
        try:
            betavoltaic_power(CI_TO_BQ, 5670.0, **bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % bad)


# --- the flight record ----------------------------------------------------

def test_the_space_reactor_record():
    """Table 12.3. The two systems that actually flew repeatedly were the least
    efficient and the least ambitious; the most capable design never flew at all.

    BUK: 3% efficient, 31 flights. SP-100: 5% efficient, 100 kW(e), 5.4 tonnes,
    zero flights. That is the shape of the whole programme."""
    flown = {k: v for k, v in SPACE_REACTORS.items() if v["flights"] > 0}
    assert set(flown) == {"SNAP-10A", "BUK", "TOPAZ-I"}
    assert SPACE_REACTORS["BUK"]["flights"] == 31
    assert SPACE_REACTORS["SP-100"]["flights"] == 0
    # every one converts at 1-5%, an order of magnitude below a turbine
    for k, v in SPACE_REACTORS.items():
        eta = v["kwe"] / v["kwt"]
        assert 0.01 <= eta <= 0.06, "%s: %.3f" % (k, eta)
        assert eta < 0.34 / 5                    # cf. ~NE-22's LWR
    # SP-100 is the most efficient AND has the best specific mass, by 3.5x
    best_sm = min(SPACE_REACTORS, key=lambda k: SPACE_REACTORS[k]["mass_kg"]
                  / SPACE_REACTORS[k]["kwe"])
    assert best_sm == "SP-100"
    assert _rel(SPACE_REACTORS["SP-100"]["mass_kg"] / SPACE_REACTORS["SP-100"]["kwe"],
                54.2, 1e-2)
    # the thermionic systems beat the thermoelectric ones on efficiency
    ti = [v["kwe"] / v["kwt"] for v in SPACE_REACTORS.values() if v["converter"] == "TI"]
    assert min(ti) > SPACE_REACTORS["BUK"]["kwe"] / SPACE_REACTORS["BUK"]["kwt"]


def test_the_snap_series():
    """Table 12.1. The 90Sr units are one to two ORDERS OF MAGNITUDE heavier per
    watt than the 238Pu ones, because 90Sr's beta emissions need shielding and
    its specific power is 60x lower. Every one of the space missions flew
    plutonium; the strontium units sat on the sea floor and in the Arctic."""
    per_watt = {}
    for name, (func, fuel, we, mass, life) in SNAP_GENERATORS.items():
        if mass is not None:
            per_watt[name] = mass / we
    sr = [v for k, v in per_watt.items() if SNAP_GENERATORS[k][1] == "90Sr"]
    pu = [v for k, v in per_watt.items() if SNAP_GENERATORS[k][1] == "238Pu"]
    assert min(sr) > 10 * max(pu), "%.1f vs %.1f" % (min(sr), max(pu))
    # and the 90Sr specific power really is ~60x lower
    assert _rel(RADIONUCLIDE_SOURCES["238Pu"][3]
                / RADIONUCLIDE_SOURCES["90Sr"][3], 0.609, 1e-2)
    # every 238Pu unit has a 5-year design life; the 210Po and 242Cm ones 90 days
    for name, (_, fuel, _, _, life) in SNAP_GENERATORS.items():
        if fuel == "238Pu":
            assert _approx(life, 5.0)
        if fuel in ("210Po", "242Cm"):
            assert life < 0.3
    # the highest-power unit is the shortest-lived: SNAP-29, 500 W for 90 days
    hottest = max(SNAP_GENERATORS, key=lambda k: SNAP_GENERATORS[k][2])
    assert hottest == "SNAP-29"
    assert SNAP_GENERATORS[hottest][4] < 0.3


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
