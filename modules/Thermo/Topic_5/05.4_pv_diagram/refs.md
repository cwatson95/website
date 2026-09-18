# 5.4 — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Topic (code symbol) | Section № & title | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| p–v–T surface | §3.2.1 *p–v–T Surface* | — | 97 | 115 |
| p–v diagram, dome, critical point | §3.2.2 *Projections of the p–v–T Surface* | — | 99–100 | 117–118 |
| boundary work `δW = p dV` | §2.2.3 *Expansion or Compression Work* | **2.16** | 48 | 66 |
| work `W = ∫p dV` (area on p–V) (`work_pdV`, `work_isobaric`) | §2.2.5 *(area interpretation)* | **2.17** | 48–49 | 66–67 |
| polytropic / isothermal closed forms (`work_polytropic`, `work_isothermal_ideal_gas`) | Example 2.1 *Evaluating Expansion Work* | — | 50–51 | 68–69 |

Worked checks: **Ex 2.1** polytropic gas `p₁=3 bar`, `V₁=0.1→V₂=0.2 m³`: `n=1.5` →
`W=17.6 kJ`, `n=1` → `20.79 kJ`, `n=0` → `30 kJ` (p.50–51). Isobaric water-work terms of
**Ex 3.4** (`W/m=−112.2 kJ/kg`, p.119) and **Ex 6.1** (`W/m=186.38 kJ/kg`, p.304) are
reproduced here and in `5.EP`.

> This module needs no steam-table data — it integrates `p` over `V` for a given path.
> The `p`–`V` end states for the water examples come from `5.1`/`5.2` (the steam tables).

## See also
`5.1` (the dome the p–v diagram bounds), `5.5` (the T–s diagram — area = heat),
`5.EP` (Examples 3.4, 6.1), `5.EQ`.
