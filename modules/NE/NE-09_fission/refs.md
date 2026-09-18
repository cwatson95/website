# NE-09 — References

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
| Fission reactions; splitting a heavy nucleus | §6.5.3 | 150 | 173 |
| Spontaneous fission; ²⁵²Cf | §6.5.3 | 151 | 174 |
| **Table 6.2** — nuclides which spontaneously fission (`SPONTANEOUS_FISSION`) | Table 6.2 | 151 | 174 |
| Caption: ²⁴¹Pu, ²⁵⁰Cm, ²⁴⁹Bk also beta-decay (`BETA_BRANCH_PERCENT`) | Table 6.2 caption | 151 | 174 |
| Competing channels: elastic, inelastic, capture, fission | §6.5.3 | 152 | 175 |
| **Fissile / fissionable / fertile** (`FISSILE`, `is_fissile`) | §6.5.3 | 152 | 175 |
| The two breeding chains ²³²Th→²³³U, ²³⁸U→²³⁹Pu (`BREEDING`) | §6.5.3 | 152 | 175 |
| Thermal / epithermal / fast neutrons | §6.5.3 fn. 5 | 152 | 175 |
| Characteristics of the fission reaction | §6.6 | 153 | 176 |
| **Excitation energy $E^*=S_n+E_n$** (`excitation_energy`) | §6.6 | 153 | 176 |
| Scission; the highly charged fragments | Eq. (6.32) | 153 | 176 |
| Prompt neutrons $\nu_p$; prompt gammas | §6.6 | 153 | 176 |
| Ternary fission (~0.2% alphas) | §6.6 fn. 6 | 153 | 176 |
| Fission after prompt emission | Eq. (6.33) | 154 | 177 |
| **Nucleon conservation** (`conserve_fission`) | Eq. (6.34) | 154 | 177 |
| Fission products | §6.6.1 | 154 | 177 |
| Isobaric β⁻ chains; n/p ratio 1.57 vs 1.2–1.4 | §6.6.1 | 154 | 177 |
| ¹⁴⁰Xe chain — the Hahn/Strassmann/Meitner discovery | Eq. (6.35) | 154 | 177 |
| ¹⁴⁷Nd chain — promethium | Eq. (6.36) | 155 | 178 |
| ⁹⁹Sr chain — ⁹⁹ᵐTc | Eq. (6.37) | 155 | 178 |
| ¹³⁵Sb chain — ¹³⁵Xe poisoning | Eq. (6.38) | 155 | 178 |
| Mass distribution; asymmetry, peak/valley ≈ 650 | §6.6.1, Fig. 6.6 | 155–156 | 178–179 |
| Cumulative chain yield $y_k(A)$ | Eq. (6.39) | 156 | 179 |
| Momentum conservation between fragments | Eq. (6.40) | 156 | 179 |
| **$E_L/E_H=m_H/m_L$** (`fragment_energy_split`) | Eq. (6.41) | 156 | 179 |
| Fragment energy distribution; 99.2 and 68.1 MeV means | Fig. 6.7 | 157 | 180 |
| Neutron emission in fission | §6.6.2 | 157 | 180 |
| **Example 6.4** — 183.6 MeV, $E_H=69.8$ MeV (`prompt_energy_release`) | Example 6.4 | 157–158 | 180–181 |
| Prompt and delayed neutrons; $\beta\equiv\bar\nu_d/\bar\nu$ | §6.6.2 | 158 | 181 |
| **Table 6.3** — $\bar\nu$ and $\beta$ (`NEUTRON_YIELD`) | Table 6.3 | 158 | 181 |
| Energies of fission neutrons; peak 0.7 MeV, mean ~2 MeV | §6.6.2, Fig. 6.8 | 158–159 | 181–182 |
| **Watt distribution** (`watt_spectrum`) | Eq. (6.42) | 159 | 182 |
| Compact form $ae^{-E/b}\sinh\sqrt{cE}$ | Eq. (6.43) | 159 | 182 |
| **Table 6.4** — Watt parameters (`WATT_PARAMS`) | Table 6.4 | 159 | 182 |
| Energy released in fission; the 200 MeV estimate | §6.6.3 | 160 | 183 |
| **Example 6.5** — 24.2 MeV delayed (`delayed_energy_release`) | Example 6.5 | 160 | 183 |
| **Table 6.5** — the energy budget (`FISSION_ENERGY_MEV`) | Table 6.5 | 161 | 184 |
| **Decay heat** $1.4t^{-1.2}$, $1.26t^{-1.2}$ (`decay_heat_*`) | Eqs. (6.44)–(6.45) | 161 | 184 |
| Decay-heat emission rates vs time | Fig. 6.9 | 162 | 185 |
| 1 W = 3.1e10 fissions/s (`fissions_per_second`) | §6.6.3 | 162 | 185 |
| **1 MWd = 1.05 g fissioned = 1.24 g consumed** (`grams_per_mwd`) | §6.6.3 | 162–163 | 185–186 |
| Atomic masses (`load_atomic_masses`) | Table B.1 | 570–587 | 593–610 |

## Problems (verified, S&F 3rd ed. Ch. 6)
Chapter 6's problem set begins on printed **174** (PDF 197). Problems **16–21**
belong to this module; **1–15** are kinematics (`~NE-08`) and **22–25** are fusion
(`~NE-10`).

- **Prob. 16** — neutrons/s from 1 mg of ²⁵²Cf — printed 176, PDF 199.
- **Prob. 17** — ²³⁵U fission giving ¹²¹Ag and 4 prompt neutrons — printed 176, PDF 199.
- **Prob. 18** — ⁹⁰Kr + ¹⁴²Ba + 4n + 6γ, taken to stable end products — printed 176–177, PDF 199–200.
- **Prob. 19** — 10 g of ²³⁵U at 100 W; the ⁹⁹Tc inventory after a year — printed 177, PDF 200.
- **Prob. 20** — a 100 W bulb, in uranium and in coal — printed 177, PDF 200.
- **Prob. 21** — a 7 kg TNT-equivalent criticality accident — printed 177, PDF 200.

Worked solutions for most chapter problems are in the authors' solution manual,
`nuclear_science_sol_shultis_faw.pdf`, indexed by chapter and problem number.

## Two errata in Table 6.2

Table 6.2 (printed 151) lists five columns per nuclide: half-life, spontaneous
fission probability per decay, neutrons per fission, alphas per fission, and
neutrons per gram-second. Those are **over-determined**. Two relations must hold,
neither of them printed in the book:

$$\text{n/(g·s)}=\frac{\ln2}{T_{1/2}}\cdot\frac{N_A}{A}\cdot P_{\text{fis}}\cdot\nu,
\qquad
\frac{\alpha}{\text{fission}}=\frac{P_\alpha}{P_{\text{fis}}},$$

with $P_\alpha=1-P_{\text{fis}}-P_\beta$ and $P_\beta$ taken from the table's own
caption for the three nuclides that also beta-decay (²⁴¹Pu 99.99755%, ²⁵⁰Cm 14%,
²⁴⁹Bk 99.99856%). `test_table_6_2_is_internally_consistent` applies both to all
26 rows. **Twenty-four rows agree to within 5%.** Two do not, and in each case
the row's *other* columns agree on what the value should be:

**²³⁷Np — fission probability, printed $2.1\times10^{-12}$ %, should be
$2.1\times10^{-10}$ %.** Two independent checks give the same factor of 100:

- the alphas-per-fission column, 4.7×10¹¹, implies a fission *fraction* of
  $1/4.7\times10^{11}=2.13\times10^{-12}$, i.e. $2.1\times10^{-10}$ %;
- the emission rate, 1.1×10⁻⁴ n/(g·s), with $T_{1/2}=2.14\times10^{6}$ y and
  $\nu=2.05$, also requires $2.1\times10^{-10}$ %.

The printed figure appears to confuse the fission *fraction* with the fission
*percentage* for this one row.

**²⁴⁸Cm — emission rate, printed $4.1\times10^{12}$ n/(g·s), should be
$4.1\times10^{7}$.** From its own half-life ($3.39\times10^{5}$ y), fission
probability (8.26%) and $\nu$ (3.14), the rate is $4.1\times10^{7}$. The printed
value is also *physically impossible*: it would make ²⁴⁸Cm — half-life 339 000
years — a brighter neutron source than ²⁵²Cf ($2.3\times10^{12}$, half-life
2.6 years) despite fissioning 130 000 times more slowly per atom. The
alphas-per-fission column (11) is consistent with the corrected value.
$4.1\times10^{7}$ n/(g·s) is also the figure quoted elsewhere for ²⁴⁸Cm sources.

Both corrections are applied in `SPONTANEOUS_FISSION`; the printed values are
preserved in `TABLE_6_2_ERRATA`, and `test_the_two_table_6_2_typos` pins each
correction to the specific power of ten and the specific cross-check that forces
it. Nothing is discarded silently.

## A caution the book states but the formula does not enforce

**The decay-heat correlations have a stated range.** S&F give
Eqs. (6.44)–(6.45) as valid for $10\ \text{s}<t<10^{5}$ s. The book's own
Problem 21 then asks for the decay power **three months** after an accident —
$7.8\times10^{6}$ s, nearly two decades beyond the range. `decay_heat_total` does
not clamp its argument, deliberately: silently returning a range-limited answer
would hide the issue, and the formula is the book's. The caller must check.
Beyond $10^{5}$ s the true curve flattens relative to $t^{-1.2}$ as the
short-lived chains exhaust and a handful of specific nuclides (⁹⁰Sr, ¹³⁷Cs and
their daughters) come to dominate, so the extrapolation **under**estimates.
`problems/problems.md` P6 works the problem and says so.

## Cross-module dependencies
- **`~NE-08`** — the neutron-induced reaction and the compound nucleus.
- **`~NE-03`** — binding energy per nucleon; the 0.9 MeV/nucleon that fission
  harvests, and the separation energy $S_n$ recomputed here.
- **`~NE-02`** — the SEMF pairing term, which is the entire fissile/fissionable
  distinction.
- **`~NE-07`** — the isobaric decay chains, and the production-and-decay
  equation that governs fission-product inventories.
- **`~NE-05`** — spontaneous fission as a decay branch competing with alpha.
- **`../data_tables/`** — `B1_atomic_masses.csv` (2931 nuclides).

## Further reading
- Keepin, G.R., *Physics of Nuclear Kinetics* (1965) — S&F's source for
  Tables 6.3 and Fig. 6.7; still the standard reference on delayed-neutron groups.
- Reilly, Ensslin & Smith, *Passive Nondestructive Assay of Nuclear Materials*
  (1991) — S&F's source for Table 6.2; the practical treatment of spontaneous
  fission as an assay signature.
- Lamarsh & Baratta, *Introduction to Nuclear Engineering*, §4.3 — the fission
  process with the liquid-drop barrier worked through explicitly.
- Wahl, A.C., *Atomic Data and Nuclear Data Tables* **39** (1988) 1 — fission
  yields $y(A,Z)$ in full, behind S&F's Fig. 6.6.
- ANS-5.1, *Decay Heat Power in Light Water Reactors* — the standard that
  replaces Eqs. (6.44)–(6.45) for engineering use, valid to $10^{9}$ s.
