"""
QM-01  Origins of quantum theory  --  the four experiments that broke classical
physics, as closed-form formulae you can evaluate and cross-check.

Part of the physics topic network (see modules/topic_network.txt, module QM-01).
Root of the QUANTUM MECHANICS trunk; no QM prerequisites. Feeds into ~QM-02
(the wavefunction the de Broglie wave becomes) and ~QM-03 (Schrödinger eq.).

The five clusters, each a function group below:
  1. Black-body radiation   -- Planck's law; its Rayleigh-Jeans & Wien limits;
                               Stefan-Boltzmann and Wien displacement as
                               *consequences* (recovered here by integrating /
                               maximising Planck, not by quoting sigma and b).
  2. Photoelectric effect   -- Einstein's K_max = h f - W; threshold; stopping V.
  3. Bohr model             -- E_n, r_n, and the Rydberg series (Balmer etc.).
  4. de Broglie waves       -- lambda = h / p, the seed of the whole trunk.
  5. Compton scattering     -- the photon's momentum, Delta-lambda = lambda_C(1-cos).

Pure standard library (math only): the black-body integral uses a trapezoid
rule and the Wien peak a golden-section search, so every "known constant"
(sigma, b, R_inf, ...) is REDERIVED from h, c, k_B, e, m_e and checked in the
tests rather than hard-coded into the answer.
"""

import math

__all__ = [
    # constants (CODATA 2018)
    "h", "hbar", "c", "k_B", "e", "m_e", "eps0", "a0", "Ry_eV", "R_inf",
    "sigma_SB", "wien_b", "lambda_C",
    # black body
    "planck_u_nu", "planck_B_lambda", "rayleigh_jeans_u_nu", "wien_u_nu",
    "stefan_boltzmann_sigma", "wien_displacement_b",
    # photoelectric
    "photon_energy", "photoelectric_Kmax", "threshold_frequency", "stopping_voltage",
    # Bohr
    "bohr_energy_eV", "bohr_radius", "rydberg_inverse_wavelength", "rydberg_wavelength",
    # de Broglie / Compton
    "de_broglie_wavelength", "de_broglie_from_energy", "compton_shift",
]

# --- physical constants, CODATA 2018 (SI) ------------------------------------
h     = 6.62607015e-34      # Planck constant            [J s]   (exact)
hbar  = 1.054571817e-34     # reduced Planck constant    [J s]
c     = 2.99792458e8        # speed of light             [m/s]   (exact)
k_B   = 1.380649e-23        # Boltzmann constant         [J/K]   (exact)
e     = 1.602176634e-19     # elementary charge          [C]     (exact)
m_e   = 9.1093837015e-31    # electron mass              [kg]
eps0  = 8.8541878128e-12    # vacuum permittivity        [F/m]
# derived reference values (used ONLY to check the rederivations, see tests)
a0       = 5.29177210903e-11   # Bohr radius             [m]
Ry_eV    = 13.605693122994     # Rydberg energy          [eV]
R_inf    = 1.0973731568160e7   # Rydberg constant        [1/m]
sigma_SB = 5.670374419e-8      # Stefan-Boltzmann const  [W/m^2/K^4]
wien_b   = 2.897771955e-3      # Wien displacement const [m K]
lambda_C = 2.42631023867e-12   # Compton wavelength      [m]


# --- 1. black-body radiation -------------------------------------------------

def planck_u_nu(nu, T):
    """Planck spectral energy density per unit frequency  u(nu,T)  [J s / m^3].

        u(nu,T) = (8 pi h nu^3 / c^3) / (exp(h nu / k_B T) - 1)

    Integrate over all nu to get the total energy density a T^4 (a = 4 sigma/c).
    """
    x = h * nu / (k_B * T)
    return (8.0 * math.pi * h * nu**3 / c**3) / math.expm1(x)


def planck_B_lambda(lam, T):
    """Planck spectral radiance per unit wavelength  B(lambda,T)  [W / m^2 / m / sr].

        B(lambda,T) = (2 h c^2 / lambda^5) / (exp(h c / (lambda k_B T)) - 1)

    Its peak in lambda obeys Wien's displacement law (see wien_displacement_b).
    """
    x = h * c / (lam * k_B * T)
    return (2.0 * h * c**2 / lam**5) / math.expm1(x)


def rayleigh_jeans_u_nu(nu, T):
    """Classical Rayleigh-Jeans law  u = 8 pi nu^2 k_B T / c^3  (the 'UV catastrophe').

    It is the  h nu << k_B T  limit of Planck (exp(x)-1 -> x)."""
    return 8.0 * math.pi * nu**2 * k_B * T / c**3


def wien_u_nu(nu, T):
    """Wien's high-frequency approximation  u = (8 pi h nu^3/c^3) exp(-h nu/k_B T).

    It is the  h nu >> k_B T  limit of Planck (exp(x)-1 -> exp(x))."""
    return (8.0 * math.pi * h * nu**3 / c**3) * math.exp(-h * nu / (k_B * T))


def stefan_boltzmann_sigma(T=1.0, n=200000, x_max=50.0):
    """Recover the Stefan-Boltzmann constant by integrating Planck over frequency.

        integral_0^inf u(nu,T) dnu = a T^4,   a = 8 pi^5 k_B^4 / (15 h^3 c^3) = 4 sigma/c
    so  sigma = c a / 4.  We substitute x = h nu / k_B T and trapezoid-integrate
    x^3/(e^x - 1) on (0, x_max]; the exact value is pi^4/15 = 6.4939....  Returns
    the recovered sigma in W/m^2/K^4 (compare to sigma_SB)."""
    # integral of x^3/(e^x-1) dx
    dx = x_max / n
    total = 0.0
    prev = 0.0  # integrand -> 0 as x -> 0 (x^3/x = x^2 -> 0)
    for i in range(1, n + 1):
        x = i * dx
        val = x**3 / math.expm1(x)
        total += 0.5 * (prev + val) * dx
        prev = val
    a = 8.0 * math.pi * k_B**4 / (h**3 * c**3) * total   # u_total = a T^4 (T=1)
    return c * a / 4.0


def wien_displacement_b(T=1000.0):
    """Recover Wien's displacement constant b = lambda_max * T  by maximising
    B(lambda,T) over lambda (golden-section search). b ~ 2.898e-3 m K and is
    independent of T."""
    gr = (math.sqrt(5.0) - 1.0) / 2.0
    lo, hi = 1e-9, 1e-2          # bracket the visible/IR peak for T~1000 K
    f = lambda lam: planck_B_lambda(lam, T)
    a_, b_ = lo, hi
    cc = b_ - gr * (b_ - a_)
    dd = a_ + gr * (b_ - a_)
    for _ in range(200):
        if f(cc) < f(dd):
            a_ = cc
        else:
            b_ = dd
        cc = b_ - gr * (b_ - a_)
        dd = a_ + gr * (b_ - a_)
    lam_max = 0.5 * (a_ + b_)
    return lam_max * T


# --- 2. photoelectric effect -------------------------------------------------

def photon_energy(freq):
    """Energy of one photon  E = h f  [J]."""
    return h * freq


def photoelectric_Kmax(freq, work_function_J):
    """Einstein's photoelectric equation  K_max = h f - W  [J].

    Returns the maximum kinetic energy of an ejected electron; negative (clamped
    to 0.0) below threshold, where no electron is emitted regardless of intensity.
    """
    K = h * freq - work_function_J
    return K if K > 0.0 else 0.0


def threshold_frequency(work_function_J):
    """Cutoff frequency  f_0 = W / h: below it the photoelectric effect stops."""
    return work_function_J / h


def stopping_voltage(freq, work_function_J):
    """Stopping potential  V_s = K_max / e  [V] (the voltage that just halts the
    fastest photoelectrons)."""
    return photoelectric_Kmax(freq, work_function_J) / e


# --- 3. Bohr model -----------------------------------------------------------

def bohr_energy_eV(n, Z=1):
    """Bohr energy level  E_n = -(Z^2/n^2) * 13.606 eV.

    Derived from first principles as E_n = -(m_e e^4 Z^2)/(8 eps0^2 h^2 n^2);
    here returned in eV. E_1(H) = -13.6 eV (the ionization energy)."""
    E_J = -(m_e * e**4 * Z**2) / (8.0 * eps0**2 * h**2 * n**2)
    return E_J / e


def bohr_radius(n, Z=1):
    """Radius of the n-th Bohr orbit  r_n = n^2 a0 / Z  [m], with the Bohr radius
    a0 = 4 pi eps0 hbar^2 / (m_e e^2) computed from constants."""
    a0_calc = 4.0 * math.pi * eps0 * hbar**2 / (m_e * e**2)
    return n**2 * a0_calc / Z


def rydberg_inverse_wavelength(n1, n2, Z=1):
    """Rydberg formula  1/lambda = R Z^2 (1/n1^2 - 1/n2^2)  [1/m], n2 > n1.

    R is built from constants as R = m_e e^4 / (8 eps0^2 h^3 c). The series:
    n1=1 Lyman (UV), n1=2 Balmer (visible), n1=3 Paschen (IR)."""
    R = m_e * e**4 / (8.0 * eps0**2 * h**3 * c)
    return R * Z**2 * (1.0 / n1**2 - 1.0 / n2**2)


def rydberg_wavelength(n1, n2, Z=1):
    """Emitted/absorbed wavelength for the n2 -> n1 transition  [m]."""
    return 1.0 / rydberg_inverse_wavelength(n1, n2, Z)


# --- 4. de Broglie waves  &  5. Compton scattering ---------------------------

def de_broglie_wavelength(p):
    """de Broglie wavelength  lambda = h / p  [m]  -- matter is wavelike.
    This relation (Griffiths 3e Sec.1.6) is the bridge to ~QM-02/~QM-03: the
    "wave" whose squared modulus QM-02 reinterprets as a probability density."""
    return h / p


def de_broglie_from_energy(E_kin_J, mass=m_e):
    """Non-relativistic de Broglie wavelength from kinetic energy:
    p = sqrt(2 m E),  lambda = h / sqrt(2 m E)  [m]. (100 eV electron -> 0.123 nm.)"""
    p = math.sqrt(2.0 * mass * E_kin_J)
    return h / p


def compton_shift(theta):
    """Compton wavelength shift  Delta-lambda = (h/m_e c)(1 - cos theta)  [m].
    Maximal (= 2 lambda_C ~ 4.85 pm) at back-scatter theta = pi; proves the
    photon carries momentum p = h/lambda."""
    return (h / (m_e * c)) * (1.0 - math.cos(theta))


# --- demo --------------------------------------------------------------------

def _demo():
    print("QM-01 Origins -- numbers that broke classical physics\n")
    print("Black body:")
    print("  recovered sigma = %.4e  (CODATA %.4e) W/m^2/K^4"
          % (stefan_boltzmann_sigma(), sigma_SB))
    print("  recovered b     = %.4e  (CODATA %.4e) m K"
          % (wien_displacement_b(), wien_b))
    Tsun = 5772.0
    print("  Sun (T=5772 K) peak wavelength = %.0f nm"
          % (wien_displacement_b() / Tsun * 1e9))
    print("\nPhotoelectric (sodium, W = 2.28 eV):")
    W = 2.28 * e
    print("  threshold = %.3e Hz (%.0f nm)"
          % (threshold_frequency(W), c / threshold_frequency(W) * 1e9))
    f = c / 400e-9
    print("  400 nm light -> K_max = %.3f eV, stopping V = %.3f V"
          % (photoelectric_Kmax(f, W) / e, stopping_voltage(f, W)))
    print("\nBohr / hydrogen:")
    print("  E_1 = %.3f eV, E_2 = %.3f eV" % (bohr_energy_eV(1), bohr_energy_eV(2)))
    print("  Balmer H-alpha (3->2) = %.1f nm" % (rydberg_wavelength(2, 3) * 1e9))
    print("\nde Broglie / Compton:")
    print("  100 eV electron: lambda = %.4f nm" % (de_broglie_from_energy(100 * e) * 1e9))
    print("  Compton max shift (180 deg) = %.3f pm" % (compton_shift(math.pi) * 1e12))


if __name__ == "__main__":
    _demo()
