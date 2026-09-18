"""QF-05  Quantum field theory in curved spacetime -- the Hawking & Unruh effects.

Physics topic network, module QF-05 (modules/topic_network.txt).  Capstone of the
[QF] trunk and the link into the user's Quantum_Optics curved-spacetime / squeezed-
spacetimes work.  Sources: Birrell & Davies, *Quantum Fields in Curved Space*
(Bogoliubov framework Ch. 2-3, the Unruh effect Ch. 4, quantum black holes Ch. 8);
Fulling, *Aspects of Quantum Field Theory in Curved Space-Time* (the particle
concept & accelerated observers).  Builds on ~QF-01 (canonical quantization & the
vacuum), ~RE-13 (Einstein equations / stress-energy) and ~RE-14 (Schwarzschild
horizon & surface gravity).

THE ONE IDEA.  The vacuum is NOT observer-independent.  A free field has *no*
preferred mode decomposition in a general spacetime: expand it in one complete set
of modes {u_k} (with annihilation operators a_k) or another {u'_j} (a'_j), and the
two are related by a **Bogoliubov transformation**

        u'_j = sum_k ( alpha_jk u_k + beta_jk u_k^* ),
        a'_j = sum_k ( alpha_jk^* a_k - beta_jk^* a_k^dagger ),

with the normalization  sum_k ( |alpha_jk|^2 - |beta_jk|^2 ) = 1  (preserving the
bosonic commutators).  Whenever the "mixing" coefficients beta_jk are non-zero, the
a'-vacuum is full of a-particles:

        <0'| N_k |0'> = sum_j |beta_jk|^2 .

Two physical incarnations:
  * UNRUH.  A uniformly accelerated (Rindler) observer, proper acceleration a, sees
    the Minkowski vacuum as a THERMAL bath at  T_U = hbar a / (2 pi c k_B).  The
    Bogoliubov coefficients give a Planck spectrum, |beta_w|^2/|alpha_w|^2 =
    exp(-2 pi c w / a), hence <n_w> = |beta_w|^2 = 1/(exp(hbar w / k_B T_U) - 1).
  * HAWKING.  A black hole radiates thermally at  T_H = hbar c^3 / (8 pi G M k_B)
    = hbar kappa / (2 pi c k_B), with surface gravity kappa = c^4/(4 G M) (~RE-14).
    T_H ~ 1/M: a solar-mass hole is ~6e-8 K (colder than the CMB), a 1 kg hole is
    ~1e23 K.  Energy loss dM/dt ~ -1/M^2 gives a lifetime tau ~ M^3.

A horizon is, in the language of ~QO-05, a two-mode SQUEEZER: writing
alpha = cosh r, beta = sinh r reproduces |alpha|^2 - |beta|^2 = 1 and a thermal
<N> = sinh^2 r -- the squeezed-vacuum bridge to the Quantum_Optics drafts.

Self-contained: SI constants are defined locally; numpy only (no sibling imports).
Angular frequencies w are in rad/s, so hbar*w is an energy.
"""

import numpy as np

# --- SI physical constants (defined locally; module is self-contained) --------
HBAR  = 1.054571817e-34      # reduced Planck constant            [J s]
C     = 2.99792458e8         # speed of light in vacuum           [m/s]
K_B   = 1.380649e-23         # Boltzmann constant                 [J/K]
G     = 6.67430e-11          # Newtonian gravitational constant   [m^3 kg^-1 s^-2]
M_SUN = 1.98892e30           # solar mass                         [kg]

__all__ = [
    "HBAR", "C", "K_B", "G", "M_SUN",
    "schwarzschild_radius", "surface_gravity",
    "unruh_temperature", "hawking_temperature",
    "bose_occupation", "fermi_occupation",
    "bogoliubov_check", "particle_number", "squeeze_to_bogoliubov",
    "thermal_beta_squared", "unruh_beta_ratio", "unruh_occupation",
    "evaporation_lifetime",
]


# --- horizon geometry (the ~RE-14 quantities, in SI) -------------------------

def schwarzschild_radius(M):
    """Event-horizon radius  r_s = 2 G M / c^2  (~RE-14)."""
    return 2.0 * G * M / C ** 2


def surface_gravity(M):
    """Surface gravity of a Schwarzschild horizon  kappa = c^4/(4 G M) = c^2/(2 r_s).
    It is the redshifted acceleration at the horizon, and sets T_H = hbar kappa/(2 pi c k_B)."""
    return C ** 2 / (2.0 * schwarzschild_radius(M))


# --- the two temperatures ----------------------------------------------------

def unruh_temperature(a):
    """Unruh temperature seen by a uniformly accelerated observer,
        T_U = hbar a / (2 pi c k_B),
    LINEAR in the proper acceleration a [m/s^2].  (Birrell & Davies Ch. 4.)"""
    return HBAR * a / (2.0 * np.pi * C * K_B)


def hawking_temperature(M):
    """Hawking temperature of a Schwarzschild black hole of mass M [kg],
        T_H = hbar c^3 / (8 pi G M k_B) = hbar kappa / (2 pi c k_B),
    INVERSELY proportional to the mass.  (Birrell & Davies Ch. 8.)"""
    return HBAR * C ** 3 / (8.0 * np.pi * G * M * K_B)


# --- Planck / thermal occupation numbers -------------------------------------

def bose_occupation(omega, T):
    """Bose-Einstein (Planck) occupation of a mode of angular frequency omega
    at temperature T:   <n> = 1 / (exp(hbar omega / k_B T) - 1).
    Uses expm1 for numerical stability; accepts scalars or numpy arrays."""
    x = HBAR * np.asarray(omega, dtype=float) / (K_B * T)
    # stable for all x > 0:  1/(e^x - 1) = e^{-x} / (1 - e^{-x})  (no overflow)
    return np.exp(-x) / (-np.expm1(-x))


def fermi_occupation(omega, T):
    """Fermi-Dirac occupation  <n> = 1 / (exp(hbar omega / k_B T) + 1).
    Written via tanh for stability; bounded in (0, 1/2]."""
    x = HBAR * np.asarray(omega, dtype=float) / (K_B * T)
    return 0.5 * (1.0 - np.tanh(0.5 * x))


# --- Bogoliubov bookkeeping --------------------------------------------------

def bogoliubov_check(alpha, beta):
    """Bosonic Bogoliubov normalization  sum(|alpha|^2) - sum(|beta|^2),
    which must equal 1 for a properly normalized output mode (commutator-preserving).
    Accepts scalars or arrays (the sum runs over the input-mode index k)."""
    a = np.asarray(alpha, dtype=complex)
    b = np.asarray(beta, dtype=complex)
    return float(np.sum(np.abs(a) ** 2) - np.sum(np.abs(b) ** 2))


def particle_number(beta):
    """Particles in the rotated vacuum  <N> = sum_k |beta_k|^2  -- non-zero beta
    (mode mixing) means the vacuum is populated.  Accepts a scalar or array."""
    b = np.asarray(beta, dtype=complex)
    return float(np.sum(np.abs(b) ** 2))


def squeeze_to_bogoliubov(r):
    """A horizon acts as a two-mode squeezer (~QO-05): for squeezing parameter r,
        (alpha, beta) = (cosh r, sinh r),
    which automatically satisfies |alpha|^2 - |beta|^2 = 1 and gives <N> = sinh^2 r."""
    return np.cosh(r), np.sinh(r)


# --- the thermal spectrum from Bogoliubov mixing -----------------------------

def thermal_beta_squared(omega, T, statistics="bose"):
    """Thermal |beta_omega|^2 spectrum = the mode occupation a horizon imprints:
        |beta_omega|^2 = 1 / (exp(hbar omega / k_B T) -+ 1),
    minus sign for bosons (Planck / Bose-Einstein), plus for fermions (Fermi-Dirac).
    This IS the Planck spectrum -- identical to `bose_occupation` for statistics='bose'."""
    if statistics == "bose":
        return bose_occupation(omega, T)
    if statistics == "fermi":
        return fermi_occupation(omega, T)
    raise ValueError("statistics must be 'bose' or 'fermi'")


def unruh_beta_ratio(omega, a):
    """Ratio of Bogoliubov coefficients for a Rindler mode of frequency omega,
        |beta_omega|^2 / |alpha_omega|^2 = exp(-2 pi c omega / a),
    the detailed-balance factor that makes the Unruh spectrum thermal."""
    return np.exp(-2.0 * np.pi * C * np.asarray(omega, dtype=float) / a)


def unruh_occupation(omega, a):
    """Occupation of a Rindler mode in the Minkowski vacuum, built PURELY from the
    Bogoliubov ratio R = |beta|^2/|alpha|^2 and the normalization |alpha|^2-|beta|^2=1:
        |beta|^2 = R / (1 - R) = 1 / (exp(2 pi c omega / a) - 1).
    Equals `bose_occupation(omega, unruh_temperature(a))` -- i.e. it is Planckian."""
    R = unruh_beta_ratio(omega, a)
    return R / (1.0 - R)


# --- black-hole evaporation --------------------------------------------------

def evaporation_lifetime(M):
    """Hawking evaporation lifetime (single massless field, Stefan-Boltzmann
    estimate):  tau = 5120 pi G^2 M^3 / (hbar c^4),  scaling as M^3 because
    dM/dt = -hbar c^4 / (15360 pi G^2 M^2).  For M_sun this is ~2e67 yr."""
    return 5120.0 * np.pi * G ** 2 * M ** 3 / (HBAR * C ** 4)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QF-05  QFT in curved spacetime -- Hawking & Unruh  (SI units)")
    print("=" * 62)

    # 1) Unruh: temperature is linear in acceleration
    a = 1.0e20
    print("\n1) UNRUH effect (T_U = hbar a / 2 pi c k_B):")
    print("   a = %.0e m/s^2  ->  T_U = %.4f K" % (a, unruh_temperature(a)))
    print("   doubling a doubles T_U:  T_U(2a)/T_U(a) = %.3f"
          % (unruh_temperature(2 * a) / unruh_temperature(a)))
    print("   everyday g = 9.81 m/s^2  ->  T_U = %.2e K  (utterly unmeasurable)"
          % unruh_temperature(9.81))

    # 2) the Unruh spectrum is thermal (Planckian)
    w = a / (2.0 * np.pi * C)            # mode with hbar w / k_B T_U = 1
    nU = unruh_occupation(w, a)
    nP = bose_occupation(w, unruh_temperature(a))
    print("\n2) the Bogoliubov occupation IS Planck:")
    print("   |beta_w|^2 from Bogoliubov ratio  = %.6f" % nU)
    print("   Bose factor at T_U                = %.6f   (identical)" % nP)
    print("   |beta_w|^2/|alpha_w|^2 = exp(-2 pi c w/a) = %.6f" % unruh_beta_ratio(w, a))

    # 3) Hawking: temperature ~ 1/M
    print("\n3) HAWKING effect (T_H = hbar c^3 / 8 pi G M k_B = hbar kappa / 2 pi c k_B):")
    print("   solar mass  M = %.3e kg : r_s = %.3f km, kappa = %.3e m/s^2"
          % (M_SUN, schwarzschild_radius(M_SUN) / 1e3, surface_gravity(M_SUN)))
    print("                              T_H = %.3e K   (colder than the 2.7 K CMB!)"
          % hawking_temperature(M_SUN))
    print("   T_H via surface gravity        = %.3e K   (identical)"
          % (HBAR * surface_gravity(M_SUN) / (2.0 * np.pi * C * K_B)))
    print("   1 kg black hole : T_H = %.3e K   (T_H ~ 1/M, so tiny holes are blazing hot)"
          % hawking_temperature(1.0))

    # 4) Bogoliubov normalization / squeezing
    r = 1.3
    alpha, beta = squeeze_to_bogoliubov(r)
    print("\n4) BOGOLIUBOV / squeezing (alpha=cosh r, beta=sinh r):")
    print("   r = %.2f : |alpha|^2 - |beta|^2 = %.12f   (= 1, commutators preserved)"
          % (r, bogoliubov_check(alpha, beta)))
    print("   created particles <N> = sum|beta|^2 = sinh^2 r = %.4f" % particle_number(beta))

    # 5) evaporation
    tau = evaporation_lifetime(M_SUN)
    print("\n5) EVAPORATION (tau = 5120 pi G^2 M^3 / hbar c^4 ~ M^3):")
    print("   solar-mass lifetime tau = %.3e s = %.3e yr" % (tau, tau / 3.15576e7))
    print("   tau(2M)/tau(M) = %.1f  (cubic in mass)"
          % (evaporation_lifetime(2 * M_SUN) / evaporation_lifetime(M_SUN)))


if __name__ == "__main__":
    _demo()
