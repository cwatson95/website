"""NE-08 tests -- binary reaction kinematics against Shultis & Faw §§6.1-6.5
and the atomic masses of Appendix B.

Run:  python3 test_binary_kinematics.py
"""

import math

from binary_kinematics import (
    M_N_U, M_H_U, M_E_U, U_MEV, COULOMB_MEV_FM, R0_FM,
    load_atomic_masses, atomic_mass, has_nuclide,
    q_value_masses, threshold_energy, threshold_energy_approx,
    coulomb_barrier, closest_approach, overall_threshold, minimum_product_energy,
    cm_kinetic_energy, cm_velocity_fraction,
    scattering_energy, elastic_scattering_energy_ratio, alpha_collision,
    max_fractional_energy_loss, mean_energy_after_collision,
    average_log_energy_decrement, collisions_to_thermalize,
    max_lab_scattering_angle, recoil_energy,
    electron_recoil_energy, max_electron_recoil_energy,
)

TAB = load_atomic_masses()


def _approx(a, b, tol=1e-9):
    return abs(a - b) <= tol * max(1.0, abs(a), abs(b))


def _m(A, Z):
    """Mass in u; the free neutron is not in Appendix B's atomic-mass table."""
    return M_N_U if (A, Z) == (1, 0) else atomic_mass(A, Z, table=TAB)


def _reaction(x, X, y, Y):
    """(Q, m_x, m_X, m_y, m_Y) for a reaction given as (A, Z) pairs."""
    mx, mX, my, mY = _m(*x), _m(*X), _m(*y), _m(*Y)
    return q_value_masses(mx, mX, my, mY), mx, mX, my, mY


# --- the kinematic threshold  [Eqs. (6.14)-(6.15)] --------------------------

def test_endoergic_threshold_exceeds_the_q_value():
    """The projectile must supply |Q| AND the centre-of-mass motion the products
    are forced to keep.  Quoting |Q| is always an underestimate."""
    for x, X, y, Y in [((1, 0), (16, 8), (4, 2), (13, 6)),
                       ((1, 1), (3, 1), (1, 0), (3, 2)),
                       ((1, 1), (7, 3), (1, 0), (7, 4))]:
        Q, mx, mX, my, mY = _reaction(x, X, y, Y)
        assert Q < 0
        assert threshold_energy(Q, mx, my, mY) > abs(Q)


def test_known_thresholds():
    """Two thresholds that appear in every reaction-physics table."""
    Q, mx, mX, my, mY = _reaction((1, 1), (3, 1), (1, 0), (3, 2))     # 3H(p,n)3He
    assert _approx(Q, -0.7638, tol=1e-3)
    assert _approx(threshold_energy(Q, mx, my, mY), 1.0189, tol=1e-3)

    Q, mx, mX, my, mY = _reaction((1, 0), (16, 8), (4, 2), (13, 6))   # 16O(n,a)13C
    assert _approx(Q, -2.2156, tol=1e-3)
    assert _approx(threshold_energy(Q, mx, my, mY), 2.3553, tol=1e-3)

    # 7Li(p,n)7Be -- a neutron-metrology calibration standard at 1.8804 MeV.
    # S&F §6.4.2 prints 1.875, which its own masses do not reproduce; see refs.md.
    Q, mx, mX, my, mY = _reaction((1, 1), (7, 3), (1, 0), (7, 4))
    assert _approx(Q, -1.6442, tol=1e-3)
    assert _approx(threshold_energy(Q, mx, my, mY), 1.8803, tol=1e-3)
    assert not _approx(threshold_energy(Q, mx, my, mY), 1.875, tol=1e-3)


def test_exact_and_approximate_thresholds_agree():
    """Eq. (6.15) drops terms of order Q/(m c^2), so it should track Eq. (6.14)
    to a part in 10^4 -- far below any experimental beam-energy resolution."""
    for x, X, y, Y in [((1, 0), (16, 8), (4, 2), (13, 6)),
                       ((1, 1), (3, 1), (1, 0), (3, 2)),
                       ((1, 1), (7, 3), (1, 0), (7, 4))]:
        Q, mx, mX, my, mY = _reaction(x, X, y, Y)
        ex = threshold_energy(Q, mx, my, mY)
        ap = threshold_energy_approx(Q, mx, mX)
        assert _approx(ex, ap, tol=2e-4), "%.6f vs %.6f" % (ex, ap)


def test_exoergic_reactions_have_no_kinematic_threshold():
    """Q > 0 means the reaction can proceed with a projectile at rest -- 14N(n,p)
    and 9Be(alpha,n) both run on thermal/room-temperature particles."""
    for x, X, y, Y in [((1, 0), (14, 7), (1, 1), (14, 6)),
                       ((4, 2), (9, 4), (1, 0), (12, 6)),
                       ((2, 1), (2, 1), (1, 0), (3, 2))]:
        Q, mx, mX, my, mY = _reaction(x, X, y, Y)
        assert Q > 0
        assert threshold_energy(Q, mx, my, mY) == 0.0
        assert threshold_energy_approx(Q, mx, mX) == 0.0


def test_threshold_excess_grows_with_projectile_to_target_ratio():
    """E_th/|Q| = 1 + m_x/m_X.  A neutron on 238U wastes almost nothing; a
    deuteron on a deuteron wastes half its energy on centre-of-mass motion."""
    Q = -5.0
    light = threshold_energy_approx(Q, M_N_U, 238.0) / abs(Q)
    heavy = threshold_energy_approx(Q, 2.0, 2.0) / abs(Q)
    assert _approx(light, 1.0 + M_N_U / 238.0)
    assert _approx(heavy, 2.0)
    assert light < heavy


# --- the centre-of-mass split  [§6.2] ---------------------------------------

def test_cm_energy_is_the_usable_fraction():
    """E_cm = E_lab m_X/(m_x+m_X); the remainder is locked in the motion of the
    centre of mass and can never drive a reaction."""
    e = 10.0
    for mx, mX in [(1.0, 1.0), (M_N_U, 12.0), (4.0, 238.0)]:
        ecm = cm_kinetic_energy(e, mx, mX)
        assert 0 < ecm < e
        assert _approx(ecm + e * mx / (mx + mX), e)
        assert _approx(cm_velocity_fraction(mx, mX), mx / (mx + mX))
    # equal masses: exactly half is usable
    assert _approx(cm_kinetic_energy(10.0, 2.0, 2.0), 5.0)
    # a heavy target barely recoils, so nearly all the energy is usable
    assert cm_kinetic_energy(10.0, M_N_U, 238.0) > 9.9


def test_threshold_delivers_exactly_the_q_value_in_the_cm_frame():
    """The defining statement of the threshold: at E_lab = E_th the
    centre-of-mass energy equals |Q| and the products are born at rest."""
    for x, X, y, Y in [((1, 0), (16, 8), (4, 2), (13, 6)),
                       ((1, 1), (7, 3), (1, 0), (7, 4))]:
        Q, mx, mX, my, mY = _reaction(x, X, y, Y)
        eth = threshold_energy_approx(Q, mx, mX)
        assert _approx(cm_kinetic_energy(eth, mx, mX), abs(Q), tol=1e-12)


# --- the Coulomb barrier  [§6.3.2] ------------------------------------------

def test_neutrons_feel_no_barrier():
    """Z_x = 0 gives V_C = 0 at every target -- the single fact that makes
    neutron-induced reactions the basis of reactor physics (~NE-13, ~NE-19)."""
    for ZX, AX in [(1, 1), (6, 12), (92, 235), (92, 238)]:
        assert coulomb_barrier(0, 1, ZX, AX) == 0.0
    assert closest_approach(1.0, 0, 92) == 0.0


def test_barrier_matches_the_books_1_20_mev_form():
    """Eq. (6.19) is quoted as E_C ~ 1.20 Z_x Z_X/(A_x^1/3 + A_X^1/3) MeV.  That
    numerator is e^2/(4 pi eps0 r0) with r0 = 1.2 fm from Eq. (1.7), so the two
    forms must be the same function -- and the book's own worked values pin it."""
    assert _approx(COULOMB_MEV_FM / R0_FM, 1.20, tol=3e-4)
    for Zx, Ax, ZX, AX in [(1, 2, 6, 13), (1, 1, 6, 14), (2, 4, 92, 238)]:
        R = R0_FM * (Ax ** (1 / 3.0) + AX ** (1 / 3.0))
        assert _approx(coulomb_barrier(Zx, Ax, ZX, AX), COULOMB_MEV_FM * Zx * ZX / R)
    # 7Li(p,n)7Be: S&F §6.4.2 quotes 1.236 MeV for the Coulomb threshold
    assert _approx(coulomb_barrier(1, 1, 3, 7), 1.236, tol=1e-3)


def test_barrier_scales_with_charge_and_shrinks_with_size():
    """Checked against a hand evaluation and against the published ordering."""
    vc = coulomb_barrier(2, 4, 92, 238)
    R = R0_FM * (4 ** (1 / 3.0) + 238 ** (1 / 3.0))
    assert _approx(vc, COULOMB_MEV_FM * 2 * 92 / R)
    assert _approx(vc, 28.363, tol=1e-4), "%.4f" % vc
    # d+t is the easiest fusion barrier; alpha on uranium is essentially closed
    assert (coulomb_barrier(1, 2, 1, 3) < coulomb_barrier(1, 1, 6, 12)
            < coulomb_barrier(2, 4, 4, 9) < vc)
    # doubling both charges quadruples the barrier at fixed radius
    assert _approx(coulomb_barrier(2, 4, 2, 4) / coulomb_barrier(1, 4, 1, 4), 4.0)


def test_reproduces_example_6_1():
    """S&F Example 6.1 (printed p. 144) tabulates Q, the Coulomb threshold, the
    kinematic threshold, which one governs, and the minimum product energy for
    three routes to the compound nucleus 15N*.  All four columns, all three rows.

    This is the strongest single check in the module: it exercises the Q-value,
    both thresholds, Eq. (6.20) and the product-energy identity at once, against
    numbers the authors published."""
    rows = [
        # reaction               x        X        y        Z_x A_x Z_X A_X
        ("13C(d,t)12C",    (2, 1), (13, 6), (3, 1), (12, 6), 1, 2, 6, 13,
         1.311, 1.994, 0.0, "C", 3.305),
        ("14C(p,n)14N",    (1, 1), (14, 6), (1, 0), (14, 7), 1, 1, 6, 14,
         -0.6259, 2.111, 0.6706, "C", 1.485),
        ("14N(n,a)11B",    (1, 0), (14, 7), (4, 2), (11, 5), 0, 1, 7, 14,
         -0.1582, 0.0, 0.1695, "K", 0.0113),
    ]
    for (name, x, X, y, Y, Zx, Ax, ZX, AX,
         q_exp, ec_exp, eth_exp, governs, prod_exp) in rows:
        Q, mx, mX, my, mY = _reaction(x, X, y, Y)
        assert _approx(Q, q_exp, tol=2e-3), "%s Q = %.4f" % (name, Q)

        ec = coulomb_barrier(Zx, Ax, ZX, AX)
        assert _approx(ec, ec_exp, tol=2e-3), "%s E_C = %.4f" % (name, ec)

        eth = threshold_energy(Q, mx, my, mY)
        assert _approx(eth, eth_exp, tol=3e-3), "%s E_th = %.4f" % (name, eth)

        ov = overall_threshold(Q, mx, mX, my, mY, Zx, Ax, ZX, AX)
        assert _approx(ov, max(ec_exp, eth_exp), tol=2e-3), name
        # which hurdle governs -- Coulomb for the two charged projectiles,
        # kinematic for the neutron
        assert (ec > eth) == (governs == "C"), name

        prod = minimum_product_energy(Q, mx, mX, my, mY, Zx, Ax, ZX, AX)
        assert _approx(prod, prod_exp, tol=5e-3), "%s min E = %.4f" % (name, prod)
        assert prod >= 0.0


def test_closest_approach_is_inverse_in_energy():
    """r_min = Z_x Z_X e^2/(4 pi eps0 E): ten times the energy gets ten times
    closer.  Rutherford's alphas on gold stopped ~30 fm out, well outside the
    ~7 fm nucleus -- which is why he saw pure Coulomb scattering."""
    r1 = closest_approach(1.0, 2, 79)
    r10 = closest_approach(10.0, 2, 79)
    assert _approx(r1 / r10, 10.0)
    assert _approx(closest_approach(7.7, 2, 79), COULOMB_MEV_FM * 2 * 79 / 7.7)
    assert 25.0 < closest_approach(7.7, 2, 79) < 35.0
    # using the CM energy always gives a larger (more conservative) distance
    assert closest_approach(7.7, 2, 79, m_x=4.0, m_X=197.0) > closest_approach(7.7, 2, 79)


def test_overall_threshold_takes_the_larger_requirement():
    """A charged-particle reaction can be strongly exoergic and still need an
    accelerator: 9Be(alpha,n)12C has Q = +5.7 MeV yet the alpha must climb a
    2.6 MeV barrier [Eq. (6.20)]."""
    Q, mx, mX, my, mY = _reaction((4, 2), (9, 4), (1, 0), (12, 6))
    assert Q > 0
    assert threshold_energy(Q, mx, my, mY) == 0.0
    vc = coulomb_barrier(2, 4, 4, 9)
    assert _approx(overall_threshold(Q, mx, mX, my, mY, 2, 4, 4, 9), vc)
    assert vc > 2.0
    # the barrier energy is not lost -- it reappears in the products
    assert _approx(minimum_product_energy(Q, mx, mX, my, mY, 2, 4, 4, 9), Q + vc)
    # for a neutron the barrier drops out and only the kinematics remain
    Q, mx, mX, my, mY = _reaction((1, 0), (16, 8), (4, 2), (13, 6))
    assert _approx(overall_threshold(Q, mx, mX, my, mY, 0, 1, 8, 16),
                   threshold_energy(Q, mx, my, mY))
    # and at that threshold the products are born with essentially no energy
    assert abs(minimum_product_energy(Q, mx, mX, my, mY, 0, 1, 8, 16)) < 0.15


# --- elastic scattering and moderation  [Eq. (6.25), §6.5] ------------------

def test_energy_ratio_spans_alpha_to_one():
    """E'/E = 1 at forward scattering and alpha at 180 degrees, monotonically
    decreasing in between [Eq. (6.25) with Q = 0]."""
    for A in (1, 2, 12, 238):
        assert _approx(elastic_scattering_energy_ratio(A, 0.0), 1.0)
        assert _approx(elastic_scattering_energy_ratio(A, math.pi), alpha_collision(A))
        prev = 1.0
        for deg in range(0, 181, 5):
            r = elastic_scattering_energy_ratio(A, math.radians(deg))
            assert r <= prev + 1e-12
            assert alpha_collision(A) - 1e-12 <= r <= 1.0 + 1e-12
            prev = r


def test_ninety_degree_scattering_has_a_closed_form():
    """At theta = 90 degrees Eq. (6.25) collapses to E'/E = (A-1)/(A+1)."""
    for A in (2, 9, 12, 56, 238):
        assert _approx(elastic_scattering_energy_ratio(A, math.pi / 2),
                       (A - 1.0) / (A + 1.0))


def test_hydrogen_can_stop_a_neutron_dead():
    """alpha(1H) = 0: a head-on collision with a proton transfers the entire
    neutron energy.  Nothing else in the table can do this."""
    assert _approx(alpha_collision(1), 0.0)
    assert _approx(max_fractional_energy_loss(1), 1.0)
    assert _approx(elastic_scattering_energy_ratio(1, math.pi), 0.0, tol=1e-12)
    assert _approx(recoil_energy(1, 2.0, math.pi), 2.0, tol=1e-12)


def test_alpha_values_match_the_standard_table():
    """alpha = ((A-1)/(A+1))^2 for the nuclides that matter in moderator choice."""
    for A, expect in [(1, 0.0), (2, 1 / 9.0), (9, 0.640), (12, 0.7160),
                      (16, 0.7785), (238, 0.9833)]:
        assert _approx(alpha_collision(A), expect, tol=1e-3), A
    # heavier target -> less energy lost per collision, always
    prev = -1.0
    for A in (1, 2, 4, 9, 12, 16, 56, 238):
        a = alpha_collision(A)
        assert a > prev
        prev = a
    assert _approx(max_fractional_energy_loss(238), 1.0 - alpha_collision(238))


def test_mean_energy_is_the_midpoint():
    """Isotropic CM scattering makes E' uniform on [alpha E, E], so the mean is
    E(1+alpha)/2 -- and a neutron keeps 99.2% of its energy on average when it
    hits 238U."""
    for A in (1, 2, 12, 238):
        assert _approx(mean_energy_after_collision(A, 2.0),
                       2.0 * (1.0 + alpha_collision(A)) / 2.0)
    assert _approx(mean_energy_after_collision(1), 0.5)
    assert _approx(mean_energy_after_collision(238), 0.99167, tol=1e-4)


def test_reproduces_table_6_1():
    """S&F Table 6.1 (printed p. 150) tabulates alpha, xi and the number of
    elastic scatters to slow a 2 MeV neutron to 0.025 eV.  Every entry for a
    single nuclide is reproduced here to the printed precision.  (The two
    compound entries, H2O and D2O, are mixtures and need the scattering cross
    sections of ~NE-13 to weight them, so they are out of scope.)"""
    table = [                       # A,    alpha,   xi,      n
        (1,   0.0,    1.0,     18.2),
        (2,   0.111,  0.725,   25.1),
        (4,   0.360,  0.425,   42.8),
        (9,   0.640,  0.207,   88.1),
        (12,  0.716,  0.158,   115.0),
        (238, 0.983,  0.0084,  2172.0),
    ]
    for A, a, xi, n in table:
        assert _approx(alpha_collision(A), a, tol=2e-3), "alpha(%d)" % A
        assert _approx(average_log_energy_decrement(A), xi, tol=6e-3), "xi(%d)" % A
        got = collisions_to_thermalize(A, e_start_mev=2.0, e_end_ev=0.025)
        assert _approx(got, n, tol=3e-3), "n(%d): %.1f vs %.1f" % (A, got, n)


def test_xi_matches_the_published_moderator_table():
    """xi = 1 + alpha ln(alpha)/(1-alpha) [Eq. (6.29)] -- the numbers quoted in
    every reactor-physics text."""
    for A, expect in [(1, 1.000), (2, 0.725), (12, 0.158), (16, 0.120),
                      (238, 0.00838)]:
        assert _approx(average_log_energy_decrement(A), expect, tol=5e-3), A
    assert average_log_energy_decrement(1) == 1.0          # exact, not a limit
    # xi is continuous at A = 1: approach it from above
    assert _approx(average_log_energy_decrement(1.0001), 1.0, tol=1e-3)
    # and it falls monotonically with mass
    prev = 2.0
    for A in (1, 2, 9, 12, 16, 56, 238):
        xi = average_log_energy_decrement(A)
        assert 0 < xi < prev
        prev = xi


def test_collisions_to_thermalize():
    """n = ln(E0/E1)/xi.  Hydrogen thermalises a 2 MeV fission neutron in ~18
    collisions, graphite needs ~115, and 238U would need over 2000 -- which is
    why nobody moderates with uranium."""
    for A, expect in [(1, 18.186), (2, 25.072), (9, 88.023), (12, 115.267),
                      (238, 2170.15)]:
        assert _approx(collisions_to_thermalize(A), expect, tol=1e-4), A
    # the count is inversely proportional to xi and logarithmic in the range
    assert _approx(collisions_to_thermalize(12) * average_log_energy_decrement(12),
                   math.log(2e6 / 0.0253))
    assert collisions_to_thermalize(12, e_start_mev=1.0) < collisions_to_thermalize(12)


def test_recoil_energy_conserves_the_collision():
    """E_recoil = E - E'; it is zero for forward scattering and maximal at 180
    degrees, where it equals (1-alpha)E."""
    E, A = 2.0, 12
    assert _approx(recoil_energy(A, E, 0.0), 0.0, tol=1e-12)
    assert _approx(recoil_energy(A, E, math.pi), E * max_fractional_energy_loss(A))
    for deg in (30, 90, 150):
        th = math.radians(deg)
        assert _approx(recoil_energy(A, E, th)
                       + E * elastic_scattering_energy_ratio(A, th), E)


def test_hydrogen_forbids_backscatter():
    """S&F Example 6.3: for A = 1 the kinematics reduce to E'/E = cos^2(theta_s)
    with 0 <= theta_s <= pi/2 -- a neutron cannot bounce back off a proton, the
    result 'well known to every pool player'."""
    for deg in (0, 30, 45, 60, 89):
        th = math.radians(deg)
        assert _approx(elastic_scattering_energy_ratio(1, th), math.cos(th) ** 2)
    for deg in (91, 120, 180):
        assert _approx(elastic_scattering_energy_ratio(1, math.radians(deg)),
                       0.0, tol=1e-12)


def test_a_heavy_particle_barely_notices_an_electron():
    """Eq. (6.22): the most a 4 MeV alpha can lose to one electron is
    4(m_e/M)E = 2.2 keV -- S&F Example 6.2.  Tens of thousands of such
    collisions are needed to stop it (~NE-14)."""
    loss = max_electron_recoil_energy(4.0, 4.0026032)
    assert _approx(loss * 1e3, 2.19, tol=5e-3), "%.4f keV" % (loss * 1e3)
    assert loss / 4.0 < 1e-3
    # cos^2 falloff, and zero for a grazing 90-degree recoil
    assert _approx(electron_recoil_energy(4.0, 4.0026032, math.pi / 3), loss / 4.0)
    assert _approx(electron_recoil_energy(4.0, 4.0026032, math.pi / 2), 0.0, tol=1e-12)
    # a proton loses twice as large a fraction as an alpha of the same energy
    assert _approx(max_electron_recoil_energy(4.0, 1.00728)
                   / max_electron_recoil_energy(4.0, 4.0026032), 4.0026032 / 1.00728)


def test_a_neutron_can_always_be_backscattered():
    """m_X >= m_n for every nuclide, so the laboratory angle is unrestricted --
    unlike a heavy projectile on a light target, which stays forward-directed."""
    assert _approx(max_lab_scattering_angle(M_N_U, 12.0), math.pi)
    assert _approx(max_lab_scattering_angle(1.0, 1.0), math.pi)
    assert _approx(max_lab_scattering_angle(4.0, 1.0), math.asin(0.25))
    assert max_lab_scattering_angle(238.0, 1.0) < math.radians(1.0)


def test_the_neutron_detection_reaction():
    """S&F §6.4.1: 3He(n,p)3H, the workhorse neutron-detection reaction.  Q =
    0.764 MeV, and a thermal neutron gives the proton 0.573 MeV and the triton
    0.191 MeV -- the ionization that a 3He counter actually measures (~NE-15)."""
    Q, mn, m3he, mp, m3h = _reaction((1, 0), (3, 2), (1, 1), (3, 1))
    assert _approx(Q, 0.764, tol=1e-3), "%.4f" % Q
    assert coulomb_barrier(0, 1, 2, 3) == 0.0          # no threshold at all
    assert threshold_energy(Q, mn, mp, m3h) == 0.0
    # with a negligible-energy neutron the products share Q by inverse mass
    assert _approx(Q * m3h / (mp + m3h), 0.573, tol=2e-3)
    assert _approx(Q * mp / (mp + m3h), 0.191, tol=3e-3)


def test_inelastic_scattering_and_the_double_energy_region():
    """The general Eq. (6.25) with Q < 0.  For the 4.439 MeV first excited state
    of 12C the threshold is 4.81 MeV, and in a narrow window above it BOTH roots
    are real: one scattering angle, two possible outgoing energies."""
    Q = -4.439
    th45 = math.radians(45)
    # elastic is the Q = 0 special case, and only the '+' root survives.  For
    # A = 1 past 90 degrees even that root goes negative -- the no-backscatter
    # result -- and the ratio helper reports it as zero.
    for A in (1, 12, 238):
        for deg in (0, 45, 120):
            r = scattering_energy(A, 2.0, math.radians(deg), 0.0, "+")
            assert _approx(0.0 if r is None else r,
                           2.0 * elastic_scattering_energy_ratio(A, math.radians(deg)))
    assert scattering_energy(1, 2.0, math.radians(120), 0.0, "+") is None
    # below threshold the reaction simply cannot happen
    assert scattering_energy(12, 4.0, th45, Q, "+") is None
    # inside the window both roots are real and distinct
    hi = scattering_energy(12, 4.83, th45, Q, "+")
    lo = scattering_energy(12, 4.83, th45, Q, "-")
    assert hi is not None and lo is not None and hi > lo > 0
    # above the window only the '+' root remains
    assert scattering_energy(12, 8.0, th45, Q, "-") is None
    assert _approx(scattering_energy(12, 8.0, th45, Q, "+"), 3.2242, tol=1e-3)
    # the window is bounded above by E = -AQ/(A-1), a couple of tens of keV wide
    assert _approx(-12 * Q / 11.0, 4.8425, tol=1e-4)
    assert scattering_energy(12, 4.9, th45, Q, "-") is None


# --- table sanity and input validation --------------------------------------

def test_masses_and_constants():
    assert has_nuclide(12, 6) and has_nuclide(238, 92)
    assert _approx(atomic_mass(12, 6, table=TAB), 12.0, tol=1e-12)
    assert M_N_U > M_H_U                            # the neutron is the heavier one
    assert _approx(q_value_masses(M_N_U, 0.0, M_H_U, 0.0), 0.7823, tol=1e-3)
    # Table A.1 and Appendix B quote slightly different neutron masses -- 7.7e-9 u,
    # about 7 eV.  Documented in ~NE-03; far below anything this module resolves.
    assert has_nuclide(1, 0)
    assert abs(atomic_mass(1, 0, table=TAB) - M_N_U) * U_MEV < 1e-5


def test_invalid_inputs_raise():
    bad = [(threshold_energy, (-1.0, 1.0, 0.4, 0.5)),      # m_y+m_Y-m_x <= 0
           (threshold_energy_approx, (-1.0, 1.0, 0.0)),
           (cm_kinetic_energy, (1.0, 0.0, 1.0)),
           (coulomb_barrier, (1, 0, 1, 1)),
           (closest_approach, (0.0, 2, 79)),
           (alpha_collision, (0.5,)),
           (average_log_energy_decrement, (0.0,)),
           (collisions_to_thermalize, (12, 0.0)),
           (elastic_scattering_energy_ratio, (0.5, 0.0)),
           (max_lab_scattering_angle, (1.0, 0.0))]
    for fn, args in bad:
        try:
            fn(*args)
        except ValueError:
            pass
        else:
            raise AssertionError("%s%r should be rejected" % (fn.__name__, args))


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
