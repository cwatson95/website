"""
diesel_cycle.py  —  Module 09.3 (Air-Standard Diesel Cycle)

The air-standard Diesel cycle models the compression-ignition engine.  It keeps the
Otto cycle's isentropic compression but adds heat at constant PRESSURE rather than
constant volume (Moran 8e Sec. 9.3, Fig. 9.5):

  1-2  isentropic compression
  2-3  constant-PRESSURE heat addition   (fuel injected into hot compressed air, burns)
  3-4  isentropic expansion (remainder of the power stroke)
  4-1  constant-volume heat rejection

Because process 2-3 does p-V work, the heat added is an ENTHALPY difference, and the
thermal efficiency is (Eq. 9.11)

  eta = 1 - (u4 - u1)/(h3 - h2)                         (air-table form; Table A-22)

On a COLD AIR-STANDARD basis (constant specific heats) this becomes a closed form in
the compression ratio r = V1/V2 and the CUTOFF RATIO rc = V3/V2 (Eq. 9.13):

  eta = 1 - (1/r^(k-1)) * ( (rc^k - 1) / (k*(rc - 1)) )   (cold air-standard)

The bracket exceeds 1 for rc > 1, so for the SAME r the Diesel cycle is LESS efficient
than the Otto cycle; as rc -> 1 it reduces to the Otto form 1 - 1/r^(k-1) (Eq. 9.8).
Diesels run at higher r (12-20) than spark engines.  k = 1.4 for air.
Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""

K_AIR = 1.4


def diesel_efficiency(r, rc, k=K_AIR):
    """Cold air-standard Diesel thermal efficiency:
    eta = 1 - (1/r^(k-1)) * (rc^k - 1)/(k(rc - 1)),
    r = compression ratio, rc = cutoff ratio V3/V2. [Moran Eq. 9.13, Sec. 9.3, p.519]"""
    return 1.0 - (1.0 / r ** (k - 1.0)) * (rc ** k - 1.0) / (k * (rc - 1.0))


def diesel_efficiency_air_table(u1, u4, h2, h3):
    """Air-standard Diesel efficiency from tabulated properties (Table A-22):
    eta = 1 - (u4 - u1)/(h3 - h2)  (heat added at constant p -> enthalpy).
    [Moran Eq. 9.11, Sec. 9.3, p.519]"""
    return 1.0 - (u4 - u1) / (h3 - h2)


def cutoff_ratio(V3, V2):
    """Cutoff ratio rc = V3/V2 = T3/T2 (constant-pressure heat-addition stretch).
    [Moran Sec. 9.3, p.519]"""
    return V3 / V2


def temp_after_isentropic_compression(T1, r, k=K_AIR):
    """End-of-compression temperature, cold air-standard:  T2 = T1 r^(k-1).
    [Moran Sec. 9.3, p.519]"""
    return T1 * r ** (k - 1.0)


def temp_after_constant_pressure_heat(T2, rc):
    """End-of-heat-addition temperature:  T3 = rc T2  (constant p, V3/V2 = rc).
    [Moran Sec. 9.3, p.519]"""
    return rc * T2


def temp_after_isentropic_expansion(T3, r, rc, k=K_AIR):
    """End-of-expansion temperature, cold air-standard:  T4 = T3 (rc/r)^(k-1),
    using V4/V3 = r/rc (Eq. 9.12). [Moran Sec. 9.3, p.519]"""
    return T3 * (rc / r) ** (k - 1.0)


def _demo():
    print("Module 09.3 -- Air-Standard Diesel Cycle  (compression ignition; constant-p burn)\n")
    print("  Cold air-standard, k=1.4 (cutoff ratio rc=2):")
    for r in (15.0, 18.0, 21.0):
        print("    r=%2d, rc=2 -> eta = %.4f" % (int(r), diesel_efficiency(r, 2.0)))
    print("\n  Example 9.2 (r=18, rc=2, T1=300 K, p1=0.1 MPa):")
    print("    air-table (u1=214.07,u4=664.3,h2=930.98,h3=1999.1): eta = %.3f   [book 0.578]"
          % diesel_efficiency_air_table(214.07, 664.3, 930.98, 1999.1))
    print("    cold air-standard closed form (Eq. 9.13):          eta = %.3f   (overpredicts)"
          % diesel_efficiency(18.0, 2.0))
    print("\n  As rc -> 1 the Diesel cycle reduces to Otto:")
    print("    diesel(18, rc=1.0001) = %.4f  ~  otto 1-1/18^0.4 = %.4f"
          % (diesel_efficiency(18.0, 1.0001), 1.0 - 1.0/18.0**0.4))


if __name__ == "__main__":
    _demo()
