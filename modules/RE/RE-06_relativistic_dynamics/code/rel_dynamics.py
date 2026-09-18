"""
RE-06  Relativistic dynamics  --  4-momentum, E = mc^2, relativistic collisions,
the centre-of-momentum frame, thresholds, and Compton scattering.

Part of the physics topic network (see modules/topic_network.txt, module RE-06).
Prerequisites: RE-05 (Minkowski 4-vectors & the mass shell), ~CM-06 (Newtonian
linear momentum & its conservation -- this is its relativistic completion).
Feeds into: ~QM-22 (relativistic QM: p.p = -m^2 becomes the Klein-Gordon
operator).

THE ONE IDEA.  Energy and momentum are the time and space parts of ONE 4-vector
        p^mu = m U^mu = (E, p),     E = gamma m,   p = gamma m v   (c = 1),
whose invariant is the mass shell
        p . p = -m^2     <=>     E^2 = p^2 + m^2 .
Total 4-momentum is conserved in every interaction -- a single law that contains
both Newtonian momentum conservation (the spatial part, ~CM-06, recovered as
v -> 0) and energy conservation (the time part), now inseparable.  Mass is just
rest energy, E_0 = m, and can be created or destroyed: that is why colliders have
thresholds and why an inelastic collision gets heavier.

This module builds 4-momenta with RE-05 and checks its low-speed limit against
CM-06's Newtonian momentum.  Units c = 1.
"""

import os
import sys
import math

# --- import RE-05 (Minkowski) and CM-06 (Newtonian momentum) by relative path -
_RE05 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "RE-05_minkowski_spacetime", "code")
_CM06 = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                     "..", "..", "..", "CM", "CM-06_linear_momentum", "code")
for _p in (_RE05, _CM06):
    if _p not in sys.path:
        sys.path.insert(0, _p)
import minkowski            # RE-05: four_momentum, mdot, invariant_mass, ETA
import linear_momentum      # CM-06: momentum, total_momentum (Newtonian)

__all__ = [
    "gamma", "energy", "momentum", "kinetic_energy",
    "four_momentum", "photon_four_momentum",
    "total_four_momentum", "is_conserved",
    "system_invariant_mass", "com_velocity",
    "inelastic_stick", "threshold_kinetic_energy", "compton_shift",
]


def gamma(v):
    """Lorentz factor of a 3-velocity v (|v| < 1, c = 1)."""
    v2 = sum(c * c for c in v)
    return 1.0 / math.sqrt(1.0 - v2)


# --- energy, momentum, kinetic energy ----------------------------------------

def energy(m, v):
    """Relativistic energy  E = gamma m  (c = 1). At rest E = m (= mc^2)."""
    return gamma(v) * m


def momentum(m, v):
    """Relativistic 3-momentum  p = gamma m v. Reduces to CM-06's m v as v -> 0."""
    g = gamma(v)
    return [g * m * vi for vi in v]


def kinetic_energy(m, v):
    """Relativistic kinetic energy  T = (gamma - 1) m  =  E - m.
    Newtonian limit  T -> 1/2 m v^2  as v -> 0."""
    return (gamma(v) - 1.0) * m


# --- 4-momentum --------------------------------------------------------------

def four_momentum(m, v):
    """4-momentum  p^mu = (E, p_x, p_y, p_z) = m U^mu  (RE-05). On the mass shell
    p.p = -m^2."""
    return minkowski.four_momentum(m, list(v))


def photon_four_momentum(E, direction):
    """4-momentum of a massless particle: p = (E, E n_hat), n_hat a unit vector.
    Null: p.p = 0, so |p| = E and it moves at c."""
    n = list(direction)
    norm = math.sqrt(sum(c * c for c in n)) or 1.0
    n = [c / norm for c in n]
    return [E, E * n[0], E * n[1], E * n[2]]


# --- conservation, systems, the COM frame ------------------------------------

def total_four_momentum(four_momenta):
    """Sum of 4-momenta (componentwise). The conserved quantity of any
    interaction -- the relativistic completion of CM-06's total_momentum."""
    return [sum(p[mu] for p in four_momenta) for mu in range(4)]


def is_conserved(before, after, tol=1e-9):
    """True iff total 4-momentum is the same before and after (all 4 components):
    energy AND momentum conservation as one statement."""
    pb, pa = total_four_momentum(before), total_four_momentum(after)
    return all(abs(pb[mu] - pa[mu]) <= tol * (1.0 + abs(pb[mu])) for mu in range(4))


def system_invariant_mass(four_momenta):
    """Invariant mass of a system,  M = sqrt(-P.P)  with P the total 4-momentum
    (RE-05.invariant_mass). Frame-independent; equals the total energy in the COM
    frame. Two back-to-back photons have M = 2E -- mass from massless parts."""
    return minkowski.invariant_mass(total_four_momentum(four_momenta))


def com_velocity(four_momenta):
    """Velocity of the centre-of-momentum frame:  v_com = P_spatial / E_total.
    Boosting to it makes the total 3-momentum vanish."""
    P = total_four_momentum(four_momenta)
    return [P[1] / P[0], P[2] / P[0], P[3] / P[0]]


# --- collisions --------------------------------------------------------------

def inelastic_stick(m1, v1, m2, v2):
    """Two particles collide head-on and stick. 4-momentum is conserved, so the
    product's 4-momentum is the sum; its REST MASS is the system invariant mass,
    which EXCEEDS m1 + m2 -- the lost kinetic energy became mass (E = mc^2).
    Returns (M_product, v_product)."""
    p1, p2 = four_momentum(m1, v1), four_momentum(m2, v2)
    P = total_four_momentum([p1, p2])
    M = minkowski.invariant_mass(P)
    v = [P[1] / P[0], P[2] / P[0], P[3] / P[0]]
    return M, v


def threshold_kinetic_energy(m_beam, m_target, m_products_total):
    """Minimum LAB kinetic energy of the beam (target at rest) to create final
    products of total rest mass M:  using s = (M)^2 at threshold,
        T = (M^2 - (m_beam + m_target)^2) / (2 m_target).
    Example: p+p -> p+p+p+pbar has M = 4 m_p, m_beam = m_target = m_p, giving
    T = 6 m_p (the antiproton-discovery threshold)."""
    M = m_products_total
    E_beam = (M * M - m_beam * m_beam - m_target * m_target) / (2.0 * m_target)
    return E_beam - m_beam


def compton_shift(theta, m_e):
    """Compton wavelength shift  d_lambda = (1/m_e)(1 - cos theta)  (reduced
    Compton wavelength hbar/m_e c = 1/m_e in natural units). Zero forward,
    maximum 2/m_e on backscatter -- the photon loses energy to the electron."""
    return (1.0 - math.cos(theta)) / m_e


# --- demo --------------------------------------------------------------------

def _demo():
    print("RE-06  Relativistic dynamics -- demo   (4-momentum via RE-05)")
    print("=" * 60)
    print("c = 1; builds on CM-06 (Newtonian p) and RE-05 (mass shell)\n")

    print("the mass shell E^2 = p^2 + m^2, and T -> 1/2 m v^2 at low speed:")
    for v in (0.001, 0.1, 0.6, 0.9):
        m = 1.0
        E, p, T = energy(m, [v, 0, 0]), momentum(m, [v, 0, 0])[0], kinetic_energy(m, [v, 0, 0])
        print("  v=%.3f: E=%.5f  p=%.5f  E^2-p^2=%.5f(=m^2)  T=%.5f (1/2 m v^2=%.5f)"
              % (v, E, p, E * E - p * p, T, 0.5 * m * v * v))

    print("\nlow-speed momentum matches CM-06 exactly:")
    v = [0.001, 0.0, 0.0]
    print("  RE-06 momentum=%.8f   CM-06 momentum=%.8f"
          % (momentum(2.0, v)[0], linear_momentum.momentum(2.0, v)[0]))

    print("\ninelastic collision -- KE becomes mass (the product is heavier):")
    M, vp = inelastic_stick(1.0, [0.8, 0, 0], 1.0, [-0.8, 0, 0])
    print("  two m=1 at +-0.8c stick -> M=%.4f (> 2.0), at rest v=%.3f" % (M, vp[0]))

    print("\ntwo back-to-back photons make a massive system:")
    g1 = photon_four_momentum(3.0, [1, 0, 0]); g2 = photon_four_momentum(3.0, [-1, 0, 0])
    print("  E=3 each, opposite -> system invariant mass = %.4f (= 2E)"
          % system_invariant_mass([g1, g2]))

    print("\nantiproton threshold  p p -> p p p pbar  (m_p = 1):")
    print("  T_threshold = %.1f m_p   (the famous 6 m_p c^2 ~ 5.6 GeV)"
          % threshold_kinetic_energy(1.0, 1.0, 4.0))

    print("\nCompton shift (m_e = 1):  d_lambda = (1-cos theta)/m_e")
    for th in (0.0, math.pi / 2, math.pi):
        print("  theta=%5.1f deg -> d_lambda = %.4f" % (math.degrees(th), compton_shift(th, 1.0)))


if __name__ == "__main__":
    _demo()
