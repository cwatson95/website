"""
MA-03  Coordinate systems -- Cartesian, cylindrical, spherical; curvilinear
scale factors and Jacobians.

Part of the physics topic network (modules/topic_network.txt, module MA-03).
Uses ~MA-01 (dot/cross/norm to check the bases are orthonormal & right-handed);
supports ~MA-02 (operators in curvilinear coords) and ~EM-04 / ~QM-12 (problems
with spherical/cylindrical symmetry).

Conventions (physics):
  cylindrical (rho, phi, z):  x=rho cos phi, y=rho sin phi, z=z
  spherical   (r, theta, phi): theta = polar angle from +z in [0,pi];
                               phi = azimuth from +x;
                               x=r sin th cos ph, y=r sin th sin ph, z=r cos th

NOTE: MA-01 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "MA-01_vector_algebra", "code"))
if _MA01 not in sys.path:
    sys.path.insert(0, _MA01)

from vector_algebra import dot  # noqa: E402  (used by the component-conversion helpers)

__all__ = [
    "cart_to_cyl", "cyl_to_cart", "cart_to_sph", "sph_to_cart",
    "cyl_basis", "sph_basis", "cyl_scale_factors", "sph_scale_factors",
    "cyl_jacobian", "sph_jacobian",
    "vector_to_spherical", "vector_from_spherical",
]


# --- point transforms --------------------------------------------------------

def cart_to_cyl(x, y, z):
    """(x,y,z) -> (rho, phi, z),  phi in (-pi, pi]."""
    return (math.hypot(x, y), math.atan2(y, x), z)


def cyl_to_cart(rho, phi, z):
    """(rho, phi, z) -> (x, y, z)."""
    return (rho * math.cos(phi), rho * math.sin(phi), z)


def cart_to_sph(x, y, z):
    """(x,y,z) -> (r, theta, phi),  theta in [0,pi] from +z,  phi in (-pi,pi]."""
    r = math.sqrt(x * x + y * y + z * z)
    theta = math.atan2(math.hypot(x, y), z) if r > 0.0 else 0.0
    return (r, theta, math.atan2(y, x))


def sph_to_cart(r, theta, phi):
    """(r, theta, phi) -> (x, y, z)."""
    s = r * math.sin(theta)
    return (s * math.cos(phi), s * math.sin(phi), r * math.cos(theta))


# --- orthonormal basis vectors (Cartesian components) ------------------------

def cyl_basis(phi):
    """(e_rho, e_phi, e_z) of cylindrical coords at azimuth phi."""
    c, s = math.cos(phi), math.sin(phi)
    return ((c, s, 0.0), (-s, c, 0.0), (0.0, 0.0, 1.0))


def sph_basis(theta, phi):
    """(e_r, e_theta, e_phi) of spherical coords at (theta, phi)."""
    st, ct = math.sin(theta), math.cos(theta)
    cp, sp = math.cos(phi), math.sin(phi)
    e_r = (st * cp, st * sp, ct)
    e_theta = (ct * cp, ct * sp, -st)
    e_phi = (-sp, cp, 0.0)
    return (e_r, e_theta, e_phi)


# --- scale factors & volume elements (Jacobians) -----------------------------

def cyl_scale_factors(rho):
    """(h_rho, h_phi, h_z) = (1, rho, 1)."""
    return (1.0, rho, 1.0)


def sph_scale_factors(r, theta):
    """(h_r, h_theta, h_phi) = (1, r, r sin theta)."""
    return (1.0, r, r * math.sin(theta))


def cyl_jacobian(rho):
    """Volume element factor: dV = rho d(rho) d(phi) dz  ->  rho."""
    return rho


def sph_jacobian(r, theta):
    """Volume element factor: dV = r^2 sin(theta) dr d(theta) d(phi)."""
    return r * r * math.sin(theta)


# --- vector component conversion (reuses MA-01 dot) --------------------------

def vector_to_spherical(vx, vy, vz, theta, phi):
    """Components of a Cartesian vector in the spherical basis at (theta, phi):
       (v_r, v_theta, v_phi) = (v.e_r, v.e_theta, v.e_phi)."""
    v = (vx, vy, vz)
    e_r, e_theta, e_phi = sph_basis(theta, phi)
    return (dot(v, e_r), dot(v, e_theta), dot(v, e_phi))


def vector_from_spherical(v_r, v_theta, v_phi, theta, phi):
    """Inverse of vector_to_spherical: spherical components -> Cartesian."""
    e_r, e_theta, e_phi = sph_basis(theta, phi)
    return tuple(v_r * e_r[i] + v_theta * e_theta[i] + v_phi * e_phi[i] for i in range(3))


# --- demo --------------------------------------------------------------------

def _demo():
    from vector_algebra import cross, norm
    print("MA-03 coordinate systems -- demo")
    print("=" * 32)

    p = (1.0, 1.0, 1.0)
    print("point", p)
    print("  -> cylindrical (rho,phi,z) =", tuple(round(c, 4) for c in cart_to_cyl(*p)))
    print("  -> spherical   (r,theta,phi)=", tuple(round(c, 4) for c in cart_to_sph(*p)))
    print("  round-trip sph:", tuple(round(c, 12) for c in sph_to_cart(*cart_to_sph(*p))))

    theta, phi = math.radians(60), math.radians(40)
    e_r, e_th, e_ph = sph_basis(theta, phi)
    print("\nspherical basis at theta=60,phi=40 deg:")
    print("  |e_r|,|e_th|,|e_ph| =", round(norm(e_r), 6), round(norm(e_th), 6), round(norm(e_ph), 6))
    print("  e_r.e_th, e_r.e_ph  =", round(dot(e_r, e_th), 12), round(dot(e_r, e_ph), 12))
    print("  e_r x e_th == e_ph ?", tuple(round(c, 6) for c in cross(e_r, e_th)))

    r = 2.0
    print("\nscale factors (sph) at r=2,theta=60:", tuple(round(c, 4) for c in sph_scale_factors(r, theta)))
    print("  product == Jacobian r^2 sin th ?", round(1.0 * r * (r * math.sin(theta)), 4),
          "==", round(sph_jacobian(r, theta), 4))


if __name__ == "__main__":
    _demo()
