"""
equations.py  —  Module 2.EQ (Topic 2: canonical work/energy equation registry)

The key equations of Topic 2 (Energy & Work) in canonical Moran 8e form, each one
function.  `test_equations.py` imports the Topic-2 concept modules (2.1/2.2/2.3/
2.4/2.5/2.6) and asserts they reproduce these forms exactly — verifying the
topic's equations are right and used consistently.

Citations: Moran 8e (printed pages; PDF = +17); full table in ../refs.md.
Units: general/elastic/electrical/shaft work and KE/PE in **J**; moving-boundary
work in **kJ** (p [kPa], V [m³]); power in **W**.
"""
import math

G = 9.81


# --- work (§2.2) ------------------------------------------------------------
def general_work(F_of_s, s1, s2, n_steps=20000):
    """W = ∫ F·ds  [J].  [Moran Eq. 2.12, §2.2, p.44]"""
    h = (s2 - s1) / n_steps
    tot = 0.5 * (F_of_s(s1) + F_of_s(s2))
    for k in range(1, n_steps):
        tot += F_of_s(s1 + k * h)
    return tot * h


def boundary_work(p_of_V, V1, V2, n_steps=20000):
    """W = ∫ p dV  [kJ]  (p kPa, V m³).  [Moran Eq. 2.17, §2.2.3, p.48]"""
    h = (V2 - V1) / n_steps
    tot = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        tot += p_of_V(V1 + k * h)
    return tot * h


def shaft_work(torque, omega, dt):
    """W = τ ω dt  [J]  (constant τ, ω).  [Moran Eq. 2.20, §2.2.6, p.53]"""
    return torque * omega * dt


def electric_work(voltage, current, dt):
    """|W| = V I dt  [J]  (−VI into the system).  [Moran Eq. 2.21, §2.2.6, p.53]"""
    return voltage * current * dt


def spring_work(k, x1, x2):
    """Work on a linear spring  W = ½ k (x₂² − x₁²)  [J].  [Moran §2.2.6, p.52]"""
    return 0.5 * k * (x2 * x2 - x1 * x1)


# --- power (§2.2.2) ---------------------------------------------------------
def power_force_velocity(F, V):
    """Ẇ = F·V  [W].  [Moran Eq. 2.13, §2.2.2, p.46]"""
    return F * V


def shaft_power(torque, omega):
    """Ẇ = τ ω  [W].  [Moran Eq. 2.20, §2.2.6, p.53]"""
    return torque * omega


def electric_power(voltage, current):
    """Ẇ = V I  [W]  (−VI into the system).  [Moran Eq. 2.21, §2.2.6, p.53]"""
    return voltage * current


# --- mechanical energy (§2.1) and total energy (§2.3) -----------------------
def kinetic_energy(m, V):
    """KE = ½ m V²  [J].  [Moran §2.1.1, p.41]"""
    return 0.5 * m * V * V


def delta_KE(m, V1, V2):
    """ΔKE = ½ m (V₂² − V₁²)  [J].  [Moran Eq. 2.5, §2.1.1, p.41]"""
    return 0.5 * m * (V2 * V2 - V1 * V1)


def potential_energy(m, z, g=G):
    """PE = m g z  [J].  [Moran §2.1.2, p.42]"""
    return m * g * z


def delta_PE(m, z1, z2, g=G):
    """ΔPE = m g (z₂ − z₁)  [J].  [Moran Eq. 2.10, §2.1.2, p.42]"""
    return m * g * (z2 - z1)


def total_energy(U, KE, PE):
    """Total energy of a system  E = U + KE + PE.  [Moran Eq. 2.27, §2.3, p.55]"""
    return U + KE + PE


REGISTRY = [
    ("2.12", "general_work", "W = ∫F·ds", "§2.2", "p.44"),
    ("2.17", "boundary_work", "W = ∫p dV", "§2.2.3", "p.48"),
    ("2.20", "shaft_work / shaft_power", "Ẇ = τω", "§2.2.6", "p.53"),
    ("2.21", "electric_work / electric_power", "Ẇ = −εi", "§2.2.6", "p.53"),
    ("(2.18)", "spring_work", "W = ½k(x₂²−x₁²)", "§2.2.6", "p.52"),
    ("2.13", "power_force_velocity", "Ẇ = F·V", "§2.2.2", "p.46"),
    ("2.5", "delta_KE / kinetic_energy", "ΔKE = ½m(V₂²−V₁²)", "§2.1.1", "p.41"),
    ("2.10", "delta_PE / potential_energy", "ΔPE = mg(z₂−z₁)", "§2.1.2", "p.42"),
    ("2.27", "total_energy", "E = U + KE + PE", "§2.3", "p.55"),
]


def _demo():
    print("Module 2.EQ — Topic 2 (Energy & Work) equation registry\n")
    for eq, fn, form, sec, pg in REGISTRY:
        print(f"  Eq {eq:<7} {fn:<32} {form:<24} [Moran {sec}, {pg}]")


if __name__ == "__main__":
    _demo()
