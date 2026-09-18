"""QF-02  Interactions & Feynman diagrams -- perturbation theory & the S-matrix.

Physics topic network, module QF-02 (modules/topic_network.txt).
Source: Peskin & Schroeder, *An Introduction to Quantum Field Theory*, Ch. 4
(interacting fields; the Dyson series; Wick's theorem; Feynman diagrams; cross
sections and the S-matrix).  Builds on ~QF-01 (free fields and their propagators)
and ~QM-16 (time-dependent perturbation theory -> the Dyson series); the
non-relativistic limit is ~QM-18 (the Born approximation, d sigma/d Omega = |f|^2).

Natural units hbar = c = 1, metric diag(+,-,-,-) so an on-shell momentum obeys
p^2 = E^2 - |p|^2 = m^2.

What is here
------------
* Kinematics.  Mandelstam invariants s, t, u for 2->2 elastic equal-mass
  scattering in the CM frame, obeying the identity

        s + t + u = sum_i m_i^2 = 4 m^2 ,

  with the CM energy sqrt(s) = E_cm  (`mandelstam`, `cm_energy`, `cm_momentum`).
* Dynamics.  The phi^4 four-point vertex is -i lambda, giving the tree-level
  2->2 amplitude  i M = -i lambda, hence |M|^2 = lambda^2 (isotropic).  In the CM
  frame the differential cross section is  d sigma/d Omega = |M|^2/(64 pi^2 s);
  integrating with the identical-particle factor 1/2 gives the total

        sigma = lambda^2 / (32 pi s)            (Peskin Sect. 4.5)

  (`phi4_amplitude_squared`, `phi4_differential_cross_section`,
  `phi4_cross_section`).  The O(lambda^2) loop corrections diverge -> ~QF-04.
* The Feynman propagator  D_F(p) = i/(p^2 - m^2 + i eps), the contraction of two
  fields in Wick's theorem and the internal line of every diagram (`propagator`).
"""

import numpy as np

__all__ = [
    "MINKOWSKI",
    "minkowski_dot", "minkowski_square", "on_shell_energy",
    "cm_energy", "cm_momentum",
    "mandelstam", "mandelstam_sum",
    "phi4_amplitude_squared", "phi4_differential_cross_section",
    "phi4_cross_section", "propagator",
]

# metric diag(+1,-1,-1,-1): an on-shell 4-momentum has p^2 = E^2 - |p|^2 = m^2
MINKOWSKI = np.diag([1.0, -1.0, -1.0, -1.0])


# --- Minkowski 4-vector algebra ----------------------------------------------

def minkowski_dot(a, b):
    """Lorentz inner product a.b = a0 b0 - a_vec . b_vec  (metric +,-,-,-)."""
    a = np.asarray(a, dtype=float)
    b = np.asarray(b, dtype=float)
    return float(a[0] * b[0] - np.dot(a[1:], b[1:]))


def minkowski_square(p):
    """Invariant square p^2 = p.p; equals m^2 for an on-shell momentum."""
    return minkowski_dot(p, p)


def on_shell_energy(p_vec, m):
    """On-shell energy of a particle of mass m with 3-momentum p_vec:
        E = sqrt(|p_vec|^2 + m^2)   (the positive root of p^2 = m^2)."""
    p_vec = np.asarray(p_vec, dtype=float)
    return float(np.sqrt(np.dot(p_vec, p_vec) + m * m))


# --- two-body kinematics -----------------------------------------------------

def cm_energy(p1, p2):
    """Centre-of-mass energy sqrt(s) of a two-particle state, s = (p1 + p2)^2.

    p1, p2 are 4-momenta [E, px, py, pz].  This is the invariant mass of the pair;
    in the frame where the 3-momenta cancel it is the total energy."""
    s = minkowski_square(np.asarray(p1, float) + np.asarray(p2, float))
    return float(np.sqrt(s))


def cm_momentum(E_cm, m):
    """Magnitude of each particle's CM 3-momentum for an equal-mass pair:
        |p| = (1/2) sqrt(s - 4 m^2),   s = E_cm^2.
    Real only above threshold E_cm >= 2 m; below threshold there is no phase
    space and this returns 0."""
    arg = 0.25 * (E_cm * E_cm - 4.0 * m * m)
    return float(np.sqrt(arg)) if arg > 0.0 else 0.0


def mandelstam(E_cm, theta, m):
    """Mandelstam invariants (s, t, u) for 2->2 elastic equal-mass scattering in
    the CM frame at scattering angle theta:

        s = E_cm^2,
        t = -(1/2)(s - 4 m^2)(1 - cos theta) = -2 |p|^2 (1 - cos theta),
        u = -(1/2)(s - 4 m^2)(1 + cos theta) = -2 |p|^2 (1 + cos theta),

    with |p| the CM momentum.  They obey the Mandelstam identity
        s + t + u = 4 m^2  (= sum of the four squared external masses)
    for ALL E_cm and theta.  Above threshold (E_cm >= 2 m) both t, u <= 0
    (spacelike momentum transfer).  Returns (s, t, u).  [Peskin Sect. 4.5]"""
    s = E_cm * E_cm
    half = 0.5 * (s - 4.0 * m * m)
    c = np.cos(theta)
    t = -half * (1.0 - c)
    u = -half * (1.0 + c)
    return float(s), float(t), float(u)


def mandelstam_sum(m):
    """Right-hand side of the Mandelstam identity for four equal-mass legs:
        s + t + u = sum_i m_i^2 = 4 m^2."""
    return 4.0 * m * m


# --- phi^4 dynamics ----------------------------------------------------------

def phi4_amplitude_squared(lam):
    """Tree-level 2->2 amplitude-squared in phi^4 theory.

    The single four-point vertex -i lambda gives  i M = -i lambda, so M = -lambda
    and |M|^2 = lambda^2 -- isotropic (no angular dependence) at this order.
    [Peskin Sect. 4.5; the O(lambda^2) loop corrections diverge -> ~QF-04.]"""
    return lam * lam


def phi4_differential_cross_section(E_cm, lam, m):
    """CM differential cross section for 2->2 elastic equal-mass scattering,
        d sigma/d Omega = |M|^2 / (64 pi^2 s)   [Peskin Eq. 4.84, |p_f| = |p_i|].
    For phi^4 the amplitude is isotropic (|M|^2 = lambda^2).  Returns 0 below
    threshold E_cm < 2 m (no real final-state momenta)."""
    if E_cm < 2.0 * m:
        return 0.0
    s = E_cm * E_cm
    return phi4_amplitude_squared(lam) / (64.0 * np.pi ** 2 * s)


def phi4_cross_section(E_cm, lam, m):
    """Total tree-level 2->2 cross section in phi^4 theory.

    Integrate the (isotropic) differential cross section over solid angle and
    include the symmetry factor 1/2 for the two IDENTICAL final-state particles:

        sigma = (1/2) * (4 pi) * lambda^2/(64 pi^2 s) = lambda^2 / (32 pi s),

    with s = E_cm^2  (Peskin Sect. 4.5).  Positive, proportional to lambda^2, and
    zero below threshold E_cm < 2 m (the incoming pair needs sqrt(s) >= 2 m to be
    on-shell).  Returns a number."""
    if E_cm < 2.0 * m:
        return 0.0
    s = E_cm * E_cm
    return lam * lam / (32.0 * np.pi * s)


# --- the Feynman propagator --------------------------------------------------

def propagator(p, m, eps=1e-9):
    """Feynman propagator of a scalar of mass m at 4-momentum p:

        D_F(p) = i / (p^2 - m^2 + i eps),      p^2 = E^2 - |p_vec|^2.

    `p` is a 4-vector [E, px, py, pz].  The +i eps (Feynman boundary condition)
    regulates the on-shell pole p^2 = m^2; with x = p^2 - m^2,

        D_F = (eps + i x) / (x^2 + eps^2),

    so Re D_F = eps/(x^2 + eps^2) is a Lorentzian of width eps (a nascent
    pi delta(x) on shell) and Im D_F = x/(x^2 + eps^2) -> the principal value 1/x
    off shell.  [Peskin Sect. 2.4 / 4.3]  Returns a complex number."""
    p2 = minkowski_square(p)
    return 1j / (p2 - m * m + 1j * eps)


# --- demo --------------------------------------------------------------------

def _demo():
    print("QF-02  Interactions & Feynman diagrams -- demo  (hbar = c = 1)")
    print("=" * 64)

    m, lam = 1.0, 0.3

    # 1) a Mandelstam triple with the s + t + u = 4 m^2 sum check
    E_cm, theta = 5.0, np.pi / 3.0
    s, t, u = mandelstam(E_cm, theta, m)
    print("\n1) Mandelstam invariants  (m = %.1f, E_cm = %.1f, theta = pi/3):" % (m, E_cm))
    print("   s = %+.4f   ( = E_cm^2 = %.4f )" % (s, E_cm ** 2))
    print("   t = %+.4f" % t)
    print("   u = %+.4f" % u)
    print("   s + t + u = %.6f   (should be 4 m^2 = %.6f)"
          % (s + t + u, mandelstam_sum(m)))
    print("   CM momentum |p| = %.4f = (1/2) sqrt(s - 4 m^2)" % cm_momentum(E_cm, m))

    # 2) phi^4 amplitude and total cross section vs sqrt(s)
    print("\n2) phi^4 tree level:  i M = -i lambda,  |M|^2 = lambda^2 = %.4f"
          % phi4_amplitude_squared(lam))
    print("   total sigma(sqrt s) = lambda^2 / (32 pi s):")
    for E in [1.50, 2.00, 3.00, 5.00, 10.00]:
        sig = phi4_cross_section(E, lam, m)
        tag = "   (below threshold 2m -> no phase space)" if E < 2.0 * m else ""
        print("     sqrt(s) = %6.3f :  sigma = %.6e%s" % (E, sig, tag))
    print("   sigma(2 lambda)/sigma(lambda) = %.3f   (expect 4 = 2^2, i.e. ~ lambda^2)"
          % (phi4_cross_section(5.0, 2 * lam, m) / phi4_cross_section(5.0, lam, m)))

    # 3) the Feynman propagator: finite off shell, poles on shell
    print("\n3) Feynman propagator  D_F(p) = i/(p^2 - m^2 + i eps):")
    p_off = np.array([3.0, 0.0, 0.0, 0.0])               # p^2 = 9 (m^2 = 1) off shell
    z = propagator(p_off, m)
    print("   off shell p^2 = %.2f :  D_F = %.5f %+.5fi,  |D_F| = %.5f"
          % (minkowski_square(p_off), z.real, z.imag, abs(z)))
    p_on = np.array([np.sqrt(5.0), 2.0, 0.0, 0.0])       # E^2 - 4 = 1 = m^2, on shell
    print("   on  shell p^2 = %.2f :  |D_F| ~ 1/eps = %.3e   (the pole)"
          % (minkowski_square(p_on), abs(propagator(p_on, m, eps=1e-6))))


if __name__ == "__main__":
    _demo()
