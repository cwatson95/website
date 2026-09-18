# Constants (shared)

Cross-cutting, Thermo-level **constants** module (per `modules/Thermo/plan.txt`):
machine-readable like `steam_tables/`, consumed by the topic modules. Holds both
front-matter universal constants and a body table pulled from the text.

## Files
- `gas_constants.csv` — **Moran Table 3.1**, "Values of the gas constant R"
  (printed p.128 / PDF 145): each substance's specific gas constant `R`
  (kJ/kg·K and Btu/lb·°R) plus molecular weight `M`.
- `constants.csv` — universal/physical constants: universal gas constant
  `R̄ = 8.314 kJ/kmol·K` (§3.11.1, p.127), standard gravity, standard atmosphere,
  `g_c`, Avogadro number, Boltzmann constant, absolute zero.
- `code/constants.py` — loaders + helpers `gas_constant(name)`, `molar_mass(name)`,
  `constant(name, units)`, and `RBAR`.
- `code/test_constants.py` — verifies the tables.

## Self-verification
The defining relation `R = R̄ / M` (Moran Eq. 3.25) checks Table 3.1 against
itself: `R · M = R̄ = 8.314 kJ/kmol·K` for every substance (to table rounding).
The universal table is cross-checked too (`k_B = R̄/N_A`).

```bash
cd code
python3 constants.py          # print Table 3.1 with the R*M check
python3 test_constants.py     # -> "All 20 tests passed."
```

## Use
```python
import constants as C
C.gas_constant("Air")                       # 0.2870 kJ/kg-K
C.RBAR                                       # 8.314 kJ/kmol-K
C.constant("Standard atmosphere", "kPa")    # 101.325
```

## Notes
`R` and `M` values are Moran Table 3.1 / Table A-1; molecular weights use standard
atomic weights (≈ Table A-1). The front-matter conversion factors live alongside
in `../Thermodynamics_Conversion_Factors_and_Constants.md`.
