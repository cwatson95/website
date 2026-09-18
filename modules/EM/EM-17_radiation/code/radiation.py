"""EM-17  Radiation -- retarded potentials, Lienard-Wiechert, dipole & Larmor.

Physics topic network, module EM-17 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 10.2-10.3 (potentials) and 11.1-11.2 (radiation).
Builds on ~EM-01/~EM-08 (EPS0, MU0 -> c), ~MA-01 (vector ops); the retarded
potential is a Green's-function solution of the wave equation (~MA-14).

News of a source travels at c, so the potentials depend on the RETARDED time
    t_r = t - ɽ/c        (Eq. 10.19),
and for a moving point charge they become the Lienard-Wiechert potentials
    V = (1/4 pi eps0) q c / (ɽ c - ɽ . v) ,   A = (v / c^2) V       (Eq. 10.46-10.47),
all evaluated at t_r.  Accelerating charges radiate: a slow charge by the Larmor
formula P = mu0 q^2 a^2 / (6 pi c) (Eq. 11.70), an oscillating dipole with the
sin^2(theta) pattern and total power P = mu0 p0^2 w^4 / (12 pi c) (Eq. 11.22).
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

from electrostatics import EPS0, K_E                         # noqa: E402
from magnetostatics import MU0                               # noqa: E402
from vector_algebra import dot, norm, unit                   # noqa: E402

C = 1.0 / math.sqrt(MU0 * EPS0)

__all__ = [
    "C", "retarded_time", "retarded_potential_static",
    "lienard_wiechert", "larmor_power",
    "dipole_radiated_power", "dipole_angular_power", "total_power_from_pattern",
]


def _sub(a, b):
    return (a[0] - b[0], a[1] - b[1], a[2] - b[2])


# --- retarded time and potentials (Eq. 10.19, 10.26) -------------------------

def retarded_time(field_point, trajectory, t, c=C, iters=200, tol=1e-15):
    """Solve the implicit retarded-time condition t_r = t - |r - w(t_r)|/c for a
    source moving along trajectory w(.). Fixed-point iteration (converges for
    sub-luminal motion).  For a static source this returns t - distance/c."""
    tr = t
    for _ in range(iters):
        d = norm(_sub(field_point, trajectory(tr)))
        new = t - d / c
        if abs(new - tr) <= tol:
            return new
        tr = new
    return tr


def retarded_potential_static(q, source, field_point, t, c=C):
    """For a STATIC point charge the retarded potential is just Coulomb's, since
    the source never moved:  V = q/(4 pi eps0 r), evaluated at any t.  Returned
    with its retarded time t_r = t - r/c to make the causal delay explicit."""
    r = norm(_sub(field_point, source))
    return K_E * q / r, t - r / c


def lienard_wiechert(q, trajectory, velocity, field_point, t, c=C):
    """Lienard-Wiechert potentials of a moving point charge (Eq. 10.46-10.47):
        V = (1/4 pi eps0) q / [ ɽ (1 - rhat . v / c) ] ,   A = (v / c^2) V,
    with ɽ, rhat, v all at the retarded time.  Returns (V, A_vec, t_r)."""
    tr = retarded_time(field_point, trajectory, t, c)
    sep = _sub(field_point, trajectory(tr))
    script_r = norm(sep)
    rhat = unit(sep)
    v = velocity(tr)
    denom = script_r * (1.0 - dot(rhat, v) / c)
    V = K_E * q / denom
    A = tuple(vi / c ** 2 * V for vi in v)
    return V, A, tr


# --- radiated power (Eq. 11.70, 11.22, 11.21) --------------------------------

def larmor_power(q, a):
    """Larmor formula -- power radiated by a slow, accelerating point charge
    (Eq. 11.70):  P = mu0 q^2 a^2 / (6 pi c)."""
    return MU0 * q ** 2 * a ** 2 / (6.0 * math.pi * C)


def dipole_radiated_power(p0, omega):
    """Total time-averaged power of an oscillating electric dipole p0 cos(wt)
    (Eq. 11.22):  <P> = mu0 p0^2 w^4 / (12 pi c)."""
    return MU0 * p0 ** 2 * omega ** 4 / (12.0 * math.pi * C)


def dipole_angular_power(theta, p0, omega):
    """Angular distribution of dipole radiation (Eq. 11.21):
        dP/dOmega = (mu0 p0^2 w^4 / 32 pi^2 c) sin^2(theta).
    Doughnut pattern: maximum broadside (theta=pi/2), null along the axis."""
    return (MU0 * p0 ** 2 * omega ** 4 / (32.0 * math.pi ** 2 * C)) * math.sin(theta) ** 2


def total_power_from_pattern(p0, omega, n=2000):
    """Integrate dP/dOmega over the sphere -> should recover <P> (Eq. 11.22).
    int sin^2(theta) dOmega = 8 pi / 3."""
    dtheta = math.pi / n
    total = 0.0
    for i in range(n):
        th = (i + 0.5) * dtheta
        total += dipole_angular_power(th, p0, omega) * 2.0 * math.pi * math.sin(th) * dtheta
    return total


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-17 radiation -- demo")
    print("=" * 30)

    # retarded time for a static charge: t_r = t - r/c
    src, fp = (0.0, 0.0, 0.0), (3.0, 0.0, 0.0)
    V, tr = retarded_potential_static(1e-9, src, fp, t=10.0)
    print(f"static charge: V at r=3 m = {V:.4f} V,  t_r = t - r/c = {tr:.10f} s")

    # Lienard-Wiechert for a charge moving at constant velocity along x
    q, v0 = 1e-9, 0.5 * C
    traj = lambda tt: (v0 * tt, 0.0, 0.0)
    vel = lambda tt: (v0, 0.0, 0.0)
    Vlw, Alw, trlw = lienard_wiechert(q, traj, vel, (0.0, 2.0, 0.0), t=0.0)
    print(f"\nmoving charge (v=0.5c): V_LW = {Vlw:.4f} V,  |A| = {norm(Alw):.3e},  t_r = {trlw:.3e} s")
    print("  (V is enhanced over Coulomb by the 1/(1 - rhat.v/c) beaming factor)")

    # Larmor: an electron in a 1e20 m/s^2 acceleration
    e, a = 1.602e-19, 1e22
    print(f"\nLarmor: electron at a={a:.0e} m/s^2 radiates P = {larmor_power(e, a):.3e} W")

    # dipole radiation: total power vs the integrated angular pattern
    p0, w = 1e-11, 2 * math.pi * 1e8
    P = dipole_radiated_power(p0, w)
    Pint = total_power_from_pattern(p0, w)
    print(f"\noscillating dipole (p0={p0:.0e}, f=100 MHz):")
    print(f"  <P> = mu0 p0^2 w^4 / 12 pi c     = {P:.4e} W")
    print(f"  integral of dP/dOmega over sphere = {Pint:.4e} W  (match)")
    print(f"  pattern: broadside/axial ratio = {dipole_angular_power(math.pi/2,p0,w):.3e} "
          f"/ {dipole_angular_power(0.0,p0,w):.1e} (null on axis)")


if __name__ == "__main__":
    _demo()
