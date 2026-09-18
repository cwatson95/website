# 3.1 — Zeroth Law & Temperature

First module of **Topic 3 (The Laws)**; see `modules/Thermo/list.txt`.

- **Builds on:** Topic 1 (systems & properties) — temperature is the property
  that makes a system's state measurable.
- **Feeds into:** the **absolute** `T` used by `3.2` (1st law), `3.3` (2nd law /
  Carnot), `3.4` (3rd law), and all property data (Topic 5).

## Scope
The **zeroth law**: if two bodies are each in thermal equilibrium with a third,
they are in equilibrium with each other (Moran §1.7, p.19). That transitivity is
what makes *temperature* a consistent property — and what makes a thermometer
(the reusable "third body") meaningful. This module is the **temperature-scale
toolkit**:

| from → to | relation | `code/temperature.py` |
|-----------|----------|------------------------|
| K → °R | `T_R = 1.8 T_K` | `rankine_from_kelvin` |
| K ↔ °C | `T_C = T_K − 273.15` | `celsius_from_kelvin` / `kelvin_from_celsius` |
| °R → °F | `T_F = T_R − 459.67` | `fahrenheit_from_rankine` |
| °C ↔ °F | `T_F = 1.8 T_C + 32` | `fahrenheit_from_celsius` / `celsius_from_fahrenheit` |

Kelvin and Rankine are **absolute** (zero at absolute zero); Celsius and
Fahrenheit are shifted. **In every thermodynamic law, `T` must be absolute** —
a ratio like `T_C/T_H` (Carnot, `3.3`) is meaningless on °C/°F.

## Run
```bash
cd code && python3 temperature.py     # fixed points + conversions + zeroth-law demo
python3 test_temperature.py           # "All 18 tests passed."
```

## Files
`notes.md`, `code/temperature.py`, `code/test_temperature.py`, `problems/problems.md`, `refs.md`.
