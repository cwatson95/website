# MA-09 — Fourier Series & Transforms

Math trunk (see `modules/topic_network.txt`). **Prereq:** `~MA-05` (the complex
exponential is the kernel). **Pairs with** `~MA-08` (separation → Fourier modes).
**Feeds:** `~CM-16` (normal modes), `~QM-08` (momentum space), `~EM-15` (spectra).

## Scope
The **discrete Fourier transform** and its inverse, a **radix-2 FFT**, the DFT bin
frequencies, and numerical **Fourier-series coefficients** with reconstruction.
The DFT kernel e^{−2πi kn/N} = `euler(−2π kn/N)` is a direct reuse of `~MA-05`.

## Operations — `code/fourier.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `dft(x)` / `idft(X)` | DFT and inverse (complex form) | Boas §7.7 p.358; §7.12 p.378 |
| `fft(x)` | radix-2 Cooley–Tukey (power-of-2) | (algorithm; same result as `dft`) |
| `dft_freqs(N, dt)` | frequency of each bin | Boas §7.12 p.378 |
| `fourier_series_coeffs(f, P, M)` | a₀, aₙ, bₙ of a periodic f | Boas §7.5 p.350 |
| `series_value(a0, a, b, P, x)` | evaluate the truncated series | Boas §7.6 p.355 (Dirichlet) |

## Use
```python
import math
from fourier import dft, idft, fft, fourier_series_coeffs

x = [math.cos(2*math.pi*2*n/16) for n in range(16)]   # 2 cycles
X = dft(x)                 # peaks at bins 2 and 14
idft(X)                    # recovers x
fft(x)                     # same as dft, O(N log N)

sq = lambda t: 1.0 if (t % 1.0) < 0.5 else -1.0        # square wave
a0, a, b = fourier_series_coeffs(sq, 1.0, 5)           # b_n = 4/(n*pi), odd n
```

## Run
```bash
cd code
python3 fourier.py          # demo (DFT peaks, idft/fft checks, square-wave series)
python3 test_fourier.py     # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/fourier.py` · `code/test_fourier.py` · `problems/problems.md`
