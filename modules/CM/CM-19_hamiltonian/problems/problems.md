# CM-19 — Problems

Work by hand, then check with `code/hamiltonian.py`. Citations in `../refs.md`.

### P1.  Legendre transform of the oscillator  *(Goldstein 3e §8.1, p.334)*
From L = ½q̇² − ½ω²q² get p = q̇ and H = ½p² + ½ω²q². *Check:*
`hamiltonian_from_potential(1, lambda q: 0.5*w*w*q*q)`.

*Answer:* $p=\dot q$ and $H=\tfrac12 p^2+\tfrac12\omega^2 q^2$ (the total energy $T+V$).

**Solution.** The momentum conjugate to $q$ is $p=\partial L/\partial\dot q=\dot q$, so the
velocity to eliminate is $\dot q=p$. The Hamiltonian is the Legendre transform of $L$ in $\dot q$:
$$H=p\dot q-L=p\cdot p-\Big(\tfrac12 p^2-\tfrac12\omega^2 q^2\Big)=\tfrac12 p^2+\tfrac12\omega^2 q^2.$$
Because $L$ is quadratic in $\dot q$, Euler's theorem gives $p\dot q=2T$, hence
$H=2T-(T-V)=T+V$ is just the total energy. The code's
`hamiltonian_from_potential(1, lambda q: 0.5*w*w*q*q)` builds exactly
$H(q,p)=p^2/2+\tfrac12\omega^2q^2$; for $\omega=2$ at the start $(q,p)=(1,0)$ it returns
$H=\tfrac12\cdot4\cdot1^2=2$, the demo's `H: 2.000000`.

### P2.  Hamilton's equations  *(Fowles 7e §10.9, p.455)*
Show q̇ = ∂H/∂p = p and ṗ = −∂H/∂q = −ω²q, recovering SHM. *Check:* `hamilton_rhs`
signs and the integrated q(t) = cos(ωt).

*Answer:* $\dot q=p,\ \dot p=-\omega^2 q$, so $\ddot q=-\omega^2 q$ — SHM with $q(t)=\cos\omega t$.

**Solution.** Reading the partials of $H=\tfrac12 p^2+\tfrac12\omega^2 q^2$ straight off,
$$\dot q=\frac{\partial H}{\partial p}=p,\qquad \dot p=-\frac{\partial H}{\partial q}=-\omega^2 q.$$
The single second-order Euler–Lagrange equation has split into two symmetric first-order
equations. Differentiating the first and substituting the second eliminates $p$:
$\ddot q=\dot p=-\omega^2 q$, simple harmonic motion, solved by $q(t)=\cos\omega t$ for
$q(0)=1,\ \dot q(0)=0$. The code's `hamilton_rhs` returns
$[\,\partial H/\partial p,\,-\partial H/\partial q\,]=[\,p,\,-\omega^2 q\,]$ — at
$\omega=3,\ (q,p)=(2,5)$ that is $(\dot q,\dot p)=(5,-18)$ with the correct signs — and
integrating at $\omega=2$ from $(1,0)$ gives $q(\pi/2)=\cos\pi=-1$, the demo's
`q(pi/2) = -1.00000`.

### P3.  Energy is conserved  *(Goldstein 3e §8.1, p.334)*
Show dH/dt = 0 along the flow when H has no explicit time. *Check:* H constant
along `integrate_hamilton`.

*Answer:* $dH/dt=\partial H/\partial t$ along the flow, which vanishes when $H$ has no explicit $t$.

**Solution.** Differentiate $H(q,p,t)$ along a trajectory with the chain rule, then
substitute Hamilton's equations $\dot q=\partial H/\partial p,\ \dot p=-\partial H/\partial q$:
$$\frac{dH}{dt}=\frac{\partial H}{\partial q}\dot q+\frac{\partial H}{\partial p}\dot p+\frac{\partial H}{\partial t}=\frac{\partial H}{\partial q}\frac{\partial H}{\partial p}-\frac{\partial H}{\partial p}\frac{\partial H}{\partial q}+\frac{\partial H}{\partial t}=\frac{\partial H}{\partial t}.$$
The two dynamical terms cancel identically, so an autonomous Hamiltonian
($\partial H/\partial t=0$) is conserved — the energy is a constant of the motion. The demo
integrates the $\omega=2$ oscillator over a full period and prints `H: 2.000000 -> 2.000000`,
and `test_energy_conserved` (with $\omega=1.5$) holds $H$ fixed to within $10^{-5}$ all along
the flow.

### P4.  Phase-space orbit  *(Fowles 7e §10.9, p.455)*
Show the SHO orbit in (q, p) is the closed ellipse p² + ω²q² = 2E. *Check:* the
quantity p² + ω²q² is constant on the trajectory.

*Answer:* $p^2+\omega^2 q^2=2E$ — an ellipse with semi-axes $\sqrt{2E}$ (in $p$) and
$\sqrt{2E}/\omega$ (in $q$).

**Solution.** Energy conservation (P3) pins the orbit to a level set of
$H=\tfrac12 p^2+\tfrac12\omega^2 q^2=E$. Multiplying through by $2$,
$$p^2+\omega^2 q^2=2E=\text{const},$$
the equation of an ellipse in the $(q,p)$ plane with semi-axis $\sqrt{2E}$ along the
$p$-axis and $\sqrt{2E}/\omega$ along the $q$-axis. The level set is a closed curve, so the
motion is periodic and returns to its starting point each period. In the demo, $\omega=2$
launched from $(q,p)=(1,0)$ has $E=2$, giving $p^2+\omega^2q^2=2E=4$ (numerically equal to
$\omega^2$ here because $q_0=1$); the printed `p^2 + w^2 q^2 along orbit: [4.0, 4.0, ...]`
stays pinned at $4.0$, and `test_phase_orbit_is_closed_ellipse` confirms the trajectory
closes after one period.

### P5.  Pendulum phase portrait
Sketch the (θ, p_θ) phase portrait of a pendulum: closed curves (libration) inside
the separatrix, open curves (rotation) outside. *(Integrate from several energies.)*

*Answer:* center at $(0,0)$, saddles at $(\pm\pi,0)$; libration (closed loops) for
$E<2mg\ell$, rotation (open curves) for $E>2mg\ell$, divided by the separatrix at $E=2mg\ell$.

**Solution.** For the pendulum $H=\dfrac{p_\theta^2}{2m\ell^2}+mg\ell(1-\cos\theta)$,
Hamilton's equations are
$$\dot\theta=\frac{\partial H}{\partial p_\theta}=\frac{p_\theta}{m\ell^2},\qquad
\dot p_\theta=-\frac{\partial H}{\partial\theta}=-mg\ell\sin\theta.$$
Energy $E=H$ is conserved (P3), so each orbit is a contour $E=\text{const}$. The equilibria
$\sin\theta=0,\ p_\theta=0$ are a stable **center** at $(0,0)$ and unstable **saddles** at
$(\pm\pi,0)$, whose energy $E=2mg\ell$ defines the **separatrix**. For $E<2mg\ell$ the bob
cannot reach the top: $p_\theta$ vanishes at two turning points and the contour is a closed
loop about $(0,0)$ — **libration**. For $E>2mg\ell$, $p_\theta$ keeps one sign, $\theta$
advances without bound, and the contour runs off across the $\theta$-axis — **rotation** over
the top. Integrating `integrate_hamilton` from energies straddling $2mg\ell$ traces exactly
these two families, separated by the separatrix through $(\pm\pi,0)$.
