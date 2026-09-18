"""
equations.py  —  Module 12.EQ (Topic 12: canonical equation registry,
                 Combustion & Reacting Mixtures)

The key equations of Topic 12 in canonical Moran 8e form, one per function:

(A) COMBUSTION trunk (Moran Ch.13; concept module 12.1)
  * theoretical O2 / air    a_O2 = C + H/4 + S - O/2 ; AF_bar = 4.76 a_O2  (Sec. 13.1.2)
  * air-fuel ratio          AF = AF_bar (M_air/M_fuel)                     (Eq. 13.2)
  * % theoretical / % excess air / equivalence ratio                      (Sec. 13.1.2)
  * products dew point      p_v = y_v p                                    (Sec. 13.1.3)
  * enthalpy                h = h_f0 + dh                                  (Eq. 13.9)
  * steady-flow balance     (Qcv-Wcv)/nF = SUM_P n(h_f0+dh) - SUM_R n(h_f0+dh)
                                                                 (Eqs. 13.12b/13.15b)
  * closed rigid vessel     Q - W = SUM_P n h - SUM_R n h - R TP nP + R TR nR
                                                                 (Eq. 13.17b)
  * enthalpy of combustion  h_RP = SUM_P n h - SUM_R n h; HHV/LHV = |h_RP| (Eq. 13.18)
  * adiabatic flame balance SUM_P n (dh) = SUM_R n h_f0 - SUM_P n h_f0    (Eq. 13.21b)

(B) EQUILIBRIUM trunk (Moran Ch.14; concept module 12.2)
  * chemical potential      mu = g0 + R T ln(y p/pref)                     (Eq. 14.17)
  * reaction equilibrium    nuA muA + nuB muB = nuC muC + nuD muD          (Eq. 14.26)
  * Gibbs of reaction       dG0 = SUM_P nu(h - T s0) - SUM_R nu(h - T s0)  (Eq. 14.29b)
  * ln K = -dG0/(R T);  K = PROD y^nu (p/pref)^dnu;  log10K* = -log10K
                                                        (Eqs. 14.31 / 14.32 / 14.34)
  * K in moles              K = PROD n^nu ((p/pref)/n)^dnu                 (Eq. 14.35)
  * ionization equilibrium  A <-> A+ + e-:  K = [z^2/(1-z^2)](p/pref)
                                            (Sec. 14.4.3, Eq. 14.45 / Ex. 14.8)

(C) PLASMA extension  *** [~PK, NOT Moran] ***
  * the SAHA equation supplies the ionization-equilibrium constant that Moran
    Sec. 14.4.3 says "can be calculated ... by using the procedures of statistical
    thermodynamics" but does not give:
        n_+ n_e / n_0 = 2 (g_+/g_0) n_Q(T) exp(-chi/kB T),  n_Q = (2 pi m_e kB T/h^2)^1.5
    and, converted to Moran's dimensionless form (ideal-gas p = n_tot kB T),
        K(T) = S(T) kB T / p_ref            with  S = the Saha right-hand side.
    Sources: Saha 1920; Chen; Rybicki & Lightman Sec. 9.5; Carroll & Ostlie Sec. 8.1.

test_equations.py checks every equation against a book-verified value, then CROSS-CHECKS:
it sys.path-imports the concept modules 12.1 (fuels.py) and 12.2 (ionization.py) and the
worked-examples module 12.EP (examples.py), asserting identical results, so a formula
change anywhere in the topic fails this suite.

Units: enthalpies/Gibbs kJ/kmol; s0 kJ/kmol.K; R_BAR = 8.314 kJ/kmol.K; Saha part SI.
Citations: Moran 8e (PDF = printed + 18; ../refs.md); part (C) is ~PK, NOT Moran.
"""
import math

M_AIR = 28.97               # kg/kmol (Moran Sec. 13.1.2, p.808)
N2_PER_O2 = 3.76            # mol N2 accompanying each mol O2 (Sec. 13.1.2, p.807)
AIR_PER_O2 = 4.76           # mol air per mol O2
R_BAR = 8.314               # kJ/kmol.K
# --- SI constants for the Saha extension (CODATA), as in module 12.2 ---
M_E = 9.1093837015e-31      # kg
K_B = 1.380649e-23          # J/K
H_PLANCK = 6.62607015e-34   # J.s
EV = 1.602176634e-19        # J
P_REF_PA = 101325.0         # 1 atm in Pa (pref of Moran's K)


# ============================================================================
# (A)  COMBUSTION trunk (Moran Ch.13; concept module 12.1)
# ============================================================================
def theoretical_O2(nC, nH, nO=0.0, nS=0.0):
    """a_O2 = C + H/4 + S - O/2, theoretical (stoichiometric) O2 per mole of fuel.
    [from Eqs. 13.3-13.4, Sec. 13.1.2, p.808]"""
    return nC + nH / 4.0 + nS - nO / 2.0


def theoretical_air_molar(nC, nH, nO=0.0, nS=0.0):
    """AF_bar_theo = 4.76 a_O2, theoretical air per mole of fuel (molar).
    [Sec. 13.1.2, Eq. 13.4 (methane: 9.52), p.808]"""
    return AIR_PER_O2 * theoretical_O2(nC, nH, nO, nS)


def air_fuel_mass_from_molar(afr_molar, M_fuel, M_air=M_AIR):
    """AF = AF_bar (M_air/M_fuel). [Eq. 13.2, Sec. 13.1.2, p.808]"""
    return afr_molar * (M_air / M_fuel)


def percent_theoretical_air(afr_actual, afr_theoretical):
    """% theoretical air = AF/AF_theo (1.13 = 113%). [Sec. 13.1.2, p.808]"""
    return afr_actual / afr_theoretical


def percent_excess_air(afr_actual, afr_theoretical):
    """% excess air = (AF - AF_theo)/AF_theo (150% theo = 50% excess).
    [Sec. 13.1.2, p.808]"""
    return (afr_actual - afr_theoretical) / afr_theoretical


def equivalence_ratio(afr_actual, afr_theoretical):
    """phi = (F/A)_act/(F/A)_theo = AF_theo/AF_act; <1 lean, >1 rich.
    [Sec. 13.1.2, p.809]"""
    return afr_theoretical / afr_actual


def dew_point_partial_pressure(y_vapor, p_mixture):
    """p_v = y_v p; the dew point of the products is T_sat(p_v).
    [Sec. 13.1.3, Ex. 13.2(c), p.812]"""
    return y_vapor * p_mixture


def enthalpy_formation_plus_dh(h_f0, dh=0.0):
    """h(T, p) = h_f0 + [h(T) - h(Tref)] = h_f0 + dh. [Eq. 13.9, Sec. 13.2.1, p.817]"""
    return h_f0 + dh


def stream_enthalpy(terms):
    """SUM_i n_i (h_f0 + dh)_i for a reactant or product stream; terms = [(n, h_f0, dh)].
    [Eq. 13.15b sums, Sec. 13.2.2, p.819]"""
    return sum(n * enthalpy_formation_plus_dh(h_f0, dh) for (n, h_f0, dh) in terms)


def energy_balance_steady(products, reactants):
    """(Qcv - Wcv)/nF = hP - hR = SUM_P n(h_f0+dh) - SUM_R n(h_f0+dh), per mole fuel.
    [Eqs. 13.12b/13.15b, Sec. 13.2.2, p.818-819]"""
    return stream_enthalpy(products) - stream_enthalpy(reactants)


def energy_balance_closed(products, reactants, T_products, T_reactants):
    """Closed rigid system (u = h - R T):
    Q - W = SUM_P n(h_f0+dh) - SUM_R n(h_f0+dh) - R TP SUM_P n + R TR SUM_R n.
    [Eq. 13.17b, Sec. 13.2.2, p.823]"""
    nP = sum(n for (n, _, _) in products)
    nR = sum(n for (n, _, _) in reactants)
    return (stream_enthalpy(products) - stream_enthalpy(reactants)
            - R_BAR * T_products * nP + R_BAR * T_reactants * nR)


def enthalpy_of_combustion(products, reactants):
    """h_RP = SUM_P n_e h_e - SUM_R n_i h_i (complete combustion, same T, p).
    [Eq. 13.18, Sec. 13.2.3, p.825]"""
    return stream_enthalpy(products) - stream_enthalpy(reactants)


def heating_value_molar(h_RP):
    """Heating value = |h_RP|: HHV with liquid product water, LHV with vapor.
    [Sec. 13.2.3, p.825]"""
    return abs(h_RP)


def heating_value_mass(h_RP, M_fuel):
    """Heating value per unit mass of fuel = |h_RP|/M_fuel. [Sec. 13.2.3, p.826]"""
    return abs(h_RP) / M_fuel


def adiabatic_flame_rhs(reactants_hf, products_hf):
    """RHS of the table-data adiabatic-flame balance (reactants entering at Tref):
    SUM_P n_e (dh)_e = SUM_R n_i h_f0,i - SUM_P n_e h_f0,e.
    reactants_hf / products_hf = [(n, h_f0)].  [Eq. 13.21b, Sec. 13.3.1, p.829]"""
    return (sum(n * hf for (n, hf) in reactants_hf)
            - sum(n * hf for (n, hf) in products_hf))


def interpolate_flame_temperature(rhs, table):
    """Adiabatic flame temperature by linear interpolation of SUM_P n(dh)_e(T) between
    the two bracketing trial temperatures; table = {T: SUM_P n(dh)_e}.
    [Ex. 13.8 iteration procedure, Sec. 13.3.1, p.829-831]"""
    Ts = sorted(table)
    for Tlo, Thi in zip(Ts, Ts[1:]):
        if table[Tlo] <= rhs <= table[Thi]:
            return Tlo + (Thi - Tlo) * (rhs - table[Tlo]) / (table[Thi] - table[Tlo])
    raise ValueError("rhs not bracketed by the trial-temperature table")


# ============================================================================
# (B)  EQUILIBRIUM trunk (Moran Ch.14; concept module 12.2)
# ============================================================================
def chemical_potential_ideal_gas(g0, T, y, p_over_pref):
    """mu_i = g0_i + R T ln(y_i p/pref) for component i of an ideal gas mixture.
    [Eq. 14.17, Sec. 14.1, p.886]"""
    return g0 + R_BAR * T * math.log(y * p_over_pref)


def reaction_equilibrium_residual(products, reactants):
    """Equation of reaction equilibrium: SUM_P nu mu - SUM_R nu mu = 0 at equilibrium.
    products/reactants = [(nu, mu)]; returns the residual.  [Eq. 14.26, Sec. 14.2, p.889]"""
    return (sum(nu * mu for (nu, mu) in products)
            - sum(nu * mu for (nu, mu) in reactants))


def gibbs_of_reaction(products, reactants, T):
    """dG0 = SUM_P nu(h - T s0) - SUM_R nu(h - T s0), h & s0 at T (s0 at 1 atm).
    products/reactants = [(nu, h, s0)].  [Eq. 14.29b, Sec. 14.3.1, p.890]"""
    gP = sum(nu * (h - T * s0) for (nu, h, s0) in products)
    gR = sum(nu * (h - T * s0) for (nu, h, s0) in reactants)
    return gP - gR


def lnK_from_gibbs(dG0, T):
    """ln K = -dG0/(R T). [Eq. 14.31, Sec. 14.3.1, p.890]"""
    return -dG0 / (R_BAR * T)


def log10K_from_gibbs(dG0, T):
    """log10 K (the Table A-27 tabulation). [Sec. 14.3.1, p.890]"""
    return lnK_from_gibbs(dG0, T) / math.log(10.0)


def equilibrium_constant_composition(products, reactants, p_over_pref):
    """K = [PROD_P y^nu / PROD_R y^nu] (p/pref)^dnu; products/reactants = [(y, nu)].
    [Eq. 14.32, Sec. 14.3.1, p.890]"""
    num = 1.0
    for (y, nu) in products:
        num *= y ** nu
    den = 1.0
    for (y, nu) in reactants:
        den *= y ** nu
    dnu = sum(nu for (_, nu) in products) - sum(nu for (_, nu) in reactants)
    return (num / den) * p_over_pref ** dnu


def log10K_inverse(log10K):
    """Inverse reaction: log10 K* = -log10 K (K* = 1/K). [Eq. 14.34, Sec. 14.3.1, p.890]"""
    return -log10K


def equilibrium_constant_moles(products, reactants, n_total, p_over_pref):
    """K = [PROD_P n^nu / PROD_R n^nu] ((p/pref)/n)^dnu with n = total moles incl.
    inerts; products/reactants = [(n_i, nu)].  [Eq. 14.35, Sec. 14.3.2, p.892]"""
    num = 1.0
    for (ni, nu) in products:
        num *= ni ** nu
    den = 1.0
    for (ni, nu) in reactants:
        den *= ni ** nu
    dnu = sum(nu for (_, nu) in products) - sum(nu for (_, nu) in reactants)
    return (num / den) * (p_over_pref / n_total) ** dnu


def ionization_K_from_extent(z, p_over_pref):
    """Ionization equilibrium A <-> A+ + e- starting from 1 mol neutral A
    (extent z, n = 1 + z):  K = [z^2/(1 - z^2)] (p/pref).
    [Sec. 14.4.3 (Eq. 14.45), Ex. 14.8, p.904-905]"""
    return (z * z / (1.0 - z * z)) * p_over_pref


def ionization_extent_from_K(K, p_over_pref):
    """Extent of single ionization from K (inverse of the above):
    z = sqrt(K / (K + p/pref)).  [Sec. 14.4.3, Ex. 14.8, p.904-905]"""
    return math.sqrt(K / (K + p_over_pref))


# ============================================================================
# (C)  PLASMA extension  *** [~PK, NOT Moran] ***
# ============================================================================
def quantum_concentration(T, m=M_E):
    """n_Q = (2 pi m kB T / h^2)^(3/2) = 1/lambda^3 [m^-3], the electron-translation
    factor.  *** [~PK, NOT Moran; Reif; Rybicki & Lightman Sec. 9.5] ***"""
    return (2.0 * math.pi * m * K_B * T / H_PLANCK ** 2) ** 1.5


def saha_rhs(T, chi_eV, g_ratio=0.5):
    """Saha equation right-hand side S = n_+ n_e/n_0 [m^-3]:
    2 (g_+/g_0) n_Q(T) exp(-chi/(kB T)).  Hydrogen ground state: g_ratio = 1/2.
    *** [~PK, NOT Moran; Saha 1920; Chen; Rybicki & Lightman 9.5] ***"""
    return 2.0 * g_ratio * quantum_concentration(T) * math.exp(-chi_eV * EV / (K_B * T))


def saha_ionization_K(T, chi_eV, g_ratio=0.5, p_ref=P_REF_PA):
    """Moran-style dimensionless ionization-equilibrium constant from the Saha equation:
    K(T) = S(T) kB T / p_ref  (density-independent, pref = 1 atm).  Feeding this K to
    ionization_extent_from_K with the actual p/pref returns the Saha ionization fraction
    -- the statistical-thermodynamics calculation Moran Sec. 14.4.3 cites but omits.
    *** [~PK, NOT Moran] ***"""
    return saha_rhs(T, chi_eV, g_ratio) * K_B * T / p_ref


REGISTRY = [
    # (Eq., function, form, module, source)
    ("13.3-4", "theoretical_O2",              "a_O2 = C + H/4 + S - O/2",            "12.1", "Sec. 13.1.2, p.808"),
    ("13.4",   "theoretical_air_molar",       "AF_bar_theo = 4.76 a_O2",             "12.1", "Sec. 13.1.2, p.808"),
    ("13.2",   "air_fuel_mass_from_molar",    "AF = AF_bar (M_air/M_fuel)",          "12.1", "Sec. 13.1.2, p.808"),
    ("(13.5)", "percent_theoretical_air",     "%theo = AF/AF_theo",                  "12.1", "Sec. 13.1.2, p.808"),
    ("(13.5)", "percent_excess_air",          "%excess = AF/AF_theo - 1",            "12.1", "Sec. 13.1.2, p.808"),
    ("--",     "equivalence_ratio",           "phi = AF_theo/AF_act",                "12.1", "Sec. 13.1.2, p.809"),
    ("--",     "dew_point_partial_pressure",  "p_v = y_v p",                         "12.1", "Sec. 13.1.3, p.812"),
    ("13.9",   "enthalpy_formation_plus_dh",  "h = h_f0 + dh",                       "12.1", "Sec. 13.2.1, p.817"),
    ("13.15b", "stream_enthalpy",             "SUM n (h_f0 + dh)",                   "12.1", "Sec. 13.2.2, p.819"),
    ("13.12b", "energy_balance_steady",       "(Qcv-Wcv)/nF = hP - hR",              "12.1", "Sec. 13.2.2, p.818"),
    ("13.17b", "energy_balance_closed",       "Q-W = dH - R(TP nP - TR nR)",         "12.EP", "Sec. 13.2.2, p.823"),
    ("13.18",  "enthalpy_of_combustion",      "h_RP = SUM_P nh - SUM_R nh",          "12.1", "Sec. 13.2.3, p.825"),
    ("--",     "heating_value_molar",         "HHV/LHV = |h_RP|",                    "12.1", "Sec. 13.2.3, p.825"),
    ("--",     "heating_value_mass",          "|h_RP|/M_fuel",                       "12.1", "Sec. 13.2.3, p.826"),
    ("13.21b", "adiabatic_flame_rhs",         "SUM_P n dh = SUM_R n hf - SUM_P n hf", "12.EP", "Sec. 13.3.1, p.829"),
    ("13.21b", "interpolate_flame_temperature", "T_P bracketing/interpolation",      "12.EP", "Sec. 13.3.1, p.829-831"),
    ("14.17",  "chemical_potential_ideal_gas", "mu = g0 + RT ln(y p/pref)",          "12.2", "Sec. 14.1, p.886"),
    ("14.26",  "reaction_equilibrium_residual", "SUM_P nu mu = SUM_R nu mu",         "12.2", "Sec. 14.2, p.889"),
    ("14.29b", "gibbs_of_reaction",           "dG0 = SUM nu(h - T s0)|P-R",          "12.2", "Sec. 14.3.1, p.890"),
    ("14.31",  "lnK_from_gibbs",              "ln K = -dG0/(RT)",                    "12.2", "Sec. 14.3.1, p.890"),
    ("14.32",  "equilibrium_constant_composition", "K = PROD y^nu (p/pref)^dnu",     "12.2", "Sec. 14.3.1, p.890"),
    ("14.34",  "log10K_inverse",              "log10K* = -log10K",                   "12.2", "Sec. 14.3.1, p.890"),
    ("14.35",  "equilibrium_constant_moles",  "K = PROD n^nu ((p/pref)/n)^dnu",      "12.2", "Sec. 14.3.2, p.892"),
    ("14.45",  "ionization_K_from_extent",    "K = z^2/(1-z^2) (p/pref)",            "12.HP", "Sec. 14.4.3, p.904-905"),
    ("14.45",  "ionization_extent_from_K",    "z = sqrt(K/(K + p/pref))",            "12.HP", "Sec. 14.4.3, p.904-905"),
    ("~PK",    "quantum_concentration",       "n_Q = (2 pi m kT/h^2)^1.5",           "12.2", "~PK, NOT Moran (Reif; R&L 9.5)"),
    ("~PK",    "saha_rhs",                    "S = 2(g+/g0) n_Q e^(-chi/kT)",        "12.2", "~PK, NOT Moran (Saha 1920; Chen)"),
    ("~PK",    "saha_ionization_K",           "K = S kB T/pref",                     "12.2", "~PK, NOT Moran (bridge to Eq. 14.35)"),
]


def _demo():
    print("Module 12.EQ -- Topic 12 (Combustion & Reacting Mixtures) equation registry\n")
    for eq, fn, form, mod, src in REGISTRY:
        tag = src if src.startswith("~PK") else "Moran " + src
        print("  Eq %-7s %-33s %-38s [%s | %s]" % (eq, fn, form, mod, tag))
    print("\n  (~PK rows are the Saha plasma extension -- NOT in Moran 8e; see refs.md.)")


if __name__ == "__main__":
    _demo()
