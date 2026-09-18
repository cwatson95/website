# CM-06 — Problems

Work by hand, then check with `code/linear_momentum.py`. Citations in `../refs.md`.

### P1.  Impulse equals change in momentum  *(Fowles 7e §7.5, p.305)*
For a particle under a constant force F over time Δt, show **J** = **F**Δt = Δ**p**.
*Check:* `impulse(lambda t:F, 0, dt)` vs `momentum(m, vT) − momentum(m, v0)`.

**Solution.** Newton's second law in momentum form is $\mathbf F=d\mathbf p/dt$, so integrating over the interval gives the impulse–momentum theorem:
$$\mathbf J=\int_{t_1}^{t_2}\mathbf F\,dt=\int_{t_1}^{t_2}\frac{d\mathbf p}{dt}\,dt=\mathbf p(t_2)-\mathbf p(t_1)=\Delta\mathbf p.$$
For a **constant** force the integral is simply $\mathbf F\,\Delta t$, hence $\mathbf J=\mathbf F\,\Delta t=\Delta\mathbf p$. In code, `impulse(lambda t:F, 0, dt)` equals $m\mathbf v_T-m\mathbf v_0=$ `momentum(m, vT) − momentum(m, v0)`.

### P2.  A time-varying force  *(Fowles 7e §7.5, p.305)*
For F(t) = (t, 0, 0), compute the impulse over [0, 2] (= (2,0,0)). *Check:*
`impulse(lambda t:(t,0,0), 0, 2)`.

**Solution.** Only the $x$-component of $\mathbf F(t)=(t,0,0)$ is nonzero, so
$$J_x=\int_0^2 t\,dt=\Big[\tfrac12 t^2\Big]_0^2=\tfrac12(4)=2,\qquad J_y=J_z=0.$$
Thus $\mathbf J=(2,0,0)$, exactly the trapezoidal value returned by `impulse(lambda t:(t,0,0), 0, 2)`.

### P3.  Conservation in the absence of external force  *(Fowles 7e §7.1, p.277)*
Show that equal-and-opposite internal forces give zero net impulse on the system,
so total momentum is conserved. *Check:* `impulse(f) + impulse(-f) = 0`.

**Solution.** By Newton's third law the internal forces act in equal-and-opposite pairs $\mathbf f_{21}=-\mathbf f_{12}$ over the same interval, so their impulses cancel:
$$\mathbf J_{12}+\mathbf J_{21}=\int_{t_1}^{t_2}\big(\mathbf f_{12}+(-\mathbf f_{12})\big)\,dt=\mathbf 0.$$
Hence the net internal impulse is zero, and $\Delta\mathbf P=\mathbf J^{\rm(ext)}$; with no external force $\mathbf P$ is conserved. In code `impulse(f) + impulse(-f) = 0` componentwise (the demo prints $[0,0,0]$).

### P4.  Recoil  *(Goldstein 3e §1.2, p.6)*
A stationary body of mass M splits into m₁ and m₂. Use ΣP = 0 to relate their
velocities (m₁v₁ = −m₂v₂). *Check:* `total_momentum([m1,m2],[v1,v2])` ≈ 0.

**Solution.** The body starts at rest, so $\mathbf P_\text{initial}=\mathbf 0$; with no external force $\mathbf P$ is conserved, so after the split
$$\mathbf P=m_1\mathbf v_1+m_2\mathbf v_2=\mathbf 0\ \Longrightarrow\ m_1\mathbf v_1=-m_2\mathbf v_2.$$
The fragments recoil back-to-back with momenta of equal magnitude and opposite direction; the lighter one moves faster, $|\mathbf v_1|/|\mathbf v_2|=m_2/m_1$. For any such pair `total_momentum([m1,m2],[v1,v2])` $\approx(0,0,0)$.

### P5.  Rocket idea  *(Marion & Thornton 5e §9.3, p.331)*
Explain how a rocket accelerates with no external force by ejecting mass backward
(the system's total momentum is conserved; the rocket gains what the exhaust loses).

**Solution.** Treat rocket + exhaust as one isolated system, so the total momentum is conserved even though the rocket accelerates. In time $dt$ a rocket of mass $m$ ejects $dm_\text{ex}$ of exhaust at velocity $u$ backward relative to the rocket; momentum balance $m\,dv=u\,dm_\text{ex}$ supplies the forward thrust. Integrating $m\,dv=-u\,dm$ (with $dm=-dm_\text{ex}$ the rocket's mass loss) gives the **Tsiolkovsky equation**
$$\Delta v=u\,\ln\!\frac{m_i}{m_f}.$$
The forward momentum the rocket gains exactly equals the backward momentum carried off by the exhaust, so $\mathbf P_\text{total}$ never changes — propulsion with no external force.
