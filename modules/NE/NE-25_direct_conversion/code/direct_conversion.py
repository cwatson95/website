"""NE-25  Direct energy conversion: thermoelectric, thermionic, AMTEC, betavoltaic.

Nuclear Science & Engineering trunk, module NE-25 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 12.5-12.11 (printed pp. 449-478).  Pure stdlib.

~NE-22's power plant converts heat to electricity with a turbine, and needs
2000 tonnes of machinery to do it at 34%.  This module is about the alternatives
that have NO MOVING PARTS, and about the one application where that is worth
paying almost any efficiency penalty for: a spacecraft that must run for decades
with nobody to fix it.

The trade is stark.  A thermoelectric converter runs at 5-7%; a turbine runs at
34%.  Voyager 1 has been returning data since 1977 on 470 W of thermoelectrics,
and no turbine has ever run unattended for forty-seven years.

Two things organise the subject.

  * EVERY DEVICE HERE IS STILL A HEAT ENGINE, and still bounded by Carnot.
    Thermoelectric, thermionic, AMTEC and Stirling all take heat in hot and
    reject it cold; what they replace is the TURBINE, not the thermodynamics.
    Only the betavoltaic escapes -- it converts particle energy directly, and
    pays for it with microwatts.

  * THE ISOTOPE IS CHOSEN BY HALF-LIFE, NOT BY POWER.  Table 12.2's specific
    powers span a factor of 1500, and 210Po's 144 W/g looks unbeatable until you
    notice its 138-day half-life.  238Pu's 0.558 W/g and 87.7 years is why every
    outer-planet mission has flown it, and why the world ran out.

Table 12.2 is the quantitative heart of the chapter, and it is fully
self-consistent: all nine specific powers reproduce from specific activity times
recoverable energy, and all nine specific activities reproduce from the half-life
and mass number.
"""

import math

__all__ = [
    "CI_TO_BQ", "MEV_TO_J", "AVOGADRO", "RICHARDSON_A", "K_B_EV",
    "RADIONUCLIDE_SOURCES", "SNAP_GENERATORS", "SPACE_REACTORS",
    "CONVERTER_TYPES",
    "specific_activity", "specific_power", "activity_per_watt",
    "power_after", "fuel_mass_for_power", "mission_sizing",
    "carnot_efficiency", "thermoelectric_efficiency", "zt_for_efficiency",
    "richardson_current", "thermionic_ideal_efficiency",
    "betavoltaic_power", "shielding_needed",
]

CI_TO_BQ = 3.7e10
MEV_TO_J = 1.602177e-13
AVOGADRO = 6.022141e23
SECONDS_PER_YEAR = 3.155760e7
RICHARDSON_A = 120.17          # A cm^-2 K^-2, the Richardson constant
K_B_EV = 8.617333e-5

# --- Table 12.2 (printed p. 469): the nine practical thermal sources --------
# nuclide -> (half-life y, recoverable MeV/decay, Ci/g, W/g, Ci/W, emitter,
#             cm of Pb for the stated shielding case)
RADIONUCLIDE_SOURCES = {
    "144Ce": (284.9 / 365.25, 1.30, 3190.0, 24.6, 130.0, "beta", 6.5),
    "90Sr": (28.84, 1.132, 136.0, 0.916, 149.0, "beta", 0.0),
    "137Cs": (30.07, 0.187, 87.0, 0.0966, 901.0, "beta", 7.5),
    "147Pm": (2.623, 0.062, 927.0, 0.341, 2722.0, "beta", 0.0),
    "60Co": (5.271, 0.0962, 1131.0, 0.644, 1755.0, "beta", 18.0),
    "242Cm": (162.8 / 365.25, 6.11, 3307.0, 120.0, 27.6, "alpha", None),
    "244Cm": (18.101, 5.803, 80.9, 2.78, 29.1, "alpha", None),
    "210Po": (138.4 / 365.25, 5.411, 4494.0, 144.0, 31.2, "alpha", 0.0),
    "238Pu": (87.7, 5.495, 17.1, 0.558, 30.7, "alpha", None),
}
# mass numbers, for the specific-activity cross-check
MASS_NUMBERS = {"144Ce": 144, "90Sr": 90, "137Cs": 137, "147Pm": 147,
                "60Co": 60, "242Cm": 242, "244Cm": 244, "210Po": 210,
                "238Pu": 238}

# --- Table 12.1 (printed p. 452): a representative slice of the SNAP series --
# name -> (function, fuel, W(e), mass kg, design life y)
SNAP_GENERATORS = {
    "SNAP-3": ("demonstration", "210Po", 2.5, 1.82, 90 / 365.25),
    "SNAP-3A": ("satellite power", "238Pu", 2.7, 2.10, 5.0),
    "SNAP-7A": ("navigation buoy", "90Sr", 10.0, 850.0, 2.0),
    "SNAP-7B": ("navigation light", "90Sr", 60.0, 2100.0, 2.0),
    "SNAP-9A": ("satellite power", "238Pu", 25.0, 12.0, 5.0),
    "SNAP-11": ("moon probe", "242Cm", 23.0, 14.0, 90 / 365.25),
    "SNAP-19": ("Viking/Pioneer", "238Pu", 45.0, None, 5.0),
    "SNAP-27": ("Apollo lunar modules", "238Pu", 60.0, 14.0, 5.0),
    "SNAP-29": ("various missions", "210Po", 500.0, 230.0, 90 / 365.25),
}

# --- Table 12.3 (printed p. 477): space power reactors ----------------------
SPACE_REACTORS = {
    "SNAP-10A": {"country": "US", "kwt": 45, "kwe": 0.65, "converter": "TE",
                 "fuel": "UZrx", "u235_kg": 4.3, "mass_kg": 435, "flights": 1},
    "SP-100": {"country": "US", "kwt": 2000, "kwe": 100, "converter": "TE",
               "fuel": "UN", "u235_kg": 140, "mass_kg": 5422, "flights": 0},
    "BUK": {"country": "USSR", "kwt": 100, "kwe": 3, "converter": "TE",
            "fuel": "UMo", "u235_kg": 30, "mass_kg": 930, "flights": 31},
    "TOPAZ-I": {"country": "USSR", "kwt": 150, "kwe": 5, "converter": "TI",
                "fuel": "UO2", "u235_kg": 11.5, "mass_kg": 980, "flights": 2},
    "TOPAZ-II": {"country": "USSR", "kwt": 135, "kwe": 5.5, "converter": "TI",
                 "fuel": "UO2", "u235_kg": 25, "mass_kg": 1061, "flights": 0},
}

# §§12.5-12.9, as the chapter characterises them
CONVERTER_TYPES = {
    "thermoelectric": {"efficiency": (0.05, 0.10), "heat_engine": True,
                       "moving_parts": False,
                       "note": "Seebeck; a few tenths of a volt per cell"},
    "thermionic": {"efficiency": (0.01, 0.10), "heat_engine": True,
                   "moving_parts": False,
                   "note": "needs emitter temperatures above ~1400 K"},
    "AMTEC": {"efficiency": (0.15, 0.25), "heat_engine": True,
              "moving_parts": False,
              "note": "sodium through beta-alumina; the best no-moving-parts option"},
    "Stirling": {"efficiency": (0.25, 0.30), "heat_engine": True,
                 "moving_parts": True,
                 "note": "highest efficiency, but a piston that must not seize"},
    "betavoltaic": {"efficiency": (0.005, 0.08), "heat_engine": False,
                    "moving_parts": False,
                    "note": "converts particle energy directly; microwatts"},
}


# --- radionuclide sources  [S&F Table 12.2] ---------------------------------

def specific_activity(half_life_y, mass_number):
    """Ci/g, from lambda N: ln2/T_half x N_A/A.

    Table 12.2's specific-activity row reproduces from this to better than 1.3%
    for all nine nuclides (90Sr is the worst, plausibly because its entry is
    quoted in secular equilibrium with 90Y), which is the first check that the
    table is sound."""
    if half_life_y <= 0 or mass_number <= 0:
        raise ValueError("half-life and mass number must be positive")
    lam = math.log(2.0) / (half_life_y * SECONDS_PER_YEAR)
    return lam * AVOGADRO / mass_number / CI_TO_BQ


def specific_power(specific_activity_ci_per_g, mev_per_decay):
    """W/g = (Ci/g)(3.7e10 dec/s/Ci)(MeV/dec)(1.602e-13 J/MeV).

    Table 12.2's specific-power row reproduces from its own activity and energy
    rows to better than 0.5% for all nine nuclides -- so the table's three
    numeric rows are mutually consistent and only one of them is independent."""
    if specific_activity_ci_per_g < 0 or mev_per_decay < 0:
        raise ValueError("activity and energy must be non-negative")
    return specific_activity_ci_per_g * CI_TO_BQ * mev_per_decay * MEV_TO_J


def activity_per_watt(specific_activity_ci_per_g, mev_per_decay):
    """Ci needed per thermal watt -- the number that sets the shielding and the
    transport licence, and which is NOT proportional to the power."""
    p = specific_power(specific_activity_ci_per_g, mev_per_decay)
    if p <= 0:
        raise ValueError("cannot divide by zero specific power")
    return specific_activity_ci_per_g / p


def power_after(years, half_life_y, initial_power=1.0):
    """Thermal power remaining after a given time -- pure exponential decay.

    This is why the isotope is chosen by half-life and not by specific power.
    210Po's 144 W/g is 1500 times 137Cs's, and after two years there is 2e-2 of
    it left; 238Pu still has 98%."""
    if years < 0 or half_life_y <= 0:
        raise ValueError("time must be non-negative and half-life positive")
    return initial_power * math.exp(-years * math.log(2.0) / half_life_y)


def fuel_mass_for_power(watts_electric, nuclide, efficiency=0.06,
                        years=0.0, sources=None):
    """Grams of a radionuclide needed to deliver a given ELECTRICAL power after a
    given time, at a given converter efficiency.

    The `years` argument is the point: a mission is sized by its power at
    END of life, not at launch."""
    src = RADIONUCLIDE_SOURCES if sources is None else sources
    if nuclide not in src:
        raise KeyError("no Table 12.2 entry for %r; have %s"
                       % (nuclide, sorted(src)))
    if not 0 < efficiency < 1:
        raise ValueError("efficiency must lie in (0, 1)")
    half_life, _, _, w_per_g, _, _, _ = src[nuclide]
    thermal = watts_electric / efficiency
    return thermal / (w_per_g * power_after(years, half_life))


def mission_sizing(watts_electric, mission_years, efficiency=0.06):
    """Fuel mass for every Table 12.2 nuclide, sized to deliver the power at END
    of mission.  Returns [(nuclide, grams), ...] sorted by mass.

    The ranking inverts as the mission lengthens, which is the whole content of
    §12.10: short missions want specific power, long missions want half-life."""
    out = []
    for nuc in RADIONUCLIDE_SOURCES:
        try:
            out.append((nuc, fuel_mass_for_power(watts_electric, nuc,
                                                 efficiency, mission_years)))
        except OverflowError:
            out.append((nuc, float("inf")))
    return sorted(out, key=lambda kv: kv[1])


def shielding_needed(nuclide):
    """cm of lead for Table 12.2's stated case (10 rad/h at 1 m from 100 W).

    None means the source is a neutron emitter (the curium isotopes, by
    spontaneous fission) and lead does not help; 0 means negligible."""
    if nuclide not in RADIONUCLIDE_SOURCES:
        raise KeyError("no Table 12.2 entry for %r" % nuclide)
    return RADIONUCLIDE_SOURCES[nuclide][6]


# --- the converters  [S&F §§12.5-12.9] --------------------------------------

def carnot_efficiency(t_hot_k, t_cold_k):
    """(T_h - T_c)/T_h  [S&F §12.6.1].  Every device in this chapter except the
    betavoltaic is a heat engine and is bounded by it."""
    if t_hot_k <= 0 or t_cold_k <= 0:
        raise ValueError("absolute temperatures must be positive")
    if t_cold_k >= t_hot_k:
        raise ValueError("the sink must be colder than the source")
    return (t_hot_k - t_cold_k) / t_hot_k


def thermoelectric_efficiency(zt, t_hot_k, t_cold_k):
    """The standard thermoelectric efficiency, which S&F quote results from but
    never write down:

        eta = eta_Carnot (sqrt(1+ZT) - 1)/(sqrt(1+ZT) + T_c/T_h),

    with ZT the dimensionless figure of merit at the mean temperature.  The
    second factor is the penalty for using a solid instead of a working fluid,
    and it is severe: ZT = 1 -- the best materials achieved for decades -- costs
    a factor of five, which is exactly how 10% comes out of a 50% Carnot limit."""
    if zt < 0:
        raise ValueError("ZT cannot be negative")
    eta_c = carnot_efficiency(t_hot_k, t_cold_k)
    m = math.sqrt(1.0 + zt)
    return eta_c * (m - 1.0) / (m + t_cold_k / t_hot_k)


def zt_for_efficiency(target, t_hot_k, t_cold_k, lo=0.0, hi=1e4):
    """The ZT a material would need to reach a target efficiency.

    REFUSES a target above Carnot: no value of ZT reaches it, and the bisection
    would otherwise run to its upper bound and return a plausible-looking
    number."""
    eta_c = carnot_efficiency(t_hot_k, t_cold_k)
    if target >= eta_c:
        raise ValueError("eta = %.3f is at or above the Carnot limit %.3f for "
                         "%.0f K -> %.0f K; no ZT reaches it"
                         % (target, eta_c, t_hot_k, t_cold_k))
    for _ in range(300):
        mid = 0.5 * (lo + hi)
        if thermoelectric_efficiency(mid, t_hot_k, t_cold_k) < target:
            lo = mid
        else:
            hi = mid
    return 0.5 * (lo + hi)


def richardson_current(t_k, work_function_ev, a=RICHARDSON_A):
    """Thermionic emission current density, A/cm^2:  J = A T^2 exp(-phi/kT).

    S&F describe thermionic conversion without the emission law it rests on.
    The exponential is why §12.6.1's "emitter temperatures in excess of 1400 K"
    is not a preference: at 1000 K a 2.5 eV emitter gives 1e-9 A/cm^2, and at
    1800 K it gives 0.4."""
    if t_k <= 0 or work_function_ev <= 0:
        raise ValueError("temperature and work function must be positive")
    return a * t_k ** 2 * math.exp(-work_function_ev / (K_B_EV * t_k))


def thermionic_ideal_efficiency(t_emitter_k, t_collector_k,
                                phi_emitter=2.6, phi_collector=1.4):
    """A first-order thermionic efficiency: the useful work per emitted electron
    (phi_e - phi_c) against the energy it carries away (phi_e + 2kT_e).

    Deliberately crude, and it lands in §12.6.1's quoted 1-10% band.  The point
    is the structure: the output voltage is a DIFFERENCE of work functions, so
    the collector must be a poor emitter and the emitter a good one -- and both
    must stay that way while sitting millimetres apart at 1800 K."""
    if phi_emitter <= phi_collector:
        raise ValueError("the emitter work function must exceed the collector's "
                         "or the cell produces no voltage")
    eta_c = carnot_efficiency(t_emitter_k, t_collector_k)
    useful = phi_emitter - phi_collector
    carried = phi_emitter + 2.0 * K_B_EV * t_emitter_k
    return min(useful / carried, eta_c)


def betavoltaic_power(activity_bq, mean_beta_ev, efficiency=0.02):
    """Electrical power from a betavoltaic cell, W  [S&F §12.9.2].

    NOT a heat engine -- the beta particles create electron-hole pairs directly,
    so there is no Carnot bound and no temperature difference to maintain.  The
    price is scale: a curie of tritium at 5.7 keV mean beta energy and 2%
    conversion gives 34 microwatts, which is why betavoltaics power pacemakers
    and memory backup and nothing else."""
    if activity_bq < 0 or mean_beta_ev < 0:
        raise ValueError("activity and energy must be non-negative")
    if not 0 < efficiency < 1:
        raise ValueError("efficiency must lie in (0, 1)")
    return activity_bq * mean_beta_ev * 1.602177e-19 * efficiency


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-25  direct energy conversion\n")

    print("  Table 12.2 checks against itself")
    print("   nuclide   T1/2 (y)   W/g printed   W/g derived   Ci/g printed  derived")
    for nuc, (t12, e, a, w, _, _, _) in RADIONUCLIDE_SOURCES.items():
        print("   %-9s %8.3f %13.4f %13.4f %14.1f %8.1f"
              % (nuc, t12, w, specific_power(a, e), a,
                 specific_activity(t12, MASS_NUMBERS[nuc])))

    print("\n  the isotope is chosen by half-life, not by specific power")
    print("   nuclide   W/g     fraction of power left after")
    print("                     1 y      5 y     20 y     50 y")
    for nuc in ("210Po", "242Cm", "144Ce", "147Pm", "244Cm", "90Sr", "238Pu"):
        t12 = RADIONUCLIDE_SOURCES[nuc][0]
        print("   %-9s %7.3f %8.4f %8.4f %8.4f %8.4f"
              % (nuc, RADIONUCLIDE_SOURCES[nuc][3],
                 power_after(1, t12), power_after(5, t12),
                 power_after(20, t12), power_after(50, t12)))

    print("\n  sizing a 100 W(e) RTG at 6% conversion")
    for years in (0.25, 5.0, 30.0):
        best = mission_sizing(100.0, years)[:3]
        print("   %5.2f-year mission: %s"
              % (years, ", ".join("%s %.0f g" % (n, g) for n, g in best)))
    print("   -> 210Po wins a 3-month mission and is useless past a year.")
    print("      By MASS the curiums win the long ones -- but both are strong")
    print("      spontaneous-fission neutron emitters that lead cannot shield,")
    print("      so every outer-planet mission has flown 238Pu instead.")

    print("\n  every one of these is still a heat engine  [§12.6.1]")
    th, tc = 1300.0, 500.0
    print("   Carnot from %.0f K to %.0f K: %.3f" % (th, tc, carnot_efficiency(th, tc)))
    print("   ZT     thermoelectric efficiency   as a fraction of Carnot")
    for zt in (0.5, 1.0, 2.0, 4.0, 10.0):
        e = thermoelectric_efficiency(zt, th, tc)
        print("   %5.1f %22.4f %20.3f" % (zt, e, e / carnot_efficiency(th, tc)))
    print("   -> ZT = 1 costs a factor of five. That is why a 60%-Carnot")
    print("      temperature difference yields a 7% converter.")

    print("\n  thermionics need 1400 K for a reason  [§12.6.1]")
    print("   T (K)     J (A/cm2), phi = 2.5 eV")
    for t in (800.0, 1000.0, 1400.0, 1800.0, 2200.0):
        print("   %7.0f %14.4e" % (t, richardson_current(t, 2.5)))
    print("   ideal efficiency at 1800 K -> 800 K: %.3f"
          % thermionic_ideal_efficiency(1800.0, 800.0))

    print("\n  the one device that is not a heat engine  [§12.9.2]")
    for nuc, act, e in (("3H", 3.7e10, 5670.0), ("63Ni", 3.7e10, 17400.0)):
        print("   1 Ci of %-5s at %6.0f eV mean beta -> %.1f uW"
              % (nuc, e, 1e6 * betavoltaic_power(act, e)))
    print("   no Carnot bound, no temperature difference -- and microwatts.")

    print("\n  space reactors  [Table 12.3]")
    print("   name         kW(t)  kW(e)   eta    conv   kg    kg/kW(e)  flights")
    for k, v in SPACE_REACTORS.items():
        print("   %-12s %5.0f %6.1f %6.3f %6s %6.0f %9.0f %8d"
              % (k, v["kwt"], v["kwe"], v["kwe"] / v["kwt"], v["converter"],
                 v["mass_kg"], v["mass_kg"] / v["kwe"], v["flights"]))
    print("   -> BUK flew 31 times at 3% efficiency. SP-100 was 5% efficient,")
    print("      five tonnes, and never flew at all.")


if __name__ == "__main__":
    _demo()
