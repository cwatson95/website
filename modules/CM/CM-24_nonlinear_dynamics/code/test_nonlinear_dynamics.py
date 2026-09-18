"""Tests for CM-24 nonlinear dynamics. Reuses MA-22/MA-07 (imported transitively).

Run:  python3 test_nonlinear_dynamics.py     ->  "All N tests passed."
"""
import math

from nonlinear_dynamics import (
    classify_fixed_point, integrate_flow, pendulum_flow, van_der_pol, lyapunov_logistic,
)


def test_undamped_pendulum_fixed_points():
    f = pendulum_flow(0.0)
    assert classify_fixed_point(f, (0.0, 0.0)) == "center"          # bottom: neutral oscillation
    assert classify_fixed_point(f, (math.pi, 0.0)) == "saddle"      # top: unstable


def test_damped_pendulum_fixed_points():
    f = pendulum_flow(0.5)
    assert classify_fixed_point(f, (0.0, 0.0)) == "stable spiral"   # bottom: spirals to rest
    assert classify_fixed_point(f, (math.pi, 0.0)) == "saddle"      # top: still a saddle


def test_van_der_pol_limit_cycle():
    f = van_der_pol(1.0)
    amps = []
    for start in ((0.1, 0.0), (3.0, 0.0)):                          # inside and outside the cycle
        ts, ys = integrate_flow(f, start, 0.0, 60.0, 12000)
        amps.append(max(abs(s[0]) for s in ys[-3000:]))
    assert 1.8 < amps[0] < 2.3 and 1.8 < amps[1] < 2.3              # both reach the cycle
    assert abs(amps[0] - amps[1]) < 0.1                            # same attractor regardless of start


def test_logistic_lyapunov_is_chaotic():
    # reuse MA-22: at r=4 the logistic map is chaotic with Lyapunov exponent ln 2
    assert abs(lyapunov_logistic(4.0) - math.log(2)) < 1e-2
    # at r=2.5 (stable fixed point) the exponent is negative (not chaotic)
    assert lyapunov_logistic(2.5) < 0.0


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
