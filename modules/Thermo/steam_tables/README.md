# Steam Tables (SI) — Water Properties

Property tables for **water (H₂O)** transcribed from the appendix of
**Moran, Shapiro, Boettner & Bailey — *Fundamentals of Engineering Thermodynamics*, 8th Edition**
(Tables A‑2 … A‑6, "Tables in SI Units"). Companion to
[`../Thermodynamics_Conversion_Factors_and_Constants.md`](../Thermodynamics_Conversion_Factors_and_Constants.md).

The numbers here are reference data — they were pulled **programmatically** from the
PDF (not hand‑typed) and cross‑validated, so they can be trusted as the canonical
source for property lookups and cycle calculations in the Thermo modules.

---

## Files

| File | Table | What it is | Book pp. |
|------|-------|------------|---------|
| `A2_sat_water_temperature.csv` | A‑2 | Saturated water (liquid–vapor), **temperature** entry | 927–928 |
| `A3_sat_water_pressure.csv`    | A‑3 | Saturated water (liquid–vapor), **pressure** entry | 929–930 |
| `A4_superheated_water.csv`     | A‑4 | **Superheated** water vapor | 931–934 |
| `A5_compressed_liquid_water.csv` | A‑5 | **Compressed** (subcooled) liquid water | 935 |
| `A6_sat_water_solid_vapor.csv` | A‑6 | Saturated water (**solid–vapor**), sublimation | 936 |
| `steam_tables.md` | — | Human‑readable rendering of all five tables | — |
| `_extract.py` | — | Reproducible extractor + self‑validation (run from `modules/Thermo/`) | — |

The CSVs are the canonical data; `steam_tables.md` is a rendering for reading.

---

## Symbols, units, and conventions

| Symbol | Quantity | Unit |
|--------|----------|------|
| `T` | temperature | °C |
| `P` | pressure | bar (A‑2…A‑5); **kPa** (A‑6) |
| `v` | specific volume | m³/kg |
| `u` | specific internal energy | kJ/kg |
| `h` | specific enthalpy | kJ/kg |
| `s` | specific entropy | kJ/kg·K |

**Subscripts** — `f` = saturated liquid, `g` = saturated vapor,
`fg` = vapor − liquid (evaporation), `i` = saturated solid / ice,
`ig` = sublimation (vapor − solid).

**The `×10³` columns.** Liquid/solid specific volumes are tabulated scaled by 10³
(column names end in `_x1e3_m3kg`): the true value is **table ÷ 1000**. E.g. in A‑2
`vf_x1e3_m3kg = 1.0002` → `vf = 1.0002 × 10⁻³ m³/kg`. Vapor volumes (`vg`) are direct.
This affects `vf` (A‑2/A‑3), the whole `v` column of A‑5, and `vi` (A‑6) — but **not**
A‑4 (superheated `v` is direct m³/kg).

**Reference state.** `u_f` and `s_f` are set to zero for saturated liquid at the
triple point (0.01 °C); hence `A‑6` solid/ice energies and entropies are **negative**
(they lie below the liquid reference). Cross‑check: `hg` and `ug` at 0.01 °C agree
between A‑2 and A‑6 (2501.4 and 2375.3 kJ/kg).

**The `sat` column (A‑4, A‑5).** `sat = 1` marks the saturation reference row of a
pressure block — saturated **vapor** in A‑4, saturated **liquid** in A‑5 — for which
`T_C = Tsat_C`. All other rows are `sat = 0`.

**Supercritical blocks.** Above the critical pressure (p_c = 220.9 bar, T_c = 374.14 °C)
there is no saturation state: blocks at 240/280/320 bar (A‑4) and 250/300 bar (A‑5)
have a blank `Tsat_C` and no `sat = 1` row.

---

## Coverage

- **A‑2**: 70 temperatures, 0.01 °C → 374.14 °C (critical point).
- **A‑3**: 50 pressures, 0.04 bar → 220.9 bar (critical point).
- **A‑4**: 24 pressure blocks, 0.06 → 320 bar; T up to 900 °C (278 rows).
- **A‑5**: 8 pressure blocks, 25 → 300 bar (66 rows).
- **A‑6**: 22 temperatures, 0.01 °C → −40 °C.

---

## How it was extracted & validated

`_extract.py` clusters the PDF text layer into rows by word coordinates
(PyMuPDF). A‑2…A‑5 parse directly; A‑6 is printed **rotated 90°** so its text layer
is scrambled — it was read from a high‑DPI render and embedded, then guarded by the
checks below. Re‑run any time with:

```bash
cd modules/Thermo
python3 steam_tables/_extract.py        # re-validates, then rewrites the CSVs + steam_tables.md
```

Nothing is written unless **all** checks pass:

- **Row counts & monotonicity** — T/P strictly ordered; endpoints land on the
  triple and critical points.
- **Anchor values** vs. independent references — e.g. sat 100 °C (P = 1.014 bar,
  h_fg = 2257.0, h_g = 2676.1, s_g = 7.3549); superheated 10 bar/200 °C
  (v 0.2060, u 2621.9, h 2827.9, s 6.6940) and 100 bar/400 °C (v 0.02641, …).
- **Cross‑table agreement** — every A‑4 saturated‑vapor row and A‑5 saturated‑liquid
  row matches the independent A‑3 saturation table at the same pressure (0 mismatches).
- **A‑6 internal consistency** — `u_ig = u_g − u_i`, `h_ig = h_g − h_i`,
  `s_ig = s_g − s_i`, `h_i ≈ u_i`; and every A‑6 value matches an exact token on the
  source page.

---

## Quick use

```python
import pandas as pd
A2 = pd.read_csv("steam_tables/A2_sat_water_temperature.csv")
hg_100 = A2.loc[A2.T_C == 100, "hg_kJkg"].item()      # 2676.1 kJ/kg

A4 = pd.read_csv("steam_tables/A4_superheated_water.csv")
block = A4[(A4.P_bar == 100) & (A4.sat == 0)]          # superheated rows at 100 bar
```

> Remember the `×10³` columns (`*_x1e3_m3kg`) — divide by 1000 for m³/kg.
