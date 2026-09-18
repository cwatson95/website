"""
MA-22  Topology & dynamical systems -- linear stability of equilibria (classified
by the Jacobian's eigenvalues), the logistic map's route to chaos and its Lyapunov
exponent, period detection, and the Euler characteristic as a topological invariant.

Part of the physics topic network (modules/topic_network.txt, module MA-22 [adv]).
Feeds ~CM-24 (nonlinear dynamics & chaos) and ~CM-15 (oscillator stability);
the topology side (~MA-14 d^2=0 -> de Rham) connects forms to global structure.

Pure Python, dependency-free. Equilibria are classified from the 2x2 Jacobian's
eigenvalues (Chicone pp.20-23); the logistic map's Lyapunov exponent is the orbit
average of ln|f'| (= ln 2 exactly at r=4); the Euler characteristic V-E+F is
checked to be 2 for every convex polyhedron (sphere topology) and 0 for the torus.
"""

import math

__all__ = [
    "classify_equilibrium", "eigenvalues_2x2",
    "logistic", "logistic_orbit", "lyapunov_logistic", "period_of_orbit",
    "euler_characteristic", "PLATONIC",
]


# --- linear stability of a planar equilibrium --------------------------------

def eigenvalues_2x2(J):
    """The two eigenvalues of a 2x2 matrix (possibly complex)."""
    a, b = J[0]
    c, d = J[1]
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    if disc >= 0:
        r = math.sqrt(disc)
        return (complex((tr + r) / 2), complex((tr - r) / 2))
    r = math.sqrt(-disc)
    return (complex(tr / 2, r / 2), complex(tr / 2, -r / 2))


def classify_equilibrium(J):
    """Classify the rest point of x' = J x from the eigenvalues of J
    (Chicone §1.6, pp.20-23): saddle / stable|unstable node / stable|unstable
    spiral / center. Stability is set by the sign of the real parts."""
    a, b = J[0]
    c, d = J[1]
    tr = a + d
    det = a * d - b * c
    disc = tr * tr - 4 * det
    if abs(det) < 1e-12:
        return "degenerate"
    if det < 0:
        return "saddle"                                  # real eigenvalues, opposite sign
    if disc < -1e-12:                                    # complex pair
        if abs(tr) < 1e-9:
            return "center"
        return "stable spiral" if tr < 0 else "unstable spiral"
    return "stable node" if tr < 0 else "unstable node"  # real, same sign


# --- the logistic map: order, period-doubling, chaos -------------------------

def logistic(r, x):
    return r * x * (1 - x)


def logistic_orbit(r, x0, n, skip=0):
    """Return n iterates of the logistic map after discarding `skip` transients."""
    x = x0
    for _ in range(skip):
        x = logistic(r, x)
    out = []
    for _ in range(n):
        out.append(x)
        x = logistic(r, x)
    return out


def lyapunov_logistic(r, x0=0.1, n=200000, skip=1000):
    """Lyapunov exponent lambda = <ln|f'(x)|> along the orbit, f'(x)=r(1-2x).
    lambda < 0 on a stable cycle, lambda > 0 in chaos (= ln 2 at r=4)."""
    x = x0
    for _ in range(skip):
        x = logistic(r, x)
    s = 0.0
    for _ in range(n):
        deriv = r * (1 - 2 * x)
        s += math.log(abs(deriv)) if deriv != 0 else 0.0
        x = logistic(r, x)
    return s / n


def period_of_orbit(r, x0=0.1, skip=4000, window=256, tol=1e-6):
    """Detect the period of the attracting cycle (1, 2, 4, ...) after transients;
    returns -1 if no period <= window/2 is found (chaotic / very long)."""
    orbit = logistic_orbit(r, x0, window, skip=skip)
    for p in range(1, window // 2):
        if all(abs(orbit[i] - orbit[i + p]) < tol for i in range(window - p)):
            return p
    return -1


# --- topology: the Euler characteristic --------------------------------------

def euler_characteristic(V, E, F):
    """chi = V - E + F. For any convex polyhedron (a triangulated sphere) chi = 2;
    a torus gives 0. chi is a TOPOLOGICAL invariant -- independent of how you mesh."""
    return V - E + F


# (vertices, edges, faces) of the five Platonic solids -- all have chi = 2
PLATONIC = {
    "tetrahedron": (4, 6, 4),
    "cube": (8, 12, 6),
    "octahedron": (6, 12, 8),
    "dodecahedron": (20, 30, 12),
    "icosahedron": (12, 30, 20),
}


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-22 topology & dynamical systems -- demo")
    print("=" * 43)

    print("\nlinear stability -- classify x' = J x by the eigenvalues of J:")
    cases = {
        "saddle":          [[1, 0], [0, -1]],
        "stable node":     [[-2, 0], [0, -1]],
        "unstable node":   [[2, 0], [0, 1]],
        "stable spiral":   [[-1, -2], [2, -1]],
        "center":          [[0, -1], [1, 0]],
    }
    for name, J in cases.items():
        ev = eigenvalues_2x2(J)
        print(f"  {classify_equilibrium(J):16s} (expected {name:14s})  eigenvalues {ev[0]:.2g}, {ev[1]:.2g}")

    print("\nlogistic map x -> r x(1-x): period and Lyapunov exponent:")
    for r in (2.5, 3.2, 3.5, 3.835, 4.0):
        p = period_of_orbit(r)
        lam = lyapunov_logistic(r)
        tag = "chaos" if lam > 0 else "stable"
        print(f"  r={r:<5}: period {p:>3}   lambda = {lam:+.4f}  ({tag})")
    print(f"  -> at r=4, lambda should be ln 2 = {math.log(2):.4f}")

    print("\nEuler characteristic V - E + F (= 2 for every convex polyhedron):")
    for name, (V, E, F) in PLATONIC.items():
        print(f"  {name:12s} ({V:2d},{E:2d},{F:2d}): chi = {euler_characteristic(V, E, F)}")
    print(f"  torus (mesh 9,27,18):      chi = {euler_characteristic(9, 27, 18)}  (= 0, one handle)")


if __name__ == "__main__":
    _demo()
