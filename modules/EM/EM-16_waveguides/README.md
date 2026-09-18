# EM-16 — Waveguides, Cavities & Transmission Lines

Sixteenth module of the **ELECTRICITY & MAGNETISM** trunk (see
`modules/topic_network.txt`); the wave-propagation thread `~EM-15` → **EM-16**.

- **Prerequisites:** `~EM-15` (electromagnetic waves) — used directly: the code
  imports the vacuum wave speed `C` from `em_waves`. The transverse mode pattern is
  a 2-D Helmholtz boundary-value problem (`~MA-08`, separation of variables).
- **Feeds into:** — (terminal leaf of the wave thread; the guide/cavity **mode**
  picture is reused by `~QO-01`, where the same modes are counted and quantized).

## Scope
A free plane wave (`~EM-15`) fills all of space. **Confine** it to a hollow
conductor and the transverse profile can no longer be arbitrary: the walls quantize
it into a discrete set of **modes** $(m,n)$, each with a **cutoff** angular
frequency
$$\omega_{mn}=c\pi\sqrt{(m/a)^2+(n/b)^2}\qquad(\text{Eq. 9.186}),$$
for a rectangular guide of cross-section $a\times b$. **Above** its cutoff a mode
propagates, but the guide is **dispersive**: phase velocity $v_p>c$, group
(signal/energy) velocity $v_g<c$, the two locked by $v_p\,v_g=c^2$. **Below** cutoff
the mode is **evanescent** — it decays as $e^{-\kappa z}$ and carries no power. The
lowest cutoff belongs to the dominant $\mathrm{TE}_{10}$ mode. A **TEM**
transmission line (two conductors — e.g. a coax) escapes all of this: it has **no
cutoff** and carries every frequency, down to DC, at $c$.

## Operations — `code/waveguides.py`

| call | meaning | reference (printed page) |
|------|---------|--------------------------|
| `cutoff_angular_frequency(m, n, a, b)` | ω_mn = cπ√((m/a)²+(n/b)²), the TE_mn / TM_mn cutoff | Gr §9.5.2 Eq.9.186 p.428 |
| `cutoff_frequency(m, n, a, b)` | f_mn = ω_mn/2π in Hz | Gr §9.5.2 p.428 |
| `dominant_mode_cutoff(a, b)` | lowest cutoff — the dominant TE₁₀ (a ≥ b): ω₁₀ = cπ/a | Gr §9.5.2 p.428 |
| `is_propagating(omega, m, n, a, b)` | ω > ω_mn? (propagating vs. evanescent) | Gr §9.5.2 p.428 |
| `guide_wavenumber(omega, omega_co)` | k = (1/c)√(ω²−ω_co²) above cutoff (else 0.0) | Gr §9.5.2 Eq.9.186 p.428 |
| `evanescent_decay(omega, omega_co)` | κ = (1/c)√(ω_co²−ω²) below cutoff (e^−κz) | Gr §9.5.2 p.428 |
| `phase_velocity_guide(omega, omega_co)` | v_p = c/√(1−(ω_co/ω)²) > c | Gr §9.5.2 p.428 |
| `group_velocity_guide(omega, omega_co)` | v_g = c√(1−(ω_co/ω)²) < c; note v_p·v_g = c² | Gr §9.5.2 p.428 |
| `tem_line_speed()` | TEM coax line: no cutoff, every frequency at c | Gr §9.5.3 p.431 |

Constant: `C` = vacuum speed of light $1/\sqrt{\mu_0\varepsilon_0}$, imported from
`~EM-15` (`em_waves`). Here `a`, `b` are the guide's cross-section dimensions (with
`a ≥ b`), `m`, `n` the mode integers, and `omega_co` a mode's cutoff angular
frequency `ω_mn`.

## Use
```python
from waveguides import (cutoff_frequency, dominant_mode_cutoff, is_propagating,
                        guide_wavenumber, phase_velocity_guide, group_velocity_guide,
                        evanescent_decay, tem_line_speed, C)

a, b = 0.0229, 0.0102                       # WR-90 X-band guide, metres
cutoff_frequency(1, 0, a, b) / 1e9          # ~6.55 GHz: the TE10 (dominant) cutoff
w_co = dominant_mode_cutoff(a, b)           # ~4.11e10 rad/s  (= c pi / a)

w = 1.5 * w_co                              # drive the dominant mode above cutoff
is_propagating(w, 1, 0, a, b)              # True
vp = phase_velocity_guide(w, w_co)          # > c
vg = group_velocity_guide(w, w_co)          # < c
vp * vg                                     # ~ c**2  (the hallmark identity)

evanescent_decay(0.5 * w_co, w_co)          # > 0: below cutoff -> e^{-kappa z}, no power
guide_wavenumber(0.5 * w_co, w_co)          # 0.0: no real wavenumber below cutoff
tem_line_speed()                            # c: a coax line passes every frequency
```

## Run
```bash
cd code
python3 waveguides.py          # demo: WR-90 cutoffs, TE10 dispersion, evanescence, TEM coax
python3 test_waveguides.py     # tests  ->  "All 7 tests passed."
```
(`waveguides.py` imports `~EM-15`'s `em_waves` by relative path for the wave speed
`C`; this becomes `from physkit… import …` once the shared package exists.)

## Files
- `notes.md` — derivations with inline page citations
- `code/waveguides.py`, `code/test_waveguides.py`
- `problems/problems.md` — worked problems (Griffiths §9.5)
- `refs.md` — full citation table (edition, section, **printed + PDF page**)
