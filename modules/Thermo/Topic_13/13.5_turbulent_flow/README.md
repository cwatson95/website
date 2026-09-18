# 13.5 — Turbulent Pipe Flow  *(~CM, not from Moran 8e)*

Module 5 of **Topic 13 (Compressible Flow & Gas Dynamics)** — the **cross-trunk**
companion to `13.4`: the *same pipe*, the *other* regime.

> **Cross-trunk note.** This material is standard **fluid mechanics (~CM)** and is **NOT
> in Moran 8e**. (Moran's Ch.9 — Topic 13's trunk — treats *compressible* flow; the
> viscous pipe-flow regimes are fluid mechanics. Moran 8e never defines the Reynolds
> number.) Sources are White, *Fluid Mechanics*; Munson, *Fundamentals of Fluid
> Mechanics*; Cengel & Cimbala, *Fluid Mechanics*.

- **Builds on:** `13.4` (Reynolds number, the laminar regime, Darcy–Weisbach).
- **Feeds into:** Moody-chart pipe-network design (beyond this leaf).

## Scope
Above `Re ≈ 4000` round-pipe flow is **turbulent** — chaotic, well-mixed, with a flatter
profile and a friction factor that depends on *both* `Re` and the relative roughness
`ε/D` (the Moody chart), no longer the exact laminar `64/Re`.

| use | relation | `code/turbulent_flow.py` |
|-----|----------|--------------------------|
| Reynolds number | `Re = ρVD/μ = VD/ν` | `reynolds_number`, `reynolds_number_kinematic` |
| regime | `Re<2300` lam · `2300–4000` trans · `>4000` turb | `is_turbulent`, `flow_regime` |
| smooth-pipe friction | Blasius `f = 0.316/Re^{1/4}` | `friction_factor_blasius` |
| general friction (Moody) | Colebrook `1/√f = −2log₁₀(ε/D/3.7 + 2.51/(Re√f))` | `friction_factor_colebrook` |
| explicit fit | Haaland (≈Colebrook to ~1.5%) | `friction_factor_haaland` |
| velocity profile | `u(r)=u_max(1−r/R)^{1/n}`, `V/u_max=2n²/((n+1)(2n+1))` | `power_law_velocity_profile`, `mean_velocity_power_law` |
| pressure drop / head loss | Darcy `f(L/D)(ρV²/2)` | `pressure_drop_darcy`, `head_loss_darcy` |

**Key idea:** turbulence replaces the laminar `f = 64/Re` with the **Colebrook/Moody**
`f(Re, ε/D)`; for a smooth wall at moderate `Re` the explicit **Blasius** `f = 0.316/Re^{1/4}`
suffices. The profile flattens (`V/u_max = 0.82` at `n=7`, vs `0.5` laminar), so mixing
and wall shear dominate. The `code` checks Colebrook’s residual vanishes, its rough-wall
limit hits Nikuradse, and the Darcy `ΔP = ρg·h_L` identity holds.

## Run
```bash
cd code && python3 turbulent_flow.py      # Re, Blasius vs Colebrook vs Haaland, profile
python3 test_turbulent_flow.py            # "All 22 tests passed."
```

## Files
`notes.md`, `code/turbulent_flow.py`, `code/test_turbulent_flow.py`, `problems/problems.md`, `refs.md`.
