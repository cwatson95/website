# 12.2 — References  *(part B is ~PK, NOT Moran 8e)*

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

## (A) Moran trunk — chemical equilibrium / dissociation (Ch.14)
| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| chemical potential, ideal gas (`gibbs_of_reaction`) | §14.1 *Introducing Equilibrium Criteria* | 14.17 | 886 | 904 |
| equation of reaction equilibrium | §14.2 *Equation of Reaction Equilibrium* | 14.26 | 889 | 907 |
| equilibrium constant `K` (`equilibrium_constant_from_composition`) | §14.3.1 *Equilibrium Constant for Ideal Gas Mixtures* | **14.32** | 890 | 908 |
| `ΔG° = Σν(h̄−Ts°)` (`gibbs_of_reaction`) | §14.3.1 | **14.29b** | 890 | 908 |
| `ln K = −ΔG°/(R̄T)` (`lnK_from_gibbs`) | §14.3.1 | **14.31** | 890 | 908 |
| inverse reaction `log₁₀K*=−log₁₀K` (`log10K_inverse`) | §14.3.1 | **14.34** | 890 | 908 |
| equilibrium composition (`dissociation_extent_CO2`) | §14.3.2 *Calculating Equilibrium Compositions* | **14.35** | 892 | 910 |

Worked anchors (reproduced in `code/ionization.py`): **Ex 14.1** `K` for CO + ½O₂ ⇌ CO₂
(298 K: `ΔG°=−257,253`, `log₁₀K=45.093`; 2000 K: `ΔG°=−110,453`, `log₁₀K=2.885`)
p.891–892 / PDF 909–910; **Ex 14.2** CO₂ dissociation at 2500 K (`K=0.0363`, `z=0.129` at
1 atm, `0.062` at 10 atm) p.892–893 / PDF 910–911; **Ex 14.4** inert N₂ effect (`z=0.175`)
p.894–895 / PDF 912–913. Data: **Table A-25** (h°_f, s°; p.970 / PDF 988), **Table A-23**
(ideal-gas h̄(T); SI p.965–968 / PDF 983–986), **Table A-27** (log₁₀K).

## (B) Cross-trunk plasma extension — Saha ionization  *(~PK, NOT in Moran 8e)*
> The Saha equation and the electron quantum concentration are **not in Moran 8e** — there
> are no Moran §/Eq/page citations for part (B). They are standard results from
> statistical mechanics and plasma physics.

| Source (cross-trunk, ~PK) | Used for |
|---|---|
| M. N. Saha, *Phil. Mag.* **40**, 472 (1920) | the Saha ionization equation (original) |
| F. F. Chen, *Introduction to Plasma Physics and Controlled Fusion*, 3e | Saha equation, degree of ionization, plasma LTE |
| Rybicki & Lightman, *Radiative Processes in Astrophysics*, §9.5 | Saha equation, quantum concentration / partition functions |
| Carroll & Ostlie, *An Introduction to Modern Astrophysics*, §8.1 | Saha equation in stellar atmospheres (hydrogen ionization) |
| F. Reif, *Fundamentals of Statistical and Thermal Physics* | electron thermal de Broglie wavelength `λ = h/√(2πm_e k_BT)`, `n_Q = 1/λ³` |

CODATA constants used: `m_e = 9.1093837015e−31 kg`, `k_B = 1.380649e−23 J/K`,
`h = 6.62607015e−34 J·s`, `1 eV = 1.602176634e−19 J`. Literature anchor checked: electron
thermal de Broglie wavelength ≈ **4.30 nm at 300 K**. The Saha ionization fractions have
**no official answer key** and are presented as physically-consistent worked values
(bounded `0<x<1`, monotone in `T` and density, correct `T→0` / `T→∞` limits).

## See also
`12.1` (combustion enthalpies feeding `ΔG°`), `12.EP` (Ex 14.1/14.2 worked),
`12.EQ` (equation registry, cross-imports this module), `12.HP` (homework, §14 problems).
