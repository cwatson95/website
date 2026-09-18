# SM-05 — Phase Transitions & Critical Phenomena (notes)

A **phase transition** is a point where the free energy of `~SM-03` loses
analyticity in the thermodynamic limit, so a small change in temperature or field
produces a qualitative change of state. The Ising model is the minimal setting.

Citation key (full details + PDF pages in `refs.md`): **Pa** = Pathria 3e;
**Sch** = Schroeder (image-only). Printed pages. (In Pathria 3e the criticality
chapter is **Ch.12**, exact results **Ch.13**, the renormalization group **Ch.14**.)

## 1. The mean-field (Weiss) Ising model
Each spin $s_i=\pm1$ couples to its $q$ neighbors with energy $-J\sum_{\langle ij\rangle}s_is_j$.
**Mean-field theory** replaces the neighbors by their average $m=\langle s\rangle$,
so each spin sees an effective field and [Pa §12.5, p.420]:
$$\boxed{\,m=\tanh\!\big[(T_c/T)\,m+b\big]\,},\qquad T_c=\frac{qJ}{k},$$
with $b=\mu B/kT$ a reduced applied field. Code: `critical_temperature`,
`mean_field_magnetization` (solved by **bisection**: near $T_c$ the map slope $\to1$
and fixed-point iteration crawls — critical slowing down).

## 2. Spontaneous magnetization and the order parameter
At $b=0$ the equation $m=\tanh[(T_c/T)m]$ has only $m=0$ for $T>T_c$ (the slope at
the origin is $T_c/T<1$), but a **nonzero** solution appears for $T<T_c$: a
**spontaneous magnetization** that switches on continuously — a **second-order**
transition. $m$ is the **order parameter**; it is the analogue of `~SM-03`'s
fluctuation story, with the susceptibility $\partial m/\partial b$ diverging at
$T_c$. Code: `spontaneous_magnetization`, `mean_field_residual`.

## 3. Critical exponent β
Expanding $\tanh$ for small $m$ near $T_c$ gives $m\simeq\sqrt3\,(1-T/T_c)^{1/2}$, so
[Pa §12.7, p.435]:
$$m\sim (T_c-T)^{\beta},\qquad \beta=\tfrac12\ \ (\text{mean field}).$$
Real 3-D magnets have $\beta\approx0.33$; mean field is exact only above four
dimensions — fixing it is the job of the **renormalization group** (Pa Ch.14, §14.1,
p.540; `~QF-04`). Code: `critical_exponent_beta` recovers ½ by a log–log slope.

## 4. The exact 1-D Ising chain
Solved exactly by the transfer matrix [Pa §13.2, p.476], the 1-D chain has
$$m=\frac{\sinh(\beta h)}{\sqrt{\sinh^2(\beta h)+e^{-4\beta J}}},$$
which is **0 at $h=0$ for every $T>0$**: no spontaneous magnetization, no transition.
Thermal fluctuations destroy long-range order in one dimension. (The 2-D Ising model,
Pa §13.4, p.488, *does* order — Onsager's solution.) Code: `ising_1d_magnetization`.

## 5. Landau theory
Near a continuous transition, expand the free energy in the (small) order parameter
respecting symmetry $m\to-m$ [Pa §12.10, p.442]:
$$F(m)=a(T-T_c)\,m^2+b\,m^4,\qquad a,b>0.$$
For $T>T_c$ a single well at $m=0$; for $T<T_c$ a **double well** at
$m_0=\pm\sqrt{a(T_c-T)/2b}\sim(T_c-T)^{1/2}$ — the same $\beta=\tfrac12$. Code:
`landau_free_energy`, `landau_equilibrium_magnetization`.

## Where this goes
- `~QF-04` — the renormalization group explains why distinct systems share critical exponents (universality).
- `~SM-03` — the diverging susceptibility is the fluctuation–dissipation theme at criticality.
- The Landau expansion is the template for order parameters across physics (superconductivity, the Higgs field).
