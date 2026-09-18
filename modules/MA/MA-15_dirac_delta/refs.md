# MA-15 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Boas, *Mathematical Methods in the Physical Sciences*, **3rd ed.** (2006) | `MA_Mathematics/MathematicalMethodsInThePhysicalSciences3rdEditionByMaryL.BoasZ-lib.org.pdf` | PDF = printed **+ 19** |

All in **Chapter 8 §11, The Dirac Delta Function** (begins printed p.449). Boas
*amplified* the delta treatment for the 3rd edition (her preface) and keeps it in
the ODE chapter, right before Green functions (§12, `~MA-14`).

| Topic (code symbol) | Section / equation | Printed p. | PDF p. |
|---|---|---|---|
| δ as distribution; impulse/jump; definition (`gaussian_delta` … `sift`, `heaviside`) | §11 intro *The Dirac Delta Function* | 449 | 468 |
| impulse response y″+ω²y=δ (bridge to `~MA-14`) | §11 Example 1, eq.(11.2) | 450 | 469 |
| Fourier representation δ=(1/2π)∫e^{ikx}dk (`fourier_delta_kernel`) | §11 eqs.(11.12)–(11.16) | 454 | 473 |
| sifting property | §11 eqs.(11.14)–(11.18) | 454–455 | 473–474 |
| scaling & composition δ(ax), δ[(x−a)(x−b)], δ[f(x)] (`delta_compose_rhs/_integral`) | §11 eq.(11.19) (c),(d),(e) | 456 | 475 |
| δ in 2-D/3-D — point source (`~EM-01`, `~MA-14`) | §11 eqs.(11.20)–(11.21) | 456 | 475 |
| Fourier-transform machinery behind the kernel | Ch.7 §12 *Fourier Transforms* | 378 | 397 |

## Further reading (not page-pinned here)
- **Butkov**, *Mathematical Physics* (`MA_Mathematics/MPHY_butkov.pdf`) develops
  distributions / generalized functions more formally. Scanned image PDF (no text
  layer), so pages are not pinned here.

## Notes (verified)
- Boas's eq.(11.19) on **p.456** is the source for the whole composition section:
  (c) δ(ax)=δ(x)/|a|, (d) δ[(x−a)(x−b)]=[δ(x−a)+δ(x−b)]/|a−b| (the verified
  δ(x²−c²) example), and (e) the general δ[f(x)]=Σ δ(x−xᵢ)/|f′(xᵢ)|.
- The very first delta example (eq.11.2, p.450) is the forced oscillator
  y″+ω²y=δ — the same impulse response that becomes the causal Green's function in
  `~MA-14`; this is why §11 sits next to §12 (Green functions) in Boas.
- The δ-as-Fourier-integral identity is derived in §11 itself (p.454), not only in
  the Fourier chapter — both are cited.
