# RE-07 — Relativistic Doppler Effect & Aberration

Module of the **RELATIVITY** trunk (see `modules/topic_network.txt`). How a light
ray's **frequency** and **direction** change between inertial frames — both read off
the Lorentz transformation of one null 4-vector, the 4-wavevector.

- **Prerequisites:** `RE-03` (Lorentz transformations — the boost `Λ`), `RE-05`
  (Minkowski 4-vectors & the null cone).
- **Feeds into:** `~RE-06` (relativistic dynamics — the photon 4-momentum is `ħk`),
  `~RE-08` (covariant formulation), `~EM-18` (relativistic electrodynamics, beaming).

## Scope
The **4-wavevector** `kᵘ = (ω, 𝐤)`, null for light (`k·k = 0`, `|𝐤| = ω`); the
**longitudinal**, **general angular**, and **transverse** Doppler shifts;
relativistic **aberration** `cosθ' = (cosθ−β)/(1−β cosθ)`, the **aberration of
starlight**, and the **headlight/beaming** cone `arccos β`; and a brief, conceptual
note on **Penrose–Terrell rotation** (a fast sphere still looks circular).

## Conventions (whole RE trunk)
- Natural units **c = 1**; event `x = (ct, x, y, z)`; metric **η = diag(−1,+1,+1,+1)**.
- `β = v/c`, `γ = 1/√(1−β²)`. Boost is along **+x** by the active RE-03 `Λ(β)`:
  `ct' = γ(ct − βx)`, `x' = γ(x − βct)` (frame S′ moves at `+β x̂`).
- **Angle convention:** `θ` is the ray's *propagation* angle from the boost axis,
  measured in the observer's frame. `θ=0` ⇒ approach/blueshift, `θ=π` ⇒
  recede/redshift, `θ=π/2` ⇒ transverse.

## The one idea
A plane wave's phase `kₘxᵐ` is a Lorentz scalar, so `kᵘ = (ω, 𝐤)` is a 4-vector,
**null** for light. **Doppler and aberration are the time part and the space part of
one transformation** `k' = Λk`:

```
ω'   = γω(1 − β cosθ)         ← Doppler   (the time component)
cosθ' = (cosθ − β)/(1 − β cosθ)   ← aberration (the spatial direction)
```

## Operations — `code/doppler_aberration.py`
| call | meaning |
|------|---------|
| `gamma(beta)`, `bondi_k(beta)` | `γ`; Bondi `k = √((1+β)/(1−β))` |
| `doppler_longitudinal(beta)` | `√((1−β)/(1+β))` — receding redshift `= 1/bondi_k` |
| `doppler_general(beta, theta)` | `1/(γ(1−β cosθ))` — full angular factor |
| `doppler_transverse(beta)` | `1/γ` at `θ=90°` — pure time-dilation redshift |
| `aberration(theta, beta)` | `θ'` with `cosθ'=(cosθ−β)/(1−β cosθ)` |
| `four_wavevector(omega, theta)` | null `kᵘ=(ω, ω cosθ, ω sinθ, 0)` |
| `transform_wavevector(beta, k)` | `k' = Λ(β)k` (RE-03 boost) — carries both effects |
| `wavevector_frequency(k)`, `wavevector_angle(k)` | read off `ω = k⁰`, `θ = atan2(k_y,k_x)` |
| `headlight_halfangle(beta)` | forward cone `arccos β` (half the photons) |

## Use
```python
from doppler_aberration import (doppler_longitudinal, doppler_transverse,
    doppler_general, aberration, four_wavevector, transform_wavevector,
    wavevector_frequency, wavevector_angle, headlight_halfangle)
import math

doppler_longitudinal(0.6)              # 0.5    (receding source, redshift)
doppler_transverse(0.6)                # 0.8    = 1/γ, pure time dilation
math.degrees(headlight_halfangle(0.9)) # 25.84° forward beaming cone

# one boost = Doppler AND aberration, exactly:
k  = four_wavevector(1.0, math.radians(50))
kp = transform_wavevector(0.6, k)
wavevector_frequency(k)/wavevector_frequency(kp)   # == doppler_general(0.6, 50°)
wavevector_angle(kp)                                # == aberration(50°, 0.6)
```

## Run
```bash
cd code
python3 doppler_aberration.py        # demo: Doppler tables, beaming, the k-boost cross-check
python3 test_doppler_aberration.py   # 8 property-based tests -> "All 8 tests passed."
```

## Files
- `notes.md` — 4-wavevector → Doppler (long./angular/transverse) → aberration → beaming → Terrell
- `code/doppler_aberration.py` — the library (pure stdlib; reuses RE-03's boost for the cross-check)
- `code/test_doppler_aberration.py` — limits, signs, fixed points, and the `k'=Λk` cross-check
- `problems/problems.md` — worked problems (Zee III.3/III.4; Griffiths Ch.12)
- `refs.md` — verified textbook citations
