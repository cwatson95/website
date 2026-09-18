"""SM-06  Non-equilibrium & kinetic theory -- Maxwell-Boltzmann, transport.

Physics topic network, module SM-06 (modules/topic_network.txt).
Source: Pathria 3e, Ch. 6 (kinetic considerations) and Ch. 15 (Brownian motion).
Builds on ~SM-01 (K_B).  The Boltzmann transport equation is the bridge to
~PK-01 (Vlasov/Boltzmann) and ~CM-23 (fluid limit).

In equilibrium the molecular speeds follow the **Maxwell-Boltzmann distribution**
(Pa Sect. 6.4)
    f(v) = 4 pi (m/2 pi kT)^{3/2} v^2 exp(-m v^2 / 2 kT),
with three characteristic speeds in fixed ratio,
    v_p = sqrt(2kT/m) < <v> = sqrt(8kT/pi m) < v_rms = sqrt(3kT/m),
and mean kinetic energy <1/2 m v^2> = 3/2 kT (equipartition).  Collisions set the
**mean free path** lambda = 1/(sqrt2 n sigma) and hence the transport coefficients
(diffusion, viscosity, conductivity); Brownian motion gives Einstein's D = mu kT.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "SM-01_probability_ensembles", "code"))
if _SM01 not in sys.path:
    sys.path.insert(0, _SM01)

from probability_ensembles import K_B                       # noqa: E402

__all__ = [
    "K_B", "maxwell_speed_pdf", "most_probable_speed", "mean_speed", "rms_speed",
    "mean_kinetic_energy", "mean_free_path", "collision_rate", "effusion_flux",
    "diffusion_coefficient", "einstein_relation_diffusion",
]


# --- the Maxwell-Boltzmann speed distribution (Pa Sect. 6.4) -----------------

def maxwell_speed_pdf(v, m, T):
    """Maxwell-Boltzmann speed probability density
        f(v) = 4 pi (m/2 pi kT)^{3/2} v^2 exp(-m v^2 / 2 kT)."""
    a = m / (2.0 * math.pi * K_B * T)
    return 4.0 * math.pi * a ** 1.5 * v * v * math.exp(-m * v * v / (2.0 * K_B * T))


def most_probable_speed(m, T):
    """Peak of f(v):  v_p = sqrt(2 kT / m)."""
    return math.sqrt(2.0 * K_B * T / m)


def mean_speed(m, T):
    """Mean speed  <v> = sqrt(8 kT / pi m)."""
    return math.sqrt(8.0 * K_B * T / (math.pi * m))


def rms_speed(m, T):
    """Root-mean-square speed  v_rms = sqrt(3 kT / m)."""
    return math.sqrt(3.0 * K_B * T / m)


def mean_kinetic_energy(T):
    """Mean translational kinetic energy per molecule  <1/2 m v^2> = 3/2 kT
    (equipartition over 3 translational degrees of freedom)."""
    return 1.5 * K_B * T


# --- collisions and transport (Pa Sect. 6.4) ---------------------------------

def mean_free_path(number_density, diameter):
    """Mean free path  lambda = 1/(sqrt2 n sigma),  sigma = pi d^2 the collision
    cross-section (the sqrt2 accounts for relative molecular motion)."""
    sigma = math.pi * diameter ** 2
    return 1.0 / (math.sqrt(2.0) * number_density * sigma)


def collision_rate(number_density, diameter, m, T):
    """Collision frequency per molecule  z = <v>/lambda = sqrt2 n sigma <v>."""
    return mean_speed(m, T) / mean_free_path(number_density, diameter)


def effusion_flux(number_density, m, T):
    """Effusion flux through a small hole  Phi = (1/4) n <v>  (molecules per area
    per time) -- the kinetic-theory wall-collision rate."""
    return 0.25 * number_density * mean_speed(m, T)


def diffusion_coefficient(number_density, diameter, m, T):
    """Kinetic-theory self-diffusion coefficient  D = (1/3) <v> lambda."""
    return (1.0 / 3.0) * mean_speed(m, T) * mean_free_path(number_density, diameter)


def einstein_relation_diffusion(mobility, T):
    """Einstein relation (Pa Ch. 15):  D = mu kT,  mu the mobility -- a
    fluctuation-dissipation link between diffusion and drag."""
    return mobility * K_B * T


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-06 kinetic theory & transport -- demo")
    print("=" * 42)

    m_N2 = 4.652e-26      # nitrogen molecule [kg]
    T = 300.0
    vp, vbar, vrms = most_probable_speed(m_N2, T), mean_speed(m_N2, T), rms_speed(m_N2, T)
    print(f"N2 gas at T = {T} K:")
    print(f"  v_p   = {vp:7.1f} m/s   (sqrt(2kT/m))")
    print(f"  <v>   = {vbar:7.1f} m/s   (sqrt(8kT/pi m))")
    print(f"  v_rms = {vrms:7.1f} m/s   (sqrt(3kT/m))")
    print(f"  ordering v_p < <v> < v_rms,  ratios {vp/vp:.3f} : {vbar/vp:.3f} : {vrms/vp:.3f}")
    print(f"           (= 1 : sqrt(4/pi)={math.sqrt(4/math.pi):.3f} : sqrt(3/2)={math.sqrt(1.5):.3f})")
    print(f"  <1/2 m v^2> = {0.5*m_N2*vrms**2:.3e} J  = 3/2 kT = {mean_kinetic_energy(T):.3e} J")

    # transport at 1 atm
    n = 101325.0 / (K_B * T)     # ideal-gas number density at 1 atm
    d = 3.7e-10                  # N2 kinetic diameter [m]
    print(f"\nat 1 atm (n = {n:.3e} /m^3, d = {d*1e9:.2f} nm):")
    print(f"  mean free path lambda = {mean_free_path(n, d)*1e9:.1f} nm")
    print(f"  collision rate z = {collision_rate(n, d, m_N2, T):.3e} /s")
    print(f"  diffusion D = (1/3)<v>lambda = {diffusion_coefficient(n, d, m_N2, T):.3e} m^2/s")

    print(f"\nEinstein relation D = mu kT (mobility mu = 1e11 s/kg): "
          f"D = {einstein_relation_diffusion(1e11, T):.3e} m^2/s")


if __name__ == "__main__":
    _demo()
