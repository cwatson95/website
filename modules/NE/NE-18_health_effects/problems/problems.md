# NE-18 — Problems

Work each by hand, then check with `code/health_effects.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. P1–P7 are
the book's Chapter 9 problems 7, 8, 9, 11, 13, 14 and 16 (printed 319–320); P8 is
added from the authors' solution manual. Chapter 9's problems 1–6 are dosimetry
and belong to `~NE-17`.

Note the solution manual is numbered **+2** from problem 7 onward and restates
several problems with different numbers — see `../refs.md`. These follow the
textbook.

### P1.  A 2.3 Gy accident  *(S&F Ch. 9, Prob. 7)*
A male worker receives an accidental whole-body dose of 2.3 Gy. What symptoms,
and when?
*Check:* six Table 9.7 thresholds passed; ~5% 60-day lethality; survivable.

**Solution.** The answer is a **timeline**, not a number. From Table 9.7 the dose
passes six thresholds — testes (0.3 Gy), eye lens (0.5), GI vomiting (0.5),
ovary-equivalent (0.6), GI diarrhea (1.0) and **bone-marrow death (1.8)** — and
misses skin erythema (3.0).

| when | what |
|---|---|
| minutes–48 h | prodromal: nausea, vomiting, fatigue, weakness [Table 9.10] |
| 2–3 weeks | **latent stage** — apparent well-being |
| ~46 days | sperm count begins to fall; ~80% down by 74 days |
| 3–6 weeks | manifest illness: ~30% drop in blood-cell production, infection risk |
| beyond 6 weeks | recovery likely if he survives |

Quantitatively: 2.3 Gy sits in Table 9.8's **LD5/60 band (2.0–2.5 Gy)**, so
roughly $\boxed{5\%}$ 60-day lethality without treatment — and marrow death is
possible but not likely, since its $D_{50}$ is 3.8 Gy. Modern supportive care
(transfusion, antibiotics, colony-stimulating factors) moves this substantially;
Table 9.8 is explicitly the untreated case.

**Note what is *not* the point.** The stochastic risk from 2.3 Gy — about a 13%
lifetime chance of a radiogenic fatal cancer at 0.057/Gy — is real but is not what
sends him to hospital. Deterministic and stochastic effects operate on completely
different timescales and both must be quoted.

### P2.  A population dose  *(S&F Ch. 9, Prob. 8)*
500 000 people receive an average whole-body 0.5 rad (0.005 Gy).
*Check:* 2500 person-Gy; 8–12 first-generation hereditary cases; 143 cancer
deaths against 102 100 natural.

**Solution.**
(a) Collective gonad dose $=5\times10^5\times0.005=\boxed{2500}$ person-Gy.

(b) From Table 9.11, 3000–4700 first-generation cases per Gy per million progeny:
$$(3000\text{–}4700)\times\tfrac{5\times10^5}{10^6}\times0.005=\boxed{8\text{–}12\ \text{cases}}.$$
Over the first *two* generations the table's 3950–6700 gives 10–17.

(c) Naturally, 738 000 per million progeny, i.e. $\boxed{369\,000}$ cases among
500 000 births. **The radiation contribution is 1 case in 30 000 natural ones.**

(d) At 0.057 fatal cancers per Gy,
$5\times10^5\times0.005\times0.057=\boxed{143\ \text{deaths}}$, against a natural
expectation of $0.5(22\,810+18\,030)/10^5\times5\times10^5=\boxed{102\,100}$ —
**0.14%**.

The honest framing is that last ratio. 143 deaths is a large number and it is
also undetectable: a 0.14% shift on 102 100 is far inside the year-to-year
variation of the natural rate, which is why an epidemiological study of this
population would find nothing whatever the truth was.

### P3.  A high-background region  *(S&F Ch. 9, Prob. 9)*
900 000 people receive an extra 125 mrem/y (whole-body, low-LET).
*Check:* 3.38 × 10⁴ person-Gy; 133–226 cases per generation against 266 000
natural.

**Solution.** Taking a 30-year mean reproductive age, each person accumulates
$30\times1.25$ mSv $=0.0375$ Gy to the gonads, so
$$D_g=0.0375\times900\,000=\boxed{3.38\times10^4\ \text{person-Gy}}.$$
At 3950–6700 cases per 10⁶ person-Gy this is $\boxed{133\text{–}226}$ cases per
generation.

Naturally: with a 75-year lifespan and 30-year reproduction interval there are
$(30/75)\times900\,000=360\,000$ liveborn per generation, so
$738\,000\times0.36=\boxed{266\,000}$ natural cases — the radiation contributes
**0.06%**.

**This is the calculation that makes high-background regions interesting.** Places
like Kerala and Yangjiang have exactly this structure, and the predicted excess is
three orders of magnitude below the natural incidence. The studies S&F cite in
§9.10.2 that find *inverse* correlations there are not detecting hormesis over
LNT; they are detecting that neither model predicts anything measurable, and that
whatever else varies between regions dominates.

### P4.  Cancer from natural background  *(S&F Ch. 9, Prob. 11)*
How many U.S. deaths per year from cancer caused by natural background (excluding
radon lung dose)? Assume 200 mrem/y and 320 million people.
*Check:* ~2.7 × 10⁶ lifetime excess, ~36 000/y, about 5.6% of natural cancer
mortality.

**Solution.** 200 mrem/y = 2 mGy/y continuous, so use Table 9.14's **second**
scenario (continuous lifetime 1 mGy/y), whose excess mortality is 332 (M) and
497 (F) per 10⁵. Scaling linearly to 2 mGy/y,
$$N=\frac{332+497}{2}\times2\times\frac{3.2\times10^8}{10^5}=\boxed{2.65\times10^6}$$
lifetime excess deaths. For a static population with a 73.1-year lifespan that is
$\boxed{36\,000\ \text{per year}}$, against a natural cancer mortality of
$0.5(239.9+162.7)/10^5\times3.2\times10^8=\boxed{644\,000}$ per year — **5.6%**.

**Careful with the table.** The solution manual works this problem with the
(480 + 660) figures, which are the **single 0.1 Gy** scenario, and then scales
them by "2 mGy / 1 mGy" — mixing a one-off exposure risk with an annual rate.
That gives 3.7 × 10⁶ instead of 2.7 × 10⁶. Table 9.14 has a row for exactly this
question; use it.

And treat the answer with suspicion in the other direction too: it is LNT applied
at 2 mGy/y, a fiftieth of the dose at which any excess has ever been seen. The
result is a property of the model.

### P5.  A week's occupational exposure  *(S&F Ch. 9, Prob. 13)*
A male reactor operator receives 0.95 rem whole-body in a week. Probability he
(a) dies of cancer, (b) dies of cancer *caused by this*, (c) has a child with
hereditary illness, (d) has one *caused by this*?
*Check:* 22.8%; 5.4 × 10⁻⁴; 73.8%; ~5 × 10⁻⁵.

**Solution.** 0.95 rem = 9.5 mSv.

(a) From Table 9.14's natural expectation, $22\,810/10^5=\boxed{22.8\%}$.
(b) $0.0095\times0.057=\boxed{5.4\times10^{-4}}$, about 1 in 1850.
(c) From Table 9.11, $738\,000/10^6=\boxed{73.8\%}$ — nearly three in four, over
a whole lifetime and counting multifactorial disease.
(d) $(3950\text{–}6700)\times10^{-6}\times0.0095=\boxed{4\text{–}6\times10^{-5}}$.

**Set (a) beside (b) and (c) beside (d).** The exposure multiplies his cancer
death risk by 1.0024 and his child's hereditary-illness risk by 1.00007. That
comparison — not the absolute risk — is what a worker actually needs, and it is
what the problem is for. Note also that 9.5 mSv in one week is a fifth of the
*annual* limit, so it would be a reportable event even though the risk arithmetic
looks negligible; limits control cumulative exposure, not single events.

### P6.  Two radon environments  *(S&F Ch. 9, Prob. 14)*
75% of the time at 4.6 pCi/L with F = 0.6; 25% at 1.3 pCi/L with F = 0.8. Annual
exposure on an EEC basis?
*Check:* 0.756 MBq h m⁻³.

**Solution.** With 1 pCi/L = 37 Bq/m³, the concentrations are 170.2 and
48.1 Bq/m³. Apply $EEC=F\,C_0$ to each and weight by occupancy:
$$\overline{EEC}=0.75(0.6)(170.2)+0.25(0.8)(48.1)=76.6+9.6=86.2\ \text{Bq/m}^3,$$
and over 8766 hours,
$$\boxed{0.756\ \text{MBq h m}^{-3}\ \text{per year}}.$$

**Note the equilibrium factor is not a detail.** The higher-concentration
environment has the *lower* F, and if you ignored F entirely you would get
1.22 MBq h m⁻³ — **62% too high**. F is what converts a radon measurement into a
hazard, and it is why the EPA's 4 pCi/L action level is quoted "uncorrected for
disequilibrium, with F = 0.5 assumed".

For scale, 0.756 MBq h m⁻³ is 1.2 WLM per year — well above the U.S. residential
average and around the EPA action level.

### P7.  A woman's lifetime radon risk  *(S&F Ch. 9, Prob. 16)*
75% of the time at 25 Bq/m³ EEC, 25% at 5 Bq/m³, for life. (a) Non-smoker,
(b) smoker?
*Check:* 0.15%; 1.42%.

**Solution.** The occupancy-weighted EEC is $0.75(25)+0.25(5)=20$ Bq/m³, so the
annual exposure is $20\times8766/10^6=0.175$ MBq h m⁻³. From Table 9.15,
$$\text{non-smoker: }0.0088\times0.175=\boxed{1.5\times10^{-3}},\qquad
\text{smoker: }0.081\times0.175=\boxed{1.4\times10^{-2}}.$$

**The ratio is the answer worth remembering: 9.2×.** Radon and tobacco multiply
rather than add, because both act on the same bronchial epithelium and smoking
both damages clearance and supplies the promotion step. Two consequences follow.
Radon remediation buys a smoker nearly ten times what it buys a non-smoker — so
remediation and cessation are not independent policies. And a radon risk quoted
for a "general population" (Table 9.15's mixed row, 0.039) is an average over a
population whose two halves differ tenfold; it describes almost nobody.

### P8.  Goiânia, 1987  *(added; the authors' solution manual, Ch. 9 Prob. 12)*
A 5 × 10¹³ Bq ¹³⁷Cs radiotherapy source was stolen from an abandoned clinic and
broken open. The 0.662 MeV gamma is emitted 94.4% of the time. (a) Dose to
someone one metre away for an hour. (b) Consequences. (c) 1000 further people
received up to 200 mSv — expected cancers, and deaths? (d) Natural expectation?
*Check:* 4.7 Gy; 23 cancers, 11 deaths, against 204 natural.

**Solution.**
(a) Using `~NE-17`, the fluence rate at 1 m is
$$\phi=\frac{(0.944)(5\times10^{13})}{4\pi(100)^2}=3.76\times10^8\ \text{cm}^{-2}\text{s}^{-1},$$
and with water's $\mu_{en}/\rho=0.03260$ cm²/g at 0.662 MeV,
$$\dot D=1.602\times10^{-10}(0.662)(0.03260)(3.76\times10^8)=1.30\times10^{-3}\ \text{Gy/s},$$
so an hour gives $\boxed{4.7\ \text{Gy}}$.

(b) That is above LD50/60 (3.0–3.5 Gy) and inside the LD90–LD99 range: **without
intensive treatment this is expected to be fatal**. Historically the man who
opened the source survived; four other people died, including a six-year-old
child who ate food contaminated with the caesium chloride powder.

(c) From Table 9.14, incidence $0.5(900+1370)/(10^5\times0.1\ \mathrm{Gy})=0.1135$
per person-Gy and mortality 0.0570 per person-Gy, so at 0.2 Gy for 1000 people:
$\boxed{23\ \text{cancers}}$ and $\boxed{11\ \text{deaths}}$.

(d) Naturally, $0.5(22\,810+18\,030)/10^5\times1000=\boxed{204}$ cancer deaths.

**The two halves of this problem are the two halves of the module.** The thief's
4.7 Gy is deterministic: a specific, predictable, near-certain illness in *that
person*, on a timetable set by Table 9.8. The 1000 bystanders' 11 deaths are
stochastic: nobody can be identified, the excess is 5% of a natural 204 and would
never be detectable, and the number itself rests on linear extrapolation from
0.2 Gy — right at the edge of where S&F say excess risk becomes observable at all.

*A note on the manual's arithmetic:* it interpolates $\mu_{en}/\rho=0.03260$
correctly and then substitutes 0.03206 — the tabulated 0.8 MeV value — into the
dose expression, giving 4.61 Gy. It is the same adjacent-row substitution that
appears twice in the Chapter 9 solutions (`~NE-17` `refs.md`); here it costs 2%
and changes nothing about the conclusion.
