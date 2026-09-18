# CM-20 — Poisson Brackets & Canonical Transformations (notes)

Citation key (details + PDF pages in `refs.md`): **G** = Goldstein 3e *(image scan)*.

## The Poisson bracket
For one degree of freedom [G §9.5 p.388]:
$$\{f,g\}=\frac{\partial f}{\partial q}\frac{\partial g}{\partial p}
         -\frac{\partial f}{\partial p}\frac{\partial g}{\partial q}.$$
It is bilinear and **antisymmetric**, {f,g} = −{g,f}, and the **fundamental
bracket** is {q, p} = 1 (a test). Code: `poisson_bracket`.

## Dynamics in bracket form
Hamilton's equations (`~CM-19`) collapse into one statement [G §9.6 p.396]:
$$\frac{df}{dt}=\{f,H\}+\frac{\partial f}{\partial t}.$$
So q̇ = {q, H} = ∂H/∂p and ṗ = {p, H} = −∂H/∂q, and **a quantity is conserved iff
its bracket with H vanishes** — e.g. {H, H} = 0 (energy), {p, H} = 0 for a free
particle (momentum). Code: `time_derivative`.

## Canonical transformations
A change of variables (q, p) → (Q, P) is **canonical** — it preserves the form of
Hamilton's equations — iff it preserves the fundamental bracket [G §9.5 p.388]:
$$\{Q,P\}=1.$$
Code: `is_canonical`. Phase-space scalings (Q = λq, P = p/λ) and the swap
(Q = p, P = −q) pass; Q = q, P = 2p fails (tests). Preserving {q,p} is the same as
preserving phase-space volume — **Liouville's theorem** (`~MA-22`). Replacing the
bracket by {,} → (1/iℏ)[,] turns this whole structure into quantum mechanics — the
Poisson-bracket → commutator bridge to `~QM-05` (one of the KEY BRIDGES).
