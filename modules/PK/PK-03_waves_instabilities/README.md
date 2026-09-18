# PK-03 — Plasma Waves & Instabilities — Langmuir, Ion-Acoustic, Landau Damping

Third module of the **PLASMA & KINETIC THEORY** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** `~PK-01` (the kinetic / Vlasov distribution $f_0(v)$ and the
  plasma dielectric function), `~CM-15` (the driven harmonic oscillator and
  dispersion/resonance language).
- **Cross-links:** `~CM-23` (fluid limit; sound waves), `~CM-25` / `~EM-15` (waves in
  a dispersive medium), `~MA-06` (the Landau contour — residues & analytic
  continuation), `~PK-02` (the fluid/MHD moments that give Bohm–Gross without the
  kinetic damping).

## Scope
A plasma responds to any disturbance with collective fields, so it carries a family
of **electrostatic waves** set by two scales — the **plasma frequency**
ω_p = √(n e²/ε₀m_e) and the **Debye length** λ_D = √(ε₀k_BT/n e²) = v_th/ω_p.
**Langmuir (electron plasma) waves** ring near ω_p with a warm pressure correction,
the **Bohm–Gross** relation ω² = ω_p² + 3k²v_th² (cold limit ω→ω_p). **Ion-acoustic
waves** are the plasma's sound, ω = k c_s/√(1+k²λ_D²) with c_s = √(k_BT_e/m_i), going
to ω≈k c_s at long wavelength. Two effects have no acoustic analogue and need the
**kinetic (Vlasov, `~PK-01`)** picture: **Landau damping**, a collisionless loss to
particles resonant at the phase velocity v=ω/k (rate ∝ ∂f₀/∂v there; a falling
Maxwellian damps, γ<0), computed by deforming the velocity integral onto the
**Landau contour (`~MA-06`)**; and the **two-stream instability**, where two
counter-streaming beams give a *rising* resonant slope and the wave grows instead
(Im ω>0 for kv₀<ω_p, peak γ_max = ω_p/√8). This module makes all four quantitative
and checks the cold/long-wavelength limits, the damping sign, and the unstable band.

## Operations — `code/plasma_waves.py`

| call | meaning | reference |
|------|---------|-----------|
| `plasma_frequency(n, q, m)` | ω_p = √(n q²/ε₀m) | M §1.2.2 |
| `debye_length(n, T, q)` | λ_D = √(ε₀k_BT/n q²) = v_th/ω_p | M §1.2.1 |
| `thermal_speed(T, m)` | v_th = √(k_BT/m) | M §1.2.3 |
| `bohm_gross(k, n, T, m)` | Langmuir ω = √(ω_p²+3k²v_th²) | M §1.3.1.4 |
| `ion_acoustic(k, Te, n, mi)` | ω = k c_s/√(1+k²λ_D²), c_s=√(k_BT_e/m_i) | M §1.3.1.5 |
| `landau_damping_rate(k, n, T, m)` | γ = −ω_p√(π/8)(kλ_D)⁻³ exp(−1/2(kλ_D)²−3/2) | M §1.3.4 / A.4 |
| `two_stream_growth_rate(k, n, m, v0)` | Im ω from 1=½ω_p²[1/(ω−kv₀)²+1/(ω+kv₀)²] | M §1.3.1.3 |

Constants (SI, CODATA 2018): `EPS0`, `ELEM_CHARGE`, `ELECTRON_MASS`, `PROTON_MASS`, `K_B`.

## Use
```python
import numpy as np
from plasma_waves import (plasma_frequency, debye_length, bohm_gross,
                          ion_acoustic, landau_damping_rate, two_stream_growth_rate,
                          ELEM_CHARGE as e, ELECTRON_MASS as me, PROTON_MASS as mi)

n, T = 1e18, 1e4
wp = plasma_frequency(n, e, me)            # 5.64e10 rad/s
lD = debye_length(n, T, e)                 # 6.90e-6 m  (= v_th/wp)

bohm_gross(0.01/lD, n, T, me) / wp         # ~1.0001  -> w -> w_p as k->0
ion_acoustic(0.01/lD, T, n, mi) / (0.01/lD * (1.381e-23*T/mi)**0.5)  # ~1.0 -> w = k c_s
landau_damping_rate(0.4/lD, n, T, me) / wp # -0.096   (collisionless damping, gamma<0)

v0 = 5 * (1.381e-23*T/me)**0.5             # counter-streaming beam speed
two_stream_growth_rate(0.6124*wp/v0, n, me, v0) / wp   # ~0.354 = 1/sqrt(8) (peak growth)
```

## Run
```bash
cd code
python3 plasma_waves.py          # demo: dispersion samples, Landau rate, two-stream band
python3 test_plasma_waves.py     # tests  ->  "All 7 tests passed."
```

## Files
- `notes.md` — derivations: the two scales, Bohm–Gross, ion-acoustic, the Landau contour, two-stream
- `code/plasma_waves.py`, `code/test_plasma_waves.py`
- `problems/problems.md` — worked problems (Michel Ch.1 & Formulary A)
- `refs.md` — citation table (Michel, *Introduction to Laser-Plasma Interactions*; section-level)
