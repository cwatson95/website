# NE-20 — Reactor kinetics: point kinetics, delayed neutrons, feedback, xenon (notes)

`~NE-19` asked whether a reactor is critical. This module asks what happens when
it is not, and the whole answer rests on one number:

> For ²³⁵U, **β = 0.0065** of the fission neutrons are *delayed*.

Citation key (full details in `refs.md`): **S&F** = Shultis & Faw 3rd ed.,
§§10.7–10.9 and Addenda 2–3, cited by **printed** page (PDF = printed + 23).

## 1. Why 0.65% of the neutrons decide everything

Take the naive model [Eq. (10.27)]: a cycle of length $\ell_0$, a gain of
$k_{\rm eff}-1$ per cycle, so
$$n(t)=n_0\exp\left[\frac{k_{\rm eff}-1}{\ell_0}t\right].$$
With $\ell_0=10^{-4}$ s and a **0.1%** increase in $k_{\rm eff}$, after one second
$n/n_0=e^{10}\approx22\,000$. No operator and no control system could act in time.

But some fission neutrons are not emitted at fission. They come from the β-decay
of certain fission products — ¹³⁷I is S&F's example — seconds to minutes later.
The average precursor lives $\tau=\sum a_i/\lambda_i=12.95$ s, so the *effective*
generation time [Eq. (10.31)] is
$$\ell=(1-\beta)\ell_0+\beta(\ell_0+\tau)=\ell_0+\beta\tau\approx0.084\ \text{s},$$
**840 times longer than $\ell_0$**. The same insertion now gives an 84 s period
and a 1.2% rise in a second.

That is the entire margin on which reactor control depends, and it is why
reactivity is measured in **dollars**, $k(\$)=\rho/\beta$: the natural unit is the
delayed fraction itself.

**The margin shrinks as fuel burns.** β is 0.0065 for ²³⁵U, 0.0026 for ²³³U and
0.0021 for ²³⁹Pu [Table 10.9]. As plutonium builds in over a cycle, the same
δk is worth up to three times as many dollars — an end-of-life core is markedly
more responsive than a fresh one.

## 2. The prompt-critical cliff

Reactivity in dollars makes the danger legible. At $k(\$)=1$ — $\rho=\beta$ —
the prompt neutrons alone sustain the chain, the delayed ones are no longer
needed, and the period stops being set by $\tau$ and starts being set by $\ell_0$
[Eq. (10.36)]:
$$T=\frac{\ell_0/\beta}{k(\$)-1}.$$

| $k(\$)$ | asymptotic period |
|---|---|
| 0.1 | 98 s |
| 0.5 | 5.8 s |
| 0.9 | 0.49 s |
| **1.5** | **0.030 s** |
| 5.0 | 0.0039 s |

**Three orders of magnitude across one decade of reactivity.** That is what
"prompt critical" means, and it is why the module's `small_insertion_period`
**refuses** beyond 0.3\$: Eq. (10.33) does not blow up at the cliff, it keeps
returning a comfortable-looking number. At 1.5\$ it would report 8.6 s where the
truth is 0.03 s — a 280-fold error in the direction of *there is plenty of time*.

**A caution about the approximation itself.** Even where S&F use it, it is not
very good. Example 10.12 gets $T=128$ s for 0.1\$; the exact inhour equation
gives **98 s**. The approximation replaces $\sum a_i/(\lambda_i+\omega)$ by
$\sum a_i/\lambda_i$, which needs $\omega\ll\lambda_{\min}=0.0124$ s⁻¹, i.e.
$T\gg80$ s — and 98 s is barely above that. Not an erratum; an approximation
whose 32% error is worth knowing.

## 3. The shutdown speed limit

The same physics runs backwards, and it is less comfortable. After a large
negative insertion the prompt neutrons vanish at once, but the *existing*
precursors keep decaying at their own rate. So the power falls in two stages: a
**prompt drop** by $1/(1-k(\$))$, then an exponential whose period cannot be
faster than the longest-lived precursor group:
$$T_{\min}=-\frac{55.7\ \text{s}}{\ln2}=-80.4\ \text{s}.$$

The module reproduces exactly that floor from the inhour equation: −83.5 s at
−1\$, −80.9 s at −5\$, −80.4 s at −100\$. **You cannot scram faster than this.**
Reaching $10^{-4}$ of full power takes about ten minutes however hard you push —
and that is *before* decay heat, which does not care about the chain reaction at
all. This is the physics behind every loss-of-cooling accident.

## 4. Point kinetics

Tracking precursors explicitly gives the **point reactor kinetics equations**
[Eqs. (10.86)]:
$$\frac{dn}{dt}=\frac{\rho-\beta}{\ell}n+\sum_i\lambda_iC_i+S,\qquad
\frac{dC_i}{dt}=\frac{\beta_i}{\ell}n-\lambda_iC_i.$$

Assuming $e^{\omega t}$ gives the **inhour equation** [Eq. (10.39)]
$$\omega\left[\frac{\ell}{\beta}+\sum_i\frac{a_i}{\lambda_i+\omega}\right]=k(\$),$$
with $G+1$ roots; the largest, $\omega_0$, gives the asymptotic period, and the
rest decay away as the prompt jump.

**A notation warning.** S&F write both $\ell_0+\beta\tau\approx0.084$ s
[Eq. (10.31)] and $\ell_0/k_{\rm eff}\approx10^{-4}$ s [Eq. (10.83)] as "$\ell$",
and the two differ by a factor of 840. Eq. (10.42) is only correct with the
first; Eqs. (10.39) and (10.84)–(10.87), which surround it, use the second. The
module names them `effective_generation_time` and `prompt_generation_time` on
purpose.

## 5. Feedback: what makes a reactor self-regulating

$k_{\rm eff}$ is not a constant of the machine; the machine changes it as it
runs [§10.8]. Slowly, by **isotopic** change — fuel burnup (negative), plutonium
breeding (positive), fission-product poisons (negative), burnable poisons
(positive, by design, to offset burnup). Quickly, by **temperature**:

- **Doppler broadening** — the dominant term. Hot fuel nuclei move, smearing
  ²³⁸U's resonances so more neutrons are captured, so $p$ falls. It acts in
  *milliseconds*, faster than any control system, and it is negative.
- **Moderator expansion** — LWRs are deliberately run slightly *undermoderated*
  (`~NE-19` §6), so losing moderator moves them further from the optimum and
  $k$ falls. Voiding is the extreme case and is strongly negative in an LWR.
- **Spectrum hardening** — mostly negligible, except that ²³⁹Pu's 0.3 eV
  resonance makes it *positive*, which limits how much plutonium a core may hold.
  TRIGA fuel exploits the opposite sign deliberately: ZrH's vibrating hydrogen
  pulls neutrons out of the thermal group within milliseconds, which is what lets
  those reactors be pulsed far above prompt critical and survive.

**A reactor is safe only if the net coefficient is negative.** A positive one is
not merely undesirable, it is a positive feedback loop — the RBMK-1000's positive
void coefficient at low power is the reason Chernobyl-4's excursion could not
stop itself.

## 6. Xenon: the poison that grows after you shut down

¹³⁵Xe has $\sigma_a=2.7\times10^6$ b — **the largest thermal absorption cross
section of any nuclide**, 54 000 times the 50 b rule-of-thumb used for fission
products collectively. It sits in the ¹³⁵Te → ¹³⁵I → ¹³⁵Xe chain, and the
dynamics turn on one asymmetry [Eqs. (10.50)–(10.51)]:
$$\frac{I_0}{\Sigma_f}=\frac{\gamma_I\phi}{\lambda_I}\quad\text{(linear for ever)},
\qquad
\frac{X_0}{\Sigma_f}=\frac{(\gamma_I+\gamma_X)\phi}{\lambda_X+\sigma_a^X\phi}
\quad\text{(saturates above }\phi\sim7.8\times10^{12}).$$

**Iodine grows without limit; xenon saturates**, because above that flux the
xenon is burned out as fast as it is made. So a high-power reactor sits on an
iodine reservoir *ten times* its xenon inventory — and after a scram that
reservoir decays into xenon with no flux to burn it.

The result: **the poison keeps growing for about 11 hours**, peaking at 4.5× its
operating value, and does not fall back below that value for over a day. If the
peak exceeds the control system's available positive reactivity the reactor has
**poisoned out** and cannot be restarted at all. With 0.10 of override, the
time-to-poison from $\phi=10^{14}$ is **2.5 hours**, and the lockout lasts about
30 — S&F's "15–25 hour poison shutdown time".

That two-and-a-half-hour window, and the production pressure to use it, is a
recognisable ingredient of the Chernobyl-4 sequence.

**Samarium** is quieter and stranger. ¹⁴⁹Sm is *stable*, so its only loss channel
is burnup — and since both production and loss scale with flux, its equilibrium
$$\frac{S_0}{\Sigma_f}=\frac{\gamma_P}{\sigma_a^S}$$
is **independent of flux entirely**. Every reactor ends up with the same
equilibrium samarium poisoning whatever its power. And unlike xenon, the
post-shutdown buildup is permanent: nothing removes it until the reactor restarts.

## Where this goes

- `~NE-19` — the six factors whose changes *are* the reactivity.
- `~NE-21` — where the spatial flux shape comes from; xenon oscillations are a
  spatial instability the point model cannot see.
- `~NE-22` — control rods, boron, burnable poisons as engineering.
- `~NE-23` — burnup reactivity loss over a fuel cycle.
- `~NE-09` — the fission-product yields γ_I, γ_X, γ_P.
- `~MA-11` — the coupled linear ODE system this is.

## A note on this module's corrections

Three printed slips in §§10.7–10.9, all pinned by tests or by the docstrings.

1. **Example 10.12** refers twice to "the reactor of Example 10.7". Example 10.7
   is the fast-fission-factor calculation of §10.4; the 0.1\$ insertion and the
   δk = 0.00065 it quotes belong to **Example 10.11**.
2. **§10.7.4** gives the longest precursor's mean lifetime as "ln 2/T₁/₂ ≃ 80 s".
   The formula is inverted — ln2/55.7 s is 0.0124 s⁻¹, a decay *constant*; the
   lifetime is T₁/₂/ln2, and the printed **value** 80 s is right.
3. **§10.9.2** closes by saying the samarium transient does not decay away
   "since ¹⁴⁹Pm is stable". ¹⁴⁹Pm has a **53 h half-life** — the decay chain three
   paragraphs earlier says so — and it is ¹⁴⁹**Sm** that is stable. (Eq. (10.55)
   also carries σ_a^**X** where σ_a^**S** belongs, and the equilibrium samarium is
   attributed to Eq. (10.52) when it follows from Eq. (10.53).)
