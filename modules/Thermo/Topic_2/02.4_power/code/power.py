"""
power.py  —  Module 2.4 (Power)

Power is the **rate** of energy transfer by work, Ẇ = δW/dt, following Moran 8e
§2.2.  Each work mode of module 2.1 has a corresponding power.  Same sign
convention: Ẇ > 0 when work is done BY the system.

SI units: F [N], V [m/s] → Ẇ [W]; torque [N·m], ω [rad/s] → [W]; voltage [V],
current [A] → [W]; energy [J], time [s].
"""


def power_force_velocity(F, V):
    """Power of a force on a moving boundary point  Ẇ = F·V  [W].  [Moran Eq. 2.13]"""
    return F * V


def shaft_power(torque, omega):
    """Power transmitted by a rotating shaft  Ẇ = τ ω  [W]  (ω in rad/s).
    [Moran Eq. 2.20]"""
    return torque * omega


def electric_power(voltage, current):
    """Electric power  Ẇ = V I  [W]  (magnitude; into the system it is −VI by the
    BY-the-system convention).  [Moran §2.2, Ẇ = −εi]"""
    return voltage * current


def power_from_work(W, dt):
    """Average power  Ẇ = W/dt  [W]."""
    return W / dt


def energy_from_power(P_avg, dt):
    """Energy transferred at average power P_avg over dt:  W = P_avg · dt  [J]."""
    return P_avg * dt


def rpm_to_rad_s(rpm):
    """Convert rotational speed: ω [rad/s] = rpm · 2π/60."""
    return rpm * 2.0 * 3.141592653589793 / 60.0


def _demo():
    print("Module 2.4 — Power: rate of work (Ẇ = δW/dt)\n")
    print(f"  force·velocity (500 N at 4 m/s)        = {power_force_velocity(500.0, 4.0):.0f} W")
    print(f"  shaft τω (9.7 N·m at 1000 rpm)         = {shaft_power(9.7, rpm_to_rad_s(1000)):.1f} W")
    print(f"  electric V I (110 V, 10 A)             = {electric_power(110.0, 10.0):.0f} W")
    print(f"  energy from power (1.8 kW for 60 s)    = {energy_from_power(1800.0, 60.0)/1000:.1f} kJ")


if __name__ == "__main__":
    _demo()
