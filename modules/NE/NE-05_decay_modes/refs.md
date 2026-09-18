# NE-05 — References

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
| Overview of radioactivity; types of decay | §§5.1–5.2 | 97–98 | 120–121 |
| Radioactive decay diagrams | §5.3 | 98–102 | 121–125 |
| Gamma decay / isomeric transition (`q_isomeric_transition`) | §5.4.1 | 102 | 125 |
| Alpha decay reaction, daughter ion picking up electrons | Eq. (5.6) | 103 | 126 |
| **$Q_\alpha$ from atomic masses** (`q_alpha`) | Eq. (5.7) | 103 | 126 |
| Energy and momentum conservation for the two-body split | Eqs. (5.8)–(5.10) | 104 | 127 |
| **Alpha kinetic energy** $E_\alpha = Q\,M_D/(M_D+M_\alpha)$ (`alpha_kinetic_energy`) | Eq. (5.11) | 104 | 127 |
| Daughter recoil energy (`daughter_recoil_energy`) | Eq. (5.12) | 104 | 127 |
| Beta-minus decay reaction | Eq. (5.13) | 105 | 128 |
| **$Q_{\beta^-}$ — atomic masses cancel exactly** (`q_beta_minus`) | Eq. (5.14) | 105 | 128 |
| $Q_{\beta^-}$ with an excited daughter | Eq. (5.15) | 106 | 129 |
| Beta spectrum endpoint $(E_{\beta^-})_{\max}=Q$ (`beta_endpoint`) | Eq. (5.16) | 106 | 129 |
| Positron decay reaction | Eq. (5.17) | 107 | 130 |
| **$Q_{\beta^+}$ — the $2m_ec^2$ penalty** (`q_beta_plus`, `TWO_ME_MEV`) | Eq. (5.18) | 107 | 130 |
| $Q_{\beta^+}$ with an excited daughter | Eq. (5.19) | 108 | 131 |
| Electron capture reaction | Eq. (5.21) | 109 | 132 |
| **$Q_{\mathrm{EC}}$ — same form as $\beta^-$** (`q_electron_capture`) | Eq. (5.22) | 109 | 132 |
| $Q_{\mathrm{EC}}$ with an excited daughter | Eq. (5.23) | 109 | 132 |
| Neutron decay (`q_neutron_emission`) | §5.4.6 | 110 | 133 |
| Proton decay (`q_proton_emission`) | §5.4.7 | 110 | 133 |
| Internal conversion | §5.4.8 | 111 | 134 |
| Radioactive decay data — the source of Appendix D | §5.9 | 131 | 154 |
| Measured atomic masses (`load_atomic_masses`) | App. B | 570–587 | 593–610 |
| Measured emission energies (`load_decay_radiation`, `measured_emissions`) | App. D | 596–624 | 619–647 |

## Problems (verified, S&F 3rd ed. Ch. 5)
Chapter 5's problem set begins on printed **132** (PDF 155).

- **Prob. 1** — identify the decay type and the unknown species in seven reactions, and give the total kinetic energy of the products: $^{210}$Po$\to(?)+\alpha$; $^{38}$S$\to(?)+e^-+\bar\nu$; $(?)\to{}^{27}$Al$+e^++\nu$; $^{145}$Sm$\to{}^{145}$Pm$+(?)$; $^{137}$Xe$^*\to(?)+n$ ($E^*=6.71$ MeV); $^{108}$Te$\to{}^{107}$Sb$+(?)$ ($E^*=3.4$ MeV); $^{60}$Ni$^*\to(?)+e^-$ ($E^*=0.125$ MeV, $BE_e^K=8.33$ keV) — printed 132, PDF 155.
- **Prob. 2** — gamma recoil: show $E_\gamma<E^*$, derive $E_\gamma = m_nc^2[\sqrt{1+2E^*/m_nc^2}-1]\simeq E^*(1-E^*/2m_nc^2)$, and verify with an example that the difference is negligible — printed 132, PDF 155.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## A disagreement between Appendix B and Appendix D

For most nuclides the two appendices close to a fraction of a keV: computing
$Q_{\beta^-}$ from Appendix B masses reproduces the Appendix D beta endpoint for
$^3$H, $^{14}$C, $^{32}$P and $^{90}$Sr to better than 0.3 keV, and for $^{60}$Co
the endpoint plus the two-gamma cascade closes on $Q$ to 0.3 keV out of 2824.

$^{137}$Cs is the exception. Appendix D's endpoints (511.5 keV feeding the 661.66
keV level, and 1173.2 keV to the ground state) are internally consistent and imply
a total decay energy of **1173.2 keV**, while Appendix B's masses give
**1176.5 keV** — a gap of 3.3 keV, or 0.3%. The modern evaluated value is
1175.6 keV, between the two. Appendix B carries Audi–Wapstra 1995 masses and
Appendix D carries MIRD/ICRP-era decay data, so the two are simply different
vintages. `test_cesium137_shows_a_small_appendix_disagreement` asserts the size
of the gap so that it stays visible.

## Cross-module dependencies
- **`~NE-04`** — Q-values in general, and the neutral-atom substitution rule that
  this module has to modify mode by mode.
- **`~NE-02`** — the mass parabolas that decide *which* mode a nuclide takes; the
  even-$A$ two-branch structure is why $^{40}$K decays both ways.
- **`~NE-03`** — $Q_\alpha=-S_\alpha$, and the barrier argument for why
  energetic instability is not observed instability.
- **`../data_tables/`** — `B1_atomic_masses.csv` and `D1_decay_radiation.csv`.

## Further reading
- Krane, *Introductory Nuclear Physics*, Chs. 8–10 — alpha, beta and gamma decay
  in depth, including Gamow's barrier-penetration theory and the beta selection
  rules S&F only gestures at.
- ICRP Publication 38, *Radionuclide Transformations* — one of the sources behind
  Appendix D.
