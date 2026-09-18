# QO-06 — References

| Book (edition) | File | Notes |
|---|---|---|
| Boyd, *Nonlinear Optics*, **4th ed.** | `QO_Quantum_Optics/boyd_optics.pdf` | **primary**; has a text layer. Cited at **chapter/section level** (page offsets not verified). |
| Boyd, *Nonlinear Optics*, **4th ed.** (scan) | `QO_Quantum_Optics/NonlinearOptics-Boyd-4thEd.pdf` | same edition, **image-only scan** — cited at **chapter level only**. |
| Scully & Zubairy, *Quantum Optics* | `QO_Quantum_Optics/QuantumOptics.ZubairyMuhammadSuhail.pdf` | cross-cited for the **quantum** view of parametric down-conversion (→ `~QO-05`). |

> Granularity: citations are by **chapter** (and section title where standard),
> not page. The Boyd chapter map used here is the conventional 4th-edition
> structure and is the one named in the module brief; the scanned copy has no
> machine-readable page layer, so no page numbers are asserted. Tighten to
> section/page by opening `boyd_optics.pdf` (text layer present) if needed.

## Topic → location

| Topic (code symbol) | Source | Chapter / title |
|---|---|---|
| nonlinear polarization P = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + …), χ⁽ⁿ⁾ orders of magnitude (`chi_polarization`) | Boyd | Ch. 1 *The Nonlinear Optical Susceptibility* |
| SHG, phase matching, Δk, sinc² efficiency, coherence length (`shg_efficiency`, `shg_phase_mismatch`, `coherence_length`) | Boyd | Ch. 2 *Wave-Equation Description of Nonlinear Optical Interactions* (SHG & phase-matching sections) |
| Manley–Rowe relations / photon-number conservation, OPA (`manley_rowe_check`) | Boyd | Ch. 2 (coupled-amplitude / Manley–Rowe section) |
| optical Kerr effect n = n₀ + n₂I, χ⁽³⁾ ↔ n₂ (`kerr_index`) | Boyd | Ch. 4 *The Intensity-Dependent Refractive Index* |
| self-phase modulation, the B-integral, four-wave mixing (`kerr_phase`) | Boyd | Ch. 4 / Ch. 7 *Processes Resulting from the Intensity-Dependent Refractive Index* |
| stimulated Brillouin scattering, Lorentzian gain, Brillouin shift (`brillouin_shift`, `brillouin_gain`) | Boyd | Ch. 9 *Stimulated Brillouin and Stimulated Rayleigh Scattering* |
| stimulated Raman scattering, Lorentzian gain (`raman_gain`) | Boyd | Ch. 10 *Stimulated Raman Scattering …* |
| parametric down-conversion → squeezed/entangled light (quantum Manley–Rowe) | SZ | parametric amplification / squeezed-state chapters |

## See also
- **→ SBS_Project** (`projects/SBS_Project/`) — the stimulated-Brillouin gain
  spectrum `g_B(ν)` (here `brillouin_gain`), phase conjugation, and pulse
  compression. `SBS_code/sbs_gain.py` computes the same Lorentzian-class lineshape
  (with a velocity-dependent kinetic correction) and fits it to Kr/N₂ data.
- `~EM-15` (EM waves in media: dispersion n(ω), k = nω/c — sets the SHG phase
  mismatch and the Brillouin shift) and `~QO-01` (optical modes / the photon
  picture behind Manley–Rowe).
- `~QO-05` (squeezing & entangled photons — χ⁽²⁾ as a quantum source; Scully–Zubairy)
  and `~QO-03` (stimulated emission / optical gain — the e^{gIz} language of SBS/Raman).
- `~PK-04` (excimer/KrF laser kinetics — the high-fluence regime where the Kerr
  B-integral and SBS thresholds bite).
- Boyd Ch. 1–2 (χ⁽²⁾, SHG, phase matching), Ch. 4/7 (Kerr, SPM), Ch. 9–10 (SBS, Raman).
