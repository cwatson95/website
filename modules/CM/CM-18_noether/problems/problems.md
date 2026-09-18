# CM-18 — Problems

Work by hand, then check with `code/noether.py`. Citations in `../refs.md`.

### P1.  Translation → momentum  *(Goldstein 3e §2.6, p.54)*
Show that if L is invariant under q → q + ε then p = ∂L/∂q̇ is conserved. *Check:*
free particle has `symmetry_defect` ~0 and a constant `noether_charge`.

**Solution.** Under the flow $\delta q=\varepsilon f(q)$ the Lagrangian changes, to
first order, by
$$\delta L=\varepsilon\left(\frac{\partial L}{\partial q}\,f+\frac{\partial L}{\partial\dot q}\,\dot f\right).$$
On a trajectory the Euler–Lagrange equation gives $\partial L/\partial q=\tfrac{d}{dt}(\partial L/\partial\dot q)=\dot p$,
so the two terms collapse into a single total derivative:
$$\delta L=\varepsilon\big(\dot p\,f+p\,\dot f\big)=\varepsilon\,\frac{d}{dt}\big(p\,f\big)=\varepsilon\,\dot Q,\qquad Q=\frac{\partial L}{\partial\dot q}\,f.$$
A symmetry means $\delta L=0$, hence $\dot Q=0$. For pure translation $f=1$ this charge is
$Q=p=\partial L/\partial\dot q$ — the momentum. The free particle $L=\tfrac12\dot q^2$ has no
$q$-dependence, so the defect vanishes (`symmetry_defect` $=$ `0.00e+00`) and the charge is
frozen along the motion: `noether_charge` runs $2.5000\to2.5000$.

### P2.  A potential breaks translation  *(Goldstein 3e §2.6, p.54)*
Show the harmonic oscillator is **not** translation-invariant (V depends on q), so
momentum is not conserved. *Check:* `symmetry_defect(sho, f=1)` ≠ 0.

**Solution.** Now the potential $V=\tfrac12 w^2q^2$ depends on position, so
$$\frac{\partial L}{\partial q}=-w^2q\neq0.$$
The first-order change under $q\to q+\varepsilon$ (here $f=1$, $f'=0$) is exactly
$\delta L/\varepsilon=\partial L/\partial q=-w^2q$, which is what `symmetry_defect` evaluates.
With $w=2$ at the demo point $q=1$ this gives $-(2^2)(1)=-4\neq0$, so translation is broken and
the Euler–Lagrange equation reads $\dot p=\partial L/\partial q=-w^2q\neq0$ — the momentum is
not conserved, it is being driven by the restoring force. This matches
`symmetry_defect(sho, f=1)` $=-4.0000$.

### P3.  Time-translation → energy  *(Goldstein 3e §2.6, p.54)*
Show that if ∂L/∂t = 0 the Jacobi energy h = q̇ ∂L/∂q̇ − L is conserved. *Check:*
`energy` is constant along the oscillator's integrated motion.

**Solution.** Differentiate the Jacobi energy $h=\dot q\,\partial L/\partial\dot q-L$ along
the motion:
$$\frac{dh}{dt}=\ddot q\,\frac{\partial L}{\partial\dot q}+\dot q\,\frac{d}{dt}\frac{\partial L}{\partial\dot q}-\frac{dL}{dt}.$$
Expanding $\dfrac{dL}{dt}=\dfrac{\partial L}{\partial t}+\dfrac{\partial L}{\partial q}\dot q+\dfrac{\partial L}{\partial\dot q}\ddot q$
and using the Euler–Lagrange relation $\tfrac{d}{dt}(\partial L/\partial\dot q)=\partial L/\partial q$,
every term cancels except one:
$$\frac{dh}{dt}=-\frac{\partial L}{\partial t}.$$
So time-translation symmetry, $\partial L/\partial t=0$, makes $h$ conserved — Noether's theorem
for the clock. The oscillator $h=\tfrac12\dot q^2+\tfrac12 w^2q^2=T+V$ carries no explicit $t$;
with amplitude $A=1$ and $w=2$ it equals $\tfrac12 w^2A^2=2$, held fixed along the integrated
orbit so that `energy` runs $2.00000\to2.00000$.

### P4.  Rotation → angular momentum  *(→ `~CM-09`)*
For a central Lagrangian, the rotation symmetry gives conserved angular momentum.
Connect this to the central-force result of `~CM-09`/`~CM-11`.
*Answer:* the rotation generator $f=(-y,x)$ gives the Noether charge $Q=xp_y-yp_x=L_z$ —
angular momentum, the conserved quantity of central-force motion (`~CM-09`/`~CM-11`).

**Solution.** Take a planar central Lagrangian $L=\tfrac12 m(\dot x^2+\dot y^2)-V(r)$ with
$r=\sqrt{x^2+y^2}$. An infinitesimal rotation by $\delta\phi$ acts as $\delta x=-y\,\delta\phi$,
$\delta y=x\,\delta\phi$, i.e. generator $f=(-y,x)$; it leaves $r$ (hence $V$) and the kinetic
$\dot x^2+\dot y^2$ unchanged, so $\delta L=0$. The two-component Noether charge is then
$$Q=\frac{\partial L}{\partial\dot x}f_x+\frac{\partial L}{\partial\dot y}f_y=p_x(-y)+p_y(x)=x\,p_y-y\,p_x=L_z.$$
Equivalently, in polar coordinates $L=\tfrac12 m(\dot r^2+r^2\dot\theta^2)-V(r)$ is independent of
$\theta$, so $\theta$ is cyclic and $p_\theta=\partial L/\partial\dot\theta=mr^2\dot\theta$ is
conserved — the same $L_z$. This is exactly the angular momentum that fixes the orbital plane and
gives Kepler's second law in `~CM-09`/`~CM-11`; it is the rotational twin of the
translation $\to$ momentum charge verified in P1 (`noether_charge` $2.5000\to2.5000$).

### P5.  Cyclic coordinates  *(Goldstein 3e §2.6, p.54)*
Identify the cyclic coordinate(s) of a planar Kepler Lagrangian L(r, ṙ, θ̇) and the
conserved momentum each implies (here, the angular momentum p_θ).
*Answer:* $\theta$ is the only cyclic coordinate; $p_\theta=\partial L/\partial\dot\theta=mr^2\dot\theta$
(angular momentum) is conserved. $r$ is not cyclic, while $\partial L/\partial t=0$ additionally
conserves energy.

**Solution.** The planar Kepler Lagrangian
$$L(r,\dot r,\dot\theta)=\tfrac12 m\big(\dot r^2+r^2\dot\theta^2\big)+\frac{GMm}{r}$$
contains $\theta$ only through $\dot\theta$, never $\theta$ itself, so $\theta$ is cyclic:
$\partial L/\partial\theta=0$ and the Euler–Lagrange equation collapses to
$\tfrac{d}{dt}(\partial L/\partial\dot\theta)=0$. Hence
$$p_\theta=\frac{\partial L}{\partial\dot\theta}=mr^2\dot\theta=\text{const},$$
the conserved angular momentum (the $f=1$ rotation charge of P4). By contrast $r$ appears
explicitly — in $r^2\dot\theta^2$ and in $GMm/r$ — so $p_r=m\dot r$ is *not* conserved; that
equation carries the centrifugal and gravitational forces. Since $L$ also has no explicit $t$, the
Jacobi energy is conserved as well, exactly as in P3 (`energy` $2.00000\to2.00000$). One missing
coordinate $\Rightarrow$ one conserved momentum — the cyclic-coordinate shortcut.
