"""
CM-25  Waves in continuous media -- the wave equation on a string, normal modes,
and phase vs group velocity in dispersive media.

Part of the physics topic network (modules/topic_network.txt, module CM-25).
Reuses ~MA-08 (`wave_1d`, `wave_mode`) for the PDE; the modes connect to ~MA-09
(Fourier). Links to ~EM-15 (EM waves) and ~CM-15/~CM-16 (the discrete oscillator
limit).

A string of tension T and linear density mu carries transverse waves at speed
c = sqrt(T/mu), governed by  y_tt = c^2 y_xx.  The medium is *dispersive* when
omega depends nonlinearly on k, so phase velocity omega/k and group velocity
domega/dk differ.

NOTE: MA-08 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA08 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-08_pde", "code"))
if _MA08 not in sys.path:
    sys.path.insert(0, _MA08)

from pde import wave_1d, wave_mode  # noqa: E402

__all__ = [
    "wave_speed", "string_mode_frequency", "string_wavelength",
    "phase_velocity", "group_velocity", "nondispersive", "klein_gordon",
]


def wave_speed(tension, mu):
    """Transverse wave speed on a string:  c = sqrt(T/mu)."""
    return math.sqrt(tension / mu)


def string_mode_frequency(n, c, L):
    """nth normal-mode frequency of a string fixed at both ends:  f_n = n c / (2 L)."""
    return n * c / (2.0 * L)


def string_wavelength(n, L):
    """nth-mode wavelength:  lambda_n = 2 L / n."""
    return 2.0 * L / n


def phase_velocity(omega, k):
    """Phase velocity  v_p = omega / k."""
    return omega / k


def group_velocity(omega_of_k, k, dk=1e-6):
    """Group velocity  v_g = d omega / dk  (numerical)."""
    return (omega_of_k(k + dk) - omega_of_k(k - dk)) / (2.0 * dk)


def nondispersive(c):
    """A non-dispersive medium:  omega(k) = c k."""
    return lambda k: c * k


def klein_gordon(c, omega0):
    """A dispersive medium:  omega(k) = sqrt(c^2 k^2 + omega0^2)  (plasma / Klein-Gordon)."""
    return lambda k: math.sqrt(c * c * k * k + omega0 * omega0)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-25 waves in continuous media -- demo")
    print("=" * 32)
    c = wave_speed(100.0, 0.01)
    print(f"wave speed sqrt(T/mu) for T=100, mu=0.01: c = {c}")
    print(f"string modes (c={c}, L=1): f_1={string_mode_frequency(1, c, 1)}, f_2={string_mode_frequency(2, c, 1)}")

    print("\nnon-dispersive omega=c k (c=2): v_p =", phase_velocity(nondispersive(2.0)(3.0), 3.0),
          " v_g =", round(group_velocity(nondispersive(2.0), 3.0), 6), " (both = c)")

    kg = klein_gordon(2.0, 1.0)
    k = 1.0
    vp, vg = phase_velocity(kg(k), k), group_velocity(kg, k)
    print(f"dispersive (Klein-Gordon, c=2, omega0=1) at k=1: v_p={vp:.4f} (>c), v_g={vg:.4f} (<c), v_p*v_g={vp * vg:.4f} (=c^2)")


if __name__ == "__main__":
    _demo()
