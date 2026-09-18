"""test_extensive.py — checks for Module 1.3.  Run: python3 test_extensive.py"""
from extensive import (total, scales_with_extent, is_additive,
                       volume, internal_energy, kinetic_energy)

_n = 0


def chk(name, got, want, tol=1e-9):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want {want!r}"
    _n += 1


chk("total", total([2.0, 1.0, 0.5]), 3.5)
# additivity: V(2kg)+V(1kg) == V(3kg) at the same specific volume
chk("volume additive", volume(2.0, 0.5) + volume(1.0, 0.5), volume(3.0, 0.5))
chk("is_additive true", is_additive([2.0, 1.0], 3.0), True)
chk("is_additive false", is_additive([2.0, 1.0], 3.1), False)
# scales with extent: k copies -> k times the value
chk("scales_with_extent", scales_with_extent(internal_energy(1.0, 100.0), 2), internal_energy(2.0, 100.0))
chk("internal_energy", internal_energy(2.0, 100.0), 200.0)
chk("kinetic_energy", kinetic_energy(2.0, 10.0), 100.0)   # 1/2*2*100 J

print(f"All {_n} tests passed.")
