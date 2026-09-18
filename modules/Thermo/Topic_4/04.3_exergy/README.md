# 4.3 — Exergy (availability)

Module of **Topic 4 (Properties & State Functions)**.

- **Builds on:** `4.2` (entropy & `σ`), `3.3` (2nd law), `4.1` (the `pV` structure).
- **Feeds into:** second-law efficiency (Topic 7), component/plant analysis (Topic 8),
  cycle improvement (Topic 9).

## Scope
**Exergy** is the maximum theoretical work available as a system relaxes to the
*dead state* `(T₀, p₀)`. From combined energy + entropy balances (Moran Ch.7):

| quantity | relation | `code/exergy.py` |
|----------|----------|-------------------|
| specific exergy | `e = (u−u₀)+p₀(v−v₀)−T₀(s−s₀)+ke+pe` | `specific_exergy` |
| exergy change | `(U₂−U₁)+p₀(V₂−V₁)−T₀(S₂−S₁)+…` | `exergy_change` |
| transfer w/ heat | `E_q = (1−T₀/T_b)Q` | `exergy_transfer_heat` |
| transfer w/ work | `E_w = W − p₀(V₂−V₁)` | `exergy_transfer_work` |
| **destruction** | `E_d = T₀·σ ≥ 0` | `exergy_destruction` |

Balance: `E₂−E₁ = E_q − E_w − E_d`. Unlike energy, exergy is **destroyed** by
irreversibilities — and `E_d = T₀σ` is exactly `T₀` times the entropy production of
module `4.2`.

## Run
```bash
cd code && python3 exergy.py          # Ex 7.2 (water), 7.3 (oven wall), HW 7.32
python3 test_exergy.py                # "All 14 tests passed."
```

## Files
`notes.md`, `code/exergy.py`, `code/test_exergy.py`, `problems/problems.md`, `refs.md`.
