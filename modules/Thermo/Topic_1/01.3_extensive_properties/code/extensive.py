"""
extensive.py  —  Module 1.3 (Extensive Properties)

An **extensive** property depends on the size (extent) of the system and is
**additive over subsystems**: divide a system in two and the property is the sum
of the parts.  Mass m, volume V, energy E (and U, KE, PE), enthalpy H, entropy S
are extensive.  [Moran 8e §1.3.3 "Extensive and Intensive Properties"; cites in
../refs.md.]

The operational signature, used in the tests:
  - additive:           X_total = sum(X_i) over subsystems
  - scales with extent: X(k * system) = k * X(system)

Contrast with module 1.4 (intensive properties), which do NOT add — they
mass-average.
"""


def total(values):
    """Total of an extensive property over subsystems: X = sum(X_i)."""
    return sum(values)


def scales_with_extent(X_per_unit, k):
    """An extensive property of k identical units is k times one unit's value."""
    return k * X_per_unit


def is_additive(parts, whole, tol=1e-9):
    """True if the subsystem values sum to the whole (the test for extensivity)."""
    return abs(sum(parts) - whole) <= tol


# common extensive properties, written as (extent) x (per-mass value) to make the
# "scales with mass" character explicit
def volume(m, v):
    """Extensive volume V = m v   (mass x specific volume)."""
    return m * v


def internal_energy(m, u):
    """Extensive internal energy U = m u."""
    return m * u


def kinetic_energy(m, V):
    """Extensive kinetic energy KE = 1/2 m V^2  [J]."""
    return 0.5 * m * V * V


def _demo():
    print("Module 1.3 — Extensive properties: additive & size-dependent\n")
    # split a 3 kg system into 2 kg + 1 kg subsystems of equal specific volume
    v = 0.5                                  # m^3/kg, same intensive state
    V1, V2 = volume(2.0, v), volume(1.0, v)
    print(f"(1) Volume is additive:  V(2kg) + V(1kg) = {V1} + {V2} = {V1 + V2} m^3"
          f"  ==  V(3kg) = {volume(3.0, v)}")
    # doubling the system doubles every extensive property
    print(f"(2) Scales with extent:  U of 2 copies = {scales_with_extent(internal_energy(1.0, 100.0), 2)}"
          f" kJ  == U(2 kg) = {internal_energy(2.0, 100.0)} kJ")
    print(f"(3) is_additive([2,1], 3): {is_additive([2.0, 1.0], 3.0)}")


if __name__ == "__main__":
    _demo()
