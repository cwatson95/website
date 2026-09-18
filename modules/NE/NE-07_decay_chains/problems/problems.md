# NE-07 — Problems

Work each by hand, then check with `code/decay_chains.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P6
follow the book's Chapter 5 problems 18, 19, 23, 25, 26 and 28 (printed 134–135);
P7–P8 are added. Half-lives from `../data_tables/A4_isotopic_abundances.csv`.

### P1.  ⁹⁰Sr in secular equilibrium with ⁹⁰Y  *(S&F Ch. 5, Prob. 18)*
A 6.2 mg sample of $^{90}$Sr (28.79 y) sits in secular equilibrium with its
daughter $^{90}$Y (64 h). Find the activity of each and the total beta activity.
*Check:* $N=4.149\times10^{19}$, $A(^{90}\mathrm{Sr})=3.165\times10^{10}$ Bq
$=0.855$ Ci; the total beta activity is twice that.

**Solution.** The number of atoms is
$$N=\frac{6.2\times10^{-3}}{90}\times6.022\times10^{23}=4.149\times10^{19},$$
and with $\lambda=\ln2/(28.79\times3.156\times10^{7}\ \text{s})=7.629\times10^{-10}$ s⁻¹,
$$A(^{90}\text{Sr})=\lambda N=3.165\times10^{10}\ \text{Bq}=0.855\ \text{Ci}.$$

The parent outlives the daughter by a factor $28.79\times365.25\times24/64=3940$,
comfortably in the secular regime, so $A(^{90}\mathrm{Y})=A(^{90}\mathrm{Sr})$
and the **total** beta activity is $6.330\times10^{10}$ Bq — twice the strontium
alone. Forgetting the daughter halves your answer, and it matters practically:
the ⁹⁰Y beta has a 2.28 MeV endpoint against ⁹⁰Sr's 0.546 MeV, so essentially all
the penetrating dose from a "strontium-90 source" actually comes from the yttrium
(`~NE-17`).

### P2.  Approaching equilibrium  *(S&F Ch. 5, Prob. 19)*
A sample holds 1.0 GBq of $^{90}$Sr and 0.62 GBq of $^{90}$Y. What happens?
*Check:* the asymptotic ratio $A_2/A_1=\lambda_2/(\lambda_2-\lambda_1)=1.000254$;
the daughter reaches its maximum at $t_{\max}=765$ h.

**Solution.** The daughter starts below equilibrium (0.62 versus 1.0 GBq), so it
grows. Its approach is governed by its *own* half-life, not the parent's: after
$n$ daughter half-lives the shortfall is reduced by $2^{-n}$, so
$$A_2(t)\simeq A_1\big[1-(1-0.62)e^{-\lambda_2t}\big],$$
reaching 99% of equilibrium after about $\log_2(0.38/0.01)=5.2$ half-lives of
$^{90}$Y, i.e. roughly 14 days. Thereafter both decay together with the *parent's*
28.79 y half-life.

The asymptotic ratio is $\lambda_2/(\lambda_2-\lambda_1)=1.000254$ — within a
part in 4000 of unity, which is what "secular" means quantitatively. The general
statement is that a separated daughter regrows to equilibrium on the timescale of
the daughter, and this is exactly how a radionuclide generator is recharged (P8).

### P3.  Encapsulated radium  *(S&F Ch. 5, Prob. 23)*
A 40 mg sample of pure $^{226}$Ra is sealed. Find its activity, and how long
until the $^{222}$Rn daughter reaches equilibrium.
*Check:* $A=1.463\times10^{9}$ Bq $=0.0395$ Ci; radon is within 0.1% of
equilibrium after about 38 days.

**Solution.** From the specific activity of radium (0.9886 Ci/g, `~NE-06`),
$$A=40\times10^{-3}\times0.9886=0.0395\ \text{Ci}=1.463\times10^{9}\ \text{Bq}.$$
The $^{222}$Rn daughter (3.82 d) builds up as $1-e^{-\lambda_2t}$, reaching 99.9%
of equilibrium after ten of its half-lives, $\approx38$ days.

The word "encapsulated" is doing real work here. Radon is a **gas**; if the
capsule leaks, the entire chain below radium is carried away and never reaches
equilibrium, which changes both the activity and the emitted spectrum
dramatically. Old radium sources routinely fail this way, and a sealed source
that has been intact for a month can be assayed by counting *any* daughter — the
secular-equilibrium result of §3 of the notes.

### P4.  The global ¹⁴C inventory  *(S&F Ch. 5, Prob. 25)*
The world's $^{14}$C inventory is about 8.5 EBq. If it is in steady state, what
is the production rate, and how much $^{14}$C is there by mass?
*Check:* $Q_0=8.5\times10^{18}$ atoms/s; the mass is $5.1\times10^{4}$ kg.

**Solution.** At steady state, production exactly balances decay [Eq. (5.53) with
$dN/dt=0$], so
$$Q_0=\lambda N=A=8.5\times10^{18}\ \text{atoms/s}.$$
The inventory follows from $N=A/\lambda$ with
$\lambda=3.853\times10^{-12}$ s⁻¹:
$$N=\frac{8.5\times10^{18}}{3.853\times10^{-12}}=2.206\times10^{30}\ \text{atoms}
\ \Rightarrow\ m=\frac{N}{N_A}\times14=5.1\times10^{4}\ \text{kg}.$$

Fifty tonnes of radiocarbon, worldwide, maintained by cosmic rays making
$8.5\times10^{18}$ atoms every second via
${}^{14}\mathrm{N}(n,p){}^{14}\mathrm{C}$. The steady state is what licenses
radiocarbon dating at all: it is the assumption that the atmospheric
concentration a sample started with is the one measured today in living matter.

### P5.  How radioactive is a person?  *(S&F Ch. 5, Prob. 26)*
An adult contains about 140 g of potassium. What activity does its $^{40}$K
contribute?
*Check:* $^{40}$K mass 0.0164 g, $N=2.466\times10^{20}$, $A=4330$ Bq.

**Solution.** $^{40}$K is 0.0117% of natural potassium (Table A.4), so
$$m(^{40}\text{K})=140\times1.17\times10^{-4}=0.0164\ \text{g},\qquad
N=\frac{0.0164}{40}\times6.022\times10^{23}=2.466\times10^{20}.$$
With $T_{1/2}=1.248$ Gy, $\lambda=1.76\times10^{-17}$ s⁻¹ and
$$A=\lambda N=4.33\times10^{3}\ \text{Bq}.$$

Over four thousand decays per second, from potassium alone, in every adult — plus
roughly 3000 Bq of $^{14}$C. This is the natural internal dose baseline against
which every artificial exposure has to be judged (`~NE-18`), and it is the reason
"detectable radioactivity" and "hazardous radioactivity" are very different
statements. It is also homeostatically fixed: the body regulates potassium, so
eating high-potassium food does not raise the number.

### P6.  Dating charcoal  *(S&F Ch. 5, Prob. 28)*
An ancient charcoal sample has a $^{14}$C specific activity of 1.8 dpm per gram
of carbon. How old is it?
*Check:* `carbon14_age(1.8)`$=16\,606$ years.

**Solution.** Against the modern 13.56 dpm/g,
$$\frac{A}{A_0}=\frac{1.8}{13.56}=0.1328,\qquad
t=\frac{1}{\lambda}\ln\frac{A_0}{A}=\frac{5700}{\ln2}\times\ln(7.533)=16\,600\ \text{y}.$$
Equivalently $\log_2(7.533)=2.91$ half-lives.

Two caveats belong with any such number. The uncalibrated "radiocarbon year" is
not a calendar year, because atmospheric $^{14}$C has varied; real dates are
calibrated against tree-ring sequences. And at 1.8 dpm/g the counting statistics
are already demanding — a gram of carbon gives 1.8 counts per minute against a
background of comparable size, so a 1% age precision needs many hours of counting
in a shielded, low-background detector (`~NE-16`).

### P7.  Why there is no natural neptunium series
Show that the 4n+1 series cannot have survived, and say what its absence tells us.
*Check:* $^{237}$Np has $T_{1/2}=2.14$ My; over 4.5 Gy that is 2100 half-lives.

**Solution.** $A\bmod4$ is conserved along a decay chain, since alpha decay
changes $A$ by 4 and beta decay not at all — so there are exactly four possible
series. Three have parents with half-lives comparable to the age of the Earth
($^{232}$Th 14.05 Gy, $^{238}$U 4.468 Gy, $^{235}$U 704 My) and survive. The 4n+1
series is headed by $^{237}$Np at 2.14 My, and
$$\frac{N}{N_0}=e^{-\ln2\times(4.5\times10^{9})/(2.14\times10^{6})}=2^{-2103}
\approx10^{-633}.$$
Nothing survives that. Every $^{237}$Np now in existence is artificial, made in
reactors (`~NE-23`).

The inference runs the other way too, and this is the point: the *absence* of a
naturally occurring 4n+1 series is evidence that the Earth is very much older than
a few million years. The presence of $^{235}$U at 0.72% — the shortest-lived of
the three survivors — bounds the age from above. Read together, the four series
are a clock, and they were among the first evidence for a multi-billion-year
Earth.

### P8.  The technetium generator
$^{99}$Mo (66 h) decays to $^{99\mathrm{m}}$Tc (6.01 h). When should the generator
be eluted, and what is the asymptotic activity ratio?
*Check:* `daughter_maximum_time`$=22.9$ h; `activity_ratio`$=1.100$.

**Solution.** The daughter population peaks when its production rate equals its
loss rate, at
$$t_{\max}=\frac{\ln(\lambda_2/\lambda_1)}{\lambda_2-\lambda_1}
=\frac{\ln(66/6.01)}{\lambda_2-\lambda_1}=22.9\ \text{h},$$
so the generator is eluted roughly **once a day** — which is exactly how hospital
practice works. Elute earlier and the technetium has not grown in; elute later
and it is decaying faster than the molybdenum supplies it.

Since $T_1/T_2=11$, this is **transient**, not secular, equilibrium: the
asymptotic ratio is
$$\frac{A_2}{A_1}=\frac{\lambda_2}{\lambda_2-\lambda_1}=1.100,$$
so the technetium activity settles at 10% *above* the molybdenum activity (not
equal to it, as it would in the secular limit), and thereafter the pair decays
together with the parent's 66 h half-life. That 66 h is what lets a generator be
shipped from a reactor to a hospital and used for a week, while the 6 h daughter
is short enough to clear a patient quickly — the combination that made
$^{99\mathrm{m}}$Tc the most-used radionuclide in medicine (`~NE-27`).
