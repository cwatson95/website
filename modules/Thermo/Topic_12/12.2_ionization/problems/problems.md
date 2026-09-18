# 12.2 — Problems

Check with `code/ionization.py`. Citations in `../refs.md`. **P1–P4 are Moran §14; P5–P6
are the ~PK Saha extension (NOT in Moran).** `K`, `y`, `z`, `x` dimensionless; `ΔG°`
kJ/kmol; `T` [K]; `n` [m⁻³]; `χ` [eV].

### P1.  Equilibrium constant from Gibbs data  *(Moran 8e Ex 14.1, Eqs. 14.29b/14.31, p.891)*
For `CO + ½O₂ ⇌ CO₂` at 298 K, use `h°_f` (CO₂ −393,520; CO −110,530) and `s°` (CO₂ 213.69;
CO 197.54; O₂ 205.03) to find `ΔG°`, `ln K`, `log₁₀K`.
*Answer:* `ΔG° = −257,253 kJ/kmol`, `ln K = 103.83`, `log₁₀K = 45.093`. *Check:*
`equilibrium_constant_CO_oxidation(298)` → `dG0≈−257,253`, `log10K≈45.093`.

### P2.  Inverse reaction & Table A-27  *(Moran 8e Eq. 14.34, p.890)*
Table A-27 lists `log₁₀K*` for the dissociation `CO₂ → CO + ½O₂`. At 2000 K the formation
reaction gives `log₁₀K = 2.885`. What does Table A-27 list?
*Answer:* `log₁₀K* = −log₁₀K = −2.885` (book −2.884). *Check:*
`log10K_inverse(equilibrium_constant_CO_oxidation(2000)["log10K"])` ≈ −2.885.

### P3.  Effect of pressure on dissociation  *(Moran 8e Ex 14.2, Eq. 14.35, p.892)*
1 kmol CO + ½ kmol O₂ reaches equilibrium (CO₂, CO, O₂) at 2500 K (`K = 0.0363` for
`CO₂ ⇌ CO + ½O₂`). Find the kmol of CO present, `z`, at (a) 1 atm, (b) 10 atm.
*Answer:* (a) `z = 0.129`; (b) `z = 0.062` — raising `p` (with `Δν > 0`) suppresses
dissociation. *Check:* `dissociation_extent_CO2(0.0363, 1.0)` ≈ 0.129;
`dissociation_extent_CO2(0.0363, 10.0)` ≈ 0.062.

### P4.  Effect of an inert component  *(Moran 8e Ex 14.4, Eq. 14.35, p.894)*
Repeat P3(a) but with the theoretical amount of air, so 1.88 kmol inert N₂ accompanies the
½ O₂. Find `z`.
*Answer:* `z = 0.175` — the inert N₂ acts like a pressure reduction (it lowers partial
pressures), *increasing* dissociation. *Check:*
`dissociation_extent_CO2(0.0363, 1.0, n_inert=1.88)` ≈ 0.175.

### P5.  Electron quantum concentration  *(~PK, NOT Moran; Reif / Rybicki & Lightman 9.5)*
Find the electron thermal de Broglie wavelength and quantum concentration at 300 K.
*Answer:* `λ = h/√(2πm_e k_BT) = 4.30 nm`; `n_Q = 1/λ³ ≈ 1.26×10²⁵ m⁻³`. *Check:*
`thermal_debroglie_wavelength(300)*1e9` ≈ 4.30; `quantum_concentration(300)` ≈ 1.255e25.
*(This is the electron-translation factor that distinguishes Saha from Moran's K.)*

### P6.  Thermal ionization of hydrogen (Saha)  *(~PK, NOT Moran; Chen; Carroll & Ostlie 8.1)*
For hydrogen (`χ = 13.6 eV`, `g_II/g_I = ½`) at number density `n = 10²³ m⁻³`, estimate the
ionization fraction `x` at 6000 K, 10,000 K, 20,000 K.
*Answer (illustrative, no book key):* `x ≈ 2×10⁻⁴`, `0.056`, `0.96` — ionization sets in
near 10⁴ K even though `χ/k_B = 1.58×10⁵ K`, because the quantum-concentration phase-space
factor dominates. *Check:* `saha_ionization_fraction(10000, 1e23, 13.6)` ≈ 0.056;
monotone in `T` (and `x` falls if `n` rises, by recombination). **Flagged ~PK — beyond
Moran 8e; physical-consistency checks only.**
