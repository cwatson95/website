"""
intensive.py  —  Module 1.4 (Intensive Properties)

An **intensive** property is independent of system size and may vary from point
to point: temperature T, pressure p, density rho, and every **specific**
property (per unit mass) such as specific volume v = V/m or specific internal
energy u = U/m.  [Moran 8e §1.3.3; §1.5 specific volume/density; cites in
../refs.md.]

Two facts the tests pin down:
  - a specific property converts an extensive one per unit mass:  v = V/m,  u = U/m
  - intensive properties do NOT add over subsystems; they **mass-average**:
        v_mix = sum(m_i v_i) / sum(m_i) = V_total / m_total
    (contrast module 1.3, where the extensive V_total = sum(V_i) does add).
"""


def specific(X, m):
    """Specific (per-unit-mass) value of an extensive property X:  x = X / m.
    e.g. specific volume v = V/m, specific internal energy u = U/m."""
    return X / m


def molar(X, n):
    """Molar (per-mole) value of an extensive property X:  X_bar = X / n."""
    return X / n


def density(m, V):
    """Density rho = m / V = 1 / v  [kg/m^3]."""
    return m / V


def specific_volume(V, m):
    """Specific volume v = V / m = 1 / rho  [m^3/kg]."""
    return V / m


def mass_average(values, masses):
    """Mass-weighted average of an intensive property over subsystems:
    x_mix = sum(m_i x_i) / sum(m_i).  This is how intensive properties combine."""
    M = sum(masses)
    if M == 0:
        raise ValueError("total mass is zero")
    return sum(m * x for m, x in zip(masses, values)) / M


def is_size_independent(x_small, x_scaled, tol=1e-9):
    """True if an intensive property is unchanged when the system is scaled up."""
    return abs(x_small - x_scaled) <= tol


def _demo():
    print("Module 1.4 — Intensive properties: specific values & mass-averaging\n")
    # specific volume and its reciprocal, density
    v = specific_volume(1.5, 3.0)            # V=1.5 m^3, m=3 kg
    print(f"(1) v = V/m = {v} m^3/kg;  rho = 1/v = {density(3.0, 1.5)} kg/m^3")
    # scaling the system leaves v unchanged (intensive)
    print(f"(2) double the system (3 m^3, 6 kg): v = {specific_volume(3.0, 6.0)}  "
          f"-> size-independent: {is_size_independent(v, specific_volume(3.0, 6.0))}")
    # combine subsystems: intensive v MASS-AVERAGES (does not add)
    vmix = mass_average([0.5, 2.0], [3.0, 1.0])   # 3 kg at v=0.5, 1 kg at v=2.0
    print(f"(3) mix 3 kg @ v=0.5 + 1 kg @ v=2.0:  v_mix = {vmix:.3f} m^3/kg"
          f"  ( = V_total/m_total = {(3*0.5 + 1*2.0)/4} )")


if __name__ == "__main__":
    _demo()
