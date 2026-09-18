"""Tests for CM-01 kinematics. Reuses MA-01 vector algebra (imported transitively).

Run directly:   python3 test_kinematics.py        (-> "All N tests passed.")
Or with pytest: pytest test_kinematics.py
"""
import math

from kinematics import (
    velocity, acceleration, speed, curvature, radius_of_curvature,
    tangential_acceleration, normal_acceleration,
    uniform_acceleration, projectile, time_of_flight, range_, max_height,
    polar_position, polar_acceleration_components,
)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=TOL):
    return all(_approx(ui, vi, tol) for ui, vi in zip(u, v))


def test_velocity_acceleration_of_polynomial():
    # r(t) = (t, t^2, t^3)  ->  v = (1, 2t, 3t^2),  a = (0, 2, 6t)
    r = lambda t: (t, t ** 2, t ** 3)
    v, a = velocity(r), acceleration(r)
    for t in (-1.3, 0.0, 0.7, 2.0):
        assert _vapprox(v(t), (1.0, 2 * t, 3 * t * t), tol=1e-5)
        assert _vapprox(a(t), (0.0, 2.0, 6 * t), tol=1e-3)


def test_speed_is_a_function():
    r = lambda t: (3.0 * t, 4.0 * t, 0.0)            # constant velocity (3,4,0)
    sp = speed(r)
    for t in (0.0, 1.0, 5.0):
        assert _approx(sp(t), 5.0, tol=1e-5)         # |(3,4,0)| = 5


def test_projectile_gravity_range_apex():
    v0, ang, g = 25.0, math.radians(35.0), 9.81
    r = projectile(v0, ang, g)
    a = acceleration(r)
    for t in (0.1, 0.9, 1.7):
        assert _vapprox(a(t), (0.0, 0.0, -g), tol=1e-2)
    tof = time_of_flight(v0, ang, g)
    land = r(tof)
    assert _approx(land[2], 0.0, tol=1e-6)                       # returns to z=0
    assert _approx(land[0], range_(v0, ang, g), tol=1e-6)        # range matches
    assert _approx(r(tof / 2)[2], max_height(v0, ang, g), tol=1e-6)   # apex matches


def test_uniform_acceleration_matches_projectile():
    g = 9.81
    r1 = projectile(30.0, math.radians(50.0), g)
    v0 = (30.0 * math.cos(math.radians(50.0)), 0.0, 30.0 * math.sin(math.radians(50.0)))
    r2 = uniform_acceleration((0.0, 0.0, 0.0), v0, (0.0, 0.0, -g))
    for t in (0.0, 1.2, 2.5):
        assert _vapprox(r1(t), r2(t))


def test_uniform_circular_motion():
    R, w = 2.0, 3.0
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    sp, kap = speed(circ), curvature(circ)
    aN, aT, a = normal_acceleration(circ), tangential_acceleration(circ), acceleration(circ)
    for t in (0.0, 0.4, 1.1):
        assert _approx(sp(t), R * w, tol=1e-5)               # |v| = R omega
        assert _approx(kap(t), 1.0 / R, tol=1e-3)            # curvature = 1/R
        assert _approx(aN(t), (R * w) ** 2 / R, tol=1e-2)    # a_N = v^2/R
        assert _approx(aT(t), 0.0, tol=1e-2)                 # speed constant
        rt = circ(t)
        assert _vapprox(a(t), tuple(-w * w * rt[i] for i in range(3)), tol=1e-2)  # a = -w^2 r


def test_radius_of_curvature_circle_and_line():
    R, w = 1.7, 2.5
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    Rc = radius_of_curvature(circ)
    for t in (0.0, 0.5, 1.3):
        assert _approx(Rc(t), R, tol=1e-2)
    line = lambda t: (1.0 + 2.0 * t, 3.0 - t, 4.0 * t)       # straight, constant v
    kap = curvature(line)
    for t in (0.0, 1.0, -2.0):
        assert _approx(kap(t), 0.0, tol=1e-3)                # straight line: kappa = 0


def test_polar_components_circle():
    R, w = 1.5, 2.0
    a_r, a_th = polar_acceleration_components(lambda t: R, lambda t: w * t)
    for t in (0.0, 0.5, 1.3):
        assert _approx(a_r(t), -R * w * w, tol=1e-3)         # centripetal -R w^2
        assert _approx(a_th(t), 0.0, tol=1e-3)               # no Coriolis here
    r = polar_position(lambda t: R, lambda t: w * t)
    assert _vapprox(r(0.0), (R, 0.0, 0.0))


def test_polar_components_spiral_has_coriolis():
    # rho(t) = 1 + t (growing radius), theta(t) = t  ->  a_theta = rho*0 + 2*1*1 = 2
    a_r, a_th = polar_acceleration_components(lambda t: 1.0 + t, lambda t: t)
    for t in (0.0, 0.7, 2.0):
        assert _approx(a_th(t), 2.0, tol=1e-3)               # Coriolis term 2 rho' theta'
        assert _approx(a_r(t), -(1.0 + t), tol=1e-3)         # 0 - rho*1^2


def test_reuses_MA01_cross_on_functions():
    # specific angular momentum  L(t) = r x v  comes straight from MA-01's cross,
    # applied to kinematics' velocity function.
    from vector_algebra import cross
    r = lambda t: (math.cos(t), math.sin(t), t)
    v = velocity(r)
    L = cross(r, v)                                          # a function of t
    for t in (0.2, 1.0, 2.5):
        assert _vapprox(L(t), cross(r(t), v(t)), tol=1e-6)


def _run():
    tests = [val for k, val in sorted(globals().items())
             if k.startswith("test_") and callable(val)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
