"""NE-14  Charged-particle stopping: range, stopping power, the Bragg peak.

Nuclear Science & Engineering trunk, module NE-14 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 7.5 (printed pp. 205-217).  Pure stdlib; range constants are S&F
Tables 7.2 and 7.3, transcribed below.

~NE-11 through ~NE-13 dealt with NEUTRAL particles, and everything there followed
from one fact: a photon or neutron travels in straight segments past enormous
numbers of atoms and interacts a handful of times, so it is removed
probabilistically and attenuates EXPONENTIALLY, with no definite range.

Charged particles are the opposite in every respect, and the whole module follows
from that inversion:

  * They interact CONTINUOUSLY, with many electrons at once, via the long-range
    Coulomb force.  Thousands of interactions are needed to stop one.
  * Each interaction costs very little -- a 4 MeV alpha can lose at most 2.2 keV
    to one electron (~NE-08 Eq. 6.22), 0.05% of its energy.
  * So they slow down almost deterministically and stop at a definite RANGE.
    A beam of alphas is not attenuated at all until near the end of its range,
    where it drops abruptly -- the exact opposite of exp(-mu x).

Two consequences carry the rest of the trunk.  Stopping power rises as the
particle slows, so energy deposition PEAKS just before the particle stops -- the
BRAGG PEAK, which is why proton therapy can put a dose maximum inside a tumour
and nothing beyond it (~NE-27).  And because the deposition is dense and local,
charged particles are what actually does the biological damage that ~NE-17 and
~NE-18 quantify; photons and neutrons matter only through the charged particles
they set in motion.
"""

import math

__all__ = [
    "M_E_C2_MEV", "M_P_U", "M_ALPHA_U",
    "RANGE_CONSTANTS_PROTON", "RANGE_CONSTANTS_ALPHA", "RANGE_CONSTANTS_ELECTRON",
    "SUSPECT_RANGE_CONSTANTS", "EXAMPLE_7_7_B_DISCREPANCY",
    "FISSION_FRAGMENT_C", "RANGE_FORMULA_RANGE_MEV",
    "csda_mass_range", "csda_range", "range_energy_valid",
    "scaled_heavy_range", "equivalent_proton_energy",
    "radiative_to_collisional", "bremsstrahlung_crossover_energy",
    "fission_fragment_range",
    "energy_deposition_depth_fraction", "DEPOSITION_FRACTIONS",
]

M_E_C2_MEV = 0.51099891
M_P_U = 1.00727647
M_ALPHA_U = 4.00150618          # bare alpha (4He nucleus), not the neutral atom

# S&F Table 7.2 (printed p. 215): log10(rho R / g cm^-2) = a + b x + c x^2,
# x = log10(E / MeV).  Valid 0.1-10 MeV.
#
# THE LEAD ROW IS WITHHELD.  Table 7.2 prints (a, b, c) = (0.065607, 0.98751,
# 0.0047353) for protons in lead, which does not belong to the same family as
# any other proton row (all have a ~ -2.1 to -2.6, b ~ 1.38-1.51, c ~ 0.14-0.25).
# Evaluated at 4 MeV it gives 4.59 g/cm2 against 0.024-0.062 for the other ten
# materials -- 74x the largest, and about 70x the accepted PSTAR value of
# ~0.065 g/cm2.  Its b of 0.98751 is also within 1e-4 of the Pb ALPHA row's
# 0.98740, which suggests the proton row was contaminated during typesetting.
#
# Conjecture, offered as such: the printed "a" of 0.065607 is suspiciously close
# to the correct 4 MeV mass range of ~0.0656 g/cm2, so a range VALUE may have
# been set into the constant column.  Either way the row cannot be used, and
# guessing a replacement would be inventing data -- so `csda_mass_range` raises
# for this combination rather than returning a number.  Printed values are kept
# in SUSPECT_RANGE_CONSTANTS.
SUSPECT_RANGE_CONSTANTS = {
    ("proton", "Pb"): (0.065607, 0.98751, 0.0047353),
}

RANGE_CONSTANTS_PROTON = {
    "C":    (-2.5542, 1.4997, 0.22046),
    "Al":   (-2.4108, 1.4570, 0.19861),
    "Si":   (-2.4232, 1.4802, 0.17421),
    "Ar":   (-2.3756, 1.4944, 0.16909),
    "Ge":   (-2.2097, 1.4045, 0.17980),
    "Ag":   (-2.1440, 1.3815, 0.18943),
    "Xe":   (-2.1265, 1.4375, 0.13890),
    "air":  (-2.5510, 1.5066, 0.21732),
    "H2O":  (-2.6144, 1.4975, 0.23219),
    "LiF":  (-2.4883, 1.4501, 0.25453),
}

RANGE_CONSTANTS_ALPHA = {
    "C":    (-3.2132, 1.0080, 0.29815),
    "Al":   (-3.0581, 0.99132, 0.27018),
    "Si":   (-3.0813, 0.98208, 0.29625),
    "Ar":   (-3.0030, 0.93249, 0.32566),
    "Ge":   (-2.7867, 0.96529, 0.19442),
    "Ag":   (-2.7267, 0.95425, 0.21643),
    "Xe":   (-2.7556, 0.97004, 0.26094),
    "Pb":   (-2.5803, 0.98740, 0.19178),
    "air":  (-3.1854, 0.94174, 0.34192),
    "H2O":  (-3.2357, 0.93102, 0.33442),
    "LiF":  (-3.1240, 0.96343, 0.30053),
}

# S&F Table 7.3 (printed p. 216): same form, electrons, 0.1-10 MeV.
RANGE_CONSTANTS_ELECTRON = {
    "carbon":    (-0.30434, 1.2633, -0.21918),
    "aluminum":  (-0.25876, 1.2380, -0.22597),
    "silicon":   (-0.27136, 1.2360, -0.22740),
    "argon":     (-0.22887, 1.2209, -0.23682),
    "iron":      (-0.23199, 1.2165, -0.19504),
    "germanium": (-0.18537, 1.2069, -0.23702),
    "silver":    (-0.16377, 1.1903, -0.24781),
    "xenon":     (-0.14796, 1.1738, -0.25395),
    "gold":      (-0.13552, 1.1292, -0.20889),
    "lead":      (-0.10787, 1.1458, -0.25628),
    "air":       (-0.31149, 1.2419, -0.23063),
    "water":     (-0.36173, 1.2587, -0.21600),
    "tissue":    (-0.37829, 1.2803, -0.17374),   # striated muscle (ICRU)
    "bone":      (-0.33563, 1.2661, -0.17924),   # cortical bone (ICRP)
}

# S&F Eq. (7.48), printed p. 216: fission-fragment range, +-10%.
FISSION_FRAGMENT_C = {"air": 0.14, "aluminum": 0.19, "gold": 0.50}

# The empirical formula's stated validity window, MeV.
RANGE_FORMULA_RANGE_MEV = (0.1, 10.0)

# S&F Example 7.7 (printed p. 216) evaluates the proton range in WATER using
# b = 1.4501, but Table 7.2's H2O proton row gives b = 1.4975.  1.4501 is the
# LiF proton value from the row two lines below.  The table is the one that is
# right: it yields 7.202e-3 g/cm2 at 2 MeV against PSTAR's accepted 7.178e-3
# (0.3% high), while the example's b gives 6.969e-3 (2.9% low).  The example's
# final answer, 0.021 cm, is therefore ~3% low; this module's 0.0216 cm uses the
# table.  `test_example_7_7_uses_the_wrong_b` pins both.
EXAMPLE_7_7_B_DISCREPANCY = {"printed_in_example": 1.4501,
                             "table_7_2_H2O": 1.4975,
                             "same_as": "Table 7.2 LiF proton b"}

# S&F §7.5.4 (printed p. 213), from Cross, Freedman & Wong (1992): what fraction
# of a beam's energy is deposited within what fraction of the CSDA range.
DEPOSITION_FRACTIONS = {
    "beam":  {0.80: 0.60, 0.90: 0.70, 0.95: 0.80, 1.00: 1.10},
    "point": {0.90: 0.80, 0.95: 0.85, 1.00: 1.10},
}


def _tables(particle):
    return {"proton": RANGE_CONSTANTS_PROTON,
            "alpha": RANGE_CONSTANTS_ALPHA,
            "electron": RANGE_CONSTANTS_ELECTRON}[particle]


def range_energy_valid(e_mev):
    """True if e_mev lies inside Eq. (7.47)'s stated 0.1-10 MeV window."""
    lo, hi = RANGE_FORMULA_RANGE_MEV
    return lo <= e_mev <= hi


def csda_mass_range(particle, material, e_mev, strict=True):
    """CSDA range in MASS THICKNESS (g/cm2)  [S&F Eq. (7.47)]:

        log10(rho R) = a + b log10(E) + c [log10(E)]^2 .

    Mass thickness is the natural unit because it is INDEPENDENT OF DENSITY
    (rule 1 of §7.5.4): the same rho R stops a particle whether the material is
    compressed or a gas.  Divide by rho only at the end, to get a length.

    `strict` (default) refuses energies outside the tabulated 0.1-10 MeV window.
    The fit is a quadratic in log E with no physical content outside its range --
    extrapolating it produces confident nonsense, so this raises instead."""
    table = _tables(particle)
    if (particle, material) in SUSPECT_RANGE_CONSTANTS:
        raise ValueError(
            "S&F Table 7.2's %s/%s row is internally inconsistent with every "
            "other row and gives a range ~70x the accepted value; it is withheld "
            "rather than silently used. See SUSPECT_RANGE_CONSTANTS." 
            % (particle, material))
    if material not in table:
        raise KeyError("no %s range constants for %r; have %s"
                       % (particle, material, sorted(table)))
    if e_mev <= 0:
        raise ValueError("energy must be positive")
    if strict and not range_energy_valid(e_mev):
        raise ValueError("%.4g MeV is outside the %.1f-%.1f MeV window S&F state "
                         "for Eq. (7.47); pass strict=False to extrapolate anyway"
                         % (e_mev, *RANGE_FORMULA_RANGE_MEV))
    a, b, c = table[material]
    x = math.log10(e_mev)
    return 10.0 ** (a + b * x + c * x * x)


def csda_range(particle, material, e_mev, density_g_cm3, strict=True):
    """CSDA range as a LENGTH (cm) = mass range / density."""
    if density_g_cm3 <= 0:
        raise ValueError("density must be positive")
    return csda_mass_range(particle, material, e_mev, strict) / density_g_cm3


# --- scaling heavy-particle ranges  [S&F Eqs. (7.45)-(7.46), rules 1-3] ---

def equivalent_proton_energy(e_mev, mass_u):
    """Kinetic energy of a PROTON travelling at the same speed as a heavy
    particle of mass `mass_u` and energy e_mev:  E_p = E (m_p/m).

    Step 1 of S&F Example 7.7.  Ranges scale with SPEED, not energy, because the
    stopping power depends on v; so any comparison must be made at matched
    speed."""
    if mass_u <= 0 or e_mev <= 0:
        raise ValueError("mass and energy must be positive")
    return e_mev * M_P_U / mass_u


def scaled_heavy_range(rho_r_proton, mass_u, charge):
    """Mass-thickness range of a heavy particle from the proton range AT THE
    SAME SPEED  [S&F rule 2, from Eq. (7.46)]:

        rho R = rho R_p (m/m_p) (z_p/z)^2  =  rho R_p (m/m_p) / z^2 .

    The m/z^2 scaling comes straight out of Eq. (7.46): heavier particles carry
    more momentum per unit charge and so travel further, while more charge means
    stronger coupling and a shorter range.

    S&F warn the rules FAIL below about 1 MeV per atomic mass unit -- a 0.4 MeV
    alpha has about twice the range this predicts from a 0.1 MeV proton, because
    charge exchange with the medium changes the effective z."""
    if mass_u <= 0 or charge <= 0:
        raise ValueError("mass and charge must be positive")
    return rho_r_proton * (mass_u / M_P_U) / (charge * charge)


# --- bremsstrahlung  [S&F Eqs. (7.42)-(7.43)] ----------------------------

def radiative_to_collisional(e_mev, Z, mass_ratio_me_over_m=1.0):
    """Ratio of radiative to collisional stopping power  [Eq. (7.43)]:

        (dE/ds)_rad / (dE/ds)_coll ~ (E Z / 700) (m_e/M)^2 ,  E in MeV.

    The (m_e/M)^2 is why bremsstrahlung matters ONLY for electrons: a proton is
    1836x heavier, so its ratio is 3.4e6 times smaller, and S&F state flatly that
    'all other charged particles are far too massive to produce significant
    amounts of bremsstrahlung'.

    The linear Z is why it matters most in heavy materials -- and why a beta
    shield is made of PLASTIC, not lead (see `bremsstrahlung_crossover_energy`)."""
    if e_mev <= 0 or Z < 1:
        raise ValueError("energy must be positive and Z at least 1")
    return e_mev * Z / 700.0 * mass_ratio_me_over_m ** 2


def bremsstrahlung_crossover_energy(Z, mass_ratio_me_over_m=1.0):
    """Energy at which radiative loss equals collisional loss  [S&F Example 7.6]:

        E = 700 / Z  MeV   (for electrons).

    8.9 MeV in gold, 88 MeV in carbon.  Below the crossover, ionization
    dominates; above it, the particle mostly radiates."""
    if Z < 1:
        raise ValueError("Z must be at least 1")
    return 700.0 / Z / mass_ratio_me_over_m ** 2


# --- fission fragments  [S&F Eq. (7.48)] ---------------------------------

def fission_fragment_range(e_mev, material):
    """Fission-fragment range in mg/cm2  [Eq. (7.48)]:  rho R = C E^(2/3).

    Accurate to +-10%.  Fission fragments are the extreme case of everything in
    this module: charge ~20 (~NE-09), so the z^2 in the stopping power makes the
    range minute -- a few mg/cm2, i.e. microns of solid.  That is exactly why
    fission deposits its 168 MeV of fragment energy inside the fuel pellet
    (~NE-09) rather than in the coolant."""
    if material not in FISSION_FRAGMENT_C:
        raise KeyError("no Eq. (7.48) constant for %r; have %s"
                       % (material, sorted(FISSION_FRAGMENT_C)))
    if e_mev <= 0:
        raise ValueError("energy must be positive")
    return FISSION_FRAGMENT_C[material] * e_mev ** (2.0 / 3.0)


# --- where the energy actually goes  [S&F §7.5.4] ------------------------

def energy_deposition_depth_fraction(energy_fraction, geometry="beam"):
    """Fraction of the CSDA range within which a given fraction of the ENERGY is
    deposited  [S&F §7.5.4, from Cross, Freedman & Wong 1992].

    The numbers matter because the CSDA range is a PATH LENGTH along a twisting
    trajectory, not a depth.  An electron's path wanders so much that 90% of its
    energy lands within 70% of the range for a normally incident beam.  Quoting
    the CSDA range as a penetration depth overestimates shielding requirements --
    or, worse, underestimates dose if used the other way round."""
    table = DEPOSITION_FRACTIONS[geometry]
    if energy_fraction not in table:
        raise KeyError("no tabulated depth for %r of the energy in %s geometry; "
                       "have %s" % (energy_fraction, geometry, sorted(table)))
    return table[energy_fraction]


# --- demo --------------------------------------------------------------------

def _demo():
    print("NE-14  charged-particle stopping\n")

    print("  charged particles have a RANGE; neutral ones do not")
    print("   4 MeV alpha in water:   %.5f cm  = %.1f um"
          % (csda_range("alpha", "H2O", 4.0, 1.0),
             csda_range("alpha", "H2O", 4.0, 1.0) * 1e4))
    print("   4 MeV proton in water:  %.5f cm  = %.0f um"
          % (csda_range("proton", "H2O", 4.0, 1.0),
             csda_range("proton", "H2O", 4.0, 1.0) * 1e4))
    print("   1 MeV electron in water: %.4f cm = %.1f mm"
          % (csda_range("electron", "water", 1.0, 1.0),
             csda_range("electron", "water", 1.0, 1.0) * 10))
    print("   (a 1 MeV photon in water has a 14 cm mean free path and no range)")

    print("\n  the same particle, different stopping media  [mass thickness]")
    print("   material      4 MeV alpha    4 MeV proton   1 MeV electron  (g/cm2)")
    for m_a, m_e in (("H2O", "water"), ("Al", "aluminum"), ("air", "air"),
                     ("Pb", "lead"), ("C", "carbon")):
        try:
            p = "%14.5f" % csda_mass_range("proton", m_a, 4.0)
        except ValueError:
            p = "%14s" % "(withheld)"
        print("   %-12s %12.5f %s %14.5f"
              % (m_a, csda_mass_range("alpha", m_a, 4.0), p,
                 csda_mass_range("electron", m_e, 1.0)))
    print("   -> mass thickness barely varies: stopping is about electrons per gram.")

    print("\n  S&F Example 7.7: a 6 MeV triton in water, by scaling")
    ep = equivalent_proton_energy(6.0, 3.0160492)
    rp = csda_mass_range("proton", "H2O", ep)
    rt = scaled_heavy_range(rp, 3.0160492, 1)
    print("   proton of equal speed:  %.3f MeV" % ep)
    print("   its range:              %.5f g/cm2" % rp)
    print("   triton range = x m/z^2: %.5f g/cm2 = %.4f cm   (book: 0.021 cm)"
          % (rt, rt / 1.0))

    print("\n  S&F Example 7.6: where bremsstrahlung takes over")
    print("   material    Z     crossover energy (electrons)")
    for lab, Z in (("carbon", 6), ("aluminium", 13), ("iron", 26),
                   ("silver", 47), ("gold", 79), ("lead", 82)):
        print("   %-10s %3d %14.1f MeV" % (lab, Z, bremsstrahlung_crossover_energy(Z)))
    print("   at 1 MeV in lead, rad/coll = %.3f  -- 12%% of the loss is photons"
          % radiative_to_collisional(1.0, 82))
    print("   the same for a PROTON:      %.2e  -- utterly negligible"
          % radiative_to_collisional(1.0, 82, M_E_C2_MEV / (M_P_U * 931.494)))

    print("\n  fission fragments: the extreme case  [Eq. (7.48)]")
    print("   fragment                   air        aluminium      gold  (mg/cm2)")
    for e, lab in ((99.9, "light, 99.9 MeV"), (67.9, "heavy, 67.9 MeV")):
        print("   %-22s %10.2f %12.2f %10.2f"
              % (lab, fission_fragment_range(e, "air"),
                 fission_fragment_range(e, "aluminum"),
                 fission_fragment_range(e, "gold")))
    print("   in aluminium that is %.1f um -- fission energy never leaves the fuel."
          % (fission_fragment_range(99.9, "aluminum") * 1e-3 / 2.70 * 1e4))

    print("\n  range is a PATH LENGTH, not a depth  [§7.5.4]")
    print("   fraction of energy   within this fraction of the CSDA range")
    for f in (0.80, 0.90, 0.95, 1.00):
        try:
            print("   %14.0f%% %26.0f%%"
                  % (100 * f, 100 * energy_deposition_depth_fraction(f)))
        except KeyError:
            pass
    print("   -> electrons wander; 90% of the energy stops within 70% of the range.")


if __name__ == "__main__":
    _demo()
