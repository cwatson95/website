# CM-17 — Problems

Work by hand, then check with `code/lagrangian.py`. Citations in `../refs.md`.

### P1.  Euler–Lagrange for the oscillator  *(Fowles 7e §10.4, p.430; Goldstein 3e §2.3, p.44)*
For L = ½q̇² − ½ω²q² show the EL equation is q̈ = −ω²q and that q = cos(ωt) solves
it. *Check:* `el_residual` is ~0 on cos(ωt), large on a wrong path.

**Solution.** The Lagrangian $L=\tfrac12\dot q^2-\tfrac12\omega^2 q^2$ has $\partial L/\partial\dot q=\dot q$ and $\partial L/\partial q=-\omega^2 q$, so the Euler–Lagrange equation reads
$$\frac{d}{dt}\frac{\partial L}{\partial\dot q}-\frac{\partial L}{\partial q}=\frac{d}{dt}(\dot q)+\omega^2 q=\ddot q+\omega^2 q=0,$$
i.e. $\ddot q=-\omega^2 q$. Substituting the candidate $q=\cos\omega t$ gives $\ddot q=-\omega^2\cos\omega t=-\omega^2 q$, so the residual vanishes identically along it. Numerically `el_residual` on the true path $\cos\omega t$ peaks at $8.22\times10^{-5}\approx0$, whereas a wrong path such as $q=t^2$ pushes it above $0.1$ — exactly the contrast the check asserts.

### P2.  The pendulum in one coordinate  *(Fowles 7e §10.2, p.423)*
Use θ as the generalized coordinate: L = ½ml²θ̇² + mgl cos θ ⇒ θ̈ = −(g/l)sin θ.
*Check:* integrate with `integrate_eom` and confirm the EL residual stays ~0.

**Solution.** With $L=\tfrac12 ml^2\dot\theta^2+mgl\cos\theta$, the pieces are $\partial L/\partial\dot\theta=ml^2\dot\theta$ and $\partial L/\partial\theta=-mgl\sin\theta$. Euler–Lagrange then gives
$$\frac{d}{dt}\big(ml^2\dot\theta\big)+mgl\sin\theta=ml^2\ddot\theta+mgl\sin\theta=0,$$
and dividing by $ml^2$ yields $\ddot\theta=-(g/l)\sin\theta$. Feeding this acceleration to `integrate_eom` produces a trajectory that is, by construction, an extremal of $L$; evaluating `el_residual` on it gives a maximum of $4.71\times10^{-6}\approx0$, confirming the integrated path satisfies the EL equation.

### P3.  Conjugate momentum  *(Fowles 7e §10.4, p.430)*
Compute p = ∂L/∂q̇ for a kinetic Lagrangian and show it is the ordinary momentum
mq̇. *Check:* `generalized_momentum`.

**Solution.** For a kinetic-energy Lagrangian $L=\tfrac12 m\dot q^2-V(q)$ the conjugate momentum is
$$p=\frac{\partial L}{\partial\dot q}=\frac{\partial}{\partial\dot q}\Big(\tfrac12 m\dot q^2-V(q)\Big)=m\dot q,$$
since the potential $V(q)$ carries no $\dot q$ dependence and drops out — leaving exactly the ordinary Newtonian momentum. The central-difference `generalized_momentum` reproduces it: in the demo ($m=1$, $\dot q=3$) it returns $3.0000=m\dot q$, and for $m=2$, $\dot q=3$ it gives $m\dot q=6$.

### P4.  Cyclic coordinate  *(Goldstein 3e §2.6, p.54; → `~CM-18`)*
Show that if L does not depend on q, then p = ∂L/∂q̇ is conserved. *Check:* free
particle momentum is constant along the motion.

**Solution.** A coordinate is cyclic when $\partial L/\partial q=0$. The Euler–Lagrange equation then collapses to
$$\frac{d}{dt}\frac{\partial L}{\partial\dot q}=\frac{\partial L}{\partial q}=0\quad\Longrightarrow\quad p=\frac{\partial L}{\partial\dot q}=\text{const},$$
so the conjugate momentum is a constant of the motion. For the free particle $L=\tfrac12\dot q^2$ there is no $q$ in $L$, hence $p=\dot q$ is conserved: integrating $\ddot q=0$ from $\dot q=2.5$ and sampling `generalized_momentum` along the path returns $2.5$ at every checkpoint, as the test verifies.

### P5.  Jacobi energy = Hamiltonian  *(→ `~CM-19`)*
Show h = q̇ ∂L/∂q̇ − L equals T + V for L = T − V. *Check:* `jacobi_energy`.

**Solution.** Take $L=T-V$ with $T=\tfrac12 m\dot q^2$ quadratic in the velocity. Then $\partial L/\partial\dot q=m\dot q$, so $\dot q\,\partial L/\partial\dot q=m\dot q^2=2T$ (Euler's theorem for a homogeneous quadratic). Hence
$$h=\dot q\,\frac{\partial L}{\partial\dot q}-L=2T-(T-V)=T+V,$$
the total mechanical energy — and the Hamiltonian of `~CM-19`. The demo's SHO at $q=1,\dot q=0$ has $h=\tfrac12\omega^2=2$, and `jacobi_energy` returns $2.0000$; the test's case $m=1.5,\ k=4,\ q=0.7,\ \dot q=1.3$ likewise matches $T+V=2.2475$.
