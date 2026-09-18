"""Tests for CM-12 rotating frames. Reuses MA-01 (imported transitively).

Run:  python3 test_rotating_frames.py     ->  "All N tests passed."
"""
import math

from rotating_frames import (
    centrifugal_acceleration, coriolis_acceleration, euler_acceleration,
    centrifugal_force, coriolis_force,
)
from vector_algebra import dot, norm


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def _vapprox(u, v, tol=1e-9):
    return all(_approx(a, b, tol) for a, b in zip(u, v))


def test_centrifugal_points_outward():
    w = 2.0
    omega = (0.0, 0.0, w)
    for x, y in ((3.0, 0.0), (0.0, 4.0), (1.0, 1.0)):
        a = centrifugal_acceleration(omega, (x, y, 0.0))
        assert _vapprox(a, (w * w * x, w * w * y, 0.0))           # = omega^2 * r_perp, outward
        assert _approx(norm(a), w * w * math.hypot(x, y))         # magnitude omega^2 rho


def test_centrifugal_ignores_parallel_component():
    omega = (0.0, 0.0, 3.0)
    a = centrifugal_acceleration(omega, (2.0, 0.0, 5.0))          # z-part is along omega
    assert _vapprox(a, (3.0 ** 2 * 2.0, 0.0, 0.0))               # only the perpendicular part matters


def test_coriolis_perpendicular():
    omega = (0.0, 0.0, 2.0)
    for v in ((1.0, 0.0, 0.0), (0.0, 1.0, 0.0), (1.0, 2.0, 3.0)):
        a = coriolis_acceleration(omega, v)
        assert _approx(dot(a, omega), 0.0)                        # perp to omega
        assert _approx(dot(a, v), 0.0)                            # perp to v
        assert _approx(norm(a), 2.0 * norm(omega) * math.hypot(v[0], v[1]))   # 2|omega||v_perp|


def test_centripetal_balance_in_corotating_frame():
    # a particle fixed in the rotating frame (v_rot=0) needs a real centripetal force;
    # in the rotating frame the centrifugal term is what "balances" it (equal & opposite)
    omega = (0.0, 0.0, 1.5)
    r = (2.0, 0.0, 0.0)
    centrifugal = centrifugal_acceleration(omega, r)
    centripetal = tuple(-c for c in centrifugal)                  # real inward acceleration
    assert _vapprox(centripetal, (-1.5 ** 2 * 2.0, 0.0, 0.0))     # = -omega^2 r (toward centre)


def test_force_versions_scale_with_mass():
    omega, r, v, m = (0, 0, 2.0), (3, 0, 0), (0, 1, 0), 2.5
    assert _vapprox(centrifugal_force(m, omega, r),
                    tuple(m * c for c in centrifugal_acceleration(omega, r)))
    assert _vapprox(coriolis_force(m, omega, v),
                    tuple(m * c for c in coriolis_acceleration(omega, v)))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
