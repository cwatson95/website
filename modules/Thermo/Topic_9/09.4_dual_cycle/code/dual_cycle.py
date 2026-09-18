"""
dual_cycle.py  —  Module 09.4 (Air-Standard Dual Cycle)

The air-standard DUAL cycle blends the Otto and Diesel cycles: heat is added in TWO
steps -- first at constant volume (as in Otto), then at constant pressure (as in Diesel).
It models real internal-combustion p-V diagrams better than either limit (Moran 8e
Sec. 9.4, Fig. 9.7):

  1-2  isentropic compression
  2-3  constant-VOLUME   heat addition   (pressure ratio   rp = p3/p2)
  3-4  constant-PRESSURE heat addition   (cutoff/volume ratio rc = V4/V3); first part of
                                          the power stroke
  4-5  isentropic expansion (remainder of the power stroke)
  5-1  constant-volume heat rejection

Because 2-3 is constant volume (Q = du) and 3-4 is constant pressure (Q = dh), the
thermal efficiency from the air tables (Table A-22) is (Eq. 9.14)

  eta = 1 - (u5 - u1) / [ (u3 - u2) + (h4 - h3) ]        (air-table form; Table A-22)

On a COLD AIR-STANDARD basis (constant specific heats) this collapses to a closed form
in the compression ratio r = V1/V2, the pressure ratio rp = p3/p2, and the cutoff ratio
rc = V4/V3:

  eta = 1 - (1/r^(k-1)) * ( rp*rc^k - 1 ) / ( (rp - 1) + k*rp*(rc - 1) )

This reduces to the two bracketing cycles:
  * rc -> 1 (no constant-p burn)  ->  Otto    eta = 1 - 1/r^(k-1)              (Eq. 9.8)
  * rp -> 1 (no constant-V burn)  ->  Diesel  eta = 1 - (1/r^(k-1))(rc^k-1)/(k(rc-1)) (Eq. 9.13)

k = 1.4 for air.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""

K_AIR = 1.4


def dual_efficiency(r, rp, rc, k=K_AIR):
    """Cold air-standard dual-cycle thermal efficiency:
    eta = 1 - (1/r^(k-1)) (rp*rc^k - 1) / ((rp-1) + k*rp*(rc-1)),
    r = compression ratio, rp = p3/p2 (constant-V), rc = V4/V3 (constant-p).
    Reduces to Otto (rc->1) and Diesel (rp->1). [Moran Sec. 9.4 (cold air-standard), p.523]"""
    num = rp * rc ** k - 1.0
    den = (rp - 1.0) + k * rp * (rc - 1.0)
    if abs(den) < 1e-12:
        # rp -> 1 AND rc -> 1 together sends both num and den to zero. Writing
        # rp = 1+a, rc = 1+b: num ~ a + k b and den ~ a + k b, so num/den -> 1
        # and eta -> 1 - r^(1-k), the Otto value. Evaluating the fraction here
        # would be 0/0, so return that limit directly -- otherwise the docstring's
        # "reduces to Otto (rc->1)" would be true only as a limit, never at
        # the point itself.
        return 1.0 - 1.0 / r ** (k - 1.0)
    return 1.0 - (1.0 / r ** (k - 1.0)) * num / den


def dual_efficiency_air_table(u1, u2, u3, h3, h4, u5):
    """Air-standard dual efficiency from tabulated properties (Table A-22):
    eta = 1 - (u5 - u1)/[(u3 - u2) + (h4 - h3)]  (constant-V then constant-p heat add).
    [Moran Eq. 9.14, Sec. 9.4, p.523]"""
    return 1.0 - (u5 - u1) / ((u3 - u2) + (h4 - h3))


def pressure_ratio(p3, p2):
    """Constant-volume pressure ratio rp = p3/p2 = T3/T2 (the Otto-like burn).
    [Moran Sec. 9.4, p.523]"""
    return p3 / p2


def cutoff_ratio(V4, V3):
    """Constant-pressure cutoff (volume) ratio rc = V4/V3 = T4/T3 (the Diesel-like burn).
    [Moran Sec. 9.4, p.523]"""
    return V4 / V3


def temp_after_isentropic_compression(T1, r, k=K_AIR):
    """End-of-compression temperature, cold air-standard:  T2 = T1 r^(k-1).
    [Moran Sec. 9.4, p.523]"""
    return T1 * r ** (k - 1.0)


def temp_after_constant_volume_heat(T2, rp):
    """End-of-constant-volume-heat temperature:  T3 = rp T2  (p3/p2 = T3/T2).
    [Moran Sec. 9.4, p.523]"""
    return rp * T2


def temp_after_constant_pressure_heat(T3, rc):
    """End-of-constant-pressure-heat temperature:  T4 = rc T3  (V4/V3 = T4/T3).
    [Moran Sec. 9.4, p.523]"""
    return rc * T3


def temp_after_isentropic_expansion(T4, r, rc, k=K_AIR):
    """End-of-expansion temperature, cold air-standard:  T5 = T4 (rc/r)^(k-1),
    using V5/V4 = r/rc (V5 = V1, V3 = V2). [Moran Sec. 9.4, p.524]"""
    return T4 * (rc / r) ** (k - 1.0)


def mean_effective_pressure(w_net, v1, r):
    """Mean effective pressure from net work per unit mass:  mep = w_net/(v1(1 - 1/r)),
    with the displacement per unit mass v1 - v2 = v1(1 - 1/r). [Moran Sec. 9.4, p.524]"""
    return w_net / (v1 * (1.0 - 1.0 / r))


def _demo():
    print("Module 09.4 -- Air-Standard Dual Cycle  (constant-V + constant-p heat addition)\n")
    print("  Example 9.3 (r=18, rp=1.5, rc=1.2, T1=300 K, p1=0.1 MPa):")
    eta = dual_efficiency_air_table(214.07, 673.2, 1065.8, 1452.6, 1778.3, 475.96)
    print("    air-table eta = 1 - (u5-u1)/[(u3-u2)+(h4-h3)] = %.3f   [book 0.635]" % eta)
    w_net = (1065.8 - 673.2) + (1778.3 - 1452.6) - (475.96 - 214.07)
    print("    net work = %.1f kJ/kg   [book 456]" % w_net)
    print("    mep = %.2f MPa   [book 0.56]" % (mean_effective_pressure(w_net, 0.861, 18.0) / 1e3))
    print("    cold air-standard closed form (same r,rp,rc): eta = %.3f   (overpredicts)"
          % dual_efficiency(18.0, 1.5, 1.2))
    print("\n  The dual cycle brackets Otto and Diesel:")
    print("    rc -> 1 (no constant-p burn) -> Otto:   dual(18,1.5,1+e) = %.4f  ~  %.4f"
          % (dual_efficiency(18.0, 1.5, 1.0 + 1e-9), 1.0 - 1.0 / 18.0 ** 0.4))
    print("    rp -> 1 (no constant-V burn) -> Diesel: dual(18,1+e,2) = %.4f  ~  %.4f"
          % (dual_efficiency(18.0, 1.0 + 1e-9, 2.0),
             1.0 - (1.0 / 18.0 ** 0.4) * (2.0 ** 1.4 - 1.0) / (1.4 * (2.0 - 1.0))))


if __name__ == "__main__":
    _demo()
