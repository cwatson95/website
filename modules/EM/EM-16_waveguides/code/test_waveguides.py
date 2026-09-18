"""Tests for EM-16 waveguides. Reuses EM-15 (speed c).

Run:  python3 test_waveguides.py     ->  "All N tests passed."
"""
import math

# own module first: chains EM-15 (and EM-01/EM-08/MA) onto sys.path
from waveguides import (
    C, cutoff_angular_frequency, cutoff_frequency, dominant_mode_cutoff,
    is_propagating, guide_wavenumber, evanescent_decay,
    phase_velocity_guide, group_velocity_guide, tem_line_speed,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_te10_cutoff_formula():
    a, b = 0.05, 0.02
    # TE10 cutoff = c pi / a
    assert _approx(cutoff_angular_frequency(1, 0, a, b), C * math.pi / a)
    assert _approx(dominant_mode_cutoff(a, b), C * math.pi / a)


def test_mode_ordering():
    # TE10 is the lowest cutoff when a > b
    a, b = 0.05, 0.02
    w10 = cutoff_angular_frequency(1, 0, a, b)
    assert w10 < cutoff_angular_frequency(2, 0, a, b)
    assert w10 < cutoff_angular_frequency(0, 1, a, b)
    assert w10 < cutoff_angular_frequency(1, 1, a, b)


def test_propagation_threshold():
    a, b = 0.05, 0.02
    wco = cutoff_angular_frequency(1, 0, a, b)
    assert is_propagating(1.2 * wco, 1, 0, a, b)
    assert not is_propagating(0.8 * wco, 1, 0, a, b)
    # propagating -> real k > 0; below cutoff -> evanescent decay > 0, k = 0
    assert guide_wavenumber(1.2 * wco, wco) > 0
    assert guide_wavenumber(0.8 * wco, wco) == 0.0
    assert evanescent_decay(0.8 * wco, wco) > 0
    assert evanescent_decay(1.2 * wco, wco) == 0.0


def test_guide_wavenumber_value():
    wco = 1e10
    w = 2e10
    # k = (1/c) sqrt(w^2 - wco^2)
    assert _approx(guide_wavenumber(w, wco), math.sqrt(w ** 2 - wco ** 2) / C)


def test_phase_group_velocity_product():
    wco = 1e10
    for ratio in (1.1, 1.5, 3.0, 10.0):
        w = ratio * wco
        vp = phase_velocity_guide(w, wco)
        vg = group_velocity_guide(w, wco)
        assert vp > C > vg > 0                       # v_p superluminal, v_g subluminal
        assert _approx(vp * vg, C ** 2)              # the hallmark identity


def test_high_frequency_limit():
    # far above cutoff both velocities -> c
    wco = 1e10
    w = 1e6 * wco
    assert _approx(phase_velocity_guide(w, wco), C, tol=1e-6)
    assert _approx(group_velocity_guide(w, wco), C, tol=1e-6)


def test_tem_line_has_no_cutoff():
    assert _approx(tem_line_speed(), C)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
