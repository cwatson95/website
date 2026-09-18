# MA-20 — Numerical Methods (notes)

Citation key (full details + PDF pages in `refs.md`): **S** = Schaum's
*Mathematical Handbook of Formulas and Tables*; **C** = Chicone, *ODE with
Applications*. Pages are the *printed* book pages.

## 0. The organizing idea: order of accuracy
A method has **order p** if its error scales like hᵖ as the step h → 0. The
cleanest diagnostic is **step halving**: error(h)/error(h/2) ≈ 2ᵖ, so
p ≈ log₂(error(h)/error(h/2)). Every routine below is labelled by its order and
the code *measures* it (`quad_order`, `ode_order`). A wrong implementation shows
the wrong order — the most useful single test in numerics.

## 1. Quadrature
Approximate ∫ₐᵇ f by sampling:
- **Trapezoid** (order 2): straight lines between samples.
- **Simpson** (order 4): parabolas through triples of samples [S *Simpson's rule*
  p.109, §ref p.231]. Exact for cubics.
- **Gauss–Legendre** (order 2n for n nodes): place n nodes at the Legendre roots
  (`~MA-12`) with optimal weights — **exact for polynomials up to degree 2n−1**.
Code: `trapezoid`, `simpson`, `gauss_legendre`; the test confirms Gauss-2 is exact
through cubics, Gauss-3 through quintics, and that the measured orders are 2 and 4.

## 2. Root finding
Solve f(x)=0:
- **Bisection** (order 1, linear): halve a sign-changing bracket — slow but sure.
- **Newton** (order 2, quadratic): x ← x − f/f′ [S *Newton's method* p.233]. Near a
  simple root the error **squares** each step (≈ 13 correct digits in ~5 iterations).
- **Secant** (order ≈1.618): Newton with a finite-difference slope (no f′ needed).
Code: `bisection`, `newton` (returns the iterate history so the test can verify
e_{k+1} ≲ e_k²), `secant`.

## 3. ODE integrators
Advance y′ = f(t,y):
- **Euler** (order 1): y ← y + h f(t,y) — the definition of the derivative.
- **RK4** (order 4): four slope evaluations per step in the classic 1-2-2-1
  combination [S *Runge–Kutta* p.236]; the workhorse of `~MA-10`/`~MA-14` and the
  KrF kinetics solver. Existence/uniqueness of the solution being integrated is
  the theorem in [C §1.1 p.3].
Code: `euler`, `rk4`; the test measures orders 1 and 4 on y′=y (exact eᵗ).

## 4. Eigenvalues by power iteration
Repeatedly applying A to a vector amplifies the component along the eigenvector of
**largest |λ|**; normalizing each step converges to that dominant eigenpair, with
λ read off by the Rayleigh quotient. Code: `power_iteration` (validated on the
tridiagonal matrix of `~MA-04`/`~MA-11`, λ_max = 2+√2). Inverse/shifted variants
reach the other eigenvalues — the practical complement to the from-scratch Jacobi
(`~MA-04`) and Sturm-sequence (`~MA-11`) solvers.

## 5. Interpolation
The unique degree-(n−1) polynomial through n points is the **Lagrange**
interpolant, P(x)=Σ yᵢ ∏_{j≠i}(x−xⱼ)/(xᵢ−xⱼ) [S forward-difference & interpolation
p.227]. Code: `lagrange_interp` — exact recovery of any polynomial of degree < n
and exact at the nodes. (High-degree equal-spacing interpolation suffers Runge
oscillation; splines/Chebyshev nodes are the cure, beyond this module.)

## Where this goes
- `~PK-01`: the KrF/Boltzmann kinetics integrate stiff ODE systems — the RK4 here
  is the explicit baseline; stiffness pushes toward implicit/BDF methods.
- `~MA-10`…`~MA-14`: every "vs RK4" / "by Simpson" cross-check in those modules is
  this toolkit; measuring the order is how we trust them.
- `~MA-04`/`~MA-11`: power iteration, Jacobi, and the Sturm sequence are three
  routes to eigenvalues, each best in a different regime.
