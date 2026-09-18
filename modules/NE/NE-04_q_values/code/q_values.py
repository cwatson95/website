"""NE-04  Nuclear reactions and Q-values.

Nuclear Science & Engineering trunk, module NE-04 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 4.4-4.8 (printed pp. 88-94).  Pure stdlib; measured masses come
from ../../data_tables/B1_atomic_masses.csv (Appendix B).

Energy conservation across a reaction, rest mass included, defines the Q-value

    Q = (KE of products) - (KE of reactants)
      = (rest mass of reactants - rest mass of products) c^2 .

Q > 0 is exothermic: rest mass is converted to kinetic energy, and the reaction
can proceed at any incident energy.  Q < 0 is endothermic: kinetic energy is
converted to rest mass, and there is a threshold below which nothing happens
(~NE-08 computes it properly, with recoil).

The trap this module exists to defuse: Appendix B tabulates **atomic** masses,
which include Z electrons.  A reaction that changes the proton number does not
conserve the number of bound electrons, so blindly subtracting atomic masses
double-counts them.  S&F's rule (printed p. 92) is to write every charged
particle as its neutral-atom counterpart -- a proton becomes a 1H atom, an alpha
becomes a 4He atom -- after which the electrons balance and atomic masses may be
subtracted directly.  Beta decay breaks even this rule, and ~NE-05 handles it.

Reactions are written in the compact notation  X(x,y)Y, e.g. "9Be(a,n)12C".
"""

import csv
import os
import re

__all__ = [
    "M_N_U", "M_H_U", "M_E_U", "U_MEV", "PARTICLES",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "parse_nuclide", "parse_reaction", "format_nuclide",
    "species_mass_u", "species_ZA",
    "q_value", "q_value_reaction", "is_exothermic",
    "check_conservation", "q_from_binding_energies",
    "q_value_excited", "threshold_energy_naive",
    "coulomb_barrier_mev",
]

# --- constants ---------------------------------------------------------------
M_N_U = 1.0086649156        # neutron, Table A.1
M_H_U = 1.0078250321        # neutral 1H atom, Appendix B
M_E_U = 5.48579909e-4       # electron
U_MEV = 931.494043          # MeV per u

ELEMENTS = (
    "n H He Li Be B C N O F Ne Na Mg Al Si P S Cl Ar K Ca Sc Ti V Cr Mn Fe Co Ni "
    "Cu Zn Ga Ge As Se Br Kr Rb Sr Y Zr Nb Mo Tc Ru Rh Pd Ag Cd In Sn Sb Te I Xe "
    "Cs Ba La Ce Pr Nd Pm Sm Eu Gd Tb Dy Ho Er Tm Yb Lu Hf Ta W Re Os Ir Pt Au Hg "
    "Tl Pb Bi Po At Rn Fr Ra Ac Th Pa U Np Pu Am Cm Bk Cf Es Fm Md No Lr Rf Db Sg "
    "Bh Hs Mt Ds Rg"
).split()
Z_OF = {el: i for i, el in enumerate(ELEMENTS)}

# Shorthand used inside the (x,y) notation.  Each maps to (Z, A) of the
# *neutral atom* that S&F's rule substitutes for the bare particle, except the
# neutron and gamma which carry no charge.
PARTICLES = {
    "n": (0, 1),        # neutron
    "p": (1, 1),        # proton  -> 1H atom
    "d": (1, 2),        # deuteron -> 2H atom
    "t": (1, 3),        # triton  -> 3H atom
    "h": (2, 3),        # helion  -> 3He atom
    "a": (2, 4),        # alpha   -> 4He atom
    "alpha": (2, 4),
    "g": None,          # gamma: massless
    "gamma": None,
}

_CACHE = None


def _csv_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "data_tables", "B1_atomic_masses.csv"))


def load_atomic_masses(path=None):
    """{(Z, A): atomic_mass_u} from the extracted Appendix B.  Cached."""
    global _CACHE
    if _CACHE is not None and path is None:
        return _CACHE
    table = {}
    with open(path or _csv_path(), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[(int(row["Z"]), int(row["A"]))] = float(row["atomic_mass_u"])
    if path is None:
        _CACHE = table
    return table


def atomic_mass(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


# --- notation ----------------------------------------------------------------

_NUC = re.compile(r"^\s*(\d{1,3})\s*([A-Z][a-z]?)\s*$")


def parse_nuclide(text):
    """'235U' -> (235, 92).  Also accepts 'U235' and 'U-235'."""
    s = str(text).strip()
    m = _NUC.match(s)
    if not m:
        m2 = re.match(r"^\s*([A-Z][a-z]?)\s*-?\s*(\d{1,3})\s*$", s)
        if not m2:
            raise ValueError("cannot parse nuclide %r" % (text,))
        sym, A = m2.group(1), int(m2.group(2))
    else:
        A, sym = int(m.group(1)), m.group(2)
    if sym not in Z_OF:
        raise ValueError("unknown element symbol %r" % (sym,))
    return A, Z_OF[sym]


def format_nuclide(A, Z):
    """(4, 2) -> '4He'."""
    if not (0 <= Z < len(ELEMENTS)):
        raise ValueError("no element with Z=%r" % (Z,))
    return "%d%s" % (A, ELEMENTS[Z])


def species_ZA(spec):
    """(A, Z) for a nuclide string or a particle shorthand; None for a gamma."""
    if isinstance(spec, (tuple, list)):
        return int(spec[0]), int(spec[1])
    key = str(spec).strip()
    if key in PARTICLES:
        p = PARTICLES[key]
        if p is None:
            return None
        return p[1], p[0]
    return parse_nuclide(key)


def species_mass_u(spec, table=None):
    """Rest mass in u of a species, using the neutral-atom substitution.

    A gamma has zero mass.  A bare proton is charged to 1H, an alpha to 4He, and
    so on -- which is exactly what makes the electrons cancel in `q_value`."""
    za = species_ZA(spec)
    if za is None:
        return 0.0
    A, Z = za
    if (A, Z) == (1, 0):
        return M_N_U
    return atomic_mass(A, Z, table)


_REACTION = re.compile(r"^\s*([^\s(]+)\s*\(\s*([^,]+?)\s*,\s*([^)]+?)\s*\)\s*(\S+)\s*$")


def parse_reaction(text):
    """'9Be(a,n)12C' -> (['9Be','a'], ['n','12C']) as (reactants, products)."""
    m = _REACTION.match(str(text))
    if not m:
        raise ValueError("cannot parse reaction %r (expected 'X(x,y)Y')" % (text,))
    X, x, y, Y = m.groups()
    return [X, x], [y, Y]


# --- conservation  [S&F §4.7, printed p. 91] --------------------------------

def check_conservation(reactants, products):
    """Verify that nucleon number and charge balance.

    Returns (dA, dZ) = (products - reactants); both must be zero.  Gammas
    contribute nothing.  Note this counts *nuclear* charge: the neutral-atom
    substitution used for masses keeps electrons balanced automatically as long
    as Z is conserved, which is why beta decay (~NE-05) needs separate care."""
    def tally(specs):
        A = Z = 0
        for s in specs:
            za = species_ZA(s)
            if za is None:
                continue
            A += za[0]
            Z += za[1]
        return A, Z
    aR, zR = tally(reactants)
    aP, zP = tally(products)
    return aP - aR, zP - zR


# --- Q-values  [S&F Eqs. (4.17)-(4.19), printed pp. 90-91] ------------------

def q_value(reactants, products, table=None, strict=True):
    """Q in MeV for reactants -> products  [Eq. (4.18)]:

        Q = (sum of reactant rest masses - sum of product rest masses) c^2 .

    Species may be nuclide strings ('9Be'), particle shorthands ('a', 'n', 'p'),
    or (A, Z) tuples.  With `strict`, nucleon number and charge must balance."""
    if strict:
        dA, dZ = check_conservation(reactants, products)
        if (dA, dZ) != (0, 0):
            raise ValueError("reaction does not conserve (A, Z): dA=%d dZ=%d" % (dA, dZ))
    mR = sum(species_mass_u(s, table) for s in reactants)
    mP = sum(species_mass_u(s, table) for s in products)
    return (mR - mP) * U_MEV


def q_value_reaction(text, table=None, strict=True):
    """Q for a reaction written as 'X(x,y)Y', e.g. '9Be(a,n)12C'."""
    reactants, products = parse_reaction(text)
    return q_value(reactants, products, table, strict)


def is_exothermic(reactants, products, table=None):
    """True when Q > 0 -- rest mass is converted into kinetic energy."""
    return q_value(reactants, products, table) > 0.0


def q_from_binding_energies(reactants, products, table=None):
    """Q computed as a difference of binding energies rather than of masses.

    Q = sum BE(products) - sum BE(reactants).  Algebraically identical to
    `q_value` whenever nucleons are conserved, and a useful cross-check --
    it is the form that makes the B/A curve of ~NE-03 the driver of the
    energetics."""
    def total_be(specs):
        tot = 0.0
        for s in specs:
            za = species_ZA(s)
            if za is None:
                continue
            A, Z = za
            if A == 1:                      # a free nucleon has no binding energy
                continue
            M = species_mass_u(s, table)
            tot += (Z * M_H_U + (A - Z) * M_N_U - M) * U_MEV
        return tot
    return total_be(products) - total_be(reactants)


def q_value_excited(reactants, products, excitation_mev, table=None):
    """Q when a product is left in an excited state  [S&F §4.8, printed p. 93].

    An excited nucleus is heavier than its ground state by the excitation
    energy, so Q is reduced by exactly that amount."""
    if excitation_mev < 0:
        raise ValueError("excitation energy must be non-negative")
    return q_value(reactants, products, table) - excitation_mev


# --- thresholds and barriers  (previewing ~NE-08) ---------------------------

def threshold_energy_naive(reactants, products, table=None):
    """|Q| for an endothermic reaction: the *minimum conceivable* incident
    kinetic energy, ignoring the recoil that momentum conservation forces.

    This is deliberately the naive value.  The true kinematic threshold is
    larger by the factor (1 + m_x/m_X); ~NE-08 derives it.  Returns 0 for an
    exothermic reaction."""
    Q = q_value(reactants, products, table)
    return 0.0 if Q >= 0 else -Q


def coulomb_barrier_mev(A1, Z1, A2, Z2, r0_fm=1.2):
    """Coulomb barrier height (MeV) for two nuclei in contact,

        V = Z1 Z2 e^2 / (4 pi eps0 R),   R = r0 (A1^(1/3) + A2^(1/3)),

    using e^2/(4 pi eps0) = 1.43996 MeV fm and the nuclear radius coefficient
    r0 = 1.2 fm of S&F Eq. (1.7).  Together these give the 1.20 MeV numerator of
    S&F Eq. (6.19); ~NE-08 reproduces the book's Example 6.1 table with it.
    A charged projectile must have
    roughly this much energy before it can reach the nucleus at all, whatever
    the sign of Q -- which is why exothermic charged-particle reactions still
    need accelerators (~NE-08, ~NE-10)."""
    if min(A1, A2) < 1 or min(Z1, Z2) < 0:
        raise ValueError("invalid nuclide")
    R = r0_fm * (A1 ** (1.0 / 3.0) + A2 ** (1.0 / 3.0))
    return 1.43996 * Z1 * Z2 / R


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-04  Q-values\n")

    print("  Example 4.4 (printed p. 92):")
    for rx in ("9Be(a,n)12C", "16O(n,a)13C"):
        Q = q_value_reaction(rx, t)
        print("    %-14s Q = %+8.4f MeV   %s"
              % (rx, Q, "exothermic" if Q > 0 else "endothermic"))

    print("\n  the charge-conservation trap (printed p. 92), 16O(n,p)16N:")
    right = q_value(["n", "16O"], ["16N", "p"], t)
    wrong = (M_N_U + atomic_mass(16, 8, t)
             - atomic_mass(16, 7, t) - (M_H_U - M_E_U)) * U_MEV
    print("    with neutral-atom substitution : Q = %+8.4f MeV" % right)
    print("    using a bare proton mass       : Q = %+8.4f MeV" % wrong)
    print("    difference = one electron mass = %.4f MeV" % (M_E_U * U_MEV))

    print("\n  fusion reactions (S&F Ch. 4 Prob. 5)")
    for rx in ("2H(d,n)3He", "3H(d,n)4He"):
        print("    %-14s Q = %+8.4f MeV" % (rx, q_value_reaction(rx, t)))

    print("\n  Q from masses vs Q from binding energies (must agree)")
    for rx in ("9Be(a,n)12C", "2H(d,n)3He", "16O(n,a)13C"):
        r, p = parse_reaction(rx)
        print("    %-14s  masses %+8.4f   binding %+8.4f"
              % (rx, q_value(r, p, t), q_from_binding_energies(r, p, t)))

    print("\n  an excited product costs exactly its excitation energy")
    base = q_value_reaction("9Be(a,n)12C", t)
    for ex in (0.0, 4.44, 7.65):
        print("    12C at %.2f MeV excitation:  Q = %+8.4f MeV"
              % (ex, q_value_excited(*parse_reaction("9Be(a,n)12C"), excitation_mev=ex, table=t)))

    print("\n  Coulomb barriers -- why exothermic is not the same as easy")
    for (A1, Z1, A2, Z2, lab) in [(2, 1, 3, 1, "d + t"), (4, 2, 9, 4, "alpha + 9Be"),
                                  (1, 1, 12, 6, "p + 12C"), (4, 2, 238, 92, "alpha + 238U")]:
        print("    %-14s V_c = %7.2f MeV" % (lab, coulomb_barrier_mev(A1, Z1, A2, Z2)))


if __name__ == "__main__":
    _demo()
