# 12.HP — References  *(P9 is ~PK, NOT Moran 8e)*

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Problem | Topic | Printed p. | PDF p. |
|---|---|---|---|
| P1 = 13.2 | ethane air–fuel ratio, theoretical air | 867 | 885 |
| P2 = 13.7 | butane at equivalence ratio 0.9 | 868 | 886 |
| P3 = 13.30 | hexane dry-product-analysis back-out, dew point | 869 | 887 |
| P4 = 13.17 | dodecane with 150% theoretical air, dew point | 868 | 886 |
| P5 = 13.59 | enthalpy of combustion of pentane | 871 | 889 |
| P6 = 13.51 | adiabatic flame temperature, liquid propane (h°_f = −118,900 given) | 871 | 889 |
| P7 = 14.32 | closed-vessel CO/O₂ equilibrium at 2500 K, final pressure | 919 | 937 |
| P8 = 14.67 | ionization-equilibrium constant of N at 12,000 K, 6 atm | 921 | 939 |
| P9 | **Saha ionization of hydrogen — ~PK, NOT in Moran** | — | — |

Methods/equations used: Eq. 13.2 & §13.1.2 stoichiometry (p.807–809), Ex 13.2 dry-basis
method & dew point (p.811–812), Eq. 13.18 & Table A-25 heating values (p.825–826, 970),
Eq. 13.21b flame-temperature iteration as in Ex 13.8 (p.829–831), Eq. 14.35 & Table A-27
(p.892, 972), §14.4.3 / Ex 14.8 ionization form (p.904–905).

Table data embedded in `homework.py` (page-verified): **A-2** p_sat at 40/45/50/55 °C =
0.07384 / 0.09593 / 0.1235 / 0.1576 bar (p.927–928 / PDF 945–946); **A-23** h̄ rows at
298, 1140, 1160, 2350, 2400 K for CO₂/H₂O/O₂/N₂ (p.965–968 / PDF 983–986); **A-25** h°_f
and pentane heating values 45,350 / 49,010 kJ/kg (p.970 / PDF 988); **A-27**
log₁₀K(2500 K) = −1.44 for CO₂ ⇌ CO + ½O₂ (p.972 / PDF 990); molecular weights from
**A-1** (p.926 / PDF 944; dodecane's 170.33 computed from atomic weights — not listed).

> **Unverifiable against the book:** Moran prints no answers for end-of-chapter
> problems, so every tabulated number is this module's *worked solution*, closed by the
> consistency checks in `test_homework.py`. P6's flame temperatures interpolate the
> embedded A-23 brackets (finer tables would shift them by a few K). P3's given dry
> analysis does not close its N₂ balance exactly (83.06 computed vs 83.3 reported —
> measurement round-off in the book's data); C/H/O balances are used, N₂ as the check,
> exactly as in Ex 13.2.

## (P9) Cross-trunk plasma extension — Saha ionization  *(~PK, NOT in Moran 8e)*
> Moran §14.4.3 (p.904) treats ionization with the K machinery but obtains K values
> from unstated "procedures of statistical thermodynamics". P9 computes that K from
> the **Saha equation** — flagged ~PK, with **no Moran §/Eq/page** and no book key;
> it is checked for physical consistency and for exact agreement with Moran's
> Eq.-14.35 ionization form (`K = S·k_BT/p_ref`, `z = √(K/(K+p/p_ref))`).

| Source (cross-trunk, ~PK) | Used for |
|---|---|
| M. N. Saha, *Phil. Mag.* **40**, 472 (1920) | the Saha ionization equation |
| F. F. Chen, *Introduction to Plasma Physics and Controlled Fusion*, 3e | degree of ionization, plasma LTE |
| Rybicki & Lightman, *Radiative Processes in Astrophysics*, §9.5 | Saha equation, quantum concentration |
| Carroll & Ostlie, *An Introduction to Modern Astrophysics*, §8.1 | hydrogen ionization fractions |
| F. Reif, *Fundamentals of Statistical and Thermal Physics* | electron thermal de Broglie wavelength |

## See also
`12.1` (stoichiometry & first law these problems apply), `12.2` (equilibrium constant &
Saha), `12.EP` (the Ch.13/14 worked *Examples*), `12.EQ` (equation registry).
