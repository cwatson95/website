"""Tests for CM-02 equation of motion. Reuses MA-07 (imported transitively).

Run:  python3 test_equation_of_motion.py     ->  "All N tests passed."
"""
import math

from equation_of_motion import (
    trajectory, constant_force, uniform_gravity, spring_force, linear_drag, sum_forces,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_free_particle_straight_line():
    # F = 0  ->  r(t) = r0 + v0 t
    ts, rs, vs = trajectory(constant_force((0, 0, 0)), 1.0, (1, 2, 3), (1, -1, 2), 0.0, 3.0, 100)
    for t, r in zip(ts, rs):
        assert _vapprox(r, (1 + t, 2 - t, 3 + 2 * t), tol=1e-6)


def test_constant_force_parabola():
    # uniform gravity: r(t) = r0 + v0 t + 1/2 a t^2,  a = (0,0,-g)
    m, g = 2.0, 9.81
    r0, v0 = (0.0, 0.0, 0.0), (10.0, 0.0, 10.0)
    ts, rs, vs = trajectory(uniform_gravity(m, g), m, r0, v0, 0.0, 2.0, 500)
    for t, r, v in zip(ts, rs, vs):
        exact = (r0[0] + v0[0] * t, r0[1] + v0[1] * t, r0[2] + v0[2] * t - 0.5 * g * t * t)
        assert _vapprox(r, exact, tol=1e-6)
        assert _vapprox(v, (v0[0], v0[1], v0[2] - g * t), tol=1e-6)


def test_spring_is_sho():
    # m x'' = -k x  ->  x = x0 cos(w t),  w = sqrt(k/m)
    m, k = 0.5, 8.0
    w = math.sqrt(k / m)
    ts, rs, vs = trajectory(spring_force(k), m, (1.0, 0.0, 0.0), (0.0, 0.0, 0.0), 0.0, 5.0, 5000)
    for t, r, v in zip(ts, rs, vs):
        assert _approx(r[0], math.cos(w * t), tol=1e-4)
        assert _approx(v[0], -w * math.sin(w * t), tol=1e-4)


def test_drag_reaches_terminal_velocity():
    # m z'' = -m g - b z'  ->  v_z -> -m g / b
    m, g, b = 1.0, 9.81, 0.5
    ts, rs, vs = trajectory(sum_forces(uniform_gravity(m, g), linear_drag(b)), m,
                            (0, 0, 0), (0, 0, 0), 0.0, 40.0, 4000)
    assert _approx(vs[-1][2], -m * g / b, tol=1e-3)


def test_sum_forces_superposes():
    # constant up-force exactly cancelling gravity -> no acceleration
    m, g = 1.0, 9.81
    net = sum_forces(uniform_gravity(m, g), constant_force((0, 0, m * g)))
    ts, rs, vs = trajectory(net, m, (0, 0, 5), (1, 0, 0), 0.0, 2.0, 200)
    for t, r in zip(ts, rs):
        assert _vapprox(r, (t, 0.0, 5.0), tol=1e-6)            # straight line, no fall


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
