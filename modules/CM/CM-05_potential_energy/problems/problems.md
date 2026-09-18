# CM-05 — Problems

Work by hand, then check with `code/potential_energy.py`. Citations in `../refs.md`.

### P1.  Force from a potential  *(Fowles 7e §4.2, p.151)*
For U = ½k r² show **F** = −∇U = −k**r** (an isotropic spring). *Check:*
`force_from_potential(lambda x,y,z: 0.5*k*(x*x+y*y+z*z))`.

**Solution.** Write $U=\tfrac12 k r^2=\tfrac12 k(x^2+y^2+z^2)$ and take the gradient componentwise: $\partial_x U=kx$, $\partial_y U=ky$, $\partial_z U=kz$, i.e. $\nabla U=k(x,y,z)=k\mathbf r$. Therefore
$$\mathbf F=-\nabla U=-k\mathbf r,$$
an isotropic Hooke's-law spring pulling toward the origin with magnitude $kr$. For $k=3$ at $(1,2,3)$ this is $(-3,-6,-9)=-k\mathbf r$, exactly what `force_from_potential(lambda x,y,z: 0.5*k*(x*x+y*y+z*z))` returns.

### P2.  Conservative vs rotational  *(Fowles 7e §4.1, p.146)*
Show **F** = −k**r** has zero curl (conservative) while **F** = (−y, x, 0) has
curl (0,0,2) (not conservative). *Check:* `is_conservative`.

**Solution.** For $\mathbf F=-k\mathbf r=(-kx,-ky,-kz)$ each component depends only on its own coordinate, so every cross-partial in the curl vanishes and $\nabla\times\mathbf F=\mathbf 0$ — conservative. For $\mathbf F=(-y,x,0)$,
$$\nabla\times\mathbf F=\big(\partial_y 0-\partial_z x,\ \partial_z(-y)-\partial_x 0,\ \partial_x x-\partial_y(-y)\big)=(0,0,2)\neq\mathbf 0,$$
so it circulates and is not conservative. Accordingly `is_conservative` returns `True` for $-k\mathbf r$ and `False` for $(-y,x,0)$.

### P3.  Energy conservation for the oscillator  *(Fowles 7e §4.2, p.152)*
For x(t) = A cos(ωt), ω = √(k/m), show E = T + U = ½kA² is constant. *Check:*
`total_energy(m, v(t), U, r(t))` at several t.

**Solution.** With $x(t)=A\cos\omega t$ and $\omega=\sqrt{k/m}$ (so $m\omega^2=k$), the velocity is $\dot x=-A\omega\sin\omega t$. Then
$$T=\tfrac12 m\dot x^2=\tfrac12 kA^2\sin^2\omega t,\qquad U=\tfrac12 kx^2=\tfrac12 kA^2\cos^2\omega t.$$
Adding and using $\sin^2+\cos^2=1$, $E=T+U=\tfrac12 kA^2$, independent of $t$. For $k=4,\ A=1$ this is $E=2$, and `total_energy(m, v(t), U, r(t))` returns $2.0$ at every sampled time.

### P4.  Stability of a double well  *(Fowles 7e §2.3, p.63)*
For U = x⁴ − 2x² find the equilibria and classify them. *Answer:* minima at x=±1
(stable), maximum at x=0 (unstable). *Check:* `is_equilibrium`, `is_stable`.

**Solution.** Equilibria satisfy $U'(x)=0$. With $U=x^4-2x^2$,
$$U'(x)=4x^3-4x=4x(x^2-1)=0\ \Longrightarrow\ x=0,\ \pm1.$$
Classify with $U''(x)=12x^2-4$: $U''(\pm1)=8>0$ (minima, **stable**) and $U''(0)=-4<0$ (maximum, **unstable**). So $x=\pm1$ are stable wells and $x=0$ an unstable hilltop, matching `is_equilibrium` (`True` at all three) and `is_stable` (`True, False, True` at $-1,0,1$).

### P5.  Small oscillations  *(→ `~CM-15`)*
Expand U about a stable minimum x₀: U ≈ U(x₀) + ½U″(x₀)(x−x₀)². Identify the
effective spring constant k = U″(x₀) and the frequency ω = √(k/m).

**Solution.** At a stable minimum $x_0$ the force vanishes, $U'(x_0)=0$, so the Taylor expansion has no linear term:
$$U(x)\approx U(x_0)+\tfrac12 U''(x_0)(x-x_0)^2.$$
This is the harmonic potential $\tfrac12 k(x-x_0)^2$ with effective spring constant $k=U''(x_0)>0$; the force $F=-U'(x)\approx-k(x-x_0)$ is restoring, and $m\ddot x=-k(x-x_0)$ is simple harmonic motion at $\omega=\sqrt{k/m}=\sqrt{U''(x_0)/m}$. For the double well at $x_0=1$, $k=U''(1)=8$, so $\omega=\sqrt{8/m}$ — the bridge to `~CM-15`.
