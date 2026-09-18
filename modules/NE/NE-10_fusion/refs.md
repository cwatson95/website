# NE-10 — References

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
| Fusion reactions; the seven candidate fuels (`FUSION_REACTIONS`) | §6.7 | 163 | 186 |
| Threshold from the Coulomb barrier; "a few keV to several hundred keV" | §6.7 | 163 | 186 |
| Thermonuclear fusion; $E_{av}=3kT/2$; 10–300 MK (`thermal_energy`) | §6.7.1 | 163 | 186 |
| Gravitational confinement; the sun's core, 15 MK, $4\times10^{16}$ Pa (`SUN`) | §6.7.1 | 164 | 187 |
| Magnetic confinement; $10^{15}$ cm⁻³, $10^{5}$ atm | §6.7.1 | 164 | 187 |
| **D–T reaction**, 3.54 + 14.05 MeV (`reaction_product_energies`) | Eq. (6.46) | 164 | 187 |
| Tritium breeding from ⁶Li and ⁷Li (`TRITIUM_BREEDING`) | §6.7.1 | 164 | 187 |
| Inertial confinement; thermonuclear weapons | §6.7.1 | 165 | 188 |
| **Example 6.6** — d–d burned to ⁴He, 23.84 MeV (`energy_per_deuteron`) | Example 6.6 | 165 | 188 |
| The potential of fusion energy; 0.015% D, $1.4\times10^{43}$ atoms (`fusion_energy_of_water`) | §6.7.1 | 165 | 188 |
| Energy production in stars; $4\times10^{26}$ W, the core | §6.7.2 | 166 | 189 |
| $p+p\to$ D$+\beta^++\nu$, $Q=0.42$ MeV (`q_value`, positron-corrected) | §6.7.2 | 166 | 189 |
| The p–p bottleneck; 1 in $10^{18}$ per second, $3\times10^{10}$ y | §6.7.2 | 166–167 | 189–190 |
| D$+p\to{}^{3}$He, ${}^{3}$He$+{}^{3}$He$\to{}^{4}$He (`PP_CHAIN`) | §6.7.2 | 167 | 190 |
| **Net pp chain**, $Q=26.72$ MeV (`pp_chain_energy`) | Eq. (6.47) | 167 | 190 |
| pp-II and pp-III branches via ⁷Be | §6.7.2 | 167 | 190 |
| **CNO cycle** (`CNO_CYCLE`) | §6.7.2, Eq. (6.48) | 167–168 | 190–191 |
| Aging stars; the red-giant phase | §6.7.2 | 168 | 191 |
| ⁸Be unbound; the triple-alpha process (`HELIUM_BURNING`) | §6.7.2 | 168 | 191 |
| Alpha capture: ¹²C→¹⁶O→²⁰Ne→²⁴Mg | §6.7.2 | 168 | 191 |
| Carbon and oxygen burning (`ADVANCED_BURNING`) | §6.7.2 | 169 | 192 |
| Death of sun-like stars; the Chandrasekhar limit, 1.44 $M_\odot$ | §6.7.2 | 169 | 192 |
| **Type Ia supernova**; $1$–$2\times10^{44}$ J; ⁵⁶Ni→⁵⁶Co→⁵⁶Fe | §6.7.2 | 169–170 | 192–193 |
| Core temperature and density through the burning phases | Fig. 6.10 | 170 | 193 |
| Stellar lifetime against initial mass | Fig. 6.11 | 170 | 193 |
| Type II supernovae; $10^{46}$ J in a ten-second neutrino burst | §6.7.2 | 171 | 194 |
| Neutron stars (~40 km, $10^{11}$ K); black holes above ~15 $M_\odot$ | §6.7.2 | 171 | 194 |
| Nucleogenesis; the big bang and primordial abundances | §6.7.3 | 171–172 | 194–195 |
| Solar-system elemental abundances (from Table A.3) | Fig. 6.12 | 172 | 195 |
| Photodisintegration at $10^{10}$ K, $kT\simeq1$ MeV | §6.7.3 | 172–173 | 195–196 |
| **s-process and r-process**; ¹³C(α,n)¹⁶O as the s-process neutron source | §6.7.3 | 173 | 196 |
| Atomic masses (`load_atomic_masses`) | Table B.1 | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 6)
Chapter 6's problem set begins on printed **174** (PDF 197). Problems **22–25**
belong to this module; **1–15** are kinematics (`~NE-08`) and **16–21** are
fission (`~NE-09`).

- **Prob. 22** — d–d fusion energy in an 8 oz glass of water — printed 177, PDF 200.
- **Prob. 23** — the sun's mass-conversion rate, ⁴He rate and flux at earth — printed 177, PDF 200.
- **Prob. 24** — the sun's lifetime output against a Type Ia supernova — printed 177, PDF 200.
- **Prob. 25** — why hydro, wind, coal and nuclear are all indirectly fusion — printed 177, PDF 200.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Two errata

Every Q-value printed in §6.7 was recomputed from Appendix B
(`test_book_q_values`, `test_helium_and_advanced_burning_q_values`,
`test_pp_chain_sums_to_the_book_value`). **Nineteen of twenty agree to better
than 3 keV.** One does not.

**p + ¹¹B → 3α, printed 8.08 MeV, should be 8.68 MeV** (printed 163). From the
book's own Appendix B,
$$Q=\left[M(^{1}\text{H})+M(^{11}\text{B})-3M(^{4}\text{He})\right]c^2
=[1.0078250+11.0093055-12.0078098]\ \text{u}\times931.494=8.682\ \text{MeV}.$$
8.68 MeV is also the value quoted throughout the aneutronic-fusion literature.
The printed 8.08 looks like a 6→0 transposition. Corrected in
`FUSION_REACTIONS`; the printed value is preserved in `BOOK_Q_ERRATA` and
`test_the_p11B_erratum` pins both.

**The solar core radius, printed "about 7,000 km ... or about 0.1% of the sun's
total volume"** (printed 166). These two statements are inconsistent by a factor
of 1000 in volume. With $R_\odot=696{,}000$ km,
$$0.1\%\text{ of the volume}\;\Rightarrow\;r=696{,}000\times(0.001)^{1/3}
=69{,}600\ \text{km},$$
whereas 7,000 km would be $(7/696)^3=1.0\times10^{-6}$, i.e. 0.0001% of the
volume. The **volume fraction is the correct half**, because it yields the
accepted core power density:
$$\frac{4\times10^{26}\ \text{W}}{0.001\,V_\odot}=283\ \text{W/m}^3,$$
the familiar "less than a compost heap" figure. Taking 7,000 km instead would
give 280 kW/m³, a thousand times too high and comparable to a chemical rocket.
`SUN["core_radius_km"]` therefore holds $7.0\times10^{4}$ km; the printed value is
in `SUN_ERRATA`, and `test_the_solar_core_radius_erratum` checks both halves of
the sentence against each other.

## A convention S&F switch mid-section

**The pp chain is quoted with two different accounting conventions**, differing
by $4m_ec^2=2.044$ MeV — 8%.

The individual steps are given as *nuclear* $Q$-values with the $\beta^+$
correction applied: $p+p\to$ D + $\beta^+$ + $\nu$ is quoted at **0.42 MeV**,
which is $1.442-2m_ec^2$ from neutral-atom masses. Summing the three steps with
their multiplicities gives **24.69 MeV**.

But Eq. (6.47) quotes the net $4({}^1\text{H})\to{}^4\text{He}$ at **26.72 MeV**,
which is the bare neutral-atom difference $4M(^1\text{H})-M(^4\text{He})$ — i.e.
it *includes* the energy released when the two positrons subsequently annihilate
with ambient electrons.

Both are correct answers to different questions. For a star the 26.72 MeV figure
is the relevant one, since annihilation is immediate and the gammas thermalise.
`pp_chain_energy` takes an `include_annihilation` flag and defaults to the
star-relevant convention; `test_pp_chain_sums_to_the_book_value` checks that both
routes agree with the book and that they differ by exactly $4m_ec^2$. The
$\beta^+$ correction itself is the same one `~NE-05` develops for positron
emitters, and `q_value` takes an `n_positrons` argument for it.

(About 0.6 MeV of the 26.72 MeV leaves as neutrinos and is never thermalised —
not mentioned by S&F here, but it is the flux that solar-neutrino experiments
measure and is how the pp chain was confirmed.)

## Beyond the book: the Gamow peak

`modules/NE/list_NE.txt` lists "the Gamow peak" in NE-10's scope, and S&F do not
derive it — §6.7 asserts only that "the kinetic energy needed is typically a few
keV to several hundred keV" (printed 163) without saying why fusion proceeds two
orders of magnitude below the classical barrier. `gamow_energy`,
`gamow_peak_energy`, `gamow_peak_width` and `tunnelling_probability` implement
the standard treatment:
$$E_G=2\mu c^2(\pi\alpha Z_1Z_2)^2,\qquad
P\sim e^{-\sqrt{E_G/E}},\qquad
E_0=\left[\frac{E_G(kT)^2}{4}\right]^{1/3},\qquad
\Delta=\frac{4}{\sqrt3}\sqrt{E_0kT}.$$
Sources: Clayton, *Principles of Stellar Evolution and Nucleosynthesis* (1968),
Ch. 4 — the canonical derivation; Krane, *Introductory Nuclear Physics*, §14.2;
Iliadis, *Nuclear Physics of Stars* (2007), §3.2 for the modern treatment
including the non-resonant $S$-factor that this module does not attempt.

## One thing that has changed since publication

S&F write of inertial confinement that "break-even has yet to be achieved"
(printed 165). The National Ignition Facility reported **target gain > 1** in
December 2022 (2.05 MJ of laser energy in, 3.15 MJ of fusion energy out), and
higher gains since. This is target gain, not wall-plug gain — the laser drew
roughly 300 MJ from the grid — so the book's underlying point about the energy
balance of the *system* still stands, but the statement as written is out of
date. Noted here rather than silently corrected, since the module reproduces the
book.

## Cross-module dependencies
- **`~NE-08`** — the Coulomb barrier that is the entire difficulty, and the
  inverse-mass product energy split.
- **`~NE-09`** — the other slope of the binding-energy curve; the comparison of
  energy per nucleon.
- **`~NE-05`** — the $\beta^+$ mass correction, needed throughout stellar
  hydrogen burning.
- **`~NE-03`** — the binding-energy curve and its ⁶²Ni peak, where §6 stops.
- **`~NE-07`** — the ⁵⁶Ni→⁵⁶Co→⁵⁶Fe chain behind a Type Ia light curve.
- **`../data_tables/`** — `B1_atomic_masses.csv` (2931 nuclides).

## Further reading
- Clayton, D.D., *Principles of Stellar Evolution and Nucleosynthesis* (1968) —
  the standard text; Ch. 4 for the Gamow peak, Ch. 7 for the s- and r-processes.
- Burbidge, Burbidge, Fowler & Hoyle, *Rev. Mod. Phys.* **29** (1957) 547 —
  "B²FH", the paper that established stellar nucleosynthesis.
- Hoyle, F., *Astrophys. J. Suppl.* **1** (1954) 121 — the prediction of the
  ¹²C resonance from the fact that carbon exists.
- Mayo, R.M., *Introduction to Nuclear Concepts for Engineers* (1998) — S&F's
  cited source for §§6.7.1–6.7.2.
- Cottingham & Greenwood, *An Introduction to Nuclear Physics* (1986) — S&F's
  other cited source for the stellar-evolution narrative.
- Freidberg, J.P., *Plasma Physics and Fusion Energy* (2007) — the confinement
  side, picked up in `~NE-24`.
