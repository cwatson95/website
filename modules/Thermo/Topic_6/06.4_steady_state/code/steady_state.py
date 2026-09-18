"""
steady_state.py  —  Module 6.4 (Analyzing Control Volumes at Steady State)

A control volume is at STEADY STATE when every property is unchanging in time.  Then
there is no accumulation of mass or energy, so the storage terms of the rate balances
vanish (Moran 8e Sec. 4.5):

    dm_cv/dt = 0   ->   sum(mdot_i) = sum(mdot_e)                        (Eq. 4.6)
    dE_cv/dt = 0   ->   0 = Qdot_cv - Wdot_cv
                            + sum_i mdot_i (h_i + V_i^2/2 + g z_i)
                            - sum_e mdot_e (h_e + V_e^2/2 + g z_e)       (Eq. 4.18)

For the common ONE-inlet, ONE-exit device (mdot_1 = mdot_2 = mdot), this is the
steady-state energy rate balance

    0 = Qdot_cv - Wdot_cv + mdot[(h1 - h2) + (V1^2 - V2^2)/2 + g(z1 - z2)]   (Eq. 4.20a)

an accounting balance: at steady state the rate energy enters the CV equals the rate it
leaves.  Only boundary transfer quantities appear; nothing about the interior is needed.

Units: Qdot, Wdot [kW]; mdot [kg/s]; h [kJ/kg]; V [m/s]; z [m]; g [m/s^2].  Kinetic and
potential terms are converted from J/kg to kJ/kg (divide by 1000) internally.
Citations: Moran 8e (PDF = printed + 18).  Worked Example 4.4 (steam turbine).
"""


def steady_mass_residual(mdot_in, mdot_out):
    """Steady-state mass balance residual  sum(mdot_i) - sum(mdot_e)  (= 0 at steady state).
    [Moran Eq. 4.6, Sec. 4.5.1, p.181]"""
    si = sum(mdot_in) if hasattr(mdot_in, "__iter__") else mdot_in
    se = sum(mdot_out) if hasattr(mdot_out, "__iter__") else mdot_out
    return si - se


def is_steady(dmcv_dt_val, dEcv_dt_val, tol=1e-9):
    """Steady-state test: True iff both dm_cv/dt = 0 and dE_cv/dt = 0.
    [Moran Sec. 4.5.1, p.181]"""
    return abs(dmcv_dt_val) <= tol and abs(dEcv_dt_val) <= tol


def delta_ke(V1, V2):
    """Specific kinetic-energy change (V2^2 - V1^2)/2, returned in kJ/kg.
    [Moran Eq. 4.20, Sec. 4.5.1, p.181]"""
    return (V2 ** 2 - V1 ** 2) / 2.0 / 1000.0


def heat_rate_steady(Wdot_cv, mdot, h1, h2, V1=0.0, V2=0.0, z1=0.0, z2=0.0, g=9.81):
    """One-inlet/one-exit steady-state energy rate balance solved for heat transfer:
    Qdot_cv = Wdot_cv + mdot[(h2 - h1) + (V2^2 - V1^2)/2 + g(z2 - z1)]  [kW].
    [Moran Eq. 4.20a, Sec. 4.5.1, p.181]"""
    dke = (V2 ** 2 - V1 ** 2) / 2.0 / 1000.0      # J/kg -> kJ/kg
    dpe = g * (z2 - z1) / 1000.0                  # J/kg -> kJ/kg
    return Wdot_cv + mdot * ((h2 - h1) + dke + dpe)


def power_rate_steady(Qdot_cv, mdot, h1, h2, V1=0.0, V2=0.0, z1=0.0, z2=0.0, g=9.81):
    """One-inlet/one-exit steady-state energy rate balance solved for power:
    Wdot_cv = Qdot_cv + mdot[(h1 - h2) + (V1^2 - V2^2)/2 + g(z1 - z2)]  [kW].
    [Moran Eq. 4.20a, Sec. 4.5.1, p.181]"""
    dke = (V1 ** 2 - V2 ** 2) / 2.0 / 1000.0
    dpe = g * (z1 - z2) / 1000.0
    return Qdot_cv + mdot * ((h1 - h2) + dke + dpe)


def turbine_power_adiabatic(mdot, h1, h2):
    """Adiabatic turbine, KE & PE negligible:  Wdot_cv = mdot (h1 - h2)  [kW].
    [Moran Eq. (b), Sec. 4.7.1, p.188]"""
    return mdot * (h1 - h2)


def _demo():
    print("Module 6.4 -- Control Volumes at Steady State  (dm/dt=0, dE/dt=0)\n")
    # Example 4.4: steam turbine, steady state (p.188-189)
    mdot = 4600.0 / 3600.0                         # 4600 kg/h -> kg/s
    Qcv = heat_rate_steady(1000.0, mdot, 3177.2, 2345.4, V1=10.0, V2=30.0)
    print("  Ex 4.4 steam turbine: dKE = %.1f kJ/kg, Qcv = %.1f kW   [book +0.4 kJ/kg, -62.3 kW]"
          % (delta_ke(10.0, 30.0), Qcv))
    # invert: recovering the 1000 kW power output from Qcv closes the balance
    W = power_rate_steady(Qcv, mdot, 3177.2, 2345.4, V1=10.0, V2=30.0)
    print("  balance closes: power back-solved = %.1f kW  [given 1000]" % W)
    print("  neglecting KE (turbine_power_adiabatic style): Qcv = %.1f kW  [book -62.9]"
          % heat_rate_steady(1000.0, mdot, 3177.2, 2345.4))


if __name__ == "__main__":
    _demo()
