"""
pv_diagram.py  —  Module 5.4 (The p-V diagram: area under a path is work)

The p-v-T surface of a pure substance projects onto the pressure-volume (p-v) plane,
where the two-phase region appears as the vapor dome bounded by the saturated-liquid
and saturated-vapor lines, meeting at the critical point (Moran 8e Secs. 3.2-3.3,
pp.97-103).

For a closed system the only work mode of a simple compressible substance is
boundary (pdV) work.  For an INTERNALLY REVERSIBLE (quasiequilibrium) process the
pressure is uniform, so
      dW = p dV                                   (Moran Eq. 2.16, Sec. 2.2.3, p.48)
      W  = integral_1^2 p dV                      (Moran Eq. 2.17, Sec. 2.2.3, p.48)
and this integral is exactly the AREA UNDER THE PATH on a p-V diagram (Moran Sec.
2.2.5, p.49).  Because the area depends on the path, work is not a property.

Closed forms for common reversible paths (Moran Example 2.1, p.50):
      isobaric (p const):   W = p (V2 - V1)
      polytropic pV^n=const, n != 1:  W = (p2 V2 - p1 V1)/(1 - n)
      isothermal ideal gas (n = 1):   W = p1 V1 ln(V2/V1)

This module computes that area (trapezoid rule for an arbitrary path, plus the closed
forms).  Keep units consistent: p in kPa and V in m^3 give W in kJ (1 kPa.m^3 = 1 kJ;
1 bar.m^3 = 100 kJ).  Citations: Moran 8e (PDF page = printed + 18).
"""
import math


def work_pdV(p, V):
    """Boundary work as the AREA under a p-V path, by the trapezoid rule over the
    sampled points (p[i], V[i]):  W = integral p dV = sum 1/2 (p_i+p_{i+1})(V_{i+1}-V_i).
    [Moran Eq. 2.17, Sec. 2.2.5, p.49]"""
    if len(p) != len(V) or len(p) < 2:
        raise ValueError("need >= 2 matching (p, V) samples")
    return sum(0.5 * (p[i] + p[i + 1]) * (V[i + 1] - V[i]) for i in range(len(p) - 1))


def work_isobaric(p, V1, V2):
    """Constant-pressure path:  W = p (V2 - V1)  (a rectangle on p-V).
    [Moran Eq. 2.17, Sec. 2.2.3, p.48]"""
    return p * (V2 - V1)


def p_polytropic(p1, V1, V2, n):
    """Pressure at state 2 on a polytropic path pV^n = const:  p2 = p1 (V1/V2)^n.
    [Moran Example 2.1, Sec. 2.2.5, p.51]"""
    return p1 * (V1 / V2) ** n


def work_polytropic(p1, V1, p2, V2, n):
    """Polytropic path pV^n = const, n != 1:  W = (p2 V2 - p1 V1)/(1 - n).
    [Moran Example 2.1(a), Sec. 2.2.5, p.51]"""
    if abs(n - 1.0) < 1e-12:
        raise ValueError("n = 1 is the isothermal case; use work_isothermal_ideal_gas")
    return (p2 * V2 - p1 * V1) / (1.0 - n)


def work_isothermal_ideal_gas(p1, V1, V2):
    """Isothermal ideal-gas path (pV = const, n = 1):  W = p1 V1 ln(V2/V1).
    [Moran Example 2.1(b), Sec. 2.2.5, p.51]"""
    return p1 * V1 * math.log(V2 / V1)


def _polytropic_path(p1, V1, V2, n, npts=2001):
    """Sample (p, V) along pV^n = const for the trapezoid demo."""
    Vs = [V1 + (V2 - V1) * k / (npts - 1) for k in range(npts)]
    ps = [p1 * (V1 / v) ** n for v in Vs]
    return ps, Vs


def _demo():
    print("Module 5.4 -- p-V diagram: area under the path = work (integral p dV)\n")
    # Moran Example 2.1: gas, p1=3 bar=300 kPa, V1=0.1, V2=0.2 m^3 (W in kJ)
    p1, V1, V2 = 300.0, 0.1, 0.2
    p2 = p_polytropic(p1, V1, V2, 1.5)
    print("  Ex 2.1 (a) n=1.5: p2=%.1f kPa, W=%.1f kJ        [book p2=106 kPa, W=17.6 kJ]"
          % (p2, work_polytropic(p1, V1, p2, V2, 1.5)))
    print("         (b) n=1.0: W=%.2f kJ                       [book 20.79 kJ]"
          % work_isothermal_ideal_gas(p1, V1, V2))
    print("         (c) n=0  : W=%.1f kJ                       [book 30 kJ]"
          % work_isobaric(p1, V1, V2))
    # trapezoid over the sampled polytropic curve reproduces the closed form
    ps, Vs = _polytropic_path(p1, V1, V2, 1.5)
    print("     trapezoid integral p dV over n=1.5 curve = %.2f kJ (-> 17.6)" % work_pdV(ps, Vs))
    # Moran Example 3.4: water, isobaric 10 bar, v 0.3066 -> 0.1944 m^3/kg
    print("  Ex 3.4 isobaric W/m = p(v2-v1) = %.1f kJ/kg     [book -112.2]"
          % work_isobaric(1000.0, 0.3066, 0.1944))
    # Moran Example 6.1: water, isobaric 4.758 bar, v 1.0905e-3 -> 0.3928
    print("  Ex 6.1 isobaric W/m = %.2f kJ/kg                [book 186.38]"
          % work_isobaric(475.8, 1.0905e-3, 0.3928))


if __name__ == "__main__":
    _demo()
