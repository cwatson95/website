# CM-05 — Conservative Forces & Potential Energy (notes)

Citation key (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e.

## Conservative forces
A force is **conservative** if the work it does is path-independent — equivalently
(for a simply-connected region) if its curl vanishes [F §4.1 p.146]:
$$\nabla\times\mathbf F=\mathbf 0.$$
Code: `is_conservative` (reuses `~MA-02` `curl`). A rotational field like (−y, x, 0)
fails the test; any gradient field passes.

## Potential energy and F = −∇U
A conservative force is the (negative) gradient of a scalar **potential energy**
[F §4.2 "The Del Operator" p.151]:
$$\mathbf F=-\nabla U.$$
Code: `force_from_potential` (reuses `~MA-02` `gradient`). The work done equals the
drop in U, so the **total mechanical energy is conserved** [F §4.2 p.152]:
$$E=T+U=\tfrac12 m|\mathbf v|^2+U(\mathbf r)=\text{const}.$$
Code: `total_energy`; the test confirms E is constant along a 1-D oscillator's motion.

## Equilibria and stability
Equilibria are where the force vanishes, **U′(x) = 0**; they are **stable** (a
restoring force) where U is a minimum, **U″(x) > 0**, and unstable at a maximum
[F §2.3 p.63]. Code: `is_equilibrium`, `is_stable`. A double well U = x⁴ − 2x² has
stable minima at x = ±1 and an unstable hilltop at x = 0 (a test). Expanding U
about a minimum gives the harmonic oscillator of `~CM-15`.
