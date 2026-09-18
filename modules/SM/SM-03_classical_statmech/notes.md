# SM-03 — Classical Statistical Mechanics (notes)

Where `~SM-01` counts microstates of an *isolated* system (fixed energy), most
systems instead exchange energy with a **heat bath**. The right tool is then the
**canonical ensemble** and its partition function.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria 3e;
**Sch** = Schroeder (image-only). Printed pages. β ≡ 1/kT throughout.

## 1. The canonical ensemble
A small system in thermal contact with a large reservoir at temperature T has the
probability of microstate i [Pa §3.1–3.2, p.40–41]:
$$P_i=\frac{e^{-\beta E_i}}{Z},\qquad Z=\sum_i e^{-\beta E_i},$$
the **Boltzmann distribution**. Z, the **partition function**, normalizes the
probabilities and (it turns out) contains all the thermodynamics. Code:
`partition_function`, `boltzmann_probability` (the implementation shifts by the
ground-state energy for numerical stability).

## 2. Thermodynamics from Z
Every potential is a derivative of ln Z [Pa §3.3, p.50]:
$$U=\langle E\rangle=-\frac{\partial\ln Z}{\partial\beta},\qquad
  F=-kT\ln Z,\qquad S=\frac{U-F}{T}=-k\sum_i P_i\ln P_i.$$
The Helmholtz free energy is the bridge back to `~SM-02`. The two forms of S — the
thermodynamic $(U-F)/T$ and the Gibbs $-k\sum P\ln P$ — agree. Code:
`internal_energy`, `helmholtz_from_partition`, `entropy_canonical`.

## 3. Heat capacity = energy fluctuations
Differentiating $U=-\partial\ln Z/\partial\beta$ again gives a **fluctuation–
dissipation** relation [Pa §3.3]:
$$C=\frac{\partial U}{\partial T}=\frac{\langle E^2\rangle-\langle E\rangle^2}{kT^2}
   =\frac{\operatorname{Var}(E)}{kT^2}\ \ge 0.$$
A response function (heat capacity) equals an equilibrium fluctuation (energy
variance) — a theme that recurs throughout statistical physics. Code:
`heat_capacity` uses the variance form directly.

## 4. Two-level system and the Schottky anomaly
For levels $\{0,\varepsilon\}$, $\langle E\rangle=\varepsilon/(e^{\beta\varepsilon}+1)$,
giving a heat capacity that **vanishes at both extremes** and peaks near
$kT\sim0.42\,\varepsilon$ — the **Schottky anomaly** [Pa §3.9, p.70]:
$$C=k\,(\beta\varepsilon)^2\frac{e^{\beta\varepsilon}}{(e^{\beta\varepsilon}+1)^2}.$$
Cold, the gap is frozen; hot, both levels are equally full — only in between can
the system absorb heat. Code: `two_level_energy`, `two_level_heat_capacity`.

## 5. Harmonic oscillator, Einstein solid, and equipartition
The quantum oscillator (Pa §3.8, p.65) has
$\langle E\rangle=\hbar\omega(\tfrac12+1/(e^{\beta\hbar\omega}-1))$: the **zero-point**
$\hbar\omega/2$ as $T\to0$, and **equipartition** $kT$ as $T\to\infty$. Its heat
capacity (the **Einstein** model of a solid) tends to $k$ per oscillator at high T
(Dulong–Petit) and freezes out below $\hbar\omega/k$. Equipartition itself
[Pa §3.7, p.61] gives $\tfrac12kT$ per quadratic degree of freedom, so $U=(f/2)NkT$.
Code: `harmonic_oscillator_energy`, `einstein_heat_capacity`, `equipartition_energy`.

## 6. The grand canonical ensemble
Allowing particle exchange too, sum over N with fugacity $z=e^{\beta\mu}$ [Pa §4.2, p.93]:
$$\Xi=\sum_{N} z^{N} Z_N .$$
This is the natural setting for `~SM-04`'s quantum gases. Code: `grand_partition_function`.

## Where this goes
- `~SM-04` replaces the Boltzmann factor with Bose–Einstein / Fermi–Dirac occupations.
- `~SM-02` receives F = −kT ln Z and the other potentials.
- `~SM-05` builds the Ising partition function to study phase transitions.
- The fluctuation–dissipation idea (C = Var(E)/kT²) reappears as susceptibility = spin fluctuations (`~SM-05`).
