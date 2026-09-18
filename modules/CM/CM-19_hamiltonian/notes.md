# CM-19 — Hamiltonian Mechanics (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)*.

## The Legendre transform
Trade the velocity q̇ for the conjugate momentum p = ∂L/∂q̇ (`~CM-17`) via the
**Legendre transformation** to get the **Hamiltonian** [G §8.1 p.334; F §10.9 p.455]
$$H(q,p)=p\dot q-L.$$
For L = ½mq̇² − V(q) this is H = p²/2m + V(q), the total energy (`hamiltonian_from_potential`).

## Hamilton's equations
The single second-order Euler–Lagrange equation becomes **two first-order**,
symmetric equations on the phase point (q, p) [F §10.9 p.455; G §8.1 p.334]:
$$\dot q=+\frac{\partial H}{\partial p},\qquad \dot p=-\frac{\partial H}{\partial q}.$$
Code: `hamilton_rhs`, `integrate_hamilton` (via `~MA-07`). The motion is a flow in
**phase space**; for the oscillator the orbit is a closed ellipse
p² + ω²q² = const and H (the energy) is conserved (tests). Phase-space flow is the
natural setting for chaos (`~MA-22`), statistical mechanics (Liouville's theorem,
`~CM-20`), and the correspondence to quantum mechanics (`~QM-05`), where Hamilton's
equations become Heisenberg's via the Poisson-bracket → commutator bridge of `~CM-20`.
