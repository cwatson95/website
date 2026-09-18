# NE-13 — References

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
| Neutron interactions; why photon intuition fails | §7.4 | 196 | 219 |
| "all cross-section data are empirical in nature" | §7.4 | 196 | 219 |
| ENDF evaluated data files | §7.4 | 196–198 | 219–221 |
| Classification of interaction types | §7.4.1 | 198 | 221 |
| **Table 7.1** — data required for shielding calculations | Table 7.1 | 198 | 221 |
| Light / intermediate / heavy categories (`classify_nuclide`, `NUCLIDE_CLASS`) | §7.4.1 | 199 | 222 |
| **$\sigma_t=\sigma_1+\sigma_2/\sqrt{E}$** (`light_nucleus_total_cross_section`) | Eq. (7.40) | 199 | 222 |
| Bragg cutoffs below ~0.01 eV | §7.4.1 | 199 | 222 |
| Resonance character by mass (`resonance_character`, `RESONANCE_CHARACTER`) | §7.4.1 | 199 | 222 |
| Only H and D have no resonances | §7.4.1 | 199 | 222 |
| Heavy nuclides: eV resonances, <1 eV wide, unresolved above a few keV | §7.4.1 | 199 | 222 |
| $(n,\gamma)$ "seldom exceeds 200 mb" over the fission spectrum | §7.4.1 | 199–200 | 222–223 |
| Total cross sections: Al, Fe, Pb, U | Figs. 7.6–7.9 | 200–203 | 223–226 |
| Elastic vs inelastic scattering above the first excited state | §7.4.1 | 199–204 | 222–227 |
| **$(n,2n)$ thresholds: ~8 MeV typical, D 3.3, Be 1.84** (`SECONDARY_NEUTRON_THRESHOLDS`) | §7.4.1 | 204 | 227 |
| $(n,p)$ and $(n,\alpha)$ appreciable for Be, N, O in the MeV region | §7.4.1 | 204 | 227 |
| **Example 7.5** — ⁵⁵Mn activation (`activation_rate`, `activation_activity`) | Example 7.5 | 204 | 227 |
| Fission cross sections; fissile vs fissionable (`is_fissile`) | §7.4.2 | 205 | 228 |
| ²³⁵U total and fission cross sections | Fig. 7.10 | 205 | 228 |
| Fission cross sections of three fissionable isotopes | Fig. 7.11 | 205 | 228 |
| Thermal cross sections (`load_thermal_cross_sections`) | Table C.1 | 588 | 611 |
| Activation cross sections (`load_activation_data`) | Table C.2 | 589–590 | 612–613 |

## Problems (verified, S&F 3rd ed. Ch. 7)
Chapter 7's problem set begins on printed **218** (PDF 241). Problem **16**
belongs to this module; **1–13** are `~NE-11`, **12/14/15** are `~NE-12`, and
**17–21** are `~NE-14`.

- **Prob. 16** — transmission through 10 cm of iron at 27 and 28 keV, across a
  resonance — printed 219, PDF 242.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Example 7.5 uses an approximation it states; this module keeps both

S&F's Example 7.5 (printed 204) computes the activity of an irradiated ⁵⁵Mn
sample as **2.609×10¹⁰ Bq**, having written that "since the irradiation time is
very small compared to the half-life of ⁵⁶Mn, we can neglect any radioactive
decay" — i.e. using the linear form $A\simeq\lambda Rt$.

The exact saturation form of `~NE-07`, $A=R[1-e^{-\lambda t}]$, gives
**2.598×10¹⁰ Bq**. The difference is 0.45%, and it is precisely $\lambda t/2$,
the leading term dropped by the linearisation. The book's value is the *high*
one, because the linear form ignores decay occurring during irradiation.

Neither is an error — the book states its assumption and the assumption is sound
at 0.9% of saturation. But the two are different numbers, so
`activation_activity` **requires `half_life_s` to be passed explicitly** and
computes the exact form; a caller who wants the book's answer must multiply out
$\lambda Rt$ deliberately. `test_reproduces_example_7_5` asserts both values and
that their ratio is $\lambda t/2$.

## A meaningful blank in Table C.2

Appendix C.2 lists **⁹⁹ᵐTc with no activation cross section**. That blank is
correct rather than missing data: ⁹⁹ᵐTc's parent is ⁹⁹Mo, a **fission product**
(`~NE-09`), reached by decay down an isobaric chain rather than by neutron
capture on a stable target. No activation cross section applies to it.

`load_activation_data` therefore returns `None` for that field rather than
substituting 0.0, which would silently yield an activation rate of zero and look
like a valid answer. Two further rows (²³³Pa, ²³⁹Np) have no parent abundance,
for the analogous reason that their parents do not occur naturally.
`test_appendix_C2_blanks_are_meaningful` pins all three.

## A convention: the thermal reference point

Appendix C.1 is quoted at a single point, described three ways: **0.0253 eV**,
**2200 m/s**, **293.6 K**. These are consistent to about 0.2%, not exactly —
2200 m/s corresponds to 0.02525 eV. The discrepancy is harmless in absolute
terms and matters for one thing: the 1/v law is a *ratio* to a reference, so
mixing the nominal speed with the nominal energy as two different anchors
introduces a systematic 0.2% error.

`one_over_v_cross_section` anchors on `E_THERMAL_EV = 0.0253` and
`test_one_over_v_law` derives the reference speed from it rather than using the
nominal `V_THERMAL_CM_S`, while separately checking the two agree to 0.3%.

## Cross-module dependencies
- **`~NE-11`** — $\Sigma=\sigma N$, mean free path and $R=\Sigma\phi$, restated
  here for neutrons; and the "absorption means every removal channel" convention.
- **`~NE-12`** — the contrast this module is built against: smooth $Z$-power laws
  for photons, no law at all for neutrons.
- **`~NE-08`** — elastic-scattering kinematics, ξ and the collision counts that
  make moderation quantitative; the compound nucleus behind every resonance.
- **`~NE-09`** — the fissile/fissionable split, here in cross-section terms; and
  ⁹⁹Mo as a fission product.
- **`~NE-07`** — the decay-with-production law that governs activation.
- **`../data_tables/`** — `C1_thermal_neutron_cross_sections.csv` (27 nuclides),
  `C2_activation_radionuclides.csv` (31 entries).

## Further reading
- Kinsey, R. (ed.), *ENDF/B Summary Documentation*, BNL-NCS-17541 (1979); Rose &
  Dunford (1991) — S&F's cited evaluated-data sources.
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, §3.6–3.7 — resonance
  structure and the Breit–Wigner form, which S&F omit entirely.
- Mughabghab, S.F., *Atlas of Neutron Resonances* — the resonance parameters
  themselves, for anyone who needs the actual widths and spacings.
- Bell & Glasstone, *Nuclear Reactor Theory*, Ch. 8 — resonance absorption and
  self-shielding, the quantitative version of `problems.md` P7.
- Knoll, *Radiation Detection and Measurement*, Ch. 14 — ¹⁰B and ⁶Li as detector
  materials, and why their 1/v behaviour matters there (`~NE-15`).
