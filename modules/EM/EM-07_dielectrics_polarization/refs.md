# EM-07 — References

Page-level citations **verified by reading the page text** in the PDF.
**Printed** = number on the page; **PDF** = viewer page index.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Griffiths, *Introduction to Electrodynamics*, **4th ed.** (2017 reissue) | `EM_Electricity_Magnetism/GriffithsEM.pdf` | PDF = printed **+ 18** |

The offset was confirmed against the page text (PDF p.185 carries printed "167", the start
of §4.1.2 *Induced Dipoles*). Griffiths is the worked source for the whole EM-01..EM-10
sequence; Jackson 3e and Schwinger sit at a higher level (see *See also*).

## Topic → location

| Topic (code symbol) | Section / title | Printed p. | PDF p. |
|---|---|---|---|
| induced dipoles **p** = α**E** (polarizability α) | §4.1.2 *Induced Dipoles* (Eq. 4.1) | 167 | 185 |
| polarization **P** (definition) | §4.1.4 *Polarization* | 172 | 190 |
| bound charge (`bound_surface_charge`, `bound_volume_charge`) | §4.2.1 *Bound Charges* (Eq. 4.11–4.12) | 173 | 191 |
| uniformly polarized sphere (`polarized_sphere_surface_charge`, `polarized_sphere_inner_field`) | §4.2.1 *Bound Charges*, Ex. 4.2 | 173 † | 191 † |
| displacement **D** = ε₀**E** + **P** (`displacement_field`, `displacement_point_free_charge`) | §4.3.1 *Gauss's Law in Presence of Dielectrics* (Eq. 4.21) | 181 | 199 |
| Gauss for **D**, ∮**D**·d**a** = Q_free (`free_charge_enclosed`) | §4.3.1 (Eq. 4.23) | 181 | 199 |
| susceptibility / permittivity / dielectric constant (`susceptibility_from_eps_r`, `permittivity`, `polarization_linear`, `displacement_linear`) | §4.4.1 *Susceptibility, Permittivity, Dielectric Constant* (Eq. 4.30, 4.32, 4.34) | 185 | 203 |
| dielectric-filled capacitor, C → ε_r C (`capacitance_with_dielectric`) | §4.4.1 (corollary of Eq. 4.32) | 185 † | 203 † |

† §4.2.1 begins on printed p.173 and §4.4.1 on printed p.185 (both spot-checked against the
map). Example 4.2 (the uniformly polarized sphere) sits a few pages into §4.2, and the
capacitance scaling is the immediate corollary of the dielectric constant within §4.4.1; the
*exact* sub-pages were not independently re-verified, so they are anchored to the verified
section starts.

## See also
- `~EM-01` for the vacuum Coulomb field (`coulomb_field`) and `EPS0`/`K_E`, reused by
  `displacement_point_free_charge` and `polarization_linear`.
- `~EM-02` for the flux integral (`flux_through_sphere`), reused by `free_charge_enclosed` —
  Gauss's law for **D** is EM-02's flux law applied to the displacement.
- `~MA-02` for `divergence`, reused by `bound_volume_charge` (ρ_b = −∇·**P**). Griffiths
  reviews this vector calculus in Ch. 1.
- `~EM-10` (Gr **Ch. 6**, magnetic materials) is the step-for-step magnetic analogue:
  **M**↔**P**, bound currents↔bound charge, **H**↔**D** — the same construction one chapter on.
- `~CMx` (condensed matter) for the microscopic origin of α and χ_e (Clausius–Mossotti, ε(ω)).
- Higher-level treatments: Jackson, *Classical Electrodynamics* 3e, **Ch. 4** (Multipoles,
  Electrostatics of Macroscopic Media, Dielectrics) (`EM/Jackson…SolutionManual…pdf` holds
  solutions only locally); Schwinger, *Classical Electrodynamics* (`EM_Electricity_Magnetism/SchwingerEM.pdf`).
