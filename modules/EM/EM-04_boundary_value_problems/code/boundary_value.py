"""EM-04  Boundary-value problems -- images, separation of variables, uniqueness.

Physics topic network, module EM-04 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 3.1-3.3.  Builds on ~EM-01 / ~EM-03 (fields and
potentials) and ~MA-08 (the Laplace PDE).

Three ways to solve grad^2 V = 0 with boundary data:
  1. Method of images (Sect. 3.2): replace a grounded conductor by image charges
     that reproduce its boundary condition.  Classic: a point charge q a height d
     above a grounded plane -> image -q at -d.
  2. Separation of variables (Sect. 3.3): the semi-infinite slot, solved as a
     Fourier sine series and summed in closed form (Eq. 3.36).
  3. Relaxation: iterate the discrete Laplace equation to the unique solution
     fixed by the boundary -- a numerical demonstration of the uniqueness theorem
     (Sect. 3.1.5).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM01 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-01_electrostatics", "code"))
_EM03 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-03_electric_potential", "code"))
for _p in (_EM01, _EM03):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from electrostatics import EPS0, K_E, coulomb_field                      # noqa: E402
from electric_potential import potential_point_charges                   # noqa: E402

__all__ = [
    "image_potential_plane", "image_field_plane", "induced_surface_charge",
    "total_induced_charge", "image_force",
    "slot_potential_series", "slot_potential_closed",
    "solve_laplace_2d",
]


# --- 1. method of images: charge q at height d over a grounded plane z=0 ------

def image_potential_plane(q, d):
    """Potential for z > 0 of charge q at (0,0,d) above a grounded plane z=0,
    built from the real charge plus image -q at (0,0,-d).  V = 0 on the plane."""
    return potential_point_charges([(q, (0.0, 0.0, d)), (-q, (0.0, 0.0, -d))])


def image_field_plane(q, d):
    """The corresponding field (real + image charge), valid in z > 0."""
    return coulomb_field([(q, (0.0, 0.0, d)), (-q, (0.0, 0.0, -d))])


def induced_surface_charge(q, d):
    """Induced surface density on the plane (Eq. 3.10):
        sigma(x,y) = - q d / (2 pi (x^2 + y^2 + d^2)^(3/2))."""
    def sigma(x, y):
        return -q * d / (2.0 * math.pi * (x * x + y * y + d * d) ** 1.5)
    return sigma


def total_induced_charge(q, d, R=200.0, n=400):
    """Integral of sigma over the plane -- equals -q (Eq. 3.10 result).
    Midpoint quadrature in polar coordinates out to radius R*d."""
    sigma = induced_surface_charge(q, d)
    rmax = R * d
    dr = rmax / n
    total = 0.0
    for i in range(n):
        s = (i + 0.5) * dr                                  # cylindrical radius
        total += sigma(s, 0.0) * (2.0 * math.pi * s) * dr   # ring area 2 pi s dr
    return total


def image_force(q, d):
    """Attractive force on q toward the plane (Eq. 3.12):
        F = - (1/4 pi eps0) q^2 / (2 d)^2   (negative = toward the conductor)."""
    return -K_E * q * q / (2.0 * d) ** 2


# --- 2. separation of variables: the semi-infinite slot (Sect. 3.3.1) --------

def slot_potential_series(V0, a, N=200):
    """Fourier-series solution for a slot: grounded plates at y=0 and y=a, the
    end strip x=0 held at V0, slot extending to x>0 (Eq. 3.34/3.35):
        V(x,y) = (4 V0 / pi) sum_{n odd} (1/n) exp(-n pi x / a) sin(n pi y / a).
    """
    def V(x, y):
        s = 0.0
        for n in range(1, N + 1, 2):                        # odd n only
            s += math.exp(-n * math.pi * x / a) * math.sin(n * math.pi * y / a) / n
        return 4.0 * V0 / math.pi * s
    return V


def slot_potential_closed(V0, a):
    """Closed-form sum of the same series (Griffiths Eq. 3.36):
        V(x,y) = (2 V0 / pi) arctan( sin(pi y / a) / sinh(pi x / a) )."""
    def V(x, y):
        denom = math.sinh(math.pi * x / a)
        if denom == 0.0:
            return V0 if 0.0 < y < a else 0.0
        return (2.0 * V0 / math.pi) * math.atan2(math.sin(math.pi * y / a), denom)
    return V


# --- 3. relaxation: the uniqueness theorem, numerically (Sect. 3.1.5) ---------

def solve_laplace_2d(bc, nx=41, ny=41, Lx=1.0, Ly=1.0, tol=1e-8, max_iter=20000):
    """Solve grad^2 V = 0 on a grid by Gauss-Seidel relaxation.

    `bc(x, y)` supplies Dirichlet values on the boundary.  Interior values are
    irrelevant to the answer -- the iteration converges to the ONE potential the
    boundary allows (uniqueness theorem).  Returns (grid, xs, ys).
    """
    xs = [Lx * i / (nx - 1) for i in range(nx)]
    ys = [Ly * j / (ny - 1) for j in range(ny)]
    V = [[0.0] * ny for _ in range(nx)]
    for i in range(nx):                                     # set boundary, zero interior
        for j in range(ny):
            if i in (0, nx - 1) or j in (0, ny - 1):
                V[i][j] = bc(xs[i], ys[j])
    for _ in range(max_iter):
        worst = 0.0
        for i in range(1, nx - 1):
            for j in range(1, ny - 1):
                new = 0.25 * (V[i + 1][j] + V[i - 1][j] + V[i][j + 1] + V[i][j - 1])
                worst = max(worst, abs(new - V[i][j]))
                V[i][j] = new
        if worst < tol:
            break
    return V, xs, ys


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-04 boundary-value problems -- demo")
    print("=" * 38)

    q, d = 1e-9, 0.1
    V = image_potential_plane(q, d)
    print("image charge: q=1 nC at d=0.1 m over a grounded plane")
    print(f"  V on the plane (z=0)      = {V(0.05, 0.03, 0.0):.3e} V   (= 0, grounded)")
    print(f"  total induced charge      = {total_induced_charge(q, d):.4e} C  (= -q = {-q:.1e})")
    print(f"  image force on q          = {image_force(q, d):.4e} N  (attractive, toward plane)")

    print("\nseparation of variables: semi-infinite slot, V0=10 V, a=1")
    Vs, Vc = slot_potential_series(10.0, 1.0), slot_potential_closed(10.0, 1.0)
    for (x, y) in [(0.3, 0.5), (0.5, 0.25), (0.8, 0.7)]:
        print(f"  V({x},{y}): series = {Vs(x, y):.5f}   closed form = {Vc(x, y):.5f}")

    print("\nuniqueness via relaxation: box with V = V0 x/L on the boundary")
    grid, xs, ys = solve_laplace_2d(lambda x, y: 10.0 * x, nx=21, ny=21)
    i, j = 13, 7
    print(f"  V({xs[i]:.2f},{ys[j]:.2f}) relaxed = {grid[i][j]:.5f}   analytic 10*x = {10.0*xs[i]:.5f}")


if __name__ == "__main__":
    _demo()
