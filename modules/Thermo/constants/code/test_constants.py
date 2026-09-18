"""
test_constants.py — checks for the Constants module.

Verifies Table 3.1 against itself via R = R-bar/M (Moran Eq. 3.25): for every
substance, R * M must equal the universal gas constant within rounding.

Run:  cd code && python3 test_constants.py   ->  "All N tests passed."
"""
import constants as C

_n = 0


def chk(name, cond):
    global _n
    assert cond, f"{name} failed"
    _n += 1


# every substance: R * M == R-bar (8.314 kJ/kmol-K) to within table rounding
for r in C.GAS:
    R, M = float(r["R_kJ_kgK"]), float(r["M_kg_kmol"])
    chk(f"R*M {r['substance']}", abs(R * M - C.RBAR) <= 0.02)

# spot values from Table 3.1
chk("Air R", abs(C.gas_constant("Air") - 0.2870) < 1e-9)
chk("Hydrogen R", abs(C.gas_constant("Hydrogen") - 4.1240) < 1e-9)
chk("Water R", abs(C.gas_constant("Water") - 0.4614) < 1e-9)
chk("N2 == CO R", C.gas_constant("Nitrogen") == C.gas_constant("Carbon monoxide"))

# universal constants
chk("R-bar", abs(C.constant("Universal gas constant", "kJ/kmol-K") - 8.314) < 1e-9)
chk("atm kPa", abs(C.constant("Standard atmosphere", "kPa") - 101.325) < 1e-9)
chk("gc", abs(C.constant("Gravitational constant (English)") - 32.174) < 1e-9)
chk("absolute zero", abs(C.constant("Absolute zero") + 273.15) < 1e-9)
# Boltzmann = R-bar / N_A  (R-bar in kJ/kmol-K == J/mol-K numerically)
kB = C.RBAR / C.constant("Avogadro number")            # J/mol-K / (1/mol) = J/K
chk("kB ~ Rbar/NA", abs(kB - 1.380649e-23) < 1e-27)

print(f"All {_n} tests passed.")
