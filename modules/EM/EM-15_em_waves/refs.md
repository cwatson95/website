# EM-15 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was re-confirmed across Griffiths chapters 7–12 against the page text
(e.g. PDF p.400 carries printed "382", the start of §9.1.1 *The Wave Equation*).
Griffiths is the worked source for the EM-11..EM-18 sequence; Jackson 3e and
Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| wave equation, dispersion ω=vk (`wave_equation_residual`, `scalar_plane_wave`) | §9.1.1 *The Wave Equation* (Eq. 9.2) | 382 | 400 |
| sinusoidal waves, k, ω, v=ω/k (`wavelength`) | §9.1.2 *Sinusoidal Waves* | 385 | 403 |
| polarization (`classify_polarization`) | §9.1.4 *Polarization* | 391 | 409 |
| monochromatic plane waves, B₀=E₀/c (`transverse_B`, `is_transverse`) | §9.2.2 *Monochromatic Plane Waves* (Eq. 9.49) | 394 | 412 |
| energy, momentum, intensity ⟨S⟩=½cε₀E₀² | §9.2.3 *Energy and Momentum in EM Waves* (Eq. 9.59) | 398 | 416 |
| linear media, v=c/n, n=√(ε_r μ_r) (`refractive_index`, `phase_velocity`) | §9.3.1 *Propagation in Linear Media* (Eq. 9.68) | 401 | 419 |
| reflection/transmission, r, t, R, T (`fresnel_normal`, `reflectance`, `transmittance`) | §9.3.2 *Reflection and Transmission at Normal Incidence* (Eq. 9.82) | 403 | 421 |

§9.4 *Absorption and Dispersion* (the frequency-dependent index n(ω)) closes the
chapter and rounds out the nominal §9.1–9.4 scope, but is not exercised by the
code here; it is cited at section level only — no specific page was verified in
the citation map.

## See also
- `~EM-13` (Maxwell's equations) — a plane wave is the source-free solution; the
  transversality and **B** = (1/c) **k̂**×**E** come straight from ∇·**E** = 0 and
  Faraday's law.
- `~MA-02` for `laplacian`, used by `wave_equation_residual`; `~MA-01` for
  `cross`/`dot`/`norm`/`unit`, used by `transverse_B`/`is_transverse`. The speed
  `C` = 1/√(μ₀ε₀) is built from `~EM-01` `EPS0` and `~EM-08` `MU0`.
- `~MA-09` (Fourier) builds general wave packets from these monochromatic plane
  waves — `KEY BRIDGE B9`.
- Downstream: `~EM-16` (waveguides & cavities), `~EM-17` (radiation),
  `~QO-01` (classical & quantized light / photons).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, Ch. 7
  *Plane Electromagnetic Waves and Wave Propagation* (`EM/Jackson…SolutionManual…pdf`
  holds solutions only locally); Schwinger et al., *Classical Electrodynamics*
  (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
