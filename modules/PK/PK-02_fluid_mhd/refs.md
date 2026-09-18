# PK-02 — References

| Book (edition) | File | Notes |
|---|---|---|
| Michel, *Introduction to Laser-Plasma Interactions* (Springer, Graduate Texts in Physics) | `PK_Plasma_Kinetic_Theory/Laser_plasma_pierre_michel.pdf` | **primary.** Section numbers/titles below are read directly off the PDF's table-of-contents bookmarks; cited at **section level** |
| Rhodes (ed.), *Excimer Lasers* (Topics in Applied Physics **Vol. 30**, Springer) | `PK_Plasma_Kinetic_Theory/Excimer_Lasers_Topics_Rhodes.pdf` | cross-cite for the excimer/KrF discharge-plasma context; the PDF has **no embedded outline**, so cited at **book/chapter level only** |

> **Citation granularity.** Citations are given at **section/chapter level, not page
> level.** Michel section numbers and titles are taken verbatim from the PDF
> bookmarks (verified to exist); the printed↔PDF page offset was **not** checked, so
> **no page numbers are quoted** here (contrast `~SM-06/refs.md`, which verifies
> Pathria page-by-page). The fluid-moment material — continuity (Michel Eq. 1.63) and
> the momentum/force equation (Michel Eqs. 1.73–1.74) — is in §1.2.4.2. The
> **MHD-specific** results (Alfvén speed, magnetic pressure, plasma β, ideal Ohm's law,
> induction / frozen-in flux) are **standard magnetized-plasma textbook material**;
> Michel's laser-plasma text is mostly *unmagnetized*, so those are cited at chapter
> level (Ch.1, the fluid framework) rather than to a dedicated MHD section.

## Topic → location

| Topic (code symbol) | Source | Section / title |
|---|---|---|
| (drifting) Maxwellian, thermal speed v_T = √(T/m) (`moments_of_maxwellian`) | Mi | §1.2.3 *Equilibrium (Maxwellian) Velocity Distributions in Plasmas* |
| velocity moments → fluid fields n, **u**, P, p = nk_BT (`moments_of_maxwellian`) | Mi | §1.2.4.2 *The Fluid Equations* (ensemble averages, the scalar pressure) |
| Vlasov equation the moments are taken of | Mi | §1.2.4.1 *The Vlasov Equation* (and §1.2.4 intro) |
| continuity = 0th moment, ∂n/∂t+∇·(n**u**)=0 (`continuity_residual`) | Mi | §1.2.4.2 (Eq. 1.63) |
| momentum/force = 1st moment, closure ∇p = γk_BT∇n (`sound_speed`) | Mi | §1.2.4.2 (Eqs. 1.73–1.74, polytropic γ = (N+2)/N) |
| acoustic / sound speed, dielectric-fluid wave framework (`sound_speed`) | Mi | §1.3.1 *Fluid Description: Dielectric Framework*; §1.3.2 *Rapid Derivation of the Wave Equations; Acoustic Waves…* |
| ideal MHD: Alfvén speed, magnetic pressure, plasma β, frozen-in flux (`alfven_speed`, `fast_magnetosonic_speed`, `magnetic_pressure`, `plasma_beta`) | Mi | Ch.1 (fluid framework; standard magnetized-plasma results — see granularity note) |
| excimer / KrF discharge-plasma kinetics (the per-species continuity moment with sources) | Rh | *Excimer Lasers*, rare-gas-halide formation & laser kinetics (book/chapter level) |

## See also
- `~PK-01` (the distribution function f and the Vlasov/Boltzmann equation these moments
  are taken of) and `~SM-06` (the identical moment construction for a neutral gas).
- `~CM-22` (mass continuity — the **same** law, KEY BRIDGE B2; mirrors the
  `continuity_residual` check) and `~CM-23` (the neutral Euler/Navier–Stokes limit).
- `~EM-13` (Maxwell's equations & Faraday's law behind the induction equation) and
  `~PK-03` (plasma waves & instabilities from these fluid equations).
- (→) `Kinetic_Modeling/KrF_and_LoKI` — the KrF/LoKI 0-D kinetics code is the
  per-species continuity (rate) moment with collisional source terms; this module is
  its spatially-resolved fluid generalization.
- Michel Ch.1 (rigorous moment derivation); Rhodes (excimer/KrF context, book level).
