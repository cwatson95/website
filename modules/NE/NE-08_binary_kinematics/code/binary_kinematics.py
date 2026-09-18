"""NE-08  Binary reaction kinematics, thresholds and the Coulomb barrier.

Nuclear Science & Engineering trunk, module NE-08 (modules/NE/list_NE.txt),
following Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, 3rd
ed., Sections 6.1-6.5 (printed pp. 136-153).  Pure stdlib; masses from
../../data_tables/B1_atomic_masses.csv.

~NE-04 gave the Q-value -- whether a reaction is energetically allowed.  This
module answers the two questions that actually decide whether it happens:

  1. KINEMATIC THRESHOLD.  For Q < 0 the incident particle must supply |Q| AND
     the centre-of-mass motion the products are forced to carry:

        E_th = -Q (m_y + m_Y)/(m_y + m_Y - m_x) ~ -Q (1 + m_x/m_X)   [Eq. 6.15]

     Quoting |Q| as the threshold, as ~NE-04's deliberately-named
     `threshold_energy_naive` does, is always an underestimate.

  2. COULOMB BARRIER.  A charged projectile must reach the nuclear surface
     before the strong force can act.  This applies whatever the sign of Q, and
     it is why exothermic charged-particle reactions still need accelerators
     while neutron reactions run at thermal energies.

The same kinematics, specialised to a neutron scattering elastically, gives the
energy-loss law that governs moderation (~NE-13, ~NE-19):

    E'/E in [alpha, 1],    alpha = ((A-1)/(A+1))^2 ,

so a single collision with hydrogen can stop a neutron dead while one with 238U
barely dents it.  That inequality is the whole reason reactors are built around
light moderators.
"""

import csv
import math
import os

__all__ = [
    "M_N_U", "M_H_U", "U_MEV", "COULOMB_MEV_FM", "R0_FM",
    "load_atomic_masses", "atomic_mass", "has_nuclide",
    "q_value_masses", "threshold_energy", "threshold_energy_approx",
    "coulomb_barrier", "closest_approach", "overall_threshold",
    "minimum_product_energy",
    "cm_kinetic_energy", "cm_velocity_fraction",
    "scattering_energy", "elastic_scattering_energy_ratio", "alpha_collision",
    "max_fractional_energy_loss", "mean_energy_after_collision",
    "average_log_energy_decrement", "collisions_to_thermalize",
    "max_lab_scattering_angle", "recoil_energy",
    "electron_recoil_energy", "max_electron_recoil_energy",
]

M_N_U = 1.0086649156
M_H_U = 1.0078250321
M_E_U = 5.4857990945e-4
U_MEV = 931.494043
COULOMB_MEV_FM = 1.43996          # e^2/(4 pi eps0), in MeV fm
R0_FM = 1.2                       # nuclear radius coefficient, S&F Eq. (1.7)
# COULOMB_MEV_FM/R0_FM = 1.1999... -- the 1.20 MeV numerator of S&F Eq. (6.19)

_MASSES = None


def _csv_path():
    here = os.path.dirname(os.path.abspath(__file__))
    return os.path.normpath(os.path.join(
        here, os.pardir, os.pardir, "data_tables", "B1_atomic_masses.csv"))


def load_atomic_masses(path=None):
    """{(Z, A): atomic_mass_u} from the extracted Appendix B.  Cached."""
    global _MASSES
    if _MASSES is not None and path is None:
        return _MASSES
    table = {}
    with open(path or _csv_path(), newline="", encoding="utf-8") as fh:
        for row in csv.DictReader(fh):
            table[(int(row["Z"]), int(row["A"]))] = float(row["atomic_mass_u"])
    if path is None:
        _MASSES = table
    return table


def atomic_mass(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return t[(int(Z), int(A))]


def has_nuclide(A, Z, table=None):
    t = load_atomic_masses() if table is None else table
    return (int(Z), int(A)) in t


def q_value_masses(m_x, m_X, m_y, m_Y):
    """Q = [(m_x + m_X) - (m_y + m_Y)] c^2 in MeV, masses in u  [Eqs. (6.4)-(6.6)].

    Neutral-atom masses may be used throughout when the electron count balances;
    ~NE-04 works through the cases where it does not."""
    return ((m_x + m_X) - (m_y + m_Y)) * U_MEV


# --- kinematic threshold  [S&F Eqs. (6.14)-(6.15), printed p. 142] ---------

def threshold_energy(q_mev, m_x, m_y, m_Y):
    """Exact kinematic threshold  [Eq. (6.14)]:

        E_th = -Q (m_y + m_Y) / (m_y + m_Y - m_x) .

    Zero for an exoergic reaction.  Masses in u, Q and the result in MeV."""
    if q_mev >= 0:
        return 0.0
    den = m_y + m_Y - m_x
    if den <= 0:
        raise ValueError("unphysical mass combination")
    return -q_mev * (m_y + m_Y) / den


def threshold_energy_approx(q_mev, m_x, m_X):
    """The usual approximation  [Eq. (6.15)]:  E_th ~ -Q (1 + m_x/m_X).

    Good because rest masses vastly exceed Q/c^2; it makes the physics obvious --
    the excess over |Q| is the centre-of-mass kinetic energy the products must
    retain, and it grows as the projectile approaches the target in mass."""
    if q_mev >= 0:
        return 0.0
    if m_X <= 0:
        raise ValueError("target mass must be positive")
    return -q_mev * (1.0 + m_x / m_X)


def cm_kinetic_energy(e_lab, m_x, m_X):
    """Kinetic energy available in the centre-of-mass frame:

        E_cm = E_lab * m_X/(m_x + m_X) .

    The rest, E_lab * m_x/(m_x+m_X), is locked up in the motion of the centre of
    mass and can never drive a reaction.  This is the whole content of the
    threshold correction."""
    if m_x <= 0 or m_X <= 0:
        raise ValueError("masses must be positive")
    return e_lab * m_X / (m_x + m_X)


def cm_velocity_fraction(m_x, m_X):
    """v_cm / v_x = m_x/(m_x + m_X): the fraction of the projectile's velocity
    carried by the centre of mass."""
    return m_x / (m_x + m_X)


# --- Coulomb barrier  [S&F §6.3.2, Eqs. (6.16)-(6.18), printed p. 143] ----

def coulomb_barrier(Z_x, A_x, Z_X, A_X, r0_fm=R0_FM):
    """Barrier height (MeV) with the two nuclei just touching  [Eq. (6.19)]:

        E_x^C = Z_x Z_X e^2/(4 pi eps0 R) ~ 1.20 Z_x Z_X/(A_x^1/3 + A_X^1/3),

    with R = r0(A_x^(1/3) + A_X^(1/3)) and r0 = 1.2 fm  [Eq. (1.7)].  This is the
    work done by the projectile against a target treated as fixed, so it is a
    LABORATORY energy and enters Eq. (6.20) directly -- see `overall_threshold`.

    Zero for a neutral projectile -- which is exactly why neutron-induced
    reactions dominate reactor physics (~NE-13, ~NE-19)."""
    if min(A_x, A_X) < 1 or min(Z_x, Z_X) < 0:
        raise ValueError("invalid nuclide")
    if Z_x == 0 or Z_X == 0:
        return 0.0
    R = r0_fm * (A_x ** (1.0 / 3.0) + A_X ** (1.0 / 3.0))
    return COULOMB_MEV_FM * Z_x * Z_X / R


def closest_approach(e_lab_mev, Z_x, Z_X, m_x=None, m_X=None):
    """Distance of closest approach (fm) for a head-on Coulomb collision.

    Using the centre-of-mass energy when masses are supplied -- only that part of
    the laboratory energy is available to fight the repulsion."""
    if e_lab_mev <= 0:
        raise ValueError("energy must be positive")
    if Z_x == 0 or Z_X == 0:
        return 0.0
    e = e_lab_mev if (m_x is None or m_X is None) else cm_kinetic_energy(e_lab_mev, m_x, m_X)
    return COULOMB_MEV_FM * Z_x * Z_X / e


def overall_threshold(q_mev, m_x, m_X, m_y, m_Y, Z_x, A_x, Z_X, A_X, r0_fm=R0_FM):
    """The energy a projectile actually needs  [Eq. (6.20), printed p. 144]:

        (E_x^th)_min = max(E_x^C, E_x^th) .

    Both are laboratory-frame requirements, and the reaction needs whichever
    hurdle is higher.  A neutron sees only the kinematic term; an exoergic
    charged-particle reaction sees only the barrier."""
    kin = threshold_energy(q_mev, m_x, m_y, m_Y)
    vc = coulomb_barrier(Z_x, A_x, Z_X, A_X, r0_fm)
    return max(kin, vc)


def minimum_product_energy(q_mev, m_x, m_X, m_y, m_Y, Z_x, A_x, Z_X, A_X,
                           r0_fm=R0_FM):
    """Least kinetic energy the products can carry away, Q + (E_x^th)_min
    [S&F Example 6.1, printed p. 144].

    Never negative: at the kinematic threshold it is zero for a neutral
    projectile, and for a charged one the barrier energy is not lost -- the
    target recoils, and the whole of E_x^C reappears in the products."""
    return q_mev + overall_threshold(q_mev, m_x, m_X, m_y, m_Y,
                                     Z_x, A_x, Z_X, A_X, r0_fm)


# --- neutron scattering kinematics  [S&F Eq. (6.25), printed p. 148] ------

def scattering_energy(A, e_in, theta_s_rad, q_mev=0.0, branch="+"):
    """Scattered-neutron energy E' from the general Eq. (6.25):

        E' = { sqrt(E) cos(t) +- sqrt[ E(A^2 - 1 + cos^2 t) + A(A+1)Q ] }^2
             / (A+1)^2 ,

    with A = M/m_n the scatterer's mass number.  Q = 0 is elastic scattering, for
    which only the '+' root is physical; Q < 0 is inelastic scattering leaving the
    nucleus in an excited state, and just above its threshold BOTH roots are real
    -- the double-energy region, where one scattering angle gives two possible
    outgoing energies.  Returns None when the root is complex, i.e. when the
    reaction cannot occur at that angle and energy."""
    if A < 1:
        raise ValueError("mass number must be at least 1")
    if e_in < 0:
        raise ValueError("incident energy must be non-negative")
    if branch not in ("+", "-"):
        raise ValueError("branch must be '+' or '-'")
    c = math.cos(theta_s_rad)
    disc = e_in * (A * A - 1.0 + c * c) + A * (A + 1.0) * q_mev
    if disc < 0:
        return None
    root = math.sqrt(e_in) * c + (1.0 if branch == "+" else -1.0) * math.sqrt(disc)
    if root < 0:
        return None
    return root ** 2 / (A + 1.0) ** 2


def elastic_scattering_energy_ratio(A, theta_s_rad):
    """E'/E for a neutron scattered elastically through lab angle theta_s
    [Eq. (6.25) with Q = 0]:

        E'/E = [cos(theta) + sqrt(A^2 - 1 + cos^2(theta))]^2 / (A+1)^2 .

    Runs from 1 at forward scattering to alpha = ((A-1)/(A+1))^2 at 180 degrees.
    Independent of E, which is what makes alpha and xi energy-independent."""
    r = scattering_energy(A, 1.0, theta_s_rad, 0.0, "+")
    return 0.0 if r is None else r


def alpha_collision(A):
    """alpha = ((A-1)/(A+1))^2, the minimum fraction of its energy a neutron can
    retain in one elastic collision.

    alpha = 0 for hydrogen (a neutron can be stopped dead in a single hit) and
    0.983 for 238U (a neutron loses at most 1.7%).  The single most important
    number in moderator selection (~NE-19)."""
    if A < 1:
        raise ValueError("mass number must be at least 1")
    return ((A - 1.0) / (A + 1.0)) ** 2


def max_fractional_energy_loss(A):
    """1 - alpha: the largest fraction of its energy a neutron can lose in one
    elastic collision (a head-on hit)."""
    return 1.0 - alpha_collision(A)


def mean_energy_after_collision(A, e_in=1.0):
    """Average energy after one elastic collision, E_out = E_in (1+alpha)/2.

    Scattering is isotropic in the centre-of-mass frame for low-energy neutrons,
    which makes E' uniform on [alpha E, E] in the laboratory -- so the mean is
    the midpoint."""
    return e_in * (1.0 + alpha_collision(A)) / 2.0


def average_log_energy_decrement(A):
    """xi = <ln(E/E')>, the mean logarithmic energy decrement per collision:

        xi = 1 + alpha ln(alpha)/(1 - alpha),      xi = 1 exactly for A = 1.

    Constant with energy, which is what makes it the natural currency for
    counting collisions during moderation (~NE-13, ~NE-19)."""
    if A < 1:
        raise ValueError("mass number must be at least 1")
    if A == 1:
        return 1.0
    a = alpha_collision(A)
    return 1.0 + a * math.log(a) / (1.0 - a)


def collisions_to_thermalize(A, e_start_mev=2.0, e_end_ev=0.0253):
    """Mean number of elastic collisions to slow a neutron from fission energy
    to thermal:  n = ln(E_start/E_end) / xi ."""
    if e_start_mev <= 0 or e_end_ev <= 0:
        raise ValueError("energies must be positive")
    return math.log(e_start_mev * 1e6 / e_end_ev) / average_log_energy_decrement(A)


def max_lab_scattering_angle(m_x, m_X):
    """Maximum laboratory scattering angle of the projectile, in radians:

        pi                 if m_X >= m_x   (any angle, including backscatter)
        asin(m_X/m_x)      if m_X <  m_x .

    A light target cannot turn a heavy projectile around -- the reason a
    heavy-ion beam stays forward-directed, and the reason a neutron CAN be
    backscattered by anything (m_X >= m_n for every nuclide)."""
    if m_x <= 0 or m_X <= 0:
        raise ValueError("masses must be positive")
    if m_X >= m_x:
        return math.pi
    return math.asin(m_X / m_x)


def recoil_energy(A, e_in, theta_s_rad):
    """Energy given to the recoiling nucleus in an elastic neutron collision."""
    return e_in * (1.0 - elastic_scattering_energy_ratio(A, theta_s_rad))


# --- heavy particle on an electron  [S&F §6.4.3, Eqs. (6.21)-(6.22)] ------

def electron_recoil_energy(e_heavy_mev, m_heavy_u, theta_e_rad):
    """Energy handed to a struck free electron  [Eq. (6.21)]:

        E_e = 4 (m_e/M) E_M cos^2(theta_e) .

    The same binary kinematics as above, with the mass ratio now enormous."""
    if m_heavy_u <= 0:
        raise ValueError("projectile mass must be positive")
    return 4.0 * (M_E_U / m_heavy_u) * e_heavy_mev * math.cos(theta_e_rad) ** 2


def max_electron_recoil_energy(e_heavy_mev, m_heavy_u):
    """Largest possible loss in one electron collision  [Eq. (6.22)]:
    4(m_e/M)E_M, reached at theta_e = 0.

    For a 4 MeV alpha this is 2.2 keV out of 4 MeV -- so a heavy charged particle
    must make tens of thousands of collisions to stop, and travels in almost a
    straight line while doing it (~NE-14)."""
    return electron_recoil_energy(e_heavy_mev, m_heavy_u, 0.0)


# --- demo --------------------------------------------------------------------

def _demo():
    t = load_atomic_masses()
    print("NE-08  binary kinematics, thresholds and barriers\n")

    print("  the threshold exceeds |Q| by the centre-of-mass share")
    print("   reaction               Q       |Q|     E_th(exact)  E_th(approx)  excess")
    cases = [("16O(n,a)13C", (1, 0), (16, 8), (4, 2), (13, 6)),
             ("14N(n,p)14C", (1, 0), (14, 7), (1, 1), (14, 6)),
             ("9Be(a,n)12C", (4, 2), (9, 4), (1, 0), (12, 6)),
             ("3H(p,n)3He", (1, 1), (3, 1), (1, 0), (3, 2))]
    for name, x, X, y, Y in cases:
        mx = M_N_U if x == (1, 0) else atomic_mass(*x, table=t)
        mX = atomic_mass(*X, table=t)
        my = M_N_U if y == (1, 0) else atomic_mass(*y, table=t)
        mY = atomic_mass(*Y, table=t)
        Q = q_value_masses(mx, mX, my, mY)
        ex = threshold_energy(Q, mx, my, mY)
        ap = threshold_energy_approx(Q, mx, mX)
        print("   %-14s %+8.4f %8.4f  %10.4f  %11.4f  %+6.2f%%"
              % (name, Q, abs(Q), ex, ap,
                 100 * (ex / abs(Q) - 1) if Q < 0 else 0.0))

    print("\n  Coulomb barriers: neutrons feel none")
    print("   projectile + target      V_C (MeV)")
    for Zx, Ax, ZX, AX, lab in [(0, 1, 92, 235, "n + 235U"), (1, 1, 6, 12, "p + 12C"),
                                (1, 2, 1, 3, "d + t"), (2, 4, 4, 9, "alpha + 9Be"),
                                (2, 4, 92, 238, "alpha + 238U")]:
        print("   %-22s %9.3f" % (lab, coulomb_barrier(Zx, Ax, ZX, AX)))

    print("\n  elastic neutron scattering: the moderator table")
    print("   nuclide    A     alpha    max loss   <E'/E>     xi    collisions 2 MeV->thermal")
    for A, lab in [(1, "1H"), (2, "2H"), (9, "9Be"), (12, "12C"),
                   (16, "16O"), (23, "23Na"), (56, "56Fe"), (238, "238U")]:
        print("   %-9s %4d  %8.4f  %8.4f  %8.4f  %6.4f  %10.1f"
              % (lab, A, alpha_collision(A), max_fractional_energy_loss(A),
                 mean_energy_after_collision(A), average_log_energy_decrement(A),
                 collisions_to_thermalize(A)))

    print("\n  the other extreme: a heavy particle striking a free electron")
    print("   projectile          E (MeV)   max loss to one electron")
    for m, lab, E in [(4.0026032, "alpha", 4.0), (1.00727647, "proton", 4.0),
                      (238.05079, "238U ion", 100.0)]:
        print("   %-18s %7.1f   %10.4f keV"
              % (lab, E, 1e3 * max_electron_recoil_energy(E, m)))

    print("\n  a single collision, as a function of angle (A = 12, carbon)")
    print("   angle (deg)   E'/E")
    for deg in (0, 30, 60, 90, 120, 150, 180):
        print("   %9d   %7.4f" % (deg, elastic_scattering_energy_ratio(12, math.radians(deg))))


if __name__ == "__main__":
    _demo()
