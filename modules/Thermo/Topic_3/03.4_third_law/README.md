# 3.4 — Third Law

Fourth module of **Topic 3 (The Laws)** — it fixes the *zero* of entropy.

- **Builds on:** `3.3` (second law / entropy direction), `3.1` (absolute `T`).
- **Feeds into:** absolute entropy `S` (`4.2`), Gibbs function & combustion (Topic 12).

## Scope
The **third law** (Moran §13.5.1, p.837):
> the entropy of a **pure crystalline** substance is zero at the absolute zero of
> temperature, 0 K or 0 °R.

Non-crystalline substances keep a nonzero *residual* entropy. With `S(0)=0` as the
datum, the **absolute entropy** follows from calorimetry,
`S(T) = ∫₀ᵀ c_p/T dT`; the Debye limit `c_p ~ aT³` makes the integrand vanish at
`T=0`, so `S(T)` is finite.

| concept | relation | `code/third_law.py` |
|---------|----------|----------------------|
| third-law datum | `S(0 K) = 0` (pure crystal) | `standard_entropy_at_zero` |
| Debye heat capacity | `c_p = a T³` | `debye_cp` |
| absolute entropy | `S(T) = ∫₀ᵀ c_p/T dT` | `absolute_entropy` |
| analytic check | `S = a T³/3` | `absolute_entropy_debye` |
| unattainability | `β = T_C/(T_H−T_C) → 0` | `carnot_cop_refrigerator` |

## Run
```bash
cd code && python3 third_law.py       # S(0)=0, Debye integral, unattainability
python3 test_third_law.py             # "All 11 tests passed."
```

## Files
`notes.md`, `code/third_law.py`, `code/test_third_law.py`, `problems/problems.md`, `refs.md`.
