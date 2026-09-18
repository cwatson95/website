"""test_power.py — checks for Module 2.4.  Run: python3 test_power.py"""
import math
from power import (power_force_velocity, shaft_power, electric_power,
                   power_from_work, energy_from_power, rpm_to_rad_s)

_n = 0
def chk(name, got, want, tol=1e-3):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

chk("force*velocity", power_force_velocity(500.0, 4.0), 2000.0)
chk("rpm->rad/s", rpm_to_rad_s(1000.0), 1000.0 * 2 * math.pi / 60.0)
chk("shaft power", shaft_power(9.7, rpm_to_rad_s(1000.0)), 9.7 * 1000.0 * 2 * math.pi / 60.0, 1e-9)
chk("electric power", electric_power(110.0, 10.0), 1100.0)
chk("power from work", power_from_work(1800.0, 1.0), 1800.0)
chk("energy from power", energy_from_power(1800.0, 60.0), 108000.0)
# consistency: energy_from_power then power_from_work round-trips
chk("round trip", power_from_work(energy_from_power(1800.0, 60.0), 60.0), 1800.0)

# the value quoted in notes.md: 9.7 N.m at 1000 rpm is 1016 W
chk("9.7 N.m @ 1000 rpm = 1016 W", shaft_power(9.7, rpm_to_rad_s(1000.0)), 1016.0, tol=0.5)
# forgetting rpm -> rad/s overstates the power by 60/(2 pi) = 9.55, not by 2 pi/60
chk("rpm-into-tau-omega error factor",
    shaft_power(9.7, 1000.0) / shaft_power(9.7, rpm_to_rad_s(1000.0)),
    60.0 / (2.0 * math.pi), tol=1e-9)
chk("that factor is 9.55", 60.0 / (2.0 * math.pi), 9.55, tol=5e-3)
# a force perpendicular to the motion transmits no power (dot product)
chk("no power without a component along V", power_force_velocity(0.0, 4.0), 0.0)

print(f"All {_n} tests passed.")
