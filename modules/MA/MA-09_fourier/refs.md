# MA-09 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

All Boas references are in **Ch.7, Fourier Series and Transforms**.

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Fourier coefficients (`fourier_series_coeffs`) | §7.5 *Fourier Coefficients* | 350 | 369 |
| Dirichlet conditions / convergence (`series_value`) | §7.6 *Dirichlet Conditions* | 355 | 374 |
| complex (exponential) form (`dft`, `idft`) | §7.7 *Complex Form of Fourier Series* | 358 | 377 |
| Parseval's theorem | §7.11 *Parseval's Theorem* | 375 | 394 |
| the Fourier transform (`dft` as discrete FT; `dft_freqs`) | §7.12 *Fourier Transforms* | 378 | 397 |

## Notes
- The **DFT kernel** e^{−2πi kn/N} is `euler(...)` from `~MA-05` — the same complex
  exponential as the §7.7 complex Fourier series.
- The **FFT** (radix-2 Cooley–Tukey) is a fast *algorithm* for the DFT, not a Boas
  section; it returns the identical array (verified against `dft` in the tests).

## Further reading (not page-verified)
- Butkov, *Mathematical Physics*, **Ch.4** (Fourier series) and **Ch.7** (Fourier
  transforms). `MA_Mathematics/MPHY_butkov.pdf` is a **scanned, image-only PDF with no
  text layer**, so its section/page numbers are not verifiable here.
