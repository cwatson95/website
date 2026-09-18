"""NE-22  Nuclear power reactors: PWR/BWR steam cycles, Gen III and IV designs.

Nuclear Science & Engineering trunk, module NE-22 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 11.1-11.6 (printed pp. 370-429).  Pure stdlib.

~NE-19 to ~NE-21 built a critical core.  This module is about the machine around
it, and the machine is mostly a STEAM PLANT.  Everything distinctive about
reactor engineering follows from one constraint:

    Water's critical temperature is 374 C, so a water-cooled core cannot run
    hotter than about 340 C, so the steam is barely superheated, so the Carnot
    ceiling is ~45% and the achieved efficiency is ~34%.

That number governs the rest.  A 1000 MW(e) plant must therefore make ~3000 MW of
heat and throw ~2000 MW of it into a river or a cooling tower; the turbines must
be the large, expensive, wet-steam kind; and the whole Generation IV programme is
in one sense an attempt to escape the 374 C ceiling by using gas, sodium, lead or
salt instead.

The module is mostly CURATED DATA -- Tables 11.1-11.6 -- plus the arithmetic that
checks it against itself.  That checking is the point: S&F's Table 11.2 for a PWR
is internally consistent to within 2% on five independent relations (core volume
against power density, fuel loading against specific power, rod count against
linear heat rate, linear heat rate against surface heat flux, rod pitch against
assembly width), which is what lets it be trusted.  Table 11.3's BWR entries are
not: its specific power, thermal output and fuel loading disagree by 14%.
"""

import math

__all__ = [
    "WATER_CRITICAL_C", "TYPICAL_CORE_LIMIT_C", "PWR", "BWR",
    "GEN_III_BWR", "GEN_III_PWR", "SMALL_REACTORS", "GEN_IV_SYSTEMS",
    "NUCLEAR_SHARE_2013",
    "carnot_efficiency", "thermal_efficiency", "second_law_ratio",
    "waste_heat", "core_volume", "power_density", "specific_power",
    "total_rod_length", "linear_heat_rate", "surface_heat_flux",
    "peaking_factor", "assembly_width", "cycle_length_days",
    "capacity_factor_energy", "coolant_is_liquid",
    "BWR_SPECIFIC_POWER_INCONSISTENCY",
]

WATER_CRITICAL_C = 374.0            # S&F §11.1.4 prints 375; the accepted value is 373.95
TYPICAL_CORE_LIMIT_C = 340.0        # §11.1.4


# --- Table 11.2 (printed p. 379): a 1970s 1000 MW(e)-class PWR --------------
PWR = {
    "thermal_MW": 3800.0, "electric_MW": 1300.0, "efficiency": 0.34,
    "core_length_m": 4.17, "core_diameter_m": 3.37,
    "specific_power_kW_per_kgU": 33.0, "power_density_kW_per_L": 102.0,
    "linear_heat_rate_kW_per_m": 17.5,
    "heat_flux_avg_MW_per_m2": 0.584, "heat_flux_max_MW_per_m2": 1.46,
    "pressure_MPa": 15.5, "inlet_C": 292.0, "outlet_C": 329.0,
    "steam_temp_C": 284.0, "steam_pressure_psia": 1000.0,
    "vessel_id_m": 4.4, "vessel_height_m": 13.6, "vessel_wall_cm": 22.0,
    "pellet_diameter_mm": 8.19, "rod_od_mm": 9.5, "clad_thickness_mm": 0.57,
    "rod_pitch_mm": 12.6, "rods_per_assembly": 264, "lattice": 17,
    "assembly_width_cm": 21.4, "assemblies": 193,
    "fuel_loading_kg": 115e3, "equil_enrichment_pct": 3.2,
    "burnup_GWd_per_tU": 33.0, "control_assemblies": 68,
    "absorber": "Ag-In-Cd and/or B4C", "soluble_poison": "boric acid",
}

# --- Table 11.3 (printed p. 386): a 1970s 1000 MW(e)-class BWR --------------
BWR = {
    "thermal_MW": 3830.0, "electric_MW": 1330.0, "efficiency": 0.34,
    "core_length_m": 3.76, "core_diameter_m": 4.8,
    "specific_power_kW_per_kgU": 25.9, "power_density_kW_per_L": 56.0,
    "linear_heat_rate_kW_per_m": 20.7,
    "heat_flux_avg_MW_per_m2": 0.51, "heat_flux_max_MW_per_m2": 1.12,
    "pressure_MPa": 7.17, "feedwater_C": 216.0, "steam_temp_C": 290.0,
    "void_fraction_avg": 0.37, "void_fraction_max": 0.75,
    "vessel_id_m": 6.4, "vessel_height_m": 22.1, "vessel_wall_cm": 15.0,
    "pellet_diameter_mm": 10.57, "rod_od_mm": 12.52, "clad_thickness_mm": 0.864,
    "rod_pitch_mm": 16.3, "rods_per_assembly": 62, "lattice": 8,
    "assembly_width_cm": 13.4, "assemblies": 760,
    "fuel_loading_kg": 168e3, "equil_enrichment_pct": 1.9,
    "burnup_GWd_per_tU": 27.5, "control_assemblies": 193,
    "absorber": "boron carbide", "burnable_poison": "gadolinium",
}

# Table 11.3's specific power, thermal output and fuel loading do not agree:
# 25.9 kW/kg x 168 t = 4351 MW against the printed 3830 MW.  See refs.md.
BWR_SPECIFIC_POWER_INCONSISTENCY = 25.9

# --- Table 11.4 (printed p. 391): the BWR evolution -------------------------
GEN_III_BWR = {
    "BWR/6": {"thermal_MW": 3900, "electric_MW": 1360, "vessel_h_m": 21.8,
              "vessel_d_m": 6.4, "bundles": 800, "active_height_m": 3.7,
              "power_density_kW_per_L": 54.2, "control_drives": 193,
              "recirculation_pumps": 2, "safety_pumps": 9, "diesels": 3},
    "ABWR": {"thermal_MW": 3925, "electric_MW": 1350, "vessel_h_m": 21.1,
             "vessel_d_m": 7.1, "bundles": 872, "active_height_m": 3.7,
             "power_density_kW_per_L": 51, "control_drives": 205,
             "recirculation_pumps": 10, "safety_pumps": 18, "diesels": 3},
    "ESBWR": {"thermal_MW": 4500, "electric_MW": 1550, "vessel_h_m": 27.7,
              "vessel_d_m": 7.1, "bundles": 1132, "active_height_m": 3.0,
              "power_density_kW_per_L": 54, "control_drives": 269,
              "recirculation_pumps": 0, "safety_pumps": 0, "diesels": 0},
}

# --- Table 11.5 (printed p. 393): the PWR evolution -------------------------
GEN_III_PWR = {
    "AP1000": {"thermal_MW": 3400, "electric_MW": 1117, "loops": 2,
               "hot_leg_C": 321, "bundles": 157, "lattice": 17,
               "active_height_m": 4.3, "linear_heat_rate_W_per_cm": 187,
               "control_clusters": 53, "vessel_id_cm": 399,
               "vessel_flow_m3_per_h": 68100},
    "EPR": {"thermal_MW": 4324, "electric_MW": 1600, "loops": 4,
            "hot_leg_C": 327, "bundles": 241, "lattice": 17,
            "active_height_m": 4.2, "linear_heat_rate_W_per_cm": 156,
            "control_clusters": 89, "vessel_id_cm": 489,
            "vessel_flow_m3_per_h": 113320},
}

# --- Table 11.6 (printed p. 400): small modular designs, a representative set
SMALL_REACTORS = {
    "CAREM": (27, "PWR", "Argentina", "under construction"),
    "mPower": (180, "PWR", "USA", "conceptual"),
    "KLT-40": (25, "PWR", "Russia", "under construction"),
    "RITM-200": (55, "PWR", "Russia", "under construction"),
    "VBER-300": (295, "PWR", "Russia", "licensing"),
    "SMART": (100, "PWR", "South Korea", "licensed"),
    "IRIS": (100, "PWR", "international", "basic design"),
    "NuScale": (45, "LWR", "USA", "basic design"),
    "Westinghouse SMR": (225, "PWR", "USA", "basic design"),
    "PBMR": (165, "HTGR", "South Africa", "detailed design"),
    "GT-MHR": (285, "HTGR", "Russia", "conceptual"),
    "Fuji MSR": (150, "MSR", "Japan", "conceptual"),
    "BREST": (300, "LFR", "Russia", "detailed design"),
    "SVBR": (55, "LFR", "Russia", "conceptual"),
    "4S": (30, "FNR", "Japan", "detailed design"),
    "S-PRISM": (311, "FBR", "USA", "detailed design"),
    "TerraPower TWR": (10, "TWR", "USA", "preliminary"),
}

# --- §11.5: the six Generation IV systems -----------------------------------
GEN_IV_SYSTEMS = {
    "SCWR": {"name": "supercritical water-cooled", "coolant": "supercritical water",
             "outlet_C": 550, "spectrum": "thermal or fast", "efficiency": 0.44},
    "LFR": {"name": "lead-cooled fast", "coolant": "lead or lead-bismuth",
            "outlet_C": 550, "spectrum": "fast", "efficiency": 0.42},
    "MSR": {"name": "molten salt", "coolant": "fluoride salt",
            "outlet_C": 700, "spectrum": "thermal or fast", "efficiency": 0.44},
    "GFR": {"name": "gas-cooled fast", "coolant": "helium",
            "outlet_C": 850, "spectrum": "fast", "efficiency": 0.48},
    "VHTR": {"name": "very high temperature", "coolant": "helium",
             "outlet_C": 1000, "spectrum": "thermal", "efficiency": 0.50},
    "SFR": {"name": "sodium-cooled fast", "coolant": "sodium",
            "outlet_C": 550, "spectrum": "fast", "efficiency": 0.40},
}

# --- Table 11.1 (printed p. 372): 2013 nuclear share, a representative subset
NUCLEAR_SHARE_2013 = {
    "France": (79, 63.13, 58), "Slovakia": (52, 1.82, 4), "Belgium": (51, 5.89, 7),
    "Ukraine": (48, 13.10, 15), "Sweden": (45, 9.30, 10), "Switzerland": (44, 3.24, 5),
    "Armenia": (40, 0.38, 1), "Slovenia": (39, 0.67, 1), "Bulgaria": (36, 1.91, 2),
    "Hungary": (36, 1.89, 4), "Czech Republic": (35, 3.68, 6),
    "South Korea": (32, 20.70, 23), "Japan": (27, 42.28, 48),
    "Germany": (27, 12.06, 9), "Finland": (26, 2.72, 4), "United States": (21, 101.06, 99),
    "Taiwan": (21, 4.88, 6), "Spain": (19, 7.07, 7), "Russia": (17, 23.64, 33),
    "United Kingdom": (16, 9.21, 16), "Canada": (15, 13.47, 19),
    "India": (3, 5.31, 21), "China": (2, 18.66, 22), "WORLD": (16, 375.41, 435),
}


# --- efficiency  [S&F §11.1.2, Eq. (11.1)] ----------------------------------

def carnot_efficiency(t_in_c, t_out_c):
    """eta = (T_in - T_out)/T_in, absolute temperatures  [S&F Eq. (11.1)].

    The ceiling no heat engine beats.  For a PWR delivering 284 C steam to a
    condenser at ~33 C it is 45%, and the plant achieves 34% -- 75% of Carnot,
    which is a respectable turbine and not a bad reactor."""
    t_in, t_out = t_in_c + 273.15, t_out_c + 273.15
    if t_in <= 0 or t_out <= 0:
        raise ValueError("absolute temperatures must be positive")
    if t_out >= t_in:
        raise ValueError("the sink must be colder than the source")
    return (t_in - t_out) / t_in


def thermal_efficiency(electric_mw, thermal_mw):
    """eta = MW(e)/MW(t)."""
    if thermal_mw <= 0:
        raise ValueError("thermal power must be positive")
    if electric_mw < 0:
        raise ValueError("electric power cannot be negative")
    return electric_mw / thermal_mw


def second_law_ratio(electric_mw, thermal_mw, t_in_c, t_out_c):
    """The achieved efficiency as a fraction of Carnot.

    REFUSES a ratio above 1.  An efficiency that exceeds Carnot is not an
    optimistic estimate, it is a second-law violation, and the most likely cause
    is quoting MW(t) where MW(e) belongs -- an error of a factor of three that
    otherwise looks plausible on both sides."""
    eta = thermal_efficiency(electric_mw, thermal_mw)
    eta_c = carnot_efficiency(t_in_c, t_out_c)
    ratio = eta / eta_c
    if ratio > 1.0:
        raise ValueError(
            "eta = %.3f exceeds the Carnot limit %.3f for %.0f C -> %.0f C. "
            "This is a second-law violation, not a good design; check whether "
            "MW(t) and MW(e) have been swapped." % (eta, eta_c, t_in_c, t_out_c))
    return ratio


def waste_heat(electric_mw, efficiency):
    """Heat rejected to the environment, MW(t).

    The number that sizes the cooling towers and picks the site.  A 1000 MW(e)
    plant at 34% rejects 1940 MW -- nearly twice what it sells."""
    if not 0 < efficiency < 1:
        raise ValueError("efficiency must lie in (0, 1)")
    return electric_mw * (1.0 / efficiency - 1.0)


def coolant_is_liquid(temperature_c, critical_c=WATER_CRITICAL_C):
    """Can this coolant still be liquid at this temperature, at any pressure?

    Above the critical temperature no pressure produces a liquid phase [§11.1.4],
    and a water-moderated core needs liquid water both to moderate and to cool.
    That is a hard ceiling on the core outlet, not a design preference."""
    return temperature_c < critical_c


# --- core geometry and heat ratings  [S&F Tables 11.2-11.3] -----------------

def core_volume(length_m, diameter_m):
    """Active core volume, m^3."""
    if length_m <= 0 or diameter_m <= 0:
        raise ValueError("dimensions must be positive")
    return math.pi * (diameter_m / 2.0) ** 2 * length_m


def power_density(thermal_mw, length_m, diameter_m):
    """kW per litre of core.  A PWR runs at 102, a BWR at 56 -- a factor of 1.8,
    because a BWR must leave room for the steam voids that a PWR forbids."""
    return thermal_mw * 1e3 / (core_volume(length_m, diameter_m) * 1e3)


def specific_power(thermal_mw, fuel_loading_kg):
    """kW per kg of uranium."""
    if fuel_loading_kg <= 0:
        raise ValueError("fuel loading must be positive")
    return thermal_mw * 1e3 / fuel_loading_kg


def total_rod_length(assemblies, rods_per_assembly, active_length_m):
    """Total fuel-rod length in the core, m."""
    return assemblies * rods_per_assembly * active_length_m


def linear_heat_rate(thermal_mw, assemblies, rods_per_assembly, active_length_m):
    """kW per metre of fuel rod -- the number a fuel designer actually works to,
    because it sets the pellet centreline temperature and hence melting."""
    return thermal_mw * 1e3 / total_rod_length(assemblies, rods_per_assembly,
                                               active_length_m)


def surface_heat_flux(linear_kw_per_m, rod_od_mm):
    """MW/m^2 at the clad surface, from the linear rate: q'' = q'/(pi d).

    This is the quantity that departure-from-nucleate-boiling limits, and it is
    why a BWR -- which boils on purpose -- runs a lower flux than a PWR."""
    if rod_od_mm <= 0:
        raise ValueError("rod diameter must be positive")
    return linear_kw_per_m / (math.pi * rod_od_mm * 1e-3) / 1e3


def peaking_factor(max_value, avg_value):
    """max/average, for flux, power density or heat flux.

    ~NE-21 computes 3.64 for a BARE uniform cylinder.  Table 11.2's PWR runs
    2.50 and Table 11.3's BWR 2.20 -- the difference is the reflector, fuel
    zoning and burnable poisons of a real design, and each tenth is saleable
    power."""
    if avg_value <= 0:
        raise ValueError("the average must be positive")
    if max_value < avg_value:
        raise ValueError("a maximum below the average is not a peaking factor")
    return max_value / avg_value


def assembly_width(lattice, pitch_mm):
    """Assembly width from the rod lattice and pitch, cm."""
    return lattice * pitch_mm / 10.0


def cycle_length_days(burnup_gwd_per_t, loading_kg, thermal_mw):
    """Full-power days between refuellings, from the discharge burnup."""
    if thermal_mw <= 0 or loading_kg <= 0 or burnup_gwd_per_t <= 0:
        raise ValueError("all arguments must be positive")
    return burnup_gwd_per_t * (loading_kg / 1e3) / (thermal_mw / 1e3)


def capacity_factor_energy(electric_mw, capacity_factor, years=1.0):
    """Energy actually delivered, MW(e)-years -- the quantity that pays for the
    plant, and the one Table 11.1's capacity column does not give."""
    if not 0 < capacity_factor <= 1:
        raise ValueError("the capacity factor must lie in (0, 1]")
    return electric_mw * capacity_factor * years


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-22  nuclear power reactors\n")

    print("  the 374 C ceiling that sets everything else  [§11.1.4]")
    print("   water's critical temperature   %.0f C" % WATER_CRITICAL_C)
    print("   typical core outlet limit      %.0f C" % TYPICAL_CORE_LIMIT_C)
    print("   PWR steam to the turbine       %.0f C" % PWR["steam_temp_C"])
    eta_c = carnot_efficiency(PWR["steam_temp_C"], 33.0)
    print("   Carnot from 284 C to 33 C      %.3f" % eta_c)
    print("   achieved                       %.3f  = %.0f%% of Carnot"
          % (PWR["efficiency"], 100 * PWR["efficiency"] / eta_c))
    print("   a gas-cooled core at 540 C would allow %.3f"
          % carnot_efficiency(540.0, 33.0))

    print("\n  what 34%% means for the plant")
    for mwe in (1000.0, 1600.0):
        print("   %.0f MW(e) needs %.0f MW(t) and rejects %.0f MW to the environment"
              % (mwe, mwe / 0.34, waste_heat(mwe, 0.34)))

    print("\n  Table 11.2 (PWR) checks against itself")
    print("   quantity              printed    derived")
    print("   efficiency          %9.3f %10.4f"
          % (PWR["efficiency"], thermal_efficiency(PWR["electric_MW"], PWR["thermal_MW"])))
    print("   power density kW/L  %9.1f %10.1f"
          % (PWR["power_density_kW_per_L"],
             power_density(PWR["thermal_MW"], PWR["core_length_m"], PWR["core_diameter_m"])))
    print("   specific power      %9.1f %10.1f"
          % (PWR["specific_power_kW_per_kgU"],
             specific_power(PWR["thermal_MW"], PWR["fuel_loading_kg"])))
    print("   linear heat kW/m    %9.1f %10.1f"
          % (PWR["linear_heat_rate_kW_per_m"],
             linear_heat_rate(PWR["thermal_MW"], PWR["assemblies"],
                              PWR["rods_per_assembly"], PWR["core_length_m"])))
    print("   heat flux MW/m2     %9.3f %10.4f"
          % (PWR["heat_flux_avg_MW_per_m2"],
             surface_heat_flux(PWR["linear_heat_rate_kW_per_m"], PWR["rod_od_mm"])))
    print("   assembly width cm   %9.1f %10.1f"
          % (PWR["assembly_width_cm"],
             assembly_width(PWR["lattice"], PWR["rod_pitch_mm"])))

    print("\n  Table 11.3 (BWR) does not")
    print("   specific power      %9.1f %10.1f  <-- 14%% apart"
          % (BWR["specific_power_kW_per_kgU"],
             specific_power(BWR["thermal_MW"], BWR["fuel_loading_kg"])))
    print("   power density kW/L  %9.1f %10.1f"
          % (BWR["power_density_kW_per_L"],
             power_density(BWR["thermal_MW"], BWR["core_length_m"], BWR["core_diameter_m"])))

    print("\n  PWR against BWR")
    rows = (("thermal MW", "thermal_MW", "%8.0f"), ("efficiency", "efficiency", "%8.2f"),
            ("pressure MPa", "pressure_MPa", "%8.2f"),
            ("power density kW/L", "power_density_kW_per_L", "%8.1f"),
            ("specific power", "specific_power_kW_per_kgU", "%8.1f"),
            ("equil. enrichment %", "equil_enrichment_pct", "%8.1f"),
            ("burnup GWd/tU", "burnup_GWd_per_tU", "%8.1f"),
            ("assemblies", "assemblies", "%8.0f"))
    print("   %-22s %8s %8s" % ("", "PWR", "BWR"))
    for label, key, fmt in rows:
        print(("   %-22s " + fmt + " " + fmt) % (label, PWR[key], BWR[key]))
    print("   peaking (max/avg flux) %8.2f %8.2f"
          % (peaking_factor(PWR["heat_flux_max_MW_per_m2"], PWR["heat_flux_avg_MW_per_m2"]),
             peaking_factor(BWR["heat_flux_max_MW_per_m2"], BWR["heat_flux_avg_MW_per_m2"])))
    print("   -> ~NE-21 gives 3.64 for a BARE uniform cylinder; real cores buy")
    print("      the difference with reflectors, zoning and burnable poisons.")

    print("\n  cycle length from the discharge burnup")
    for name, r in (("PWR", PWR), ("BWR", BWR)):
        d = cycle_length_days(r["burnup_GWd_per_tU"], r["fuel_loading_kg"], r["thermal_MW"])
        print("   %s: %.0f full-power days = %.1f years" % (name, d, d / 365.25))

    print("\n  Generation III: the same steam, fewer moving parts  [Table 11.4]")
    print("   design    MW(e)   eta    bundles  recirc  safety  diesels")
    for name, v in GEN_III_BWR.items():
        print("   %-9s %5.0f %6.3f %8d %7d %7d %8d"
              % (name, v["electric_MW"],
                 thermal_efficiency(v["electric_MW"], v["thermal_MW"]),
                 v["bundles"], v["recirculation_pumps"], v["safety_pumps"],
                 v["diesels"]))
    print("   -> the ESBWR removes every pump and diesel: passive safety is")
    print("      not a better pump, it is no pump.")

    print("\n  Generation IV: escaping the 374 C ceiling  [§11.5]")
    print("   system  coolant                outlet C   eta   spectrum")
    for k, v in sorted(GEN_IV_SYSTEMS.items(), key=lambda kv: kv[1]["outlet_C"]):
        print("   %-7s %-22s %7d %6.2f   %s"
              % (k, v["coolant"], v["outlet_C"], v["efficiency"], v["spectrum"]))
    print("   -> four of the six are FAST, which is the fuel-cycle argument")
    print("      of ~NE-23, not a thermodynamic one.")


if __name__ == "__main__":
    _demo()
