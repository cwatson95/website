# NE-26 — Problems

Work each by hand, then check with `code/applications.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. Chapter 13
carries no worked problems; these are added.

### P1.  How long to irradiate  *(added)*
A target is activated in a reactor. What fraction of saturation is reached in
three half-lives, and how long for 99%?
*Check:* 87.5%; 6.6 half-lives.

**Solution.** $A(t)=R(1-e^{-\lambda t})$, so the saturation fraction is
$1-2^{-t/T_{1/2}}$: three half-lives gives $\boxed{87.5\%}$, and 99% needs
$-\log_2(0.01)=\boxed{6.6}$ half-lives.

**The economics are in the tail.** Doubling from three half-lives to six buys 11
percentage points; going to ten buys 12. A reactor irradiation position is
expensive and shared, so production is scheduled at two to three half-lives and
the rest is left on the table deliberately.

Note also what saturation *means*: at saturation the product decays exactly as
fast as it is made, so the activity is $R$ regardless of how long you wait. There
is no way to accumulate more of a short-lived isotope than the flux supports —
which is why ⁹⁹ᵐTc is made from a generator and not irradiated directly.

### P2.  When to milk the cow  *(added)*
A ⁹⁹Mo/⁹⁹ᵐTc generator is eluted. When does the daughter activity peak, and what
is it after 24 hours?
*Check:* 48.5 hours; 95% of the peak.

**Solution.** With $T_p=65.9$ d and $T_d=6.01$ h,
$$t_{\max}=\frac{\ln(\lambda_d/\lambda_p)}{\lambda_d-\lambda_p}=\boxed{48.5\ \text{h}},$$
and at 24 h the activity is already $\boxed{95\%}$ of that.

**That 95% is the whole logistics of nuclear medicine.** Waiting the full two
days for the last 5% is not worth a day's delay, so generators are **eluted
daily** and delivered weekly — the parent's 66-day half-life carries the supply
chain while the daughter's 6 hours keeps the patient dose short.

The general principle: a generator lets you ship a short-lived isotope by
shipping a long-lived one. S&F's other example takes it further — ¹³⁷Cs at 30
years feeding ¹³⁷ᵐBa at 2.55 minutes, a ratio of six million.

### P3.  Two measurements with no calibration  *(added)*
(a) 5 cm³ of tracer at 2 × 10⁶ Bq/cm³ is injected into a tank and mixes to
1.8 Bq/cm³. What is the volume? (b) A river is dosed at 5 × 10⁶ Bq/s and reads
20 Bq/m³ downstream. What is the flow?
*Check:* 5.6 m³; 2.5 × 10⁵ m³/s.

**Solution.**
(a) $V=V_0C_0/C=5(2\times10^6)/1.8=5.56\times10^6$ cm³ $=\boxed{5.6\ \text{m}^3}$.
(b) $q=Q_0/C=5\times10^6/20=\boxed{2.5\times10^5\ \text{m}^3/\text{s}}$.

**Neither needed a calibrated detector.** In (a) only the *ratio* $C_0/C$ enters,
so efficiency, geometry and dead time cancel provided the same instrument
measures both samples. In (b) the channel's cross-section never appears — the
tracer must leave at the rate it enters, whatever the river is doing in between.

That is why these two techniques are used where nothing else works: an
irregularly shaped vessel, a blast furnace, a human bloodstream, a tidal estuary.
The measurement is *made* by conservation rather than by instrumentation.

(2.5 × 10⁵ m³/s is a very large river — the Amazon is about 2 × 10⁵. The numbers
here are chosen to be round, not realistic.)

### P4.  Designing a thickness gauge  *(added)*
Steel has µ = 0.57 cm⁻¹ for ¹³⁷Cs gammas. What thickness should a transmission
gauge be designed around, and what is the penalty at 1 cm?
*Check:* 3.5 cm; 1.7× worse.

**Solution.** The precision is
$\sigma_t/t=e^{\mu t/2}/(\mu t\sqrt{N_0})$, minimised at $\mu t=2$, so
$$t=\frac{2}{0.57}=\boxed{3.5\ \text{cm}}.$$
At 1 cm, $\mu t=0.57$ and the precision is $\boxed{1.7\times}$ worse.

**Read the tolerance, not just the optimum.** Anything from 0.9 to 3.6 mean free
paths is within 25% of the best achievable — so the rule does not demand
precision, it tells you which *source* to pick. For thin steel you want a soft
gamma (¹⁷⁰Tm at 84 keV); for thick steel a hard one (⁶⁰Co at 1.25 MeV). Table
13.2's pairings are that choice made for radiography.

**And do not apply this to radiography.** Table 13.2 runs 2 to 9 mean free paths,
because radiography maximises contrast through a workpiece of *fixed* thickness
rather than minimising the variance of a thickness *estimate*. Same exponential,
different objective.

### P5.  Four billion atoms  *(added)*
NAA detects europium at 0.9 pg. How many atoms is that, and how much worse is
iron?
*Check:* 3.6 × 10⁹ atoms; iron is 1.1 × 10⁷ times worse.

**Solution.** $0.9\times10^{-12}\ \text{g}/152\times6.022\times10^{23}
=\boxed{3.6\times10^9}$ atoms. Iron's limit is 10 µg, a factor of
$\boxed{1.1\times10^7}$.

**Seven decades between two elements in the same table.** The spread has nothing
to do with the instrument: it is the activation cross section, and whether the
product emits a gamma distinguishable from everything else in the sample.
Europium has an enormous cross section and a clean gamma; iron has neither.

So NAA is not an assay you can point at an unknown sample and expect an answer
from. It is exquisite for a few dozen elements and blind to the rest — which is
why §13.4.7 lists applications (forensic trace signatures, geological samples,
pesticide bromine and chlorine, vanadium in refined oil) rather than claiming
generality. **Every one of those uses is chosen to sit on the sensitive end of
this table.**

### P6.  The same word for two different things  *(added)*
Compare the doses used to inhibit potato sprouting and to sterilise medical
supplies with a lethal human dose.
*Check:* 60 Gy and 25 000 Gy against an LD50/60 of 3.5 Gy.

**Solution.** From §13.5: sprout inhibition 60–150 Gy, medical sterilisation
25 kGy. From `~NE-18` Table 9.8, the human LD50/60 is about 3.5 Gy. So the
*lowest* industrial process dose is **17×** a dose that kills half of exposed
people, and sterilisation is $\boxed{7100\times}$ it.

**This is the number that settles the "is irradiated food radioactive"
question**, though not in the way it is usually argued. The answer is no, because
gamma irradiation at these energies cannot activate anything — but the more
useful framing is that industrial and biological doses are not on the same scale
at all. A potato receives, in one pass, seventeen human lethal doses and is
unchanged except that it will not sprout.

Note too that the constraint on full food sterilisation is not radiological. S&F
say it "often is accompanied by unacceptable changes in flavor, smell, color and
texture" — the technology is limited by taste, not by safety, which is a useful
corrective to assuming physics is always what stops an application.
