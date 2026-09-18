"""
mass_conservation.py  —  Module 6.5 (Conservation of Mass for a Control Volume)

The conservation-of-mass principle for a control volume (CV) is the MASS RATE BALANCE
(Moran 8e Sec. 4.1):

    dm_cv/dt = sum(mdot_i) - sum(mdot_e)              (Eq. 4.2)

the time rate of change of mass inside the CV equals the total rate in at the inlets
minus the total rate out at the exits.  For ONE inlet and ONE exit it is Eq. 4.1.

The instantaneous mass flow rate of a one-dimensional stream is

    mdot = rho * A * V = A * V / v                    (Eqs. 4.4a, 4.4b)

(A = flow area, V = velocity normal to A, v = specific volume, rho = density).  The
product A*V is the volumetric flow rate.

At STEADY STATE there is no accumulation, dm_cv/dt = 0, so the mass rate balance
reduces to

    sum(mdot_i) = sum(mdot_e)                         (Eq. 4.6)

total mass in = total mass out.  (Steady state and one-dimensional flow are
independent idealizations; one does not imply the other.)

Units: mdot [kg/s], A [m^2], V [m/s], v [m^3/kg], rho [kg/m^3].
Citations: Moran 8e (PDF = printed + 18).  Worked Examples 4.1 (feedwater heater,
steady) and 4.2 (barrel filling, transient) in ../problems and module 6.EP.
"""


def mass_flow_rate(A, V, v):
    """One-dimensional mass flow rate  mdot = A V / v  [kg/s].
    [Moran Eq. 4.4b, Sec. 4.2.1, p.172]"""
    return A * V / v


def mass_flow_rate_rho(rho, A, V):
    """One-dimensional mass flow rate  mdot = rho A V  [kg/s].
    [Moran Eq. 4.4a, Sec. 4.2.1, p.172]"""
    return rho * A * V


def mdot_from_volumetric(AV, v):
    """Mass flow rate from a volumetric flow rate AV and specific volume v:
    mdot = (A V) / v.  [Moran Eq. 4.4b, Sec. 4.2.1, p.172]"""
    return AV / v


def velocity_from_mdot(mdot, v, A):
    """Velocity of a one-dimensional stream  V = mdot v / A  (from Eq. 4.4b).
    [Moran Eq. 4.4b, Sec. 4.2.1, p.172]"""
    return mdot * v / A


def dmcv_dt(mdot_in, mdot_out):
    """Mass rate balance  dm_cv/dt = sum(mdot_i) - sum(mdot_e).
    mdot_in, mdot_out are lists (or single floats) of inlet / exit flow rates.
    [Moran Eq. 4.2, Sec. 4.1.1, p.170]"""
    si = sum(mdot_in) if hasattr(mdot_in, "__iter__") else mdot_in
    se = sum(mdot_out) if hasattr(mdot_out, "__iter__") else mdot_out
    return si - se


def steady_mass_residual(mdot_in, mdot_out):
    """At steady state dm_cv/dt = 0, so sum(mdot_i) - sum(mdot_e) should be 0.
    Returns the residual (= dmcv_dt).  [Moran Eq. 4.6, Sec. 4.2.2, p.173]"""
    return dmcv_dt(mdot_in, mdot_out)


def is_steady_mass(mdot_in, mdot_out, tol=1e-9):
    """Steady-state mass test: True iff sum(mdot_i) == sum(mdot_e).
    [Moran Eq. 4.6, Sec. 4.2.2, p.173]"""
    return abs(steady_mass_residual(mdot_in, mdot_out)) <= tol


def _demo():
    print("Module 6.5 -- Conservation of Mass  (mass rate balance, Eq. 4.2)\n")
    # Example 4.1: feedwater heater, steady, 2 inlets + 1 exit (p.174-175)
    mdot1 = 40.0
    mdot3 = mdot_from_volumetric(0.06, 1.108e-3)        # (AV)3 / v3
    mdot2 = mdot3 - mdot1                                # steady: mdot1+mdot2 = mdot3
    V2 = velocity_from_mdot(mdot2, 1.0078e-3, 25e-4)     # v2 ~ vf(40C), A2 = 25 cm^2
    print("  Ex 4.1 feedwater heater (steady): mdot3 = %.2f kg/s, mdot2 = %.2f kg/s, V2 = %.1f m/s"
          % (mdot3, mdot2, V2))
    print("         [book 54.15, 14.15, 5.7]  -- sum(in)=sum(out)? %s" %
          is_steady_mass([mdot1, mdot2], [mdot3]))
    # Example 4.2: barrel filling, transient -> steady height where mdot_e = mdot_i (p.175-176)
    mdot_i, k = 30.0, 9.0                                # mdot_e = 9 L (lb/s), L in ft
    L_ss = mdot_i / k                                    # dL/dt = 0  ->  9 L = 30
    print("  Ex 4.2 barrel (transient -> steady): L_steady = mdot_i/9 = %.2f ft  [book 3.33]" % L_ss)


if __name__ == "__main__":
    _demo()
