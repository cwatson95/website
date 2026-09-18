# 09.3 — Air-Standard Diesel Cycle

Third module of **Topic 9** — the compression-ignition engine idealization.

- **Builds on:** `09.2` (Otto — shares the isentropic compression), `09.1` (ceiling).
- **Feeds into:** the dual cycle (`09.4`), of which Diesel is the `r_p → 1` limit.

## Scope
Isentropic compression, **constant-pressure** heat addition (fuel injected into hot
air), isentropic expansion, constant-volume rejection (Moran §9.3). Efficiency depends
on the compression ratio `r` **and** the cutoff ratio `rc = V₃/V₂`.

| quantity | relation | function |
|----------|----------|----------|
| efficiency (cold air-standard) | `η = 1 − (1/r^(k−1))·(rc^k−1)/(k(rc−1))` (Eq. 9.13) | `diesel_efficiency` |
| efficiency (air-table) | `η = 1 − (u₄−u₁)/(h₃−h₂)` (Eq. 9.11) | `diesel_efficiency_air_table` |
| cutoff ratio | `rc = V₃/V₂ = T₃/T₂` | `cutoff_ratio` |
| state temperatures | `T₂=T₁r^(k−1)`, `T₃=rc·T₂`, `T₄=T₃(rc/r)^(k−1)` | `temp_after_*` |

For the **same `r`**, Diesel is *less* efficient than Otto (the bracket > 1 for `rc > 1`);
as `rc → 1` it reduces to Otto. Diesels recover with higher `r`. `k = 1.4` for air.

## Run
```bash
cd code && python3 diesel_cycle.py      # η(r,rc), Example 9.2 (0.578 air-table, 0.632 cold)
python3 test_diesel_cycle.py            # "All 10 tests passed."
```

## Files
`notes.md`, `code/diesel_cycle.py`, `code/test_diesel_cycle.py`, `problems/problems.md`, `refs.md`.
