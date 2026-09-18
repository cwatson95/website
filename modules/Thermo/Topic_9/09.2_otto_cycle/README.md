# 09.2 — Air-Standard Otto Cycle

Second module of **Topic 9** — the spark-ignition (gasoline) engine idealization.

- **Builds on:** `09.1` (Carnot ceiling), `07.1` (thermal efficiency), Topic 6 (isentropic).
- **Feeds into:** Diesel (`09.3`) and dual (`09.4`), which share its isentropic legs.

## Scope
Four internally reversible processes of air: isentropic compression, **constant-volume**
heat addition (spark-ignited burn), isentropic expansion, constant-volume rejection
(Moran §9.2). Efficiency depends only on the compression ratio `r`.

| quantity | relation | function |
|----------|----------|----------|
| efficiency (cold air-standard) | `η = 1 − 1/r^(k−1)` (Eq. 9.8) | `otto_efficiency` |
| efficiency (air-table) | `η = 1 − (u₄−u₁)/(u₃−u₂)` (Eq. 9.3) | `otto_efficiency_air_table` |
| end of compression | `T₂ = T₁·r^(k−1)` (Eq. 9.6) | `temp_after_isentropic_compression` |
| end of expansion | `T₄ = T₃/r^(k−1)` (Eq. 9.7) | `temp_after_isentropic_expansion` |
| net work / mep | `w = η·q₂₃`, `mep = W/(V₁−V₂)` | `net_work_cold`, `mean_effective_pressure` |

`r = V₁/V₂` is the **compression ratio**; for air `k = c_p/c_v = 1.4`. Efficiency
rises with `r`. The cold-air closed form overpredicts vs the air-table method.

## Run
```bash
cd code && python3 otto_cycle.py        # η(r), Example 9.1 (0.565 cold, 0.51 air-table)
python3 test_otto_cycle.py              # "All 10 tests passed."
```

## Files
`notes.md`, `code/otto_cycle.py`, `code/test_otto_cycle.py`, `problems/problems.md`, `refs.md`.
