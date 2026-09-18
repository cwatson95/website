# MA-08 — Partial Differential Equations (notes)

Citation keys (details + PDF pages in `refs.md`): **B** = Boas 3e ·
**Gr** = Griffiths 4e. Pages are the *printed* book pages. (Butkov is image-only
and cited at chapter level in `refs.md`, without page numbers.)

## 1. The three classic linear PDEs
| equation | form | physics |
|---|---|---|
| **Laplace** | ∇²u = 0 | electrostatic potential, steady-state temperature [B §13.2 p.621; Gr §3.1 p.113] |
| **heat/diffusion** | u_t = α∇²u | temperature, diffusion, (imaginary t) Schrödinger [B §13.3 p.628] |
| **wave** | u_tt = c²∇²u | strings, sound, EM waves [B §13.4 p.633] |

## 2. Separation of variables — the analytic engine
Seek u(x,t) = X(x)T(t). Substituting and dividing forces each side to equal a
constant (the **separation constant**), splitting one PDE into ODEs (`~MA-07`)
[Gr §3.3 p.130]. For the heat equation on [0,L] with u(0)=u(L)=0,
the spatial ODE X″=−k²X with those boundary conditions only admits k = nπ/L, giving
$$u(x,t)=\sum_n b_n\sin\frac{n\pi x}{L}\,e^{-\alpha (n\pi/L)^2 t}.$$
The coefficients bₙ come from the initial condition by **Fourier's trick** [Gr p.136]
— i.e. `~MA-09`. Code: `heat_mode`, `wave_mode` are single such modes; the wave
version replaces the decay e^{−…t} with the oscillation cos(cnπt/L).

## 3. Solving numerically (this module's code)
Discretize space (and time) and replace derivatives by finite differences (the
1-D Laplacian uᵢ₊₁−2uᵢ+uᵢ₋₁ over dx²):
- **heat** — explicit FTCS, stable for r = α dt/dx² ≤ ½ (`heat_1d`);
- **wave** — leapfrog in time, stable for the Courant number c dt/dx ≤ 1 (`wave_1d`);
- **Laplace** — no time: relax each interior point to the average of its four
  neighbours until it stops changing (Gauss–Seidel, `laplace_2d`). The discrete
  5-point Laplacian is *exact* for quadratics, so a harmonic polynomial like
  x²−y² is reproduced to machine precision (a test).

## Where this goes
Separation of variables in spherical coordinates (`~MA-03`) produces Legendre
polynomials and spherical harmonics (`~MA-12`), the workhorses of `~EM-04`
(boundary-value problems) and `~QM-12` (the hydrogen atom).
