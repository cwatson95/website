"""
MA-09  Fourier series & transforms -- the discrete Fourier transform (DFT), a
radix-2 FFT, the inverse, and numerical Fourier-series coefficients.

Part of the physics topic network (modules/topic_network.txt, module MA-09).
Builds on ~MA-05 (the complex exponential is the DFT kernel) and pairs with
~MA-08 (separation of variables -> Fourier modes); feeds ~CM-16 (normal modes),
~QM-08 (momentum space), ~EM-15 (spectra).

The DFT kernel is e^{-2 pi i k n / N} = euler(-2 pi k n / N) -- a direct reuse of
MA-05.  Signals are lists of (real or complex) samples.

NOTE: MA-05 imported by relative path; becomes `from physkit...` later.
"""

import math
import os
import sys

_HERE = os.path.dirname(os.path.abspath(__file__))
_MA05 = os.path.abspath(os.path.join(_HERE, "..", "..", "MA-05_complex_numbers", "code"))
if _MA05 not in sys.path:
    sys.path.insert(0, _MA05)

from complex_numbers import euler  # noqa: E402  (DFT twiddle factor e^{i theta})

__all__ = ["dft", "idft", "fft", "dft_freqs", "fourier_series_coeffs", "series_value"]


def dft(x):
    """Discrete Fourier transform  X_k = sum_n x_n e^{-2 pi i k n / N}  (O(N^2))."""
    N = len(x)
    X = []
    for k in range(N):
        s = 0j
        for n in range(N):
            s += x[n] * euler(-2.0 * math.pi * k * n / N)
        X.append(s)
    return X


def idft(X):
    """Inverse DFT  x_n = (1/N) sum_k X_k e^{+2 pi i k n / N}."""
    N = len(X)
    out = []
    for n in range(N):
        s = 0j
        for k in range(N):
            s += X[k] * euler(2.0 * math.pi * k * n / N)
        out.append(s / N)
    return out


def _fft(a):
    N = len(a)
    if N <= 1:
        return a
    even, odd = _fft(a[0::2]), _fft(a[1::2])
    twiddle = [euler(-2.0 * math.pi * k / N) * odd[k] for k in range(N // 2)]
    return ([even[k] + twiddle[k] for k in range(N // 2)]
            + [even[k] - twiddle[k] for k in range(N // 2)])


def fft(x):
    """Radix-2 Cooley-Tukey FFT (length must be a power of 2). Same result as dft, O(N log N)."""
    N = len(x)
    if N & (N - 1) != 0 or N == 0:
        raise ValueError("fft length must be a power of 2; use dft() otherwise")
    return _fft([complex(v) for v in x])


def dft_freqs(N, dt=1.0):
    """The frequencies (cycles per unit) for the N DFT bins, sampling step dt."""
    return [(k if k < (N + 1) // 2 else k - N) / (N * dt) for k in range(N)]


def fourier_series_coeffs(f, P, M, n_int=4000):
    """Real Fourier-series coefficients of a P-periodic f, for n = 1..M:
        f(x) ~ a0/2 + sum_n [ a_n cos(2 pi n x/P) + b_n sin(2 pi n x/P) ],
        a_n = (2/P) int_0^P f cos(...) dx,  b_n = (2/P) int_0^P f sin(...) dx.
    Returns (a0, [a_1..a_M], [b_1..b_M]) by midpoint integration."""
    dx = P / n_int

    def integ(g):
        return sum(g((i + 0.5) * dx) for i in range(n_int)) * dx

    w = 2.0 * math.pi / P
    a0 = (2.0 / P) * integ(f)
    a = [(2.0 / P) * integ(lambda x, n=n: f(x) * math.cos(w * n * x)) for n in range(1, M + 1)]
    b = [(2.0 / P) * integ(lambda x, n=n: f(x) * math.sin(w * n * x)) for n in range(1, M + 1)]
    return a0, a, b


def series_value(a0, a, b, P, x):
    """Evaluate the truncated Fourier series at x."""
    w = 2.0 * math.pi / P
    s = a0 / 2.0
    for n in range(1, len(a) + 1):
        s += a[n - 1] * math.cos(w * n * x) + b[n - 1] * math.sin(w * n * x)
    return s


# --- demo --------------------------------------------------------------------

def _demo():
    print("MA-09 Fourier -- demo")
    print("=" * 32)

    N = 16
    sig = [math.cos(2.0 * math.pi * 2.0 * n / N) for n in range(N)]   # pure cos, 2 cycles
    X = dft(sig)
    peaks = [k for k in range(N) if abs(X[k]) > 1e-6]
    print("DFT of cos(2 cycles): nonzero bins =", peaks, " (expect 2 and", N - 2, ")")
    print("  idft(dft(x)) == x ?", all(abs(v - s) < 1e-9 for v, s in zip(idft(X), sig)))
    print("  fft == dft ?       ", all(abs(a - b) < 1e-9 for a, b in zip(fft(sig), X)))

    print("\nFourier series of a square wave (period 1):")
    sq = lambda x: 1.0 if (x % 1.0) < 0.5 else -1.0
    a0, a, b = fourier_series_coeffs(sq, 1.0, 5)
    print("  b_n =", [round(v, 4) for v in b], " (expect 4/(n pi) for odd n: ",
          [round(4 / (n * math.pi), 4) if n % 2 else 0.0 for n in range(1, 6)], ")")


if __name__ == "__main__":
    _demo()
