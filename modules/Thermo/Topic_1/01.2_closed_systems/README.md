# 1.2 — Closed Systems (Control Mass)

Topic 1 (*Foundations & system concepts*) module; see `modules/Thermo/list.txt`.
Standalone — cross-links use the `list.txt` numbering.

- **Prerequisites:** `2` energy & work and `3.2` the First Law (the balance this
  applies); `1.5` quasiequilibrium (needed for `∫p dV` to be defined).
- **Generalized by:** `1.1` open systems — a control volume is this control-mass
  balance plus the flow terms `Σṁ(h+V²/2+gz)`.
- **Feeds into:** `2` expansion/compression work, the gas-power **cycles** in
  group `9` (Otto, Diesel, Stirling — all closed-system piston cycles).

## Scope
A **closed system** (control mass) is a fixed quantity of matter: no mass crosses
the boundary, only heat `Q` and work `W`. Two things to compute:

1. **Energy balance** — `ΔKE + ΔPE + ΔU = Q − W` (sign: `Q` in +, `W` out +).
2. **Boundary work** of a quasiequilibrium volume change — `W = ∫p dV`, with the
   closed form for a **polytropic** process `pVⁿ = const`:
   `W = (p₂V₂ − p₁V₁)/(1 − n)` for `n ≠ 1`, and `p₁V₁ ln(V₂/V₁)` for `n = 1`.

Derivations with page citations are in `notes.md`/`refs.md`.

## Operations — `code/closed_systems.py`

| call | meaning | reference (Moran 8e) |
|------|---------|----------------------|
| `delta_KE(m, V1, V2)` / `delta_PE(m, z1, z2)` | ½m(V₂²−V₁²) / mg(z₂−z₁) | §2.1 |
| `energy_balance_residual(Q, W, dU, dKE, dPE)` | (Q−W) − (ΔU+ΔKE+ΔPE); 0 when satisfied | §2.5 "Energy Balance for Closed Systems" |
| `heat_transfer(W, dU, …)` / `work_done(Q, dU, …)` | solve the balance for Q or W | §2.5 |
| `power_balance_residual(Qdot, Wdot, dEdt)` | time-rate form `dE/dt = Q̇ − Ẇ` | §2.5 |
| `pdv_work_trapz(p_of_V, V1, V2)` | `∫p dV` numerically (any path) | §2.2 "Expansion or Compression Work" |
| `polytropic_work(p1, V1, V2, n)` | closed-form `∫p dV` for `pVⁿ=const` | §2.2 |
| `polytropic_pressure(p1, V1, V2, n)` | `p₂ = p₁(V₁/V₂)ⁿ` | §2.2 |
| `constant_pressure_work(p, V1, V2)` | `p(V₂−V₁)` (polytropic n=0) | §2.2 |

Units: `p` [kPa], `V` [m³] ⇒ `Q, W, U` [kJ]; `m` [kg], velocity [m/s], `z` [m].

## Use
```python
from closed_systems import polytropic_work, polytropic_pressure, work_done

# air compressed pV^1.3 = const from 100 kPa, 1 m^3 to 0.5 m^3
polytropic_pressure(100, 1, 0.5, 1.3)     # 246.2 kPa
W = polytropic_work(100, 1, 0.5, 1.3)     # -77.05 kJ  (work in)
# if adiabatic, the first law gives the internal-energy rise:
work_done(Q=0.0, dU=0.0) - W              # dU = Q - W = +77.05 kJ
```

## Run
```bash
cd code
python3 closed_systems.py          # demo: polytropic, isothermal, adiabatic, KE/PE
python3 test_closed_systems.py     # tests  ->  "All 15 tests passed."
```

## Files
- `notes.md` — energy balance & `∫p dV` derivations with inline page citations
- `code/closed_systems.py`, `code/test_closed_systems.py`
- `problems/problems.md` — worked problems (Moran Ch.2)
- `refs.md` — citation table (section, equation, **printed + PDF page**)
