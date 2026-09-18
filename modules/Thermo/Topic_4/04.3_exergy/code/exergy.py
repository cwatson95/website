"""
exergy.py  —  Module 4.3 (Exergy / availability)

Exergy is the MAXIMUM theoretical work obtainable as a system comes into equilibrium
with a reference environment (the *dead state* at T0, p0).  Built from combined
energy + entropy balances (Moran 8e Ch.7).  Unlike energy, exergy is DESTROYED by
irreversibilities, and the destruction is tied straight to entropy production:
Ed = T0 * sigma (Eq. 7.7) -- this is the bridge from module 4.2.

System exergy (Eq. 7.1) / specific (Eq. 7.2):
    E = (U-U0) + p0(V-V0) - T0(S-S0) + KE + PE
Closed-system exergy balance (Eq. 7.4):
    E2 - E1 = Eq - Ew - Ed
      Eq = integral (1 - T0/Tb) dQ        exergy transfer with heat   (Eq. 7.5)
      Ew = W - p0 (V2 - V1)               exergy transfer with work   (Eq. 7.6)
      Ed = T0 * sigma  (>= 0)             exergy destruction          (Eq. 7.7)

T0 in K (or degR); energies in kJ (or Btu) consistently.  Citations: Moran 8e
(PDF = printed + 18); see ../refs.md.
"""
import math


def specific_exergy(u, v, s, u0, v0, s0, T0, p0, KE=0.0, PE=0.0):
    """Specific exergy relative to the dead state (T0, p0):
    e = (u-u0) + p0 (v-v0) - T0 (s-s0) + KE + PE. [Moran Eq. 7.2, Sec. 7.3.2, p.376]"""
    return (u - u0) + p0 * (v - v0) - T0 * (s - s0) + KE + PE


def exergy_change(dU, dV, dS, T0, p0, dKE=0.0, dPE=0.0):
    """Exergy change between two states:
    E2-E1 = (U2-U1) + p0(V2-V1) - T0(S2-S1) + dKE + dPE. [Moran Eq. 7.3, Sec. 7.3.3, p.378]"""
    return dU + p0 * dV - T0 * dS + dKE + dPE


def exergy_transfer_heat(Q, T0, Tb):
    """Exergy transferred with heat Q across a boundary at Tb:
    Eq = (1 - T0/Tb) Q. [Moran Eq. 7.5, Sec. 7.4.1, p.380]"""
    return (1.0 - T0 / Tb) * Q


def exergy_transfer_work(W, p0, dV):
    """Exergy transferred with work:  Ew = W - p0 (V2 - V1). [Moran Eq. 7.6, Sec. 7.4.1, p.380]"""
    return W - p0 * dV


def exergy_destruction(T0, sigma):
    """Exergy destroyed by irreversibility:  Ed = T0 * sigma  (>= 0).
    The direct bridge to entropy production (module 4.2). [Moran Eq. 7.7, Sec. 7.4.1, p.380]"""
    return T0 * sigma


def exergy_change_incompressible(m, c, T1, T2, T0):
    """Exergy change of an incompressible body (const volume):
    E2-E1 = m c [ (T2-T1) - T0 ln(T2/T1) ].  (From Eq. 7.3 with dU=mc dT, dS=mc dT/T.)
    [Moran Sec. 7.3; cf. Eq. 6.13]"""
    return m * c * ((T2 - T1) - T0 * math.log(T2 / T1))


def _demo():
    print("Module 4.3 -- Exergy  (Ed = T0 * sigma; exergy is destroyed, energy is not)\n")
    # Ex 7.2 -- reworks the Ex 6.1 water process; dead state T0=293.15 K, p0=100 kPa
    T0, p0 = 293.15, 100.0
    Eq = exergy_transfer_heat(2114.1, T0, 423.15)        # 649.49 kJ/kg
    Ew = exergy_transfer_work(186.38, p0, 0.39171)        # 147.21 kJ/kg
    Ed = exergy_destruction(T0, 0.0)                      # 0 (reversible)
    print("  Ex 7.2 (water, reversible): Eq/m=%.2f, Ew/m=%.2f, Ed/m=%.1f kJ/kg" % (Eq, Ew, Ed))
    print("    -> de = Eq - Ew - Ed = %.2f kJ/kg  [book 502.38]" % (Eq - Ew - Ed))
    # Ex 7.3 -- oven wall: exergy destroyed by heat conduction across a finite dT
    Eq1 = exergy_transfer_heat(0.2, 293.0, 575.0)
    Eq2 = exergy_transfer_heat(0.2, 293.0, 310.0)
    print("\n  Ex 7.3 (oven wall): Ed/A = Eq_in - Eq_out = %.3f kW/m^2  [book ~0.09]" % (Eq1 - Eq2))
    # HW 7.32 -- rigid insulated air + paddle: all work-exergy in is mostly destroyed
    sigma = 0.5 * 0.171 * math.log(600.0 / 520.0)
    print("\n  HW 7.32 (air, paddle): Ed = T0 sigma = %.2f Btu, dE = %.2f Btu  [book 6.57, 0.27]"
          % (exergy_destruction(537.0, sigma), exergy_change(6.84, 0.0, sigma, 537.0, 14.7)))


if __name__ == "__main__":
    _demo()
