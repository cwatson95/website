# NE-11 — References

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
| Attenuation of neutral particle beams | §7.1 | 179 | 202 |
| **Linear interaction coefficient** $\mu_i\equiv\lim P_i(\Delta x)/\Delta x$ | §7.1.1, Eq. (7.1) | 180 | 203 |
| Channels add: $\mu_t=\sum_i\mu_i$ | Eq. (7.2) | 180 | 203 |
| Attenuation of uncollided radiation; $dI^o/dx=-\mu_tI^o$ | §7.1.2, Eq. (7.3) | 181 | 204 |
| **$I^o(x)=I^o(0)e^{-\mu_tx}$** (`uncollided_intensity`) | Eq. (7.4) | 181 | 204 |
| $P(x)=1-e^{-\mu x}$ (`interaction_probability`) | Eq. (7.5) | 181 | 204 |
| $\bar P(x)=e^{-\mu x}$ (`survival_probability`) | Eq. (7.6) | 181 | 204 |
| Average travel distance; $p(x)=\mu e^{-\mu x}$ (`path_length_pdf`) | §7.1.3, Eq. (7.7) | 181–182 | 204–205 |
| **Mean free path** $\bar x=1/\mu$ (`mean_free_path`) | Eq. (7.8) | 182 | 205 |
| **Half-thickness** $x_{1/2}=\ln2/\mu$ (`half_thickness`) | §7.1.4, Eq. (7.9) | 182 | 205 |
| **Example 7.1** — tenth-thickness in water and lead (`tenth_thickness`) | Example 7.1 | 182 | 205 |
| Scattered radiation; the **buildup factor** $I=BI^o$ (`buildup_intensity`) | §7.1.5 | 183 | 206 |
| Microscopic cross sections; the barn | §7.1.6 | 183–184 | 206–207 |
| **$\mu_i=\sigma_iN=\sigma_i\rho N_a/A$** (`macroscopic_cross_section`, `atom_density`) | Eq. (7.10) | 183 | 206 |
| **Mass coefficient** $\mu_i/\rho=(N_a/A)\sigma_i$ (`mass_coefficient`) | Eq. (7.11) | 184 | 207 |
| Mixtures by volume, $\mu_i=\sum_jN^j\sigma_i^j$ (`compound_macroscopic`) | Eq. (7.12) | 184 | 207 |
| Mixtures by weight, $\mu/\rho=\sum_jw_j(\mu/\rho)_j$ (`mixture_mass_coefficient`) | Eq. (7.13) | 184 | 207 |
| **Example 7.2** — a 50/50 iron-lead mixture (`mixture_density`) | Example 7.2 | 184 | 207 |
| **Example 7.3** — thermal-neutron absorption in water (`absorption_cross_section`) | Example 7.3 | 184–185 | 207–208 |
| Calculation of radiation interaction rates | §7.2 | 185 | 208 |
| **Flux density** $\phi\equiv vn$ (`flux_density`) | §7.2.1, Eq. (7.14) | 186 | 209 |
| **Reaction-rate density** $\hat R_i=\mu_i\phi$ (`reaction_rate_density`) | §7.2.2, Eq. (7.15) | 186 | 209 |
| $\hat R_i=\Sigma_i\phi$ for neutrons | Eq. (7.16) | 186 | 209 |
| Energy- and time-dependent flux density | §7.2.3, Eqs. (7.17)–(7.18) | 187 | 210 |
| Fissions in a volume over an interval | Eq. (7.19) | 187 | 210 |
| **Fluence** $\Phi=\int\phi\,dt$ (`fluence`) | §7.2.4, Eqs. (7.20)–(7.22) | 187–188 | 210–211 |
| Uncollided flux from an isotropic point source | §7.2.5 | 188 | 211 |
| **Point source in vacuum**, $S_p/4\pi r^2$ (`point_source_flux`) | Eq. (7.23) | 188 | 211 |
| Detector response $R^o=\mu_d\Delta V_dS_p/4\pi r^2$ | Eq. (7.24) | 189 | 212 |
| Point source in an attenuating medium | Eq. (7.25) | 189 | 212 |
| **Point source behind a shield** (`point_source_flux_shielded`) | Eq. (7.26) | 189 | 212 |
| **Layered shields**, $\exp(-\sum_i\mu_it_i)$ (`point_source_flux_layered`) | Eq. (7.27) | 190 | 213 |
| Heterogeneous media; the optical path $\ell=\int\mu\,ds$ | Eqs. (7.28)–(7.31) | 190 | 213 |
| Thermal-neutron cross sections (`load_thermal_cross_sections`) | Table C.1 | 588 | 611 |
| Photon mass coefficients (`load_photon_coefficients`) | Table C.3 | 591–595 | 614–618 |

## Problems (verified, S&F 3rd ed. Ch. 7)
Chapter 7's problem set begins on printed **218** (PDF 241). Problems **1–13**
belong to this module; **14–15** are photon interactions (`~NE-12`), **16** is
neutron interactions (`~NE-13`) and **17–21** are charged-particle stopping
(`~NE-14`).

- **Prob. 1** — inferring $\mu_t$ from a 6 cm transmission measurement — printed 218, PDF 241.
- **Prob. 2** — half-thickness for 1 MeV photons in water, iron, lead — printed 218, PDF 241.
- **Prob. 3** — tenth-thickness vs energy, 0.1–10 MeV, four materials — printed 218, PDF 241.
- **Prob. 4** — working back from a 2.6 cm tenth-thickness — printed 218, PDF 241.
- **Probs. 5–6** — first-interaction probabilities in two and then $N$ slabs — printed 218, PDF 241.
- **Prob. 7** — derive Eq. (7.8) — printed 218, PDF 241.
- **Prob. 8** — natural uranium: $\Sigma_t$ and $\Sigma_f$ — printed 218, PDF 241.
- **Prob. 9** — linear coefficients in air (data supplied in the problem) — printed 219, PDF 242.
- **Prob. 10** — mean free path of a thermal neutron in graphite — printed 219, PDF 242.
- **Prob. 11** — particle density from flux density, photons vs neutrons — printed 219, PDF 242.
- **Probs. 12–13** — reaction rates in an irradiated sample — printed 219, PDF 242.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## An erratum in Example 7.2

**The iron density, printed 7.784 g/cm³, should be 7.874.** S&F's Example 7.2
(printed p. 184) writes

> $(1\ \text{g}/\rho_{\text{Fe}})+(1\ \text{g}/\rho_{\text{Pb}})=(1/7.784)+(1/11.35)=0.2151\ \text{cm}^3$

and then $\rho_{\text{mix}}=2/0.2151=9.298$ g/cm³. **The arithmetic does not
follow from the printed number.** With 7.784 the sum is 0.21657 cm³ and
$\rho_{\text{mix}}=9.235$; only $\rho_{\text{Fe}}=7.874$ gives the 0.2151 and
9.298 that the book prints two lines later.

7.874 g/cm³ is also the accepted density of iron at room temperature, so the
printed **7.784 is a digit transposition** and the rest of the example is right.
`MATERIALS["iron"]["density"]` therefore holds 7.874, the printed value is kept
in `DENSITY_ERRATA`, and `test_the_iron_density_typo` checks that the corrected
value reproduces both of the book's downstream numbers while the printed one
reproduces neither.

Consequence for the final answer: $\mu_{\text{mix}}=0.5929$ cm⁻¹ (book) rather
than 0.5889, a 0.7% difference — small, but the point of checking is that it was
found rather than assumed.

## Two conventions worth stating plainly

**"Absorption" means every removal channel, not just capture.** Appendix C.1
tabulates $(n,\gamma)$, $(n,\alpha)$, $(n,p)$, $(n,f)$ and scattering
separately. The absorption cross section $\sigma_a$ is the sum of the first four
— everything that consumes the neutron — and excludes scattering, which merely
changes its energy. Example 7.3 uses 0.239 b for ¹⁷O, which is
$(n,\alpha)\,0.235+(n,\gamma)\,0.0038$; taking the capture column alone would
understate ¹⁷O's absorption by a factor of 60. `absorption_cross_section` sums
the four channels and `ABSORPTION_CHANNELS` names them.

**Eq. (7.4) is a lower bound, not an answer.** It tracks *uncollided* particles.
S&F flag this in §7.1.5 and then leave buildup factors to tabulations, which is
reasonable for a textbook and dangerous in practice: for a metre of concrete
against MeV photons $B\sim10$, so a shield sized on exponential attenuation alone
is under-designed by an order of magnitude. `buildup_intensity` requires the
caller to supply $B$ and refuses $B<1$; it does not invent one. Problem P8 in
`problems/problems.md` closes on this point deliberately.

## Cross-module dependencies
- **`~NE-06`** — the decay constant $\lambda$, of which $\mu$ is the spatial
  analogue; every result in §1 of the notes is that correspondence.
- **`~NE-08`** — the elastic-scattering kinematics behind the neutron
  scattering cross sections used here, and the collision counts that make the
  graphite mean free path meaningful.
- **`~NE-09`** — $\Sigma_f\phi$ is reactor power; the ²³⁵U/²³⁸U cross-section
  contrast in P5 is why enrichment exists.
- **`../data_tables/`** — `C1_thermal_neutron_cross_sections.csv` (27 nuclides)
  and `C3_photon_coefficients_{air,water,concrete,iron,lead}.csv`.

## Further reading
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, §3.3–3.6 — the same
  material with more worked neutron examples.
- Berger, Hubbell et al., *XCOM: Photon Cross Sections Database*, NIST — the
  modern source behind Appendix C.3, tabulated to arbitrary energies and
  compositions.
- Chilton, Shultis & Faw, *Principles of Radiation Shielding* (1984) — buildup
  factors in full, the topic §7.1.5 defers.
- Bell & Glasstone, *Nuclear Reactor Theory* (1970), Ch. 1 — the transport
  equation from which $R=\mu\phi$ is the zeroth-order consequence.
