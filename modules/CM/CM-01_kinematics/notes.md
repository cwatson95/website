# CM-01 — Kinematics (notes)

Kinematics = the geometry of motion, *before* forces. The state of a point
particle is its **position vector as a function of time**, **r**(t); everything
else is built from it by differentiation and the MA-01 vector products.

Citation keys (full details + PDF pages in `refs.md`):
**F** = Fowles & Cassiday 7e · **MT** = Marion & Thornton 5e · **G** = Goldstein,
Poole & Safko 3e. Page numbers are the *printed* book pages.

## 1. Position, velocity, acceleration
$$\mathbf v(t)=\frac{d\mathbf r}{dt},\qquad
  \mathbf a(t)=\frac{d\mathbf v}{dt}=\frac{d^2\mathbf r}{dt^2}.$$
Defined component-wise in a fixed Cartesian frame [F §1.10, p.31; MT §1.14
Eqs.1.87–1.88, p.30; G §1.1 Eq.1.1, p.1]. In code these are `velocity(r)` and
`acceleration(r)`, formed by central finite differences of the trajectory
function — so the inputs and outputs are *functions of t*, matching MA-01.

## 2. Speed, arc length, the unit tangent
Speed is the magnitude `speed(r) = |v|` (MA-01 `norm` applied to the velocity
function). The unit tangent is
$$\hat{\mathbf T}=\frac{\mathbf v}{|\mathbf v|},\qquad
  s(t)=\int_{t_0}^{t}|\mathbf v|\,dt' \ \text{(arc length)}.$$

## 3. Tangential & normal components of acceleration
Resolve **a** along the path (**T̂**) and toward the centre of curvature (**N̂**):
$$\mathbf a=\underbrace{\frac{d|\mathbf v|}{dt}}_{a_T}\hat{\mathbf T}
          +\underbrace{\frac{|\mathbf v|^2}{\rho}}_{a_N}\hat{\mathbf N},
  \qquad
  a_T=\frac{\mathbf a\cdot\mathbf v}{|\mathbf v|},\quad
  a_N=\frac{|\mathbf v\times\mathbf a|}{|\mathbf v|}.$$
The curvature and radius of curvature are
$$\kappa=\frac{|\mathbf v\times\mathbf a|}{|\mathbf v|^{3}},\qquad \rho=\frac1\kappa .$$
Fowles develops these through problems rather than a section: the relation
**v**×**a** = (v³/ρ)**B̂** and a_T, a_N are Probs. 1.25–1.27 [F p.46]. Code:
`tangential_acceleration`, `normal_acceleration`, `curvature`,
`radius_of_curvature` — each a dot/cross from MA-01 wrapped as a function of t.

*Checks:* a straight line has κ=0; a circle of radius R has κ=1/R and a_N=v²/R.

## 4. Motion in a uniform field — projectiles
Constant acceleration integrates immediately:
$$\mathbf r(t)=\mathbf r_0+\mathbf v_0\,t+\tfrac12\mathbf a\,t^2 .$$
For a launch speed v₀ at angle θ over level ground (gravity −g **ẑ**)
[F §4.3, p.156; MT §2.4 & Ex.2.6, p.63]:
$$t_\text{flight}=\frac{2v_0\sin\theta}{g},\quad
  R=\frac{v_0^2\sin2\theta}{g},\quad
  h_\text{max}=\frac{(v_0\sin\theta)^2}{2g}.$$
Code: `uniform_acceleration`, `projectile`, `time_of_flight`, `range_`,
`max_height`. (Air resistance — the **v**- and **v²**-laws — is MT Ex.2.5–2.7,
pp.62–65; left for a later extension.)

## 5. Plane-polar coordinates
With **r** = r **ê_r** and a rotating basis (dê_r/dt = θ̇ ê_θ, dê_θ/dt = −θ̇ ê_r):
$$\mathbf v=\dot r\,\hat{\mathbf e}_r+r\dot\theta\,\hat{\mathbf e}_\theta,\qquad
  \mathbf a=\underbrace{(\ddot r-r\dot\theta^2)}_{a_r}\hat{\mathbf e}_r
           +\underbrace{(r\ddot\theta+2\dot r\dot\theta)}_{a_\theta}\hat{\mathbf e}_\theta .$$
The two "extra" terms are the heart of rotational kinematics:
- **−r θ̇²** in a_r is the **centripetal** acceleration (→ `~CM-10`);
- **2 ṙ θ̇** in a_θ is the **Coriolis** term (named as such later, in rotating
  frames, `~CM-12` / F §5.2).

[F §1.11, p.36; MT §1.14 Eqs.1.97–1.98, p.32; G §1.6 gives the same physics via
the kinetic energy T = ½m(ṙ² + r²θ̇²), Eq.1.75, p.26.] Code:
`polar_position(rho, theta)` builds **r**(t); `polar_acceleration_components`
returns (a_r, a_θ). *Check:* uniform circular motion (ρ=R, θ=ωt) gives
a_r = −Rω², a_θ = 0; a growing-radius spiral switches on the Coriolis term.

## 6. Bridge to dynamics (CM-09)
Multiply velocity by mass and the MA-01 cross product turns kinematics into the
conserved quantities of mechanics:
$$\mathbf p=m\mathbf v,\qquad
  \mathbf L=\mathbf r\times\mathbf p,\qquad
  \mathbf N=\mathbf r\times\mathbf F=\frac{d\mathbf L}{dt}.$$
[G §1.1, Eqs.1.7–1.11, pp.2–3.] In code, `cross(r, velocity(r))` is already the
specific angular momentum **r**×**v** as a function of t — the same object
`~CM-09` will conserve for central forces (`~CM-11`).
