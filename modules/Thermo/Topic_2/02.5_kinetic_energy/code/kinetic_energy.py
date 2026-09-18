"""
kinetic_energy.py  —  Module 2.5 (Kinetic Energy)

Kinetic energy is the energy of bulk motion, KE = ½ m V², introduced via the
work–energy idea: the net work of the resultant force on a body equals its change
in kinetic energy (Moran 8e §2.1.1, Eq. 2.5).

    ΔKE = KE₂ − KE₁ = ½ m (V₂² − V₁²) = W_net .

Units here are **joules** (m [kg], V [m/s]); the thermo energy-balance modules
1.2 / 1.EQ return the same quantity in kJ (÷1000) for use alongside Q and W.
"""


def kinetic_energy(m, V):
    """KE = ½ m V²  [J]."""
    return 0.5 * m * V * V


def delta_KE(m, V1, V2):
    """ΔKE = ½ m (V₂² − V₁²)  [J].  [Moran Eq. 2.5, §2.1.1, p.41]"""
    return 0.5 * m * (V2 * V2 - V1 * V1)


def work_from_KE(m, V1, V2):
    """Work–energy theorem: net work on a particle = its ΔKE  [J]."""
    return delta_KE(m, V1, V2)


def speed_after_work(m, V1, W_net):
    """Speed after net work W_net is added to a body initially at V1 (½mV₂²=½mV₁²+W)."""
    return (V1 * V1 + 2.0 * W_net / m) ** 0.5


def _demo():
    print("Module 2.5 — Kinetic energy (KE = ½mV²; net work = ΔKE)\n")
    print(f"  KE of 2 kg at 10 m/s        = {kinetic_energy(2.0, 10.0):.0f} J")
    print(f"  ΔKE 1000 kg, 100->20 m/s    = {delta_KE(1000.0, 100.0, 20.0)/1000:.0f} kJ")
    print(f"  speed after +100 J on 2 kg from rest = {speed_after_work(2.0, 0.0, 100.0):.1f} m/s")


if __name__ == "__main__":
    _demo()
