# NE-07 — Decay chains, equilibria and radiodating (notes)

`~NE-06` followed one nuclide decaying alone. Real radioactivity almost never
looks like that: a parent decays to a daughter that decays in turn, and every
member is simultaneously being created and destroyed. Adding a source term to
the first-order equation of `~NE-06` covers both cases that matter — production
by irradiation, and production by a parent's decay.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§5.6–5.9, cited by **printed** page (PDF = printed + 23). Half-lives from
`../data_tables/A4_isotopic_abundances.csv`.

## 1. Decay with production, and saturation

With a creation rate $Q(t)$ [S&F Eqs. (5.50)–(5.51), p. 117]
$$\frac{dN}{dt}=-\lambda N+Q(t),$$
whose general solution is [S&F Eq. (5.52)]
$$N(t)=N_0e^{-\lambda t}+\int_0^t Q(t')e^{-\lambda(t-t')}dt' .$$
For constant $Q_0$ this integrates to [S&F Eq. (5.53)]
$$\boxed{\;N(t)=N_0e^{-\lambda t}+\frac{Q_0}{\lambda}\big[1-e^{-\lambda t}\big]\;}$$
— `decay_with_production`. As $t\to\infty$, $N\to N_e=Q_0/\lambda$
(`equilibrium_number`), and the corresponding **activity is $\lambda N_e=Q_0$**:
at saturation the sample decays exactly as fast as it is being made. You cannot
irradiate a target to an activity greater than its production rate, however long
you leave it in.

`approach_fraction` gives $1-e^{-\lambda t}$, the fraction of saturation reached:

| irradiation time | fraction of saturation |
|---|---|
| 1 half-life | 0.500 |
| 2 | 0.750 |
| 3 | 0.875 |
| 5 | 0.969 |
| 10 | 0.999 |

This is the rule of thumb behind every activation calculation (`~NE-26`):
irradiating for more than about five half-lives of the product buys almost
nothing. It is also why short-lived medical isotopes are made close to the point
of use.

## 2. The Bateman chain

For a chain $X_1\to X_2\to\cdots\to X_n$ each member obeys
[S&F Eq. (5.68), p. 122]
$$\frac{dN_1}{dt}=-\lambda_1N_1,\qquad
\frac{dN_j}{dt}=\lambda_{j-1}N_{j-1}-\lambda_jN_j,$$
production from above, loss from below. With a pure parent at $t=0$ the solution
is a sum of exponentials [S&F Eq. (5.69)]
$$A_j(t)=\lambda_jN_j(t)=N_1(0)\sum_{m=1}^{j}C_me^{-\lambda_mt},$$
with coefficients fixed entirely by the decay constants [S&F Eq. (5.70)]
$$C_m=\frac{\prod_{i=1}^{j}\lambda_i}{\prod_{i=1,\,i\neq m}^{j}(\lambda_i-\lambda_m)} .$$
`bateman_coefficients`, `bateman_activity` and `bateman_number` implement these;
`test_bateman_satisfies_the_chain_odes` checks numerically that the result really
does solve the system, and `test_daughters_start_at_zero_and_the_parent_at_n0`
checks the initial conditions.

Note the failure mode: equal decay constants make a denominator vanish. That is
not a bug in the formula but a genuine degeneracy needing a separate (polynomial
times exponential) solution, and `bateman_coefficients` raises rather than
returning nonsense.

**The two-member case** is worth knowing by heart (`two_component_chain`):
$$N_2(t)=N_1(0)\frac{\lambda_1}{\lambda_2-\lambda_1}
\big[e^{-\lambda_1t}-e^{-\lambda_2t}\big].$$
The daughter starts at zero, rises, peaks, and falls. It peaks when production
equals loss, $\lambda_1N_1=\lambda_2N_2$, at
$$t_{\max}=\frac{\ln(\lambda_2/\lambda_1)}{\lambda_2-\lambda_1},$$
`daughter_maximum_time` (`test_daughter_peaks_where_its_derivative_vanishes`).

That formula has a direct commercial use. A **⁹⁹Mo/⁹⁹ᵐTc generator** — the
workhorse of nuclear medicine (`~NE-27`) — pairs a 66 h parent with a 6.01 h
daughter, and $t_{\max}=22.9$ h. Elute it about once a day and you recover
nearly all the technetium that has grown in; elute much sooner and there is
little there, much later and it has decayed away.

## 3. Two kinds of equilibrium

Once the daughter's transient has died away, the ratio of activities settles.
`activity_ratio` gives the asymptotic value
$$\frac{A_2}{A_1}=\frac{\lambda_2}{\lambda_2-\lambda_1}\qquad(\lambda_2>\lambda_1).$$

**Transient equilibrium** ($\lambda_2>\lambda_1$ but comparably): the ratio is a
fixed number greater than one, and the pair then decays together with the
*parent's* half-life. For ⁹⁹Mo/⁹⁹ᵐTc, $A_2/A_1=1.10$.

**Secular equilibrium** ($\lambda_1\lll\lambda_2$): the ratio tends to **one**.
The parent's activity is effectively constant over the daughter's whole
lifetime, so $dN_j/dt\simeq0$ for every member and [S&F Eqs. (5.71)–(5.72), p. 125]
$$\lambda_1N_1=\lambda_2N_2=\cdots=\lambda_{n-1}N_{n-1}
\quad\Longleftrightarrow\quad
\boxed{\;A_0=A_1=A_2=\cdots=A_{n-1}\;}$$
**every member of the chain has the same activity.** This is the single most
useful fact in the module. An undisturbed uranium ore sample holds equal
activities of ²³⁸U, ²³⁴U, ²³⁰Th, ²²⁶Ra, ²²²Rn, ²¹⁰Pb and ²¹⁰Po, despite their
half-lives spanning from 4.5 Gy down to 3.8 days
(`test_uranium_series_members_are_secular_with_the_parent`).

Three consequences follow immediately:

- **Radon.** ²²²Rn has the same activity as the ²³⁸U in the rock beneath a
  house. It is a noble gas, so it escapes and accumulates indoors — the largest
  single contributor to natural human radiation dose (`~NE-18`).
- **Radium from uranium.** Radium is not mined; it is separated from uranium ore,
  where secular equilibrium guarantees a fixed radium-to-uranium ratio.
- **Assay by proxy.** Measuring any one member's activity gives all the others,
  which is how ore grades are determined from gamma counting.

The equilibrium is destroyed by chemical separation, and the time taken to
re-establish it is set by the *longest-lived* daughter — which is how one can
tell how recently a sample was processed.

## 4. Four series, three survivors

Alpha decay changes $A$ by 4; beta decay does not change it at all. So
$A\bmod4$ is **conserved** along a chain, and there are exactly four possible
series (`series_of`, `NATURAL_SERIES`):

| $A\bmod4$ | series | parent | end | parent $T_{1/2}$ | still present? |
|---|---|---|---|---|---|
| 0 | thorium | ²³²Th | ²⁰⁸Pb | 14.05 Gy | yes |
| 1 | neptunium | ²³⁷Np | ²⁰⁹Bi | 2.14 My | **no** |
| 2 | uranium | ²³⁸U | ²⁰⁶Pb | 4.468 Gy | yes |
| 3 | actinium | ²³⁵U | ²⁰⁷Pb | 704 My | yes |

Only three occur in nature. The neptunium series is extinct because its longest-
lived member has a 2.14 My half-life — over the Earth's 4.5 Gy age that is 2100
half-lives, a survival factor of $10^{-633}$
(`test_neptunium_series_is_extinct`). Its absence is not a coincidence but a
clock reading: it tells us the Earth is very much older than 2 My. Three of the
four series end on lead isotopes, which is why lead is anomalously abundant among
the heavy elements and why its isotopic composition varies with the local
uranium and thorium content.

## 5. Radiodating

Two strategies [S&F §5.8, pp. 128–131].

**Measure the surviving parent** [§5.8.1]. If the initial amount is known,
$$t=\frac{1}{\lambda}\ln\frac{N_0}{N},$$
`age_from_parent_fraction`. **Radiocarbon** works this way: cosmic rays maintain
a roughly steady ¹⁴C concentration in the atmosphere via
${}^{14}\mathrm{N}(n,p){}^{14}\mathrm{C}$ (`~NE-04` P1), living things exchange
carbon with it, and the clock starts at death. `carbon14_age` converts a measured
specific activity against the 13.56 dpm/g of living matter:

| activity (dpm/g) | age (y) |
|---|---|
| 13.56 | 0 |
| 6.78 | 5 700 |
| 3.39 | 11 400 |
| 0.85 | 22 800 |
| 0.013 | 57 000 |

The method's limit is about ten half-lives, ~57 000 y, where a gram of carbon
gives roughly one count per hour and the signal drowns in background
(`~NE-16`). Its weakness is the assumption of a constant initial concentration —
atmospheric ¹⁴C has in fact varied with solar activity and, since 1950, with
fossil-fuel burning and weapons testing, which is why raw radiocarbon ages must
be calibrated against tree rings.

**Measure the accumulated stable daughter** [§5.8.2]. Every parent that decayed
became a daughter, so $N_D=N_P(e^{\lambda t}-1)$ and
$$t=\frac{1}{\lambda}\ln\!\left(1+\frac{N_D}{N_P}\right),$$
`age_from_daughter_ratio`. This needs **no** initial-amount assumption — only
that no daughter was present at $t=0$ and none has escaped since. It is the basis
of U/Pb and K/Ar dating and reaches back billions of years. A rock with
$N(^{206}\mathrm{Pb})/N(^{238}\mathrm{U})=0.1$ is 615 My old; a ratio of 1.0 is
exactly one half-life, 4.47 Gy.

> **The branching trap.** For K/Ar, only **10.72%** of ⁴⁰K decays give ⁴⁰Ar; the
> other 89% give ⁴⁰Ca (`~NE-05`). The accumulated argon is therefore
> $f\,N_P(e^{\lambda t}-1)$, and using the raw ratio makes a rock look 3.4 times
> younger than it is. `age_from_daughter_ratio` takes a `branch_fraction`
> argument for exactly this, and
> `test_potassium_argon_needs_the_branching_correction` pins the factor.

## Where this goes

- `~NE-09` — fission products are born far to the neutron-rich side and cascade
  down isobaric chains exactly like these.
- `~NE-18` — radon, the largest natural dose contributor, is a secular-equilibrium
  consequence.
- `~NE-20` — the same production-and-decay equation, with a neutron flux driving
  $Q$, becomes fission-product poisoning (xenon and samarium).
- `~NE-23` — spent-fuel activity as a function of cooling time is a Bateman
  problem over hundreds of chains.
- `~NE-26`, `~NE-27` — activation analysis and the ⁹⁹Mo/⁹⁹ᵐTc generator both
  live on §1 and §2 of these notes.
