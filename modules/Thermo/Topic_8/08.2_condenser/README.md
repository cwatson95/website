# 08.2 — Condenser

Module 2 of **Topic 8 (Components & Devices)**.

- **Builds on:** the steady control-volume energy balance and property data
  (`08.1`, Topics 3–4); two-phase quality (Topic 4).
- **Feeds into:** `08.3` (the condenser seen as a *two-stream* heat exchanger),
  `08.4` (the heat rejected here is the heat-pump output `Q_H`), and Topic 9 cycles.

## Scope
A **condenser** rejects heat from a working fluid, condensing vapor to liquid. Toolkit
(`code/condenser.py`):

| use | relation | function |
|-----|----------|----------|
| single-stream heat rate (signed) | `Q̇cv = ṁ(h_out−h_in)` (< 0) | `heat_transfer_rate` |
| heat **rejected** (magnitude) | `ṁ(h_in−h_out)` | `heat_rejected` |
| cycle condenser, per mass | `Q̇out/ṁ = h2−h3` (Eq. 10.5) | `condenser_heat_per_mass` |
| two-phase enthalpy | `h = hf + x(hg−hf)` | `enthalpy_two_phase` |
| quality from enthalpy | `x = (h−hf)/(hg−hf)` | `quality_from_h` |

**Key idea:** with `Ẇcv = 0` and negligible ΔKE/ΔPE, the working-fluid-side balance is
just `Q̇cv = ṁΔh`, and for a condenser `Q̇cv < 0` (heat out).

## Run
```bash
cd code && python3 condenser.py     # Ex 4.7 steam condenser + Ex 10.4 heat-pump condenser
python3 test_condenser.py           # "All 11 tests passed."
```

## Files
`notes.md`, `code/condenser.py`, `code/test_condenser.py`, `problems/problems.md`, `refs.md`.
