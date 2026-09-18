# NE-16 — Problems

Work each by hand, then check with `code/counting_statistics.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P2
follow the book's Chapter 8 problems 2 and 7 (printed 268–269); P3–P7 are added.
Chapter 8's other problems are detector physics and belong to `~NE-15`.

### P1.  A GM tube with a long dead time  *(S&F Ch. 8, Prob. 2)*
A GM tube has $\tau=0.25$ ms and reads 900 counts/s. What is the true rate?
*Check:* 1161 counts/s.

**Solution.** The dead fraction is
$$m\tau=900\times0.25\times10^{-3}=0.225,$$
so the tube is unable to respond **22.5% of the time**. From Eq. (8.15),
$$n=\frac{m}{1-m\tau}=\frac{900}{0.775}=\boxed{1161\ \text{counts/s}}.$$

The correction is +29%, which is far outside S&F's own advice to keep
$m\tau<0.05$. At this rate the measurement is dominated by the correction model,
not by the data: switch to a lower-activity source, a smaller solid angle, or a
detector with a shorter dead time.

For contrast, at $m\tau=0.05$ the correction is only 5.3%, and the maximum
observed rate meeting that condition is $0.05/\tau=200$ counts/s for this tube.

### P2.  Five one-minute counts  *(S&F Ch. 8, Prob. 7)*
The counts are 1255, 1286, 1234, 1301, 1221. What is the standard deviation of
the average? By what factor would a sixth measurement change it?
*Check:* 15.87; ×0.913.

**Solution.** The mean is
$$\bar x=\frac{1255+1286+1234+1301+1221}{5}=1259.4,$$
and by Eq. (8.13)
$$\sigma_{\bar x}=\sqrt{\frac{\bar x}{N}}=\sqrt{\frac{1259.4}{5}}=\boxed{15.87},$$
so the result is $1259\pm16$ counts per minute (one standard deviation, 68%).

A sixth measurement changes $N$ from 5 to 6, so
$$\frac{\sigma_6}{\sigma_5}=\sqrt{\frac{5}{6}}=\boxed{0.913}$$
— an 8.7% improvement for a 20% increase in effort. That is $1/\sqrt N$ again,
and it is why "just count longer" runs out of value quickly.

**A check the problem does not ask for but should.** The *observed* sample
standard deviation of the five values is 33.8. Counting statistics predict
$\sqrt{\bar x}=35.5$ for a single measurement. Those agree, which is evidence the
source was stable over the series. Had the observed scatter been, say, 90, the
excess would signal something real — a decaying source, a drifting detector — and
quoting $\sigma_{\bar x}=15.9$ would then be badly optimistic. **Always compare
the two.**

### P3.  How long must you count?  *(added)*
A sample gives 45 counts/s against negligible background. How long to reach 1%
precision? 0.1%?
*Check:* 3.7 minutes; 6.2 hours.

**Solution.** Precision is set by *total counts*, so invert Table 8.3:
$$N=\frac{1}{f^2}.$$
For 1%, $N=10^4$ counts, requiring $10^4/45=222$ s $=\boxed{3.7\ \text{min}}$.
For 0.1%, $N=10^6$, requiring $10^6/45=22\,222$ s $=\boxed{6.2\ \text{hours}}$.

**A factor of ten in precision costs a factor of a hundred in time.** This is the
single most useful calculation in planning a measurement, and it explains a great
deal of laboratory practice — why 1% is a common target and 0.1% is a research
project, and why counting statistics rather than instrument quality is usually
the binding constraint.

### P4.  A source barely above background  *(added)*
A 10-minute count gives 3120 counts; a 10-minute background gives 3000. Is the
source detected?
*Check:* net 0.200 ± 0.130 counts/s — a 1.5σ result, not a detection.

**Solution.** Rates are $5.200$ and $5.000$ s⁻¹, so the net is $0.200$ s⁻¹. The
uncertainty is
$$\sigma_r=\sqrt{\frac{3120}{600^2}+\frac{3000}{600^2}}=\frac{\sqrt{6120}}{600}
=0.130\ \text{s}^{-1}.$$

So the net rate is $0.200\pm0.130$ s⁻¹ — **1.53σ**, which by Table 8.4 would be
exceeded by chance about 13% of the time if the true source strength were zero.
That is **not a detection** by any conventional criterion (the usual thresholds
are 3σ or the Currie limits).

Note how the raw numbers mislead: 3120 counts is a 1.8% measurement, and 3000 is
1.8%. The *difference* of two 1.8% numbers is a 65% measurement, because the
difference is small and the errors add in quadrature.

To reach 3σ here you would need $\sigma_r\le0.067$, i.e. four times the counting
time — 40 minutes each. That is the real cost of working near background, and it
is why the low-background techniques of §2 exist.

### P5.  Dividing the time properly  *(added)*
You have one hour total. The sample reads about 50 counts/s and the background
about 2 counts/s. How should the hour be divided, and how much does it matter?
*Check:* 83% on the sample; an even split is 20% worse.

**Solution.** By the rule of §2,
$$\frac{t_g}{t_b}=\sqrt{\frac{50}{2}}=5.0,\qquad
f_g=\frac{\sqrt{50}}{\sqrt{50}+\sqrt2}=0.833,$$
so **50 minutes on the sample and 10 on the background**.

The size of the win: with $\sigma_r^2=r_g/t_g+r_b/t_b$ over 3600 s,

| split | $\sigma_r$ (s⁻¹) |
|---|---|
| optimal (83/17) | **0.1414** |
| even (50/50) | 0.1700 |

The even split is **20% worse**, which by the $1/\sqrt N$ rule is equivalent to
throwing away 44% of the hour. The rule costs nothing to apply, which is why it
is worth knowing even though S&F omit it.

Note the direction: **more time on the stronger sample**, which surprises people
who reason that the weaker background "needs more help". The background's
contribution to the variance is already smaller; the optimum balances the two
contributions, not the two rates.

### P6.  When a detector lies about a hot field  *(added)*
A survey meter has $\tau=50$ μs. You approach a source and the reading climbs to
14 000 counts/s, then stops rising. What is going on?
*Check:* the ceiling is $1/\tau=20\,000$ s⁻¹; the true rate is unknowable.

**Solution.** The forward map is $m=n/(1+n\tau)$, which saturates:
$$m_{\max}=\frac1\tau=\frac{1}{50\times10^{-6}}=20\,000\ \text{s}^{-1}.$$

At a reading of 14 000, $m\tau=0.70$. Formally Eq. (8.15) gives
$n=14\,000/0.30=46\,700$ s⁻¹ — but that correction is **more than double** the
measurement, so it is entirely a statement about the assumed model. The
paralysable model would give a different answer, and in that model the observed
rate actually *falls* at very high input, so a low reading could correspond to an
enormous field.

`true_rate` refuses past $m\tau=0.5$ for exactly this reason.

**What the reading "stopping" means is that the instrument is at or near
saturation, and the field could be anything from 50 000 to 10⁹ s⁻¹.** The correct
response is to back away and use an instrument with a shorter dead time or a
different principle (an ion chamber in current mode does not have this failure
mode at all, because it does not resolve individual events).

This is why survey instruments are designed to peg high or alarm rather than fold
over, and why a suspiciously *low* reading near a known strong source must never
be taken at face value.

### P7.  Measuring the dead time you were never given  *(added)*
Two sources read 8000 and 10 000 counts/s separately, and 16 900 together
(backgrounds negligible). Estimate $\tau$.
*Check:* 6.9 μs.

**Solution.** If there were no dead time the combined rate would be 18 000 s⁻¹.
It is 16 900, so 1100 counts/s are lost. To leading order,
$$\tau\simeq\frac{m_1+m_2-m_{12}}{2m_1m_2}
=\frac{1100}{2\times8000\times10\,000}=\boxed{6.9\ \mu\text{s}}.$$

This is the **two-source method**, and it is how $\tau$ is actually obtained —
S&F give Eq. (8.15) without ever saying where the dead time comes from. The
method works precisely *because* the losses are non-linear: if counting were
linear the combined rate would be exactly the sum and there would be no signal to
measure.

Two cautions. The formula is leading-order and always **underestimates** — the
module's test shows it is 4% low at modest loss and 23% low when
$(n_1+n_2)\tau\simeq0.8$, so the sources should be weak enough that
$m\tau\lesssim0.1$. And the result is model-dependent in the same way as
Eq. (8.15) itself: this is the non-paralysable $\tau$, and a paralysable analysis
of the same three numbers gives a different value.
