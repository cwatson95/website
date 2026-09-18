"""NE-01  Atomic models -- Rutherford scattering, the Bohr atom, hydrogen spectra.

Nuclear Science & Engineering trunk, module NE-01 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Section 3.1 "Development of the Modern Atom Model" (printed pp. 54-63).
Pure numpy + stdlib.

The Bohr atom is built from three postulates: the electron orbits classically,
its angular momentum is quantized as L = n h/2pi, and light is emitted only on
transitions between allowed orbits.  Balancing the Coulomb attraction against the
centripetal requirement,

    m_e v^2 / r = Z e^2 / (4 pi eps0 r^2),      L = m_e v r = n h / 2pi,

fixes the orbit radius and speed, and hence the energy

    E_n = - m_e (Z e^2)^2 / (8 eps0^2 n^2 h^2) = -13.606 Z^2 / n^2  eV.

Transitions reproduce the empirical Rydberg formula 1/lambda = R (1/n0^2 - 1/n^2)
that had been fitted to hydrogen's spectrum decades earlier -- the model's whole
claim to fame.  Replacing m_e by the electron's reduced mass turns the
infinite-nucleus constant R_inf into the measured R_H.

All constants are the CODATA-2002 values the book tabulates in Table A.1, so
every number here reproduces the book's own arithmetic.
"""

import math

__all__ = [
    "C", "E_CHARGE", "M_E", "M_P", "H_PLANCK", "EPS0", "EV_PER_J",
    "R_INF", "R_H", "BOHR_RADIUS", "HARTREE_EV",
    "reduced_mass", "reduced_mass_ratio",
    "bohr_radius", "bohr_velocity", "bohr_energy", "bohr_angular_momentum",
    "bohr_orbital_period", "ionization_energy",
    "transition_energy", "transition_wavelength", "rydberg_wavelength",
    "rydberg_constant", "series_limit_wavelength", "SERIES_NAMES", "series_name",
    "fine_structure_constant", "is_nonrelativistic",
    "thomson_scattering_probability",
]

# --- CODATA 2002, exactly as printed in Table A.1 (printed p. 555) -----------
C = 2.99792458e8            # m/s      speed of light
E_CHARGE = 1.60217653e-19   # C        elementary charge
M_E = 9.1093826e-31         # kg       electron rest mass
M_P = 1.67262171e-27        # kg       proton rest mass
H_PLANCK = 6.6260693e-34    # J s      Planck constant
EPS0 = 8.854187817e-12      # F/m      electric constant
EV_PER_J = 1.0 / E_CHARGE   # eV per J


def _rydberg_from(mass):
    """R = m e^4 / (8 eps0^2 c h^3)  in m^-1  [Eq. (3.7), printed p. 60]."""
    return mass * E_CHARGE ** 4 / (8.0 * EPS0 ** 2 * C * H_PLANCK ** 3)


R_INF = _rydberg_from(M_E)                       # 1.0973732e7 m^-1
R_H = _rydberg_from(M_E * M_P / (M_E + M_P))     # 1.0967758e7 m^-1
BOHR_RADIUS = EPS0 * H_PLANCK ** 2 / (math.pi * M_E * E_CHARGE ** 2)   # 5.2918e-11 m
HARTREE_EV = M_E * E_CHARGE ** 4 / (8.0 * EPS0 ** 2 * H_PLANCK ** 2) * EV_PER_J  # 13.606 eV


# --- reduced mass  (printed p. 60) -------------------------------------------

def reduced_mass(m1, m2):
    """Reduced mass  mu = m1 m2 / (m1 + m2)  of a two-body system."""
    if m1 <= 0 or m2 <= 0:
        raise ValueError("masses must be positive")
    return m1 * m2 / (m1 + m2)


def reduced_mass_ratio(nuclear_mass=M_P):
    """mu_e / m_e for an electron bound to a nucleus of the given mass.

    For hydrogen this is 0.999455679; it is the factor that converts R_inf into
    the measured R_H.  (The book prints 0.999445568 on p. 60, which does not
    reproduce its own R_H -- see refs.md.)"""
    return reduced_mass(M_E, nuclear_mass) / M_E


def rydberg_constant(nuclear_mass=None):
    """Rydberg constant in m^-1.  With no argument, the infinite-nucleus value
    R_inf; given a nuclear mass, the finite-mass value (R_H for the proton)."""
    if nuclear_mass is None:
        return R_INF
    return _rydberg_from(reduced_mass(M_E, nuclear_mass))


# --- the Bohr orbits  [Eqs. (3.2)-(3.4), printed p. 59] ----------------------

def bohr_radius(n, Z=1, nuclear_mass=None):
    """Orbit radius  r_n = n^2 h^2 eps0 / (pi m Z e^2)  in metres.

    r_1 = 5.2918e-11 m for hydrogen -- the Bohr radius."""
    _check_n(n)
    m = M_E if nuclear_mass is None else reduced_mass(M_E, nuclear_mass)
    return n ** 2 * H_PLANCK ** 2 * EPS0 / (math.pi * m * Z * E_CHARGE ** 2)


def bohr_velocity(n, Z=1):
    """Orbit speed  v_n = Z e^2 / (2 eps0 n h)  in m/s.  v_1 = 2.188e6 m/s."""
    _check_n(n)
    return Z * E_CHARGE ** 2 / (2.0 * EPS0 * n * H_PLANCK)


def bohr_angular_momentum(n):
    """L = n h / (2 pi)  -- Bohr's second postulate [Eq. (3.3)]."""
    _check_n(n)
    return n * H_PLANCK / (2.0 * math.pi)


def bohr_energy(n, Z=1, nuclear_mass=None):
    """Total energy of orbit n, in eV  [Eq. (3.5), printed p. 60]:

        E_n = - m (Z e^2)^2 / (8 eps0^2 n^2 h^2) = -13.606 Z^2/n^2 eV.

    Negative: the electron is bound, and |E_n| is the work needed to free it."""
    _check_n(n)
    m = M_E if nuclear_mass is None else reduced_mass(M_E, nuclear_mass)
    joules = -m * (Z * E_CHARGE ** 2) ** 2 / (8.0 * EPS0 ** 2 * n ** 2 * H_PLANCK ** 2)
    return joules * EV_PER_J


def bohr_orbital_period(n, Z=1):
    """Classical orbital period  T = 2 pi r_n / v_n  in seconds."""
    return 2.0 * math.pi * bohr_radius(n, Z) / bohr_velocity(n, Z)


def ionization_energy(Z=1, n=1):
    """Energy (eV) to remove an electron from level n of a one-electron ion.

    ionization_energy(1) = 13.606 eV (hydrogen);
    ionization_energy(2) = 54.42 eV (He+, Example 3.1, printed p. 60)."""
    return -bohr_energy(n, Z)


# --- transitions and spectra  [Eqs. (3.6)-(3.7), printed p. 60] --------------

def transition_energy(n_lo, n_hi, Z=1, nuclear_mass=None):
    """Photon energy (eV) emitted on the transition n_hi -> n_lo, n_hi > n_lo."""
    _check_pair(n_lo, n_hi)
    return bohr_energy(n_hi, Z, nuclear_mass) - bohr_energy(n_lo, Z, nuclear_mass)


def transition_wavelength(n_lo, n_hi, Z=1, nuclear_mass=None):
    """Wavelength (m) of the photon emitted on n_hi -> n_lo, from E = hc/lambda."""
    dE = transition_energy(n_lo, n_hi, Z, nuclear_mass)
    return H_PLANCK * C / (dE * E_CHARGE)


def rydberg_wavelength(n_lo, n_hi, Z=1, R=R_H):
    """The empirical Rydberg formula  1/lambda = R Z^2 (1/n_lo^2 - 1/n_hi^2),
    [Eq. (3.1), printed p. 58].  Returns the wavelength in metres."""
    _check_pair(n_lo, n_hi)
    inv = R * Z ** 2 * (1.0 / n_lo ** 2 - 1.0 / n_hi ** 2)
    return 1.0 / inv


def series_limit_wavelength(n_lo, Z=1, R=R_H):
    """Short-wavelength limit of a series (n_hi -> infinity): lambda = n_lo^2/(R Z^2)."""
    _check_n(n_lo)
    return n_lo ** 2 / (R * Z ** 2)


SERIES_NAMES = {1: "Lyman", 2: "Balmer", 3: "Paschen", 4: "Brackett", 5: "Pfund"}


def series_name(n_lo):
    """Name of the hydrogen series terminating on level n_lo (Table 3.1, p. 59)."""
    return SERIES_NAMES.get(n_lo, "n_lo=%d" % n_lo)


# --- consistency of the non-relativistic treatment  (printed p. 60) ---------

def fine_structure_constant():
    """alpha = e^2 / (2 eps0 h c) = v_1/c for hydrogen, about 1/137."""
    return E_CHARGE ** 2 / (2.0 * EPS0 * H_PLANCK * C)


def is_nonrelativistic(n, Z=1, tol=0.01):
    """True when v_n/c < tol, i.e. classical mechanics is safe for this orbit.

    The book makes exactly this check for hydrogen's ground state, where
    v_1 = 2.187e6 m/s << c (printed p. 60)."""
    return bohr_velocity(n, Z) / C < tol


# --- the Geiger-Marsden result that killed the plum-pudding model -----------

def thomson_scattering_probability(phi_deg, phi_m_deg=1.0):
    """Thomson-model probability that an alpha scatters by at least phi:
    P = exp(-phi/phi_m) with phi_m ~ 1 degree (printed p. 58).

    At 90 degrees this gives ~1e-40, while Geiger and Marsden measured about
    1 in 8000 -- the discrepancy that forced Rutherford's nuclear atom."""
    if phi_deg < 0 or phi_m_deg <= 0:
        raise ValueError("angles must be positive")
    return math.exp(-phi_deg / phi_m_deg)


# --- helpers ----------------------------------------------------------------

def _check_n(n):
    if n != int(n) or n < 1:
        raise ValueError("principal quantum number must be a positive integer")


def _check_pair(n_lo, n_hi):
    _check_n(n_lo)
    _check_n(n_hi)
    if n_hi <= n_lo:
        raise ValueError("n_hi must exceed n_lo for an emission line")


# --- demo -------------------------------------------------------------------

def _demo():
    print("NE-01  the Bohr atom\n")
    print("  R_inf = %.7e m^-1     R_H = %.7e m^-1" % (R_INF, R_H))
    print("  book's R_H (printed p. 60) = 1.0967758e7 m^-1")
    print("  mu_e/m_e = %.9f\n" % reduced_mass_ratio())

    print("  hydrogen orbits")
    print("    n     r_n (m)      v_n (m/s)     E_n (eV)")
    for n in (1, 2, 3, 4):
        print("    %d   %10.4e   %10.4e   %9.4f"
              % (n, bohr_radius(n), bohr_velocity(n), bohr_energy(n)))

    print("\n  hydrogen series (transition n_hi -> n_lo), wavelengths in nm,")
    print("  using the reduced electron mass so these are the measured lines")
    for n_lo in (1, 2, 3):
        head = "    %-9s" % series_name(n_lo)
        lines = " ".join("%6.1f" % (transition_wavelength(n_lo, n, nuclear_mass=M_P) * 1e9)
                         for n in range(n_lo + 1, n_lo + 5))
        print("%s %s   limit %6.1f" % (head, lines,
                                       series_limit_wavelength(n_lo) * 1e9))

    print("\n  Balmer alpha (3->2): %.2f nm with the reduced mass, %.2f nm without;"
          % (transition_wavelength(2, 3, nuclear_mass=M_P) * 1e9,
             transition_wavelength(2, 3) * 1e9))
    print("  the book's Fig. 3.4 marks it at 656.3 nm -- only the first is right")
    print("  He+ ionization energy: %.2f eV   (Example 3.1)" % ionization_energy(2))
    print("  v_1/c = %.6f = alpha = 1/%.2f"
          % (bohr_velocity(1) / C, 1.0 / fine_structure_constant()))
    print("\n  Thomson model, P(scatter > 90 deg) = %.1e" % thomson_scattering_probability(90.0))
    print("  Geiger-Marsden measured 1/8000 = %.1e -- 36 orders of magnitude out"
          % (1.0 / 8000))


if __name__ == "__main__":
    _demo()
