# 2.7 — Buoyancy (notes)

The one fluid-statics leaf of Topic 2, kept here because M develops it in
Chapter 1 alongside pressure measurement, and because the $\rho g$ product it
turns on is the same one that carries `2.6`'s potential energy. The mechanics
trunk (`~CM`) treats fluid statics properly; this module covers what a
thermodynamics course needs — Archimedes' principle, and the density ratio that
decides whether a thing floats.

Citation key (full table in `refs.md`): **M** = Moran, Shapiro, Boettner &
Bailey, *Fundamentals of Engineering Thermodynamics*, 8th ed., cited by
**printed** page (PDF = printed + 18).

## 1. Pressure with depth

In a continuous fluid at rest, pressures at equal elevations are equal, and an
elementary force balance on a column of liquid of height $L$ gives
[M Eq. 1.11, §1.6.1, p.15]
$$p=p_{\text{atm}}+\rho g L ,$$
with $p_{\text{atm}}$ the local atmospheric pressure and $\rho$ the fluid
density. This is the integrated form of the hydrostatic relation
$dp/dz=-\rho g$ (with $z$ positive upward), specialised to constant $\rho$ and
$g$ — a good approximation "for short columns of liquid" [M p.16], which is why
manometer and barometer readings can be quoted as a length of mercury at all.

Everything in this module follows from that single linear-in-depth statement.

## 2. Archimedes, derived rather than asserted

Because pressure increases downward, the pressure forces acting on the underside
of a submerged body are larger than those on its top, and the resultant — the
**buoyant force** — acts vertically upward [M §1.6.2, p.16].

M evaluates it for a rectangular block of horizontal area $A$ whose top and
bottom faces sit at depths $L_1$ and $L_2$ [M Fig. 1.11, p.17]:
$$F = A(p_2-p_1)
= A\bigl(p_{\text{atm}}+\rho g L_2\bigr)-A\bigl(p_{\text{atm}}+\rho g L_1\bigr)$$
$$= \rho g A\,(L_2-L_1)
= \boxed{\;\rho\,g\,V\;}$$
— `buoyant_force`. Two cancellations carry the whole result:

- **$p_{\text{atm}}$ drops out.** The ambient pressure pushes equally on top and
  bottom, so buoyancy does not depend on it. A body is no more buoyant at sea
  level than on a mountain, other things equal.
- **$A(L_2-L_1)$ is just the volume.** The area and the depths disappear into
  $V$, which is why the result holds for a body of *any* shape, not only the
  block used to derive it.

So the buoyant force equals the weight of the displaced liquid — Archimedes'
principle — and it depends on the density of the **fluid**, never on that of the
body. The body's density decides only what the buoyant force has to compete
with.

## 3. Apparent weight

A submerged body hung from a scale reads its true weight less the buoyant force
$$W_{\text{apparent}}=W-\rho_{\text{fluid}}\,g\,V$$
— `apparent_weight`. For a 10 L steel block ($\rho=7850$ kg/m³) the true weight
is 770.1 N; immersed in water it reads 672.0 N, a relief of 98.1 N, which is
$\rho_{\text{water}}gV$ and comes to 12.7% of its weight. The reading reaches
zero when the fluid density matches the body's, and would go negative — the body
floats up — beyond it.

This is the measurement Archimedes is supposed to have used: weighing a crown in
air and again in water gives $V$ without deforming it, and $W/gV$ is then the
density that identifies the metal.

## 4. Floating, and the density ratio

A freely floating body sinks until the buoyant force balances its weight, using
only the *submerged* part of its volume:
$$\rho_{\text{fluid}}\,g\,V_{\text{sub}}=\rho_{\text{body}}\,g\,V_{\text{total}}
\quad\Longrightarrow\quad
\boxed{\;\frac{V_{\text{sub}}}{V_{\text{total}}}=\frac{\rho_{\text{body}}}{\rho_{\text{fluid}}}\;}$$
— `submerged_fraction`. Both $g$ and the shape cancel, leaving a pure density
ratio. Equilibrium exists only while that ratio is below 1, which is the
predicate `floats(rho_object, rho_fluid)`; at exactly 1 the body is neutrally
buoyant at any depth, and above it there is no equilibrium and it sinks.

| body | $\rho$ (kg/m³) | in fresh water | submerged |
|---|---|---|---|
| cork | 240 | floats | 24.0% |
| oak | 750 | floats | 75.0% |
| ice | 917 | floats | 91.7% |
| steel | 7850 | sinks | — |

Ice in **sea** water ($\rho\approx1025$) sits $917/1025=89.5\%$ under, which is
the proverbial tip of the iceberg — about a ninth of it shows. The figure is
sensitive to which water you mean, and that is the point of writing the relation
as a ratio.

## 5. What the code checks

`test_buoyancy.py` pins: $F_b=\rho gV$; the apparent-weight subtraction; the
`floats` predicate on either side of the boundary; the submerged fraction for
ice in fresh and in sea water; the cancellation of $g$ (the same fraction at a
different gravity); and neutral buoyancy at $\rho_{\text{body}}=\rho_{\text{fluid}}$.

## Where this goes

- `2.6` — the same $\rho g$ product, there carrying gravitational potential
  energy rather than a pressure gradient.
- `1.4` — density and specific volume as intensive properties; buoyancy is
  entirely a statement about *intensive* densities, which is why sizes cancel.
- `~CM` — fluid statics and dynamics proper, where this becomes one boundary
  condition among many.
- `13.4`/`13.5` — the other fluids leaves of this trunk, where the fluid moves
  and viscosity enters.
