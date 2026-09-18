# MA-06 — Problems

Work by hand, then check with `code/complex_analysis.py`. Citations in `../refs.md`.

### P1.  Test analyticity  *(Boas 3e §14.2, p.667)*
Use Cauchy–Riemann to show f(z)=z² is analytic everywhere but f(z)=z̄ is nowhere
analytic. *Check:* `cauchy_riemann(lambda z: z*z, ...)` (True) vs
`cauchy_riemann(lambda z: z.conjugate(), ...)` (False).

**Solution.** Write $z=x+iy$ and split each map into $f=u+iv$. For $f(z)=z^2=(x^2-y^2)+i\,(2xy)$ we read off $u=x^2-y^2,\ v=2xy$, so
$$u_x=2x=v_y,\qquad u_y=-2y=-v_x,$$
and both Cauchy–Riemann equations hold for every $(x,y)$ — $z^2$ is analytic everywhere. For $f(z)=\bar z=x-iy$ we have $u=x,\ v=-y$, giving $u_x=1$ but $v_y=-1$, so $u_x\neq v_y$ at **every** point and C–R fails identically: $\bar z$ is nowhere analytic. This is why `cauchy_riemann(lambda z: z*z, ...)` returns `True` while `cauchy_riemann(lambda z: z.conjugate(), ...)` returns `False`.

### P2.  ∮ dz/z = 2πi  *(Boas 3e §14.3, p.674)*
Parametrize the unit circle z=e^{iθ} and evaluate ∮ dz/z directly; then show
∮ zⁿ dz = 0 for every other integer n. *Check:* `contour_integral(lambda z: 1/z,
circle(0,1), 0, 2*pi)` ≈ 2πi; `contour_integral(lambda z: z*z, ...)` ≈ 0.

**Solution.** Parametrize the unit circle as $z=e^{i\theta}$, $\theta\in[0,2\pi]$, so $dz=ie^{i\theta}\,d\theta$. Then
$$\oint\frac{dz}{z}=\int_0^{2\pi}\frac{ie^{i\theta}}{e^{i\theta}}\,d\theta=\int_0^{2\pi} i\,d\theta=2\pi i.$$
For any other integer $n\neq-1$,
$$\oint z^n\,dz=\int_0^{2\pi}e^{in\theta}\,ie^{i\theta}\,d\theta=i\int_0^{2\pi}e^{i(n+1)\theta}\,d\theta=\frac{e^{i(n+1)2\pi}-1}{n+1}=0,$$
since $e^{i(n+1)2\pi}=1$. Only the $n=-1$ term survives — the source of every residue. Numerically `contour_integral(1/z,…)` $\approx 6.2832\,i=2\pi i$ and `contour_integral(z*z,…)` $\approx 0$.

### P3.  Cauchy's integral formula  *(Boas 3e §14.3 Thm VI, p.675)*
Verify f(0) = (1/2πi)∮ eᶻ/z dz around the unit circle equals e⁰ = 1.
*Check:* `cauchy_integral_formula(cmath.exp, 0)` ≈ 1.

**Solution.** Cauchy's integral formula says that for $f$ analytic inside the loop, $f(z_0)=\dfrac{1}{2\pi i}\oint\dfrac{f(z)}{z-z_0}\,dz$. Take $f(z)=e^z$ (entire, hence analytic inside the unit circle) and $z_0=0$:
$$\frac{1}{2\pi i}\oint\frac{e^z}{z}\,dz=f(0)=e^0=1.$$
The boundary integral reproduces the interior value at the centre — the analytic mean-value property. `cauchy_integral_formula(cmath.exp, 0)` returns $\approx 1.0000000009$, the $10^{-9}$ residual being the trapezoidal discretization error, confirming the formula.

### P4.  Residues  *(Boas 3e §14.5, p.682)*
Find the residues of 1/(z²+1) at z=±i and confirm Res = ±1/2i. Then check the
residue theorem: ∮ around \|z\|=2 (enclosing both) = 2πi·(sum) = 0.
*Check:* `residue_at(lambda z: 1/(z*z+1), 1j)` ≈ −0.5j.

**Solution.** Factor $\dfrac{1}{z^2+1}=\dfrac{1}{(z-i)(z+i)}$; both poles are simple, so $\operatorname{Res}_{z_0}f=\lim_{z\to z_0}(z-z_0)f(z)$ gives
$$\operatorname{Res}_{i}=\frac{1}{i+i}=\frac{1}{2i}=-\tfrac12 i,\qquad
\operatorname{Res}_{-i}=\frac{1}{-i-i}=\frac{1}{-2i}=+\tfrac12 i.$$
The two residues sum to zero, so by the residue theorem $\oint_{|z|=2}\dfrac{dz}{z^2+1}=2\pi i\,(-\tfrac12 i+\tfrac12 i)=0$. The code confirms `residue_at(lambda z: 1/(z*z+1), 1j)` $\approx -0.5j$ (and $+0.5j$ at $-i$), i.e. $\pm 1/2i$.

### P5.  A real integral by residues  *(Boas 3e §14.7, contour methods)*
The residue theorem gives ∫_{−∞}^{∞} dx/(1+x²) = π (close the contour in the
upper half-plane; only the pole at z=i contributes, residue 1/2i, so 2πi·(1/2i)=π).
*Check:* compare to `2*pi*residue_at(lambda z: 1/(z*z+1), 1j) * 1j` → π.

**Solution.** Close the real axis with a large semicircle of radius $R$ in the upper half-plane. On the arc $|f|\sim R^{-2}$ while its length is $\sim\pi R$, so that contribution $\to 0$ as $R\to\infty$ and the closed-contour integral equals the real-line integral. Only the pole $z=i$ lies inside, with $\operatorname{Res}_i\dfrac{1}{z^2+1}=\dfrac{1}{2i}$, so
$$\int_{-\infty}^{\infty}\frac{dx}{1+x^2}=2\pi i\cdot\frac{1}{2i}=\pi.$$
The check `2*pi*residue_at(…,1j)*1j` assembles $2\pi i\cdot\operatorname{Res}_i$ (the extra `1j` supplies the $i$ of $2\pi i$), returning $\approx 3.14159=\pi$.
