"""EM-12  AC circuits & the driven RLC -- impedance, resonance, Q.

Physics topic network, module EM-12 (modules/topic_network.txt).
Source: Griffiths 4e, Ch. 7 (EMF & inductance, Sect. 7.1-7.2); the steady-state
AC method (complex impedance) is the ~MA-05/~MA-06 complex-exponential technique,
and the driven RLC is the electrical twin of the ~CM-15 driven oscillator
(KEY BRIDGE: same equation L q'' + R q' + q/C = V0 cos(wt)).

Drive everything at frequency w with phasors (V -> V0 e^{iwt}); a passive element
has a complex impedance Z (Ohm's law V = I Z):
    Z_R = R ,   Z_L = i w L ,   Z_C = 1/(i w C) = -i/(w C).
A series RLC is resistive at resonance w0 = 1/sqrt(LC), where the reactances
cancel: the current peaks and runs in phase with the drive.  Sharpness is the
quality factor Q = w0 L / R = (1/R) sqrt(L/C).
"""

import cmath
import math

__all__ = [
    "impedance_resistor", "impedance_inductor", "impedance_capacitor",
    "impedance_series", "impedance_parallel", "series_rlc_impedance",
    "resonant_frequency", "quality_factor", "bandwidth",
    "current_amplitude", "current_phase", "average_power",
]


# --- element impedances ------------------------------------------------------

def impedance_resistor(R):
    """Z_R = R (real)."""
    return complex(R, 0.0)


def impedance_inductor(L, omega):
    """Z_L = i w L  (voltage leads current by 90 deg)."""
    return complex(0.0, omega * L)


def impedance_capacitor(C, omega):
    """Z_C = 1/(i w C) = -i/(w C)  (current leads voltage by 90 deg)."""
    return complex(0.0, -1.0 / (omega * C))


def impedance_series(*Zs):
    """Series combination: impedances add."""
    return sum(Zs, complex(0.0, 0.0))


def impedance_parallel(*Zs):
    """Parallel combination: reciprocals add."""
    return 1.0 / sum(1.0 / Z for Z in Zs)


# --- the series RLC ----------------------------------------------------------

def series_rlc_impedance(R, L, C, omega):
    """Z = R + i(wL - 1/wC) for a series RLC driven at frequency w."""
    return complex(R, omega * L - 1.0 / (omega * C))


def resonant_frequency(L, C):
    """Natural / resonant angular frequency  w0 = 1/sqrt(LC)."""
    return 1.0 / math.sqrt(L * C)


def quality_factor(R, L, C):
    """Quality factor  Q = w0 L / R = (1/R) sqrt(L/C)  (sharpness of resonance)."""
    return (1.0 / R) * math.sqrt(L / C)


def bandwidth(R, L):
    """Resonance full width at half-power (in angular frequency):  dw = R / L = w0 / Q."""
    return R / L


# --- response: amplitude, phase, power ---------------------------------------

def current_amplitude(V0, Z):
    """Peak current amplitude |I| = V0 / |Z| for drive amplitude V0."""
    return V0 / abs(Z)


def current_phase(Z):
    """Phase of the current relative to the driving voltage:  -arg(Z).
    > 0 (leading) below resonance (capacitive); < 0 (lagging) above (inductive)."""
    return -cmath.phase(Z)


def average_power(V0, Z):
    """Time-averaged power delivered:  <P> = (1/2) |I|^2 R = (1/2) V0^2 Re(Z)/|Z|^2."""
    return 0.5 * V0 ** 2 * Z.real / (abs(Z) ** 2)


# --- demo --------------------------------------------------------------------

def _demo():
    print("EM-12 AC circuits & driven RLC -- demo")
    print("=" * 40)

    R, L, C, V0 = 10.0, 1e-3, 1e-6, 5.0
    w0 = resonant_frequency(L, C)
    Q = quality_factor(R, L, C)
    print(f"series RLC: R={R} ohm, L={L} H, C={C} F, drive V0={V0} V")
    print(f"  resonance w0 = 1/sqrt(LC) = {w0:.4e} rad/s   (f0 = {w0/(2*math.pi):.1f} Hz)")
    print(f"  quality factor Q = {Q:.3f},  bandwidth dw = R/L = {bandwidth(R,L):.3e} rad/s  (w0/Q = {w0/Q:.3e})")

    print(f"\n{'w/w0':>7} {'|Z| (ohm)':>11} {'|I| (A)':>10} {'phase (deg)':>12} {'<P> (W)':>10}")
    for ratio in (0.5, 0.9, 1.0, 1.1, 2.0):
        w = ratio * w0
        Z = series_rlc_impedance(R, L, C, w)
        print(f"{ratio:7.2f} {abs(Z):11.3f} {current_amplitude(V0,Z):10.4f} "
              f"{math.degrees(current_phase(Z)):12.2f} {average_power(V0,Z):10.4f}")
    print("\nAt resonance Z is purely resistive (Z=R), |I| is maximal, phase=0,")
    print("and <P> = V0^2/2R peaks -- exactly the ~CM-15 driven-oscillator resonance.")


if __name__ == "__main__":
    _demo()
