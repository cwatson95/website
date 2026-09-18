# MA-09 — Fourier Series & Transforms (notes)

Citation keys (details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are the *printed* book pages. (Butkov is image-only and
cited at chapter level in `refs.md`, without page numbers.)

## 1. Fourier series
A P-periodic f (satisfying the **Dirichlet conditions** [B §7.6 p.355]) expands as
$$f(x)=\frac{a_0}{2}+\sum_{n\ge 1}\Big(a_n\cos\tfrac{2\pi n x}{P}+b_n\sin\tfrac{2\pi n x}{P}\Big),$$
with coefficients from orthogonality ("Fourier's trick") [B §7.5 p.350]:
$$a_n=\frac2P\!\int_0^P f\cos\tfrac{2\pi nx}{P}dx,\quad
  b_n=\frac2P\!\int_0^P f\sin\tfrac{2\pi nx}{P}dx.$$
Code: `fourier_series_coeffs`, `series_value`. (A square wave gives bₙ = 4/(nπ)
for odd n — a test.)

## 2. Complex form
Using e^{iθ}=cosθ+i sinθ (`~MA-05`), the series collapses to one sum [B §7.7 p.358]:
$$f(x)=\sum_{n} c_n\,e^{\,2\pi i n x/P},\qquad c_n=\frac1P\int_0^P f\,e^{-2\pi i n x/P}dx.$$
This complex exponential is exactly the **DFT kernel**.

## 3. The discrete Fourier transform
For N samples xₙ,
$$X_k=\sum_{n=0}^{N-1} x_n\,e^{-2\pi i k n/N},\qquad
  x_n=\frac1N\sum_{k=0}^{N-1} X_k\,e^{+2\pi i k n/N}.$$
Code: `dft`, `idft` (each kernel value is `euler(...)` from MA-05). `dft_freqs`
labels the bins; the upper half are the negative frequencies. **Parseval's
theorem** [B §7.11 p.375] is energy conservation: Σ|xₙ|² = (1/N)Σ|Xₖ|² (a test).

## 4. The fast Fourier transform
The DFT is O(N²); splitting even/odd indices recursively (**Cooley–Tukey**) makes
it O(N log N). Code: `fft` (radix-2) returns the same array as `dft` (a test) but
far faster for large N.

## 5. The Fourier transform
Letting P→∞ turns the series into the integral transform [B §7.12 p.378],
f(x) = ∫ g(k)e^{ikx}dk. This is the continuous limit the DFT
approximates, and the bridge to momentum space in `~QM-08` and spectra in `~EM-15`.
