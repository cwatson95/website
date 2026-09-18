"""NE-18  Radiation health effects: deterministic and stochastic risk, LNT,
protection standards.

Nuclear Science & Engineering trunk, module NE-18 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 9.5-9.10 (printed pp. 288-316).  Pure stdlib.

~NE-17 produced a number in sieverts.  This module turns it into a statement
about people, and the first thing to understand is that there are TWO kinds of
statement and they behave in opposite ways:

  DETERMINISTIC effects have a THRESHOLD, and above it SEVERITY grows with dose.
    Erythema, cataract, sterility, marrow failure.  Below the threshold nobody is
    affected -- not "few", NOBODY.  A dose of 0.5 Gy causes no erythema in anyone
    at all, and 6 Gy causes it in half.  These are the effects of an accident.

  STOCHASTIC effects have no established threshold, and dose changes the
    PROBABILITY, not the severity.  Cancer and hereditary illness.  A radiogenic
    cancer is indistinguishable from a spontaneous one, so the effect is visible
    only as a statistical excess -- and it is not visible at all below ~0.2 Gy,
    which is exactly the range every regulation is written about.

That last sentence is the whole difficulty of the subject.  Every number in
Sections 9.7-9.9 is an extrapolation from high-dose data (mostly Hiroshima and
Nagasaki) into a region where the effect has never been measured and, at
attainable statistical power, cannot be.  The linear no-threshold model is the
extrapolation that regulation uses; §9.10 is the book's own account of why that
choice is contested.  The module carries all five candidate dose-effect shapes
and fits none of them, because the data do not distinguish them.

One consequence deserves separating out, because it is where LNT is most often
abused.  Linearity means a collective dose predicts the same number of deaths
however it is spread: 10^7 people at 0.01 mSv "gives" as many cancers as 1000
people at 100 mSv.  S&F state this as a property of the model.  ICRP-103 states
that computing deaths that way from trivial individual doses "is not reasonable
and should be avoided".  `radiogenic_cancer_deaths` therefore REFUSES trivial
individual doses unless explicitly overridden.
"""

import math

__all__ = [
    "DETERMINISTIC_EFFECTS", "LETHAL_DOSES", "SUBLETHAL_EFFECTS",
    "PRODROMAL_SYMPTOMS", "ARS_STAGES",
    "deterministic_effects_at", "lethality_fraction", "midline_from_free_field",
    "GENETIC_RISKS", "GENETIC_BASELINE_TOTAL", "MOUSE_INDUCED_RATE_PER_GY",
    "HUMAN_SPONTANEOUS_RATE", "doubling_dose", "hereditary_risk",
    "CANCER_BASELINE", "LIFETIME_CANCER_RISK", "EXPOSURE_SCENARIOS", "DDREF",
    "cancer_risk_at_age", "scaled_cancer_risk", "cancer_risk_per_gy",
    "radiogenic_cancer_deaths", "excess_relative_risk",
    "probability_of_causation",
    "RN222_CHAIN", "PO218_ALPHA_MEV", "PO214_ALPHA_MEV",
    "potential_alpha_energy_per_bq", "equilibrium_equivalent_concentration",
    "annual_radon_exposure", "RADON_RISK_BY_POPULATION",
    "RADON_RISK_BY_AGE_DURATION", "radon_lung_cancer_risk",
    "WL_MEV_PER_LITRE", "WLM_HOURS", "wlm_to_bq_h_per_m3", "bq_h_per_m3_to_wlm",
    "NCRP_1987_LIMITS", "occupational_limit_sv", "public_limit_sv",
    "cumulative_dose_guidance_sv", "FATAL_CANCER_RISK_PER_SV",
    "HEREDITARY_RISK_PER_SV",
    "lnt", "linear_with_threshold", "quadratic", "linear_quadratic", "hormetic",
    "TABLE_9_11_TOTAL_ERRATA", "EXAMPLE_9_7_DEATHS_ERRATA",
    "EXAMPLE_9_7_RESPIRATORY_ERRATA",
]

# --- deterministic effects  [S&F §9.5, Tables 9.7-9.10] ------------------

# Table 9.7 (printed p. 290): median effective dose D50 and threshold Dth, in Gy,
# for gamma photons at <= 0.06 Gy/h.  Source: Scott and Hahn [1989].
DETERMINISTIC_EFFECTS = [
    ("skin", "erythema", 6.0, 1.0, 3.0, 1.0),
    ("skin", "moist desquamation", 30.0, 6.0, 10.0, 2.0),
    ("ovary", "permanent ovulation suppression", 3.0, 1.0, 0.6, 0.4),
    ("testes", "sperm count suppressed for 2 y", 0.6, 0.1, 0.3, 0.1),
    ("eye lens", "cataract", 3.1, 0.9, 0.5, 0.5),
    ("lung", "death", 70.0, 30.0, 40.0, 20.0),        # at 0.5 Gy/h
    ("GI system", "vomiting", 2.0, 0.5, 0.5, 0.0),
    ("GI system", "diarrhea", 3.0, 0.8, 1.0, 0.0),
    ("GI system", "death", 15.0, 5.0, 8.0, 0.0),
    ("bone marrow", "death", 3.8, 0.6, 1.8, 0.3),
]

# Table 9.8 (printed p. 292): mid-line absorbed dose, Gy.  Anno et al. [1989].
LETHAL_DOSES = {
    "LD5/60": (2.0, 2.5), "LD10/60": (2.5, 3.0), "LD50/60": (3.0, 3.5),
    "LD90/60": (3.5, 4.5), "LD99/60": (4.5, 5.5),
}

# Table 9.9 (printed p. 293): effects of high sublethal doses, Gy.
SUBLETHAL_EFFECTS = [
    ((0.05, 0.25), "detectable only by chromosome analysis"),
    ((0.25, 0.50), "detectable in groups by white-blood-cell count"),
    ((0.50, 0.75), "readily detectable in a specific individual"),
    ((0.50, 1.00), "mild effects on the first day; slight blood-count depression"),
    ((0.75, 1.25), "vomiting in 10% of those exposed"),
    ((1.00, 2.00), "nausea and vomiting in 20-70%; 20-35% drop in blood cell "
                   "production from loss of marrow stem cells"),
    ((1.50, 2.00), "transient disability and clear haematological change in a "
                   "majority"),
]

# Table 9.10 (printed p. 293): the prodromal syndrome.  Langham [1967].
PRODROMAL_SYMPTOMS = {
    "gastrointestinal": ["anorexia", "nausea", "vomiting", "diarrhea",
                         "intestinal cramps", "salivation", "dehydration"],
    "neuromuscular": ["fatigue", "apathy", "sweating", "fever", "headache",
                      "hypotension", "hypotensive shock"],
}

# §9.5.3 (printed p. 294), after Wald [1967].
ARS_STAGES = [
    ("prodromal", 0.0, 48.0, "gastrointestinal and neuromuscular symptoms; "
                             "lymphocytes fall within 24 h"),
    ("latent", 48.0, 504.0, "remission of prodromal symptoms -- apparent "
                            "well-being, and the most dangerous stage to "
                            "mistake for recovery"),
    ("manifest illness", 504.0, 1344.0, "sharply defined GI and haematological "
                                        "symptoms; secondary infection, "
                                        "dehydration, electrolyte loss"),
    ("recovery", 1344.0, float("inf"), "surviving six weeks makes permanent "
                                       "recovery likely"),
]

MIDLINE_PER_ROENTGEN_RAD = 2.0 / 3.0      # §9.5.3: mid-line rad ~ 2/3 free-field R


def deterministic_effects_at(dose_gy, use_threshold=True):
    """Which Table 9.7 endpoints are possible at this dose.

    Returns [(organ, endpoint, D50, Dth), ...] for every entry whose THRESHOLD
    the dose exceeds.  With `use_threshold=False` the comparison is against D50
    instead, i.e. effects expected in the majority.

    Below its threshold an effect does not occur in anyone -- that is what
    distinguishes a deterministic effect from a stochastic one, and it is why
    this function returns an empty list rather than a small probability."""
    if dose_gy < 0:
        raise ValueError("dose cannot be negative")
    key = 4 if use_threshold else 2
    return [(e[0], e[1], e[2], e[4]) for e in DETERMINISTIC_EFFECTS
            if dose_gy >= e[key]]


def lethality_fraction(midline_dose_gy):
    """Approximate 60-day lethality without medical treatment, from Table 9.8.

    Linear interpolation between the midpoints of the tabulated LD bands.  Below
    the LD5 band it returns 0 and above the LD99 band 1, which is the shape the
    table asserts and NOT an extrapolation of a fitted curve.

    The dose is the MID-LINE absorbed dose (the average near the abdomen), which
    for photons is about two thirds of the free-field exposure in roentgens --
    a distinction that matters by 50% and is routinely lost."""
    if midline_dose_gy < 0:
        raise ValueError("dose cannot be negative")
    pts = sorted((0.5 * (lo + hi), float(name.split("LD")[1].split("/")[0]) / 100.0)
                 for name, (lo, hi) in LETHAL_DOSES.items())
    if midline_dose_gy <= pts[0][0]:
        return 0.0 if midline_dose_gy < LETHAL_DOSES["LD5/60"][0] else pts[0][1]
    if midline_dose_gy >= pts[-1][0]:
        return 1.0 if midline_dose_gy > LETHAL_DOSES["LD99/60"][1] else pts[-1][1]
    for (d0, f0), (d1, f1) in zip(pts, pts[1:]):
        if d0 <= midline_dose_gy <= d1:
            return f0 + (f1 - f0) * (midline_dose_gy - d0) / (d1 - d0)
    raise AssertionError("unreachable")


def midline_from_free_field(exposure_roentgen):
    """Mid-line absorbed dose (rad) from a free-field exposure (R)  [§9.5.3].

    S&F's rule of thumb: the mid-line dose in rad is about 2/3 the free-field
    exposure in roentgens.  Note this is smaller than ~NE-17's 1 R = 0.873 rad in
    air, because the body attenuates its own midline."""
    if exposure_roentgen < 0:
        raise ValueError("exposure cannot be negative")
    return MIDLINE_PER_ROENTGEN_RAD * exposure_roentgen


# --- hereditary effects  [S&F §9.6, Table 9.11] --------------------------

# Table 9.11 (printed p. 296): (baseline per million progeny, first-generation
# cases/Gy, second-generation cases/Gy), each range as (low, high).
GENETIC_RISKS = {
    "Mendelian dominant and X-linked": (16500, (750, 1500), (1300, 2500)),
    "Mendelian recessive": (7500, (0, 0), (0, 0)),
    "chromosomal": (4000, None, None),       # folded into the other rows
    "chronic multifactorial": (650000, (250, 1200), (250, 1200)),
    "congenital abnormalities": (60000, (2000, 2000), (2400, 3000)),
}
GENETIC_BASELINE_TOTAL = 738000

MOUSE_INDUCED_RATE_PER_GY = 3.6e-6        # §9.6.2 (printed p. 296)
HUMAN_SPONTANEOUS_RATE = 2.95e-6          # per gene locus per generation

# Table 9.11's printed second-generation total.  Its own column sums to 3950.
TABLE_9_11_TOTAL_ERRATA = (3930, 6700)


def doubling_dose(human_spontaneous=HUMAN_SPONTANEOUS_RATE,
                  mouse_induced=MOUSE_INDUCED_RATE_PER_GY):
    """DD = R_human / R_mice  [S&F §9.6.2], in Gy.

    The gonad dose that adds as many mutations as arise spontaneously.  Note what
    it is made of: a spontaneous rate measured in humans divided by an induced
    rate measured in MICE, because no induced human rate exists -- not even from
    the atomic-bomb survivors, in whom no heritable effect has ever been
    demonstrated.  The 0.82 Gy this gives is rounded to 1 Gy throughout."""
    if human_spontaneous <= 0 or mouse_induced <= 0:
        raise ValueError("mutation rates must be positive")
    return human_spontaneous / mouse_induced


def hereditary_risk(baseline, dd_gy, mc, prcf):
    """Risk per Gy = P x (1/DD) x MC x PRCF   [S&F Eq. (9.13)].

    MC is the mutation component (what fraction of the disease frequency
    responds to mutation rate at all) and PRCF the potential recoverability
    correction factor (what fraction of induced mutations could show up as human
    disease).  For chronic multifactorial disease MC = 0.02 and PRCF = 0.02-0.09,
    i.e. the product is under 0.2% -- which is the quantitative reason the huge
    650 000 per million baseline contributes so little radiogenic risk."""
    if dd_gy <= 0:
        raise ValueError("doubling dose must be positive")
    if not 0 <= mc <= 1 or not 0 <= prcf <= 1:
        raise ValueError("MC and PRCF are fractions in [0, 1]")
    return baseline * mc * prcf / dd_gy


# --- cancer  [S&F §9.7, Tables 9.12-9.14] --------------------------------

# Table 9.12 (printed p. 298): 2002 U.S. rates per 100 000 per year.
# site -> (incidence male, incidence female, deaths male, deaths female)
CANCER_BASELINE = {
    "leukemia": (14.6, 8.8, 10.1, 5.7),
    "lymphoma": (25.1, 17.9, 10.2, 6.5),
    "respiratory": (94.7, 55.8, 76.2, 42.2),
    "digestive": (106.9, 71.4, 59.1, 35.9),
    "breast": (None, 124.9, None, 25.5),
    "genital": (167.3, 48.9, 28.6, 16.7),
    "urinary": (56.3, 19.1, 13.9, 5.3),
    "other": (80.6, 58.2, 41.8, 24.9),
}
CANCER_BASELINE_TOTAL = (545.5, 405.0, 239.9, 162.7)

# Table 9.13 (printed p. 302): excess lifetime cases per 100 000 exposed to
# 0.1 Gy, by age at exposure.  [sex][kind][endpoint] -> {age: value}
_AGES = (0, 10, 20, 30, 40, 50, 60, 70, 80)
LIFETIME_CANCER_RISK = {
    "female": {
        "incidence": {"leukemia": (185, 86, 71, 63, 62, 62, 57, 51, 37),
                      "solid": (4592, 2525, 1575, 1002, 824, 678, 529, 358, 177)},
        "mortality": {"leukemia": (53, 53, 51, 51, 52, 54, 55, 52, 38),
                      "solid": (1717, 1051, 711, 491, 455, 415, 354, 265, 152)},
    },
    "male": {
        "incidence": {"leukemia": (237, 120, 96, 84, 84, 84, 82, 73, 48),
                      "solid": (2326, 1325, 881, 602, 564, 507, 407, 270, 126)},
        "mortality": {"leukemia": (71, 71, 67, 64, 67, 71, 73, 69, 51),
                      "solid": (1028, 641, 444, 317, 310, 289, 246, 181, 102)},
    },
}
TABLE_9_13_DOSE_GY = 0.1

# Table 9.14 (printed p. 303): per 100 000, by scenario.
EXPOSURE_SCENARIOS = {
    "single 0.1 Gy": {
        "radiation induced": {"cases": (900, 1370), "deaths": (480, 660)},
        "natural": {"cases": (46330, 37490), "deaths": (22810, 18030)},
    },
    "1 mGy per year for life": {
        "radiation induced": {"cases": (621, 1019), "deaths": (332, 497)},
    },
    "10 mGy per year, age 18-65": {
        "radiation induced": {"cases": (3059, 4295), "deaths": (1700, 2389)},
    },
}
DDREF = 1.5                     # §9.7.3: applied to solid cancers, not leukemia

# BEIR-VII ERR model for all solid cancer  [S&F Eq. (9.16)], incidence.
_ERR_BETA = {"male": 0.33, "female": 0.57}
_ERR_GAMMA = -0.30
_ERR_ETA = -1.4

# The trivial-dose floor below which `radiogenic_cancer_deaths` refuses.  Chosen
# as a tenth of the world-average natural background (~2.4 mSv/y), i.e. well
# inside the year-to-year variation nobody can detect.
TRIVIAL_DOSE_SV = 2.4e-4


def cancer_risk_at_age(sex, age_at_exposure, kind="mortality", endpoint="solid"):
    """Excess lifetime cancer risk per 100 000 for 0.1 Gy  [S&F Table 9.13].

    Linearly interpolated in age at exposure.  The dominant feature of the table
    is that risk falls ~4x from infancy to age 60 for solid cancer and barely
    moves for leukemia -- because solid cancers need decades of latency that an
    older person does not have, while leukemia appears within a few years."""
    try:
        row = LIFETIME_CANCER_RISK[sex][kind][endpoint]
    except KeyError:
        raise KeyError("no Table 9.13 row for (%r, %r, %r)" % (sex, kind, endpoint))
    if age_at_exposure < _AGES[0] or age_at_exposure > _AGES[-1]:
        raise ValueError("Table 9.13 covers ages %d-%d" % (_AGES[0], _AGES[-1]))
    for a0, a1, v0, v1 in zip(_AGES, _AGES[1:], row, row[1:]):
        if a0 <= age_at_exposure <= a1:
            return v0 + (v1 - v0) * (age_at_exposure - a0) / (a1 - a0)
    return row[-1]


def scaled_cancer_risk(sex, age_at_exposure, dose_gy, kind="mortality",
                       endpoint="solid"):
    """Table 9.13 scaled linearly to another dose -- the LNT step, made explicit.

    Returns a probability, not a rate per 100 000.  This is exactly what S&F
    Example 9.6 does, and the linearity being used is an assumption, not a
    measurement."""
    if dose_gy < 0:
        raise ValueError("dose cannot be negative")
    return (cancer_risk_at_age(sex, age_at_exposure, kind, endpoint) / 1e5
            * dose_gy / TABLE_9_13_DOSE_GY)


def cancer_risk_per_gy(scenario="single 0.1 Gy"):
    """Sex-averaged fatal-cancer risk per Gy from Table 9.14  [§9.7.3].

    For the 0.1 Gy scenario: 0.5(480 + 660)/(0.1 Gy x 1e5) = 0.057/Gy, which S&F
    round to 0.05/Gy = 5e-4 per rem and use as the general environmental risk
    factor."""
    d = EXPOSURE_SCENARIOS[scenario]["radiation induced"]["deaths"]
    if scenario != "single 0.1 Gy":
        raise ValueError("only the single-exposure scenario carries a dose that "
                         "a per-Gy risk can be divided by; the other two are "
                         "lifetime accumulations")
    return 0.5 * (d[0] + d[1]) / (TABLE_9_13_DOSE_GY * 1e5)


def radiogenic_cancer_deaths(people, individual_dose_sv, allow_trivial=False):
    """Expected excess fatal cancers = N x D x 0.057/Sv.

    REFUSES an individual dose below `TRIVIAL_DOSE_SV` unless `allow_trivial`.

    The refusal is the point.  Linearity makes the product N x D the only thing
    that matters, so the model happily reports deaths from a population dose
    assembled out of individual doses far below anything ever observed to do
    anything.  S&F note this property; ICRP-103 says computing deaths that way
    "is not reasonable and should be avoided".  The arithmetic is not wrong --
    it is the extrapolation underneath it that has no support, and a function
    that returns a confident number hides exactly that."""
    if people < 0 or individual_dose_sv < 0:
        raise ValueError("population and dose must be non-negative")
    if individual_dose_sv < TRIVIAL_DOSE_SV and not allow_trivial:
        raise ValueError(
            "individual dose %.3g Sv is below %.3g Sv, a tenth of natural "
            "background: the LNT model will still return a number, but no "
            "excess has been observed anywhere near this dose and ICRP-103 "
            "advises against computing deaths from it. Pass allow_trivial=True "
            "to proceed deliberately." % (individual_dose_sv, TRIVIAL_DOSE_SV))
    return people * individual_dose_sv * cancer_risk_per_gy()


def excess_relative_risk(dose_sv, sex, age_at_exposure, age_attained):
    """ERR for all solid cancer  [S&F Eq. (9.16), BEIR-VII incidence]:

        ERR = beta_s D exp(e* gamma) (a/60)^eta,

    with e* = (a_o - 30)/10 for a_o < 30 and 0 above.  beta = 0.33 (male),
    0.57 (female); gamma = -0.30, eta = -1.4.

    Both exponents are negative, so risk falls with age at exposure and with
    attained age -- the same two trends Table 9.13 shows, here in closed form."""
    if sex not in _ERR_BETA:
        raise KeyError("sex must be 'male' or 'female'")
    if dose_sv < 0 or age_at_exposure < 0 or age_attained <= 0:
        raise ValueError("dose and ages must be non-negative")
    e_star = (age_at_exposure - 30.0) / 10.0 if age_at_exposure < 30 else 0.0
    return (_ERR_BETA[sex] * dose_sv * math.exp(e_star * _ERR_GAMMA)
            * (age_attained / 60.0) ** _ERR_ETA)


def probability_of_causation(err):
    """PC = ERR/(1 + ERR)   [S&F Eq. (9.17)], also called assigned share.

    The probability that a cancer which HAS occurred was caused by a known prior
    exposure.  It is a compensation instrument, not a physical quantity: no test
    can attribute an individual tumour, so the law uses the ratio of excess to
    total risk in place of causation."""
    if err < 0:
        raise ValueError("excess relative risk cannot be negative")
    return err / (1.0 + err)


# --- radon  [S&F §9.8, Eqs. (9.18)-(9.21), Tables 9.15-9.16] -------------

# The 222Rn chain of Eq. (9.18): (nuclide, half-life in seconds, alpha MeV).
RN222_CHAIN = [("218Po", 3.05 * 60, 6.003), ("214Pb", 26.8 * 60, 0.0),
               ("214Bi", 19.9 * 60, 0.0), ("214Po", 164e-6, 7.687)]
PO218_ALPHA_MEV = 6.003
PO214_ALPHA_MEV = 7.687

WL_MEV_PER_LITRE = 1.3e5        # the definition of one working level
WLM_HOURS = 170.0               # a working-level month
WLM_BQ_H_PER_M3 = 629000.0      # S&F §9.9 footnote 4


def potential_alpha_energy_per_bq():
    """Potential alpha energy concentration (MeV m^-3) per Bq m^-3 of EEC
    [S&F Eqs. (9.19)-(9.20)].

    Each daughter is worth the alpha energy still to come from it and everything
    below it, weighted by its MEAN LIFE 1/lambda -- because it is the number of
    atoms present, not the decay rate, that carries stored energy:

        E = (E1+E4)/lam1 + E4(1/lam2 + 1/lam3 + 1/lam4).

    214Pb and 214Bi emit no alphas at all and yet contribute 90% of the total,
    because their half-lives are hundreds of times longer than 218Po's and they
    each carry 214Po's 7.687 MeV in escrow.  214Po's own term is negligible: it
    lives 164 microseconds."""
    lam = [math.log(2.0) / t for _, t, _ in RN222_CHAIN]
    e = (PO218_ALPHA_MEV + PO214_ALPHA_MEV) / lam[0]
    e += PO214_ALPHA_MEV * (1.0 / lam[1] + 1.0 / lam[2] + 1.0 / lam[3])
    return e


def equilibrium_equivalent_concentration(radon_bq_m3, equilibrium_factor):
    """EEC = F x C0   [S&F Eq. (9.21)].

    Plate-out and ventilation keep the daughters below secular equilibrium, so
    F < 1 (the EPA uses 0.5, a Canadian survey measured 0.52 +- 0.12).  The EEC
    is the equilibrium radon concentration that would carry the same potential
    alpha energy -- i.e. the same hazard -- as the actual mixture."""
    if radon_bq_m3 < 0:
        raise ValueError("concentration cannot be negative")
    if not 0 < equilibrium_factor <= 1:
        raise ValueError("the equilibrium factor lies in (0, 1]: values above 1 "
                         "would mean the daughters exceed secular equilibrium")
    return equilibrium_factor * radon_bq_m3


def annual_radon_exposure(eec_bq_m3, hours=8766.0):
    """Annual exposure in MBq h m^-3 on an EEC basis  [S&F §9.8.2]."""
    if eec_bq_m3 < 0:
        raise ValueError("EEC cannot be negative")
    return eec_bq_m3 * hours / 1e6


# Table 9.15 (printed p. 306): lifetime mortality per MBq h m^-3 annual exposure.
# population -> (life expectancy y, excess risk)
RADON_RISK_BY_POPULATION = {
    "male": (69.7, 0.055), "female": (76.4, 0.022), "mixed": (73.1, 0.039),
    "nonsmoking male": (70.5, 0.016), "nonsmoking female": (76.7, 0.0088),
    "smoking male": (69.0, 0.16), "smoking female": (75.9, 0.081),
}

# Table 9.16 (printed p. 307): lifetime risk per MBq h m^-3 annual exposure,
# by age at first exposure and duration.  NCRP [1984].
_RADON_DURATIONS = (1, 5, 10, 30, "life")
RADON_RISK_BY_AGE_DURATION = {
    1: (0.00010, 0.00054, 0.0012, 0.0054, 0.014),
    10: (0.00014, 0.00079, 0.0017, 0.0076, 0.014),
    20: (0.00021, 0.0011, 0.0024, 0.0087, 0.012),
    30: (0.00029, 0.0016, 0.0033, 0.0087, 0.012),
    40: (0.00033, 0.0016, 0.0032, 0.0067, 0.0072),
    50: (0.00027, 0.0013, 0.0022, 0.0040, 0.0043),
    60: (0.00021, 0.00074, 0.0014, 0.0021, 0.0021),
    70: (0.00011, 0.00045, 0.00060, 0.00060, 0.00060),
}


def radon_lung_cancer_risk(annual_exposure_mbq_h_m3, population="mixed"):
    """Lifetime probability of death from radon-induced lung cancer
    [S&F Table 9.15].

    The single most important number here is the smoking ratio: a smoker's
    radiogenic risk is TEN times a non-smoker's for the same radon exposure.
    Radon and tobacco are multiplicative, not additive, which means radon
    remediation buys a smoker ten times what it buys anyone else."""
    if annual_exposure_mbq_h_m3 < 0:
        raise ValueError("exposure cannot be negative")
    if population not in RADON_RISK_BY_POPULATION:
        raise KeyError("no Table 9.15 row for %r; have %s"
                       % (population, sorted(RADON_RISK_BY_POPULATION)))
    return annual_exposure_mbq_h_m3 * RADON_RISK_BY_POPULATION[population][1]


def wlm_to_bq_h_per_m3(wlm):
    """1 WLM = 629 000 Bq h m^-3 (EEC)  [S&F §9.9, footnote 4]."""
    if wlm < 0:
        raise ValueError("exposure cannot be negative")
    return wlm * WLM_BQ_H_PER_M3


def bq_h_per_m3_to_wlm(bq_h_per_m3):
    """The inverse."""
    if bq_h_per_m3 < 0:
        raise ValueError("exposure cannot be negative")
    return bq_h_per_m3 / WLM_BQ_H_PER_M3


# --- protection standards  [S&F §9.9, Table 9.17] ------------------------

FATAL_CANCER_RISK_PER_SV = 1.0e-2       # §9.9.2, NCRP [1987]
HEREDITARY_RISK_PER_SV = 0.4e-2         # first two generations

# Table 9.17 (printed p. 310), in mSv per year unless noted.
NCRP_1987_LIMITS = {
    "occupational stochastic": 50.0,
    "occupational lens of the eye": 150.0,
    "occupational other organs": 500.0,
    "occupational cumulative per year of age": 10.0,
    "public continuous": 1.0,
    "public infrequent": 5.0,
    "public remedial action level": 5.0,
    "public lens, skin, extremities": 50.0,
    "embryo-fetus total": 5.0,
    "embryo-fetus monthly": 0.5,
    "negligible individual risk level": 0.01,
}


def occupational_limit_sv(acceptable_annual_risk=50e-6, skew=10.0,
                          working_years=40.0,
                          risk_per_sv=FATAL_CANCER_RISK_PER_SV):
    """Re-derive the 50 mSv/y occupational limit  [S&F §9.9.1].

        limit = (skew x lifetime risk) / (years x risk per Sv)

    with an acceptable average annual occupational death rate of 50 per million,
    a 40-year career, and the observation that average doses in radiation work
    run about a tenth of the most-exposed individual's -- hence the factor 10.

    The limit is not a biological threshold.  It is a comparison with the fatal
    accident rate in industries already agreed to be safe, run backwards through
    an assumed linear risk coefficient."""
    lifetime = acceptable_annual_risk * working_years
    return skew * lifetime / (working_years * risk_per_sv)


def public_limit_sv(acceptable_lifetime_risk=4e-3, lifespan=70.0,
                    risk_per_sv=FATAL_CANCER_RISK_PER_SV):
    """The same argument for members of the public  [S&F §9.9.1].

    Gives 5.7 mSv/y; the adopted 1977 limit was 5 mSv/y, and the modern one is
    1 mSv/y (Table 9.17, "public continuous").  The gap between what the risk
    argument produces and what was adopted is not an error -- it is the margin
    that ALARA adds on top."""
    return acceptable_lifetime_risk / (lifespan * risk_per_sv)


def cumulative_dose_guidance_sv(age_years):
    """NCRP cumulative guidance: 10 mSv x age in years  [Table 9.17]."""
    if age_years < 0:
        raise ValueError("age cannot be negative")
    return 10e-3 * age_years


# --- dose-effect models  [S&F §9.10, Fig. 9.3] ---------------------------

def lnt(dose, alpha=1.0):
    """(a) linear, no threshold -- the regulatory model."""
    return alpha * dose


def linear_with_threshold(dose, alpha=1.0, threshold=0.1):
    """(b) linear above a threshold."""
    return alpha * max(0.0, dose - threshold)


def quadratic(dose, beta=1.0):
    """(c) quadratic, no threshold -- adopted for leukemia."""
    return beta * dose * dose


def linear_quadratic(dose, alpha=1.0, beta=1.0):
    """(d) linear-quadratic -- the shape the high-dose data actually suggest,
    and the reason a DDREF is needed at all."""
    return alpha * dose + beta * dose * dose


def hormetic(dose, alpha=1.0, zep=0.2, scale=None):
    """(e) hormetic: a beneficial dip crossing zero effect at the ZEP.

        f(D) = alpha D - b D exp(-D/s),   b = alpha exp(zep/s),  s = zep/2

    which vanishes at D = 0 and again at the zero-equivalent point, is negative
    (beneficial) between them, and is asymptotically the LNT line.

    Provided so the shape can be drawn and compared, NOT as a risk calculator.
    S&F §9.10 sets out the case for it -- Cohen's county-level radon study, the
    nuclear-worker cohorts, the high-background regions -- and the case is
    contested. No parameter here is fitted to anything."""
    if zep <= 0:
        raise ValueError("the zero-equivalent point must be positive")
    s = 0.5 * zep if scale is None else scale
    if s <= 0:
        raise ValueError("the scale must be positive")
    b = alpha * math.exp(zep / s)
    return alpha * dose - b * dose * math.exp(-dose / s)


# --- the printed values this module corrects (see refs.md) ---------------

EXAMPLE_9_7_DEATHS_ERRATA = 3116        # its own factors give 3416
EXAMPLE_9_7_RESPIRATORY_ERRATA = (71.9, 25.2)   # Table 9.12 gives 76.2, 42.2


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-18  radiation health effects\n")

    print("  deterministic: nothing happens below the threshold")
    for d in (0.2, 0.5, 1.0, 2.3, 4.0):
        eff = deterministic_effects_at(d)
        print("   %.1f Gy: %d endpoint(s) possible%s" %
              (d, len(eff), (" -- " + ", ".join("%s %s" % (o, e)
                                                for o, e, _, _ in eff[:3])) if eff else ""))

    print("\n  lethality without treatment  [Table 9.8]")
    for d in (1.5, 2.25, 3.25, 4.0, 5.0, 6.0):
        print("   mid-line %.2f Gy -> %.0f%% 60-day lethality"
              % (d, 100 * lethality_fraction(d)))

    print("\n  hereditary  [Eq. (9.13)]")
    print("   doubling dose = %.3f Gy, rounded to 1 Gy" % doubling_dose())
    lo = hereditary_risk(16500, 1.0, 0.3, 0.15)
    hi = hereditary_risk(16500, 1.0, 0.3, 0.30)
    print("   dominant + X-linked: %.0f to %.0f per Gy per million  (book 750-1500)"
          % (lo, hi))
    print("   chronic multifactorial baseline is 39x larger and yields %.0f-%.0f"
          % (hereditary_risk(650000, 1.0, 0.02, 0.02),
             hereditary_risk(650000, 1.0, 0.02, 0.09)))

    print("\n  cancer  [Tables 9.13, 9.14]")
    print("   sex-averaged fatal risk = %.4f per Gy = %.0e per rem"
          % (cancer_risk_per_gy(), cancer_risk_per_gy() / 100))
    print("   Example 9.6: 30-y male, 0.02 Gy")
    print("     leukemia   %.6f  = 1 in %.0f" %
          (scaled_cancer_risk("male", 30, 0.02, endpoint="leukemia"),
           1 / scaled_cancer_risk("male", 30, 0.02, endpoint="leukemia")))
    print("     all solid  %.6f  = 1 in %.0f" %
          (scaled_cancer_risk("male", 30, 0.02),
           1 / scaled_cancer_risk("male", 30, 0.02)))
    print("   age dependence of solid-cancer mortality risk (female):")
    for a in (0, 20, 40, 60, 80):
        print("     exposed at %2d -> %6.0f per 1e5 per 0.1 Gy"
              % (a, cancer_risk_at_age("female", a)))

    print("\n  radon  [Eqs. (9.19)-(9.21)]")
    e = potential_alpha_energy_per_bq()
    print("   potential alpha energy = %.0f MeV/m3 per Bq/m3 EEC = %.3e J/m3"
          % (e, e * 1.602e-13))
    print("   -> 1 WL (%.1e MeV/L) is %.0f Bq/m3 EEC; 1 WLM = %.0f Bq h/m3"
          % (WL_MEV_PER_LITRE, WL_MEV_PER_LITRE * 1e3 / e,
             WLM_HOURS * WL_MEV_PER_LITRE * 1e3 / e))
    print("   (S&F's footnote says 629 000, using the conventional 3700 Bq/m3)")
    eec = equilibrium_equivalent_concentration(46.0, 0.5)   # U.S. average
    exp_ = annual_radon_exposure(eec)
    print("   U.S. average 46 Bq/m3 at F = 0.5 -> EEC %.0f Bq/m3, %.4f MBq h/m3/y"
          % (eec, exp_))
    for pop in ("mixed", "nonsmoking male", "smoking male"):
        print("     %-16s lifetime risk %.4f" % (pop, radon_lung_cancer_risk(exp_, pop)))

    print("\n  standards  [§9.9.1, Table 9.17]")
    print("   occupational limit re-derived: %.0f mSv/y  (adopted 50)"
          % (1000 * occupational_limit_sv()))
    print("   public limit re-derived:       %.1f mSv/y  (adopted 5 in 1977, 1 today)"
          % (1000 * public_limit_sv()))
    print("   cumulative guidance at age 40: %.0f mSv" % (1000 * cumulative_dose_guidance_sv(40)))

    print("\n  the collective-dose trap")
    try:
        radiogenic_cancer_deaths(1e7, 1e-5)
    except ValueError as exc:
        print("   refused: %s" % str(exc)[:72] + "...")
    print("   10^7 people at 0.01 mSv and 1000 at 100 mSv are the same collective")
    print("   dose (%.0f person-Sv) and the same %.1f predicted deaths under LNT."
          % (1e7 * 1e-5, radiogenic_cancer_deaths(1e7, 1e-5, allow_trivial=True)))


if __name__ == "__main__":
    _demo()
