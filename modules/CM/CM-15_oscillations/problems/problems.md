# CM-15 — Problems

Work by hand, then check with `code/oscillations.py`. Citations in `../refs.md`.

### P1.  Simple harmonic motion  *(Fowles 7e §3.2, p.84)*
Solve x″ + ω₀²x = 0 and confirm the period is 2π/ω₀, independent of amplitude.
*Check:* `integrate_oscillator(omega0, 0, 1, 0, …)` vs cos(ω₀t).
*Answer:* $x(t)=C\cos(\omega_0 t+\varphi)$ with period $T=2\pi/\omega_0$, independent of amplitude.

**Solution.** The equation $x''+\omega_0^2x=0$ is linear with constant coefficients; the trial $x=e^{rt}$ gives the characteristic equation $r^2+\omega_0^2=0$, so $r=\pm i\omega_0$ and
$$x(t)=A\cos\omega_0 t+B\sin\omega_0 t=C\cos(\omega_0 t+\varphi).$$
The motion repeats when the phase advances by $2\pi$, i.e. $\omega_0 T=2\pi\Rightarrow T=2\pi/\omega_0$ — set purely by $\omega_0$, with no dependence on the amplitude $C$ (the equation is linear). The data $x(0)=1,\ x'(0)=0$ fix $A=1,B=0$, so $x=\cos\omega_0 t$; the SHM run of `integrate_oscillator` then returns $x(\pi)=1.00000=\cos2\pi$.

### P2.  Underdamped envelope  *(Fowles 7e §3.4, p.96; Marion & Thornton 5e §3.5, p.108)*
Show the free underdamped response is e^{−γt}[cos ω_d t + (γ/ω_d) sin ω_d t] with
ω_d = √(ω₀²−γ²). *Check:* `underdamped_solution` vs `integrate_oscillator`.
*Answer:* $x(t)=e^{-\gamma t}\big[\cos\omega_d t+(\gamma/\omega_d)\sin\omega_d t\big]$ with $\omega_d=\sqrt{\omega_0^2-\gamma^2}$.

**Solution.** For $x''+2\gamma x'+\omega_0^2x=0$ the trial $x=e^{rt}$ gives $r^2+2\gamma r+\omega_0^2=0$, hence
$$r=-\gamma\pm\sqrt{\gamma^2-\omega_0^2}=-\gamma\pm i\omega_d,\qquad \omega_d=\sqrt{\omega_0^2-\gamma^2},$$
real-oscillatory when $\gamma<\omega_0$. So $x=e^{-\gamma t}(A\cos\omega_d t+B\sin\omega_d t)$. Imposing $x(0)=1$ gives $A=1$, and $x'(0)=0=-\gamma A+\omega_d B$ gives $B=\gamma/\omega_d$, so $x(t)=e^{-\gamma t}[\cos\omega_d t+(\gamma/\omega_d)\sin\omega_d t]$ — precisely `underdamped_solution`, which tracks `integrate_oscillator` to $\sim10^{-4}$ (e.g. $\omega_d=1.98997$ for $\omega_0=2,\gamma=0.2$).

### P3.  Quality factor  *(Fowles 7e §3.6, p.113)*
Show Q = ω₀/(2γ) and that the energy decays as e^{−2γt}. *Check:* energy ratio in
`integrate_oscillator`; `quality_factor`.
*Answer:* $E\propto e^{-2\gamma t}$ and $Q=\omega_0/(2\gamma)$; e.g. `quality_factor(2,0.2)`$=5$.

**Solution.** The free underdamped motion sits inside the envelope $e^{-\gamma t}$, so the energy, quadratic in amplitude, decays at twice the rate:
$$E(t)=\tfrac12\dot x^2+\tfrac12\omega_0^2x^2\ \propto\ \big(e^{-\gamma t}\big)^2=e^{-2\gamma t}.$$
The fractional energy lost per radian of oscillation is $\dfrac{-\dot E}{\omega_0 E}=\dfrac{2\gamma}{\omega_0}\equiv\dfrac1Q$, so $Q=\omega_0/(2\gamma)$. Thus `quality_factor(2,0.2)`$=5.000$, and over $t=10$ at $\gamma=0.3$ the energy ratio is $\approx e^{-2\gamma t}=e^{-6}\approx0.0025$, well under the $5\%$ the decay test requires.

### P4.  Resonance curve  *(Fowles 7e §3.6, p.113; Marion & Thornton 5e §3.6, p.117)*
Derive A(ω) = F₀/√((ω₀²−ω²)²+(2γω)²) and show it peaks at √(ω₀²−2γ²).
*Check:* `driven_amplitude` vs the steady-state amplitude from `integrate_oscillator`.
*Answer:* $A(\omega)=F_0/\sqrt{(\omega_0^2-\omega^2)^2+(2\gamma\omega)^2}$, peaking at $\omega=\sqrt{\omega_0^2-2\gamma^2}$.

**Solution.** Seek the steady state of $x''+2\gamma x'+\omega_0^2x=F_0\cos\omega t$ as $x=\mathrm{Re}\,[X e^{i\omega t}]$. Substituting,
$$(-\omega^2+2i\gamma\omega+\omega_0^2)X=F_0\ \Rightarrow\ A(\omega)=|X|=\frac{F_0}{\sqrt{(\omega_0^2-\omega^2)^2+(2\gamma\omega)^2}}.$$
The peak minimizes the denominator $D(\omega)=(\omega_0^2-\omega^2)^2+(2\gamma\omega)^2$: setting $\tfrac{dD}{d\omega}=-4\omega(\omega_0^2-\omega^2)+8\gamma^2\omega=0$ gives $\omega^2=\omega_0^2-2\gamma^2$, i.e. resonance at $\omega=\sqrt{\omega_0^2-2\gamma^2}$. For $\omega_0=2,\gamma=0.2$, `resonance_frequency`$=1.9799$ and `driven_amplitude(2,0.2,1,1.5)`$=0.5405$ matches the integrator's steady amplitude $0.5405$.

### P5.  Small oscillations from a potential  *(→ `~CM-05`)*
Expand a potential about a minimum and identify ω₀ = √(U″(x₀)/m); apply to the
pendulum (U″ = mgl ⇒ ω₀ = √(g/l)). *(Connects `~CM-05` stability to this module.)*
*Answer:* $\omega_0=\sqrt{U''(x_0)/m}$ (generally $\sqrt{U''/I}$); for the pendulum $\omega_0=\sqrt{g/l}$.

**Solution.** At a minimum $x_0$ we have $U'(x_0)=0$, so the Taylor expansion gives
$$U(x)=U(x_0)+\tfrac12 U''(x_0)(x-x_0)^2+\cdots,\qquad F=-U'\approx -U''(x_0)\,(x-x_0).$$
Then $m\ddot\xi=-U''(x_0)\,\xi$ for $\xi=x-x_0$ — simple harmonic motion with $\omega_0=\sqrt{U''(x_0)/m}$ (a positive $U''$, a genuine minimum, is exactly the `~CM-05` stability condition). For the pendulum $U(\theta)=mgl(1-\cos\theta)$ the curvature is $U''(0)=mgl$ and the inertia is $I=ml^2$, so $\omega_0=\sqrt{U''/I}=\sqrt{mgl/ml^2}=\sqrt{g/l}$ — the $\omega_0$ that feeds every `integrate_oscillator` run in this module.
