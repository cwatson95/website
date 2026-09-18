"""NE-26  Industrial & research applications: tracers, radiography, NAA, gauges.

Nuclear Science & Engineering trunk, module NE-26 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Chapter 13 (printed pp. 476-510).  Pure stdlib.

Chapter 13 is a CATALOGUE -- three dozen applications, organised by what is
happening physically:

    RADIATION AS A LABEL      tracers: leaks, flows, wear, mixing, dating
    MATERIALS AFFECT RADIATION  gauges: thickness, density, level; radiography;
                                NAA, XRF, PIGE; smoke detectors
    RADIATION AFFECTS MATERIALS  sterilisation, food preservation, polymer
                                 cross-linking, insect control
    NUCLEAR ENERGY AS HEAT       (~NE-22, ~NE-25)

Almost none of it needs new physics.  What it needs is the physics of ~NE-06,
~NE-11 and ~NE-12 applied with an eye on the *sensitivity* -- and that is where
the chapter stops short.  It describes a transmission thickness gauge without
ever asking what thickness the gauge should be designed for; the answer,

    mu * t = 2

exactly, falls out of counting statistics in three lines and is the single most
useful design rule in the chapter.

Two other things are supplied here.  The 99Mo/99mTc generator -- "the most widely
used radioisotope in medical diagnoses" -- is described without the transient
equilibrium that says when to milk it (48.5 hours).  And tracer dilution is
given as V = V0(C0/C) without the observation that makes it practical: only the
RATIO matters, so no absolute calibration is ever needed.
"""

import math

__all__ = [
    "PRODUCTION_ROUTES", "APPLICATION_CATEGORIES", "RADIOGRAPHY_SOURCES",
    "NAA_SENSITIVITY", "PROCESS_DOSES", "GENERATORS",
    "activation_activity", "saturation_fraction", "irradiation_time_for",
    "generator_daughter_activity", "optimal_milking_time",
    "tracer_dilution_volume", "flow_rate_from_tracer", "transit_flow_rate",
    "transmission", "thickness_from_transmission", "gauge_precision",
    "optimal_gauge_thickness", "geometric_unsharpness",
    "naa_detectable_mass", "radiodate",
]

# --- §13.1: the three production routes -------------------------------------
PRODUCTION_ROUTES = {
    "reactor irradiation": {
        "decay": "beta-minus", "examples": ["59Co(n,g)60Co", "14N(n,p)14C",
                                            "6Li(n,a)3H"],
        "note": "neutron-rich products, so beta-minus with gammas"},
    "fission-product recovery": {
        "decay": "beta-minus", "examples": ["137Cs", "90Sr"],
        "note": "chemically separated from spent fuel (~NE-23)"},
    "accelerator": {
        "decay": "beta-plus", "examples": ["65Cu(p,n)65Zn", "68Zn(p,2n)67Ga",
                                           "25Mg(p,a)22Na", "58Ni(p,2p)57Co"],
        "note": "proton-rich products, so positron emitters -- which is why PET "
                "isotopes come from cyclotrons (~NE-27)"},
}

# --- §13.1: radionuclide generators -----------------------------------------
# parent -> (parent T_half h, daughter, daughter T_half h)
GENERATORS = {
    "99Mo": (65.9 * 24, "99mTc", 6.01),
    "137Cs": (30.1 * 365.25 * 24, "137mBa", 2.55 / 60),
}

# --- Table 13.1 (printed p. 478): how the chapter organises itself ----------
APPLICATION_CATEGORIES = {
    "radiation as a label": ["leak detection", "pipeline interfaces",
                             "flow patterns", "flow rates", "labeled reagents",
                             "tracer dilution", "wear analysis", "mixing times",
                             "residence times", "frequency response",
                             "surface temperature", "radiodating"],
    "materials affect radiation": ["radiography", "thickness gauging",
                                   "density gauges", "level gauges",
                                   "absorptiometry", "oil-well logging",
                                   "NAA", "capture-gamma analysis", "XRF",
                                   "PIGE", "molecular structure",
                                   "smoke detectors"],
    "radiation affects materials": ["food preservation", "sterilisation",
                                    "insect control", "polymer modification",
                                    "biological mutation"],
}

# --- Table 13.2 (printed p. 484): gamma sources used in radiography ---------
# nuclide -> (half-life, principal gamma MeV, typical steel thickness cm)
RADIOGRAPHY_SOURCES = {
    "170Tm": (128.6, 0.084, 1.2),        # days
    "192Ir": (73.8, 0.34, 7.5),
    "137Cs": (30.1 * 365.25, 0.662, 10.0),
    "60Co": (5.27 * 365.25, 1.25, 22.0),
}

# --- Table 13.3 (printed p. 489): NAA detection limits, micrograms ----------
# 1 h irradiation at 1e13 cm^-2 s^-1, no interfering elements
NAA_SENSITIVITY = {
    "Eu": 0.0000009, "Ge": 0.00005, "Sm": 0.00009, "Ag": 0.0001, "Ar": 0.0001,
    "As": 0.0002, "Au": 0.0002, "Na": 0.0004, "Sr": 0.0009, "Al": 0.001,
    "Gd": 0.002, "Ga": 0.004, "Ni": 0.004, "Os": 0.004, "Tb": 0.005,
    "Ba": 0.005, "Hf": 0.007, "Th": 0.007, "Ta": 0.009, "Mo": 0.01,
    "Te": 0.01, "Sn": 0.02, "Nd": 0.02, "Bi": 0.05, "Nb": 0.1, "F": 0.2,
    "Ne": 0.4, "Fe": 10.0,
}

# --- §13.5: process doses ---------------------------------------------------
PROCESS_DOSES = {
    "sprout inhibition (potatoes, onions)": (60.0, 150.0),
    "insect disinfestation (grain)": (200.0, 500.0),
    "pasteurisation (milk, poultry)": (1e3, 1e4),
    "medical sterilisation": (2.5e4, 2.5e4),
    "food sterilisation": (2e4, 5e4),
}


# --- production  [S&F §13.1] ------------------------------------------------

def activation_activity(production_rate, half_life, t):
    """A(t) = R(1 - e^{-lambda t}) -- activation in a reactor.

    The saturation activity is R, and it is approached exponentially: no amount
    of extra irradiation gets past it, because at saturation the product decays
    as fast as it is made."""
    if production_rate < 0 or half_life <= 0 or t < 0:
        raise ValueError("rate, half-life and time must be non-negative")
    lam = math.log(2.0) / half_life
    return production_rate * (1.0 - math.exp(-lam * t))


def saturation_fraction(t, half_life):
    """The fraction of saturation activity reached: 1 - 2^{-t/T_half}.

    One half-life gets 50%, three get 87.5%, seven get 99.2%.  Irradiating for
    much more than three half-lives buys almost nothing, which is why production
    schedules are quoted in half-lives and not in hours."""
    if half_life <= 0 or t < 0:
        raise ValueError("half-life and time must be positive")
    return 1.0 - 2.0 ** (-t / half_life)


def irradiation_time_for(fraction, half_life):
    """Irradiation time to reach a given fraction of saturation.

    REFUSES a fraction of 1 or more: saturation is approached asymptotically and
    never reached, so the answer would be infinite."""
    if not 0 < fraction < 1:
        raise ValueError("saturation is asymptotic: a fraction of %g is "
                         "unreachable in finite time" % fraction)
    return -half_life * math.log2(1.0 - fraction)


def generator_daughter_activity(t_hours, parent="99Mo", parent_activity=1.0):
    """Daughter activity after milking, from the Bateman solution for a
    parent-daughter pair  [~NE-07, applied to S&F §13.1's "cow"].

        A_d(t) = A_p(0) * lam_d/(lam_d - lam_p) * (e^{-lam_p t} - e^{-lam_d t})

    S&F describe the 99Mo/99mTc generator as "the most widely used radioisotope
    in medical diagnoses" without the ingrowth that says when to use it."""
    if parent not in GENERATORS:
        raise KeyError("no generator data for %r; have %s"
                       % (parent, sorted(GENERATORS)))
    if t_hours < 0:
        raise ValueError("time cannot be negative")
    tp, _, td = GENERATORS[parent]
    lp, ld = math.log(2.0) / tp, math.log(2.0) / td
    return (parent_activity * ld / (ld - lp)
            * (math.exp(-lp * t_hours) - math.exp(-ld * t_hours)))


def optimal_milking_time(parent="99Mo"):
    """Hours after milking at which the daughter activity peaks:

        t_max = ln(lam_d/lam_p)/(lam_d - lam_p) .

    For 99Mo/99mTc this is 48.5 hours -- about two days, which is exactly why
    hospital generators are delivered weekly and eluted daily."""
    if parent not in GENERATORS:
        raise KeyError("no generator data for %r" % parent)
    tp, _, td = GENERATORS[parent]
    lp, ld = math.log(2.0) / tp, math.log(2.0) / td
    return math.log(ld / lp) / (ld - lp)


# --- tracers  [S&F §13.3] ---------------------------------------------------

def tracer_dilution_volume(v_injected, c_injected, c_mixed):
    """V = V0 (C0/C)  [S&F §13.3.6].

    The practical point S&F make and it is worth repeating: **only the ratio
    matters**.  No absolute activity calibration is needed, no detector
    efficiency, no geometry factor -- measure the same sample twice with the same
    instrument and divide.  That is why the technique works for a river estuary,
    a blast furnace and a human bloodstream alike."""
    if v_injected <= 0 or c_injected <= 0 or c_mixed <= 0:
        raise ValueError("volumes and concentrations must be positive")
    if c_mixed > c_injected:
        raise ValueError("the mixed concentration exceeds the injected one: "
                         "dilution cannot concentrate a tracer")
    return v_injected * c_injected / c_mixed


def flow_rate_from_tracer(injection_rate, downstream_concentration):
    """q = Q0/C  [S&F §13.3.4, the tracer rate balance].

    Inject at a constant Q0 Bq/s and the tracer must reappear downstream at the
    same rate, so the flow follows from one concentration measurement -- with no
    knowledge of the channel's cross-section at all.  That is the whole reason it
    is used on rivers."""
    if injection_rate <= 0 or downstream_concentration <= 0:
        raise ValueError("injection rate and concentration must be positive")
    return injection_rate / downstream_concentration


def transit_flow_rate(distance, peak_time, area):
    """The peak-to-peak method: q = A * distance/t_peak  [S&F §13.3.4].

    Needs a known, constant cross-section, which is why it suits a pipeline and
    the rate-balance method suits a river."""
    if distance <= 0 or peak_time <= 0 or area <= 0:
        raise ValueError("distance, time and area must be positive")
    return area * distance / peak_time


def radiodate(activity_ratio, half_life):
    """t = T_half log2(1/ratio)  [S&F §13.3.12], for a decaying clock."""
    if not 0 < activity_ratio <= 1:
        raise ValueError("the activity ratio must lie in (0, 1]")
    return half_life * math.log2(1.0 / activity_ratio)


# --- gauges  [S&F §13.4] ----------------------------------------------------

def transmission(mu, thickness):
    """I/I0 = e^{-mu t}  [~NE-11], the basis of every gauge in §13.4."""
    if mu < 0 or thickness < 0:
        raise ValueError("mu and thickness must be non-negative")
    return math.exp(-mu * thickness)


def thickness_from_transmission(i_over_i0, mu):
    """t = ln(I0/I)/mu -- the gauge read backwards."""
    if not 0 < i_over_i0 <= 1:
        raise ValueError("the transmission must lie in (0, 1]")
    if mu <= 0:
        raise ValueError("mu must be positive")
    return math.log(1.0 / i_over_i0) / mu


def gauge_precision(mu, thickness, counts_unattenuated):
    """Fractional precision in thickness from counting statistics alone:

        sigma_t/t = e^{mu t/2}/(mu t sqrt(N0)) .

    Two effects fight: a thicker attenuation gives more SIGNAL per unit thickness
    (the mu t in the denominator) and fewer COUNTS (the exponential).  S&F
    describe transmission gauges without ever writing this down, and it is what
    decides the source and the geometry."""
    if mu <= 0 or thickness <= 0 or counts_unattenuated <= 0:
        raise ValueError("mu, thickness and counts must be positive")
    return (math.exp(mu * thickness / 2.0)
            / (mu * thickness * math.sqrt(counts_unattenuated)))


def optimal_gauge_thickness(mu=None):
    """The optimum operating point of a transmission gauge:  mu*t = 2, exactly.

    Minimising `gauge_precision` over mu at fixed t gives d/dmu[e^{mu t/2}/mu] = 0,
    i.e. t/2 = 1/mu.  TWO MEAN FREE PATHS -- and the penalty for missing it is
    real but forgiving: 1.9x worse at mu*t = 0.5, 2.5x worse at 6.

    This is the single most useful design rule in Chapter 13 and the chapter
    does not contain it.

    It applies to a THICKNESS GAUGE, which is optimising the precision of a
    measured thickness.  It does NOT describe Table 13.2's radiography practice:
    those source/thickness pairs run 2 to 9 mean free paths, because radiography
    is optimising contrast and penetration through a fixed workpiece, not the
    variance of a thickness estimate.  Two different problems with two different
    optima, and the module keeps them apart."""
    if mu is None:
        return 2.0
    if mu <= 0:
        raise ValueError("mu must be positive")
    return 2.0 / mu


def geometric_unsharpness(source_size, object_to_film, source_to_object):
    """U_g = F d/(D)  -- the penumbra that limits radiographic resolution.

    Not in S&F, and it is the reason radiography sources are made small and
    placed far away: the blur is proportional to the source size and to how far
    the defect sits from the film."""
    if min(source_size, object_to_film, source_to_object) <= 0:
        raise ValueError("all dimensions must be positive")
    return source_size * object_to_film / source_to_object


def naa_detectable_mass(element, hours=1.0, flux=1e13):
    """Minimum detectable mass, micrograms  [S&F Table 13.3].

    The table is for 1 h at 1e13 cm^-2 s^-1.  Scaling is by the ACTIVITY
    produced, so it improves linearly with flux and with the saturation fraction
    -- not linearly with time, which is the trap: ten hours does not buy ten
    times the sensitivity for a short-lived product."""
    if element not in NAA_SENSITIVITY:
        raise KeyError("no Table 13.3 entry for %r" % element)
    if hours <= 0 or flux <= 0:
        raise ValueError("time and flux must be positive")
    return NAA_SENSITIVITY[element] * (1e13 / flux) * (1.0 / hours)


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-26  industrial and research applications\n")

    print("  the three production routes decide the decay mode  [§13.1]")
    for k, v in PRODUCTION_ROUTES.items():
        print("   %-26s -> %-11s e.g. %s"
              % (k, v["decay"], v["examples"][0]))
    print("   -> proton-rich means positron emission, which is why every PET")
    print("      isotope comes from a cyclotron (~NE-27).")

    print("\n  activation saturates  [§13.1]")
    print("   half-lives   fraction of saturation")
    for n in (0.5, 1, 2, 3, 5, 7, 10):
        print("   %10.1f %20.4f" % (n, saturation_fraction(n, 1.0)))
    print("   -> three half-lives gets 87.5%; ten gets 99.9%. Nobody irradiates")
    print("      for ten.")

    print("\n  the 99Mo cow  [§13.1]")
    t_opt = optimal_milking_time()
    print("   99mTc peaks %.1f h (%.2f d) after milking" % (t_opt, t_opt / 24))
    print("   hours after milking    99mTc activity (per unit 99Mo)")
    for h in (1, 6, 12, 24, 48.5, 72, 120):
        print("   %18.1f %22.4f" % (h, generator_daughter_activity(h)))
    print("   -> delivered weekly, eluted daily: the generator is a way to ship")
    print("      a 6-hour isotope by shipping a 66-day one.")

    print("\n  tracers: only the ratio matters  [§13.3.6]")
    v = tracer_dilution_volume(10.0, 1e6, 2.5)
    print("   10 cm3 at 1e6 Bq/cm3, diluted to 2.5 Bq/cm3 -> %.3e cm3 = %.0f m3"
          % (v, v / 1e6))
    print("   no detector efficiency, no geometry, no absolute calibration.")
    q = flow_rate_from_tracer(1e7, 50.0)
    print("   1e7 Bq/s injected, 50 Bq/m3 downstream -> %.3e m3/s" % q)
    print("   ...and no knowledge of the river's cross-section either.")

    print("\n  the design rule Chapter 13 does not contain")
    print("   mu*t    relative precision (arbitrary units)")
    best = gauge_precision(2.0, 1.0, 1e6)
    for x in (0.2, 0.5, 1.0, 2.0, 3.0, 4.0, 6.0, 8.0):
        p = gauge_precision(x, 1.0, 1e6)
        print("   %5.1f %14.4e   %5.2fx worse than optimal" % (x, p, p / best))
    print("   -> optimum at mu*t = %.1f exactly, and forgiving on either side."
          % optimal_gauge_thickness())

    print("\n  ...but radiography is NOT run at that optimum  [Table 13.2]")
    print("   source    gamma (MeV)   steel (cm)   mu (1/cm)   mu*t")
    for k, (t12, e, thick) in RADIOGRAPHY_SOURCES.items():
        mu = {0.084: 1.5, 0.34: 0.75, 0.662: 0.57, 1.25: 0.42}[e]
        print("   %-9s %10.3f %12.1f %11.2f %7.1f"
              % (k, e, thick, mu, mu * thick))
    print("   -> 2 to 9 mean free paths, because radiography optimises CONTRAST")
    print("      through a fixed workpiece, not the variance of a thickness")
    print("      estimate. Same attenuation law, different objective function.")

    print("\n  NAA sensitivity spans seven decades  [Table 13.3]")
    ranked = sorted(NAA_SENSITIVITY.items(), key=lambda kv: kv[1])
    print("   best:  " + ", ".join("%s %.1e" % (k, v) for k, v in ranked[:4]))
    print("   worst: " + ", ".join("%s %.1e" % (k, v) for k, v in ranked[-3:]))
    print("   -> europium at 0.9 picograms; iron at 10 micrograms. Seven decades")
    print("      of difference, set by cross section and by what gammas follow.")

    print("\n  process doses  [§13.5]")
    for k, (lo, hi) in sorted(PROCESS_DOSES.items(), key=lambda kv: kv[1][0]):
        print("   %-38s %8.0f - %-8.0f Gy" % (k, lo, hi))
    print("   -> sprout inhibition needs 60 Gy; sterilisation 25 000. A factor")
    print("      of 400, and both are called 'irradiation'.")


if __name__ == "__main__":
    _demo()
