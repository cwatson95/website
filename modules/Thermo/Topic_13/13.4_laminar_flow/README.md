# 13.4 — Laminar Pipe Flow  *(~CM, not from Moran 8e)*

Module 4 of **Topic 13 (Compressible Flow & Gas Dynamics)** — a **cross-trunk** bridge
to fluid mechanics.

> **Cross-trunk note.** This material is standard **fluid mechanics (~CM)** and is **NOT
> in Moran 8e**. There are no Moran citations here; sources are White, *Fluid Mechanics*;
> Munson, *Fundamentals of Fluid Mechanics*; Cengel & Cimbala, *Fluid Mechanics*.

- **Builds on:** the Reynolds-number idea (inertia vs viscosity) and pipe geometry.
- **Feeds into:** `13.5` (turbulent flow) — the same pipe, the *other* regime.

## Scope
The **Reynolds number** sets the flow regime; below `Re ≈ 2300` round-pipe flow is
**laminar** (orderly, layered), with an exact parabolic profile and friction factor.

| use | relation | `code/laminar_flow.py` |
|-----|----------|--------------------|
| Reynolds number | `Re = ρVD/μ = VD/ν` | `reynolds_number`, `reynolds_number_kinematic` |
| laminar criterion | `Re ≲ 2300` | `is_laminar` |
| friction factor | `f = 64/Re` (exact) | `friction_factor_laminar` |
| velocity profile | `u(r) = u_max(1−(r/R)²)`, `V = u_max/2` | `velocity_profile_parabolic`, `mean_velocity_from_max` |
| pressure drop | Darcy `f(L/D)(ρV²/2)` = Hagen–Poiseuille `32μLV/D²` | `pressure_drop_darcy`, `pressure_drop_hagen_poiseuille` |

**Key idea:** for laminar pipe flow the friction factor is the *exact* `f = 64/Re`, and
the Darcy–Weisbach pressure drop collapses to the Hagen–Poiseuille law `ΔP = 32μLV/D²` —
linear in velocity (the `code` checks the two forms agree to machine precision).

## Run
```bash
cd code && python3 laminar_flow.py      # Re, f=64/Re, Darcy == Hagen-Poiseuille
python3 test_laminar_flow.py            # "All 15 tests passed."
```

## Files
`notes.md`, `code/laminar_flow.py`, `code/test_laminar_flow.py`, `problems/problems.md`, `refs.md`.
