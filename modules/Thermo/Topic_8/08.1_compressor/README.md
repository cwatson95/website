# 08.1 — Compressor

Opening module of **Topic 8 (Components & Devices)**.

- **Builds on:** the steady-state control-volume mass and energy rate balances
  (Topic 3 / Moran §4), enthalpy and property data (Topic 4), and isentropic
  processes / entropy (Topics 5–7).
- **Feeds into:** `08.2` (condenser that receives the hot compressed vapor),
  `08.4` (vapor-compression heat pump — the compressor is its work-input core), and the
  cycle modules of Topic 9.

## Scope
A **compressor** raises a gas's pressure by work input. The toolkit (`code/compressor.py`):

| use | relation | function |
|-----|----------|----------|
| mass flow rate | `ṁ = A·V/v` (Eq. 4.4b) | `mass_flow_rate` |
| ideal-gas mass flow | `ṁ = A·V·p/(R·T)` | `mass_flow_rate_ideal_gas` |
| CV power (signed) | `Ẇcv = Q̇cv + ṁ[(h1−h2)+(V1²−V2²)/2+g(z1−z2)]` | `power_cv` |
| power **input** | `−Ẇcv` | `power_input` |
| actual / isentropic work | `h2−h1` / `h2s−h1` | `actual_compressor_work`, `isentropic_compressor_work` |
| isentropic efficiency | `η_c = (h2s−h1)/(h2−h1)` (Eq. 6.48) | `isentropic_efficiency` |
| exit state from η_c | `h2 = h1 + (h2s−h1)/η_c` | `exit_enthalpy_from_efficiency` |

**Key idea:** `Ẇcv < 0` for a compressor (work is done *on* the gas); the minimum work
for a given pressure rise is the isentropic one, and `η_c` measures how close a real
machine gets.

**Units note:** `power_cv`/`power_input` use **strict SI** (`h` in J/kg, `V` in m/s,
result in W) so the enthalpy and kinetic-energy terms are consistent; the work/efficiency
helpers take enthalpy *differences*, so kJ/kg is fine there.

## Run
```bash
cd code && python3 compressor.py     # Ex 4.5 air compressor + Ex 6.14 R-22 η_c
python3 test_compressor.py           # "All 13 tests passed."
```

## Files
`notes.md`, `code/compressor.py`, `code/test_compressor.py`, `problems/problems.md`, `refs.md`.
