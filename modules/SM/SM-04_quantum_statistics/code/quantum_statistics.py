"""SM-04  Quantum statistics -- Bose-Einstein & Fermi-Dirac gases, Planck.

Physics topic network, module SM-04 (modules/topic_network.txt).
Source: Pathria 3e, Ch. 5-8.  Builds on ~SM-03 (K_B, HBAR); ~QM-14 supplies the
symmetrization that forces the two statistics.

Indistinguishable quanta fill single-particle states with mean occupation
(Pa Sect. 6.3)
    <n> = 1 / (e^{(eps - mu)/kT} -+ 1),
the lower sign for **bosons** (Bose-Einstein, no occupancy limit) and the upper
for **fermions** (Fermi-Dirac, <n> <= 1, the Pauli principle).  When
(eps - mu) >> kT both reduce to the classical Maxwell-Boltzmann factor.
At T = 0 the Fermi gas fills every state up to the Fermi energy and none above;
the photon gas (bosons, mu = 0) gives the Planck blackbody spectrum, with a Wien
peak at hbar w ~ 2.82 kT and a Stefan-Boltzmann energy density ~ T^4.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SM03 = os.path.abspath(os.path.join(_HERE, "..", "..", "SM-03_classical_statmech", "code"))
if _SM03 not in sys.path:
    sys.path.insert(0, _SM03)

from classical_statmech import K_B, HBAR                    # noqa: E402

C_LIGHT = 2.99792458e8        # speed of light [m/s]

__all__ = [
    "K_B", "HBAR", "C_LIGHT",
    "bose_einstein", "fermi_dirac", "maxwell_boltzmann", "fermi_dirac_T0",
    "planck_energy_density", "rayleigh_jeans", "wien_peak_x",
    "radiation_energy_density", "stefan_boltzmann_constant",
]


# --- the three occupation numbers (Pa Sect. 6.3) -----------------------------

def bose_einstein(eps, mu, T):
    """Bose-Einstein mean occupation  <n> = 1/(e^{(eps-mu)/kT} - 1).
    Requires eps > mu (else divergent / unphysical)."""
    x = (eps - mu) / (K_B * T)
    return 1.0 / (math.exp(x) - 1.0)


def fermi_dirac(eps, mu, T):
    """Fermi-Dirac mean occupation  <n> = 1/(e^{(eps-mu)/kT} + 1).  Always in [0,1]
    (Pauli).  Equals 1/2 exactly at eps = mu (the chemical potential / Fermi level)."""
    x = (eps - mu) / (K_B * T)
    return 1.0 / (math.exp(x) + 1.0)


def maxwell_boltzmann(eps, mu, T):
    """Classical Maxwell-Boltzmann occupation  <n> = e^{-(eps-mu)/kT}
    (the common dilute / high-temperature limit of BE and FD)."""
    return math.exp(-(eps - mu) / (K_B * T))


def fermi_dirac_T0(eps, e_fermi):
    """Zero-temperature Fermi-Dirac: a step function -- every state below the Fermi
    energy is filled, every state above is empty (1/2 right at e_fermi)."""
    if eps < e_fermi:
        return 1.0
    if eps > e_fermi:
        return 0.0
    return 0.5


# --- blackbody radiation: the photon gas (Pa Sect. 7.3) ----------------------

def planck_energy_density(omega, T):
    """Planck spectral energy density per unit angular frequency:
        u(w) = (hbar w^3)/(pi^2 c^3) * 1/(e^{hbar w/kT} - 1)   [J s / m^3].
    Bosons with mu = 0; integrates to the Stefan-Boltzmann T^4 law."""
    x = HBAR * omega / (K_B * T)
    return (HBAR * omega ** 3) / (math.pi ** 2 * C_LIGHT ** 3) / (math.exp(x) - 1.0)


def rayleigh_jeans(omega, T):
    """Classical Rayleigh-Jeans law  u(w) = (w^2/pi^2 c^3) kT  -- the low-frequency
    limit of Planck (and the source of the 'ultraviolet catastrophe')."""
    return omega ** 2 / (math.pi ** 2 * C_LIGHT ** 3) * K_B * T


def wien_peak_x():
    """Dimensionless location x = hbar w_max/kT of the Planck peak (Wien's law):
    the root of 3(1 - e^{-x}) = x, x ~ 2.821439."""
    x = 3.0
    for _ in range(100):
        x = 3.0 * (1.0 - math.exp(-x))
    return x


def radiation_energy_density(T):
    """Total energy density of blackbody radiation  U/V = a T^4 (Stefan-Boltzmann),
    a = pi^2 k^4 / (15 hbar^3 c^3) -- the closed-form integral of Planck over w."""
    a = math.pi ** 2 * K_B ** 4 / (15.0 * HBAR ** 3 * C_LIGHT ** 3)
    return a * T ** 4


def stefan_boltzmann_constant():
    """Stefan-Boltzmann constant  sigma = pi^2 k^4 / (60 hbar^3 c^2) = a c / 4
    (radiated power per area = sigma T^4)."""
    return math.pi ** 2 * K_B ** 4 / (60.0 * HBAR ** 3 * C_LIGHT ** 2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-04 quantum statistics -- demo")
    print("=" * 36)

    mu, T = 1e-20, 300.0
    print(f"occupation vs energy (mu={mu:.0e} J, T={T} K, kT={K_B*T:.2e} J):")
    print(f"{'eps-mu (kT)':>12} {'Bose-Einstein':>14} {'Fermi-Dirac':>12} {'Maxwell-Boltz':>14}")
    for d in (-0.5, 0.0, 1.0, 3.0, 10.0):
        eps = mu + d * K_B * T
        be = bose_einstein(eps, mu, T) if d > 0 else float('nan')
        print(f"{d:12.1f} {be:14.4f} {fermi_dirac(eps, mu, T):12.4f} {maxwell_boltzmann(eps, mu, T):14.4f}")
    print("  FD = 1/2 at eps=mu; FD <= 1 always (Pauli); all three agree once eps-mu >> kT.")

    # Fermi gas at T=0
    eF = 5.0 * 1.602e-19       # 5 eV, typical metal
    print(f"\nFermi gas at T=0 (e_F = 5 eV): n(0.9 e_F)={fermi_dirac_T0(0.9*eF, eF)}, "
          f"n(1.1 e_F)={fermi_dirac_T0(1.1*eF, eF)}")

    # Planck spectrum
    print(f"\nblackbody radiation:")
    print(f"  Wien peak at hbar w/kT = {wien_peak_x():.6f}")
    T = 5778.0     # the Sun
    print(f"  Sun (T={T} K): energy density U/V = {radiation_energy_density(T):.4e} J/m^3")
    print(f"  Stefan-Boltzmann sigma = {stefan_boltzmann_constant():.6e} W/m^2/K^4  (CODATA 5.670e-8)")
    # Rayleigh-Jeans agreement at low frequency
    w_low = 1e11
    print(f"  at low w={w_low:.0e}: Planck/Rayleigh-Jeans = "
          f"{planck_energy_density(w_low, T)/rayleigh_jeans(w_low, T):.5f} (-> 1)")


if __name__ == "__main__":
    _demo()
