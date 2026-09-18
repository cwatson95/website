"""EM-02  Gauss's law -- flux, symmetry, and the fields of charge distributions.

Physics topic network, module EM-02 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 2.2.  Builds on ~EM-01 (point-charge fields) and
~MA-02 (surface_flux for the flux integral, divergence for the local form).

Integral Gauss's law (Eq. 2.13) :   oint E . da = Q_enc / eps0
Differential Gauss's law (Eq. 2.16):  div E = rho / eps0

The headline check is that the flux of a point charge through ANY closed surface
that encloses it is q/eps0, independent of the surface -- computed here by feeding
EM-01's field straight into MA-02's `surface_flux`.  We also give the three
high-symmetry fields of Sect. 2.2.3 (sphere, line, plane).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
if _EM01 not in sys.path:
    sys.path.insert(0, _EM01)

# EM-01 puts MA-01 and MA-02 on the path as a side effect of importing it.
from electrostatics import EPS0, K_E, point_charge_field, coulomb_field  # noqa: E402
from vector_calculus import surface_flux, divergence                     # noqa: E402

__all__ = [
    "sphere_surface", "flux_through_sphere", "enclosed_charge", "gauss_residual",
    "uniform_sphere_field", "line_charge_field", "plane_sheet_field",
]


# --- closed surfaces and the flux integral (Eq. 2.13) ------------------------

def sphere_surface(center=(0.0, 0.0, 0.0), R=1.0):
    """Outward-oriented parametrization S(u,v) of a sphere of radius R, with
    u = polar in [0, pi], v = azimuth in [0, 2 pi]. Feed to MA-02 surface_flux."""
    cx, cy, cz = center

    def S(u, v):
        return (cx + R * math.sin(u) * math.cos(v),
                cy + R * math.sin(u) * math.sin(v),
                cz + R * math.cos(u))
    return S


def flux_through_sphere(E, center=(0.0, 0.0, 0.0), R=1.0, n=80):
    """Electric flux  oint E . da  through a sphere, via MA-02 surface_flux."""
    return surface_flux(E, sphere_surface(center, R), 0.0, math.pi, 0.0, 2.0 * math.pi, n, n)


def enclosed_charge(E, center=(0.0, 0.0, 0.0), R=1.0, n=80):
    """Charge enclosed by a Gaussian sphere, read off Gauss's law:  Q = eps0 * flux."""
    return EPS0 * flux_through_sphere(E, center, R, n)


def gauss_residual(E, rho, point, h_scale=None):
    """Local Gauss check at `point`:  div E - rho/eps0  (should be ~0, Eq. 2.16).

    Returns the residual divided by the natural scale rho/eps0 when that is
    nonzero, so the finite-difference truncation error reads as a pure number.
    """
    x, y, z = point
    resid = divergence(E)(x, y, z) - rho / EPS0
    scale = abs(rho / EPS0)
    return resid / scale if scale > 0 else resid


# --- the three textbook symmetries (Sect. 2.2.3) -----------------------------

def uniform_sphere_field(Q, R, center=(0.0, 0.0, 0.0)):
    """Field of a uniformly charged solid sphere (total charge Q, radius R):
        outside (r >= R):  E = k Q / r^2  rhat        (looks like a point charge)
        inside  (r <  R):  E = k Q r / R^3  rhat       (grows linearly)
    Continuous at r = R. Returns a field function."""
    cx, cy, cz = center

    def E(x, y, z):
        rx, ry, rz = x - cx, y - cy, z - cz
        r = math.sqrt(rx * rx + ry * ry + rz * rz)
        if r == 0.0:
            return (0.0, 0.0, 0.0)
        if r >= R:
            c = K_E * Q / (r ** 3)
        else:
            c = K_E * Q / (R ** 3)                       # k Q r / R^3 along rhat
        return (c * rx, c * ry, c * rz)
    return E


def line_charge_field(lam, axis="z"):
    """Field of an infinite line charge (linear density lam) on the given axis:
        E = lam / (2 pi eps0 s)  shat ,   s = distance from the axis.
    Cylindrical-radial, falls off like 1/s (Eq. from Sect. 2.2.3)."""
    def E(x, y, z):
        if axis == "z":
            sx, sy, sz = x, y, 0.0
        elif axis == "y":
            sx, sy, sz = x, 0.0, z
        else:
            sx, sy, sz = 0.0, y, z
        s = math.sqrt(sx * sx + sy * sy + sz * sz)
        if s == 0.0:
            return (0.0, 0.0, 0.0)
        c = lam / (2.0 * math.pi * EPS0 * s * s)         # /s for magnitude, /s for unit vec
        return (c * sx, c * sy, c * sz)
    return E


def plane_sheet_field(sigma, normal="z"):
    """Field of an infinite sheet of surface charge sigma in a coordinate plane:
        E = sigma / (2 eps0)  away from the sheet (uniform, Sect. 2.2.3).
    The field is discontinuous by sigma/eps0 across the sheet."""
    i = {"x": 0, "y": 1, "z": 2}[normal]
    mag = sigma / (2.0 * EPS0)

    def E(x, y, z):
        coord = (x, y, z)[i]
        out = [0.0, 0.0, 0.0]
        out[i] = mag if coord >= 0.0 else -mag
        return tuple(out)
    return E


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-02 Gauss's law -- demo")
    print("=" * 32)

    q = 1e-9
    E = point_charge_field(q)
    print("flux of a 1 nC point charge through enclosing spheres (Eq. 2.13):")
    for R in (0.1, 0.5, 2.0):
        phi = flux_through_sphere(E, (0, 0, 0), R)
        print(f"  R = {R:>4} m:  eps0 * flux = {EPS0 * phi:.4e} C   (= q = {q:.1e}, surface-independent)")

    # a charge OUTSIDE the surface contributes zero net flux
    Eout = point_charge_field(q, (3.0, 0.0, 0.0))
    print(f"\ncharge outside the sphere:  eps0 * flux = {EPS0 * flux_through_sphere(Eout, (0,0,0), 1.0):.2e} C   (= 0)")

    # high-symmetry fields (Sect. 2.2.3)
    Q, R = 2e-9, 0.1
    Es = uniform_sphere_field(Q, R)
    from electrostatics import field_magnitude
    print(f"\nuniformly charged sphere (Q={Q:.0e} C, R={R} m):")
    print(f"  |E| at r=2R   = {field_magnitude(Es)(2*R,0,0):.4e}  (k Q /(2R)^2 = {K_E*Q/(2*R)**2:.4e})")
    print(f"  |E| at r=R/2  = {field_magnitude(Es)(R/2,0,0):.4e}  (k Q (R/2)/R^3 = {K_E*Q*(R/2)/R**3:.4e})")

    # local (differential) Gauss inside the sphere:  div E = rho/eps0
    rho = Q / ((4.0 / 3.0) * math.pi * R ** 3)
    print(f"\ndifferential Gauss inside (Eq. 2.16):  (div E - rho/eps0)/(rho/eps0) = "
          f"{gauss_residual(Es, rho, (R/3, 0, 0)):.2e}  (-> 0)")

    sig = 1e-9
    Ep = plane_sheet_field(sig)
    jump = Ep(0, 0, 1e-6)[2] - Ep(0, 0, -1e-6)[2]
    print(f"\ninfinite sheet (sigma={sig:.0e}):  field jump across it = {jump:.4e}  (= sigma/eps0 = {sig/EPS0:.4e})")


if __name__ == "__main__":
    _demo()
