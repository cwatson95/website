# CM-06 — Linear Momentum (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**G** = Goldstein 3e *(image scan)*.

## Momentum and Newton's second law
**Linear momentum** is **p** = m**v** [F §2.1 p.58]; Newton's second law in its
original form is **F** = d**p**/dt. The time integral of the force is the
**impulse** [F §7.5 p.305]:
$$\mathbf J=\int_{t_1}^{t_2}\mathbf F\,dt=\Delta\mathbf p.$$
Code: `momentum`, `impulse`; the test confirms **J** = Δ**p** for a constant force.

## Conservation of total momentum
For a system, the total momentum is **P** = Σᵢ mᵢ**v**ᵢ [G §1.2 p.6]. Internal
forces cancel in pairs by Newton's **third law**, so
$$\frac{d\mathbf P}{dt}=\mathbf F^{\rm(ext)};$$
with no external force, **P is conserved** [F §7.1 p.277]. Code: `total_momentum`;
the test shows equal-and-opposite internal impulses sum to zero, so the system's
momentum is unchanged. This is the bookkeeping behind collisions (`~CM-08`) and,
via Noether's theorem, follows from the homogeneity of space (`~CM-18`).
