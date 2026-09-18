# NE-18 — Radiation health effects: deterministic & stochastic risk, LNT (notes)

`~NE-17` produced a number in sieverts. This module turns it into a statement
about people — and the first thing to get right is that there are **two kinds of
statement**, and they behave in opposite ways.

| | threshold? | dose changes | example |
|---|---|---|---|
| **deterministic** | yes | the **severity** | erythema, cataract, marrow failure |
| **stochastic** | none established | the **probability** | cancer, hereditary illness |

Below a deterministic threshold the effect happens to *nobody* — not "few". Above
it, everybody who gets a bigger dose gets a worse effect. Stochastic effects are
the reverse: a radiogenic cancer is indistinguishable from a spontaneous one, so
the effect exists only as a statistical excess.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§9.5–9.10, cited by **printed** page (PDF = printed + 23).

## 1. Deterministic effects, and why the dose convention matters

Table 9.7 tabulates a threshold $D_{th}$ and a median effective dose $D_{50}$ for
each endpoint. The most radiosensitive is the testes (0.3 Gy threshold for a
two-year sperm suppression) — six times below the marrow-death threshold — and
the range across the table spans 0.3 to 40 Gy.

Lethality [Table 9.8] is stated as LD*x*/60, the dose fatal to *x*% within 60
days, without medical treatment:

| | mid-line dose (Gy) |
|---|---|
| LD5/60 | 2.0–2.5 |
| **LD50/60** | **3.0–3.5** |
| LD99/60 | 4.5–5.5 |

**The whole span from "almost everyone lives" to "almost everyone dies" is a
factor of 2.2 in dose.** That is why accident dosimetry has to be good to tens of
percent, and it is why the *dose convention* matters: S&F name three (free-field
exposure in R, whole-body average, mid-line), and the **mid-line dose in rad is
about ⅔ the free-field exposure in R**. Confusing them is a 50% error in a place
where 50% moves you two rows down the table.

Above about 6 Gy, death shifts from marrow failure to gastrointestinal failure;
above 50 Gy to cardiovascular and neurological failure within days; above 500 Gy
it is nearly instantaneous. The clinical course [§9.5.3] is prodromal → **latent**
→ manifest illness → recovery, and the latent stage is the dangerous one to
misread: two to three weeks of apparent well-being.

## 2. Hereditary effects, and the mouse in the middle

Risk estimates rest on the **doubling dose** — the gonad dose that adds as many
mutations as arise spontaneously [§9.6.2]:
$$DD=\frac{R_{\rm human}}{R^{\rm rad}_{\rm mice}}=\frac{2.95\times10^{-6}}{3.6\times10^{-6}}=0.82\ \text{Gy}\to1\ \text{Gy}.$$

Look at what that fraction is made of. The numerator is a **human spontaneous**
rate; the denominator is a **mouse induced** rate. There is no human induced rate
— *no heritable effect has ever been demonstrated in the atomic-bomb survivors*,
the most intensively studied exposed population in history. The entire hereditary
risk estimate is an interspecies extrapolation.

Not every mutation becomes a disease, so [Eq. (9.13)]
$$\text{risk per Gy}=P\times\frac{1}{DD}\times MC\times PRCF,$$
with $MC$ the mutation component and $PRCF$ the potential recoverability
correction factor. For dominant and X-linked disorders,
$16\,500\times0.3\times(0.15\text{–}0.30)/1\ \text{Gy}=750\text{–}1500$ per Gy per
million progeny [Eq. (9.14)].

**The correction factors, not the baselines, drive the answer.** Chronic
multifactorial disease has a baseline 39× larger (650 000 per million) and
contributes a *comparable* risk, because its $MC\times PRCF$ is 75× smaller.

The bottom line of Table 9.11: 3000–4700 excess cases per Gy per million progeny
in the first generation, against a baseline of 738 000 — **an 0.4–0.6% increase
over the natural rate for a whole gray to the gonads.**

## 3. Cancer, and the region where measurement stops

> "Excess cancer risk cannot be observed at doses less than about 0.2 Gy and,
> therefore, risks for lower doses cannot be determined directly." — §9.7

That single sentence governs everything after it. Every risk coefficient comes
from high-dose data (chiefly Hiroshima and Nagasaki), and every regulation
applies to doses far below where the effect has ever been seen.

The transfer is done by (i) assuming linearity, and (ii) dividing by a **DDREF**
of 1.5 for solid cancers to account for repair at low dose rate. Leukemia is
handled separately with a linear-quadratic model, because its dose response
visibly curves.

Two summary numbers are worth carrying:

- **Table 9.13** — excess lifetime risk by age at exposure. Solid-cancer risk
  falls **elevenfold** from infancy to age 80; leukemia risk is nearly flat. The
  reason is latency: solid cancers seldom appear before 10 years and keep
  appearing for 30 or more, so an older person may not live to express one, while
  leukemia appears within a few years.
- **§9.7.3** — the sex-averaged fatal-cancer risk factor,
  $$0.5(480+660)/(0.1\ \text{Gy}\times10^5)=0.057\ \text{Gy}^{-1},$$
  rounded to 0.05/Gy = $5\times10^{-4}$ per rem. Note that §9.9.2 quotes NCRP's
  $10^{-2}$ Sv⁻¹ for the same quantity — **5.7× smaller, in the same chapter.**
  Neither is wrong; they are different committees' fits, and the spread is an
  honest measure of the uncertainty.

For adjudication rather than prediction, the **probability of causation**
[Eq. (9.17)] is $PC=ERR/(1+ERR)$: not a physical quantity but a legal instrument,
because no test can attribute an individual tumour.

### The collective-dose trap

Linearity means only the product $N\times D$ matters, so $10^7$ people at
0.01 mSv "produce" the same 5.7 deaths as 1000 people at 100 mSv. S&F state this
as a property of the model. ICRP-103 states that computing deaths this way from
trivial individual doses "is not reasonable and should be avoided".
`radiogenic_cancer_deaths` **refuses** an individual dose below a tenth of natural
background unless explicitly overridden — the arithmetic is fine; it is the
extrapolation underneath that has no support, and a confident number hides that.

## 4. Radon: the largest exposure, and a subtle quantity

Radon is half the world's natural background (`~NE-17` §6) and possibly a
significant fraction of lung cancer. The hazard is **not** the radon: it is a
noble gas and is exhaled. It is the short-lived daughters [Eq. (9.18)], which
deposit in the bronchial epithelium and decay there.

The right quantity is the **potential alpha energy concentration** [Eq. (9.19)]:
the alpha energy that *will eventually* be emitted, which weights each daughter
by its mean life $1/\lambda$ rather than its activity:
$$E_{\rm tot}=(E_1+E_4)\frac{C_1}{\lambda_1}+E_4\left(\frac{C_2}{\lambda_2}+\frac{C_3}{\lambda_3}+\frac{C_4}{\lambda_4}\right).$$

**²¹⁴Pb and ²¹⁴Bi emit no alpha particles at all and carry 90% of the hazard** —
each holds ²¹⁴Po's 7.687 MeV in escrow and lives hundreds of times longer than
²¹⁸Po. ²¹⁴Po's own term is negligible: it lives 164 µs.

Computed from the chain's own constants this gives **34 689 MeV m⁻³ per Bq m⁻³ of
EEC = 5.56 × 10⁻⁹ J m⁻³**, the internationally accepted value, which S&F never
state. It also reproduces their WLM footnote: 1 WL ≡ 1.3 × 10⁵ MeV/L → 3748 Bq/m³
(conventionally 3700), and 170 h of it is 629 000 Bq h m⁻³.

Plate-out keeps the daughters below equilibrium, so the **equilibrium factor**
$F=E_{\rm tot}/E^{\rm equil}_{\rm tot}<1$ (EPA uses 0.5) and the **equilibrium
equivalent concentration** is $EEC=F\,C_0$ [Eq. (9.21)].

The dominant result [Table 9.15]: **a smoker's radiogenic lung-cancer risk is ten
times a non-smoker's** for the same radon exposure. The two hazards multiply
rather than add, so radon remediation is worth ten times as much to a smoker, and
neither can be assessed alone.

## 5. Standards: a risk comparison, not a threshold

The 1972 ICRP task-group argument [§9.9.1] is worth seeing, because it explains
what a dose limit *is*:

- Occupations "with a high standard of safety" kill fewer than 100 workers per
  million per year; take 50 per million as acceptable, over a 40-year career.
- Average doses run ~10% of the most-exposed individual's, so allow the
  individual limit to be 10× the average target.
- $(10\times0.002)/(40\ \text{y}\times10^{-4}\ \text{rem}^{-1})=5$ rem/y
  = **50 mSv/y**.

For the public, $0.004/(70\times10^{-4})=5.7$ mSv/y — and the adopted limit was
5 mSv/y, with today's continuous-exposure limit **1 mSv/y**. That factor of ~6
between the risk argument and the adopted number is ALARA, not arithmetic.

**A dose limit is therefore not a biological boundary.** It is a comparison with
accident rates in industries already agreed to be safe, run backwards through an
assumed linear risk coefficient. Table 9.17's structure follows: 50 mSv/y
occupational stochastic, 500 mSv/y to a single organ (ten times looser, because
it guards a *threshold* rather than a probability), 1 mSv/y public, and a
"negligible individual risk level" 100× below that.

## 6. Hormesis, and what §9.10 is actually doing

S&F devote a section to arguing that the LNT model may be wrong at low dose:
Cohen's county-level study finding lung cancer *decreasing* 7% per pCi/L of
radon; nuclear-worker cohorts with relative cancer mortality of 0.45–0.76;
high-background regions in China and India with inverse correlations. They also
give the mechanism — free-radical scavengers, DNA repair enzymes, division delay
and apoptosis — that a threshold or hormetic model would need.

The module carries **all five** shapes of Fig. 9.3 and **fits none of them**. That
is the honest position: at the doses regulation is written about, the candidate
models differ by less than anything ever measured, and the choice of LNT is a
choice of the most conservative shape available where measurement stops. Note the
asymmetry S&F do not spell out — most of the hormesis evidence is ecological or
observational, where a healthy-worker effect and confounding by smoking are
exactly the kind of bias that produces relative risks below 1.

## Where this goes

- `~NE-17` — supplies the effective dose this module consumes, and the 2.4 mSv/y
  background that is its unit of comparison.
- `~NE-16` — every epidemiological excess is a counting problem; the 0.2 Gy
  observability floor is a statistical-power statement.
- `~NE-22`, `~NE-23` — the limits derived here are design constraints there.
- `~NE-27` — therapy deliberately drives deterministic effects into the tumour
  while keeping them out of everything else.
- `~ST-12` — the risk-model machinery this module specialises.

## A note on this module's five corrections

Five printed results in this chapter are contradicted by the book's own numbers.
Each is pinned by a test.

1. **Table 9.11** second-generation column adds to 3950; its Total row prints
   3930. Unlike the others this one is *not resolvable from the book alone* — the
   percentage row was computed from the printed total, so the two agree with each
   other. The test pins the inconsistency, not a resolution.
2. **Example 9.7** prints "3116 radon-induced deaths" where its own factors give
   3416 — and its own next sentence divides by 73 years to get 47/y, which
   requires 3416.
3. **Example 9.7** quotes natural respiratory-cancer mortality "from Table 9.12"
   as 71.9 and 25.2 per 10⁵; Table 9.12 says 76.2 and 42.2, and its four columns
   add correctly to its own totals. The answer is 592 deaths/y, not 486.
4. **Solution manual, ²²⁶Ra body burden** uses 6.288 MeV for ²²²Rn's alpha. That
   is **²²⁰Rn's** alpha; Appendix D gives 5.4897 MeV for ²²²Rn. The dose rate is
   4.99 rad/y, not 5.15.
5. **Solution manual, the banana problem** computes λ(⁴⁰K) with 3600 s per day
   instead of 86 400, and N(⁴⁰K) ten times too small. The errors partly cancel:
   30.9 Bq where natural potassium's specific activity gives 12.9 Bq.
