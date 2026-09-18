"""Tests for CM-10 circular motion. Reuses MA-01/CM-01 (imported transitively).

Run:  python3 test_circular_motion.py     ->  "All N tests passed."
"""
import math

from circular_motion import (
    uniform_circular, centripetal_acceleration, centripetal_force,
    period, frequency, angular_velocity,
)
from kinematics import speed, curvature, normal_acceleration, acceleration
from vector_algebra import norm


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_centripetal_relations():
    assert _approx(centripetal_acceleration(6.0, 2.0), 18.0)            # v^2/R
    assert _approx(centripetal_acceleration(2.0 * 3.0, 2.0), 3.0 ** 2 * 2.0)   # = omega^2 R
    assert _approx(centripetal_force(1.5, 6.0, 2.0), 1.5 * 18.0)        # m v^2/R


def test_period_frequency():
    w = 3.0
    assert _approx(period(w), 2 * math.pi / 3)
    assert _approx(frequency(w), 3 / (2 * math.pi))
    assert _approx(angular_velocity(period(w)), w)                      # round trip


def test_matches_CM01_on_trajectory():
    R, w = 2.0, 3.0
    v = R * w
    circ = uniform_circular(R, w)
    for t in (0.0, 0.4, 1.1):
        assert _approx(norm(circ(t)), R)                               # stays on the circle
        assert _approx(speed(circ)(t), v, tol=1e-5)                    # |v| = R omega
        assert _approx(curvature(circ)(t), 1.0 / R, tol=1e-3)          # kappa = 1/R
        assert _approx(normal_acceleration(circ)(t), centripetal_acceleration(v, R), tol=1e-2)


def test_acceleration_points_to_centre():
    R, w = 2.0, 3.0
    circ = uniform_circular(R, w)
    a = acceleration(circ)
    for t in (0.2, 0.9, 1.5):
        rt = circ(t)
        assert _vapprox(a(t), tuple(-w * w * c for c in rt), tol=1e-2)  # a = -omega^2 r (inward)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
