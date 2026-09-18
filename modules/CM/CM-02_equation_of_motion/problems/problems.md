# CM-02 — Problems

Work by hand, then check with `code/equation_of_motion.py`. Citations in `../refs.md`.

### P1.  Projectile as a constant-acceleration solution  *(Fowles 7e §4.1, p.144)*
Integrate m**r″** = m**g** to get **r**(t) = **r₀** + **v₀**t + ½**g**t² and confirm
it matches the projectile of `~CM-01`. *Check:* `trajectory(uniform_gravity(m), m, …)`.

**Solution.** Newton's law $m\ddot{\mathbf r}=m\mathbf g$ cancels the mass, leaving $\ddot{\mathbf r}=\mathbf g$ (constant). Integrate once for $\dot{\mathbf r}=\mathbf v_0+\mathbf g\,t$ and again:
$$\mathbf r(t)=\mathbf r_0+\mathbf v_0 t+\tfrac12\mathbf g\,t^2,$$
the same parabola as the `~CM-01` projectile. With $\mathbf g=(0,0,-9.81)$, $\mathbf v_0=(10,0,10)$, $\mathbf r_0=\mathbf 0$, $m=2$: $x(2)=20$ and $z(2)=10\cdot2-\tfrac12(9.81)(2)^2=0.38$. The RK4 `trajectory(uniform_gravity(m), m, …)` returns $\mathbf r(2)=(20.0,0,0.38)$, confirming the closed form.

### P2.  Spring → simple harmonic motion  *(Fowles 7e §2.4, p.63)*
For m x″ = −k x show x(t) = x₀cos(ωt) + (v₀/ω)sin(ωt), ω = √(k/m). *Check:*
`trajectory(spring_force(k), m, (1,0,0), (0,0,0), …)` vs cos(ωt).

**Solution.** Dividing $m\ddot x=-kx$ by $m$ gives $\ddot x=-\omega^2 x$ with $\omega=\sqrt{k/m}$ — the SHM equation, whose general solution is $x(t)=A\cos\omega t+B\sin\omega t$. The initial conditions fix the constants: $x(0)=x_0\Rightarrow A=x_0$, and $\dot x(0)=v_0\Rightarrow B\omega=v_0$, i.e. $B=v_0/\omega$. Hence
$$x(t)=x_0\cos\omega t+\frac{v_0}{\omega}\sin\omega t.$$
With $x_0=1,\ v_0=0,\ k=8,\ m=0.5$ (so $\omega=4$) this reduces to $x(t)=\cos4t$; the integrator gives $x(5)=0.4081=\cos(4\cdot5)$, matching `cos(ωt)`.

### P3.  Terminal velocity  *(Fowles 7e §2.4, p.63)*
For falling with linear drag, m z″ = −mg − b z′, show the velocity approaches
v∞ = −mg/b. *Check:* integrate `sum_forces(uniform_gravity(m), linear_drag(b))`.

**Solution.** Write the vertical equation in terms of $v=\dot z$: $m\dot v=-mg-bv$, i.e. $\dot v=-g-\frac{b}{m}v$. The motion stops accelerating when $\dot v=0$, which defines the terminal velocity
$$0=-g-\frac{b}{m}v_\infty\ \Rightarrow\ v_\infty=-\frac{mg}{b}.$$
Solving the linear ODE gives $v(t)=v_\infty+(v_0-v_\infty)e^{-bt/m}$, so $v\to v_\infty$ as $t\to\infty$ for any $v_0$. Integrating `sum_forces(uniform_gravity(m), linear_drag(b))` with $m=1,\ b=0.5$ yields $v_z\to-19.62=-mg/b$.

### P4.  Free-body equilibrium  *(Fowles 7e §2.1, p.47)*
Show that a constant applied force exactly cancelling gravity gives zero net force,
hence straight-line motion. *Check:* `sum_forces(uniform_gravity(m), constant_force((0,0,mg)))`.

**Solution.** The net force is the vector sum of the two applied forces,
$$\mathbf F_\text{net}=\underbrace{(0,0,-mg)}_{\text{gravity}}+\underbrace{(0,0,+mg)}_{\text{applied}}=(0,0,0).$$
By Newton's second law $m\ddot{\mathbf r}=\mathbf F_\text{net}=\mathbf 0$, so $\ddot{\mathbf r}=\mathbf 0$ and the velocity is constant — the body moves in a straight line at constant speed (Newton's first law as the zero-force special case). `sum_forces(uniform_gravity(m), constant_force((0,0,mg)))` returns $(0,0,0)$ at every $(t,\mathbf r,\mathbf v)$.

### P5.  Newton's third law preview  *(Fowles 7e §2.1, p.47)*
Argue that internal forces in a two-body system cancel pairwise, so the total
momentum is unaffected — the conservation law made explicit in `~CM-06`.

**Solution.** Label the mutual forces $\mathbf F_{12}$ (on body 1 from body 2) and $\mathbf F_{21}$ (on body 2 from body 1). Newton's third law states $\mathbf F_{12}=-\mathbf F_{21}$. With no external forces each body obeys $\dot{\mathbf p}_1=\mathbf F_{12}$ and $\dot{\mathbf p}_2=\mathbf F_{21}$, so the total momentum evolves as
$$\frac{d}{dt}(\mathbf p_1+\mathbf p_2)=\mathbf F_{12}+\mathbf F_{21}=\mathbf 0.$$
The internal forces cancel pairwise, leaving $\mathbf p_1+\mathbf p_2$ constant in time — exactly the momentum-conservation law developed in `~CM-06`.
