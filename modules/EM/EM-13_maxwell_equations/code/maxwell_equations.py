"""EM-13  Maxwell's equations -- displacement current, the four laws, plane waves.

Physics topic network, module EM-13 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 7.3.  Builds on ~EM-01 (EPS0), ~EM-08 (MU0), and
~MA-02 (divergence, curl) -- the four equations are statements about div and curl
of E and B, evaluated here directly on field functions.

Maxwell's fix to Ampere's law adds the displacement current Jd = eps0 dE/dt
(Eq. 7.38), closing the set (Eq. 7.39-7.42):
    div E = rho/eps0 ,   div B = 0 ,
    curl E = - dB/dt ,   curl B = mu0 J + mu0 eps0 dE/dt .
The pay-off is light: in vacuum the equations force a wave with speed
c = 1/sqrt(mu0 eps0).  The headline check (`verify_vacuum_plane_wave`) feeds a
plane wave through MA-02's operators and confirms all four residuals vanish.
Verification uses natural units (c given as a parameter) to keep the
finite-difference time derivative well conditioned.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
_EM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-08_magnetostatics", "code"))
for _p in (_EM01, _EM08):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from electrostatics import EPS0                              # noqa: E402
from magnetostatics import MU0                               # noqa: E402
from vector_algebra import norm                              # noqa: E402
from vector_calculus import divergence, curl                 # noqa: E402

C_SI = 1.0 / math.sqrt(MU0 * EPS0)        # speed of light from the SI constants

__all__ = [
    "EPS0", "MU0", "C_SI", "displacement_current_density",
    "plane_wave_fields", "partial_t",
    "gauss_E_residual", "gauss_B_residual",
    "faraday_residual", "ampere_maxwell_residual",
    "verify_vacuum_plane_wave",
]

_TINY = 1e-300


def _snap(F, t):
    """Freeze a field F(x,y,z,t) at time t -> a spatial field f(x,y,z)."""
    return lambda x, y, z: F(x, y, z, t)


# --- displacement current (Eq. 7.38) -----------------------------------------

def displacement_current_density(dE_dt):
    """Maxwell's displacement current density  Jd = eps0 dE/dt  (Eq. 7.38),
    given the time derivative dE/dt as a 3-tuple (SI)."""
    return tuple(EPS0 * c for c in dE_dt)


# --- a vacuum plane wave (Sect. 9.2, used to test Sect. 7.3) -----------------

def plane_wave_fields(E0, k, c=1.0):
    """Monochromatic plane wave propagating +z, E along x, B along y:
        E = E0 cos(kz - wt) xhat ,   B = (E0/c) cos(kz - wt) yhat ,   w = c k.
    Returns (E, B, w) with E, B as 4-arg field functions (x, y, z, t)."""
    w = c * k
    B0 = E0 / c

    def E(x, y, z, t):
        ph = math.cos(k * z - w * t)
        return (E0 * ph, 0.0, 0.0)

    def B(x, y, z, t):
        ph = math.cos(k * z - w * t)
        return (0.0, B0 * ph, 0.0)
    return E, B, w


def partial_t(F, x, y, z, t, dt=1e-6):
    """Time derivative dF/dt of a 4-arg vector field (central difference)."""
    fp, fm = F(x, y, z, t + dt), F(x, y, z, t - dt)
    return tuple((fp[i] - fm[i]) / (2.0 * dt) for i in range(3))


# --- the four Maxwell residuals (normalized, ~0 when satisfied) ---------------

def gauss_E_residual(E, rho, x, y, z, t):
    """div E - rho/eps0, normalized by the field's derivative scale (~|curl E|)."""
    dE = divergence(_snap(E, t))(x, y, z)
    scale = norm(curl(_snap(E, t))(x, y, z)) + _TINY
    return (dE - rho / EPS0) / scale


def gauss_B_residual(B, x, y, z, t):
    """div B, normalized by |curl B| (B has no sources: div B = 0)."""
    dB = divergence(_snap(B, t))(x, y, z)
    scale = norm(curl(_snap(B, t))(x, y, z)) + _TINY
    return dB / scale


def faraday_residual(E, B, x, y, z, t):
    """|curl E + dB/dt| / max(|curl E|, |dB/dt|)   (Faraday, Eq. 7.41)."""
    cE = curl(_snap(E, t))(x, y, z)
    dB = partial_t(B, x, y, z, t)
    r = tuple(cE[i] + dB[i] for i in range(3))
    scale = max(norm(cE), norm(dB)) + _TINY
    return norm(r) / scale


def ampere_maxwell_residual(E, B, J, x, y, z, t, c=1.0):
    """|curl B - mu0 J - (1/c^2) dE/dt| normalized (Ampere-Maxwell, Eq. 7.42).
    In the wave's units mu0 eps0 = 1/c^2; J is a 3-tuple current density."""
    cB = curl(_snap(B, t))(x, y, z)
    dE = partial_t(E, x, y, z, t)
    disp = tuple(dE[i] / c ** 2 for i in range(3))
    Jt = tuple(MU0 * J[i] for i in range(3))
    r = tuple(cB[i] - Jt[i] - disp[i] for i in range(3))
    scale = max(norm(cB), norm(disp), norm(Jt)) + _TINY
    return norm(r) / scale


def verify_vacuum_plane_wave(E0, k, c, point, t):
    """Evaluate all four Maxwell residuals for a vacuum plane wave at (point, t).
    Returns a dict of normalized residuals -- all ~0 if Maxwell is satisfied."""
    E, B, w = plane_wave_fields(E0, k, c)
    x, y, z = point
    return {
        "gauss_E": gauss_E_residual(E, 0.0, x, y, z, t),
        "gauss_B": gauss_B_residual(B, x, y, z, t),
        "faraday": faraday_residual(E, B, x, y, z, t),
        "ampere_maxwell": ampere_maxwell_residual(E, B, (0.0, 0.0, 0.0), x, y, z, t, c),
    }


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-13 Maxwell's equations -- demo")
    print("=" * 36)
    print(f"speed of light from SI constants: c = 1/sqrt(mu0 eps0) = {C_SI:.6e} m/s")

    # displacement current magnitude (Eq. 7.38) for a charging capacitor: dE/dt
    dEdt = (1e12, 0.0, 0.0)        # V/m/s
    Jd = displacement_current_density(dEdt)
    print(f"\ndisplacement current for dE/dt = 1e12 V/m/s:  Jd = eps0 dE/dt = {Jd[0]:.4e} A/m^2")

    # the headline: a vacuum plane wave satisfies all four Maxwell equations
    print("\nvacuum plane wave (E0=1, k=1, c=1), Maxwell residuals at a few (point,t):")
    for (point, t) in [((0.1, 0.2, 0.3), 0.4), ((1.0, -0.5, 0.7), 1.3)]:
        res = verify_vacuum_plane_wave(1.0, 1.0, 1.0, point, t)
        s = "  ".join(f"{k}={v:.1e}" for k, v in res.items())
        print(f"  at {point}, t={t}:  {s}")
    print("\nAll four residuals -> 0: div E=0, div B=0, curl E=-dB/dt, curl B=(1/c^2)dE/dt.")
    print("The wave is self-consistent only when w = c k -- light is a Maxwell solution.")


if __name__ == "__main__":
    _demo()
