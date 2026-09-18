# NE-02 — Nuclear models

Second module of the **NUCLEAR SCIENCE & ENGINEERING** trunk (see
`modules/NE/list_NE.txt`). Covers **§3.2, "Models of the Nucleus"** (printed
pp. 63–78) of Shultis & Faw, 3rd ed.: nuclear size, the liquid drop model and
its semi-empirical mass formula, the line of stability, mass parabolas, and the
shell-model magic numbers.

- **Prerequisites:** `~NE-01` (the nuclear atom), `~QM-14` (independent-particle
  models and shell filling), `~EM-06` (electrostatic energy of a charged sphere —
  the Coulomb term). Helpful: `~SM-01` (why an even/odd pairing energy shows up
  as a two-branch systematics).
- **Cross-links:** `~NE-03` (binding energy and the $B/A$ curve, made quantitative
  from measured masses), `~NE-04` (Q-values are mass differences of this kind),
  `~NE-05` and `~NE-07` (mass parabolas decide decay direction and chain
  termination), `~NE-09` (the surface-vs-Coulomb competition *is* the fission
  barrier; $Z^{2}/A$ is the fissionability parameter), `~NE-10` (the $B/A$ peak
  is why fusion releases energy), `~NE-19` (magic nuclides have low absorption
  cross sections — reactor materials).

## Scope
Electron scattering shows nuclear matter has **constant density**: $R=1.1A^{1/3}$
fm, so $A/V=0.179$ nucleons/fm³ for every nuclide, and the nuclear force must
*saturate*. That justifies treating the nucleus as an incompressible drop whose
binding energy is a bulk term minus four corrections
$$BE=a_vA-a_sA^{2/3}-a_c\frac{Z^{2}}{A^{1/3}}-a_a\frac{(A-2Z)^{2}}{A}-\frac{a_p}{\sqrt A},$$
with $a_v=15.835$, $a_s=18.33$, $a_c=0.714$, $a_a=23.20$ MeV and
$a_p=\pm11.2$ MeV (positive odd-odd, negative even-even). Minimising the mass over
$Z$ at fixed $A$ gives the **line of stability**
$$Z(A)=\frac{A}{2}\frac{1+(m_n-m_p)c^{2}/4a_a}{1+a_cA^{2/3}/4a_a},$$
which bends neutron-rich as Coulomb repulsion grows ($N/Z$ from 1.00 at $A=20$ to
1.56 at $A=238$). Across an isobar the pairing term splits the masses into two
parabolas — even-even below, odd-odd above — which is why odd-$A$ isobars
typically have one stable nuclide and even-$A$ isobars two. What the model cannot
produce is the extra binding at $Z$ or $N=2,8,20,28,50,82,126$; those residuals
(up to +11.7 MeV at ²⁰⁸Pb) are the shell effect.

## Operations — `code/nuclear_models.py`

| call | meaning | reference |
|------|---------|-----------|
| `nuclear_radius(A)` | $R=1.1A^{1/3}$ fm | Eq. (3.13) |
| `nuclear_volume(A)`, `nucleon_number_density(A)` | $\tfrac43\pi R^{3}$; $A/V=0.179$ fm⁻³ for all $A$ | §3.2.1 |
| `parity_class(A, Z)` | `even-even` / `odd-odd` / `odd-even` | §3.2.5 |
| `pairing_sign(A, Z)`, `pairing_term(A, Z)` | $a_p/A_P\in\{+1,0,-1\}$; the term $-a_p/\sqrt A$ | Eq. (3.16) |
| `semf_terms(A, Z)` | the five contributions separately, MeV | Eq. (3.16) |
| `semf_binding_energy(A, Z)` | total $BE$, MeV | Eq. (3.16) |
| `semf_binding_energy_per_nucleon(A, Z)` | $BE/A$ — the curve peaking near iron | §3.2.5 |
| `semf_nuclear_mass_u(A, Z)` | $Zm_p+(A-Z)m_n-BE/c^{2}$ | Eq. (3.16) |
| `semf_atomic_mass_u(A, Z)` | $ZM(^1\mathrm{H})+(A-Z)m_n-BE/c^{2}$ | pp. 73–74 |
| `semf_mass_excess_mev(A, Z)` | $(M-A)c^{2}$ | §3.2.5 |
| `most_stable_Z(A)`, `most_stable_Z_rounded(A)` | the line of stability | Eq. (3.18) |
| `isobar_masses(A, z_lo, z_hi)` | $(Z,M)$ across an isobar — a mass parabola | §3.2.6 |
| `is_magic(n)`, `is_doubly_magic(A, Z)`, `magic_gap(A, Z)` | 2, 8, 20, 28, 50, 82, 126 | §3.2.7 |
| `load_atomic_masses()` | `{(Z,A): mass_u}` from Appendix B | App. B |
| `measured_binding_energy(A, Z)` | $BE$ from the **measured** mass | App. B |

## Use
```python
from nuclear_models import (semf_binding_energy_per_nucleon, measured_binding_energy,
                            most_stable_Z, semf_terms, is_doubly_magic)

semf_binding_energy_per_nucleon(56, 26)      # 8.699 MeV/nucleon (measured 8.790)
measured_binding_energy(208, 82)             # 1636.45 MeV
most_stable_Z(238)                           # 93.14 -> heavy nuclides are neutron rich
semf_terms(208, 82)["coulomb"]               # -810.29 MeV, the term that limits heavy nuclei
is_doubly_magic(208, 82)                     # True  (Z=82, N=126)
measured_binding_energy(208, 82) - semf_binding_energy(208, 82)   # +11.70 MeV shell surplus
```

## Run
```bash
cd code
python3 nuclear_models.py        # demo: density, SEMF vs measured, stability line, A=110 isobar
python3 test_nuclear_models.py   # tests  ->  "All 19 tests passed."
cd ../figures && python3 make_figures.py
```

Needs `../../data_tables/B1_atomic_masses.csv` (already extracted; see that
directory's README) for everything that compares against measured masses.

## Files
- `notes.md` — constant nuclear density and saturation → the five SEMF terms and
  the pairing sign trap → how well it works against Appendix B → the line of
  stability → mass parabolas and the A=110 isobar → magic numbers as the model's
  failure mode, with a "Where this goes" map.
- `code/nuclear_models.py`, `code/test_nuclear_models.py` (numpy + stdlib only).
  Tests check the book's formulas *and* validate the model against 150+ measured
  masses, confirming better than 0.25 MeV/nucleon for $A\ge40$ and a positive
  shell surplus at every doubly magic nuclide.
- `problems/problems.md` — 8 worked problems (S&F Ch. 3 problems 6, 7, 9, 10 plus
  four added) with numeric `*Check:*` lines.
- `figures/` — the $B/A$ curve against measured data, the SEMF term breakdown,
  the chart of the nuclides with the stability line, and the A=110 mass parabolas.
- `refs.md` — page-verified citations to S&F §3.2.
