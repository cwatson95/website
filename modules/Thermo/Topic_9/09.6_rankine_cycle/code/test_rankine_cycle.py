"""test_rankine_cycle.py — checks for Module 09.6.  Run: python3 test_rankine_cycle.py

Book-verified values from Moran Ex 8.1/8.2/8.3; the plain saturation/superheat lookups
are also cross-checked against the project water tables (../../steam_tables CSVs).
"""
import csv
import math
import os

from rankine_cycle import (turbine_work, condenser_heat, pump_work, boiler_heat,
                           rankine_efficiency, rankine_efficiency_from_heat,
                           back_work_ratio, pump_work_approx,
                           quality_from_entropy, enthalpy_two_phase,
                           ideal_efficiency_avg_temps,
                           turbine_exit_actual, pump_work_actual, reheat_efficiency)

_n = 0
def chk(name, got, want, tol=1e-6):
    global _n
    assert math.isclose(got, want, rel_tol=0, abs_tol=tol), f"{name}: {got!r} != {want!r}"
    _n += 1

# ---- Example 8.1: ideal Rankine, sat vapor 8.0 MPa -> 0.008 MPa, 100 MW -----
h1, s1 = 2758.0, 5.7432                        # Table A-3 @ 8.0 MPa (sat vapor)
sf, sg = 0.5926, 8.2287                        # Table A-3 @ 0.008 MPa
hf, hfg = 173.88, 2403.1
x2 = quality_from_entropy(s1, sf, sg)
chk("x2 = 0.6745", x2, 0.6745, 0.0001)
h2 = enthalpy_two_phase(x2, hf, hfg)
chk("h2 = 1794.8", h2, 1794.8, 0.1)
h3 = hf                                        # sat liquid 0.008 MPa
wp = pump_work_approx(1.0084e-3, 8.0, 8000.0)  # v3 m3/kg, p kPa -> kJ/kg
chk("wp = 8.06 (Eq. 8.7b)", wp, 8.06, 0.01)
h4 = h3 + wp
chk("h4 = 181.94", h4, 181.94, 0.01)
chk("wt = 963.2", turbine_work(h1, h2), 963.2, 0.1)
chk("eta = 0.371", rankine_efficiency(h1, h2, h3, h4), 0.371, 0.001)
chk("bwr = 8.37e-3", back_work_ratio(h1, h2, h3, h4), 8.37e-3, 0.01e-3)
mdot = 100e3 * 3600.0 / ((h1 - h2) - (h4 - h3))          # kg/h
chk("mdot = 3.77e5 kg/h", mdot, 3.77e5, 0.005e5)
# (d)-(f) with the book's rounded mdot = 3.77e5 kg/h (replicating its steps)
chk("Qin = 269.77 MW", 3.77e5 * boiler_heat(h4, h1) / 3600.0 / 1e3, 269.77, 0.05)
chk("Qout = 169.75 MW", 3.77e5 * condenser_heat(h2, h3) / 3600.0 / 1e3, 169.75, 0.05)
chk("mcw = 7.3e6 kg/h", 169.75e3 * 3600.0 / (146.68 - 62.99), 7.3e6, 0.01e6)
# eta from heats matches eta from works (Eq. 8.5b == 8.5a)
chk("8.5b == 8.5a", rankine_efficiency_from_heat(boiler_heat(h4, h1), condenser_heat(h2, h3)),
    rankine_efficiency(h1, h2, h3, h4))
# Quick Quiz: mdot = 150 kg/s -> 143.2 MW at the same eta
chk("quiz 150 kg/s -> 143.2 MW", 150.0 * ((h1 - h2) - (h4 - h3)) / 1e3, 143.2, 0.1)

# ---- Example 8.2: same cycle with eta_t = eta_p = 85% -----------------------
h2a = turbine_exit_actual(h1, h2, 0.85)
chk("h2 actual = 1939.3", h2a, 1939.3, 0.05)
wpa = pump_work_actual(wp, 0.85)
chk("wp actual = 9.48", wpa, 9.48, 0.01)
h4a = h3 + wpa
chk("h4 actual = 183.36", h4a, 183.36, 0.01)
chk("eta = 0.314", rankine_efficiency(h1, h2a, h3, h4a), 0.314, 0.001)
mdot2 = 100e3 * 3600.0 / ((h1 - h2a) - (h4a - h3))
chk("mdot = 4.449e5 kg/h", mdot2, 4.449e5, 0.005e5)
chk("Qin = 318.2 MW", 4.449e5 * boiler_heat(h4a, h1) / 3600.0 / 1e3, 318.2, 0.1)
chk("Qout = 218.2 MW", 4.449e5 * condenser_heat(h2a, h3) / 3600.0 / 1e3, 218.2, 0.1)
# Quick Quiz: mdot = 150 kg/s -> pump power 1422 kW, bwr = 0.0116
chk("quiz pump power = 1422 kW", 150.0 * wpa, 1422.0, 1.0)
chk("quiz bwr = 0.0116", back_work_ratio(h1, h2a, h3, h4a), 0.0116, 0.0001)

# ---- Example 8.3: ideal reheat (8.0 MPa, 480 C; reheat 0.7 MPa, 440 C) ------
h1r, s1r = 3348.4, 6.6586                      # Table A-4 @ 8.0 MPa, 480 C
x2r = quality_from_entropy(s1r, 1.9922, 6.708) # Table A-3 @ 0.7 MPa
chk("x2 = 0.9895", x2r, 0.9895, 0.0001)
h2r = enthalpy_two_phase(x2r, 697.22, 2066.3)
chk("h2 = 2741.8", h2r, 2741.8, 0.1)
h3r, s3r = 3353.3, 7.7571                      # Table A-4 @ 0.7 MPa, 440 C
x4r = quality_from_entropy(s3r, sf, sg)
chk("x4 = 0.9382 (> 0.9 guideline)", x4r, 0.9382, 0.0001)
h4r = enthalpy_two_phase(x4r, hf, hfg)
chk("h4 = 2428.5", h4r, 2428.5, 0.1)
chk("eta reheat = 0.403", reheat_efficiency(h1r, h2r, h3r, h4r, 173.88, 181.94), 0.403, 0.001)
mdot3 = 100e3 * 3600.0 / ((h1r - h2r) + (h3r - h4r) - 8.06)
chk("mdot = 2.363e5 kg/h", mdot3, 2.363e5, 0.003e5)
chk("Qout = 148 MW", 2.363e5 * (h4r - 173.88) / 3600.0 / 1e3, 148.0, 0.2)
# reheat raises both eta and the turbine-exit quality vs Ex 8.1
assert reheat_efficiency(h1r, h2r, h3r, h4r, 173.88, 181.94) > rankine_efficiency(h1, h2, h3, h4);  _n += 1
assert x4r > x2;  _n += 1

# ---- structure/consistency ---------------------------------------------------
# energy balance closes: qin - qout = wt - wp
chk("qin - qout = wnet", boiler_heat(h4, h1) - condenser_heat(h2, h3),
    turbine_work(h1, h2) - pump_work(h3, h4))
# Rankine bwr (~0.8%) is tiny vs the Brayton 40-80% (module 09.5)
assert back_work_ratio(h1, h2, h3, h4) < 0.02;  _n += 1
# below the Carnot ceiling for its saturation-temperature extremes
# (Tsat @ 8.0 MPa = 295.1 C, @ 0.008 MPa = 41.51 C; Table A-3)
eta_carnot = 1.0 - (41.51 + 273.15) / (295.1 + 273.15)
assert rankine_efficiency(h1, h2, h3, h4) < eta_carnot;  _n += 1
# Eq. 8.8 form: raising Tin_bar or lowering Tout raises eta
assert ideal_efficiency_avg_temps(600.0, 315.0) > ideal_efficiency_avg_temps(550.0, 315.0);  _n += 1
assert ideal_efficiency_avg_temps(600.0, 305.0) > ideal_efficiency_avg_temps(600.0, 315.0);  _n += 1

# ---- cross-check pure table lookups vs the project steam-table CSVs ---------
_STEAM = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                                       "..", "..", "..", "steam_tables"))
def _a3(p_bar):
    for r in csv.DictReader(open(os.path.join(_STEAM, "A3_sat_water_pressure.csv"))):
        if math.isclose(float(r["P_bar"]), p_bar, rel_tol=1e-6):
            return r
    raise KeyError(p_bar)

r80 = _a3(80.0)
chk("CSV hg(80 bar) = 2758.0", float(r80["hg_kJkg"]), 2758.0)
chk("CSV sg(80 bar) = 5.7432", float(r80["sg_kJkgK"]), 5.7432)
r008 = _a3(0.08)
chk("CSV hf(0.08 bar) = 173.88", float(r008["hf_kJkg"]), 173.88)
chk("CSV hfg(0.08 bar) = 2403.1", float(r008["hfg_kJkg"]), 2403.1)
chk("CSV sf(0.08 bar) = 0.5926", float(r008["sf_kJkgK"]), 0.5926)
chk("CSV sg(0.08 bar) = 8.2287", float(r008["sg_kJkgK"]), 8.2287)
chk("CSV vf(0.08 bar) = 1.0084e-3", float(r008["vf_x1e3_m3kg"]) * 1e-3, 1.0084e-3)
r7 = _a3(7.0)
chk("CSV hf(7 bar) = 697.22", float(r7["hf_kJkg"]), 697.22)
chk("CSV sf/sg(7 bar)", float(r7["sf_kJkgK"]) + float(r7["sg_kJkgK"]), 1.9922 + 6.7080)
for r in csv.DictReader(open(os.path.join(_STEAM, "A4_superheated_water.csv"))):
    if float(r["P_bar"]) == 80.0 and r["T_C"] == "480":
        chk("CSV A-4 h(80 bar, 480 C) = 3348.4", float(r["h_kJkg"]), 3348.4)
        chk("CSV A-4 s(80 bar, 480 C) = 6.6586", float(r["s_kJkgK"]), 6.6586)
    if float(r["P_bar"]) == 7.0 and r["T_C"] == "440":
        chk("CSV A-4 h(7 bar, 440 C) = 3353.3", float(r["h_kJkg"]), 3353.3)
        chk("CSV A-4 s(7 bar, 440 C) = 7.7571", float(r["s_kJkgK"]), 7.7571)

print(f"All {_n} tests passed.")
