# 2.1 — Work (notes)

Work and heat are the only two ways energy crosses the boundary of a closed
system, and everything in Topics 3 and 9 is bookkeeping over that pair. This
module defines work, fixes its sign, establishes that it is *not* a property,
and enumerates the modes. `2.2`/`2.3` then evaluate the most important mode in
detail, and `2.4` converts all of them to rates.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18).

## 1. The mechanical definition, and why it is not enough

From mechanics, work is force through displacement [M Eq. 2.12, §2.2, p.44]:
$$\boxed{\;W=\int_{s_1}^{s_2}\mathbf F\cdot d\mathbf s\;}$$
— `work_force_displacement`, which integrates any callable $F(s)$ over a path.
The dot product is doing real work here: only the force component *along* the
displacement transfers energy.

But M is careful to note that thermodynamics "deals with phenomena not included
within the scope of mechanics" [p.44]. A battery driving a current across a
system boundary transfers energy with no macroscopic force or displacement
anywhere in sight. Eq. 2.12 cannot describe it, yet it is plainly work.

## 2. The thermodynamic definition

So the definition is broadened [M §2.2, p.44]:

> Work is done by a system on its surroundings if **the sole effect on
> everything external to the system could have been the raising of a weight**.

Three things about this deserve attention.

- It is a *test*, not a formula. It tells you whether an interaction counts as
  work, and Eq. 2.12 or one of §4's mode formulas then tells you how much.
- The subjunctive is essential: "**could have been**". The test is not whether a
  weight was actually raised, nor whether a force actually acted through a
  distance, but whether the sole external effect *could* have been the elevation
  of a weight. Nothing need be lifted anywhere.
- It reduces to the mechanical definition when a force and displacement exist,
  since raising a weight is exactly a force through a distance. The extension is
  natural rather than a redefinition.

M's Fig. 2.3 [p.45] is the pair of cases that motivates it. In system A a paddle
wheel stirs a gas: work could in principle be evaluated from the forces and
motions at the paddle boundary, consistent with Eq. 2.12. In system B a battery
drives a current across the boundary; the only external effect could have been
the raising of a weight (run the current through an ideal motor instead), so it
is work — but Eq. 2.12 is useless for computing it.

The same test is what excludes **heat**: energy crossing because of a
temperature difference cannot be made to raise a weight and nothing else, and
that is the operative distinction between the two terms of the first law.

## 3. Sign convention, and the inexact differential

Thermodynamics takes [M §2.2.1, p.45]
$$W>0 \;\;\text{work done BY the system},\qquad
W<0 \;\;\text{work done ON the system},$$
which is a historical inheritance from engine analysis — the engineer's product
is work out — and is why the first law reads $\Delta E=Q-W$ with a minus.

Work is a **path function**. There is no property $W$ of the state, so
$$\int_1^2\delta W = W \qquad\text{(not } W_2-W_1\text{)},$$
in contrast to a property such as volume, for which $\int_1^2 dV=V_2-V_1$
regardless of the route [M §2.2.1, p.46]. Hence the symbol $\delta W$: the
differential is **inexact**. Module `1.5` exhibits three quasiequilibrium paths
between the same end states that deliver three different works, and `2.2`'s
Example 2.1 does the same for three polytropic exponents.

Saying "the system contains 5 kJ of work" is therefore meaningless. A system
contains energy; work is a transfer.

## 4. The modes

Each mode has the same structure — an **intensive** force-like quantity times
the change in an **extensive** displacement-like quantity — and M collects them
in one generalized expression [M Eq. 2.26, §2.2.8, p.54]:
$$\delta W = p\,dV+\sigma\,d(Ax)+\tau_{\text{surf}}\,dA-\varepsilon\,dZ+\dots$$

| mode | force $\times$ displacement | expression | call |
|---|---|---|---|
| moving boundary | $p\times dV$ | $W=\int p\,dV$ [M Eq. 2.17, p.48] | `boundary_work` |
| rotating shaft | $\tau\times d\theta$ | $W=\tau\omega\,\Delta t$ [M Eq. 2.20, p.53] | `shaft_work` |
| electrical | $\varepsilon\times dZ$ | $\dot W=-\varepsilon i$ [M Eq. 2.21, p.53] | `electric_work` |
| elastic (bar) | $\sigma\times d(Ax)$ | $W=-\int\sigma A\,dx$ [M Eq. 2.18, p.52] | — |
| spring | $kx\times dx$ | $W=\tfrac12k(x_2^2-x_1^2)$ | `spring_work` |

The moving-boundary mode is the one thermodynamics lives on, and `2.2`/`2.3`
develop it. The electrical sign is discussed in `2.4` §4: $-\varepsilon i$ is the
signed contribution, while `electric_work` returns the magnitude.

## 5. The spring, and why work is not proportional to displacement

A linear spring resists with $F=kx$, so stretching it from $x_1$ to $x_2$ takes
$$W=\int_{x_1}^{x_2}kx\,dx=\tfrac12k\bigl(x_2^{2}-x_1^{2}\bigr)$$
— `spring_work`. Because the force grows with extension, the work is
**quadratic** in displacement, and equal increments of stretch cost unequal
amounts:

| stretch of a 200 N/m spring | work stored |
|---|---|
| 0 → 0.1 m | 1.0 J |
| 0 → 0.2 m | 4.0 J |
| 0.1 → 0.2 m | 3.0 J |

Doubling the stretch quadruples the stored energy, and the second decimetre
costs three times the first. A constant 50 N force over 3 m, by contrast, does a
flat 150 J. The lesson generalises: $W=\int F\,ds$ cares about the whole force
profile, not the endpoints — which is §3's path-dependence in miniature.

## 6. Units

Force times distance: the newton-metre, named the **joule**, with kJ the working
unit [M §2.1.3, p.43]. Every mode in §4 must come out in the same unit, which is
the arithmetic precondition for adding them in an energy balance at all. The
$p\,dV$ mode is the one to watch: with $p$ in kPa and $V$ in m³ the product is
already kJ, whereas $\tfrac12mV^2$ in kg and m/s gives J and needs dividing by
$10^{3}$ first (`2.5`).

## 7. What the code checks

`test_work.py` pins: $\int F\,ds$ for a constant force and for the linear spring,
against the closed form; the quadratic scaling of spring work (0→0.2 m storing
four times 0→0.1 m, and the 0.1→0.2 m increment being three times the first);
shaft and electrical work as rate × time; and the boundary-work integrator
agreeing with $p\,\Delta V$ at constant pressure.

## Where this goes

- `2.2` / `2.3` — the moving-boundary mode evaluated in full, both directions.
- `2.4` — every mode above, as a rate.
- `1.5` — path-dependence demonstrated on three explicit paths.
- `3.2` — work entering the first law, $\Delta E=Q-W$.
- `5.4` — the $p$–$V$ diagram, where the area *is* this integral.
