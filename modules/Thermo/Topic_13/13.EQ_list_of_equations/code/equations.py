"""
equations.py  —  Module 13.EQ (Topic 13: canonical equation registry, Compressible Flow)

The key equations of Topic 13 in canonical form, one per function:
  * compressible-flow trunk (Moran 8e Ch.9, Secs. 9.12-9.14):
        speed of sound, Mach number, stagnation enthalpy & ratios,
        area-velocity, isentropic area-Mach & critical ratios, normal-shock functions
  * cross-trunk leaves (~CM, NOT Moran): pipe-flow Reynolds number and friction factors
        (laminar f=64/Re from 13.4; turbulent Blasius/Colebrook from 13.5)

`test_equations.py` checks each value AND imports the concept modules 13.1-13.5,
asserting they reproduce these forms (so any formula drift fails the test).

Citations: Moran 8e (printed pages; PDF = printed + 18) for the Ch.9 set; cross-trunk
fluid mechanics for the pipe-flow leaves.  Full table in ../refs.md.
"""
import math


# --- compressible flow: sound, Mach, stagnation (Moran Sec. 9.12) -----------
def speed_of_sound_ideal_gas(k, R, T):
    """c = sqrt(k R T) [m/s], R in J/kg.K. [Moran Eq. 9.37, Sec. 9.12.2, p.570]"""
    return math.sqrt(k * R * T)


def mach_number(V, c):
    """M = V / c. [Moran Eq. 9.38, Sec. 9.12.2, p.570]"""
    return V / c


def stagnation_enthalpy(h, V):
    """ho = h + V^2/2. [Moran Eq. 9.39, Sec. 9.12.3, p.571]"""
    return h + V * V / 2.0


# --- isentropic flow functions (Moran Sec. 9.14.1) --------------------------
def stagnation_temperature_ratio(M, k):
    """To/T = 1 + (k-1)/2 M^2. [Moran Eq. 9.50, Sec. 9.14.1, p.578]"""
    return 1.0 + (k - 1.0) / 2.0 * M * M


def stagnation_pressure_ratio(M, k):
    """po/p = (1 + (k-1)/2 M^2)^(k/(k-1)). [Moran Eq. 9.51, Sec. 9.14.1, p.578]"""
    return stagnation_temperature_ratio(M, k) ** (k / (k - 1.0))


def area_mach_ratio(M, k):
    """A/A* = (1/M)[ (2/(k+1))(1 + (k-1)/2 M^2) ]^((k+1)/(2(k-1))).
    [Moran Eq. 9.52, Sec. 9.14.1, p.578]"""
    t = (2.0 / (k + 1.0)) * stagnation_temperature_ratio(M, k)
    return (1.0 / M) * t ** ((k + 1.0) / (2.0 * (k - 1.0)))


def critical_pressure_ratio(k):
    """p*/po = (2/(k+1))^(k/(k-1)) (= Eq. 9.51 at M=1; 0.528 for k=1.4).
    [Moran Eq. 9.51 @M=1, Sec. 9.13.2/9.14.1, p.574/578]"""
    return (2.0 / (k + 1.0)) ** (k / (k - 1.0))


def critical_temperature_ratio(k):
    """T*/To = 2/(k+1) (= Eq. 9.50 at M=1). [Moran Eq. 9.50 @M=1, Sec. 9.14.1, p.578]"""
    return 2.0 / (k + 1.0)


# --- area-velocity relation (Moran Sec. 9.13.1) -----------------------------
def area_change_ratio(dV_over_V, M):
    """dA/A = -(dV/V)(1 - M^2). [Moran Eq. 9.45, Sec. 9.13.1, p.573]"""
    return -dV_over_V * (1.0 - M * M)


# --- normal-shock functions (Moran Sec. 9.14.2) -----------------------------
def mach_after_shock(Mx, k):
    """My = sqrt( (Mx^2 + 2/(k-1)) / ((2k/(k-1)) Mx^2 - 1) ).
    [Moran Eq. 9.55, Sec. 9.14.2, p.581]"""
    num = Mx * Mx + 2.0 / (k - 1.0)
    den = (2.0 * k / (k - 1.0)) * Mx * Mx - 1.0
    return math.sqrt(num / den)


def shock_pressure_ratio(Mx, k):
    """py/px = (1 + k Mx^2)/(1 + k My^2). [Moran Eq. 9.54, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    return (1.0 + k * Mx * Mx) / (1.0 + k * My * My)


def shock_temperature_ratio(Mx, k):
    """Ty/Tx = (1+(k-1)/2 Mx^2)/(1+(k-1)/2 My^2). [Moran Eq. 9.53, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    return stagnation_temperature_ratio(Mx, k) / stagnation_temperature_ratio(My, k)


def stagnation_pressure_ratio_across_shock(Mx, k):
    """poy/pox = (Mx/My)[ (1+(k-1)/2 My^2)/(1+(k-1)/2 Mx^2) ]^((k+1)/(2(k-1))).
    [Moran Eq. 9.56, Sec. 9.14.2, p.581]"""
    My = mach_after_shock(Mx, k)
    E = (k + 1.0) / (2.0 * (k - 1.0))
    base = stagnation_temperature_ratio(My, k) / stagnation_temperature_ratio(Mx, k)
    return (Mx / My) * base ** E


# --- cross-trunk leaves: pipe-flow Re & friction (~CM, NOT Moran) -----------
def reynolds_number(rho, V, D, mu):
    """Re = rho V D / mu (inertial/viscous). [~CM, not Moran; 13.4/13.5; White Sec. 6.3]"""
    return rho * V * D / mu


def friction_factor_laminar(Re):
    """Laminar Darcy friction factor f = 64/Re. [~CM, not Moran; 13.4; White Eq. 6.12]"""
    return 64.0 / Re


def friction_factor_blasius(Re):
    """Turbulent smooth-pipe Blasius f = 0.316/Re^0.25. [~CM, not Moran; 13.5; White Eq. 6.38]"""
    return 0.316 * Re ** -0.25


REGISTRY = [
    ("9.37", "speed_of_sound_ideal_gas",  "c = sqrt(k R T)",                   "M",  "Sec. 9.12.2, p.570"),
    ("9.38", "mach_number",               "M = V/c",                           "M",  "Sec. 9.12.2, p.570"),
    ("9.39", "stagnation_enthalpy",       "ho = h + V^2/2",                    "M",  "Sec. 9.12.3, p.571"),
    ("9.45", "area_change_ratio",         "dA/A = -(dV/V)(1-M^2)",             "M",  "Sec. 9.13.1, p.573"),
    ("9.50", "stagnation_temperature_ratio", "To/T = 1+(k-1)/2 M^2",          "M",  "Sec. 9.14.1, p.578"),
    ("9.51", "stagnation_pressure_ratio", "po/p = (To/T)^(k/(k-1))",           "M",  "Sec. 9.14.1, p.578"),
    ("9.52", "area_mach_ratio",           "A/A* = (1/M)[..]^((k+1)/2(k-1))",   "M",  "Sec. 9.14.1, p.578"),
    ("9.51*","critical_pressure_ratio",   "p*/po = (2/(k+1))^(k/(k-1))",       "M",  "Sec. 9.13.2, p.574"),
    ("9.50*","critical_temperature_ratio","T*/To = 2/(k+1)",                   "M",  "Sec. 9.14.1, p.578"),
    ("9.55", "mach_after_shock",          "My^2 = (Mx^2+2/(k-1))/(..)",        "M",  "Sec. 9.14.2, p.581"),
    ("9.54", "shock_pressure_ratio",      "py/px = (1+kMx^2)/(1+kMy^2)",       "M",  "Sec. 9.14.2, p.581"),
    ("9.53", "shock_temperature_ratio",   "Ty/Tx = (To/T)x/(To/T)y",           "M",  "Sec. 9.14.2, p.581"),
    ("9.56", "stagnation_pressure_ratio_across_shock", "poy/pox = (Mx/My)[..]","M",  "Sec. 9.14.2, p.581"),
    ("~CM",  "reynolds_number",           "Re = rho V D / mu",                 "CM", "13.4/13.5 (White 6.3)"),
    ("~CM",  "friction_factor_laminar",   "f = 64/Re",                         "CM", "13.4 (White 6.12)"),
    ("~CM",  "friction_factor_blasius",   "f = 0.316/Re^0.25",                 "CM", "13.5 (White 6.38)"),
]


def _demo():
    print("Module 13.EQ -- Topic 13 (Compressible Flow & Gas Dynamics) equation registry\n")
    for eq, fn, form, trunk, src in REGISTRY:
        tag = "Moran" if trunk == "M" else "~CM  "
        print(f"  [{trunk:2}] Eq {eq:<6} {fn:<34} {form:<34} [{tag} {src}]")


if __name__ == "__main__":
    _demo()
