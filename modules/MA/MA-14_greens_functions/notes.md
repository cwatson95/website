# MA-14 — Green's Functions (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. Boas introduces Green functions for ODEs in **Chapter 8
§12** and uses them for PDEs in **Chapter 13**.

## 1. The idea: invert the operator with a point source
To solve L u = f with homogeneous boundary conditions, first solve for the
response to a **unit point source** [B §12 *A Brief Introduction to Green
Functions* p.461]:
$$L_x\,G(x,\xi)=\delta(x-\xi).$$
Because L is linear and f(x)=∫f(ξ)δ(x−ξ)dξ is a superposition of point sources,
$$\boxed{\,u(x)=\int G(x,\xi)\,f(\xi)\,d\xi\,}$$
solves L u=f. G is the **integral-operator inverse** of the differential operator
L. (The δ source is `~MA-15`.) Code: `solve_bvp_greens` does the integral.

## 2. Construction for a boundary-value problem
For −u″=f on [0,1] with u(0)=u(1)=0, build G from two homogeneous solutions, one
satisfying each boundary condition: y₁=x (y₁(0)=0), y₂=1−x (y₂(1)=0). Splice them
at x=ξ, continuous, with the **derivative jump** [G_x]=−1 set by the δ (integrate
−G″=δ across ξ):
$$G(x,\xi)=x_<\,(1-x_>),\qquad x_<=\min(x,\xi),\ x_>=\max(x,\xi).$$
Two properties the tests check: **symmetry** G(x,ξ)=G(ξ,x) (the operator is
self-adjoint, `~MA-11`) and the unit slope-jump at x=ξ. For −u″+k²u the same
recipe with y₁=sinh kx, y₂=sinh k(1−x) gives G=sinh(kx_<)sinh(k(1−x_>))/(k sinh k).
Code: `green_dirichlet`, `green_helmholtz`; both validated against
`solve_bvp_direct` (a finite-difference solve).

## 3. The eigenfunction (spectral) expansion
Expand G in the eigenfunctions of L (the `~MA-11` Sturm–Liouville basis). With
Lφ_n=λ_n w φ_n,
$$G(x,\xi)=\sum_n \frac{\varphi_n(x)\,\varphi_n(\xi)}{\lambda_n},$$
i.e. **G is L⁻¹ written in the eigenbasis** — each mode is divided by its
eigenvalue. For −u″ on [0,1]: φ_n=√2 sin(nπx), λ_n=(nπ)², so
G=Σ 2 sin(nπx)sin(nπξ)/(nπ)². The code shows this series converging to the
closed-form tent of §2. (A vanishing λ_n — a zero mode — is exactly when the
Green's function fails to exist: the Fredholm alternative.) Code: `green_series`.

## 4. The causal Green's function (the propagator)
For an **initial-value** problem the boundary data are replaced by causality. For
y″+ω²y=δ(t−τ), y(0)=y′(0)=0:
$$G(t,\tau)=\frac{\sin\omega(t-\tau)}{\omega}\,H(t-\tau),$$
zero before the kick (Heaviside H) — the **retarded propagator**. The forced
solution is the convolution y(t)=∫₀ᵗ G(t,τ)f(τ)dτ (cf. the convolution theorem,
`~MA-10`); G here is the inverse Laplace transform of 1/(s²+ω²). Code:
`causal_green_oscillator`, `solve_oscillator_greens`, checked against
`rk4_oscillator` and the closed form y=(1−cos ωt)/ω² for a unit step.

## Where this goes
- `~EM-17`: the retarded potential is the Green's function of the wave operator,
  G=δ(t−|r−r′|/c)/(4π|r−r′|) — §4 in 3+1 dimensions; Liénard–Wiechert is its
  moving-source value.
- `~QM-19`: the quantum **propagator** ⟨x|e^{−iHt/ħ}|x′⟩ is the Green's function
  of the Schrödinger operator; its path-integral form sums §4 over all paths.
- `~MA-11`: §3 is the spectral inverse — completeness (Σφ_nφ_n=δ) divided by the
  spectrum. Green's functions and eigenfunction expansions are the same statement.
