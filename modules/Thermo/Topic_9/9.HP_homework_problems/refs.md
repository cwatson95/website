# 9.HP — References

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Problem | Topic | Section / source | Printed p. | PDF p. |
|---|---|---|---|---|
| P1 | Carnot ceiling verdicts | §5.9.1 (Eq. 5.9) | 265 | 283 |
| P2 | Otto cycle, cold air-standard | §9.2 (Eqs. 9.6–9.8) + mep §9.1 (Eq. 9.1) | 511, 514–515 | 529, 532–533 |
| P3 | compression ratio for target η | §9.2 (Eq. 9.8 inverted) | 515 | 533 |
| P4 | Diesel cycle, cold air-standard | §9.3 (Eqs. 9.12–9.13) | 519 | 537 |
| P5 | cutoff-ratio effect vs Otto | §9.3 (Eq. 9.13; bracket > 1 discussion) | 519–520 | 537–538 |
| P6 | dual cycle brackets Otto/Diesel | §9.4 (Eq. 9.14 cold closed form) | 522–523 | 540–541 |
| P7 | ideal Brayton, cold air-standard | §9.6.2 (Eqs. 9.23–9.25) + bwr (Eq. 9.20) | 528–529, 532 | 546–547, 550 |
| P8 | Brayton with η_t, η_c | §9.6.3 | 535 | 553 |
| P9 | Brayton with regenerator | §9.7 (Eqs. 9.26–9.27) | 538–539 | 556–557 |
| P10 | ideal Rankine (60 → 0.10 bar) | §8.2.1–8.2.2 (Eqs. 8.1–8.7b) | 446–449 | 464–467 |
| P11 | condenser-pressure effect | §8.2.3 (Fig. 8.4b) | 453–454 | 471–472 |
| P12 | boiler-pressure effect + Carnot | §8.2.3 (Fig. 8.4a, Eq. 8.8) | 453–454 | 471–472 |

Worked **solutions** (Moran has no key). Each cycle is cross-checked for closure:
`q_in − q_out = w_net`, η below the Carnot ceiling (Eq. 5.9) at its temperature
extremes, bwr in the characteristic band (Brayton 40–80% per p.528; Rankine ~1–2% per
p.447–448), mep > 0, and the §8.2.3 pressure trends. Rankine saturation states come
from the project water tables (`modules/Thermo/steam_tables/A3_sat_water_pressure.csv`,
extracted from Moran Table A-3).

## See also
`09.1`–`09.6` (the cycles), `9.EQ` (equations), `9.EP` (worked Examples), `7.HP`
(performance-metric homework these problems extend).
