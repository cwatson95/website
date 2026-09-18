# NE-06 — Problems

Work each by hand, then check with `code/decay_kinetics.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6
follow the book's Chapter 5 problems 8, 10, 11, 12, 13 and 14 (printed 133–134);
P7–P8 are added. Throughout $\lambda=\ln2/T_{1/2}$ and $A=\lambda N$.

### P1.  Decay constant and mean life of ⁴⁰K  *(S&F Ch. 5, Prob. 8)*
$^{40}$K has a half-life of 1.29 Gy. Find $\lambda$ and the mean lifetime.
*Check:* $\lambda=1.7027\times10^{-17}$ s⁻¹; mean life $5.873\times10^{16}$ s
$=1.861$ Gy.

**Solution.** With $T_{1/2}=1.29\times10^{9}\times3.156\times10^{7}$ s
$=4.071\times10^{16}$ s,
$$\lambda=\frac{\ln2}{T_{1/2}}=\frac{0.6931}{4.071\times10^{16}}
=1.703\times10^{-17}\ \text{s}^{-1},$$
$$T_{\text{av}}=\frac{1}{\lambda}=5.873\times10^{16}\ \text{s}=1.861\ \text{Gy}.$$
The mean life is $1/\ln2=1.443$ times the half-life — not equal to it. ⁴⁰K is the
dominant source of natural radioactivity in the human body (about 4000 Bq in an
adult, from the potassium in muscle), and its 1.29 Gy half-life, comparable to the
age of the Earth, is why it is still around at all.

### P2.  Half-life from a measured decline  *(S&F Ch. 5, Prob. 10)*
An activity falls by 30% in one week. What is the half-life?
*Check:* $\lambda=0.05095$ d⁻¹, $T_{1/2}=13.60$ d.

**Solution.** "Decreases by 30%" means 70% remains, so
$$0.70=e^{-\lambda(7\ \text{d})}
\ \Longrightarrow\ \lambda=\frac{-\ln0.70}{7}=\frac{0.3567}{7}=0.05095\ \text{d}^{-1},$$
$$T_{1/2}=\frac{\ln2}{\lambda}=\frac{0.6931}{0.05095}=13.60\ \text{d}.$$
Equivalently, `half_lives_elapsed(0.70)`$=0.5146$ half-lives elapsed in 7 days, so
$T_{1/2}=7/0.5146=13.60$ d. Note that this measurement needs no knowledge of the
sample size, the detector efficiency or the geometry — a *ratio* of activities
cancels all of them, which is why decay-curve fitting is such a robust way to
identify a nuclide (`~NE-16`).

### P3.  ¹³²I  *(S&F Ch. 5, Prob. 11)*
$^{132}$I decays by $\beta^-$ to $^{132}$Xe with a 2.3 h half-life. Find the decay
constant, and the fraction of a sample remaining after 24 hours.
*Check:* $\lambda=8.372\times10^{-5}$ s⁻¹ $=0.3014$ h⁻¹; after 24 h,
$7.3\times10^{-4}$ remains.

**Solution.** $\lambda=\ln2/2.3\ \text{h}=0.3014$ h⁻¹ $=8.372\times10^{-5}$ s⁻¹.
After 24 h, $n=24/2.3=10.43$ half-lives have passed, so
$$\frac{N}{N_0}=e^{-0.3014\times24}=2^{-10.43}=7.3\times10^{-4}.$$
Roughly one part in 1400. The practical reading: **ten half-lives reduces a
sample by a factor of about 1000**, which is the rule of thumb behind "hold it
for ten half-lives and it is gone." For ¹³²I that is a day; for ¹³⁷Cs it is three
centuries; for ²³⁹Pu it is a quarter of a million years (`~NE-23`).

### P4.  How much ³²P is 5 mCi?  *(S&F Ch. 5, Prob. 12)*
Find the mass of $^{32}$P (half-life 14.28 d) in a 5 mCi source.
*Check:* $A=1.85\times10^{8}$ Bq, $N=3.293\times10^{14}$ atoms,
$m=1.75\times10^{-8}$ g.

**Solution.** Convert to becquerels: $5\times10^{-3}\times3.7\times10^{10}
=1.85\times10^{8}$ decays/s. With
$\lambda=\ln2/(14.28\times86400)=5.618\times10^{-7}$ s⁻¹,
$$N=\frac{A}{\lambda}=\frac{1.85\times10^{8}}{5.618\times10^{-7}}
=3.293\times10^{14}\ \text{atoms},$$
$$m=\frac{N}{N_A}\times32=\frac{3.293\times10^{14}}{6.022\times10^{23}}\times32
=1.75\times10^{-8}\ \text{g}=17.5\ \text{ng}.$$
Seventeen nanograms. This is the recurring surprise of radioactive sources: a
clinically or industrially useful activity corresponds to an invisible quantity of
material. It also means **chemical toxicity is almost never the issue** for
short-lived nuclides — the hazard is entirely radiological (`~NE-18`).

### P5.  1.20 MBq of ²⁴Na and of ²³⁸U  *(S&F Ch. 5, Prob. 13)*
How many atoms in each?
*Check:* $9.32\times10^{10}$ atoms of $^{24}$Na (14.96 h);
$2.44\times10^{23}$ atoms of $^{238}$U (4.468 Gy) — 96.5 g.

**Solution.** $N=A/\lambda=AT_{1/2}/\ln2$ in both cases.
$$N(^{24}\text{Na})=\frac{1.20\times10^{6}\times(14.96\times3600)}{0.6931}
=9.32\times10^{10},$$
$$N(^{238}\text{U})=\frac{1.20\times10^{6}\times(4.468\times10^{9}\times3.156\times10^{7})}{0.6931}
=2.44\times10^{23}\ \Rightarrow\ 96.5\ \text{g}.$$

Twelve orders of magnitude apart for the *same activity*. A vial of ²⁴Na holding
0.004 µg is as "radioactive" as a 96 gram lump of uranium. This is the inversion
of §3 of the notes seen from the other side: activity measures decay *rate*, and
buying the same rate from a long-lived nuclide costs enormously more material.
It is also why natural uranium can be handled with gloves while a comparable
activity of a short-lived fission product cannot.

### P6.  Dating a piece of wood  *(S&F Ch. 5, Prob. 14)*
A specimen contained $10^{12}$ atoms of $^{14}$C in 1986. What was its activity?
*Check:* $3.853$ Bq $=231.2$ disintegrations per minute.

**Solution.** With $T_{1/2}=5700$ y $=1.799\times10^{11}$ s,
$\lambda=3.853\times10^{-12}$ s⁻¹, so
$$A=\lambda N=3.853\times10^{-12}\times10^{12}=3.853\ \text{Bq}=231\ \text{dpm}.$$
Under four decays per second from a *trillion* atoms — the consequence of a
5700-year half-life. This is exactly why radiocarbon dating is hard: the signal
is a handful of counts per minute against a cosmic-ray and detector background of
the same order, so long counting times and heavy shielding are needed
(`~NE-16` for the counting statistics, `~NE-07` for turning the activity into a
date).

### P7.  ⁴⁰K branches both ways
$^{40}$K decays 89.28% by $\beta^-$ and 10.72% by EC, with an observed half-life of
1.28 Gy. Find the partial half-life of each channel, and show why they are not
what a detector measures.
*Check:* `partial_half_life(1.28e9 y, 0.8928)`$=1.434$ Gy;
`partial_half_life(1.28e9 y, 0.1072)`$=11.94$ Gy.

**Solution.** Independent channels add **rates** [Eq. (5.48)]:
$$\lambda=\lambda_{\beta^-}+\lambda_{\mathrm{EC}},\qquad
f_i=\frac{\lambda_i}{\lambda}.$$
So $\lambda_{\beta^-}=0.8928\lambda$ and $\lambda_{\mathrm{EC}}=0.1072\lambda$, giving
partial half-lives
$$T_{\beta^-}=\frac{T_{1/2}}{0.8928}=1.434\ \text{Gy},\qquad
T_{\mathrm{EC}}=\frac{T_{1/2}}{0.1072}=11.94\ \text{Gy}.$$
Both **exceed** the observed 1.28 Gy, and neither is measurable on its own: a
partial half-life is the half-life the nuclide *would* have if the other channel
were switched off. What is observed is always the total. Adding half-lives
directly ($1.434+11.94$, or any average of them) is meaningless — it is the
reciprocals that add.

The EC branch matters out of all proportion to its 10.7%: it produces $^{40}$Ar,
and since argon is a gas that escapes molten rock but is trapped on
solidification, the $^{40}$K/$^{40}$Ar ratio dates the rock's last melting.
Potassium–argon dating is how the geological timescale was calibrated (`~NE-07`).

### P8.  Why the mean life is not the half-life
Show that the mean decay time is $1/\lambda$, and explain the 44% gap.
*Check:* `mean_lifetime(t_half=T)/T`$=1.442695=1/\ln2$; numerical integration of
$p(t)$ confirms both normalisation and mean.

**Solution.** The decay time has density $p(t)=\lambda e^{-\lambda t}$
[Eq. (5.43)] — the probability of surviving to $t$ and then decaying in $dt$.
Integrating by parts,
$$T_{\text{av}}=\int_0^\infty t\,\lambda e^{-\lambda t}\,dt
=\Big[-te^{-\lambda t}\Big]_0^\infty+\int_0^\infty e^{-\lambda t}dt
=0+\frac{1}{\lambda}=\frac{1}{\lambda}.$$
Hence $T_{\text{av}}/T_{1/2}=1/\ln2=1.4427$.

The gap is a mean-versus-median effect. The half-life is by construction the
**median** decay time: half the nuclei are gone by then. But the survivors have
an unbounded tail — a few last for many half-lives — and since the distribution
is skewed right, the mean sits above the median. The same 1.443 factor appears
wherever an exponential does: it is the ratio of mean free path to half-thickness
in `~NE-11`, and of mean lifetime to half-life in every first-order rate process.
