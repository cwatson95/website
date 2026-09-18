# 09.6 — Rankine Cycle

Sixth module of **Topic 9** — the vapor power (steam) cycle behind most of the world's electricity.

- **Builds on:** `09.1` (Carnot ceiling), `09.5` (Brayton — the gas counterpart), `07.1`
  (η_t/η_p), Topic 5 (steam tables → `steam_tables/`).
- **Feeds into:** superheat/reheat plant design (§8.3), `8.x` component modules (turbine ↔ condenser ↔ pump ↔ boiler).

## Scope
Water circulates through four steady-flow components: turbine, condenser, pump, boiler
(Moran §8.2). The pump moves *liquid*, so the back work ratio collapses to ~1%.

| quantity | relation | function |
|----------|----------|----------|
| turbine work | `Ẇ_t/ṁ = h₁−h₂` (Eq. 8.1) | `turbine_work` |
| condenser heat | `Q̇_out/ṁ = h₂−h₃` (Eq. 8.2) | `condenser_heat` |
| pump work | `Ẇ_p/ṁ = h₄−h₃` (Eq. 8.3) | `pump_work` |
| boiler heat | `Q̇_in/ṁ = h₁−h₄` (Eq. 8.4) | `boiler_heat` |
| efficiency | `η = [(h₁−h₂)−(h₄−h₃)]/(h₁−h₄)` (Eq. 8.5a/b) | `rankine_efficiency*` |
| back work ratio | `bwr = (h₄−h₃)/(h₁−h₂)` — **~1–2%** (Eq. 8.6) | `back_work_ratio` |
| pump work approx. | `(Ẇ_p/ṁ)_s ≈ v₃(p₄−p₃)` (Eq. 8.7b) | `pump_work_approx` |
| pressure effects | `η_ideal = 1 − T̄_out/T̄_in` (Eq. 8.8) | `ideal_efficiency_avg_temps` |
| irreversibilities | `h₂ = h₁−η_t(h₁−h₂s)` (8.9), `Ẇ_p = Ẇ_p,s/η_p` (8.10b) | `turbine_exit_actual`, `pump_work_actual` |
| reheat | two-stage expansion, `x_exit ≥ 0.9` (§8.3) | `reheat_efficiency` |

Boiler pressure **up** / condenser pressure **down** ⇒ η up; superheat+reheat raise η
*and* keep turbine-exit quality above ~90%. States from Tables A-2/A-3/A-4 (the module
cross-checks Moran's quoted values against `../../steam_tables/*.csv`).

## Run
```bash
cd code && python3 rankine_cycle.py     # Examples 8.1 (0.371), 8.2 (0.314), 8.3 (0.403)
python3 test_rankine_cycle.py           # "All 49 tests passed."
```

## Files
`notes.md`, `code/rankine_cycle.py`, `code/test_rankine_cycle.py`, `problems/problems.md`, `refs.md`.
