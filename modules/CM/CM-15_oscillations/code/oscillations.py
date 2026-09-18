"""
CM-15  Oscillations -- simple harmonic, damped, and driven motion; resonance and
the quality factor.

Part of the physics topic network (modules/topic_network.txt, module CM-15).
Reuses ~MA-07 (the integrator); the analytic forms come from the constant-
coefficient ODEs of ~MA-07/~CM-05; links to ~EM-12 (driven RLC) and ~CM-16
(normal modes).

The damped, driven oscillator (per unit mass):
    x'' + 2 gamma x' + omega0^2 x = F0 cos(omega_d t).

NOTE: MA-07 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
if _MA07 not in sys.path:
    sys.path.insert(0, _MA07)

from ode import integrate  # noqa: E402

__all__ = [
    "integrate_oscillator", "damped_frequency", "driven_amplitude",
    "resonance_frequency", "quality_factor", "underdamped_solution",
]


def _rhs(omega0, gamma, F0, omega_d):
    def rhs(t, y):
        x, v = y
        return [v, -2.0 * gamma * v - omega0 ** 2 * x + F0 * math.cos(omega_d * t)]
    return rhs


def integrate_oscillator(omega0, gamma, x0, v0, t0, t1, n, F0=0.0, omega_d=0.0):
    """Integrate the damped, driven oscillator. Returns (ts, states=[x, v])."""
    return integrate(_rhs(omega0, gamma, F0, omega_d), [x0, v0], t0, t1, n)


def damped_frequency(omega0, gamma):
    """Underdamped oscillation frequency  omega_d = sqrt(omega0^2 - gamma^2)."""
    return math.sqrt(omega0 ** 2 - gamma ** 2)


def driven_amplitude(omega0, gamma, F0, omega_d):
    """Steady-state amplitude  A = F0 / sqrt((omega0^2 - omega^2)^2 + (2 gamma omega)^2)."""
    return F0 / math.sqrt((omega0 ** 2 - omega_d ** 2) ** 2 + (2.0 * gamma * omega_d) ** 2)


def resonance_frequency(omega0, gamma):
    """Amplitude resonance peaks at  omega = sqrt(omega0^2 - 2 gamma^2)."""
    return math.sqrt(omega0 ** 2 - 2.0 * gamma ** 2)


def quality_factor(omega0, gamma):
    """Quality factor  Q = omega0 / (2 gamma)."""
    return omega0 / (2.0 * gamma)


def underdamped_solution(omega0, gamma, x0=1.0, v0=0.0):
    """Closed-form underdamped free response x(t) for the given initial conditions."""
    wd = damped_frequency(omega0, gamma)

    def x(t):
        A = x0
        B = (v0 + gamma * x0) / wd
        return math.exp(-gamma * t) * (A * math.cos(wd * t) + B * math.sin(wd * t))
    return x


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-15 oscillations -- demo")
    print("=" * 32)
    w0 = 2.0
    ts, ys = integrate_oscillator(w0, 0.0, 1.0, 0.0, 0.0, math.pi, 4000)
    print(f"SHM (gamma=0, w0=2): x(pi) = {ys[-1][0]:.5f}  (cos(2 pi)=1)")

    g = 0.2
    print(f"\ndamped (w0=2, gamma=0.2): omega_d = {damped_frequency(w0, g):.5f}, Q = {quality_factor(w0, g):.3f}")

    g, wd, F0 = 0.2, 1.5, 1.0
    A = driven_amplitude(w0, g, F0, wd)
    ts, ys = integrate_oscillator(w0, g, 0.0, 0.0, 0.0, 100.0, 20000, F0=F0, omega_d=wd)
    tail = [abs(s[0]) for s in ys[-280:]]
    print(f"\ndriven (w_d=1.5): steady amplitude numeric {max(tail):.4f}  vs formula {A:.4f}")
    print(f"  amplitude resonance at omega = {resonance_frequency(w0, g):.4f}")


if __name__ == "__main__":
    _demo()
