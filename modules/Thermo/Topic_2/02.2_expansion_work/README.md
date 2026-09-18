# 2.2 — Expansion Work

Topic 2 (*Energy & Work*) module; see `modules/Thermo/list.txt`.

The positive branch of moving-boundary work: when a system **expands** (`V₂>V₁`),
`W = ∫p dV > 0` — the system does work on its surroundings (e.g. an engine's power
stroke). The `∫p dV` machinery and its path-dependence are in `1.2`/`1.5`; the
work modes overview is `2.1`. This module is the expansion view.

| call | meaning |
|------|---------|
| `expansion_work(p_of_V, V1, V2)` | `∫p dV` (requires `V2>V1`), > 0 |
| `constant_pressure_expansion(p, V1, V2)` | `p(V₂−V₁)` |
| `isothermal_expansion(p1, V1, V2)` | `p₁V₁ ln(V₂/V₁)` |

```bash
cd code && python3 expansion_work.py
python3 test_expansion_work.py        # "All 5 tests passed."
```

Files: `notes.md`, `code/expansion_work.py`, `code/test_expansion_work.py`,
`problems/problems.md`, `refs.md`.
