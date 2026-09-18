# CM-14 — Problems

Work by hand, then check with `code/euler_equations.py`. Citations in `../refs.md`.

### P1.  Conservation in torque-free motion  *(Fowles 7e §9.4, p.383)*
Show that with **N** = 0, both |**L**|² = Σ(I_iω_i)² and T = ½ΣI_iω_i² are
constant. *Check:* `L_magnitude_sq` and `rotational_energy` along `integrate_euler`.
*Answer:* both are constants of the torque-free motion; numerically $|\mathbf L|^2=14$ and $T=3$ stay fixed.

**Solution.** Torque-free Euler is $I_i\dot\omega_i=(I_j-I_k)\omega_j\omega_k$ (cyclic $ijk$). Differentiating $|\mathbf L|^2=\sum_i (I_i\omega_i)^2$,
$$\frac{d|\mathbf L|^2}{dt}=2\sum_i (I_i\omega_i)(I_i\dot\omega_i)=2\,\omega_1\omega_2\omega_3\big[I_1(I_2-I_3)+I_2(I_3-I_1)+I_3(I_1-I_2)\big]=0,$$
since the bracket cancels term by term. For the energy $T=\tfrac12\sum_i I_i\omega_i^2$,
$$\frac{dT}{dt}=\sum_i \omega_i\,(I_i\dot\omega_i)=\omega_1\omega_2\omega_3\big[(I_2-I_3)+(I_3-I_1)+(I_1-I_2)\big]=0.$$
Both rates vanish identically, so $|\mathbf L|^2$ and $T$ are conserved — exactly as `integrate_euler` ($I=1,2,3$, $\omega_0=1,1,1$) shows, holding $|\mathbf L|^2$ at $14.000$ and $T$ at $3.000$.

### P2.  Steady spin about a principal axis  *(Fowles 7e §9.3, p.381)*
Show ω = ω₀ **ê_k** (along a principal axis) is a fixed point of Euler's equations.
*Check:* integrate from (ω₀,0,0), (0,ω₀,0), (0,0,ω₀) — each stays put.
*Answer:* yes — a pure principal-axis spin is a fixed point, $\dot{\boldsymbol\omega}=0$.

**Solution.** Put $\boldsymbol\omega=(\omega_0,0,0)$ into Euler's equations:
$$I_1\dot\omega_1=(I_2-I_3)\,0\cdot0=0,\quad I_2\dot\omega_2=(I_3-I_1)\,0\cdot\omega_0=0,\quad I_3\dot\omega_3=(I_1-I_2)\,\omega_0\cdot0=0.$$
Every right-hand side is a product of the two *other* components, and a single-axis spin has only one nonzero component, so all three vanish and $\dot{\boldsymbol\omega}=0$ — a fixed point. The same holds for $\hat e_2$ and $\hat e_3$. Hence integrating from $(\omega_0,0,0)$, $(0,\omega_0,0)$, $(0,0,\omega_0)$ each stays put, as the steady-rotation test confirms.

### P3.  Tennis-racket theorem  *(Marion & Thornton 5e §11.9, p.444)*
Argue from Euler's equations that spin about the intermediate axis is unstable
while spin about the largest/smallest is stable. *(Perturb ω slightly off each
axis and watch the growth/oscillation.)*
*Answer:* stable about the largest and smallest axes (bounded oscillation), unstable about the intermediate one (exponential growth).

**Solution.** Spin about axis 1 with a small transverse perturbation, $\boldsymbol\omega=(\Omega,\eta_2,\eta_3)$. To first order $\dot\omega_1=O(\eta^2)$, so $\Omega$ is constant and
$$I_2\dot\eta_2=(I_3-I_1)\Omega\,\eta_3,\qquad I_3\dot\eta_3=(I_1-I_2)\Omega\,\eta_2.$$
Differentiating the first and substituting the second gives $\ddot\eta_2=\big[(I_3-I_1)(I_1-I_2)/(I_2I_3)\big]\Omega^2\,\eta_2$. If axis 1 is the largest or smallest moment the two factors have opposite signs, the coefficient is negative, and $\eta_2$ *oscillates* (stable). If axis 1 is the intermediate moment the factors share a sign, the coefficient is positive, and $\eta_2\propto e^{\sigma t}$ grows (unstable). With $I=(1,2,3)$, perturbing the intermediate axis $\hat e_2$ blows up in `integrate_euler`, while $\hat e_1,\hat e_3$ merely wobble.

### P4.  Symmetric-top precession  *(Fowles 7e §9.5, p.384)*
For I₁ = I₂ show ω₃ is constant and (ω₁,ω₂) rotate at Ω = (I₃−I₁)/I₁·ω₃.
*Check:* `precession_rate(1,2,3)` and that ω₁²+ω₂² is constant in `integrate_euler`.
*Answer:* $\omega_3$ is constant and $(\omega_1,\omega_2)$ circles at $\Omega=(I_3-I_1)\omega_3/I_1$; e.g. `precession_rate(1,2,3)`$=3$.

**Solution.** With $I_1=I_2$ the third Euler equation is $I_3\dot\omega_3=(I_1-I_2)\omega_1\omega_2=0$, so $\omega_3$ is constant. The first two become
$$\dot\omega_1=-\Omega\,\omega_2,\qquad \dot\omega_2=+\Omega\,\omega_1,\qquad \Omega\equiv\frac{I_3-I_1}{I_1}\,\omega_3.$$
Writing $\zeta=\omega_1+i\omega_2$ gives $\dot\zeta=i\Omega\zeta$, hence $\zeta=\zeta_0e^{i\Omega t}$: the transverse vector rotates at the steady rate $\Omega$ and $\omega_1^2+\omega_2^2=|\zeta|^2$ is constant. For $I=(1,1,2)$, $\omega_3=3$ this gives $\Omega=(2-1)/1\cdot3=3$, matching `precession_rate(1,2,3)`$=3.0$ and the conserved $\omega_1^2+\omega_2^2=0.25$ in `integrate_euler`.

### P5.  The free Earth wobble
The Earth is a slightly oblate symmetric top; estimate its free-precession
("Chandler wobble") period from Ω with (I₃−I₁)/I₁ ≈ 1/305. *(A back-of-envelope
application of `precession_rate`.)*
*Answer:* a free-precession period $T\approx305$ days ($\sim10$ months); the observed Chandler wobble ($\sim433$ d) runs longer because the Earth is not perfectly rigid.

**Solution.** From the symmetric-top result the body-frame precession rate is $\Omega=\dfrac{I_3-I_1}{I_1}\,\omega_3$ with $\omega_3$ the spin (one turn per day). The wobble period is
$$T=\frac{2\pi}{\Omega}=\frac{I_1}{I_3-I_1}\cdot\frac{2\pi}{\omega_3}\approx 305\times(1\ \text{day})\approx 305\ \text{days}.$$
So the spin axis traces a small circle about the figure axis roughly every ten months — feeding $(I_1,I_3)=(305,306)$ to `precession_rate` returns the same $\Omega=\omega_3/305$. The measured Chandler period is $\sim433$ days; the $\sim40\%$ excess is the fingerprint of Earth's elastic (non-rigid) response, but the rigid-body estimate nails the order of magnitude.
