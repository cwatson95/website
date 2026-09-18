"""
expansion_work.py  —  Module 2.2 (Expansion Work)

The moving-boundary work when a system **expands** (V increases). It is the
positive branch of W = ∫p dV (Moran §2.2.3, Eq. 2.17): the system does work ON
its surroundings, e.g. the power stroke of an engine. The full ∫p dV machinery
and path-dependence live in modules 1.2 / 1.5; this module is the expansion view.

p [kPa], V [m³] → W [kJ];  W > 0 for expansion.
"""
import math


def expansion_work(p_of_V, V1, V2, n_steps=20000):
    """W = ∫_{V1}^{V2} p dV for an expansion (V2 > V1); result > 0  [kJ]."""
    if V2 < V1:
        raise ValueError("expansion requires V2 > V1; use module 2.3 for compression")
    h = (V2 - V1) / n_steps
    tot = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        tot += p_of_V(V1 + k * h)
    return tot * h


def constant_pressure_expansion(p, V1, V2):
    """W = p (V2 − V1) at constant pressure  [kJ]."""
    return p * (V2 - V1)


def isothermal_expansion(p1, V1, V2):
    """Isothermal ideal-gas expansion W = p1 V1 ln(V2/V1)  [kJ]  (pV = const)."""
    return p1 * V1 * math.log(V2 / V1)


def _demo():
    print("Module 2.2 — Expansion work (W>0, work done BY the system)\n")
    print(f"  constant-p (200 kPa, 1->1.5 m³)  W = {constant_pressure_expansion(200.0, 1.0, 1.5):.1f} kJ")
    print(f"  isothermal (100 kPa, 1->2 m³)    W = {isothermal_expansion(100.0, 1.0, 2.0):.2f} kJ")
    print(f"  ∫p dV check (const p)            W = {expansion_work(lambda V: 200.0, 1.0, 1.5):.1f} kJ")


if __name__ == "__main__":
    _demo()
