# 2.6 — Potential Energy (notes)

`2.5` derived kinetic energy from Newton's second law and stopped at the
work–energy theorem. This module takes that theorem as its *point of departure*
— M's own phrase [p.42] — and extends it: by singling out gravity from the other
forces, a second energy store appears that depends only on position. Together
with internal energy these make the total $E=U+\mathrm{KE}+\mathrm{PE}$
[M Eq. 2.27, §2.3, p.55] that the energy balances of `1.1` and `1.2` account for.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18). This module works in **joules** ($m$ in
kg, $z$ in m, $g$ in m/s²); the balances in `1.1`/`1.2` want kJ.

## 1. Splitting gravity out of the resultant force

Take a body of mass $m$ moving vertically from $z_1$ to $z_2$, with $z$ measured
positive **upward**. Two forces act: gravity, of magnitude $mg$ directed
downward, and $R$, the resultant of everything else [M Fig. 2.2, p.42].

The work–energy theorem (`2.5`, Eq. 2.6) equates the total work of all forces to
$\Delta\mathrm{KE}$. Writing that total as the two contributions
[M Eq. 2.7, p.42]:
$$\tfrac12m\bigl(V_2^{2}-V_1^{2}\bigr)=\int_{z_1}^{z_2}R\,dz-\int_{z_1}^{z_2}mg\,dz .$$
The minus sign on the gravity term is not a convention to memorise — it is
forced: the gravitational force points down while $z$ increases upward, so the
dot product $\mathbf{F}\cdot d\mathbf{s}$ is negative for a rising body.

The gravity integral is trivial **if $g$ is constant**, which M assumes
throughout [TAKE NOTE, p.42], and Eq. 2.8 follows:
$$\int_{z_1}^{z_2}mg\,dz=mg\,(z_2-z_1).$$
Substituting into Eq. 2.7 and moving that term to the left [M Eq. 2.9, p.42]:
$$\tfrac12m\bigl(V_2^{2}-V_1^{2}\bigr)+mg\,(z_2-z_1)=\int_{z_1}^{z_2}R\,dz .$$
The structural move is the rearrangement itself. What began as *work done by
gravity* on the right has become a *stored quantity* on the left, sitting
alongside kinetic energy and sharing its units. Naming it gives the
**gravitational potential energy** [M Eq. 2.10, §2.1.2, p.42]:
$$\boxed{\;\Delta\mathrm{PE}=\mathrm{PE}_2-\mathrm{PE}_1=mg\,(z_2-z_1)\;}
\qquad \mathrm{PE}=mgz$$
— `delta_PE` and `potential_energy`, with $g$ defaulting to the standard
$9.81\ \mathrm{m/s^{2}}$ but overridable, since M's own worked example uses
$9.7$.

Read Eq. 2.9 again with the names attached: the work of all forces *other than
gravity* equals the change in kinetic **plus** potential energy. Gravity has
been removed from the work ledger and promoted to a store. That bookkeeping
trick is the prototype for every potential in physics.

## 2. The sign of gravity's work

Since $\Delta\mathrm{PE}$ was *defined* as the negative of the work gravity
does,
$$W_{\text{gravity}}=-\Delta\mathrm{PE}=-mg\,(z_2-z_1)$$
— `work_by_gravity`. So:

- a body **rising** ($z_2>z_1$) gains PE, and gravity does **negative** work on
  it: something else must supply the energy;
- a body **falling** gains nothing in PE — it loses it — and gravity does
  **positive** work, which (with $R=0$) reappears as kinetic energy.

Raising 10 kg by 50 m takes $\Delta\mathrm{PE}=(10)(9.81)(50)=4905$ J; released,
gravity returns exactly $+4905$ J. The two are the same number with opposite
signs, which is what makes the gravitational field *conservative* and what lets
pumped-storage hydro work at all.

## 3. The datum is arbitrary; only differences are physical

$\mathrm{PE}=mgz$ requires a choice of where $z=0$, and nothing in the physics
selects it. Shifting the datum by $z_0$ shifts every potential energy by the
constant $-mgz_0$ — and cancels identically from
$$\Delta\mathrm{PE}=mg\bigl[(z_2-z_0)-(z_1-z_0)\bigr]=mg(z_2-z_1).$$
So two analysts using different datums will disagree about how much potential
energy a body "has" and agree exactly about every $\Delta\mathrm{PE}$, every
work, and every heat. `fig2_datum_independence` draws three datum choices as
three parallel lines and marks the common 30 m fall.

The practical rule: pick any datum, and keep it fixed for the whole problem. The
same freedom, and the same discipline, attaches to the enthalpy and entropy
datums of the steam tables (`5.1`), where the reference is saturated liquid at
the triple point and only differences are ever used.

## 4. Constant $g$, and when it fails

Eq. 2.8 assumed $g$ constant over the elevation change. Since
$g\propto 1/r^{2}$, over a height $h$ near the surface
$$\frac{\Delta g}{g}\approx-\frac{2h}{R_\oplus},$$
which for $h=1$ km and $R_\oplus\approx6.37\times10^{6}$ m is about $-0.03\%$.
For any terrestrial engineering problem the assumption is far better than the
data. It fails for orbital mechanics, where $\mathrm{PE}=-GMm/r$ replaces $mgz$
— and where the datum is conventionally taken at infinity rather than at the
ground, which is why orbital potential energies are negative.

## 5. Units, and the book's own worked check

M works a units example on p.43 that this module reproduces. A 1 kg system
descends 10 m where $g=9.7\ \mathrm{m/s^{2}}$:
$$\Delta\mathrm{PE}=(1)(9.7)(-10)=-97\ \mathrm{J}=-0.097\ \mathrm{kJ},$$
which the book quotes as $-0.10$ kJ. `delta_PE(1.0, 0.0, -10.0, g=9.7)` returns
$-97.0$ J; `test_potential_energy.py` pins it against the book's rounded value,
alongside the same example's $\Delta\mathrm{KE}=0.34$ kJ from `2.5` — the two
were computed on the same system precisely so the units could be compared.

Note the magnitudes: a 15 m/s speed-up is worth 0.34 kJ, a 10 m drop only
0.097 kJ, while the internal energy of that same kilogram of water changes by
hundreds of kJ for a modest temperature change. That ordering is why
$\Delta\mathrm{PE}$ is the first term dropped from a closed-system balance, and
`1.1`'s `fig1` makes the same point for flow devices: a 300 m elevation change
is under 0.1% of a typical steam enthalpy.

## 6. Consistency checks in the code

`test_potential_energy.py` pins: $\mathrm{PE}=mgz$; $\Delta\mathrm{PE}$ for both
a rise and a fall; $W_{\text{gravity}}=-\Delta\mathrm{PE}$; datum independence,
by evaluating the same fall against three different datums and asserting one
answer; and M's $-0.10$ kJ units example.

## Where this goes

- `2.5` — kinetic energy, the other half of the same derivation.
- `1.2` — $\Delta\mathrm{PE}$ in the closed-system balance
  $Q-W=\Delta U+\Delta\mathrm{KE}+\Delta\mathrm{PE}$.
- `1.1` / `6.4` — the $gz$ term of the flow energy $\psi=h+V^{2}/2+gz$, and the
  criterion for dropping it.
- `2.7` — buoyancy, the other place a $\rho g$ product governs a mechanical
  balance, and the fluid-statics leaf of this topic.
