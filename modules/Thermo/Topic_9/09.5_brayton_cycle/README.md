# 09.5 — Air-Standard Brayton Cycle

Fifth module of **Topic 9** — the gas-turbine / jet-engine idealization; the first *steady-flow* cycle.

- **Builds on:** `09.1` (Carnot ceiling), `07.1` (efficiency, isentropic η_t/η_c), Topic 6 (isentropic relations).
- **Feeds into:** `09.6` (Rankine — the vapor counterpart with tiny bwr), `10.2` (Stirling/Ericsson share the regenerator, Eq. 9.27).

## Scope
Four internally reversible steady-flow processes of air: isentropic compression,
**constant-pressure** heat addition, isentropic expansion, constant-pressure rejection
(Moran §9.6). Efficiency depends only on the **compressor pressure ratio** `r_p = p₂/p₁`.

| quantity | relation | function |
|----------|----------|----------|
| turbine / compressor work | `Ẇ_t/ṁ = h₃−h₄`, `Ẇ_c/ṁ = h₂−h₁` (Eqs. 9.15–9.16) | `turbine_work`, `compressor_work` |
| heat added / rejected | `Q̇_in/ṁ = h₃−h₂`, `Q̇_out/ṁ = h₄−h₁` (Eqs. 9.17–9.18) | `heat_added`, `heat_rejected` |
| efficiency (air-table) | `η = [(h₃−h₄)−(h₂−h₁)]/(h₃−h₂)` (Eq. 9.19) | `brayton_efficiency_air_table` |
| back work ratio | `bwr = (h₂−h₁)/(h₃−h₄)` — **40–80%!** (Eq. 9.20) | `back_work_ratio` |
| efficiency (cold air-standard) | `η = 1 − 1/r_p^((k−1)/k)` (Eq. 9.25) | `brayton_efficiency` |
| state temperatures | `T₂ = T₁r_p^((k−1)/k)`, `T₄ = T₃(1/r_p)^((k−1)/k)` (Eqs. 9.23–9.24) | `temp_after_*` |
| max-net-work ratio | `r_p* = (T₃/T₁)^(k/2(k−1))` (Ex 9.5) | `pressure_ratio_max_work` |
| irreversibilities | `Ẇ_t = η_t·Ẇ_t,s`, `Ẇ_c = Ẇ_c,s/η_c` (§9.6.3) | `*_work_actual` |
| regeneration | `η_reg = (h_x−h₂)/(h₄−h₂)` (Eq. 9.27), `Q̇_in/ṁ = h₃−h_x` (9.26) | `regenerator_*` |

Efficiency rises with `r_p`; net work per unit mass peaks near `r_p ≈ 21` for 300/1700 K.
`k = 1.4` for air. Compressing *gas* costs a large slice of the turbine output.

## Run
```bash
cd code && python3 brayton_cycle.py     # Examples 9.4 (0.457/0.396), 9.6 (0.249), 9.7 (0.568)
python3 test_brayton_cycle.py           # "All 31 tests passed."
```

## Files
`notes.md`, `code/brayton_cycle.py`, `code/test_brayton_cycle.py`, `problems/problems.md`, `refs.md`.
