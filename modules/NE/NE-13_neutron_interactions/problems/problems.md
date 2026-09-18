# NE-13 — Problems

Work each by hand, then check with `code/neutron_interactions.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1 follows
the book's Chapter 7 problem 16 (printed 219); P2 reproduces Example 7.5; P3–P7
are added. Cross sections from `../data_tables/C1_*.csv` and `../data_tables/C2_*.csv`.

### P1.  A resonance in iron  *(S&F Ch. 7, Prob. 16)*
From Fig. 7.7, iron's total cross section is about 0.4 b at 27 keV and about
90 b at 28 keV. Estimate the fraction of neutrons passing through a 10 cm slab
without interacting, at each energy.
*Check:* 88% at 27 keV; $3\times10^{-33}$ at 28 keV.

**Solution.** Iron: $\rho=7.874$ g/cm³, $A=55.85$, so
$$N=\frac{7.874\times6.022\times10^{23}}{55.85}=0.0849\times10^{24}\ \text{cm}^{-3}.$$

At 27 keV, $\Sigma_t=0.0849\times0.4=0.0340$ cm⁻¹, so $\Sigma_t x=0.340$ and
$$e^{-0.340}=\boxed{0.712}.$$

At 28 keV, $\Sigma_t=0.0849\times90=7.64$ cm⁻¹, $\Sigma_t x=76.4$, and
$$e^{-76.4}=\boxed{6\times10^{-34}}.$$

*(Using S&F's approximate read-off values; the point is the ratio, not the third
figure.)*

**A 1 keV change in energy — 3.7% — changes the transmitted fraction by 33
orders of magnitude.** Nothing in photon physics behaves remotely like this.
That is what a resonance is, and it is why:

- neutron transport cannot use a coarse energy grid the way photon transport
  can — codes carry hundreds to thousands of energy groups (`~NE-21`);
- "iron shields neutrons well" is a meaningless statement without specifying the
  energy;
- **resonance self-shielding** matters: the outer layer of a lump absorbs so
  strongly at the resonance energy that the interior never sees those neutrons,
  so the lump's effective cross section is far below its nominal one. This is
  exactly why reactor fuel is lumped into rods rather than dissolved in the
  moderator (`~NE-19`).

### P2.  Activating a manganese foil  *(S&F Example 7.5)*
2 g of ⁵⁵Mn is exposed for 2 minutes to a thermal flux of $10^{13}$ cm⁻² s⁻¹.
⁵⁵Mn(n,γ)⁵⁶Mn has $\sigma_\gamma=13.3$ b and ⁵⁶Mn has $T_{1/2}=2.579$ h. Find the
activity immediately after.
*Check:* book 2.609×10¹⁰ Bq; exact 2.598×10¹⁰ Bq.

**Solution.** The production rate is
$$R=\frac{mN_A}{A}\sigma_\gamma\phi
=\frac{2\times6.022\times10^{23}}{55}\times13.3\times10^{-24}\times10^{13}
=2.913\times10^{12}\ \text{s}^{-1},$$
and $\lambda=\ln2/(2.579\times3600)=7.466\times10^{-5}$ s⁻¹.

The book, stating that $t\ll T_{1/2}$, uses the linear form:
$$A\simeq\lambda Rt=2.913\times10^{12}\times7.466\times10^{-5}\times120
=\boxed{2.609\times10^{10}\ \text{Bq}}.$$

The exact form is the saturation law of `~NE-07`:
$$A=R\left[1-e^{-\lambda t}\right]=2.913\times10^{12}\times8.9189\times10^{-3}
=\boxed{2.598\times10^{10}\ \text{Bq}}.$$

The gap is 0.45%, and it is not arbitrary: expanding $1-e^{-x}\simeq x-x^2/2$
gives a relative error of exactly $\lambda t/2=0.448\%$. **The book's answer is
the high one**, because the linear form ignores the decay that occurs *during*
irradiation.

The approximation is safe here because $R$ has climbed only 0.9% of the way to
saturation. It would not be safe for a 3-hour irradiation of the same foil,
where the error reaches 25%. `activation_activity` therefore requires the
half-life explicitly rather than silently choosing a form.

### P3.  Why moderation pays for itself  *(added)*
A fission neutron is born at 2 MeV. Estimate what slowing it to thermal buys in
²³⁵U fission probability, and weigh that against the cost in collisions.
*Check:* ~600× in cross section; ~115 graphite collisions.

**Solution.** From the 1/v law anchored at thermal, dropping from 1 keV to
0.0253 eV multiplies an absorption cross section by
$$\sqrt{1000/0.0253}=199.$$
From 2 MeV the naive 1/v extrapolation would give $\sqrt{2\times10^6/0.0253}
=8900$, but 1/v does not hold through the resonance region, so the honest
comparison is measured: $\sigma_f(^{235}\text{U})$ is 587 b thermal against
roughly 1 b at 1 MeV — **about 600×**.

The cost, from `~NE-08`, is 115 elastic collisions in graphite (18 in hydrogen),
each of which risks capture. So moderation trades ~10² collisions for ~10³ in
reaction probability: worth it by an order of magnitude, and the margin is what
makes thermal reactors possible with only 0.7%-enriched uranium.

A fast reactor declines this trade deliberately. It runs at ~1 b instead of
587 b and compensates with **much higher fuel enrichment and a much larger
neutron population** — which is exactly why fast reactors need 15–20% enrichment
or plutonium fuel while thermal reactors run on 3–5%.

### P4.  Why ¹⁰B and not ¹¹B  *(added)*
Boron carbide (B₄C) is the standard control-rod material. Natural boron is 19.9%
¹⁰B and 80.1% ¹¹B. Compute the absorption cross section of natural boron and of
enriched ¹⁰B, and explain the enrichment.
*Check:* natural 764 b; ¹⁰B 3840 b.

**Solution.** From Table C.1, $\sigma_a(^{10}\text{B})=3840$ b (essentially all
$(n,\alpha)$) and $\sigma_a(^{11}\text{B})=0.00553$ b. Atom-weighted,
$$\bar\sigma_a=0.199(3840)+0.801(0.00553)=\boxed{764\ \text{b}},$$
so **¹¹B contributes 0.0004 b of the 764 — one part in two million.** Natural
boron is, for neutron purposes, 19.9% useful material and 80.1% inert filler.

Enriching to pure ¹⁰B multiplies the cross section by 5.0, letting a control rod
be five times thinner or five times more effective at the same size. That is why
enriched ¹⁰B is used where space is tight, despite the cost.

The ¹⁰B(n,α)⁷Li reaction is doubly convenient: the products are charged and
stop locally (no penetrating secondary radiation, unlike a capture gamma), and
the reaction has no resonances — it is 1/v over the whole thermal and epithermal
range, so a boron rod's worth is predictable rather than energy-dependent. Both
properties are why boron also lines neutron detectors (`~NE-15`).

### P5.  η, not ν, is what must exceed one  *(added)*
Compute η for ²³³U, ²³⁵U and ²³⁹Pu and explain why ²³³U is the best of the three
despite having the smallest ν.
*Check:* 2.28, 2.08, 2.11.

**Solution.** $\eta=\nu\sigma_f/\sigma_a$ with $\sigma_a=\sigma_f+\sigma_\gamma$:

| | $\nu$ | $\sigma_f$ | $\sigma_\gamma$ | $\alpha$ | $\eta$ |
|---|---|---|---|---|---|
| ²³³U | 2.48 | 529 | 46 | 0.087 | **2.282** |
| ²³⁵U | 2.43 | 587 | 99 | 0.169 | 2.078 |
| ²³⁹Pu | 2.87 | 749 | 271 | 0.362 | 2.107 |

²³⁹Pu produces the most neutrons per fission by a wide margin (2.87 against
2.48), and still ends up **below** ²³³U per neutron absorbed. The reason is
entirely $\alpha$: 27% of ²³⁹Pu's thermal absorptions are captures rather than
fissions, against 8% for ²³³U.

Two consequences. **Breeding** requires $\eta>2$ — one neutron to sustain the
chain, one to convert a fertile nucleus, plus margin for leakage and parasitic
absorption. All three clear 2, but only just, and only ²³³U clears it
comfortably *in a thermal spectrum*. That is the technical case for the
thorium–²³³U cycle, and why the alternative (²³⁸U→²³⁹Pu) is pursued in **fast**
spectra instead, where ²³⁹Pu's η rises to about 2.4.

The second consequence is `~NE-19`: η is the first of the four factors, and
everything else in the four-factor formula is a number less than 1 eating into
it.

### P6.  A moderator must scatter and not absorb  *(added)*
Rank ¹H, ²H and ¹²C as moderators using both ξ (from `~NE-08`) and the
scattering-to-absorption ratio.
*Check:* σ_s/σ_a = 92 (¹H), 8400 (²H), 1394 (¹²C).

**Solution.** Two properties matter and they pull in opposite directions.

| | $\xi$ | collisions to thermal | $\sigma_s/\sigma_a$ |
|---|---|---|---|
| ¹H | 1.000 | 18 | **92** |
| ²H | 0.725 | 25 | **8400** |
| ¹²C | 0.158 | 115 | **1394** |

Hydrogen slows neutrons fastest — one collision can stop a neutron dead
(`~NE-08`) — but absorbs 92× less often than it scatters, which sounds fine
until you multiply by 18 collisions: about 18% of neutrons are lost. That is
survivable only with enriched fuel, which is exactly why **light-water reactors
cannot run on natural uranium**.

Deuterium slows more slowly (25 collisions) but absorbs 8400× less often, losing
only ~0.3%. Heavy water is the reason **CANDU reactors run on natural uranium**
and need no enrichment plant at all — a proliferation-relevant difference that
follows directly from one cross-section ratio.

Graphite sits in between and has the advantage of being a cheap solid.

The proper figure of merit combines both, the **moderating ratio**
$\xi\Sigma_s/\Sigma_a$, which `~NE-19` develops. The lesson here is that ξ alone
ranks ¹H first and the full picture ranks ²H first.

### P7.  Where a fission neutron has to survive  *(added)*
Explain, using §3 of the notes, why reactor fuel is fabricated into rods rather
than dissolved uniformly in the moderator.
*Check:* ²³⁸U's capture resonances sit at eV energies, < 1 eV wide.

**Solution.** A neutron born at 2 MeV must reach 0.025 eV. On the way down it
passes through the eV region, where ²³⁸U has narrow, extremely tall capture
resonances (heavy nuclide: eV energies, <1 eV widths). Every neutron captured
there is lost from the chain, and ²³⁸U is 99.3% of the fuel.

Two geometries:

- **Homogeneous** (fuel dissolved in moderator): a neutron slowing down is
  always adjacent to ²³⁸U, so it passes through the resonance energies *in the
  presence of* the absorber. Capture probability is high.
- **Heterogeneous** (fuel lumped into rods): most of the slowing-down happens in
  the moderator *between* rods, where there is no ²³⁸U. A neutron crosses the
  dangerous energy band in a region where the absorber is absent, then re-enters
  the fuel already thermal, where ²³⁵U's 587 b is waiting.

There is a second, reinforcing effect. At a resonance energy the fuel's cross
section is so large that the outer skin of a rod absorbs essentially everything —
**resonance self-shielding** — so the interior of the rod is shadowed and the
lump's effective resonance absorption is far below what its mass suggests.

Both effects raise the resonance escape probability, and both require the fuel to
be *spatially separated* from the moderator. This is why every thermal power
reactor ever built uses discrete fuel rods, and it is a design consequence that
falls directly out of the resonance widths in §3.
