"""
CM-18  Symmetries & Noether's theorem -- every continuous symmetry of the
Lagrangian gives a conserved quantity.

Part of the physics topic network (modules/topic_network.txt, module CM-18).
Reuses ~CM-17 (`generalized_momentum`, `jacobi_energy`, `integrate_eom`); links
to ~MA-18 (groups) and the conservation laws of ~CM-06/~CM-09.

For a 1-DOF system with Lagrangian L(t, q, qdot): the continuous transformation
delta q = eps f(q) is a symmetry if it leaves L unchanged, and then the **Noether
charge**  Q = (dL/dqdot) f(q)  is conserved. Translation (f=1) -> momentum;
time-translation (no explicit t) -> energy.

NOTE: CM-17 imported by relative path; becomes `from physkit...` later.
"""

import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_CM17 = os.path.abspath(os.path.join(_HERE, "..", "..", "CM-17_lagrangian", "code"))
if _CM17 not in sys.path:
    sys.path.insert(0, _CM17)

from lagrangian import generalized_momentum, jacobi_energy, integrate_eom  # noqa: E402

__all__ = ["noether_charge", "symmetry_defect", "energy", "integrate_eom"]


def noether_charge(L, f, t, q, qdot):
    """Conserved quantity for the symmetry delta q = eps f(q):  Q = (dL/dqdot) f(q)."""
    return generalized_momentum(L, t, q, qdot) * f(q)


def symmetry_defect(L, f, t, q, qdot, eps=1e-5):
    """First-order change in L under the flow delta q = eps f(q),
    delta qdot = eps f'(q) qdot.  ~0 means f generates a symmetry of L."""
    df = (f(q + 1e-6) - f(q - 1e-6)) / 2e-6
    return (L(t, q + eps * f(q), qdot + eps * df * qdot) - L(t, q, qdot)) / eps


def energy(L, t, q, qdot):
    """The Jacobi energy (Hamiltonian); conserved when L has no explicit time
    dependence -- Noether's theorem for time-translation symmetry."""
    return jacobi_energy(L, t, q, qdot)


# --- demo --------------------------------------------------------------------

def _demo():
    print("CM-18 symmetries & Noether's theorem -- demo")
    print("=" * 32)

    free = lambda t, q, p: 0.5 * p * p                            # free particle
    print("free particle L = 1/2 q'^2:")
    print(f"  translation symmetric? defect = {symmetry_defect(free, lambda q: 1.0, 0, 1.0, 2.0):.2e}  (~0)")
    ts, ys = integrate_eom(lambda t, q, qd: 0.0, 0.0, 2.5, 0.0, 4.0, 800)
    Q = [noether_charge(free, lambda q: 1.0, t, s[0], s[1]) for t, s in zip(ts, ys)]
    print(f"  Noether charge (momentum): {Q[0]:.4f} -> {Q[-1]:.4f}  (conserved)")

    w = 2.0
    sho = lambda t, q, p: 0.5 * p * p - 0.5 * w * w * q * q
    print("\nharmonic oscillator (V breaks translation, but L has no explicit t):")
    print(f"  translation defect = {symmetry_defect(sho, lambda q: 1.0, 0, 1.0, 0.5):.4f}  (!= 0)")
    ts, ys = integrate_eom(lambda t, q, qd: -w * w * q, 1.0, 0.0, 0.0, 5.0, 5000)
    E = [energy(sho, t, s[0], s[1]) for t, s in zip(ts, ys)]
    print(f"  energy (time-translation): {E[0]:.5f} -> {E[-1]:.5f}  (conserved = 1/2 w^2 = 2)")


if __name__ == "__main__":
    _demo()
