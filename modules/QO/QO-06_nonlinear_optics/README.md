# QO-06 — Nonlinear Optics — χ⁽²⁾/χ⁽³⁾, Parametric, SBS & Raman

Closing module of the **QUANTUM & NONLINEAR OPTICS** trunk (see
`modules/topic_network.txt`) — and the textbook bridge to the user's
**SBS_Project** (stimulated Brillouin scattering).

- **Prerequisites:** `~EM-15` (EM waves in media — dispersion n(ω), the wave
  vector k = nω/c, intensity I ∝ E²), `~QO-01` (classical & quantized optical
  modes — the photon picture behind Manley–Rowe).
- **Cross-links:** `~EM-15` (refractive index / phase velocity → phase
  mismatch), `~QO-05` (parametric down-conversion is χ⁽²⁾ run as a quantum
  source → squeezing & entangled photons), `~QO-03` (stimulated emission / optical
  gain, the same exponential-gain language as SBS/Raman), `~PK-04` (excimer-laser
  kinetics — the high-fluence regime where the Kerr B-integral bites). **→
  SBS_Project** (the Brillouin gain spectrum, phase conjugation, pulse
  compression).

## Scope
At ordinary intensities a medium responds linearly, **P** = ε₀χ⁽¹⁾**E**, and
optics is superposition. Drive it with a laser and the polarization picks up
higher powers of the field, **P** = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + χ⁽³⁾E³ + …); because the
expansion parameter is the field measured against the atomic field
E_at ≈ 10¹¹ V/m, each order is smaller by ~E/E_at, so the new terms only matter
at laser intensities. The **χ⁽²⁾** term (non-centrosymmetric crystals) mixes
three waves: **second-harmonic generation** ω+ω→2ω, sum- and
difference-frequency, and **optical parametric amplification**. Whether they
build up coherently is set entirely by the **phase mismatch**
Δk = k(2ω) − 2k(ω): the SHG efficiency follows sinc²(ΔkL/2), peaking at Δk = 0
and first nulling at ΔkL = 2π, with **coherence length** L_c = π/|Δk| fixed by
material dispersion (`~EM-15`). Photon bookkeeping across any parametric step is
the **Manley–Rowe** relation — one pump photon in, one signal + one idler photon
out — which is energy conservation written per-photon. The **χ⁽³⁾** term (present
in every material) gives the **optical Kerr effect** n = n₀ + n₂I, hence
**self-phase modulation** φ_NL = (2π/λ)n₂IL (the laser "B-integral") and
four-wave mixing — and, through the same χ⁽³⁾, the **stimulated Brillouin (SBS)**
and **Raman** gains: a Lorentzian g(Ω) peaked at the acoustic/vibrational shift.
That SBS Lorentzian is precisely what the user's **SBS_Project** computes (gain
spectra, phase-conjugate mirrors, pulse compression).

## Operations — `code/nonlinear_optics.py`

| call | meaning | reference |
|------|---------|-----------|
| `chi_polarization(E, chi1, chi2, chi3)` | P = ε₀(χ⁽¹⁾E + χ⁽²⁾E² + χ⁽³⁾E³) | Boyd Ch.1 |
| `shg_phase_mismatch(n_fund, n_sh, wavelength_fund)` | Δk = (4π/λ)(n(2ω) − n(ω)) | Boyd Ch.2 |
| `shg_efficiency(delta_k, L, eta0=1)` | η = η₀ sinc²(ΔkL/2), peak at Δk=0 | Boyd Ch.2 |
| `coherence_length(delta_k)` | L_c = π/\|Δk\| | Boyd Ch.2 |
| `manley_rowe_check(omega_pump, omega_signal, I_pump, I_signal, I_idler, d_photons)` | photon-number conservation across a parametric step | Boyd Ch.2 |
| `kerr_index(n0, n2, I)` | n = n₀ + n₂I (optical Kerr effect) | Boyd Ch.4 |
| `kerr_phase(n2, I, L, wavelength)` | φ_NL = (2π/λ)n₂IL (self-phase modulation) | Boyd Ch.4/7 |
| `brillouin_shift(n, v_sound, wavelength_pump)` | ν_B = 2 n v_s/λ_p (backscatter) | Boyd Ch.9 |
| `brillouin_gain(Omega, Omega_B, gamma_B, g0=1)` | Lorentzian SBS gain, peak g₀ at Ω_B, FWHM γ_B | Boyd Ch.9 |
| `raman_gain(Omega, Omega_R, gamma_R, g0=1)` | Lorentzian SRS gain at the Raman shift | Boyd Ch.10 |

Constants (defined locally, SI): `C`, `EPS0`, `HBAR`. The code is self-contained
(numpy only).

## Use
```python
import numpy as np
from nonlinear_optics import (shg_efficiency, coherence_length, kerr_phase,
                              brillouin_shift, brillouin_gain, manley_rowe_check, C)

shg_efficiency(0.0, 1e-3)                  # 1.0  -- perfect phase matching (peak)
shg_efficiency(2*np.pi/1e-3, 1e-3)         # ~0   -- first null at Delta k L = 2 pi
coherence_length(3.543e5)                  # ~8.9e-6 m   (L_c = pi/|Delta k|)

kerr_phase(2.6e-20, 1e15, 1e-2, 1.064e-6)  # ~1.54 rad   (B-integral, self-phase mod.)

nu_B = brillouin_shift(1.33, 1480.0, 532e-9)   # ~7.4e9 Hz  (water, backscatter)
brillouin_gain(nu_B, nu_B, 100e6)              # 1.0  -- SBS gain peaks at the shift
```

## Run
```bash
cd code
python3 nonlinear_optics.py        # demo: chi^(n) orders, SHG sinc^2 nulls, L_c, Manley-Rowe, Kerr phase, SBS gain peak
python3 test_nonlinear_optics.py   # tests  ->  "All 10 tests passed."
```

## Files
- `notes.md` — derivations (χ⁽ⁿ⁾ series → SHG/phase matching → Manley–Rowe → Kerr/SPM → SBS/Raman) with chapter-level citations
- `code/nonlinear_optics.py`, `code/test_nonlinear_optics.py`
- `problems/problems.md` — worked problems (Boyd Ch.1, 2, 4, 9, 10)
- `refs.md` — citation table (Boyd 4e; Scully–Zubairy) + cross-links incl. SBS_Project
