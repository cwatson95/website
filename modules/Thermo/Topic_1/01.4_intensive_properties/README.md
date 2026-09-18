# 1.4 — Intensive Properties

Topic 1 (*Foundations*) module; see `modules/Thermo/list.txt`.

- **Pairs with:** `1.3` extensive properties.
- **Feeds into:** `5` property tables (which tabulate intensive `v, u, h, s`);
  the state principle / `p–v–T` work in later topics.

## Scope
A property is **intensive** if it is independent of system size and may vary from
point to point: temperature `T`, pressure `p`, density `ρ`, and every **specific**
(per-unit-mass) property — specific volume `v = V/m`, specific internal energy
`u = U/m`, etc. Two facts:
- a specific property is an extensive one per unit mass: `v = V/m = 1/ρ`;
- intensive properties **mass-average** over subsystems, they don't add:
  `v_mix = Σ(mᵢ vᵢ)/Σmᵢ = V_total/m_total` (contrast `1.3`).

## Operations — `code/intensive.py`

| call | meaning |
|------|---------|
| `specific(X, m)` / `molar(X, n)` | `X/m` (e.g. `v=V/m`) / `X/n` |
| `density(m, V)` / `specific_volume(V, m)` | `ρ = m/V` / `v = V/m = 1/ρ` |
| `mass_average(values, masses)` | how intensive properties combine |
| `is_size_independent(x1, x2)` | intensive ⇒ unchanged under scaling |

## Run
```bash
cd code && python3 intensive.py        # demo: v, ρ, mass-averaging
python3 test_intensive.py              # "All 8 tests passed."
```

## Files
`notes.md` (definitions + cites), `code/intensive.py`, `code/test_intensive.py`,
`problems/problems.md`, `refs.md`.
