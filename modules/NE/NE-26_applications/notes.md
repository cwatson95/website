# NE-26 — Industrial & research applications: tracers, radiography, NAA (notes)

Chapter 13 is a **catalogue** — three dozen applications — and S&F organise it by
what is physically happening, which is the right cut:

| | |
|---|---|
| **radiation as a label** | tracers: leaks, flows, wear, mixing, residence times, dating |
| **materials affect radiation** | gauges (thickness, density, level), radiography, NAA, XRF, PIGE, smoke detectors |
| **radiation affects materials** | sterilisation, food preservation, polymer cross-linking, insect control |
| **nuclear energy as heat** | `~NE-22`, `~NE-25` |

Almost none of it needs new physics. It needs `~NE-06`, `~NE-11` and `~NE-12`
applied **with an eye on the sensitivity** — and that is where the chapter stops
short.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., Ch. 13,
cited by **printed** page (PDF = printed + 23).

## 1. The production route decides the decay mode

§13.1's organising insight, worth stating plainly because everything downstream
follows from it:

| route | product | decays by |
|---|---|---|
| reactor irradiation | neutron-rich | β⁻ (+ γ) |
| fission-product recovery | neutron-rich | β⁻ |
| **accelerator** | **proton-rich** | **β⁺** |

**Every PET isotope comes from a cyclotron and none comes from a reactor**
(`~NE-27`), and that is not an accident of industrial history — it is a
consequence of which side of the valley of stability each route lands on.

Activation saturates: $A(t)=R(1-e^{-\lambda t})$. Three half-lives buys 87.5%
and the next seven buy twelve percentage points, so nobody irradiates for ten.

## 2. The ⁹⁹Mo cow

S&F call ⁹⁹ᵐTc "the most widely used radioisotope in medical diagnoses" and
describe the generator without the transient equilibrium that operates it. From
the Bateman solution (`~NE-07`), ingrowth peaks at
$$t_{\max}=\frac{\ln(\lambda_d/\lambda_p)}{\lambda_d-\lambda_p}=48.5\ \text{hours}.$$

Two days — and the activity is already at 95% of the peak after 24 hours. That is
exactly why hospital generators are **delivered weekly and eluted daily**.

The generator is a way to ship a 6-hour isotope by shipping a 66-day one, and the
¹³⁷Cs/¹³⁷ᵐBa pair takes it to the extreme: a 30-year parent for a 2.5-minute
daughter, a ratio of six million.

## 3. Tracers: the ratio is the whole trick

**Dilution** [§13.3.6]: $V=V_0(C_0/C)$. Only the *ratio* enters — detector
efficiency, geometry and absolute calibration all cancel. Measure the same sample
twice on the same instrument and divide. That is why one technique serves a river
estuary, a blast furnace and a human bloodstream.

**Rate balance** [§13.3.4]: inject at a constant $Q_0$ Bq/s, and in steady state
the tracer must reappear downstream at the same rate, so $q=Q_0/C$ — **with no
knowledge of the channel's cross-section at all**. That is why it is the river
method, while the peak-to-peak transit method (which needs a known area) is the
pipeline method.

## 4. The design rule Chapter 13 does not contain

§13.4.2 describes transmission thickness gauging without asking what attenuation
the gauge should be *designed* for. Counting statistics answer it in three lines.
With $N_0$ counts unattenuated,
$$\frac{\sigma_t}{t}=\frac{e^{\mu t/2}}{\mu t\sqrt{N_0}},$$
and minimising over $\mu$ at fixed $t$ gives
$$\boxed{\mu t=2}$$
**exactly** — two mean free paths. More attenuation gives more signal per unit
thickness (the $\mu t$ downstairs) and fewer counts (the exponential); the optimum
is where they balance.

It is also forgiving: anything from 0.9 to 3.6 mfp is within 25% of the best
achievable, 1.9× worse at 0.5 and 2.5× worse at 6. That tolerance is why the rule
is useful in practice and not merely true.

**And it does not describe radiography.** Table 13.2's source/thickness pairs run
**2 to 9** mean free paths, because radiography maximises *contrast* through a
workpiece of fixed thickness rather than minimising the variance of a thickness
estimate. Same attenuation law, different objective function — and conflating the
two is the obvious way to misuse the rule.

## 5. NAA is exquisite and narrow

Table 13.3 spans **seven decades**: europium at 0.9 picograms (about four billion
atoms) and iron at 10 micrograms. The spread is set by two things the method
cannot control — the activation cross section, and whether the product emits a
gamma distinguishable from everything else in the sample.

So NAA is not a general assay. §13.4.7 is careful to list what it is *used* for —
forensic trace signatures, geological samples, pesticide residues, vanadium in
refined oil — rather than claiming it is universal, and the table shows why.

## 6. "Irradiation" spans a factor of 400

| process | dose |
|---|---|
| sprout inhibition (potatoes, onions) | 60–150 Gy |
| insect disinfestation (grain) | 200–500 Gy |
| pasteurisation (milk, poultry) | 1–10 kGy |
| food sterilisation | 20–50 kGy |
| medical sterilisation | 25 kGy |

Note where the ladder *starts*. The lowest process dose is **seventeen times**
`~NE-18`'s human LD50/60 of 3.5 Gy. Food irradiation and radiation exposure are
not the same phenomenon at different scales; they are not on the same scale at
all.

S&F also note that full sterilisation of food "often is accompanied by
unacceptable changes in flavor, smell, color and texture" — which is the real
reason the technology is not routine, and a useful reminder that the binding
constraint on an application is often not the physics.

## Where this goes

- `~NE-06` — decay and activation kinetics; §1 and §2 are that chapter applied.
- `~NE-07` — the Bateman solution behind the generator.
- `~NE-11`, `~NE-12` — attenuation and the photon coefficients every gauge uses.
- `~NE-16` — counting statistics; §4's design rule is entirely `~NE-16`'s $1/\sqrt N$.
- `~NE-18` — the dose scale §6 is measured against.
- `~NE-27` — medical applications, and where the cyclotron isotopes go.

## A note on what this module adds

Nothing in Chapter 13 was found to be wrong. It is a descriptive chapter and it
describes accurately. Three quantitative relations are missing, and each converts
a description into a design:

1. **The gauge optimum, $\mu t=2$.** Derived from `~NE-16`'s counting statistics;
   the single most useful design rule in the chapter, and absent from it.
2. **The generator ingrowth time, 48.5 h.** The Bateman peak for ⁹⁹Mo/⁹⁹ᵐTc,
   which is what actually determines hospital logistics.
3. **Geometric unsharpness**, $U_g=Fd/D$ — the penumbra that limits radiographic
   resolution and explains why sources are small and placed far away.

The module also keeps the gauge optimum and radiography *apart*, because Table
13.2 shows they are different problems, and a rule applied outside its objective
function is worse than no rule.
