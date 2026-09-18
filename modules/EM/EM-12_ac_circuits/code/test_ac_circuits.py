"""Tests for EM-12 AC circuits & driven RLC. Self-contained (cmath).

Run:  python3 test_ac_circuits.py     ->  "All N tests passed."
"""
import cmath
import math

from ac_circuits import (
    impedance_resistor, impedance_inductor, impedance_capacitor,
    impedance_series, impedance_parallel, series_rlc_impedance,
    resonant_frequency, quality_factor, bandwidth,
    current_amplitude, current_phase, average_power,
)


def _approx(x, y, tol=1e-9):
    return abs(x - y) <= tol * (1.0 + abs(y))


def test_element_impedances():
    w = 1000.0
    assert impedance_resistor(50.0) == complex(50.0, 0.0)
    assert _approx(impedance_inductor(2e-3, w).imag, w * 2e-3)
    assert _approx(impedance_capacitor(1e-6, w).imag, -1.0 / (w * 1e-6))


def test_series_and_parallel():
    Z1, Z2 = complex(3, 4), complex(0, -2)
    assert impedance_series(Z1, Z2) == complex(3, 2)
    # two equal resistors in parallel -> half
    assert _approx(impedance_parallel(complex(10, 0), complex(10, 0)).real, 5.0)


def test_resonance_is_purely_resistive():
    R, L, C = 10.0, 1e-3, 1e-6
    w0 = resonant_frequency(L, C)
    Z = series_rlc_impedance(R, L, C, w0)
    assert _approx(Z.imag, 0.0, tol=1e-6)             # reactances cancel
    assert _approx(Z.real, R)
    assert _approx(w0, 1.0 / math.sqrt(L * C))


def test_current_peaks_at_resonance():
    R, L, C, V0 = 10.0, 1e-3, 1e-6, 5.0
    w0 = resonant_frequency(L, C)
    I0 = current_amplitude(V0, series_rlc_impedance(R, L, C, w0))
    assert _approx(I0, V0 / R)                        # max current = V0/R
    # off resonance the current is smaller
    for ratio in (0.7, 1.3):
        Ioff = current_amplitude(V0, series_rlc_impedance(R, L, C, ratio * w0))
        assert Ioff < I0


def test_phase_sign_across_resonance():
    R, L, C = 10.0, 1e-3, 1e-6
    w0 = resonant_frequency(L, C)
    # below resonance: capacitive, current leads (phase > 0)
    assert current_phase(series_rlc_impedance(R, L, C, 0.5 * w0)) > 0
    # above resonance: inductive, current lags (phase < 0)
    assert current_phase(series_rlc_impedance(R, L, C, 2.0 * w0)) < 0
    # at resonance: in phase
    assert _approx(current_phase(series_rlc_impedance(R, L, C, w0)), 0.0, tol=1e-6)


def test_quality_factor_and_bandwidth():
    R, L, C = 5.0, 2e-3, 5e-7
    w0 = resonant_frequency(L, C)
    Q = quality_factor(R, L, C)
    assert _approx(Q, w0 * L / R)                     # Q = w0 L / R
    assert _approx(Q, (1.0 / R) * math.sqrt(L / C))
    # bandwidth relation dw = w0 / Q = R / L
    assert _approx(bandwidth(R, L), w0 / Q)


def test_average_power_peaks_at_resonance():
    R, L, C, V0 = 8.0, 1e-3, 1e-6, 4.0
    w0 = resonant_frequency(L, C)
    P0 = average_power(V0, series_rlc_impedance(R, L, C, w0))
    assert _approx(P0, V0 ** 2 / (2 * R))             # max average power
    assert average_power(V0, series_rlc_impedance(R, L, C, 0.6 * w0)) < P0
    # half-power points at w0 +/- dw/2 give P0/2
    dw = bandwidth(R, L)
    Zhp = series_rlc_impedance(R, L, C, w0 + dw / 2)
    assert _approx(average_power(V0, Zhp), P0 / 2, tol=2e-2)


def _run():
    tests = [v for k, v in sorted(globals().items())
             if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
