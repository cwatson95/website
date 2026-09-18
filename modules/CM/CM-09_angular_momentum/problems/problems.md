# CM-09 — Problems

Work by hand, then check with `code/angular_momentum.py`. Citations in `../refs.md`.

### P1.  Angular momentum and torque  *(Fowles 7e §7.2, p.278)*
Compute **L** = m**r**×**v** for m=2, **r**=(1,0,0), **v**=(0,3,0), and the torque
of **F**=(0,5,0) at **r**=(2,0,0). *Check:* `angular_momentum`, `torque`.

**Solution.** The cross products are
$$\mathbf r\times\mathbf v=(1,0,0)\times(0,3,0)=(0,0,3),\qquad \mathbf L=m(\mathbf r\times\mathbf v)=2(0,0,3)=(0,0,6).$$
For the torque, $\mathbf N=\mathbf r\times\mathbf F=(2,0,0)\times(0,5,0)=(0,0,10)$. Both point along $+\hat{\mathbf z}$ (right-hand rule for motion/force in the $xy$-plane), giving $\mathbf L=(0,0,6)$ and $\mathbf N=(0,0,10)$ — exactly `angular_momentum(2,(1,0,0),(0,3,0))` and `torque((2,0,0),(0,5,0))`.

### P2.  A central force exerts no torque  *(Fowles 7e §6.4, p.226)*
Show **N** = **r** × **F** = **0** whenever **F** ∥ **r**. *Check:*
`torque((2,1,0), (-4,-2,0))` → (0,0,0).

**Solution.** "Central" means the force is parallel to the radius vector, $\mathbf F=\lambda\,\mathbf r$ for some scalar $\lambda$. Then
$$\mathbf N=\mathbf r\times\mathbf F=\mathbf r\times(\lambda\mathbf r)=\lambda\,(\mathbf r\times\mathbf r)=\mathbf 0,$$
since any vector crossed with itself vanishes. Here $\mathbf F=(-4,-2,0)=-2\,(2,1,0)=-2\,\mathbf r$ is (anti)parallel to $\mathbf r$, so `torque((2,1,0), (-4,-2,0))` $\to(0,0,0)$.

### P3.  dL/dt = N  *(Fowles 7e §7.2, p.278)*
For any trajectory, show d**L**/dt = m**r**×**a** = **N**. *Check:* numerically
differentiate `angular_momentum_of(m, traj)` and compare to `torque_rate(m, traj)`.

**Solution.** Differentiate $\mathbf L=m(\mathbf r\times\mathbf v)$ with the product rule:
$$\frac{d\mathbf L}{dt}=m\big(\underbrace{\mathbf v\times\mathbf v}_{=\,\mathbf 0}+\mathbf r\times\mathbf a\big)=m\,(\mathbf r\times\mathbf a)=\mathbf r\times(m\mathbf a)=\mathbf r\times\mathbf F=\mathbf N,$$
using $\mathbf v\times\mathbf v=\mathbf 0$ and Newton's law $\mathbf F=m\mathbf a$. So torque is the rate of change of angular momentum. Numerically, for $\mathbf r(t)=(t,t^2,\sin t)$ and $m=2$ at $t=0.7$, both the finite difference of `angular_momentum_of(m, traj)` and `torque_rate(m, traj)` give $(-3.208,\,0.902,\,2.800)$.

### P4.  Angular momentum of circular motion  *(Goldstein 3e §1.2, p.6)*
For **r**(t) = (R cos ωt, R sin ωt, 0) show **L** = m R²ω **ẑ** is constant. *Check:*
`angular_momentum_of` at several t.

**Solution.** With $\mathbf r=(R\cos\omega t,R\sin\omega t,0)$ and $\mathbf v=\dot{\mathbf r}=(-R\omega\sin\omega t,R\omega\cos\omega t,0)$, only the $z$-component of $\mathbf r\times\mathbf v$ survives:
$$(\mathbf r\times\mathbf v)_z=x\dot y-y\dot x=R^2\omega\cos^2\omega t+R^2\omega\sin^2\omega t=R^2\omega.$$
Hence $\mathbf L=m(\mathbf r\times\mathbf v)=mR^2\omega\,\hat{\mathbf z}$, independent of $t$. With $R=2,\ \omega=3,\ m=1.5$ this is $(0,0,18)$ at every sample time, as `angular_momentum_of` confirms — constant because the centripetal force is central.

### P5.  Kepler's second law  *(Fowles 7e §6.4, p.226)*
Show that constant **L** implies the radius vector sweeps equal areas in equal
times (dA/dt = L/2m). This is the conservation law underlying `~CM-11`.

**Solution.** In time $dt$ the radius vector sweeps a thin triangle of area $dA=\tfrac12|\mathbf r\times d\mathbf r|=\tfrac12|\mathbf r\times\mathbf v|\,dt$. Therefore
$$\frac{dA}{dt}=\frac12|\mathbf r\times\mathbf v|=\frac{|\mathbf L|}{2m},$$
since $\mathbf L=m(\mathbf r\times\mathbf v)$. When the force is central, $\mathbf L$ is conserved (P2), so $dA/dt=L/2m$ is **constant**: the radius vector sweeps equal areas in equal times — Kepler's second law, the conservation law underlying the orbit problem `~CM-11`.
