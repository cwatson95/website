"""
test_homework.py — checks for Module 2.HP.

Worked solutions (Moran has no answer key): the tests pin the computed answers for
reproducibility and add independent consistency checks (given endpoints recovered,
energy balances close).

Run:  cd code && python3 test_homework.py   ->  "All N tests passed."
"""
import homework as h

_n = 0
def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want {want!r} (tol {tol})"
    _n += 1

# kinetic / potential
chk("2.10 V1", h.p2_10()["V1_ft_s"], 151.88, 0.05)
chk("2.14 V2", h.p2_14()["V2_ft_s"], 200.75, 0.05)
chk("2.16 V2", h.p2_16()["V2_m_s"], 11.23, 0.01)
chk("2.19 W", h.p2_19()["W_kJ"], 32.0, 1e-6)
chk("2.22 P", h.p2_22()["P_kW"], 67.99, 0.05)

# ∫p dV work
chk("2.27 W", h.p2_27()["W_Btu"], -4.63, 0.01)
chk("2.27 p1 endpoint", h.p2_27()["p1_psi"], 5.0, 1e-9)    # consistency: recovers given p1
chk("2.27 p2 endpoint", h.p2_27()["p2_psi"], 20.0, 1e-9)
chk("2.29 p2", h.p2_29()["p2_bar"], 2.00, 0.01)
chk("2.29 W", h.p2_29()["W_kJ"], 1283.9, 0.5)
chk("2.30 p1", h.p2_30()["p1_bar"], 9.0, 1e-9)
chk("2.30 p2", h.p2_30()["p2_bar"], 5.0, 1e-9)
chk("2.30 W", h.p2_30()["W_kJ"], 12.59, 0.01)
chk("2.35 V2", h.p2_35()["V2_ft3"], 0.8, 1e-9)
chk("2.35 W12", h.p2_35()["W12_Btu"], -11.91, 0.01)
chk("2.35 W31", h.p2_35()["W31_Btu"], 5.92, 0.01)

# spring / shaft / electrical
chk("2.36 P_hp", h.p2_36()["P_hp"], 0.1364, 0.001)
chk("2.36 W_1min", h.p2_36()["W_1min_Btu"], 5.78, 0.01)
chk("2.37 F", h.p2_37()["F_kN"], 2.667, 0.001)
chk("2.37 rpm", h.p2_37()["rpm"], 334.2, 0.1)
chk("2.38 R", h.p2_38()["R_ohm"], 20.0, 1e-9)
chk("2.38 W", h.p2_38()["W_kJ"], 9.0, 1e-9)
chk("2.45 W", h.p2_45()["W_J"], 20.0, 1e-6)

# energy balance
chk("2.65 dU", h.p2_65()["dU_Btu"], 2.12, 0.01)
chk("2.66 du", h.p2_66()["du_Btu_lb"], 54.0, 0.05)
chk("2.70 T2", h.p2_70()["T2_R"], 820.3, 0.1)
chk("2.64 W", h.p2_64()["W_kJ"], -120.0, 1e-9)
chk("2.64 Q", h.p2_64()["Q_kJ"], -76.25, 0.01)
chk("2.64 K", h.p2_64()["K_kW_min"], 0.006354, 1e-5)

# independent consistency: 2.64 energy balance ΔU = Q − W must close
chk("2.64 balance", (h.p2_64()["Q_kJ"] - h.p2_64()["W_kJ"]) - (276.67 - 232.92), 0.0, 1e-9)

print(f"All {_n} tests passed.")
