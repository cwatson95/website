# 10.EP — References

Examples read page-by-page from the PDF. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| 5.1 | Evaluating Power Cycle Performance | 266–267 | 284–285 |
| 5.2 | Evaluating Refrigerator Performance | 268–269 | 286–287 |
| 5.3 | Evaluating Heat Pump Performance | 269–270 | 287–288 |
| S.1 | Ideal Stirling Engine with Regeneration | *module-authored* | — |

**No worked Stirling Example in Moran** — verified by reading §9.8.4 *Ericsson and
Stirling Cycles* (printed p.552–553, PDF 570–571): the section is descriptive, with no
numbered Example; the chapter's Stirling numerics appear only as end-of-chapter
Problems 9.102–9.103 (p.601, PDF 619; worked in `10.HP`). Ex S.1 is this module's
book-style replacement, driven by `10.2`'s functions with a `10.1` Carnot cross-check.

## Equations used
Carnot ceilings `η_max`/`β_max`/`γ_max` (Eqs. 5.9–5.11, p.265/267); efficiency and COP
definitions `η = W/Q_H`, `η = 1 − Q_C/Q_H`, `β = Q_C/W`, `γ = Q_H/W` (Eqs. 5.4, p.256;
5.5–5.6, p.259; 2.42, p.74); isothermal ideal-gas heat/work (Eq. 2.17 form, p.48–49);
regenerator duty `c_v(T_H−T_C)` (§9.8.4, p.552; Eq. 3.50 form, p.140). Canonical
implementations: `10.1`/`10.2` (concept modules), aggregated in `10.EQ`. Ex 5.3 uses
`1 kW·h = 3413 Btu` (as quoted in the example).

## See also
`10.EQ` (the equations these use), `10.HP` (end-of-chapter problems incl. the Ch.9
Stirling problems), and the concept modules `10.1`, `10.2`.
