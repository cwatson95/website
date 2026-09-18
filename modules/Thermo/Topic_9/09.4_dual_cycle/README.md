# 09.4 — Air-Standard Dual Cycle

Fourth module of **Topic 9** — the dual (mixed) combustion idealization that *brackets* Otto
and Diesel.

- **Builds on:** `09.2` (Otto — the `r_c → 1` limit) and `09.3` (Diesel — the `r_p → 1` limit);
  shares the isentropic compression/expansion.
- **Ceiling:** `09.1` (Carnot).

## Scope
Isentropic compression, **two-stage** heat addition — constant **volume** (pressure ratio
`r_p = p₃/p₂`) then constant **pressure** (cutoff ratio `r_c = V₄/V₃`) — isentropic expansion,
constant-volume rejection (Moran §9.4). Approximates real IC-engine p–V diagrams better than
either bracketing cycle.

| quantity | relation | function |
|----------|----------|----------|
| efficiency (air-table) | `η = 1 − (u₅−u₁)/[(u₃−u₂)+(h₄−h₃)]` (Eq. 9.14) | `dual_efficiency_air_table` |
| efficiency (cold air-standard) | `η = 1 − (1/r^(k−1))·(r_p r_c^k − 1)/((r_p−1)+k r_p(r_c−1))` | `dual_efficiency` |
| pressure ratio | `r_p = p₃/p₂ = T₃/T₂` | `pressure_ratio` |
| cutoff ratio | `r_c = V₄/V₃ = T₄/T₃` | `cutoff_ratio` |
| state temperatures | `T₂=T₁r^(k−1)`, `T₃=r_pT₂`, `T₄=r_cT₃`, `T₅=T₄(r_c/r)^(k−1)` | `temp_after_*` |
| mean effective pressure | `mep = w_net/[v₁(1−1/r)]` | `mean_effective_pressure` |

The closed form **reduces to** Otto (`r_c → 1`, Eq. 9.8) and Diesel (`r_p → 1`, Eq. 9.13).
`k = 1.4` for air.

## Run
```bash
cd code && python3 dual_cycle.py     # Example 9.3 (η = 0.635 air-table), Otto/Diesel limits
python3 test_dual_cycle.py           # "All 14 tests passed."
```

## Files
`notes.md`, `code/dual_cycle.py`, `code/test_dual_cycle.py`, `problems/problems.md`, `refs.md`.
