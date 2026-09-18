"""test_adiabatic.py — checks for Module 6.3.  Run: python3 test_adiabatic.py"""
import math
from adiabatic import (is_adiabatic, delta_s_ideal_gas_so, delta_s_ideal_gas_cp,
                       cp_from_k, cv_from_k, temp_ratio_from_pressure, final_temp_isentropic,
                       temp_ratio_from_volume, pressure_ratio_from_volume,
                       final_pressure_isentropic, p2_from_pr, v2_from_vr, pr2_isentropic,
                       isentropic_turbine_eff, isentropic_nozzle_eff)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# adiabatic test
assert is_adiabatic(0.0) is True;       _n += 1
assert is_adiabatic(1e-12) is True;     _n += 1
assert is_adiabatic(5.0) is False;      _n += 1

R = 8.314 / 28.97       # air gas constant, kJ/kg.K
# ideal-gas Delta s, s0 tables (Sec. 6.5.1 inline example): 300 K,1 bar -> 1000 K,3 bar
chk("ds s0 air", delta_s_ideal_gas_so(2.96770, 1.70203, R, 3.0, 1.0), 0.9504, 1e-3)
# ideal-gas Delta s, constant cp (Sec. 6.5.2 inline example): 300 K,1 bar -> 400 K,5 bar
chk("ds cp air", delta_s_ideal_gas_cp(1.008, 400.0, 300.0, R, 5.0, 1.0), -0.1719, 1e-3)

# specific heats from k (Eq. 3.47): cp - cv = R, cp/cv = k
chk("cp_from_k", cp_from_k(1.4, 0.287), 1.4 * 0.287 / 0.4)
chk("cv_from_k", cv_from_k(1.4, 0.287), 0.287 / 0.4)
chk("cp-cv=R", cp_from_k(1.4, 0.287) - cv_from_k(1.4, 0.287), 0.287, 1e-9)
chk("cp/cv=k", cp_from_k(1.4, 0.287) / cv_from_k(1.4, 0.287), 1.4, 1e-9)

# isentropic constant-k relations are mutually consistent (Eqs 6.43-6.45)
k = 1.4
# p v^k = const: choose v2/v1=0.5 -> p2/p1=2^k ; and T2/T1 from p and from v must agree
pr = pressure_ratio_from_volume(1.0, 0.5, k)            # p2/p1 = 2^1.4
chk("pv^k", pr, 2.0 ** 1.4)
chk("T from p == T from v", temp_ratio_from_pressure(pr, 1.0, k),
    temp_ratio_from_volume(1.0, 0.5, k), 1e-12)
# final_temp_isentropic round-trips with final_pressure_isentropic
T2 = final_temp_isentropic(300.0, 10.0, 1.0, k)
chk("Tp round-trip", final_pressure_isentropic(300.0, T2, 1.0, k), 10.0, 1e-9)

# Example 6.9 -- air isentropic, 1 atm/540 R -> 1160 R (p.329-330)
chk("Ex6.9 p2 pr", p2_from_pr(1.0, 1.3860, 21.18), 15.28, 0.01)
chk("Ex6.9 p2 k", final_pressure_isentropic(540.0, 1160.0, 1.0, 1.39), 15.26, 0.05)

# Example 6.10 -- air leaking from a tank (p.330-331)
chk("Ex6.10 pr2", pr2_isentropic(8.411, 1.0, 5.0), 1.6822, 1e-4)
m2 = (1.0 / 5.0) * (500.0 / 317.0) * 5.0
chk("Ex6.10 m2", m2, 1.58, 0.01)

# relative volume helper (Eq. 6.42)
chk("v2_from_vr", v2_from_vr(0.5, 100.0, 50.0), 0.25)

# Example 6.11 -- steam-turbine work from isentropic efficiency (p.333-334)
chk("Ex6.11 W/m", 0.75 * (3105.6 - 2743.0), 271.95, 0.05)
# Example 6.12 -- air-turbine isentropic efficiency (p.334-335)
chk("Ex6.12 eta_t", isentropic_turbine_eff(390.88, 390.88 - 74.0, 285.27), 0.70, 0.005)
# nozzle efficiency
chk("nozzle eff", isentropic_nozzle_eff(95.0, 100.0), 0.95)

print(f"All {_n} tests passed.")
