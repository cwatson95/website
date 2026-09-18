# QF-03 — References

| Book (edition) | File | Notes |
|---|---|---|
| Peskin & Schroeder, *An Introduction to Quantum Field Theory* (1995) | `QF_Quantum_Field_Theory/QFTPeskin.pdf` | **primary**; cited at **section level** (Ch. 4 QED & minimal coupling, Ch. 5 & 7 the Ward identity) |
| Zee, *Quantum Field Theory in a Nutshell*, **2nd ed.** | `QF_Quantum_Field_Theory/Zee_QFT.pdf` | cross-cite for the massless photon (§III.4) and non-abelian gauge theory (Part IV); cited at **section/part level** |

> **Granularity.** Citations are given by **section number and title**, which are
> stable across printings; printed↔PDF page offsets were **not** verified here, so no
> page numbers are quoted (cf. `~SM-06/refs.md`, which does verify pages). Open the
> PDFs above and tighten to page level if needed. Peskin section titles follow the
> 1995 first edition; Zee follows the 2nd edition.

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| local gauge invariance, covariant derivative D_μ = ∂_μ + ieA_μ, minimal coupling, F_μν, the QED Lagrangian (`covariant_derivative`, `field_strength`, `gauge_transform`) | Pe | §4.1 *Perturbation Theory — Philosophy and Examples* (the QED Lagrangian & gauge transformation) |
| the QED interaction vertex −ieγ^μ; gauge structure of the photon propagator | Pe | §4.8 *Feynman Rules for Quantum Electrodynamics* |
| static potential from one-boson exchange; the Yukawa potential and its m → 0 (Coulomb) limit (`yukawa_to_coulomb`) | Pe | §4.7 *Feynman Rules for Fermions* (the Yukawa-potential example) |
| the Ward identity k_μℳ^μ = 0 (photon polarization sums) | Pe | §5.5 *Photon Polarization Sums* |
| the Ward–Takahashi identity (general proof) | Pe | §7.4 *The Ward–Takahashi Identity* |
| geometry of gauge invariance (deeper, non-abelian) | Pe | §15.1 *The Geometry of Gauge Invariance* |
| gauge invariance forbids a photon mass — "a photon can find no rest" | Zee | §III.4 *Gauge Invariance: A Photon Can Find No Rest* |
| non-abelian gauge theory (Yang–Mills, the SU(N) generalization) | Zee | Part IV (*Symmetry and Symmetry Breaking*; non-abelian gauge theory) |

## See also
- `~EM-09` — the **classical, abelian seed**: the gauge freedom **A** → **A** + ∇λ
  that leaves **B** = ∇×**A** unchanged is exactly `gauge_transform` here, and its
  field-theory promotion to a *local phase symmetry* is the whole content of QF-03
  (**KEY BRIDGE B8**: `~MA-18` → `~CM-18` → QF-03).
- `~CM-18` (Noether: the global U(1) gives the conserved current j^μ = ψ̄γ^μψ) and
  `~MA-18` (U(1) and Lie groups, the symmetry being gauged).
- `~EM-18` — the relativistic field tensor F^{μν} that `field_strength` builds
  (F_{0i} = E_i, F_{ij} = −ε_{ijk}B_k); `~EM-01` — the Coulomb 1/r the massless
  photon produces; `~QM-04` — the minimal-coupling gauge-invariant current.
- `~QF-01` (the quantized Dirac/EM fields underlying ℒ_QED), `~QF-02` (Feynman
  diagrams / the vertex), and `~QF-04` (renormalization, protected by gauge symmetry).
- Higher-level / complementary: Peskin Ch. 15 (the geometric, non-abelian view);
  Weinberg, *The Quantum Theory of Fields* Vol. 1 (`QF_Quantum_Field_Theory/Weinberg_The_Quantum_Theory_of_Fields_vol_1.pdf`),
  Ch. 8 (the gauge principle from massless-particle consistency).
