# NE-05 — Radioactive decay modes

Fifth module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§§5.1–5.4** (printed pp. 97–111) of Shultis &
Faw, 3rd ed.: the decay modes, their Q-values in atomic masses, and how the
released energy is shared among the products.

- **Prerequisites:** `~NE-04` (Q-values and the neutral-atom substitution rule
  that this module has to modify mode by mode), `~NE-03` ($Q_\alpha=-S_\alpha$),
  `~NE-02` (mass parabolas — which decide *which* mode a nuclide takes),
  `~CM-06` (momentum conservation in a two-body break-up).
- **Cross-links:** `~NE-06` (how fast these decays go), `~NE-07` (chains of them),
  `~NE-09` (fission fragments are born neutron-rich and cascade by $\beta^-$;
  delayed neutrons are P5 of the problem set), `~NE-15` (sharp alpha lines vs
  continuous beta spectra, and what detectors do with each), `~NE-17`
  (Appendix D's per-decay yields feed internal dose), `~NE-27` (annihilation
  photons from $\beta^+$ are the basis of PET).

## Scope
Every decay Q-value is a difference of **atomic** masses, but the electron
bookkeeping differs by mode — and that is the module:

$$Q_\alpha=M(\mathrm{P})-M(\mathrm{D})-M(^4\mathrm{He}),\qquad
Q_{\beta^-}=M(\mathrm{P})-M(\mathrm{D}),$$
$$Q_{\beta^+}=M(\mathrm{P})-M(\mathrm{D})-2m_e,\qquad
Q_{\mathrm{EC}}=M(\mathrm{P})-M(\mathrm{D}).$$

The $2m_ec^{2}=1.022$ MeV penalty on positron emission is not pedantry: since
$\beta^+$ and EC connect the same pair, a parent with $0<Q_{\mathrm{EC}}<1.022$
MeV can **only** capture — which is exactly why ⁷Be, ⁵¹Cr, ⁵⁵Fe, ¹²⁵I and ¹⁴⁵Sm
are pure EC emitters. Alpha decay is two-body, so the alpha emerges with a sharp
$E_\alpha=Q\,A_D/(A_D+4)\approx0.98Q$; beta decay is three-body, so the electron
gets a continuous spectrum whose endpoint is $Q$. Both are checked against
Appendix D: Q from masses reproduces the measured beta endpoints of ³H, ¹⁴C, ³²P
and ⁹⁰Sr to better than 0.3 keV, and for ⁶⁰Co the endpoint plus the two-gamma
cascade closes on $Q$ to 0.3 keV out of 2824.

## Operations — `code/decay_modes.py`

| call | meaning | reference |
|------|---------|-----------|
| `daughter_of(A, Z, mode)` | $(A,Z)$ of the daughter for any mode | §5.2 |
| `q_alpha(A, Z, excitation)` | $M(\mathrm{P})-M(\mathrm{D})-M(^4\mathrm{He})$ | Eq. (5.7) |
| `alpha_kinetic_energy(A, Z)` | $Q\,M_D/(M_D+M_\alpha)$ — the sharp line | Eq. (5.11) |
| `daughter_recoil_energy(A, Z)` | $Q-E_\alpha$ | Eq. (5.12) |
| `q_beta_minus(A, Z)` | $M(\mathrm{P})-M(\mathrm{D})$, no correction | Eq. (5.14) |
| `q_beta_plus(A, Z)` | $M(\mathrm{P})-M(\mathrm{D})-2m_e$ | Eq. (5.18) |
| `q_electron_capture(A, Z)` | $M(\mathrm{P})-M(\mathrm{D})$ | Eq. (5.22) |
| `beta_endpoint(A, Z, mode)` | $(E_\beta)_{\max}=Q$ | Eq. (5.16) |
| `q_isomeric_transition(E*)` | gamma decay: $Q=E^{*}$ | §5.4.1 |
| `q_neutron_emission(A, Z)` | $-S_n$; positive only with excitation (delayed neutrons) | §5.4.6 |
| `q_proton_emission(A, Z)` | $-S_p$, neutral-atom form | §5.4.7 |
| `allowed_decay_modes(A, Z)` | `{mode: Q}` for every mode with $Q>0$ | §5.4 |
| `dominant_decay_mode(A, Z)` | the largest-$Q$ open mode | §5.4 |
| `TWO_ME_MEV` | $2m_ec^{2}=1.02200$ MeV | Eq. (5.18) |
| `load_decay_radiation()`, `measured_emissions(nuc, group)` | Appendix D emission data | App. D |

## Use
```python
from decay_modes import (q_alpha, alpha_kinetic_energy, q_beta_minus,
                         q_beta_plus, q_electron_capture, dominant_decay_mode)

q_alpha(226, 88)                  # 4.8706 MeV
alpha_kinetic_energy(226, 88)     # 4.7844 MeV -- the measured line energy
q_beta_minus(3, 1) * 1000         # 18.59 keV  -- the tritium endpoint
q_electron_capture(7, 4)          # +0.8618 MeV
q_beta_plus(7, 4)                 # -0.1602 MeV  => 7Be is a pure EC emitter
dominant_decay_mode(238, 92)      # 'alpha'
```

## Run
```bash
cd code
python3 decay_modes.py        # demo: alpha splits, the three beta modes, EC window
python3 test_decay_modes.py   # tests  ->  "All 20 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv` and `D1_decay_radiation.csv`.

## Files
- `notes.md` — the four Q-values and *why* each electron correction is what it is
  → the 1.022 MeV EC-only window → sharp lines vs continuous spectra →
  cross-appendix validation (including the one case that does not close) → mode
  prediction and its limits, with a "Where this goes" map.
- `code/decay_modes.py`, `code/test_decay_modes.py` (stdlib only). Tests include
  the cross-appendix check (masses vs measured endpoints), the ⁶⁰Co cascade
  closing to 0.3 keV, and the documented 3.3 keV ¹³⁷Cs disagreement.
- `problems/problems.md` — 8 worked problems: the seven parts of S&F Ch. 5
  Prob. 1 (one per decay mode, including delayed neutron and delayed proton
  emission and internal conversion) plus Prob. 2 on gamma recoil.
- `figures/` — the EC-only window, the alpha energy split, a sharp alpha line
  against a continuous beta spectrum, and the ⁶⁰Co energy budget closing across
  two appendices.
- `refs.md` — page-verified citations, plus the Appendix B / Appendix D
  disagreement for ¹³⁷Cs.
