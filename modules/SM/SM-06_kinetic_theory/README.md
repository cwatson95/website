# SM-06 — Non-equilibrium & Kinetic Theory

Final module of the **STATISTICAL MECHANICS & THERMODYNAMICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~SM-01` (`K_B`, the statistical picture).
- **Cross-links:** `~PK-01` (Vlasov/Boltzmann kinetic theory), `~CM-23` (the fluid/Navier–Stokes limit).

## Scope
Equilibrium statistical mechanics gives the **Maxwell–Boltzmann speed distribution**
f(v) ∝ v² e^{−mv²/2kT}, with three characteristic speeds in fixed ratio,
v_p < ⟨v⟩ < v_rms, and mean kinetic energy ⟨½mv²⟩ = (3/2)kT (equipartition).
**Collisions** then set the **mean free path** λ = 1/(√2 nσ), the collision rate,
the **effusion** flux, and — by random walks between collisions — the **transport
coefficients** (diffusion). **Brownian motion** gives Einstein's relation D = µkT,
the prototype fluctuation–dissipation theorem; the **Boltzmann transport equation**
is the bridge to `~PK-01` and the fluid equations of `~CM-23`.

## Operations — `code/kinetic_theory.py`

| call | meaning | reference |
|------|---------|-----------|
| `maxwell_speed_pdf(v, m, T)` | f(v) = 4π(m/2πkT)^{3/2} v² e^{−mv²/2kT} | Pa §6.4 p.152 |
| `most_probable_speed(m, T)` | v_p = √(2kT/m) | Pa §6.4 p.152 |
| `mean_speed(m, T)` | ⟨v⟩ = √(8kT/πm) | Pa §6.4 p.152 |
| `rms_speed(m, T)` | v_rms = √(3kT/m) | Pa §6.4 p.152 |
| `mean_kinetic_energy(T)` | ⟨½mv²⟩ = (3/2)kT | Pa §6.4 p.152 |
| `mean_free_path(n, diameter)` | λ = 1/(√2 nπd²) | Pa §6.4 p.152 |
| `collision_rate(n, d, m, T)` | z = ⟨v⟩/λ | Pa §6.4 p.152 |
| `effusion_flux(n, m, T)` | Φ = ¼ n⟨v⟩ | Pa §6.4 p.152 |
| `diffusion_coefficient(n, d, m, T)` | D = ⅓⟨v⟩λ | Pa §6.4 p.152 |
| `einstein_relation_diffusion(mobility, T)` | D = µkT | Pa §15.2 p.587 |

Constant: `K_B` (re-exported).

## Use
```python
from kinetic_theory import mean_speed, rms_speed, mean_free_path, K_B

m_N2 = 4.652e-26
mean_speed(m_N2, 300.0), rms_speed(m_N2, 300.0)    # 476, 517 m/s  (v_p < <v> < v_rms)
n = 101325/(K_B*300.0)                              # number density at 1 atm
mean_free_path(n, 3.7e-10)                          # ~6.7e-8 m (67 nm)
```

## Run
```bash
cd code
python3 kinetic_theory.py          # demo: speeds, equipartition, mean free path, diffusion, Einstein relation
python3 test_kinetic_theory.py     # tests  ->  "All 7 tests passed."
```

## Files
- `notes.md` — derivations with inline page citations
- `code/kinetic_theory.py`, `code/test_kinetic_theory.py`
- `problems/problems.md` — worked problems (Pathria Ch.6, Ch.15; Schroeder Ch.6)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
