# 12.EQ — References  *(Saha rows are ~PK, NOT Moran 8e)*

Verified by reading the page text. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

Per-equation §/page citations are in `equations.md` and in the concept modules' `refs.md`
(`12.1`, `12.2`). This module aggregates and machine-verifies them.

| Group | Module(s) | Equations | Printed p. | PDF p. |
|---|---|---|---|---|
| Stoichiometry, air model, AF ratio | `12.1` | 13.2, (13.3–13.5) | 806–809 | 824–827 |
| Products & dew point | `12.1` | `p_v = y_v p` | 811–812 | 829–830 |
| Enthalpy of formation | `12.1` | 13.9 | 816–817 | 834–835 |
| Steady-flow energy balance | `12.1` | 13.12b, 13.15b | 818–819 | 836–837 |
| Closed-vessel energy balance | `12.EP` (Ex 13.6) | 13.16–13.17b | 823 | 841 |
| Enthalpy of combustion, HHV/LHV | `12.1` | 13.18 | 825–826 | 843–844 |
| Adiabatic flame temperature | `12.EP` (Ex 13.8) | 13.21a/b | 828–829 | 846–847 |
| Chemical potential / reaction equilibrium | `12.2` | 14.17, 14.26 | 886, 889 | 904, 907 |
| Equilibrium constant `K(T)` | `12.2` | 14.29b, 14.31, 14.32, 14.34 | 890 | 908 |
| K in moles (equilibrium composition) | `12.2` | 14.35 | 892 | 910 |
| Ionization equilibrium | `12.HP` (P8) | 14.45, Ex 14.8 | 904–905 | 922–923 |
| van't Hoff (adjacent, **not** in registry) | — | 14.43b, 14.44 | 903–904 | 921–922 |
| Saha equation & quantum concentration | `12.2` part B | **~PK, NOT Moran** | — | — |

Book-verified anchor values used by `test_equations.py`: Ex 13.1 (AF̄ 59.5/AF 15.1,
p.809–810), Eq. 13.4 methane (9.52 → 17.19, p.808), Ex 13.2 (113%, p_v 2.484 psi,
p.811–812), Eq. 13.9 spot value (CO₂@500 K = −3.852×10⁵, §13.3.2, p.829), Ex 13.5
(h̄_P −359,475, p.822), Ex 13.6 (Q −745,436, p₂ 3.02 atm, p.825), Ex 13.7 (890,330 /
55,507; 802,310 / 50,019, p.826–827), Ex 13.8 (RHS 5,074,630; T_P 2395 K, p.831),
Ex 14.1 (ΔG° −257,253 / −110,453; log₁₀K 45.093 / 2.885, p.891), Ex 14.2 (K 0.0363,
z 0.129, p.893), Ex 14.8 (K 15.63 @ z 0.95 → p 1.69 atm; Quick Quiz z 0.662, p.904–905).
Data: **Table A-25** (h°_f, g°_f, s̄°; p.970 / PDF 988), **Table A-23** (h̄(T), s̄°(T); SI
p.965–968 / PDF 983–986), **Table A-27** (log₁₀K; p.972 / PDF 990).

## Saha rows (~PK, NOT in Moran 8e)
> Moran §14.4.3 (p.904) applies the K machinery to ionization but obtains K values
> "using the procedures of statistical thermodynamics" without stating them. The Saha
> equation is that missing formula; it and the electron quantum concentration are
> flagged **~PK** and carry **no Moran §/Eq/page**.

| Source (cross-trunk, ~PK) | Used for |
|---|---|
| M. N. Saha, *Phil. Mag.* **40**, 472 (1920) | the Saha ionization equation (original) |
| F. F. Chen, *Introduction to Plasma Physics and Controlled Fusion*, 3e | Saha equation, degree of ionization |
| Rybicki & Lightman, *Radiative Processes in Astrophysics*, §9.5 | Saha equation, quantum concentration |
| Carroll & Ostlie, *An Introduction to Modern Astrophysics*, §8.1 | Saha equation in stellar atmospheres |
| F. Reif, *Fundamentals of Statistical and Thermal Physics* | `λ = h/√(2πm_e k_BT)`, `n_Q = 1/λ³` |

CODATA constants as in `12.2`; literature anchor: electron thermal de Broglie wavelength
≈ **4.30 nm at 300 K**. The `K = S·k_BT/p_ref` bridge row is checked by exact algebraic
consistency against Moran's Eq.-14.35 ionization form (no external key exists).

## See also
`12.1`, `12.2` (the concept modules), `12.EP` (worked Examples 13.1–14.2 using these),
`12.HP` (homework, incl. the §14.4.3 ionization problems).
