"""
test_examples.py  —  checks for Module 10.EP.

Each assertion regenerates a Moran 8e worked Example (Ch.5) from its GIVEN data
and matches the book's published ANSWER (tolerances absorb the book's rounding).
Ex S.1 is the module-authored Stirling analysis (Moran has no worked Stirling
Example); its checks close against the concept modules 10.1/10.2.

Run:  cd code && python3 test_examples.py   ->  "All N tests passed."
"""
import examples as ex

_n = 0


def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want book {want!r} (tol {tol})"
    _n += 1


# Example 5.1 — power cycle between 2000 K and 400 K, Q_H = 1000 kJ
e51 = ex.ex_5_1()
chk("5.1 eta_max", e51["eta_max"], 0.80, tol=1e-9)
assert e51["verdict_a"] == "irreversible", e51["verdict_a"]; _n += 1
chk("5.1 eta (b)", e51["eta_b"], 0.85, tol=1e-9)
assert e51["verdict_b"] == "impossible", e51["verdict_b"]; _n += 1
chk("5.1 W (c)", e51["W_c"], 800.0, tol=1e-9)
chk("5.1 eta (c)", e51["eta_c"], 0.80, tol=1e-9)
assert e51["verdict_c"] == "reversible", e51["verdict_c"]; _n += 1
chk("5.1 QQ eta", e51["eta_qq"], 0.90, tol=1e-9)
assert e51["verdict_qq"] == "impossible", e51["verdict_qq"]; _n += 1

# Example 5.2 — freezer at 268 K, surroundings 295 K, 8000 kJ/h with 3200 kJ/h
e52 = ex.ex_5_2()
chk("5.2 beta", e52["beta"], 2.5, tol=1e-9)
chk("5.2 beta_max (book 9.9)", e52["beta_max"], 9.9, tol=0.05)      # exact 268/27 = 9.926
assert e52["irreversible"], "beta must sit below the reversible ceiling"; _n += 1
chk("5.2 QQ claimed beta", e52["beta_claim"], 10.0, tol=1e-9)
assert not e52["claim_valid"], "800 kJ/h claim must be invalid"; _n += 1

# Example 5.3 — heat pump: building 530 R, outside 492 R, 5e5 Btu/day, 13 c/kWh
e53 = ex.ex_5_3()
chk("5.3 gamma_max (book 13.95)", e53["gamma_max"], 13.95, tol=0.01)
chk("5.3 W_min (book 3.58e4)", e53["W_min"], 3.58e4, tol=100.0)
chk("5.3 cost ($/day)", e53["cost_min"], 1.36, tol=0.01)
chk("5.3 QQ cost, COP 3", e53["cost_cop3"], 6.35, tol=0.01)
chk("5.3 QQ cost, resistance", e53["cost_resistance"], 19.04, tol=0.01)

# Example S.1 — module-authored ideal Stirling (air, 1000 K / 300 K, r = 2)
es1 = ex.ex_s_1()
chk("S.1 Q_34", es1["Q_34"], 198.93, tol=0.01)
chk("S.1 Q_12", es1["Q_12"], 59.68, tol=0.01)
chk("S.1 W_net", es1["W_net"], 139.25, tol=0.01)
chk("S.1 W = Q_34 - Q_12", es1["W_net"], es1["Q_34"] - es1["Q_12"], tol=1e-9)
chk("S.1 Q_regen", es1["Q_regen"], 502.6, tol=0.01)
chk("S.1 eta", es1["eta"], 0.70, tol=1e-9)
chk("S.1 eta = ideal Stirling", es1["eta"], es1["eta_ideal"], tol=1e-9)
chk("S.1 eta = Carnot ceiling", es1["eta"], es1["eta_carnot"], tol=1e-9)
chk("S.1 eta without regen", es1["eta_no_regen"], 0.1985, tol=1e-4)

print(f"All {_n} tests passed.")
