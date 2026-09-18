# EM-13 — Maxwell's Equations

Thirteenth module of the **ELECTRICITY & MAGNETISM** trunk (see `modules/topic_network.txt`) —
where the static halves of `~EM-01` and `~EM-08` are stitched into one **dynamical** set by
the displacement current, and light falls out as the consequence.

- **Prerequisites:** `~EM-01` (electrostatics — supplies `EPS0` = ε₀ and the ∇·**E** = ρ/ε₀,
  ∇×**E** structure), `~EM-08` (magnetostatics — supplies `MU0` = μ₀ and the ∇·**B** = 0,
  ∇×**B** = μ₀**J** half), `~MA-02` (vector calculus — `divergence` and `curl`, the operators
  every one of the four equations is written in).
- **Feeds into:** `~EM-14` (conservation laws — Poynting's theorem, field energy & momentum
  follow from these four equations), `~EM-15` (electromagnetic waves — the vacuum solution
  worked out in full); the charge-continuity equation ∂ρ/∂t + ∇·**J** = 0 ties to `~CM-22`
  (**KEY BRIDGE B2**).

## Scope
The keystone of the subject: the four **Maxwell's equations**, and the one term —
**Maxwell's displacement current** $\mathbf J_d = \varepsilon_0\,\partial\mathbf E/\partial t$
(Eq. 7.38) — that Maxwell added to Ampère's law to make the set consistent and dynamical.
With it the four laws read ∇·**E** = ρ/ε₀, ∇·**B** = 0, ∇×**E** = −∂**B**/∂t, and
∇×**B** = μ₀**J** + μ₀ε₀ ∂**E**/∂t (Eq. 7.39–7.42).

Each equation is a statement about a **divergence or a curl** of **E** or **B**, so each maps
onto exactly one MA-02 operator and is checked directly on field functions — no glue code. The
fields here are 4-argument functions `F(x, y, z, t)`; each residual function freezes the time
slice and hands the spatial field to MA-02's `divergence`/`curl`. The headline,
`verify_vacuum_plane_wave`, feeds a vacuum plane wave through those operators and confirms all
four normalized residuals vanish — which happens only when ω = ck, forcing the wave speed
$c = 1/\sqrt{\mu_0\varepsilon_0}$: light is what electrostatics + magnetostatics + the
displacement current predict.

The verification runs in **natural units** (the wave speed `c` is a free parameter, taken = 1)
so the central-difference time derivative `partial_t` stays well conditioned; with the SI value
$c\approx3\times10^8$ the field would oscillate far faster than the finite step `dt`. The
genuine SI number is reported separately as `C_SI` = 1/√(μ₀ε₀) ≈ 2.998×10⁸ m/s. The residuals
are dimensionless (normalized by the local derivative scale), so "satisfied" means ≈ 0 in any
units.

## Operations — `code/maxwell_equations.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `displacement_current_density(dE_dt)` | **J**_d = ε₀ ∂**E**/∂t, Maxwell's fix to Ampère | Gr §7.3.2 Eq.7.38 p.334 |
| `plane_wave_fields(E0, k, c)` | vacuum plane wave (**E**, **B**, ω = ck); test vehicle | Gr §7.3.3 → §9.2.2 p.394 |
| `partial_t(F, x, y, z, t)` | central-difference ∂**F**/∂t of a 4-arg field | — (numeric helper) |
| `gauss_E_residual(E, rho, …)` | ∇·**E** − ρ/ε₀ (Gauss), normalized | Gr §7.3.3 Eq.7.39 p.337 |
| `gauss_B_residual(B, …)` | ∇·**B** (no monopoles), normalized | Gr §7.3.3 Eq.7.40 p.337 |
| `faraday_residual(E, B, …)` | ∇×**E** + ∂**B**/∂t (Faraday), normalized | Gr §7.3.3 Eq.7.41 p.337 |
| `ampere_maxwell_residual(E, B, J, …)` | ∇×**B** − μ₀**J** − μ₀ε₀ ∂**E**/∂t, normalized | Gr §7.3.3 Eq.7.42 p.337 |
| `verify_vacuum_plane_wave(E0, k, c, point, t)` | all four residuals at (point, t) → dict ≈ 0 | Gr §7.3.3 Eq.7.39–7.42 p.337 |

Constants: `EPS0` (ε₀, from `~EM-01`), `MU0` (μ₀, from `~EM-08`), and `C_SI` = 1/√(μ₀ε₀)
≈ 2.998×10⁸ m/s — the speed of light read straight off the two static constants. In
`ampere_maxwell_residual` the displacement term is written (1/c²) ∂**E**/∂t, since in the
wave's natural units μ₀ε₀ = 1/c²; the **J** term keeps the SI `MU0` (irrelevant in vacuum,
where **J** = 0).

## Use
```python
from maxwell_equations import (displacement_current_density, plane_wave_fields,
                               faraday_residual, gauss_B_residual,
                               verify_vacuum_plane_wave, C_SI)

C_SI                                                # ~ 2.998e8 m/s -- light from two static constants

displacement_current_density((1e12, 0, 0))[0]       # ~ 8.85 A/m^2: Jd = eps0 dE/dt (a charging capacitor)

E, B, w = plane_wave_fields(1.0, 1.0, c=1.0)        # +z plane wave: E along x, B along y, w = c k = 1
faraday_residual(E, B, 0.1, 0.2, 0.3, 0.4)          # ~1e-7: curl E + dB/dt = 0  (Eq. 7.41)
gauss_B_residual(B, 0.1, 0.2, 0.3, 0.4)             # ~0:    div B = 0, no magnetic charge (Eq. 7.40)

verify_vacuum_plane_wave(1.0, 1.0, 1.0, (0.1, 0.2, 0.3), 0.4)
#   {'gauss_E': ~0, 'gauss_B': ~0, 'faraday': ~1e-7, 'ampere_maxwell': ~1e-7}  -- all four satisfied
```

## Run
```bash
cd code
python3 maxwell_equations.py       # demo: c from constants, displacement current, plane-wave residuals
python3 test_maxwell_equations.py  # tests  ->  "All 6 tests passed."
```
(`maxwell_equations.py` chains EM-01/EM-08 — and through them MA-01/MA-02 — onto `sys.path`
by relative path; this becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/maxwell_equations.py`, `code/test_maxwell_equations.py`
- `problems/problems.md` — worked problems (Griffiths Ch. 7)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
