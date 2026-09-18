# RE-13 — Einstein Field Equations (notes)

Conventions: metric `g_{μν}(x)`, mostly-plus signature `(−+++)`, geometrized units
`G = c = 1`. The Einstein tensor `G_{μν}=R_{μν}−½Rg_{μν}` and Ricci `R_{μν}`, `R`
are RE-11's (computed there by finite differences). 4-velocities are unit timelike,
`u·u = g_{μν}u^μu^ν = −1`. Field equation `G_{μν}=8πT_{μν}`.

## 1. The two halves of general relativity
RE-12 gave the first half — **spacetime tells matter how to move**: a free particle
follows a geodesic, `D u^μ/dτ = 0`, the curved-spacetime `F = 0`. This module gives
the second — **matter tells spacetime how to curve**. The metric `g_{μν}` is itself
the dynamical gravitational field (RE-10/§V.3 in Zee: there is no field *on*
spacetime, the geometry *is* the field), and we need the equation that determines it
from its sources, the gravitational analogue of `∇²Φ=4πρ` (Newton) or
`∂_μF^{μν}=J^ν` (Maxwell). That equation is Einstein's.

## 2. Why the left side is the Einstein tensor
We want `(\text{curvature})_{μν} = κ\,T_{μν}` with `T_{μν}` the source. The source is
constrained: in special relativity energy–momentum is locally conserved,
`∂_μT^{μν}=0`, which in curved spacetime becomes
$$\nabla_\mu T^{\mu\nu} = 0 .$$
So the curvature tensor on the left **must be divergence-free too**. Among the
tensors built from `g` and its first two derivatives, that requirement is met
*identically* by exactly one combination — the Einstein tensor — through the
**contracted Bianchi identity** (RE-11 §3)
$$\boxed{\ \nabla_\mu G^{\mu\nu} = \nabla_\mu\!\left(R^{\mu\nu}-\tfrac12 R\,g^{\mu\nu}\right)=0\ }.$$
Neither `R_{μν}` nor `R\,g_{μν}` is separately conserved; only their `G` combination
is. Hence the field equation must read
$$G_{\mu\nu} = 8\pi\,T_{\mu\nu},$$
*not* `R_{μν}∝T_{μν}`: choosing `G` makes `∇_μT^{μν}=0` an automatic consequence of
the geometry, for free (`field_equation_residual`; `test_schwarzschild_is_a_vacuum_solution`).

## 3. The field equation, its trace-reversed form, and Λ
**The equation.** `G_{μν}=8πT_{μν}`: ten coupled, nonlinear, second-order PDEs for
the metric. Taking the trace with `g^{μν}` (in 4-D, `g^{μν}G_{μν}=(1−n/2)R=−R`)
gives `−R=8πT`, i.e. `R=−8πT` with `T=g^{μν}T_{μν}`. Substituting back yields the
algebraically equivalent **trace-reversed form**
$$\boxed{\ R_{\mu\nu} = 8\pi\!\left(T_{\mu\nu}-\tfrac12 T\,g_{\mu\nu}\right)\ }$$
(`trace_reversed_ricci`). Its left side is plain Ricci, which is why it is the form
you integrate and why **vacuum** (`T=0`) immediately gives `R_{μν}=0`. The
round-trip `R=8π(T−½Tg) ⇔ G=8πT` is exact algebra
(`test_trace_reversed_equivalent_to_einstein`).

**The cosmological constant.** The Bianchi identity also permits a term `Λg_{μν}`
(since `∇_μg^{μν}=0`):
$$G_{\mu\nu} + \Lambda\,g_{\mu\nu} = 8\pi\,T_{\mu\nu}.$$
`Λ` acts like a vacuum energy with `T^{(\Lambda)}_{μν}=−(\Lambda/8\pi)g_{μν}`
(pressure `p=−ρ`). On flat space with `T=0` the residual is exactly `Λη_{μν}`
(`test_cosmological_constant_on_flat_space`); curved to match, it is the de Sitter
universe (§6).

## 4. The stress-energy tensor
`T_{μν}` is the source: the flux of `μ`-momentum across a surface of constant `x^ν`.
It is symmetric (`T_{μν}=T_{νμ}`) and its components are `T_{00}=` energy density,
`T_{0i}=` momentum density, `T_{ij}=` stress (pressure + shear). The workhorse is the
**perfect fluid** — isotropic in its rest frame, no shear or heat flux:
$$\boxed{\ T_{\mu\nu} = (\rho+p)\,u_\mu u_\nu + p\,g_{\mu\nu}\ }$$
(`stress_energy_perfect_fluid`), with `ρ` the rest-frame energy density, `p` the
pressure, `u` the 4-velocity. Its trace is frame- and metric-independent,
$$g^{\mu\nu}T_{\mu\nu} = (\rho+p)(u\cdot u) + p\,n = -\rho + 3p\quad(n=4)$$
(`trace`; `test_perfect_fluid_trace_is_minus_rho_plus_3p`). Special cases:
- **dust** `p=0`, `T_{μν}=ρu_μu_ν` (cold matter; trace `−ρ`) — `stress_energy_dust`;
- **radiation** `p=ρ/3`, **traceless** `T=0` (a conformal source) — `test_dust_and_radiation_traces`;
- **vacuum energy** `p=−ρ` (`= Λ`).

For an observer at rest, `T_{00}=−\rho\,g_{00}` (`= ρ` in Minkowski): the time-time
component *is* the energy density (`test_rest_frame_gives_energy_density`). The
canonical **field** source — the electromagnetic stress tensor
`T_{μν}=F_{μα}F_ν{}^α−¼g_{μν}F_{αβ}F^{αβ}` — belongs to **~EM-14** (forward
reference; not built here). This same `T_{μν}`, fed into `G_{μν}=8πT_{μν}` for a
homogeneous isotropic fluid, becomes the **Friedmann equations** of RE-15.

## 5. The Newtonian limit — fixing the `8π`
Three approximations: the field is **weak** (`g_{μν}=η_{μν}+h_{μν}`, `|h|≪1`),
**static** (`∂_0h=0`), and sources move **slowly**. The geodesic equation then
reduces to `\ddot x^i = -\Gamma^i_{00} = -\tfrac12\partial_i h_{00}`; matching
Newton's `\ddot x^i = -\partial_i\Phi` fixes
$$g_{00} = -(1+2\Phi)\qquad(h_{00}=-2\Phi),$$
the metric potential (Zee §V.4; cpope §5.5). For the field-equation side, the
linearized time-time Einstein tensor of the **isotropic** weak-field metric
`g_{00}=-(1+2\Phi)`, `g_{ij}=(1-2\Phi)\delta_{ij}` is
$$G_{00} \simeq 2\,\nabla^2\Phi$$
(the spatial perturbation is essential — `g_{00}` alone gives only `R_{00}=\nabla^2\Phi`).
Then the `00` field equation `G_{00}=8\pi T_{00}=8\pi\rho` becomes
$$2\nabla^2\Phi = 8\pi\rho \iff \nabla^2\Phi = 4\pi\rho,$$
**Poisson's equation** — provided the constant is `8π`. Any other constant would
violate the Newtonian limit; this is how `κ=8πG/c^4 → 8π` is pinned (Zee §VI.5).
`newtonian_poisson_residual` builds `g=η+h` for a smooth `Φ` (a Gaussian lump),
forms `G_{00}` numerically, and checks `G_{00}-2\nabla^2\Phi\approx0`
(`test_newtonian_limit_fixes_8pi`, loose finite-difference tolerance).

## 6. Vacuum and the Λ-vacuum: Schwarzschild and de Sitter
**Vacuum** (`T_{μν}=0`, `Λ=0`): `R_{μν}=0` (equivalently `G_{μν}=0`). This is *not*
flat space — `R_{μνρσ}` can be large (the Weyl part survives, RE-11 §5). The unique
spherically-symmetric vacuum is **Schwarzschild** (RE-11/RE-14):
`field_equation_residual(schwarzschild_metric(M), 0, x) ≈ 0`. **Λ-vacuum**
(`T_{μν}=0`, `Λ≠0`): `G_{μν}+\Lambda g_{μν}=0`, i.e. `R_{μν}=\Lambda g_{μν}` —
maximally symmetric. With `Λ>0` this is **de Sitter** space, `R_{μν}=(3/L^2)g_{μν}`,
`Λ=3/L^2`, a cosmic horizon at `r=L` (`de_sitter_metric`;
`test_de_sitter_is_a_lambda_vacuum`, and the wrong `Λ` is *not* a solution — the
equation has real content). de Sitter is the late-time attractor of our
accelerating universe and the playground of RE-15's dark energy.
