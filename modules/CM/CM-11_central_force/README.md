# CM-11 — Central-Force Motion

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~CM-07`
(reduced mass), `~CM-09` (conserved L), `~MA-07` (integrator). **Links:** `~QM-12`
(hydrogen atom), `~RE-14` (Schwarzschild orbits).

## Scope
The reduction of a central-force problem to a 1-D radial motion in the **effective
potential** U_eff(r) = U(r) + L²/(2μr²), the circular orbit, **Kepler's laws**,
and a numerically integrated orbit (reusing MA-07) that conserves energy and
angular momentum.

## Operations — `code/central_force.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `effective_potential(U, L, mu)` | U(r) + L²/(2μr²) | Fowles §6.9 p.251 |
| `kepler_potential(k)`, `kepler_force(k)` | U = −k/r, F = −k/r² | Fowles §6.5 p.229 |
| `circular_orbit_radius(L, mu, k)` | r₀ = L²/(μk) | Fowles §6.5 p.229 |
| `kepler_period(a, mu, k)` | T = 2π√(μa³/k) (T² ∝ a³) | Fowles §6.3 p.225 |
| `orbit(force_radial, mu, r0, v0, …)` | integrate the planar orbit | Fowles §6.5 p.229 |

## Use
```python
from central_force import circular_orbit_radius, kepler_period, orbit, kepler_force
r0 = circular_orbit_radius(1.0, 1.0, 1.0)        # L^2/(mu k)
kepler_period(r0, 1.0, 1.0)                       # 2 pi sqrt(mu r0^3 / k)
ts, ys = orbit(kepler_force(1.0), 1.0, (r0,0), (0, 1.0/r0), 0, 6, 4000)
```

## Run
```bash
cd code
python3 central_force.py        # demo (U_eff minimum, integrated orbit, Kepler III)
python3 test_central_force.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/central_force.py` · `code/test_central_force.py` · `problems/problems.md`
