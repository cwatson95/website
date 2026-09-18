# 4.2 — Entropy

Keystone module of **Topic 4 (Properties & State Functions)**.

- **Builds on:** `3.3` (second law / Clausius inequality), `4.1` (`h`, for the 2nd T dS eq).
- **Feeds into:** `4.3` (exergy: `Ed = T₀σ`), isentropic processes & efficiency (Topics 6, 7),
  every cycle (Topic 9). Mixture form `s = sf + x·sfg` ties to `4.4`.

## Scope
The path-independence of `∮(δQ/T)_rev` (Clausius inequality) makes **entropy** a
property, `dS = (δQ/T)_int,rev` (Moran Eq. 6.2). The toolkit:

| use | relation | `code/entropy.py` |
|-----|----------|--------------------|
| T dS equations | `T ds = du + p dv`; `T ds = dh − v dp` | `du_from_tds`, `dh_from_tds` |
| incompressible | `Δs = c·ln(T₂/T₁)` | `entropy_change_incompressible` |
| ideal gas (tables) | `Δs = s°(T₂)−s°(T₁) − R·ln(p₂/p₁)` | `entropy_change_ideal_gas_tables` |
| ideal gas (const cp/cv) | `cp·ln(T₂/T₁) − R·ln(p₂/p₁)` / `cv·ln + R·ln(v₂/v₁)` | `..._cp` / `..._cv` |
| two-phase | `s = sf + x·sfg` | `entropy_mixture` |
| reversible heat | `Q = ∫T dS` | `heat_isothermal_rev` |
| **entropy balance** | `S₂−S₁ = ∫δQ/T_b + σ`, `σ ≥ 0` | `entropy_production_closed`, `process_allowed` |

**Key idea:** `σ` (entropy produced by irreversibility) is **not a property** —
Moran Ex 6.1 (reversible) and Ex 6.2 (irreversible) have the *same* `Δs` between the
*same* states, yet `σ = 0` vs `σ = 4.9961 kJ/kg·K`.

## Run
```bash
cd code && python3 entropy.py         # Ex 6.1/6.2 pair, ideal-gas Δs
python3 test_entropy.py               # "All 16 tests passed."
```

## Files
`notes.md`, `code/entropy.py`, `code/test_entropy.py`, `problems/problems.md`, `refs.md`.
