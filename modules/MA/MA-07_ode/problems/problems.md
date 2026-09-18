# MA-07 — Problems

Work by hand, then check with `code/ode.py`. Citations in `../refs.md`.

### P1.  Exponential growth/decay  *(Boas 3e §8.2–8.3, pp.395–401)*
Solve y′ = ky analytically (y = y₀e^{kt}), then integrate numerically and compare
at t = 1 for k = 1 and k = −2. *Check:* `integrate(lambda t,y:[k*y[0]], [1.0], 0, 1, 1000)`
vs `exp(k)`.

**Solution.** The equation $y'=ky$ is separable: $\frac{dy}{y}=k\,dt$. Integrating both sides,
$\ln y = kt + C$, so $y=y_0e^{kt}$ — exponential growth ($k>0$) or decay ($k<0$). With $y_0=1$,
$$y(1)=e^{k}.$$
For $k=1$: $e^{1}=2.71828183$; for $k=-2$: $e^{-2}=0.13533528$. RK4 over 1000 steps reproduces
both to 8 digits, so `integrate(lambda t,y:[k*y[0]], [1.0], 0, 1, 1000)` matches `exp(k)`.

### P2.  The harmonic oscillator  *(Boas 3e §8.5, p.408)*
Solve y″ + y = 0 with y(0)=1, y′(0)=0 → y = cos t. Reduce to a first-order system
and integrate to t = 2π; confirm y(2π)=1, y′(2π)=0. *Check:*
`integrate(second_order_system(lambda t,y,v:-y), [1,0], 0, 2*pi, 4000)`.

**Solution.** The characteristic equation $\lambda^2+1=0$ gives $\lambda=\pm i$, so
$y=A\cos t+B\sin t$. The conditions $y(0)=1\Rightarrow A=1$ and $y'(0)=0\Rightarrow B=0$ leave
$y=\cos t$. Setting $v=y'$ reduces the equation to the first-order system
$$\frac{d}{dt}\begin{pmatrix}y\\ v\end{pmatrix}=\begin{pmatrix}v\\ -y\end{pmatrix},$$
which is exactly what `second_order_system` builds. At $t=2\pi$, $y=\cos2\pi=1$ and
$y'=-\sin2\pi=0$ — the integration returns $y(2\pi)=1.000000$, $y'(2\pi)=0.000000$.

### P3.  Damping regimes  *(Boas 3e §8.5, p.408)*
For y″ + b y′ + y = 0, find b for which the roots of λ²+bλ+1=0 are real (over-damped),
equal (critical, b=2), or complex (under-damped). Integrate b=0.4 and watch it
ring down. *Check:* `second_order_system(lambda t,y,v: -0.4*v - y)`.

**Solution.** Trying $y=e^{\lambda t}$ gives the characteristic equation $\lambda^2+b\lambda+1=0$,
with roots $\lambda=\tfrac{-b\pm\sqrt{b^2-4}}{2}$. The discriminant $b^2-4$ sets the regime
(taking $b>0$): **real distinct** roots — over-damped — for $b>2$; a **repeated** root
$\lambda=-1$ — critically damped — at $b=2$; **complex** roots — under-damped — for $0<b<2$.
With $b=0.4$, $\lambda=-0.2\pm i\sqrt{0.96}$, a decaying oscillation $e^{-0.2t}\cos(\sqrt{0.96}\,t-\phi)$.
Integrating to $t=20$ it rings down to $y(20)=0.015985$, confirming the under-damped envelope.

### P4.  Resonance  *(Boas 3e §8.6, p.417)*
For y″ + ω₀²y = cos(ωt), show the amplitude blows up as ω→ω₀. Integrate near and
off resonance and compare the growth. *Check:* drive term in the RHS of `integrate`.

**Solution.** Seek a particular solution $y_p=C\cos(\omega t)$ of $y''+\omega_0^2y=\cos(\omega t)$;
substituting gives $(\omega_0^2-\omega^2)C=1$, so
$$y_p=\frac{\cos(\omega t)}{\omega_0^2-\omega^2},$$
whose amplitude $1/|\omega_0^2-\omega^2|\to\infty$ as $\omega\to\omega_0$. At exact resonance this
ansatz fails and the solution is secular, $y_p=\dfrac{t\sin(\omega_0 t)}{2\omega_0}$, growing
**linearly** in $t$. With $\omega_0=1$ and zero initial data, integrating to $t=40$ gives
$\max|y|\approx19.6$ on resonance ($\omega=1$, the $\sim t/2$ ramp) versus only $\approx1.6$ off
resonance ($\omega=1.5$, bounded beats of amplitude $\sim2/|1-\omega^2|$) — adding the drive term
to the RHS makes the blow-up plain.

### P5.  Linear system via eigenvalues  *(Boas 3e §8.5, p.408; bridge to `~MA-04`, `~CM-16`)*
For dx/dt = A x with A = [[0,1],[1,0]] (symmetric), diagonalize and write
x(t) = Σ(vᵢ·x₀)e^{λᵢt}vᵢ; show x₀=(1,0) gives (cosh t, sinh t). *Check:*
`linear_evolve_symmetric(A, [1,0], t)` vs `integrate(linear_rhs(A), [1,0], 0, t, 3000)`.

**Solution.** The symmetric matrix $A=\begin{pmatrix}0&1\\1&0\end{pmatrix}$ has eigenvalues $\lambda_\pm=\pm1$ with orthonormal eigenvectors $\mathbf v_\pm=\tfrac1{\sqrt2}(1,\pm1)$. Projecting the initial data, $\mathbf v_\pm\!\cdot\!\mathbf x_0=\tfrac1{\sqrt2}$ for $\mathbf x_0=(1,0)$, and each eigen-mode evolves independently as $e^{\lambda_i t}$:
$$\mathbf x(t)=\sum_i(\mathbf v_i\!\cdot\!\mathbf x_0)\,e^{\lambda_i t}\,\mathbf v_i=\tfrac12 e^{t}(1,1)+\tfrac12 e^{-t}(1,-1)=\big(\tfrac12(e^{t}{+}e^{-t}),\,\tfrac12(e^{t}{-}e^{-t})\big)=(\cosh t,\,\sinh t).$$
Diagonalization decouples the system into two scalar exponentials. At $t=0.7$, $(\cosh0.7,\sinh0.7)=(1.255169,0.758584)$, and `linear_evolve_symmetric(A, [1,0], 0.7)` reproduces this, matching `integrate(linear_rhs(A), [1,0], 0, t, 3000)` to all six digits.
