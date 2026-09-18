"""
ionization.py  —  Module 12.2 (Dissociation, Chemical Equilibrium & Ionization)

TWO TRUNKS, clearly separated:

(A) MORAN TRUNK -- high-temperature DISSOCIATION via the equilibrium constant K
    (Moran 8e Chapter 14, Secs. 14.2-14.3).  For an ideal-gas reaction
        nuA A + nuB B  <->  nuC C + nuD D ,
    the equilibrium constant is
        K(T) = [ yC^nuC yD^nuD / (yA^nuA yB^nuB) ] (p/pref)^(dnu),   dnu = nuC+nuD-nuA-nuB
    and is fixed by the standard Gibbs change of reaction
        ln K = -dG0/(R_bar T),   dG0 = SUM_P nu*(h - T s0) - SUM_R nu*(h - T s0).
    Table A-27 tabulates log10 K(T).  log10 K* = -log10 K for the inverse reaction.

(B) PLASMA EXTENSION (~PK) -- the SAHA equation for thermal ionization.
    *** THIS PART IS BEYOND MORAN 8e. ***  Moran Ch.14 stops at molecular dissociation;
    the ionization equilibrium  A <-> A+ + e-  in a hot plasma is given by the Saha
    equation (M. N. Saha 1920), a standard statistical-mechanics / plasma-physics result:
        n_(i+1) n_e / n_i = 2 (g_(i+1)/g_i) (2 pi m_e k_B T / h^2)^(3/2) exp(-chi_i/(k_B T)).
    It is the same dG0 = -RT ln K idea with the electron's translational partition
    function (the quantum concentration n_Q) supplying the entropy of the freed electron.
    Sources (cross-trunk, ~PK): F. F. Chen, *Introduction to Plasma Physics and
    Controlled Fusion*; Rybicki & Lightman, *Radiative Processes in Astrophysics* Sec.9.5;
    Carroll & Ostlie, *An Introduction to Modern Astrophysics* Sec.8.1; Reif, *Statistical
    and Thermal Physics*.  Functions in part (B) are tagged [~PK, NOT Moran].

Units (A): enthalpies/Gibbs kJ/kmol, entropies kJ/kmol.K, R_bar = 8.314 kJ/kmol.K.
Units (B): SI -- T [K], n [m^-3], chi [eV]; constants below in SI.
Citations: Moran 8e (PDF = printed + 18; refs.md) for (A); cross-trunk texts for (B).
"""
import math

R_BAR = 8.314               # kJ/kmol.K  (universal gas constant)
# --- SI physical constants for the Saha part (CODATA) ---
M_E = 9.1093837015e-31      # electron mass, kg
K_B = 1.380649e-23          # Boltzmann constant, J/K
H_PLANCK = 6.62607015e-34   # Planck constant, J.s
EV = 1.602176634e-19        # 1 eV in J


# ============================================================================
# (A)  MORAN TRUNK: dissociation & the equilibrium constant (Ch.14)
# ============================================================================
def delta_nu(nu_products, nu_reactants):
    """Change in total moles of gaseous species  dnu = SUM nu_products - SUM nu_reactants.
    [Moran Sec. 14.3.1, exponent of (p/pref) in Eq. 14.32, p.890]"""
    return sum(nu_products) - sum(nu_reactants)


def equilibrium_constant_from_composition(products, reactants, p_over_pref):
    """Equilibrium constant from the equilibrium mole fractions:
        K = [ PROD y_C^nuC ] / [ PROD y_A^nuA ] * (p/pref)^dnu.
    products/reactants = lists of (y, nu).  [Moran Eq. 14.32, Sec. 14.3.1, p.890]"""
    num = 1.0
    for (y, nu) in products:
        num *= y ** nu
    den = 1.0
    for (y, nu) in reactants:
        den *= y ** nu
    dnu = sum(nu for (_, nu) in products) - sum(nu for (_, nu) in reactants)
    return (num / den) * p_over_pref ** dnu


def gibbs_of_reaction(products, reactants, T):
    """Standard Gibbs change of reaction at T (1 atm), from enthalpy & absolute entropy:
        dG0 = SUM_P nu (h - T s0) - SUM_R nu (h - T s0).
    products/reactants = lists of (nu, h, s0), h & s0 evaluated at T (h in kJ/kmol,
    s0 in kJ/kmol.K).  [Moran Eq. 14.29b, Sec. 14.3.1, p.890]"""
    gP = sum(nu * (h - T * s0) for (nu, h, s0) in products)
    gR = sum(nu * (h - T * s0) for (nu, h, s0) in reactants)
    return gP - gR


def lnK_from_gibbs(dG0, T):
    """ln K = -dG0/(R_bar T).  [Moran Eq. 14.31, Sec. 14.3.1, p.890]"""
    return -dG0 / (R_BAR * T)


def K_from_gibbs(dG0, T):
    """K = exp(-dG0/(R_bar T)).  [Moran Eqs. 14.31-14.32, Sec. 14.3.1, p.890]"""
    return math.exp(lnK_from_gibbs(dG0, T))


def log10K_from_gibbs(dG0, T):
    """log10 K (as tabulated in Table A-27).  [Moran Sec. 14.3.1, p.890]"""
    return lnK_from_gibbs(dG0, T) / math.log(10.0)


def log10K_inverse(log10K):
    """For the inverse reaction, log10 K* = -log10 K.  [Moran Eq. 14.34, p.890]"""
    return -log10K


# --- reproduce Moran Example 14.1: K for  CO + 1/2 O2 <-> CO2 ----------------
# Embedded Table A-25 (298 K) and Table A-23 (2000 K) data exactly as the book quotes.
_HF = {"CO2": -393520.0, "CO": -110530.0, "O2": 0.0}            # h_f0, kJ/kmol (A-25)
_S298 = {"CO2": 213.69, "CO": 197.54, "O2": 205.03}            # s0(298), kJ/kmol.K (A-25)
_H = {  # ideal-gas enthalpy h_bar(T), kJ/kmol (Table A-23)
    "CO2": {298: 9364.0, 2000: 100804.0},
    "CO":  {298: 8669.0, 2000: 65408.0},
    "O2":  {298: 8682.0, 2000: 67881.0},
}
_S = {  # absolute entropy s0(T), kJ/kmol.K at 2000 K (Table A-23)
    "CO2": {2000: 309.210}, "CO": {2000: 258.600}, "O2": {2000: 268.655},
}


def equilibrium_constant_CO_oxidation(T):
    """Moran Example 14.1: equilibrium constant for  CO + 1/2 O2 <-> CO2  at T = 298 or
    2000 K, using Table A-23/A-25 data.  Returns dG0 (kJ/kmol), lnK, log10K.
    [Moran Ex. 14.1, Eqs. 14.29b/14.31, p.891]"""
    if T == 298:
        # dh = 0 at Tref; absolute entropies are the 298-K values
        prod = [(1, _HF["CO2"], _S298["CO2"])]
        reac = [(1, _HF["CO"], _S298["CO"]), (0.5, _HF["O2"], _S298["O2"])]
    elif T == 2000:
        def h(sp):
            return _HF[sp] + (_H[sp][2000] - _H[sp][298])
        prod = [(1, h("CO2"), _S["CO2"][2000])]
        reac = [(1, h("CO"), _S["CO"][2000]), (0.5, h("O2"), _S["O2"][2000])]
    else:
        raise ValueError("Example 14.1 tabulates T = 298 K or 2000 K")
    dG0 = gibbs_of_reaction(prod, reac, float(T))
    return {"dG0": dG0, "lnK": lnK_from_gibbs(dG0, float(T)),
            "log10K": log10K_from_gibbs(dG0, float(T))}


def dissociation_extent_CO2(K, p_over_pref, n_inert=0.0, tol=1e-12, itmax=200):
    """Degree of dissociation for  CO + 1/2 O2 (+ a N2 inert) -> z CO + (z/2) O2 +
    (1-z) CO2 (+ a N2)  at equilibrium (Moran Ex. 14.2 / 14.4 form):
        K = [z/(1-z)] [z/(2 + 2a + z)]^(1/2) (p/pref)^(1/2),
    where z = kmol CO present and a = n_inert.  Solved by bisection for z in (0,1).
    [Moran Eq. 14.35, Ex. 14.2, p.892-893]"""
    base = 2.0 + 2.0 * n_inert

    def f(z):
        return (z / (1.0 - z)) * (z / (base + z)) ** 0.5 * p_over_pref ** 0.5 - K

    lo, hi = 1e-12, 1.0 - 1e-12
    for _ in range(itmax):
        z = 0.5 * (lo + hi)
        if f(z) > 0:
            hi = z
        else:
            lo = z
        if hi - lo < tol:
            break
    return 0.5 * (lo + hi)


# ============================================================================
# (B)  PLASMA EXTENSION (~PK, NOT Moran): the Saha ionization equation
# ============================================================================
def thermal_debroglie_wavelength(T, m=M_E):
    """Thermal de Broglie wavelength  lambda = h / sqrt(2 pi m k_B T)  [m].
    For electrons at 300 K, lambda ~ 4.3 nm.  [~PK, NOT Moran; Reif, Stat. Mech.]"""
    return H_PLANCK / math.sqrt(2.0 * math.pi * m * K_B * T)


def quantum_concentration(T, m=M_E):
    """Quantum concentration  n_Q = (2 pi m k_B T / h^2)^(3/2) = 1/lambda^3  [m^-3]
    (translational partition function per unit volume of the freed electron).
    [~PK, NOT Moran; Reif / Rybicki & Lightman Sec. 9.5]"""
    return (2.0 * math.pi * m * K_B * T / H_PLANCK ** 2) ** 1.5


def saha_rhs(T, chi_eV, g_ratio=0.5):
    """Right-hand side of the Saha equation  n_(i+1) n_e / n_i  [m^-3]:
        2 (g_(i+1)/g_i) n_Q(T) exp(-chi/(k_B T)).
    g_ratio = g_(i+1)/g_i (hydrogen ground state: g_I=2, g_II=1 -> 0.5).
    *** [~PK, NOT Moran -- plasma/stat-mech extension; Chen; Rybicki & Lightman 9.5] ***"""
    return 2.0 * g_ratio * quantum_concentration(T) * math.exp(-chi_eV * EV / (K_B * T))


def saha_ionization_fraction(T, n_total, chi_eV, g_ratio=0.5):
    """Degree of ionization x = n_e/n_total for a single-ionization gas in LTE.  With
    x^2/(1-x) = S/n_total and S = saha_rhs, x = (-r + sqrt(r^2 + 4r))/2, r = S/n_total.
    Returns x in (0,1): x->0 as T->0, x->1 as T->infinity.
    *** [~PK, NOT Moran -- Saha 1920; Chen; Carroll & Ostlie Sec. 8.1] ***"""
    r = saha_rhs(T, chi_eV, g_ratio) / n_total
    return (-r + math.sqrt(r * r + 4.0 * r)) / 2.0


def saha_electron_density(T, n_total, chi_eV, g_ratio=0.5):
    """Electron number density n_e = x n_total from the Saha ionization fraction [m^-3].
    *** [~PK, NOT Moran -- plasma extension] ***"""
    return saha_ionization_fraction(T, n_total, chi_eV, g_ratio) * n_total


def _demo():
    print("Module 12.2 -- Dissociation, equilibrium constant K, and ionization\n")
    print("  (A) MORAN trunk -- equilibrium constant (Ch.14):")
    for T in (298, 2000):
        r = equilibrium_constant_CO_oxidation(T)
        print("    Ex 14.1  CO+1/2O2<->CO2  T=%4dK: dG0=%9.0f kJ/kmol, log10K=%7.3f"
              % (T, r["dG0"], r["log10K"]))
    print("      [book: 298K dG0=-257,253 log10K=45.093; 2000K dG0=-110,453 log10K=2.885]")
    z1 = dissociation_extent_CO2(0.0363, 1.0)
    z10 = dissociation_extent_CO2(0.0363, 10.0)
    print("    Ex 14.2  CO2 dissociation @2500K (K=0.0363): z(CO)=%.3f at 1 atm, %.3f at 10 atm"
          % (z1, z10))
    print("      [book z=0.129 (1 atm), 0.062 (10 atm); higher p suppresses dissociation]")

    print("\n  (B) PLASMA extension [~PK, NOT Moran] -- Saha equation:")
    print("    electron de Broglie wavelength @300K = %.2f nm   [lit. ~4.30 nm]"
          % (thermal_debroglie_wavelength(300.0) * 1e9))
    print("    quantum concentration n_Q @300K      = %.3e m^-3" % quantum_concentration(300.0))
    for T in (6000.0, 10000.0, 20000.0):
        x = saha_ionization_fraction(T, 1.0e23, 13.6)      # hydrogen, n=1e23 m^-3
        print("    H ionization @%6.0fK, n=1e23 m^-3:  x = %.4g" % (T, x))
    print("      (x rises steeply with T though chi/k_B = 158,000 K >> T -- the n_Q factor)")


if __name__ == "__main__":
    _demo()
