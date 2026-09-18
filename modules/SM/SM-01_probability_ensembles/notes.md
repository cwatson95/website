# SM-01 — Probability Foundations & Ensembles (notes)

Statistical mechanics connects the microscopic (10²³ molecules obeying mechanics)
to the macroscopic (a handful of thermodynamic variables) by **counting**. The
central quantity is the **multiplicity** Ω — how many microstates correspond to a
given macrostate — and everything follows from one postulate about it.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria & Beale,
*Statistical Mechanics* 3e; **Sch** = Schroeder, *Thermal Physics* (image-only).
Page numbers are the *printed* book pages.

## 1. Microstates, macrostates, and the fundamental postulate
A **microstate** is a complete specification of the system (every spin, every
molecule's position and momentum); a **macrostate** is the coarse description
(total energy, magnetization, …). The **fundamental postulate** [Pa §1.1, p.1]:
*an isolated system in equilibrium is equally likely to be in any of its accessible
microstates.* The probability of a macrostate is then
$$P(\text{macrostate})=\frac{\Omega(\text{macrostate})}{\Omega_\text{total}},$$
so the most probable macrostate is simply the one with the largest multiplicity.
Code: `multiplicity_two_state(N,n)` = C(N,n) counts the microstates of a two-state
(spin-½ paramagnet / coin) system; `multiplicity_einstein_solid(N,q)` = C(q+N−1,q)
counts ways to share q energy quanta among N oscillators.

## 2. Boltzmann entropy
Define the **entropy** as the logarithm of the multiplicity [Pa §1.2, p.3]:
$$\boxed{\,S=k\ln\Omega\,}$$
The logarithm makes entropy **extensive**: two independent systems have
Ω = Ω₁Ω₂, so S = k ln(Ω₁Ω₂) = S₁ + S₂. Maximizing S subject to constraints
reproduces all of thermodynamics (the program of `~SM-02`/`~SM-03`). Code:
`boltzmann_entropy(omega, k)`; with k = 1 it returns the entropy in nats, with
k = `K_B` in J/K. The additivity is checked in the demo and tests.

## 3. Stirling's approximation
Counting requires factorials of huge numbers, tamed by **Stirling's formula**
[Pa §1.4, p.10; Sch Ch.2]:
$$\ln n! = n\ln n - n + \tfrac12\ln(2\pi n) + \cdots$$
The leading $n\ln n - n$ already gives entropies to fractions of a percent for
$n\sim 10^{23}$; the $\tfrac12\ln(2\pi n)$ term is negligible per particle but
useful for moderate n. Code: `stirling_ln_factorial(n)` (refined) and its
`leading_only=True` form, benchmarked against `math.lgamma`.

## 4. The two-state distribution and the thermodynamic limit
For N fair two-state elements the macrostate "n up" has probability
$$P(N,n)=\frac{1}{2^N}\binom{N}{n},$$
a **binomial** distribution (`~MA-19`) with mean N/2 and variance N/4. Its
**fractional width** is
$$\frac{\sigma}{\langle n\rangle}=\frac{\sqrt N/2}{N/2}=\frac{1}{\sqrt N},$$
so the relative fluctuations vanish as N → ∞: at N ~ 10²³ the distribution is a
delta function and the macrostate is effectively certain — this is *why*
thermodynamics is deterministic [Pa §1.2, p.3]. Near the peak the binomial becomes
a **Gaussian** (de Moivre–Laplace), `gaussian_approx_two_state` = MA-19's
`normal_pdf(n; N/2, √N/2)`. Code: `two_state_probability`, `fractional_width`.

## Where this goes
- `~SM-02` turns S = k ln Ω into temperature (1/T = ∂S/∂U) and the laws of thermodynamics.
- `~SM-03` recasts the counting as the **canonical ensemble** and the partition function.
- `~MA-19` supplies the binomial/normal machinery; the 1/√N law is the central-limit theorem.
- The same "log of a count" entropy reappears as Shannon/Gibbs entropy −k Σ P ln P (`~SM-03`).
