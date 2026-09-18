# QF-05 — QFT in Curved Spacetime — Hawking & Unruh Effects

Capstone of the **QUANTUM FIELD THEORY** trunk (see `modules/topic_network.txt`),
and the entry point to the user's **Quantum_Optics curved-spacetime / squeezed-
spacetimes** research line. Where `~QF-01` quantized fields against a fixed vacuum,
this module shows that vacuum is observer-dependent — and that acceleration and
horizons turn it thermal.

- **Prerequisites:** `~QF-01` (canonical quantization & the vacuum / mode
  expansion), `~RE-13` (Einstein equations & the stress-energy source), `~RE-14`
  (Schwarzschild horizon, r_s = 2M, surface gravity κ).
- **Cross-links:** `~QO-05` (squeezing & two-mode squeezed vacua — a horizon is a
  squeezer), `~SM-06`/`~SM-01` (the Bose–Einstein / Planck distribution that the
  spectrum turns out to be), `~RE-15` (cosmological particle creation, the same
  Bogoliubov machinery in an expanding universe).

## Scope
A free quantum field has no preferred particle decomposition once observers
accelerate or spacetime curves: expanding the same field in two complete mode sets
relates their annihilation operators by a **Bogoliubov transformation**
a′_j = Σ_k(α*_{jk} a_k − β*_{jk} a_k†), normalized so Σ_k(|α_{jk}|² − |β_{jk}|²) = 1.
The mixing coefficients **are** particles: the rotated vacuum holds
⟨N⟩ = Σ_k|β_{jk}|² of them. Two horizons make this thermal. A uniformly accelerated
(**Rindler**) observer sees the Minkowski vacuum as a Planckian bath at the **Unruh
temperature** T_U = ℏa/2πck_B, because |β_ω|²/|α_ω|² = e^{−2πcω/a} forces the
occupation to 1/(e^{ℏω/k_BT_U} − 1). A black hole radiates at the **Hawking
temperature** T_H = ℏc³/8πGM k_B = ℏκ/2πck_B — inversely proportional to mass, so
~6×10⁻⁸ K for the Sun but ~10²³ K for a 1 kg hole — and slowly evaporates with a
lifetime τ ∝ M³. The optical face of all this, α = cosh r, β = sinh r, is **two-mode
squeezing**: the horizon is a squeezer (`~QO-05`).

## The one idea
β ≠ 0 means particles. One coefficient does everything: it is the off-diagonal piece
of the change of mode basis, it is the squeezing of the vacuum, and — through the
single relation |β_ω|²/|α_ω|² = e^{−ℏω/k_BT} — it is a *thermal* spectrum. Unruh and
Hawking are the same theorem evaluated at two horizons, with T fixed by the
acceleration a or the surface gravity κ.

## Operations — `code/curved_spacetime.py` (SI units, defined locally)
| call | meaning | reference |
|------|---------|-----------|
| `schwarzschild_radius(M)` | r_s = 2GM/c² (`~RE-14`) | BD Ch. 8 |
| `surface_gravity(M)` | κ = c⁴/4GM = c²/2r_s | BD Ch. 8 |
| `unruh_temperature(a)` | T_U = ℏa/2πck_B (linear in a) | BD §4.5 |
| `hawking_temperature(M)` | T_H = ℏc³/8πGM k_B = ℏκ/2πck_B (∝ 1/M) | BD Ch. 8 |
| `bose_occupation(omega, T)` | Planck factor 1/(e^{ℏω/k_BT} − 1) | BD Ch. 4 |
| `fermi_occupation(omega, T)` | 1/(e^{ℏω/k_BT} + 1) | BD Ch. 4 |
| `bogoliubov_check(alpha, beta)` | Σ\|α\|² − Σ\|β\|² (must be 1) | BD §2.2 |
| `particle_number(beta)` | ⟨N⟩ = Σ_k\|β_k\|² | BD §3.4 |
| `squeeze_to_bogoliubov(r)` | (cosh r, sinh r) — the horizon as a squeezer (`~QO-05`) | Ful |
| `thermal_beta_squared(omega, T, statistics)` | 1/(e^{ℏω/k_BT} ∓ 1) — the spectrum *is* Planckian | BD Ch. 4 |
| `unruh_beta_ratio(omega, a)` | \|β_ω\|²/\|α_ω\|² = e^{−2πcω/a} | BD §4.5 |
| `unruh_occupation(omega, a)` | 1/(e^{2πcω/a} − 1) from the ratio + normalization | BD §4.5 |
| `evaporation_lifetime(M)` | τ = 5120πG²M³/ℏc⁴ (∝ M³) | BD Ch. 8 |

Constants (SI): `HBAR`, `C`, `K_B`, `G`, `M_SUN`.

## Use
```python
from curved_spacetime import (unruh_temperature, hawking_temperature,
                              bose_occupation, unruh_occupation,
                              bogoliubov_check, squeeze_to_bogoliubov,
                              evaporation_lifetime, M_SUN)

unruh_temperature(1e20)                 # 0.4055 K  (linear in a)
hawking_temperature(M_SUN)              # 6.17e-8 K (colder than the CMB)
hawking_temperature(1.0)               # 1.23e23 K (T_H ~ 1/M)

# the accelerated vacuum is thermal: Bogoliubov occupation == Bose factor at T_U
a, w = 1e20, 5e10
unruh_occupation(w, a) - bose_occupation(w, unruh_temperature(a))   # ~1e-16

# a horizon is a two-mode squeezer: |alpha|^2 - |beta|^2 = 1
alpha, beta = squeeze_to_bogoliubov(1.3)
bogoliubov_check(alpha, beta)          # 1.0  (commutators preserved)

evaporation_lifetime(M_SUN) / 3.156e7  # 2.1e67 yr
```

## Run
```bash
cd code
python3 curved_spacetime.py        # demo: T_U(a), Planckian spectrum, T_H(M_sun)/1kg, Bogoliubov norm, lifetime
python3 test_curved_spacetime.py   # tests  ->  "All 12 tests passed."
```
*Self-contained (SI constants defined locally; numpy only). No sibling imports;
runs in well under a second.*

## Files
- `notes.md` — Bogoliubov transformations, the squeezed-vacuum picture, Unruh, the thermal spectrum, Hawking, evaporation (10 display equations)
- `code/curved_spacetime.py`, `code/test_curved_spacetime.py`
- `problems/problems.md` — worked problems (Birrell & Davies Ch. 2–4, 8; Fulling)
- `refs.md` — chapter-level citations (Birrell–Davies, Fulling) + cross-links incl. the user's Quantum_Optics curved-spacetime work
