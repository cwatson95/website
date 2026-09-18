"""NE-09  Fission: fissile vs fissionable, fragments, neutrons and the energy budget.

Nuclear Science & Engineering trunk, module NE-09 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 6.5.3 and 6.6 (printed pp. 150-163).  Pure stdlib; masses from
../../data_tables/B1_atomic_masses.csv.

~NE-08 established that a neutron faces no Coulomb barrier and can therefore be
absorbed by any nucleus at any energy.  Fission is what happens when the nucleus
absorbing it is heavy enough that the resulting compound nucleus can deform past
the point where the short-ranged strong force can hold the two ends together.

Four numbers carry this module:

  1. E* = S_n + E_n.  The excitation energy of the compound nucleus is the
     binding energy the absorbed neutron releases PLUS whatever kinetic energy it
     brought.  Comparing E* with the fission barrier splits the actinides into
     FISSILE (a zero-energy neutron suffices: 233U, 235U, 239Pu, 241Pu) and merely
     FISSIONABLE (a fast neutron is needed: 238U, 232Th, 240Pu).  The whole
     distinction turns on the pairing term of ~NE-02 -- odd-N targets gain more
     binding energy from an added neutron than even-N ones do.

  2. ~200 MeV per fission, of which 168 MeV is fission-fragment kinetic energy
     deposited within a millimetre, and 12 MeV leaves in neutrinos and is
     unrecoverable.

  3. nu ~ 2.4-2.9 neutrons per fission, of which a fraction beta ~ 0.0065 arrive
     seconds to minutes late.  That tiny delayed fraction is what makes a reactor
     controllable at human timescales (~NE-20).

  4. 1 MWd per 1.24 g of 235U consumed -- the number that makes the fuel cycle of
     ~NE-23 look the way it does.
"""

import csv
import math
import os

__all__ = [
    "M_N_U", "M_H_U", "U_MEV", "MEV_PER_J", "AVOGADRO",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "SPONTANEOUS_FISSION", "NEUTRON_YIELD", "WATT_PARAMS", "FISSION_ENERGY_MEV",
    "TABLE_6_2_ERRATA", "BETA_BRANCH_PERCENT",
    "FISSILE", "FISSIONABLE", "FERTILE", "BREEDING",
    "separation_energy_n", "excitation_energy", "is_fissile",
    "spontaneous_fission_rate", "neutrons_per_gram_second",
    "fragment_energy_split", "prompt_energy_release", "delayed_energy_release",
    "conserve_fission", "partner_fragment",
    "total_neutrons", "delayed_fraction", "delayed_neutrons",
    "watt_spectrum", "watt_mean_energy", "watt_peak_energy", "fission_energy",
    "decay_heat_gamma", "decay_heat_beta", "decay_heat_total",
    "fissions_per_second", "grams_per_mwd", "mwd_per_gram", "burnup_energy",
]

M_N_U = 1.0086649156
M_H_U = 1.0078250321
U_MEV = 931.494043
MEV_PER_J = 1.0 / 1.602176487e-13     # MeV per joule
AVOGADRO = 6.0221415e23

# --- S&F Table 6.2 (printed p. 151): nuclides which spontaneously fission ----
# nuclide -> (half_life_years, fission_probability_percent, neutrons_per_fission,
#             alphas_per_fission, neutrons_per_gram_second)
#
# TWO PRINTED VALUES ARE CORRECTED HERE.  The table carries three independent
# columns tied to the same physics -- half-life, fission probability, alphas per
# fission and neutron emission rate -- so each row can be checked against itself
# (`test_table_6_2_is_internally_consistent` does exactly that, and 24 of the 26
# rows agree to within 5%).  The two that did not are typos, and in each case the
# OTHER two columns agree on what the right value is:
#
#   237Np  fission probability printed as 2.1e-12 %.  Both the alphas-per-fission
#          column (4.7e11 => fission fraction 2.1e-12, i.e. 2.1e-10 %) and the
#          emission rate (1.1e-4 n/(g s)) require 2.1e-10 %.  Corrected.
#   248Cm  emission rate printed as 4.1e12 n/(g s).  Its 3.39e5 y half-life and
#          8.26% fission probability give 4.1e7, and 4.1e12 would make a
#          339 000-year nuclide a brighter neutron source than 252Cf (2.3e12,
#          half-life 2.6 y), which is impossible.  4.1e7 is also the value
#          quoted elsewhere for 248Cm sources.  Corrected.
#
# Printed values are kept in TABLE_6_2_ERRATA so nothing is silently discarded.
TABLE_6_2_ERRATA = {
    "237Np": ("fission_probability_percent", 2.1e-12, 2.1e-10),
    "248Cm": ("neutrons_per_gram_second", 4.1e12, 4.1e7),
}

# Caption to Table 6.2: these three also beta-decay, with the given probability,
# so alpha emission is NOT simply the complement of spontaneous fission for them.
BETA_BRANCH_PERCENT = {"241Pu": 99.99755, "250Cm": 14.0, "249Bk": 99.99856}

SPONTANEOUS_FISSION = {
    "233U":  (1.59e5,   1.3e-10, 1.76, 7.6e11, 8.6e-4),
    "235U":  (7.04e8,   2.0e-7,  1.86, 5.0e8,  3.0e-4),
    "238U":  (4.47e9,   5.4e-5,  2.07, 1.9e6,  0.0136),
    "237Np": (2.14e6,   2.1e-10, 2.05, 4.7e11, 1.1e-4),   # corrected, see errata
    "236Pu": (2.85,     8.1e-8,  2.23, 1.2e9,  3.6e4),
    "238Pu": (87.7,     1.8e-7,  2.28, 5.4e8,  2.7e3),
    "239Pu": (2.41e4,   4.4e-10, 2.16, 2.3e11, 2.2e-2),
    "240Pu": (6569.0,   5.0e-6,  2.21, 2.0e7,  920.0),
    "241Pu": (14.35,    5.7e-13, 2.25, 4.3e9,  0.05),
    "242Pu": (3.76e5,   5.5e-4,  2.24, 1.8e5,  1.8e3),
    "244Pu": (8.26e7,   0.125,   2.28, 8.0e2,  1.9e3),
    "241Am": (433.6,    4.1e-10, 3.22, 2.4e11, 1.18),
    "242Cm": (163.0 / 365.25, 6.8e-6, 2.70, 1.5e7, 2.3e7),
    "244Cm": (18.11,    1.3e-4,  2.77, 7.5e5,  1.1e7),
    "246Cm": (4730.0,   0.0261,  2.86, 3.8e3,  8.5e6),
    "248Cm": (3.39e5,   8.26,    3.14, 11.0,   4.1e7),    # corrected, see errata
    "250Cm": (6900.0,   61.0,    3.31, 0.40,   1.6e10),
    "249Bk": (320.0 / 365.25, 4.7e-8, 3.67, 3.1e4, 1.1e5),
    "246Cf": (35.7 / (24 * 365.25), 2.0e-4, 2.83, 5.0e5, 7.5e10),
    "248Cf": (333.5 / 365.25, 2.9e-3, 3.00, 3.5e4, 5.1e9),
    "249Cf": (350.6,    5.2e-7,  3.20, 1.9e8,  2.5e3),
    "250Cf": (13.08,    0.077,   3.49, 1.3e3,  1.1e10),
    "252Cf": (2.638,    3.09,    3.73, 31.0,   2.3e12),
    "254Cf": (60.5 / 365.25, 99.69, 3.89, 0.0031, 1.2e15),
    "253Es": (20.47 / 365.25, 8.7e-6, 3.70, 1.2e7, 3.0e8),
    "254Fm": (3.24 / (24 * 365.25), 0.053, 4.00, 1.9e3, 3.0e14),
}

# --- S&F Table 6.3 (printed p. 158): nu and the delayed fraction beta -------
# nuclide -> {"fast": (nu, beta), "thermal": (nu, beta)}
NEUTRON_YIELD = {
    "235U":  {"fast": (2.57, 0.0064), "thermal": (2.43, 0.0065)},
    "233U":  {"fast": (2.62, 0.0026), "thermal": (2.48, 0.0026)},
    "239Pu": {"fast": (3.09, 0.0020), "thermal": (2.87, 0.0021)},
    "241Pu": {"thermal": (3.14, 0.0049)},
    "238U":  {"fast": (2.79, 0.0148)},
    "232Th": {"fast": (2.44, 0.0203)},
    "240Pu": {"fast": (3.3, 0.0026)},
}

# --- S&F Table 6.4 (printed p. 159): Watt spectrum parameters ---------------
# (nuclide, fission type) -> (E_w, T_w, a, b, c)
WATT_PARAMS = {
    ("233U", "thermal"):      (0.3870, 1.108, 0.6077, 1.1080, 1.2608),
    ("235U", "thermal"):      (0.4340, 1.035, 0.5535, 1.0347, 1.6214),
    ("239Pu", "thermal"):     (0.4130, 1.159, 0.5710, 1.1593, 1.2292),
    ("232Th", "fast"):        (0.4305, 0.971, 0.5601, 0.9711, 1.8262),
    ("238U", "fast"):         (0.4159, 1.027, 0.5759, 1.0269, 1.5776),
    ("252Cf", "spontaneous"): (0.3590, 1.175, 0.6400, 1.1750, 1.0401),
}

# --- S&F Table 6.5 (printed p. 161): average energy per thermal 235U fission -
# component -> (produced_MeV, recoverable_MeV)
FISSION_ENERGY_MEV = {
    "fragment_kinetic":   (168.0, 168.0),
    "prompt_neutrons":    (5.0, 5.0),
    "prompt_gammas":      (7.0, 7.0),
    "capture_gammas":     (0.0, 6.0),      # 3-9 MeV, core-design dependent
    "delayed_beta":       (8.0, 8.0),
    "delayed_gamma":      (7.0, 7.0),
    "neutrinos":          (12.0, 0.0),     # never recoverable
}

FISSILE = ("233U", "235U", "239Pu", "241Pu")
FISSIONABLE = ("232Th", "238U", "240Pu")
FERTILE = ("232Th", "238U")
# S&F printed p. 152: the two important breeding chains
BREEDING = {
    "232Th": ("233Th", "22 m", "233Pa", "27 d", "233U"),
    "238U":  ("239U", "24 m", "239Np", "56 h", "239Pu"),
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
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


# --- fissile vs fissionable  [S&F §6.5.3, printed p. 152] ------------------

def separation_energy_n(A, Z, table=None):
    """Neutron separation energy S_n of nuclide (A, Z), in MeV:

        S_n = [ M(A-1, Z) + m_n - M(A, Z) ] c^2 .

    This is the energy released when a free neutron is absorbed -- the excitation
    it hands to the compound nucleus before any kinetic energy is counted.
    Same quantity as ~NE-03's `neutron_separation_energy`, repeated here so this
    module stands alone."""
    t = load_atomic_masses() if table is None else table
    return (atomic_mass(A - 1, Z, t) + M_N_U - atomic_mass(A, Z, t)) * U_MEV


def excitation_energy(A_target, Z_target, e_neutron_mev=0.0, table=None):
    """Excitation energy E* of the compound nucleus formed when nuclide
    (A_target, Z_target) absorbs a neutron  [S&F §6.6, printed p. 153]:

        E* = S_n(A_target + 1) + E_n ,

    neglecting the compound nucleus's negligible recoil.  Note S_n is evaluated
    for the PRODUCT nucleus -- absorbing a neutron by 235U makes 236U, and it is
    236U's neutron binding energy that is released."""
    return separation_energy_n(A_target + 1, Z_target, table) + e_neutron_mev


def is_fissile(A, Z, barrier_mev=6.2, table=None):
    """True if a zero-energy neutron excites the compound nucleus above its
    fission barrier -- the definition of a FISSILE nuclide.

    The barrier is ~6 MeV across the actinides and varies only slowly, so the
    fissile/fissionable split is decided almost entirely by S_n, which in turn is
    decided by the PAIRING term of ~NE-02: adding a neutron to an odd-N target
    (235U, N=143) completes a pair and releases ~1 MeV more than adding one to an
    even-N target (238U, N=146).  That single MeV is the difference between a
    reactor fuel and a reactor blanket."""
    return excitation_energy(A, Z, 0.0, table) > barrier_mev


# --- spontaneous fission  [S&F Table 6.2, printed p. 151] ------------------

def spontaneous_fission_rate(nuclide, mass_g=1.0):
    """Spontaneous fissions per second in `mass_g` grams, from Table 6.2's
    neutrons per gram-second divided by neutrons per fission."""
    if nuclide not in SPONTANEOUS_FISSION:
        raise KeyError("%s does not appear in S&F Table 6.2" % nuclide)
    _, _, nu, _, n_per_gs = SPONTANEOUS_FISSION[nuclide]
    return mass_g * n_per_gs / nu


def neutrons_per_gram_second(nuclide):
    """Table 6.2's spontaneous-fission neutron emission rate, n/(g s).

    252Cf's 2.3e12 is why a 10 microgram source is a usable laboratory neutron
    generator, and 240Pu's 920 is why reactor-grade plutonium cannot be used in a
    gun-type weapon -- it pre-initiates."""
    if nuclide not in SPONTANEOUS_FISSION:
        raise KeyError("%s does not appear in S&F Table 6.2" % nuclide)
    return SPONTANEOUS_FISSION[nuclide][4]


# --- fragments  [S&F Eqs. (6.34), (6.40)-(6.41)] ---------------------------

def conserve_fission(A_target, Z_target, A_light, Z_light, nu_prompt):
    """(A_heavy, Z_heavy) fixed by conservation  [Eq. (6.34)]:

        A_L + A_H + nu_p = A_target + 1,     Z_L + Z_H = Z_target .

    Raises if the result is unphysical."""
    A_h = A_target + 1 - A_light - nu_prompt
    Z_h = Z_target - Z_light
    if A_h < 1 or Z_h < 1 or A_h < Z_h:
        raise ValueError("unphysical heavy fragment: A=%r Z=%r" % (A_h, Z_h))
    return A_h, Z_h


def partner_fragment(A_target, A_light, nu_prompt):
    """Mass number of the partner fragment, A_H = A_target + 1 - A_L - nu_p."""
    return A_target + 1 - A_light - nu_prompt


def fragment_energy_split(e_total_mev, m_light, m_heavy):
    """(E_light, E_heavy) from momentum conservation  [Eqs. (6.40)-(6.41)]:

        E_L/E_H = m_H/m_L ,     E_L + E_H = E_total ,

    so E_L = E_total m_H/(m_L + m_H).  The LIGHTER fragment carries MORE energy,
    which is why the measured fragment-energy spectrum is bimodal with peaks at
    99.2 and 68.1 MeV rather than a single line at ~84."""
    if m_light <= 0 or m_heavy <= 0:
        raise ValueError("masses must be positive")
    tot = m_light + m_heavy
    return e_total_mev * m_heavy / tot, e_total_mev * m_light / tot


def prompt_energy_release(A_target, Z_target, fragments, nu_prompt, table=None):
    """Prompt energy release E_p from the mass deficit  [S&F Example 6.4]:

        E_p = [ M(target) + m_n - sum M(fragments) - nu_p m_n ] c^2 ,

    with `fragments` a list of (A, Z) pairs AFTER prompt neutron emission.
    Neutral-atom masses may be used because the electron count balances."""
    t = load_atomic_masses() if table is None else table
    lhs = atomic_mass(A_target, Z_target, t) + M_N_U
    rhs = sum(atomic_mass(A, Z, t) for A, Z in fragments) + nu_prompt * M_N_U
    return (lhs - rhs) * U_MEV


def delayed_energy_release(products, stable_ends, table=None):
    """Delayed energy release as fission products beta-decay to stability
    [S&F Example 6.5]:

        E_d = [ sum M(products) - sum M(stable ends) ] c^2 .

    Electron masses cancel: each beta- emitted is matched by an ambient electron
    absorbed to keep the atom neutral, so NEUTRAL-ATOM masses give the answer
    directly with no per-decay correction (contrast ~NE-05's beta+ and EC cases).
    The result includes the neutrino energy, which is not recoverable."""
    t = load_atomic_masses() if table is None else table
    a = sum(atomic_mass(A, Z, t) for A, Z in products)
    b = sum(atomic_mass(A, Z, t) for A, Z in stable_ends)
    return (a - b) * U_MEV


# --- fission neutrons  [S&F Table 6.3, Eqs. (6.42)-(6.43)] -----------------

def total_neutrons(nuclide, spectrum="thermal"):
    """Average total neutrons per fission, nu = nu_p + nu_d  [Table 6.3]."""
    entry = NEUTRON_YIELD.get(nuclide, {})
    if spectrum not in entry:
        raise KeyError("no %s-fission data for %s in S&F Table 6.3"
                       % (spectrum, nuclide))
    return entry[spectrum][0]


def delayed_fraction(nuclide, spectrum="thermal"):
    """Delayed neutron fraction beta = nu_d/nu  [Table 6.3].

    Always under 1%, and yet it sets the entire timescale of reactor control: a
    reactor held just below prompt criticality responds on the seconds-to-minutes
    timescale of the delayed-neutron precursors rather than the ~1e-4 s prompt
    neutron lifetime (~NE-20)."""
    entry = NEUTRON_YIELD.get(nuclide, {})
    if spectrum not in entry:
        raise KeyError("no %s-fission data for %s in S&F Table 6.3"
                       % (spectrum, nuclide))
    return entry[spectrum][1]


def delayed_neutrons(nuclide, spectrum="thermal"):
    """nu_d = beta * nu, the delayed neutrons per fission."""
    return total_neutrons(nuclide, spectrum) * delayed_fraction(nuclide, spectrum)


def watt_spectrum(e_mev, nuclide="235U", spectrum="thermal"):
    """Prompt fission-neutron energy distribution chi(E)  [Eq. (6.42)]:

        chi(E) = exp[-(E + E_w)/T_w] / sqrt(pi E_w T_w) * sinh( sqrt(4 E_w E)/T_w )

    normalised so that the integral over all E is 1, with units of 1/MeV."""
    key = (nuclide, spectrum)
    if key not in WATT_PARAMS:
        raise KeyError("no Watt parameters for %r in S&F Table 6.4" % (key,))
    if e_mev < 0:
        raise ValueError("energy must be non-negative")
    Ew, Tw = WATT_PARAMS[key][0], WATT_PARAMS[key][1]
    pre = math.exp(-(e_mev + Ew) / Tw) / math.sqrt(math.pi * Ew * Tw)
    return pre * math.sinh(math.sqrt(4.0 * Ew * e_mev) / Tw)


def watt_peak_energy(nuclide="235U", spectrum="thermal", e_max=5.0, n=20000):
    """Most probable prompt fission-neutron energy -- the mode of chi(E), near
    0.7 MeV for every fissile nuclide  [S&F p. 158]."""
    h = e_max / n
    best, arg = -1.0, 0.0
    for i in range(1, n + 1):
        e = i * h
        c = watt_spectrum(e, nuclide, spectrum)
        if c > best:
            best, arg = c, e
    return arg


def watt_mean_energy(nuclide="235U", spectrum="thermal", e_max=25.0, n=20000):
    """Mean prompt fission-neutron energy, by numerical integration of chi(E).

    Comes out near 2 MeV for every fissile nuclide, while chi(E) PEAKS near
    0.7 MeV -- the spectrum is broad and right-skewed, so the mean and the mode
    are very different numbers and quoting the wrong one is a common error."""
    h = e_max / n
    tot = num = 0.0
    for i in range(n):
        e = (i + 0.5) * h
        c = watt_spectrum(e, nuclide, spectrum)
        tot += c * h
        num += e * c * h
    return num / tot


# --- energy released  [S&F Table 6.5, Eqs. (6.44)-(6.45)] ------------------

def fission_energy(recoverable=False):
    """Total energy per thermal 235U fission, MeV  [Table 6.5]:
    207 MeV produced, ~201 MeV recoverable in a core."""
    i = 1 if recoverable else 0
    return sum(v[i] for v in FISSION_ENERGY_MEV.values())


def decay_heat_gamma(t_s):
    """Delayed gamma power per fission  [Eq. (6.44)]:  1.4 t^-1.2 MeV/s.
    Valid for 10 s < t < 1e5 s."""
    if t_s <= 0:
        raise ValueError("time must be positive")
    return 1.4 * t_s ** -1.2


def decay_heat_beta(t_s):
    """Delayed beta power per fission  [Eq. (6.45)]:  1.26 t^-1.2 MeV/s."""
    if t_s <= 0:
        raise ValueError("time must be positive")
    return 1.26 * t_s ** -1.2


def decay_heat_total(t_s):
    """Combined delayed beta + gamma power per fission, MeV/s.

    This is the heat a shut-down reactor keeps producing.  It does not switch
    off, it decays as t^-1.2 -- roughly 7% of full power at shutdown, 1% after an
    hour -- and every loss-of-coolant accident in history is a story about it
    (~NE-22, ~NE-23)."""
    return decay_heat_gamma(t_s) + decay_heat_beta(t_s)


# --- macroscopic conversions  [S&F printed pp. 162-163] --------------------

def fissions_per_second(power_w, energy_per_fission_mev=200.0):
    """Fission rate sustaining a given thermal power  [S&F p. 162]:
    1 W ~ 3.1e10 fissions/s at 200 MeV recoverable per fission."""
    if power_w < 0 or energy_per_fission_mev <= 0:
        raise ValueError("invalid power or fission energy")
    return power_w * MEV_PER_J / energy_per_fission_mev


def grams_per_mwd(A=235, energy_per_fission_mev=200.0, fission_fraction=1.0):
    """Grams of a nuclide FISSIONED (fission_fraction=1) or CONSUMED
    (fission_fraction=0.85 for thermal 235U) per megawatt-day  [S&F p. 163]:

        1 MWd = 1.05 g of 235U fissioned = 1.24 g of 235U consumed.

    The 0.85 is the fission-to-absorption ratio: 15% of thermal neutrons absorbed
    by 235U give (n,gamma) 236U instead of fission (~NE-13, ~NE-19)."""
    if not 0 < fission_fraction <= 1:
        raise ValueError("fission fraction must be in (0, 1]")
    rate = fissions_per_second(1e6, energy_per_fission_mev)      # 1 MW
    return rate * 86400.0 * A / AVOGADRO / fission_fraction


def mwd_per_gram(A=235, energy_per_fission_mev=200.0, fission_fraction=1.0):
    """Inverse of `grams_per_mwd` -- burnup per gram."""
    return 1.0 / grams_per_mwd(A, energy_per_fission_mev, fission_fraction)


def burnup_energy(mass_g, A=235, energy_per_fission_mev=200.0):
    """Thermal energy (MWd) from completely fissioning `mass_g` grams."""
    return mass_g * mwd_per_gram(A, energy_per_fission_mev)


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-09  fission\n")

    print("  fissile vs fissionable: one MeV of pairing energy decides it")
    print("   target    N    compound   E* at 0 eV   vs 6.2 MeV barrier   class")
    for A, Z, elem, lab in [(233, 92, "U", "233U"), (235, 92, "U", "235U"),
                            (238, 92, "U", "238U"), (239, 94, "Pu", "239Pu"),
                            (241, 94, "Pu", "241Pu"), (240, 94, "Pu", "240Pu"),
                            (232, 90, "Th", "232Th")]:
        e = excitation_energy(A, Z, 0.0, t)
        fis = is_fissile(A, Z, table=t)
        print("   %-8s %4d %8s %10.3f %14s      %s"
              % (lab, A - Z, "%d%s" % (A + 1, elem), e, "%+.2f" % (e - 6.2),
                 "fissile" if fis else "fissionable (fast only)"))
    print("   -> odd-N targets (233U, 235U, 239Pu, 241Pu) pair up the added neutron")
    print("      and release ~1.5 MeV more.  238U needs %.2f MeV of kinetic energy."
          % max(0.0, 6.2 - excitation_energy(238, 92, 0.0, t)))

    print("\n  S&F Example 6.4: 235U(n,f) -> 139Xe + 95Sr + 2n + 7 gammas")
    ep = prompt_energy_release(235, 92, [(139, 54), (95, 38)], 2, t)
    eff = ep - 5.2 - 6.7
    el, eh = fragment_energy_split(eff, atomic_mass(95, 38, t), atomic_mass(139, 54, t))
    print("   prompt release E_p          = %7.1f MeV" % ep)
    print("   fragment kinetic energy E_ff = %7.1f MeV" % eff)
    print("   light (95Sr) / heavy (139Xe) = %6.1f / %.1f MeV" % (el, eh))
    ed = delayed_energy_release([(139, 54), (95, 38)], [(139, 57), (95, 42)], t)
    print("   Example 6.5: delayed release = %7.1f MeV  (7 beta decays)" % ed)

    print("\n  the 200 MeV budget  [Table 6.5]")
    for k in ("fragment_kinetic", "prompt_neutrons", "prompt_gammas",
              "capture_gammas", "delayed_beta", "delayed_gamma", "neutrinos"):
        p, r = FISSION_ENERGY_MEV[k]
        print("   %-20s produced %5.1f   recoverable %5.1f" % (k, p, r))
    print("   %-20s produced %5.1f   recoverable %5.1f"
          % ("TOTAL", fission_energy(False), fission_energy(True)))

    print("\n  neutrons per fission  [Table 6.3]")
    print("   nuclide   nu(thermal)  beta      nu_d      1/beta")
    for n in ("235U", "233U", "239Pu", "241Pu"):
        nu, b = total_neutrons(n), delayed_fraction(n)
        print("   %-9s %8.2f %10.4f %8.4f %8.0f" % (n, nu, b, nu * b, 1 / b))

    print("\n  prompt fission-neutron spectrum  [Eq. (6.42)]")
    print("   nuclide          peak (MeV)   mean (MeV)")
    for n, s in [("235U", "thermal"), ("239Pu", "thermal"), ("252Cf", "spontaneous")]:
        print("   %-8s %-8s %8.2f %12.2f"
              % (n, s, watt_peak_energy(n, s), watt_mean_energy(n, s)))
    print("   -> mode ~0.7 MeV but mean ~2 MeV: the spectrum is broad and skewed.")

    print("\n  spontaneous fission  [Table 6.2]")
    print("   nuclide     n/(g s)    SF per decay (%)   use")
    for n, use in [("252Cf", "laboratory neutron source"),
                   ("254Cf", "the only nuclide that mostly fissions"),
                   ("240Pu", "pre-initiation in weapons-grade Pu"),
                   ("238U", "background in natural uranium")]:
        hl, fp, nu, al, ngs = SPONTANEOUS_FISSION[n]
        print("   %-10s %10.2e %13.3g       %s" % (n, ngs, fp, use))

    print("\n  macroscopic conversions")
    print("   1 W sustains          %.2e fissions/s" % fissions_per_second(1.0))
    print("   1 MWd fissions        %.3f g of 235U" % grams_per_mwd())
    print("   1 MWd consumes        %.3f g of 235U (85%% of absorptions fission)"
          % grams_per_mwd(fission_fraction=0.85))
    print("   1 g of 235U yields    %.3f MWd = %.1f GJ"
          % (mwd_per_gram(), mwd_per_gram() * 86.4))

    print("\n  decay heat after shutdown  [Eqs. (6.44)-(6.45)]")
    print("   t (s)     MeV/s per fission    relative to 200 MeV prompt")
    for ts in (10.0, 100.0, 3600.0, 86400.0):
        d = decay_heat_total(ts)
        print("   %8.0f  %18.3e  %20.3e" % (ts, d, d / 200.0))


if __name__ == "__main__":
    _demo()
