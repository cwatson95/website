"""
heat_exchanger.py  —  Module 08.3 (Heat exchanger: two-stream thermal transfer)

A (recuperative) HEAT EXCHANGER transfers energy between a HOT stream and a COLD stream
separated by a wall.  Take a control volume around the WHOLE device.  The only work is
flow work (Wdot_cv = 0); when stray heat transfer to the surroundings and KE/PE changes
are negligible the steady energy rate balance is

    0 = Qdot_cv - Wdot_cv + mdot_h (h_hi - h_ho) + mdot_c (h_ci - h_co)   (from Eq. 4.18)

With Qdot_cv = Wdot_cv = 0 this says the energy GIVEN UP by the hot stream is exactly the
energy PICKED UP by the cold stream:

    mdot_h (h_hi - h_ho) = mdot_c (h_co - h_ci)

from which the mass-flow ratio follows:

    mdot_c / mdot_h = (h_hi - h_ho) / (h_co - h_ci)

For an ideal-gas or incompressible stream with constant specific heat, dh = c (T_out - T_in),
so the same balance can be written in terms of temperatures.

Worked anchor: Example 4.7 (power-plant condenser as a two-stream exchanger): the cooling-
water-to-steam mass-flow ratio is 36.3.

Units: h [J/kg or kJ/kg], c [same per K], T [K or degC consistently], mdot [kg/s].
Citations: Moran 8e (PDF = printed + 18; refs.md).
"""


def energy_balance_residual(mdot_h, h_hi, h_ho, mdot_c, h_ci, h_co, Qcv=0.0, Wcv=0.0):
    """Steady whole-exchanger energy-balance residual (should be ~0 at a valid solution):
        Qcv - Wcv + mdot_h (h_hi - h_ho) + mdot_c (h_ci - h_co).
    [Moran from Eq. 4.18, Sec. 4.9.1, p.196]"""
    return Qcv - Wcv + mdot_h * (h_hi - h_ho) + mdot_c * (h_ci - h_co)


def mass_flow_ratio_cold_to_hot(h_hi, h_ho, h_ci, h_co):
    """Adiabatic two-stream exchanger:  mdot_c/mdot_h = (h_hi - h_ho)/(h_co - h_ci).
    [Moran Ex. 4.7 result, from Eq. 4.18, Sec. 4.9.1, p.197]"""
    return (h_hi - h_ho) / (h_co - h_ci)


def mass_flow_other(mdot_known, dh_known, dh_other):
    """Solve mdot_known*dh_known = mdot_other*dh_other for mdot_other, where each dh is the
    magnitude of that stream's enthalpy change.  [Moran from Eq. 4.18, Sec. 4.9.1, p.196]"""
    return mdot_known * dh_known / dh_other


def heat_duty(mdot, h_in, h_out):
    """Per-stream heat rate  Qdot = mdot (h_out - h_in)  (energy added to that stream;
    positive for the cold stream, negative for the hot stream).
    [Moran from Eq. 4.20a, Sec. 4.9.1, p.196]"""
    return mdot * (h_out - h_in)


def sensible_enthalpy_change(cp, T_in, T_out):
    """Ideal-gas / incompressible enthalpy change  dh = cp (T_out - T_in).
    [Moran Eq. 3.51/3.20b, Sec. 3.13.2/3.10.3, p.130/118]"""
    return cp * (T_out - T_in)


def enthalpy_two_phase(hf, hg, x):
    """Two-phase mixture enthalpy  h = hf + x (hg - hf)  (for a condensing/evaporating
    stream).  [Moran Eq. 3.2/3.6 form, Sec. 3.6, p.103]"""
    return hf + x * (hg - hf)


def _demo():
    print("Module 08.3 -- Heat exchanger (two-stream thermal transfer)\n")
    # Example 4.7: condensing steam (hot) vs cooling water (cold).
    # hot: h_hi = 2465.1 (0.1 bar, x=0.95), h_ho = 188.45 (45 C)
    # cold: h_co - h_ci = 62.7 kJ/kg (cooling water 20 -> 35 C)
    h_hi, h_ho = 2465.1, 188.45
    dcold = 62.7                                          # h_co - h_ci
    ratio = mass_flow_ratio_cold_to_hot(h_hi, h_ho, 0.0, dcold)
    print("  Ex 4.7 cooling-water/steam mass-flow ratio = %.1f   [book 36.3]" % ratio)
    # whole-exchanger balance closes (Qcv = Wcv = 0): pick mdot_h = 1, mdot_c = ratio
    res = energy_balance_residual(1.0, h_hi, h_ho, ratio, 0.0, dcold)
    print("  energy-balance residual = %.2e kJ/s (should be ~0)" % res)
    # Quick Quiz: mdot_steam = 125 kg/s -> mdot_water
    mdot_w = mass_flow_other(125.0, h_hi - h_ho, dcold)
    print("  at mdot_steam = 125 kg/s -> cooling water = %.0f kg/s   [book 4538]" % mdot_w)


if __name__ == "__main__":
    _demo()
