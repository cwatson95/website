# RE-16 — References

Page-level citations **verified by reading the page text** (PyMuPDF) in the PDFs
under `books/library/`. **Printed** = the number on the page; **PDF** = the
viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Zee, *Einstein Gravity in a Nutshell* (2013) | `RE_Relativity_Cosmology/EinsteinGravityInANutshell.pdf` | PDF = printed **+ 23** |

The whole gravitational-wave development is Zee **§IX.4** *Linearized Gravity and
Gravitational Waves* (chapter opener: printed **563**, PDF **586**); the
linearized Ricci tensor it reuses is derived back in **§VI.5** *Gravity Goes Live*
(printed **388**, PDF **411**). Each row below was confirmed by reading that page.

## Topic → location

| Topic (code symbol) | Source | Section / content | Printed p. | PDF p. |
|---|---|---|---|---|
| linearized Ricci `R_{μν}` (input to `□h̄=−16πT`) | Zee | §VI.5 *Gravity Goes Live* — Einstein tensor from `δS_EH` | 388 | 411 |
| section opener; `g=η+h`, "watch the ripples" | Zee | §IX.4 *Linearized Gravity and Gravitational Waves* | 563 | 586 |
| Lorenz/harmonic gauge `h'_{μν}=h_{μν}−∂_με_ν−∂_νε_μ` | Zee | §IX.4 *Weak field and harmonic gauge* | 564 | 587 |
| wave eqn `□h̄=−16πT`, TT gauge, **2 polarizations** (`tt_wave`, `is_transverse_traceless`, `dispersion_omega`, `wave_equation_residual`) | Zee | §IX.4 *Degrees of polarizations* (Eqs. 4–6, `k²=0`) | 565 | 588 |
| `h_+`/`h_×`, single particle stays put, ring of particles (`ring_response`, `area_change`) | Zee | §IX.4 *Detection of gravitational waves* | 566 | 589 |
| retarded Green's function = EM's, propagates at `c` | Zee | §IX.4 (multipole expansion, Eqs. 13–15) | 568 | 591 |
| quadrupole formula `h̄_{ij}=(2/r)Q̈_{ij}`, no monopole/dipole (`reduced_quadrupole`) | Zee | §IX.4 (Eq. 16, `Q_{ij}=∫y_iy_jT⁰⁰`) | 569 | 592 |

## Standard results stated but **not** page-pinned here
`quadrupole_luminosity` (`P = ⅕⟨Q⃛_{ij}Q⃛^{ij}⟩`), `chirp_mass`, `gw_frequency`,
and `chirp_rate` (`ḟ ∝ f^{11/3}M_c^{5/3}`) are the standard Einstein
quadrupole-luminosity and binary-inspiral results. Zee §IX.4 derives the
quadrupole *amplitude* `h̄_{ij}=(2/r)Q̈_{ij}` (p. 569, above) but states neither
the radiated *power* nor the inspiral chirp (the word "chirp" does not appear in
the text), so they are presented from the physics, not cited to a verified page.
The observational anchors — the Hulse–Taylor binary pulsar (mentioned on Zee
p. 563) and **GW150914** (LIGO, 2015) — are quoted as historical facts, not
page-cited.

## Cross-module dependency
None at runtime (pure stdlib). Physically this module **linearizes RE-13**'s
Einstein equation and its wave moves matter via **RE-11**'s geodesic deviation:
the tidal field carried by a TT wave is the linearized Riemann tensor
`R_{i0j0} = −½ ḧ_{ij}^{TT}`. The metric/η conventions are RE-05's.

## Further reading (not page-verified — image-only scans, no text layer)
- d'Inverno, *Introducing Einstein's Relativity*, Ch. on linearized GR &
  gravitational waves — `RE_Relativity_Cosmology/RayD_Inverno-IntroducingEinstein_sRelativity.pdf`.
- Weinberg, *Gravitation and Cosmology*, Ch. 10 (gravitational radiation; the
  quadrupole luminosity formula) — `RE_Relativity_Cosmology/Grav.Cosm.Weinberg.pdf`.
- *(Both PDFs are scanned images with no extractable text, so page numbers are
  not cited — same policy as the other RE/MA modules.)*
