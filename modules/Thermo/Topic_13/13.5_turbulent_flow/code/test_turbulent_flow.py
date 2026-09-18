"""test_turbulent_flow.py — checks for Module 13.5 [~CM].  Run: python3 test_turbulent_flow.py"""
import math
from turbulent_flow import (reynolds_number, reynolds_number_kinematic, is_turbulent,
                            flow_regime, friction_factor_blasius, friction_factor_colebrook,
                            friction_factor_haaland, power_law_velocity_profile,
                            mean_velocity_power_law, pressure_drop_darcy, head_loss_darcy)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# --- Reynolds number (same group as 13.4) ---
chk("Re water", reynolds_number(1000.0, 2.0, 0.05, 1.0e-3), 100000.0)
chk("Re = VD/nu", reynolds_number_kinematic(2.0, 0.05, 1.0e-3 / 1000.0),
    reynolds_number(1000.0, 2.0, 0.05, 1.0e-3))
# --- regime classification ---
assert is_turbulent(100000.0) is True;  _n += 1
assert is_turbulent(2000.0) is False;   _n += 1
assert flow_regime(225.0) == "laminar";        _n += 1
assert flow_regime(3000.0) == "transitional";  _n += 1
assert flow_regime(100000.0) == "turbulent";   _n += 1
# --- Blasius f = 0.316/Re^0.25 ---
chk("Blasius @Re=1e5", friction_factor_blasius(1.0e5), 0.316 * 1.0e5 ** -0.25)
chk("Blasius value @Re=1e5", friction_factor_blasius(1.0e5), 0.017771, 1e-5)
chk("Blasius @Re=1e4", friction_factor_blasius(1.0e4), 0.0316, 1e-4)
# --- Colebrook: smooth limit close to Blasius; satisfies its own implicit equation ---
f_sm = friction_factor_colebrook(1.0e5, 0.0)
chk("Colebrook smooth @1e5", f_sm, 0.01799, 1e-4)
# residual of the Colebrook equation must vanish
res = 1.0 / math.sqrt(f_sm) - (-2.0 * math.log10(0.0 / 3.7 + 2.51 / (1.0e5 * math.sqrt(f_sm))))
chk("Colebrook residual", res, 0.0, 1e-8)
f_r = friction_factor_colebrook(1.0e5, 0.001)
chk("Colebrook rough @1e5", f_r, 0.02217, 1e-4)
assert f_r > f_sm;  _n += 1                         # roughness raises f
# --- Haaland approximates Colebrook within ~1.5% ---
chk("Haaland ~ Colebrook (rr=0.001)", friction_factor_haaland(1.0e5, 0.001), f_r, 0.0005)
# fully-rough limit: Colebrook -> Nikuradse 1/(-2 log10(rr/3.7))^2, Re-independent
f_rough = friction_factor_colebrook(1.0e8, 0.05)
chk("fully-rough limit", f_rough, (-2.0 * math.log10(0.05 / 3.7)) ** -2, 1e-4)
# --- power-law profile: flatter than parabola ---
chk("u(0)=u_max", power_law_velocity_profile(10.0, 0.0, 0.05, 7), 10.0)
chk("u(R)=0", power_law_velocity_profile(10.0, 0.05, 0.05, 7), 0.0)
chk("V/u_max (n=7)", mean_velocity_power_law(1.0, 7), 2.0 * 49.0 / (8.0 * 15.0))
assert mean_velocity_power_law(1.0, 7) > 0.5;  _n += 1   # flatter than laminar (0.5)
# --- Darcy-Weisbach pressure drop & head loss (same form as 13.4) ---
rho, V, D, L = 1000.0, 2.0, 0.05, 10.0
f = friction_factor_colebrook(reynolds_number(rho, V, D, 1.0e-3), 0.0)
dP = pressure_drop_darcy(f, L, D, rho, V)
chk("dP = rho g h_L", dP, rho * 9.80665 * head_loss_darcy(f, L, D, V), 1e-6)
chk("dP value", dP, f * (L / D) * (rho * V * V / 2.0), 1e-9)

print(f"All {_n} tests passed.")
