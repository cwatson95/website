# NE-06 — Decay kinetics (notes)

`~NE-05` established *which* way a nuclide decays and *how much* energy comes
out. This module answers *how fast*, and it is shorter than the others because
the whole subject follows from a single assumption.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed., §5.5,
cited by **printed** page (PDF = printed + 23). Half-lives from
`../data_tables/A4_isotopic_abundances.csv`.

## 1. One assumption, and everything else

A nucleus has a **constant probability per unit time** of decaying, independent
of its history and of its neighbours [S&F Eq. (5.32)]:
$$\lambda\equiv\lim_{\Delta t\to0}\frac{P(\text{decay in }\Delta t)}{\Delta t}.$$
For a population of $N$ identical nuclei the expected number decaying in $dt$ is
$\lambda N\,dt$, so [S&F Eq. (5.33)]
$$\frac{dN}{dt}=-\lambda N
\quad\Longrightarrow\quad
\boxed{\;N(t)=N_0e^{-\lambda t}\;}$$
[S&F Eq. (5.34)] — `number_remaining`. Every other result in this module is a
rearrangement of that exponential.

**Half-life** [S&F Eqs. (5.35)–(5.36)]. Setting $N=N_0/2$,
$$T_{1/2}=\frac{\ln2}{\lambda}=\frac{0.693}{\lambda},$$
`decay_constant` and `half_life`. Equivalently $N(t)=N_0(1/2)^{t/T_{1/2}}$
[S&F Eq. (5.39)], and the number of half-lives to reach a surviving fraction $f$
is $n=-\log_2 f=-1.443\ln f$ [S&F Eq. (5.38)] — `half_lives_elapsed`.

**Mean life** [S&F Eq. (5.44)]. The decay time is a random variable with density
$p(t)=\lambda e^{-\lambda t}$ [S&F Eq. (5.43)], and its mean is
$$T_{\text{av}}=\int_0^\infty t\lambda e^{-\lambda t}\,dt=\frac{1}{\lambda}
=\frac{T_{1/2}}{\ln2}=1.443\,T_{1/2}.$$
`mean_lifetime`. The mean life exceeds the half-life by 44%, because the
exponential's long tail drags the mean above the median. Confusing the two is a
common slip; `test_mean_life_is_1_44_half_lives` pins it.

**Memorylessness.** $P(\text{survive to }t)=e^{-\lambda t}$ [S&F Eq. (5.40)] does
not depend on how long the nucleus has already existed:
$$\frac{P(\text{survive }a+T)}{P(\text{survive }a)}=e^{-\lambda T}=\tfrac12
\quad\text{for every }a.$$
A nucleus does not age (`test_decay_is_memoryless`). "How old is this atom?" has
no answer; only "how old is this *sample*?" does, and that is `~NE-07`'s
radiodating. For small intervals $P(\Delta t)\simeq\lambda\Delta t$
[S&F Eq. (5.42)] — the approximation behind every reaction-rate estimate in
`~NE-11`.

This is the same mathematics as the exponential distribution of `~ST-11` and as
Beer's law for photon attenuation in `~NE-11`: one differential equation, three
physical readings. In `~NE-11` the independent variable is distance rather than
time, and $\lambda$ becomes the linear attenuation coefficient.

## 2. Activity — what is actually measured

You never count nuclei; you count decays. The **activity** is
[S&F Eq. (5.45)]
$$A(t)\equiv-\frac{dN}{dt}=\lambda N(t)=A_0e^{-\lambda t},$$
`activity` and `activity_at_time`. It decays with the same constant as the
population. Units:

- **becquerel** (Bq) = one decay per second (SI);
- **curie** (Ci) $=3.7\times10^{10}$ Bq, *defined* so as to be the activity of
  one gram of ²²⁶Ra.

`curies` and `becquerels` convert. The historical definition is worth checking:
`specific_activity(half_life_of("226Ra"), 226)` gives $3.658\times10^{10}$ Bq/g
$=0.9886$ Ci/g. Not exactly 1.000, and the reason is instructive — the curie is
now *fixed* at $3.7\times10^{10}$ Bq exactly, while radium's half-life has since
been revised upward. The 1.1% gap is a century of metrology, not an arithmetic
error (`test_one_gram_of_radium_is_about_one_curie`).

## 3. Specific activity, and the inversion that organises the subject

For a pure sample, activity per gram is
$$\mathrm{SA}=\lambda N=\frac{\ln2}{T_{1/2}}\cdot\frac{N_A}{A},$$
`specific_activity`. Note the **inverse** dependence on half-life:

| nuclide | $T_{1/2}$ | Ci/g |
|---|---|---|
| ³H | 12.3 y | $9.67\times10^{3}$ |
| ⁶⁰Co | 5.27 y | $1.13\times10^{3}$ |
| ⁹⁰Sr | 28.8 y | $1.38\times10^{2}$ |
| ¹³⁷Cs | 30.2 y | $8.65\times10^{1}$ |
| ²²⁶Ra | 1600 y | $9.89\times10^{-1}$ |
| ²³⁸U | 4.47 Gy | $3.36\times10^{-7}$ |

Ten orders of magnitude between tritium and uranium. **The most intensely
radioactive nuclides are the ones that disappear fastest**, and the two
properties cannot be separated — they are the same parameter. Almost all of
radiological protection follows from this trade-off (`~NE-18`): a short-lived
nuclide is a severe hazard now and gone in a year; a long-lived one is a mild
hazard that must be contained for geological time. Nuclear waste is difficult
precisely because it contains both (`~NE-23`).

## 4. Competing decay channels

When a nuclide can decay several ways — ⁴⁰K by both $\beta^-$ and EC
(`~NE-05`) — the channels are independent, so their **rates** add
[S&F Eqs. (5.47)–(5.48)]:
$$\frac{dN}{dt}=-\sum_i\lambda_iN\equiv-\lambda N,\qquad \lambda=\sum_i\lambda_i,$$
`total_decay_constant`. Half-lives do **not** add; the combined half-life is
shorter than any individual channel's. The fraction of decays going by channel
$i$ is the branching ratio [S&F Eq. (5.49)]
$$f_i=\frac{\lambda_i}{\lambda},$$
`branching_fractions`, and the *partial* half-life a channel would have on its own
is $T_i=T_{1/2}/f_i$ — always longer than the observed half-life
(`partial_half_life`). Quoting a partial half-life as if it were observable is a
routine confusion; for ⁴⁰K the observed 1.28 Gy corresponds to partial half-lives
of 1.43 Gy ($\beta^-$, 89.3%) and 11.9 Gy (EC, 10.7%).

## 5. Reading half-lives out of the data

`parse_half_life` converts the strings Appendix A.4 prints — `"12.32 y"`,
`"5.70 ky"`, `"704 My"`, `"stable"`, even the limit `">600 Ty"` — into seconds,
handling the SI-prefixed year units the book uses ($\mathrm{ky}=10^{3}$ y through
$\mathrm{Ey}=10^{18}$ y). `load_half_lives` builds the whole table, 918 nuclides,
and `test_known_half_lives_from_appendix_a4` validates ten of them against
standard values (³H 12.32 y, ¹⁴C 5700 y, ⁶⁰Co 5.2714 y, ²³⁵U 704 My,
²³⁸U 4.468 Gy, ²³⁹Pu 24110 y, …).

The span is worth noticing: the tabulated half-lives run from hours to $10^{18}$
years — twenty-two orders of magnitude — all governed by the same exponential.
Nothing else in the trunk has that dynamic range, and it is why `~NE-07`'s decay
chains behave as they do: a chain whose members differ by ten orders of magnitude
in $\lambda$ reaches secular equilibrium, in which the slowest step alone sets the
pace.

## Where this goes

- `~NE-07` — chains of decays, the Bateman equations, secular equilibrium, and
  radiodating.
- `~NE-11` — the identical mathematics with distance replacing time: $e^{-\mu x}$.
- `~NE-16` — counting statistics: activity is a *rate*, so counts are Poisson
  (`~ST-09`) and the uncertainty on a measured activity is $\sqrt N$.
- `~NE-18` — specific activity and half-life set the hazard from a given nuclide.
- `~NE-20` — the same first-order kinetics, with a production term, becomes
  reactor point kinetics and fission-product poisoning.
