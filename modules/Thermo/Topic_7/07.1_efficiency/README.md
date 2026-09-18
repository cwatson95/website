# 07.1 — Efficiency

The single module of **Topic 7 (Performance Metrics)** — every "how good is it?"
number in one place.

- **Builds on:** `2.x` (cycle energy balance `W_cycle = Q_in − Q_out`), `3.3`
  (second law → Carnot ceilings), Topic 6 (reversible/adiabatic → *isentropic*).
- **Feeds into:** every cycle's rating (Topic 9: Otto/Diesel/Brayton/Rankine) and
  every device's rating (Topic 8: turbines, compressors, pumps, heat pumps).

## Scope
Three families of metric — *desired output / required input* in every case — plus the
ceilings the second law imposes (`code/efficiency.py`):

| family | metric | relation | function |
|--------|--------|----------|----------|
| power cycle | thermal efficiency | `η = W_cycle/Q_in = 1 − Q_out/Q_in` | `thermal_efficiency`, `…_from_heat` |
| refrigeration | COP (refrig.) | `β = Q_C/W_cycle` | `cop_refrigerator` |
| heat pump | COP (heat pump) | `γ = Q_H/W_cycle` (`γ = β + 1`) | `cop_heat_pump` |
| **ceiling** | Carnot efficiency | `η_max = 1 − T_C/T_H` | `carnot_efficiency` |
| **ceiling** | max COPs | `β_max = T_C/(T_H−T_C)`, `γ_max = T_H/(T_H−T_C)` | `carnot_cop_*` |
| device | isentropic turbine | `η_t = (h1−h2)/(h1−h2s)` | `isentropic_turbine_efficiency` |
| device | isentropic nozzle | `η_n = (V₂²/2)/(V₂²/2)_s` | `isentropic_nozzle_efficiency` |
| device | isentropic compressor/pump | `η_c = (h2s−h1)/(h2−h1)` | `isentropic_compressor_efficiency` |

**Cycle Q's and W are positive magnitudes** (Moran's cycle convention, §2.6.1).
**Carnot `T` is absolute (K or °R).** Each *isentropic* η compares the real device with
the reversible-adiabatic one at the **same inlet state and same exit pressure**.

This module *cross-references* the Carnot ceilings (module `3.3`) and the isentropic
ideal (Topic 6) rather than re-deriving them.

## Run
```bash
cd code && python3 efficiency.py      # thermal η, COPs, Carnot ceilings, isentropic η
python3 test_efficiency.py            # "All 24 tests passed."
```

## Files
`notes.md`, `code/efficiency.py`, `code/test_efficiency.py`, `problems/problems.md`, `refs.md`.
