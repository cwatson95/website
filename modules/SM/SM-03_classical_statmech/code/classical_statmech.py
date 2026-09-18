"""SM-03  Classical statistical mechanics -- ensembles & partition functions.

Physics topic network, module SM-03 (modules/topic_network.txt).
Source: Pathria 3e, Ch. 3 (canonical) and Ch. 4 (grand canonical).
Builds on ~SM-01 (K_B); ~SM-02 supplies the thermodynamic potentials this feeds.

A system in contact with a heat bath at temperature T occupies state i with the
**Boltzmann probability** P_i = e^{-beta E_i}/Z (Pa Sect. 3.2), where the
**partition function**
    Z = sum_i e^{-beta E_i},    beta = 1/kT
encodes all the thermodynamics:
    U = -d(ln Z)/d(beta),   F = -kT ln Z,   S = (U - F)/T,   C = Var(E)/(kT^2).
The last identity -- heat capacity = energy fluctuations -- is the simplest
fluctuation-dissipation relation.  Worked here: the two-level system (Schottky
anomaly), the harmonic oscillator / Einstein solid, and equipartition.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_SM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "SM-01_probability_ensembles", "code"))
if _SM01 not in sys.path:
    sys.path.insert(0, _SM01)

from probability_ensembles import K_B                       # noqa: E402

HBAR = 1.054571817e-34        # reduced Planck constant [J s]

__all__ = [
    "K_B", "HBAR", "partition_function", "boltzmann_probability",
    "internal_energy", "helmholtz_from_partition", "entropy_canonical",
    "heat_capacity", "two_level_energy", "two_level_heat_capacity",
    "harmonic_oscillator_energy", "einstein_heat_capacity",
    "equipartition_energy", "grand_partition_function",
]


# --- the canonical ensemble (Pa Sect. 3.2-3.3) -------------------------------

def partition_function(energies, T):
    """Canonical partition function  Z = sum_i exp(-E_i/kT)."""
    beta = 1.0 / (K_B * T)
    e0 = min(energies)                                      # shift for numerical stability
    return sum(math.exp(-beta * (E - e0)) for E in energies) * math.exp(-beta * e0)


def boltzmann_probability(energies, T):
    """Occupation probabilities  P_i = exp(-E_i/kT)/Z  (a list summing to 1)."""
    beta = 1.0 / (K_B * T)
    e0 = min(energies)
    w = [math.exp(-beta * (E - e0)) for E in energies]
    s = sum(w)
    return [wi / s for wi in w]


def internal_energy(energies, T):
    """Mean energy  U = <E> = sum_i E_i P_i  (= -d ln Z/d beta)."""
    p = boltzmann_probability(energies, T)
    return sum(E * pi for E, pi in zip(energies, p))


def helmholtz_from_partition(Z, T):
    """Helmholtz free energy from the partition function:  F = -kT ln Z (Pa 3.3)."""
    return -K_B * T * math.log(Z)


def entropy_canonical(energies, T):
    """Entropy from S = (U - F)/T, equivalently the Gibbs form -k sum P ln P."""
    U = internal_energy(energies, T)
    F = helmholtz_from_partition(partition_function(energies, T), T)
    return (U - F) / T


def heat_capacity(energies, T):
    """Heat capacity from energy fluctuations  C = Var(E)/(k T^2)  (= dU/dT).
    The simplest fluctuation-dissipation relation."""
    p = boltzmann_probability(energies, T)
    U = sum(E * pi for E, pi in zip(energies, p))
    E2 = sum(E * E * pi for E, pi in zip(energies, p))
    return (E2 - U * U) / (K_B * T * T)


# --- two-level system (Schottky anomaly) -------------------------------------

def two_level_energy(eps, T):
    """Mean energy of a two-level system {0, eps}:  <E> = eps/(e^{beta eps}+1)."""
    x = eps / (K_B * T)
    return eps / (math.exp(x) + 1.0)


def two_level_heat_capacity(eps, T):
    """Heat capacity of a two-level system (the Schottky anomaly):
        C = k (beta eps)^2 e^{beta eps} / (e^{beta eps}+1)^2."""
    x = eps / (K_B * T)
    ex = math.exp(x)
    return K_B * x * x * ex / (ex + 1.0) ** 2


# --- harmonic oscillator / Einstein solid ------------------------------------

def harmonic_oscillator_energy(omega, T):
    """Mean energy of a quantum oscillator (Planck):
        <E> = hbar w (1/2 + 1/(e^{beta hbar w} - 1)).
    -> hbar w/2 (zero-point) as T->0,  -> kT (equipartition) as T->infinity."""
    x = HBAR * omega / (K_B * T)
    return HBAR * omega * (0.5 + 1.0 / (math.exp(x) - 1.0))


def einstein_heat_capacity(omega, T):
    """Einstein heat capacity of one oscillator:
        C = k (beta hbar w)^2 e^{x}/(e^{x}-1)^2,  x = hbar w/kT.
    -> k (Dulong-Petit) at high T, -> 0 (frozen out) at low T."""
    x = HBAR * omega / (K_B * T)
    ex = math.exp(x)
    return K_B * x * x * ex / (ex - 1.0) ** 2


def equipartition_energy(quadratic_dof, N, T):
    """Classical equipartition: 1/2 kT per quadratic degree of freedom (Pa 3.7):
        U = (f/2) N k T  for f quadratic DoF per particle."""
    return 0.5 * quadratic_dof * N * K_B * T


# --- grand canonical ensemble (Pa Sect. 4.2) ---------------------------------

def grand_partition_function(Z_of_N, z, Nmax):
    """Grand partition function  Xi = sum_{N=0}^{Nmax} z^N Z_N  (z = fugacity).
    Z_of_N(N) returns the N-particle canonical partition function."""
    return sum(z ** N * Z_of_N(N) for N in range(Nmax + 1))


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-03 classical statistical mechanics -- demo")
    print("=" * 46)

    # two-level system: ground state wins cold, levels equalize hot
    eps = 1e-21
    print(f"two-level system, eps = {eps:.0e} J  (eps/k = {eps/K_B:.1f} K):")
    for T in (10.0, 72.0, 1000.0):
        p = boltzmann_probability([0.0, eps], T)
        print(f"  T={T:>6} K: P(ground)={p[0]:.4f}, P(excited)={p[1]:.4f}, "
              f"<E>/eps={two_level_energy(eps, T)/eps:.4f}")
    # the Schottky peak
    Tpeak = eps / (K_B * 2.4)        # C peaks near kT ~ 0.42 eps
    print(f"  Schottky heat capacity at T={Tpeak:.1f} K: C/k = {two_level_heat_capacity(eps, Tpeak)/K_B:.4f}")

    # harmonic oscillator: zero-point -> equipartition
    omega = 1e13
    print(f"\nquantum oscillator, hbar*omega/k = {HBAR*omega/K_B:.1f} K:")
    for T in (10.0, 760.0, 100000.0):
        E = harmonic_oscillator_energy(omega, T)
        print(f"  T={T:>8} K: <E>/(hbar w)={E/(HBAR*omega):.4f}  (->1/2 cold, -> kT/hbar w hot)")
    print(f"  Einstein C/k at high T -> {einstein_heat_capacity(omega, 1e5)/K_B:.4f} (Dulong-Petit = 1)")
    print(f"  Einstein C/k at low T  -> {einstein_heat_capacity(omega, 8.0)/K_B:.2e} (frozen out, kT << hbar w)")

    # U from -dlnZ/dbeta agrees with sum E P
    levels = [0.0, 1e-21, 2e-21, 3e-21]
    T = 80.0
    print(f"\ncheck U = <E> = -dlnZ/dbeta for a 4-level system at T={T} K:")
    print(f"  sum E_i P_i = {internal_energy(levels, T):.4e} J;  C = Var(E)/kT^2 = {heat_capacity(levels, T):.4e} J/K")


if __name__ == "__main__":
    _demo()
