# 13.HP — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Problem | Topic | Printed p. | PDF p. |
|---|---|---|---|
| 9.113 | sonic velocity of air / CO₂ / He | 601 | 619 |
| 9.121 | derive & evaluate critical (sonic) ratios | 601 | 619 |
| 9.123 | converging nozzle, gas mixture (choked) | 602 | 620 |
| 9.124 | converging nozzle, air / CO₂ / argon | 602 | 620 |
| 9.125 | converging nozzle, effect of raising po | 602 | 620 |
| 9.136 | normal shock (py, pox) | 602 | 620 |
| 9.137 | C–D nozzle, shock at exit plane | 603 | 621 |

Equations used: 9.37 (c=√kRT), 9.50/9.51 (isentropic ratios) and their M=1 critical
limits, 9.51-inverse (M from p), 9.53/9.54/9.55 (normal-shock functions). Worked
**solutions** (Moran has no key); each is cross-checked for physical consistency.

> **Unverifiable against the book:** Moran prints no answers for these problems, so the
> tabulated numbers are this module's *worked solutions*. The `k`/`M` used for each gas
> (Table A-20 room-temperature ideal-gas values) are stated in `homework.py`; 9.113's
> CO₂/air results in particular depend on that `k` choice and high-T `k` variation is
> neglected (cold-gas-standard).

## See also
`13.1`–`13.3` (the relations these problems apply), `13.EP` (the Ch.9 *examples*),
`13.EQ` (equation registry).
