"""Tests for CM-03 reference frames. Pure stdlib.

Run:  python3 test_reference_frames.py     ->  "All N tests passed."
"""
import random

from reference_frames import (
    galilean_position, galilean_velocity, relative_velocity,
    cm_velocity, to_cm_frame, total_momentum,
)


def _approx(x, y, tol=1e-12):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-12):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_galilean_position_and_velocity():
    r, V, t = [5.0, 1.0, -2.0], [2.0, 0.0, 1.0], 3.0
    assert _vapprox(galilean_position(r, V, t), [5 - 6, 1 - 0, -2 - 3])
    v = [4.0, -1.0, 0.0]
    assert _vapprox(galilean_velocity(v, V), [2.0, -1.0, -1.0])


def test_relative_velocity_antisymmetric():
    rng = random.Random(0)
    for _ in range(100):
        a = [rng.uniform(-5, 5) for _ in range(3)]
        b = [rng.uniform(-5, 5) for _ in range(3)]
        rel = relative_velocity(a, b)
        assert _vapprox(rel, [-x for x in relative_velocity(b, a)])      # v_AB = -v_BA


def test_cm_velocity():
    # equal masses -> CM velocity is the average
    assert _vapprox(cm_velocity([1.0, 1.0], [[2, 0, 0], [4, 0, 0]]), [3.0, 0.0, 0.0])
    # 2:1 mass ratio
    assert _vapprox(cm_velocity([2.0, 1.0], [[3, 0, 0], [0, 0, 0]]), [2.0, 0.0, 0.0])


def test_cm_frame_has_zero_momentum():
    rng = random.Random(1)
    for _ in range(100):
        n = rng.randint(2, 5)
        masses = [rng.uniform(0.5, 4) for _ in range(n)]
        vels = [[rng.uniform(-3, 3) for _ in range(3)] for _ in range(n)]
        cm_vels = to_cm_frame(masses, vels)
        assert _vapprox(total_momentum(masses, cm_vels), [0.0, 0.0, 0.0], tol=1e-9)


def test_galilean_preserves_relative_velocity():
    # relative velocities are frame-independent (a Galilean invariant)
    va, vb, V = [3.0, 1.0, 0.0], [1.0, -2.0, 4.0], [5.0, 5.0, 5.0]
    assert _vapprox(relative_velocity(va, vb),
                    relative_velocity(galilean_velocity(va, V), galilean_velocity(vb, V)))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
