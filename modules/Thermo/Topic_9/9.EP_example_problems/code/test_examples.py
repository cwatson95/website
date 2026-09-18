"""
test_examples.py  —  checks for Module 9.EP.

Each assertion regenerates a Moran 8e worked cycle Example from its GIVEN data and
matches the book's published ANSWER (tolerances absorb the book's rounding).

Run:  cd code && python3 test_examples.py   ->  "All N tests passed."
"""
import examples as ex

_n = 0


def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want book {want!r} (tol {tol})"
    _n += 1


# Example 9.1 — Otto cycle (English units)
e = ex.ex_9_1()
chk("9.1 vr2", e["vr2"], 18.04, 0.01)
chk("9.1 p2", e["p2_atm"], 17.96, 0.01)
chk("9.1 p3", e["p3_atm"], 53.3, 0.05)
chk("9.1 vr4", e["vr4"], 5.16, 0.01)
chk("9.1 p4", e["p4_atm"], 3.48, 0.01)
chk("9.1 eta", e["eta"], 0.51, 0.002)
chk("9.1 m", e["m_lb"], 1.47e-3, 0.01e-3)
chk("9.1 W", e["W_Btu"], 0.382, 0.001)
chk("9.1 mep", e["mep_atm"], 8.03, 0.01)
chk("9.1 quiz Q23", e["Q23_Btu"], 0.750, 0.001)
chk("9.1 quiz Q41", e["Q41_Btu"], 0.368, 0.001)
chk("9.1 T2 cold", e["T2_cold"], 1241.0, 0.6)
chk("9.1 T4 cold", e["T4_cold"], 1567.0, 0.6)
chk("9.1 eta cold", e["eta_cold"], 0.565, 0.001)

# Example 9.2 — Diesel cycle
e = ex.ex_9_2()
chk("9.2 T2", e["T2"], 898.3, 0.01)
chk("9.2 p2", e["p2_MPa"], 5.39, 0.005)
chk("9.2 T3", e["T3"], 1796.6, 0.01)
chk("9.2 T4", e["T4"], 887.7, 0.01)
chk("9.2 p4", e["p4_MPa"], 0.3, 0.005)
chk("9.2 eta", e["eta"], 0.578, 0.001)
chk("9.2 w", e["w_kJkg"], 617.9, 0.05)
chk("9.2 v1", e["v1"], 0.861, 0.001)
chk("9.2 mep", e["mep_MPa"], 0.76, 0.005)
chk("9.2 quiz displacement", e["displacement_L"], 10.0, 0.05)
chk("9.2 eta cold (note)", e["eta_cold"], 0.632, 0.001)

# Example 9.3 — dual cycle
e = ex.ex_9_3()
chk("9.3 T3", e["T3"], 1347.5, 0.1)
chk("9.3 T4", e["T4"], 1617.0, 0.1)
chk("9.3 vr5", e["vr5"], 84.135, 0.001)
chk("9.3 eta", e["eta"], 0.635, 0.001)
chk("9.3 quiz Qin", e["Qin_kJkg"], 718.0, 0.5)
chk("9.3 quiz w", e["w_kJkg"], 456.0, 0.5)
chk("9.3 mep", e["mep_MPa"], 0.56, 0.005)

# Example 9.4 — ideal Brayton cycle
e = ex.ex_9_4()
chk("9.4 pr2", e["pr2"], 13.86, 0.001)
chk("9.4 pr4", e["pr4"], 45.05, 0.001)
chk("9.4 eta", e["eta"], 0.457, 0.001)
chk("9.4 bwr", e["bwr"], 0.396, 0.001)
chk("9.4 mdot", e["mdot"], 5.807, 0.001)
chk("9.4 W", e["W_kW"], 2481.0, 1.0)
chk("9.4 quiz Qin", e["Qin_kW"], 5432.0, 1.0)
chk("9.4 T2 cold", e["T2_cold"], 579.2, 0.05)
chk("9.4 T4 cold", e["T4_cold"], 725.1, 0.05)
chk("9.4 eta cold", e["eta_cold"], 0.482, 0.001)
chk("9.4 bwr cold", e["bwr_cold"], 0.414, 0.001)
chk("9.4 W cold", e["W_cold_kW"], 2308.0, 2.0)

# Example 9.5 — pressure ratio for maximum net work (quiz: ~21)
chk("9.5 rp*", ex.ex_9_5()["rp_star"], 21.0, 0.25)

# Example 9.6 — Brayton with irreversibilities
e = ex.ex_9_6()
chk("9.6 wt", e["wt"], 565.5, 0.05)
chk("9.6 wc", e["wc"], 349.6, 0.05)
chk("9.6 h2", e["h2"], 649.8, 0.05)
chk("9.6 qin", e["qin"], 865.6, 0.05)
chk("9.6 eta", e["eta"], 0.249, 0.001)
chk("9.6 bwr", e["bwr"], 0.618, 0.001)
chk("9.6 W", e["W_kW"], 1254.0, 1.0)
chk("9.6 quiz eta 70%", e["eta_70"], 0.168, 0.001)
chk("9.6 quiz bwr 70%", e["bwr_70"], 0.7065, 0.0005)

# Example 9.7 — Brayton with regeneration
e = ex.ex_9_7()
chk("9.7 hx", e["hx"], 762.8, 0.05)
chk("9.7 eta_reg round-trip", e["eta_reg_check"], 0.8, 1e-9)
chk("9.7 eta", e["eta"], 0.568, 0.001)
chk("9.7 quiz eta_reg=1", e["eta_100"], 0.604, 0.001)

# Example 8.1 — ideal Rankine cycle
e = ex.ex_8_1()
chk("8.1 x2", e["x2"], 0.6745, 0.0001)
chk("8.1 h2", e["h2"], 1794.8, 0.1)
chk("8.1 wp", e["wp"], 8.06, 0.005)
chk("8.1 h4", e["h4"], 181.94, 0.01)
chk("8.1 eta", e["eta"], 0.371, 0.001)
chk("8.1 bwr", e["bwr"], 8.37e-3, 0.01e-3)
chk("8.1 mdot", e["mdot_kgh"], 3.77e5, 0.005e5)
chk("8.1 Qin", e["Qin_MW"], 269.77, 0.05)
chk("8.1 Qout", e["Qout_MW"], 169.75, 0.05)
chk("8.1 mcw", e["mcw_kgh"], 7.3e6, 0.01e6)
chk("8.1 quiz 150 kg/s", e["W_150kgs_MW"], 143.2, 0.1)

# Example 8.2 — Rankine with irreversibilities
e = ex.ex_8_2()
chk("8.2 h2", e["h2"], 1939.3, 0.05)
chk("8.2 wp", e["wp"], 9.48, 0.005)
chk("8.2 h4", e["h4"], 183.36, 0.01)
chk("8.2 eta", e["eta"], 0.314, 0.001)
chk("8.2 mdot", e["mdot_kgh"], 4.449e5, 0.005e5)
chk("8.2 Qin", e["Qin_MW"], 318.2, 0.1)
chk("8.2 Qout", e["Qout_MW"], 218.2, 0.1)
chk("8.2 mcw", e["mcw_kgh"], 9.39e6, 0.01e6)
chk("8.2 quiz pump power", e["Wp_150kgs_kW"], 1422.0, 1.0)
chk("8.2 quiz bwr", e["bwr"], 0.0116, 0.0001)

# Example 8.3 — ideal reheat cycle
e = ex.ex_8_3()
chk("8.3 x2", e["x2"], 0.9895, 0.0001)
chk("8.3 h2", e["h2"], 2741.8, 0.1)
chk("8.3 x4", e["x4"], 0.9382, 0.0001)
chk("8.3 h4", e["h4"], 2428.5, 0.1)
chk("8.3 eta", e["eta"], 0.403, 0.001)
chk("8.3 mdot", e["mdot_kgh"], 2.363e5, 0.003e5)
chk("8.3 Qout", e["Qout_MW"], 148.0, 0.2)
chk("8.3 quiz reheat Qin", e["Qreheat_MW"], 40.1, 0.05)
chk("8.3 quiz reheat frac", e["reheat_frac"], 0.162, 0.001)

# Example 8.4 — reheat cycle with turbine irreversibility
e = ex.ex_8_4()
chk("8.4 h2", e["h2"], 2832.8, 0.05)
chk("8.4 h4", e["h4"], 2567.2, 0.05)
chk("8.4 eta", e["eta"], 0.351, 0.001)

print(f"All {_n} tests passed.")
