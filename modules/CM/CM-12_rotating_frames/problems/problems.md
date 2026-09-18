# CM-12 — Problems

Work by hand, then check with `code/rotating_frames.py`. Citations in `../refs.md`.

### P1.  Centrifugal acceleration  *(Fowles 7e §5.3, p.196)*
For **ω** = ω**ẑ** show −ω×(ω×r) = ω²**ρ** (outward, ρ the perpendicular
displacement). *Check:* `centrifugal_acceleration((0,0,w), (x,y,0))` = (w²x, w²y, 0).
*Answer:* $-\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r)=\omega^2\mathbf r-\boldsymbol\omega(\boldsymbol\omega\cdot\mathbf r)=\omega^2\boldsymbol\rho$, outward with magnitude $\omega^2\rho$.

**Solution.** Apply the BAC–CAB identity $\mathbf a\times(\mathbf b\times\mathbf c)=\mathbf b(\mathbf a\cdot\mathbf c)-\mathbf c(\mathbf a\cdot\mathbf b)$:
$$\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r)=\boldsymbol\omega(\boldsymbol\omega\cdot\mathbf r)-\mathbf r\,\omega^2,$$
so $-\boldsymbol\omega\times(\boldsymbol\omega\times\mathbf r)=\omega^2\mathbf r-\boldsymbol\omega(\boldsymbol\omega\cdot\mathbf r)=\omega^2\boldsymbol\rho$, where $\boldsymbol\rho=\mathbf r-(\hat{\boldsymbol\omega}\cdot\mathbf r)\hat{\boldsymbol\omega}$ is the part of $\mathbf r$ perpendicular to the axis. It points outward with magnitude $\omega^2\rho$. For $\boldsymbol\omega=\omega\hat{\mathbf z}$ and $\mathbf r=(x,y,0)$ we have $\boldsymbol\omega\cdot\mathbf r=0$, giving $(\omega^2x,\omega^2y,0)$ — exactly what `centrifugal_acceleration((0,0,w),(x,y,0))` returns, e.g. $(12,0,0)$ for $\omega=2,\ \mathbf r=(3,0,0)$.

### P2.  Coriolis is perpendicular  *(Fowles 7e §5.3, p.196)*
Show −2ω×v is perpendicular to both **ω** and **v**, with magnitude 2ω v_⟂.
*Check:* `dot(coriolis_acceleration(omega, v), omega)` ≈ 0 and likewise with v.
*Answer:* perpendicular to both since $\mathbf a\times\mathbf b\perp\mathbf a,\mathbf b$; magnitude $2\omega v_\perp$.

**Solution.** The Coriolis term is $\mathbf a_{\rm cor}=-2\boldsymbol\omega\times\mathbf v$. A cross product is orthogonal to each of its factors, so
$$\mathbf a_{\rm cor}\cdot\boldsymbol\omega=-2(\boldsymbol\omega\times\mathbf v)\cdot\boldsymbol\omega=0,\qquad \mathbf a_{\rm cor}\cdot\mathbf v=-2(\boldsymbol\omega\times\mathbf v)\cdot\mathbf v=0,$$
both being triple products with a repeated vector. Its magnitude is $|\mathbf a_{\rm cor}|=2|\boldsymbol\omega\times\mathbf v|=2\omega v\sin\theta=2\omega v_\perp$, with $v_\perp$ the component of $\mathbf v$ perpendicular to $\boldsymbol\omega$. Hence `dot(coriolis_acceleration(omega,v), omega)` and the same with `v` are both $\approx0$; for $\boldsymbol\omega=2\hat{\mathbf z},\ \mathbf v=(0,1,0)$ the result $(4,0,0)$ has magnitude $4=2\cdot2\cdot1$.

### P3.  Only the perpendicular part matters  *(Marion & Thornton 5e §10.3, p.391)*
Show the centrifugal term depends only on the component of **r** perpendicular to
**ω**. *Check:* `centrifugal_acceleration((0,0,3), (2,0,5))` ignores the z=5 part.
*Answer:* $\mathbf a_{\rm cf}=\omega^2\boldsymbol\rho$ depends only on $\mathbf r_\perp$; the part of $\mathbf r$ along $\boldsymbol\omega$ drops out.

**Solution.** Split $\mathbf r=\mathbf r_\parallel+\mathbf r_\perp$ with $\mathbf r_\parallel=(\hat{\boldsymbol\omega}\cdot\mathbf r)\hat{\boldsymbol\omega}$. From P1, $\mathbf a_{\rm cf}=\omega^2\mathbf r-\boldsymbol\omega(\boldsymbol\omega\cdot\mathbf r)$; the parallel piece cancels because $\boldsymbol\omega\cdot\mathbf r_\parallel=\omega(\hat{\boldsymbol\omega}\cdot\mathbf r)$ gives
$$\omega^2\mathbf r_\parallel-\boldsymbol\omega(\boldsymbol\omega\cdot\mathbf r_\parallel)=\omega^2\mathbf r_\parallel-\omega^2\mathbf r_\parallel=\mathbf 0,$$
leaving $\mathbf a_{\rm cf}=\omega^2\mathbf r_\perp=\omega^2\boldsymbol\rho$ (equivalently $\boldsymbol\omega\times\mathbf r_\parallel=0$). For $\boldsymbol\omega=3\hat{\mathbf z},\ \mathbf r=(2,0,5)$ the $z=5$ piece is along $\boldsymbol\omega$ and drops out:
$$\mathbf a_{\rm cf}=(3^2\cdot2,\,0,\,0)=(18,0,0),$$
exactly what `centrifugal_acceleration((0,0,3),(2,0,5))` returns.

### P4.  Foucault deflection  *(Marion & Thornton 5e §10.3, p.391)*
Explain qualitatively how the Coriolis force rotates the plane of a pendulum's
swing (the Foucault pendulum) and why the effect vanishes at the equator.
*Answer:* the swing plane precesses at angular rate $\Omega\sin\lambda$ (clockwise in the N. hemisphere); at the equator $\sin\lambda=0$, so there is no precession.

**Solution.** In Earth's rotating frame the bob feels $\mathbf a_{\rm cor}=-2\boldsymbol\Omega\times\mathbf v$. By P2 this force is always perpendicular to the velocity, so it does no work — it cannot change the swing's speed or amplitude, only steer $\mathbf v$ sideways. A push that is permanently $\perp\mathbf v$ rotates the line of swing at a steady rate. Only the local vertical component of $\boldsymbol\Omega$, namely $\Omega_{\rm vert}=\Omega\sin\lambda$ at latitude $\lambda$, turns the horizontal swing plane about the "up" axis, giving a precession period
$$T_F=\frac{2\pi}{\Omega\sin\lambda}=\frac{24\ \text{h}}{\sin\lambda}.$$
At the poles $\sin\lambda=1$ (one turn per day); at the equator $\lambda=0$, so $\boldsymbol\Omega$ is horizontal, its vertical component vanishes, and the Coriolis force has no component about the vertical — the plane does not precess.

### P5.  Centrifugal vs centripetal  *(→ `~CM-10`)*
A bead at rest in a frame co-rotating with a turntable feels an outward
centrifugal force balanced by the real (inward) centripetal force. Show the two
are equal and opposite. *Check:* compare `centrifugal_acceleration` to −ω²**r**.
*Answer:* with $\mathbf v_{\rm rot}=0$ the rotating-frame balance gives $\mathbf F_{\rm real}/m=-\mathbf a_{\rm cf}=-\omega^2\boldsymbol\rho$ — equal magnitude $\omega^2\rho$, opposite direction.

**Solution.** A bead held fixed on the turntable has $\mathbf v_{\rm rot}=0$ and $\mathbf a_{\rm rot}=0$, so the Coriolis term ($\propto\mathbf v_{\rm rot}$) vanishes and the rotating-frame Newton law reads
$$0=\frac{\mathbf F_{\rm real}}{m}+\mathbf a_{\rm cf}\ \Longrightarrow\ \frac{\mathbf F_{\rm real}}{m}=-\mathbf a_{\rm cf}=-\omega^2\boldsymbol\rho.$$
The real force is thus inward with magnitude $\omega^2\rho$ — precisely the centripetal acceleration an inertial observer needs to hold the bead on its circle, so the two are equal and opposite. For $\boldsymbol\omega=1.5\hat{\mathbf z},\ \mathbf r=(2,0,0)$: `centrifugal_acceleration` $=(4.5,0,0)$ (outward) while the centripetal is $-\omega^2\mathbf r=(-4.5,0,0)$, as the check compares.
