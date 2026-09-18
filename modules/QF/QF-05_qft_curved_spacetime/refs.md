# QF-05 — References

Citations are at **chapter level**. The Birrell–Davies chapter starts were read off
the PDF's embedded table of contents (PyMuPDF), so the **PDF page** of each chapter
is verified; individual equation/printed-page numbers within a chapter were **not**
separately verified and are not invented (same policy as `~QM-04`/`~RE-14`). Fulling
has no extractable ToC layer, so it is cited at **chapter/topic level only**.

| Book (edition) | File | Granularity |
|---|---|---|
| Birrell & Davies, *Quantum Fields in Curved Space* (CUP, 1982) | `QF_Quantum_Field_Theory/QuantumFieldsInCurvedSpaceBirrellDavies.pdf` | **chapter** (PDF page of each chapter start verified) |
| S. A. Fulling, *Aspects of Quantum Field Theory in Curved Space-Time* (LMS Student Texts, CUP 1989) | `QF_Quantum_Field_Theory/AspectsOfQuantumFieldTheoryInCurvedSpacetimeLondon-StephenA_Fulling.pdf` | **chapter/topic** (no ToC layer; pages not cited) |

> Birrell–Davies is the canonical reference for everything in this module: the
> Bogoliubov framework and the particle concept (Ch. 2–3), the Unruh effect for
> accelerated observers (Ch. 4), and quantum black holes / Hawking radiation and
> evaporation (Ch. 8). Fulling is the complementary text on the *meaning* of the
> particle concept and the inequivalence of vacua under acceleration.

## Topic → location

| Topic (code symbol) | Source | Chapter / title | PDF p. (chapter start) |
|---|---|---|---|
| mode expansion, the vacuum, canonical commutators (`bogoliubov_check`) | BD | **Ch. 2** *Quantum field theory in Minkowski space* | 20 |
| Bogoliubov transformations α, β; particle creation ⟨N⟩ = Σ\|β\|² (`particle_number`, `squeeze_to_bogoliubov`) | BD | **Ch. 3** *Quantum field theory in curved spacetime* | 46 |
| the Unruh effect; Rindler observer; thermal spectrum \|β_ω\|²/\|α_ω\|² = e^{−2πcω/a} (`unruh_temperature`, `unruh_beta_ratio`, `unruh_occupation`, `bose_occupation`, `thermal_beta_squared`) | BD | **Ch. 4** *Flat spacetime examples* (§4.5, accelerated observers) | 99 |
| quantum black holes; surface gravity κ; T_H = ℏκ/2πck_B; evaporation τ ∝ M³ (`surface_gravity`, `hawking_temperature`, `schwarzschild_radius`, `evaporation_lifetime`) | BD | **Ch. 8** *Quantum black holes* | 259 |
| the particle concept, inequivalent vacua, accelerated observers (conceptual backing for `bogoliubov_check`, `unruh_temperature`) | Ful | field quantization & Bogoliubov transformations; thermal effects for accelerated/black-hole observers | — (no ToC layer) |

## Cross-module dependency
**None for the code** — `code/curved_spacetime.py` defines its SI constants locally
and imports only `numpy`, so it runs in place with no sibling modules. Conceptually
it sits on top of `~QF-01` (the quantized field and its vacuum), `~RE-14` (the
Schwarzschild horizon r_s = 2M and surface gravity κ, here re-expressed in SI by
`schwarzschild_radius`/`surface_gravity`), and `~RE-13` (the Einstein equations and
the stress-energy ⟨T_μν⟩ that back-reacts during evaporation).

## See also
- `~RE-14` (Schwarzschild & black holes — the classical horizon, redshift, and
  surface gravity that Hawking's Bogoliubov β is built on) and `~RE-13` (Einstein
  field equations / stress-energy source).
- `~QF-01` (canonical field quantization & the vacuum) — the structure this module
  shows is observer-dependent.
- `~QO-05` (squeezing & nonclassical light) — the two-mode-squeezer reading
  α = cosh r, β = sinh r is the optics behind the user's **Quantum_Optics
  curved-spacetime / squeezed-spacetimes** drafts (the `(-> Quantum_Optics
  curved-spacetime)` link on the `[QF]` trunk in `topic_network.txt`).
- `~SM-06`/`~SM-01` (the Bose–Einstein / Planck distribution that the Unruh and
  Hawking spectra turn out to be) and `~RE-15` (FLRW cosmological particle creation,
  the same Bogoliubov machinery in an expanding universe).
- Birrell & Davies Ch. 2–4 and Ch. 8 (the rigorous treatment); Fulling (the
  conceptual companion on the particle concept and accelerated vacua).
