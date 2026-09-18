# NE-01 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | solutions numbered by chapter/problem |

Offset verified at both ends of the book: printed 54 (the Chapter 3 opening) is
PDF 77; printed 555 (Appendix A) is PDF 578.

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Discovery of radioactivity; Becquerel and the Curies | §3.1.1 | 54–57 | 77–80 |
| Thomson's plum-pudding model | §3.1.2 | 57 | 80 |
| Geiger–Marsden; $P(\ge\phi)=e^{-\phi/\phi_m}$, $\phi_m\simeq1^\circ$; 1 alpha in 8000 past $90^\circ$; nucleus within $10^{-12}$ cm (`thomson_scattering_probability`) | §3.1.3 | 58 | 81 |
| Empirical Rydberg formula $1/\lambda = R_H(1/n_o^2-1/n^2)$, $R_H=10\,967\,758$ m$^{-1}$ (`rydberg_wavelength`) | Eq. (3.1) | 58 | 81 |
| Hydrogen spectral series — Lyman, Balmer, Paschen, Brackett, Pfund (`series_name`, `SERIES_NAMES`) | Table 3.1 | 59 | 82 |
| Bohr's three postulates | §3.1.4 | 59 | 82 |
| Force balance $m_ev^2/r = Ze^2/4\pi\epsilon_0r^2$ (`test_coulomb_balances_centripetal_force`) | Eq. (3.2) | 59 | 82 |
| Angular-momentum quantization $L=m_evr=nh/2\pi$ (`bohr_angular_momentum`) | Eq. (3.3) | 59 | 82 |
| Orbit radius and speed $r_n$, $v_n$ (`bohr_radius`, `bohr_velocity`) | Eq. (3.4) | 59 | 82 |
| $r_1=5.293\times10^{-11}$ m, $v_1=2.187\times10^6$ m/s; $v_1\ll c$ justifies non-relativistic mechanics (`fine_structure_constant`, `is_nonrelativistic`) | §3.1.4 | 60 | 83 |
| Energy levels $E_n=-m_e(Ze^2)^2/8\epsilon_0^2n^2h^2$; $E_1=-13.606$ eV (`bohr_energy`, `ionization_energy`) | Eq. (3.5) | 60 | 83 |
| Transition energy $h\nu = E_n-E_{n_o}$ (`transition_energy`) | Eq. (3.6) | 60 | 83 |
| Emission wavelength and $R_\infty$ (`transition_wavelength`, `rydberg_constant`) | Eq. (3.7) | 60 | 83 |
| Reduced mass $\mu_e=m_em_p/(m_e+m_p)$; $R_H=\mu_ee^4/8\epsilon_0^2ch^3$ (`reduced_mass`, `reduced_mass_ratio`) | §3.1.4 | 60 | 83 |
| Example 3.1 — ionization energy of He⁺ (54.4 eV) | Ex. 3.1 | 60–61 | 83–84 |
| Sommerfeld elliptic orbits | §3.1.5 | 61 | 84 |
| The quantum-mechanical atom | §3.1.6 | 62 | 85 |
| Physical constants used throughout (CODATA 2002) | Table A.1 | 555 | 578 |

## Problems (verified, S&F 3rd ed. Ch. 3)
Chapter 3's problem set begins on printed **77** (PDF 100); problems 1–9 are on
that page, 10 onward on printed 78. The ones belonging to this module:

- **Prob. 1** — wavelengths of the first three Lyman lines, and their photon energies — printed 77, PDF 100.
- **Prob. 2** — the first Bohr orbit: (a) radius, (b) total energy, (c) ionization energy — printed 77, PDF 100.
- **Prob. 3** — photon energy to excite hydrogen from the ground state to the first excited orbit — printed 77, PDF 100.
- **Prob. 4** — de Broglie wavelength of the $n=1$ electron compared with the orbit circumference (the standing-wave reading of postulate 2) — printed 77, PDF 100.
- **Prob. 5** — limiting (smallest) wavelengths of the Lyman, Balmer and Paschen series — printed 77, PDF 100.
- **Prob. 8** — the hydrogen atom's mass defect (Appendix B) against the Bohr ionization energy — printed 77, PDF 100.

Problems 6, 7, 9 and 10 concern the nucleus and belong to `~NE-02`.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Erratum found while building this module

**S&F printed p. 60 — the reduced-mass ratio.** The text states
$\mu_e = 0.999445568\,m_e$. That value gives
$$R_H=\frac{\mu_e}{m_e}R_\infty = 0.999445568\times1.0973732\times10^{7}
= 1.0967647\times10^{7}\ \mathrm{m^{-1}},$$
which disagrees with the $R_H = 10\,967\,758$ m$^{-1}$ printed two lines later —
and the book claims eight-significant-figure agreement with experiment. Using
the constants of its own Table A.1,
$$\frac{\mu_e}{m_e}=\frac{m_p}{m_e+m_p}=0.999455679
\;\Longrightarrow\; R_H = 1.0967758\times10^{7}\ \mathrm{m^{-1}},$$
which reproduces the printed $R_H$ exactly. The printed ratio appears to have a
stray digit. `test_reduced_mass_ratio_reproduces_book_R_H` asserts both the
correct value and the failure of the printed one.

(A second class of book errata — two isotopic abundances in Table A.4 — is
recorded in `../data_tables/README.md`.)

## Cross-module dependencies
- **`~QM-03`, `~QM-08`** — the old quantum theory and the orbital picture that
  supersedes Bohr's orbits.
- **`~EM-06`** — Coulomb's law and $V=-Ze^2/4\pi\epsilon_0 r$, used in §3 of the notes.
- **`~NE-12`** — photoelectric absorption edges are the inner-shell ionization
  energies this module computes; the edge structure is visible in
  `../data_tables/C3_photon_coefficients_lead.csv`.

## Further reading
- Krane, *Introductory Nuclear Physics*, Ch. 2 — a fuller treatment of Rutherford
  scattering, including the differential cross section S&F only alludes to.
- Kaplan, *Nuclear Physics*, 2nd ed. (1963) — the source S&F cites for the
  reduced-mass correction and for Fig. 3.4.
