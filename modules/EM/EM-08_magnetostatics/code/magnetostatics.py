"""EM-08  Magnetostatics -- Lorentz force, Biot-Savart, Ampere's law.

Physics topic network, module EM-08 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 5.1-5.3.  Builds on ~MA-01 (cross product, the heart
of every magnetic formula) and ~MA-02 (line_integral for Ampere, divergence for
div B = 0).

Magnetic force is a cross product:
    F = Q (v x B)              (Eq. 5.1)        F = I (dl x B)   (Eq. 5.16)
Steady currents source B through the Biot-Savart law:
    B(r) = (mu0 I / 4 pi) int (dl' x rhat) / r^2      (Eq. 5.39)
and the field obeys the magnetostatic Maxwell pair
    div B = 0   (Eq. 5.50)      curl B = mu0 J   ->   oint B.dl = mu0 I_enc  (Eq. 5.57).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-01_vector_algebra", "code"))
_MA02 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-02_vector_calculus", "code"))
for _p in (_MA01, _MA02):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from vector_algebra import cross, dot, norm      # noqa: E402
from vector_calculus import line_integral, divergence   # noqa: E402

__all__ = [
    "MU0", "lorentz_force", "force_on_wire",
    "biot_savart", "circular_loop_field", "loop_axis_field_closed",
    "infinite_wire_field", "ampere_circulation", "div_B_residual",
]

MU0 = 1.25663706212e-6        # vacuum permeability  [T m / A]  (~ 4 pi x 1e-7)


# --- magnetic force (Eq. 5.1, 5.16) ------------------------------------------

def lorentz_force(Q, v, B, E=(0.0, 0.0, 0.0)):
    """Lorentz force  F = Q(E + v x B)  (Eq. 5.1; magnetic part Q v x B).
    Uses MA-01 cross. v, B, E are 3-tuples; returns the force 3-tuple."""
    vxB = cross(v, B)
    return tuple(Q * (E[i] + vxB[i]) for i in range(3))


def force_on_wire(I, dl, B):
    """Force on a straight current element  F = I (dl x B)  (Eq. 5.16)."""
    f = cross(dl, B)
    return tuple(I * c for c in f)


# --- Biot-Savart law (Eq. 5.39) ----------------------------------------------

def biot_savart(I, path, a, b, n=2000):
    """B(r) of a current I along the curve path(t), t in [a, b] (Eq. 5.39):
        B = (mu0 I / 4 pi) int (dl' x (r - l')) / |r - l'|^3 dt,
    with dl' = path'(t) dt (central difference).  Reuses MA-01 cross."""
    hh = 1e-7
    dt = (b - a) / n
    pref = MU0 * I / (4.0 * math.pi)

    def B(x, y, z):
        bx = by = bz = 0.0
        for k in range(n):
            t = a + (k + 0.5) * dt
            lp = path(t)
            dl = tuple((path(t + hh)[i] - path(t - hh)[i]) / (2.0 * hh) for i in range(3))
            sep = (x - lp[0], y - lp[1], z - lp[2])
            r = norm(sep)
            if r == 0.0:
                continue
            cx, cy, cz = cross(dl, sep)
            inv = 1.0 / r ** 3
            bx += cx * inv
            by += cy * inv
            bz += cz * inv
        return (pref * bx * dt, pref * by * dt, pref * bz * dt)
    return B


def circular_loop_field(I, R, n=2000):
    """B of a circular current loop of radius R in the z=0 plane (Biot-Savart)."""
    loop = lambda t: (R * math.cos(t), R * math.sin(t), 0.0)
    return biot_savart(I, loop, 0.0, 2.0 * math.pi, n)


def loop_axis_field_closed(I, R, z):
    """Closed-form on-axis field of a current loop (Eq. 5.41):
        B_z = mu0 I R^2 / (2 (R^2 + z^2)^(3/2)) ."""
    return MU0 * I * R ** 2 / (2.0 * (R ** 2 + z ** 2) ** 1.5)


# --- infinite straight wire and Ampere's law (Eq. 5.36, 5.57) ----------------

def infinite_wire_field(I, axis="z"):
    """B of an infinite straight wire carrying I along `axis` (Eq. 5.36):
        |B| = mu0 I / (2 pi s),  direction phi-hat (azimuthal, right-hand rule).
    For the z-axis, B = (mu0 I / 2 pi s) (-sin phi, cos phi, 0)."""
    def B(x, y, z):
        if axis == "z":
            s2 = x * x + y * y
            if s2 == 0.0:
                return (0.0, 0.0, 0.0)
            c = MU0 * I / (2.0 * math.pi * s2)             # /s for magnitude, /s for phi-hat
            return (-c * y, c * x, 0.0)
        if axis == "x":
            s2 = y * y + z * z
            if s2 == 0.0:
                return (0.0, 0.0, 0.0)
            c = MU0 * I / (2.0 * math.pi * s2)
            return (0.0, -c * z, c * y)
        s2 = x * x + z * z                                 # axis == 'y'
        if s2 == 0.0:
            return (0.0, 0.0, 0.0)
        c = MU0 * I / (2.0 * math.pi * s2)
        return (c * z, 0.0, -c * x)
    return B


def ampere_circulation(B, s, z0=0.0, n=2000):
    """oint B.dl around a circle of radius s about the z-axis (Eq. 5.57).
    For an enclosed current I this equals mu0 I.  Reuses MA-02 line_integral."""
    circle = lambda t: (s * math.cos(t), s * math.sin(t), z0)
    return line_integral(B, circle, 0.0, 2.0 * math.pi, n)


def div_B_residual(B, point):
    """Local check  div B = 0 (Eq. 5.50), normalized by the field's gradient
    scale |B|/r so the finite-difference residual reads as a pure number."""
    x, y, z = point
    r = norm(point) or 1.0
    scale = norm(B(x, y, z)) / r
    d = divergence(B)(x, y, z)
    return d / scale if scale > 0 else d


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-08 magnetostatics -- demo")
    print("=" * 32)

    # cyclotron geometry: F = Q v x B is perpendicular to v
    Q, v, B0 = 1.602e-19, (1e6, 0.0, 0.0), (0.0, 0.0, 0.5)
    F = lorentz_force(Q, v, B0)
    print("Lorentz force  F = Q v x B:")
    print(f"  v=x_hat, B=z_hat -> F = {tuple(f'{c:.3e}' for c in F)}  (along -y, perp to v and B)")

    # infinite wire
    I = 10.0
    Bw = infinite_wire_field(I)
    print(f"\ninfinite wire I = {I} A:")
    for s in (0.01, 0.05):
        print(f"  |B| at s={s} m = {norm(Bw(s, 0, 0)):.4e} T   (mu0 I/2pi s = {MU0*I/(2*math.pi*s):.4e})")
    print(f"  Ampere: oint B.dl (s=0.03) = {ampere_circulation(Bw, 0.03):.4e}   (mu0 I = {MU0*I:.4e})")
    print(f"  div B / scale = {div_B_residual(Bw, (0.04, 0.02, 0.0)):.2e}  (-> 0)")

    # current loop on its axis: Biot-Savart vs closed form
    I, R = 5.0, 0.1
    Bloop = circular_loop_field(I, R)
    print(f"\ncircular loop I={I} A, R={R} m, on axis:")
    for z in (0.0, 0.1, 0.3):
        print(f"  z={z}: Biot-Savart B_z = {Bloop(0,0,z)[2]:.4e}   closed form = {loop_axis_field_closed(I,R,z):.4e}")


if __name__ == "__main__":
    _demo()
