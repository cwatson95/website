# EM-14 — EM Conservation Laws

Conservation-laws module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-01` (the field **E**, the constant `EPS0` = ε₀), `~EM-08`
  (magnetostatics, `MU0` = μ₀), `~MA-01` (`cross`, `dot`, `norm`) — all imported directly.
- **Feeds into:** `~EM-15` (plane EM waves make `⟨S⟩` and radiation pressure concrete),
  `~EM-17` (an accelerating charge radiates this Poynting flux out to infinity).

## Scope
Once the fields are dynamical (`~EM-13`), the **electromagnetic field itself carries
energy, momentum and angular momentum**, and the books balance. The field stores an
**energy density** $u$, transports it with the **Poynting flux**
**S** = (1/μ₀)(**E**×**B**) — the energy flux, built on the MA-01 `cross` — carries a
**momentum density** **g** = ε₀(**E**×**B**) = **S**/c², and exerts forces through the
**Maxwell stress tensor** $T_{ij}$. Each obeys a **continuity equation**: the same
local-conservation bookkeeping as mass (`~CM-22`) and charge (KEY BRIDGE B2).

For a **plane wave** all of this collapses to the memorable trio $S = c\,u$, $g = u/c$
and $T_{zz} = -u$; an absorbing surface then feels a **radiation pressure** $S/c$
($2S/c$ if it reflects). Fields are the same `E(x, y, z) -> (Ex, Ey, Ez)` functions as
`~EM-01`/`~EM-08`, so the densities and fluxes here are just MA-01 vector algebra applied
to them — no glue code. SI units throughout.

## Operations — `code/conservation_laws.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `poynting_vector(E, B)` | **S** = (1/μ₀)(**E**×**B**), the energy flux (reuses MA-01 `cross`) | Gr §8.1.2 Eq.8.10 p.358 |
| `energy_density(E, B)` | u = (ε₀/2)\|**E**\|² + (1/2μ₀)\|**B**\|² | Gr §8.1.2 Eq.8.13 p.357 |
| `momentum_density(E, B)` | **g** = ε₀(**E**×**B**) = **S**/c² | Gr §8.2.3 Eq.8.30 p.366 |
| `maxwell_stress_tensor(E, B)` | T_ij = ε₀(E_iE_j − ½δ_ij E²) + (1/μ₀)(B_iB_j − ½δ_ij B²), a 3×3 | Gr §8.2.2 Eq.8.19 p.362 |
| `radiation_pressure(S_mag, reflected=False)` | P = S/c (absorber), 2S/c (reflector) | Gr §8.2.3 p.366 |
| `plane_wave_snapshot(E0, k, z_phase=0, c=C)` | snapshot (**E**,**B**) of a +z plane wave, B₀ = E₀/c | Gr §9.2.2 Eq.9.49 p.394 (→ `~EM-15`) |

Constants: `EPS0` (ε₀, via `~EM-01`), `MU0` (μ₀, via `~EM-08`), and `C` = 1/√(μ₀ε₀) ≈
3.00×10⁸ m/s (built from the two). **E**, **B** are passed as field *functions*; each
return value is itself a function of (x, y, z) — a scalar for `energy_density`, a triple
for `poynting_vector`/`momentum_density`, a 3×3 list for `maxwell_stress_tensor`.

## Use
```python
from conservation_laws import (
    poynting_vector, energy_density, momentum_density,
    radiation_pressure, plane_wave_snapshot, C,
)
from vector_algebra import norm                       # ~MA-01, straight onto the field

E, B = plane_wave_snapshot(1000.0, k=0.0)             # +z plane wave, E0 = 1000 V/m
S = poynting_vector(E, B)                             # S(x,y,z) = (1/mu0) E x B  (along +z)
u = energy_density(E, B)
g = momentum_density(E, B)

norm(S(0, 0, 0)), C * u(0, 0, 0)                      # equal:  S = c u   (plane wave)
norm(g(0, 0, 0)), u(0, 0, 0) / C                      # equal:  g = u / c
radiation_pressure(norm(S(0, 0, 0)))                  # S/c  -> pressure on an absorber (Pa)
radiation_pressure(norm(S(0, 0, 0)), reflected=True)  # 2S/c -> pressure on a mirror
```

## Run
```bash
cd code
python3 conservation_laws.py          # demo: plane-wave S, u, g, radiation pressure, T_zz = -u
python3 test_conservation_laws.py     # tests  ->  "All 7 tests passed."
```
(`conservation_laws.py` imports `~EM-01`/`~EM-08` and `~MA-01` by relative path; this
becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/conservation_laws.py`, `code/test_conservation_laws.py`
- `problems/problems.md` — worked problems (Griffiths §8.1–8.2)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
