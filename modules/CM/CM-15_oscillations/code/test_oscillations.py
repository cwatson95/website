"""Tests for CM-15 oscillations. Reuses MA-07 (imported transitively).

Run:  python3 test_oscillations.py     ->  "All N tests passed."
"""
import math

from oscillations import (
    integrate_oscillator, damped_frequency, driven_amplitude,
    resonance_frequency, quality_factor, underdamped_solution,
)


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_simple_harmonic_motion():
    w0 = 2.0
    ts, ys = integrate_oscillator(w0, 0.0, 1.0, 0.0, 0.0, 2 * math.pi, 8000)
    for t, s in list(zip(ts, ys))[::400]:
        assert _approx(s[0], math.cos(w0 * t), tol=1e-4)         # x = cos(w0 t)
        assert _approx(s[1], -w0 * math.sin(w0 * t), tol=1e-4)


def test_underdamped_matches_closed_form():
    w0, g = 3.0, 0.4
    x = underdamped_solution(w0, g, x0=1.0, v0=0.0)
    ts, ys = integrate_oscillator(w0, g, 1.0, 0.0, 0.0, 6.0, 12000)
    for t, s in list(zip(ts, ys))[::500]:
        assert _approx(s[0], x(t), tol=1e-4)                     # numeric == analytic envelope*cos
    assert _approx(damped_frequency(w0, g), math.sqrt(w0 ** 2 - g ** 2))


def test_energy_decays_when_damped():
    w0, g = 2.0, 0.3
    ts, ys = integrate_oscillator(w0, g, 1.0, 0.0, 0.0, 10.0, 8000)

    def E(s):
        return 0.5 * s[1] ** 2 + 0.5 * w0 ** 2 * s[0] ** 2
    assert E(ys[-1]) < 0.05 * E(ys[0])                           # most energy dissipated


def test_driven_steady_state_amplitude():
    w0, g, wd, F0 = 2.0, 0.2, 1.5, 1.0
    A = driven_amplitude(w0, g, F0, wd)
    ts, ys = integrate_oscillator(w0, g, 0.0, 0.0, 0.0, 120.0, 24000, F0=F0, omega_d=wd)
    period_pts = int(24000 / 120.0 * (2 * math.pi / wd)) + 2     # samples in one drive period
    tail_amp = max(abs(s[0]) for s in ys[-period_pts:])
    assert _approx(tail_amp, A, tol=2e-2)                        # transient gone -> formula amplitude


def test_resonance_and_Q():
    w0, g = 5.0, 0.5
    assert _approx(resonance_frequency(w0, g), math.sqrt(w0 ** 2 - 2 * g ** 2))
    assert _approx(quality_factor(w0, g), w0 / (2 * g))
    # amplitude is indeed largest near the resonance frequency
    wr = resonance_frequency(w0, g)
    Ar = driven_amplitude(w0, g, 1.0, wr)
    assert Ar > driven_amplitude(w0, g, 1.0, wr * 0.8) and Ar > driven_amplitude(w0, g, 1.0, wr * 1.2)


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
