"""EM-11  Electromagnetic induction -- Faraday's & Lenz's laws, inductance.

Physics topic network, module EM-11 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 7.1-7.2.  Builds on ~EM-08 (B fields, MU0) and
~MA-02 (surface_flux for the magnetic flux).

A changing magnetic flux drives an EMF (Faraday's law, Eq. 7.x):
    EMF = - d(Phi)/dt ,        Phi = int B . da ,        curl E = - dB/dt (Eq. 7.18)
the minus sign being Lenz's law (the induced current opposes the change).  Flux
linkage defines inductance Phi = L I (Eq. 7.27-7.28), and a current-carrying coil
stores W = (1/2) L I^2 = (1/2 mu0) int B^2 dtau (Eq. 7.34-7.35) -- the same energy
seen in the charges or in the field, as in ~EM-06.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM08 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-08_magnetostatics", "code"))
if _EM08 not in sys.path:
    sys.path.insert(0, _EM08)

from magnetostatics import MU0                              # noqa: E402
from vector_calculus import surface_flux                    # noqa: E402

__all__ = [
    "flat_loop_surface", "magnetic_flux", "faraday_emf", "lenz_sign",
    "motional_emf", "solenoid_inductance", "mutual_inductance_solenoids",
    "energy_in_inductor", "magnetic_energy_density", "magnetic_field_energy_solenoid",
]


# --- magnetic flux and Faraday's law (Eq. 7.x) -------------------------------

def flat_loop_surface(x0, x1, y0, y1, z=0.0):
    """Parametrization S(u,v) of a flat rectangular loop in the plane z=const,
    oriented +z (for feeding MA-02 surface_flux)."""
    def S(u, v):
        return (x0 + u * (x1 - x0), y0 + v * (y1 - y0), z)
    return S


def magnetic_flux(B, surf, n=60):
    """Phi = int B . da through the parametrized surface surf(u,v), u,v in [0,1].
    Reuses MA-02 surface_flux."""
    return surface_flux(B, surf, 0.0, 1.0, 0.0, 1.0, n, n)


def faraday_emf(flux_of_t, t, dt=1e-6):
    """Induced EMF = - d(Phi)/dt at time t (central difference of flux_of_t)."""
    return -(flux_of_t(t + dt) - flux_of_t(t - dt)) / (2.0 * dt)


def lenz_sign(dflux_dt):
    """Sign of the induced EMF/current relative to the loop's positive sense:
    opposite to the change in flux (Lenz).  Returns -1, 0, or +1."""
    if dflux_dt > 0:
        return -1
    if dflux_dt < 0:
        return +1
    return 0


def motional_emf(B, v, length):
    """EMF of a rod of length L moving at speed v perpendicular to a uniform field
    B (all mutually perpendicular):  EMF = B v L  (Eq. 7.13)."""
    return B * v * length


# --- inductance (Eq. 7.27-7.28) ----------------------------------------------

def solenoid_inductance(N, area, length):
    """Self-inductance of a long solenoid, N turns, cross-section A, length l:
        L = mu0 N^2 A / l   (Eq. 7.27)."""
    return MU0 * N * N * area / length


def mutual_inductance_solenoids(N1, N2, area, length):
    """Mutual inductance of two coaxial solenoids sharing A and l:
        M = mu0 N1 N2 A / l.  Symmetric: M_12 = M_21 (Eq. 7.24)."""
    return MU0 * N1 * N2 * area / length


# --- energy in the magnetic field (Eq. 7.34-7.35) ----------------------------

def energy_in_inductor(L, I):
    """Energy stored in an inductor:  W = (1/2) L I^2  (Eq. 7.34)."""
    return 0.5 * L * I * I


def magnetic_energy_density(B):
    """Energy density in the magnetic field:  u = |B|^2 / (2 mu0)  (Eq. 7.35),
    as a scalar field from a field function B."""
    def u(x, y, z):
        bx, by, bz = B(x, y, z)
        return (bx * bx + by * by + bz * bz) / (2.0 * MU0)
    return u


def magnetic_field_energy_solenoid(N, area, length, I):
    """Field energy of a solenoid by (1/2 mu0) int B^2 dtau, with B = mu0 N I / l
    uniform inside and ~0 outside.  Equals (1/2) L I^2 (the EM-06 two-pictures check)."""
    B_inside = MU0 * N * I / length
    volume = area * length
    return (B_inside ** 2) / (2.0 * MU0) * volume


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-11 electromagnetic induction -- demo")
    print("=" * 40)

    # Faraday: a loop of area A in a sinusoidally varying uniform field B(t) = B0 sin(wt) zhat
    A, B0, w = 0.01, 0.5, 100.0
    flux = lambda t: B0 * math.sin(w * t) * A          # Phi(t) = B0 A sin(wt)
    print("loop A=0.01 m^2 in B(t)=0.5 sin(100 t) zhat:")
    for t in (0.0, 0.005, 0.01):
        emf = faraday_emf(flux, t)
        exact = -B0 * A * w * math.cos(w * t)
        print(f"  t={t}: EMF = {emf:+.5e} V   (-B0 A w cos wt = {exact:+.5e})")

    # motional EMF
    print(f"\nmotional EMF (B=0.3 T, v=2 m/s, L=0.5 m): {motional_emf(0.3, 2.0, 0.5):.4f} V")

    # solenoid inductance and the two energy pictures
    N, area, length, I = 1000, 1e-4, 0.2, 3.0
    L = solenoid_inductance(N, area, length)
    print(f"\nsolenoid N={N}, A={area} m^2, l={length} m:")
    print(f"  L = mu0 N^2 A / l       = {L:.4e} H")
    print(f"  W = (1/2) L I^2         = {energy_in_inductor(L, I):.4e} J")
    print(f"  W = (1/2mu0) int B^2 dV = {magnetic_field_energy_solenoid(N, area, length, I):.4e} J  (agree)")


if __name__ == "__main__":
    _demo()
