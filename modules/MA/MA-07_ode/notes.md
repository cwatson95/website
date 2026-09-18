# MA-07 — Ordinary Differential Equations (notes)

Citation keys (details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are the *printed* book pages. (Butkov is image-only and
cited at chapter level in `refs.md`, without page numbers.)

## 1. First-order equations (analytic)
- **Separable** dy/dx = g(x)h(y): integrate dy/h = g dx [B §8.2 p.395].
- **Linear** y′ + P(x)y = Q(x): multiply by the integrating factor e^{∫P} [B §8.3
  p.401]. These solve growth/decay, RC circuits, and the like.

## 2. Second-order constant-coefficient (the oscillator)
ay″ + by′ + cy = 0 is solved by y = e^{λx} with the **characteristic equation**
aλ² + bλ + c = 0 [B §8.5 p.408]. The three regimes — real roots
(over-damped), repeated (critical), complex (under-damped, oscillatory) — are the
damped harmonic oscillator. The forced/inhomogeneous case adds a particular
solution (resonance when the drive hits the natural frequency) [B §8.6 p.417].
This is `~CM-15`.

## 3. Series solutions
When coefficients vary, expand in a (generalized) power series — the **Frobenius
method** [B §12.11 p.585] — which is how Legendre, Bessel and Hermite functions
(`~MA-12`) arise from their ODEs.

## 4. Numerical integration (this module's code)
Reduce any ODE to first order, dy/dt = f(t, y) with y a vector (a second-order
equation becomes [y, y′], via `second_order_system`). Then step:
- **Euler:** yₙ₊₁ = yₙ + Δt f — first order, large error.
- **RK4:** the classical 4-stage rule — fourth order, the workhorse.
`integrate` returns the whole trajectory; the test shows RK4 hitting e and cos t
to ~1e-5 where Euler is far off.

## 5. Linear systems by diagonalization (reusing MA-04)
For dx/dt = A x with **symmetric** A, diagonalize A = QΛQᵀ (`~MA-04`
`eig_symmetric`) and evolve each eigen-mode independently:
$$\mathbf x(t)=e^{At}\mathbf x_0=\sum_i (\mathbf v_i\!\cdot\!\mathbf x_0)\,e^{\lambda_i t}\,\mathbf v_i.$$
Code: `linear_evolve_symmetric`; the test checks it equals RK4 of dx/dt=Ax and,
for A=[[0,1],[1,0]], the closed form (cosh t, sinh t). This eigen-mode picture is
exactly the **normal modes** of `~CM-16` and the stationary states of `~QM-03`.
