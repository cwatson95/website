# NE-24 — Fusion reactors: Lawson criterion, the triple product, MCF & ICF

Twenty-fourth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), opening Chapter 12. Covers **§§12.1–12.4** (printed
pp. 429–455) of Shultis & Faw, 3rd ed.: plasmas and the Saha equation, D-T and
D-D reactivity, bremsstrahlung and ignition, the gain factor, Lawson and the
triple product, magnetic confinement and ITER, inertial confinement, and the Z
machine, spherical tokamak and stellarator.

- **Prerequisites:** `~NE-10` (fusion Q-values, the Gamow peak), `~NE-13` (the
  14.1 MeV neutron), `~PK-01`/`~PK-02` (plasma physics).
- **Cross-links:** `~NE-25` (direct conversion), `~NE-22` (the fission plant
  fusion must eventually beat).

## Scope
Why the most energetic reaction available is also the hardest to use. Three
difficulties compound: a plasma switches on abruptly (Saha), it radiates faster
than it burns until an ignition temperature that is 17× higher for D-D than D-T,
and it must then be *held* — n·τ·T ≥ 3 × 10¹⁵ keV s cm⁻³. Magnetic confinement
buys that with τ ~ 1 s; inertial confinement has 0.8 ns and must buy it with a
thousandfold compression instead. And even then, a power plant needs Q ≈ 20, not
the Q = 1 of "break-even".

## Operations — `code/fusion.py`

| call | meaning | reference |
|------|---------|-----------|
| `saha_ionization_fraction(T, n, I)` | the ionised fraction | Eq. (12.1) |
| `sigma_v_dt(kT)`, `sigma_v_dd(kT)` | ⟨σv⟩ cm³/s — **the curves S&F only draw** | Fig. 12.1 |
| `fusion_power_density(n, kT, rxn)` | n²⟨σv⟩Q/4 (D-T) or /2 (D-D) | Eq. (12.5) |
| `bremsstrahlung_power_density(n, kT, Z)` | 1.42e−34 Z² n² √T | Eq. (12.6) |
| `ignition_temperature(rxn, Z)` | where they cross; fuel property only | §12.2 |
| `gain_factor(...)`, `breakeven_alpha_fraction(rxn)` | Q ≈ 20; 3.5/17.6 | Eq. (12.7) |
| `energy_confinement_time(n, kT, P_loss)` | 3nkT/P_loss — note the **3** | Eq. (12.8) |
| `lawson_n_tau(kT, rxn)` | 12kT/(E_c⟨σv⟩), or 6 for D-D | Eq. (12.10) |
| `triple_product(kT, rxn)`, `optimal_temperature(rxn)` | nτT and its minimum | Eqs. (12.11)–(12.14) |
| `icf_confinement_time(R, kT)` | R√(m/kT) — nanoseconds | Eq. (12.15) |
| `areal_density_for_burn(φ)`, `icf_burn_fraction(ρR)` | φ = ρR/(ρR+H_B) | added |
| `REACTIONS`, `ITER` | Eqs. (12.2)–(12.3); §12.2.6 | — |

## Use
```python
from fusion import (saha_ionization_fraction, sigma_v_dt, ignition_temperature,
                    gain_factor, breakeven_alpha_fraction, lawson_n_tau,
                    triple_product, optimal_temperature, icf_confinement_time,
                    areal_density_for_burn, K_B_EV)

saha_ionization_fraction(13150.0, 2e21, 13.06)   # 0.950 -- S&F's example
saha_ionization_fraction(13150.0, 2e21)          # 0.924 with the true 13.598 eV

ignition_temperature("D-T") * 1e3 / K_B_EV       # 3.1e7 K  (S&F Fig. 12.2: 3e7)
ignition_temperature("D-D") * 1e3 / K_B_EV       # 5.3e8 K  (S&F Fig. 12.2: 6e8)

gain_factor()                                    # 20.4 -- what a PLANT needs
breakeven_alpha_fraction("D-T")                  # 0.199 -- what Q = 1 buys

optimal_temperature("D-T")                       # (13.6 keV, 3.0e15 keV s cm^-3)
icf_confinement_time(0.05, 10.0)                 # 8.0e-10 s for a 1 mm pellet
areal_density_for_burn(0.3)                      # 2.6 g/cm2 vs ~0.02 uncompressed

sigma_v_dd(150.0)                                # raises: the Gamow fit is wrong there
```

## Run
```bash
cd code
python3 fusion.py        # demo: Saha, ignition, Lawson, the gain factor, ICF
python3 test_fusion.py   # tests  ->  "All 10 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — the three compounding difficulties in order, then why Q = 1 is not
  the goal, then the two ways to satisfy Lawson, with a "Where this goes" map and
  a note on the module's finding.
- `code/fusion.py`, `code/test_fusion.py` (stdlib only). Both reactivity fits
  **refuse** outside their range; the D-D fit is allowed to 100 keV precisely
  because D-D ignition at 46 keV sits in its degraded band — which is itself
  worth knowing — and its docstring states which direction the error runs.
- `problems/problems.md` — 6 worked problems with numeric `*Check:*` lines.
- `figures/` — the Saha switch with both ionisation energies, the power balance
  reproducing Fig. 12.2's ignition temperatures, Lawson beside the triple product
  and why it replaced it, and ICF's nanoseconds beside the compression they force.
- `refs.md` — page-verified citations; the 13.06 eV ionisation energy and how the
  book's own example is consistent with it; the reactivity fits and their
  validation; and a garbled sentence in §12.2.6.
