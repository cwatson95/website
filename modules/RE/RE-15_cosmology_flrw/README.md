# RE-15 — Cosmology: the FLRW universe

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). General
relativity applied to the universe as a whole: the cosmological principle forces the
**FLRW metric**, and the Einstein equations reduce it to the **Friedmann equations**
for a single function, the scale factor `a(t)`.

- **Prerequisites:** `RE-11` (curvature — the **Einstein tensor**, which this module
  *imports*), `RE-13` (the Einstein field equations). Spatial slices are the
  constant-curvature 3-spaces of RE-11 §6.
- **Feeds into:** observational cosmology — distances & the distance ladder, the CMB,
  Big-Bang nucleosynthesis, and the growth of structure.

## Scope
The **cosmological principle** (homogeneity + isotropy) ⇒ the FLRW metric
`ds² = −dt² + a(t)²[dr²/(1−kr²) + r²dΩ²]`, `k = +1/0/−1`; the scale factor `a(t)`, the
**Hubble rate** `H = ȧ/a`, and cosmological **redshift** `1+z = a₀/a_emit`; feeding
FLRW into the Einstein equations to get the **Friedmann equations**; **critical
density** `ρ_c = 3H²/8π`, the density parameter `Ω = ρ/ρ_c`, and the flat/open/closed
trichotomy; the **three eras** (radiation `a∝t^½`, matter `a∝t^⅔`, de Sitter `a∝e^{Ht}`);
and the **fluid equation** `ρ̇ = −3H(ρ+p)` (= `∇_μT^{μν}=0`).

## The one idea
Demand that the universe look the same everywhere and in every direction. That single
symmetry collapses the metric to one function `a(t)`, and Einstein’s equations collapse
to two ODEs for it — the Friedmann equations. **The universe is described by one
equation.** This module doesn’t just assert that link: `G00_from_flrw` hands the FLRW
metric to RE-11’s curvature engine and *computes* `G₀₀ = 3[(ȧ/a)² + k/a²]`, recovering
the first Friedmann equation from the metric.

## Operations — `code/cosmology.py` (G = c = 1; mostly-plus; imports RE-11)
| call | meaning |
|------|---------|
| `flrw_metric(a_func, k)` | FLRW metric as a callable `x→g`, `x=(t,r,θ,φ)` |
| `hubble(a, adot)` | Hubble rate `H = ȧ/a` |
| `redshift(a_emit, a_obs=1)` | `1+z = a_obs/a_emit` |
| `friedmann_1_residual(a,adot,rho,k,Λ=0)` | `(ȧ/a)² − 8πρ/3 + k/a² − Λ/3` |
| `friedmann_2_residual(a,addot,rho,p,Λ=0)` | `ä/a + (4π/3)(ρ+3p) − Λ/3` |
| `fluid_equation_residual(rho,rhodot,a,adot,p)` | `ρ̇ + 3(ȧ/a)(ρ+p)` |
| `critical_density(H)` / `omega(rho,H)` | `ρ_c = 3H²/8π` / `Ω = ρ/ρ_c` |
| `G00_from_flrw(a_func,k,t,eps)` | `G₀₀` of FLRW via `curvature.einstein_tensor` |
| `de_sitter_scale_factor(H)`, `power_law_scale_factor(p)`, `era_density(a,w)` | reference solutions `e^{Ht}`, `t^p`, `a^{−3(1+w)}` |

## Use
```python
from cosmology import (G00_from_flrw, de_sitter_scale_factor,
                       friedmann_1_residual, critical_density, omega, redshift)

# FLRW => Friedmann, straight from the Einstein tensor (RE-11):
G00_from_flrw(de_sitter_scale_factor(1.0), 0, 0.7)   # ≈ 3H² = 3.0 (de Sitter, k=0)

friedmann_1_residual(1.0, 1.0, 3/(8*3.14159), 0)     # ≈ 0  (on-shell flat, ρ=ρ_c)
omega(critical_density(1.0), 1.0)                    # 1.0  (flat ⇔ Ω=1)
redshift(0.5)                                        # 1.0  (a_emit=½ ⇒ z=1)
```

## Run
```bash
cd code
python3 cosmology.py          # demo: FLRW⇒Friedmann (G₀₀), three eras, Ω trichotomy, redshift
python3 test_cosmology.py     # 13 tests -> "All 13 tests passed."
```
*(Imports RE-11 via `../../RE-11_curvature/code` — which itself adds MA-17 to
`sys.path`; run in place. Pure stdlib `math`.)*

## Files
- `notes.md` — cosmological principle ⇒ FLRW; `a(t)`, `H`, redshift; the Friedmann
  equations from `G_μν`; `ρ_c`/`Ω` trichotomy; the three eras; the fluid equation
- `code/cosmology.py` — the toolkit (imports RE-11’s `einstein_tensor`)
- `code/test_cosmology.py` — FLRW⇒Friedmann (loose FD tol); eras; fluid eq.; `Ω`; redshift
- `problems/problems.md` — worked problems (Zee, Dodelson)
- `refs.md` — page-verified citations
