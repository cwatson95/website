# CM-13 — Rigid-Body Dynamics (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## The inertia tensor
For rotation about a point, **L** = I**ω** and T = ½**ω**·I**ω**, where the
**inertia tensor** is [F §9.1 p.361; MT §11.3 p.415]
$$I_{ij}=\sum_a m_a\big(r_a^2\,\delta_{ij}-r_{a,i}\,r_{a,j}\big).$$
It is real and **symmetric**. Code: `inertia_tensor`; the scalar moment about a
unit axis **n** is n·I·n (`moment_about_axis`). In general **L** is *not* parallel
to **ω** — the body wobbles.

## Principal axes (the MA-04 bridge)
Because I is symmetric it can be **diagonalized by an orthogonal transformation**
(`~MA-04`): its eigenvectors are the **principal axes** and its eigenvalues the
**principal moments** I₁, I₂, I₃ [F §9.2 p.371; MT §11.5 p.424]:
$$I=Q\,\mathrm{diag}(I_1,I_2,I_3)\,Q^{\mathsf T}.$$
Along a principal axis, **L** = I_k**ω** is parallel to **ω** (a steady rotation).
Code: `principal_axes` is literally `eig_symmetric` from MA-04 — the from-scratch
Jacobi eigensolver built back in the Math trunk. The tests confirm the principal
moments are the eigenvalues, the axes are orthonormal, and the moments are
**invariant under rotating the body** (they are intrinsic). This diagonalization
is what makes Euler's equations (`~CM-14`) simple, and it is the same linear-algebra
move as quantum observables (`~QM-05`).
