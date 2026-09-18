# EM-15 — Electromagnetic Waves

The wave/radiation block (`~EM-15`–`~EM-18`) of the **ELECTRICITY & MAGNETISM**
trunk (see `modules/topic_network.txt`), opening with the free-space wave.

- **Prerequisites:** `~EM-13` (Maxwell's equations — a plane wave is the
  source-free solution), `~MA-02` (`laplacian`, for the wave equation). The code
  also reuses `~EM-01`/`~EM-08` (`EPS0`, `MU0` → `c`) and `~MA-01` (`cross`,
  `dot`, `norm`, `unit`).
- **Feeds into:** `~EM-16` (waveguides & cavities — the wave confined between
  conductors), `~EM-17` (radiation — the wave with a source). Cross-links:
  `~MA-09` (Fourier — pulses from monochromatic waves), `~QO-01` (quantized light).

## Scope
The payoff of Maxwell's equations `~EM-13`: in empty space the four equations
combine into the **wave equation** ∂²f/∂t² = v²∇²f (Eq. 9.2), whose solutions
travel at v = ω/k. The simplest is a **transverse, monochromatic plane wave** —
**E** and **B** perpendicular to the propagation direction **k̂** and to each
other, with **B** locked to **E** by **B** = (1/v) **k̂**×**E** (Eq. 9.49) and
smaller by a factor v. In a linear medium the speed drops to v = c/n with
**refractive index** n = √(ε_r μ_r) (Eq. 9.68); at a normal interface the wave
splits into reflected and transmitted parts whose **Fresnel** amplitudes (Eq.
9.82) carry power fractions R and T that sum to 1. The transverse plane leaves
two degrees of freedom — **polarization** (linear, circular, or elliptical).

A scalar wave is a function `f(x, y, z, t)`, so `wave_equation_residual` feeds
its spatial part to the MA-02 `laplacian` and differences its time part,
returning ~0 *exactly* when ω = vk — the dispersion relation is **checked**, not
assumed. Amplitudes are MA-01 vectors, so `transverse_B` is just (1/v)
`cross`(k̂, **E₀**) and `is_transverse` is a `dot` against k̂. This module is the
companion to `~EM-13`: every plane wave here is a vacuum solution of those
equations, and the speed `C` = 1/√(μ₀ε₀) is assembled from `~EM-01`'s `EPS0` and
`~EM-08`'s `MU0`. SI units throughout.

## Operations — `code/em_waves.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `refractive_index(eps_r, mu_r=1)` | n = √(ε_r μ_r), index of refraction | Gr §9.3.1 Eq.9.68 p.401 |
| `phase_velocity(eps_r, mu_r=1)` | v = c/n in a linear medium | Gr §9.3.1 p.401 |
| `wavelength(omega, v=C)` | λ = 2πv/ω from frequency and speed | Gr §9.1.2 p.385 |
| `transverse_B(E0, khat, v=C)` | **B₀** = (1/v) **k̂**×**E₀**, the locked magnetic amplitude | Gr §9.2.2 Eq.9.49 p.394 |
| `is_transverse(vec, khat)` | test **vec**·**k̂** = 0 (transversality) | Gr §9.2.2 p.394 |
| `fresnel_normal(n1, n2)` | r = (n₁−n₂)/(n₁+n₂), t = 2n₁/(n₁+n₂) | Gr §9.3.2 Eq.9.82 p.403 |
| `reflectance(n1, n2)` | R = r², power fraction reflected | Gr §9.3.2 p.403 |
| `transmittance(n1, n2)` | T = (n₂/n₁)t² = 1 − R | Gr §9.3.2 p.403 |
| `scalar_plane_wave(k, omega)` | f = cos(kz − ωt), a +z travelling wave | Gr §9.1.2 p.385 |
| `wave_equation_residual(f, v, x,y,z,t)` | normalized ∂²f/∂t² − v²∇²f (≈0 iff ω=vk) | Gr §9.1.1 Eq.9.2 p.382 |
| `classify_polarization(Ax, Ay, delta)` | "linear" / "circular" / "elliptical" | Gr §9.1.4 p.391 |

Constant: `C` = 1/√(μ₀ε₀) ≈ 2.998×10⁸ m/s, the speed of light, built from
`~EM-01`'s `EPS0` and `~EM-08`'s `MU0`. `khat` is the propagation direction
(unit-normalized internally); the polarization phase `delta` = phase_y − phase_x.

## Use
```python
from em_waves import (transverse_B, refractive_index, phase_velocity,
                      fresnel_normal, reflectance, transmittance, C)
from vector_algebra import norm, dot                   # ~MA-01, straight onto the amplitudes

E0, khat = (1000.0, 0.0, 0.0), (0.0, 0.0, 1.0)         # E along x, wave travels +z
B0 = transverse_B(E0, khat)                            # ~ (0, 3.34e-6, 0) T, along +y
norm(B0)                                               # = norm(E0)/C : |B| = |E|/c
dot(E0, khat), dot(B0, khat)                           # (0, 0): E and B both transverse

refractive_index(2.25)                                 # 1.5   (glass, eps_r = 2.25)
phase_velocity(2.25)                                   # c/1.5 ~ 2.0e8 m/s

r, t = fresnel_normal(1.0, 1.5)                        # air -> glass: r = -0.2, t = 0.8
reflectance(1.0, 1.5), transmittance(1.0, 1.5)        # (0.04, 0.96): R + T = 1 (4% reflected)
```

## Run
```bash
cd code
python3 em_waves.py                # demo: transverse B from E, a medium, air->glass, residual, polarization
python3 test_em_waves.py           # tests  ->  "All 7 tests passed."
```
(`em_waves.py` chains `~EM-01`/`~EM-08` and `~MA-01`/`~MA-02` onto `sys.path` by
relative path; this becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/em_waves.py`, `code/test_em_waves.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 9)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
