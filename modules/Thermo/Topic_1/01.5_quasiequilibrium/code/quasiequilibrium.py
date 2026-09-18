"""
quasiequilibrium.py  —  Module 1.5 (Quasiequilibrium Processes)

A **quasiequilibrium** (quasistatic) process is an idealized process so slow that
the system stays infinitesimally close to equilibrium throughout, so a single
pressure p is defined at every step.  Only then is the process a continuous
**path** of equilibrium states that can be drawn on a p-V diagram, and only then
is the boundary work the area under that path:

        W = ∫_{V1}^{V2} p dV            [Moran 8e Eq. 2.17, §2.2; cites ../refs.md]

The point of this module is that **work is path-dependent**: between the SAME end
states, different quasiequilibrium paths enclose different areas and so deliver
different work.  (Heat is path-dependent too — that is why W and Q are not
properties, while U is.)

Units:  p [kPa], V [m^3]  ->  W [kJ].
"""
import math


def pdv_work(p_of_V, V1, V2, n_steps=20000):
    """Boundary work W = ∫ p dV along a quasiequilibrium path p(V) [kJ] (trapezoid)."""
    h = (V2 - V1) / n_steps
    s = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        s += p_of_V(V1 + k * h)
    return s * h


def constant_pressure_work(p, V1, V2):
    """W = p (V2 - V1)  [kJ]  (horizontal line on the p-V diagram)."""
    return p * (V2 - V1)


def constant_volume_work(V1, V2=None):
    """W = 0: no volume change, no boundary work (vertical line on p-V)."""
    return 0.0


def polytropic_work(p1, V1, V2, n):
    """W for p V^n = const  [kJ]:  (p2 V2 - p1 V1)/(1-n), or p1 V1 ln(V2/V1) if n=1."""
    if math.isclose(n, 1.0):
        return p1 * V1 * math.log(V2 / V1)
    p2 = p1 * (V1 / V2) ** n
    return (p2 * V2 - p1 * V1) / (1.0 - n)


def path_work(segments):
    """Total work over a sequence of quasiequilibrium segments [kJ].
    Each segment is a tuple:
        ("p", p, V1, V2)              constant-pressure leg
        ("V", V)                      constant-volume leg (W = 0)
        ("poly", p1, V1, V2, n)       polytropic leg
    """
    W = 0.0
    for seg in segments:
        kind = seg[0]
        if kind == "p":
            W += constant_pressure_work(seg[1], seg[2], seg[3])
        elif kind == "V":
            W += 0.0
        elif kind == "poly":
            W += polytropic_work(seg[1], seg[2], seg[3], seg[4])
        else:
            raise ValueError(f"unknown segment {kind!r}")
    return W


def _demo():
    print("Module 1.5 — Quasiequilibrium: work is the area under p(V), path-dependent\n")
    # SAME end states  A=(100 kPa, 2 m^3)  ->  B=(200 kPa, 1 m^3)
    # Path 1: polytropic through both points (here n=1, isothermal: 100*2 = 200*1)
    W1 = polytropic_work(100.0, 2.0, 1.0, 1.0)
    # Path 2: constant p (100) to V=1, then constant V (1) to p=200
    W2 = path_work([("p", 100.0, 2.0, 1.0), ("V", 1.0)])
    # Path 3: constant V (2) to p=200, then constant p (200) to V=1
    W3 = path_work([("V", 2.0), ("p", 200.0, 2.0, 1.0)])
    print(f"  A=(100 kPa, 2 m^3) -> B=(200 kPa, 1 m^3), three quasiequilibrium paths:")
    print(f"   path 1 (isothermal n=1):        W = {W1:7.2f} kJ")
    print(f"   path 2 (const-p then const-V):  W = {W2:7.2f} kJ")
    print(f"   path 3 (const-V then const-p):  W = {W3:7.2f} kJ")
    print(f"  Same end states, different work  ->  W is NOT a property (path function).")


if __name__ == "__main__":
    _demo()
