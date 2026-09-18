"""EM-16  Waveguides, cavities & transmission lines.

Physics topic network, module EM-16 (modules/topic_network.txt).
Source: Griffiths 4e, Sect. 9.5.  Builds on ~EM-15 (the free-space wave, speed c).

Confining a wave to a hollow conductor quantizes its transverse profile into modes
(m, n), each with a cutoff frequency below which it cannot propagate (Eq. 9.186):
    w_mn = c pi sqrt((m/a)^2 + (n/b)^2).
Above cutoff the guide wavenumber is k = (1/c) sqrt(w^2 - w_mn^2); the wave is
dispersive, with
    v_phase = c / sqrt(1 - (w_mn/w)^2) > c ,   v_group = c sqrt(1 - (w_mn/w)^2) < c ,
and  v_phase * v_group = c^2.  A coaxial (TEM) line has no cutoff -- it carries
every frequency at c, the basis of the transmission line (Sect. 9.5.3).
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_EM15 = os.path.abspath(os.path.join(_HERE, "..", "..", "EM-15_em_waves", "code"))
if _EM15 not in sys.path:
    sys.path.insert(0, _EM15)

from em_waves import C                                      # noqa: E402

__all__ = [
    "C", "cutoff_angular_frequency", "cutoff_frequency", "dominant_mode_cutoff",
    "is_propagating", "guide_wavenumber", "evanescent_decay",
    "phase_velocity_guide", "group_velocity_guide", "tem_line_speed",
]


# --- rectangular guide cutoffs (Eq. 9.186) -----------------------------------

def cutoff_angular_frequency(m, n, a, b):
    """Cutoff angular frequency of the TE_mn / TM_mn mode of an a x b guide:
        w_mn = c pi sqrt((m/a)^2 + (n/b)^2)."""
    return C * math.pi * math.sqrt((m / a) ** 2 + (n / b) ** 2)


def cutoff_frequency(m, n, a, b):
    """Cutoff in ordinary frequency  f_mn = w_mn / 2 pi (Hz)."""
    return cutoff_angular_frequency(m, n, a, b) / (2.0 * math.pi)


def dominant_mode_cutoff(a, b):
    """Lowest cutoff of a rectangular guide (the dominant TE10 mode, a >= b):
        w_10 = c pi / a."""
    a, b = max(a, b), min(a, b)
    return cutoff_angular_frequency(1, 0, a, b)


# --- dispersion above / below cutoff -----------------------------------------

def is_propagating(omega, m, n, a, b):
    """True iff the drive frequency exceeds the mode cutoff (mode propagates)."""
    return omega > cutoff_angular_frequency(m, n, a, b)


def guide_wavenumber(omega, omega_co):
    """Longitudinal wavenumber  k = (1/c) sqrt(w^2 - w_co^2)  for w > w_co
    (propagating).  Returns 0.0 at/below cutoff (use `evanescent_decay` there)."""
    if omega <= omega_co:
        return 0.0
    return math.sqrt(omega ** 2 - omega_co ** 2) / C


def evanescent_decay(omega, omega_co):
    """Below cutoff the mode is evanescent, ~ e^{-kappa z} with
        kappa = (1/c) sqrt(w_co^2 - w^2)  (w < w_co)."""
    if omega >= omega_co:
        return 0.0
    return math.sqrt(omega_co ** 2 - omega ** 2) / C


def phase_velocity_guide(omega, omega_co):
    """Phase velocity in the guide  v_p = c / sqrt(1 - (w_co/w)^2)  (> c)."""
    return C / math.sqrt(1.0 - (omega_co / omega) ** 2)


def group_velocity_guide(omega, omega_co):
    """Group (energy/signal) velocity  v_g = c sqrt(1 - (w_co/w)^2)  (< c).
    Note v_p * v_g = c^2."""
    return C * math.sqrt(1.0 - (omega_co / omega) ** 2)


def tem_line_speed():
    """A TEM transmission line (e.g. coax) has no cutoff: every frequency
    propagates at c (in vacuum dielectric).  Sect. 9.5.3."""
    return C


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-16 waveguides & transmission lines -- demo")
    print("=" * 46)

    a, b = 0.0229, 0.0102        # WR-90 X-band guide, metres
    print(f"rectangular guide a={a*1e3:.1f} mm, b={b*1e3:.1f} mm:")
    for (m, n) in [(1, 0), (2, 0), (0, 1), (1, 1)]:
        f = cutoff_frequency(m, n, a, b)
        print(f"  TE{m}{n}: f_cutoff = {f/1e9:.3f} GHz")
    print(f"  dominant mode cutoff w_10 = {dominant_mode_cutoff(a,b):.4e} rad/s")

    # operate the dominant mode above cutoff
    w_co = cutoff_angular_frequency(1, 0, a, b)
    w = 1.5 * w_co
    k = guide_wavenumber(w, w_co)
    vp = phase_velocity_guide(w, w_co)
    vg = group_velocity_guide(w, w_co)
    print(f"\ndriving TE10 at w = 1.5 w_co:")
    print(f"  guide wavenumber k = {k:.4f} rad/m")
    print(f"  v_phase = {vp:.4e} m/s (> c),  v_group = {vg:.4e} m/s (< c)")
    print(f"  v_phase * v_group = {vp*vg:.6e}  (= c^2 = {C**2:.6e})")

    # below cutoff: evanescent
    w_below = 0.5 * w_co
    print(f"\ndriving at w = 0.5 w_co (below cutoff): does not propagate;")
    print(f"  evanescent decay kappa = {evanescent_decay(w_below, w_co):.4f} 1/m")

    print(f"\nTEM coax line: no cutoff, speed = {tem_line_speed():.4e} m/s = c (all frequencies)")


if __name__ == "__main__":
    _demo()
