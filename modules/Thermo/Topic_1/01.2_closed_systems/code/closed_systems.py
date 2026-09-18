"""
closed_systems.py  —  Module 1.2 (Closed Systems / Control Mass)

The closed-system (control-mass) energy balance and the work done in a
quasiequilibrium volume change, following

    Moran, Shapiro, Boettner & Bailey, *Fundamentals of Engineering
    Thermodynamics*, 8th ed., Ch. 1 (§1.2.1) and Ch. 2 ("Energy and the First
    Law of Thermodynamics").  Exact section/equation/page citations in ../refs.md.

A closed system is a fixed quantity of matter: **no mass crosses the boundary**,
only energy (as heat Q and work W).  The first law is then the energy balance

    dKE + dPE + dU  =  Q - W            (Moran Eq. 2.35)

with the sign convention Q > 0 INTO the system, W > 0 done BY the system.  This
is the control-mass special case of the open-system balance in module 1.1
(the flow terms are gone).

Units (SI, Moran):  p [kPa]   V [m^3]   so  pV, Q, W, U [kJ]
                    m [kg]    velocity [m/s]   z [m]   g = 9.81 m/s^2
(kinetic/potential energies come out in J and are divided by 1000 -> kJ.)
"""
import math

G = 9.81  # m/s^2


# ----------------------------------------------------------- energy components
def delta_KE(m, V1, V2):
    """Change in kinetic energy  dKE = 1/2 m (V2^2 - V1^2)  [kJ].  [Moran Eq. 2.5]"""
    return 0.5 * m * (V2 * V2 - V1 * V1) / 1000.0


def delta_PE(m, z1, z2, g=G):
    """Change in potential energy  dPE = m g (z2 - z1)  [kJ].  [Moran Eq. 2.10]"""
    return m * g * (z2 - z1) / 1000.0


# ------------------------------------------------------ closed-system 1st law
def energy_balance_residual(Q, W, dU, dKE=0.0, dPE=0.0):
    """Residual of the closed-system energy balance  [kJ]:

        (Q - W) - (dU + dKE + dPE) .

    Zero when the balance is satisfied.  [Moran Eq. 2.35, "Energy Balance for
    Closed Systems".]
    """
    return (Q - W) - (dU + dKE + dPE)


def heat_transfer(W, dU, dKE=0.0, dPE=0.0):
    """Solve the energy balance for the heat transfer  Q = dU + dKE + dPE + W  [kJ]."""
    return dU + dKE + dPE + W


def work_done(Q, dU, dKE=0.0, dPE=0.0):
    """Solve the energy balance for the work  W = Q - (dU + dKE + dPE)  [kJ]."""
    return Q - (dU + dKE + dPE)


def power_balance_residual(Qdot, Wdot, dEdt):
    """Time-rate form residual  [kW]:  (Qdot - Wdot) - dE/dt .
    [Moran Eq. 2.37, time rate of the energy balance.]"""
    return (Qdot - Wdot) - dEdt


# --------------------------------------- quasiequilibrium pdV (boundary) work
def pdv_work_trapz(p_of_V, V1, V2, n_steps=20000):
    """Boundary work  W = ∫_{V1}^{V2} p dV  [kJ] for a quasiequilibrium process,
    p given as a callable p(V) in kPa, V in m^3.  Composite trapezoid.
    [Moran Eq. 2.17, "Expansion or Compression Work".]
    """
    h = (V2 - V1) / n_steps
    s = 0.5 * (p_of_V(V1) + p_of_V(V2))
    for k in range(1, n_steps):
        s += p_of_V(V1 + k * h)
    return s * h


def polytropic_pressure(p1, V1, V2, n):
    """Pressure after a polytropic process p V^n = const:  p2 = p1 (V1/V2)^n  [kPa]."""
    return p1 * (V1 / V2) ** n


def polytropic_work(p1, V1, V2, n, p2=None):
    """Closed-form boundary work of a polytropic process p V^n = const  [kJ]:

        n != 1:  W = (p2 V2 - p1 V1) / (1 - n)
        n == 1:  W = p1 V1 ln(V2 / V1)        (isothermal, ideal gas)

    p in kPa, V in m^3 -> W in kJ.  If p2 is not given it is found from
    p1 V1^n = p2 V2^n.  [Moran Eqs. 2.17 and the §2.2 polytropic results.]
    """
    if math.isclose(n, 1.0):
        return p1 * V1 * math.log(V2 / V1)
    if p2 is None:
        p2 = polytropic_pressure(p1, V1, V2, n)
    return (p2 * V2 - p1 * V1) / (1.0 - n)


def constant_pressure_work(p, V1, V2):
    """Boundary work at constant pressure  W = p (V2 - V1)  [kJ]  (polytropic n=0)."""
    return p * (V2 - V1)


# ------------------------------------------------------------------- demo ----
def _demo():
    print("Module 1.2 — Closed systems: worked checks\n")

    # piston-cylinder, air compressed polytropically pV^1.3 = const
    p1, V1, V2, n = 100.0, 1.0, 0.5, 1.3          # kPa, m^3
    p2 = polytropic_pressure(p1, V1, V2, n)
    W = polytropic_work(p1, V1, V2, n)
    print(f"(1) Polytropic n=1.3: p2 = {p2:.1f} kPa, W = {W:.2f} kJ (work IN, < 0)")
    print(f"    trapezoid ∫p dV check: {pdv_work_trapz(lambda V: p1*(V1/V)**n, V1, V2):.2f} kJ")

    # if that compression is adiabatic (Q=0) with negligible ke/pe: dU = Q - W = -W
    print(f"(2) If adiabatic (Q=0): dU = Q - W = {-W:.2f} kJ (internal energy rises)")

    # isothermal ideal-gas expansion n=1
    print(f"(3) Isothermal n=1, double the volume: W = p1 V1 ln2 = "
          f"{polytropic_work(100.0, 1.0, 2.0, 1.0):.2f} kJ")

    # kinetic / potential pieces
    print(f"(4) dKE (2 kg, 0->10 m/s) = {delta_KE(2.0, 0.0, 10.0):.3f} kJ;  "
          f"dPE (0->10 m) = {delta_PE(2.0, 0.0, 10.0):.3f} kJ")


if __name__ == "__main__":
    _demo()
