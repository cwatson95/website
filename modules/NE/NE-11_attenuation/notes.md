# NE-11 — Attenuation, cross sections, flux density and reaction rates (notes)

Chapters 3–6 asked *whether* a reaction can happen and *how much energy* it
releases. Neither question is enough to build anything. A reactor designer needs
the fission **rate**; a shield designer needs the dose **behind the wall**; a
detector designer needs the **count rate**. All three are the same calculation,
and this module is that calculation.

It rests on two quantities and one product.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§7.1–7.2, cited by **printed** page (PDF = printed + 23). Coefficients from
`../data_tables/C3_photon_coefficients_*.csv` and
`../data_tables/C1_thermal_neutron_cross_sections.csv`.

## 1. The interaction coefficient, and why you already know it

Define [S&F Eq. (7.1)]
$$\mu_i\equiv\lim_{\Delta x\to0}\frac{P_i(\Delta x)}{\Delta x},$$
the probability per unit path length of interaction $i$. It is called the
**linear interaction coefficient** in photon work and the **macroscopic cross
section** $\Sigma_i$ in neutron work; they are the same thing. Channels add
[Eq. (7.2)]: $\mu_t=\sum_i\mu_i$.

Now notice what this is. $\mu$ is a constant probability per unit *distance*,
exactly as the decay constant $\lambda$ of `~NE-06` is a constant probability per
unit *time*. Every result transfers:

| decay (`~NE-06`) | attenuation (here) |
|---|---|
| $\lambda$, per unit time | $\mu$, per unit distance |
| $N(t)=N_0e^{-\lambda t}$ | $I^o(x)=I^o(0)e^{-\mu x}$ [Eq. (7.4)] |
| $p(t)=\lambda e^{-\lambda t}$ | $p(x)=\mu e^{-\mu x}$ [Eq. (7.7)] |
| mean life $1/\lambda$ | **mean free path** $1/\mu$ [Eq. (7.8)] |
| half-life $\ln2/\lambda$ | **half-thickness** $\ln2/\mu$ [Eq. (7.9)] |
| decay is memoryless | interaction is memoryless |

The memorylessness is worth pausing on. A photon that has already crossed 50 cm
of water is exactly as likely to survive the next centimetre as one that just
entered. Radiation does not wear out; it is removed, one all-or-nothing event at
a time. `test_probabilities_are_complementary_and_memoryless` checks it directly.

The practical consequence is that **the only variable that matters is the product
$\mu x$** — the optical thickness, measured in mean free paths. Ten centimetres
of lead and 109 cm of water are the same shield because both are 7.7 mfp. Shield
designers think in mfp for this reason, and `mean_free_paths_traversed` exists to
encourage it.

**Example 7.1** [printed p. 182]: how much shielding reduces a 1 MeV beam
tenfold? $x_{1/10}=\ln10/\mu$, giving 32.6 cm of water or 2.98 cm of lead. Both
reproduce exactly from the extracted Appendix C.3.

## 2. The caveat that matters most: uncollided ≠ total

Equation (7.4) tracks **uncollided** particles only. A photon that Compton
scatters is not gone — it is still in the shield, at lower energy and a new
direction, and it can still emerge and deliver dose. The true field is
[S&F §7.1.5]
$$I(x)=B(x)\,I^o(x),\qquad B\ge1,$$
where $B$ is the **buildup factor**, obtained from transport calculations that
are well beyond this book (and this module — `buildup_intensity` applies whatever
$B$ the caller supplies).

This is not a small correction. For a metre of concrete against MeV photons $B$
is of order 10. **A shield designed on exponential attenuation alone is
under-designed by an order of magnitude.** Exponential attenuation is a lower
bound on the field, and it should always be read as one.

## 3. From microscopic to macroscopic

The bridge is one equation [Eq. (7.10)]:
$$\mu_i=\sigma_i N=\sigma_i\frac{\rho N_a}{A},$$
a per-atom effective area $\sigma$ (the **microscopic cross section**, measured
in **barns**, $10^{-24}$ cm²) times an atom density $N$. Dividing by density
gives [Eq. (7.11)]
$$\frac{\mu_i}{\rho}=\frac{N_a}{A}\sigma_i,$$
which is **intrinsic** — independent of how the material is packed. Liquid water
and water vapour have the same $\mu/\rho$ and wildly different $\mu$. That is why
Appendix C.3 tabulates the ratio, and why one table serves for any density.

The barn is sized so that $1\ \text{b}\times10^{24}\ \text{cm}^{-3}=1\ \text{cm}^{-1}$
exactly, which is why atom densities in this field are habitually quoted in units
of $10^{24}$ cm⁻³: the exponents cancel and $\Sigma$ falls out directly.

A caution about the word *area*. $\sigma$ has the dimensions of area and is
often described as the target's effective size, which is a useful picture until
one notices that $\sigma$ depends on the incident energy — and, in a crystal, on
direction. Nothing physical changes size. The honest reading is the one S&F
give: $\sigma$ is the interaction probability per unit path length, normalised to
one target atom per unit volume.

**Mixtures and compounds.** Linear coefficients add by volume [Eq. (7.12)],
mass coefficients by weight fraction [Eq. (7.13)]:
$$\frac{\mu}{\rho}\bigg|_{\text{mix}}=\sum_jw_j\left(\frac{\mu}{\rho}\right)_j.$$
**Example 7.2** [printed p. 184] mixes iron and lead half-and-half by weight at
1 MeV: $(\mu/\rho)_{\text{mix}}=0.06377$ cm²/g, $\rho_{\text{mix}}=9.298$ g/cm³,
$\mu=0.5929$ cm⁻¹. (The example prints an iron density its own arithmetic
contradicts — see `refs.md`.)

**Example 7.3** [printed p. 184] does the neutron version for water, summing
over all five stable isotopes of hydrogen and oxygen to get
$\Sigma_a=0.0223$ cm⁻¹. The instructive part is what the example then observes:
**¹H alone gives the same 0.0223**. The other four terms vanish for two different
reasons — ¹⁶O is abundant but nearly transparent (0.00019 b), while ¹⁷O absorbs
1250 times more strongly but is 0.04% abundant. Cross section and abundance
*multiply*, so a term needs both to be large. Neither factor alone tells you
whether a nuclide matters.

(A trap in that example: "absorption" means **every** channel that removes the
neutron — $(n,\gamma)$, $(n,\alpha)$, $(n,p)$, $(n,f)$ — but not scattering.
¹⁷O's 0.239 b is mostly $(n,\alpha)$, not capture; reading the capture column
alone understates it sixtyfold. `absorption_cross_section` sums them.)

## 4. Flux density, and the equation everything reduces to

To get a *rate* we need a measure of "how much radiation is here". Beam intensity
works for a beam and fails for a field going in all directions at once. The
useful measure is the **flux density** [Eq. (7.14)]
$$\phi(\mathbf r)\equiv v\,n(\mathbf r).$$

Read it as **total particle track length per unit volume per unit time**, not as
"flow through an area". The track-length reading is what makes the next step
obvious, and it works regardless of direction — which is the whole point, since
inside a reactor or a shield the radiation goes everywhere.

Then, since $1/\mu_i$ is the mean distance a particle travels per interaction of
type $i$, and $\phi$ is the distance travelled per cm³ per second,
$$\boxed{\;\hat R_i(\mathbf r)=\mu_i\,\phi(\mathbf r)\;}$$
[Eqs. (7.15)–(7.16)]. **This is the most-used equation in nuclear engineering.**
Reactor power is $\Sigma_f\phi$ times 200 MeV; a detector's count rate is
$\mu_d\phi$ times its volume; tissue dose is $\mu_{en}\phi$ times the energy.
Same product, different subscript.

Generalised to energy and time [Eqs. (7.17)–(7.19)] it becomes the integral that
every reactor-physics code evaluates:
$$\text{fissions in }(t_1,t_2)=\int_{t_1}^{t_2}\!\!dt\int_V\!\!dV\int_0^{E_{\max}}\!\!dE\;
\Sigma_f(\mathbf r,E,t)\,\phi(\mathbf r,E,t).$$

**Fluence** is the time integral of flux density [Eq. (7.21)],
$\Phi=\int\phi\,dt$. Flux density measures the *rate* of interactions; fluence
measures their *cumulative number*. Dose limits are written against fluence
(`~NE-17`), while reactor power is written against flux — the distinction is
exactly the one between activity and total decays in `~NE-06`.

## 5. Point sources: two attenuations that behave differently

An isotropic point source emitting $S_p$ per second gives, in vacuum
[Eq. (7.23)],
$$\phi^o(r)=\frac{S_p}{4\pi r^2},$$
and with attenuating material in the way [Eqs. (7.25)–(7.27)],
$$\phi^o(r)=\frac{S_p}{4\pi r^2}\exp\left(-\sum_i\mu_it_i\right).$$

The two factors are worth separating because they behave *completely
differently*:

- **Geometric attenuation**, $1/r^2$: a power law. Free, but weak. Ten times
  further away buys a factor of 100 — and then you have run out of room.
- **Material attenuation**, $e^{-\mu t}$: an exponential. Expensive, but
  unboundedly strong. 10 cm of lead buys a factor of 2300 against a 1 MeV source,
  and *the next 10 cm buys the same factor again*.

At one metre from a 1 Ci 1 MeV source, 10 cm of lead beats retreating to ten
metres by a factor of 23. That asymmetry is why radiation protection is built on
**time, distance and shielding** in that order of increasing cost and increasing
power — and why the exponent in Eq. (7.27) is a sum of $\mu_it_i$: **shields
compose by optical thickness, not by centimetres.**

## Where this goes

- `~NE-12` — the photon $\mu/\rho$ used here, decomposed into photoelectric,
  Compton and pair production, and the $Z$ and $E$ dependence of each.
- `~NE-13` — the neutron cross sections: 1/v absorption, resonances, and why
  $\sigma$ varies over six orders of magnitude across the resonance region.
- `~NE-14` — charged particles, which do *not* obey any of this: they lose energy
  continuously and have a definite range rather than an exponential tail.
- `~NE-15`, `~NE-16` — detectors count $\mu_d\phi V$; the statistics of that
  count are Poisson.
- `~NE-17` — dose is $\mu_{en}\phi E/\rho$; the `en` column of Appendix C.3
  loaded here is exactly the one dosimetry needs.
- `~NE-19`, `~NE-21` — $\Sigma_f\phi$ is reactor power; the flux density this
  module takes as given is what diffusion theory computes.
