# EM-11 — Electromagnetic Induction

Eleventh module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~EM-08` (magnetostatics — the **B** field and the constant
  `MU0`, used directly) and `~MA-02` (vector calculus — `surface_flux`, reused
  verbatim for the magnetic flux).
- **Feeds into:** `~EM-12` (AC circuits & driven RLC — an inductance `L` in a
  driven loop), `~EM-13` (Maxwell's equations — the induced-field law
  ∇×**E** = −∂**B**/∂t becomes one of the four).

## Scope
The first **time-dependent** chapter of the subject. A **changing magnetic flux
drives an EMF** — *Faraday's law* — and the induced current always flows so as to
**oppose the change** that produced it (*Lenz's law*, the minus sign). The flux can
change two ways: because **B** itself varies in time (a genuine induced electric
field, ∇×**E** = −∂**B**/∂t) or because the circuit moves through **B** (*motional*
EMF, the Lorentz force on the carriers). The flux itself, Φ = ∫**B**·d**a**, is just
the `~MA-02` `surface_flux` of the `~EM-08` field, reused without change.

Flux linkage proportional to current defines **inductance**, Φ = L I, and a
current-carrying coil stores energy that reads **two ways** — ½LI² in the circuit
or (1/2μ₀)∫B² dτ spread through the field — which agree exactly, echoing the
charge-vs-field energy duality of `~EM-06`. SI units throughout; a field is a
function `B(x, y, z) -> (Bx, By, Bz)` (the MA-02 convention), so `surface_flux`
acts on it with no glue code.

## Operations — `code/induction.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `flat_loop_surface(x0, x1, y0, y1, z)` | flat rectangular loop `S(u,v)` oriented +**ẑ**, ready for the flux integral | Gr §7.2.1 p.312 |
| `magnetic_flux(B, surf)` | Φ = ∫**B**·d**a** through the loop (reuses MA-02 `surface_flux`) | Gr §7.2.1 p.312 |
| `faraday_emf(flux_of_t, t)` | EMF = −dΦ/dt at time `t` (central difference) | Gr §7.2.1 p.312 |
| `lenz_sign(dflux_dt)` | sign of the induced EMF: opposite to the change in flux | Gr §7.2.1 p.312 |
| `motional_emf(B, v, length)` | EMF = B v L of a rod cutting field lines | Gr §7.1.3 p.305 |
| `solenoid_inductance(N, area, length)` | self-inductance L = μ₀N²A/l | Gr §7.2.3 Eq.7.27 p.321 |
| `mutual_inductance_solenoids(N1, N2, area, length)` | M = μ₀N₁N₂A/l, symmetric M₁₂ = M₂₁ | Gr §7.2.3 p.321 |
| `energy_in_inductor(L, I)` | W = ½LI² stored in an inductor | Gr §7.2.4 Eq.7.34 p.328 |
| `magnetic_energy_density(B)` | u = \|**B**\|²/2μ₀ as a scalar field | Gr §7.2.4 Eq.7.35 p.328 |
| `magnetic_field_energy_solenoid(N, area, length, I)` | W = (1/2μ₀)∫B² dτ for a solenoid (= ½LI²) | Gr §7.2.4 Eq.7.35 p.328 |

Constant: `MU0` (μ₀, the permeability of free space) is imported straight from
`~EM-08`. The flux and inductance/energy formulas are all built on it.

## Use
```python
import math
from induction import (flat_loop_surface, magnetic_flux, faraday_emf,
                       motional_emf, solenoid_inductance,
                       energy_in_inductor, magnetic_field_energy_solenoid)

# uniform B0 zhat through a flat 1 m^2 loop:  Phi = B0 * A
B    = lambda x, y, z: (0.0, 0.0, 0.4)
loop = flat_loop_surface(0.0, 1.0, 0.0, 1.0)
magnetic_flux(B, loop)                                  # ~ 0.4 Wb   (reuses MA-02 surface_flux)

# Faraday:  Phi(t) = B0 A sin(wt)  ->  EMF = -B0 A w cos(wt)
flux = lambda t: 0.5 * 0.01 * math.sin(100.0 * t)
faraday_emf(flux, 0.0)                                  # ~ -0.5 V   (= -B0 A w at t=0)

motional_emf(0.3, 2.0, 0.5)                             # 0.3 V      (B v L)

# solenoid inductance and the two energy pictures (they agree)
L = solenoid_inductance(1000, 1e-4, 0.2)               # ~ 6.28e-4 H
energy_in_inductor(L, 3.0)                              # ~ 2.83e-3 J  (1/2 L I^2)
magnetic_field_energy_solenoid(1000, 1e-4, 0.2, 3.0)   # ~ 2.83e-3 J  ((1/2mu0) int B^2 dV)
```

## Run
```bash
cd code
python3 induction.py          # demo: Faraday sinusoid, motional EMF, solenoid L, the two energy pictures
python3 test_induction.py     # tests  ->  "All 7 tests passed."
```
(`induction.py` chains `~EM-08` — and through it `~MA-01`/`~MA-02` — onto
`sys.path` by relative path; this becomes `from physkit… import …` once the shared
package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/induction.py`, `code/test_induction.py`
- `problems/problems.md` — worked problems (Griffiths §7.1–7.2)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
