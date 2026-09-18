# 11.EP — Example Problems (Topic 11)

Support module for **Topic 11 (Psychrometrics — Moist Air)**: Moran 8e Chapter-12 worked
**Examples 12.7, 12.8, 12.11, 12.12**, transcribed and **code-verified**. Holds its own
code because the psychrometric examples are specific to Topic 11.

## What it does
- `examples.md` — index of the examples (given → find → book answer → function).
- `code/examples.py` — each example solved from its given data via Eqs. 12.43–12.52.
- `code/test_examples.py` — regenerates each published answer and checks it (21 checks).

## Scope
Cooling moist air at **constant pressure** (dew point, condensate — Ex. 12.7) and at
**constant volume** (delayed onset of condensation — Ex. 12.8); and two steady-flow
air-conditioning devices: a **dehumidifier** (refrigeration load in tons — Ex. 12.11) and
a **steam-spray humidifier** (exit state on the chart — Ex. 12.12). Together they
exercise the humidity ratio (12.43), relative humidity (12.44), mixture enthalpy
(12.46), the water mass balance (12.52), and the air-conditioning energy balance (12.55).

## Run
```bash
cd code
python3 examples.py
python3 test_examples.py     # -> "All 21 tests passed."
```

## Files
`examples.md`, `code/examples.py`, `code/test_examples.py`, `refs.md`.
