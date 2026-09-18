# RE-16 — Gravitational Waves

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). The wave
sector of general relativity: ripples in spacetime itself — their wave equation,
their two polarizations, how they move matter, and how orbiting masses make them.

- **Prerequisites:** `RE-11` (curvature — the linearized Riemann tensor is the
  tidal field a wave carries), `RE-13` (the Einstein field equations being
  linearized here), `RE-05` (η and the Minkowski inner product).
- **Feeds into:** gravitational-wave astronomy (LIGO/Virgo, GW150914), the
  inspiral templates of `~RE-17` (numerical relativity), and the radiation
  reaction that drives binary evolution.

## Scope
**Linearized gravity** `g = η + h`, `|h| ≪ 1`; the trace-reversed `h̄_{μν}` and the
**Lorenz-gauge wave equation** `□h̄_{μν} = −16πT_{μν}`; the **transverse-traceless
(TT) gauge** and its **two polarizations** `h_+`, `h_×`; the **area-preserving
deformation** of a ring of free particles; the **quadrupole formula** (no monopole
or dipole radiation) and its **luminosity**; and the **binary chirp** with the
**chirp mass** `M_c`.

## The one idea
Perturb flat spacetime, `g = η + h`, and Einstein's equation linearizes — in
Lorenz gauge — to the **ordinary wave equation** `□h̄ = −16πT`. In vacuum `□h̄ = 0`,
so gravity propagates **at c**, carrying just **two** transverse polarizations.
The wave **shears** space (stretch x ⇔ squeeze y) without changing volume
(traceless), and it is **sourced by the quadrupole** — mass and momentum
conservation forbid monopole and dipole radiation, so a spherical source is
silent and the lowest radiation is `O(1/c⁵)`, faint but real.

## Operations — `code/gravitational_waves.py` (G = c = 1; η = diag(−1,+1,+1,+1))
| call | meaning |
|------|---------|
| `tt_wave(h_plus, h_cross, omega, t, z)` | TT perturbation `h_{μν}` (4×4) of a `+z` wave at phase `ω(t−z)` |
| `is_transverse_traceless(h)` | spatial-traceless **and** time/propagation rows ≈ 0 |
| `dispersion_omega(k)` = `|k|` | null dispersion: waves travel at `c` |
| `wave_equation_residual(h_plus, h_cross, omega, k, t, z)` | `max|□h|` = 0 iff `ω=|k|` |
| `ring_response(h_plus, h_cross, phase, ring_points)` | displace each `ξ` by `½h^i_j ξ^j` |
| `area_change(h_plus, h_cross, phase)` | fractional ring-area change `= −¼(h_+²+h_×²)cos²` (`O(h²)≈0`) |
| `chirp_mass(m1, m2)` | `M_c = (m₁m₂)^{3/5}/(m₁+m₂)^{1/5}` |
| `gw_frequency(m1, m2, r)` = `2·orbital_frequency` | `(1/π)√(M/r³)` |
| `reduced_quadrupole(points)`, `quadrupole_luminosity(Q3dot)` | trace-free `Q̄_{ij}`; `P = ⅕Σ(Q⃛_{ij})²` |
| `chirp_rate(f, Mc)` | `(96/5)π^{8/3} M_c^{5/3} f^{11/3}` |

## Use
```python
from gravitational_waves import (tt_wave, is_transverse_traceless,
    dispersion_omega, wave_equation_residual, ring_response, area_change,
    chirp_mass, gw_frequency)

h = tt_wave(0.1, 0.05, 1.0, 0.0, 0.0)        # +z plane wave at t=z=0
is_transverse_traceless(h)                    # True  (spatial trace 0, transverse)
wave_equation_residual(0.1, 0.05, dispersion_omega(1.0), 1.0)  # ≈0  (travels at c)
ring_response(0.2, 0.0, 0.0, [(1,0),(0,1)])   # [(1.1,0.0), (0.0,0.9)]  stretch x, squeeze y
area_change(0.2, 0.0, 0.0)                    # ≈ -0.01  (O(h²): area preserved)
chirp_mass(36.0, 29.0)                        # 28.10  (GW150914-like, Msun)
gw_frequency(36.0, 29.0, 50.0)               # 0.00726 = 2 × orbital
```

## Run
```bash
cd code
python3 gravitational_waves.py        # demo: TT wave, speed c, ring, silent sphere, chirp
python3 test_gravitational_waves.py   # 12 property tests -> "All 12 tests passed."
```
*(Pure stdlib — `math` only; no third-party packages, no path setup.)*

## Files
- `notes.md` — linearized field eqn, Lorenz/TT gauge, polarizations, ring response, quadrupole formula, chirp
- `code/gravitational_waves.py` — the analytic toolkit (pure stdlib)
- `code/test_gravitational_waves.py` — TT, `□h=0`⇔`ω=|k|`, ring strain/area, polarization orthogonality, chirp mass, silent sphere
- `problems/problems.md` — worked problems (Zee §IX.4, §VI.5)
- `refs.md` — verified citations
