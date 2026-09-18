"""NE-13  Neutron interactions: the 1/v law, resonances, activation, fission.

Nuclear Science & Engineering trunk, module NE-13 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 7.4 (printed pp. 196-205).  Pure stdlib; cross sections from
../../data_tables/C1_thermal_neutron_cross_sections.csv and
../../data_tables/C2_activation_radionuclides.csv.

~NE-12 decomposed the photon coefficient into three processes with smooth,
predictable Z and E dependences.  Neutron cross sections are the opposite in
every respect, and the contrast is the point of this module:

  * Neutrons interact with the NUCLEUS, not the electrons.  So there is no Z^4,
    no Z/A ~ 1/2, no smooth trend at all -- sigma varies erratically from element
    to element and even between isotopes of the same element.  1H absorbs
    0.333 b and 2H absorbs 0.0005 b; 235U fissions at 587 b and 238U at 1.2e-5 b.
  * There is no predictive theory.  S&F are blunt about it: "all cross-section
    data are empirical in nature, with little guidance available for
    interpolation between different energies or isotopes."  This module therefore
    TABULATES and interpolates within the two regimes where behaviour is regular,
    and refuses to extrapolate anywhere else.

Two regularities do exist, and between them they carry most of reactor physics:

  1. THE 1/v LAW.  Below ~1 keV, absorption goes as 1/sqrt(E) -- a slow neutron
     spends longer near a nucleus and is likelier to be captured.  This is what
     makes moderation (~NE-08) worth the trouble: slowing a fission neutron by
     eight decades raises its fission cross section on 235U by a factor of ~1000.
  2. RESONANCES.  Narrow, enormous peaks where the neutron's energy matches a
     compound-nucleus level.  Their placement is what separates fuel from
     poison from structure, and their WIDTH relative to spacing is why 238U
     capture is a resonance-escape problem rather than a simple absorption
     (~NE-19).
"""

import csv
import math
import os

__all__ = [
    "AVOGADRO", "BARN_CM2", "M_N_U", "K_BOLTZ_EV_PER_K",
    "E_THERMAL_EV", "V_THERMAL_CM_S", "T_THERMAL_K",
    "NUCLIDE_CLASS", "RESONANCE_CHARACTER", "SECONDARY_NEUTRON_THRESHOLDS",
    "load_thermal_cross_sections", "load_activation_data",
    "absorption_cross_section", "scattering_cross_section", "total_cross_section",
    "fission_cross_section", "capture_to_fission_ratio", "eta_neutrons_per_absorption",
    "neutron_speed", "neutron_energy_from_speed", "maxwellian_most_probable_energy",
    "one_over_v_cross_section", "light_nucleus_total_cross_section",
    "classify_nuclide", "resonance_character",
    "macroscopic_cross_section", "atom_density", "mean_free_path",
    "activation_rate", "activation_activity", "saturation_activity",
    "is_fissile", "is_fissionable",
]

AVOGADRO = 6.0221415e23
BARN_CM2 = 1.0e-24
M_N_U = 1.0086649156
K_BOLTZ_EV_PER_K = 8.617343e-5

# The thermal reference point, at which Appendix C.1 is quoted.
E_THERMAL_EV = 0.0253            # 2200 m/s neutron
V_THERMAL_CM_S = 2.2e5
T_THERMAL_K = 293.6              # E = kT at 0.0253 eV

# S&F §7.4.1 (printed p. 199): the three broad categories
NUCLIDE_CLASS = {"light": (0, 25), "intermediate": (25, 150), "heavy": (150, 300)}

# S&F §7.4.1: resonance character by category -- (typical energy, typical width)
RESONANCE_CHARACTER = {
    "light":        {"energy": "keV to MeV", "width": "keV to MeV",
                     "note": "wide and sparse; H and D have none at all"},
    "intermediate": {"energy": "100 eV to several keV", "width": "intermediate",
                     "note": "neither as high nor as narrow as heavy nuclei"},
    "heavy":        {"energy": "eV region", "width": "1 eV or less",
                     "note": "narrow with large peak values; unresolved above a few keV"},
}

# S&F §7.4.1 (printed p. 204): (n,2n) thresholds, MeV.  Most nuclides sit near
# 8 MeV, but D and Be are anomalously low AND have no inelastic competition.
SECONDARY_NEUTRON_THRESHOLDS = {"2H": 3.3, "9Be": 1.84, "typical": 8.0}

_THERMAL = None
_ACTIVATION = None


def _table_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, os.pardir, os.pardir, "data_tables"))


def load_thermal_cross_sections():
    """{nuclide: {"Z", "A", "symbol", "sigma": {reaction: barns}, ...}} from
    Appendix C.1.  Reactions: 'gamma', 's', 't', 'alpha', 'p', 'f'."""
    global _THERMAL
    if _THERMAL is not None:
        return _THERMAL
    out = {}
    with open(os.path.join(_table_dir(), "C1_thermal_neutron_cross_sections.csv"),
              newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            e = out.setdefault(r["nuclide"], {"Z": int(r["Z"]), "A": int(r["A"]),
                                              "symbol": r["symbol"], "sigma": {}})
            if r["abundance_pct"]:
                e["abundance_pct"] = float(r["abundance_pct"])
            if r["half_life"]:
                e["half_life"] = r["half_life"]
            e["sigma"][r["reaction"]] = float(r["sigma_b"])
    _THERMAL = out
    return out


def load_activation_data():
    """{activated_nuclide: {...}} from Appendix C.2 -- the (n,gamma) activation
    cross sections and the half-lives of what they produce.

    `sigma_b` is None where the table leaves it blank, and `parent_abundance_pct`
    is None where the parent does not occur naturally.  Both blanks are
    meaningful rather than missing: 99mTc's parent 99Mo is a FISSION PRODUCT
    (~NE-09), reached by decay rather than by neutron capture on a stable target,
    so no activation cross section applies to it at all.  Callers must handle
    None rather than have a zero substituted for them."""
    global _ACTIVATION
    if _ACTIVATION is not None:
        return _ACTIVATION
    out = {}
    with open(os.path.join(_table_dir(), "C2_activation_radionuclides.csv"),
              newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            out[r["activated_nuclide"]] = {
                "half_life": r["activated_half_life"],
                "parent": r["parent_nuclide"],
                "parent_abundance_pct": (float(r["parent_abundance_pct"])
                                         if r["parent_abundance_pct"] else None),
                "sigma_b": (float(r["activation_sigma_b"])
                            if r["activation_sigma_b"] else None),
            }
    _ACTIVATION = out
    return out


# --- cross-section lookups  [Table C.1] -----------------------------------

ABSORPTION_CHANNELS = ("gamma", "alpha", "p", "f")


def _sigma(nuclide, table=None):
    t = load_thermal_cross_sections() if table is None else table
    if nuclide not in t:
        raise KeyError("%s is not in Appendix C.1" % nuclide)
    return t[nuclide]["sigma"]


def absorption_cross_section(nuclide, table=None):
    """sigma_a: every channel that REMOVES the neutron -- (n,gamma), (n,alpha),
    (n,p), (n,f) -- but not scattering, which only changes its energy.

    The same convention as ~NE-11; repeated here because this module is where it
    does the most work."""
    s = _sigma(nuclide, table)
    return sum(s.get(c, 0.0) for c in ABSORPTION_CHANNELS)


def scattering_cross_section(nuclide, table=None):
    """sigma_s, the elastic scattering cross section."""
    return _sigma(nuclide, table).get("s", 0.0)


def total_cross_section(nuclide, table=None):
    """sigma_t as tabulated, falling back to sigma_a + sigma_s.

    S&F note that sigma_t is "the most easily measured and the most widely
    reported", and that a large sigma_t is the signal to go looking at the
    components in detail."""
    s = _sigma(nuclide, table)
    if "t" in s:
        return s["t"]
    return absorption_cross_section(nuclide, table) + scattering_cross_section(nuclide, table)


def fission_cross_section(nuclide, table=None):
    """sigma_f at thermal energy, 0 if the nuclide has no fission entry."""
    return _sigma(nuclide, table).get("f", 0.0)


def capture_to_fission_ratio(nuclide, table=None):
    """alpha = sigma_gamma/sigma_f, the capture-to-fission ratio.

    Every captured neutron is one not causing fission AND one making a heavier
    actinide, so alpha is a direct measure of how wastefully a fuel absorbs.
    235U's 0.169 against 239Pu's 0.362 is a large part of why plutonium recycling
    is harder than it looks (~NE-23)."""
    f = fission_cross_section(nuclide, table)
    if f <= 0:
        raise ValueError("%s has no thermal fission cross section" % nuclide)
    return _sigma(nuclide, table).get("gamma", 0.0) / f


def eta_neutrons_per_absorption(nuclide, nu, table=None):
    """eta = nu sigma_f/sigma_a: neutrons released per neutron ABSORBED, as
    distinct from nu, the neutrons per FISSION.

    This is the quantity that has to exceed 1 for a chain reaction, and it is
    always smaller than nu because some absorptions are captures.  It opens the
    four-factor formula of ~NE-19."""
    a = absorption_cross_section(nuclide, table)
    if a <= 0:
        raise ValueError("%s has no absorption cross section" % nuclide)
    return nu * fission_cross_section(nuclide, table) / a


# --- speeds, energies and the 1/v law  [Eq. (7.40)] -----------------------

def neutron_speed(e_ev):
    """Non-relativistic speed in cm/s from kinetic energy in eV."""
    if e_ev < 0:
        raise ValueError("energy must be non-negative")
    # E = mv^2/2 with m in u; 1 u = 1.6605389e-24 g, 1 eV = 1.6021765e-12 erg
    m_g = M_N_U * 1.6605389e-24
    return math.sqrt(2.0 * e_ev * 1.6021765e-12 / m_g)


def neutron_energy_from_speed(v_cm_s):
    """Kinetic energy in eV from speed in cm/s -- the inverse of `neutron_speed`."""
    if v_cm_s < 0:
        raise ValueError("speed must be non-negative")
    m_g = M_N_U * 1.6605389e-24
    return 0.5 * m_g * v_cm_s ** 2 / 1.6021765e-12


def maxwellian_most_probable_energy(temperature_k=T_THERMAL_K):
    """kT in eV -- the most probable energy of a Maxwellian neutron population.

    0.0253 eV at 293.6 K, the reference point for every tabulated thermal cross
    section, corresponding to 2200 m/s."""
    return K_BOLTZ_EV_PER_K * temperature_k


def one_over_v_cross_section(sigma_ref, e_ev, e_ref_ev=E_THERMAL_EV):
    """Absorption cross section under the 1/v law:

        sigma(E) = sigma_ref sqrt(E_ref/E) .

    The second term of S&F Eq. (7.40).  A slow neutron lingers near the nucleus
    in proportion to 1/v, so the capture probability scales the same way.  Good
    below ~1 keV for light nuclei and away from resonances; NOT valid across a
    resonance, which is why `light_nucleus_total_cross_section` carries a range
    check and this function documents its own."""
    if e_ev <= 0 or e_ref_ev <= 0:
        raise ValueError("energies must be positive")
    if sigma_ref < 0:
        raise ValueError("cross section must be non-negative")
    return sigma_ref * math.sqrt(e_ref_ev / e_ev)


def light_nucleus_total_cross_section(sigma1, sigma2, e_ev):
    """S&F Eq. (7.40):  sigma_t = sigma_1 + sigma_2/sqrt(E).

    Two terms with two different physical origins: sigma_1 is elastic
    scattering, which is nearly energy-independent at low energy, and
    sigma_2/sqrt(E) is radiative capture obeying 1/v.  Valid for light and some
    magic-number nuclei below about 1 keV.

    Raises above 1 keV rather than extrapolating -- above that, resonances
    appear and Eq. (7.40) means nothing."""
    if e_ev <= 0:
        raise ValueError("energy must be positive")
    if e_ev > 1.0e3:
        raise ValueError("Eq. (7.40) is stated for E < 1 keV; %.4g eV is above "
                         "the resonance onset, where no smooth form applies" % e_ev)
    return sigma1 + sigma2 / math.sqrt(e_ev)


# --- classification  [S&F §7.4.1, printed p. 199] -------------------------

def classify_nuclide(A):
    """'light' (A < 25), 'intermediate', or 'heavy' (A > 150)."""
    if A < 1:
        raise ValueError("mass number must be at least 1")
    if A < 25:
        return "light"
    return "heavy" if A > 150 else "intermediate"


def resonance_character(A):
    """What the resonances look like for a nuclide of this mass -- energy,
    width and a qualitative note  [S&F §7.4.1].

    The trend is monotone and physically simple: heavier nuclei have denser
    level schemes, so their resonances come at lower energies, closer together
    and narrower.  Above a few keV a heavy nuclide's resonances cannot even be
    resolved."""
    return RESONANCE_CHARACTER[classify_nuclide(A)]


# --- macroscopic quantities (as ~NE-11) -----------------------------------

def atom_density(density_g_cm3, atomic_weight):
    """N = rho N_a/A, atoms per cm3."""
    if density_g_cm3 < 0 or atomic_weight <= 0:
        raise ValueError("invalid density or atomic weight")
    return density_g_cm3 * AVOGADRO / atomic_weight


def macroscopic_cross_section(sigma_barns, number_density_per_cm3):
    """Sigma = sigma N, in 1/cm."""
    if sigma_barns < 0 or number_density_per_cm3 < 0:
        raise ValueError("cross section and density must be non-negative")
    return sigma_barns * BARN_CM2 * number_density_per_cm3


def mean_free_path(sigma_macroscopic):
    """1/Sigma, cm."""
    if sigma_macroscopic <= 0:
        raise ValueError("macroscopic cross section must be positive")
    return 1.0 / sigma_macroscopic


# --- activation  [S&F Example 7.5, printed p. 204] ------------------------

def activation_rate(mass_g, atomic_weight, sigma_b, flux):
    """(n,gamma) reactions per second in a thin sample:

        R = (m N_a/A) sigma phi ,

    i.e. Eq. (7.24) with the sample volume cancelling against the density.  Thin
    means the flux is undepressed through the sample -- true when the sample is
    much less than a mean free path thick, which is the usual foil-activation
    condition."""
    if mass_g < 0 or flux < 0:
        raise ValueError("mass and flux must be non-negative")
    n_atoms = mass_g * AVOGADRO / atomic_weight
    return n_atoms * sigma_b * BARN_CM2 * flux


def activation_activity(mass_g, atomic_weight, sigma_b, flux, t_irrad_s,
                        half_life_s=None):
    """Activity (Bq) immediately after irradiation.

    With `half_life_s` given, uses the exact saturation form of ~NE-07,
        A = R [1 - exp(-lambda t)] ,
    which is what a long irradiation needs.  Without it, assumes t << T_half and
    returns lambda R t -- the approximation S&F's Example 7.5 makes explicitly
    ("the irradiation time is very small compared to the half-life").  Supply the
    half-life unless you have checked that assumption."""
    r = activation_rate(mass_g, atomic_weight, sigma_b, flux)
    if half_life_s is None:
        raise ValueError("half_life_s is required; pass it explicitly so the "
                         "short-irradiation assumption is a choice, not a default")
    if half_life_s <= 0 or t_irrad_s < 0:
        raise ValueError("half-life must be positive and time non-negative")
    lam = math.log(2.0) / half_life_s
    return r * (1.0 - math.exp(-lam * t_irrad_s))


def saturation_activity(mass_g, atomic_weight, sigma_b, flux):
    """The ceiling: irradiate forever and the activity approaches the production
    rate R  [~NE-07's saturation].  No amount of irradiation exceeds it."""
    return activation_rate(mass_g, atomic_weight, sigma_b, flux)


# --- fissile vs fissionable  [S&F §7.4.2, printed p. 205] -----------------

def is_fissile(nuclide, table=None, threshold_b=100.0):
    """True if the nuclide fissions readily on a THERMAL neutron.

    S&F name 233U, 235U and 239Pu; the tabulated thermal fission cross sections
    separate them from everything else by four orders of magnitude, so any
    threshold in that gap gives the same answer (~NE-09 derives the underlying
    pairing argument)."""
    return fission_cross_section(nuclide, table) >= threshold_b


def is_fissionable(nuclide, table=None):
    """True if the nuclide can be made to fission by a sufficiently energetic
    neutron -- which is most heavy nuclides, including every fissile one."""
    t = load_thermal_cross_sections() if table is None else table
    if nuclide not in t:
        raise KeyError("%s is not in Appendix C.1" % nuclide)
    return t[nuclide]["A"] > 220


# --- demo --------------------------------------------------------------------

def _demo():
    xs = load_thermal_cross_sections()
    print("NE-13  neutron interactions\n")

    print("  neutron cross sections are erratic where photon ones are smooth")
    print("   nuclide   sigma_a (b)   sigma_s (b)   s/a      comment")
    for n, note in [("1H", "moderates well, absorbs a little"),
                    ("2H", "absorbs 660x less than 1H"),
                    ("10B", "the standard absorber"),
                    ("11B", "its own isotope, 700x weaker"),
                    ("12C", "graphite: scatters, never absorbs"),
                    ("235U", "fissions"),
                    ("238U", "captures instead")]:
        a = absorption_cross_section(n, xs)
        s = scattering_cross_section(n, xs)
        ratio = "%8.3g" % (s / a) if (a and s) else "%8s" % ("-" if not s else "inf")
        print("   %-9s %11.4g %13s %s   %s"
              % (n, a, ("%.4g" % s) if s else "n/t", ratio, note))
    print("   ('n/t' = not tabulated separately in C.1)")
    print("   -> 1H vs 2H differ by 660x; 10B vs 11B by 700000x.  No trend to fit.")

    print("\n  the 1/v law  [Eq. (7.40), second term]")
    print("   E (eV)      v (cm/s)     sigma_a(1H)   x thermal")
    for e in (1e-3, 0.0253, 1.0, 100.0, 1e3):
        s = one_over_v_cross_section(absorption_cross_section("1H", xs), e)
        print("   %9.4g %12.3e %12.4g %10.3f" % (e, neutron_speed(e), s,
                                                 s / absorption_cross_section("1H", xs)))
    print("   -> slowing a neutron from 1 keV to thermal multiplies capture by 200.")

    print("\n  which is why moderation pays: 235U fission at fast vs thermal")
    print("   thermal sigma_f(235U) = %.0f b" % fission_cross_section("235U", xs))
    print("   at 1 MeV it is about 1 b -- a factor of ~600 lost by not moderating.")

    print("\n  resonance character by mass  [§7.4.1]")
    print("   nuclide    A   class          resonances")
    for n in ("1H", "12C", "23Na", "56Fe", "238U"):
        A = xs[n]["A"] if n in xs else {"23Na": 23, "56Fe": 56}[n]
        rc = resonance_character(A)
        print("   %-9s %3d  %-13s %s at %s" % (n, A, classify_nuclide(A),
                                               rc["width"], rc["energy"]))

    print("\n  S&F Example 7.5: activating a 2 g manganese sample")
    act = load_activation_data()
    mn = act["56Mn"]
    t_half = 2.579 * 3600.0
    a = activation_activity(2.0, 55.0, mn["sigma_b"], 1e13, 120.0, t_half)
    print("   55Mn(n,gamma)56Mn, sigma = %.1f b, T_1/2 = %s" % (mn["sigma_b"], mn["half_life"]))
    print("   2 g, 1e13 /cm2/s, 120 s  ->  %.4e Bq   (book: 2.609e10)" % a)
    print("   saturation activity would be %.4e Bq -- %.2f%% of the way there"
          % (saturation_activity(2.0, 55.0, mn["sigma_b"], 1e13),
             100 * a / saturation_activity(2.0, 55.0, mn["sigma_b"], 1e13)))

    print("\n  fissile vs merely fissionable  [§7.4.2]")
    print("   nuclide   sigma_f (b)   sigma_gamma (b)   alpha = c/f   fissile?")
    for n in ("233U", "235U", "239Pu", "241Pu", "238U", "232Th", "240Pu"):
        f = fission_cross_section(n, xs)
        g = xs[n]["sigma"].get("gamma", 0.0)
        try:
            al = "%.3f" % capture_to_fission_ratio(n, xs)
        except ValueError:
            al = "-"
        print("   %-9s %11.4g %17.4g %13s   %s"
              % (n, f, g, al, "yes" if is_fissile(n, xs) else "no"))

    print("\n  eta: neutrons per neutron ABSORBED (not per fission)")
    for n, nu in (("233U", 2.48), ("235U", 2.43), ("239Pu", 2.87)):
        print("   %-7s nu = %.2f  ->  eta = %.3f" % (n, nu, eta_neutrons_per_absorption(n, nu, xs)))
    print("   -> eta > 1 is the necessary condition for a chain reaction (~NE-19).")


if __name__ == "__main__":
    _demo()
