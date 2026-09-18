# PK-01 — References

| Book (edition) | File | Notes |
|---|---|---|
| Michel, *Introduction to Laser-Plasma Interactions* (Springer, Graduate Texts in Physics, 2023) | `PK_Plasma_Kinetic_Theory/Laser_plasma_pierre_michel.pdf` | **primary source**; cited at **section level** from the book's own embedded outline (PDF page given as the navigable locator) |
| Rhodes (ed.), *Excimer Lasers* (Topics in Applied Physics **30**, 2nd enlarged ed., Springer, 1984) | `PK_Plasma_Kinetic_Theory/Excimer_Lasers_Topics_Rhodes.pdf` | the **excimer/KrF application** context (`~PK-04`); no embedded outline, cited at **chapter level** with printed pages read from its Contents |
| Pathria & Beale, *Statistical Mechanics*, 3rd ed. | `SM_Statistical_Mechanics/PathriaStatMech.pdf` | cross-shelf: kinetic theory & the Maxwellian (§6.4); page-verified in `~SM-06` |

> Michel's section numbers/titles are taken from the PDF's embedded outline and were
> confirmed by opening the pages; the **PDF page** is the verified locator. Printed↔PDF
> offsets were *not* separately pinned (≈ −14: §1.2.1 prints as p.7), so citations are
> by **section**, in the spirit of `~SM-06`'s treatment of the image-only Schroeder.
> Michel's Appendix A.1 "Plasma Parameters" is the formulary the code follows verbatim:
> ω_pe (A.1), v_Te = √(T_e/m) (A.4), λ_De = v_Te/ω_pe (A.6), N_De = n_e λ_De³ (A.8).

## Topic → location

| Topic (code symbol) | Source | Section / title | Locator |
|---|---|---|---|
| distribution function & Maxwellian (`maxwellian`, `thermal_speed`) | Mi | §1.2.3 *Equilibrium (Maxwellian) Velocity Distributions in Plasmas* | PDF p.25 |
| Debye length & screening (`debye_length`) | Mi | §1.2.1 *The Plasma State; Debye Length and Screening* | PDF p.21 |
| plasma frequency (`plasma_frequency`) | Mi | §1.2.2 *The Plasma Frequency* | PDF p.24 |
| plasma parameter Λ = nλ_D³ (`plasma_parameter`) | Mi | §1.2.1; Appendix A.1, Eq. (A.8) N_De = n_e λ_De³ | PDF p.21 / 415 |
| Vlasov equation & phase-space continuity (`free_stream`, `vlasov_residual`) | Mi | §1.2.4.1 *The Vlasov Equation* (in §1.2.4 *Kinetic (Vlasov) and Fluid Descriptions*) | PDF p.28 |
| parameter formulary (ω_p, v_T, λ_D, N_De) | Mi | Appendix A.1 *Plasma Parameters*, Eqs. (A.1),(A.4),(A.6),(A.8) | PDF p.415 |
| collisions; moments → fluid (Boltzmann RHS; `~PK-02`) | Mi | §1.4 *Electron-Ion Collisions*; §1.2.4.2 *The Fluid Equations* | PDF p.65 / 29 |
| Landau damping (forward link `~PK-03`) | Mi | §1.3.4 *Landau Damping* | PDF p.50 |
| excimer / KrF kinetics (application, `~PK-04`) | Rh | Ch.4 *Rare Gas Halogen Excimers*, §4.2 *Reaction Kinetics*; §7.2 *KrF\* System (248 nm)* | printed p.87, 96, 220 |
| Maxwell–Boltzmann distribution & transport (cross-shelf) | Pa | §6.4 *Kinetic considerations* | see `~SM-06` |

## See also
- `~SM-06` (the Maxwellian & Boltzmann transport equation — KEY BRIDGE B10) and
  `~MA-19` (probability distributions & moments) — the prerequisites.
- `~CM-22` (continuity of mass) and `~QM-04` (continuity of probability) — the other
  faces of **KEY BRIDGE B2**; the `vlasov_residual` check mirrors `~QM-04`'s `continuity_residual`.
- `~PK-02` (velocity moments → fluid / MHD), `~PK-03` (plasma waves & Landau damping),
  `~PK-04` (excimer rate kinetics / EEDF — the KrF/LoKI simulator in this repo).
- Michel §1.2 & Appendix A.1 (primary, rigorous); Rhodes Ch.4 & §7.2 (the KrF
  application); Pathria §6.4 (gentle kinetic theory, cross-shelf).
