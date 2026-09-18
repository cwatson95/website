# CM-08 — Problems

Work by hand, then check with `code/collisions.py`. Citations in `../refs.md`.

### P1.  Elastic collision conserves p and T  *(Fowles 7e §7.5, p.303)*
Derive the 1-D elastic final velocities and verify both momentum and kinetic
energy are conserved. *Check:* `elastic_collision_1d` for several mass ratios.

**Solution.** Momentum and kinetic-energy conservation read $m_1v_1+m_2v_2=m_1v_1'+m_2v_2'$ and $m_1v_1^2+m_2v_2^2=m_1v_1'^2+m_2v_2'^2$. Writing each as $m_1(v_1-v_1')=m_2(v_2'-v_2)$ and $m_1(v_1^2-v_1'^2)=m_2(v_2'^2-v_2^2)$ and dividing gives $v_1+v_1'=v_2+v_2'$, i.e. the **relative velocity reverses**, $v_1'-v_2'=-(v_1-v_2)$. Solving this together with momentum conservation,
$$v_1'=\frac{(m_1-m_2)v_1+2m_2v_2}{m_1+m_2},\qquad v_2'=\frac{(m_2-m_1)v_2+2m_1v_1}{m_1+m_2}.$$
Substituting back confirms both $p$ and $T$ are unchanged, which is what `elastic_collision_1d` returns for every mass ratio (e.g. a light ball off a wall, $m_2\to\infty$, gives $v_1'\to-v_1$).

### P2.  Equal masses exchange velocities  *(Marion & Thornton 5e §9.6, p.345)*
Show m₁ = m₂ gives v₁′ = v₂, v₂′ = v₁. *Check:* `elastic_collision_1d(2,5,2,-1)` → (−1,5).

**Solution.** Put $m_1=m_2=m$ in the elastic formulas; the differences $m_1-m_2$ and $m_2-m_1$ vanish, leaving
$$v_1'=\frac{2m\,v_2}{2m}=v_2,\qquad v_2'=\frac{2m\,v_1}{2m}=v_1.$$
So equal masses simply **exchange** velocities. With $m_1=m_2=2$, $v_1=5$, $v_2=-1$ this gives $v_1'=-1$, $v_2'=5$, i.e. `elastic_collision_1d(2,5,2,-1)` $\to(-1,5)$.

### P3.  Inelastic collision  *(Marion & Thornton 5e §9.8, p.358)*
Show the common final velocity is the CM velocity and that kinetic energy is lost.
*Check:* `inelastic_collision(2,[4,0,0],1,[0,0,0])` and compare T before/after.

**Solution.** Sticking means a single final velocity $v'$; momentum conservation $(m_1+m_2)v'=m_1v_1+m_2v_2$ gives
$$v'=\frac{m_1v_1+m_2v_2}{m_1+m_2}=v_\text{cm},$$
exactly the centre-of-mass velocity (`~CM-07`). The kinetic energy drops by $T_i-T_f=\tfrac12\mu(v_1-v_2)^2$ with reduced mass $\mu=m_1m_2/(m_1+m_2)$. For $m=[2,1]$, $v_1=4$, $v_2=0$: $v'=8/3\approx2.667=v_\text{cm}$, and $T_i=16\to T_f=\tfrac12(3)(8/3)^2=32/3$, a loss of $16/3\approx5.333$ — matching `inelastic_collision(2,[4,0,0],1,[0,0,0])` and the before/after kinetic energies.

### P4.  Rutherford angle ↔ impact parameter  *(Fowles 7e §6.14, p.264)*
Invert θ = 2 arctan(k/2Eb) to b = (k/2E)cot(θ/2); for b = k/2E show θ = 90°.
*Check:* `rutherford_angle(0.5, 1, 1)` → π/2 and the inverse relation.

**Solution.** Halving and taking the tangent of $\theta=2\arctan\!\frac{k}{2Eb}$ gives $\tan\frac\theta2=\frac{k}{2Eb}$, so
$$b=\frac{k}{2E\tan(\theta/2)}=\frac{k}{2E}\cot\frac\theta2.$$
At the special value $b=k/2E$ this forces $\tan(\theta/2)=1$, i.e. $\theta/2=45^\circ$ and $\boxed{\theta=90^\circ}$. With $k=E=1$ and $b=0.5=k/2E$, `rutherford_angle(0.5, 1, 1)` returns $\pi/2$, confirming the inverse relation.

### P5.  Forward divergence of the cross-section  *(Goldstein 3e §3.10, p.110)*
Show dσ/dΩ = (k/4E)²/sin⁴(θ/2) → ∞ as θ → 0, and explain why (the Coulomb force has
infinite range, so even far-off particles deflect a little). *Check:*
`rutherford_cross_section(small, E, k)` grows without bound.

**Solution.** As $\theta\to0$, $\sin(\theta/2)\approx\theta/2\to0$, so
$$\frac{d\sigma}{d\Omega}=\Big(\frac{k}{4E}\Big)^2\frac{1}{\sin^4(\theta/2)}\sim\Big(\frac{k}{4E}\Big)^2\frac{16}{\theta^4}\longrightarrow\infty.$$
Physically the Coulomb force $\propto1/r^2$ has **infinite range**: particles incident at arbitrarily large impact parameter are still deflected by a small angle, and since $b=(k/2E)\cot(\theta/2)\to\infty$ as $\theta\to0$, an unbounded range of $b$ piles up into the forward direction. Hence `rutherford_cross_section(small, E, k)` grows without bound (e.g. $\approx1.08\times10^7$ at $\theta=1^\circ$ versus $0.25$ at $90^\circ$).
