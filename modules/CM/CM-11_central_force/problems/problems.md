# CM-11 — Problems

Work by hand, then check with `code/central_force.py`. Citations in `../refs.md`.

### P1.  The effective potential  *(Fowles 7e §6.9, p.251)*
For U = −k/r show U_eff(r) = −k/r + L²/(2μr²) has a single minimum at
r₀ = L²/(μk) — the circular orbit. *Check:* `effective_potential` derivative at
`circular_orbit_radius`.
*Answer:* $r_0=L^2/(\mu k)$; it is a minimum since $U_{\rm eff}''(r_0)=k/r_0^3>0$.

**Solution.** Differentiate $U_{\rm eff}(r)=-\dfrac{k}{r}+\dfrac{L^2}{2\mu r^2}$ and set the slope to zero:
$$U_{\rm eff}'(r)=\frac{k}{r^2}-\frac{L^2}{\mu r^3}=0\ \Longrightarrow\ r_0=\frac{L^2}{\mu k},$$
the only stationary point for $r>0$. Its character follows from the curvature, using $L^2=\mu k r_0$:
$$U_{\rm eff}''(r)=-\frac{2k}{r^3}+\frac{3L^2}{\mu r^4},\qquad U_{\rm eff}''(r_0)=-\frac{2k}{r_0^3}+\frac{3k}{r_0^3}=\frac{k}{r_0^3}>0.$$
So $U_{\rm eff}$ has a single, stable minimum at $r_0$ — the circular orbit. Numerically `effective_potential` has slope $U_{\rm eff}'(r_0)\approx-2.8\times10^{-11}\approx0$ at `circular_orbit_radius`, confirming the extremum.

### P2.  Kepler's third law  *(Fowles 7e §6.3, p.225)*
Show T² = (4π²μ/k) a³, so T²/a³ is the same for every orbit. *Check:*
`kepler_period(a, μ, k)` for several a.
*Answer:* $T^2/a^3=4\pi^2\mu/k$, a constant; for $\mu=k=1$ it is $4\pi^2\approx39.478$.

**Solution.** On a circular orbit of radius $a$ the inward force supplies the centripetal acceleration, $\dfrac{k}{a^2}=\mu\dfrac{v^2}{a}$, so $v^2=\dfrac{k}{\mu a}$. The period is the circumference over the speed,
$$T=\frac{2\pi a}{v}=2\pi a\sqrt{\frac{\mu a}{k}}=2\pi\sqrt{\frac{\mu a^3}{k}}.$$
Squaring gives Kepler III,
$$T^2=\frac{4\pi^2\mu}{k}\,a^3\ \Longrightarrow\ \frac{T^2}{a^3}=\frac{4\pi^2\mu}{k},$$
independent of $a$. With $\mu=k=1$, `kepler_period` returns $T^2/a^3=4\pi^2=39.4784$ for both $a=1$ and $a=4$.

### P3.  Conservation along an orbit  *(Fowles 7e §6.5, p.229)*
Integrate a bound orbit and confirm E = ½μ|v|² + U(r) and L_z = μ(x v_y − y v_x)
are constant. *Check:* compute both along `orbit(...)`.
*Answer:* both are constant — $E$ because a central force does work only through $dr$, and $L_z$ because the torque $\mathbf r\times\mathbf F$ vanishes when $\mathbf F\parallel\hat{\mathbf r}$.

**Solution.** A central force is $\mathbf F=f(r)\hat{\mathbf r}=-\dfrac{dU}{dr}\hat{\mathbf r}$. Differentiating the energy and using $\mu\dot{\mathbf v}=\mathbf F$ and $\mathbf v\cdot\hat{\mathbf r}=\dot r$,
$$\frac{dE}{dt}=\mu\,\mathbf v\!\cdot\!\dot{\mathbf v}+\frac{dU}{dr}\dot r=\mathbf v\!\cdot\!\mathbf F+\frac{dU}{dr}\dot r=-\frac{dU}{dr}\dot r+\frac{dU}{dr}\dot r=0.$$
For angular momentum the torque is $\boldsymbol\tau=\mathbf r\times\mathbf F=f(r)\,(\mathbf r\times\hat{\mathbf r})=0$, so $\dot{\mathbf L}=0$ and $L_z=\mu(x\dot y-y\dot x)$ is fixed. Along the integrated bound orbit ($v=0.8\,v_c$) both $E$ and $L_z$ hold to $\sim10^{-4}$, and $E<0$ confirms a bound ellipse.

### P4.  Circular orbit speed  *(Marion & Thornton 5e Ch.8, p.287)*
For the circular orbit show the speed is v = √(k/(μr₀)) and that starting with
this tangential speed keeps r constant. *Check:* integrate with v = L/(μr₀).
*Answer:* $v=\sqrt{k/(\mu r_0)}=L/(\mu r_0)$; for $k=\mu=r_0=1$ this is $v=1$ and $r$ stays at $1$.

**Solution.** On the circular orbit the acceleration is purely centripetal, $a_r=-v^2/r_0$, and the only radial force is $F_r=-k/r_0^2$. Newton's radial law $\mu a_r=F_r$ gives
$$\mu\frac{v^2}{r_0}=\frac{k}{r_0^2}\ \Longrightarrow\ v=\sqrt{\frac{k}{\mu r_0}}.$$
The motion is tangential, so $L=\mu v r_0$; with $r_0=L^2/(\mu k)$ one checks $v=L/(\mu r_0)=\sqrt{\mu k r_0}/(\mu r_0)=\sqrt{k/(\mu r_0)}$ — the same speed. Launching from $(r_0,0)$ with velocity $(0,v)$ therefore keeps the radius fixed: for $k=\mu=r_0=1$ the integrator holds $r\in[1.0000,1.0000]$.

### P5.  Bound vs unbound  *(Fowles 7e §6.5, p.229)*
Argue from the sign of E whether the orbit is an ellipse (E<0), parabola (E=0),
or hyperbola (E>0). *Check:* integrate orbits with v below/at/above escape speed.
*Answer:* the sign of $E=\tfrac12\mu v^2-k/r$ decides: $E<0$ ellipse, $E=0$ parabola (at $v=v_{\rm esc}=\sqrt{2k/\mu r}$), $E>0$ hyperbola.

**Solution.** Because $U=-k/r\to0$ as $r\to\infty$, the energy far away is $E=\tfrac12\mu v_\infty^2$. The particle can reach infinity only if it still has $v_\infty^2=2E/\mu\ge0$, i.e. $E\ge0$:
$$E<0\ (\text{ellipse}),\qquad E=0\ (\text{parabola}),\qquad E>0\ (\text{hyperbola}).$$
The threshold $E=0$ at radius $r$ defines the escape speed,
$$\tfrac12\mu v_{\rm esc}^2=\frac{k}{r}\ \Longrightarrow\ v_{\rm esc}=\sqrt{\frac{2k}{\mu r}}=\sqrt2\,v_{\rm circ}.$$
Starting at $r=1$ with $\mu=k=1$ ($v_{\rm circ}=1$, $v_{\rm esc}=\sqrt2$): integrating with $v<v_{\rm esc}$ gives $E<0$ (a bound ellipse, as in the conservation test), $v=v_{\rm esc}$ gives $E=0$ (parabola), and $v>v_{\rm esc}$ gives $E>0$ (an escaping hyperbola).
