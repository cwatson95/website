"""EM-05  Multipole expansion -- monopole, dipole, quadrupole; the dipole field.

Physics topic network, module EM-05 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 3.4.  Builds on ~EM-01 (exact field) and ~EM-03
(exact potential), against which the truncated expansion is checked.

The potential of a localized charge cloud, seen from far away, is a series in
1/r (Eq. 3.95):
    V(r) = (1/4 pi eps0) sum_n (1/r^(n+1)) sum_a q_a (r'_a)^n P_n(cos alpha_a),
the monopole (1/r), dipole (1/r^2), quadrupole (1/r^3), ... terms.  Each added
term cuts the far-field error by another power of (size/r).  The dipole term and
its field (Eq. 3.99, 3.103-3.104) dominate any neutral object.
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

from electrostatics import EPS0, K_E, coulomb_field      # noqa: E402
from electric_potential import potential_point_charges   # noqa: E402
from vector_algebra import dot, norm, unit               # noqa: E402

__all__ = [
    "monopole_moment", "dipole_moment", "quadrupole_moment",
    "dipole_potential", "dipole_field", "multipole_potential",
]


# --- the moments (Sect. 3.4.2) -----------------------------------------------

def monopole_moment(charges):
    """Total charge  Q = sum q_a  (the n=0 / monopole moment)."""
    return sum(q for (q, _) in charges)


def dipole_moment(charges):
    """Electric dipole moment  p = sum q_a r'_a  (vector, Eq. 3.98).
    Origin-independent only for a neutral system (Q = 0)."""
    px = sum(q * r[0] for (q, r) in charges)
    py = sum(q * r[1] for (q, r) in charges)
    pz = sum(q * r[2] for (q, r) in charges)
    return (px, py, pz)


def quadrupole_moment(charges):
    """Traceless quadrupole tensor  Q_ij = sum q_a (3 r_i r_j - r^2 delta_ij).
    Returned as a 3x3 list of lists."""
    Q = [[0.0] * 3 for _ in range(3)]
    for (q, r) in charges:
        r2 = dot(r, r)
        for i in range(3):
            for j in range(3):
                Q[i][j] += q * (3.0 * r[i] * r[j] - (r2 if i == j else 0.0))
    return Q


# --- dipole potential and field (Eq. 3.99, 3.104) ----------------------------

def dipole_potential(p, source=(0.0, 0.0, 0.0)):
    """Potential of a pure dipole p at `source` (Eq. 3.99):
        V = (1/4 pi eps0) p . rhat / r^2 ."""
    sx, sy, sz = source

    def V(x, y, z):
        rv = (x - sx, y - sy, z - sz)
        r = norm(rv)
        if r == 0.0:
            return math.inf
        return K_E * dot(p, rv) / r ** 3                    # p.rhat/r^2 = p.r/r^3
    return V


def dipole_field(p, source=(0.0, 0.0, 0.0)):
    """Field of a pure dipole (Eq. 3.104):
        E = (1/4 pi eps0) (1/r^3) [ 3 (p.rhat) rhat - p ].
    On the axis E = 2 k p / r^3 (along p); on the bisector E = - k p / r^3."""
    sx, sy, sz = source

    def E(x, y, z):
        rv = (x - sx, y - sy, z - sz)
        r = norm(rv)
        if r == 0.0:
            return (math.inf, math.inf, math.inf)
        rh = unit(rv)
        pr = dot(p, rh)
        c = K_E / r ** 3
        return tuple(c * (3.0 * pr * rh[i] - p[i]) for i in range(3))
    return E


# --- the truncated expansion (Eq. 3.95) --------------------------------------

def _legendre(n, u):
    """P_n(u) for n = 0,1,2 (all we need for monopole/dipole/quadrupole)."""
    if n == 0:
        return 1.0
    if n == 1:
        return u
    return 0.5 * (3.0 * u * u - 1.0)


def multipole_potential(charges, lmax=1):
    """Approximate far-field potential keeping terms up to order lmax (Eq. 3.95).

    lmax = 0 monopole, 1 + dipole, 2 + quadrupole.  Converges to the exact
    ~EM-03 potential as r grows; each term adds one power of (size/r) accuracy.
    """
    def V(x, y, z):
        rv = (x, y, z)
        r = norm(rv)
        if r == 0.0:
            return math.inf
        rh = unit(rv)
        total = 0.0
        for n in range(lmax + 1):
            term = 0.0
            for (q, rp) in charges:
                rpn = norm(rp)
                cos_a = dot(rp, rh) / rpn if rpn > 0 else 1.0
                term += q * (rpn ** n) * _legendre(n, cos_a)
            total += term / r ** (n + 1)
        return K_E * total
    return V


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-05 multipole expansion -- demo")
    print("=" * 34)

    # a physical dipole: +q at +a/2 z, -q at -a/2 z  ->  p = q a zhat
    q, a = 1e-9, 0.01
    dip = [(q, (0, 0, a / 2)), (-q, (0, 0, -a / 2))]
    print("physical dipole (+q,-q):")
    print(f"  monopole Q = {monopole_moment(dip):.2e} C   (= 0, neutral)")
    print(f"  dipole   p = {tuple(round(c, 13) for c in dipole_moment(dip))} C m   (= q a zhat = {q*a:.2e})")

    p = dipole_moment(dip)
    Vexact = potential_point_charges(dip)
    print("\nexpansion vs exact potential, on the axis:")
    print(f"{'r/a':>8} {'monopole':>12} {'+dipole':>12} {'exact':>12}")
    for rr in (5 * a, 20 * a, 100 * a):
        Vm = multipole_potential(dip, lmax=0)(0, 0, rr)
        Vd = multipole_potential(dip, lmax=1)(0, 0, rr)
        Ve = Vexact(0, 0, rr)
        print(f"{rr/a:8.0f} {Vm:12.4e} {Vd:12.4e} {Ve:12.4e}")

    print("\ndipole field structure (p along z):")
    Edip = dipole_field(p)
    z = 0.1
    print(f"  on axis  (0,0,{z}):  E_z = {Edip(0,0,z)[2]:.4e}  (= 2kp/r^3 = {2*K_E*norm(p)/z**3:.4e})")
    print(f"  bisector ({z},0,0): E_z = {Edip(z,0,0)[2]:.4e}  (= -kp/r^3 = {-K_E*norm(p)/z**3:.4e})")


if __name__ == "__main__":
    _demo()
