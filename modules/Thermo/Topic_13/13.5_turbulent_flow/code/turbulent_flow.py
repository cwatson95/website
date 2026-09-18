"""
turbulent_flow.py  —  Module 13.5 (Turbulent Pipe Flow)

CROSS-TRUNK (~CM): this is standard fluid-mechanics material and is NOT in Moran 8e
(Fundamentals of Engineering Thermodynamics).  Moran's Ch.9 (Topic 13's trunk) treats
*compressible* flow; the viscous pipe-flow REGIMES live in fluid mechanics.  References:
F. White, *Fluid Mechanics* 7e Ch.6; Munson/Young/Okiishi, *Fundamentals of Fluid
Mechanics* Ch.8; Cengel & Cimbala, *Fluid Mechanics* Ch.8.  Companion to 13.4 (laminar)
-- same pipe, the OTHER regime.

The governing dimensionless group is the REYNOLDS NUMBER, inertial / viscous forces:

    Re = rho V D / mu = V D / nu          (nu = mu/rho, kinematic viscosity)

For flow in a round pipe the regime is, roughly,
    Re < ~2300    laminar          (module 13.4, f = 64/Re exact)
    2300..4000    transitional
    Re > ~4000    fully TURBULENT  (this module)

In the turbulent regime the Darcy friction factor is NO LONGER 64/Re; it depends on Re
AND on the relative roughness eps/D, and is given implicitly by the COLEBROOK equation

    1/sqrt(f) = -2 log10( (eps/D)/3.7 + 2.51/(Re sqrt(f)) ),

whose smooth-wall (eps -> 0) limit at moderate Re is well approximated by the explicit
BLASIUS correlation  f = 0.316 / Re^0.25  (valid ~4e3 < Re < 1e5).  HAALAND's explicit
formula approximates Colebrook to ~1.5%.  The turbulent velocity profile is much FLATTER
than the laminar parabola; the 1/n power law (n ~ 7) gives  V/u_max = 2n^2/((n+1)(2n+1)).
The Darcy-Weisbach pressure drop  dP = f (L/D)(rho V^2/2)  is unchanged in form.

Units (SI): rho [kg/m^3], V [m/s], D,R,r,L,eps [m], mu [Pa.s], nu [m^2/s], dP [Pa].
NOT a Moran citation -- cross-trunk fluid mechanics.
"""
import math


def reynolds_number(rho, V, D, mu):
    """Reynolds number  Re = rho V D / mu  (inertial / viscous); same group as 13.4.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.3]"""
    return rho * V * D / mu


def reynolds_number_kinematic(V, D, nu):
    """Reynolds number from kinematic viscosity  Re = V D / nu, nu = mu/rho.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.3]"""
    return V * D / nu


def is_turbulent(Re, Re_crit=4000.0):
    """Pipe-flow turbulent criterion  Re > ~4000 (fully turbulent above ~4000).
    [~CM, not from Moran 8e; Cengel & Cimbala Fluid Mechanics, Ch.8]"""
    return Re > Re_crit


def flow_regime(Re):
    """Classify by Reynolds number: 'laminar' (Re<2300), 'transitional'
    (2300<=Re<=4000), or 'turbulent' (Re>4000).
    [~CM, not from Moran 8e; Cengel & Cimbala Fluid Mechanics, Ch.8]"""
    if Re < 2300.0:
        return "laminar"
    if Re <= 4000.0:
        return "transitional"
    return "turbulent"


def friction_factor_blasius(Re):
    """Blasius smooth-pipe turbulent Darcy friction factor  f = 0.316 / Re^0.25
    (valid ~4e3 < Re < 1e5).  [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.38]"""
    return 0.316 * Re ** -0.25


def friction_factor_colebrook(Re, rel_rough, tol=1e-12, itmax=200):
    """Colebrook implicit turbulent Darcy friction factor (Moody chart), solved by
    fixed-point iteration of  1/sqrt(f) = -2 log10( (eps/D)/3.7 + 2.51/(Re sqrt(f)) ).
    rel_rough = eps/D (0 = hydraulically smooth).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.48 (Colebrook 1939)]"""
    f = 0.02
    for _ in range(itmax):
        rhs = -2.0 * math.log10(rel_rough / 3.7 + 2.51 / (Re * math.sqrt(f)))
        f_new = 1.0 / (rhs * rhs)
        if abs(f_new - f) < tol:
            return f_new
        f = f_new
    return f


def friction_factor_haaland(Re, rel_rough):
    """Haaland explicit approximation to Colebrook (within ~1.5%):
    1/sqrt(f) = -1.8 log10( ((eps/D)/3.7)^1.11 + 6.9/Re ).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Eq. 6.49 (Haaland 1983)]"""
    rhs = -1.8 * math.log10((rel_rough / 3.7) ** 1.11 + 6.9 / Re)
    return 1.0 / (rhs * rhs)


def power_law_velocity_profile(u_max, r, R, n=7):
    """Turbulent 1/n power-law profile  u(r) = u_max (1 - r/R)^(1/n)  (n ~ 7).
    Much flatter than the laminar parabola of 13.4.
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.6]"""
    return u_max * (1.0 - r / R) ** (1.0 / n)


def mean_velocity_power_law(u_max, n=7):
    """Mean velocity of the 1/n power-law profile  V/u_max = 2 n^2 / ((n+1)(2n+1)).
    For n=7 this is 0.8167 (vs 0.5 for the laminar parabola).
    [~CM, not from Moran 8e; White Fluid Mechanics 7e, Sec. 6.6]"""
    return u_max * (2.0 * n * n) / ((n + 1.0) * (2.0 * n + 1.0))


def pressure_drop_darcy(f, L, D, rho, V):
    """Darcy-Weisbach pressure drop  dP = f (L/D)(rho V^2 / 2)  (same form as laminar;
    only f differs in the turbulent regime).
    [~CM, not from Moran 8e; Munson Fundamentals of Fluid Mechanics, Sec. 8.4]"""
    return f * (L / D) * (rho * V * V / 2.0)


def head_loss_darcy(f, L, D, V, g=9.80665):
    """Darcy-Weisbach head loss  h_L = f (L/D)(V^2 / 2g)  [m].
    [~CM, not from Moran 8e; Munson Fundamentals of Fluid Mechanics, Sec. 8.4]"""
    return f * (L / D) * (V * V / (2.0 * g))


def _demo():
    print("Module 13.5 -- Turbulent pipe flow  [~CM, NOT from Moran 8e]\n")
    rho, V, D, mu = 1000.0, 2.0, 0.05, 1.0e-3            # water
    Re = reynolds_number(rho, V, D, mu)
    print("  Water pipe: rho=1000, V=2, D=0.05, mu=1e-3 -> Re = %.0f  (%s)"
          % (Re, flow_regime(Re)))
    print("  Blasius   f = 0.316/Re^0.25       = %.5f" % friction_factor_blasius(Re))
    print("  Colebrook f (smooth, eps/D=0)     = %.5f" % friction_factor_colebrook(Re, 0.0))
    print("  Colebrook f (eps/D=0.001)         = %.5f" % friction_factor_colebrook(Re, 0.001))
    print("  Haaland   f (eps/D=0.001)         = %.5f  [~Colebrook]"
          % friction_factor_haaland(Re, 0.001))
    print("  Profile: laminar V/u_max=0.5  vs  turbulent (n=7) V/u_max=%.4f (flatter)"
          % (mean_velocity_power_law(1.0, 7)))
    f = friction_factor_colebrook(Re, 0.0)
    print("  dP over L=10 m (smooth) = %.0f Pa" % pressure_drop_darcy(f, 10.0, D, rho, V))


if __name__ == "__main__":
    _demo()
