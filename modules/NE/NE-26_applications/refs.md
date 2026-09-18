# NE-26 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |

## Topic → location

| Topic (code symbol) | Section | Printed p. | PDF p. |
|---|---|---|---|
| **Production of radioisotopes** (`PRODUCTION_ROUTES`) | §13.1 | 476–477 | 499–500 |
| Reactor irradiation; fission recovery; accelerators | §13.1 | 477 | 500 |
| **Radionuclide generators; the ⁹⁹Mo "cow"** (`GENERATORS`) | §13.1 | 477 | 500 |
| Industrial and research uses; the four categories | §13.2 | 477–479 | 500–502 |
| **Table 13.1** — the catalogue (`APPLICATION_CATEGORIES`) | Table 13.1 | 478 | 501 |
| Tracer applications | §13.3 | 479–482 | 502–505 |
| Leak detection; pipeline interfaces; flow patterns | §§13.3.1–13.3.3 | 480 | 503 |
| **Flow rate measurement** (`flow_rate_from_tracer`) | §13.3.4 | 480–481 | 503–504 |
| **Tracer dilution** (`tracer_dilution_volume`) | §13.3.6 | 481 | 504 |
| Wear, mixing, residence times, frequency response | §§13.3.7–13.3.11 | 481–482 | 504–505 |
| Radiodating | §13.3.12 | 482 | 505 |
| Materials affect radiation | §13.4 | 482–495 | 505–518 |
| **Radiography** (`geometric_unsharpness`) | §13.4.1 | 483–485 | 506–508 |
| **Table 13.2** — radiography sources (`RADIOGRAPHY_SOURCES`) | Table 13.2 | 484 | 507 |
| **Thickness gauging** (`gauge_precision`) | §13.4.2 | 485–487 | 508–510 |
| Density, level gauges; absorptiometry; well logging | §§13.4.3–13.4.6 | 487–488 | 510–511 |
| **Neutron activation analysis** (`naa_detectable_mass`) | §13.4.7 | 488–490 | 511–513 |
| **Table 13.3** — NAA sensitivities (`NAA_SENSITIVITY`) | Table 13.3 | 489 | 512 |
| Capture-gamma; XRF; PIGE; molecular structure | §§13.4.8–13.4.11 | 490–494 | 513–517 |
| Smoke detectors | §13.4.12 | 494–495 | 517–518 |
| Radiation affects materials | §13.5 | 495–500 | 518–523 |
| **Food preservation** (`PROCESS_DOSES`) | §13.5.1 | 495–496 | 518–519 |
| Sterilisation; insect control; polymer modification | §§13.5.2–13.5.4 | 496–498 | 519–521 |
| Particle accelerators for research | §13.6 | 500–510 | 523–533 |

## Three relations this module adds

Nothing in Chapter 13 was found to be wrong. It is a descriptive chapter and it
describes accurately. Three quantitative relations are absent, and each turns a
description into a design.

### The transmission-gauge optimum: µt = 2
§13.4.2 explains transmission thickness gauging in detail and never asks what
attenuation the gauge should be designed for. `~NE-16`'s counting statistics
answer it in three lines. With $N_0$ counts unattenuated and $N=N_0e^{-\mu t}$,
$$\sigma_N/N=1/\sqrt N,\qquad \frac{\sigma_t}{t}=\frac{e^{\mu t/2}}{\mu t\sqrt{N_0}},$$
and $\partial/\partial\mu$ at fixed $t$ gives $t/2=1/\mu$, i.e.

$$\boxed{\mu t = 2}$$

exactly. Two effects fight: more attenuation gives more signal per unit thickness
and fewer counts to measure it with.

It is also **forgiving** — within 25% of optimal over 0.9 to 3.6 mean free paths,
1.9× worse at 0.5 and 2.5× worse at 6 — which is why it is useful in practice and
not merely true. *Verified numerically in
`test_the_transmission_gauge_optimum_is_exactly_two_mean_free_paths`.*

### The generator ingrowth time
§13.1 calls ⁹⁹ᵐTc "the most widely used radioisotope in medical diagnoses" and
describes the ⁹⁹Mo cow without the transient equilibrium that operates it. From
the Bateman solution (`~NE-07`),
$$t_{\max}=\frac{\ln(\lambda_d/\lambda_p)}{\lambda_d-\lambda_p}=48.5\ \text{h},$$
and the daughter is already at 95% of that peak after 24 hours. That is the whole
basis of hospital logistics: generators are delivered weekly and eluted daily.
`optimal_milking_time`.

### Geometric unsharpness
$U_g=Fd/D$, the penumbra a finite source casts, which limits radiographic
resolution and is why sources are made small and placed far from the workpiece.
Not in §13.4.1. `geometric_unsharpness`.

## A rule that must be kept in its lane

The µt = 2 optimum applies to a **thickness gauge**, which minimises the variance
of a thickness estimate. It does **not** describe Table 13.2's radiography
practice:

| source | γ (MeV) | steel (cm) | µt |
|---|---|---|---|
| ¹⁷⁰Tm | 0.084 | 1.2 | 1.8 |
| ¹⁹²Ir | 0.34 | 7.5 | 5.6 |
| ¹³⁷Cs | 0.662 | 10 | 5.7 |
| ⁶⁰Co | 1.25 | 22 | 9.2 |

Two to nine mean free paths, because radiography maximises **contrast** through a
workpiece of *fixed* thickness rather than minimising the variance of a
measurement. Same attenuation law, different objective function.

The module keeps them apart deliberately, and
`test_radiography_is_not_run_at_the_gauge_optimum` asserts the discrepancy so
that a later reader cannot quietly "fix" it. A rule applied outside its objective
function is worse than no rule.

## Two other things worth recording

**§13.1's organising insight, stated plainly.** Reactor and fission routes give
*neutron-rich* products (β⁻); accelerators give *proton-rich* products (β⁺). That
is why every PET isotope comes from a cyclotron and none from a reactor
(`~NE-27`) — a fact of nuclear structure rather than of industrial history.

**Where the dose ladder starts.** §13.5's lowest process dose, 60 Gy for sprout
inhibition, is **seventeen times** `~NE-18`'s human LD50/60 of 3.5 Gy, and
sterilisation is 7000 times it. Food irradiation and human radiation exposure are
not the same phenomenon at different scales.

S&F also note that full radiation sterilisation of food "often is accompanied by
unacceptable changes in flavor, smell, color and texture" — the binding
constraint on the application is organoleptic, not radiological, which is a
useful corrective to assuming the physics is always what limits a technology.

## Cross-module dependencies
- **`~NE-06`, `~NE-07`** — activation kinetics and the Bateman solution behind
  §§1–2 of the notes.
- **`~NE-11`, `~NE-12`** — attenuation and the photon coefficients every gauge in
  §13.4 rests on.
- **`~NE-16`** — counting statistics; the gauge optimum is entirely its 1/√N.
- **`~NE-18`** — the dose scale §13.5 is measured against.
- **`~NE-23`** — where ¹³⁷Cs and ⁹⁰Sr sources come from.
- **`~NE-27`** — the medical half of the applications, and the destination of the
  cyclotron isotopes.

## Further reading
- IAEA, *Radiotracer Applications in Industry — A Guidebook* (TRS-423) — the
  tracer methods of §13.3 in operational detail.
- Halmshaw, R., *Industrial Radiology* — radiography including unsharpness,
  contrast and the source/thickness pairings of Table 13.2.
- Alfassi, Z.B. (ed.), *Activation Analysis* — NAA's sensitivities and the
  interference problems Table 13.3 assumes away.
- Knoll, G.F., *Radiation Detection and Measurement*, Ch. 20 — gauging and
  process control, including the statistics behind the µt optimum.
