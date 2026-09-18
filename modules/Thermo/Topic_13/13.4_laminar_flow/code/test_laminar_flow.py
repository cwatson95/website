"""test_laminar_flow.py — checks for Module 13.4 [~CM].  Run: python3 test_laminar_flow.py"""
import math
from laminar_flow import (reynolds_number, reynolds_number_kinematic, is_laminar,
                          friction_factor_laminar, velocity_profile_parabolic,
                          mean_velocity_from_max, pressure_drop_darcy,
                          pressure_drop_hagen_poiseuille, volumetric_flow_hagen_poiseuille)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- Reynolds number ---
chk("Re oil", reynolds_number(900.0, 2.0, 0.05, 0.4), 225.0)
chk("Re = VD/nu", reynolds_number_kinematic(2.0, 0.05, 0.4 / 900.0),
    reynolds_number(900.0, 2.0, 0.05, 0.4))
chk("Re water turbulent value", reynolds_number(1000.0, 2.0, 0.05, 1.0e-3), 100000.0)
# --- laminar criterion (~Re<2300) ---
assert is_laminar(225.0) is True;     _n += 1
assert is_laminar(2000.0) is True;    _n += 1
assert is_laminar(100000.0) is False; _n += 1
# --- friction factor f = 64/Re ---
chk("f @Re=225", friction_factor_laminar(225.0), 64.0 / 225.0)
chk("f @Re=2000", friction_factor_laminar(2000.0), 0.032)
# --- parabolic profile: u(0)=u_max, u(R)=0, mean=u_max/2 ---
chk("u(0)=u_max", velocity_profile_parabolic(4.0, 0.0, 0.025), 4.0)
chk("u(R)=0", velocity_profile_parabolic(4.0, 0.025, 0.025), 0.0)
chk("u(R/2)", velocity_profile_parabolic(4.0, 0.0125, 0.025), 4.0 * (1.0 - 0.25))
chk("mean = u_max/2", mean_velocity_from_max(4.0), 2.0)
# --- Darcy with f=64/Re EQUALS Hagen-Poiseuille (the key consistency check) ---
rho, V, D, mu, L = 900.0, 2.0, 0.05, 0.4, 10.0
Re = reynolds_number(rho, V, D, mu)
f = friction_factor_laminar(Re)
dP_darcy = pressure_drop_darcy(f, L, D, rho, V)
dP_hp = pressure_drop_hagen_poiseuille(mu, L, V, D)
chk("dP Darcy = dP Hagen-Poiseuille", dP_darcy, dP_hp, 1e-6)
chk("dP value", dP_hp, 102400.0, 1.0)
# --- Hagen-Poiseuille Q = pi R^4 dP/(8 mu L) consistent with Q = V * A ---
Q_hp = volumetric_flow_hagen_poiseuille(dP_hp, D / 2.0, mu, L)
chk("Q = V*A", Q_hp, V * math.pi * (D / 2.0) ** 2, 1e-9)

print(f"All {_n} tests passed.")
