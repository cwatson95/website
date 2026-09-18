# MACRO_EM-02 — References

Page-level citations **verified by extracting the page text** from the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Wilcox & Thron, *Macroscopic Electrodynamics: An Introduction*, **2nd ed.** | `books/macro_electrodynamics_wilcox.pdf` | PDF = printed **+ 23** |

Offset confirmed against page text (PDF p.92 carries printed "69", the start of
§2.14 Exercises; PDF p.52 carries printed "29", the chapter opening). The book
works in **Gaussian units** ($\vec\nabla\cdot\vec E=4\pi\rho$, $\Phi=q/r$); this
module keeps that convention.

## Topic → location (chapter body)

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| Coulomb field, superposition, ρ (Eqs. 2.1–2.5) | §2.1 *Electric field: definition* | 29–30 | 52–53 |
| δ as limit of scaled bumps; sampling, scaling, δ(f(x)) (2.6–2.16) (`lorentzian_delta`) | §2.2 *The Dirac delta function…* | 31–33 | 54–56 |
| curvilinear δ, Jacobian & scale factors (2.25–2.30) (`jacobian_matrix`, `scale_factors`) | §2.2 (end) | 35–36 | 58–59 |
| Fourier representation (2.31–2.34) | §2.2 (end) | 36 | 59 |
| line/surface/membrane deltas (2.35–2.39) | §2.3 *Line and surface delta functions* | 37–38 | 60–61 |
| solid angle dΩ (2.42), Gauss law (2.44–2.47) (`flux2d`, `gauss_flux_sphere`) | §2.4 *Gauss' law and solid angles* | 38–41 | 61–64 |
| potential Φ, Poisson, ∇²(1/r)=−4πδ (2.48–2.55) | §2.4 (end) | 41–42 | 64–65 |
| ε-modified potential (2.56–2.60) (`phi_shell_eps`) | §2.5 *Verification of the inverse square law…* | 42–43 | 65–66 |
| concentric shells Φ_out/Φ_in (2.62–2.63), q_a result (2.65), photon-mass reading (`qa_eps_exact`) | §2.5 (end), Fig. 2.10 | 44–45 | 67–68 |
| surface-charge jumps (2.66–2.75) | §2.6 *Surface charge and dipole layers* | 45–46 | 68–69 |
| dipole layer D=σd, Φ, ΔΦ=4πD (2.76–2.81) (`phi_dipole_disk_axis`) | §2.6 (end), Fig. 2.13 | 47–49 | 70–72 |
| Green's first identity (2.83), D/N/mixed uniqueness (2.84–2.89), σ=∂ₙΦ/4π (2.92) | §2.7 *Boundary conditions and uniqueness* | 49–51 | 72–74 |
| G_D definition & representation (2.93–2.100) | §2.8 *Dirichlet and Neumann Green functions* | 51–52 | 74–75 |
| G_N: −4π/S condition, representation, ⟨Φ⟩ (2.101–2.106) | §2.8 | 53 | 76 |
| symmetry of G; symmetrization (2.107–2.111) (`gn1_symm`) | §2.8 | 54–55 | 77–78 |
| source-on-boundary surface deltas (2.112–2.123) | §2.8 (end) | 55–58 | 78–81 |
| 1-D G_D construction (2.124–2.136) (`gd1`) | §2.9 *One-dimensional Green function examples* | 58–59 | 81–82 |
| 1-D Neumann BCs (2.137), representation (2.138), G_N^symm (2.139) (`gn1_unsym`, `gn1_symm`) | §2.9 (end) | 60 | 83 |
| assembly energy → field energy w=E²/8π (2.140–2.147) (`ball_self_energy`) | §2.10 *Electrostatic energy* | 60–61 | 83–84 |
| point self-energy linear divergence (2.148–2.149); G as interaction energy; Thompson's theorem | §2.10 (end) | 61–62 | 84–85 |
| averaged-field force, F/A = 2πσ² (2.156–2.161) (`surface_force_per_area`) | §2.11 *Normal force on a charged surface* | 63–64 | 86–87 |
| C_ij from G_D (2.162–2.166), symmetry (2.167), W=½ΣC_ijV_iV_j (2.168–2.170) (`cap_matrix_shells`) | §2.12 *Capacitance* | 65–66 | 88–89 |
| ΣᵢC_ij=0 (2.171–2.175), isolated C (2.176–2.177), sum rule (2.178), plates (2.179–2.182) (`system_capacitance`) | §2.12 (end) | 66–68 | 89–91 |
| photon-mass & capacitance reading list | §2.13 *Going Deeper* | 68 | 91 |
| **Exercises 2.1.1–2.12.11 (41)** | **§2.14 Exercises** | **69–86** | **92–109** |

## Exercise block → pages

| Exercises | Printed pp. | PDF pp. |
|---|---|---|
| 2.1.1, 2.2.1–2.2.2 | 69 | 92 |
| 2.2.3–2.2.4, 2.4.1 | 70 | 93 |
| 2.4.2–2.4.4 | 71–73 | 94–96 |
| 2.5.1–2.5.2 | 73–74 | 96–97 |
| 2.6.1–2.6.4 | 74–77 | 97–100 |
| 2.7.1–2.7.3 | 77–78 | 100–101 |
| 2.8.1–2.8.3 | 78–79 | 101–102 |
| 2.9.1–2.9.4 | 79–81 | 102–104 |
| 2.10.1–2.10.4 | 81–82 | 104–105 |
| 2.11.1 | 82 | 105 |
| 2.12.1–2.12.11 | 82–86 | 105–109 |

## See also (cross-trunk)

- `~EM-01` (Coulomb field) / `~EM-02` (Gauss law) / `~EM-03` (potential, Poisson) —
  the Griffiths-level (SI) versions of §§2.1–2.4; mind the unit dictionary
  ($4\pi\epsilon_0\to1$: $\rho/\epsilon_0\leftrightarrow4\pi\rho$).
- `~EM-04` (boundary-value problems) — uniqueness theorems and the image method
  that Wilcox Ch. 3 builds on top of this chapter's Green functions.
- `~EM-06` (conductors & capacitance) — the SI single-capacitor picture that
  §2.12 generalizes to the full $C_{ij}$ matrix.
- `~MA-14` (Green's functions) — the Sturm–Liouville/jump-condition construction
  used verbatim in §2.9 and Exercises 2.9.1–2.9.4.
- `~MA-15` (Dirac delta) — δ-sequences, δ(f(x)), and curvilinear deltas behind
  Exercises 2.2.1–2.2.4.
- Comparable treatments: Jackson, *Classical Electrodynamics* 3e Ch. 1
  (SI/Gaussian mix; his Problem 2.28 ≙ Exercise 2.8.3) and Ch. 2; Griffiths 4e
  Chs. 2–3 at gentler level.
