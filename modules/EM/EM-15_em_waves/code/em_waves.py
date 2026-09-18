"""EM-15  Electromagnetic waves -- propagation, polarization, reflection.

Physics topic network, module EM-15 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 9.1-9.4.  Builds on ~EM-01/~EM-08 (EPS0, MU0 -> c),
~MA-01 (cross) and ~MA-02 (laplacian for the wave equation).  Companion to
~EM-13: a plane wave is the vacuum solution of Maxwell's equations.

A wave obeys  d^2 f / dt^2 = v^2 grad^2 f  (Eq. 9.2), so omega = v k.  An EM plane
wave is transverse with B locked to E (Eq. 9.49):  B = (1/v) khat x E,  |B| = |E|/v.
In a linear medium v = c/n with n = sqrt(eps_r mu_r) (Eq. 9.68); at a normal
interface the amplitudes split by the Fresnel coefficients (Eq. 9.82) with
reflectance + transmittance = 1.
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
from vector_algebra import cross, dot, norm, unit            # noqa: E402
from vector_calculus import laplacian                        # noqa: E402

C = 1.0 / math.sqrt(MU0 * EPS0)

__all__ = [
    "C", "refractive_index", "phase_velocity", "wavelength",
    "transverse_B", "is_transverse",
    "fresnel_normal", "reflectance", "transmittance",
    "scalar_plane_wave", "wave_equation_residual", "classify_polarization",
]


# --- dispersion and media (Eq. 9.2, 9.68) ------------------------------------

def refractive_index(eps_r, mu_r=1.0):
    """Index of refraction  n = sqrt(eps_r mu_r)  (Eq. 9.68)."""
    return math.sqrt(eps_r * mu_r)


def phase_velocity(eps_r, mu_r=1.0):
    """Phase velocity in a linear medium  v = c / n."""
    return C / refractive_index(eps_r, mu_r)


def wavelength(omega, v=C):
    """Wavelength from angular frequency and speed:  lambda = 2 pi v / omega."""
    return 2.0 * math.pi * v / omega


# --- transverse structure: B from E (Eq. 9.49) -------------------------------

def transverse_B(E0, khat, v=C):
    """Magnetic amplitude of a plane wave:  B0 = (1/v) khat x E0  (Eq. 9.49).
    Perpendicular to both E0 and the propagation direction, with |B0| = |E0|/v."""
    kh = unit(khat)
    return tuple(c / v for c in cross(kh, E0))


def is_transverse(vec, khat, tol=1e-9):
    """True if `vec` is perpendicular to the propagation direction (vec . khat = 0)."""
    return abs(dot(vec, unit(khat))) <= tol * (norm(vec) + 1e-30)


# --- reflection & transmission at normal incidence (Eq. 9.82) ----------------

def fresnel_normal(n1, n2):
    """Amplitude reflection/transmission coefficients at normal incidence
    (non-magnetic media):  r = (n1 - n2)/(n1 + n2),  t = 2 n1/(n1 + n2)."""
    r = (n1 - n2) / (n1 + n2)
    t = 2.0 * n1 / (n1 + n2)
    return r, t


def reflectance(n1, n2):
    """Fraction of incident power reflected:  R = r^2."""
    r, _ = fresnel_normal(n1, n2)
    return r * r


def transmittance(n1, n2):
    """Fraction of incident power transmitted:  T = (n2/n1) t^2 = 1 - R."""
    _, t = fresnel_normal(n1, n2)
    return (n2 / n1) * t * t


# --- the wave equation (Eq. 9.2) ---------------------------------------------

def scalar_plane_wave(k, omega):
    """A scalar plane wave f(x,y,z,t) = cos(k z - omega t) travelling +z."""
    return lambda x, y, z, t: math.cos(k * z - omega * t)


def wave_equation_residual(f, v, x, y, z, t, dt=1e-6):
    """Normalized residual of  d^2 f/dt^2 - v^2 grad^2 f  (Eq. 9.2), ~0 for a wave
    with omega = v k.  Uses MA-02 laplacian (space) + central difference (time)."""
    snap = lambda xx, yy, zz: f(xx, yy, zz, t)
    lap = laplacian(snap)(x, y, z)
    ftt = (f(x, y, z, t + dt) - 2.0 * f(x, y, z, t) + f(x, y, z, t - dt)) / dt ** 2
    scale = max(abs(ftt), abs(v ** 2 * lap)) + 1e-300
    return (ftt - v ** 2 * lap) / scale


# --- polarization (Sect. 9.1.4) ----------------------------------------------

def classify_polarization(Ax, Ay, delta, tol=1e-9):
    """Classify the polarization of a wave with x,y amplitudes Ax,Ay and phase
    difference delta (= phase_y - phase_x):
      linear if delta = 0 or pi (or a zero amplitude),
      circular if Ax = Ay and delta = +/- pi/2,
      elliptical otherwise."""
    if abs(Ax) < tol or abs(Ay) < tol:
        return "linear"
    s = math.sin(delta)
    if abs(s) < tol:
        return "linear"                                   # delta = 0 or pi
    if abs(Ax - Ay) < tol and abs(abs(delta) - math.pi / 2) < tol:
        return "circular"
    return "elliptical"


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-15 electromagnetic waves -- demo")
    print("=" * 36)

    # transverse structure of a +z wave with E along x
    E0 = (1000.0, 0.0, 0.0)
    khat = (0.0, 0.0, 1.0)
    B0 = transverse_B(E0, khat)
    print(f"E0 = {E0} V/m along x, propagation +z:")
    print(f"  B0 = (1/c) khat x E0 = {tuple(f'{c:.3e}' for c in B0)} T (along +y)")
    print(f"  |B0| = {norm(B0):.4e} = |E0|/c = {norm(E0)/C:.4e};  E.k = {dot(E0,khat)}, B.k = {dot(B0,khat)} (transverse)")

    # a medium
    eps_r = 2.25                                          # glass, n = 1.5
    print(f"\nlinear medium eps_r={eps_r}: n = {refractive_index(eps_r):.3f}, v = c/n = {phase_velocity(eps_r):.4e} m/s")

    # normal-incidence reflection air (n=1) -> glass (n=1.5)
    n1, n2 = 1.0, 1.5
    r, t = fresnel_normal(n1, n2)
    R, T = reflectance(n1, n2), transmittance(n1, n2)
    print(f"\nair->glass normal incidence: r={r:.4f}, t={t:.4f}")
    print(f"  R = {R:.4f}, T = {T:.4f}, R+T = {R+T:.6f}  (~4% reflected)")

    # wave equation residual
    k, v = 1.0, 1.0
    f = scalar_plane_wave(k, v * k)
    res = wave_equation_residual(f, v, 0.1, 0.2, 0.3, 0.4)
    print(f"\nwave-equation residual for omega=vk: {res:.2e} (-> 0)")

    # polarization
    print("\npolarization:")
    print(f"  Ax=1, Ay=1, delta=pi/2 : {classify_polarization(1, 1, math.pi/2)}")
    print(f"  Ax=1, Ay=1, delta=0    : {classify_polarization(1, 1, 0.0)}")
    print(f"  Ax=2, Ay=1, delta=pi/2 : {classify_polarization(2, 1, math.pi/2)}")


if __name__ == "__main__":
    _demo()
