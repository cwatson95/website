"""Tests for MA-09 Fourier. Reuses MA-05 (imported transitively).

Run:  python3 test_fourier.py     ->  "All N tests passed."
"""
import cmath
import math
import random

from fourier import dft, idft, fft, dft_freqs, fourier_series_coeffs, series_value


def _capprox(z, w, tol=1e-9):
    return abs(z - w) <= tol * (1.0 + abs(w))


def test_idft_inverts_dft():
    rng = random.Random(0)
    x = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(12)]
    assert all(_capprox(a, b) for a, b in zip(idft(dft(x)), x))


def test_dft_of_pure_cosine():
    N, k0 = 16, 3
    x = [math.cos(2.0 * math.pi * k0 * n / N) for n in range(N)]
    X = dft(x)
    assert abs(X[k0]) > 1.0 and abs(X[N - k0]) > 1.0                 # peaks at k0 and N-k0
    assert _capprox(abs(X[k0]), N / 2.0, tol=1e-6)
    for k in range(N):
        if k not in (k0, N - k0):
            assert abs(X[k]) < 1e-6                                  # everything else ~ 0


def test_fft_matches_dft():
    rng = random.Random(1)
    for N in (2, 4, 8, 16):
        x = [complex(rng.uniform(-1, 1), rng.uniform(-1, 1)) for _ in range(N)]
        assert all(_capprox(a, b, tol=1e-9) for a, b in zip(fft(x), dft(x)))


def test_parseval():
    rng = random.Random(2)
    x = [complex(rng.uniform(-2, 2), rng.uniform(-2, 2)) for _ in range(10)]
    X = dft(x)
    lhs = sum(abs(v) ** 2 for v in x)
    rhs = sum(abs(v) ** 2 for v in X) / len(x)
    assert abs(lhs - rhs) < 1e-9 * (1.0 + abs(rhs))


def test_freqs():
    f = dft_freqs(8, dt=1.0)
    assert f[0] == 0.0 and f[1] == 1.0 / 8 and f[4] == -0.5 and f[7] == -1.0 / 8


def test_series_coeffs_pure_modes():
    a0, a, b = fourier_series_coeffs(lambda x: math.cos(2 * math.pi * x), 1.0, 3)
    assert abs(a[0] - 1.0) < 1e-3 and abs(a[1]) < 1e-3 and abs(b[0]) < 1e-3
    a0, a, b = fourier_series_coeffs(lambda x: math.sin(2 * math.pi * x), 1.0, 3)
    assert abs(b[0] - 1.0) < 1e-3 and abs(a[0]) < 1e-3


def test_series_coeffs_square_wave():
    # odd square wave on period 1 -> b_n = 4/(n pi) for odd n, 0 otherwise
    sq = lambda x: 1.0 if (x % 1.0) < 0.5 else -1.0
    a0, a, b = fourier_series_coeffs(sq, 1.0, 5, n_int=8000)
    assert abs(a0) < 1e-2 and all(abs(av) < 1e-2 for av in a)        # even part ~ 0
    assert abs(b[0] - 4.0 / math.pi) < 1e-2                          # b_1 = 4/pi
    assert abs(b[1]) < 1e-2                                          # b_2 = 0
    assert abs(b[2] - 4.0 / (3.0 * math.pi)) < 1e-2                  # b_3 = 4/3pi


def test_series_reconstruction():
    f = lambda x: 0.5 + math.cos(2 * math.pi * x) + 0.3 * math.sin(4 * math.pi * x)
    a0, a, b = fourier_series_coeffs(f, 1.0, 4)
    for x in (0.1, 0.37, 0.6, 0.95):
        assert abs(series_value(a0, a, b, 1.0, x) - f(x)) < 1e-2


def _run():
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    for fn in tests:
        fn()
        print("PASS", fn.__name__)
    print("\nAll %d tests passed." % len(tests))


if __name__ == "__main__":
    _run()
