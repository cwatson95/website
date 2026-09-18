# RE-13 — Einstein Field Equations

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The other
half of general relativity: having built the curvature of spacetime (RE-11) and
the motion of matter through it (RE-12), this module writes down the law that
couples them — **how matter curves spacetime**.

- **Prerequisites:** `RE-11` (curvature — the **Einstein tensor `G_μν`**; this
  module *imports* it), `RE-12` (geodesics — "spacetime tells matter how to
  move"). Soft: `~MA-16`/`~MA-17` (tensors, the metric).
- **Feeds into:** `~RE-14` (Schwarzschild — the vacuum solution verified here),
  `~RE-15` (FLRW cosmology — Friedmann's equations are `G_μν=8πT_μν` for a perfect
  fluid), `~RE-16` (gravitational waves), `~QF-05` (QFT in curved spacetime).
- **Cross-link:** `~EM-14` (the electromagnetic stress tensor — the canonical
  field `T_μν`; forward-referenced, **not** imported).

## Scope
The **Einstein field equation** `G_μν = 8πT_μν` and *why its left side is `G`*: the
contracted Bianchi identity `∇_μG^{μν}=0` (RE-11 §3) forces `∇_μT^{μν}=0`, local
energy–momentum conservation. The **stress-energy tensor** (perfect fluid, dust,
forward-ref the EM field); the **trace-reversed form** `R_μν=8π(T_μν−½Tg_μν)`; the
**cosmological constant** `G_μν+Λg_μν=8πT_μν`; the **vacuum** equation `R_μν=0`
(Schwarzschild) and the Λ-vacuum (de Sitter); and the **Newtonian/weak-field
limit** that reproduces Poisson `∇²Φ=4πρ` and so *fixes the constant `8π`*.

## The one idea
> *Spacetime tells matter how to move; matter tells spacetime how to curve.*

The second clause is one tensor equation, `G_μν = 8πT_μν` (G = c = 1). The Einstein
tensor `G = Ric − ½Rg` is **singled out** as the left side because it is the unique
divergence-free combination of the metric and its first two derivatives — so
setting it `∝ T_μν` makes conservation `∇_μT^{μν}=0` automatic. The proportionality
constant `8π` is then nailed by one demand: in the weak, slow, static limit the
equation must collapse to Newton.

## Operations — `code/einstein_equations.py` (G = c = 1; metric is a callable `x→g`)
| call | meaning |
|------|---------|
| `einstein_tensor(metric,x)` | `G_μν=R_μν−½Rg_μν` — thin wrapper of RE-11 |
| `stress_energy_perfect_fluid(rho,p,u,metric,x)` | `T_μν=(ρ+p)u_μu_ν+pg_μν` (lower indices; `u·u=−1`) |
| `stress_energy_dust(rho,u,metric,x)` | the `p=0` perfect fluid, `T_μν=ρu_μu_ν` |
| `trace(metric,T,x)` | `g^{μν}T_μν` (perfect fluid → `−ρ+3p`) |
| `trace_reversed_ricci(metric,T,x)` | `R_μν=8π(T_μν−½Tg_μν)` |
| `field_equation_residual(metric,T,x,Lambda=0)` | `G_μν+Λg_μν−8πT_μν` (`0` on a solution) |
| `newtonian_poisson_residual(Phi,x,eps)` | `G_00−2∇²Φ` for `g=η+h` — the weak-field check |
| `rest_four_velocity(metric,x)` | `u^μ=(1/√(−g_00),0,…)`, normalized |
| `minkowski_metric()`, `schwarzschild_metric(M)`, `de_sitter_metric(L)` | reference metrics |

## Use
```python
from einstein_equations import (field_equation_residual, stress_energy_perfect_fluid,
                                 trace, rest_four_velocity,
                                 minkowski_metric, schwarzschild_metric, de_sitter_metric)

sch = schwarzschild_metric(1.0)
field_equation_residual(sch, 0, [0, 10, 1.2, 0.7])      # ≈ 0  (vacuum: G_μν = 0)

mink = minkowski_metric()
u = rest_four_velocity(mink, [0, 0, 0, 0])               # (1, 0, 0, 0)
T = stress_energy_perfect_fluid(2.5, 0.4, u, mink, [0, 0, 0, 0])
T[0][0], trace(mink, T, [0, 0, 0, 0])                    # (2.5 = ρ, −1.3 = −ρ+3p)

ds = de_sitter_metric(10.0)
field_equation_residual(ds, 0, [0, 3, 1.2, 0.6], Lambda=3 / 10**2)   # ≈ 0  (Λ-vacuum)
```

## Run
```bash
cd code
python3 einstein_equations.py          # demo: vacuum, perfect fluid, trace-reversal, Newtonian limit, Λ
python3 test_einstein_equations.py     # 11 tests -> "All 11 tests passed."
```
*(Adds `../../RE-11_curvature/code` to `sys.path`, which in turn pulls in MA-17; run in place.)*

## Files
- `notes.md` — conservation→`G`, the field equation, the stress-energy tensor, the Newtonian limit, vacuum & Λ
- `code/einstein_equations.py` — the matter side (imports RE-11 for the geometry side)
- `code/test_einstein_equations.py` — vacuum, perfect-fluid algebra, trace-reversal, Newtonian limit, Λ
- `problems/problems.md` — worked problems (Zee, cpope)
- `refs.md` — verified citations
