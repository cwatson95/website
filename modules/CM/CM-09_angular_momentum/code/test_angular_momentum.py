"""Tests for CM-09 angular momentum & torque. Reuses MA-01/CM-01 (transitively).

Run:  python3 test_angular_momentum.py     ->  "All N tests passed."
"""
import math

from angular_momentum import angular_momentum, torque, angular_momentum_of, torque_rate


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-6):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_angular_momentum_and_torque():
    assert _vapprox(angular_momentum(2.0, (1, 0, 0), (0, 3, 0)), (0.0, 0.0, 6.0))
    assert _vapprox(torque((2, 0, 0), (0, 5, 0)), (0.0, 0.0, 10.0))


def test_central_force_zero_torque():
    # F parallel (or antiparallel) to r  ->  r x F = 0
    assert _vapprox(torque((2, 1, 0), (-4, -2, 0)), (0.0, 0.0, 0.0))
    assert _vapprox(torque((1, 2, 3), (2, 4, 6)), (0.0, 0.0, 0.0))


def test_circular_motion_L_constant():
    R, w, m = 2.0, 3.0, 1.5
    circ = lambda t: (R * math.cos(w * t), R * math.sin(w * t), 0.0)
    L = angular_momentum_of(m, circ)
    Lz = m * R * R * w
    for t in (0.0, 0.5, 1.3, 2.0):
        assert _vapprox(L(t), (0.0, 0.0, Lz), tol=1e-5)             # conserved, along +z


def test_dL_dt_equals_torque():
    # dL/dt = m d/dt(r x v) = r x (m a) = N  for any trajectory
    m = 1.5
    traj = lambda t: (t, t ** 2, t ** 3)
    L = angular_momentum_of(m, traj)
    N = torque_rate(m, traj)
    h = 1e-5
    for t in (0.5, 1.0, 1.7):
        dLdt = tuple((L(t + h)[i] - L(t - h)[i]) / (2 * h) for i in range(3))
        assert _vapprox(dLdt, N(t), tol=1e-3)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
