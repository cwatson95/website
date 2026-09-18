# NE-20 — References

Page-level citations **verified by reading the page text** (poppler `pdftotext`)
in the PDF under `books/library/`. **Printed** = the number on the page;
**PDF** = the viewer page.

| Book (edition) | File | Printed → PDF |
|---|---|---|
| Shultis & Faw, *Fundamentals of Nuclear Science and Engineering*, **3rd ed.** (2017) | `NE_Nuclear_Engineering/nuclear_science_shultis_faw.pdf` | PDF = printed **+ 23** |
| Shultis & Faw, *Problem Solution Manual*, 3rd ed. (2016) | `NE_Nuclear_Engineering/nuclear_science_sol_shultis_faw.pdf` | indexed by chapter/problem |

## Topic → location

| Topic (code symbol) | Section / Eq. | Printed p. | PDF p. |
|---|---|---|---|
| Reactor kinetics; why the dynamic response matters | §10.7 | 339 | 362 |
| The simple (prompt-only) model (`simple_period`) | Eqs. (10.26)–(10.29), §10.7.1 | 339–340 | 362–363 |
| Delayed neutrons; ¹³⁷I as precursor | §10.7.2, Fig. 10.7 | 340 | 363 |
| **Table 10.9** — six delayed groups (`DELAYED_GROUPS`) | Table 10.9 | 341 | 364 |
| Effective vs physical β (10–15% larger) | §10.7.2 | 341 | 364 |
| Reactivity, delta-k, dollars, pcm (`reactivity`, `dollars`) | Eq. (10.30), §10.7.3 | 342 | 365 |
| **Example 10.11** — 0.1\$ gives k_eff = 1.00065 | Ex. 10.11 | 342 | 365 |
| **Effective generation time** ℓ = ℓ₀ + βτ | Eq. (10.31), §10.7.4 | 342 | 365 |
| **Period for small insertions** (`small_insertion_period`) | Eqs. (10.32)–(10.34) | 343 | 366 |
| **Super prompt critical** (`prompt_critical_period`) | Eqs. (10.35)–(10.36) | 343 | 366 |
| Subcritical reactors; the −80 s floor | §10.7.4 | 343–344 | 366–367 |
| **Example 10.12** — 10 W to 10 kW in 884 s | Ex. 10.12 | 344 | 367 |
| Power transients; the steady-state source relation | §10.7.5, Eq. (10.37) | 344–345 | 367–368 |
| Step insertion; prompt jump; Fig. 10.8 | Eq. (10.38), §10.7.5 | 345–346 | 368–369 |
| **The inhour equation** (`inhour`, `asymptotic_period`) | Eq. (10.39) | 346 | 369 |
| Asymptotic period vs reactivity | Eqs. (10.40)–(10.42), Figs. 10.9–10.10 | 347 | 370 |
| Reactivity feedback; the block diagram | §10.8, Fig. 10.11 | 348 | 371 |
| Isotopic feedback: burnup, breeding, poisons, burnable poisons | §10.8.1 | 348–349 | 371–372 |
| **Temperature feedback**; Doppler, expansion, spectrum hardening, TRIGA | §10.8.2 | 349–350 | 372–373 |
| Fission product poisons; the 50 b collective rule | §10.9 | 351 | 374 |
| **Poison reactivity** (`poison_reactivity`) | Eqs. (10.43)–(10.45) | 351 | 374 |
| **¹³⁵Xe**; σ_a = 2.7×10⁶ b; the decay chain | §10.9.1 | 351–352 | 374–375 |
| **The I/Xe system** (`xenon_transient`) | Eqs. (10.46)–(10.49) | 352 | 375 |
| **Equilibrium I and Xe** (`iodine_xenon_equilibrium`) | Eqs. (10.50)–(10.51), Fig. 10.12 | 352–353 | 375–376 |
| Shutdown transient; time-to-poison; poison shutdown time | §10.9.1, Figs. 10.13–10.15 | 353–354 | 376–377 |
| Xenon spatial oscillations, ~10 h period | §10.9.1 | 354 | 377 |
| **¹⁴⁹Sm** (`promethium_samarium_equilibrium`) | Eqs. (10.52)–(10.55), §10.9.2 | 355–356 | 378–379 |
| **Point kinetics derivation** (`solve_point_kinetics`) | Eqs. (10.81)–(10.87), §10.11 | 362–364 | 385–387 |
| **Step-insertion solution** (`step_response`) | Eqs. (10.88)–(10.108), §10.12 | 364–366 | 387–389 |

## Problems (verified, S&F 3rd ed. Ch. 10)
Chapter 10's problems begin on printed **366** (PDF 389). Problems **24–33**
belong to this module; **1–23** are the life cycle and are worked in `~NE-19`.

- **Prob. 24** — a control-rod drop giving a −200 s period — printed 368, PDF 391.
- **Prob. 25** — asymptotic periods for ±0.08\$ — printed 368, PDF 391.
- **Prob. 26** — time to reach 10⁻⁴ of full power after a scram — printed 368, PDF 391.
- **Prob. 27** — a 0.15\$ insertion transient — printed 368, PDF 391.
- **Prob. 32** — does ¹³⁵Xe give feedback in a fast reactor? — printed 369, PDF 392.
- **Prob. 33** — the time scales of six feedback mechanisms — printed 369, PDF 392.

## Three printed slips this module corrects

### Example 10.12 cites the wrong example (printed p. 344)
It opens "If the reactor of **Example 10.7** were initially operating at a power
of 10 W…" and continues "From **Example 10.7**, the reactivity insertion is
δk = 0.00065". Example 10.7 is the fast-fission-factor calculation of §10.4 and
contains no reactivity at all; δk = 0.00065 and the 0.1\$ insertion are
**Example 10.11**'s, on the facing page. *Recorded in
`test_reproduces_examples_10_11_and_10_12`.*

### §10.7.4 inverts the lifetime formula (printed p. 344)
"…the longest lived delayed neutron precursor which has a half-life of about 55 s
(see Table 10.9) or a mean lifetime of **ln 2/T₁/₂ ≃ 80 s**." As written that is
ln2/55.7 s = 0.0124 s⁻¹, a decay *constant*. The mean lifetime is T₁/₂/ln2, and
the printed value 80 s is correct — §10.7.4 uses the right form eight lines
earlier for the *average* precursor ("τ = T₁/₂/ln 2 ≃ 12.8 s"). *Pinned by
`test_shutdown_cannot_beat_the_longest_lived_precursor`, which derives the −80.4 s
floor from the correct form and checks the inhour equation converges to it.*

### §10.9.2 attributes stability to the wrong nuclide (printed p. 356)
The closing sentence: "unlike the ¹³⁵Xe transient following a reactor shutdown,
the ¹⁴⁹Sm transient does not decay away with time **since ¹⁴⁹Pm is stable**."

¹⁴⁹Pm has a **53 h half-life** — the decay chain printed three paragraphs earlier
in the same section says so, and Eq. (10.52) is built on its decay constant λ_P.
It is ¹⁴⁹**Sm** that is stable, which the section's own opening sentence states
("This stable nuclide is a daughter of…"). The physics of the conclusion is right
and the reason given is not. *Pinned by
`test_samarium_equilibrium_is_independent_of_flux`, which asserts λ_P > 0 and
recovers the 53 h half-life.*

Two smaller slips in the same section: Eq. (10.55)'s final term carries
σ_a^**X** where σ_a^**S** belongs (xenon's cross section in a samarium equation),
and the flux-independent equilibrium S₀ = γ_P Σ_f/σ_a^S is attributed to
Eq. (10.52) when it follows from setting Eq. (10.53) to zero.

## The ℓ notation collision
S&F use the symbol ℓ for two quantities that differ by a factor of **840**:

- **Eq. (10.31)**, §10.7.4: ℓ = ℓ₀ + βτ ≈ 0.084 s — the *effective* generation
  time averaged over prompt and delayed neutrons.
- **Eq. (10.83)**, §10.11: ℓ ≡ ℓ₀/k_eff ≈ 10⁻⁴ s — the *prompt* generation time,
  and the ℓ of the point kinetics equations and of the inhour equation (10.39).

Eq. (10.42) — "T_as ≃ ℓ/(βk₀), which is in agreement with Eq. (10.33)" — is
correct only under the **first** reading; under the second it gives 0.57 s where
the answer is ~100 s. It sits one paragraph below Eq. (10.39), which uses the
second. The very next sentence, "for k₀ ≫ 1\$, T_as ≃ (ℓ/β)/(k₀−1)", requires the
**second** reading to agree with Eq. (10.36).

The module names them `effective_generation_time` and `prompt_generation_time`,
and `test_the_mean_precursor_lifetime_is_the_control_time_scale` pins the ratio.

## How good is Eq. (10.33), where the book uses it?
Example 10.12 applies T = βτ/δk at 0.1\$ and gets 128 s. The exact inhour
equation gives **98 s** — the approximation is **32% high** at the point of use.

The approximation replaces Σ a_i/(λ_i+ω) by Σ a_i/λ_i, which requires
ω ≪ λ_min = 0.0124 s⁻¹, i.e. T ≫ 80 s. At 0.1\$ the true period is 98 s, barely
above the floor, and the longest-lived group — which contributes 20% of τ — is
the one most affected. The error falls below 1% only under about 0.01\$.

This is not an erratum: S&F state the condition |δk| ≪ β. It is worth quantifying
because 0.1\$ *looks* small. `test_the_small_insertion_formula_is_already_32_
percent_high_at_0_1_dollars` measures it and checks the error shrinks
monotonically as the insertion does.

## Where the module refuses rather than answering

**`small_insertion_period` beyond 0.3\$.** Eq. (10.33) does not diverge at prompt
critical — it keeps returning a plausible number. At 1.5\$ it reports 8.6 s where
the truth is 0.030 s, a **287-fold** error in the direction of "there is plenty of
time". Nothing in the formula's shape warns you; only the refusal does.

**`prompt_jump_factor` at or above 1\$.** 1/(1−k(\$)) diverges there, which is the
mathematical signature of prompt criticality: above 1\$ there is no
jump-then-drift, only an excursion.

## Cross-module dependencies
- **`~NE-19`** — the six factors; a control rod is a change in f, Doppler is a
  change in p.
- **`~NE-09`** — fission-product yields γ_I = 0.061, γ_X = 0.003, γ_P = 0.0113.
- **`~NE-21`** — the spatial flux the point model integrates away; xenon
  oscillations are exactly what a point model cannot represent.
- **`~NE-22`**, **`~NE-23`** — control and burnup as engineering.
- **`~MA-11`** — the coupled linear ODE system and its eigenvalues.

## Further reading
- Keepin, G.R., *Physics of Nuclear Kinetics* (1965) — the source of Table 10.9
  and still the standard reference for delayed-neutron data.
- Hetrick, D.L., *Dynamics of Nuclear Reactors* — point kinetics with feedback,
  including the nonlinear Nordheim–Fuchs model of a prompt excursion.
- Duderstadt & Hamilton, *Nuclear Reactor Analysis*, Ch. 6–7 — the derivation of
  point kinetics from the transport equation, and where "point" stops being valid.
- INSAG-7, *The Chernobyl Accident: Updating of INSAG-1* (IAEA, 1992) — the xenon
  poisoning, positive void coefficient and prompt excursion of §§10.8–10.9 in one
  documented sequence.
