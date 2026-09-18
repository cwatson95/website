# NE-27 — Medical applications: imaging and therapy (notes)

Chapter 14 is where the whole trunk arrives. Almost every earlier module
reappears, not as theory but as a constraint on a machine someone has to buy.
The chapter's own division is the right one, and it is sharper than it looks:

| | wants | |
|---|---|---|
| **diagnosis** | the **smallest** dose that still forms an image | §§14.1–14.4 |
| **therapy** | the **largest** dose the tumour can take and the tissue beside it cannot | §14.5 |

Those are opposite optimisations of the same quantity. Nearly every technique in
the chapter is an attempt to sharpen one of them **spatially** — and the useful
way to read §14.5 is to ask, of each modality, *how* it sharpens.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., Ch. 14,
cited by **printed** page (PDF = printed + 23).

## 1. The anode fixes the energy, so the metal *is* the setting

Table 14.2 (p. 515) lists ten characteristic lines for W, Mo and Rh, each with a
wavelength, an energy and an excitation voltage. The first check to run is that
the wavelength and energy columns are the same photon twice:

$$E = \frac{hc}{\lambda}, \qquad hc = 12.398\ \text{keV·Å}$$

**Confirmed** — all ten lines reproduce, mean error 5.7 × 10⁻⁵, worst
1.6 × 10⁻⁴ (Rh Kα₁, 20.2126 computed vs 20.2158 printed). The excitation
voltage exceeds every line it excites, as it must: it is the shell's binding
energy, and the line is the energy released refilling the vacancy, always less.

Moseley's law, $E_{K\alpha} \approx 10.2\ \text{eV}\,(Z-1)^2$, estimates the Kα₁
lines to 2% for Mo and Rh and 8% for W — the screening approximation degrades at
high $Z$. What the fit is *for* is the design point the chapter leaves implicit:

> A characteristic line cannot be tuned. It can only be **replaced**.

Hence mammography (§14.1.3) uses a **molybdenum** anode at 17.5/19.6 keV, where
`~NE-12`'s photoelectric $Z^4/E^3$ still separates one soft tissue from another,
and general radiography uses **tungsten** at 59.3 keV, where photons get through
a torso. A factor of 3.4 in energy, and there is no dial for it — it is a
different tube. (Rhodium at 20.2 keV sits between, for denser breasts.)

## 2. Contrast is the photoelectric effect, and it is spent by 100 keV

`~NE-12` again: photoelectric absorption goes as $Z^4/E^3$, Compton scattering
only as electron density. At 20 keV bone against soft tissue is an enormous
contrast; by 100 keV $\mu$ has become nearly a measure of density alone and most
of the contrast is gone. Every imaging protocol is a settlement between the two:

- low energy → contrast, but the photons are absorbed, so **dose**;
- high energy → penetration and less dose, but the image goes flat.

Contrast agents are the way out — iodine ($Z=53$) and barium ($Z=56$) put a high
$Z$ where the anatomy has none, and their K edges are placed deliberately.

## 3. The unit Chapter 14 never defines

§14.1.5 is the chapter's most mathematical section. It builds the projection
integral (Eq. 14.8) — the **Radon transform** —

$$p_\theta(t) = -\ln\frac{I_\theta(t)}{I_0} = \int\!\!\int f(x,y)\,
\delta(x\cos\theta + y\sin\theta - t)\,dx\,dy$$

then the 1-D and 2-D Fourier transforms (Eqs. 14.9–14.12) and filtered
backprojection. It names Hounsfield and Cormack. And it never states the
**Hounsfield unit**, which is the number every clinical CT image is actually
displayed in:

$$\mathrm{HU} = 1000\,\frac{\mu - \mu_w}{\mu_w}$$

That is worth stating because of what it *is*: `~NE-11`'s attenuation
coefficient, affinely rescaled and pinned at **two** points — water at 0 and air
at −1000. One fixed point would only remove an offset; two remove the scale as
well, which is what makes a CT number comparable between machines and between
hospitals. The −1000 floor is physical, not conventional: below it $\mu$ would be
negative, and the module's `mu_from_hounsfield` refuses to go there.

**Erratum, same page.** S&F write that Hounsfield and Cormack "shared the Nobel
prize in 1972". The prize was **1979** (Physiology or Medicine, "for the
development of computer assisted tomography"). 1972 is a real date in the story —
Hounsfield's first published CT images, and EMI's first clinical scanner — so the
book has collapsed the demonstration into the prize, seven years early. Pinned by
`test_the_ct_nobel_year_is_wrong_in_the_book`.

## 4. SPECT: the collimator is the instrument

§14.1.7's chain is: the gamma camera's position logic gives an intrinsic
resolution $R_I$ = 2.5–4.5 mm; the collimator turns a detected event into a
*direction*; the two blurs combine in quadrature (Eq. 14.19),

$$R_{\rm sys} = \sqrt{R_{ph}^2 + (R_I/M)^2}, \qquad M = f/b .$$

Quadrature means the larger term wins, and the practical reading is that **SPECT
resolution is a collimator problem**: with a coarse pinhole, improving the
crystal from 4.5 mm to 2.5 mm returns only a quarter of the 2 mm (`code`
demonstrates both regimes). And the collimator cannot simply be made finer,
because it works by *absorbing* every photon that is not travelling the right
way — resolution is bought directly out of sensitivity.

**Erratum, p. 528.** Fig. 14.16's caption gives the pinhole point-spread as
"$R_{ph}/(f+b) = d/b$ or $R_{ph} = (d/b)/(f+b)$". The written division is
impossible on dimensions alone — it has units of 1/length — and the caption's own
first equality says the second should be the *product* $d(f+b)/b$. There is a
second, subtler mismatch underneath: that product is the blur in the **image**
plane, whereas the body text's $R_{ph} = (d/f)(f+b)$ is the same blur referred
back to the **object** plane, smaller by exactly $M$. Eq. (14.19) closes only
with the object-referred form, because its other term $R_I/M$ is object-referred
too. So the body text is right, the caption is right about a different plane, and
the printed division is a typo. `pinhole_resolution` implements the body's form
and the test pins all three statements against each other.

## 5. PET: what coincidence buys, and the two floors it cannot get under

A positron annihilates into **two 511 keV photons, back to back**. A coincidence
between two detectors therefore defines a *line* through the patient with no
absorbing collimator at all — S&F's "electronic collimation" — which is why PET
beats SPECT on resolution and sensitivity at once.

Table 14.3 (p. 530) is the chapter's best-verified table. Its four nuclides give

| | ¹¹C | ¹³N | ¹⁵O | ¹⁸F |
|---|---|---|---|---|
| $\bar{E}/E_{max}$ | 0.402 | 0.410 | 0.424 | 0.394 |

all within 0.03 of 0.40, against the ≈0.33 typical of **β⁻** emitters. The
difference is Coulomb: the nucleus repels the departing positron, pushing the
spectrum up. Four independent entries agreeing is a sign the table is measured
data. Re-reading them out of the repo's shared decay table
(`data_tables/D1_decay_radiation.csv`) reproduces every $E_{max}$, $\bar{E}$ and
branch to better than 0.5%, and gives the 511 keV yield as **exactly twice** the
positron branch — 199.52% against 99.76% for ¹¹C, and so on down. Two photons per
positron, which is the entire basis of the method.

Two floors bound PET's resolution, and **neither is a detector problem**:

1. **Positron range.** The positron travels before it annihilates, so the line of
   response points at where it *stopped*. Scaling from S&F's own statement that a
   1 MeV positron goes about 4 mm: ¹⁸F blurs 0.5 mm, ¹⁵O blurs 2.5 mm. No
   detector at any price recovers that.
2. **Timing.** A 10 ns coincidence window corresponds to $c\tau/2$ = **150 cm**
   along the line — far larger than a patient. Conventional PET therefore
   localises by reconstruction, not by timing. (Time-of-flight scanners at 400 ps
   reach 6 cm, which finally beats the patient; that is beyond the book, and it
   improves signal-to-noise rather than resolution.)

## 6. Why a PET centre is a bigger commitment than a SPECT one

This is `~NE-26`'s production argument arriving with consequences. A positron
emitter is **proton-rich**, so it is made by a $(p,x)$ reaction on a cyclotron —
all four of Table 14.3's production reactions are $(p,\alpha)$ or $(p,n)$ — and
nuclides that far from stability do not last. Time to fall to a tenth:

| | ¹⁸F | ¹¹C | ¹³N | ¹⁵O |
|---|---|---|---|---|
| $T_{1/2}$ | 110 min | 20.5 min | 9.97 min | 122 s |
| to 10% | **6.1 h** | 68 min | 33 min | **6.8 min** |

S&F put it exactly right: "only ¹⁸F [has] a sufficiently long life to permit
transport of radiopharmaceuticals to sites a few hours from the point of
preparation." A factor of 54 separates it from ¹⁵O. The other three need the
cyclotron **in the building** — and that, not the scanner, is what makes PET
expensive. SPECT escapes the whole problem by using ⁹⁹ᵐTc from a generator
(`~NE-26` §13.1): ship the 66-hour parent, elute the 6-hour daughter on site.

¹⁸F is also, independently, the best of the four on positron range (0.50 mm vs
2.52 mm for ¹⁵O). Two unrelated arguments picking the same nuclide is why FDG
became the workhorse of clinical PET.

**A caution on Table 14.5.** It is process → tracer and carries *no* energies or
half-lives; §14.1.7 names ⁹⁹ᵐTc, ¹²⁵I and ¹³¹I in prose. The quantitative SPECT
data in `code/medical.py` therefore comes from the repo's shared tables, not from
Chapter 14, and is labelled as such.

## 7. Therapy: nine ways of sharpening the same ratio

The quantity is the **therapeutic ratio**, tumour dose over normal-tissue dose,
and it must exceed 1 or there is no treatment. Sorting §14.5 by *how* each
modality raises it collapses eleven subsections into three ideas:

| how | modalities |
|---|---|
| **geometrically** | conformal (CRT), IMRT, stereotactic, teletherapy at higher energy |
| **physically** | electron beams (finite range), proton beams (**the Bragg peak**, `~NE-14`), brachytherapy ($1/r^2$ from inside) |
| **biochemically** | radionuclide therapy (¹³¹I to thyroid), BNCT (¹⁰B where the tumour is) |

The Bragg peak is the cleanest case and the direct payoff of `~NE-14`: a charged
particle deposits most of its energy at the *end* of its range, so a proton beam
can be stopped behind the tumour instead of continuing out through the patient.
Photons cannot do this — they attenuate exponentially and never stop.
Brachytherapy is the crudest and among the most effective: $1/r^2$ over 0.5 to
10 cm is a factor of **400**, obtained for free by placing the source inside.

Fractionation (2 Gy/day × 5 days × 6 weeks = 60 Gy) is the same optimisation in
time rather than space, and rests on the `~NE-18` distinction: normal tissue
repairs sublethal damage between fractions better than tumour does.

## 8. The numbers therapy is aimed at

Tables 14.6 and 14.7 (p. 541) support three statements in the text, and **all
three check out**:

- Table 14.6 sums **exactly** to its printed totals in all four columns
  (699,560 / 668,470 / 290,890 / 272,810) — a real check on a hand-typeset
  table, and one that failed for `~NE-22`'s Table 11.3.
- Those totals give the text's "1.37 million new cases" (1,368,030) and "564
  thousand deaths" (563,700).
- Table 14.7: lifetime incidence 46.6% for men — the text's "nearly half"; 38.0%
  for women, where "nearly half" is generous. Of those, 49% of men and 48% of
  women die of it — the text's "only about half ... survive".

Solid cancers are >90% of every column. Leukemia is rare and mostly fatal (86% of
male cases); thyroid cancer is the mirror image, more than twice as common in
women and rarely fatal (17% in men, 11% in women) — which is why `~NE-18` carries
a separate thyroid weighting rather than folding it into whole-body dose.

## Where this goes

| from | used here as |
|---|---|
| `~NE-11` attenuation | $\mu$ itself; the Hounsfield unit is $\mu$ rescaled |
| `~NE-12` photon interactions | photoelectric $Z^4/E^3$ = contrast; Compton = its loss |
| `~NE-14` charged particles | the Bragg peak; electron-beam range |
| `~NE-15` detectors | NaI(Tl) gamma cameras, PMT arrays, coincidence timing |
| `~NE-16` counting statistics | why sensitivity, not resolution, limits SPECT |
| `~NE-18` health effects | the dose that treats vs the dose that harms; fractionation |
| `~NE-26` production routes | proton-rich → β⁺ → cyclotron → short half-life → PET's cost |

## A note on what this module adds

The chapter is descriptive where it could be quantitative. Supplied here, each
pinned by a test:

- the **Hounsfield unit** and its −1000 floor (§14.1.5 defines neither);
- **Moseley's law** as the reason anode choice is energy choice;
- the **transport calculation** that turns S&F's sentence about ¹⁸F into 6.1 hours
  against 6.8 minutes;
- the **positron-range floor** and the $c\tau/2$ **timing length**, from the
  book's own 1 MeV → 4 mm and 10–25 ns;
- quantitative **SPECT tracer data**, sourced from `data_tables/` and cross-read
  by the tests, because Table 14.5 has none;
- the resolution of Fig. 14.16's **dimensionally impossible caption**, and the
  Nobel-year correction.
