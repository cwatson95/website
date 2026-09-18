# NE-19 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`,
both `-layout` and `-raw`) in the PDF under `books/library/`. **Printed** = the
number on the page; **PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Neutron moderation; why small A | §10.1 | 322 | 345 |
| Thermal neutrons; the Maxwellian (`maxwellian_flux`) | Eq. (10.1), §10.2 | 322 | 345 |
| E_mp = kT, Ebar = 2kT; 0.0253 eV = 2200 m/s | §10.2 | 322 | 345 |
| Thermal absorption rate | Eqs. (10.2)–(10.4) | 322–323 | 345–346 |
| **Westcott averaging** (`westcott_averaged_cross_section`) | Eq. (10.5) | 323 | 346 |
| **Table 10.1** — thermal-*averaged* σ (`FUEL_THERMAL_AVERAGED`) | Table 10.1 | 323 | 346 |
| Thermal-neutron properties of fuels; breeding needs η > 2 | §10.3 | 323–324 | 346–347 |
| **Table 10.2** — σ *at 0.0253 eV* (`FUEL_PROPERTIES`) | Table 10.2 | 324 | 347 |
| The neutron life cycle | §10.4, Fig. 10.1 | 324–325 | 347–348 |
| Quantifying the cycle; the six factors | §10.4.1 | 325–330 | 348–353 |
| **ε** (`fast_fission_factor`), Fig. 10.2 fit | Eq. (10.6) | 326 | 349 |
| **p**, and the effective resonance integral | Eqs. (10.7)–(10.9) | 327 | 350 |
| **Table 10.3** — ξ and σ_sM in the slowing-down region | Table 10.3 | 327 | 350 |
| **f** (`thermal_utilization_homogeneous`) | Eqs. (10.10)–(10.11) | 327–328 | 350–351 |
| **η** (`thermal_fission_factor`) | Eq. (10.12) | 328 | 351 |
| **Examples 10.1–10.2** — f in graphite; η at 2% | Ex. 10.1–10.2 | 328 | 351 |
| **Table 10.4** — moderator thermal properties (`MODERATOR_THERMAL`) | Table 10.4 | 329 | 352 |
| **P_NL^th**, the diffusion length, the buckling | Eqs. (10.13)–(10.14) | 329 | 352 |
| **P_NL^f**, the Fermi age | Eq. (10.15) | 329–330 | 352–353 |
| The cycle with numbers | Fig. 10.3 | 330 | 353 |
| **Examples 10.3–10.4** — k_∞ and non-leakage | Ex. 10.3–10.4 | 330–331 | 353–354 |
| **k_eff and k_∞** (`k_effective`, `k_infinity`) | Eqs. (10.16)–(10.17), §10.4.2 | 331 | 354 |
| Variation with fuel-to-moderator ratio | Fig. 10.4 | 332 | 355 |
| **Examples 10.5–10.6** — critical radius and mass | Ex. 10.5–10.6 | 332–333 | 355–356 |
| **Examples 10.7–10.8** — ε and p for U/water | Ex. 10.7–10.8 | 333 | 356 |
| Homogeneous vs heterogeneous cores | §10.5 | 334–337 | 357–360 |
| **Table 10.5** — optimum moderation (`OPTIMUM_RATIOS`) | Table 10.5 | 334 | 357 |
| **Lumped p** (`resonance_escape_lattice`) | Eq. (10.18) | 335 | 358 |
| **Rod resonance integral** (`resonance_integral_rod`) | Eq. (10.19) | 335 | 358 |
| **Tables 10.6–10.7** — (A, C) and ξ_M Σ_sM | Tables 10.6–10.7 | 335 | 358 |
| **Wigner–Seitz**: b = a/√π, 1/f, F and E | Eqs. (10.20)–(10.23), Fig. 10.5 | 336 | 359 |
| **Series for F and E** (`lattice_F`, `lattice_E`) | Eqs. (10.24)–(10.25) | 336 | 359 |
| **Table 10.8** — the graphite lattice (`LATTICE_TABLE`) | Table 10.8 | 337 | 360 |
| **Examples 10.9–10.10** — f and p for the lattice | Ex. 10.9–10.10 | 338 | 361 |
| Reflectors; flux flattening | §10.6, Fig. 10.6 | 337–339 | 360–362 |

## Problems (verified, S&F 3rd ed. Ch. 10)
Chapter 10's problems begin on printed **366** (PDF 389). Problems **1–23**
belong to this module; **24 onward** are kinetics and are worked in `~NE-20`.

- **Prob. 5** — the Westcott factor for ²³⁵U — printed 366, PDF 389.
- **Prob. 7–11** — η for natural and enriched uranium — printed 366, PDF 389.
- **Prob. 12** — a fully enriched solution; k_∞ and the critical radius — printed 367, PDF 390.
- **Prob. 13** — nine perturbations to a critical core — printed 367, PDF 390.
- **Prob. 17–19** — graphite-moderated mixtures and a critical cube — printed 367, PDF 390.
- **Prob. 21–22** — a ²³⁵U/water sphere — printed 368, PDF 391.

## Six printed results this module corrects

### Eqs. (10.16) and (10.17) omit the fast fission factor (printed p. 331)
S&F define ε as the *first* of six factors (§10.4.1, printed 325) and then print
$$k_{\rm eff}=p\eta fP^f_{NL}P^{th}_{NL},\qquad k_\infty=\eta pf,$$
calling the second "the four-factor formula" — which has three factors in it.
Fig. 10.3's flow diagram carries the same omission.

The book's own tables settle it. **Table 10.5's water row** is ε = 1.051,
η = 1.338, f = 0.869, p = 0.727 and k_∞ = 0.888. The product ηpf is 0.845;
εηpf is 0.888. Water is the only row of Table 10.5 with ε ≠ 1, and it is exactly
the row that discriminates. **Table 10.8** confirms it independently across
eleven rows, all with ε = 1.027.

`k_infinity` therefore takes ε and defaults it to 1, so the examples (all of
which use fully enriched or very dilute uranium, where ε really is 1) reproduce
unchanged. *Verified: `test_the_four_factor_formula_is_missing_epsilon`.*

### Table 10.3 — heavy water's scattering cross section (printed p. 327)
The row reads ξ = 0.509, σ_sM = 0.509 b: the same number twice, in adjacent
columns. The accepted D₂O scattering cross section is ~10.6 b, and **Table 10.7**
gives ξ_M Σ_sM = 0.178 cm⁻¹ for the same material, which with D₂O's atom density
requires σ_sM = 10.57 b. The printed value is out by a factor of 21.

The cross-check is trustworthy because it reproduces **graphite to four figures**
(0.0608 against 0.06084) and beryllium to 0.7%. *Verified:
`test_table_10_3_heavy_water_scattering_cross_section`.*

### Example 10.1 — a stray 6.206 (printed p. 328)
The example computes Σ_a^U/N^U = 6.639 b, then displays
$$f=\frac{6.206N^U}{6.206N^U+0.003421N^C}=\frac{6.639}{6.639+0.003421(N^C/N^U)}=0.8118,$$
so 6.206 appears between two correct uses of 6.639 and reproduces neither: it
would give 0.8012. *Verified: `test_reproduces_example_10_1`.*

### Example 10.3 — ν written where η belongs (printed p. 330)
Having just computed η = 2.080, the example writes
$k_\infty=\eta f=2.4367\times0.8143=1.6939$. But 2.4367 is ν₂₃₅ (Table 10.2), and
$2.4367\times0.8143=1.984$. The printed **answer** 1.6939 is
$2.080\times0.8143$, so the answer is right and the displayed factor is not.
*Verified: `test_reproduces_examples_10_3_to_10_6`.*

### Example 10.4 — 3500 where Table 10.4 says 3070 (printed p. 331)
$L^2=L_C^2(1-f)=3500(1-0.8143)=570.1$. But $3500\times0.1857=650$, while
Table 10.4's $L_T^2=3070$ cm² for graphite gives $3070\times0.1857=570.1$
exactly. The printed coefficient is contradicted by the printed answer. (The same
example also carries an unresolved "Eq. (??)" cross-reference, as does
Example 10.9.) *Verified: same test.*

### Example 10.9 — an inserted 8 (printed p. 338)
Two lines after computing $b=20/\sqrt\pi=11.284$ cm, the example writes
$z=b/L_M=11.8284/55.4=0.20368$. $11.284/55.4=0.20368$; $11.8284/55.4=0.21351$.
*Verified: `test_reproduces_examples_10_9_and_10_10`.*

Example 10.10 has two presentational slips in the same vein: the display
labelled "the resonance integral … from Eq. (10.19)" is actually p from
Eq. (10.18), and the following expression for p drops the minus sign in its
exponent (exp(+0.105) = 1.111, not the printed 0.90028).

## Recorded but not corrected

### The heterogeneous ε gain
§10.4.1 states that ε "in a heterogeneous core is 5–10% higher than in an
equivalent homogeneous mixture". Eq. (10.6)'s own fitted constants — which are
the fit to Fig. 10.2's uranium-rod curve — give at most **1.2%**, anywhere in
their range, and less than 0.5% at the N₂₃₈/N_W = 0.584 of Example 10.7. The
prose may refer to a different comparison (tightly packed lattices against the
dilute limit); it is not reproduced by the equation printed beside it.

### ε below one at infinite dilution
Eq. (10.6) tends to $a-c=0.99934$ as the fuel is diluted away. ε counts fissions
*added* by fast neutrons and cannot be below 1; the 0.07% shortfall is an
artefact of an empirical fit evaluated outside its range. `k_infinity` refuses
ε < 1 rather than propagating it.

## An equation whose printed layout invites a 68% error
Eq. (10.25)'s series for E(y,z) is **correct as printed**, but its
two-dimensional layout places two fractions side by side —
$$E=1+\frac{z^2}{2}\;\frac{z^2}{z^2-y^2}\;\left[\ln\frac zy-\frac34+\frac{y^2}{4z^2}\right]\!\!\!\!\!\!\!\!\!\!$$
— where the large bracket in fact opens *after* $z^2/2$, so that
$z^2/(z^2-y^2)$ multiplies only the logarithm. Read the two leading fractions as
a single $z^2/[2(z^2-y^2)]$ prefactor and Example 10.9's E becomes 1.736 instead
of 1.031, and its f becomes 0.553 instead of 0.905.

This module was initially written with the wrong reading and caught it by
checking the series against the exact Bessel form of Eq. (10.22), which is what
`test_the_lattice_series_matches_the_bessel_form` now does permanently. The
misreading is asserted *as* a misreading so it stays refuted.

## Cross-module dependencies
- **`~NE-13`** — elastic-scattering kinematics, α, ξ and the number of collisions
  to thermal; Table 6.1 is the input to §10.1.
- **`~NE-09`** — ν and the fission cross sections behind η.
- **`~NE-11`** — macroscopic cross sections, mean free path, reaction rates.
- **`~NE-20`** — the time behaviour when k_eff ≠ 1.
- **`~NE-21`** — the diffusion equation that produces B², L² and Table 10.10.

## Further reading
- Lamarsh, J.R. & Baratta, A.J., *Introduction to Nuclear Engineering*, 3rd ed.,
  Ch. 6–7 — the source of Eqs. (10.6), (10.18), (10.19) and the lattice constants.
- Lamarsh, J.R., *Introduction to Nuclear Reactor Theory* (1966) — the derivations
  S&F cite but do not reproduce, including the Wigner–Seitz treatment.
- Duderstadt, J.J. & Hamilton, L.J., *Nuclear Reactor Analysis*, Ch. 8 — modern
  lattice physics, and why tightly packed power lattices need transport methods
  rather than Eq. (10.21).
- Weinberg, A.M. & Wigner, E.P., *The Physical Theory of Neutron Chain Reactors* —
  the original of the resonance-escape and lumping arguments of §10.5.
