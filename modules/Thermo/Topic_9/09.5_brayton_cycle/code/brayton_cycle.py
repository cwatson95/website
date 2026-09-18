"""
brayton_cycle.py  —  Module 09.5 (Air-Standard Brayton Cycle)

The air-standard Brayton cycle models the GAS TURBINE: a compressor, a heat exchanger
(replacing the combustor), a turbine, and a second heat exchanger closing the loop
(Moran 8e Sec. 9.6, Fig. 9.9).  Four internally reversible processes of air at steady
state:

  1-2  isentropic compression   (compressor;  work IN)
  2-3  constant-pressure heat addition
  3-4  isentropic expansion     (turbine;     work OUT)
  4-1  constant-pressure heat rejection

Reducing the control-volume mass/energy balances (ke/pe negligible) gives, per unit
of mass flowing (Sec. 9.6.1):

  Wt/m = h3 - h4    (9.15)      Qin/m  = h3 - h2   (9.17)
  Wc/m = h2 - h1    (9.16)      Qout/m = h4 - h1   (9.18)

  eta = [(h3-h4) - (h2-h1)] / (h3-h2)               (Eq. 9.19, air-table; Table A-22)
  bwr = (h2-h1)/(h3-h4)                             (Eq. 9.20, back work ratio)

Because the compressor handles GAS, the back work ratio is large -- typically 40-80%
of the turbine output, vs only 1-2% for the Rankine pump (module 09.6).  On a COLD
AIR-STANDARD basis (constant specific heats) the isentropic relations T2 = T1 rp^((k-1)/k)
and T4 = T3 (1/rp)^((k-1)/k) (Eqs. 9.23, 9.24) collapse Eq. 9.19 to

  eta = 1 - 1/rp^((k-1)/k)                          (Eq. 9.25, cold air-standard)

where rp = p2/p1 is the COMPRESSOR PRESSURE RATIO.  Efficiency rises with rp; the net
work per unit mass instead peaks at rp = (T3/T1)^(k/(2(k-1))) (Example 9.5).  Real
turbines/compressors have isentropic efficiencies eta_t, eta_c (Sec. 9.6.3), and a
REGENERATOR preheats the compressor exit with turbine exhaust (Sec. 9.7, Eq. 9.27).
k = 1.4 for air.  Citations: Moran 8e (PDF = printed + 18); see ../refs.md.
"""

K_AIR = 1.4  # cp/cv for air, cold air-standard (Moran Table A-20, ~300 K)


# --- component work and heat transfers (Sec. 9.6.1) --------------------------
def turbine_work(h3, h4):
    """Turbine work per unit of mass flowing:  Wt/m = h3 - h4.
    [Moran Eq. 9.15, Sec. 9.6.1, p.527]"""
    return h3 - h4


def compressor_work(h1, h2):
    """Compressor work INPUT per unit of mass flowing:  Wc/m = h2 - h1 (positive).
    [Moran Eq. 9.16, Sec. 9.6.1, p.527]"""
    return h2 - h1


def heat_added(h2, h3):
    """Heat added per unit of mass flowing:  Qin/m = h3 - h2.
    [Moran Eq. 9.17, Sec. 9.6.1, p.527]"""
    return h3 - h2


def heat_rejected(h1, h4):
    """Heat rejected per unit of mass flowing:  Qout/m = h4 - h1 (positive).
    [Moran Eq. 9.18, Sec. 9.6.1, p.528]"""
    return h4 - h1


def brayton_efficiency_air_table(h1, h2, h3, h4):
    """Air-standard Brayton thermal efficiency from tabulated enthalpies (Table A-22):
    eta = [(h3 - h4) - (h2 - h1)]/(h3 - h2). [Moran Eq. 9.19, Sec. 9.6.1, p.528]"""
    return ((h3 - h4) - (h2 - h1)) / (h3 - h2)


def back_work_ratio(h1, h2, h3, h4):
    """Back work ratio:  bwr = (Wc/m)/(Wt/m) = (h2 - h1)/(h3 - h4).  Gas turbines run
    40-80% (vs 1-2% for vapor power plants). [Moran Eq. 9.20, Sec. 9.6.1, p.528]"""
    return (h2 - h1) / (h3 - h4)


# --- ideal-cycle isentropic legs (Sec. 9.6.2) --------------------------------
def pr_after_compression(pr1, rp):
    """Relative pressure after isentropic compression:  pr2 = pr1 (p2/p1)
    (pr tabulated vs T in Table A-22). [Moran Eq. 9.21, Sec. 9.6.2, p.529]"""
    return pr1 * rp


def pr_after_expansion(pr3, rp):
    """Relative pressure after isentropic expansion:  pr4 = pr3 (p4/p3) = pr3/rp
    (constant-p heat exchangers give p4/p3 = p1/p2). [Moran Eq. 9.22, Sec. 9.6.2, p.529]"""
    return pr3 / rp


def temp_after_isentropic_compression(T1, rp, k=K_AIR):
    """End-of-compression temperature, cold air-standard:  T2 = T1 (p2/p1)^((k-1)/k).
    [Moran Eq. 9.23, Sec. 9.6.2, p.529]"""
    return T1 * rp ** ((k - 1.0) / k)


def temp_after_isentropic_expansion(T3, rp, k=K_AIR):
    """End-of-expansion temperature, cold air-standard:  T4 = T3 (p1/p2)^((k-1)/k).
    [Moran Eq. 9.24, Sec. 9.6.2, p.529]"""
    return T3 * (1.0 / rp) ** ((k - 1.0) / k)


def brayton_efficiency(rp, k=K_AIR):
    """Cold air-standard ideal Brayton thermal efficiency:
    eta = 1 - 1/rp^((k-1)/k),  rp = compressor pressure ratio p2/p1.
    Rises with rp. [Moran Eq. 9.25, Sec. 9.6.2, p.532]"""
    return 1.0 - 1.0 / rp ** ((k - 1.0) / k)


def pressure_ratio_max_work(T1, T3, k=K_AIR):
    """Compressor pressure ratio maximizing the NET WORK per unit of mass flow (cold
    air-standard, fixed compressor-inlet T1 and turbine-inlet T3):
    rp = (T3/T1)^(k/(2(k-1))).  [Moran Ex 9.5 Eq. (a), Sec. 9.6.2, p.534]"""
    return (T3 / T1) ** (k / (2.0 * (k - 1.0)))


# --- irreversibilities (Sec. 9.6.3) ------------------------------------------
def turbine_work_actual(wt_s, eta_t):
    """Actual turbine work from the isentropic value:  Wt/m = eta_t (Wt/m)_s, with
    eta_t = (h3-h4)/(h3-h4s) (Eq. 6.46). [Moran Sec. 9.6.3, p.535-536]"""
    return eta_t * wt_s


def compressor_work_actual(wc_s, eta_c):
    """Actual compressor work from the isentropic value:  Wc/m = (Wc/m)_s / eta_c, with
    eta_c = (h2s-h1)/(h2-h1) (Eq. 6.48). [Moran Sec. 9.6.3, p.535-536]"""
    return wc_s / eta_c


# --- regeneration pointer (Sec. 9.7) -----------------------------------------
def regenerator_effectiveness(hx, h2, h4):
    """Regenerator effectiveness:  eta_reg = (hx - h2)/(h4 - h2)  (actual over maximum
    enthalpy rise of the compressor-side air; -> 1 as hx -> h4).
    [Moran Eq. 9.27, Sec. 9.7, p.539]"""
    return (hx - h2) / (h4 - h2)


def regenerator_exit_enthalpy(h2, h4, eta_reg):
    """Compressor-side regenerator exit enthalpy from the effectiveness (Eq. 9.27
    solved for hx):  hx = h2 + eta_reg (h4 - h2). [Moran Eq. 9.27, Sec. 9.7, p.539-540]"""
    return h2 + eta_reg * (h4 - h2)


def heat_added_regenerative(hx, h3):
    """Heat added with a regenerator:  Qin/m = h3 - hx  (only x -> 3 needs external
    heat; net work is unchanged, so eta rises). [Moran Eq. 9.26, Sec. 9.7, p.538]"""
    return h3 - hx


def _demo():
    print("Module 09.5 -- Air-Standard Brayton Cycle  (gas turbine; large back work ratio)\n")
    print("  Cold air-standard, k=1.4:  eta = 1 - 1/rp^((k-1)/k)")
    for rp in (6.0, 10.0, 20.0):
        print("    rp=%2d -> eta = %.4f" % (int(rp), brayton_efficiency(rp)))
    print("\n  Example 9.4 (ideal; 100 kPa, 300 K, rp=10, T3=1400 K; Table A-22):")
    h1, h2, h3, h4 = 300.19, 579.9, 1515.4, 808.5
    print("    wt = %.1f, wc = %.1f, qin = %.1f kJ/kg" %
          (turbine_work(h3, h4), compressor_work(h1, h2), heat_added(h2, h3)))
    print("    eta = %.3f   [book 0.457];  bwr = %.3f   [book 0.396]"
          % (brayton_efficiency_air_table(h1, h2, h3, h4), back_work_ratio(h1, h2, h3, h4)))
    print("    cold air-standard (same rp): eta = %.3f, T2 = %.1f K, T4 = %.1f K"
          % (brayton_efficiency(10.0),
             temp_after_isentropic_compression(300.0, 10.0),
             temp_after_isentropic_expansion(1400.0, 10.0)),
          "  [book 0.482, 579.2, 725.1]")
    print("\n  Example 9.6 (same cycle, eta_t = eta_c = 80%):")
    wt = turbine_work_actual(706.9, 0.8)
    wc = compressor_work_actual(279.7, 0.8)
    h2a = h1 + wc
    print("    wt = %.1f, wc = %.1f, h2 = %.1f, qin = %.1f kJ/kg" % (wt, wc, h2a, h3 - h2a))
    print("    eta = %.3f   [book 0.249];  bwr = %.3f   [book 0.618] -- irreversibility bites"
          % ((wt - wc) / (h3 - h2a), wc / wt))
    print("\n  Example 9.7 (regenerator, eta_reg = 80%, on the Ex 9.4 cycle):")
    hx = regenerator_exit_enthalpy(h2, h4, 0.8)
    print("    hx = %.1f kJ/kg  [book 762.8];  qin drops to %.1f kJ/kg"
          % (hx, heat_added_regenerative(hx, h3)))
    print("    eta = %.3f   [book 0.568, up from 0.457]"
          % (((h3 - h4) - (h2 - h1)) / heat_added_regenerative(hx, h3)))
    print("\n  Net-work-optimal pressure ratio (Ex 9.5): rp*(300 K, 1700 K) = %.0f  [book ~21]"
          % pressure_ratio_max_work(300.0, 1700.0))


if __name__ == "__main__":
    _demo()
