"""Tests for RE-12 geodesics & the variational principle.

Run directly:   python3 test_geodesics.py      (-> "All N tests passed.")
Or with pytest: pytest test_geodesics.py

These are property-based physics checks. Christoffel symbols and the variational
residual are finite-differenced (MA-17 / MA-13) and the worldlines are RK4-
integrated, so integrated/differenced quantities use LOOSE tolerances. Headlines:
flat geodesics are straight lines; the sphere's equator is a great circle (a
latitude is not); the Euler-Lagrange equation of the action reproduces the
Christoffel symbols; the inertial twin has maximal proper time; and Killing
symmetries (d_phi, d_t) give conserved angular momentum / energy along geodesics.
"""
import math

from geodesics import (
    geodesic_rhs, integrate_geodesic, lagrangian, action_length,
    euler_lagrange_gives_christoffel, is_geodesic, killing_conserved,
    minkowski_metric, schwarzschild_metric, sphere_metric,
)


def _approx(x, y, tol):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_flat_geodesic_is_a_straight_line():
    """Minkowski: Gamma = 0, so geodesic_rhs = 0, velocity is constant and the
    worldline is x(lam) = x0 + v0 lam exactly."""
    mink = minkowski_metric()
    x0, v0 = [0.0, 0.2, -0.5, 1.0], [1.3, 0.4, -0.2, 0.25]
    # geodesic_rhs vanishes identically in flat space, for any velocity
    assert all(abs(c) <= 1e-9 for c in geodesic_rhs(mink, [3.0, 1.0, -2.0, 5.0], v0))
    traj = integrate_geodesic(mink, x0, v0, dtau=0.4, steps=10)
    # velocity constant; position linear
    for x, v in traj:
        assert all(abs(v[i] - v0[i]) <= 1e-9 for i in range(4))
    xend, _ = traj[-1]
    lam = 0.4 * 10
    assert all(_approx(xend[i], x0[i] + v0[i] * lam, 1e-9) for i in range(4))
    # a uniformly-sampled straight line passes is_geodesic
    line = [[x0[i] + v0[i] * 0.4 * k for i in range(4)] for k in range(9)]
    assert is_geodesic(mink, line, dtau=0.4)


def test_sphere_equator_is_geodesic_latitude_is_not():
    """A great circle (the equator theta=pi/2) is a geodesic; a circle of latitude
    theta != pi/2 is not -- it needs a sideways force to stay on it."""
    s = sphere_metric(1.0)
    equator = [[math.pi / 2, 0.2 * k] for k in range(10)]
    assert is_geodesic(s, equator, dtau=0.2)
    for theta in (0.6, 1.0, 1.4):                      # any latitude off the equator
        latitude = [[theta, 0.2 * k] for k in range(10)]
        assert not is_geodesic(s, latitude, dtau=0.2)


def test_sphere_equatorial_geodesic_stays_on_great_circle():
    """Started on the equator moving in phi, the integrated geodesic stays at
    theta = pi/2 and keeps constant phidot (Gamma^theta_{phiphi} = 0 there)."""
    s = sphere_metric(1.0)
    traj = integrate_geodesic(s, [math.pi / 2, 0.0], [0.0, 1.0], dtau=0.2, steps=15)
    for x, v in traj:
        assert _approx(x[0], math.pi / 2, 1e-9)        # theta pinned to pi/2
        assert _approx(v[1], 1.0, 1e-6)                # phidot constant


def test_variational_equation_reproduces_christoffel():
    """The Euler-Lagrange equation of L = 1/2 g_{mu nu} xdot^mu xdot^nu (computed
    via MA-13) equals the geodesic RHS -Gamma xdot xdot (computed via MA-17).
    This is the variational <=> Christoffel equivalence."""
    cases = [
        (sphere_metric(1.0), [1.1, 0.5], [0.4, 0.9]),
        (sphere_metric(2.0), [0.8, 2.0], [-0.6, 0.7]),
        (schwarzschild_metric(1.0), [0.0, 8.0, math.pi / 2, 0.3], [1.0, 0.1, 0.05, 0.04]),
        (schwarzschild_metric(1.0), [0.0, 12.0, 1.1, 0.0], [1.2, -0.2, 0.03, 0.05]),
    ]
    for metric, x, v in cases:
        a_el = euler_lagrange_gives_christoffel(metric, x, v)
        a_g = geodesic_rhs(metric, x, v)
        for i in range(len(x)):
            assert abs(a_el[i] - a_g[i]) <= 1e-4 + 1e-3 * abs(a_g[i])


def test_lagrangian_is_half_inner_product():
    """L = 1/2 g_{mu nu} xdot^mu xdot^nu = 1/2 (xdot . xdot).  A unit timelike
    tangent gives L = -1/2 (mostly-plus signature)."""
    mink = minkowski_metric()
    # 4-velocity of a particle with 3-velocity beta: U = gamma(1, beta), U.U = -1
    beta = 0.6
    g = 1.0 / math.sqrt(1.0 - beta * beta)
    U = [g, g * beta, 0.0, 0.0]
    assert _approx(lagrangian(mink, [0, 0, 0, 0], U), -0.5, 1e-12)
    # an explicit spacelike example
    assert _approx(lagrangian(mink, [0, 0, 0, 0], [0.0, 2.0, 0.0, 0.0]), 2.0, 1e-12)


def test_affine_parameter_gives_constant_speed():
    """Along an affine geodesic the tangent norm 2L = g_{mu nu} xdot^mu xdot^nu is
    conserved -- the geodesic moves at constant 'speed'.  Checked on a tilted
    great circle of the sphere (theta and phidot both vary, but the norm does not)."""
    s = sphere_metric(1.0)
    traj = integrate_geodesic(s, [math.pi / 2, 0.0], [0.35, 1.0], dtau=0.15, steps=40)
    norms = [2.0 * lagrangian(s, x, v) for x, v in traj]
    assert (max(norms) - min(norms)) <= 1e-3
    assert _approx(norms[0], 0.35 ** 2 + 1.0 ** 2, 1e-9)   # = a^2(thetadot^2+sin^2 th phidot^2)


def test_null_geodesic_stays_null():
    """A light ray (null tangent, 2L = 0) integrated through Schwarzschild stays
    null -- the geodesic preserves the causal character of its tangent."""
    sch = schwarzschild_metric(1.0)
    r = 10.0
    f = 1.0 - 2.0 / r
    phid = 0.1
    tdot = r * phid / math.sqrt(f)             # -f tdot^2 + r^2 phid^2 = 0 (rdot = 0)
    x0, v0 = [0.0, r, math.pi / 2, 0.0], [tdot, 0.0, 0.0, phid]
    assert abs(2.0 * lagrangian(sch, x0, v0)) <= 1e-12
    traj = integrate_geodesic(sch, x0, v0, dtau=0.3, steps=40)
    assert max(abs(2.0 * lagrangian(sch, x, v)) for x, v in traj) <= 1e-4
    # the ray actually moves (non-trivial check)
    assert max(x[1] for x, v in traj) - r > 1.0


def test_maximal_aging_timelike_geodesic_has_longest_proper_time():
    """Between two timelike-separated events the straight (inertial) worldline -- a
    geodesic -- has the LONGEST proper time (RE-05's reversed triangle inequality).
    Proper time strictly decreases as the path is bent away from the geodesic."""
    mink = minkowski_metric()
    T = 10.0
    N = 20
    straight = [[T * k / N, 0.0, 0.0, 0.0] for k in range(N + 1)]
    tau0 = action_length(mink, straight)
    assert _approx(tau0, T, 1e-9)              # = sqrt(T^2)
    prev = tau0
    for amp in (0.5, 1.0, 2.0, 3.0):           # tent-shaped spatial detours, fixed endpoints
        bent = [[T * k / N, amp * (1.0 - abs(1.0 - 2.0 * k / N)), 0.0, 0.0]
                for k in range(N + 1)]
        tau = action_length(mink, bent)
        assert tau < prev                      # more bending -> less aging
        prev = tau


def test_killing_angular_momentum_conserved_on_sphere():
    """d_phi is a Killing vector of the round sphere, so L = g_{phiphi} phidot =
    sin^2(theta) phidot is conserved along ANY geodesic -- here a tilted great
    circle whose theta swings widely while L stays put."""
    s = sphere_metric(1.0)
    dphi = [0.0, 1.0]
    traj = integrate_geodesic(s, [math.pi / 2, 0.0], [0.35, 1.0], dtau=0.15, steps=40)
    Ls = [killing_conserved(s, dphi, x, v) for x, v in traj]
    thetas = [x[0] for x, v in traj]
    assert (max(thetas) - min(thetas)) > 0.5   # theta genuinely varies (non-trivial)
    assert (max(Ls) - min(Ls)) <= 1e-3         # yet L is conserved


def test_killing_energy_and_momentum_conserved_on_schwarzschild():
    """d_t and d_phi are Killing vectors of Schwarzschild, giving conserved energy
    E = -(1-2M/r) tdot and angular momentum L = r^2 phidot along an orbit whose r
    swings from 10 out past 12."""
    sch = schwarzschild_metric(1.0)
    dt, dphi = [1.0, 0.0, 0.0, 0.0], [0.0, 0.0, 0.0, 1.0]
    traj = integrate_geodesic(sch, [0.0, 10.0, math.pi / 2, 0.0], [1.2, 0.2, 0.0, 0.04],
                              dtau=0.2, steps=60)
    rs = [x[1] for x, v in traj]
    Es = [killing_conserved(sch, dt, x, v) for x, v in traj]
    Ls = [killing_conserved(sch, dphi, x, v) for x, v in traj]
    assert (max(rs) - min(rs)) > 2.0           # orbit is genuinely radial-varying
    assert (max(Es) - min(Es)) <= 1e-4         # energy conserved
    assert (max(Ls) - min(Ls)) <= 1e-4         # angular momentum conserved


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
