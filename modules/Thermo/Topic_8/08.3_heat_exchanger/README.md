# 08.3 — Heat Exchanger

Module 3 of **Topic 8 (Components & Devices)**.

- **Builds on:** the steady control-volume energy balance and property data
  (`08.1`, `08.2`, Topics 3–4); the single-stream condenser is the one-sided special case.
- **Feeds into:** `08.4` (the heat pump's evaporator and condenser are its two
  heat exchangers) and Topic 9 cycles (feedwater heaters, regenerators).

## Scope
A two-stream **heat exchanger**: energy balance over the whole device, and the mass-flow
ratio it fixes. Toolkit (`code/heat_exchanger.py`):

| use | relation | function |
|-----|----------|----------|
| whole-device balance residual | `Q̇cv−Ẇcv + ṁ_h(h_hi−h_ho) + ṁ_c(h_ci−h_co)` | `energy_balance_residual` |
| mass-flow ratio | `ṁ_c/ṁ_h = (h_hi−h_ho)/(h_co−h_ci)` | `mass_flow_ratio_cold_to_hot` |
| solve for the other flow | `ṁ₁Δh₁ = ṁ₂Δh₂` | `mass_flow_other` |
| per-stream duty | `Q̇ = ṁ(h_out−h_in)` | `heat_duty` |
| constant-cp Δh | `Δh = cp(T_out−T_in)` | `sensible_enthalpy_change` |
| two-phase enthalpy | `h = hf + x(hg−hf)` | `enthalpy_two_phase` |

**Key idea:** enclose *both* streams ⇒ `Ẇcv = 0` and the inter-stream transfer is internal;
if also externally adiabatic, hot-stream loss = cold-stream gain.

## Run
```bash
cd code && python3 heat_exchanger.py     # Ex 4.7 condenser as a two-stream exchanger
python3 test_heat_exchanger.py           # "All 10 tests passed."
```

## Files
`notes.md`, `code/heat_exchanger.py`, `code/test_heat_exchanger.py`, `problems/problems.md`, `refs.md`.
