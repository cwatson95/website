# 6.2 — Irreversible Processes & Entropy Production

The realistic counterpart to the reversible ideal of **Topic 6** — every actual process
lives here, with **σ > 0**.

- **Builds on:** `6.1` (reversible limit, σ = 0), the entropy balance, the incompressible
  and ideal-gas Δs relations.
- **Feeds into:** `6.3` (minimum-work / isentropic-efficiency arguments), and the
  component-by-component loss accounting in Topics 7–9.

## Scope
The closed-system **entropy balance** `S₂−S₁ = ∫(δQ/T)_b + σ` [M §6.7], the sign law
`σ ≥ 0` [Eq. 6.26], and the **increase-of-entropy principle** for isolated systems
[Eq. 6.30]:

| use | relation | `code/irreversible.py` |
|-----|----------|------------------------|
| eight irreversibilities | (list) | `IRREVERSIBILITIES` |
| **entropy production** | `σ = ΔS − ∫δQ/T` | `entropy_production` |
| adiabatic σ | `σ/m = s₂−s₁` | `sigma_adiabatic` |
| steady σ̇ at one T_b | `σ̇ = −Q̇/T_b` | `entropy_production_rate` |
| **isolated/increase principle** | `σ = ΔS_sys+ΔS_surr` | `sigma_isolated` |
| incompressible Δs | `mc ln(T₂/T₁)` | `entropy_change_incompressible` |
| feasibility / class | `σ ≷ 0` | `is_possible`, `classify_process` |

**Key idea:** irreversibilities (friction, finite-ΔT heat transfer, unrestrained
expansion, mixing, …) **produce entropy**, `σ ≥ 0`. σ is *not a property* — same end
states, different paths give different σ (Ex 6.1 vs 6.2). The total entropy of an isolated
system can only **increase**.

## Run
```bash
cd code && python3 irreversible.py    # Ex 6.2 σ/m=4.9961; Ex 6.4 σ̇=4e-3; Ex 6.5 σ=0.0864
python3 test_irreversible.py          # "All N tests passed."
```

## Files
`notes.md`, `code/irreversible.py`, `code/test_irreversible.py`, `problems/problems.md`, `refs.md`.
