# MA-22 — Topology & Dynamical Systems (notes)

Citation key (full details + PDF pages in `refs.md`): **C** = Chicone, *ODE with
Applications*; **H** = Hatcher, *Algebraic Topology*. Pages are the *printed* book
pages. This is an **[adv]** module.

## 1. Equilibria and linear stability
A **rest point** (equilibrium) x₀ of ẋ=f(x) has f(x₀)=0. Its stability is read from
the **Jacobian** J=Df(x₀): near x₀ the dynamics are ẋ≈J(x−x₀), so the **eigenvalues
of J** decide everything [C §1.6 *Stability and Linearization*, pp.20–23; rest-point
definition p.10]. In the plane (J a 2×2):
- eigenvalues real, **opposite sign** → **saddle** (det J < 0);
- real, **same sign** → **node** (stable if both < 0);
- **complex** pair α±iβ → **spiral** (stable if α<0), or a **center** if α=0.
Code: `eigenvalues_2x2`, `classify_equilibrium`. *(Chicone classifies by the
**real parts of the eigenvalues**, pp.20–23; there is no "trace–determinant plane"
diagram in the book, though tr/det are a convenient shortcut to the same eigenvalues.)*

## 2. Beyond linear: limit cycles and Poincaré–Bendixson
Nonlinear planar flows can have an isolated closed orbit — a **limit cycle** [C
p.95] — that nearby trajectories spiral onto (self-sustained oscillation: heartbeat,
laser, the van der Pol oscillator). The **Poincaré–Bendixson theorem** [C *Limit
Sets and Poincaré–Bendixson Theory* p.91, thm p.94] says a bounded planar orbit that
avoids equilibria must approach a limit cycle — which is *why* there is **no chaos
in 2-D continuous flows**. Chaos needs three continuous dimensions (Lorenz, [C Ch.6
p.449]) — or just one dimension if **time is discrete**, as below.

## 3. The logistic map and the route to chaos
The one-line map xₙ₊₁ = r xₙ(1−xₙ) is the canonical chaos generator [C Ch.8
*Bifurcation* p.545; first example pp.13–14]. As r increases:
- r < 3: a single **stable fixed point** x*=1−1/r;
- r ≈ 3 → 3.45 → 3.54…: **period-doubling** 2 → 4 → 8 → … (a **bifurcation**
  cascade, accumulating at the Feigenbaum point r∞≈3.5699);
- r > r∞: **chaos**, shot through with periodic **windows** (e.g. period-3 near
  r≈3.835).
Code: `period_of_orbit` detects the cycle length; the test sees periods 1, 2, 4, 8.

## 4. The Lyapunov exponent
The signature of chaos is **sensitive dependence on initial conditions**: nearby
orbits separate exponentially, δxₙ ~ δx₀ eλⁿ, with the **Lyapunov exponent**
$$\lambda=\lim_{n\to\infty}\frac1n\sum_{k=0}^{n-1}\ln\bigl|f'(x_k)\bigr|.$$
λ < 0 means orbits converge (a stable cycle); **λ > 0 means chaos**. For the
logistic map f′(x)=r(1−2x); at r=4 the map is conjugate to the tent map and
λ = **ln 2** exactly. Code: `lyapunov_logistic`; the test confirms λ<0 on the
stable cycles (r=2.5, 3.2, 3.5), λ>0 at r=4, and λ(4)≈ln 2.

## 5. Topology: the Euler characteristic
Topology studies what survives continuous deformation. The cleanest invariant is the
**Euler characteristic** [H p.6; §*Euler characteristic* p.146]:
$$\chi=V-E+F.$$
For **any** convex polyhedron χ=2 — the code checks all five Platonic solids — because
each is a triangulated **sphere**; χ does not depend on the mesh, only on the
underlying surface. A **torus** gives χ=0, and in general χ=2−2g for a surface of
**genus** g (number of handles). This number also equals an alternating sum of Betti
numbers — the bridge to **homology** [H *The Idea of Homology* p.98] and, via d²=0
(`~MA-17`), to **de Rham cohomology**. The deeper invariant, the **fundamental
group** π₁ (loops up to deformation) [H p.26], distinguishes spaces χ cannot.

## Where this goes
- `~CM-24`: phase portraits, bifurcations, strange attractors, and the Lyapunov
  exponent are the working tools of nonlinear mechanics — this module is its math.
- `~CM-15`: a damped oscillator is a stable spiral (§1); driving and nonlinearity
  push it toward §3's cascade.
- `~MA-17`: χ and de Rham cohomology connect the *local* d²=0 to *global* topology
  (Gauss–Bonnet ties χ to the integrated curvature K of `~MA-17`).
