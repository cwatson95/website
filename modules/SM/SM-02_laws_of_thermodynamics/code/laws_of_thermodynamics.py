"""SM-02  Laws of thermodynamics -- entropy, temperature, potentials, Carnot.

Physics topic network, module SM-02 (modules/topic_network.txt).
Source: Pathria 3e Ch. 1 (Sect. 1.2-1.3); Schroeder Ch. 1,3,4,5 (image-only).
Builds on ~SM-01 (Boltzmann entropy S = k ln Omega, K_B).

The four laws and their machinery:
  0th: thermal equilibrium is transitive (a common temperature exists).
  1st: dU = T dS - P dV + mu dN  (energy conservation).
  2nd: dS_total >= 0; temperature emerges as 1/T = (dS/dU)_{V,N}.
  3rd: S -> 0 as T -> 0.
From U one builds the other potentials by Legendre transforms -- enthalpy
H = U + PV, Helmholtz F = U - TS, Gibbs G = U - TS + PV -- each natural for a
different control variable, and each pair of second derivatives gives a Maxwell
relation.  A Carnot engine between T_h and T_c has the maximal efficiency
eta = 1 - T_c/T_h (Schroeder Ch. 4).
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
    "K_B", "enthalpy", "helmholtz_free_energy", "gibbs_free_energy",
    "temperature_from_entropy", "pressure_from_helmholtz",
    "maxwell_relation_residual", "carnot_efficiency",
    "carnot_cop_refrigerator", "carnot_cop_heat_pump",
    "entropy_change_heat", "total_entropy_change_heat_flow",
]


# --- thermodynamic potentials (Legendre transforms) --------------------------

def enthalpy(U, P, V):
    """Enthalpy  H = U + P V  (natural variables S, P)."""
    return U + P * V


def helmholtz_free_energy(U, T, S):
    """Helmholtz free energy  F = U - T S  (natural variables T, V)."""
    return U - T * S


def gibbs_free_energy(U, T, S, P, V):
    """Gibbs free energy  G = U - T S + P V = H - T S  (natural variables T, P)."""
    return U - T * S + P * V


# --- temperature and pressure as entropy / free-energy derivatives -----------

def temperature_from_entropy(S_of_U, U, rel=1e-6):
    """Thermodynamic temperature from  1/T = (dS/dU)_{V,N}  (2nd law / Pa 1.2).
    S_of_U is the entropy as a function of internal energy U.  The finite-difference
    step is taken RELATIVE to U so it works across any unit scale (U ~ 1e-21 J or O(1))."""
    h = rel * abs(U) or rel
    dSdU = (S_of_U(U + h) - S_of_U(U - h)) / (2.0 * h)
    return 1.0 / dSdU


def pressure_from_helmholtz(F_of_V, V, T=None, rel=1e-6):
    """Pressure from  P = -(dF/dV)_T  (F the Helmholtz free energy).  Relative step."""
    h = rel * abs(V) or rel
    return -(F_of_V(V + h) - F_of_V(V - h)) / (2.0 * h)


# --- Maxwell relation (from F): (dS/dV)_T = (dP/dT)_V ------------------------

def maxwell_relation_residual(S_TV, P_TV, T, V, h=1e-5):
    """Residual of the Maxwell relation  (dS/dV)_T = (dP/dT)_V  (from dF=-S dT-P dV),
    given S(T,V) and P(T,V).  Returns the difference normalized by the term size."""
    dS_dV = (S_TV(T, V + h) - S_TV(T, V - h)) / (2.0 * h)
    dP_dT = (P_TV(T + h, V) - P_TV(T - h, V)) / (2.0 * h)
    scale = max(abs(dS_dV), abs(dP_dT)) + 1e-300
    return (dS_dV - dP_dT) / scale


# --- the Carnot cycle (Schroeder Ch. 4) --------------------------------------

def carnot_efficiency(T_cold, T_hot):
    """Maximum efficiency of any heat engine between T_cold and T_hot:
        eta = 1 - T_cold/T_hot  (temperatures in kelvin)."""
    return 1.0 - T_cold / T_hot


def carnot_cop_refrigerator(T_cold, T_hot):
    """Coefficient of performance of a Carnot refrigerator:  COP = T_c/(T_h - T_c)."""
    return T_cold / (T_hot - T_cold)


def carnot_cop_heat_pump(T_cold, T_hot):
    """COP of a Carnot heat pump:  COP = T_h/(T_h - T_c) = 1 + COP_fridge."""
    return T_hot / (T_hot - T_cold)


# --- the second law: entropy and heat flow -----------------------------------

def entropy_change_heat(Q, T):
    """Entropy change of a reservoir at temperature T receiving heat Q:  dS = Q/T."""
    return Q / T


def total_entropy_change_heat_flow(Q, T_hot, T_cold):
    """Total entropy change when heat Q flows spontaneously hot -> cold:
        dS = Q(1/T_c - 1/T_h) > 0  for T_h > T_c (the second law in action)."""
    return Q * (1.0 / T_cold - 1.0 / T_hot)


# --- demo --------------------------------------------------------------------

def _demo():
    print("SM-02 laws of thermodynamics -- demo")
    print("=" * 38)

    # temperature from an ideal-gas entropy S(U) = (3/2) N k ln U + const
    N = 1.0
    S_of_U = lambda U: 1.5 * N * K_B * math.log(U)
    U0 = 3.0e-21
    T = temperature_from_entropy(S_of_U, U0)
    print(f"ideal gas: S=(3/2)Nk ln U  ->  1/T=dS/dU gives U = (3/2)NkT")
    print(f"  at U={U0:.2e} J:  T = {T:.2f} K,  check (3/2)NkT = {1.5*N*K_B*T:.2e} (= U)")

    # potentials
    U, T_, S, P, V = 100.0, 300.0, 0.2, 1e5, 1e-3
    print(f"\npotentials (U={U}, T={T_}, S={S}, P={P}, V={V}):")
    print(f"  H = U+PV     = {enthalpy(U, P, V):.2f}")
    print(f"  F = U-TS     = {helmholtz_free_energy(U, T_, S):.2f}")
    print(f"  G = U-TS+PV  = {gibbs_free_energy(U, T_, S, P, V):.2f}")

    # Maxwell relation for an ideal gas
    Nk = 1.0
    S_TV = lambda T, V: Nk * (math.log(V) + 1.5 * math.log(T))
    P_TV = lambda T, V: Nk * T / V
    print(f"\nMaxwell relation (dS/dV)_T = (dP/dT)_V for ideal gas:")
    print(f"  residual = {maxwell_relation_residual(S_TV, P_TV, 300.0, 1e-3):.2e}  (-> 0)")

    # Carnot
    Tc, Th = 300.0, 600.0
    print(f"\nCarnot engine between {Tc} K and {Th} K:")
    print(f"  efficiency eta = 1 - Tc/Th = {carnot_efficiency(Tc, Th):.4f}")
    print(f"  fridge COP = {carnot_cop_refrigerator(Tc, Th):.4f}, heat-pump COP = {carnot_cop_heat_pump(Tc, Th):.4f}")

    # second law
    dS = total_entropy_change_heat_flow(1.0, Th, Tc)
    print(f"\n1 J flowing {Th} K -> {Tc} K: dS_total = {dS:.3e} J/K > 0 (second law)")


if __name__ == "__main__":
    _demo()
