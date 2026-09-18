# RE-06 — Relativistic Dynamics

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). Mechanics
done right at high speed: 4-momentum, `E=mc²`, and the conservation law that runs
every particle collision.

- **Prerequisites:** `RE-05` (Minkowski 4-vectors & the mass shell); **`~CM-06`**
  (Newtonian linear momentum & its conservation — this is its relativistic
  completion). This module *imports* both.
- **Feeds into:** `~QM-22` (relativistic QM — `p·p = −m²` becomes the
  Klein–Gordon operator).

## Scope
The 4-momentum `p^μ = mU^μ = (E, 𝐩)`, `E = γm`, `𝐩 = γm𝐯`; the **mass shell**
`p·p = −m²` ⇔ `E² = p² + m²`; rest energy `E₀ = m` and kinetic energy
`T = (γ−1)m → ½mv²`; conservation of total 4-momentum in collisions (energy +
momentum as one law); the centre-of-momentum frame; system **invariant mass**;
production **thresholds**; and **Compton** scattering.

## The one idea
Energy and momentum are the time and space parts of one 4-vector, and **total
4-momentum is conserved** in every interaction. That single statement contains
Newtonian momentum conservation (the spatial part, `~CM-06`, recovered as `v→0`)
and energy conservation (the time part), now inseparable. Mass is rest energy and
can be created or destroyed — hence colliders have thresholds, and an inelastic
collision comes out heavier.

## Operations — `code/rel_dynamics.py` (c = 1)
| call | meaning |
|------|---------|
| `energy(m,v)`, `momentum(m,v)`, `kinetic_energy(m,v)` | `γm`, `γm𝐯`, `(γ−1)m` |
| `four_momentum(m,v)`, `photon_four_momentum(E,n̂)` | `(E,𝐩)` (via RE-05); null for light |
| `total_four_momentum`, `is_conserved(before,after)` | the conserved quantity |
| `system_invariant_mass(parts)` | `√(−P·P)` = COM energy (frame-independent) |
| `com_velocity(parts)` | `𝐏/E` — velocity of the COM frame |
| `inelastic_stick(m1,v1,m2,v2)` | collision → heavier product (KE→mass) |
| `threshold_kinetic_energy(m_b,m_t,M)` | min beam KE to make products of mass `M` |
| `compton_shift(θ,m_e)` | `(1−cosθ)/m_e` wavelength shift |

## Use
```python
from rel_dynamics import system_invariant_mass, photon_four_momentum, threshold_kinetic_energy, inelastic_stick

system_invariant_mass([photon_four_momentum(3,[1,0,0]), photon_four_momentum(3,[-1,0,0])])  # 6.0 (mass from light!)
threshold_kinetic_energy(1.0, 1.0, 4.0)        # 6.0  (p+p→p+p+p+p̄ : the 6 m_p antiproton threshold)
inelastic_stick(1.0,[0.8,0,0], 1.0,[-0.8,0,0]) # (3.333, [0,0,0]) — product heavier than 2
```

## Run
```bash
cd code
python3 rel_dynamics.py        # demo: mass shell, E=mc², collisions, thresholds, Compton
python3 test_rel_dynamics.py   # 9 tests -> "All 9 tests passed."
```
*(Adds RE-05 and CM-06 `code/` dirs to `sys.path`; run in place.)*

## Files
- `notes.md` — 4-momentum, E=mc², conservation, COM frame, thresholds, Compton
- `code/rel_dynamics.py` — the library (imports RE-05 + CM-06)
- `code/test_rel_dynamics.py` — mass shell, Newtonian limit vs CM-06, invariant-mass invariance, threshold
- `problems/problems.md` — worked problems (Griffiths §12.2)
- `refs.md` — verified citations
