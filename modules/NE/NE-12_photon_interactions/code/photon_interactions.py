"""NE-12  Photon interactions: photoelectric, Compton, pair production.

Nuclear Science & Engineering trunk, module NE-12 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 7.3 (printed pp. 191-196).  Pure stdlib; coefficients from
../../data_tables/C3_photon_coefficients_*.csv.

~NE-11 took mu as given and asked what follows from it.  This module opens it up.
Across the 10 eV - 20 MeV range that matters for shielding, exactly three
processes carry the whole of mu, and they divide the energy axis between them:

    PHOTOELECTRIC     sigma ~ Z^4/E^3      dominant below ~0.1 MeV (in lead)
    COMPTON           sigma ~ Z/E          dominant in between
    PAIR PRODUCTION   sigma ~ Z^2          dominant above ~5 MeV, zero below 1.022

Two consequences run through the rest of the trunk.

  1. The Z-dependence is what makes shielding materials different.  Compton
     scattering goes as Z per atom, i.e. as Z/A ~ 1/2 per GRAM, so at MeV
     energies every material is about equally good per gram and lead wins only on
     density (~NE-11 P2).  The photoelectric effect's Z^4 breaks that tie
     completely at low energy: per gram, lead beats water by 2000x at 100 keV.
     High-Z shields are for x-rays; mass is for gammas.

  2. Only the photoelectric effect absorbs the photon outright.  Compton
     scattering leaves a degraded photon still travelling, and pair production
     returns two 0.511 MeV annihilation photons.  So mu counts interactions while
     mu_en counts energy actually deposited, and the two differ by more than a
     factor of two over most of the MeV range -- the distinction ~NE-17 is built
     on, and the reason buildup factors exist at all.
"""

import bisect
import csv
import math
import os

__all__ = [
    "M_E_C2_MEV", "TWO_ME_C2_MEV", "R_E_CM", "AVOGADRO", "BARN_CM2",
    "K_EDGE_KEV", "FLUORESCENT_YIELD", "MATERIALS",
    "load_photon_coefficients", "mass_coefficient", "linear_coefficient",
    "photoelectron_energy", "photoelectric_scaling",
    "compton_scattered_energy", "compton_electron_energy",
    "compton_edge", "backscatter_energy", "compton_wavelength_shift_A",
    "klein_nishina_per_electron", "klein_nishina_per_atom",
    "klein_nishina_mass_coefficient",
    "pair_production_threshold", "triplet_production_threshold",
    "pair_kinetic_energy_shared", "annihilation_photon_energy",
    "dominant_process", "crossover_energies",
    "energy_transfer_fraction",
]

M_E_C2_MEV = 0.51099891           # electron rest energy
TWO_ME_C2_MEV = 2.0 * M_E_C2_MEV  # 1.022 MeV -- the pair-production threshold
R_E_CM = 2.8179403e-13            # classical electron radius  [S&F Eq. (7.35)]
AVOGADRO = 6.0221415e23
BARN_CM2 = 1.0e-24

# S&F §7.3.1 (printed p. 192): K-shell binding energies, keV
K_EDGE_KEV = {"H": 0.0136, "C": 0.284, "O": 0.543, "Fe": 7.11, "Pb": 88.0, "U": 116.0}

# S&F §7.3.1: K-shell fluorescent yield at the two ends of the quoted range
FLUORESCENT_YIELD = {8: 0.005, 90: 0.965}

# Effective Z/A for the tabulated materials, and densities (see ~NE-11).
#
# Four of these are the standard NIST values.  CONCRETE is not: S&F's Appendix
# C.3 table is captioned "ANSI/ANS-6.4.3 standard concrete", whose composition
# differs from NIST's "ordinary concrete" (Z/A = 0.50932).  Using the NIST value
# leaves a 1.5% offset in the Compton coefficient that is CONSTANT with energy --
# the signature of a composition error rather than a physics one, since binding
# effects vanish at high energy.  Solving the tabulated Compton column for Z/A
# at 3 and 10 MeV, where the free-electron formula is exact to 0.3%, gives 0.5013
# and 0.5019; 0.5015 is adopted.  `test_z_over_a_is_recoverable_from_the_tables`
# re-derives all five and pins concrete against NIST's value.
MATERIALS = {
    "air":      {"density": 1.205e-3, "z_over_a": 0.49919},
    "water":    {"density": 1.0,      "z_over_a": 0.55509},
    "concrete": {"density": 2.35,     "z_over_a": 0.50150},   # from the book's own table
    "iron":     {"density": 7.874,    "z_over_a": 0.46557},
    "lead":     {"density": 11.35,    "z_over_a": 0.39575},
}
Z_OVER_A_NIST_ORDINARY_CONCRETE = 0.50932   # NOT what S&F's table uses

_PHOTON = {}


def _table_dir():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(here, os.pardir, os.pardir, "data_tables"))


def load_photon_coefficients(material):
    """[(E_MeV, {component: cm2/g}), ...] from the extracted Appendix C.3.

    Components: 'c' (incoherent/Compton), 'ph' (photoelectric), 'pp' (pair
    production), 'total', 'tr' (energy transfer), 'en' (energy absorption)."""
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


def mass_coefficient(material, e_mev, component="total"):
    """mu/rho (cm2/g), log-log interpolated in energy (see ~NE-11).

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
        f = (e_mev - lo[0]) / (hi[0] - lo[0])
        return y0 + f * (y1 - y0)
    f = math.log(e_mev / lo[0]) / math.log(hi[0] / lo[0])
    return math.exp(math.log(y0) + f * math.log(y1 / y0))


def linear_coefficient(material, e_mev, component="total", density=None):
    """mu (1/cm) = rho (mu/rho)."""
    rho = MATERIALS[material.lower()]["density"] if density is None else density
    return rho * mass_coefficient(material, e_mev, component)


# --- photoelectric effect  [S&F §7.3.1, printed p. 192] -------------------

def photoelectron_energy(e_mev, binding_mev):
    """E_e = E - E_b  [S&F §7.3.1].

    The recoiling atom takes essentially none of it -- it is thousands of times
    heavier than the electron, and by the inverse-mass split of ~NE-08 its share
    is negligible.  The photon is destroyed outright, which is what makes the
    photoelectric effect the only one of the three processes that is pure
    absorption."""
    if e_mev < binding_mev:
        raise ValueError("photon energy %.4g MeV is below the %.4g MeV binding "
                         "energy -- the shell is not accessible"
                         % (e_mev, binding_mev))
    return e_mev - binding_mev


def photoelectric_scaling(Z, e_mev, n=3.0, m=4.0):
    """Relative photoelectric cross section, sigma ~ Z^m/E^n  [Eq. (7.32)].

    S&F give n ~ 3 below about 150 keV falling to n ~ 1 above 5 MeV, and m from
    about 4 at 100 keV to 4.6 at 3 MeV, so this is explicitly a SCALING and not a
    cross section: it is dimensionless and useful only in ratios.  Use it to
    compare materials at fixed energy, or energies at fixed material, never to
    predict an absolute mu."""
    if Z < 1 or e_mev <= 0:
        raise ValueError("need Z >= 1 and positive energy")
    return Z ** m / e_mev ** n


# --- Compton scattering  [S&F §7.3.2, printed pp. 192-193] ----------------

def compton_scattered_energy(e_mev, theta_rad):
    """Scattered-photon energy  [Eq. (7.33), from Eq. (2.30)]:

        E' = E / [1 + (E/m_e c^2)(1 - cos theta)] .

    Note what does NOT appear: the target material.  Compton kinematics are
    scattering off a free electron, and every electron is identical, so E'
    depends only on E and angle.  That universality is why a Compton edge lands
    at the same energy in every detector material (~NE-15)."""
    if e_mev <= 0:
        raise ValueError("photon energy must be positive")
    return e_mev / (1.0 + (e_mev / M_E_C2_MEV) * (1.0 - math.cos(theta_rad)))


def compton_electron_energy(e_mev, theta_rad):
    """Kinetic energy given to the recoil electron, E - E'.

    This is what a detector actually measures: the scattered photon usually
    escapes, so a Compton event deposits only the electron's share (~NE-15)."""
    return e_mev - compton_scattered_energy(e_mev, theta_rad)


def compton_edge(e_mev):
    """Maximum electron energy, at theta = 180 degrees:

        E_max = E * 2E/(m_e c^2 + 2E) .

    The COMPTON EDGE -- the sharp upper end of the continuum in every gamma
    spectrum.  For 137Cs's 662 keV line it sits at 477 keV, a number worth
    memorising because it calibrates spectra (~NE-15)."""
    return compton_electron_energy(e_mev, math.pi)


def backscatter_energy(e_mev):
    """Energy of a photon scattered straight back, E'(180 degrees).

    Tends to m_e c^2/2 = 0.2555 MeV as E -> infinity, so backscatter peaks in
    gamma spectra always cluster near 200-250 keV regardless of source energy --
    the complement of the Compton edge, and their sum is E."""
    return compton_scattered_energy(e_mev, math.pi)


def compton_wavelength_shift_A(theta_rad):
    """Wavelength shift in angstroms, (h/m_e c)(1 - cos theta).

    The Compton wavelength h/m_e c = 0.02426 A is a CONSTANT, independent of both
    the photon energy and the material -- which is the whole content of Compton's
    1923 experiment and the reason it settled that photons carry momentum."""
    lambda_c = 0.0242631023867          # h/(m_e c), angstroms
    return lambda_c * (1.0 - math.cos(theta_rad))


def klein_nishina_per_electron(e_mev):
    """Total Compton cross section per ELECTRON, cm^2  [Eq. (7.34) with Z = 1]:

        sigma = pi r_e^2 lambda [ (1 - 2L - 2L^2) ln(1 + 2/L)
                                  + 2(1 + 9L + 8L^2 + 2L^3)/(L + 2)^2 ]

    with L = m_e c^2/E.  Falls roughly as 1/E at high energy and tends to the
    Thomson cross section 6.65e-25 cm^2 as E -> 0."""
    if e_mev <= 0:
        raise ValueError("photon energy must be positive")
    L = M_E_C2_MEV / e_mev
    term = ((1.0 - 2.0 * L - 2.0 * L * L) * math.log(1.0 + 2.0 / L)
            + 2.0 * (1.0 + 9.0 * L + 8.0 * L * L + 2.0 * L ** 3) / (L + 2.0) ** 2)
    return math.pi * R_E_CM ** 2 * L * term


def klein_nishina_per_atom(e_mev, Z):
    """Total Compton cross section per atom, Z times the per-electron value
    [Eq. (7.34)].

    The linear Z is the key fact: Compton scattering sees electrons, not atoms,
    and every atom simply supplies Z of them."""
    if Z < 1:
        raise ValueError("Z must be at least 1")
    return Z * klein_nishina_per_electron(e_mev)


def klein_nishina_mass_coefficient(e_mev, z_over_a):
    """Compton mass coefficient, mu_c/rho = (N_a Z/A) sigma_KN, in cm2/g.

    Because Z/A ~ 0.5 for everything except hydrogen, this is nearly
    MATERIAL-INDEPENDENT -- which is why the MeV-range mass coefficients of five
    very different materials in Appendix C.3 agree within 15% (~NE-11 P2)."""
    if z_over_a <= 0:
        raise ValueError("Z/A must be positive")
    return AVOGADRO * z_over_a * klein_nishina_per_electron(e_mev)


# --- pair production  [S&F §7.3.3, printed pp. 194-195] -------------------

def pair_production_threshold():
    """2 m_e c^2 = 1.022 MeV  [S&F §7.3.3].

    The rest energy of the pair that must be created.  Below it the process is
    forbidden absolutely, not merely unlikely -- which is why the 'pp' column of
    Appendix C.3 is identically zero below 1.022 MeV and non-zero above."""
    return TWO_ME_C2_MEV


def triplet_production_threshold():
    """4 m_e c^2 = 2.044 MeV: pair production in the field of an ELECTRON rather
    than a nucleus.  The threshold doubles because the light recoiling electron
    must carry real momentum, unlike a heavy nucleus."""
    return 2.0 * TWO_ME_C2_MEV


def pair_kinetic_energy_shared(e_mev):
    """E+ + E- = E_gamma - 2 m_e c^2  [Eq. (7.36)]: the kinetic energy shared by
    the created positron and electron, the nucleus taking momentum but
    negligible energy."""
    if e_mev < TWO_ME_C2_MEV:
        raise ValueError("%.4g MeV is below the %.4g MeV pair threshold"
                         % (e_mev, TWO_ME_C2_MEV))
    return e_mev - TWO_ME_C2_MEV


def annihilation_photon_energy():
    """0.511 MeV.  The positron slows to rest and annihilates, returning TWO
    photons back-to-back at m_e c^2 each  [S&F §7.3.3].

    So pair production does not remove 1.022 MeV from the field permanently -- it
    parks it, and hands it back as two penetrating photons some distance away.
    The 511 keV line is the signature of every positron emitter and the whole
    basis of PET (~NE-27)."""
    return M_E_C2_MEV


# --- putting the three together  [S&F §7.3.4] -----------------------------

def dominant_process(material, e_mev):
    """Which of 'ph', 'c', 'pp' has the largest coefficient at this energy."""
    parts = {k: mass_coefficient(material, e_mev, k) for k in ("ph", "c", "pp")}
    return max(parts, key=lambda k: parts[k])


def crossover_energies(material, lo=1e-3, hi=20.0, steps=4000):
    """(E_ph_to_c, E_c_to_pp) in MeV: where the dominant process changes.

    For water these are about 0.03 and 24 MeV; for lead about 0.5 and 5 MeV.
    The Compton window is WIDE for light materials and NARROW for heavy ones,
    which is the practical statement of the Z^4 and Z^2 scalings."""
    rows = load_photon_coefficients(material)
    lo = max(lo, rows[0][0])
    hi = min(hi, rows[-1][0])
    first = second = None
    prev = dominant_process(material, lo)
    for i in range(1, steps + 1):
        e = lo * (hi / lo) ** (i / float(steps))
        cur = dominant_process(material, e)
        if cur != prev:
            if prev == "ph" and first is None:
                first = e
            elif cur == "pp" and second is None:
                second = e
            prev = cur
    return first, second


def energy_transfer_fraction(material, e_mev):
    """f = mu_en/mu  [Eq. (7.39) rearranged]: the fraction of the interacting
    photon's energy actually deposited locally.

    Well below 1 through the Compton region, because the scattered photon leaves
    carrying most of the energy.  This is precisely the gap that buildup factors
    (~NE-11) and dose calculations (~NE-17) live in."""
    mu = mass_coefficient(material, e_mev, "total")
    if mu <= 0:
        raise ValueError("total coefficient is zero at %.4g MeV" % e_mev)
    return mass_coefficient(material, e_mev, "en") / mu


# --- demo --------------------------------------------------------------------

def _demo():
    print("NE-12  photon interactions\n")

    print("  the three processes divide the energy axis")
    print("   material   photoelectric -> Compton   Compton -> pair")
    for m in ("water", "concrete", "iron", "lead"):
        a, b = crossover_energies(m)
        print("   %-10s %14s MeV %17s MeV"
              % (m, "%.4f" % a if a else "-", "%.2f" % b if b else ">20"))
    print("   -> the Compton window is wide for light materials, narrow for heavy.")

    print("\n  Klein-Nishina against the tabulated Compton coefficient")
    print("   E (MeV)   sigma_KN/electron   mu_c/rho computed   tabulated   ratio")
    zoa = MATERIALS["water"]["z_over_a"]
    for e in (0.1, 0.5, 1.0, 5.0, 10.0):
        kn = klein_nishina_per_electron(e)
        calc = klein_nishina_mass_coefficient(e, zoa)
        tab = mass_coefficient("water", e, "c")
        print("   %7.2f %18.4e %18.5f %11.5f %7.3f" % (e, kn, calc, tab, calc / tab))

    print("\n  Compton kinematics are material-independent  [Eq. (7.33)]")
    print("   source        E (MeV)   E'(180)   Compton edge   sum")
    for lab, e in [("241Am", 0.05954), ("99mTc", 0.14051), ("137Cs", 0.6617),
                   ("60Co", 1.3325), ("16N", 6.129)]:
        print("   %-12s %8.4f %9.4f %14.4f %7.4f"
              % (lab, e, backscatter_energy(e), compton_edge(e),
                 backscatter_energy(e) + compton_edge(e)))
    print("   -> backscatter tends to m_e c^2/2 = %.4f MeV however hard the source."
          % (M_E_C2_MEV / 2))

    print("\n  why high-Z shields are for x-rays, not gammas")
    print("   per gram, lead / water:")
    for e in (0.05, 0.1, 0.5, 1.0, 5.0):
        r_ph = (mass_coefficient("lead", e, "ph")
                / max(mass_coefficient("water", e, "ph"), 1e-30))
        r_tot = mass_coefficient("lead", e, "total") / mass_coefficient("water", e, "total")
        print("   %5.2f MeV   photoelectric x%9.1f    total x%6.2f" % (e, r_ph, r_tot))

    print("\n  interaction is not deposition:  f = mu_en/mu")
    print("   E (MeV)     water      lead")
    for e in (0.05, 0.1, 0.5, 1.0, 5.0, 10.0):
        print("   %7.2f %10.3f %9.3f"
              % (e, energy_transfer_fraction("water", e),
                 energy_transfer_fraction("lead", e)))
    print("   -> in water at 0.1 MeV only 15% of the interacting energy stays put;")
    print("      in lead at the same energy, 73%.  Same photon, different fate.")

    print("\n  pair production")
    print("   threshold (nuclear field)  %.4f MeV" % pair_production_threshold())
    print("   threshold (electron field) %.4f MeV" % triplet_production_threshold())
    for e in (1.5, 5.0, 10.0):
        print("   at %5.1f MeV the pair shares %6.3f MeV of kinetic energy"
              % (e, pair_kinetic_energy_shared(e)))
    print("   and the positron returns 2 x %.4f MeV on annihilation."
          % annihilation_photon_energy())


if __name__ == "__main__":
    _demo()
