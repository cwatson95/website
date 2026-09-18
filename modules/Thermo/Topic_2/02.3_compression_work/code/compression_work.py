"""
compression_work.py  —  Module 2.3 (Compression Work)

The moving-boundary work when a system is **compressed** (V decreases). It is the
negative branch of W = ∫p dV (Moran §2.2.3, Eq. 2.17): the surroundings do work
ON the system, e.g. a compressor or pump. So W < 0, and the **work input** is
−W > 0. Mirror of module 2.2; shared machinery in modules 1.2 / 1.5.

p [kPa], V [m³] → W [kJ];  W < 0 for compression.
"""
import math


def compression_work(p_of_V, V1, V2, n_steps=20000):
    """W = ∫_{V1}^{V2} p dV for a compression (V2 < V1); result < 0  [kJ]."""
    if V2 > V1:
        raise ValueError("compression requires V2 < V1; use module 2.2 for expansion")
    h = (V2 - V1) / n_steps
    tot = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        tot += p_of_V(V1 + k * h)
    return tot * h


def work_input(p_of_V, V1, V2, n_steps=20000):
    """Magnitude of work that must be supplied to compress, −W > 0  [kJ]."""
    return -compression_work(p_of_V, V1, V2, n_steps)


def polytropic_compression(p1, V1, V2, n):
    """W for a polytropic compression pVⁿ = const  [kJ]  (W < 0).
    n≠1: (p2V2−p1V1)/(1−n);  n=1: p1V1 ln(V2/V1)."""
    if math.isclose(n, 1.0):
        return p1 * V1 * math.log(V2 / V1)
    p2 = p1 * (V1 / V2) ** n
    return (p2 * V2 - p1 * V1) / (1.0 - n)


def _demo():
    print("Module 2.3 — Compression work (W<0; work input = −W > 0)\n")
    W = polytropic_compression(100.0, 1.0, 0.5, 1.3)
    print(f"  polytropic n=1.3 (100 kPa, 1->0.5 m³)  W = {W:.2f} kJ, work in = {-W:.2f} kJ")
    print(f"  isothermal (100 kPa, 2->1 m³)          W = {polytropic_compression(100.0, 2.0, 1.0, 1.0):.2f} kJ")
    print(f"  work_input via ∫p dV (const 150 kPa)   = {work_input(lambda V: 150.0, 1.0, 0.6):.1f} kJ")


if __name__ == "__main__":
    _demo()
