"""NE-10  Fusion and nucleosynthesis: the barrier, the Gamow peak, and stars.

Nuclear Science & Engineering trunk, module NE-10 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 6.7 (printed pp. 163-173).  Pure stdlib; masses from
../../data_tables/B1_atomic_masses.csv.

~NE-09 harvested the right-hand side of the binding-energy curve of ~NE-03 by
splitting heavy nuclei.  This module harvests the left-hand side, which is
steeper: D-T releases 17.6 MeV from 5 nucleons (3.5 MeV each) against fission's
200 MeV from 236 (0.85 MeV each).  Per unit mass, fusion wins by a factor of four.

The catch is entirely the Coulomb barrier of ~NE-08.  It is only a few hundred
keV -- trivial compared with fission's 200 MeV payoff -- but it must be paid by
EVERY reacting pair, and the only way to pay it at scale is thermally.  Three
facts then follow, and they are the whole subject:

  1. kT of a few hundred keV means 1e9 K, which no material confines.
  2. Fusion happens far below that anyway, because the reactants TUNNEL.  The
     product of a falling Maxwellian tail and a rising tunnelling probability is
     sharply peaked at the GAMOW ENERGY E_0, tens of keV rather than hundreds --
     which is why the sun burns at 15 MK and why tokamaks aim at 10-20 keV.
  3. Even so, the sun's proton-proton bottleneck is weak-force-mediated and
     absurdly slow: one proton in 1e18 fuses per second, giving a proton lifetime
     of 3e10 y.  A star is a bad reactor and a superb one -- bad power density,
     perfect confinement, and ten billion years of fuel.

Nucleosynthesis is the same physics run to exhaustion: fusion builds nuclides up
to the iron peak and stops, and everything heavier is made by neutron capture in
the s- and r-processes (~NE-02, ~NE-05).
"""

import csv
import math
import os

__all__ = [
    "M_N_U", "M_H_U", "M_E_U", "U_MEV", "TWO_ME_MEV", "ALPHA_FS",
    "K_BOLTZ_MEV_PER_K", "AVOGADRO", "MEV_PER_J", "C_M_PER_S",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "q_value", "q_value_beta_plus",
    "FUSION_REACTIONS", "PP_CHAIN", "CNO_CYCLE", "HELIUM_BURNING",
    "ADVANCED_BURNING", "TRITIUM_BREEDING", "SUN",
    "BOOK_Q_ERRATA", "SUN_ERRATA", "PP_MULTIPLICITY", "core_power_density",
    "temperature_for_energy", "thermal_energy", "mean_thermal_energy",
    "gamow_energy", "gamow_peak_energy", "gamow_peak_width",
    "tunnelling_probability", "barrier_temperature",
    "reaction_product_energies",
    "pp_chain_energy", "energy_per_deuteron",
    "mass_to_energy", "solar_mass_loss_rate", "solar_helium_rate",
    "radiant_flux", "deuterium_atoms", "fusion_energy_of_water",
]

M_N_U = 1.0086649156
M_H_U = 1.0078250321
M_E_U = 5.4857990945e-4
U_MEV = 931.494043
TWO_ME_MEV = 2.0 * M_E_U * U_MEV            # 1.022 MeV -- the beta+ correction
ALPHA_FS = 1.0 / 137.035999                 # fine-structure constant
K_BOLTZ_MEV_PER_K = 8.617343e-11            # MeV per kelvin
AVOGADRO = 6.0221415e23
MEV_PER_J = 1.0 / 1.602176487e-13
C_M_PER_S = 2.99792458e8

# --- S&F §6.7 (printed p. 163): candidate fusion reactions -----------------
# label -> (reactants, products, book_Q_MeV) with nuclides as (A, Z)
#
# ONE BOOK Q-VALUE IS CORRECTED.  Every entry is recomputed from Appendix B
# masses by `test_book_q_values`; 6 of the 7 agree to better than 3 keV.  The
# seventh, p + 11B -> 3 alpha, is printed as 8.08 MeV but the book's own masses
# give 8.68 MeV, which is also the accepted value quoted throughout the
# aneutronic-fusion literature.  Looks like a 6 -> 0 typo.  Corrected here; the
# printed value is kept in BOOK_Q_ERRATA.
BOOK_Q_ERRATA = {"p+11B->3alpha": (8.08, 8.68)}

FUSION_REACTIONS = {
    "D+D->T+p":       ([(2, 1), (2, 1)], [(3, 1), (1, 1)], 4.03),
    "D+D->3He+n":     ([(2, 1), (2, 1)], [(3, 2), (1, 0)], 3.27),
    "D+T->4He+n":     ([(2, 1), (3, 1)], [(4, 2), (1, 0)], 17.59),
    "D+3He->4He+p":   ([(2, 1), (3, 2)], [(4, 2), (1, 1)], 18.35),
    "T+T->4He+2n":    ([(3, 1), (3, 1)], [(4, 2), (1, 0), (1, 0)], 11.33),
    "p+6Li->4He+3He": ([(1, 1), (6, 3)], [(4, 2), (3, 2)], 4.02),
    "p+11B->3alpha":  ([(1, 1), (11, 5)], [(4, 2), (4, 2), (4, 2)], 8.68),
}

# S&F p. 164: breeding the tritium that D-T fusion consumes
TRITIUM_BREEDING = {
    "n+6Li->4He+T":   ([(1, 0), (6, 3)], [(4, 2), (3, 1)], 4.78),
    "n+7Li->4He+T+n": ([(1, 0), (7, 3)], [(4, 2), (3, 1), (1, 0)], -2.5),
}

# S&F §6.7.2 (printed pp. 166-167): the proton-proton chain.
# Each step as (reactants, products, book_Q_MeV, n_positrons).
PP_CHAIN = [
    ("p+p->D",       [(1, 1), (1, 1)], [(2, 1)], 0.42, 1),
    ("D+p->3He",     [(2, 1), (1, 1)], [(3, 2)], 5.49, 0),
    ("3He+3He->4He", [(3, 2), (3, 2)], [(4, 2), (1, 1), (1, 1)], 12.86, 0),
]
# multiplicity of each step per 4He produced
PP_MULTIPLICITY = (2, 2, 1)

# S&F p. 167: the CNO cycle, catalysed by 12C.  Net effect identical to pp.
CNO_CYCLE = [
    ("p+12C->13N",     [(1, 1), (12, 6)], [(13, 7)], 0),
    ("13N->13C+b+",    [(13, 7)], [(13, 6)], 1),
    ("p+13C->14N",     [(1, 1), (13, 6)], [(14, 7)], 0),
    ("p+14N->15O",     [(1, 1), (14, 7)], [(15, 8)], 0),
    ("15O->15N+b+",    [(15, 8)], [(15, 7)], 1),
    ("p+15N->12C+4He", [(1, 1), (15, 7)], [(12, 6), (4, 2)], 0),
]

# S&F p. 168: helium burning, starting with the triple-alpha process
HELIUM_BURNING = {
    "3alpha->12C":     ([(4, 2), (4, 2), (4, 2)], [(12, 6)], 7.27),
    "4He+12C->16O":    ([(4, 2), (12, 6)], [(16, 8)], 7.16),
    "4He+16O->20Ne":   ([(4, 2), (16, 8)], [(20, 10)], 4.73),
    "4He+20Ne->24Mg":  ([(4, 2), (20, 10)], [(24, 12)], 9.31),
}

# S&F p. 169: carbon and oxygen burning in massive stars
ADVANCED_BURNING = {
    "12C+12C->20Ne+a": ([(12, 6), (12, 6)], [(20, 10), (4, 2)], 4.62),
    "12C+12C->23Na+p": ([(12, 6), (12, 6)], [(23, 11), (1, 1)], 2.24),
    "16O+16O->28Si+a": ([(16, 8), (16, 8)], [(28, 14), (4, 2)], 9.59),
    "16O+16O->31P+p":  ([(16, 8), (16, 8)], [(31, 15), (1, 1)], 7.68),
}

# S&F §§6.7.1-6.7.2: solar parameters as quoted.
#
# ONE VALUE IS CORRECTED.  S&F write that the sun's energy-producing core "is
# about 7,000 km in radius or about 0.1% of the sun's total volume".  Those two
# statements are inconsistent by a factor of 1000 in volume: with the solar
# radius of 696 000 km, 0.1% of the volume needs a radius of
# 696 000 x 0.001^(1/3) = 69 600 km, and 7 000 km would be 0.0001% of it.  The
# volume fraction is the self-consistent one -- it gives a core power density of
# 284 W/m^3, the familiar figure -- so the radius is taken as 7.0e4 km.
# `test_the_solar_core_radius_erratum` pins both halves.
SUN_ERRATA = {"core_radius_km": (7.0e3, 7.0e4)}

SUN = {
    "power_w": 4.0e26,
    "mass_kg": 2.0e30,
    "radius_km": 6.96e5,
    "core_temperature_k": 1.5e7,
    "core_radius_km": 7.0e4,            # corrected, see SUN_ERRATA
    "core_volume_fraction": 1.0e-3,
    "core_pressure_pa": 4.0e16,
    "proton_density_per_cm3": 1.0e26,
    "pp_rate_per_cm3_s": 1.0e8,
    "earth_distance_m": 1.5e11,
    "lifetime_y": 1.0e10,
}

_MASSES = None


def _csv_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "data_tables", "B1_atomic_masses.csv"))


def load_atomic_masses(path=None):
    """{(Z, A): atomic_mass_u} from the extracted Appendix B.  Cached."""
    global _MASSES
    if _MASSES is not None and path is None:
        return _MASSES
    table = {}
    with open(path or _csv_path(), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[(int(row["Z"]), int(row["A"]))] = float(row["atomic_mass_u"])
    if path is None:
        _MASSES = table
    return table


def atomic_mass(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    if (int(Z), int(A)) == (0, 1):
        return M_N_U
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


# --- Q-values  [S&F §6.7, using the conventions of ~NE-04 and ~NE-05] ------

def q_value(reactants, products, table=None, n_positrons=0):
    """Q in MeV from neutral-atom masses, with the beta+ correction of ~NE-05.

    Nuclides are (A, Z) pairs.  For each positron emitted, subtract 2 m_e c^2 =
    1.022 MeV: neutral-atom masses carry the electrons along, and a beta+ decay
    both creates a positron and leaves the daughter atom with a surplus electron.

    Getting this wrong is the single easiest error in stellar fusion, because the
    hydrogen-burning chains are full of beta+ steps.  `p + p -> D + beta+ + nu`
    comes out at 1.442 MeV without the correction and 0.420 MeV with it -- and
    0.42 MeV is the value S&F quote."""
    t = load_atomic_masses() if table is None else table
    lhs = sum(atomic_mass(A, Z, t) for A, Z in reactants)
    rhs = sum(atomic_mass(A, Z, t) for A, Z in products)
    return (lhs - rhs) * U_MEV - n_positrons * TWO_ME_MEV


def q_value_beta_plus(reactants, products, n_positrons, table=None):
    """Explicit alias for the beta+-corrected Q-value; see `q_value`."""
    return q_value(reactants, products, table, n_positrons)


# --- thermonuclear temperatures  [S&F §6.7.1, printed p. 163] -------------

def thermal_energy(temperature_k):
    """kT in MeV."""
    if temperature_k < 0:
        raise ValueError("temperature must be non-negative")
    return K_BOLTZ_MEV_PER_K * temperature_k


def mean_thermal_energy(temperature_k):
    """Mean kinetic energy of a Maxwellian particle, E_av = 3kT/2  [S&F p. 163]."""
    return 1.5 * thermal_energy(temperature_k)


def temperature_for_energy(e_mev, mean=False):
    """Temperature at which kT (or 3kT/2 if mean=True) equals e_mev."""
    if e_mev <= 0:
        raise ValueError("energy must be positive")
    return e_mev / K_BOLTZ_MEV_PER_K / (1.5 if mean else 1.0)


def barrier_temperature(Z1, A1, Z2, A2, r0_fm=1.2):
    """Temperature at which the MEAN thermal energy equals the Coulomb barrier
    of ~NE-08 -- the naive, classical answer to 'how hot must a plasma be?'.

    It comes out at 1e9-1e10 K, far above any star's core or any tokamak.  That
    it is wrong by two orders of magnitude is the entire point of the Gamow peak
    below: fusion proceeds by tunnelling, not by climbing."""
    vc = 1.43996 * Z1 * Z2 / (r0_fm * (A1 ** (1 / 3.0) + A2 ** (1 / 3.0)))
    return temperature_for_energy(vc, mean=True)


# --- the Gamow peak  [beyond S&F; see Clayton or Krane, refs.md] ----------

def gamow_energy(Z1, A1, Z2, A2):
    """Gamow energy E_G = 2 mu c^2 (pi alpha Z1 Z2)^2, in MeV.

    Sets the tunnelling probability through the Coulomb barrier,
    P ~ exp(-sqrt(E_G/E)).  Note the (Z1 Z2)^2: charge is punished quadratically
    inside a square root inside an exponential, which is why fusion fuels are
    chosen from the very bottom of the periodic table and why p-11B, with
    E_G = 22 MeV against D-T's 1.2 MeV, is so much harder despite a comparable
    Q-value."""
    if min(A1, A2) <= 0 or min(Z1, Z2) < 1:
        raise ValueError("both reactants must be charged nuclei")
    mu_u = A1 * A2 / float(A1 + A2)
    return 2.0 * mu_u * U_MEV * (math.pi * ALPHA_FS * Z1 * Z2) ** 2


def tunnelling_probability(e_mev, Z1, A1, Z2, A2):
    """Gamow factor exp(-sqrt(E_G/E)): the probability of penetrating the
    barrier at centre-of-mass energy E."""
    if e_mev <= 0:
        raise ValueError("energy must be positive")
    return math.exp(-math.sqrt(gamow_energy(Z1, A1, Z2, A2) / e_mev))


def gamow_peak_energy(temperature_k, Z1, A1, Z2, A2):
    """Gamow peak energy E_0 = [E_G (kT)^2 / 4]^(1/3), in MeV.

    Fusion in a thermal plasma happens neither at kT (too little tunnelling) nor
    at the barrier (too few particles) but at the maximum of the product of the
    two -- the Maxwellian's falling tail against the rising Gamow factor.  For
    D-T at kT = 10 keV, E_0 = 31 keV: three times the mean energy, but a hundred
    times below the classical barrier.  This is why fusion is possible at all at
    achievable temperatures."""
    kt = thermal_energy(temperature_k)
    if kt <= 0:
        raise ValueError("temperature must be positive")
    return (gamow_energy(Z1, A1, Z2, A2) * kt * kt / 4.0) ** (1.0 / 3.0)


def gamow_peak_width(temperature_k, Z1, A1, Z2, A2):
    """FWHM-like width of the Gamow peak, Delta = (4/sqrt(3)) sqrt(E_0 kT)."""
    e0 = gamow_peak_energy(temperature_k, Z1, A1, Z2, A2)
    return 4.0 / math.sqrt(3.0) * math.sqrt(e0 * thermal_energy(temperature_k))


# --- product energies and chain totals -------------------------------------

def reaction_product_energies(q_mev, m1, m2):
    """(E_1, E_2) for a two-product reaction from rest, sharing Q by inverse
    mass -- the same momentum argument as ~NE-09's fission fragments.

    For D-T this puts 3.5 MeV on the alpha and 14.1 MeV on the neutron: the alpha
    stays in the plasma and heats it (the basis of ignition, ~NE-24) while the
    neutron escapes to the blanket, where it must both carry the useful heat and
    breed the tritium."""
    if m1 <= 0 or m2 <= 0:
        raise ValueError("masses must be positive")
    return q_mev * m2 / (m1 + m2), q_mev * m1 / (m1 + m2)


def pp_chain_energy(table=None, include_annihilation=True):
    """Total energy per 4He from the proton-proton chain  [S&F Eq. (6.47)].

    Two conventions, both defensible, differing by 4 m_e c^2 = 2.044 MeV:

      nuclear only          24.69 MeV  -- the sum of the three steps' Q-values
      + positron annihilation  26.73 MeV  -- what S&F quote as 26.72 MeV

    In a star the two positrons annihilate with ambient electrons immediately, so
    the larger figure is the one that heats the sun.  About 0.6 MeV of it then
    leaves as neutrinos and is not thermalised."""
    t = load_atomic_masses() if table is None else table
    total = 0.0
    for (label, reac, prod, q_book, npos), mult in zip(PP_CHAIN, PP_MULTIPLICITY):
        total += mult * q_value(reac, prod, t, npos)
    if include_annihilation:
        total += 4.0 * M_E_U * U_MEV        # two positrons, each annihilating
    return total


def energy_per_deuteron(table=None):
    """Energy per deuteron when deuterium is burned all the way to 4He
    [S&F Example 6.6]:  D + D -> 4He releases 23.85 MeV, so 11.9 MeV each.

    Both d-d branches, followed by the secondary reactions, sum to the same
    result -- which they must, since only the endpoints matter."""
    t = load_atomic_masses() if table is None else table
    return q_value([(2, 1), (2, 1)], [(4, 2)], t) / 2.0


# --- stars and scale  [S&F §§6.7.1-6.7.2] ---------------------------------

def mass_to_energy(mass_kg):
    """E = mc^2 in joules."""
    return mass_kg * C_M_PER_S ** 2


def solar_mass_loss_rate(power_w=None):
    """Kilograms per second converted to energy, P/c^2  [S&F Ch. 6 Prob. 23].

    4.4e9 kg/s sounds catastrophic and is not: over 4.6 billion years it is 0.03%
    of the sun's mass.  (The sun loses far more mass to the solar wind.)"""
    p = SUN["power_w"] if power_w is None else power_w
    return p / C_M_PER_S ** 2


def solar_helium_rate(power_w=None, mev_per_helium=None, table=None):
    """4He nuclei produced per second, P / (energy per 4He)."""
    p = SUN["power_w"] if power_w is None else power_w
    e = pp_chain_energy(table) if mev_per_helium is None else mev_per_helium
    return p * MEV_PER_J / e


def core_power_density(power_w=None, volume_fraction=None):
    """Power per cubic metre in the sun's energy-producing core, W/m^3.

    Comes out at 284 W/m^3 -- less than a compost heap, and about the same as a
    reptile.  The sun is luminous because it is enormous, not because its core is
    intense.  A tokamak aiming at commercial power must beat this by four or five
    orders of magnitude (~NE-24), which is why gravitational confinement is no
    guide to how hard the engineering is."""
    p = SUN["power_w"] if power_w is None else power_w
    f = SUN["core_volume_fraction"] if volume_fraction is None else volume_fraction
    v_sun = 4.0 / 3.0 * math.pi * (SUN["radius_km"] * 1e3) ** 3
    return p / (f * v_sun)


def radiant_flux(power_w=None, distance_m=None):
    """Inverse-square flux, P/(4 pi r^2), in W/m^2  [S&F Ch. 6 Prob. 23]."""
    p = SUN["power_w"] if power_w is None else power_w
    r = SUN["earth_distance_m"] if distance_m is None else distance_m
    if r <= 0:
        raise ValueError("distance must be positive")
    return p / (4.0 * math.pi * r * r)


def deuterium_atoms(water_g, deuterium_fraction=1.5e-4):
    """Deuterium atoms in a mass of water, at S&F's quoted 0.015% of hydrogen."""
    if water_g < 0:
        raise ValueError("mass must be non-negative")
    hydrogen = water_g / 18.0153 * 2.0 * AVOGADRO
    return hydrogen * deuterium_fraction


def fusion_energy_of_water(water_g, deuterium_fraction=1.5e-4, table=None):
    """Joules available by burning all the deuterium in a mass of water
    [S&F Ch. 6 Prob. 22]."""
    n = deuterium_atoms(water_g, deuterium_fraction)
    return n * energy_per_deuteron(table) / MEV_PER_J


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-10  fusion and nucleosynthesis\n")

    print("  candidate fusion reactions  [S&F p. 163]")
    print("   reaction              Q computed   Q printed   E_G (MeV)  E_0 at 10 keV")
    charges = {"D+D->T+p": (1, 2, 1, 2), "D+D->3He+n": (1, 2, 1, 2),
               "D+T->4He+n": (1, 2, 1, 3), "D+3He->4He+p": (1, 2, 2, 3),
               "T+T->4He+2n": (1, 3, 1, 3), "p+6Li->4He+3He": (1, 1, 3, 6),
               "p+11B->3alpha": (1, 1, 5, 11)}
    for lab, (reac, prod, qb) in FUSION_REACTIONS.items():
        z1, a1, z2, a2 = charges[lab]
        eg = gamow_energy(z1, a1, z2, a2)
        e0 = gamow_peak_energy(temperature_for_energy(0.010), z1, a1, z2, a2)
        note = "  <- corrected" if lab in BOOK_Q_ERRATA else ""
        print("   %-20s %9.3f %11.2f %11.3f %10.1f keV%s"
              % (lab, q_value(reac, prod, t), qb, eg, e0 * 1e3, note))

    print("\n  why tunnelling is not optional")
    print("   fuel      classical barrier T      Gamow peak at 10 keV plasma")
    for lab, (z1, a1, z2, a2) in [("D-T", (1, 2, 1, 3)), ("D-D", (1, 2, 1, 2)),
                                  ("p-11B", (1, 1, 5, 11))]:
        tb = barrier_temperature(z1, a1, z2, a2)
        e0 = gamow_peak_energy(temperature_for_energy(0.010), z1, a1, z2, a2)
        print("   %-8s %12.2e K %20.1f keV" % (lab, tb, e0 * 1e3))
    print("   the sun's core is 1.5e7 K -- a thousand times below the barrier.")

    print("\n  D-T, the reaction every experiment uses  [Eq. (6.46)]")
    q = q_value([(2, 1), (3, 1)], [(4, 2), (1, 0)], t)
    ea, en = reaction_product_energies(q, atomic_mass(4, 2, t), M_N_U)
    print("   Q = %.3f MeV  ->  alpha %.2f MeV (stays, heats the plasma)" % (q, ea))
    print("                      neutron %.2f MeV (leaves, breeds and heats)" % en)
    for lab, (reac, prod, qb) in TRITIUM_BREEDING.items():
        print("   breeding: %-18s Q = %+7.3f MeV" % (lab, q_value(reac, prod, t)))

    print("\n  the proton-proton chain  [Eqs. (6.47)]")
    for (lab, reac, prod, qb, npos), mult in zip(PP_CHAIN, PP_MULTIPLICITY):
        print("   %-16s x%d   Q = %7.3f MeV  (book %.2f)%s"
              % (lab, mult, q_value(reac, prod, t, npos), qb,
                 "   [beta+ corrected]" if npos else ""))
    print("   nuclear total                %7.3f MeV" % pp_chain_energy(t, False))
    print("   + 2 positron annihilations   %7.3f MeV  (book 26.72)"
          % pp_chain_energy(t, True))

    print("\n  the CNO cycle: a catalytic loop with the same net effect")
    tot = sum(q_value(r, p, t, n) for _, r, p, n in CNO_CYCLE)
    print("   sum of the six steps         %7.3f MeV" % tot)
    print("   + 2 positron annihilations   %7.3f MeV" % (tot + 4 * M_E_U * U_MEV))
    print("   12C in, 12C out -- a catalyst, not a fuel.")

    print("\n  building the elements")
    for name, tab in [("helium burning", HELIUM_BURNING),
                      ("carbon/oxygen burning", ADVANCED_BURNING)]:
        print("   %s:" % name)
        for lab, (reac, prod, qb) in tab.items():
            print("     %-20s Q = %6.3f MeV  (book %.2f)"
                  % (lab, q_value(reac, prod, t), qb))

    print("\n  the sun, by the numbers")
    print("   power                  %.1e W" % SUN["power_w"])
    print("   mass -> energy         %.2e kg/s" % solar_mass_loss_rate())
    print("     over 4.6 Gy that is  %.3f%% of the sun's mass"
          % (100 * solar_mass_loss_rate() * 4.6e9 * 3.15576e7 / SUN["mass_kg"]))
    print("   4He produced           %.2e per second" % solar_helium_rate(table=t))
    print("   flux at earth          %.0f W/m2" % radiant_flux())
    print("   proton lifetime in core %.1e y"
          % (SUN["proton_density_per_cm3"] / SUN["pp_rate_per_cm3_s"] / 3.15576e7))
    print("   core power density     %.0f W/m3  (a compost heap beats it)"
          % core_power_density())

    print("\n  the scale of the fuel supply")
    print("   energy per deuteron    %.2f MeV" % energy_per_deuteron(t))
    print("   an 8 oz glass of water %.2e J  = %.1f days of a 10 kW house"
          % (fusion_energy_of_water(236.6, table=t),
             fusion_energy_of_water(236.6, table=t) / 1e4 / 86400))
    print("   the oceans (1.4e43 D)  %.2e J" % (1.4e43 * energy_per_deuteron(t) / MEV_PER_J))


if __name__ == "__main__":
    _demo()
