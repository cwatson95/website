"""
equations.py  —  Module 1.EQ (Topic 1: canonical equation registry)

The key equations underlying Topic 1 (Foundations), each as a single documented
function in its canonical Moran 8e form.  This module is the *reference*: the
companion test (`test_equations.py`) imports the sibling concept modules
(1.1 / 1.2 / 1.4 / 1.5) and asserts they reproduce these forms exactly, so the
equations are verified to be both (a) numerically right and (b) used consistently
across Topic 1.

Citations are Moran, Shapiro, Boettner & Bailey 8e (printed pages; PDF = +17);
full table in ../refs.md.  SI units: p [kPa], V [m^3], energies [kJ], m [kg],
velocity [m/s], z [m].
"""
import math

G = 9.81  # standard gravity [m/s^2]


# --- properties -------------------------------------------------------------
def specific_volume(V, m):
    """v = V / m  [m^3/kg].  [Moran §1.5, p.13]"""
    return V / m


def density(m, V):
    """rho = m / V = 1 / v  [kg/m^3].  [Moran Eq. 1.6, §1.5, p.13]"""
    return m / V


def celsius_to_kelvin(T_C):
    """T(K) = T(°C) + 273.15.  [Moran Eq. 1.17, §1.7.3, p.20]"""
    return T_C + 273.15


def kelvin_to_rankine(T_K):
    """T(°R) = 1.8 T(K).  [Moran Eq. 1.16, §1.7.2, p.18]"""
    return 1.8 * T_K


def gauge_to_absolute(p_gauge, p_atm):
    """p(abs) = p(gauge) + p(atm).  [Moran Eq. 1.14, §1.6.3, p.17]"""
    return p_gauge + p_atm


# --- mass & flow (open systems, module 1.1) ---------------------------------
def mass_flow_rate(A, V, v):
    """mdot = A V / v = rho A V  [kg/s].  [Moran Eq. 4.4b, §4.2.1, p.172]"""
    return A * V / v


def mass_rate_residual(sum_in, sum_out):
    """dm_cv/dt = sum(mdot_in) - sum(mdot_out)  [kg/s]; 0 at steady state.
    [Moran Eq. 4.2, §4.1, p.170]"""
    return sum_in - sum_out


def enthalpy(u, p, v):
    """h = u + p v  [kJ/kg]  (internal energy + flow work pv).  Defined in §3.6.1;
    the u + pv combination is shown for flowing matter in §4.4.2.  [Moran §4.4.2, p.179]"""
    return u + p * v


def flow_energy(h, V=0.0, z=0.0):
    """psi = h + V^2/2 + g z  [kJ/kg]  (V^2/2, gz in J/kg -> /1000).
    [Moran Eq. 4.15, §4.4.3, p.180]"""
    return h + (0.5 * V * V + G * z) / 1000.0


# --- closed-system first law (module 1.2) -----------------------------------
def delta_KE(m, V1, V2):
    """dKE = 1/2 m (V2^2 - V1^2)  [kJ].  [Moran Eq. 2.5, §2.1.1, p.41]"""
    return 0.5 * m * (V2 * V2 - V1 * V1) / 1000.0


def delta_PE(m, z1, z2, g=G):
    """dPE = m g (z2 - z1)  [kJ].  [Moran Eq. 2.10, §2.1.2, p.42]"""
    return m * g * (z2 - z1) / 1000.0


def closed_system_heat(W, dU, dKE=0.0, dPE=0.0):
    """Closed-system energy balance solved for Q:
    Q = dU + dKE + dPE + W   (from dKE+dPE+dU = Q - W).
    [Moran Eq. 2.35b, §2.5, p.61]"""
    return dU + dKE + dPE + W


# --- quasiequilibrium boundary work (modules 1.2 / 1.5) ---------------------
def boundary_work(p_of_V, V1, V2, n_steps=20000):
    """W = ∫ p dV  [kJ] along a quasiequilibrium path p(V).  [Moran Eq. 2.17, §2.2.3, p.48]"""
    h = (V2 - V1) / n_steps
    s = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        s += p_of_V(V1 + k * h)
    return s * h


def polytropic_pressure(p1, V1, V2, n):
    """p2 = p1 (V1/V2)^n  for p V^n = const  [kPa].  [Moran §2.2.5, p.50]"""
    return p1 * (V1 / V2) ** n


def polytropic_work(p1, V1, V2, n, p2=None):
    """W = (p2 V2 - p1 V1)/(1-n)  (n != 1),  p1 V1 ln(V2/V1)  (n = 1)  [kJ].
    [Moran Example 2.1, Eqs. (a),(b), p.50-51]"""
    if math.isclose(n, 1.0):
        return p1 * V1 * math.log(V2 / V1)
    if p2 is None:
        p2 = polytropic_pressure(p1, V1, V2, n)
    return (p2 * V2 - p1 * V1) / (1.0 - n)


# index used by the test and by equations.md
REGISTRY = [
    ("1.5", "specific_volume", "v = V/m", "§1.5", "p.13"),
    ("1.6", "density", "rho = m/V = 1/v", "§1.5", "p.13"),
    ("1.16", "kelvin_to_rankine", "T(°R) = 1.8 T(K)", "§1.7.2", "p.18"),
    ("1.17", "celsius_to_kelvin", "T(K) = T(°C) + 273.15", "§1.7.3", "p.20"),
    ("1.14", "gauge_to_absolute", "p(abs) = p(gauge) + p(atm)", "§1.6.3", "p.17"),
    ("2.5", "delta_KE", "dKE = 1/2 m (V2^2 - V1^2)", "§2.1.1", "p.41"),
    ("2.10", "delta_PE", "dPE = m g (z2 - z1)", "§2.1.2", "p.42"),
    ("2.17", "boundary_work", "W = ∫ p dV", "§2.2.3", "p.48"),
    ("2.1(a/b)", "polytropic_work", "W = (p2V2-p1V1)/(1-n); p1V1 ln(V2/V1)", "Ex 2.1", "p.50"),
    ("2.35b", "closed_system_heat", "dKE+dPE+dU = Q - W", "§2.5", "p.61"),
    ("4.2", "mass_rate_residual", "dm_cv/dt = Σmdot_i - Σmdot_e", "§4.1", "p.170"),
    ("4.4b", "mass_flow_rate", "mdot = A V / v", "§4.2.1", "p.172"),
    ("4.15", "flow_energy", "psi = h + V^2/2 + g z", "§4.4.3", "p.180"),
    ("h=u+pv", "enthalpy", "h = u + p v", "§4.4.2", "p.179"),
]


def _demo():
    print("Module 1.EQ — Topic 1 equation registry\n")
    for eq, fn, form, sec, pg in REGISTRY:
        print(f"  Eq {eq:<9} {fn:<22} {form:<34} [Moran {sec}, {pg}]")


if __name__ == "__main__":
    _demo()
