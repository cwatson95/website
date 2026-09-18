"""NE-22 tests -- power reactors against Shultis & Faw §§11.1-11.6 and
Tables 11.1-11.6.

The tables are the content of this chapter, so the tests are mostly
cross-checks: each table is required to reproduce its own derived quantities
from its own primary ones. Table 11.2 passes on five independent relations;
Table 11.3 fails one, by 14%.

Run:  python3 test_power_reactors.py
"""

import math

from power_reactors import (
    WATER_CRITICAL_C, TYPICAL_CORE_LIMIT_C, PWR, BWR,
    GEN_III_BWR, GEN_III_PWR, SMALL_REACTORS, GEN_IV_SYSTEMS,
    NUCLEAR_SHARE_2013, BWR_SPECIFIC_POWER_INCONSISTENCY,
    carnot_efficiency, thermal_efficiency, second_law_ratio, waste_heat,
    core_volume, power_density, specific_power, total_rod_length,
    linear_heat_rate, surface_heat_flux, peaking_factor, assembly_width,
    cycle_length_days, capacity_factor_energy, coolant_is_liquid,
)


def _rel(a, b, tol):
    return abs(a / b - 1.0) <= tol


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


# --- the thermodynamic ceiling -------------------------------------------

def test_the_374_degree_ceiling_sets_the_whole_plant():
    """S&F §11.1.4. Above water's critical temperature no pressure produces a
    liquid, and a water-moderated core needs liquid water to moderate as well as
    to cool. So the outlet is capped near 340 C, the steam reaches the turbine
    barely superheated, and the efficiency lands at ~34%.

    Every distinctive feature of an LWR plant follows: the wet-steam turbines,
    the moisture separators, the size of the condenser, and the fact that two
    thirds of the heat is thrown away."""
    assert coolant_is_liquid(300.0)
    assert coolant_is_liquid(TYPICAL_CORE_LIMIT_C)
    assert not coolant_is_liquid(400.0)
    assert not coolant_is_liquid(WATER_CRITICAL_C)
    assert TYPICAL_CORE_LIMIT_C < WATER_CRITICAL_C
    # the Carnot ceiling for PWR steam, and how close the plant gets
    eta_c = carnot_efficiency(PWR["steam_temp_C"], 33.0)
    assert _rel(eta_c, 0.4506, 1e-3), "%.4f" % eta_c
    assert _rel(PWR["efficiency"] / eta_c, 0.754, 1e-2)
    # a gas-cooled core at 540 C lifts the ceiling by 38%
    assert _rel(carnot_efficiency(540.0, 33.0), 0.6235, 1e-3)
    assert _rel(carnot_efficiency(540.0, 33.0) / eta_c, 1.384, 1e-2)
    # sanity on the function itself
    assert carnot_efficiency(100.0, 0.0) > 0
    for bad in ((100.0, 100.0), (100.0, 200.0), (-300.0, -290.0)):
        try:
            carnot_efficiency(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


def test_no_plant_may_beat_carnot():
    """`second_law_ratio` refuses a ratio above 1. The realistic way to trip it
    is not optimism but a units slip: quote MW(t) where MW(e) belongs and the
    'efficiency' becomes 1.0, which passes every plausibility check except this
    one."""
    assert _rel(second_law_ratio(1300.0, 3800.0, 284.0, 33.0), 0.759, 1e-2)
    for r in (GEN_III_PWR["AP1000"], GEN_III_PWR["EPR"]):
        ratio = second_law_ratio(r["electric_MW"], r["thermal_MW"], r["hot_leg_C"], 33.0)
        assert 0.6 < ratio < 0.85, "%.3f" % ratio
    # the units slip
    try:
        second_law_ratio(3800.0, 3800.0, 284.0, 33.0)
    except ValueError as exc:
        assert "second-law" in str(exc)
    else:
        raise AssertionError("eta = 1 should be refused")
    try:
        thermal_efficiency(100.0, 0.0)
    except ValueError:
        pass
    else:
        raise AssertionError("zero thermal power should be refused")


def test_two_thirds_of_the_heat_is_thrown_away():
    """The consequence of 34% that sizes the site. A 1000 MW(e) plant makes
    2940 MW(t) and rejects 1940 MW -- half again as much as it sells -- into a
    river, the sea, or a cooling tower."""
    q = waste_heat(1000.0, 0.34)
    assert _rel(q, 1941.0, 1e-3), "%.1f MW" % q
    assert _rel(1000.0 / 0.34, 2941.0, 1e-3)
    assert _rel(q / 1000.0, 1.94, 1e-2)
    # a 44% Gen IV plant rejects a quarter less
    assert _rel(waste_heat(1000.0, 0.44) / q, 0.655, 1e-2)
    assert waste_heat(1000.0, 0.99) < waste_heat(1000.0, 0.34)
    for bad in (0.0, 1.0, 1.5):
        try:
            waste_heat(1000.0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("efficiency %r should be rejected" % bad)


# --- the tables checking themselves ---------------------------------------

def test_table_11_2_is_consistent_on_five_independent_relations():
    """S&F's PWR table reproduces its own derived quantities from its own primary
    ones, which is what makes it trustworthy:

      core geometry -> power density            102.2 vs 102
      fuel loading  -> specific power            33.0 vs 33
      rod count     -> linear heat rate          17.9 vs 17.5
      linear rate   -> surface heat flux        0.586 vs 0.584
      lattice+pitch -> assembly width           21.42 vs 21.4
    """
    assert _rel(thermal_efficiency(PWR["electric_MW"], PWR["thermal_MW"]),
                PWR["efficiency"], 1e-2)
    assert _rel(power_density(PWR["thermal_MW"], PWR["core_length_m"],
                              PWR["core_diameter_m"]),
                PWR["power_density_kW_per_L"], 5e-3)
    assert _rel(specific_power(PWR["thermal_MW"], PWR["fuel_loading_kg"]),
                PWR["specific_power_kW_per_kgU"], 5e-3)
    assert _rel(linear_heat_rate(PWR["thermal_MW"], PWR["assemblies"],
                                 PWR["rods_per_assembly"], PWR["core_length_m"]),
                PWR["linear_heat_rate_kW_per_m"], 3e-2)
    assert _rel(surface_heat_flux(PWR["linear_heat_rate_kW_per_m"], PWR["rod_od_mm"]),
                PWR["heat_flux_avg_MW_per_m2"], 5e-3)
    assert _rel(assembly_width(PWR["lattice"], PWR["rod_pitch_mm"]),
                PWR["assembly_width_cm"], 1e-3)
    # the 17x17 lattice holds 289 positions and 264 fuel rods: 25 guide and
    # instrument tubes, which is why the assembly is not simply 289 rods
    assert PWR["lattice"] ** 2 - PWR["rods_per_assembly"] == 25
    # pellet, gap and clad add up to the rod diameter
    inner = PWR["rod_od_mm"] - 2 * PWR["clad_thickness_mm"]
    gap = (inner - PWR["pellet_diameter_mm"]) / 2.0
    assert 0.0 < gap < 0.2, "%.4f mm" % gap


def test_table_11_3_does_not_add_up():
    """The BWR table's specific power, thermal output and fuel loading are
    mutually inconsistent: 25.9 kW/kg x 168 t = 4351 MW against a printed
    3830 MW, a 14% discrepancy. Its OWN thermal output and loading imply
    22.8 kW/kg.

    The same three-way check passes exactly for the PWR table (33 x 115 = 3795
    against 3800), which is what isolates this as a defect in Table 11.3 rather
    than a flaw in the check."""
    derived = specific_power(BWR["thermal_MW"], BWR["fuel_loading_kg"])
    assert _rel(derived, 22.8, 5e-3), "%.2f kW/kg" % derived
    assert _rel(BWR_SPECIFIC_POWER_INCONSISTENCY / derived, 1.137, 1e-2)
    assert not _rel(derived, BWR["specific_power_kW_per_kgU"], 0.05)
    # the loading that WOULD be consistent with the printed specific power
    implied = BWR["thermal_MW"] * 1e3 / BWR["specific_power_kW_per_kgU"]
    assert _rel(implied / 1e3, 147.9, 1e-3), "%.1f t" % (implied / 1e3)
    # the PWR passes the same test to 0.15%
    assert _rel(specific_power(PWR["thermal_MW"], PWR["fuel_loading_kg"]),
                PWR["specific_power_kW_per_kgU"], 2e-3)
    # everything else in Table 11.3 is fine
    assert _rel(power_density(BWR["thermal_MW"], BWR["core_length_m"],
                              BWR["core_diameter_m"]),
                BWR["power_density_kW_per_L"], 1e-2)
    assert _rel(thermal_efficiency(BWR["electric_MW"], BWR["thermal_MW"]),
                BWR["efficiency"], 3e-2)
    assert BWR["lattice"] ** 2 - BWR["rods_per_assembly"] == 2      # two water rods


def test_a_pwr_and_a_bwr_differ_where_the_physics_says_they_must():
    """Same steam, same efficiency, same era -- and a factor of two in pressure
    and power density. Every difference traces to one decision: a BWR boils in
    the core and a PWR does not."""
    # the same steam and the same efficiency
    assert _rel(PWR["steam_temp_C"], BWR["steam_temp_C"], 0.03)
    assert _approx(PWR["efficiency"], BWR["efficiency"])
    # but half the pressure, because a BWR is allowed to boil
    assert _rel(PWR["pressure_MPa"] / BWR["pressure_MPa"], 2.16, 1e-2)
    # and half the power density, because the voids need room
    assert _rel(PWR["power_density_kW_per_L"] / BWR["power_density_kW_per_L"],
                1.82, 1e-2)
    assert BWR["void_fraction_avg"] > 0.3
    # a BWR core is therefore physically bigger for the same power
    assert (core_volume(BWR["core_length_m"], BWR["core_diameter_m"])
            > 1.7 * core_volume(PWR["core_length_m"], PWR["core_diameter_m"]))
    assert BWR["vessel_id_m"] > PWR["vessel_id_m"]
    # ...but its vessel wall is THINNER, because the pressure is lower
    assert BWR["vessel_wall_cm"] < PWR["vessel_wall_cm"]
    # the BWR needs less enrichment and reaches less burnup
    assert BWR["equil_enrichment_pct"] < PWR["equil_enrichment_pct"]
    assert BWR["burnup_GWd_per_tU"] < PWR["burnup_GWd_per_tU"]
    # a BWR has 4x the assemblies but a quarter the rods in each
    assert _rel(BWR["assemblies"] / PWR["assemblies"], 3.94, 1e-2)
    assert _rel(PWR["rods_per_assembly"] / BWR["rods_per_assembly"], 4.26, 1e-2)


def test_real_cores_beat_the_bare_core_peaking_factor():
    """~NE-21 derives 3.639 for a bare uniform cylinder. Table 11.2's PWR runs
    2.50 and Table 11.3's BWR 2.20, and the difference is bought with the
    reflector, fuel zoning and burnable poisons of §§11.2-11.3.

    Every tenth of peaking is directly saleable power, because the hottest fuel
    pin limits the whole reactor."""
    pwr_pf = peaking_factor(PWR["heat_flux_max_MW_per_m2"],
                            PWR["heat_flux_avg_MW_per_m2"])
    bwr_pf = peaking_factor(BWR["heat_flux_max_MW_per_m2"],
                            BWR["heat_flux_avg_MW_per_m2"])
    assert _rel(pwr_pf, 2.50, 1e-2), "%.3f" % pwr_pf
    assert _rel(bwr_pf, 2.196, 1e-2), "%.3f" % bwr_pf
    bare = 3.639
    assert pwr_pf < bare and bwr_pf < bare
    # the flattening is worth ~46% more power for the PWR at the same peak limit
    assert _rel(bare / pwr_pf, 1.456, 1e-2)
    # the BWR flattens better, because its voids give it a distributed negative
    # feedback that a PWR does not have in-core
    assert bwr_pf < pwr_pf
    try:
        peaking_factor(1.0, 2.0)
    except ValueError:
        pass
    else:
        raise AssertionError("a maximum below the average should be refused")


def test_cycle_length_from_burnup():
    """Discharge burnup, fuel loading and power give the refuelling interval, and
    both tables land near three years of full power -- which is why an 18-month
    refuelling outage cycle reloads a third of the core at a time."""
    d_pwr = cycle_length_days(PWR["burnup_GWd_per_tU"], PWR["fuel_loading_kg"],
                              PWR["thermal_MW"])
    d_bwr = cycle_length_days(BWR["burnup_GWd_per_tU"], BWR["fuel_loading_kg"],
                              BWR["thermal_MW"])
    assert _rel(d_pwr, 998.7, 1e-3), "%.1f d" % d_pwr
    assert _rel(d_bwr, 1206.0, 1e-3), "%.1f d" % d_bwr
    for d in (d_pwr, d_bwr):
        assert 2.5 < d / 365.25 < 3.5
    # a third of the core each 18 months is about the same residence time
    assert _rel(3 * 18 * 30.4 / d_pwr, 1.64, 0.05)
    for bad in ((0.0, 1e5, 3800.0), (33.0, 0.0, 3800.0), (33.0, 1e5, 0.0)):
        try:
            cycle_length_days(*bad)
        except ValueError:
            pass
        else:
            raise AssertionError("%r should be rejected" % (bad,))


# --- the generations ------------------------------------------------------

def test_generation_iii_removes_components_rather_than_improving_them():
    """Table 11.4's real content. From BWR/6 to ESBWR the electric output rises
    14% while the recirculation pumps go 2 -> 10 -> 0, the safety pumps
    9 -> 18 -> 0 and the diesel generators 3 -> 3 -> 0.

    Passive safety is not a better pump; it is no pump. The ESBWR does it by
    growing the vessel 27% taller so that natural circulation drives the core
    flow -- which is why its power density is unchanged while its active fuel is
    shorter."""
    b6, abwr, esbwr = (GEN_III_BWR[k] for k in ("BWR/6", "ABWR", "ESBWR"))
    assert esbwr["recirculation_pumps"] == 0
    assert esbwr["safety_pumps"] == 0
    assert esbwr["diesels"] == 0
    assert abwr["recirculation_pumps"] > b6["recirculation_pumps"]   # internalised
    assert _rel(esbwr["electric_MW"] / b6["electric_MW"], 1.14, 1e-2)
    assert _rel(esbwr["vessel_h_m"] / b6["vessel_h_m"], 1.27, 1e-2)
    assert esbwr["active_height_m"] < b6["active_height_m"]
    # the steam cycle does not change at all: all three sit at 34-35%
    etas = [thermal_efficiency(v["electric_MW"], v["thermal_MW"])
            for v in GEN_III_BWR.values()]
    assert max(etas) - min(etas) < 0.01
    for e in etas:
        assert 0.34 <= e <= 0.35
    # power density is essentially unchanged across the three
    pds = [v["power_density_kW_per_L"] for v in GEN_III_BWR.values()]
    assert max(pds) / min(pds) < 1.07


def test_table_11_5_linear_heat_rates_are_reproducible():
    """The AP1000 and EPR entries reproduce their own linear heat rates from
    bundle count, lattice and active height to within 4%, which is the fraction
    of lattice positions taken by guide tubes."""
    for name, r in GEN_III_PWR.items():
        q = linear_heat_rate(r["thermal_MW"], r["bundles"], 264,
                             r["active_height_m"]) * 10.0     # kW/m -> W/cm
        assert _rel(q, r["linear_heat_rate_W_per_cm"], 0.05), \
            "%s: %.1f vs %.0f W/cm" % (name, q, r["linear_heat_rate_W_per_cm"])
    # the EPR is bigger in every dimension and runs a LOWER linear rate --
    # margin bought with size, which is the Gen III trade
    ap, epr = GEN_III_PWR["AP1000"], GEN_III_PWR["EPR"]
    assert epr["thermal_MW"] > ap["thermal_MW"]
    assert epr["bundles"] > ap["bundles"]
    assert epr["vessel_id_cm"] > ap["vessel_id_cm"]
    assert epr["linear_heat_rate_W_per_cm"] < ap["linear_heat_rate_W_per_cm"]
    # and the EPR is the more efficient plant, at 37%
    assert _rel(thermal_efficiency(epr["electric_MW"], epr["thermal_MW"]), 0.370, 1e-2)
    assert _rel(thermal_efficiency(ap["electric_MW"], ap["thermal_MW"]), 0.329, 1e-2)
    # the AP1000 halves the loops and nearly halves the flow per MW
    assert ap["loops"] == 2 and epr["loops"] == 4
    assert (ap["vessel_flow_m3_per_h"] / ap["thermal_MW"]
            < epr["vessel_flow_m3_per_h"] / epr["thermal_MW"])


def test_generation_iv_is_an_escape_from_the_water_ceiling():
    """All six Gen IV systems run outlet temperatures above water's critical
    point, and every one therefore beats 34%. Four of the six are FAST reactors,
    which is a fuel-cycle argument (~NE-23) and not a thermodynamic one."""
    assert len(GEN_IV_SYSTEMS) == 6
    for k, v in GEN_IV_SYSTEMS.items():
        assert v["outlet_C"] > WATER_CRITICAL_C, k
        assert v["efficiency"] > 0.34, k
        # and each is comfortably inside its own Carnot limit
        assert v["efficiency"] < carnot_efficiency(v["outlet_C"], 33.0), k
    fast = [k for k, v in GEN_IV_SYSTEMS.items() if "fast" in v["spectrum"]]
    assert len(fast) >= 4
    # the hottest system is the most efficient
    hottest = max(GEN_IV_SYSTEMS, key=lambda k: GEN_IV_SYSTEMS[k]["outlet_C"])
    assert hottest == "VHTR"
    assert GEN_IV_SYSTEMS[hottest]["efficiency"] == max(
        v["efficiency"] for v in GEN_IV_SYSTEMS.values())
    # the efficiency gain over an LWR is 18-47%
    gains = [v["efficiency"] / 0.34 for v in GEN_IV_SYSTEMS.values()]
    assert 1.15 < min(gains) < 1.2 and 1.4 < max(gains) < 1.5


def test_the_small_reactor_landscape():
    """Table 11.6. Two things stand out: most designs are PWRs, i.e. the
    established technology shrunk rather than a new one; and almost none were
    built."""
    powers = [v[0] for v in SMALL_REACTORS.values()]
    assert all(p <= 350 for p in powers)
    types = [v[1] for v in SMALL_REACTORS.values()]
    water = sum(1 for t in types if t in ("PWR", "LWR", "BWR"))
    assert water > len(types) / 2, "%d of %d" % (water, len(types))
    assert types.count("PWR") == 8
    built = [k for k, v in SMALL_REACTORS.items() if "construction" in v[3]]
    assert len(built) <= 4, built
    # the median design is well under 200 MW(e)
    ordered = sorted(powers)
    assert ordered[len(ordered) // 2] < 200


def test_table_11_1_and_what_capacity_does_not_tell_you():
    """France leads on share (79%) and the United States on capacity (101 GW).
    Neither column is generation: an availability factor turns one into the
    other, and Table 11.1 does not give it."""
    assert max(NUCLEAR_SHARE_2013, key=lambda k: NUCLEAR_SHARE_2013[k][0]) == "France"
    countries = dict((k, v) for k, v in NUCLEAR_SHARE_2013.items() if k != "WORLD")
    assert max(countries, key=lambda k: countries[k][1]) == "United States"
    world = NUCLEAR_SHARE_2013["WORLD"]
    assert world[0] == 16 and world[2] == 435
    # the listed countries account for most of the world's capacity
    listed = sum(v[1] for v in countries.values())
    assert _rel(listed / world[1], 0.98, 0.05)
    # average unit size, and how it varies
    assert _rel(world[1] / world[2], 0.863, 1e-2)          # GW(e) per unit
    fr = NUCLEAR_SHARE_2013["France"]
    assert _rel(fr[1] / fr[2], 1.088, 1e-2)
    # energy, not capacity, is what gets sold
    assert _rel(capacity_factor_energy(1000.0, 0.90), 900.0, 1e-12)
    for bad in (0.0, 1.5):
        try:
            capacity_factor_energy(1000.0, bad)
        except ValueError:
            pass
        else:
            raise AssertionError("capacity factor %r should be rejected" % bad)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
