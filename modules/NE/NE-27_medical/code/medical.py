"""NE-27  Medical applications: projection imaging, CT, SPECT, PET, therapy.

Nuclear Science & Engineering trunk, module NE-27 (modules/NE/list_NE.txt), and
the last of the trunk.  Follows Shultis & Faw, *Fundamentals of Nuclear Science
and Engineering*, 3rd ed., Chapter 14 (printed pp. 511-554).  Pure stdlib.

Medicine is where the whole trunk arrives.  Every earlier chapter reappears here
as a design constraint, and the applications divide cleanly by what they are
trying to do with the dose:

    DIAGNOSIS wants the SMALLEST dose that still forms an image.  X-ray
      projection, mammography, CT, SPECT, PET, densitometry.
    THERAPY wants the LARGEST dose the tumour can be given and the surrounding
      tissue cannot.  Teletherapy, CRT, IMRT, electron and proton beams,
      stereotactic, brachytherapy, radionuclide therapy.

Those are opposite optimisations of the same quantity, and almost every
technique in the chapter is an attempt to sharpen one of them spatially.

Three threads run through it, each inherited from earlier modules:

  * ~NE-12's photoelectric Z^4/E^3.  It is why contrast exists at all (bone
    against tissue), why mammography needs a molybdenum anode at 17.5 keV
    rather than tungsten at 59, and why iodine and barium are contrast agents.
  * ~NE-26's production routes.  Positron emitters are proton-rich, so PET
    isotopes come from cyclotrons -- and three of the four in Table 14.3 have
    half-lives under 21 minutes, which means the cyclotron must be in the
    building.
  * ~NE-14's Bragg peak.  It is the entire argument for proton therapy: a
    charged particle deposits most of its energy at the end of its range, so
    the dose can be stopped behind the tumour instead of continuing through
    the patient.
"""

import math

__all__ = [
    "HC_KEV_ANGSTROM", "M_E_C2_KEV", "ANODE_LINES", "PET_NUCLIDES", "CT_NOBEL",
    "SPECT_TRACERS", "THERAPY_MODALITIES", "CANCER_LIFETIME_RISK",
    "xray_energy", "xray_wavelength", "moseley_k_alpha",
    "hounsfield_unit", "mu_from_hounsfield", "contrast_ratio",
    "positron_range_mm", "beta_mean_fraction", "coincidence_window_length",
    "activity_after_transport", "usable_transport_time", "CANCER_2004",
    "pinhole_resolution", "spect_system_resolution", "CANCER_2004_TOTALS",
    "annihilation_photon_energy", "therapeutic_ratio", "brachytherapy_dose_rate",
]

HC_KEV_ANGSTROM = 12.39842      # h c in keV.Angstrom
M_E_C2_KEV = 510.999            # the annihilation photon energy

# --- Table 14.2 (printed p. 515): anode and filter characteristic lines -----
# element -> {line: (wavelength Angstrom, energy keV, excitation kV)}
ANODE_LINES = {
    "W": {"Ka1": (0.2090, 59.3182, 69.525), "Kb1": (0.1844, 67.2443, 69.525),
          "La1": (1.4764, 8.3976, 10.207), "Lb1": (1.2818, 9.6724, 11.514)},
    "Mo": {"Ka1": (0.7093, 17.4793, 20.000), "Kb1": (0.6323, 19.6083, 20.000),
           "La1": (5.4066, 2.2932, 2.520)},
    "Rh": {"Ka1": (0.6134, 20.2158, 23.230), "Kb1": (0.5456, 22.7236, 23.230),
           "La1": (4.5971, 2.6973, 3.014)},
}
ATOMIC_NUMBER = {"W": 74, "Mo": 42, "Rh": 45}

# --- Table 14.3 (printed p. 530): the PET radionuclides ---------------------
# nuclide -> (Emax MeV, Eav MeV, branch, half-life minutes, production reaction)
PET_NUCLIDES = {
    "11C": (0.960, 0.386, 0.998, 20.5, "14N(p,a)"),
    "13N": (1.199, 0.492, 0.998, 9.97, "16O(p,a), 13C(p,n)"),
    "15O": (1.732, 0.735, 0.999, 122.0 / 60.0, "15N(p,n)"),
    "18F": (0.634, 0.250, 1.000, 110.0, "18O(p,n)"),
}

# --- SPECT tracers  [S&F §14.1.7, printed p. 527, names them] --------------
# S&F's Table 14.5 (printed p. 539) lists PROCESS -> TRACER and gives no
# energies or half-lives at all; §14.1.7 names 99mTc, 125I and 131I as the
# frequently used ones.  The numbers below are therefore NOT from Chapter 14 --
# they are the principal imaging gamma and the half-life from the repo's shared
# nuclear data (modules/NE/data_tables/D1_decay_radiation.csv and
# A4_isotopic_abundances.csv, extracted from S&F Appendix D).  test_medical.py
# re-reads that CSV rather than trusting this dict.
SPECT_TRACERS = {
    "99mTc": {"half_life_h": 6.015, "gamma_kev": 140.5, "intensity_pct": 89.06,
              "uses": ["bone", "cardiac perfusion", "renal", "thyroid"]},
    "123I": {"half_life_h": 13.2235, "gamma_kev": 159.0, "intensity_pct": 83.3,
             "uses": ["thyroid"]},
    "201Tl": {"half_life_h": 72.912, "gamma_kev": 70.8, "intensity_pct": 46.18,
              "uses": ["myocardial perfusion"]},
    "67Ga": {"half_life_h": 78.27, "gamma_kev": 93.3, "intensity_pct": 37.0,
             "uses": ["inflammation", "lymphoma"]},
    "111In": {"half_life_h": 67.31, "gamma_kev": 171.3, "intensity_pct": 90.24,
              "uses": ["leukocyte labelling"]},
}

# --- §14.5: the therapy modalities, ordered by how they sharpen the dose ----
THERAPY_MODALITIES = {
    "60Co teletherapy": {"era": "1950s", "sharpening": "none beyond geometry",
                         "note": "1.25 MeV gammas; the workhorse before linacs"},
    "linac teletherapy": {"era": "1960s+", "sharpening": "higher energy, sharper penumbra",
                          "note": "4-25 MV bremsstrahlung"},
    "3D conformal (CRT)": {"era": "1990s", "sharpening": "beam shaping in 3D",
                           "note": "multileaf collimators match the beam to the target outline"},
    "IMRT": {"era": "2000s", "sharpening": "intensity varied within each beam",
             "note": "concave dose distributions become possible"},
    "electron beam": {"era": "1960s+", "sharpening": "finite range",
                      "note": "sharp distal falloff; superficial targets"},
    "proton beam": {"era": "1990s+", "sharpening": "the Bragg peak",
                    "note": "~NE-14: the dose stops behind the tumour"},
    "stereotactic": {"era": "1970s+", "sharpening": "many beams, one focus",
                     "note": "Gamma Knife: ~200 60Co sources aimed at one point"},
    "brachytherapy": {"era": "1900s+", "sharpening": "1/r^2 from inside",
                      "note": "the source is placed in or beside the tumour"},
    "radionuclide therapy": {"era": "1940s+", "sharpening": "biochemical",
                             "note": "131I to thyroid; targeting is metabolic, not geometric"},
}

# --- §14.1.5 (printed p. 521): an erratum, pinned so it is not re-absorbed --
# S&F: "Hounsfield and Cormack, working independently, who shared the Nobel
# prize in 1972."  The prize was 1979 (Physiology or Medicine, "for the
# development of computer assisted tomography").  1972 is a real date in the
# story -- Hounsfield's first published CT images, and EMI's announcement of the
# first clinical scanner -- so the book has collapsed the demonstration into the
# prize.  Verified against nobelprize.org, 2026-08-01.
CT_NOBEL = {"printed_year": 1972, "actual_year": 1979,
            "laureates": ("Allan M. Cormack", "Godfrey N. Hounsfield"),
            "what_1972_was": "first published CT images / first clinical scanner"}

# --- Table 14.6 (printed p. 541): estimated U.S. 2004 cancer cases/deaths ---
# site -> (new cases M, new cases F, deaths M, deaths F).  All four columns sum
# EXACTLY to the printed totals -- see test_medical.py.
CANCER_2004 = {
    "digestive": (135410, 120230, 73240, 61600),
    "respiratory": (102730, 83820, 95460, 69670),
    "breast": (1450, 215990, 470, 40110),
    "genital": (240660, 82550, 30530, 28720),
    "urinary": (68290, 30110, 17060, 8820),
    "lymphoma": (33180, 29070, 11090, 9640),
    "leukemia": (19020, 14420, 12990, 10310),
    "other": (98820, 92280, 50050, 43940),
}
CANCER_2004_TOTALS = (699560, 668470, 290890, 272810)   # as printed

# --- Table 14.7 (printed p. 541): U.S. lifetime cancer risk -----------------
# site -> (incidence M, incidence F, mortality M, mortality F) per 100,000.
# The table prints no total row; the totals below are summed here.
CANCER_LIFETIME_RISK = {
    "solid cancer": (45500, 36900, 22100, 17500),
    "thyroid": (230, 550, 40, 60),
    "leukemia": (830, 590, 710, 530),
}


# --- x-ray production  [S&F §14.1.1, Table 14.2] ---------------------------

def xray_energy(wavelength_angstrom):
    """E = hc/lambda, keV from Angstroms.

    Every wavelength/energy pair in Table 14.2 reproduces from this to 0.02% --
    which is the check that the table is a table of the same photons twice, not
    two independent measurements."""
    if wavelength_angstrom <= 0:
        raise ValueError("wavelength must be positive")
    return HC_KEV_ANGSTROM / wavelength_angstrom


def xray_wavelength(energy_kev):
    """The inverse of `xray_energy`."""
    if energy_kev <= 0:
        raise ValueError("energy must be positive")
    return HC_KEV_ANGSTROM / energy_kev


def moseley_k_alpha(z, constant=10.2e-3):
    """Moseley's law: E(K-alpha) ~ 10.2 eV (Z-1)^2, in keV.

    A one-line estimate of Table 14.2's K lines, good to 2% for Mo and Rh and
    8% for W -- the screening approximation degrades at high Z.  It is the reason
    anode choice IS energy choice: you cannot tune a characteristic line, you can
    only change the element."""
    if z < 2:
        raise ValueError("Moseley's law needs Z >= 2")
    return constant * (z - 1) ** 2


# --- CT  [S&F §14.1.5] -----------------------------------------------------

def hounsfield_unit(mu, mu_water=0.206):
    """HU = 1000 (mu - mu_water)/mu_water.

    Water is 0 by definition and air is -1000, which fixes the scale at both
    ends.  The useful consequence is that a CT number is a *calibrated*
    attenuation coefficient -- ~NE-11's mu, made comparable between machines."""
    if mu < 0 or mu_water <= 0:
        raise ValueError("attenuation coefficients must be non-negative")
    return 1000.0 * (mu - mu_water) / mu_water


def mu_from_hounsfield(hu, mu_water=0.206):
    """The inverse.  REFUSES below -1000 HU, which would be a negative
    attenuation coefficient -- less attenuating than a vacuum."""
    if hu < -1000.0:
        raise ValueError("HU = %g is below air (-1000) and implies a negative "
                         "attenuation coefficient" % hu)
    return mu_water * (1.0 + hu / 1000.0)


def contrast_ratio(mu_a, mu_b, thickness):
    """Fractional difference in transmitted intensity between two tissues:
    1 - exp[-(mu_a - mu_b) t].

    This is why ~NE-12's photoelectric Z^4/E^3 matters clinically: at 20 keV the
    photoelectric effect dominates and bone stands out enormously against tissue;
    by 100 keV Compton scattering dominates, mu depends only on electron density,
    and the contrast largely disappears."""
    if thickness < 0:
        raise ValueError("thickness cannot be negative")
    return 1.0 - math.exp(-abs(mu_a - mu_b) * thickness)


# --- PET and SPECT  [S&F §§14.1.7-14.1.8, Table 14.3] ----------------------

def annihilation_photon_energy():
    """511 keV, and there are two of them, back to back.

    The back-to-back geometry is what makes PET different: a coincidence between
    two detectors defines a LINE through the patient without any physical
    collimator.  S&F call it electronic collimation, and it is the reason PET
    beats SPECT on both resolution and sensitivity -- a SPECT collimator throws
    away almost every photon it accepts a direction from."""
    return M_E_C2_KEV


def beta_mean_fraction(nuclide):
    """Eav/Emax for a positron emitter.

    All four of Table 14.3's nuclides sit at 0.39-0.42, against the ~0.33 typical
    of beta-MINUS emitters.  The difference is Coulomb: the nucleus repels the
    emitted positron and attracts an electron, pushing the beta-plus spectrum to
    higher energies.  Four independent entries agreeing on 0.40 is a check that
    the table is real data and not assembled from rules of thumb."""
    if nuclide not in PET_NUCLIDES:
        raise KeyError("no Table 14.3 entry for %r; have %s"
                       % (nuclide, sorted(PET_NUCLIDES)))
    emax, eav = PET_NUCLIDES[nuclide][0], PET_NUCLIDES[nuclide][1]
    return eav / emax


def pinhole_resolution(d, f, b):
    """SPECT pinhole point-spread REFERRED TO THE OBJECT PLANE, S&F §14.1.7
    (printed p. 528): R_ph = (d/f)(f + b), for aperture diameter d, image
    distance f and object distance b.

    S&F's Fig. 14.16 caption gives the same quantity as "R_ph/(f + b) = d/b or
    R_ph = (d/b)/(f + b)".  Two things are going on there.  The written division
    is a typo -- (d/b)/(f+b) has dimensions of 1/length -- and the intended
    product d(f+b)/b is the spot size in the IMAGE plane, larger than this one by
    the magnification M = f/b.  Eq. (14.19) only closes with the object-referred
    form used here, because its other term R_I/M is object-referred too."""
    if min(d, f, b) <= 0:
        raise ValueError("aperture and both distances must be positive")
    return (d / f) * (f + b)


def spect_system_resolution(r_pinhole, r_intrinsic, magnification):
    """S&F Eq. (14.19): R_sys = sqrt(R_ph^2 + (R_I/M)^2).

    Two blurs added in quadrature -- the collimator's geometry and the crystal's
    position logic (R_I = 2.5-4.5 mm, §14.1.7).  The quadrature means the LARGER
    one dominates: there is no point improving the crystal below the collimator's
    contribution, which is why SPECT resolution is a collimator problem."""
    if magnification <= 0:
        raise ValueError("magnification must be positive")
    if r_pinhole < 0 or r_intrinsic < 0:
        raise ValueError("resolutions cannot be negative")
    return math.sqrt(r_pinhole ** 2 + (r_intrinsic / magnification) ** 2)


def positron_range_mm(mean_energy_mev):
    """Approximate mean positron range in tissue, mm, scaled from S&F's own
    statement that a 1 MeV positron travels about 4 mm.

    This is a HARD resolution floor for PET, and it is why 18F (0.25 MeV mean,
    under 1 mm) is the clinical workhorse while 15O (0.735 MeV) blurs more.  No
    detector improvement can recover it: the positron has already moved before it
    annihilates."""
    if mean_energy_mev < 0:
        raise ValueError("energy cannot be negative")
    return 4.0 * mean_energy_mev ** 1.5


def coincidence_window_length(window_ns):
    """The length along a line of response that a timing window corresponds to,
    cm: c * dt / 2.

    S&F give a 10-25 ns window; at 10 ns that is 150 cm, far larger than a
    patient -- so a conventional PET scanner localises along the line only by
    reconstruction, not by timing.  (Modern time-of-flight PET reaches ~400 ps,
    i.e. 6 cm, which does help and is beyond the book.)"""
    if window_ns <= 0:
        raise ValueError("the timing window must be positive")
    return 2.998e10 * window_ns * 1e-9 / 2.0


def activity_after_transport(nuclide, hours):
    """Fraction of a PET tracer's activity surviving transport."""
    if nuclide not in PET_NUCLIDES:
        raise KeyError("no Table 14.3 entry for %r" % nuclide)
    if hours < 0:
        raise ValueError("time cannot be negative")
    t_half = PET_NUCLIDES[nuclide][3]
    return 2.0 ** (-hours * 60.0 / t_half)


def usable_transport_time(nuclide, min_fraction=0.1):
    """Hours before a tracer falls below a usable fraction of its activity.

    S&F: "only 18F [has] a sufficiently long life to permit transport of
    radiopharmaceuticals to sites a few hours from the point of preparation."
    The other three are under 21 minutes, so the cyclotron must be in the
    building -- which is why a PET centre is a far larger commitment than a
    SPECT one."""
    if not 0 < min_fraction < 1:
        raise ValueError("the usable fraction must lie in (0, 1)")
    t_half = PET_NUCLIDES[nuclide][3]
    return -math.log2(min_fraction) * t_half / 60.0


# --- therapy  [S&F §14.5] --------------------------------------------------

def therapeutic_ratio(tumour_dose, normal_tissue_dose):
    """The ratio therapy exists to maximise.

    REFUSES a ratio at or below 1: if healthy tissue receives as much as the
    tumour there is no therapy, only injury, and every technique in §14.5 --
    conformal shaping, intensity modulation, the Bragg peak, many-beam
    stereotaxis, putting the source inside -- is an attempt to raise this
    number."""
    if normal_tissue_dose <= 0:
        raise ValueError("the normal-tissue dose must be positive")
    ratio = tumour_dose / normal_tissue_dose
    if ratio <= 1.0:
        raise ValueError("a therapeutic ratio of %.3f means healthy tissue "
                         "receives at least as much dose as the tumour; that is "
                         "not therapy" % ratio)
    return ratio


def brachytherapy_dose_rate(air_kerma_strength, distance_cm,
                            dose_rate_constant=1.109):
    """Dose rate at a distance from a brachytherapy source, cGy/h, in the
    simplest (point-source, 1/r^2) approximation.

    The 1/r^2 IS the therapy: at 1 cm the dose rate is a hundred times that at
    10 cm, so placing the source inside the tumour does geometrically what
    external beams must do with collimators and many angles."""
    if air_kerma_strength < 0:
        raise ValueError("source strength cannot be negative")
    if distance_cm <= 0:
        raise ValueError("the 1/r^2 approximation diverges at the source")
    return dose_rate_constant * air_kerma_strength / distance_cm ** 2


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-27  medical applications\n")

    print("  Table 14.2 is the same photons listed twice  [§14.1.1]")
    print("   element line   lambda (A)   E printed   E = hc/lambda   Moseley")
    for el, lines in ANODE_LINES.items():
        for line, (lam, e, kv) in lines.items():
            if not line.startswith("Ka"):
                continue
            print("   %-7s %-6s %10.4f %11.4f %14.4f %9.2f"
                  % (el, line, lam, e, xray_energy(lam),
                     moseley_k_alpha(ATOMIC_NUMBER[el])))
    print("   -> anode choice IS energy choice: a characteristic line cannot be")
    print("      tuned, only replaced. Hence Mo for mammography (17.5 keV) and")
    print("      W for everything that must penetrate (59.3 keV).")

    print("\n  CT numbers are calibrated attenuation coefficients  [§14.1.5]")
    print("   tissue        mu (1/cm)    HU")
    for name, mu in (("air", 0.0), ("lung", 0.052), ("fat", 0.185),
                     ("water", 0.206), ("blood", 0.214), ("bone", 0.500)):
        print("   %-13s %9.3f %6.0f" % (name, mu, hounsfield_unit(mu)))
    print("   contrast, bone against tissue, through 5 cm:")
    for e, mu_b, mu_t in ((0.02, 3.0, 0.80), (0.06, 0.60, 0.21), (0.10, 0.35, 0.17)):
        print("     %3.0f keV: %.4f" % (e * 1e3, contrast_ratio(mu_b, mu_t, 5.0)))
    print("   -> ~NE-12's photoelectric Z^4/E^3 is the whole reason contrast exists.")

    print("\n  Table 14.3: four positron emitters, one usable off-site")
    print("   nuclide  Emax    Eav   Eav/Emax  T1/2      range (mm)  10% at (h)")
    for n, (emax, eav, br, t12, rxn) in PET_NUCLIDES.items():
        print("   %-8s %5.3f %6.3f %9.3f %7.1f m %10.2f %10.2f"
              % (n, emax, eav, beta_mean_fraction(n), t12,
                 positron_range_mm(eav), usable_transport_time(n)))
    print("   -> all four sit at Eav/Emax ~ 0.40, the beta-PLUS signature")
    print("      (beta-minus is ~0.33). And only 18F survives a journey.")

    print("\n  what PET buys and what it cannot  [§14.1.8]")
    print("   annihilation photons: 2 x %.1f keV, back to back" % annihilation_photon_energy())
    print("   a 10 ns coincidence window is %.0f cm along the line of response"
          % coincidence_window_length(10.0))
    print("   -> so timing does NOT localise within a patient; the geometry does.")
    print("   positron range sets a floor no detector can beat:")
    for n in ("18F", "15O"):
        print("     %-5s %.2f mm" % (n, positron_range_mm(PET_NUCLIDES[n][1])))

    print("\n  therapy is the same quantity optimised the other way  [§14.5]")
    for k, v in THERAPY_MODALITIES.items():
        print("   %-22s %-9s %s" % (k, v["era"], v["sharpening"]))
    print("\n   brachytherapy's 1/r^2, cGy/h per unit strength:")
    for r in (0.5, 1.0, 2.0, 5.0, 10.0):
        print("     %5.1f cm %10.3f" % (r, brachytherapy_dose_rate(1.0, r)))
    print("   -> a factor of 400 between 0.5 and 10 cm, for free.")
    try:
        therapeutic_ratio(60.0, 60.0)
    except ValueError as exc:
        print("\n   therapeutic_ratio(60, 60) refused: %s..." % str(exc)[:56])

    print("\n  the numbers therapy is aimed at  [Tables 14.6, 14.7]")
    tot = [sum(v[i] for v in CANCER_2004.values()) for i in range(4)]
    print("   Table 14.6 column sums   %s" % (tuple(tot),))
    print("   as printed               %s   -> exact, all four" % (CANCER_2004_TOTALS,))
    print("   -> %.2f M new cases, %d k deaths a year (S&F: 1.37 M, 564 k)"
          % ((tot[0] + tot[1]) / 1e6, round((tot[2] + tot[3]) / 1e3)))
    ltot = [sum(v[i] for v in CANCER_LIFETIME_RISK.values()) for i in range(4)]
    print("   lifetime incidence  M %.1f%%  F %.1f%%   ('nearly half')"
          % (ltot[0] / 1e3, ltot[1] / 1e3))
    print("   of those, dying of it   M %.0f%%  F %.0f%%   ('about half survive')"
          % (100.0 * ltot[2] / ltot[0], 100.0 * ltot[3] / ltot[1]))

    print("\n  SPECT's resolution is the collimator's, not the crystal's  [Eq. 14.19]")
    for r_ph in (0.6, 3.0):
        c = spect_system_resolution(r_ph, 4.5, 2.0)
        f = spect_system_resolution(r_ph, 2.5, 2.0)
        print("   pinhole %.1f mm:  R_sys %.2f -> %.2f mm  (%.0f%% of a 2 mm "
              "crystal gain)" % (r_ph, c, f, 50.0 * (c - f)))


if __name__ == "__main__":
    _demo()
