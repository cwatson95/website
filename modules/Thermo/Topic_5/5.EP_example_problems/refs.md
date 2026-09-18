# 5.EP — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Example | Title | Eq. used | Printed p. | PDF p. |
|---|---|---|---|---|
| **3.2** (`ex_3_2`) | Heating Water at Constant Volume | 3.1, 3.2 | 109–111 | 127–129 |
| **3.4** (`ex_3_4`) | Analyzing Two Processes in Series | 2.17, 3.2/3.6 | 118–119 | 136–137 |
| **6.1** (`ex_6_1`) | Evaluating Work and Heat Transfer for an Internally Reversible Process of Water | 2.17, 6.23 | 303–304 | 321–322 |
| in-text (`ex_superheat_uh`) | superheated water from `u`; `h = u + pv` | 3.4 | 112 | 130 |
| in-text (`ex_mollier`) | Mollier (h–s) isentropic expansion | 6.4 | 296 | 314 |

## Verified book answers (all reproduced)
- **3.2:** `v₁=0.8475 m³/kg`, `T₁=99.63 °C`, `T₂=111.4 °C`, `m=0.59 kg`, `mg₁=0.295 kg`,
  `x₂=0.731`, `mg₂=0.431 kg`, `p₃=2.11 bar`.
- **3.4:** `v₁=0.3066`, `u₁=2957.3`, `v₂=0.1944`, `W/m=−112.2`, `x₃=0.494`, `u₃=1584.0`,
  `Q/m=−1485.5 kJ/kg`.
- **6.1:** `W/m=186.38 kJ/kg`, `Q/m=2114.1 kJ/kg` (`psat(150 °C)=4.758 bar`).
- **p.112:** `v=1.793`, `u=2537.3`, `h=2716.6 kJ/kg` (and `h=u+pv` reproduces `h`).
- **p.296:** Moran's chart values `x₂≈0.98`, `h₂≈2537 kJ/kg`; table computation `x₂≈0.979`,
  `h₂≈2535` (within chart-reading accuracy — the book itself calls these "agree closely").

> **Not reproduced (data scope):** Example 3.1 (ammonia, Table A-15E) and Example 3.3
> (English-unit water, Tables A-2E/A-4E) are valid Moran examples but lie outside the
> embedded dataset, which is **SI water only** (`steam_tables/`). Example 3.5 is an IT
> software exercise (no new numbers). These are flagged here rather than reproduced.

Steam-table data: `modules/Thermo/steam_tables/` (A-2…A-4). Provenance in that README.

## See also
`5.1`–`5.5` (the relations these examples apply), `5.EQ` (equation registry), `5.HP`
(end-of-chapter homework).
