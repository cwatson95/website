# 9.EQ — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Equation (function) | Section | Eq. № | Printed p. | PDF p. |
|---|---|---|---|---|
| Carnot ceiling (`carnot_efficiency`) | §5.9.1 | 5.9 | 265 | 283 |
| mean effective pressure (`mean_effective_pressure`) | §9.1 | 9.1 | 511 | 529 |
| Otto: air-table η, cold T₂/T₄, η(r) (`otto_*`) | §9.2 | 9.3, 9.6–9.8 | 514–515 | 532–533 |
| Diesel: air-table η, η(r, r_c) (`diesel_*`) | §9.3 | 9.11, 9.13 | 519 | 537 |
| dual: air-table η, closed form (`dual_*`) | §9.4 | 9.14, — | 523 | 541 |
| Brayton: works/heats, η, bwr (`brayton_*`) | §9.6.1 | 9.15–9.20 | 527–528 | 545–546 |
| Brayton: cold-air T₂/T₄, η(r_p) (`brayton_*`) | §9.6.2 | 9.23–9.25 | 529, 532 | 547, 550 |
| regenerator effectiveness (`regenerator_effectiveness`) | §9.7 | 9.27 | 539 | 557 |
| Rankine: component balances, η, bwr (`rankine_*`) | §8.2.1 | 8.1–8.6 | 446–447 | 464–465 |
| Rankine: pump-work approximation (`rankine_pump_work_approx`) | §8.2.2 | 8.7b | 449 | 467 |

Book-verified check values come from Examples 5.1 (Carnot), 9.1 (Otto, p.515–517),
9.2 (Diesel, p.520–521), 9.3 (dual, p.523–524), 9.4/9.7 (Brayton, p.529–531, 539–541),
and 8.1 (Rankine, p.450–452) — the same Examples regenerated in `9.EP`.

## See also
The six concept modules `09.1`–`09.6` (cross-imported by `test_equations.py`),
`9.EP` (worked Examples), `9.HP` (homework), `7.EQ` (η/COP metrics these cycles feed).
