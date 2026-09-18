"""NE-11  Attenuation, cross sections, flux density and reaction rates.

Nuclear Science & Engineering trunk, module NE-11 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 7.1-7.2 (printed pp. 179-193).  Pure stdlib; coefficients from
../../data_tables/C3_photon_coefficients_*.csv and
../../data_tables/C1_thermal_neutron_cross_sections.csv.

~NE-08 through ~NE-10 answered "can this reaction happen, and how much energy
does it release".  This module answers the question that actually gets used:
HOW OFTEN.  Two quantities carry it.

  1. The LINEAR INTERACTION COEFFICIENT mu (for neutrons, the macroscopic cross
     section Sigma) -- the probability per unit path length of interacting.  It
     is the exact analogue of the decay constant lambda of ~NE-06, and it gives
     the exact same mathematics: exponential attenuation, an exponential
     path-length distribution, a mean free path 1/mu playing the role of the mean
     life, and a half-thickness ln2/mu playing the role of the half-life.

  2. The FLUX DENSITY phi = v n -- total particle track length per unit volume
     per unit time.  Reaction rate density is then just their product,

         R_i = mu_i phi ,

     which is the single most-used equation in nuclear engineering.  Everything
     from reactor power to detector counts to tissue dose is that product with
     different subscripts.

The bridge from microscopic to macroscopic is mu = sigma N: a per-atom area times
an atom density.  That is what makes tabulated cross sections usable for any
material at any density.
"""

import bisect
import csv
import math
import os

__all__ = [
    "AVOGADRO", "BARN_CM2", "MATERIALS", "DENSITY_ERRATA",
    "load_photon_coefficients", "load_thermal_cross_sections",
    "absorption_cross_section", "ABSORPTION_CHANNELS",
    "mass_coefficient", "linear_coefficient",
    "uncollided_intensity", "interaction_probability", "survival_probability",
    "path_length_pdf", "mean_free_path", "half_thickness", "tenth_thickness",
    "thickness_for_attenuation", "mean_free_paths_traversed",
    "atom_density", "molecular_density", "macroscopic_cross_section",
    "mixture_mass_coefficient", "mixture_density", "compound_macroscopic",
    "flux_density", "reaction_rate_density", "fluence",
    "point_source_flux", "point_source_flux_shielded", "point_source_flux_layered",
    "buildup_intensity",
]

AVOGADRO = 6.0221415e23
BARN_CM2 = 1.0e-24

# Densities (g/cm3) as used by S&F's Chapter 7 examples and Appendix C captions.
#
# ONE VALUE IS CORRECTED.  S&F Example 7.2 (printed p. 184) writes the iron
# density as 7.784 g/cm3, but the arithmetic in the very next line does not use
# it: the book gets 1/rho_Fe + 1/rho_Pb = 0.2151 cm3 and rho_mix = 9.298 g/cm3,
# which require rho_Fe = 7.874 (7.784 would give 0.2166 and 9.235).  7.874 g/cm3
# is also the accepted density of iron, so the PRINTED value is the typo and the
# arithmetic is right.  `test_the_iron_density_typo` pins both halves.
DENSITY_ERRATA = {"iron": (7.784, 7.874)}

MATERIALS = {
    "air":      {"density": 1.205e-3},
    "water":    {"density": 1.0},
    "concrete": {"density": 2.35},
    "iron":     {"density": 7.874},     # corrected, see DENSITY_ERRATA
    "lead":     {"density": 11.35},
}

_PHOTON = {}
_THERMAL = None


def _table_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, os.pardir, os.pardir, "data_tables"))


def load_photon_coefficients(material):
    """[(E_MeV, {component: cm2/g}), ...] from the extracted Appendix C.3.

    Components are 'c' (Compton/incoherent), 'ph' (photoelectric), 'pp' (pair
    production), 'total', 'tr' (energy transfer) and 'en' (energy absorption).
    Sorted by energy; cached per material."""
    key = material.lower()
    if key in _PHOTON:
        return _PHOTON[key]
    if key not in MATERIALS:
        raise KeyError("no Appendix C.3 table for %r; have %s"
                       % (material, sorted(MATERIALS)))
    path = os.path.join(_table_dir(), "C3_photon_coefficients_%s.csv" % key)
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            rows.append((float(r["E_MeV"]), {
                "c": float(r["mu_c_cm2_g"]),
                "ph": float(r["mu_ph_cm2_g"]),
                "pp": float(r["mu_pp_cm2_g"]),
                "total": float(r["mu_cm2_g"]),
                "tr": float(r["mu_tr_cm2_g"]),
                "en": float(r["mu_en_cm2_g"]),
            }))
    rows.sort(key=lambda t: t[0])
    _PHOTON[key] = rows
    return rows


def load_thermal_cross_sections():
    """{nuclide: {reaction: sigma_barns}} plus abundances, from Appendix C.1.

    Reactions are 'gamma' (radiative capture), 's' (scattering), 't' (total),
    'alpha', 'f' (fission) and 'p' as the table provides them."""
    global _THERMAL
    if _THERMAL is not None:
        return _THERMAL
    path = os.path.join(_table_dir(), "C1_thermal_neutron_cross_sections.csv")
    out = {}
    with open(path, newline="", encoding="utf-8") as fh:
        for r in csv.DictReader(fh):
            e = out.setdefault(r["nuclide"], {"Z": int(r["Z"]), "A": int(r["A"]),
                                              "symbol": r["symbol"], "sigma": {}})
            if r["abundance_pct"]:
                e["abundance_pct"] = float(r["abundance_pct"])
            e["sigma"][r["reaction"]] = float(r["sigma_b"])
    _THERMAL = out
    return out


ABSORPTION_CHANNELS = ("gamma", "alpha", "p", "f")


def absorption_cross_section(nuclide, table=None):
    """sigma_a: the sum of every channel that REMOVES the neutron, in barns.

    Appendix C.1 lists channels separately, and 'absorption' means all of them
    together -- (n,gamma), (n,alpha), (n,p) and (n,f) -- but NOT scattering,
    which changes the neutron's energy without consuming it.

    The distinction is not pedantic.  17O absorbs almost entirely by (n,alpha)
    at 0.235 b, with capture contributing only 0.0038 b; reading the 'gamma'
    column alone would understate its absorption sixty-fold.  S&F's Example 7.3
    uses 0.239 b for 17O, which is the sum."""
    t = load_thermal_cross_sections() if table is None else table
    if nuclide not in t:
        raise KeyError("%s is not in Appendix C.1" % nuclide)
    sig = t[nuclide]["sigma"]
    return sum(sig.get(c, 0.0) for c in ABSORPTION_CHANNELS)


def mass_coefficient(material, e_mev, component="total"):
    """mu/rho (cm2/g) at photon energy e_mev, log-log interpolated in energy.

    Appendix C.3 is tabulated on a coarse grid, and mu/rho is close to a power
    law between points, so log-log interpolation is the right choice -- linear
    interpolation over a decade-wide interval can be 30% out.

    ABSORPTION EDGES.  The table lists edge energies TWICE -- once for the shell
    just closed and once for the shell just opened (lead's K edge at 0.088 MeV
    carries mu_ph = 1.547 and 7.32).  Asking for exactly an edge energy returns
    the LOWER, below-edge value; asking just above returns the upper branch.
    Interpolation never straddles an edge, because the duplicated pair is never
    used as a bracket."""
    rows = load_photon_coefficients(material)
    energies = [e for e, _ in rows]
    if e_mev < energies[0] or e_mev > energies[-1]:
        raise ValueError("%.4g MeV is outside the tabulated range %.4g-%.4g MeV"
                         % (e_mev, energies[0], energies[-1]))
    i = bisect.bisect_left(energies, e_mev)
    if i < len(energies) and energies[i] == e_mev:
        return rows[i][1][component]
    lo, hi = rows[i - 1], rows[i]
    if hi[0] == lo[0]:                  # both halves of an absorption edge
        raise ValueError("%.6g MeV lands on the duplicated edge pair at %.6g MeV"
                         % (e_mev, lo[0]))
    y0, y1 = lo[1][component], hi[1][component]
    if y0 <= 0 or y1 <= 0:
        # linear fallback where a component is zero (e.g. pair production below
        # its 1.022 MeV threshold), since log interpolation is undefined there
        f = (e_mev - lo[0]) / (hi[0] - lo[0])
        return y0 + f * (y1 - y0)
    f = math.log(e_mev / lo[0]) / math.log(hi[0] / lo[0])
    return math.exp(math.log(y0) + f * math.log(y1 / y0))


def linear_coefficient(material, e_mev, component="total", density=None):
    """mu (1/cm) = rho (mu/rho)  [S&F Eq. (7.11) rearranged]."""
    rho = MATERIALS[material.lower()]["density"] if density is None else density
    return rho * mass_coefficient(material, e_mev, component)


# --- exponential attenuation  [S&F §§7.1.2-7.1.4] --------------------------

def uncollided_intensity(i0, mu, x):
    """I^o(x) = I^o(0) exp(-mu x)  [Eq. (7.4)].

    UNCOLLIDED only.  Particles that scatter without being absorbed are still
    present, just at a different energy and direction, so this UNDERSTATES the
    true field -- see `buildup_intensity`."""
    if mu < 0 or x < 0:
        raise ValueError("mu and x must be non-negative")
    return i0 * math.exp(-mu * x)


def interaction_probability(mu, x):
    """P(x) = 1 - exp(-mu x)  [Eq. (7.5)]: the chance of interacting somewhere
    in a path of length x."""
    if mu < 0 or x < 0:
        raise ValueError("mu and x must be non-negative")
    return 1.0 - math.exp(-mu * x)


def survival_probability(mu, x):
    """exp(-mu x)  [Eq. (7.6)]: the chance of crossing x without interacting."""
    return 1.0 - interaction_probability(mu, x)


def path_length_pdf(mu, x):
    """p(x) = mu exp(-mu x)  [Eq. (7.7)]: the distribution of distance to first
    interaction.  Normalised, with mean 1/mu.

    Identical in form to the decay-time density of ~NE-06 -- and for the same
    reason: interacting, like decaying, is memoryless."""
    if mu <= 0:
        raise ValueError("mu must be positive")
    return 0.0 if x < 0 else mu * math.exp(-mu * x)


def mean_free_path(mu):
    """1/mu  [Eq. (7.8)]: the mean distance to the first interaction.

    The direct analogue of the mean lifetime 1/lambda of ~NE-06."""
    if mu <= 0:
        raise ValueError("mu must be positive")
    return 1.0 / mu


def half_thickness(mu):
    """x_1/2 = ln2/mu  [Eq. (7.9)] -- the analogue of the half-life."""
    if mu <= 0:
        raise ValueError("mu must be positive")
    return math.log(2.0) / mu


def tenth_thickness(mu):
    """x_1/10 = ln10/mu  [S&F Example 7.1]."""
    if mu <= 0:
        raise ValueError("mu must be positive")
    return math.log(10.0) / mu


def thickness_for_attenuation(mu, factor):
    """Thickness reducing the uncollided beam by `factor` (e.g. 100 for 1%)."""
    if factor <= 1:
        raise ValueError("attenuation factor must exceed 1")
    if mu <= 0:
        raise ValueError("mu must be positive")
    return math.log(factor) / mu


def mean_free_paths_traversed(mu, x):
    """The dimensionless optical thickness mu*x -- how many mean free paths of
    material a particle must cross.  The only variable exponential attenuation
    actually depends on, which is why shield designers think in mfp."""
    return mu * x


def buildup_intensity(i0, mu, x, buildup=1.0):
    """I(x) = B(x) I^o(x)  [S&F §7.1.5]: total field from the uncollided one.

    B >= 1 always, and for thick shields it is NOT a small correction -- a metre
    of concrete against MeV photons has B of order 10, so ignoring it
    underestimates the dose behind the shield by an order of magnitude.  S&F
    leave B to tabulations and transport calculations; this function just applies
    whatever value the caller supplies."""
    if buildup < 1.0:
        raise ValueError("buildup factor cannot be less than 1")
    return buildup * uncollided_intensity(i0, mu, x)


# --- microscopic to macroscopic  [S&F §7.1.6] -----------------------------

def atom_density(density_g_cm3, atomic_weight):
    """N = rho N_a / A, atoms per cm3."""
    if density_g_cm3 < 0 or atomic_weight <= 0:
        raise ValueError("invalid density or atomic weight")
    return density_g_cm3 * AVOGADRO / atomic_weight


def molecular_density(density_g_cm3, molecular_weight):
    """Molecules per cm3 -- same formula, different bookkeeping."""
    return atom_density(density_g_cm3, molecular_weight)


def macroscopic_cross_section(sigma_barns, number_density_per_cm3):
    """Sigma = sigma N, in 1/cm  [Eq. (7.10)], with sigma in barns."""
    if sigma_barns < 0 or number_density_per_cm3 < 0:
        raise ValueError("cross section and density must be non-negative")
    return sigma_barns * BARN_CM2 * number_density_per_cm3


def mixture_mass_coefficient(components, e_mev, component="total"):
    """(mu/rho)_mix = sum_j w_j (mu/rho)_j  [Eq. (7.13)].

    `components` maps material name -> weight fraction.  Mass coefficients mix by
    WEIGHT fraction, which is why they are tabulated in preference to linear
    ones: the result is independent of how the mixture is packed."""
    total_w = sum(components.values())
    if not components or abs(total_w - 1.0) > 1e-6:
        raise ValueError("weight fractions must sum to 1 (got %.6f)" % total_w)
    return sum(w * mass_coefficient(m, e_mev, component)
               for m, w in components.items())


def mixture_density(components):
    """Density of a mixture assuming no volume change: 1/rho = sum_j w_j/rho_j.

    S&F's Example 7.2 does this the long way (2 g of a 50/50 iron-lead mixture
    occupies 1/7.784 + 1/11.35 cm3); this is the same statement."""
    total_w = sum(components.values())
    if not components or abs(total_w - 1.0) > 1e-6:
        raise ValueError("weight fractions must sum to 1 (got %.6f)" % total_w)
    inv = sum(w / MATERIALS[m.lower()]["density"] for m, w in components.items())
    return 1.0 / inv


def compound_macroscopic(molecular_density_per_cm3, contributions):
    """Sigma for a compound  [Eq. (7.12)]:  Sigma = N_mol sum_i n_i f_i sigma_i,

    with `contributions` a list of (atoms_per_molecule, isotopic_fraction,
    sigma_barns).  This is exactly the sum S&F's Example 7.3 writes out for
    thermal-neutron absorption in water."""
    total = 0.0
    for n_per_molecule, fraction, sigma_b in contributions:
        total += n_per_molecule * fraction * sigma_b
    return macroscopic_cross_section(total, molecular_density_per_cm3)


# --- flux density and reaction rates  [S&F §7.2] --------------------------

def flux_density(number_density, speed_cm_s):
    """phi = v n  [Eq. (7.14)], in 1/(cm2 s).

    Better read as 'total track length per unit volume per unit time' than as
    'flow through an area' -- the track-length reading is what makes R = mu phi
    obvious and works for a field going in all directions at once."""
    if number_density < 0 or speed_cm_s < 0:
        raise ValueError("density and speed must be non-negative")
    return number_density * speed_cm_s


def reaction_rate_density(mu_or_sigma, flux):
    """R_i = mu_i phi  [Eqs. (7.15)-(7.16)], interactions per cm3 per second.

    The single most-used equation in the field.  Reactor power, detector count
    rate and tissue dose are all this product with a different subscript."""
    if mu_or_sigma < 0 or flux < 0:
        raise ValueError("coefficient and flux must be non-negative")
    return mu_or_sigma * flux


def fluence(flux, duration_s):
    """Phi = phi * t for a steady field  [Eq. (7.21)].

    Flux density measures the RATE of interactions; fluence measures their
    CUMULATIVE number, and it is fluence that dose limits are written against
    (~NE-17)."""
    if flux < 0 or duration_s < 0:
        raise ValueError("flux and time must be non-negative")
    return flux * duration_s


# --- point sources  [S&F §7.2.5] ------------------------------------------

def point_source_flux(source_rate, r_cm):
    """Uncollided flux from an isotropic point source in vacuum,
    phi^o = S_p/(4 pi r^2)  [Eq. (7.23)] -- pure geometric attenuation."""
    if r_cm <= 0:
        raise ValueError("distance must be positive")
    if source_rate < 0:
        raise ValueError("source rate must be non-negative")
    return source_rate / (4.0 * math.pi * r_cm * r_cm)


def point_source_flux_shielded(source_rate, r_cm, mu, thickness_cm):
    """phi^o = S_p exp(-mu t)/(4 pi r^2)  [Eq. (7.26)].

    Two independent attenuations: GEOMETRIC (1/r^2, which never saturates but
    only falls as a power law) and MATERIAL (exponential in the shield
    thickness).  Distance is cheap and weak; shielding is expensive and strong.
    Holds for any shield shape, provided the source-detector ray crosses
    thickness t of it."""
    return point_source_flux(source_rate, r_cm) * survival_probability(mu, thickness_cm)


def point_source_flux_layered(source_rate, r_cm, layers):
    """phi^o = S_p exp(-sum_i mu_i t_i)/(4 pi r^2)  [Eq. (7.27)], with `layers`
    a list of (mu, thickness) pairs.

    The exponent is the total optical thickness in mean free paths -- shields
    add in mfp, not in centimetres."""
    optical = sum(mu * t for mu, t in layers)
    if optical < 0:
        raise ValueError("optical thickness cannot be negative")
    return point_source_flux(source_rate, r_cm) * math.exp(-optical)


# --- demo --------------------------------------------------------------------

def _demo():
    print("NE-11  attenuation, cross sections and reaction rates\n")

    print("  S&F Example 7.1: tenth-thickness for 1 MeV photons")
    print("   material    mu/rho (cm2/g)   mu (1/cm)   x_1/10 (cm)   x_1/2 (cm)")
    for m in ("water", "lead"):
        mr = mass_coefficient(m, 1.0)
        mu = linear_coefficient(m, 1.0)
        print("   %-10s %13.5f %11.5f %12.2f %12.3f"
              % (m, mr, mu, tenth_thickness(mu), half_thickness(mu)))
    print("   -> 32.6 cm of water or 2.98 cm of lead; the book gets 12.8 in / 1.17 in.")

    print("\n  S&F Example 7.2: a 50/50 iron-lead mixture at 1 MeV")
    mix = {"iron": 0.5, "lead": 0.5}
    mr = mixture_mass_coefficient(mix, 1.0)
    rho = mixture_density(mix)
    print("   (mu/rho)_mix = 0.5(%.5f) + 0.5(%.5f) = %.5f cm2/g"
          % (mass_coefficient("iron", 1.0), mass_coefficient("lead", 1.0), mr))
    print("   rho_mix = %.3f g/cm3   ->   mu_mix = %.4f 1/cm" % (rho, rho * mr))

    print("\n  S&F Example 7.3: thermal-neutron absorption in water")
    xs = load_thermal_cross_sections()
    n_water = molecular_density(1.0, 18.0153)
    contrib = [(2, 0.99985, absorption_cross_section("1H", xs)),
               (2, 0.00015, absorption_cross_section("2H", xs)),
               (1, 0.99756, absorption_cross_section("16O", xs)),
               (1, 0.00039, absorption_cross_section("17O", xs)),
               (1, 0.00205, absorption_cross_section("18O", xs))]
    sig = compound_macroscopic(n_water, contrib)
    only_h = compound_macroscopic(n_water, contrib[:1])
    print("   N(H2O) = %.5f x 1e24 /cm3" % (n_water / 1e24))
    print("   Sigma_a = %.4f 1/cm   (1H alone: %.4f -- everything else is noise)"
          % (sig, only_h))

    print("\n  the same mathematics as radioactive decay  [~NE-06]")
    mu = linear_coefficient("water", 1.0)
    print("   mu = %.5f /cm  <->  lambda" % mu)
    print("   mean free path %.2f cm  <->  mean life 1/lambda" % mean_free_path(mu))
    print("   half-thickness %.2f cm  <->  half-life ln2/lambda" % half_thickness(mu))
    print("   p(x) = mu exp(-mu x)   <->  decay-time density")

    print("\n  attenuation is exponential in MEAN FREE PATHS, not in cm")
    print("   mfp    transmitted     material thickness (cm) for that many mfp")
    print("                          water       lead")
    for n in (1, 2, 5, 10):
        print("   %3d    %10.3e %10.2f %10.3f"
              % (n, math.exp(-n), n / linear_coefficient("water", 1.0),
                 n / linear_coefficient("lead", 1.0)))

    print("\n  geometric vs material attenuation from a point source")
    print("   1 Ci of a 1 MeV emitter, detector 1 m away in air")
    s = 3.7e10
    print("   bare, in vacuum:            phi = %.3e /cm2/s" % point_source_flux(s, 100.0))
    mu_pb = linear_coefficient("lead", 1.0)
    for t in (0.0, 1.0, 5.0, 10.0):
        print("   through %5.1f cm of lead:    phi = %.3e /cm2/s  (%.1f mfp)"
              % (t, point_source_flux_shielded(s, 100.0, mu_pb, t),
                 mean_free_paths_traversed(mu_pb, t)))
    print("   moving to 10 m instead:     phi = %.3e /cm2/s  (only 100x)"
          % point_source_flux(s, 1000.0))

    print("\n  reaction rates: R = mu phi")
    phi = point_source_flux(s, 100.0)
    mu_en = linear_coefficient("water", 1.0, "en")
    print("   flux %.3e /cm2/s in water, mu_en = %.5f /cm" % (phi, mu_en))
    print("   energy deposition = %.4e MeV/cm3/s" % reaction_rate_density(mu_en, phi))
    print("   fluence after 1 hour = %.3e /cm2" % fluence(phi, 3600.0))


if __name__ == "__main__":
    _demo()
