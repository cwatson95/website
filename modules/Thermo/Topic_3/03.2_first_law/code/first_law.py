"""
first_law.py  —  Module 3.2 (First Law / Energy Balance)

The first law of thermodynamics: **energy is conserved** — neither created nor
destroyed, only transferred (by heat Q and work W) or stored (as internal,
kinetic, and potential energy).  For a closed system over a process 1->2 this is
the energy balance  E2 - E1 = Q - W  (Moran 8e Eq. 2.35a, Sec. 2.5).

Sign conventions (Moran):
  Q > 0  heat transfer INTO the system    (Sec. 2.4.1, p.56)
  W > 0  work done BY the system          (Sec. 2.2.1; module 2.1)

So  dE = Q - W  with  dE = dU + dKE + dPE.  Internal energy is a PROPERTY (dU
depends only on end states); Q and W are path functions (modules 1.5, 2.1).

Units: any consistent energy unit (kJ here); rates in kW.
Citations: Moran 8e (printed pages; PDF = printed + 18); full table in ../refs.md.
"""


def delta_E(Q, W):
    """Closed-system first law:  E2 - E1 = Q - W. [Moran Eq. 2.35a, Sec. 2.5, p.61]"""
    return Q - W


def closed_system_dU(Q, W, dKE=0.0, dPE=0.0):
    """Solve the balance dKE + dPE + dU = Q - W for the internal-energy change:
    dU = Q - W - dKE - dPE. [Moran Eq. 2.35b, Sec. 2.5, p.61]"""
    return Q - W - dKE - dPE


def heat_transfer(dU, W, dKE=0.0, dPE=0.0):
    """Heat from the balance:  Q = dU + dKE + dPE + W. [Moran Eq. 2.35b, p.61]"""
    return dU + dKE + dPE + W


def work_transfer(dU, Q, dKE=0.0, dPE=0.0):
    """Work from the balance:  W = Q - (dU + dKE + dPE). [Moran Eq. 2.35b, p.61]"""
    return Q - (dU + dKE + dPE)


def rate_energy_balance(Qdot, Wdot):
    """Rate form:  dE/dt = Qdot - Wdot. [Moran Eq. 2.37, Sec. 2.5.1, p.62]
    At steady state dE/dt = 0, hence Qdot = Wdot (Topic 6 / Topic 8)."""
    return Qdot - Wdot


def cycle_net_work(Q_cycle):
    """Any cycle returns to its state (dE_cycle = 0), so W_cycle = Q_cycle.
    [Moran Eq. 2.40, Sec. 2.6, p.73]"""
    return Q_cycle


def power_cycle_work(Q_in, Q_out):
    """Power cycle net work:  W_cycle = Q_in - Q_out. [Moran Eq. 2.41, Sec. 2.6, p.73]
    (The efficiency W_cycle/Q_in lives in Topic 7; bounds in module 3.3.)"""
    return Q_in - Q_out


def first_law_holds(Q, W, dE, tol=1e-9):
    """Check the closed-system balance Q - W == dE. [Moran Eq. 2.35a]"""
    return abs((Q - W) - dE) <= tol


def _demo():
    print("Module 3.2 -- First Law / Energy Balance  (Q in +, W out +)\n")
    # Moran Example 2.2: cooling a gas, dU = -22 kJ, boundary work W = +17.6 kJ
    Q = heat_transfer(dU=-22.0, W=17.6)
    print("  Ex 2.2 cooling a gas:  dU=-22 kJ, W=+17.6 kJ")
    print("    Q = dU + W = %.1f kJ        [book -4.4 kJ, heat OUT]" % Q)
    # steady-state gearbox (Ex 2.4): dE/dt = 0 -> Qdot = Wdot = -1.2 kW
    print("\n  Steady state (Ex 2.4 gearbox): dE/dt =", rate_energy_balance(-1.2, -1.2), "kW")
    # a power cycle
    print("\n  Power cycle:  Q_in=1000, Q_out=600 kJ")
    print("    W_cycle = Q_in - Q_out = %.0f kJ" % power_cycle_work(1000.0, 600.0))
    print("    check W_cycle == Q_cycle:",
          first_law_holds(Q=cycle_net_work(400.0), W=power_cycle_work(1000.0, 600.0), dE=0.0))


if __name__ == "__main__":
    _demo()
