# RE-17 — Exact solutions & numerical relativity  *(advanced)*

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The GR
capstone: the exact-solution landscape *beyond* Schwarzschild — **Kerr**,
**Reissner–Nordström**, **de Sitter** — each validated by feeding it back to
RE-11's curvature engine, plus the **3+1 / ADM** decomposition that begins
numerical relativity.

- **Prerequisites:** `RE-11` (curvature — **imported here**), `~RE-13` (Einstein
  field equations), `~RE-14` (Schwarzschild — the limit each solution reduces to).
- **Feeds into:** numerical relativity proper (binary mergers, gravitational-wave
  templates → `~RE-16`); the constant-curvature algebra reappears in `~RE-15`
  (FLRW cosmology). Forward-refs `~EM-14` for the EM source of Reissner–Nordström.

## Scope
What an **exact solution** is — a metric for which the field equations hold
identically — and how to *check* one numerically: **Kerr** (rotating, vacuum,
`R_{μν}=0`; horizons `r_±=M±√(M²−a²)`, ergosphere, frame dragging, ring
singularity); **Reissner–Nordström** (charged, `R_{μν}≠0` but scalar-flat `R=0`);
**de Sitter** (`Λ`-vacuum, `G_{μν}+Λg_{μν}=0`, `R=4Λ`). Then the move to
**numerical** relativity: the **3+1 / ADM** split (lapse `α`, shift `β^i`, spatial
`γ_{ij}`, extrinsic `K_{ij}`) into **constraints** + **evolution**, and the
**Hamiltonian constraint** initial data must satisfy.

## The one idea
We do not *solve* Einstein's equations here — we **write down** three famous
metrics and **verify** them: hand each to RE-11's finite-difference `ricci` /
`einstein_tensor` and read off the field equation. The vacuum check is the
validator — *if a Kerr component were wrong, `R_{μν}` would not vanish and the
test would fail.* The same `ricci` returns ≈0 for Kerr (vacuum) and ≠0 for
Reissner–Nordström (matter), reading off whether a source is present.

## Operations — `code/exact_solutions.py` (G = c = 1; mostly-plus; metric `x→g`)
| call | meaning |
|------|---------|
| `kerr_metric(M,a)` | Kerr in Boyer–Lindquist coords (rotating vacuum) |
| `reissner_nordstrom_metric(M,Q)` | charged BH, `f=1−2M/r+Q²/r²` (EM-sourced) |
| `de_sitter_metric(Λ)` | static patch, `f=1−Λr²/3` (`Λ`-vacuum) |
| `verify_vacuum(metric,x)` | `max|R_{μν}|` — ≈0 for Kerr/Schwarzschild |
| `verify_einstein_lambda(metric,x,Λ)` | `max|G_{μν}+Λg_{μν}|` — ≈0 for de Sitter |
| `kerr_horizons(M,a)` | `(r_−,r_+)=M∓√(M²−a²)`; raises if `a>M` (naked) |
| `kerr_ergosphere(M,a,θ)` | static limit `M+√(M²−a²cos²θ)` (`=2M` at equator) |
| `adm_decompose(metric,x)` | 3+1 split → lapse `α`, shift `β^i`, spatial `γ_{ij}` |
| `spatial_slice_metric(metric,t)` | `γ_{ij}(y)` of the `t=const` slice, as a callable |
| `hamiltonian_constraint_flat(metric,x,K_ij,rho)` | `R^{(3)}+K²−K_{ij}K^{ij}−16πρ` |

## Use
```python
from exact_solutions import kerr_metric, verify_vacuum, kerr_horizons, de_sitter_metric, verify_einstein_lambda

verify_vacuum(kerr_metric(1, 0.5), [0, 8, 1.0, 0.7])   # ≈ 0  (Kerr is Ricci-flat)
kerr_horizons(1, 0.5)                                  # (0.134, 1.866)
verify_einstein_lambda(de_sitter_metric(0.03), [0,3,1,0.7], 0.03)  # ≈ 0  (G+Λg=0)
```

## Run
```bash
cd code
python3 exact_solutions.py        # demo: Kerr vacuum, de Sitter R=4Λ, RN sourced, ADM split
python3 test_exact_solutions.py   # 13 tests -> "All 13 tests passed."
```
*(Adds `../../RE-11_curvature/code` to `sys.path` — which itself pulls in MA-17;
run in place. Pure stdlib `math`.)*

## Files
- `notes.md` — Kerr/RN/de Sitter, horizons & ergosphere, the 3+1/ADM split + constraints
- `code/exact_solutions.py` — the metrics, field-equation validators, and ADM algebra (imports RE-11)
- `code/test_exact_solutions.py` — vacuum/Λ-vacuum/sourced checks, Schwarzschild limits, horizons, ADM
- `problems/problems.md` — worked problems (Zee, Baumgarte–Shapiro, Stephani)
- `refs.md` — page-verified citations
