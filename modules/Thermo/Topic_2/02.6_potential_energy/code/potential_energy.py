"""
potential_energy.py  —  Module 2.6 (Gravitational Potential Energy)

Gravitational potential energy is the energy of position in a uniform field,
PE = m g z, introduced (like KE) from the work done against gravity (Moran 8e
§2.1.2, Eq. 2.10):

    ΔPE = PE₂ − PE₁ = m g (z₂ − z₁) = −W_gravity .

The work done BY gravity as a body rises is negative and equals −ΔPE.
Units **joules** (m [kg], z [m], g [m/s²]); modules 1.2 / 1.EQ return kJ (÷1000).
"""
G = 9.81


def potential_energy(m, z, g=G):
    """PE = m g z  [J]  (relative to z = 0)."""
    return m * g * z


def delta_PE(m, z1, z2, g=G):
    """ΔPE = m g (z₂ − z₁)  [J].  [Moran Eq. 2.10, §2.1.2, p.42]"""
    return m * g * (z2 - z1)


def work_by_gravity(m, z1, z2, g=G):
    """Work done BY gravity as the body moves z₁→z₂:  W_grav = −ΔPE  [J]."""
    return -delta_PE(m, z1, z2, g)


def _demo():
    print("Module 2.6 — Potential energy (PE = mgz; W_gravity = −ΔPE)\n")
    print(f"  PE of 2 kg at 10 m        = {potential_energy(2.0, 10.0):.1f} J")
    print(f"  ΔPE 10 kg, 0->50 m        = {delta_PE(10.0, 0.0, 50.0)/1000:.3f} kJ")
    print(f"  work by gravity falling 50 m (10 kg) = {work_by_gravity(10.0, 50.0, 0.0):.0f} J")


if __name__ == "__main__":
    _demo()
