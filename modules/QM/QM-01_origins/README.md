# QM-01 — Origins of Quantum Theory

Root module of the **QUANTUM MECHANICS** trunk (see `modules/topic_network.txt`).

- **Prerequisites:** none (this is the QM root). Light contact with classical
  EM (black-body = thermal radiation) and `~CM-15` (oscillators) helps but isn't
  required.
- **Feeds into:** `~QM-02` (the de Broglie wave becomes the wavefunction whose
  modulus-squared is a probability density), `~QM-03` (Schrödinger equation).

## Scope
The four experiments that classical physics could not explain, and the quantum
postulates introduced to fix each — as **closed-form formulae you can evaluate**:

1. **Black-body radiation** — Planck's law, its Rayleigh–Jeans (UV catastrophe)
   and Wien limits; Stefan–Boltzmann and Wien displacement recovered as
   *consequences*.
2. **Photoelectric effect** — Einstein's quantum of light, `K_max = hf − W`.
3. **Bohr model** — quantized energies/orbits and the Rydberg spectral series.
4. **de Broglie waves** — `λ = h/p`, matter as waves (the seed of the trunk).
5. **Compton scattering** — the photon's momentum `p = h/λ`.

**House rule for this module:** nothing is quoted. σ, the Wien constant `b`, the
Rydberg constant and the Compton wavelength are all **rederived** from the
fundamental constants (h, c, k_B, e, mₑ) — by *integrating* Planck (→ σ),
*maximising* Planck (→ b), and assembling combinations of constants — then
checked against CODATA in the tests. (This is the QM-trunk analogue of MA-01's
"three kinds of input, one set of functions": here it is *one set of constants,
every result derived.*)

## Operations — `code/origins.py`

| call | meaning | formula |
|------|---------|---------|
| `planck_u_nu(nu, T)` | spectral energy density | u = (8πhν³/c³)/(e^{hν/kT}−1) |
| `rayleigh_jeans_u_nu` / `wien_u_nu` | classical limits | hν≪kT and hν≫kT |
| `stefan_boltzmann_sigma()` | σ by integrating Planck | ∫u dν = aT⁴, σ = ca/4 |
| `wien_displacement_b()` | b by maximising Planck | λ_max·T = b |
| `photoelectric_Kmax(f, W)` | Einstein | K_max = hf − W (clamped ≥0) |
| `threshold_frequency(W)` | cutoff | f₀ = W/h |
| `bohr_energy_eV(n, Z)` | Bohr levels | Eₙ = −13.6 Z²/n² eV |
| `bohr_radius(n, Z)` | Bohr orbit | rₙ = n²a₀/Z |
| `rydberg_wavelength(n1, n2, Z)` | spectral line | 1/λ = RZ²(1/n1²−1/n2²) |
| `de_broglie_wavelength(p)` / `_from_energy(E)` | matter wave | λ = h/p |
| `compton_shift(theta)` | photon momentum | Δλ = λ_C(1−cosθ) |

Constants `h, hbar, c, k_B, e, m_e, eps0` (and the reference values `a0, Ry_eV,
R_inf, sigma_SB, wien_b, lambda_C` used only to *check* the rederivations) are
exported too.

## Use
```python
from origins import (stefan_boltzmann_sigma, wien_displacement_b,
                     bohr_energy_eV, rydberg_wavelength, de_broglie_from_energy, e)

stefan_boltzmann_sigma()              # 5.6704e-08  (rederived, not quoted)
wien_displacement_b() / 5772 * 1e9    # 502 nm  -> the Sun's spectrum peaks green
bohr_energy_eV(1)                     # -13.606 eV  (hydrogen ionization energy)
rydberg_wavelength(2, 3) * 1e9        # 656.1 nm  (Balmer H-alpha, visible red)
de_broglie_from_energy(100 * e) * 1e9 # 0.1226 nm (why electron microscopes work)
```

## Run
```bash
cd code
python3 origins.py          # demo: the numbers that broke classical physics
python3 test_origins.py     # tests  ->  "All 12 tests passed."
```

## Files
- `notes.md` — the five clusters, each with its derivation and the failure it fixed
- `code/origins.py` — the library (pure `math`; σ, b, R rederived, not quoted)
- `code/test_origins.py` — 12 checks: limits, recovered constants, spectral lines
- `problems/problems.md` — worked problems (Griffiths 3e)
- `refs.md` — verified textbook locations
