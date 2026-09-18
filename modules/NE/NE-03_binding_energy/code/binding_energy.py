"""NE-03  Binding energy, the mass defect, and nucleon separation energies.

Nuclear Science & Engineering trunk, module NE-03 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 4.1-4.3 (printed pp. 80-88).  Pure stdlib; measured masses come
from ../../data_tables/B1_atomic_masses.csv (Appendix B).

A nucleus weighs less than its parts.  The deficit, converted by E = mc^2, is the
binding energy -- the work needed to pull the nucleus apart into free nucleons:

    BE = [Z m_p + (A-Z) m_n - m(A,Z)] c^2        (nuclear masses)

Appendix B tabulates *atomic* masses, not nuclear ones, so the working form adds
Z electrons to each side.  Z protons become Z hydrogen atoms, the electron
binding energies very nearly cancel, and

    BE = [Z M(1H) + (A-Z) m_n - M(A,Z)] c^2      (atomic masses, S&F Eq. 4.12)

The *average* binding energy BE/A peaks near A=56, which is why both fusion and
fission release energy (~NE-09, ~NE-10).  The energy to remove one nucleon --
the separation energy -- is a difference of binding energies,

    S_n(A,Z) = BE(A,Z) - BE(A-1,Z),

and it is far more revealing than BE/A: it staggers by several MeV between even
and odd neutron number (pairing) and drops sharply just past a magic number
(shell closure).  Separation energies are the nuclear analogue of ionization
energies (~NE-01), and S_n is what decides whether a neutron can be captured
exothermically, which is where reactor physics starts (~NE-13, ~NE-19).
"""

import csv
import math
import os

__all__ = [
    "M_N_U", "M_H_U", "M_E_U", "M_P_U", "U_MEV", "MAGIC_NUMBERS",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "atomic_to_nuclear_mass", "mass_excess_mev", "mass_defect_u",
    "binding_energy", "binding_energy_per_nucleon",
    "neutron_separation_energy", "proton_separation_energy",
    "two_neutron_separation_energy", "alpha_separation_energy",
    "binding_energy_curve", "most_bound_nuclide",
    "pairing_stagger", "electron_binding_fraction",
]

# --- constants (Table A.1, printed p. 555; Appendix B for M(1H)) ------------
M_N_U = 1.0086649156        # neutron rest mass, u
M_P_U = 1.0072764669        # proton rest mass, u
M_E_U = 5.48579909e-4       # electron rest mass, u
M_H_U = 1.0078250321        # neutral 1H atom, u  (Appendix B)
U_MEV = 931.494043          # MeV per u

MAGIC_NUMBERS = (2, 8, 20, 28, 50, 82, 126)

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
    """Neutral-atom rest mass M(A,Z) in u.  KeyError if not tabulated."""
    _check(A, Z)
    t = load_atomic_masses() if table is None else table
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


# --- masses  [S&F Eq. (4.8), printed p. 81] ---------------------------------

def atomic_to_nuclear_mass(A, Z, table=None):
    """Nuclear mass from the atomic mass, m = M - Z m_e + BE_Ze/c^2.

    The electron binding term is dropped: for hydrogen it is 13.6 eV, i.e.
    1.4e-8 u, negligible beside the electron mass itself (5.5e-4 u)."""
    return atomic_mass(A, Z, table) - Z * M_E_U


def mass_excess_mev(A, Z, table=None):
    """Mass excess (M - A) c^2 in MeV -- the usual compact way to tabulate masses."""
    return (atomic_mass(A, Z, table) - A) * U_MEV


def mass_defect_u(A, Z, table=None):
    """Mass defect BE/c^2 in u: how much lighter the nuclide is than its parts."""
    return Z * M_H_U + (A - Z) * M_N_U - atomic_mass(A, Z, table)


# --- binding energy  [S&F Eq. (4.12), printed p. 81] ------------------------

def binding_energy(A, Z, table=None):
    """Total binding energy BE (MeV) from measured atomic masses:

        BE = [Z M(1H) + (A-Z) m_n - M(A,Z)] c^2 ."""
    return mass_defect_u(A, Z, table) * U_MEV


def binding_energy_per_nucleon(A, Z, table=None):
    """BE/A in MeV per nucleon."""
    _check(A, Z)
    return binding_energy(A, Z, table) / A


# --- separation energies  [S&F Eqs. (4.13)-(4.14), printed p. 87] ----------

def neutron_separation_energy(A, Z, table=None):
    """S_n = BE(A,Z) - BE(A-1,Z), the work to remove one neutron (MeV).

    Equivalently [Eq. (4.13)]  S_n = [M(A-1,Z) + m_n - M(A,Z)] c^2 ."""
    _check(A, Z)
    if A - 1 < Z:
        raise ValueError("removing a neutron would leave fewer than Z nucleons")
    return binding_energy(A, Z, table) - binding_energy(A - 1, Z, table)


def proton_separation_energy(A, Z, table=None):
    """S_p = BE(A,Z) - BE(A-1,Z-1), the work to remove one proton (MeV)."""
    _check(A, Z)
    if Z < 1:
        raise ValueError("no proton to remove")
    return binding_energy(A, Z, table) - binding_energy(A - 1, Z - 1, table)


def two_neutron_separation_energy(A, Z, table=None):
    """S_2n = BE(A,Z) - BE(A-2,Z).  Removing a *pair* cancels the odd-even
    stagger, so S_2n is the smooth quantity in which shell closures stand out."""
    _check(A, Z)
    return binding_energy(A, Z, table) - binding_energy(A - 2, Z, table)


def alpha_separation_energy(A, Z, table=None):
    """S_alpha = BE(A,Z) - BE(A-4,Z-2) - BE(4,2).

    When this is *negative* the nuclide is unstable against alpha emission, and
    -S_alpha is the decay Q-value (~NE-04, ~NE-05)."""
    _check(A, Z)
    return (binding_energy(A, Z, table) - binding_energy(A - 4, Z - 2, table)
            - binding_energy(4, 2, table))


# --- the B/A curve -----------------------------------------------------------

def binding_energy_curve(table=None, z_tolerance=None):
    """[(A, Z, BE/A), ...] for every tabulated nuclide, sorted by A.

    With `z_tolerance` set, keep only nuclides within that many protons of the
    most bound Z at each A -- i.e. the floor of the valley of stability."""
    t = load_atomic_masses() if table is None else table
    best = {}
    out = []
    for (Z, A) in t:
        if A < 2 or Z < 1:
            continue
        b = binding_energy_per_nucleon(A, Z, t)
        out.append((A, Z, b))
        if A not in best or b > best[A][1]:
            best[A] = (Z, b)
    if z_tolerance is not None:
        out = [r for r in out if abs(r[1] - best[r[0]][0]) <= z_tolerance]
    return sorted(out)


def most_bound_nuclide(table=None):
    """(A, Z, BE/A) of the most tightly bound nuclide -- the top of the curve."""
    return max(binding_energy_curve(table), key=lambda r: r[2])


# --- systematics -------------------------------------------------------------

def pairing_stagger(A, Z, table=None):
    """S_n(A,Z) - S_n(A+1,Z), in MeV.

    Adding a neutron to an odd-N nucleus completes a pair and releases extra
    energy, so S_n alternates high/low along an isotope chain. This difference
    is roughly 2 a_p/sqrt(A) ~ 2-3 MeV and is the clearest direct evidence for
    the pairing term of ~NE-02."""
    return (neutron_separation_energy(A, Z, table)
            - neutron_separation_energy(A + 1, Z, table))


def electron_binding_fraction(A, Z, ionization_ev, table=None):
    """Ratio of the atom's electron binding energy to its nuclear binding energy.

    S&F drop the electron term when converting nuclear to atomic masses
    (printed p. 81); this quantifies how safe that is -- about 1e-6 for
    hydrogen, and smaller still for heavy nuclides relative to their BE."""
    return (ionization_ev * 1e-6) / binding_energy(A, Z, table)


# --- helpers -----------------------------------------------------------------

def _check(A, Z):
    if A != int(A) or A < 1:
        raise ValueError("mass number A must be a positive integer")
    if Z != int(Z) or Z < 0 or Z > A:
        raise ValueError("atomic number Z must be an integer in [0, A]")


def _fmt(A, Z, symbols={}):
    return "%d/%d" % (A, Z)


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-03  binding energy and separation energies\n")
    print("  mass defect and binding energy, from Appendix B atomic masses")
    print("   nuclide      M (u)      defect (u)    BE (MeV)   BE/A (MeV)")
    for A, Z, name in [(2, 1, "2H"), (4, 2, "4He"), (12, 6, "12C"), (16, 8, "16O"),
                       (56, 26, "56Fe"), (208, 82, "208Pb"), (235, 92, "235U"),
                       (238, 92, "238U")]:
        print("   %-8s %11.6f %11.6f %11.2f %10.3f"
              % (name, atomic_mass(A, Z, t), mass_defect_u(A, Z, t),
                 binding_energy(A, Z, t), binding_energy_per_nucleon(A, Z, t)))

    A, Z, b = most_bound_nuclide(t)
    print("\n  most tightly bound nuclide: A=%d Z=%d at %.4f MeV/nucleon" % (A, Z, b))

    print("\n  neutron separation energy along the oxygen isotopes (Z=8)")
    print("     A    N   S_n (MeV)   parity of N")
    for A in range(15, 21):
        if not has_nuclide(A, 8, t) or not has_nuclide(A - 1, 8, t):
            continue
        N = A - 8
        print("   %3d  %3d  %9.2f   %s"
              % (A, N, neutron_separation_energy(A, 8, t), "even" if N % 2 == 0 else "odd"))

    print("\n  shell closure seen in S_n: N=82 and N=126")
    for Z, A, lab in [(58, 140, "140Ce (N=82)"), (58, 141, "141Ce (N=83)"),
                      (82, 208, "208Pb (N=126)"), (82, 209, "209Pb (N=127)")]:
        if has_nuclide(A, Z, t) and has_nuclide(A - 1, Z, t):
            print("   %-16s S_n = %6.2f MeV" % (lab, neutron_separation_energy(A, Z, t)))

    print("\n  alpha separation energy turns negative for heavy nuclides")
    print("   (negative means alpha decay is exothermic -- see ~NE-04, ~NE-05)")
    for A, Z, name in [(56, 26, "56Fe"), (120, 50, "120Sn"), (150, 62, "150Sm"),
                       (208, 82, "208Pb"), (226, 88, "226Ra"), (238, 92, "238U")]:
        if has_nuclide(A - 4, Z - 2, t):
            print("   %-8s S_alpha = %+7.2f MeV" % (name, alpha_separation_energy(A, Z, t)))

    print("\n  electron binding is negligible: for 1H it is %.2e of the deuteron BE"
          % electron_binding_fraction(2, 1, 13.6, t))


if __name__ == "__main__":
    _demo()
