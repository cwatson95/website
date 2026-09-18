# CM-16 — Coupled Oscillations & Normal Modes (notes)

Citation keys (details + PDF pages in `refs.md`): **F** = Fowles & Cassiday 7e ·
**MT** = Marion & Thornton 5e *(image scan)*.

## The small-oscillation eigenproblem
Near a stable equilibrium a system of coupled oscillators obeys
$$M\ddot{\mathbf x}=-K\mathbf x,$$
with **M** the (diagonal) mass matrix and **K** the symmetric stiffness matrix
(K_ij = ∂²U/∂x_i∂x_j). Trying **x** = **v** e^{iωt} turns it into the
**generalized eigenvalue problem** [F §11.3 p.472; MT §12.6 p.483]
$$K\mathbf v=\omega^2 M\mathbf v.$$

## Reducing to MA-04
Writing **u** = M^{1/2}**v**, this becomes the *symmetric* eigenproblem of
A = M^{−1/2} K M^{−1/2}, which `~MA-04`'s `eig_symmetric` diagonalizes:
- eigenvalues → the **normal-mode frequencies** ω (squared);
- eigenvectors → the **normal modes** (after **v** = M^{−1/2}**u**), which are
  **orthonormal in the mass inner product** vᵀMv.

Code: `normal_modes`, `mode_inner_product`. In each normal mode every particle
oscillates at the *same* frequency; a general motion is a superposition of modes —
the spatial analogue of a Fourier series (`~MA-09`). The two-equal-mass chain
gives the in-phase mode ω = √(k/m) and the out-of-phase mode ω = √(3k/m) (a test).
This is the same diagonalization as rigid-body principal axes (`~CM-13`) and the
linear-ODE eigen-method of `~MA-07`.
