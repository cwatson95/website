# NE-22 — Nuclear power reactors: PWR/BWR steam cycles, Gen III & IV designs

Twenty-second module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), opening Chapter 11. Covers **§§11.1–11.6** (printed
pp. 370–429) of Shultis & Faw, 3rd ed.: nuclear electric power, conversion
efficiency, coolant limitations, Generation II PWRs and BWRs, Generation III and
IV designs, and small modular reactors.

- **Prerequisites:** `~NE-19`/`~NE-21` (core physics, peaking), `~NE-20`
  (control and feedback), `~Thermo-08`/`~Thermo-09` (the Rankine cycle).
- **Cross-links:** `~NE-23` (enrichment, burnup, the back end), `~NE-18` (the
  dose limits that shape the plant).

## Scope
The machine around the core, and it is mostly a steam plant. Water's critical
temperature of 374 °C caps the core outlet near 340 °C, which caps the steam at
284 °C, which caps the efficiency at ~34% — so a 1000 MW(e) plant must make
2940 MW(t) and throw 1940 MW away. From that one number follow the wet-steam
turbines, the size of the condenser, the difference between a PWR and a BWR, and
the entire Generation IV programme, which is in one sense an attempt to escape
374 °C using gas, sodium, lead or salt.

## Operations — `code/power_reactors.py`

| call | meaning | reference |
|------|---------|-----------|
| `carnot_efficiency(T_in, T_out)` | (T_in−T_out)/T_in, in °C in | Eq. (11.1) |
| `thermal_efficiency(MWe, MWt)`, `second_law_ratio(...)` | η, and η/η_Carnot; **refuses > 1** | §11.1.2 |
| `waste_heat(MWe, η)` | what the cooling tower must reject | §11.1.2 |
| `coolant_is_liquid(T)` | the 374 °C ceiling | §11.1.4 |
| `core_volume`, `power_density`, `specific_power` | the geometry checks | Tables 11.2–11.3 |
| `linear_heat_rate`, `surface_heat_flux` | kW/m and MW/m² at the clad | Tables 11.2–11.3 |
| `peaking_factor(max, avg)` | 2.50 (PWR), 2.20 (BWR) vs `~NE-21`'s 3.64 | Tables 11.2–11.3 |
| `assembly_width(lattice, pitch)`, `cycle_length_days(...)` | lattice and refuelling | Tables 11.2–11.3 |
| `PWR`, `BWR` | Tables 11.2 and 11.3 in full | Tables 11.2–11.3 |
| `GEN_III_BWR`, `GEN_III_PWR` | BWR/6–ABWR–ESBWR; AP1000 vs EPR | Tables 11.4–11.5 |
| `GEN_IV_SYSTEMS`, `SMALL_REACTORS`, `NUCLEAR_SHARE_2013` | the six GIF systems; SMRs; Table 11.1 | §11.5–11.6 |

## Use
```python
from power_reactors import (PWR, BWR, carnot_efficiency, thermal_efficiency,
                            second_law_ratio, waste_heat, power_density,
                            specific_power, peaking_factor, cycle_length_days,
                            GEN_IV_SYSTEMS)

carnot_efficiency(284.0, 33.0)            # 0.451 -- the PWR's ceiling
PWR["efficiency"] / carnot_efficiency(284.0, 33.0)   # 0.754 of Carnot
waste_heat(1000.0, 0.34)                  # 1941 MW thrown away

# Table 11.2 reproduces its own derived quantities
power_density(3800.0, 4.17, 3.37)         # 102.2  (printed 102)
specific_power(3800.0, 115e3)             # 33.0   (printed 33)
# Table 11.3 does not
specific_power(3830.0, 168e3)             # 22.8   (printed 25.9) -- 14% apart

peaking_factor(1.46, 0.584)               # 2.50 vs ~NE-21's bare-core 3.64
cycle_length_days(33.0, 115e3, 3800.0)    # 999 full-power days

second_law_ratio(3800.0, 3800.0, 284.0, 33.0)   # raises: that is a second-law
                                                #   violation, not a good design
```

## Run
```bash
cd code
python3 power_reactors.py        # demo: the ceiling, the table cross-checks, PWR vs BWR, Gen III/IV
python3 test_power_reactors.py   # tests  ->  "All 13 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the 374 °C ceiling and its three consequences → PWR against BWR as
  one decision → the tables checking themselves → peaking and what flattening is
  worth → Generation III as subtraction → Generation IV and SMRs, with a "Where
  this goes" map and a note on the module's finding.
- `code/power_reactors.py`, `code/test_power_reactors.py` (stdlib only). The
  chapter's content is its tables, so the module is curated data plus the
  arithmetic that checks it: Table 11.2 passes five independent relations,
  Table 11.3 fails one. `second_law_ratio` **refuses** an efficiency above
  Carnot — the realistic way to trip it is not optimism but quoting MW(t) where
  MW(e) belongs, which passes every other plausibility check.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — the efficiency ceiling and the heat thrown away, PWR against BWR
  normalised pairwise, the Generation III component count beside its unchanged
  thermodynamics, and Generation IV against a Carnot line beside the peaking-factor
  gap.
- `refs.md` — page-verified citations; the Table 11.3 inconsistency; and the
  §11.1.2 vs §11.1.4 tension over "about 40%".
