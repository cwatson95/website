# CM-09 — Angular Momentum & Torque (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)*.

## Definitions
For a particle [F §7.2 p.278; G §1.2 p.6]:
$$\mathbf L=\mathbf r\times\mathbf p=m(\mathbf r\times\mathbf v),\qquad
  \mathbf N=\mathbf r\times\mathbf F.$$
Both reuse `~MA-01`'s `cross`. Code: `angular_momentum`, `torque`.

## The rotational equation of motion
Differentiating **L** and using **F** = m**a**,
$$\frac{d\mathbf L}{dt}=m\,\frac{d}{dt}(\mathbf r\times\mathbf v)
 =m(\underbrace{\mathbf v\times\mathbf v}_{0}+\mathbf r\times\mathbf a)
 =\mathbf r\times\mathbf F=\mathbf N.$$
So **torque is the rate of change of angular momentum** — the angular analogue of
**F** = d**p**/dt. Code: `torque_rate` (uses `~CM-01`'s `acceleration`); the test
differentiates `angular_momentum_of` along an arbitrary trajectory and recovers **N**.

## Conservation under a central force
If **F** is **central** (parallel to **r**), then **N** = **r** × **F** = **0**,
so **L is conserved** [F §6.4 p.226]. A constant **L** confines the motion to a
plane and gives Kepler's equal-areas law — the foundation of the orbit problem
`~CM-11`. For uniform circular motion **L** = m R²ω **ẑ** is constant (a test).
