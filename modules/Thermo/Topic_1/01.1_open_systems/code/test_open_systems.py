"""
test_open_systems.py  —  checks for Module 1.1 (Open Systems).

Run:   cd code && python3 test_open_systems.py     ->  "All N tests passed."

Every expected number is hand-derivable (see comments) or read straight from the
steam_tables/ CSVs, so a failure means the physics/unit handling drifted.
"""
import math

import open_systems as os_
from open_systems import (Stream, flow_energy, mass_flow_rate, mass_rate_residual,
                          energy_rate_residual, turbine_power, compressor_power,
                          nozzle_exit_velocity, diffuser_exit_enthalpy,
                          throttle_exit_enthalpy, mixing_exit_enthalpy,
                          heat_exchanger_flow_ratio)
import steam_lookup as st

_n = 0


def chk(name, got, want, tol=1e-2):
    global _n
    if not math.isclose(got, want, rel_tol=0, abs_tol=tol):
        raise AssertionError(f"{name}: got {got!r}, want {want!r} (tol {tol})")
    _n += 1


# 1. flow energy: V^2/2 = 5000 J/kg = 5 kJ/kg at 100 m/s; + g z at z=10 m
chk("flow_energy ke", flow_energy(2700.0, 100.0), 2705.0)
chk("flow_energy ke+pe", flow_energy(2700.0, 100.0, 10.0), 2705.0 + 9.81 * 10 / 1000)

# 2. mass flow rate  mdot = A V / v = 0.1*20/0.2 = 10 kg/s
chk("mass_flow_rate", mass_flow_rate(0.1, 20.0, 0.2), 10.0)

# 3. steady continuity: 2 + 1 in, 3 out  ->  residual 0
chk("mass_rate_residual", mass_rate_residual([Stream(2.0, 0), Stream(1.0, 0)],
                                             [Stream(3.0, 0)]), 0.0)

# 4. steam turbine 60 bar/400 C -> 0.10 bar, x=0.90 (h from the CSVs)
h1 = st.h_superheated(60.0, 400.0)            # 3177.2 kJ/kg (A-4 exact grid point)
h2 = st.h_two_phase(0.10, 0.90)               # 191.83 + 0.9*2392.8 = 2345.35
chk("A-4 h1 exact", h1, 3177.2)
chk("two-phase h2", h2, 2345.35)
sin, sout = Stream(1.0, h1), Stream(1.0, h2)
w = turbine_power(sin, sout)                  # 3177.2 - 2345.35 = 831.85 kJ/kg
chk("turbine_power", w, 831.85)

# 5. the energy rate balance must close for that turbine (internal consistency)
chk("energy_rate closes", energy_rate_residual(0.0, w, [sin], [sout]), 0.0, tol=1e-6)

# 6. turbine with kinetic energy 10 -> 90 m/s: psi_in=+0.05, psi_out=+4.05 kJ/kg
chk("turbine_power +ke", turbine_power(Stream(1, h1, V=10.0), Stream(1, h2, V=90.0)),
    831.85 + 0.05 - 4.05)

# 7. compressor: pumping h2 -> h1 needs +831.85 kW input
chk("compressor_power", compressor_power(Stream(1.0, h2), Stream(1.0, h1)), 831.85)

# 8. nozzle: drop 80 kJ/kg from 10 m/s -> sqrt(10^2 + 2*1000*80) = 400.12 m/s
Vout = nozzle_exit_velocity(3000.0, 2920.0, V_in=10.0)
chk("nozzle_exit_velocity", Vout, math.sqrt(100 + 160000), tol=1e-6)

# 9. diffuser is the inverse: that V_out back to ~10 m/s recovers h_in = 3000
chk("diffuser inverse", diffuser_exit_enthalpy(2920.0, Vout, 10.0), 3000.0, tol=1e-6)

# 10. throttling is isenthalpic
chk("throttle_exit_enthalpy", throttle_exit_enthalpy(271.0), 271.0)

# 11. adiabatic mixing: (2*2700 + 1*400)/3 = 1933.33 kJ/kg
chk("mixing_exit_enthalpy", mixing_exit_enthalpy([Stream(2.0, 2700.0), Stream(1.0, 400.0)]),
    5800.0 / 3.0)

# 12. heat-exchanger flow ratio: (3000-200)/(500-100) = 7
chk("heat_exchanger_flow_ratio", heat_exchanger_flow_ratio(3000.0, 200.0, 100.0, 500.0), 7.0)

# 13. steam_lookup sat interpolation: P=0.05 bar halfway between 0.04 & 0.06 bar
#     T_sat = (28.96 + 36.16)/2 = 32.56 C
chk("sat_pressure interp T", st.sat_pressure(0.05)["T_C"], 32.56, tol=1e-6)

print(f"All {_n} tests passed.")
