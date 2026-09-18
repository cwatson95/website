# NE-20 — Problems

Work each by hand, then check with `code/reactor_kinetics.py`. Citations in
`../refs.md`; **S&F** = Shultis & Faw 3rd ed., cited by printed page. These are
the book's Chapter 10 problems 24–27 and 30–33 (printed 368–369). Problems 1–23
are the neutron life cycle and belong to `~NE-19`.

Throughout, β = 0.0065 and ℓ₀ = 10⁻⁴ s for a ²³⁵U-fuelled thermal reactor.

### P1.  Reading a period  *(S&F Ch. 10, Prob. 24)*
A control rod is dropped into a critical, source-free reactor and the asymptotic
period of the exponentially decreasing power is −200 s. (a) What is k_eff
afterwards? (b) What was the insertion in dollars?
*Check:* k_eff = 0.99947; −0.081\$.

**Solution.** Solve the inhour equation [Eq. (10.39)] for the reactivity that
gives ω₀ = −1/200 s⁻¹:
$$k(\$)=\omega_0\left[\frac{\ell}{\beta}+\sum_i\frac{a_i}{\lambda_i+\omega_0}\right]
=\boxed{-0.0811\ \$}.$$
Then ρ = βk(\$) = −5.27×10⁻⁴, i.e. −52.7 pcm, and
$$k_{\rm eff}=\frac{1}{1-\rho}=\boxed{0.99947}.$$

**Note how little reactivity a −200 s period represents.** Five parts in ten
thousand — a change in the fourth significant figure of k_eff. This is exactly
why reactor operators work in dollars or pcm and never in k_eff: the interesting
range of k_eff is 0.999 to 1.001, and quoting it to three figures throws away all
the information.

The small-insertion formula would give T = τ/k(\$) = −160 s here, 20% short. The
inhour equation is not much harder and does not have that problem.

### P2.  Positive and negative are not symmetric  *(S&F Ch. 10, Prob. 25)*
What asymptotic period results from (a) +0.08\$ and (b) −0.08\$?
*Check:* +130 s; −202 s.

**Solution.** From the inhour equation, $\boxed{+130\ \text{s}}$ and
$\boxed{-202\ \text{s}}$.

**The asymmetry is the point** — the same reactivity magnitude gives a 55% longer
period going down than coming up. It follows from the shape of the inhour
equation: for ω < 0 the term $a_i/(\lambda_i+\omega)$ *grows* as ω approaches
−λ₁ from above, so a given negative ω needs less reactivity than the mirror
positive one.

Physically: shutting down, you must wait for existing precursors to decay, and
they set a floor. Starting up, new precursors accumulate and there is no
corresponding ceiling. **Reactors are easier to start than to stop**, which is a
statement about safety and not about convenience.

(The approximate formula, being odd in k(\$), gives ±162 s and misses the
asymmetry entirely.)

### P3.  How fast can you actually shut down?  *(S&F Ch. 10, Prob. 26)*
After a scram in which all rods are inserted, how long before the power falls to
10⁻⁴ of its steady-state value?
*Check:* about 10 minutes, essentially independent of how much negative
reactivity is inserted.

**Solution.** Two stages. The **prompt drop** takes the power to
$1/(1-k(\$))$ within a fraction of a second — for a −5\$ scram, to 0.167. The
remaining decay runs at the asymptotic period, which for any large negative
insertion is pinned near
$$T_{\min}=-\frac{55.7\ \text{s}}{\ln 2}=-80.4\ \text{s}.$$
So
$$t=T\ln\frac{10^{-4}}{1/(1-k(\$))}\approx\boxed{600\ \text{s}=10\ \text{min}}.$$

| scram worth | prompt drop | period | time to 10⁻⁴ |
|---|---|---|---|
| −5\$ | 0.167 | −80.9 s | 600 s |
| −10\$ | 0.091 | −80.6 s | 549 s |
| −20\$ | 0.048 | −80.5 s | 496 s |

**Quadrupling the scram worth buys 100 seconds.** That is the whole lesson: past
a few dollars, more negative reactivity does almost nothing, because the decay is
limited by precursor half-lives and not by how hard you push.

And this is still the *optimistic* half of the problem. It describes the fission
rate only; decay heat from accumulated fission products is ~7% of full power at
shutdown and falls as roughly $t^{-0.2}$, so it is still ~0.5% of full power a day
later. That is why emergency core cooling exists, and why Fukushima Daiichi's
reactors were destroyed hours after they had successfully scrammed.

### P4.  A 0.15\$ transient  *(S&F Ch. 10, Prob. 27)*
A 0.15\$ reactivity is inserted at t = 0 into a critical reactor. Describe the
power transient.
*Check:* prompt jump ×1.18; asymptotic period 57 s; ×4.1 in one minute.

**Solution.** The prompt jump is
$$\frac{n_+}{n_0}=\frac{1}{1-k(\$)}=\frac{1}{0.85}=\boxed{1.18},$$
complete within about ℓ₀/β ≈ 0.06 s. Thereafter the power rises with the
asymptotic period $\boxed{57\ \text{s}}$ from the inhour equation.

Integrating the six-group equations gives

| t | 1 s | 10 s | 60 s | 300 s | 600 s |
|---|---|---|---|---|---|
| n/n₀ | 1.24 | 1.60 | 4.12 | 288 | 5.8×10⁴ |

**Read the last column.** A modest 0.15\$ — a tenth of the way to prompt critical
— multiplies the power by 58 000 in ten minutes if nothing intervenes. "Slow
enough to control" does not mean "slow"; it means slow enough that a control
system with a few seconds of response time can keep up. Left alone, this
transient destroys the reactor.

### P5.  Xenon in a fast reactor  *(S&F Ch. 10, Prob. 32)*
Does ¹³⁵Xe produce reactivity feedback in a fast reactor? Why?
*Check:* essentially none.

**Solution.** **No.** ¹³⁵Xe's famous 2.7×10⁶ b cross section is a *thermal*
value, and it comes from a huge resonance essentially at zero energy. A fast
reactor's flux sits at hundreds of keV, where xenon's absorption cross section is
of order a barn — six orders of magnitude smaller and utterly unremarkable
against the fuel's own cross sections.

**The general principle is worth extracting.** Every poison in §10.9 is a
*thermal* poison; the whole phenomenon is a consequence of the 1/v law and of
low-lying resonances (`~NE-13`). A fast reactor has no xenon transient, no
poison-out, no time-to-poison, and no xenon spatial oscillations. It pays for
that with a much smaller β from ²³⁹Pu (0.0021, so every dollar is worth a third
as much δk) and a much shorter prompt lifetime — the margins move, they do not
disappear.

### P6.  Which feedback acts when?  *(S&F Ch. 10, Prob. 33)*
Over what time interval, within orders of magnitude, does each feedback act?

**Solution.**

| mechanism | time scale | sign | why |
|---|---|---|---|
| (a) fuel temperature | **ms** | − | Doppler broadening of ²³⁸U's resonances; the fuel heats where the fission happens, with no transport delay. The fastest and most important negative feedback there is. |
| (b) moderator/coolant temperature | **s** | − (LWR) | Heat must first cross the gap and clad, then the water must expand. In an undermoderated LWR less moderator means less reactivity. |
| (e) boiling in the core | **s** | − (LWR), + (RBMK) | Same mechanism as (b) but far stronger — a void removes moderator wholesale. The **sign depends on the design**, and a positive void coefficient is what made RBMK-1000 unstable at low power. |
| (f) increased coolant flow | **s** | − | Better cooling lowers the average moderator temperature, which in an LWR is negative reactivity. Note it acts *through* (b): flow is not itself a reactivity. |
| (c) ¹³⁵Xe | **hours** | − | Set by the 6.7 h and 9.2 h half-lives of the ¹³⁵I/¹³⁵Xe pair. Peaks ~11 h after a shutdown. |
| (d) fuel burnup | **months** | − | Fissile depletion and fission-product accumulation over a fuel cycle, offset by design with burnable poisons and plutonium breeding. |

**The ordering is the safety argument.** The fastest feedback (Doppler,
milliseconds) is negative and acts before any control system can; the slowest
(burnup, months) is compensated by design. The dangerous regime is a design where
one of the *fast* terms has the wrong sign — which is a design choice, not an
accident.

### P7.  Equilibrium poisoning  *(added)*
A reactor runs at φ = 10¹⁴ cm⁻² s⁻¹. What are the equilibrium xenon and samarium
reactivities, and how do they compare?
*Check:* −0.036 and −0.0068; xenon is 5.3× worse.

**Solution.** From Eqs. (10.50)–(10.51), $X_0/\Sigma_f=2.20\times10^{16}$ cm²,
so with $\rho_p\simeq-0.6\,\sigma_a^pN_p/\Sigma_f$,
$$\rho_{Xe}=-0.6(2.7\times10^{-18})(2.20\times10^{16})=\boxed{-0.0356}.$$
For samarium, $S_0/\Sigma_f=\gamma_P/\sigma_a^S=2.76\times10^{17}$ cm², giving
$\boxed{\rho_{Sm}=-0.0068}$.

**Three things follow.**

Xenon costs **5.3 times** as much reactivity as samarium, despite samarium having
twelve times the concentration — because its cross section is 66 times larger.

Together they are **4.2% of the core's reactivity**, held permanently in reserve
by the control system. That is a substantial fraction of a fuel cycle's total
excess reactivity and it is a direct design cost.

And the samarium number is the same for **every** reactor: $S_0$ has no flux in
it, because production and burnup both scale with φ. A research reactor at
10¹² and a power reactor at 10¹⁵ arrive at identical equilibrium samarium
poisoning. The xenon number, by contrast, is saturating at 10¹⁴ — which is why
the *post-shutdown* xenon peak is the operational problem and the equilibrium
value is not.
