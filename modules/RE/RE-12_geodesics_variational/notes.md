# RE-12 — Geodesics & the variational principle (notes)

Conventions: metric `g_{μν}(x)`, `Γ` the Levi-Civita connection (RE-09/RE-11),
affine parameter `λ` (proper time `τ` for timelike, an affine parameter for null),
`ẋ^μ = dx^μ/dλ`. Christoffel from MA-17 as `Γ[k][i][j] = Γ^k_{ij}`. Geometrized
units `G = c = 1`, signature mostly-plus.

## 1. Two definitions of a geodesic — and why they agree
A geodesic is the curved-spacetime version of a straight line, and "straight"
admits two readings:

- **Straightest** — the curve that *parallel-transports its own tangent*. Its
  tangent `u^μ = ẋ^μ` is carried along itself without turning:
  $$u^\nu \nabla_\nu u^\mu = 0 .$$
  This uses only the connection `Γ`; it is an *affine* notion (no metric needed to
  state it, only to build `Γ`).
- **Extremal** — the curve that *extremizes path length / proper time*,
  $$\delta \int ds = 0 .$$
  This uses only the metric `g` (length is `ds = \sqrt{|g_{μν}dx^μ dx^ν|}`).

For a general connection these are *different* curves. They **coincide** precisely
when `Γ` is the **Levi-Civita** connection — the unique metric-compatible
(`∇g = 0`), torsion-free connection (RE-09). That is the connection of GR, so in
gravity the straightest line and the extremal line are the same worldline. The
equivalence is what `euler_lagrange_gives_christoffel` checks numerically: the
extremal route (Euler–Lagrange, MA-13) returns exactly the straightest route
(`−Γẋẋ`, MA-17).

## 2. The geodesic equation in an affine parameter
Writing `u^ν∇_ν u^μ = 0` in coordinates with `u^μ = ẋ^μ` gives
$$\boxed{\;\ddot x^\mu + \Gamma^\mu{}_{\nu\rho}\,\dot x^\nu \dot x^\rho = 0\;}$$
(`geodesic_rhs` returns the RHS `\ddot x^\mu = -\Gamma^\mu{}_{\nu\rho}\dot x^\nu\dot x^\rho`,
which `integrate_geodesic` feeds to RK4). This form holds only for an **affine**
parameter — one for which the tangent has constant norm. A non-affine parameter
`σ(λ)` adds a term `∝ \dot x^\mu` on the right (the geodesic still traces the same
*path*, just re-clocked). Proper time `τ` is affine for timelike geodesics; for a
null geodesic, `ds = 0` so `τ` degenerates and one uses an affine parameter
defined *by* requiring this clean form. Flat space has `Γ = 0`, so geodesics are
straight lines `\dot x = \text{const}` (`test_flat_geodesic_is_a_straight_line`).

Because an affine parameter keeps the tangent norm fixed, `2L = g_{μν}\dot x^μ\dot x^ν`
is **constant along the motion** — the geodesic moves at constant "speed" and so
cannot change causal character: timelike stays timelike, null stays null
(`test_affine_parameter_gives_constant_speed`, `test_null_geodesic_stays_null`).

## 3. The variational derivation — the slick way to get Γ
Take the **affine-parameter action** (the "energy" functional, cleaner than the
square-root length because it is smooth at `\dot x = 0` and fixes an affine `λ`)
$$S = \int L\,d\lambda,\qquad L = \tfrac12\,g_{\mu\nu}(x)\,\dot x^\mu \dot x^\nu$$
(`lagrangian`). Its Euler–Lagrange equations (MA-13),
$$\frac{d}{d\lambda}\frac{\partial L}{\partial \dot x^\mu} - \frac{\partial L}{\partial x^\mu} = 0,$$
expand with `∂L/∂\dot x^μ = g_{μβ}\dot x^β` and `∂L/∂x^μ = \tfrac12 ∂_μ g_{αβ}\dot x^α\dot x^β` to
$$g_{\mu\beta}\ddot x^\beta + \big(\partial_\alpha g_{\mu\beta} - \tfrac12\partial_\mu g_{\alpha\beta}\big)\dot x^\alpha \dot x^\beta = 0
\;\Longrightarrow\; \ddot x^\mu + \Gamma^\mu{}_{\alpha\beta}\dot x^\alpha \dot x^\beta = 0,$$
because symmetrising `∂_α g_{μβ}\dot x^α\dot x^β` over `α↔β` and raising with `g^{μ·}`
**reproduces the Christoffel symbol** `Γ^μ_{αβ} = \tfrac12 g^{μλ}(∂_α g_{λβ} + ∂_β g_{λα} − ∂_λ g_{αβ})`.
So extremizing the action *is* the geodesic equation, and reading off the
coefficients of `\dot x^α\dot x^β` is the fastest hand-computation of `Γ`.
`euler_lagrange_gives_christoffel` does exactly this with MA-13: per coordinate it
forms the reduced Lagrangian, takes `variational.euler_lagrange_residual` along a
constant-velocity trial (whose residual equals `g_{μβ}\ddot x^β`), and contracts
with `g^{-1}` — matching `geodesic_rhs` to ~1e-8 on the sphere and Schwarzschild
(`test_variational_equation_reproduces_christoffel`). This is the relativity
terminus of **bridge B1** (MA-13 → CM-17 → CM-21 → RE-12): one variational idea.

## 4. Timelike geodesics maximise proper time; null geodesics are light
For a **timelike** worldline the action-length `\int ds` is the proper time `τ` —
the time a clock carried along the curve actually reads. The single minus sign in
the metric *reverses* the triangle inequality (RE-05): of all worldlines between
two timelike-separated events, the geodesic has the **longest** proper time. This
is **maximal aging** — free fall is the path of greatest elapsed time, and the
"twin paradox" is just the bent (accelerated) twin taking a shorter worldline
(`action_length`; `test_maximal_aging…` shows `τ` strictly drops as the path is
bent away from the straight line, with the inertial value `τ = T`). It is a
maximum, not a minimum, for the timelike (`ds^2<0`) branch; the same extremal is a
genuine length-minimiser for spacelike paths and a stationary "zero-length" curve
for **null** geodesics `ds = 0`, the worldlines of light (`test_null_geodesic_stays_null`).
Maximal aging is the deepest statement of the equivalence principle: gravity is
not a force; free particles simply extremise their own proper time.

## 5. Symmetries ⇒ conserved quantities (Killing vectors)
If the metric has a **symmetry** — a direction `ξ` along which it does not change,
a **Killing vector** (`\nabla_{(μ}ξ_{ν)} = 0`) — then the projection of the
momentum onto `ξ`,
$$Q = p\cdot\xi = g_{\mu\nu}\,\xi^\mu \dot x^\nu = \xi_\nu \dot x^\nu,$$
is **conserved along every geodesic** (`killing_conserved`). The proof is one
line: `dQ/dλ = \dot x^μ\nabla_μ(ξ_ν\dot x^ν) = (\nabla_μξ_ν)\dot x^μ\dot x^ν + ξ_ν\,\dot x^μ\nabla_μ\dot x^ν`,
where the first term vanishes by Killing's equation (it is symmetric `×` antisymmetric)
and the second by the geodesic equation `\dot x^μ\nabla_μ\dot x^ν = 0`. This is
Noether's theorem in geometric dress. Two cases run through all of GR:

- the round sphere is axisymmetric, `ξ = ∂_φ`, giving conserved **angular
  momentum** `L = g_{φφ}\dot φ = a^2\sin^2θ\,\dot φ` — constant even on a *tilted*
  great circle whose `θ` swings widely (`test_killing_angular_momentum…`);
- Schwarzschild is static + axisymmetric, `ξ = ∂_t` and `ξ = ∂_φ`, giving
  conserved **energy** `E = -(1-2M/r)\dot t` and **angular momentum**
  `L = r^2\sin^2θ\,\dot φ` along an orbit (`test_killing_energy_and_momentum…`).

These two constants reduce the Schwarzschild geodesics to a 1-D problem in `r`
with an effective potential — exactly the machinery RE-14 uses for orbits,
perihelion precession, and light bending.

## 6. Where this goes
The geodesic equation + the two Killing constants `(E, L)` are the entire input to
**RE-14** (Schwarzschild orbits, the classic tests of GR). The variational view
also has a Hamiltonian face: the conjugate momentum `p_μ = ∂L/∂\dot x^μ = g_{μν}\dot x^ν`
and Hamiltonian `H = \tfrac12 g^{μν}p_μ p_ν` turn geodesics into a Hamiltonian
flow, whose Hamilton–Jacobi / eikonal equation `g^{μν}∂_μ S\,∂_ν S = -m^2` is the
short-wavelength limit of wave propagation (**~CM-21**, *not yet built* — a forward
reference). For null geodesics the same eikonal equation is geometric optics in
curved spacetime: light rays are null geodesics, the bridge from this module to
gravitational lensing.
