# SM-03 — Problems

Work by hand, then check with `code/classical_statmech.py`. Citations in
`../refs.md`; **Pa** = Pathria 3e, **Sch** = Schroeder (image-only).

### P1.  Boltzmann factor and the partition function  *(Pa §3.2, p.41)*
For a three-level system {0, ε, 2ε}, write Z(T) and the occupation probabilities.
Show the ground state dominates as T → 0 and all levels equalize as T → ∞. *Check:*
`boltzmann_probability([0,1e-21,2e-21], T)` sums to 1 and is ordered P₀ > P₁ > P₂.

*Answer:* $Z=1+e^{-x}+e^{-2x}$ ($x=\varepsilon/kT$), $P_n=e^{-nx}/Z$; $P_0\to1$ as $T\to0$, all $\to\tfrac13$ as $T\to\infty$.

**Solution.** Writing $x\equiv\beta\varepsilon=\varepsilon/kT$, the three Boltzmann weights
$e^{-\beta E_i}$ are $1,\,e^{-x},\,e^{-2x}$, so
$$Z=\sum_i e^{-\beta E_i}=1+e^{-x}+e^{-2x},\qquad P_n=\frac{e^{-nx}}{Z}\quad(n=0,1,2).$$
Since $e^{-x}<1$ for every $T>0$, the weights fall with energy and $P_0>P_1>P_2$. As $T\to0$,
$x\to\infty$ so $e^{-x},e^{-2x}\to0$, giving $Z\to1$ and $P_0\to1$ — the system freezes into the
ground state. As $T\to\infty$, $x\to0$ so every weight $\to1$, $Z\to3$ and each $P_n\to\tfrac13$ —
the levels equalize. This is exactly what `boltzmann_probability([0,1e-21,2e-21], T)` returns: a
list summing to $1$ with $P_0>P_1>P_2$.

### P2.  U = −∂lnZ/∂β  *(Pa §3.3, p.50)*
Show the mean energy ⟨E⟩ = Σ E_i P_i equals −∂lnZ/∂β. *Check:* `internal_energy`
matches a numerical −d(lnZ)/dβ for a 4-level system.

*Answer:* $-\partial\ln Z/\partial\beta=Z^{-1}\sum_i E_i e^{-\beta E_i}=\sum_i E_iP_i=\langle E\rangle$.

**Solution.** Differentiate $\ln Z$ for $Z=\sum_i e^{-\beta E_i}$, using
$\partial_\beta e^{-\beta E_i}=-E_i e^{-\beta E_i}$:
$$-\frac{\partial\ln Z}{\partial\beta}=-\frac1Z\frac{\partial Z}{\partial\beta}=\frac1Z\sum_i E_i\,e^{-\beta E_i}=\sum_i E_i\,\frac{e^{-\beta E_i}}{Z}=\sum_i E_iP_i=\langle E\rangle.$$
So the thermodynamic energy is literally the log-derivative of the partition function. The closed
form $\sum_i E_iP_i$ computed by `internal_energy` therefore equals the finite-difference
$-d(\ln Z)/d\beta$ for the 4-level system (e.g. $5.69\times10^{-22}$ J at $T=80$ K).

### P3.  Heat capacity is an energy fluctuation  *(Pa §3.3, p.50)*
Derive C = dU/dT = Var(E)/(kT²). *Check:* `heat_capacity(levels, T)` equals the
numerical dU/dT.

*Answer:* $C=dU/dT=\operatorname{Var}(E)/(kT^2)\ge0$ — heat capacity is an energy fluctuation.

**Solution.** With $U=-\partial_\beta\ln Z$ and $\beta=1/kT$ (so $d\beta/dT=-1/kT^2$), the chain rule
gives
$$C=\frac{dU}{dT}=\frac{dU}{d\beta}\frac{d\beta}{dT}=\Big(-\frac{\partial^2\ln Z}{\partial\beta^2}\Big)\Big(-\frac1{kT^2}\Big)=\frac1{kT^2}\frac{\partial^2\ln Z}{\partial\beta^2}.$$
The second derivative of $\ln Z$ is the energy variance (its second cumulant),
$\partial^2_\beta\ln Z=\langle E^2\rangle-\langle E\rangle^2=\operatorname{Var}(E)$, hence
$$C=\frac{\operatorname{Var}(E)}{kT^2}\ge0.$$
A response function equals an equilibrium fluctuation — the simplest fluctuation–dissipation
relation. The variance form `heat_capacity(levels, T)` thus reproduces the numerical $dU/dT$
(e.g. $7.79\times10^{-24}$ J/K for the 4-level system at $T=80$ K).

### P4.  The Schottky anomaly  *(Pa §3.9, p.70)*
For a two-level system {0, ε}, find ⟨E⟩ and C(T). Show C → 0 at both T → 0 and
T → ∞ and peaks in between. *Check:* `two_level_heat_capacity(eps, T)` is largest
near kT ≈ 0.42 ε and small at T = 1 K and T = 10⁸ K.

*Answer:* $\langle E\rangle=\varepsilon/(e^{\beta\varepsilon}+1)$; $C=k(\beta\varepsilon)^2 e^{\beta\varepsilon}/(e^{\beta\varepsilon}+1)^2\to0$ at both extremes, peaking at $kT\approx0.42\,\varepsilon$.

**Solution.** With levels $\{0,\varepsilon\}$ and $x=\beta\varepsilon=\varepsilon/kT$, $Z=1+e^{-x}$ and
only the upper level carries energy:
$$\langle E\rangle=\frac{\varepsilon\,e^{-x}}{1+e^{-x}}=\frac{\varepsilon}{e^{x}+1}.$$
The variance is $\operatorname{Var}(E)=\langle E^2\rangle-\langle E\rangle^2=\varepsilon^2/(e^x+1)-\varepsilon^2/(e^x+1)^2=\varepsilon^2 e^{x}/(e^{x}+1)^2$, so
$$C=\frac{\operatorname{Var}(E)}{kT^2}=k\,x^2\,\frac{e^{x}}{(e^{x}+1)^2}.$$
At low $T$ ($x\to\infty$) this $\sim kx^2e^{-x}\to0$ (the gap is frozen); at high $T$ ($x\to0$) it
$\sim kx^2/4\to0$ (both levels equally full). So $C$ vanishes at both ends and bumps between,
peaking near $x\approx2.4$, i.e. $kT\approx0.42\,\varepsilon$. Accordingly
`two_level_heat_capacity(eps, T)` is largest near $kT\approx0.42\,\varepsilon$ ($C/k\approx0.44$ at
$T\approx30$ K, with $\varepsilon/k=72.4$ K) and small at $T=1$ K and $T=10^8$ K.

### P5.  Einstein solid and Dulong–Petit  *(Pa §3.8, p.65)*
For a quantum oscillator show ⟨E⟩ → ℏω/2 (zero-point) as T → 0 and ⟨E⟩ → kT
(equipartition) as T → ∞, and that the Einstein heat capacity → k at high T and
freezes out below ℏω/k. *Check:* `harmonic_oscillator_energy` and
`einstein_heat_capacity` limits; `equipartition_energy(3, N, T) = (3/2)NkT`.

*Answer:* $\langle E\rangle\to\hbar\omega/2$ ($T\to0$), $\to kT$ ($T\to\infty$); $C\to k$ at high $T$, freezes below $\hbar\omega/k$; $U=\tfrac32 NkT$.

**Solution.** Let $y=\beta\hbar\omega=\hbar\omega/kT$, so
$\langle E\rangle=\hbar\omega\big(\tfrac12+\tfrac1{e^{y}-1}\big)$. As $T\to0$, $y\to\infty$ and
$1/(e^y-1)\to0$, leaving the zero-point energy $\hbar\omega/2$. As $T\to\infty$, $y\to0$ and
$e^y-1\approx y$, so $1/(e^y-1)\approx kT/\hbar\omega$ and
$$\langle E\rangle\to\hbar\omega\Big(\tfrac12+\frac{kT}{\hbar\omega}\Big)\approx kT,$$
classical equipartition. The Einstein heat capacity $C=k\,y^2 e^{y}/(e^{y}-1)^2\to k$ as $y\to0$
(Dulong–Petit) and $\sim k\,y^2 e^{-y}\to0$ for $y\gg1$ (frozen out below $\hbar\omega/k$). Each of
three quadratic translational degrees of freedom adds $\tfrac12 kT$, so $U=\tfrac32 NkT$. Numerically
($\hbar\omega/k=76.4$ K): `harmonic_oscillator_energy` gives $\langle E\rangle/\hbar\omega=0.50$ at
$T=10$ K, `einstein_heat_capacity`$/k\to1.0$ at high $T$ and $\sim6.5\times10^{-3}$ at $T=8$ K, and
`equipartition_energy(3, N, T)` $=\tfrac32 NkT$.
