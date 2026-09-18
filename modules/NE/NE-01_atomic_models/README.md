# NE-01 — Atomic models

First module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`), a chapter-by-chapter replica of Shultis & Faw,
*Fundamentals of Nuclear Science and Engineering*, 3rd ed. Covers **§3.1,
"Development of the Modern Atom Model"** (printed pp. 54–63). The trunk opens
here because Chapters 1–2 are a units and modern-physics review already held by
`~MA-01`, `~RE-02`…`~RE-06` and `~QM-01`…`~QM-08`.

- **Prerequisites:** `~QM-03` (quantization and the old quantum theory),
  `~EM-06` (Coulomb's law and the electrostatic potential energy the orbit
  balance uses), `~CM-05` (circular motion, centripetal force). Helpful:
  `~RE-06` (the relativistic check on $v_1/c$).
- **Cross-links:** `~QM-08` (the quantum atom that replaces Bohr's orbits),
  `~NE-02` (the same modelling move applied to the nucleus), `~NE-03` (nuclear
  binding energies — $10^{6}$ times the atomic ones here), `~NE-05` (electron
  capture and internal conversion act on these atomic levels), `~NE-12`
  (photoelectric absorption edges *are* inner-shell ionization energies),
  `~QO-02` (atom–field interaction and line emission).

## Scope
Two experiments and one model. **Alpha scattering** killed the plum-pudding
atom: Thomson's model predicts $P(\ge\phi)=e^{-\phi/\phi_m}$ with
$\phi_m\simeq1^{\circ}$, so $P(\ge90^{\circ})\approx8\times10^{-40}$, while
Geiger and Marsden measured 1 in 8000 — and Rutherford put the positive charge in
a nucleus $10^{4}$ times smaller than the atom. The **hydrogen spectrum** killed
the classical orbit: sharp lines, not a continuum. Bohr's model quantizes angular
momentum, $L=nh/2\pi$, and balances Coulomb attraction against the centripetal
requirement, giving
$$r_n=\frac{n^{2}h^{2}\epsilon_0}{\pi m_e Ze^{2}},\qquad
v_n=\frac{Ze^{2}}{2\epsilon_0 nh},\qquad
E_n=-\frac{m_e(Ze^{2})^{2}}{8\epsilon_0^{2}n^{2}h^{2}}=-13.606\frac{Z^{2}}{n^{2}}\ \text{eV}.$$
Transitions then reproduce the *empirical* Rydberg formula
$1/\lambda=R(1/n_o^{2}-1/n^{2})$, and replacing $m_e$ by the reduced mass $\mu_e$
turns $R_\infty$ into the measured $R_H=10\,967\,758$ m$^{-1}$ — agreement to
eight significant figures, from four fundamental constants.

## Operations — `code/atomic_models.py`

| call | meaning | reference |
|------|---------|-----------|
| `thomson_scattering_probability(phi_deg)` | $P(\ge\phi)=e^{-\phi/\phi_m}$, the plum-pudding prediction | p. 58 |
| `bohr_radius(n, Z)` | $r_n=n^{2}h^{2}\epsilon_0/(\pi m_e Ze^{2})$ | Eq. (3.4) |
| `bohr_velocity(n, Z)` | $v_n=Ze^{2}/(2\epsilon_0 nh)$ | Eq. (3.4) |
| `bohr_angular_momentum(n)` | $L=nh/2\pi$ (postulate 2) | Eq. (3.3) |
| `bohr_energy(n, Z)` | $E_n=-13.606\,Z^{2}/n^{2}$ eV | Eq. (3.5) |
| `bohr_orbital_period(n, Z)` | $T=2\pi r_n/v_n$ | §3.1.4 |
| `ionization_energy(Z, n)` | $-E_n$; 13.606 eV for H, 54.42 eV for He⁺ | Ex. 3.1 |
| `transition_energy(n_lo, n_hi, Z)` | $h\nu=E_{n_{hi}}-E_{n_{lo}}$ | Eq. (3.6) |
| `transition_wavelength(n_lo, n_hi, Z)` | $\lambda=hc/\Delta E$ | Eq. (3.7) |
| `rydberg_wavelength(n_lo, n_hi, Z, R)` | the empirical $1/\lambda=RZ^{2}(1/n_o^{2}-1/n^{2})$ | Eq. (3.1) |
| `series_limit_wavelength(n_lo, Z, R)` | $\lambda=n_o^{2}/(RZ^{2})$, the $n\to\infty$ edge | §3.1.4 |
| `series_name(n_lo)` | Lyman / Balmer / Paschen / Brackett / Pfund | Table 3.1 |
| `reduced_mass(m1, m2)` | $\mu=m_1m_2/(m_1+m_2)$ | p. 60 |
| `reduced_mass_ratio(nuclear_mass)` | $\mu_e/m_e$ — the factor taking $R_\infty\to R_H$ | p. 60 |
| `rydberg_constant(nuclear_mass)` | $R_\infty$, or the finite-mass $R_H$ | Eq. (3.7) |
| `fine_structure_constant()` | $\alpha=e^{2}/(2\epsilon_0 hc)=v_1/c\approx1/137$ | p. 60 |
| `is_nonrelativistic(n, Z)` | is $v_n/c$ small enough for classical mechanics? | p. 60 |

Module constants `R_INF`, `R_H`, `BOHR_RADIUS`, `HARTREE_EV` and the CODATA-2002
values (`C`, `E_CHARGE`, `M_E`, `M_P`, `H_PLANCK`, `EPS0`) are exactly those
tabulated in `../data_tables/A1_physical_constants.csv`.

## Use
```python
from atomic_models import (bohr_radius, bohr_energy, ionization_energy,
                           transition_wavelength, series_limit_wavelength,
                           reduced_mass_ratio, M_P)

bohr_radius(1)                            # 5.2918e-11  the Bohr radius, in m
bohr_energy(1)                            # -13.6057    eV, hydrogen ground state
bohr_energy(1, Z=2)                       # -54.42      He+ scales as Z^2
ionization_energy(2)                      # 54.42       eV  (Example 3.1)
transition_wavelength(2, 3, nuclear_mass=M_P) * 1e9   # 656.47 nm, Balmer alpha
series_limit_wavelength(1) * 1e9          # 91.18 nm    the Lyman edge
reduced_mass_ratio()                      # 0.999455679
```

## Run
```bash
cd code
python3 atomic_models.py        # demo: orbits, the three series, the Thomson failure
python3 test_atomic_models.py   # tests  ->  "All 18 tests passed."
cd ../figures && python3 make_figures.py
```

## Files
- `notes.md` — why the plum-pudding atom failed → Bohr's postulates → orbits →
  energy levels and the virial theorem → the Rydberg formula recovered → the
  reduced-mass correction (and a misprint in the book) → what survives, with a
  "Where this goes" map.
- `code/atomic_models.py`, `code/test_atomic_models.py` (numpy + stdlib only,
  self-contained). Tests check the book's printed values *and* the model's
  internal identities: force balance, quantized $L$, the virial theorem
  $T=-E$, $V=2E$, and $E\lambda=hc$.
- `problems/problems.md` — 8 worked problems with numeric `*Check:*` lines
  against the code.
- `figures/` — the hydrogen level diagram with the emission series, and the
  Thomson-vs-Rutherford scattering discrepancy on a log scale.
- `refs.md` — page-verified citations to S&F §3.1, plus the reduced-mass erratum.
