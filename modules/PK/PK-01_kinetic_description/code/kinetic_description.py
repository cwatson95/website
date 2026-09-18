"""PK-01  Kinetic description -- distribution functions, Vlasov & Boltzmann.

Physics topic network, module PK-01 (modules/topic_network.txt).  First module
of the PLASMA & KINETIC THEORY trunk; it underlies the KrF/LoKI plasma-kinetics
code in Kinetic_Modeling/KrF_and_LoKI.

Source: Michel, *Introduction to Laser-Plasma Interactions* (Springer GTP, 2023),
Sect. 1.2 "Basic Principles of Plasma Physics" -- 1.2.1 Debye length & screening,
1.2.2 the plasma frequency, 1.2.3 Maxwellian velocity distributions, 1.2.4.1 the
Vlasov equation -- and Appendix A.1 "Plasma Parameters" (the formulary).  Builds
on ~SM-06 (the Maxwell-Boltzmann distribution and the Boltzmann transport
equation); the phase-space continuity check mirrors ~QM-04 / ~CM-22 (KEY BRIDGE
B2: one continuity law, many densities).

The one-particle distribution function f(x, v, t) counts particles per unit
phase-space volume,  dN = f d^3x d^3v.  Its velocity moments are the fluid fields

    n = INT f d^3v ,   u = (1/n) INT v f d^3v ,   p = (m/3) INT |v-u|^2 f d^3v .

f obeys the **Boltzmann equation**

    df/dt + v . grad_x f + (F/m) . grad_v f = (df/dt)_coll ,

whose collisionless limit is the **Vlasov equation** (RHS -> 0) with F the
self-consistent mean field.  With the flow divergence-free in phase space this is
just Liouville's theorem  df/dt = 0  along orbits -- the same continuity law as
mass (~CM-22) and probability (~QM-04).  The mean-field picture is justified when
the **plasma parameter** Lambda = n lambda_D^3 (the number of particles in a Debye
sphere) is large: Lambda >> 1 means weak coupling and collective behaviour.

SI units throughout; temperatures in KELVIN (1 eV = E_CHARGE/K_B = 11604.5 K).
"""

import numpy as np

__all__ = [
    "K_B", "EPS0", "M_E", "E_CHARGE",
    "maxwellian", "thermal_speed", "plasma_frequency", "debye_length",
    "plasma_parameter", "free_stream", "vlasov_residual",
]

# --- physical constants (SI, CODATA) -----------------------------------------
K_B = 1.380649e-23          # Boltzmann constant            [J/K]
EPS0 = 8.8541878128e-12     # vacuum permittivity           [F/m]
M_E = 9.1093837015e-31      # electron mass                 [kg]
E_CHARGE = 1.602176634e-19  # elementary charge             [C]  (= 1 eV in J)


# --- the distribution function: the equilibrium Maxwellian (Mi Sect. 1.2.3) --

def maxwellian(v, n, T, m):
    """Isotropic Maxwellian velocity distribution f(v) evaluated at speed v=|v|,

        f(v) = n (m / 2 pi k_B T)^{3/2} exp(-m v^2 / 2 k_B T)     [s^3 / m^6],

    the phase-space (per d^3v) density, NOT the speed pdf.  It is normalized so
    that the zeroth velocity moment returns the number density,
        INT f d^3v = INT_0^inf f(v) 4 pi v^2 dv = n
    (the 4 pi v^2 is the speed Jacobian; the speed pdf is F(v) = 4 pi v^2 f(v),
    which is what ~SM-06 `maxwell_speed_pdf` returns).  T in kelvin, m in kg.
    """
    a = m / (2.0 * np.pi * K_B * T)
    return n * a ** 1.5 * np.exp(-m * np.asarray(v) ** 2 / (2.0 * K_B * T))


def thermal_speed(T, m):
    """Thermal speed  v_T = sqrt(k_B T / m)  (Mi Eq. A.4: v_Te = sqrt(T_e/m)).

    This is the per-component rms velocity (the std-dev of each Cartesian
    velocity component of the Maxwellian); it gives the clean identity
    lambda_D = v_T / omega_p (Mi Eq. A.6).  NB conventions differ -- some authors
    use sqrt(2 k_B T/m) (the most-probable speed) or sqrt(3 k_B T/m) (the 3-D rms,
    = sqrt(3) v_T).  T in kelvin, m in kg."""
    return np.sqrt(K_B * T / m)


# --- collective scales (Mi Sect. 1.2.1-1.2.2, Appendix A.1) ------------------

def plasma_frequency(n, q=E_CHARGE, m=M_E):
    """(Electron) plasma frequency  omega_p = sqrt(n q^2 / eps0 m)   [rad/s]
    (Mi Eq. A.1).  The natural oscillation rate of a charge-density perturbation;
    sets the fastest collective timescale.  Defaults: electron charge & mass."""
    return np.sqrt(n * q ** 2 / (EPS0 * m))


def debye_length(n, T, q=E_CHARGE):
    """Debye length  lambda_D = sqrt(eps0 k_B T / n q^2)   [m]   (Mi Eq. A.6).

    The screening length: a test charge's Coulomb potential is exponentially
    cut off, phi(r) = (q_t/4 pi eps0 r) exp(-r/lambda_D), beyond ~lambda_D.
    Independent of mass; T in kelvin."""
    return np.sqrt(EPS0 * K_B * T / (n * q ** 2))


def plasma_parameter(n, T):
    """Plasma parameter  Lambda = n lambda_D^3   (Mi Eq. A.8: N_De = n_e lambda_De^3).

    The number of particles in a Debye cube -- to a 4 pi/3 it is the count in a
    Debye SPHERE.  Lambda >> 1  <=>  weak coupling: kinetic energy dominates the
    nearest-neighbour Coulomb energy, screening is statistically meaningful, and
    the collision rate is small, nu_ei/omega_p ~ ln(Lambda)/Lambda << 1 -- so the
    mean-field Vlasov description holds.  Uses the electron Debye length."""
    return n * debye_length(n, T) ** 3


# --- phase-space continuity: free streaming & the Vlasov residual ------------
# Mirrors ~QM-04 (exact step `free_step` + finite-difference `continuity_residual`).
# f is laid out as a (Nv, Nx) array: axis 0 = velocity, axis 1 = position x
# (periodic).  The force-free Vlasov equation is df/dt + v df/dx = 0.

def free_stream(f0, x, v, dt):
    """Advect f one free-streaming (force-free) step:  f1(x, v) = f0(x - v dt, v).

    Each velocity row is rigidly translated in x by s = v*dt -- the exact
    characteristic of df/dt + v df/dx = 0 -- done by an exact spectral shift
    (multiply the x-Fourier transform of each row by exp(-i k_x v dt)).  This is
    the phase-space shear that underlies Liouville's theorem: f is merely
    transported, never created or destroyed.  Requires x uniform & periodic
    (use endpoint=False).  Returns the real (Nv, Nx) array f1."""
    dx = x[1] - x[0]
    kx = 2.0 * np.pi * np.fft.fftfreq(x.shape[0], d=dx)          # (Nx,)
    shift = np.exp(-1j * kx[None, :] * np.asarray(v)[:, None] * dt)
    f1 = np.fft.ifft(np.fft.fft(f0, axis=1) * shift, axis=1)
    return np.real(f1)


def vlasov_residual(f0, f1, x, v, dt):
    """Finite-difference residual of the force-free Vlasov / phase-space
    continuity equation  df/dt + v df/dx = 0  across one streaming step.

    Mirrors ~QM-04 `continuity_residual` (same continuity law, phase-space
    density instead of |psi|^2): a centred time difference for df/dt and the
    midpoint of the (periodic, central-difference) v df/dx at the two end states.
    Returns the residual ARRAY (Nv, Nx); for a resolved field it is ~0, far below
    the size of the streaming term v df/dx itself (it is O(dt^2) + O(dx^2))."""
    dx = x[1] - x[0]
    df_dt = (f1 - f0) / dt
    dfdx0 = (np.roll(f0, -1, axis=1) - np.roll(f0, 1, axis=1)) / (2.0 * dx)
    dfdx1 = (np.roll(f1, -1, axis=1) - np.roll(f1, 1, axis=1)) / (2.0 * dx)
    dfdx_mid = 0.5 * (dfdx0 + dfdx1)
    return df_dt + np.asarray(v)[:, None] * dfdx_mid


# --- demo --------------------------------------------------------------------

def _demo():
    print("PK-01  Kinetic description -- distribution functions, Vlasov & Boltzmann")
    print("=" * 72)

    # representative plasma: n = 1e18 /m^3, T = 1 eV
    n, T_eV = 1.0e18, 1.0
    T = T_eV * E_CHARGE / K_B          # 1 eV in kelvin = 11604.5 K
    print("\nrepresentative plasma:  n = %.1e /m^3,  T = %.1f eV (= %.1f K)" % (n, T_eV, T))
    vth = thermal_speed(T, M_E)
    wp = plasma_frequency(n)
    lD = debye_length(n, T)
    Lam = plasma_parameter(n, T)
    print("  electron thermal speed  v_T = sqrt(kT/m)   = %.3e m/s" % vth)
    print("  plasma frequency        omega_p            = %.3e rad/s  (f_p = %.2f GHz)"
          % (wp, wp / (2.0 * np.pi) / 1e9))
    print("  Debye length            lambda_D           = %.3e m" % lD)
    print("    check  v_T / omega_p                     = %.3e m   (= lambda_D)" % (vth / wp))
    print("  plasma parameter        Lambda = n lD^3    = %.1f" % Lam)
    print("    -> Lambda >> 1: weakly coupled, collective; mean-field (Vlasov) holds")

    # Maxwellian moments recovered by velocity integration (n, pressure, energy)
    vmax = 10.0 * vth
    vv = np.linspace(0.0, vmax, 200000)
    f = maxwellian(vv, n, T, M_E)
    jac = 4.0 * np.pi * vv ** 2                      # speed Jacobian d^3v -> dv
    n_moment = np.trapezoid(f * jac, vv)
    p_moment = (M_E / 3.0) * np.trapezoid(vv ** 2 * f * jac, vv)
    print("\nMaxwellian velocity moments (integrate f over d^3v):")
    print("  INT f d^3v            = %.4e /m^3   (input n = %.1e)" % (n_moment, n))
    print("  p = (m/3) INT v^2 f d^3v = %.4e Pa   (n k_B T = %.4e Pa)"
          % (p_moment, n * K_B * T))

    # phase-space continuity: one free-streaming step, Vlasov residual ~ 0
    Nx, Nv = 128, 96
    L = 2.0 * np.pi
    x = np.linspace(0.0, L, Nx, endpoint=False)
    vgrid = np.linspace(-6.0, 6.0, Nv)              # natural units, v_T = 1
    M = np.exp(-vgrid ** 2 / 2.0)                   # Maxwellian background in v
    g = 1.0 + 0.3 * np.cos(x)                       # density perturbation in x
    f0 = M[:, None] * g[None, :]                    # (Nv, Nx) phase-space density
    dt = 1.0e-3
    f1 = free_stream(f0, x, vgrid, dt)
    res = vlasov_residual(f0, f1, x, vgrid, dt)
    stream = vgrid[:, None] * 0.5 * (
        (np.roll(f0, -1, 1) - np.roll(f0, 1, 1)) +
        (np.roll(f1, -1, 1) - np.roll(f1, 1, 1))) / (2.0 * (x[1] - x[0]))
    print("\nphase-space free streaming, one dt = %.0e step (df/dt + v df/dx = 0):" % dt)
    print("  max |streaming term  v df/dx|     = %.3e" % np.max(np.abs(stream)))
    print("  max |Vlasov residual|             = %.3e  (<< term -> continuity holds)"
          % np.max(np.abs(res)))
    print("  total INT f dx dv: t=0 -> %.6e ,  t=dt -> %.6e  (conserved)"
          % (f0.sum(), f1.sum()))


if __name__ == "__main__":
    _demo()
