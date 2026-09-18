# 12.EP — References

Examples read page-by-page from the PDF. **PDF = printed + 18.**

| Book | File | Offset |
|---|---|---|
| Moran et al., *Fundamentals of Engineering Thermodynamics*, **8th ed.** | `modules/Thermo/thermodynamics.pdf` | printed + 18 |

| Example | Title | Printed p. | PDF p. |
|---|---|---|---|
| 13.1 | Determining the Air–Fuel Ratio for Complete Combustion of Octane | 809–810 | 827–828 |
| 13.2 | Using a Dry Product Analysis for Combustion of Methane | 811–812 | 829–830 |
| 13.4 | Analyzing an Internal Combustion Engine Fueled with Liquid Octane | 819–821 | 837–839 |
| 13.5 | Analyzing a Gas Turbine Fueled with Methane | 821–823 | 839–841 |
| 13.6 | Analyzing Combustion of Methane with Oxygen at Constant Volume | 824–825 | 842–843 |
| 13.7 | Calculating Enthalpy of Combustion of Methane | 826–827 | 844–845 |
| 13.8 | Determining the Adiabatic Flame Temperature for Complete Combustion of Liquid Octane | 830–832 | 848–850 |
| 14.1 | Evaluating the Equilibrium Constant at a Specified Temperature | 891–892 | 909–910 |
| 14.2 | Determining Equilibrium Composition Given Temperature and Pressure | 892–893 | 910–911 |

> **Page note.** `code/examples.py` headers cite Ex 13.6 as "p.823": the closed-system
> energy balance it applies (Eqs. 13.16–13.17b) is developed on p.823; the Example
> itself begins on p.824. All other code page cites coincide with the Example headers.

## Equations used
Element balances & air model, AF̄→AF (Eq. 13.2, §13.1.2, p.807–808); dew point
`p_v = y_v p` (§13.1.3, p.811–812); `h = h°f + Δh` (Eq. 13.9, p.817); steady-flow
energy balance (Eqs. 13.12b/13.15b, p.818–819); closed-system form (Eq. 13.17b, p.823);
enthalpy of combustion & heating values (Eq. 13.18, §13.2.3, p.825–826); adiabatic
flame balance (Eqs. 13.21a/b, §13.3.1, p.829); `ΔG° = Σν(h̄−Ts̄°)`, `ln K = −ΔG°/R̄T`,
`K` composition form, inverse rule (Eqs. 14.29b/14.31/14.32/14.34, p.890); `K` in moles
(Eq. 14.35, p.892). Canonical implementations in module `12.EQ`.

## Table data embedded (verified)
**Table A-25** (p.970 / PDF 988): h°f CO₂ −393,520; H₂O(l) −285,830; H₂O(g) −241,820;
CO −110,530; CH₄(g) −74,850; C₈H₁₈(l) −249,910; s̄° CO₂ 213.69, CO 197.54, O₂ 205.03.
**Table A-23** (SI p.965–968 / PDF 983–986): the 298/730/900/1000/2000/2350/2400/2500 K
h̄ and s̄° entries quoted in each solution (e.g. Ex 13.8's iteration sums 4,955,163 /
5,089,337 / 5,358,748 regenerate exactly from the 2350/2400/2500 K rows).
**Table A-27** (p.972 / PDF 990): `CO₂ ⇌ CO + ½O₂` column −45.066 (298 K), −2.884
(2000 K), −1.440 (2500 K). English data in Ex 13.4 are the A-25E/A-23E values printed
in its solution (p.820).

## Verified book answers
13.1: 12.5 / 59.5 / 15.1; 89.25 / 22.6 / φ=0.67 (Quick Quiz). 13.2: 10.2 / 23.1 / 20.4;
10.78 / 19.47 / 113%; 0.169 / 2.484 psi / 134 °F; 0.489. 13.4: −107,530 / −1,752,251 /
−22.22 Btu/s. 13.5: −359,475 / 0.02078 kmol/s / 5.74 MW. 13.6: −745,436 kJ / 3.02 atm.
13.7: −890,330 (−55,507) / −802,310 (−50,019) / −800,552 (−49,910; book's mid-solution
"−800,522" is a print typo). 13.8: 5,074,630 / 2395 K (IT 2394) / 962 K. 14.1: −257,253,
103.83, 45.093 / −110,453, 6.643, 2.885. 14.2: K=0.0363; z=0.129, y=(0.121, 0.061,
0.818); z=0.062, yCO₂=0.91. (All reproduced.)

## See also
`12.1` (combustion stoichiometry & first law), `12.2` (equilibrium constant &
ionization), `12.EQ` (equation registry), `12.HP` (end-of-chapter homework).
