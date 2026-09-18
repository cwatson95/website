"""
CM-14  Euler's equations -- rigid-body rotation in the body (principal-axis)
frame, and torque-free precession.

Part of the physics topic network (modules/topic_network.txt, module CM-14).
Reuses ~MA-07 (the integrator); builds on ~CM-13 (principal moments).

In the principal-axis body frame, with principal moments I1, I2, I3:
    I1 omega1' = (I2 - I3) omega2 omega3 + N1   (and cyclic).
For torque-free motion (N = 0) the angular-momentum magnitude |L| and the
rotational kinetic energy are conserved.

NOTE: MA-07 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA07 = os.path.abspath(os.path.join(_HERE, "..", "..", "..", "MA", "MA-07_ode", "code"))
if _MA07 not in sys.path:
    sys.path.insert(0, _MA07)

from ode import integrate  # noqa: E402

__all__ = ["euler_rhs", "integrate_euler", "precession_rate", "L_magnitude_sq", "rotational_energy"]


def euler_rhs(I, torque=None):
    """RHS d omega/dt of Euler's equations for principal moments I=(I1,I2,I3).
    `torque` (optional) is torque(t, omega) -> (N1, N2, N3) in the body frame."""
    I1, I2, I3 = I

    def rhs(t, w):
        N = torque(t, w) if torque else (0.0, 0.0, 0.0)
        return [((I2 - I3) * w[1] * w[2] + N[0]) / I1,
                ((I3 - I1) * w[2] * w[0] + N[1]) / I2,
                ((I1 - I2) * w[0] * w[1] + N[2]) / I3]
    return rhs


def integrate_euler(I, omega0, t0, t1, n, torque=None):
    """Integrate Euler's equations. Returns (ts, omegas)."""
    return integrate(euler_rhs(I, torque), list(omega0), t0, t1, n)


def precession_rate(I_perp, I_sym, omega3):
    """Body-frame free-precession rate of a symmetric top (I1=I2=I_perp, I3=I_sym):
       Omega = (I_sym - I_perp)/I_perp * omega3."""
    return (I_sym - I_perp) / I_perp * omega3


def L_magnitude_sq(I, omega):
    """|L|^2 = (I1 w1)^2 + (I2 w2)^2 + (I3 w3)^2."""
    return sum((I[i] * omega[i]) ** 2 for i in range(3))


def rotational_energy(I, omega):
    """T = 1/2 (I1 w1^2 + I2 w2^2 + I3 w3^2)."""
    return 0.5 * sum(I[i] * omega[i] ** 2 for i in range(3))


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-14 Euler's equations -- demo")
    print("=" * 32)
    I = (1.0, 2.0, 3.0)
    ts, ws = integrate_euler(I, (1.0, 1.0, 1.0), 0.0, 5.0, 5000)
    print("torque-free (I=1,2,3, w0=1,1,1):")
    print(f"  |L|^2: {L_magnitude_sq(I, ws[0]):.5f} -> {L_magnitude_sq(I, ws[-1]):.5f}  (conserved)")
    print(f"  T:     {rotational_energy(I, ws[0]):.5f} -> {rotational_energy(I, ws[-1]):.5f}  (conserved)")

    # symmetric top: I1=I2, omega3 is constant, omega1,omega2 precess
    Is = (1.0, 1.0, 2.0)
    ts, ws = integrate_euler(Is, (0.5, 0.0, 3.0), 0.0, 5.0, 5000)
    print("\nsymmetric top (I=1,1,2, w0=0.5,0,3):")
    print(f"  omega3: {ws[0][2]:.5f} -> {ws[-1][2]:.5f}  (constant)")
    print(f"  precession rate Omega = {precession_rate(1.0, 2.0, 3.0):.4f}")


if __name__ == "__main__":
    _demo()
