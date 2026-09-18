# NE-03 — References

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
| Notation $M({}^A_Z X)$ atomic vs $m({}^A_Z X)$ nuclear; Appendix B holds **atomic** masses | §4.1.1 | 80–81 | 103–104 |
| Atomic–nuclear mass relation $M = m + Zm_e - BE_{Ze}/c^2$ (`atomic_to_nuclear_mass`) | Eq. (4.8) | 81 | 104 |
| 13.6 eV = $1.4\times10^{-8}$ u, so electron binding is negligible (`electron_binding_fraction`) | §4.1.1 | 81 | 104 |
| Formation reaction and the mass defect (`mass_defect_u`) | Eqs. (4.9), (4.10) | 81 | 104 |
| Derivation in atomic masses; the $[ZBE_{1e}-BE_{Ze}]$ term and why it is dropped | Eq. (4.11) | 81 | 104 |
| **Binding energy from atomic masses** (`binding_energy`) | Eq. (4.12) | 81 | 104 |
| Average binding energy per nucleon; the $B/A$ curve (`binding_energy_per_nucleon`, `binding_energy_curve`) | §4.1.3 | 82–85 | 105–108 |
| Binding energies of isotopes | §4.2 | 85–87 | 108–110 |
| Nucleon separation energy, mass form (`neutron_separation_energy`) | Eq. (4.13) | 87 | 110 |
| Separation energy as a difference of binding energies | Eq. (4.14) | 87 | 110 |
| Proton separation energy $S_p = BE({}^A_Z Y) - BE({}^{A-1}_{Z-1}X)$ (`proton_separation_energy`) | Eq. (4.15) | 87 | 110 |
| Even $N$ or $Z$ gives high $S_n$/$S_p$ — pairing read straight off the data (`pairing_stagger`) | §4.3 | 87 | 110 |
| **Example 4.3** — $S_n({}^{16}\mathrm{O}) = 15.66$ MeV, "exceptionally high" | Ex. 4.3 | 87 | 110 |
| Physical constants ($m_n$, $m_e$, u in MeV) | Table A.1 | 555 | 578 |
| Measured atomic masses (Audi–Wapstra 1995) (`load_atomic_masses`) | App. B | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 4)
Chapter 4's problem set begins on printed **94** (PDF 117); problems 1–4 are on
that page and 5 onward on printed 95 (PDF 118). The ones belonging to this module:

- **Prob. 2** — rest-mass energy equivalent of 1 u in MeV, straight from $E=mc^2$ — printed 94, PDF 117.
- **Prob. 3** — binding energy per nucleon for $^{16}$O, $^{17}$O, $^{56}$Fe and $^{235}$U — printed 94, PDF 117.
- **Prob. 4** — binding energy per nucleon *and* neutron separation energy for $^{16}$O and $^{17}$O — printed 94, PDF 117.
- **Prob. 6** — binding energy and $B/A$ for $^{56}$Fe and $^{235}$U, and their significance — printed 95, PDF 118.
- **Prob. 7** — estimate the electron binding energy in $^1$H from the proton and hydrogen masses (both known to 10 figures) and compare with the Bohr model — printed 95, PDF 118.
- **Prob. 8** — binding energy of $^3$He and its neutron separation energy — printed 95, PDF 118.
- **Prob. 9** — verify Eq. (4.15), the proton separation energy, from the definition of $BE$ — printed 95, PDF 118.
- **Prob. 10** — for $^{56}$Fe: remove one neutron, remove one proton, dismantle it completely, and fission it symmetrically into two $^{28}$Al — printed 95, PDF 118.

Problems 1 and 5 concern reactions and Q-values and belong to `~NE-04`.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Book-internal inconsistency found while building this module

**The neutron mass appears twice, with two values.** Table A.1 (printed p. 555)
gives $m_n = 1.008\,664\,915\,6$ u, while Appendix B (printed p. 570) lists the
free neutron at $1.008\,664\,923\,3$ u. The difference,
$7.7\times10^{-9}$ u $= 7.2$ eV, is irrelevant beside MeV-scale binding energies,
but it is not zero: computing `binding_energy(1, 0)` — the binding energy of a
lone neutron, which must be identically zero — returns $-7.2\times10^{-6}$ MeV
instead. The Table A.1 value is the CODATA-2002 one and matches the modern
recommended $1.008\,664\,915\,95$ u; Appendix B carries the older Audi–Wapstra
1995 evaluation throughout. This module uses Table A.1 for $m_n$ and $M(^1$H$)$
and Appendix B for everything else, which is the same convention the book's own
worked examples use. `test_free_nucleons_have_zero_binding_energy` measures the
residual rather than hiding it.

(Other errata found in this trunk: two Table A.4 abundances and the Appendix B
transactinide symbols — see `../data_tables/README.md`; the reduced-mass ratio on
p. 60 — see `../NE-01_atomic_models/refs.md`.)

## Cross-module dependencies
- **`~NE-01`** — the eV-vs-MeV scale separation that licenses dropping electron
  binding energies.
- **`~NE-02`** — the liquid drop model these measured values test; the pairing
  term is what the $S_n$ stagger of §5 measures directly.
- **`../data_tables/`** — `B1_atomic_masses.csv` (all masses used here) and
  `C1_thermal_neutron_cross_sections.csv` (the low capture cross sections of
  magic nuclides, the same shell effect seen in $S_n$).

## Further reading
- Krane, *Introductory Nuclear Physics*, §3.2 — separation energies and the
  odd–even stagger, with more isotope chains than S&F show.
- Audi & Wapstra, *Nuclear Physics* **A595** (1995) 409 — the mass evaluation
  Appendix B reproduces.
