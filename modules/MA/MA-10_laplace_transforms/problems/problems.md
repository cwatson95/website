# MA-10 — Problems

Work by hand, then check with `code/laplace.py`. Citations in `../refs.md`.

### P1.  Transforms from the definition  *(Boas 3e §8, p.437)*
From F(s)=∫₀^∞ f e^{−st}dt derive L{1}=1/s, L{t}=1/s², L{e^{at}}=1/(s−a), and
L{cos ωt}=s/(s²+ω²). *Check:* `laplace_numeric(lambda t: math.cos(2*t), 3.0).real`
vs `F_cos(2, 3)`.

**Solution.** Each entry is the integral $F(s)=\int_0^\infty f(t)e^{-st}dt$ (Re $s$ large enough):
$$\mathcal L\{1\}=\int_0^\infty e^{-st}dt=\Big[-\tfrac1s e^{-st}\Big]_0^\infty=\tfrac1s,\qquad
\mathcal L\{t\}=\int_0^\infty t\,e^{-st}dt=\tfrac1{s^2}\ \text{(by parts)},$$
$$\mathcal L\{e^{at}\}=\int_0^\infty e^{(a-s)t}dt=\tfrac1{s-a}\ (\text{Re }s>a).$$
For the cosine, write $\cos\omega t=\Re\,e^{i\omega t}$ and use the exponential entry with $a=i\omega$:
$\mathcal L\{e^{i\omega t}\}=\frac1{s-i\omega}=\frac{s+i\omega}{s^2+\omega^2}$, whose real part is $\frac{s}{s^2+\omega^2}$.
At $\omega=2,\,s=3$ this is $3/13\approx0.230769$, exactly what `laplace_numeric(cos 2t,3)` and `F_cos(2,3)` return.

### P2.  The derivative rule and an algebraic identity  *(Boas 3e §8, p.438)*
Show L{f′}=sF(s)−f(0). Apply it to f=sin ωt to get L{ω cos ωt}=ωs/(s²+ω²), and
check it is consistent with the cos-table entry. *Check:*
`laplace_numeric(lambda t: w*math.cos(w*t), s).real` ≈ `s*F_sin(w, s)`.

**Solution.** Integrate by parts, using $f(t)e^{-st}\to0$ as $t\to\infty$:
$$\mathcal L\{f'\}=\int_0^\infty f'(t)e^{-st}dt=\big[f e^{-st}\big]_0^\infty+s\!\int_0^\infty f e^{-st}dt=sF(s)-f(0).$$
Take $f=\sin\omega t$, so $f(0)=0$ and $f'=\omega\cos\omega t$. Then
$\mathcal L\{\omega\cos\omega t\}=s\,\mathcal L\{\sin\omega t\}-0=s\cdot\frac{\omega}{s^2+\omega^2}=\frac{\omega s}{s^2+\omega^2}$,
which is $\omega$ times the cosine table entry $\frac{s}{s^2+\omega^2}$ — consistent. Numerically
`laplace_numeric(w*cos wt, s).real` equals `s*F_sin(w, s)`.

### P3.  Convolution  *(Boas 3e §10, p.445)*
Compute e^{−t}∗e^{−2t} by the integral ∫₀ᵗ e^{−τ}e^{−2(t−τ)}dτ and show it equals
e^{−t}−e^{−2t}. Confirm its transform is 1/[(s+1)(s+2)]. *Check:*
`convolve(lambda t: math.exp(-t), lambda t: math.exp(-2*t), 1.3)`.

**Solution.** Factor the integrand and integrate:
$$\int_0^t e^{-\tau}e^{-2(t-\tau)}d\tau=e^{-2t}\!\int_0^t e^{\tau}d\tau=e^{-2t}(e^{t}-1)=e^{-t}-e^{-2t}.$$
Its transform is $\mathcal L\{e^{-t}\}-\mathcal L\{e^{-2t}\}=\frac1{s+1}-\frac1{s+2}=\frac1{(s+1)(s+2)}$,
which is exactly the product $F(s)G(s)$ of the two transforms — the convolution theorem
$\mathcal L\{f*g\}=F\,G$. At $t=1.3$, $e^{-1.3}-e^{-2.6}=0.198258$, matching
`convolve(...)`.

### P4.  An IVP by Laplace  *(Boas 3e §9, p.440)*
Solve y″+4y=0, y(0)=1, y′(0)=0. Transform to (s²+4)Y=s, so Y=s/(s²+4) and
y=cos 2t. Then redo with damping y″+0.5y′+4y=0 and identify the underdamped
form e^{αt}(C cos βt+D sin βt). *Check:* `solve_ivp_laplace(0.5, 4, 1, 0)` vs
`rk4(0.5, 4, 1, 0, 0, t)`.

**Solution.** Using $\mathcal L\{y''\}=s^2Y-sy(0)-y'(0)$, the undamped problem gives
$(s^2+4)Y=s\Rightarrow Y=\frac{s}{s^2+4}\Rightarrow y=\cos 2t$. With damping,
$(s^2+0.5s+4)Y=(s+0.5)y(0)+y'(0)=s+0.5$, so $Y=\dfrac{s+0.5}{s^2+0.5s+4}$. The denominator's
roots are $\alpha\pm i\beta$ with $\alpha=-\tfrac{0.5}{2}=-0.25$ and $\beta=\tfrac12\sqrt{4\cdot4-0.5^2}=1.9843$,
giving the underdamped response
$$y=e^{-0.25t}\Big(\cos\beta t+\tfrac{0.5+1\cdot(-0.25)}{\beta}\sin\beta t\Big)=e^{-0.25t}\big(\cos\beta t+0.126\sin\beta t\big).$$
`solve_ivp_laplace(0.5, 4, 1, 0)` reproduces this and agrees with `rk4(...)` to ~1e-4.

### P5.  Step response & steady state  *(Boas 3e §9, p.442)*
Solve y″+0.5y′+4y=3, y(0)=y′(0)=0. Show Y=3/[s(s²+0.5s+4)], that the s=0 pole
gives the steady state y_p=3/4, and the quadratic poles give the decaying
transient. *Check:* `solve_ivp_laplace(0.5, 4, 0, 0, F0=3)`; `y(20)` ≈ 0.75.

**Solution.** With zero initial data and forcing $\mathcal L\{3\}=3/s$,
$(s^2+0.5s+4)Y=3/s\Rightarrow Y=\dfrac{3}{s\,(s^2+0.5s+4)}$. Partial fractions split this into
the $s=0$ pole and the quadratic poles:
$$Y=\frac{A}{s}+\frac{Bs+C}{s^2+0.5s+4},\qquad A=\frac{3}{s^2+0.5s+4}\Big|_{s=0}=\frac{3}{4}.$$
The $A/s$ term inverts to the constant **steady state** $y_p=3/4$; the quadratic poles
$\alpha\pm i\beta$ ($\alpha=-0.25<0$) invert to a **decaying** transient $e^{-0.25t}(\dots)$ that dies
out. Hence $y(t)\to 3/4$, and `solve_ivp_laplace(0.5, 4, 0, 0, F0=3)` gives $y(20)=0.7515\approx0.75$.

### P6.  Repeated-root (critical damping)  *(Boas 3e §9, p.440; Table p.469)*
Invert 1/(s+1)². From the table t e^{at} ↔ 1/(s−a)², so L⁻¹=t e^{−t} — the
hallmark t·e^{rt} of a repeated root. *Check:* `invert_quadratic(0, 1, 2, 1)`
(i.e. (0·s+1)/(s²+2s+1)) → t e^{−t}.

**Solution.** Here $s^2+2s+1=(s+1)^2$ has the **repeated** root $r=-1$ (discriminant $2^2-4=0$).
The table pair $\mathcal L\{t\,e^{at}\}=\dfrac{1}{(s-a)^2}$ with $a=-1$ inverts $\dfrac{1}{(s+1)^2}$ to
$$\mathcal L^{-1}\Big\{\tfrac{1}{(s+1)^2}\Big\}=t\,e^{-t}.$$
The factor of $t$ — absent for distinct roots — is the signature of critical damping. With
$b_1=0,b_0=1,p=2,q=1$ the code's repeated-root branch returns $(b_1+(b_1r+b_0)t)e^{rt}=t\,e^{-t}$,
so `invert_quadratic(0, 1, 2, 1)` evaluated at $t=2$ gives $2e^{-2}=0.270671$.
