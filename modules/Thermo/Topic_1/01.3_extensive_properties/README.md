# 1.3 — Extensive Properties

Topic 1 (*Foundations*) module; see `modules/Thermo/list.txt`.

- **Pairs with:** `1.4` intensive properties (the other half of the classification).
- **Feeds into:** every balance that sums a property over a system — `1.1`/`1.2`
  energy balances, `4` enthalpy/entropy.

## Scope
A property is **extensive** if it depends on the size of the system and is
**additive over subsystems**: split a system and the property is the sum of the
parts. Mass `m`, volume `V`, energy `E` (and `U`, `KE`, `PE`), enthalpy `H`,
entropy `S` are extensive. Operationally: `X_total = Σ Xᵢ`, and `X(k·system) =
k·X(system)`.

## Operations — `code/extensive.py`

| call | meaning |
|------|---------|
| `total(values)` | `Σ Xᵢ` — extensive properties add over subsystems |
| `is_additive(parts, whole)` | test for extensivity |
| `scales_with_extent(X_unit, k)` | `k` copies have `k·X` |
| `volume(m, v)` / `internal_energy(m, u)` / `kinetic_energy(m, V)` | `X = m·x` forms |

## Run
```bash
cd code && python3 extensive.py        # demo: additivity & scaling
python3 test_extensive.py              # "All 7 tests passed."
```

## Files
`notes.md` (definitions + cites), `code/extensive.py`, `code/test_extensive.py`,
`problems/problems.md`, `refs.md`.
