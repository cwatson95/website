# 2.2 — Expansion Work (notes)

Module `2.1` established *what* work is and how it is measured at a boundary.
This module takes the single most important mechanical work mode in
thermodynamics — a gas pushing a piston out — and evaluates it. `2.3` is the
same integral run the other way, and `1.5` is the reason the answer depends on
the path at all.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18). Units throughout: $p$ in kPa, $V$ in
m³, so $W$ comes out in kJ.

## 1. Where the integral comes from

Work is force through distance. For a piston of face area $A$ moved a distance
$dx$ against a gas at pressure $p$, the force on the piston face is $pA$, so
[M Eq. 2.15, p.48]
$$\delta W = pA\,dx .$$
The volume swept is $dV = A\,dx$, which eliminates the geometry entirely
[M Eq. 2.16, p.48]:
$$\delta W = p\,dV .$$
Integrating between two states gives the **moving-boundary work**
[M Eq. 2.17, §2.2.3, p.48]:
$$\boxed{\;W=\int_{V_1}^{V_2} p\,dV\;}$$
For an expansion $V_2>V_1$ and, since $p>0$ always, $W>0$: **the system does
work on its surroundings**. That sign convention — work out is positive — is
what makes the first law read $\Delta U = Q - W$ rather than $Q + W$.

Two things are hiding in the step from $\delta W = pA\,dx$ to $p\,dV$, and both
matter:

- **$p$ must be the pressure at the piston face**, not an average over the gas.
  In a rapid expansion the gas near the piston is rarer, and at lower pressure,
  than the bulk.
- **$p$ must be a single well-defined number at each instant**, which is only
  true if the process is *quasiequilibrium* (module `1.5`). Otherwise there is
  no curve $p(V)$ to integrate along, and the "area under the path" is undefined
  because there is no path.

M is explicit that a $p$–$V$ curve fitted to measured data gives a plausible
estimate of $\int p\,dV$ "only when the measured pressure is essentially equal
to that exerted at the piston face" [M Example 2.1 note ➋, p.52].

## 2. Work is the area, and the area depends on the route

Because $W=\int p\,dV$ is an area under a curve, two processes joining the same
end states along different curves enclose different areas and deliver different
work [M Fig. 2.8, p.50]. Applying the property test of §1.3.3 to that
observation is how M concludes that **work is not a property**: it is a function
of the path, not of the state. This is the most important structural fact in the
subject, and module `1.5` is built on it.

The notation follows: $\delta W$, not $dW$. There is no function $W$ of the
state whose differential appears in the integral, so the "d" is deliberately not
an exact differential. The same holds for heat.

## 3. The polytropic family

Most analytically tractable expansions are **polytropic**, meaning
$pV^{n}=\text{const}$ for constant $n$ [M §2.2.5, p.50]. Substituting
$p=\text{const}/V^{n}$ into Eq. 2.17 and integrating,
$$W=\int_{V_1}^{V_2}\frac{\text{const}}{V^{n}}\,dV
=\frac{(\text{const})V_2^{1-n}-(\text{const})V_1^{1-n}}{1-n}.$$
Evaluating the constant at either end state — $\text{const}=p_1V_1^{n}=p_2V_2^{n}$
— collapses this to the form worth memorising [M Example 2.1(a), p.51]:
$$\boxed{\;W=\frac{p_2V_2-p_1V_1}{1-n}\;}\qquad (n\neq1)$$
The derivation divides by $1-n$, so $n=1$ must be treated separately. There
$p=\text{const}/V$ and the integral is a logarithm [M Example 2.1(b), p.51]:
$$\boxed{\;W=p_1V_1\ln\frac{V_2}{V_1}\;}\qquad (n=1)$$

This module exposes the two cases that come up most often:

| $n$ | path | closed form | call |
|---|---|---|---|
| $0$ | constant pressure | $W=p(V_2-V_1)$ | `constant_pressure_expansion` |
| $1$ | isothermal ideal gas ($pV=$ const) | $W=p_1V_1\ln(V_2/V_1)$ | `isothermal_expansion` |
| any | any $p(V)$ you can write down | $\int p\,dV$ numerically | `expansion_work` |

The general polytropic form for arbitrary $n$ lives in `1.2` (`polytropic_work`),
since it is shared with compression.

$n=1$ is isothermal **only for an ideal gas**, where $pV=mRT$ makes $pV=$ const
and $T=$ const the same statement. For steam or a refrigerant, $pV=$ const is
merely a curve and the isotherm is something else.

## 4. The worked case, checked against the book

M's Example 2.1 [pp.50–52] expands a gas along $pV^{n}=$ const from
$p_1=3.0$ bar, $V_1=0.1$ m³ to $V_2=0.2$ m³ — a doubling of volume — for three
exponents. The state-2 pressure follows from $p_2=p_1(V_1/V_2)^{n}$:

| case | $n$ | $p_2$ | $W$ (book) | reproduced by this module |
|---|---|---|---|---|
| (a) | 1.5 | 1.06 bar | $+17.6$ kJ | 17.57 kJ — `expansion_work` on $p=C/V^{1.5}$ |
| (b) | 1.0 | 1.5 bar | $+20.79$ kJ | 20.7944 kJ — `isothermal_expansion` |
| (c) | 0 | 3.0 bar | $+30$ kJ | 30.000 kJ — `constant_pressure_expansion` |

All three are the same volume change between the same end volumes, and the work
differs by a factor of 1.7 across them. The ordering is general and worth
carrying: **the larger $n$, the faster the pressure collapses as the gas
expands, and the less work the expansion returns.** At $n=0$ the pressure never
falls at all, and the area is the full rectangle.

The Quick Quiz on the same page runs a two-step path from the same start —
expand isothermally from 0.1 to 0.15 m³, then at constant pressure to 0.2 m³ —
and answers 22.16 kJ. Composing this module's two closed forms reproduces it:
$$W = \underbrace{(300)(0.1)\ln\tfrac{0.15}{0.1}}_{12.164}
    + \underbrace{(200)(0.2-0.15)}_{10.000} = 22.164\ \text{kJ},$$
where the constant pressure for the second leg is $p=p_1V_1/V=200$ kPa, read off
the isotherm at the hand-over point. That the legs must be joined at a consistent
pressure is the whole content of the exercise.

## 5. What the code does, and its one guard rail

`expansion_work(p_of_V, V1, V2)` evaluates $\int p\,dV$ by the trapezoid rule
over `n_steps=20000` panels — second-order accurate; convergence against a closed
form is demonstrated in `1.5`'s `fig2`. It accepts any callable $p(V)$, including
one with no closed-form integral.

It **raises `ValueError` if $V_2<V_1$**. That is deliberate: the integral would
evaluate perfectly well and return a negative number, but a negative "expansion
work" is a modelling error rather than a result, and the caller wanted module
`2.3`.

Checks in `test_expansion_work.py`: the constant-pressure and isothermal closed
forms; agreement between `expansion_work` and `constant_pressure_expansion` on a
flat $p(V)$; positivity of an expansion; the $V_2<V_1$ rejection; and all three
parts of Example 2.1 plus the Quick Quiz, so the table in §4 is pinned by tests
rather than asserted here.

## Where this goes

- `2.3` — the identical integral for $V_2<V_1$, where $W<0$ and the question
  becomes how much work must be *supplied*.
- `1.2` / `1.5` — the general polytropic form, the trapezoid machinery, and the
  path-dependence argument in full.
- `5.4` — the $p$–$V$ diagram in its own right, where a closed cycle's enclosed
  area becomes the net work.
- `3.2` — this $W$ entering the first law, $\Delta U = Q - W$.
- `9.2`–`9.4` — Otto, Diesel and dual cycles, built entirely from polytropic
  expansions and compressions joined end to end.
