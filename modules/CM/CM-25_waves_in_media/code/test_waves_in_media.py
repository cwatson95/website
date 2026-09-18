"""Tests for CM-25 waves in media. Reuses MA-08 (imported transitively).

Run:  python3 test_waves_in_media.py     ->  "All N tests passed."
"""
import math

from waves_in_media import (
    wave_speed, string_mode_frequency, string_wavelength,
    phase_velocity, group_velocity, nondispersive, klein_gordon,
)
from pde import wave_1d, wave_mode


def _approx(x, y, tol=1e-6):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_wave_speed_and_modes():
    assert _approx(wave_speed(100.0, 0.01), 100.0)            # sqrt(T/mu)
    c, L = 10.0, 2.0
    assert _approx(string_mode_frequency(3, c, L), 3 * c / (2 * L))
    assert _approx(string_wavelength(3, L), 2 * L / 3)
    # harmonics are integer multiples of the fundamental
    f1 = string_mode_frequency(1, c, L)
    assert _approx(string_mode_frequency(4, c, L), 4 * f1)


def test_nondispersive_vp_equals_vg():
    c = 2.0
    disp = nondispersive(c)
    for k in (0.5, 1.0, 3.0):
        assert _approx(phase_velocity(disp(k), k), c)
        assert _approx(group_velocity(disp, k), c, tol=1e-4)     # v_p = v_g = c


def test_dispersive_klein_gordon():
    c, w0 = 2.0, 1.0
    kg = klein_gordon(c, w0)
    for k in (0.5, 1.0, 2.0):
        vp = phase_velocity(kg(k), k)
        vg = group_velocity(kg, k)
        assert vp > c and vg < c                                 # v_p > c > v_g
        assert _approx(vp * vg, c * c, tol=1e-4)                 # v_p v_g = c^2


def test_string_mode_via_wave_equation():
    # reuse MA-08: a plucked n=1 mode evolves as the standing wave sin(pi x) cos(c pi t)
    L, N = 1.0, 41
    dx = L / (N - 1)
    xs = [i * dx for i in range(N)]
    c, n = 1.0, 1
    u0 = [math.sin(n * math.pi * x / L) for x in xs]
    uf = wave_1d(u0, [0.0] * N, c, dx, dx, 8)                    # C=1, T = 8 dx = 0.2
    exact = wave_mode(L, c, n)
    for i in range(1, N - 1):
        assert abs(uf[i] - exact(xs[i], 8 * dx)) < 1e-2
    # the mode's temporal frequency is exactly f_n
    assert _approx(string_mode_frequency(n, c, L), c * n / (2 * L))


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
