# MA-13 — Calculus of Variations (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. All in **Chapter 9, Calculus of Variations**.

## 1. The problem: extremize a functional
A **functional** assigns a number to a whole function:
$$J[y]=\int_{x_1}^{x_2}L\big(x,\,y(x),\,y'(x)\big)\,dx.$$
We seek the path y(x) (with y fixed at the endpoints) that makes J stationary
[B §1 *Introduction* p.472]. "What is the shortest distance between two points?"
is the simplest instance, with L=√(1+y′²). Code: `functional` evaluates J on a
sampled path by the midpoint rule.

## 2. The Euler–Lagrange equation
Stationarity under y→y+εη (η vanishing at the ends) gives, after integrating the
δy′ term by parts, the **Euler–Lagrange equation** [B §2 *The Euler Equation* p.474]:
$$\boxed{\ \frac{\partial L}{\partial y}-\frac{d}{dx}\!\left(\frac{\partial L}{\partial y'}\right)=0\ }$$
— a 2nd-order ODE for the extremal. For arclength L=√(1+y′²): ∂L/∂y=0 and
∂L/∂y′=y′/√(1+y′²) must be constant ⇒ y′ constant ⇒ a **straight line** [B §3
*Using the Euler Equation* p.478]. Code: `euler_lagrange_residual` returns the
left side along any path (~0 on an extremal); `minimize_path` drives a bent path
to the extremal by coordinate-Newton sweeps and the residual collapses to ~0.

## 3. The Beltrami first integral (when L has no explicit x)
If ∂L/∂x=0, the Euler–Lagrange equation has a **first integral** [B §3–4, the
"no x" shortcut, p.478–482]:
$$L-y'\frac{\partial L}{\partial y'}=\text{const}.$$
This is the variational ancestor of energy conservation and of the Hamiltonian
(`~CM-19`): the quantity conjugate-to-motion is conserved when the "time" variable
is absent. Code: `beltrami`. Two exact checks:
- **Brachistochrone** L=√((1+y′²)/y): on the cycloid x=a(t−sin t), y=a(1−cos t)
  the constant is 1/√(2a). (Verified to ~1e-5 using the exact slope
  y′=sin t/(1−cos t).)
- **Catenary** L=y√(1+y′²): on y=c cosh(x/c) the constant is c.

## 4. The classic problems
- **Geodesic** (shortest path): straight line — §3, recovered by `minimize_path`.
- **Brachistochrone** (fastest descent under gravity): minimize the time
  T=∫√((1+y′²)/(2g y))dx; the Beltrami integral integrates to a **cycloid** [B §4
  *The Brachistochrone Problem; Cycloids* p.482]. Code: `cycloid_brachistochrone`.
- **Minimal surface of revolution**: minimize ∫y√(1+y′²)dx; the solution is the
  **catenary** y=c cosh(x/c). Code: `catenary`.

## 5. Several variables and constraints
With several dependent variables y_i(x) there is one Euler–Lagrange equation per
y_i — and identifying L with the mechanical Lagrangian T−V gives **Lagrange's
equations of motion** [B §5 *Several Dependent Variables; Lagrange's Equations*
p.485]: this is exactly `~CM-17`. Constrained extrema (fixed length, fixed area —
the **isoperimetric** problems) are handled by Lagrange multipliers added to L [B
§6 *Isoperimetric Problems* p.491].

## Where this goes
- `~CM-17`: Hamilton's principle δ∫L dt=0 with L=T−V → Lagrange's equations; the
  whole machinery of §2 carries over with x→t.
- `~CM-19`: §3's first integral, with L the mechanical Lagrangian, is the
  conserved energy; the Legendre transform of it is the Hamiltonian.
- `~RE-12`: a geodesic extremizes ∫ds; the Euler–Lagrange equation of the metric
  arclength is the geodesic equation — same §2, curved space. (Bridge B1.)
