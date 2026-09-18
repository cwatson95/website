# CM-24 — References

This module is the **mechanics application of `~MA-22`** (topology & dynamical
systems). The mathematical content — linear stability by Jacobian eigenvalues,
the logistic map, the Lyapunov exponent — is built and cited there.

| Source | Where | Note |
|---|---|---|
| `~MA-22` `topo_dynamics` | `classify_equilibrium`, `lyapunov_logistic` | reused directly here |
| Chicone, *Ordinary Differential Equations with Applications* | §1.6 (stability from eigenvalue real parts, pp.20–23) | verified in `~MA-22` refs (text-verified) |
| `~MA-07` | `integrate` (RK4) | used for the flows / limit cycle |

## Shelf note (honest)
- Marion & Thornton 5e **does** have a chapter on this — **Ch.4 "Nonlinear
  Oscillations and Chaos"** — but it is an **image-only scan and was not folio-verified
  for this module**, so no page is cited (per the project's "a wrong page is worse
  than none" rule). If wanted, an agent can verify the §4.x pages later.
- Fowles & Cassiday and Goldstein have no dedicated nonlinear-dynamics chapter.
- The **Chicone** caveat from `~MA-22` applies: stability is classified by the
  **sign of the eigenvalues' real parts** (pp.20–23) — there is no "trace–determinant
  plane" diagram in that text.
