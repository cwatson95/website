# CM-25 — Waves in Continuous Media

Classical-mechanics trunk (see `modules/topic_network.txt`). **Prereqs:** `~MA-08`
(the wave PDE), `~MA-09` (Fourier modes). **Links:** `~EM-15` (EM waves),
`~CM-16` (the discrete-oscillator limit).

## Scope
The wave equation on a string (y_tt = c²y_xx), its **normal modes** f_n = nc/2L,
the **wave speed** c = √(T/μ), and the distinction between **phase** and **group
velocity** in dispersive media. Reuses MA-08's `wave_1d`/`wave_mode`.

## Operations — `code/waves_in_media.py`
| call | meaning | references (printed page) |
|------|---------|---------------------------|
| `wave_speed(tension, mu)` | c = √(T/μ) | Boas §13.4 p.633 |
| `string_mode_frequency(n, c, L)` | f_n = nc/2L | Boas §13.4 p.633 |
| `string_wavelength(n, L)` | λ_n = 2L/n | Boas §13.4 p.633 |
| `phase_velocity(omega, k)` | v_p = ω/k | (standard) |
| `group_velocity(omega_of_k, k)` | v_g = dω/dk | (standard) |
| `nondispersive(c)`, `klein_gordon(c, omega0)` | dispersion relations ω(k) | (standard) |

## Use
```python
from waves_in_media import string_mode_frequency, phase_velocity, group_velocity, klein_gordon
string_mode_frequency(3, 10.0, 2.0)            # 3rd harmonic of a string
kg = klein_gordon(2.0, 1.0)                     # dispersive medium
phase_velocity(kg(1.0), 1.0), group_velocity(kg, 1.0)   # v_p > c > v_g, v_p*v_g = c^2
```

## Run
```bash
cd code
python3 waves_in_media.py        # demo (string modes, phase vs group velocity)
python3 test_waves_in_media.py   # tests -> "All N tests passed."
```

## Files
`notes.md` · `refs.md` · `code/waves_in_media.py` · `code/test_waves_in_media.py` · `problems/problems.md`
