# 13.5 — References  *(~CM, not from Moran 8e)*

**Cross-trunk module.** This content is **standard fluid mechanics and is NOT in Moran
8e** — there are no Moran section/equation/page citations for it. (Moran Ch.9 covers
*compressible* flow; Moran 8e never even defines the Reynolds number — the only
"Reynolds" in the book is a reviewer's name.) The relations are textbook results from
the fluid-mechanics literature.

| Source (cross-trunk, ~CM) | Used for |
|---|---|
| F. M. White, *Fluid Mechanics*, 7th ed., Ch. 6 (Viscous Flow in Ducts) | `Re`; Blasius `f=0.316/Re^{1/4}` (Eq. 6.38); Colebrook (Eq. 6.48); Haaland (Eq. 6.49); 1/n power-law profile (Sec. 6.6) |
| B. Munson et al., *Fundamentals of Fluid Mechanics*, Ch. 8 (Pipe Flow) | Darcy–Weisbach `ΔP=f(L/D)(ρV²/2)`, head loss `h_L=f(L/D)(V²/2g)` |
| Y. Cengel & J. Cimbala, *Fluid Mechanics*, Ch. 8 | regime boundaries (`Re≲2300` laminar, `2300–4000` transitional, `>4000` turbulent); Moody chart |
| J. Nikuradse / L. F. Moody (Moody chart, 1944) | fully-rough limit `1/√f = −2log₁₀(ε/D/3.7)` |

> No equations in this module are attributable to Moran 8e. Moran Ch.9 (Topic 13's
> primary trunk) covers *compressible* flow; the **viscous turbulent pipe flow** here is
> the fluid-mechanics counterpart, included as a cross-trunk bridge.

## See also
`13.4` (laminar pipe flow, the companion cross-trunk module — same `reynolds_number`,
cross-checked in `13.EQ`). The compressible-flow modules `13.1`–`13.3` and the support
modules `13.EQ`/`13.EP`/`13.HP` are Moran-based.
