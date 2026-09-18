"""NE-17  Dosimetry: kerma, absorbed dose, equivalent and effective dose.

Nuclear Science & Engineering trunk, module NE-17 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 9.1-9.4 (printed pp. 270-288).  Pure stdlib; photon coefficients
come from ../../data_tables/C3_photon_coefficients_*.csv.

~NE-11 and ~NE-12 answered "how much radiation is there".  This module answers
"how much does it matter", and the honest answer is that it takes FOUR distinct
quantities to get there, each one a correction to the last:

    KERMA K      energy handed to charged particles per unit mass    [Eq. (9.2)]
    ABSORBED DOSE D   energy actually deposited per unit mass        [Eq. (9.1)]
    EQUIVALENT DOSE H = QF x D     same energy, weighted by how it   [Eq. (9.10)]
                                   is spread along a track
    EFFECTIVE DOSE E = sum_T w_T H_T   whole-body risk from a        [Eq. (9.12)]
                                       partial-body exposure

They are NOT interchangeable, and the differences are the physics:

  * K vs D.  Kerma counts kinetic energy released at a point; dose counts energy
    deposited there.  They agree only under CHARGED-PARTICLE EQUILIBRIUM, and
    even then kerma runs slightly high because bremsstrahlung carries energy out
    of the volume.  That is the whole of the mu_tr/mu_en distinction from ~NE-12:
    iron at 5 MeV has mu_tr/rho = 0.02112 and mu_en/rho = 0.01983, a 6.5% gap.

  * D vs H.  A gray of alpha particles is not a gray of gammas.  The quality
    factor spans a factor of TWENTY (Table 9.1), so a dose reported without its
    radiation type is not a statement about hazard at all.

  * H vs E.  Organs differ in radiosensitivity by a factor of 25 (Table 9.3), so
    a partial-body dose cannot be compared with a whole-body one until it is
    weighted.  The weights are a social judgement encoded as arithmetic, and they
    changed between ICRP 1977 and ICRP 1991 -- both tables are here.

Everything numerical rests on one conversion, worth memorising:

    D (Gy) = 1.602e-10 x E (MeV) x (mu_en/rho) (cm2/g) x Phi (cm-2)     [Eq. (9.6)]

which is nothing but "J per MeV, times g per kg".
"""

import bisect
import csv
import math
import os

__all__ = [
    "MEV_TO_J", "DOSE_PREFACTOR", "EXPOSURE_PREFACTOR", "W_AIR_EV",
    "ROENTGEN_C_PER_KG", "GY_PER_ROENTGEN", "GY_PER_RAD", "SV_PER_REM",
    "BQ_PER_CI", "AVOGADRO", "MATERIALS",
    "load_photon_coefficients", "mass_coefficient", "linear_coefficient",
    "point_source_fluence", "kerma", "absorbed_dose", "exposure",
    "roentgen_to_air_dose", "air_dose_to_roentgen",
    "photon_kerma_rate", "photon_dose_rate", "photon_dose_rate_from_lines",
    "neutron_recoil_fraction", "neutron_kerma", "water_neutron_kerma_coefficient",
    "QUALITY_FACTORS", "quality_factor", "dose_equivalent",
    "ICRP77_TISSUE_WEIGHTS", "ICRP90_TISSUE_WEIGHTS", "ICRP07_TISSUE_WEIGHTS",
    "effective_dose", "INGESTION_DOSE_COEFFICIENTS", "committed_effective_dose",
    "NATURAL_BACKGROUND_WORLD", "NATURAL_BACKGROUND_US", "US_MANMADE_BREAKDOWN",
    "rule_of_thumb_exposure_rate", "exposure_rate_exact",
    "rule_of_thumb_valid_range",
    "EXAMPLE_9_3_PRINTED_USV", "EXAMPLE_9_5_PRINTED_MREM",
    "PROBLEM_9_1_PRINTED_MEV", "PROBLEM_9_4A_PRINTED_MGY_PER_H",
]

# --- constants  [S&F §9.2.4, Eqs. (9.5), (9.6), (9.9)] -------------------

MEV_TO_J = 1.602e-13            # the book's rounding of 1.602176e-13
DOSE_PREFACTOR = 1.602e-10      # Gy per (MeV * cm2/g * cm-2)   [Eqs. (9.5), (9.6)]
EXPOSURE_PREFACTOR = 1.835e-8   # R  per (MeV * cm2/g * cm-2)   [Eq. (9.9)]
W_AIR_EV = 33.85                # eV per ion pair in air  [ICRU 1979; §9.2.5]
ROENTGEN_C_PER_KG = 2.58e-4     # the definition of the roentgen  [§9.2.5]
GY_PER_ROENTGEN = ROENTGEN_C_PER_KG * W_AIR_EV      # = 8.73 mGy; see below
GY_PER_RAD = 0.01               # 1 rad = 100 erg/g  [§9.2.2]
SV_PER_REM = 0.01               # [§9.2.7]
BQ_PER_CI = 3.7e10
AVOGADRO = 6.022e23

# Densities, as used throughout the trunk (~NE-11, ~NE-12).  Iron is 7.874, NOT
# the 7.784 printed in S&F Example 7.2 -- see modules/CHANGELOG.md.
MATERIALS = {
    "air": 1.205e-3, "water": 1.0, "concrete": 2.35, "iron": 7.874, "lead": 11.35,
}

# --- the printed values this module corrects (see refs.md) ---------------

EXAMPLE_9_3_PRINTED_USV = 10.5          # S&F Ex. 9.3; its own inputs give 0.105
EXAMPLE_9_5_PRINTED_MREM = 7.1          # S&F Ex. 9.5; the number is right, the unit is rem
PROBLEM_9_1_PRINTED_MEV = 5.37          # S&F Prob. 9.1 calls this MeV; it is keV
PROBLEM_9_4A_PRINTED_MGY_PER_H = 1.611  # solution manual; its own Prob. 5 implies 1.27

_PHOTON = {}


def _table_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, os.pardir, os.pardir, "data_tables"))


def load_photon_coefficients(material):
    """[(E_MeV, {component: cm2/g}), ...] from the extracted Appendix C.3.

    Components: 'c' incoherent, 'ph' photoelectric, 'pp' pair production,
    'total', 'tr' energy transfer, 'en' energy absorption.  Same table ~NE-12
    reads; loaded here directly rather than by importing a sibling module."""
    key = material.lower()
    if key in _PHOTON:
        return _PHOTON[key]
    if key not in MATERIALS:
        raise KeyError("no Appendix C.3 table for %r; have %s"
                       % (material, sorted(MATERIALS)))
    rows = []
    with open(os.path.join(_table_dir(), "C3_photon_coefficients_%s.csv" % key),
              newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((float(r["E_MeV"]), {
                "c": float(r["mu_c_cm2_g"]), "ph": float(r["mu_ph_cm2_g"]),
                "pp": float(r["mu_pp_cm2_g"]), "total": float(r["mu_cm2_g"]),
                "tr": float(r["mu_tr_cm2_g"]), "en": float(r["mu_en_cm2_g"]),
            }))
    rows.sort(key=lambda t: t[0])
    _PHOTON[key] = rows
    return rows


def mass_coefficient(material, e_mev, component="en", interpolation="loglog"):
    """mu/rho (cm2/g) at an arbitrary energy, from Appendix C.3.

    `interpolation` matters more than it looks.  ~NE-11 and ~NE-12 use LOG-LOG,
    which is right: the coefficients are close to power laws between grid points.
    S&F's own solutions say "linearly interpolating between tabulated values",
    and reproducing the book's numbers therefore requires `"linear"`.  The two
    agree to 0.03% on mu_en (a nearly flat curve) but differ by 0.6% on the total
    mu at 0.662 MeV, which becomes 2% in a flux after 40 cm of water.  Both are
    offered, and `test_linear_vs_loglog_interpolation` measures the gap."""
    rows = load_photon_coefficients(material)
    energies = [e for e, _ in rows]
    if e_mev < energies[0] or e_mev > energies[-1]:
        raise ValueError("%.4g MeV is outside the tabulated range %.4g-%.4g MeV"
                         % (e_mev, energies[0], energies[-1]))
    i = bisect.bisect_left(energies, e_mev)
    if i < len(energies) and energies[i] == e_mev:
        return rows[i][1][component]
    lo, hi = rows[i - 1], rows[i]
    if hi[0] == lo[0]:
        raise ValueError("%.6g MeV lands on the duplicated absorption-edge pair "
                         "at %.6g MeV" % (e_mev, lo[0]))
    y0, y1 = lo[1][component], hi[1][component]
    if interpolation == "linear" or y0 <= 0 or y1 <= 0:
        f = (e_mev - lo[0]) / (hi[0] - lo[0])
        return y0 + f * (y1 - y0)
    if interpolation != "loglog":
        raise ValueError("interpolation must be 'loglog' or 'linear'")
    f = math.log(e_mev / lo[0]) / math.log(hi[0] / lo[0])
    return math.exp(math.log(y0) + f * math.log(y1 / y0))


def linear_coefficient(material, e_mev, component="total", **kw):
    """mu (1/cm) = rho * (mu/rho)."""
    return MATERIALS[material.lower()] * mass_coefficient(material, e_mev,
                                                          component, **kw)


# --- the field  [S&F Eq. (7.25), used throughout Ch. 9] ------------------

def point_source_fluence(s_per_s, t_s, r_cm, mu_per_cm=0.0):
    """Uncollided fluence (cm-2) at r from an isotropic point source.

        Phi = S t exp(-mu r) / (4 pi r^2)

    Not new -- it is ~NE-11's Eq. (7.25) -- but every dose calculation in the
    chapter starts here, so it is repeated rather than imported."""
    if r_cm <= 0:
        raise ValueError("distance must be positive")
    if s_per_s < 0 or t_s < 0 or mu_per_cm < 0:
        raise ValueError("source strength, time and mu must be non-negative")
    return s_per_s * t_s * math.exp(-mu_per_cm * r_cm) / (4.0 * math.pi * r_cm ** 2)


# --- kerma and absorbed dose  [S&F Eqs. (9.5), (9.6)] --------------------

def kerma(e_mev, mu_tr_over_rho, fluence):
    """K (Gy) = 1.602e-10 E (mu_tr/rho) Phi   [S&F Eq. (9.5)].

    mu_tr excludes energy that leaves as scattered, annihilation or fluorescent
    photons, but INCLUDES energy the secondary electrons later radiate away as
    bremsstrahlung -- that energy was handed to a charged particle, which is all
    kerma asks."""
    if e_mev < 0 or mu_tr_over_rho < 0 or fluence < 0:
        raise ValueError("energy, coefficient and fluence must be non-negative")
    return DOSE_PREFACTOR * e_mev * mu_tr_over_rho * fluence


def absorbed_dose(e_mev, mu_en_over_rho, fluence):
    """D (Gy) = 1.602e-10 E (mu_en/rho) Phi   [S&F Eq. (9.6)].

    Valid under CHARGED-PARTICLE EQUILIBRIUM and with no local reabsorption of
    bremsstrahlung.  mu_en is mu_tr less the radiative losses, so D <= K always,
    with equality only where bremsstrahlung is negligible."""
    if e_mev < 0 or mu_en_over_rho < 0 or fluence < 0:
        raise ValueError("energy, coefficient and fluence must be non-negative")
    return DOSE_PREFACTOR * e_mev * mu_en_over_rho * fluence


def photon_kerma_rate(material, e_mev, flux_density, **kw):
    """Convenience: kerma rate (Gy/s) in `material` for a monoenergetic flux."""
    return kerma(e_mev, mass_coefficient(material, e_mev, "tr", **kw), flux_density)


def photon_dose_rate(material, e_mev, flux_density, **kw):
    """Convenience: absorbed dose rate (Gy/s) in `material`."""
    return absorbed_dose(e_mev, mass_coefficient(material, e_mev, "en", **kw),
                         flux_density)


def photon_dose_rate_from_lines(lines, activity_bq, r_cm, dose_material="air",
                                attenuator=None, interpolation="linear"):
    """Absorbed dose rate (Gy/h) at r from a point source with a discrete photon
    spectrum -- the S&F Ch. 9 Problems 4 and 5 calculation.

    `lines` is [(E_MeV, photons per decay), ...] (Appendix D).  `attenuator` is a
    material name whose mu attenuates the beam; None means no attenuation, which
    is the usual approximation for a short air path.

    Note the two materials are independent: the dose is scored in
    `dose_material` while the attenuation happens in `attenuator`.  Problem 5
    scores dose in AIR inside an IRON medium, which sounds odd until you recall
    that kerma is defined for a hypothetical receptor (§9.2.3)."""
    total = 0.0
    for e_mev, f in lines:
        mu_en = mass_coefficient(dose_material, e_mev, "en",
                                 interpolation=interpolation)
        atten = 1.0
        if attenuator is not None:
            mu = linear_coefficient(attenuator, e_mev, "total",
                                    interpolation=interpolation)
            atten = math.exp(-mu * r_cm)
        total += f * e_mev * mu_en * atten
    return DOSE_PREFACTOR * activity_bq / (4.0 * math.pi * r_cm ** 2) * 3600.0 * total


# --- exposure  [S&F §9.2.5, Eq. (9.9)] -----------------------------------

def exposure(e_mev, mu_en_over_rho_air, fluence):
    """X (roentgen) = 1.835e-8 E (mu_en/rho)_air Phi   [S&F Eq. (9.9)].

    Exposure is charge liberated per unit mass of AIR, so it is defined only for
    photons and only in air.  It survives as a unit because air and tissue happen
    to have similar photon interaction properties per gram."""
    if e_mev < 0 or mu_en_over_rho_air < 0 or fluence < 0:
        raise ValueError("energy, coefficient and fluence must be non-negative")
    return EXPOSURE_PREFACTOR * e_mev * mu_en_over_rho_air * fluence


def roentgen_to_air_dose(x_roentgen):
    """1 R of exposure = 8.73 mGy absorbed in air.

    S&F never write this conversion down, but it falls straight out of the two
    definitions: a roentgen is 2.58e-4 C/kg of liberated charge, and it costs
    W = 33.85 eV to make an ion pair, so

        D_air = (2.58e-4 C/kg) x (33.85 J/C) = 8.73e-3 Gy per R,

    which is exactly the ratio of the prefactors in Eqs. (9.6) and (9.9).  It is
    the number that lets a survey meter reading in mR/h be turned into a dose."""
    if x_roentgen < 0:
        raise ValueError("exposure cannot be negative")
    return GY_PER_ROENTGEN * x_roentgen


def air_dose_to_roentgen(d_gy):
    """The inverse of `roentgen_to_air_dose`."""
    if d_gy < 0:
        raise ValueError("dose cannot be negative")
    return d_gy / GY_PER_ROENTGEN


# --- neutron kerma  [S&F §9.2.4, Eqs. (9.7), (9.8)] ----------------------

def neutron_recoil_fraction(a):
    """Mean fraction of a neutron's energy given to a recoiling nucleus of mass
    number A, for isotropic elastic scattering in the CM frame:

        f_s = (1/2)(1 - alpha) = 2A/(A+1)^2     [S&F Eq. (9.7), from Eq. (6.28)]

    Maximum at A = 1 (hydrogen, f = 1/2) and falling as 2/A -- which is why
    hydrogenous material dominates fast-neutron dose in tissue, and why the same
    fact makes water a moderator in ~NE-13."""
    if a <= 0:
        raise ValueError("mass number must be positive")
    return 2.0 * a / (a + 1.0) ** 2


def neutron_kerma(e_mev, fs_mu_s_over_rho, fluence):
    """K (Gy) = 1.602e-10 E (f_s mu_s/rho) Phi   [S&F Eq. (9.8)].

    Elastic scattering only.  For slow and thermal neutrons this is wrong -- the
    kerma there is dominated by capture reactions such as 14N(n,p)14C and
    1H(n,gamma)2H, which S&F note but do not compute."""
    if e_mev < 0 or fs_mu_s_over_rho < 0 or fluence < 0:
        raise ValueError("energy, coefficient and fluence must be non-negative")
    return DOSE_PREFACTOR * e_mev * fs_mu_s_over_rho * fluence


def water_neutron_kerma_coefficient(sigma_s_h_b, sigma_s_o_b):
    """(f_s mu_s/rho) for water, cm2/g, from the H and O scattering cross
    sections in barns  [S&F Example 9.2]:

        (N_a/A_H2O) [2 sigma_H f_H + sigma_O f_O] .

    The factor 2 is the two hydrogens per molecule; A_H2O = 18.  Hydrogen carries
    97% of it at 0.1 MeV even though oxygen is 89% of the mass."""
    if sigma_s_h_b < 0 or sigma_s_o_b < 0:
        raise ValueError("cross sections must be non-negative")
    f_h = neutron_recoil_fraction(1)
    f_o = neutron_recoil_fraction(16)
    return (AVOGADRO / 1e24 / 18.0) * (2.0 * sigma_s_h_b * f_h
                                       + sigma_s_o_b * f_o)


# --- quality factor and dose equivalent  [S&F Table 9.1, Eq. (9.10)] -----

# S&F Table 9.1 (printed p. 279).  Neutron entries are (E_low, E_high, QF) in MeV.
QUALITY_FACTORS = {
    "photon": 1.0, "gamma": 1.0, "xray": 1.0, "beta": 1.0, "electron": 1.0,
    "proton": 5.0,          # ICRP 1991; NCRP says 2 -- see `quality_factor`
    "alpha": 20.0,
}
_NEUTRON_QF = [(0.0, 0.010, 5.0), (0.010, 0.100, 10.0), (0.100, 2.0, 20.0),
               (2.0, 20.0, 10.0), (20.0, float("inf"), 5.0)]


def quality_factor(radiation, e_mev=None, authority="ICRP"):
    """QF from S&F Table 9.1.

    REFUSES an unrecognised radiation rather than defaulting to 1.  That default
    is the single most expensive mistake available here: treating a fast-neutron
    field as QF = 1 understates the dose equivalent by a factor of twenty.

    Neutrons need an energy.  Protons are the one row where the two standards
    bodies disagree (ICRP 5, NCRP 2), so the choice is explicit."""
    key = str(radiation).lower()
    if key == "neutron":
        if e_mev is None:
            raise ValueError("the neutron quality factor spans 5 to 20 across "
                             "the table; an energy is required")
        if e_mev < 0:
            raise ValueError("energy must be non-negative")
        for lo, hi, qf in _NEUTRON_QF:
            if lo <= e_mev < hi:
                return qf
        return _NEUTRON_QF[-1][2]
    if key == "proton":
        if authority.upper() == "NCRP":
            return 2.0
        if authority.upper() != "ICRP":
            raise ValueError("authority must be 'ICRP' or 'NCRP'")
        return 5.0
    if key not in QUALITY_FACTORS:
        raise ValueError("no Table 9.1 entry for %r; known: %s. Refusing to "
                         "assume QF = 1 -- for neutrons or alphas that would "
                         "understate the hazard 5- to 20-fold"
                         % (radiation, sorted(set(QUALITY_FACTORS) | {"neutron"})))
    return QUALITY_FACTORS[key]


def dose_equivalent(d_gy, qf):
    """H (Sv) = QF x D (Gy)   [S&F Eq. (9.10)]."""
    if d_gy < 0 or qf <= 0:
        raise ValueError("dose must be non-negative and QF positive")
    return qf * d_gy


# --- effective dose  [S&F Tables 9.2, 9.3; Eqs. (9.11), (9.12)] ----------

# Table 9.2 -- ICRP [1977], for the effective dose EQUIVALENT.
ICRP77_TISSUE_WEIGHTS = {
    "gonads": 0.25, "breast": 0.15, "red marrow": 0.12, "lung": 0.12,
    "thyroid": 0.03, "bone surface": 0.03, "remainder": 0.30,
}

# Table 9.3 -- ICRP [1991], for the effective dose.
ICRP90_TISSUE_WEIGHTS = {
    "gonads": 0.20,
    "bone marrow": 0.12, "colon": 0.12, "lung": 0.12, "stomach": 0.12,
    "bladder": 0.05, "breast": 0.05, "liver": 0.05, "esophagus": 0.05,
    "thyroid": 0.05, "remainder": 0.05,
    "bone surface": 0.01, "skin": 0.01,
}

# Beyond S&F: ICRP Publication 103 (2007), the set actually in regulatory use.
# The book stops at 1991.  The direction of travel is the point -- the gonad
# weight fell 0.25 -> 0.20 -> 0.08 as the hereditary-risk estimate came down,
# while breast rose 0.05 -> 0.12.
ICRP07_TISSUE_WEIGHTS = {
    "bone marrow": 0.12, "colon": 0.12, "lung": 0.12, "stomach": 0.12,
    "breast": 0.12, "remainder": 0.12,
    "gonads": 0.08,
    "bladder": 0.04, "esophagus": 0.04, "liver": 0.04, "thyroid": 0.04,
    "bone surface": 0.01, "brain": 0.01, "salivary glands": 0.01, "skin": 0.01,
}


def effective_dose(organ_doses, weights=None):
    """E = sum_T w_T H_T   [S&F Eqs. (9.11), (9.12)].

    `organ_doses` maps organ name -> equivalent dose H_T (any consistent unit);
    the return is in that same unit.  `weights` defaults to ICRP [1991].

    REFUSES an organ that is not in the weighting set.  Silently dropping it
    would return a number that looks like an effective dose and is too low --
    the failure mode that matters, because it always errs toward saying an
    exposure was safe."""
    w = ICRP90_TISSUE_WEIGHTS if weights is None else weights
    unknown = sorted(set(organ_doses) - set(w))
    if unknown:
        raise ValueError("no tissue weighting factor for %s; known organs are "
                         "%s. Dropping them would understate the effective dose"
                         % (unknown, sorted(w)))
    return sum(w[t] * h for t, h in organ_doses.items())


# --- committed dose from ingestion  [S&F Table 9.4] ----------------------

# Table 9.4 (printed p. 286): specific committed effective dose equivalent for
# INGESTION, (f1, Sv/Bq, rem/Ci).  Cr-51 appears twice with two f1 values, so the
# key carries the solubility class.
INGESTION_DOSE_COEFFICIENTS = {
    "24Na": (1e+00, 3.9e-10, 1.4e+03), "32P": (8e-01, 2.1e-09, 7.7e+03),
    "40K": (1e+00, 5.1e-09, 1.9e+04),
    "51Cr(f1=0.1)": (1e-01, 3.6e-11, 1.3e+02),
    "51Cr(f1=0.01)": (1e-02, 4.0e-11, 1.5e+02),
    "54Mn": (1e-01, 7.3e-10, 2.7e+03), "56Mn": (1e-01, 2.6e-10, 9.5e+02),
    "55Fe": (1e-01, 1.6e-10, 5.8e+02), "59Fe": (1e-01, 1.8e-09, 6.6e+03),
    "58Co": (5e-02, 7.6e-10, 2.8e+03), "60Co": (5e-02, 2.7e-09, 1.0e+04),
    "63Ni": (5e-02, 1.4e-10, 5.4e+02), "65Ni": (5e-02, 1.6e-10, 6.1e+02),
    "64Cu": (5e-01, 1.2e-10, 4.3e+02), "65Zn": (5e-01, 3.9e-09, 1.4e+04),
    "69Zn": (5e-01, 2.3e-11, 8.5e+01), "83Br": (1e+00, 2.0e-11, 7.3e+01),
    "84Br": (1e+00, 4.1e-11, 1.5e+02), "88Rb": (1e+00, 4.4e-11, 1.6e+02),
    "89Rb": (1e+00, 2.2e-11, 8.0e+01), "89Sr": (3e-01, 2.2e-09, 8.2e+03),
    "90Sr": (3e-01, 3.5e-08, 1.3e+05), "90Y": (1e-04, 2.7e-09, 1.0e+04),
    "91mY": (1e-04, 1.0e-11, 3.9e+01), "91Y": (1e-04, 2.4e-09, 8.9e+03),
    "92Y": (1e-04, 5.0e-10, 1.9e+03), "93Y": (1e-04, 1.2e-09, 4.5e+03),
    "95Zr": (2e-03, 9.2e-10, 3.4e+03), "97Zr": (2e-03, 2.2e-09, 8.0e+03),
    "95Nb": (1e-02, 6.0e-10, 2.2e+03), "99Mo": (8e-01, 8.1e-10, 3.0e+03),
    "99mTc": (8e-01, 1.6e-11, 6.0e+01), "101Tc": (8e-01, 1.0e-11, 3.8e+01),
    "103Ru": (5e-02, 7.3e-10, 2.7e+03), "105Ru": (5e-02, 2.8e-10, 1.0e+03),
    "106Ru": (5e-02, 5.8e-09, 2.1e+04), "110mAg": (5e-02, 2.9e-09, 1.1e+04),
    "125mTe": (2e-01, 9.2e-10, 3.4e+03), "127mTe": (2e-01, 2.1e-09, 7.9e+03),
    "127Te": (2e-01, 1.9e-10, 6.9e+02), "129mTe": (2e-01, 2.7e-09, 9.9e+03),
    "129Te": (2e-01, 5.2e-11, 1.9e+02), "131mTe": (2e-01, 2.2e-09, 8.3e+03),
    "131Te": (2e-01, 2.3e-10, 8.5e+02), "132Te": (2e-01, 2.0e-09, 7.4e+03),
    "125I": (1e+00, 1.0e-08, 3.8e+04), "130I": (1e+00, 1.2e-09, 4.3e+03),
    "131I": (1e+00, 1.4e-08, 5.3e+04), "133I": (1e+00, 2.7e-09, 1.0e+04),
    "134I": (1e+00, 5.2e-11, 1.9e+02), "135I": (1e+00, 5.4e-10, 2.0e+03),
    "134Cs": (1e+00, 2.0e-08, 7.4e+04), "136Cs": (1e+00, 3.1e-09, 1.1e+04),
    "137Cs": (1e+00, 1.4e-08, 5.0e+04), "138Cs": (1e+00, 4.2e-11, 1.6e+02),
    "139Ba": (1e-01, 1.1e-10, 3.9e+02), "140Ba": (1e-01, 2.3e-09, 8.4e+03),
    "141Ba": (1e-01, 5.5e-11, 2.0e+02), "140La": (1e-03, 2.1e-09, 7.7e+03),
    "142La": (1e-03, 1.7e-10, 6.3e+02), "141Ce": (3e-04, 7.0e-10, 2.6e+03),
    "143Ce": (3e-04, 1.1e-09, 4.2e+03), "144Ce": (3e-04, 5.3e-09, 2.0e+04),
    "143Pr": (3e-04, 1.2e-09, 4.5e+03), "144Pr": (3e-04, 3.0e-11, 1.1e+02),
    "147Nd": (3e-04, 1.1e-09, 3.9e+03), "187W": (3e-01, 5.1e-10, 1.9e+03),
    "239Np": (1e-02, 8.0e-10, 2.9e+03),
}


def committed_effective_dose(intakes_bq):
    """Committed effective dose equivalent (Sv) from a single ingestion.

    `intakes_bq` maps nuclide -> activity ingested (Bq).  Doses from different
    nuclides simply add  [S&F Example 9.5].

    "Committed" means the whole 50-year integral of what that one swallow will
    ever deliver -- so the number is a debt incurred at the moment of intake, not
    a rate.  For 226Ra the delivery genuinely runs for decades; the ICRP's 50-year
    cutoff (§9.3.1) is a convention, not a physical horizon."""
    total = 0.0
    for nuclide, activity in intakes_bq.items():
        if nuclide not in INGESTION_DOSE_COEFFICIENTS:
            raise KeyError("no Table 9.4 ingestion coefficient for %r" % nuclide)
        if activity < 0:
            raise ValueError("activity cannot be negative")
        total += activity * INGESTION_DOSE_COEFFICIENTS[nuclide][1]
    return total


# --- natural background  [S&F Tables 9.5, 9.6] ---------------------------

# Table 9.5 (printed p. 287): annual global-average effective dose, mSv.
NATURAL_BACKGROUND_WORLD = {
    "cosmic high-LET": 0.1, "cosmic low-LET": 0.3,
    "terrestrial gamma": 0.5,
    "ingestion high-LET": 0.1, "ingestion low-LET": 0.2,
    "inhalation": 1.2,
}
# Table 9.6 (printed p. 288): U.S. annual effective dose equivalent, mSv.
NATURAL_BACKGROUND_US = {
    "cosmic": 0.27, "cosmogenic": 0.01, "external terrestrial": 0.28,
    "inhaled": 2.00, "in body": 0.39,
}
# §9.4 (printed p. 288): the U.S. man-made component, 0.65 mSv/y, by share.
US_MANMADE_BREAKDOWN = {
    "medical x rays": 0.58, "nuclear medicine": 0.21, "consumer products": 0.16,
    "fuel cycle": 0.01, "occupational": 0.02, "weapons fallout": 0.02,
}
US_MANMADE_MSV = 0.65


# --- the point-source rule of thumb  [S&F Ch. 9, Prob. 6] ----------------

def rule_of_thumb_exposure_rate(activity_ci, e_mev, photons_per_decay, r_ft):
    """Xdot (R/h) = 6 C E N / r^2, with C in Ci and r in FEET  [S&F Prob. 9.6].

    A field rule, not a derivation.  It works because (mu_en/rho)_air is nearly
    constant across the useful gamma range -- see `rule_of_thumb_valid_range`."""
    if r_ft <= 0:
        raise ValueError("distance must be positive")
    return 6.0 * activity_ci * e_mev * photons_per_decay / r_ft ** 2


def exposure_rate_exact(activity_ci, e_mev, photons_per_decay, r_ft,
                        interpolation="linear"):
    """The same quantity from Eq. (9.9), for comparison."""
    if r_ft <= 0:
        raise ValueError("distance must be positive")
    r_cm = 30.48 * r_ft
    phi = point_source_fluence(activity_ci * BQ_PER_CI * photons_per_decay,
                               3600.0, r_cm)
    return exposure(e_mev, mass_coefficient("air", e_mev, "en",
                                            interpolation=interpolation), phi)


def rule_of_thumb_valid_range(tolerance=0.20, e_lo=0.03, e_hi=10.0, n=4000):
    """Energies over which the 6CEN/r^2 rule is within `tolerance`  [Prob. 9.6b].

    Returns (E_min, E_max) of the widest CONTIGUOUS band containing 1 MeV.  The
    band is not the whole story and the caller should know it: air's mu_en/rho
    has a local minimum near 0.1 MeV, so the rule can fail marginally there and
    recover on both sides."""
    if not 0 < tolerance < 1:
        raise ValueError("tolerance must lie in (0, 1)")
    step = (math.log(e_hi) - math.log(e_lo)) / (n - 1)
    grid = [math.exp(math.log(e_lo) + i * step) for i in range(n)]
    ok = []
    for e in grid:
        approx = rule_of_thumb_exposure_rate(1.0, e, 1.0, 1.0)
        exact = exposure_rate_exact(1.0, e, 1.0, 1.0)
        ok.append(abs(approx / exact - 1.0) <= tolerance)
    i = min(range(n), key=lambda k: abs(grid[k] - 1.0))
    if not ok[i]:
        raise ValueError("the rule is not within %.0f%% even at 1 MeV"
                         % (100 * tolerance))
    lo = i
    while lo > 0 and ok[lo - 1]:
        lo -= 1
    hi = i
    while hi < n - 1 and ok[hi + 1]:
        hi += 1
    return grid[lo], grid[hi]


# --- demo ----------------------------------------------------------------

def _demo():
    print("NE-17  dosimetry\n")

    print("  Example 9.1: 1e8 5-MeV photons/s, 1 m away in water, scored in iron")
    phi = point_source_fluence(1e8, 1.0, 100.0,
                               linear_coefficient("water", 5.0, "total"))
    k = photon_kerma_rate("iron", 5.0, phi)
    d = photon_dose_rate("iron", 5.0, phi)
    print("   flux %.2f /cm2/s   K = %.3e Gy/s = %.2f uGy/h   (book 38.41, 2.34)"
          % (phi, k, k * 3.6e9))
    print("   D = %.3e Gy/s = %.2f uGy/h   (book 2.20)" % (d, d * 3.6e9))
    print("   K exceeds D by %.1f%% -- bremsstrahlung leaving the volume" % (100 * (k / d - 1)))

    print("\n  Example 9.2: 0.1-MeV neutrons, 1e10 /cm2/s, in water")
    c = water_neutron_kerma_coefficient(12.8, 3.5)
    print("   f_H = %.3f, f_O = %.4f, (f mu/rho) = %.4f cm2/g  (book 0.4412)"
          % (neutron_recoil_fraction(1), neutron_recoil_fraction(16), c))
    kn = neutron_kerma(0.1, c, 1e10)
    print("   K = %.4f Gy/s = %.0f Gy/h  (book 0.071, 254)" % (kn, kn * 3600))
    print("   hydrogen is 11%% of the mass and carries %.0f%% of the kerma"
          % (100 * 2 * 12.8 * 0.5 / (2 * 12.8 * 0.5 + 3.5 * neutron_recoil_fraction(16))))

    print("\n  the four quantities, for 1 MeV photons at Phi = 1e10 /cm2 in tissue")
    phi = 1e10
    d = absorbed_dose(1.0, mass_coefficient("water", 1.0, "en"), phi)
    print("   kerma          %.4f Gy" % kerma(1.0, mass_coefficient("water", 1.0, "tr"), phi))
    print("   absorbed dose  %.4f Gy" % d)
    print("   equivalent     %.4f Sv  (QF = 1)" % dose_equivalent(d, quality_factor("gamma")))
    print("   ... the same energy as alphas would be %.2f Sv"
          % dose_equivalent(d, quality_factor("alpha")))

    print("\n  exposure and the conversion S&F never writes down")
    x = exposure(1.0, mass_coefficient("air", 1.0, "en"), phi)
    print("   X = %.2f R   ->  air dose %.4f Gy" % (x, roentgen_to_air_dose(x)))
    print("   1 R = %.5f Gy in air = %.2f mGy" % (GY_PER_ROENTGEN, 1000 * GY_PER_ROENTGEN))

    print("\n  Example 9.4: effective dose equivalent from natural internal emitters")
    organs = {"lung": 0.36, "bone surface": 1.10, "red marrow": 0.50,
              "gonads": 0.36, "breast": 0.36, "thyroid": 0.36, "remainder": 0.36}
    he = effective_dose(organs, ICRP77_TISSUE_WEIGHTS)
    print("   HE = %.3f mSv/y  (book 39.90 mrem/y = %.3f mSv/y)" % (he, 0.399))

    print("\n  Example 9.5: ingesting 1 mCi 59Fe and 50 uCi 60Co")
    h = committed_effective_dose({"59Fe": 1e-3 * BQ_PER_CI,
                                  "60Co": 50e-6 * BQ_PER_CI})
    print("   committed effective dose = %.3f Sv = %.1f rem" % (h, h / SV_PER_REM))
    print("   the book prints 7.1 MREM; the number is right, the unit is rem")
    print("   for scale, natural background is %.1f mSv/y"
          % sum(NATURAL_BACKGROUND_WORLD.values()))

    print("\n  the 6CEN/r^2 rule of thumb  [Prob. 9.6]")
    lo, hi = rule_of_thumb_valid_range(0.20)
    print("   within 20%% over %.3f - %.2f MeV" % (lo, hi))
    lo5, hi5 = rule_of_thumb_valid_range(0.05)
    print("   within  5%% over %.3f - %.2f MeV" % (lo5, hi5))
    print("   energy   rule (R/h)   exact (R/h)   ratio")
    for e in (0.1, 0.3, 0.662, 1.0, 2.0, 5.0):
        a = rule_of_thumb_exposure_rate(1.0, e, 1.0, 3.0)
        x = exposure_rate_exact(1.0, e, 1.0, 3.0)
        print("   %6.3f %11.4f %13.4f %8.3f" % (e, a, x, a / x))


if __name__ == "__main__":
    _demo()
