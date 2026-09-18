"""
test_examples.py  —  checks for Module 1.EP.

Each assertion regenerates a Moran 8e worked Example from its GIVEN data and
matches the book's published ANSWER (tolerances absorb the book's rounding).

Run:  cd code && python3 test_examples.py   ->  "All N tests passed."
"""
import examples as ex

_n = 0


def chk(name, got, want, tol):
    global _n
    assert abs(got - want) <= tol, f"{name}: got {got!r}, want book {want!r} (tol {tol})"
    _n += 1


# Example 2.1 — expansion work, three polytropic exponents
e21 = ex.ex_2_1()
chk("2.1 p2 (n=1.5)", e21["p2_a_kPa"], 106.0, tol=0.5)      # 1.06 bar
chk("2.1 W (n=1.5)", e21["W_a_n1.5"], 17.6, tol=0.05)
chk("2.1 W (n=1)",   e21["W_b_n1"],   20.79, tol=0.01)
chk("2.1 W (n=0)",   e21["W_c_n0"],   30.0, tol=1e-6)

# Example 2.2 — cooling a gas: Q = m Δu + W
chk("2.2 Q", ex.ex_2_2()["Q"], -4.4, tol=0.05)

# Example 2.3 — alternative systems (English units, Btu)
e23 = ex.ex_2_3()
chk("2.3 piston pressure", e23["p_lbf_in2"], 15.4, tol=0.1)
chk("2.3 Q air-alone", e23["Q_a"], 15.36, tol=0.05)
chk("2.3 Q air+piston", e23["Q_b"], 15.35, tol=0.05)

# Example 2.4 — gearbox at steady state
e24 = ex.ex_2_4()
chk("2.4 Qdot", e24["Qdot"], -1.2, tol=0.01)
chk("2.4 W2", e24["W2"], 58.8, tol=0.01)

# Example 2.5 — silicon chip surface temperature
e25 = ex.ex_2_5()
chk("2.5 Tb (K)", e25["Tb_K"], 353.0, tol=0.5)
chk("2.5 Tb (C)", e25["Tb_C"], 80.0, tol=0.2)              # book rounds 79.85 -> 80

# Example 2.6 — transient motor
e26 = ex.ex_2_6()
chk("2.6 W_shaft", e26["Wshaft_kW"], 1.8, tol=1e-6)
chk("2.6 W_total", e26["W_total"], -0.2, tol=1e-9)
chk("2.6 dE limit", e26["dE_limit"], 4.0, tol=1e-9)

print(f"All {_n} tests passed.")
