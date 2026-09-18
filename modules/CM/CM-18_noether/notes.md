# CM-18 — Symmetries & Noether's Theorem (notes)

Citation keys (details + PDF pages in `refs.md`): **G** = Goldstein 3e *(image
scan)* · **MT** = Marion & Thornton 5e *(image scan)*.

## Symmetry ⇒ conservation
Noether's theorem: **every continuous symmetry of the Lagrangian yields a
conserved quantity** [G §2.6 p.54]. For a transformation δq = ε f(q) that leaves L
unchanged, the conserved **Noether charge** is
$$Q=\frac{\partial L}{\partial\dot q}\,f(q).$$
Code: `noether_charge`; `symmetry_defect` measures the first-order change in L
under the flow (≈ 0 means f generates a symmetry).

## The three classic cases
| symmetry | generator | conserved quantity |
|---|---|---|
| **translation** in q | f = 1 (q → q + ε) | momentum p = ∂L/∂q̇ (`~CM-06`) |
| **rotation** | f = ∂(rotation) | angular momentum (`~CM-09`) |
| **time-translation** | ∂L/∂t = 0 | energy h = q̇ ∂L/∂q̇ − L (`~CM-19`) |

Each is a **cyclic coordinate**: if L does not depend on a coordinate, its
conjugate momentum is conserved [G §2.6 p.54]. The tests show the free particle
is translation-symmetric (defect ~0) with conserved momentum, the harmonic
oscillator breaks translation (its V depends on q) but conserves **energy** because
L has no explicit time, and a dilation is *not* a symmetry of the oscillator.

This is the deepest organizing principle in physics: the conservation laws of
`~CM-06`/`~CM-09` are *consequences* of the homogeneity and isotropy of space and
the homogeneity of time. The group-theoretic side is `~MA-18`; gauging the symmetry
gives the interactions of `~QF-03`.
