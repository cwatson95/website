"""Tests for RE-01 Galilean relativity & its failure.

Run directly:   python3 test_galilean.py        (-> "All N tests passed.")
Or with pytest: pytest test_galilean.py

The theme: Galilean velocity addition is the c -> infinity limit of Einstein's
(verified against RE-03), Newton is Galilean-invariant but light is not, and the
Michelson-Morley shift the ether predicted (~0.4 fringe) was never seen.
"""
import math
import random

from galilean import (
    C_LIGHT, galilean_position, galilean_velocity_add, relativistic_velocity_add,
    galilean_limit_error, galilean_invariant_acceleration, light_speed_galilean,
    michelson_morley_shift, ether_wind_dt,
)
import lorentz            # RE-03 (on sys.path via galilean)
import reference_frames   # CM-03 (on sys.path via galilean)

TOL = 1e-9


def _approx(x, y, tol=TOL):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_galilean_addition_is_plain_sum():
    rng = random.Random(0)
    for _ in range(200):
        u, v = rng.uniform(-50, 50), rng.uniform(-50, 50)
        assert _approx(galilean_velocity_add(u, v), u + v)
        assert _approx(galilean_velocity_add(u, v), galilean_velocity_add(v, u))  # commutes


def test_relativistic_reduces_to_galilean_as_c_grows():
    """The error shrinks like 1/c^2 -> Galilean is the low-speed limit."""
    u, v = 1.0e7, 2.0e7
    errs = [galilean_limit_error(u, v, c) for c in (3e8, 3e9, 3e10, 3e12)]
    for a, b in zip(errs, errs[1:]):
        assert b < a                                   # strictly decreasing
    assert errs[-1] < 1e-3                             # and -> 0
    # each 10x in c cuts the error ~100x (1/c^2 scaling)
    assert errs[0] / errs[1] > 50


def test_relativistic_addition_matches_RE03():
    """relativistic_velocity_add must equal RE-03's dimensionless rule scaled by c."""
    rng = random.Random(1)
    c = C_LIGHT
    for _ in range(300):
        u, v = rng.uniform(-0.9, 0.9) * c, rng.uniform(-0.9, 0.9) * c
        assert _approx(relativistic_velocity_add(u, v, c),
                       c * lorentz.velocity_add(u / c, v / c))


def test_only_relativistic_respects_c():
    """Einstein addition never exceeds c; Galilean blows past it."""
    c = C_LIGHT
    assert relativistic_velocity_add(0.9 * c, 0.9 * c, c) < c       # stays sub-luminal
    assert galilean_velocity_add(0.9 * c, 0.9 * c) > c              # Galilean overshoots
    assert _approx(relativistic_velocity_add(c, 0.5 * c, c), c)     # c (+) v = c


def test_galilean_boost_matches_CM03():
    rng = random.Random(2)
    for _ in range(100):
        r = [rng.uniform(-5, 5) for _ in range(3)]
        V = [rng.uniform(-3, 3) for _ in range(3)]
        t = rng.uniform(0, 4)
        assert galilean_position(r, V, t) == reference_frames.galilean_position(r, V, t)


def test_newton_invariant_light_is_not():
    # acceleration unchanged by a Galilean boost (any boost velocity) -> F=ma invariant
    for V in (0.0, 10.0, 1e6):
        assert galilean_invariant_acceleration(9.81, V) == 9.81
    # but Galilean addition gives the wrong, frame-dependent light speed
    c = C_LIGHT
    assert light_speed_galilean(30_000.0, c) > c          # c + v != c  (the contradiction)
    assert not _approx(light_speed_galilean(30_000.0, c), c)


def test_michelson_morley_predicted_shift():
    # the famous ~0.4-fringe prediction for the 1887 apparatus
    shift = michelson_morley_shift(30_000.0, 11.0, 500e-9)
    assert 0.3 < shift < 0.5
    # scales as (v/c)^2: doubling v quadruples the shift
    s1 = michelson_morley_shift(30_000.0, 11.0, 500e-9)
    s2 = michelson_morley_shift(60_000.0, 11.0, 500e-9)
    assert _approx(s2 / s1, 4.0, 1e-6)
    assert _approx(michelson_morley_shift(0.0, 11.0, 500e-9), 0.0)   # no wind, no shift


def test_ether_wind_dt_consistency():
    # the fringe shift on a 90-degree rotation is 2 c dt / lambda
    v, L, lam = 30_000.0, 11.0, 500e-9
    dt = ether_wind_dt(v, L)
    assert dt > 0.0
    assert _approx(2.0 * C_LIGHT * dt / lam, michelson_morley_shift(v, L, lam), 1e-3)
    # leading order dt ~ (L/c)(v/c)^2
    assert _approx(dt, (L / C_LIGHT) * (v / C_LIGHT) ** 2, 1e-3)
    assert _approx(ether_wind_dt(0.0, L), 0.0)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
