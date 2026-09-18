# 12.1 — Fuels & Combustion of Reacting Mixtures

Opening module of **Topic 12 (Combustion & Reacting Mixtures)** — Moran 8e **Chapter 13**.

- **Builds on:** ideal-gas mixtures and partial pressures (Topic 11 / Moran Ch.12);
  enthalpy and steady-flow energy balances (Topics 3–4).
- **Feeds into:** `12.2` (high-T dissociation & ionization), `12.EP` (worked Examples
  13.1–13.8 incl. adiabatic flame temperature), `12.EQ`, `12.HP`.

## Scope
Complete combustion of hydrocarbon fuels with air, and the first-law accounting that
goes with it:

| use | relation | `code/fuels.py` |
|-----|----------|-----------------|
| theoretical O₂ / air | `a_O₂ = C + H/4 + S − O/2`, `AF̄ = 4.76 a_O₂` | `theoretical_O2`, `theoretical_air_molar` |
| air–fuel ratio (mass↔molar) | `AF = AF̄ (M_air/M_fuel)` | `afr_molar_to_mass`, `afr_mass_to_molar` |
| % theoretical / excess air, φ | `AF/AF_theo`, `AF_theo/AF` | `percent_theoretical_air`, `percent_excess_air`, `equivalence_ratio` |
| products & dew point | `p_v = y_v p`; `n = p_sat n_dry/(p − p_sat)` | `dew_point_partial_pressure`, `vapor_remaining_on_cooling` |
| enthalpy / heating value | `h = h°_f + Δh`; `h_RP = ΣP nh − ΣR nh`; HHV/LHV `= |h_RP|` | `enthalpy`, `enthalpy_of_combustion`, `heating_value_mass` |
| energy balance | `(Q̇−Ẇ)/ṅ_F = h̄_P − h̄_R` | `energy_balance_per_mole_fuel` |

**Key idea:** balance the reaction by **conservation of each element** (air = 4.76 mol per
mol O₂, N₂ inert), then the AFR, products, dew point, and the first-law energy balance all
follow. Enthalpies for reacting systems use the **enthalpy of formation** datum so that
species which appear/disappear are handled consistently.

## Run
```bash
cd code && python3 fuels.py          # Examples 13.1, 13.2, 13.7 reproduced from given data
python3 test_fuels.py                # "All 29 tests passed."
```

## Files
`notes.md`, `code/fuels.py`, `code/test_fuels.py`, `problems/problems.md`, `refs.md`.
