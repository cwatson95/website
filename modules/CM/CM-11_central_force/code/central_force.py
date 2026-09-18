"""
CM-11  Central-force motion -- the effective potential, circular orbits, Kepler's
laws, and the two-body reduction.

Part of the physics topic network (modules/topic_network.txt, module CM-11).
Reuses ~CM-07 (`reduced_mass`) and ~MA-07 (the integrator); builds on ~CM-05
(potential) and ~CM-09 (conserved L); links to ~QM-12 (hydrogen atom) and
~RE-14 (Schwarzschild orbits).

A central force depends only on r and points along r-hat. Conserving angular
momentum L confines motion to a plane and reduces it to a 1-D radial problem in
the effective potential U_eff(r) = U(r) + L^2/(2 mu r^2).

NOTE: CM-07/MA-07 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CM07 = os.path.abspath(os.path.join(_HERE, "..", "..", "CM-07_centre_of_mass", "code"))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
for _p in (_CM07, _MA07):
    if _p not in sys.path:
        sys.path.insert(0, _p)

from centre_of_mass import reduced_mass  # noqa: E402
from ode import integrate                # noqa: E402

__all__ = [
    "effective_potential", "kepler_potential", "kepler_force",
    "circular_orbit_radius", "kepler_period", "orbit", "reduced_mass",
]


def effective_potential(U, L, mu):
    """U_eff(r) = U(r) + L^2 / (2 mu r^2)  (the centrifugal barrier added to U)."""
    return lambda r: U(r) + L * L / (2.0 * mu * r * r)


def kepler_potential(k):
    """Attractive inverse-square potential  U(r) = -k/r  (k > 0)."""
    return lambda r: -k / r


def kepler_force(k):
    """Radial force of U=-k/r:  F_r(r) = -k/r^2  (negative = attractive)."""
    return lambda r: -k / (r * r)


def circular_orbit_radius(L, mu, k):
    """Radius of the circular orbit for U=-k/r (minimum of U_eff): r0 = L^2/(mu k)."""
    return L * L / (mu * k)


def kepler_period(a, mu, k):
    """Kepler's third law for U=-k/r:  T = 2 pi sqrt(mu a^3 / k)  (so T^2 ∝ a^3)."""
    return 2.0 * math.pi * math.sqrt(mu * a ** 3 / k)


def orbit(force_radial, mu, r0, v0, t0, t1, n):
    """Integrate planar motion of the reduced particle under a central force, with
    radial force magnitude force_radial(r) (signed). r0, v0 are 2-vectors (x, y).
    Returns (ts, states) with each state [x, y, vx, vy]. Uses MA-07's `integrate`."""
    def rhs(t, y):
        x, yy, vx, vy = y
        r = math.hypot(x, yy)
        Fr = force_radial(r)
        return [vx, vy, Fr * x / r / mu, Fr * yy / r / mu]
    return integrate(rhs, [r0[0], r0[1], v0[0], v0[1]], t0, t1, n)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-11 central-force motion -- demo")
    print("=" * 32)
    mu, k, L = 1.0, 1.0, 1.0
    r0 = circular_orbit_radius(L, mu, k)
    print(f"circular orbit: r0 = L^2/(mu k) = {r0}")
    Ueff = effective_potential(kepler_potential(k), L, mu)
    print(f"  U_eff'(r0) = {(Ueff(r0 + 1e-6) - Ueff(r0 - 1e-6)) / 2e-6:.2e}  (~0, a minimum)")
    print(f"  Kepler period T(a=r0) = {kepler_period(r0, mu, k):.4f}")

    # integrate the circular orbit: |r| should stay = r0
    vc = L / (mu * r0)                                 # tangential speed for the circular orbit
    ts, ys = orbit(kepler_force(k), mu, (r0, 0.0), (0.0, vc), 0.0, kepler_period(r0, mu, k), 4000)
    radii = [math.hypot(s[0], s[1]) for s in ys]
    print(f"  integrated circular orbit: r in [{min(radii):.4f}, {max(radii):.4f}]  (= {r0})")

    # Kepler III for two circular orbits
    for a in (1.0, 4.0):
        print(f"  a={a}: T^2/a^3 = {kepler_period(a, mu, k) ** 2 / a ** 3:.4f}")


if __name__ == "__main__":
    _demo()
