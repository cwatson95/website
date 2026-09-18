# NE-16 — Counting statistics: Poisson counting, propagated error, dead time (notes)

`~NE-15` built the detectors. This module is about what their output *means*,
and it rests on one fact that makes radiation measurement unlike most other
kinds:

> **The uncertainty is known in advance.**

You do not have to repeat a measurement to learn its precision. Radioactive
decay is a Bernoulli process (`~NE-06`), so a count $x$ has variance $x$, and the
single number you already have tells you its own error.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§8.6–8.7, cited by **printed** page (PDF = printed + 23).

## 1. The single measurement

S&F reach the Gaussian by way of the binomial [§8.6.2]: decay is binomial, the
binomial is awkward for large numbers, and for small probability and a mean above
about 20 the Gaussian describes it well [Eq. (8.9)]. Then [Eq. (8.10)]
$$\boxed{\;\sigma=\sqrt{x},\qquad \frac{\sigma}{x}=\frac{1}{\sqrt x}\;}$$

The "above about 20" is a real condition, not a formality — below it the Poisson
distribution is visibly skewed and a symmetric $x\pm\sqrt x$ interval
misrepresents it. `counting_sigma` **raises** below 20 rather than returning a
plausible-looking number.

Table 8.3 makes the scaling concrete, and it is worth memorising:

| counts | relative error |
|---|---|
| 100 | 10% |
| 400 | 5% |
| 2 500 | 2% |
| 10 000 | **1%** |
| 1 000 000 | 0.1% |

**This is a wall.** Halving an uncertainty costs four times the counting time,
and no improvement to the electronics touches it — the fluctuation is in the
source, not the instrument. Every experimental design in the field is a
negotiation with $1/\sqrt N$.

For $N$ repeated measurements [Eqs. (8.11)–(8.14)],
$$\bar x=\frac1N\sum x_i,\qquad \sigma_{\bar x}=\sqrt{\frac{\bar x}{N}},$$
which reduces to Eq. (8.10) at $N=1$ and improves as $\sqrt N$.

Note what $\sigma_{\bar x}$ is **not**: it is not the sample standard deviation
of the values. S&F derive it from counting statistics on the assumption that the
source activity is constant over the series. If the observed scatter greatly
exceeds this prediction, that is *evidence the assumption is false* — a drifting
source, a drifting detector, a temperature effect — and the right response is to
find out why, not to quote the sample sigma instead. Comparing the two is a free
and frequently ignored diagnostic.

**Confidence intervals** [Table 8.4] follow from the Gaussian: $\pm1\sigma$
encloses 68.3%, $\pm1.65\sigma$ encloses 90%, $\pm1.96\sigma$ encloses 95%. The
book's table rounds — the exact multipliers are 0.6745, 1.6449 and 1.9600 — and
`confidence_multiplier` returns the exact values. **The convention is to report
one standard deviation**; anything else must say so explicitly.

## 2. Propagation, and why background is expensive

Real results are rarely a single count. They are differences (sample minus
background) and ratios (one rate over another), and errors compound.

The rule that gets misused most often: **subtracting does not subtract the
uncertainty.** For $x\pm\sigma_x$ and $y\pm\sigma_y$,
$$\sigma_{x\pm y}=\sqrt{\sigma_x^2+\sigma_y^2}$$
— *identical* for the sum and the difference. So a small difference between two
large counts is very badly determined, and a net rate is always less precise than
either count that went into it.

For a source counted against a background,
$$r=\frac{C_g}{t_g}-\frac{C_b}{t_b},\qquad
\sigma_r=\sqrt{\frac{C_g}{t_g^2}+\frac{C_b}{t_b^2}}.$$

The consequences are stark. Count 520 in 60 s against a background of 500 in
60 s: each raw count is known to better than 5%, and the net rate of 0.33 s⁻¹
carries a **160% uncertainty**. There is no detection there at all. Where
$\sigma_r=r$ is essentially the definition of a **detection limit**, and it moves
to higher activity as the background rises — which is the entire argument for low
background counting: shielded rooms, aged lead, underground laboratories.

**Allocating a fixed counting time.** S&F do not treat this, and the result is
worth having. Minimising $\sigma_r$ at fixed $t_g+t_b$ gives
$$\frac{t_g}{t_b}=\sqrt{\frac{r_g}{r_b}}.$$
The even split is optimal only when the rates are equal. For a source ten times
background, 76% of the time belongs on the sample, and splitting evenly wastes
about 10% of the attainable precision — free precision, discarded by not
thinking about it. `test_optimal_time_split_beats_fifty_fifty` verifies the
formula by direct numerical minimisation rather than trusting the algebra.

## 3. Dead time

A detector busy processing one event cannot record the next. If $\tau$ is the
dead time and $m$ the observed rate, the fraction of time lost is $m\tau$ and the
true rate is [S&F Eq. (8.15)]
$$n=\frac{m}{1-m\tau}.$$

S&F advise keeping $m\tau<0.05$, and give the consequence: a GM tube with
$\tau=100$ μs is limited to **500 counts/s**. That is a severe restriction, and
it is the main reason GM counters are survey instruments rather than
spectrometers. It also connects directly to `~NE-15`: NaI(Tl)'s 230 ns
fluorescence needs ~530 ns to collect 90% of its light, which sets a floor on
$\tau$ that LaBr₃'s 16 ns does not.

Two things about Eq. (8.15) deserve care.

**It diverges, and it stops being trustworthy well before it does.** Past
$m\tau=0.5$ the correction exceeds the measurement itself, and the answer is then
determined by the *assumed model* rather than the data. The non-paralysable model
used here is one of two standard choices; the paralysable model — in which each
new event during the dead period *extends* it — gives a materially different
answer in exactly that regime. `true_rate` refuses beyond $m\tau=0.5$ rather than
silently picking a model.

**The forward map saturates, and that is the dangerous failure.** Inverting,
$$m=\frac{n}{1+n\tau}\xrightarrow[n\to\infty]{}\frac1\tau.$$
So the observed rate has a **ceiling**, and a detector at saturation reports the
same reading for *any* input above it. A true rate of $10^5$ s⁻¹ and one of
$10^9$ s⁻¹ both read as roughly 10 000 s⁻¹ on a 100 μs detector — a factor of
$10^4$ in the field, compressed into 10% on the meter.

That makes dead time a **safety** matter, not just a precision one: a
catastrophically intense field can read as merely moderate. It is why survey
instruments are designed to go off-scale or alarm rather than fold over, and why
a reading that seems implausibly low near a strong source must be treated as
suspect.

**Where does $\tau$ come from?** S&F state Eq. (8.15) without saying. The
standard answer is the **two-source method**: count two sources separately and
together. Because losses are non-linear, $m_{12}<m_1+m_2$, and the shortfall
measures $\tau$:
$$\tau\simeq\frac{m_1+m_2-m_{12}}{2m_1m_2}.$$
This is leading-order, and the module's test shows it degrades exactly as
expected — always *under*estimating, by 4% at low loss and 23% when
$(n_1+n_2)\tau$ reaches 0.84.

## Where this goes

- `~NE-15` — the detectors whose output this interprets; the scintillator decay
  times of Table 8.1 set the achievable $\tau$.
- `~NE-06` — the memoryless decay law that makes counting Poisson in the first
  place; the exponential inter-arrival time is what the module's simulation
  generates.
- `~NE-17` — a dose measurement is a count with all of §2's propagation applied,
  and detection limits decide what "below regulatory concern" can mean.
- `~NE-26` — activation analysis lives or dies on §2: the whole technique is a
  small net peak on a large background.
- `~ST-09`, `~ST-11` — the general Poisson and error-propagation machinery this
  module specialises.

## A note on how this module tests itself

Two of the assertions here are simulations rather than algebra, deliberately.

`test_poisson_variance_really_is_the_mean` generates events from **exponential
inter-arrival times** — the actual physical process — and checks that the sample
variance equals the sample mean. A first draft used a binomial with $p=0.2$,
whose variance is $np(1-p)$, 20% below the mean; that would have *failed against
correct code*. The test now includes the binomial case as an explicit contrast,
so the distinction is recorded rather than merely fixed.

`test_optimal_time_split_beats_fifty_fifty` finds the optimum by scanning 20 000
splits and compares it with the closed form, rather than asserting the formula
against itself.
