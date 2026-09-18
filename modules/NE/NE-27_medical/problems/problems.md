# NE-27 — Problems

Work each by hand, then check with `code/medical.py`. Citations in `../refs.md`;
**S&F** = Shultis & Faw 3rd ed., cited by printed page. Chapter 14 carries no
worked problems; these are added.

### P1.  Why mammography uses molybdenum  *(added, from Table 14.2)*
A mammography tube must deliver photons near 17–20 keV; a chest radiograph needs
~60 keV. Using Moseley's law, $E_{K\alpha} \approx 10.2\ \text{eV}\,(Z-1)^2$,
find the atomic number that puts the Kα line at each energy, and check against
Table 14.2's Mo (Z = 42) and W (Z = 74).
*Check:* Z ≈ 42 and Z ≈ 77; Mo Kα₁ = 17.48 keV, W Kα₁ = 59.32 keV.

**Solution.** Inverting, $Z = 1 + \sqrt{E/10.2\ \text{eV}}$. For 17.5 keV,
$\sqrt{17500/10.2} = 41.4$, so $Z \approx \boxed{42}$ — molybdenum. For 59.3 keV,
$\sqrt{59300/10.2} = 76.2$, so $Z \approx \boxed{77}$–78, and tungsten at 74 is
the practical choice (it also has the melting point an anode needs). Moseley
lands within 2% for Mo and 8% for W; the screening approximation degrades at high
$Z$, which is why the estimate drifts upward.

**The point is what you cannot do.** A characteristic line is fixed by the
element. You can lower the *tube voltage* and cut off the bremsstrahlung
continuum above it, but you cannot slide the Kα line to a preferred energy — so
choosing the imaging energy means choosing the metal. That is why a mammography
unit is a different machine from a chest unit, not a different setting on one.

Cross-check the wavelength column while you are there: 12.39842/0.7093 = 17.4798
against the printed 17.4793 keV. All ten lines in Table 14.2 close to 1.6 × 10⁻⁴
or better, which says the two columns are one measurement expressed twice.

---

### P2.  The unit the chapter never defines  *(added, §14.1.5)*
Water has $\mu \approx 0.206$ cm⁻¹ at CT energies. Define the Hounsfield unit so
water is 0 and air is −1000, then find the CT number of a tissue with
$\mu = 0.500$ cm⁻¹ and the $\mu$ of a lung region at −700 HU. Why must the scale
be pinned at *two* points rather than one?
*Check:* +1427 HU; 0.0618 cm⁻¹.

**Solution.** Air's $\mu$ is ~0, so requiring HU(air) = −1000 and HU(water) = 0
forces
$$\mathrm{HU} = 1000\,\frac{\mu - \mu_w}{\mu_w}.$$
Then HU(0.500) = 1000(0.500 − 0.206)/0.206 = $\boxed{+1427}$, and
$\mu = 0.206(1 - 0.700) = \boxed{0.0618\ \text{cm}^{-1}}$.

**Why two points.** A single fixed point removes only an offset; the reconstructed
$\mu$ would still carry the scanner's own scale factor — beam spectrum, detector
gain, reconstruction filter. Two fixed points remove offset *and* scale, so a
CT number means the same thing on any machine. That portability is the whole
reason radiologists quote HU rather than cm⁻¹.

Note the floor. HU = −1000 corresponds to $\mu = 0$; anything below it implies a
*negative* attenuation coefficient — a material that is less attenuating than a
vacuum. `mu_from_hounsfield` refuses it rather than returning a number.

**Erratum on the same page.** S&F say Hounsfield and Cormack "shared the Nobel
prize in 1972". The prize was 1979; 1972 is the year of the first published CT
images.

---

### P3.  The beta-plus signature  *(added, from Table 14.3)*
For each of Table 14.3's four positron emitters compute $\bar{E}/E_{max}$. Why is
the answer near 0.40 rather than the ≈0.33 familiar from β⁻ emitters?
*Check:* 0.402, 0.410, 0.424, 0.394.

**Solution.** Dividing the printed columns:

| | ¹¹C | ¹³N | ¹⁵O | ¹⁸F |
|---|---|---|---|---|
| $E_{max}$ (MeV) | 0.960 | 1.199 | 1.732 | 0.634 |
| $\bar{E}$ (MeV) | 0.386 | 0.492 | 0.735 | 0.250 |
| ratio | $\boxed{0.402}$ | $\boxed{0.410}$ | $\boxed{0.424}$ | $\boxed{0.394}$ |

**The physics is Coulomb.** The daughter nucleus is positively charged. A
departing **positron** is repelled by it, which pushes the emitted spectrum
towards higher energies; a departing **electron** is attracted, which drags it
down. So β⁺ spectra sit near 0.40 of the endpoint and β⁻ spectra near 0.33. Four
independent table entries agreeing on 0.40 is a check that Table 14.3 is measured
data rather than assembled from a rule of thumb.

Re-reading the same nuclides out of the trunk's shared decay table
(`data_tables/D1_decay_radiation.csv`) reproduces every $E_{max}$, $\bar{E}$ and
branch to better than 0.5%, and gives the 511 keV yield as *exactly twice* the
positron branch (199.52% against 99.76% for ¹¹C). Two photons per positron —
which is what makes coincidence detection possible at all.

---

### P4.  Only one of them can be shipped  *(added, §14.1.8)*
S&F write that "only ¹⁸F [has] a sufficiently long life to permit transport of
radiopharmaceuticals to sites a few hours from the point of preparation." Put a
number on it: for each PET nuclide, how long until the activity falls to 10% of
what left the cyclotron?
*Check:* ¹⁸F 6.09 h; ¹¹C 68 min; ¹³N 33 min; ¹⁵O 6.8 min.

**Solution.** $A/A_0 = 2^{-t/T_{1/2}}$, so $t(10\%) = T_{1/2}\log_2 10 =
3.322\,T_{1/2}$:

| | ¹⁸F | ¹¹C | ¹³N | ¹⁵O |
|---|---|---|---|---|
| $T_{1/2}$ | 110 min | 20.5 min | 9.97 min | 122 s |
| $t(10\%)$ | $\boxed{6.09\ \text{h}}$ | $\boxed{68\ \text{min}}$ | $\boxed{33\ \text{min}}$ | $\boxed{6.8\ \text{min}}$ |

A factor of **54** separates ¹⁸F from ¹⁵O. Over a two-hour delivery ¹⁸F retains
47% of its activity; ¹⁵O retains $2^{-59} \approx 2\times10^{-18}$, which is to
say none.

**Where the constraint comes from.** `~NE-26`'s production argument: a positron
emitter is proton-rich, so it is made by a $(p,x)$ reaction on a cyclotron — all
four production reactions in Table 14.3 are $(p,\alpha)$ or $(p,n)$ — and nuclides
that far from stability are short-lived. So three of the four require the
cyclotron *in the building*, and that, more than the scanner, is what makes a PET
centre expensive. SPECT sidesteps it entirely with the ⁹⁹Mo/⁹⁹ᵐTc generator: ship
the 66-hour parent, elute the 6-hour daughter on site.

---

### P5.  What PET's resolution is actually limited by  *(added, §14.1.8)*
(a) A 10 ns coincidence window localises an annihilation to what distance along
the line of response? (b) Taking S&F's statement that a 1 MeV positron travels
about 4 mm in tissue and scaling as $\bar{E}^{1.5}$, how far do ¹⁸F and ¹⁵O
positrons travel before annihilating? (c) Which limit can be engineered away?
*Check:* 150 cm; 0.50 mm and 2.52 mm; neither, by a better detector.

**Solution.** (a) Two photons leave simultaneously; a time difference $\Delta t$
displaces the annihilation point by $c\,\Delta t/2$ along the line. With
$\Delta t = 10$ ns, $c\Delta t/2 = (3\times10^{10}\ \text{cm/s})(10^{-8}\
\text{s})/2 = \boxed{150\ \text{cm}}$ — far larger than a patient. Conventional
PET therefore localises **by reconstruction, not by timing**: the window's only
job is to reject accidental coincidences.

(b) $R = 4.0\,\bar{E}^{1.5}$ mm gives $4(0.250)^{1.5} = \boxed{0.50}$ mm for ¹⁸F
and $4(0.735)^{1.5} = \boxed{2.52}$ mm for ¹⁵O.

(c) **Neither.** The timing limit is a property of the clock, and improving it is
exactly what time-of-flight PET does — 400 ps gives 6 cm, which finally beats the
patient (this is beyond the book, and it improves signal-to-noise more than
resolution). But the positron range is not a detector property at all: the
positron has already *moved* before it emits the photons, so the line of response
points at where it stopped, not where the tracer was. No detector at any price
recovers that.

This is a second, independent argument for ¹⁸F — five times sharper than ¹⁵O — on
top of P4's transport argument. Two unrelated criteria selecting the same nuclide
is why FDG became the workhorse of clinical PET.

---

### P6.  The therapeutic ratio, and three ways to raise it  *(added, §14.5)*
A tumour receives 70 Gy while surrounding tissue receives 35 Gy. (a) What is the
therapeutic ratio, and why must it exceed 1? (b) A brachytherapy source is placed
in the tumour rather than beamed from outside; compare the dose at 0.5 cm with
that at 10 cm. (c) Classify §14.5's modalities by *how* each sharpens the ratio.
*Check:* 2.0; a factor of 400.

**Solution.** (a) $\mathrm{TR} = 70/35 = \boxed{2.0}$. If TR ≤ 1 the healthy
tissue receives at least as much dose as the tumour, and there is no treatment —
only harm. `therapeutic_ratio` refuses that case rather than returning a number,
because a ratio of 0.5 is not a bad treatment, it is not a treatment.

(b) $1/r^2$ gives $(10/0.5)^2 = \boxed{400}$. That factor comes for free from
geometry, which is why brachytherapy — the oldest modality in the chapter —
remains among the most effective: putting the source *inside* buys a dose
gradient no external beam can match.

(c) Sorting §14.5's eleven subsections by mechanism collapses them to three:

| how it sharpens | modalities |
|---|---|
| **geometrically** | conformal (CRT), IMRT, stereotactic, higher-energy teletherapy |
| **physically** | electron beams (finite range), proton beams (**the Bragg peak**), brachytherapy ($1/r^2$) |
| **biochemically** | radionuclide therapy (¹³¹I to thyroid), BNCT (¹⁰B in the tumour) |

The proton case is `~NE-14` cashed in: a charged particle deposits most of its
energy at the *end* of its range, so the beam can be stopped behind the tumour.
Photons cannot do this — they attenuate exponentially and never stop, so every
photon beam deposits dose all the way out the far side of the patient.

**And fractionation is the same optimisation in time.** 2 Gy/day × 5 days ×
6 weeks = 60 Gy works because normal tissue repairs sublethal damage between
fractions better than tumour does (`~NE-18`). The ratio being optimised is
identical; only the axis changes.
