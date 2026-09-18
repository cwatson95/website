"""PK-02  Fluid & MHD description of a plasma -- velocity moments, continuity,
momentum, and the characteristic speeds of magnetohydrodynamics.

Physics topic network, module PK-02 (modules/topic_network.txt).
Source: Michel, *Introduction to Laser-Plasma Interactions* (Springer), Ch. 1 --
Sect. 1.2.3 (equilibrium/Maxwellian velocity distributions), Sect. 1.2.4 (kinetic
Vlasov and FLUID descriptions: the moment hierarchy), Sect. 1.3.1-1.3.2 (the
dielectric/fluid wave framework and acoustic waves).  The ideal-MHD reduction,
the Alfven speed, the magnetic pressure and the plasma beta are standard
magnetized-plasma results (stated by Michel at chapter level; laser plasmas are
usually unmagnetized).  Builds on ~PK-01 (the distribution function f and the
Vlasov/Boltzmann equation); the continuity equation is KEY BRIDGE B2, the same
local conservation law as mass (~CM-22), charge (~EM-13) and probability (~QM-04).

Taking velocity moments of the kinetic equation (integrating the Vlasov equation
weighted by 1, v, v^2, ...) turns f(r, v, t) into fluid fields:

    n   = integral f d^3v                              (number density,   0th moment)
    u   = (1/n) integral v f d^3v                      (mean velocity,    1st moment)
    P   = m integral (v-u)(v-u) f d^3v                 (pressure tensor,  2nd moment)
    p   = (1/3) tr P = n k_B T                          (scalar pressure, Maxwellian)

The 0th moment of the Vlasov equation gives CONTINUITY (Michel Eq. 1.63)

    d n / dt + div(n u) = 0,

and the 1st moment gives the MOMENTUM (force) equation (Michel Eqs. 1.73-1.74)

    m n (d u/dt + u . grad u) = - div P + q n (E + u x B).

Each moment couples to the next (continuity needs u, momentum needs P, ...): the
hierarchy must be CLOSED, usually polytropically  p = C rho^gamma  (so the
pressure-gradient term becomes grad p = gamma k_B T grad n).  Summing the two-fluid
equations over species under quasineutrality yields IDEAL MHD,

    rho D u/Dt = - grad p + J x B,     E + u x B = 0,     dB/dt = curl(u x B),

with characteristic speeds  c_s = sqrt(gamma p/rho) (sound),
v_A = B / sqrt(mu0 rho) (Alfven),  and  v_fast = sqrt(c_s^2 + v_A^2) (fast
magnetosonic, perpendicular propagation); the magnetic pressure is B^2/2mu0 and
the plasma beta is beta = p / (B^2/2mu0).

Conventions: SI throughout, with k_B restored explicitly (Michel measures T in
energy units, k_B = 1; here p = n k_B T).
"""

import numpy as np

# --- local physical constants (SI) -- module is self-contained ----------------
MU0 = 4.0e-7 * np.pi          # vacuum permeability  [T m / A] = [H/m]
K_B = 1.380649e-23            # Boltzmann constant   [J/K]
M_P = 1.67262192369e-27       # proton mass          [kg]
M_E = 9.1093837015e-31        # electron mass        [kg]  (demo convenience)

__all__ = [
    "MU0", "K_B", "M_P", "M_E",
    "moments_of_maxwellian",
    "sound_speed", "alfven_speed", "fast_magnetosonic_speed",
    "magnetic_pressure", "plasma_beta",
    "continuity_residual",
]


# --- velocity moments of a drifting Maxwellian (Michel Sect. 1.2.3-1.2.4) ------

def moments_of_maxwellian(n, u, T, m, n_grid=4001, n_thermal=8.0):
    """Recover the fluid fields (n, u, p) by numerically integrating the
    velocity moments of a drifting Maxwellian

        f(v) = n (m/2 pi k_B T)^{3/2} exp[ -m |v - u|^2 / (2 k_B T) ].

    Returns (n_rec, u_rec, p_rec):
        n_rec = integral f d^3v                       -> n            (0th moment)
        u_rec = (1/n) integral v f d^3v               -> u            (1st moment)
        p_rec = (1/3) m integral |v-u|^2 f d^3v       -> n k_B T      (scalar pressure)

    The drifting Maxwellian is separable, so the 3-D integral factorizes into three
    1-D quadratures (trapezoid rule over u_i +/- n_thermal * v_T).  This is the
    numerical demonstration that the 0th/1st/2nd moments reproduce (n, u, n k_B T)
    -- the foundation of the fluid description (Michel Sect. 1.2.4.2).
    """
    u = np.asarray(u, dtype=float)
    if u.shape != (3,):
        raise ValueError("u must be a length-3 velocity vector")
    v_T = np.sqrt(K_B * T / m)                          # thermal speed sqrt(k_B T/m)
    pref = np.sqrt(m / (2.0 * np.pi * K_B * T))         # 1-D Maxwellian prefactor

    I0 = np.empty(3)   # per-axis normalization  ~ 1
    I1 = np.empty(3)   # per-axis first moment    ~ u_i
    I2 = np.empty(3)   # per-axis central 2nd mom ~ k_B T / m
    for i in range(3):
        vi = u[i] + np.linspace(-n_thermal * v_T, n_thermal * v_T, n_grid)
        f1 = pref * np.exp(-m * (vi - u[i]) ** 2 / (2.0 * K_B * T))
        I0[i] = np.trapezoid(f1, vi)
        I1[i] = np.trapezoid(vi * f1, vi)
        I2[i] = np.trapezoid((vi - u[i]) ** 2 * f1, vi)

    n_rec = n * I0[0] * I0[1] * I0[2]
    u_rec = I1 / I0                                     # componentwise mean velocity
    # scalar pressure p = (m/3) integral |v-u|^2 f d^3v, separated over the 3 axes
    second = (I2[0] * I0[1] * I0[2]
              + I0[0] * I2[1] * I0[2]
              + I0[0] * I0[1] * I2[2])
    p_rec = (m / 3.0) * n * second
    return n_rec, u_rec, p_rec


# --- characteristic speeds (Michel Sect. 1.3; standard MHD) --------------------

def sound_speed(gamma, p, rho):
    """Adiabatic sound speed  c_s = sqrt(gamma p / rho)  (the polytropic-closure
    speed of the momentum equation; gamma = 5/3 for a 3-D monatomic plasma,
    gamma = 3 for the 1-D adiabatic wave of Michel Sect. 1.2.4.2)."""
    return np.sqrt(gamma * p / rho)


def alfven_speed(B, rho, mu0=MU0):
    """Alfven speed  v_A = B / sqrt(mu0 rho)  -- the speed of a shear wave on the
    frozen-in magnetic field, set by magnetic tension over mass density."""
    return B / np.sqrt(mu0 * rho)


def fast_magnetosonic_speed(c_s, v_A):
    """Fast magnetosonic speed for PERPENDICULAR propagation,
    v_fast = sqrt(c_s^2 + v_A^2)  -- sound and Alfven (magnetic-pressure) waves add
    in quadrature when k is perpendicular to B."""
    return np.sqrt(c_s ** 2 + v_A ** 2)


def magnetic_pressure(B, mu0=MU0):
    """Magnetic pressure  P_B = B^2 / (2 mu0)  -- the isotropic part of the Maxwell
    stress; B^2/2mu0 is also the magnetic energy density."""
    return B ** 2 / (2.0 * mu0)


def plasma_beta(n, T, B, mu0=MU0):
    """Plasma beta  beta = p / (B^2 / 2 mu0) = n k_B T / (B^2 / 2 mu0),  the ratio
    of thermal to magnetic pressure (single-component p = n k_B T).  beta << 1 is a
    magnetically dominated (force-free) plasma; beta >> 1 is gas-pressure dominated."""
    p = n * K_B * T
    return p / magnetic_pressure(B, mu0)


# --- the 0th-moment law: continuity for a 1-D advected density (cf. ~CM-22) ----

def continuity_residual(rho0, rho1, u, dx, dt):
    """Finite-difference residual of the continuity equation  d rho/dt + d(rho u)/dx
    across one time step, for a 1-D density advected at constant speed u.

    Mirrors ~CM-22 / ~QM-04 `continuity_residual` (same conservation law, KEY BRIDGE
    B2 -- here the conserved density is plasma number density n).  Uses a centred
    time difference for d rho/dt and the midpoint of the flux divergence at the two
    end states; returns the residual ARRAY (~0 wherever the profile is resolved).
    For a rigid travelling wave rho = f(x - u t) the residual vanishes identically.
    """
    drho_dt = (rho1 - rho0) / dt
    flux0 = rho0 * u
    flux1 = rho1 * u
    div_flux = 0.5 * (np.gradient(flux0, dx) + np.gradient(flux1, dx))
    return drho_dt + div_flux


# --- demo ---------------------------------------------------------------------

def _demo():
    print("PK-02  Fluid & MHD description -- demo")
    print("=" * 46)

    # 1) velocity moments of a drifting Maxwellian recover (n, u, p = n k_B T)
    n = 1.0e19            # m^-3
    u = (1.0e5, 0.0, 0.0)  # drift velocity [m/s]
    T = 1.0e5            # K
    m = M_P              # proton plasma
    n_rec, u_rec, p_rec = moments_of_maxwellian(n, u, T, m)
    print("\n1) moments of a drifting Maxwellian (n=%.1e, u_x=%.1e, T=%.1e K):" % (n, u[0], T))
    print("   0th moment  n   = %.6e  (input %.6e)" % (n_rec, n))
    print("   1st moment  u_x = %.6e  (input %.6e)" % (u_rec[0], u[0]))
    print("   2nd moment  p   = %.6e  =  n k_B T = %.6e" % (p_rec, n * K_B * T))

    # 2) representative magnetized plasma: speeds, magnetic pressure, beta
    n = 1.0e19           # m^-3   (e.g. tokamak edge / dense laser-produced plasma)
    T = 1.16e6           # K      (~100 eV)
    B = 1.0              # T
    gamma = 5.0 / 3.0
    rho = n * M_P
    p = n * K_B * T
    c_s = sound_speed(gamma, p, rho)
    v_A = alfven_speed(B, rho)
    v_f = fast_magnetosonic_speed(c_s, v_A)
    P_B = magnetic_pressure(B)
    beta = plasma_beta(n, T, B)
    print("\n2) magnetized hydrogen plasma  (n=%.1e /m^3, T=%.2e K ~100 eV, B=%.1f T):" % (n, T, B))
    print("   thermal pressure p   = %.3e Pa" % p)
    print("   magnetic pressure P_B= %.3e Pa  (= B^2/2mu0)" % P_B)
    print("   sound speed   c_s    = %.3e m/s  (= sqrt(gamma p/rho))" % c_s)
    print("   Alfven speed  v_A    = %.3e m/s  (= B/sqrt(mu0 rho))" % v_A)
    print("   fast magnetosonic    = %.3e m/s  (= sqrt(c_s^2+v_A^2))" % v_f)
    print("   plasma beta   beta   = %.3e        (= p / P_B)" % beta)
    print("   -> beta << 1: magnetically dominated, c_s << v_A")

    # 3) the 0th-moment law: continuity holds for an advected density bump
    L, npts = 40.0, 400
    x = np.linspace(-L / 2, L / 2, npts)
    dx = x[1] - x[0]
    u1d, dt = 0.5, 1e-3
    bump = lambda xx: np.exp(-(xx) ** 2)
    rho0 = bump(x - u1d * 0.0)
    rho1 = bump(x - u1d * dt)
    res = continuity_residual(rho0, rho1, u1d, dx, dt)
    drho_dt = (rho1 - rho0) / dt
    print("\n3) continuity (0th moment) for rho = exp(-(x-ut)^2), u=%.1f:" % u1d)
    print("   max|d rho/dt|        = %.3e" % np.max(np.abs(drho_dt)))
    print("   max|d rho/dt+d(ru)/dx|= %.3e   (residual << term -> mass conserved)"
          % np.max(np.abs(res)))


if __name__ == "__main__":
    _demo()
