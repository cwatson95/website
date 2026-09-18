# CM-24 — Problems

Work by hand, then check with `code/nonlinear_dynamics.py`. Citations in `../refs.md`.

### P1.  Pendulum fixed points  *(MA-22 / Chicone §1.6)*
For ẋ = (ω, −sin θ) find the fixed points and classify them: (0,0) a center, (π,0)
a saddle. *Check:* `classify_fixed_point(pendulum_flow(0.0), …)`.

*Answer:* fixed points $(0,0)$ and $(\pi,0)$; eigenvalues $\pm i$ (a center) at the bottom, $\pm1$ (a saddle) at the top.

**Solution.** Fixed points require $\omega=0$ and $\sin\theta=0$, i.e. $(\theta,\omega)=(0,0)$ (hanging down) and $(\pi,0)$ (inverted). The Jacobian of the flow $(\omega,\,-\sin\theta)$ and its characteristic equation are
$$J=\begin{pmatrix}0&1\\-\cos\theta&0\end{pmatrix},\qquad \lambda^2+\cos\theta=0.$$
At $(0,0)$, $\cos\theta=1$ gives $\lambda^2=-1$, so $\lambda=\pm i$: purely imaginary — a **center**, the undamped bob oscillating forever. At $(\pi,0)$, $\cos\theta=-1$ gives $\lambda^2=1$, so $\lambda=\pm1$: real and opposite-signed — a **saddle**, the unstable inverted point. So `classify_fixed_point(pendulum_flow(0.0), …)` returns center at $(0,0)$ and saddle at $(\pi,0)$.

### P2.  Damping turns the center into a spiral  *(MA-22 / Chicone §1.6)*
Add damping (γ > 0) and show (0,0) becomes a **stable spiral** (the eigenvalues
gain a negative real part) while (π,0) stays a saddle. *Check:*
`classify_fixed_point(pendulum_flow(0.5), …)`.

*Answer:* damping moves the bottom eigenvalues to $-\tfrac{\gamma}{2}\pm i\sqrt{1-\gamma^2/4}$ (negative real part — a stable spiral); the top stays a saddle.

**Solution.** With linear damping the Jacobian gains $-\gamma$ in the lower-right corner:
$$J=\begin{pmatrix}0&1\\-\cos\theta&-\gamma\end{pmatrix},\qquad \lambda^2+\gamma\lambda+\cos\theta=0.$$
At the bottom ($\cos\theta=1$), $\lambda=-\tfrac{\gamma}{2}\pm\sqrt{\gamma^2/4-1}$; for $\gamma=0.5$ the discriminant is negative, giving complex eigenvalues with real part $-\gamma/2=-0.25<0$ — the center becomes a **stable spiral** that spirals to rest. At the top ($\cos\theta=-1$), $\lambda^2+\gamma\lambda-1=0$ has roots multiplying to $-1$, so they stay real with opposite signs — a **saddle** for any $\gamma$. Hence `classify_fixed_point(pendulum_flow(0.5), …)` gives stable spiral at $(0,0)$ and saddle at $(\pi,0)$.

### P3.  Van der Pol limit cycle  *(→ `~MA-22`)*
Show the van der Pol oscillator has an attracting limit cycle: integrate from
inside and outside and confirm both reach the same closed orbit. *Check:*
`integrate_flow(van_der_pol(1.0), …)` from (0.1,0) and (3,0).

*Answer:* a single attracting limit cycle of amplitude $\approx2$; trajectories from inside and outside both converge to it (amplitude $\approx2.009$).

**Solution.** Write the oscillator as the flow $\dot x=y,\ \dot y=\mu(1-x^2)y-x$ and track the energy $E=\tfrac12(x^2+y^2)$:
$$\frac{dE}{dt}=x\dot x+y\dot y=\mu\,(1-x^2)\,y^2,$$
which is **positive** for $|x|<1$ (negative damping pumps energy in, so small orbits grow) and **negative** for $|x|>1$ (damping drains energy, so large orbits shrink). The two regimes balance on a single isolated closed curve that attracts every nearby trajectory — a limit cycle, impossible for a linear system. Numerically at $\mu=1$, starts at $(0.1,0)$ inside and $(3,0)$ outside both relax to amplitude $\approx2.009$, exactly what `integrate_flow(van_der_pol(1.0), …)` returns for both.

### P4.  Sensitive dependence  *(MA-22)*
For the logistic map at r = 4, show the Lyapunov exponent is ln 2 > 0 (chaos) and
that at r = 2.5 it is negative (a stable fixed point). *Check:* `lyapunov_logistic`.

*Answer:* $\lambda(4)=\ln2\approx0.693>0$ (chaotic — errors double each step); $\lambda(2.5)=\ln\tfrac12\approx-0.693<0$ (a stable fixed point).

**Solution.** The Lyapunov exponent averages the log-stretching of the map $x\mapsto rx(1-x)$, whose derivative is $f'(x)=r(1-2x)$:
$$\lambda=\lim_{N\to\infty}\frac1N\sum_{n=0}^{N-1}\ln\big|r(1-2x_n)\big|.$$
At $r=4$ the map is conjugate to a doubling (Bernoulli) shift, so $\lambda=\ln2\approx0.693>0$: an initial error grows like $e^{\lambda n}$, doubling each step — sensitive dependence on initial conditions, i.e. chaos. At $r=2.5$ the orbit sits at the stable fixed point $x_*=1-1/r=0.6$, where $|f'(x_*)|=|2-r|=0.5$, giving $\lambda=\ln0.5=-\ln2\approx-0.693<0$ and decaying perturbations. Thus `lyapunov_logistic(4.0)` $=0.6931$ while `lyapunov_logistic(2.5)` $=-0.6931<0$.

### P5.  The route to chaos
Describe period-doubling as r increases in the logistic map (2 → 4 → 8 → … →
chaos) — the Feigenbaum scenario. *(Sweep `lyapunov_logistic(r)` from 2.8 to 4.)*

*Answer:* stable fixed point $\to$ period 2 ($r=3$) $\to$ 4 ($\approx3.449$) $\to$ 8 ($\approx3.544$) $\to\cdots$ accumulating at $r_\infty\approx3.570$ (Feigenbaum, ratio $\delta\approx4.669$), then chaos ($\lambda>0$) threaded with periodic windows.

**Solution.** The fixed point $x_*=1-1/r$ is stable while $|f'(x_*)|=|2-r|<1$, i.e. $r<3$. At $r=3$ the multiplier reaches $-1$ and the orbit period-doubles to a 2-cycle; that doubles to a 4-cycle at $r\approx3.449$, then 8 at $r\approx3.544$, and so on, the thresholds converging geometrically,
$$\frac{r_n-r_{n-1}}{r_{n+1}-r_n}\ \to\ \delta\approx4.669\quad(\text{Feigenbaum}),$$
to an accumulation point $r_\infty\approx3.5699$ where the period becomes infinite and chaos sets in. Sweeping `lyapunov_logistic(r)` shows exactly this: $\lambda<0$ in the periodic regime ($r=2.8\to-0.223$, $r=3.5\to-0.873$), $\lambda\to0^-$ at each bifurcation, then $\lambda>0$ once chaotic ($r=3.7\to0.356$, $r=4\to0.693$), dipping back below zero inside periodic windows such as the period-3 window near $r=3.83$ ($\lambda=-0.370$). This universal period-doubling cascade is the Feigenbaum route to chaos.
