"""
rankine_cycle.py  —  Module 09.6 (Rankine Cycle)

The Rankine cycle is the VAPOR POWER cycle -- the working model of steam power plants
(coal, nuclear, solar-thermal, geothermal; Moran 8e Table 8.2).  Water circulates
through four steady-flow components (Sec. 8.2, Fig. 8.2), state numbering per Moran:

  1-2  turbine:    vapor expands to condenser pressure       Wt/m  = h1 - h2   (8.1)
  2-3  condenser:  heat rejected to cooling water            Qout/m = h2 - h3  (8.2)
  3-4  pump:       liquid pushed back to boiler pressure     Wp/m  = h4 - h3   (8.3)
  4-1  boiler:     heat added, feedwater -> vapor            Qin/m = h1 - h4   (8.4)

  eta = [(h1-h2) - (h4-h3)]/(h1-h4)      (Eq. 8.5a)     thermal efficiency
  bwr = (h4-h3)/(h1-h2)                  (Eq. 8.6)      back work ratio, ~1-2% (!)

In the IDEAL Rankine cycle (Sec. 8.2.2) the turbine and pump are isentropic and the
heat exchangers have no pressure drop; state 1 is saturated (or superheated) vapor and
state 3 saturated liquid.  Because the pump handles LIQUID, its work is tiny and well
approximated by (Eq. 8.7b)

  (Wp/m)_s ~ v3 (p4 - p3)

-- compare the 40-80% back work ratio of the gas-turbine Brayton cycle (module 09.5).
Efficiency rises with boiler pressure and falls with condenser pressure (Sec. 8.2.3,
eta_ideal = 1 - Tout/Tin_bar, Eq. 8.8).  Real plants add SUPERHEAT and REHEAT (Sec. 8.3)
to raise the mean temperature of heat addition while keeping turbine-exit quality
x >~ 0.9.  Irreversibilities enter through eta_t (Eq. 8.9) and eta_p (Eq. 8.10).

Steam states come from the water tables (Tables A-2/A-3/A-4; project CSVs in
modules/Thermo/steam_tables/).  Citations: Moran 8e (PDF = printed + 18); ../refs.md.
"""


# --- component energy balances (Sec. 8.2.1) ----------------------------------
def turbine_work(h1, h2):
    """Turbine work per unit of mass flowing:  Wt/m = h1 - h2.
    [Moran Eq. 8.1, Sec. 8.2.1, p.446]"""
    return h1 - h2


def condenser_heat(h2, h3):
    """Heat rejected to cooling water per unit of mass:  Qout/m = h2 - h3.
    [Moran Eq. 8.2, Sec. 8.2.1, p.447]"""
    return h2 - h3


def pump_work(h3, h4):
    """Pump work INPUT per unit of mass:  Wp/m = h4 - h3 (positive).
    [Moran Eq. 8.3, Sec. 8.2.1, p.447]"""
    return h4 - h3


def boiler_heat(h4, h1):
    """Heat added in the boiler per unit of mass:  Qin/m = h1 - h4.
    [Moran Eq. 8.4, Sec. 8.2.1, p.447]"""
    return h1 - h4


def rankine_efficiency(h1, h2, h3, h4):
    """Rankine thermal efficiency:  eta = [(h1-h2) - (h4-h3)]/(h1-h4).
    [Moran Eq. 8.5a, Sec. 8.2.1, p.447]"""
    return ((h1 - h2) - (h4 - h3)) / (h1 - h4)


def rankine_efficiency_from_heat(q_in, q_out):
    """Rankine efficiency from the heat transfers:  eta = 1 - (Qout/m)/(Qin/m).
    [Moran Eq. 8.5b, Sec. 8.2.1, p.447]"""
    return 1.0 - q_out / q_in


def back_work_ratio(h1, h2, h3, h4):
    """Back work ratio:  bwr = (Wp/m)/(Wt/m) = (h4-h3)/(h1-h2).  Characteristically
    ~1-2% for vapor plants (liquid pump). [Moran Eq. 8.6, Sec. 8.2.1, p.447]"""
    return (h4 - h3) / (h1 - h2)


# --- ideal cycle helpers (Sec. 8.2.2) ----------------------------------------
def pump_work_approx(v3, p3, p4):
    """Isentropic pump work, incompressible-liquid approximation:
    (Wp/m)_s ~ v3 (p4 - p3),  v3 = specific volume at pump inlet.  With v3 in m^3/kg
    and p in kPa the result is kJ/kg. [Moran Eq. 8.7b, Sec. 8.2.2, p.449]"""
    return v3 * (p4 - p3)


def quality_from_entropy(s, sf, sg):
    """Two-phase quality from entropy at the exit pressure:  x = (s - sf)/(sg - sf)
    (isentropic turbine: s = s1). [Moran Ex 8.1, p.451; s = sf + x sfg]"""
    return (s - sf) / (sg - sf)


def enthalpy_two_phase(x, hf, hfg):
    """Two-phase enthalpy from quality:  h = hf + x hfg.
    [Moran Ex 8.1, p.451; Table A-3 f/fg/g columns]"""
    return hf + x * hfg


def ideal_efficiency_avg_temps(T_in_bar, T_out):
    """Ideal-cycle efficiency from average heat-transfer temperatures (absolute):
    eta_ideal = 1 - T_out/T_in_bar.  Boiler pressure UP or condenser pressure DOWN
    raises eta. [Moran Eq. 8.8, Sec. 8.2.3, p.453]"""
    return 1.0 - T_out / T_in_bar


# --- irreversibilities (Sec. 8.2.4) ------------------------------------------
def turbine_exit_actual(h1, h2s, eta_t):
    """Actual turbine-exit enthalpy from the isentropic exit state:
    h2 = h1 - eta_t (h1 - h2s),  eta_t = (h1-h2)/(h1-h2s).
    [Moran Eq. 8.9, Sec. 8.2.4, p.455]"""
    return h1 - eta_t * (h1 - h2s)


def pump_work_actual(wp_s, eta_p):
    """Actual pump work from the isentropic value:  Wp/m = (Wp/m)_s / eta_p, with
    eta_p = (Wp/m)_s/(Wp/m) = v3(p4-p3)/(h4-h3). [Moran Eq. 8.10b, Sec. 8.2.4, p.456]"""
    return wp_s / eta_p


# --- superheat & reheat (Sec. 8.3) -------------------------------------------
def reheat_efficiency(h1, h2, h3, h4, h5, h6):
    """Ideal reheat-cycle thermal efficiency (two turbine stages, states per Fig. 8.7:
    1-2 HP turbine, 2-3 reheat, 3-4 LP turbine, 4-5 condenser, 5-6 pump, 6-1 boiler):
    eta = [(h1-h2) + (h3-h4) - (h6-h5)] / [(h1-h6) + (h3-h2)].
    [Moran Sec. 8.3 / Ex 8.3, p.459-462]"""
    return ((h1 - h2) + (h3 - h4) - (h6 - h5)) / ((h1 - h6) + (h3 - h2))


def _demo():
    print("Module 09.6 -- Rankine Cycle  (vapor power; tiny back work ratio)\n")
    print("  Example 8.1 (ideal; sat vapor 8.0 MPa -> condenser 0.008 MPa, 100 MW):")
    h1, s1 = 2758.0, 5.7432                     # Table A-3, sat vapor 8.0 MPa
    x2 = quality_from_entropy(s1, 0.5926, 8.2287)
    h2 = enthalpy_two_phase(x2, 173.88, 2403.1)
    h3 = 173.88                                 # sat liquid 0.008 MPa
    wp = pump_work_approx(1.0084e-3, 8.0, 8000.0)
    h4 = h3 + wp
    print("    x2 = %.4f  [book 0.6745];  h2 = %.1f  [book 1794.8 kJ/kg]" % (x2, h2))
    print("    wp = v3*dp = %.2f kJ/kg  [book 8.06];  h4 = %.2f  [book 181.94]" % (wp, h4))
    print("    eta = %.3f  [book 0.371];  bwr = %.5f  [book 8.37e-3]"
          % (rankine_efficiency(h1, h2, h3, h4), back_work_ratio(h1, h2, h3, h4)))
    print("    mdot = %.3g kg/h  [book 3.77e5]"
          % (100e3 * 3600.0 / ((h1 - h2) - (h4 - h3))))
    print("\n  Example 8.2 (same cycle, eta_t = eta_p = 85%):")
    h2a = turbine_exit_actual(h1, h2, 0.85)
    wpa = pump_work_actual(wp, 0.85)
    print("    h2 = %.1f  [book 1939.3];  wp = %.2f  [book 9.48];  h4 = %.2f  [book 183.36]"
          % (h2a, wpa, h3 + wpa))
    print("    eta = %.3f  [book 0.314] -- turbine irreversibility dominates"
          % rankine_efficiency(h1, h2a, h3, h3 + wpa))
    print("\n  Example 8.3 (superheat + reheat: 8.0 MPa/480 C -> 0.7 MPa, reheat 440 C):")
    x2r = quality_from_entropy(6.6586, 1.9922, 6.708)
    h2r = enthalpy_two_phase(x2r, 697.22, 2066.3)
    x4r = quality_from_entropy(7.7571, 0.5926, 8.2287)
    h4r = enthalpy_two_phase(x4r, 173.88, 2403.1)
    print("    HP exit x = %.4f, h = %.1f  [book 0.9895, 2741.8]" % (x2r, h2r))
    print("    LP exit x = %.4f (>0.9), h = %.1f  [book 0.9382, 2428.5]" % (x4r, h4r))
    print("    eta = %.3f  [book 0.403, up from 0.371]"
          % reheat_efficiency(3348.4, h2r, 3353.3, h4r, 173.88, 181.94))
    print("\n  Pressure effects (Eq. 8.8): eta_ideal = 1 - Tout/Tin_bar -- boiler p UP,")
    print("    condenser p DOWN both raise eta; condenser runs below atmospheric.")


if __name__ == "__main__":
    _demo()
