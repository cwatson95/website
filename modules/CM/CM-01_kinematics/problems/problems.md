# CM-01 — Problems

Work by hand, then check with `code/kinematics.py`. Citations verified against
the PDFs (editions & PDF pages in `../refs.md`).

### P1.  Projectile range and maximum height  *(Marion & Thornton 5e, Ex. 2.6, p.63)*
A projectile is launched at speed v₀ and angle θ over level ground. Derive
t_flight = 2v₀sinθ/g, R = v₀²sin2θ/g, and h_max = (v₀sinθ)²/2g, and show the
range is maximal at θ = 45°.
*Check:* `range_(v0, θ)`, `max_height(v0, θ)`, `time_of_flight(v0, θ)`; confirm
`acceleration(projectile(v0, θ))(t) ≈ (0,0,−9.81)` at several t.

**Solution.** Gravity gives the constant acceleration $\mathbf a=-g\,\hat{\mathbf z}$, so with launch velocity $\mathbf v_0=(v_0\cos\theta,\,0,\,v_0\sin\theta)$ the height is $z(t)=v_0\sin\theta\,t-\tfrac12 g t^2$. Setting $z=0$ gives the flight time $t_\text{flight}=2v_0\sin\theta/g$. The horizontal range is
$$R=v_0\cos\theta\,t_\text{flight}=\frac{2v_0^2\sin\theta\cos\theta}{g}=\frac{v_0^2\sin2\theta}{g}.$$
At the apex ($t=t_\text{flight}/2$, $v_z=0$) the height is $h_\text{max}=(v_0\sin\theta)^2/2g$. Since $R\propto\sin2\theta$ is largest when $2\theta=90^\circ$, the range peaks at $\theta=45^\circ$. For $v_0=20,\ \theta=40^\circ$ this gives $R\approx40.155$ m, $h_\text{max}\approx8.424$ m, $t_\text{flight}\approx2.621$ s, matching `range_`, `max_height`, `time_of_flight`.

### P2.  Velocity & acceleration in plane polar coordinates  *(Fowles 7e §1.11, p.36; M&T Eqs. 1.97–1.98, p.32)*
Starting from **r** = r ê_r and dê_r/dt = θ̇ ê_θ, dê_θ/dt = −θ̇ ê_r, derive
**v** = ṙ ê_r + r θ̇ ê_θ and **a** = (r̈ − r θ̇²)ê_r + (r θ̈ + 2ṙ θ̇)ê_θ.
Identify the centripetal and Coriolis terms.
*Check:* `polar_acceleration_components(rho, theta)` for ρ(t)=R, θ(t)=ωt gives
(−Rω², 0); for ρ(t)=1+t, θ(t)=t the Coriolis term gives a_θ = 2.

**Solution.** Differentiate $\mathbf r=r\,\hat{\mathbf e}_r$ using $\dot{\hat{\mathbf e}}_r=\dot\theta\,\hat{\mathbf e}_\theta$:
$$\mathbf v=\dot r\,\hat{\mathbf e}_r+r\dot{\hat{\mathbf e}}_r=\dot r\,\hat{\mathbf e}_r+r\dot\theta\,\hat{\mathbf e}_\theta.$$
Differentiate again, now also using $\dot{\hat{\mathbf e}}_\theta=-\dot\theta\,\hat{\mathbf e}_r$:
$$\mathbf a=\ddot r\,\hat{\mathbf e}_r+\dot r\dot\theta\,\hat{\mathbf e}_\theta+(\dot r\dot\theta+r\ddot\theta)\,\hat{\mathbf e}_\theta+r\dot\theta(-\dot\theta\,\hat{\mathbf e}_r)=(\ddot r-r\dot\theta^2)\,\hat{\mathbf e}_r+(r\ddot\theta+2\dot r\dot\theta)\,\hat{\mathbf e}_\theta.$$
The $-r\dot\theta^2$ in $a_r$ is the centripetal term; the $2\dot r\dot\theta$ in $a_\theta$ is the Coriolis term. For $\rho=R,\ \theta=\omega t$: $a_r=-R\omega^2,\ a_\theta=0$; for $\rho=1+t,\ \theta=t$: $a_\theta=2\dot r\dot\theta=2$, matching `polar_acceleration_components`.

### P3.  Radius of curvature from v × a  *(Fowles 7e, Prob. 1.27, p.46)*
Show that for any trajectory the radius of curvature is ρ = |**v**|³ / |**v**×**a**|,
i.e. |**v**×**a**| = v³/ρ. (Hint: **a** = a_T **T̂** + (v²/ρ) **N̂**, and **v**×**T̂** = 0.)
*Check:* for a circle of radius R, `radius_of_curvature(circ)(t) ≈ R`; for a
straight line, `curvature(line)(t) ≈ 0`.

**Solution.** Write the acceleration in the tangential/normal (Frenet) basis, $\mathbf a=a_T\hat{\mathbf T}+(v^2/\rho)\hat{\mathbf N}$, and the velocity as $\mathbf v=v\,\hat{\mathbf T}$ with $v=|\mathbf v|$. Then
$$\mathbf v\times\mathbf a=v\,\hat{\mathbf T}\times\!\Big(a_T\hat{\mathbf T}+\frac{v^2}{\rho}\hat{\mathbf N}\Big)=\frac{v^3}{\rho}\,(\hat{\mathbf T}\times\hat{\mathbf N})=\frac{v^3}{\rho}\,\hat{\mathbf B},$$
since $\hat{\mathbf T}\times\hat{\mathbf T}=\mathbf 0$. Taking magnitudes, $|\mathbf v\times\mathbf a|=v^3/\rho$, hence $\rho=|\mathbf v|^3/|\mathbf v\times\mathbf a|$ and $\kappa=1/\rho=|\mathbf v\times\mathbf a|/|\mathbf v|^3$. A circle of radius $R$ gives $\rho=R$ (so `radius_of_curvature(circ)≈R`); a straight line has $\mathbf a\parallel\mathbf v$, so $\mathbf v\times\mathbf a=\mathbf 0$ and $\kappa=0$.

### P4.  Centripetal acceleration of uniform circular motion  *(Fowles 7e §1.11, p.36)*
For **r**(t) = (R cos ωt, R sin ωt, 0) show |**v**| = Rω is constant, the
acceleration is **a** = −ω²**r** (points to the centre), and a_N = v²/R = Rω²
with a_T = 0.
*Check:* `speed`, `normal_acceleration`, `tangential_acceleration`, and
`acceleration(circ)(t) ≈ −ω² r(t)`.

**Solution.** Differentiate $\mathbf r=(R\cos\omega t,\,R\sin\omega t,\,0)$:
$$\mathbf v=(-R\omega\sin\omega t,\,R\omega\cos\omega t,\,0),\qquad |\mathbf v|=R\omega=\text{const}.$$
Differentiating again, $\mathbf a=(-R\omega^2\cos\omega t,\,-R\omega^2\sin\omega t,\,0)=-\omega^2\mathbf r$, which points from the particle straight back to the centre. Because the speed is constant, $a_T=d|\mathbf v|/dt=0$, so all of $\mathbf a$ is normal: $a_N=|\mathbf a|=R\omega^2=(R\omega)^2/R=v^2/R$. With $R=2,\ \omega=3$ the code gives $|\mathbf v|=6$, $a_N=18=R\omega^2$, $a_T\approx0$, and $\mathbf a=-9\,\mathbf r$.

### P5.  Specific angular momentum of a helix  *(bridge to `~CM-09`; Goldstein 3e §1.1, Eq. 1.7, p.2)*
For the helix **r**(t) = (cos t, sin t, t): compute **v**, the specific angular
momentum **ℓ** = **r**×**v**, and d**ℓ**/dt. Is **ℓ** conserved? What does that
say about whether the (would-be) force is central?
*Check:* build `v = velocity(r)` and `l = cross(r, v)` (MA-01 `cross` on the
velocity function); sample `[l(t+h)−l(t)]/h` and compare to `cross(r, acceleration(r))(t)`.

**Solution.** For $\mathbf r=(\cos t,\sin t,t)$, $\mathbf v=\dot{\mathbf r}=(-\sin t,\cos t,1)$, so
$$\boldsymbol\ell=\mathbf r\times\mathbf v=(\sin t-t\cos t,\ -\cos t-t\sin t,\ 1).$$
Differentiating, $\dfrac{d\boldsymbol\ell}{dt}=(t\sin t,\ -t\cos t,\ 0)$, which equals $\mathbf r\times\mathbf a$ with $\mathbf a=\ddot{\mathbf r}=(-\cos t,-\sin t,0)$ (the $\dot{\mathbf r}\times\dot{\mathbf r}$ part vanishes, leaving only $\mathbf r\times\mathbf a$). Since $d\boldsymbol\ell/dt\neq\mathbf 0$, $\boldsymbol\ell$ is **not** conserved: there is a nonzero torque $\mathbf r\times\mathbf a$, so the would-be force is **not** central (a central force $\parallel\mathbf r$ would give $\mathbf r\times\mathbf a=\mathbf 0$). Sampling at $t=0.7$ gives $d\boldsymbol\ell/dt\approx(0.451,-0.535,0)$, equal to `cross(r, acceleration(r))(0.7)`.
