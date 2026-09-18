"""
buoyancy.py  —  Module 2.7 (Buoyancy)

Buoyancy is a **fluid-statics** topic (a cross-link to the Classical-Mechanics /
fluids trunk, ~CM), included in Topic 2 because it is a force/energy bookkeeping
that uses the hydrostatic pressure of module 1.4/§1.6.

**Archimedes' principle:** a body immersed in a fluid feels an upward **buoyant
force equal to the weight of the fluid it displaces**,
    F_b = ρ_fluid · g · V_displaced .
This is the net of the hydrostatic pressure p = ρ g h acting over the surface;
Moran 8e derives it in §1.6.2 "Buoyancy" (p.16-17) from the pressure-depth
relation (Eq. 1.11) and names it Archimedes' principle.  Applied in Problem 1.54.

SI units: ρ [kg/m³], V [m³], g [m/s²] → F [N].
"""
G = 9.81


def buoyant_force(rho_fluid, V_displaced, g=G):
    """Archimedes' buoyant force  F_b = ρ_fluid g V_displaced  [N]."""
    return rho_fluid * g * V_displaced


def apparent_weight(true_weight, rho_fluid, V_object, g=G):
    """Apparent (submerged) weight = true weight − buoyant force  [N]."""
    return true_weight - buoyant_force(rho_fluid, V_object, g)


def floats(rho_object, rho_fluid):
    """True if a body of mean density ρ_object floats in a fluid of density ρ_fluid."""
    return rho_object < rho_fluid


def submerged_fraction(rho_object, rho_fluid):
    """For a freely floating body (F_b = weight), the fraction of volume submerged
    is ρ_object / ρ_fluid."""
    if rho_object > rho_fluid:
        raise ValueError("body sinks (ρ_object > ρ_fluid)")
    return rho_object / rho_fluid


def _demo():
    print("Module 2.7 — Buoyancy (Archimedes; fluid-statics cross-link ~CM)\n")
    print(f"  F_b on 1 m³ submerged in water = {buoyant_force(1000.0, 1.0):.0f} N")
    # iceberg in seawater
    f = submerged_fraction(917.0, 1025.0)
    print(f"  iceberg (ρ=917) in seawater (ρ=1025): {f*100:.1f}% submerged  (tip-of-the-iceberg)")
    # a 100 N steel object (ρ=7850) displacing its volume in water
    V = 100.0 / (7850.0 * G)
    print(f"  100 N steel object, apparent weight in water = {apparent_weight(100.0, 1000.0, V):.1f} N")
    print(f"  does pine (ρ=500) float in water? {floats(500.0, 1000.0)}")


if __name__ == "__main__":
    _demo()
