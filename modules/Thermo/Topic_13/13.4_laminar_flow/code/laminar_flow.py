"""
laminar_flow.py  —  Module 13.4 (Laminar Pipe Flow)

CROSS-TRUNK (~CM): this is standard fluid-mechanics material and is NOT in Moran 8e
(Fundamentals of Engineering Thermodynamics).  References: F. White, *Fluid Mechanics*
7e Ch.6; Munson/Young/Okiishi, *Fundamentals of Fluid Mechanics*; Cengel & Cimbala,
*Fluid Mechanics* Ch.8.  Use for orderly, layered ("laminar") viscous flow in a round
pipe.

The governing dimensionless group is the REYNOLDS NUMBER, the ratio of inertial to
viscous forces:

    Re = rho V D / mu = V D / nu          (nu = mu/rho, kinematic viscosity)

For flow in a round pipe the flow is LAMINAR when Re is below roughly 2300.  In that
regime the fully developed velocity profile is the parabolic Hagen-Poiseuille profile

    u(r) = u_max (1 - (r/R)^2),   with mean velocity  V = u_max / 2,

and the Darcy friction factor has the exact closed form

    f = 64 / Re,

so the Darcy-Weisbach pressure drop  dP = f (L/D)(rho V^2 / 2)  reduces to the
Hagen-Poiseuille law  dP = 32 mu L V / D^2.

Units (SI): rho [kg/m^3], V [m/s], D,R,r,L [m], mu [Pa.s], nu [m^2/s], dP [Pa].
NOT a Moran citation -- cross-trunk fluid mechanics.
"""
import math


def reynolds_number(rho, V, D, mu):
    """Reynolds number  Re = rho V D / mu  (inertial / viscous).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.3]"""
    return rho * V * D / mu


def reynolds_number_kinematic(V, D, nu):
    """Reynolds number from kinematic viscosity  Re = V D / nu, nu = mu/rho.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.3]"""
    return V * D / nu


def is_laminar(Re, Re_crit=2300.0):
    """Pipe-flow laminar criterion  Re < ~2300 (transition begins near 2300).
    [~CM, not from Moran 8e; Cengel & Cimbala Fluid Mechanics, Ch.8]"""
    return Re < Re_crit


def friction_factor_laminar(Re):
    """Laminar Darcy friction factor (round pipe, exact)  f = 64 / Re.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.12]"""
    return 64.0 / Re


def velocity_profile_parabolic(u_max, r, R):
    """Fully developed laminar (Hagen-Poiseuille) profile  u(r) = u_max (1 - (r/R)^2).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.4]"""
    return u_max * (1.0 - (r / R) ** 2)


def mean_velocity_from_max(u_max):
    """Mean velocity of the parabolic profile  V = u_max / 2.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.4]"""
    return u_max / 2.0


def pressure_drop_darcy(f, L, D, rho, V):
    """Darcy-Weisbach pressure drop  dP = f (L/D)(rho V^2 / 2).
    [~CM, not from Moran 8e; Munson Fundamentals of Fluid Mechanics, Sec. 8.4]"""
    return f * (L / D) * (rho * V * V / 2.0)


def pressure_drop_hagen_poiseuille(mu, L, V, D):
    """Hagen-Poiseuille laminar pressure drop  dP = 32 mu L V / D^2
    (identical to Darcy with f = 64/Re).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.12]"""
    return 32.0 * mu * L * V / (D * D)


def volumetric_flow_hagen_poiseuille(dP, R, mu, L):
    """Hagen-Poiseuille volumetric flow  Q = pi R^4 dP / (8 mu L).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.12]"""
    return math.pi * R ** 4 * dP / (8.0 * mu * L)


def _demo():
    print("Module 13.4 -- Laminar pipe flow  [~CM, NOT from Moran 8e]\n")
    rho, V, D, mu, L = 900.0, 2.0, 0.05, 0.4, 10.0     # oil: rho=900, mu=0.4 Pa.s
    Re = reynolds_number(rho, V, D, mu)
    print("  Oil pipe: rho=900, V=2, D=0.05, mu=0.4 -> Re = %.0f  (laminar? %s)"
          % (Re, is_laminar(Re)))
    f = friction_factor_laminar(Re)
    print("  f = 64/Re = %.4f" % f)
    dP1 = pressure_drop_darcy(f, L, D, rho, V)
    dP2 = pressure_drop_hagen_poiseuille(mu, L, V, D)
    print("  dP (Darcy, f=64/Re) = %.0f Pa  ==  dP (Hagen-Poiseuille) = %.0f Pa" % (dP1, dP2))
    print("  parabolic profile: u(0)=u_max, u(R)=0, mean V = u_max/2 = %.1f (u_max=%.1f)"
          % (mean_velocity_from_max(4.0), 4.0))


if __name__ == "__main__":
    _demo()
