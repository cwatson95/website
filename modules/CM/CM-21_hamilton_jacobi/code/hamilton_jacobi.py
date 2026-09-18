"""
CM-21  Hamilton-Jacobi theory & action-angle variables.

Part of the physics topic network (modules/topic_network.txt, module CM-21).
Builds on ~CM-19 (Hamiltonian); reuses ~MA-07 for a direct-integration check.
Links to ~QM-15 (WKB, where S/hbar is the phase) and ~RE-12 (the action as a
geodesic length).

For a conservative 1-DOF system H = p^2/2m + V(q), Hamilton's characteristic
function is W(q) = integral p dq with p = sqrt(2m(E - V)). The **action
variable** J = oint p dq is an adiabatic invariant, and the motion's **period**
is T = dJ/dE -- exact even for anharmonic wells.

NOTE: MA-07 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
if _MA07 not in sys.path:
    sys.path.insert(0, _MA07)

from ode import integrate  # noqa: E402  (used in the demo cross-check)

__all__ = [
    "turning_points", "characteristic_function", "action_variable",
    "period", "frequency",
]


def _bisect(f, a, b, it=80):
    fa = f(a)
    for _ in range(it):
        m = 0.5 * (a + b)
        fm = f(m)
        if (fa > 0.0) == (fm > 0.0):
            a, fa = m, fm
        else:
            b = m
    return 0.5 * (a + b)


def turning_points(V, E, q_min, q_max, q0=0.0):
    """The two turning points where V(q) = E, bracketing the well minimum q0."""
    left = _bisect(lambda q: V(q) - E, q_min, q0)
    right = _bisect(lambda q: V(q) - E, q0, q_max)
    return left, right


def characteristic_function(V, m, E, q, q_min, q0=0.0, n=2000):
    """Hamilton's characteristic function W(q) = int_{q-}^{q} sqrt(2m(E-V)) dq'."""
    a = turning_points(V, E, q_min, q_min + 2 * (q0 - q_min), q0)[0]
    h = (q - a) / n
    s = 0.0
    for i in range(n):
        qq = a + (i + 0.5) * h
        arg = 2.0 * m * (E - V(qq))
        if arg > 0.0:
            s += math.sqrt(arg) * h
    return s


def action_variable(V, m, E, q_min, q_max, q0=0.0, n=4000):
    """The action  J = oint p dq = 2 int_{q-}^{q+} sqrt(2m(E - V(q))) dq."""
    a, b = turning_points(V, E, q_min, q_max, q0)
    h = (b - a) / n
    s = 0.0
    for i in range(n):
        q = a + (i + 0.5) * h
        arg = 2.0 * m * (E - V(q))
        if arg > 0.0:
            s += math.sqrt(arg) * h
    return 2.0 * s


def period(V, m, E, q_min, q_max, q0=0.0, n=4000):
    """The oscillation period  T = oint dq/v = dJ/dE.  Evaluated with the angle
    substitution q = c + A sin(theta), whose cos(theta) factor cancels the
    1/sqrt(E - V) singularity at the turning points."""
    a, b = turning_points(V, E, q_min, q_max, q0)
    c, A = 0.5 * (a + b), 0.5 * (b - a)
    dth = math.pi / n
    total = 0.0
    for i in range(n):
        th = -0.5 * math.pi + (i + 0.5) * dth
        q = c + A * math.sin(th)
        denom = E - V(q)
        if denom > 0.0:
            total += A * math.cos(th) / math.sqrt(denom) * dth
    return math.sqrt(2.0 * m) * total


def frequency(V, m, E, q_min, q_max, q0=0.0, n=4000):
    """Angular frequency  omega = 2 pi / T."""
    return 2.0 * math.pi / period(V, m, E, q_min, q_max, q0, n)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-21 Hamilton-Jacobi & action-angle -- demo")
    print("=" * 32)
    w, m = 2.0, 1.0
    V = lambda q: 0.5 * m * w * w * q * q
    for E in (1.0, 2.0, 4.0):
        J = action_variable(V, m, E, -10, 10)
        print(f"SHO E={E}: J = {J:.5f}  (2 pi E/w = {2 * math.pi * E / w:.5f}), "
              f"T = {period(V, m, E, -10, 10):.5f}  (2 pi/w = {2 * math.pi / w:.5f}, isochronous)")

    print("\npendulum V=1-cos(theta) (anharmonic): period grows with amplitude")
    Vp = lambda q: 1.0 - math.cos(q)
    for E in (0.01, 0.5, 1.5):
        print(f"  E={E}: T = {period(Vp, 1.0, E, -3.1, 3.1):.4f}   (small-E -> 2 pi = {2 * math.pi:.4f})")


if __name__ == "__main__":
    _demo()
