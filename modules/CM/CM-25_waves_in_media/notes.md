# CM-25 — Waves in Continuous Media (notes)

Citation key (details + PDF pages in `refs.md`): **B** = Boas 3e.

## The wave equation and the string
A string of tension T and linear density μ, displaced transversely, obeys the
**wave equation** [B §13.4 p.633]
$$\frac{\partial^2 y}{\partial t^2}=c^2\frac{\partial^2 y}{\partial x^2},\qquad c=\sqrt{T/\mu}.$$
This is the continuum limit of the coupled oscillators of `~CM-16`. Code:
`wave_speed`; the PDE is solved by `~MA-08`'s `wave_1d`.

## Normal modes of a fixed–fixed string
Separation of variables (`~MA-08`) with y(0) = y(L) = 0 gives standing modes
sin(nπx/L)cos(ωₙt), so only discrete frequencies survive [B §13.4 p.633]:
$$f_n=\frac{nc}{2L},\qquad \lambda_n=\frac{2L}{n},\quad n=1,2,3,\dots$$
The harmonics are integer multiples of the fundamental — why strings sound
musical. Code: `string_mode_frequency`, `string_wavelength`; the test evolves a
plucked mode with `~MA-08`'s `wave_1d` and matches the standing-wave `wave_mode`.
A general pluck is a superposition of modes — a spatial Fourier series (`~MA-09`).

## Dispersion: phase vs group velocity
A wave e^{i(kx−ωt)} has **phase velocity** v_p = ω/k; a wave *packet* travels at
the **group velocity** v_g = dω/dk. The medium is **dispersive** when ω(k) is
nonlinear:
- **non-dispersive** (string, light in vacuum) ω = ck ⇒ v_p = v_g = c;
- **dispersive** (e.g. Klein–Gordon / a plasma) ω = √(c²k² + ω₀²) ⇒ v_p > c > v_g
  with v_p·v_g = c² (a test) — the phase outruns c but the signal (group) does not.

Code: `phase_velocity`, `group_velocity`, `nondispersive`, `klein_gordon`. The
electromagnetic version is `~EM-15`.
