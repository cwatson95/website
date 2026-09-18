"""
work.py  —  Module 2.1 (Work)

Work is an energy transfer across a system boundary that could, in principle,
raise a weight: W = ∫ F·ds.  This module is the **catalog of work modes** — the
several physical ways a system does (or receives) work — under one thermodynamic
sign convention, following Moran 8e §2.2.  (The ∫p dV boundary mode and its
path-dependence are developed in modules 1.2 / 1.5; collected here too.)

Sign convention (Moran): **W > 0 when work is done BY the system** on its
surroundings.  Work is a **path function** (an inexact differential δW), not a
property — see module 1.5.

SI units:  force [N], displacement [m], so W [J] (= N·m);  p [kPa], V [m³] → [kJ];
torque [N·m], ω [rad/s], V (voltage) [V], current [A], spring k [N/m].
"""
import math


def work_force_displacement(F_of_s, s1, s2, n_steps=20000):
    """General work  W = ∫ F·ds  [J] for a force F(s) along a path.
    [Moran Eq. 2.12, §2.2, p.44]"""
    h = (s2 - s1) / n_steps
    tot = 0.5 * (F_of_s(s1) + F_of_s(s2))
    for k in range(1, n_steps):
        tot += F_of_s(s1 + k * h)
    return tot * h


def boundary_work(p_of_V, V1, V2, n_steps=20000):
    """Moving-boundary (pdV) work  W = ∫ p dV  [kJ]  (p kPa, V m³).  [Moran Eq. 2.17]
    Positive for expansion (V₂>V₁), negative for compression.  See modules 1.2, 1.5."""
    h = (V2 - V1) / n_steps
    tot = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        tot += p_of_V(V1 + k * h)
    return tot * h


def shaft_work(torque, omega, dt):
    """Work transmitted by a rotating shaft over time dt at constant τ, ω:
    W = τ ω dt  [J].  Positive = work OUT of the system (e.g. a turbine shaft).
    [Moran §2.2; Ẇ = τω, Eq. 2.20]"""
    return torque * omega * dt


def electric_work(voltage, current, dt):
    """Electrical work-energy magnitude  |W| = V I dt  [J].

    Moran's convention makes electrical power INTO a system negative work
    (Ẇ = −V I), so the work done BY the system is −V I dt.  This returns the
    magnitude V I dt; apply the sign per direction.  [Moran Eq. 2.21, §2.2.6, p.53]"""
    return voltage * current * dt


def spring_work(k, x1, x2):
    """Work done ON a linear spring stretched from x₁ to x₂:
    W = ½ k (x₂² − x₁²)  [J]  (x measured from the natural length).  [Moran §2.2]"""
    return 0.5 * k * (x2 * x2 - x1 * x1)


def _demo():
    print("Module 2.1 — Work: a catalog of work modes (W>0 done BY the system)\n")
    # boundary work: constant-pressure expansion 200 kPa, 1->1.5 m^3
    print(f"  boundary  ∫p dV (200 kPa, 1->1.5 m³)  = {boundary_work(lambda V: 200.0, 1.0, 1.5):.1f} kJ")
    # general F·ds: constant 50 N over 3 m
    print(f"  force·disp (50 N over 3 m)            = {work_force_displacement(lambda s: 50.0, 0.0, 3.0):.1f} J")
    # shaft: 18 N·m at 100 rad/s for 1 s
    print(f"  shaft  τω·dt (18 N·m, 100 rad/s, 1 s) = {shaft_work(18.0, 100.0, 1.0):.0f} J")
    # electrical: 110 V, 10 A for 1 s
    print(f"  electric  V I dt (110 V, 10 A, 1 s)   = {electric_work(110.0, 10.0, 1.0):.0f} J (into system)")
    # spring: k=200 N/m stretched 0 -> 0.1 m
    print(f"  spring  ½k(x²) (200 N/m, 0->0.1 m)    = {spring_work(200.0, 0.0, 0.1):.1f} J")


if __name__ == "__main__":
    _demo()
