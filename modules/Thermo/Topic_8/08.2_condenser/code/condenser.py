"""
condenser.py  —  Module 08.2 (Condenser: heat-rejection / phase-change exchanger)

A CONDENSER is a single-stream heat exchanger that REJECTS heat from a working fluid,
usually condensing a vapor to liquid at (nearly) constant pressure.  For a control volume
enclosing the working-fluid side, the only work is flow work (Wdot_cv = 0) and kinetic /
potential energy changes are negligible, so the steady energy rate balance reduces to

    Qdot_cv = mdot (h_out - h_in)                                    (from Eq. 4.20a)

Because the fluid LOSES energy (h_out < h_in), Qdot_cv is NEGATIVE -- heat is rejected.
The magnitude of the heat-rejection rate is mdot(h_in - h_out).

In a vapor-compression cycle the condenser sits between the compressor (state 2, hot
vapor) and the expansion valve (state 3, saturated/subcooled liquid); per unit mass of
refrigerant the heat rejected is  Qdot_out/mdot = h2 - h3  (Moran Eq. 10.5, Sec. 10.2.1).

Worked anchors: Example 4.7 (power-plant condenser, steam side: Qdot_cv/mdot =
-2276.7 kJ/kg) and Example 10.4 (heat-pump condenser, Qdot_out = 34.98 kW).

Units: h [J/kg or kJ/kg], mdot [kg/s] -> Qdot in the matching power unit.
Citations: Moran 8e (PDF = printed + 18; refs.md).
"""


def heat_transfer_rate(mdot, h_in, h_out):
    """Signed heat-transfer rate  Qdot_cv = mdot (h_out - h_in)  (Wdot_cv = 0, dKE,dPE = 0).
    NEGATIVE for a condenser (h_out < h_in).  [Moran from Eq. 4.20a, Sec. 4.9.1, p.196]"""
    return mdot * (h_out - h_in)


def heat_rejected(mdot, h_in, h_out):
    """Magnitude of heat REJECTED  = mdot (h_in - h_out) = -Qdot_cv (positive).
    [Moran from Eq. 4.20a, Sec. 4.9.1, p.196]"""
    return mdot * (h_in - h_out)


def condenser_heat_per_mass(h2, h3):
    """Cycle condenser: heat rejected per unit mass  Qdot_out/mdot = h2 - h3
    (state 2 = compressor exit, state 3 = condenser exit liquid).
    [Moran Eq. 10.5, Sec. 10.2.1, p.613]"""
    return h2 - h3


def enthalpy_two_phase(hf, hg, x):
    """Enthalpy of a two-phase liquid-vapor mixture  h = hf + x (hg - hf).
    [Moran Eq. 3.2/3.6 form, Sec. 3.6, p.103]"""
    return hf + x * (hg - hf)


def quality_from_h(h, hf, hg):
    """Quality from enthalpy  x = (h - hf)/(hg - hf)  (0 <= x <= 1 in the dome).
    [Moran Eq. 3.6 rearranged, Sec. 3.6, p.103]"""
    return (h - hf) / (hg - hf)


def _demo():
    print("Module 08.2 -- Condenser (heat-rejection / phase-change exchanger)\n")
    # Example 4.7 steam side: steam in at 0.1 bar, x=0.95; condensate out at 45 C.
    # Table A-3 @0.1 bar: hf=191.83, hg=2584.7; Table A-2 @45 C: hf=188.45 kJ/kg.
    h1 = enthalpy_two_phase(191.83, 2584.7, 0.95)        # 2465.1 kJ/kg
    h2 = 188.45                                            # hf(45 C)
    q = heat_transfer_rate(1.0, h1, h2)                   # per kg of steam
    print("  Ex 4.7 condenser (steam side): h1 = %.1f kJ/kg [book 2465.1]" % h1)
    print("    Qdot_cv/mdot = h2 - h1 = %.1f kJ/kg   [book -2276.7]" % q)
    # Example 10.4 heat-pump condenser: h2=280.19, h3=105.29 kJ/kg, mdot=0.2 kg/s.
    Qout = heat_rejected(0.2, 280.19, 105.29)            # kW (= mdot(h2-h3))
    print("  Ex 10.4 heat-pump condenser: Qdot_out = %.2f kW   [book 34.98]" % Qout)
    print("    per-mass: h2 - h3 = %.2f kJ/kg" % condenser_heat_per_mass(280.19, 105.29))


if __name__ == "__main__":
    _demo()
