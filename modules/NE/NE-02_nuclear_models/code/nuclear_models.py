"""NE-02  Nuclear models -- nuclear size, the liquid drop model, the line of
stability, mass parabolas, and the shell-model magic numbers.

Nuclear Science & Engineering trunk, module NE-02 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 3.2 "Models of the Nucleus" (printed pp. 63-78).  Pure numpy +
stdlib; the measured masses it validates against are read from
../../data_tables/B1_atomic_masses.csv (Appendix B).

Electron scattering shows nuclear matter has essentially constant density, so
R = 1.1 A^(1/3) fm and the nucleus behaves like an incompressible drop whose
nucleons bind only to their neighbours.  That picture gives the semi-empirical
mass formula: a bulk term proportional to A, minus corrections for the
under-bound surface, Coulomb repulsion among protons, neutron-proton asymmetry,
and nucleon pairing,

    BE = a_v A - a_s A^(2/3) - a_c Z^2/A^(1/3) - a_a (A-2Z)^2/A - a_p/sqrt(A).

Minimising the resulting mass over Z at fixed A predicts the line of stability;
plotting it over an isobar gives the mass parabolas that explain which nuclides
beta-decay in which direction (~NE-05).  What the model cannot explain -- the
magic numbers 2, 8, 20, 28, 50, 82, 126 -- is what forces the shell model.

Sign convention (S&F Eq. 3.16, printed p. 73): a_p is *positive* for odd-odd
nuclei, zero for odd-even, and *negative* for even-even, and it enters BE as
-a_p/sqrt(A).  So even-even nuclei gain binding energy and odd-odd nuclei lose
it.  Getting this sign backwards inverts the mass parabolas.
"""

import csv
import math
import os

__all__ = [
    "A_V", "A_S", "A_C", "A_A", "A_P", "R0_FM",
    "M_P_U", "M_N_U", "M_H_U", "M_E_U", "U_MEV", "MAGIC_NUMBERS",
    "nuclear_radius", "nuclear_volume", "nucleon_number_density",
    "pairing_sign", "pairing_term", "parity_class",
    "semf_terms", "semf_binding_energy", "semf_binding_energy_per_nucleon",
    "semf_nuclear_mass_u", "semf_atomic_mass_u", "semf_mass_excess_mev",
    "most_stable_Z", "most_stable_Z_rounded", "isobar_masses",
    "is_magic", "is_doubly_magic", "magic_gap",
    "load_atomic_masses", "measured_binding_energy",
]

# --- liquid drop constants [Wapstra 1958], S&F printed p. 73, in MeV ---------
A_V = 15.835        # volume
A_S = 18.33         # surface
A_C = 0.714         # Coulomb
A_A = 23.20         # asymmetry
A_P = 11.2          # pairing magnitude

R0_FM = 1.1         # R = R0 A^(1/3) fm  [S&F Eq. (3.13), printed p. 64]

# --- masses, in u, from Table A.1 / Appendix B ------------------------------
M_P_U = 1.0072764669        # proton
M_N_U = 1.0086649156        # neutron
M_E_U = 5.48579909e-4       # electron
M_H_U = 1.0078250321        # neutral 1H atom (Appendix B)
U_MEV = 931.494043          # MeV per u

MAGIC_NUMBERS = (2, 8, 20, 28, 50, 82, 126)


# --- nuclear size  [S&F §3.2.1, Eq. (3.13)] ---------------------------------

def nuclear_radius(A):
    """Nuclear radius  R = 1.1 A^(1/3) fm  [Eq. (3.13), printed p. 64]."""
    _check_A(A)
    return R0_FM * A ** (1.0 / 3.0)


def nuclear_volume(A):
    """Volume (fm^3) of the equivalent sphere, (4/3) pi R^3 -- proportional to A."""
    return 4.0 / 3.0 * math.pi * nuclear_radius(A) ** 3


def nucleon_number_density(A):
    """Nucleons per fm^3, A / V.  Essentially constant (~0.18 fm^-3) for all A --
    the observation that motivates the incompressible-drop picture."""
    return A / nuclear_volume(A)


# --- pairing ----------------------------------------------------------------

def parity_class(A, Z):
    """'even-even', 'odd-odd', or 'odd-even' for the (N, Z) parity combination."""
    _check_AZ(A, Z)
    N = A - Z
    if Z % 2 == 0 and N % 2 == 0:
        return "even-even"
    if Z % 2 == 1 and N % 2 == 1:
        return "odd-odd"
    return "odd-even"


def pairing_sign(A, Z):
    """a_p / A_P: +1 for odd-odd, -1 for even-even, 0 otherwise [printed p. 73]."""
    cls = parity_class(A, Z)
    return {"odd-odd": 1.0, "even-even": -1.0, "odd-even": 0.0}[cls]


def pairing_term(A, Z):
    """The pairing contribution to BE, -a_p/sqrt(A), in MeV.

    Positive (more bound) for even-even, negative for odd-odd, zero otherwise."""
    return -pairing_sign(A, Z) * A_P / math.sqrt(A)


# --- the semi-empirical mass formula  [S&F Eq. (3.16), printed p. 73] -------

def semf_terms(A, Z):
    """The five binding-energy contributions, in MeV, as a dict.

    volume  = +a_v A
    surface = -a_s A^(2/3)
    coulomb = -a_c Z^2 / A^(1/3)
    asymmetry = -a_a (A - 2Z)^2 / A
    pairing = -a_p / sqrt(A)

    They sum to the total binding energy."""
    _check_AZ(A, Z)
    return {
        "volume": A_V * A,
        "surface": -A_S * A ** (2.0 / 3.0),
        "coulomb": -A_C * Z ** 2 / A ** (1.0 / 3.0),
        "asymmetry": -A_A * (A - 2.0 * Z) ** 2 / A,
        "pairing": pairing_term(A, Z),
    }


def semf_binding_energy(A, Z):
    """Total binding energy BE (MeV) predicted by the liquid drop model."""
    return sum(semf_terms(A, Z).values())


def semf_binding_energy_per_nucleon(A, Z):
    """BE/A in MeV per nucleon -- the curve that peaks near iron."""
    return semf_binding_energy(A, Z) / A


def semf_nuclear_mass_u(A, Z):
    """Nuclear (not atomic) mass in u  [Eq. (3.16)]:

        m = Z m_p + (A-Z) m_n - BE/c^2 ."""
    _check_AZ(A, Z)
    return Z * M_P_U + (A - Z) * M_N_U - semf_binding_energy(A, Z) / U_MEV


def semf_atomic_mass_u(A, Z):
    """Neutral-atom mass in u  [S&F printed pp. 73-74]:

        M = Z M(1H) + (A-Z) m_n - BE/c^2 .

    Adding Z electrons to both sides of the nuclear formula replaces Z protons
    by Z hydrogen atoms; the electron binding energies (eV) are negligible
    against the nuclear binding energy (MeV) and largely cancel."""
    _check_AZ(A, Z)
    return Z * M_H_U + (A - Z) * M_N_U - semf_binding_energy(A, Z) / U_MEV


def semf_mass_excess_mev(A, Z):
    """Mass excess (M - A) in MeV, the usual tabulated form."""
    return (semf_atomic_mass_u(A, Z) - A) * U_MEV


# --- the line of stability  [S&F Eqs. (3.17)-(3.18), printed p. 73] ---------

def most_stable_Z(A):
    """Z minimising the nuclear mass at fixed A  [Eq. (3.18)]:

        Z(A) = (A/2) * [1 + (m_n - m_p)c^2/(4 a_a)] / [1 + a_c A^(2/3)/(4 a_a)] .

    Returned as a real number; the physical nuclide is the nearest integer.
    For small A this tends to A/2 (equal N and Z); the A^(2/3) in the
    denominator -- Coulomb repulsion -- pulls it below A/2 as A grows, which is
    why heavy stable nuclides are neutron rich."""
    _check_A(A)
    dmc2 = (M_N_U - M_P_U) * U_MEV          # 1.293 MeV
    return (A / 2.0) * (1.0 + dmc2 / (4.0 * A_A)) / (1.0 + A_C * A ** (2.0 / 3.0) / (4.0 * A_A))


def most_stable_Z_rounded(A):
    """Nearest integer Z to `most_stable_Z(A)`, clamped to [1, A]."""
    return max(1, min(int(A), int(round(most_stable_Z(A)))))


def isobar_masses(A, z_lo=None, z_hi=None, atomic=True):
    """[(Z, mass_u), ...] across an isobar -- the data behind a mass parabola.

    With `atomic=True` the neutral-atom mass is returned. Even-even and odd-odd
    members lie on two distinct curves separated by 2 a_p/sqrt(A), which is what
    makes some A have two stable nuclides (see `~NE-05`)."""
    _check_A(A)
    z0 = 1 if z_lo is None else z_lo
    z1 = int(A) if z_hi is None else z_hi
    f = semf_atomic_mass_u if atomic else semf_nuclear_mass_u
    return [(Z, f(A, Z)) for Z in range(int(z0), int(z1) + 1)]


# --- magic numbers  [S&F §3.2.7, printed p. 75] -----------------------------

def is_magic(n):
    """True if n is one of 2, 8, 20, 28, 50, 82, 126."""
    return int(n) in MAGIC_NUMBERS


def is_doubly_magic(A, Z):
    """True when both Z and N = A - Z are magic (4He, 16O, 40Ca, 48Ca, 208Pb...)."""
    _check_AZ(A, Z)
    return is_magic(Z) and is_magic(A - Z)


def magic_gap(A, Z):
    """Distance of (Z, N) from the nearest magic numbers, as (dZ, dN).

    The liquid drop model is smooth in A and Z, so it cannot produce the extra
    binding seen at these shell closures; the size of the residual is roughly
    what the shell model has to supply."""
    _check_AZ(A, Z)
    N = A - Z
    dz = min(abs(Z - m) for m in MAGIC_NUMBERS)
    dn = min(abs(N - m) for m in MAGIC_NUMBERS)
    return dz, dn


# --- measured masses, from the extracted Appendix B -------------------------

_MASS_CACHE = None


def _mass_csv_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "data_tables", "B1_atomic_masses.csv"))


def load_atomic_masses(path=None):
    """{(Z, A): atomic_mass_u} from ../../data_tables/B1_atomic_masses.csv.

    That file is the extraction of the book's Appendix B (Audi-Wapstra 1995);
    see data_tables/README.md.  Cached after the first call."""
    global _MASS_CACHE
    if _MASS_CACHE is not None and path is None:
        return _MASS_CACHE
    p = path or _mass_csv_path()
    table = {}
    with open(p, newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[(int(row["Z"]), int(row["A"]))] = float(row["atomic_mass_u"])
    if path is None:
        _MASS_CACHE = table
    return table


def measured_binding_energy(A, Z, table=None):
    """Binding energy (MeV) from the *measured* atomic mass:

        BE = [Z M(1H) + (A-Z) m_n - M(A,Z)] c^2 .

    Raises KeyError if the nuclide is not in the mass table."""
    _check_AZ(A, Z)
    t = load_atomic_masses() if table is None else table
    M = t[(int(Z), int(A))]
    return (Z * M_H_U + (A - Z) * M_N_U - M) * U_MEV


# --- helpers ----------------------------------------------------------------

def _check_A(A):
    if A != int(A) or A < 1:
        raise ValueError("mass number A must be a positive integer")


def _check_AZ(A, Z):
    _check_A(A)
    if Z != int(Z) or Z < 0 or Z > A:
        raise ValueError("atomic number Z must be an integer in [0, A]")


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-02  the liquid drop model\n")
    print("  nuclear matter is incompressible:")
    print("     A      R (fm)   nucleons/fm^3")
    for A in (4, 27, 56, 120, 208, 238):
        print("   %4d   %7.2f   %11.4f" % (A, nuclear_radius(A), nucleon_number_density(A)))

    print("\n  binding energy per nucleon, liquid drop vs measured (Appendix B)")
    print("   nuclide     SEMF      measured    error     parity")
    try:
        for A, Z, name in [(4, 2, "4He"), (16, 8, "16O"), (40, 20, "40Ca"),
                           (56, 26, "56Fe"), (120, 50, "120Sn"), (208, 82, "208Pb"),
                           (235, 92, "235U"), (238, 92, "238U")]:
            semf = semf_binding_energy_per_nucleon(A, Z)
            meas = measured_binding_energy(A, Z) / A
            print("   %-8s %8.3f  %10.3f  %+8.3f    %s"
                  % (name, semf, meas, semf - meas, parity_class(A, Z)))
    except (OSError, KeyError) as exc:
        print("   (mass table unavailable: %s)" % exc)

    print("\n  the line of stability, Z(A) from Eq. (3.18)")
    print("     A    Z(A)   round   A/2   N/Z")
    for A in (20, 56, 100, 150, 208, 238):
        z = most_stable_Z(A)
        zr = most_stable_Z_rounded(A)
        print("   %4d  %6.2f  %5d  %5.1f  %5.3f" % (A, z, zr, A / 2, (A - zr) / zr))

    print("\n  the A=110 isobar (S&F Fig. 3.13): atomic mass less 109.9 u, in mu")
    print("     Z   parity        mass-109.9 (mu)")
    for Z, m in isobar_masses(110, 43, 51):
        print("   %3d   %-11s %12.2f" % (Z, parity_class(110, Z), (m - 109.9) * 1000))
    print("   most stable Z from Eq. (3.18): %.2f" % most_stable_Z(110))

    print("\n  doubly magic nuclides the drop model cannot explain:")
    for A, Z, name in [(4, 2, "4He"), (16, 8, "16O"), (40, 20, "40Ca"),
                       (48, 20, "48Ca"), (208, 82, "208Pb")]:
        try:
            resid = measured_binding_energy(A, Z) - semf_binding_energy(A, Z)
        except (OSError, KeyError):
            resid = float("nan")
        print("   %-7s Z=%3d N=%3d  doubly magic=%-5s  measured - SEMF = %+6.2f MeV"
              % (name, Z, A - Z, is_doubly_magic(A, Z), resid))


if __name__ == "__main__":
    _demo()
