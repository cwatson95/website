# 08.4 — Heat Pump / Refrigerator

Module 4 of **Topic 8 (Components & Devices)** — the **device & COP** view of a reversed
cycle. (The full state-by-state cycle analysis is Topic 9.)

- **Builds on:** the compressor (`08.1`), condenser (`08.2`), heat exchanger (`08.3`), the
  Carnot corollaries (Topic 6 / Moran §5.10–5.11), and two-phase property data (Topic 4).
- **Feeds into:** Topic 9 vapor-compression / Brayton refrigeration cycles.

## Scope
Rate a refrigerator / heat pump by its **coefficient of performance**. Toolkit
(`code/heat_pump.py`):

| use | relation | function |
|-----|----------|----------|
| cycle first law | `Q_H = Q_C + W_net` (Eq. 10.8) | `heat_rejected` |
| refrigerator COP | `β = Q_C/W_net` (Eq. 10.7) | `cop_refrigeration` |
| heat-pump COP | `γ = Q_H/W_net` (Eq. 10.10) | `cop_heat_pump` |
| Carnot refrigerator | `β_max = T_C/(T_H−T_C)` (Eq. 10.1) | `carnot_cop_refrigeration` |
| Carnot heat pump | `γ_max = T_H/(T_H−T_C)` (Eq. 10.9) | `carnot_cop_heat_pump` |
| VC refrigerator COP | `β = (h1−h4)/(h2−h1)` (Eq. 10.7) | `cop_ref_from_enthalpies` |
| VC heat-pump COP | `γ = (h2−h3)/(h2−h1)` (Eq. 10.10) | `cop_hp_from_enthalpies` |

**Key idea:** `γ = β + 1` (so a heat-pump COP is always ≥ 1), and both are capped by the
Carnot value `T_H/(T_H−T_C)`; the temperatures must be in **kelvin**.

**Distinct from Topic 9:** this module is the *device/COP* layer (ratios and limits);
Topic 9 fixes every state, draws the T–s/p–h diagrams, and applies isentropic efficiencies.

## Run
```bash
cd code && python3 heat_pump.py     # Ex 10.1 refrigerator (β=9.24) + Ex 10.4 heat pump (γ=4.65)
python3 test_heat_pump.py           # "All 16 tests passed."
```

## Files
`notes.md`, `code/heat_pump.py`, `code/test_heat_pump.py`, `problems/problems.md`, `refs.md`.
