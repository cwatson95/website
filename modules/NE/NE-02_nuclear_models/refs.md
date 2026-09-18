# NE-02 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Fundamental properties of the nucleus; electron scattering and muonic x-rays | §3.2.1 | 63–64 | 86–87 |
| Proton and nucleon density, Fermi/Woods–Saxon profile $\rho_o/[1+e^{(r-R)/a}]$ | Eqs. (3.8), (3.11) | 63–64 | 86–87 |
| Density parameters $R$, $a$, $\rho_o$ for three nuclei; $R/A^{1/3}$ constant | Table 3.2 | 64 | 87 |
| Nuclear radius $R=1.1A^{1/3}\times10^{-15}$ m (`nuclear_radius`, `nucleon_number_density`) | Eq. (3.13) | 64 | 87 |
| Proton–electron model and why it fails (confinement energy) | §3.2.2 | 65 | 88 |
| Proton–neutron model | §3.2.3 | 66 | 89 |
| Stability of nuclei; number of stable isotopes vs $Z$ and vs $N$ (even/odd systematics) | §3.2.4, Figs. 3.11–3.12 | 68–71 | 91–94 |
| Liquid drop model; saturation and the incompressible-drop analogy | §3.2.5 | 70–71 | 93–94 |
| Naive mass sum $m=Zm_p+(A-Z)m_n$ | Eq. (3.15) | 71 | 94 |
| The four binding-energy corrections — surface, Coulomb, asymmetry, pairing (`semf_terms`) | §3.2.5 | 72 | 95 |
| Semi-empirical mass formula (`semf_binding_energy`, `semf_nuclear_mass_u`) | Eq. (3.16) | 73 | 96 |
| Constants $a_v=15.835$, $a_s=18.33$, $a_c=0.714$, $a_a=23.20$, $a_p=\pm11.2$ MeV [Wapstra 1958] | §3.2.5 | 73 | 96 |
| Stationarity condition $\partial m/\partial Z=0$ | Eq. (3.17) | 73 | 96 |
| Line of stability $Z(A)$ (`most_stable_Z`) | Eq. (3.18) | 73 | 96 |
| Atomic-mass form $M=ZM(^1\mathrm{H})+(A-Z)m_n-BE/c^2$ (`semf_atomic_mass_u`) | §3.2.5 | 73–74 | 96–97 |
| Mass parabolas; the $A=110$ isobar, two curves for even-even and odd-odd (`isobar_masses`) | §3.2.6, Fig. 3.13 | 74–75 | 97–98 |
| Magic numbers 2, 8, 20, 28, 50, 82, 126 (`is_magic`, `is_doubly_magic`) | §3.2.7 | 75 | 98 |
| The nuclear shell model; spin–orbit coupling | §3.2.7 | 75–76 | 98–99 |
| Other nuclear models (collective, optical) | §3.2.8 | 76 | 99 |
| Measured atomic masses (Audi–Wapstra 1995) (`load_atomic_masses`, `measured_binding_energy`) | App. B | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 3)
The Chapter 3 problem set begins on printed **77** (PDF 100); problems 1–9 are on
that page and 10 onward on printed 78. The ones belonging to this module:

- **Prob. 6** — using the nucleon distribution of Eq. (3.11), the fractional density drop between $r=R-2a$ and $r=R+2a$ — printed 77, PDF 100.
- **Prob. 7** — tabulate the liquid-drop binding energy and all its contributions for ⁴⁰Ca and ²⁰⁸Pb — printed 77, PDF 100.
- **Prob. 9** — plot each per-nucleon contribution (volume, surface, asymmetry, Coulomb) and the total $B/A$ against $A$, taking $Z$ from Eq. (3.18) — printed 77, PDF 100.
- **Prob. 10** — using Appendix B masses, plot $[70-{}^{A}_{Z}\mathrm{X}]$ against $Z$ for the $A=70$ isobar chain (⁷⁰Kr, ⁷⁰Br, …) — printed 78, PDF 101.

Problems 1–5 and 8 concern the atom and belong to `~NE-01`.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A note on the pairing sign
S&F Eq. (3.16) writes the pairing contribution as $-a_p/\sqrt A$ with $a_p$
**positive for odd-$N$/odd-$Z$** and **negative for even-$N$/even-$Z$**
(printed p. 73). The net effect is therefore $+11.2/\sqrt A$ MeV of *extra*
binding for even-even nuclei. Several other texts define $\delta$ with the
opposite sign and add it, so the constants are not portable between books
without checking. `pairing_sign` and `test_pairing_helps_even_even_and_hurts_odd_odd`
fix the convention used here; the observable consequence is that the even-even
mass parabola of an isobar lies *below* the odd-odd one, which is what S&F's
Fig. 3.13 shows.

## Cross-module dependencies
- **`~NE-01`** — the nuclear atom; the eV-vs-MeV scale separation that lets the
  electron binding energy be dropped when converting nuclear to atomic masses.
- **`~QM-14`** — independent-particle models, the basis of the shell model.
- **`../data_tables/`** — `B1_atomic_masses.csv` (measured masses, Appendix B) and
  `C1_thermal_neutron_cross_sections.csv` (the low absorption cross sections of
  magic nuclides).

## Further reading
- Krane, *Introductory Nuclear Physics*, Ch. 3 (nuclear properties) and Ch. 5
  (the shell model, including the spin–orbit term S&F only mentions).
- Wapstra, A.H., *Handbuch der Physik* 38/1 (1958) — the source of the
  liquid-drop constants used here.
- Bohr & Wheeler (1939) — the liquid drop model applied to fission, picked up in
  `~NE-09`.
