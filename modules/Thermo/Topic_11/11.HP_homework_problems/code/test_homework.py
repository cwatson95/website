"""test_homework.py — checks for Module 11.HP (Moran Ch.12 psychrometric problems).
Run: python3 test_homework.py.

Moran has NO answer key for end-of-chapter problems, so these verify (a) the worked
solution values reproduce, and (b) physical consistency (dew point vs dry bulb, omega
ordering for humidification vs dehumidification, mass-balance closure, sign of Q)."""
import math
from homework import (p12_51, p12_52, p12_56, p12_60, p12_77, p12_78, p12_92)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

def ok(name, cond):
    global _n
    assert cond, f"{name}: consistency check failed"
    _n += 1


# ===== 12.51  cooling at constant pressure (SI) =====
r = p12_51()
chk("12.51 omega1", r["omega1"], 0.006674, 5e-6)
chk("12.51 dew C", r["dew_point_C"], 18.44, 0.05)
chk("12.51 ma", r["ma"], 595.98, 0.05)
chk("12.51 Q", r["Q_kJ_per_h"], -6062.0, 2.0)
ok("12.51 dew point below dry bulb", r["dew_point_C"] < 30.0)
ok("12.51 no condensation (dew < 20 C exit)", r["condensation"] is False and r["omega2"] == r["omega1"])
ok("12.51 cooling Q < 0", r["Q_kJ_per_h"] < 0)

# ===== 12.52  isothermal compression -> condensation (English) =====
r = p12_52()
chk("12.52 omega1", r["omega1"], 0.016516, 5e-6)
chk("12.52 omega2", r["omega2"], 0.010221, 5e-6)
chk("12.52 mw", r["mw_condensed"], 0.012385, 5e-5)
ok("12.52 condensation occurs", r["condensation"] is True)
ok("12.52 omega drops (vapor removed)", r["omega2"] < r["omega1"])
ok("12.52 condensate positive", r["mw_condensed"] > 0)

# ===== 12.56  dew point of N2/water-vapor mixture (English) =====
r = p12_56()
chk("12.56 pv", r["pv"], 2.9392, 1e-3)
chk("12.56 dew F", r["dew_point_F"], 140.57, 0.05)
ok("12.56 pv = yv*p", math.isclose(r["pv"], 0.20 * 14.696, abs_tol=1e-6))
ok("12.56 dew point below dry bulb", r["dew_point_F"] < 200.0)

# ===== 12.60  dehumidifier with refrigerant (SI) =====
r = p12_60()
chk("12.60 omega1", r["omega1"], 0.020795, 5e-6)
chk("12.60 omega2", r["omega2"], 0.010241, 5e-6)
chk("12.60 mw/ma", r["mw_per_ma"], 0.010554, 5e-6)
chk("12.60 mr/ma", r["mr_per_ma"], 0.4167, 1e-3)
ok("12.60 dehumidification (omega drops)", r["omega2"] < r["omega1"])
ok("12.60 mw/ma = omega1-omega2", math.isclose(r["mw_per_ma"], r["omega1"] - r["omega2"], abs_tol=1e-9))
ok("12.60 refrigerant flow positive", r["mr_per_ma"] > 0)

# ===== 12.77  wet-bulb / dry-bulb then cooling (English) =====
r = p12_77()
chk("12.77 omega'", r["omega_prime"], 0.014691, 5e-6)
chk("12.77 omega1", r["omega1"], 0.011441, 5e-6)
chk("12.77 phi1", r["phi1"], 0.490, 2e-3)
chk("12.77 dew F", r["dew_point_F"], 60.97, 0.05)
chk("12.77 Q", r["Q_Btu_per_min"], -48.44, 0.1)
ok("12.77 wet-bulb depression positive (omega < omega')", r["omega1"] < r["omega_prime"])
ok("12.77 phi < 1 (unsaturated)", r["phi1"] < 1.0)
ok("12.77 dew(61) < wet-bulb(68) < dry-bulb(82)", r["dew_point_F"] < 68.0)
ok("12.77 cooled to 62 F > dew point -> no condensation", r["condensation"] is False)

# ===== 12.78  dehumidifier (SI) =====
r = p12_78()
chk("12.78 omega1", r["omega1"], 0.017767, 5e-6)
chk("12.78 omega2", r["omega2"], 0.010646, 5e-6)
chk("12.78 condensate/ma", r["condensate_per_ma"], 0.007122, 5e-6)
chk("12.78 Q/ma", r["Q_per_ma"], -38.31, 0.05)
ok("12.78 dehumidification (omega drops)", r["omega2"] < r["omega1"])
ok("12.78 condensate = omega1-omega2", math.isclose(r["condensate_per_ma"], r["omega1"] - r["omega2"], abs_tol=1e-9))
ok("12.78 heat removed (Q<0)", r["Q_per_ma"] < 0)

# ===== 12.92  evaporative cooler (SI) =====
r = p12_92()
chk("12.92 omega1", r["omega1"], 0.003521, 5e-6)
chk("12.92 omega2", r["omega2"], 0.007627, 5e-6)
chk("12.92 ma", r["ma"], 56.247, 0.02)
chk("12.92 liquid rate", r["liquid_rate"], 0.2309, 5e-4)
chk("12.92 phi2", r["phi2"], 0.382, 2e-3)
ok("12.92 humidification (omega rises)", r["omega2"] > r["omega1"])
ok("12.92 liquid added = ma(omega2-omega1)", math.isclose(r["liquid_rate"], r["ma"] * (r["omega2"] - r["omega1"]), abs_tol=1e-9))
ok("12.92 evaporative cooling raises phi", r["phi2"] > 0.10)

print(f"All {_n} tests passed.")
