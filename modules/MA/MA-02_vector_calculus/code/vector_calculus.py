"""
MA-02  Vector calculus -- grad, div, curl, Laplacian; line & surface integrals.

Part of the physics topic network (modules/topic_network.txt, module MA-02).
Builds on ~MA-01 (uses dot/cross/unit); feeds ~EM-* (Maxwell), ~CM-22 (continuity).

A scalar field is a function  f(x, y, z) -> number;  a vector field is a function
F(x, y, z) -> (Fx, Fy, Fz).  The differential operators return NEW fields (closed
over a step size h, evaluated by central finite differences), so results compose:
laplacian(f) == divergence(gradient(f)), curl(gradient(f)) == 0, etc.

The integral helpers (line_integral, surface_flux) let you check the integral
theorems numerically -- Stokes and the divergence theorem -- and they reuse
MA-01's dot and cross directly.

NOTE: MA-01 is imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA01 = os.path.abspath(os.path.join(_HERE, "..", "..", "MA-01_vector_algebra", "code"))
if _MA01 not in sys.path:
    sys.path.insert(0, _MA01)

from vector_algebra import dot, cross, unit  # noqa: E402

__all__ = [
    "gradient", "divergence", "curl", "laplacian", "directional_derivative",
    "line_integral", "surface_flux",
]


# --- differential operators (central finite differences) ---------------------

def gradient(f, h=1e-5):
    """grad f = (df/dx, df/dy, df/dz)   (scalar field -> vector field)."""
    def g(x, y, z):
        return ((f(x + h, y, z) - f(x - h, y, z)) / (2.0 * h),
                (f(x, y + h, z) - f(x, y - h, z)) / (2.0 * h),
                (f(x, y, z + h) - f(x, y, z - h)) / (2.0 * h))
    return g


def divergence(F, h=1e-5):
    """div F = dFx/dx + dFy/dy + dFz/dz   (vector field -> scalar field)."""
    def d(x, y, z):
        dFx = (F(x + h, y, z)[0] - F(x - h, y, z)[0]) / (2.0 * h)
        dFy = (F(x, y + h, z)[1] - F(x, y - h, z)[1]) / (2.0 * h)
        dFz = (F(x, y, z + h)[2] - F(x, y, z - h)[2]) / (2.0 * h)
        return dFx + dFy + dFz
    return d


def curl(F, h=1e-5):
    """curl F = nabla x F   (vector field -> vector field)."""
    def c(x, y, z):
        dFz_dy = (F(x, y + h, z)[2] - F(x, y - h, z)[2]) / (2.0 * h)
        dFy_dz = (F(x, y, z + h)[1] - F(x, y, z - h)[1]) / (2.0 * h)
        dFx_dz = (F(x, y, z + h)[0] - F(x, y, z - h)[0]) / (2.0 * h)
        dFz_dx = (F(x + h, y, z)[2] - F(x - h, y, z)[2]) / (2.0 * h)
        dFy_dx = (F(x + h, y, z)[1] - F(x - h, y, z)[1]) / (2.0 * h)
        dFx_dy = (F(x, y + h, z)[0] - F(x, y - h, z)[0]) / (2.0 * h)
        return (dFz_dy - dFy_dz, dFx_dz - dFz_dx, dFy_dx - dFx_dy)
    return c


def laplacian(f, h=1e-4):
    """lap f = div grad f = d2f/dx2 + d2f/dy2 + d2f/dz2  (scalar -> scalar)."""
    def L(x, y, z):
        f0 = f(x, y, z)
        return ((f(x + h, y, z) - 2.0 * f0 + f(x - h, y, z)) / h ** 2
                + (f(x, y + h, z) - 2.0 * f0 + f(x, y - h, z)) / h ** 2
                + (f(x, y, z + h) - 2.0 * f0 + f(x, y, z - h)) / h ** 2)
    return L


def directional_derivative(f, direction, h=1e-5):
    """Rate of change of f along `direction`:  grad f . dir_hat  (scalar field)."""
    uhat = unit(direction)
    g = gradient(f, h)
    return lambda x, y, z: dot(g(x, y, z), uhat)


# --- integral theorems (numerical) -------------------------------------------

def line_integral(F, path, a, b, n=2000):
    """Work integral  ∫_a^b F(path(t)) . dl  along the curve path(t)->(x,y,z).

    Trapezoidal rule on F(path(t)) . path'(t).  For a closed loop (path(a)=path(b))
    this is the circulation, which Stokes' theorem ties to the curl flux.
    """
    hh = 1e-6

    def integrand(t):
        p_plus, p_minus = path(t + hh), path(t - hh)
        dl = tuple((p_plus[i] - p_minus[i]) / (2.0 * hh) for i in range(3))
        return dot(F(*path(t)), dl)

    dt = (b - a) / n
    total = 0.5 * (integrand(a) + integrand(b))
    for k in range(1, n):
        total += integrand(a + k * dt)
    return total * dt


def surface_flux(F, surf, u0, u1, v0, v1, nu=80, nv=80):
    """Flux  ∬ F . dS  through the parametrized surface surf(u,v)->(x,y,z),
    with dS = (r_u x r_v) du dv (midpoint rule).  For a closed surface the
    divergence theorem ties this to ∭ div F dV.
    """
    hh = 1e-6

    def integrand(u, v):
        ru = tuple((surf(u + hh, v)[i] - surf(u - hh, v)[i]) / (2.0 * hh) for i in range(3))
        rv = tuple((surf(u, v + hh)[i] - surf(u, v - hh)[i]) / (2.0 * hh) for i in range(3))
        return dot(F(*surf(u, v)), cross(ru, rv))

    du, dv = (u1 - u0) / nu, (v1 - v0) / nv
    total = 0.0
    for i in range(nu):
        for j in range(nv):
            total += integrand(u0 + (i + 0.5) * du, v0 + (j + 0.5) * dv)
    return total * du * dv


# --- demo --------------------------------------------------------------------

def _demo():
    import math
    print("MA-02 vector calculus -- demo")
    print("=" * 32)

    f = lambda x, y, z: x ** 2 + y ** 2 + z ** 2          # f = r^2
    print("f = r^2:")
    print("  grad f at (1,2,3) =", tuple(round(c, 4) for c in gradient(f)(1, 2, 3)), " (= 2r)")
    print("  lap  f everywhere =", round(laplacian(f)(1, 2, 3), 4), " (= 6)")

    F = lambda x, y, z: (-y, x, 0.0)                       # rigid rotation field
    print("\nF = (-y, x, 0):")
    print("  div  F =", round(divergence(F)(1, 1, 1), 6), " (= 0)")
    print("  curl F =", tuple(round(c, 4) for c in curl(F)(1, 1, 1)), " (= (0,0,2))")

    print("\nidentities:")
    print("  curl(grad f) =", tuple(round(c, 6) for c in curl(gradient(f))(1, 2, 1)), " (= 0)")
    G = lambda x, y, z: (x * y, y * z, z * x)
    print("  div(curl G)  =", round(divergence(curl(G))(0.7, -0.3, 0.5), 6), " (= 0)")

    print("\nintegral theorems:")
    circle = lambda t: (math.cos(t), math.sin(t), 0.0)
    circ = line_integral(F, circle, 0.0, 2 * math.pi)
    print(f"  Stokes:   circulation of (-y,x,0) round unit circle = {circ:.5f}  (= 2*pi = {2*math.pi:.5f})")
    sphere = lambda u, v: (math.sin(u) * math.cos(v), math.sin(u) * math.sin(v), math.cos(u))
    R = lambda x, y, z: (x, y, z)
    flux = surface_flux(R, sphere, 0.0, math.pi, 0.0, 2 * math.pi, 60, 60)
    print(f"  Gauss:    flux of r through unit sphere = {flux:.5f}  (= 4*pi = {4*math.pi:.5f})")


if __name__ == "__main__":
    _demo()
