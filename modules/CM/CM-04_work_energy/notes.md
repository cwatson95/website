# CM-04 — Work & Energy (notes)

Citation key (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e.

## Work and kinetic energy
The **work** done by a force along a path is the line integral [F §4.1 p.145]
$$W=\int_C \mathbf F\cdot d\mathbf l,$$
which is literally `~MA-02`'s `line_integral`. **Kinetic energy** is T = ½m|v|².

## The work–energy theorem
From **F** = m d**v**/dt, dotting with **v** dt = d**l** and integrating gives
[F §4.1 "The Work Principle" p.145]
$$W=\int_{\mathbf a}^{\mathbf b}\mathbf F\cdot d\mathbf l=T_b-T_a=\Delta T.$$
The net work on a particle equals its change in kinetic energy — regardless of
the kind of force. **Power** is the rate of working, P = **F**·**v**. Code:
`work`, `kinetic_energy`, `power`; the test integrates the work along the actual
path of a constant-force motion and checks it equals ΔT.

## Where this goes
When the force is **conservative** the work is path-independent and can be stored
as a **potential energy** — the next module, `~CM-05`, with F = −∇U and the
conservation law T + U = E. Energy accounting also distinguishes elastic from
inelastic collisions in `~CM-08`.
