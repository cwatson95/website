# PK-04 — Atomic & Molecular Kinetics — Rate Equations, Excimer Chemistry & EEDF

Fourth module of the **PLASMA & KINETIC THEORY** trunk (see `modules/topic_network.txt`).
This module ties directly to the user's own research code — the KrF excimer-laser
plasma-kinetics simulator in `projects/Kinetic_Modeling/KrF_and_LoKI`.

- **Prerequisites:** `~SM-06` (kinetic theory, the Maxwellian $\langle\sigma v\rangle$),
  `~PK-01` (the electron kinetic equation that yields the EEDF).
- **Cross-links:** `~QO-03` (spontaneous/stimulated emission, laser gain — the photon
  side of KrF* kinetics), `~SM-06` (⟨σv⟩ averaging), `~PK-01` (non-Maxwellian EEDF).

## Scope
A laser-pumped gas is a coupled set of **rate equations** $\dot n_i=\sum$(production)$-\sum$(loss)
for every species, with each reaction weighted by a **rate coefficient**. For
electron-impact processes that coefficient is an EEDF average,
$k=\langle\sigma v\rangle=\int\sigma v\,f\,d^3v$, and for a threshold cross-section the
Maxwellian average collapses to the **Arrhenius** form $k\propto e^{-E_{\rm th}/kT}$ —
the activation energy *is* the cross-section threshold. In equilibrium **detailed
balance** between ionization and recombination fixes the **Saha** ionization fraction,
which climbs from neutral to fully ionized with temperature. The capstone is a 0-D
**KrF\* excimer** scheme — electron-impact pump, harpooning $\mathrm{Kr}^*+\mathrm{F_2}\to\mathrm{KrF}^*+\mathrm{F}$,
radiative decay $\mathrm{KrF}^*\to\mathrm{Kr}+\mathrm{F}+h\nu$ at 248 nm, and F₂ quenching —
integrated as a stiff ODE system in which KrF\* rises to a peak then decays while the
heavy-particle (atom) inventories are conserved exactly. Because the lower
$(\mathrm{Kr}+\mathrm{F})$ state is repulsive, emission is bound–free and the inversion
(hence 248 nm gain, `~QO-03`) is automatic. This is the teaching distillation of the
repo's `phantom11` simulator: a 26-element log-packed state vector, LoKI/EEDF swarm
tables, and `run_sim → build_rhs_u → rhs_u`.

## Operations — `code/molecular_kinetics.py`

| call | meaning | reference |
|------|---------|-----------|
| `maxwell_energy_pdf(E_eV, T)` | EEDF F(ε) = 2√(ε/π)(kT)⁻³ᐟ² e^{−ε/kT}, ∫F = 1, ⟨ε⟩ = 3/2 kT | Mi; `~SM-06` |
| `rate_coefficient_maxwellian(T, sigma0, E_threshold)` | k = ⟨σv⟩ over a Maxwellian EEDF (step σ), numeric energy integral | Mi; `~SM-06` |
| `rate_coefficient_step_closed_form(T, sigma0, E_threshold)` | k = σ₀⟨v⟩(1 + E_th/kT) e^{−E_th/kT} | Mi; `~SM-06` |
| `arrhenius(T, A, Ea)` | k = A e^{−Ea/kT} | Mi |
| `saha_ratio(T, E_ion, g_i, g_0)` | n_e n_i/n₀ = (2g_i/g₀)(2πm_e kT/h²)³ᐟ² e^{−E_ion/kT} | Mi |
| `saha_ionization_fraction(T, n_total, E_ion)` | ionization fraction x = n_i/n_total (rises with T) | Mi |
| `default_krf_params()` | authentic KrF* rate constants (r25/r31/r32) | Rh; phantom11 |
| `excimer_rhs(t, y, p)` | dy/dt = production − loss for [Kr, Kr*, F₂, F, KrF*, photons] | Rh; phantom11 |
| `simulate_krf(...)` | 0-D KrF* pulse via `scipy.integrate.solve_ivp` (stiff LSODA) | Rh; phantom11 |
| `photon_energy_eV(wavelength_nm)` | E = hc/λ (248 nm → 4.999 eV) | Rh; `~QO-03` |

Constants: `K_B_J`, `K_B_EV`, `M_E`, `E_CHARGE`, `H_PLANCK`, `C_LIGHT` (SI, eV companions).

## Use
```python
from molecular_kinetics import rate_coefficient_maxwellian, saha_ionization_fraction, simulate_krf

rate_coefficient_maxwellian(3.0e4, 1e-20, 9.9)     # ~1.1e-15 m^3/s  (rises with T)
saha_ionization_fraction(2.0e4, 1e24, 14.0)        # ~0.83           (rises with T)

res = simulate_krf()                               # 0-D KrF* excimer pulse
res["peak_KrFs"], res["peak_time"] * 1e9           # ~1.45e22 m^-3 at ~54 ns, then decays
```

## Run
```bash
cd code
python3 molecular_kinetics.py        # demo: rate coefficient vs T, Saha fraction, KrF* peak
python3 test_molecular_kinetics.py   # tests  ->  "All 11 tests passed."
```

## Files
- `notes.md` — rate equations, the EEDF average, Arrhenius/Saha, the KrF* scheme & gain
- `code/molecular_kinetics.py`, `code/test_molecular_kinetics.py`
- `problems/problems.md` — worked problems (Rhodes; Michel; Smirnov)
- `refs.md` — citation table (section/chapter level) + the in-repo KrF/LoKI living reference
