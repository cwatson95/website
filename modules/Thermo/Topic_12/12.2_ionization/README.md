# 12.2 — Dissociation, Equilibrium Constant & Ionization

Module 2 of **Topic 12 (Combustion & Reacting Mixtures)** — the high-temperature limit of
`12.1`. **Cross-trunk module:** the dissociation half is Moran 8e **Chapter 14**; the
ionization half (the **Saha equation**) is a **plasma-physics extension beyond Moran**.

> **Cross-trunk note (~PK).** Part (A) — the equilibrium constant `K(T)` and molecular
> dissociation — is straight Moran §14.2–14.3. Part (B) — thermal **ionization** via the
> **Saha equation** — is **NOT in Moran 8e**; it is a standard statistical-mechanics /
> plasma result (Saha 1920), cited to Chen, Rybicki & Lightman, Carroll & Ostlie, Reif.
> All Saha functions are tagged `[~PK, NOT Moran]`.

- **Builds on:** `12.1` (combustion enthalpies, `h = h°_f + Δh`); ideal-gas mixtures.
- **Feeds into:** the dissociation correction to the adiabatic flame temperature; plasma
  kinetics (the `~PK` ionization leaf).

## Scope
| use | relation | `code/ionization.py` | trunk |
|-----|----------|----------------------|-------|
| equilibrium constant | `K = Πy_i^{ν_i}(p/p_ref)^{Δν}` | `equilibrium_constant_from_composition` | Moran 14.32 |
| K from thermo data | `ln K = −ΔG°/(R̄T)`, `ΔG° = Σν(h̄−Ts°)` | `gibbs_of_reaction`, `K_from_gibbs`, `log10K_from_gibbs` | Moran 14.29b/14.31 |
| inverse reaction | `log₁₀K* = −log₁₀K` | `log10K_inverse` | Moran 14.34 |
| Ex 14.1 reproduction | CO + ½O₂ ⇌ CO₂ | `equilibrium_constant_CO_oxidation` | Moran Ex 14.1 |
| dissociation extent | `K = z/(1−z)·[z/(2+2a+z)]^½(p/p_ref)^½` | `dissociation_extent_CO2` | Moran Ex 14.2/14.4 |
| **Saha ionization** | `n_{i+1}n_e/n_i = 2(g'/g)n_Q e^{−χ/k_BT}` | `saha_rhs`, `saha_ionization_fraction` | **~PK, NOT Moran** |
| quantum concentration | `n_Q = (2πm_e k_BT/h²)^{3/2} = 1/λ³` | `quantum_concentration`, `thermal_debroglie_wavelength` | **~PK, NOT Moran** |

**Key idea:** dissociation and ionization are both `ΔG° = −R̄T ln K`. The difference is
that ionization frees an electron, whose *translational* partition function (`n_Q`) is the
extra factor in Saha — which is exactly why the cross-trunk flag is needed: Moran's K
machinery covers chemistry, not the electron phase space.

## Run
```bash
cd code && python3 ionization.py     # Ex 14.1/14.2 (Moran) + Saha demo (flagged ~PK)
python3 test_ionization.py           # "All 27 tests passed."
```

## Files
`notes.md`, `code/ionization.py`, `code/test_ionization.py`, `problems/problems.md`, `refs.md`.
