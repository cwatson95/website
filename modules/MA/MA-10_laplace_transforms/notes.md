# MA-10 — Laplace & Integral Transforms (notes)

Citation key (full details + PDF pages in `refs.md`): **B** = Boas 3e. Pages are
the *printed* book pages. Laplace transforms and the Dirac delta were moved into
the ODE chapter (Ch.8) in the 3rd edition — see Boas's own preface.

## 1. Definition and the operational idea
The (one-sided) **Laplace transform** of f(t), t ≥ 0, is
$$F(s)=\mathcal L\{f\}(s)=\int_0^\infty f(t)\,e^{-st}\,dt,$$
defined for Re s large enough that the integral converges [B §8 *The Laplace
Transform* p.437]. It trades a function of *t* for a function of *s*; the point is
that **calculus in t becomes algebra in s**. Code: `laplace_numeric` evaluates the
integral by Simpson quadrature (it needs Re s > 0); `F_const/F_exp/F_pow/F_cos/F_sin`
are the table entries it is checked against.

A short table (all from the integral) [B Table p.469]:
$$1\!\to\!\tfrac1s,\quad e^{at}\!\to\!\tfrac1{s-a},\quad t^n\!\to\!\tfrac{n!}{s^{n+1}},\quad
\cos\omega t\!\to\!\tfrac{s}{s^2+\omega^2},\quad \sin\omega t\!\to\!\tfrac{\omega}{s^2+\omega^2}.$$

## 2. The operational rules
Linearity is immediate. The two that do the work [B §8 p.437–439]:
- **First-shift (s-shift):** $\mathcal L\{e^{at}f(t)\}(s)=F(s-a)$. Multiplying by
  e^{at} just translates the transform — this is why damping α only shifts poles.
- **Derivative:** $\mathcal L\{f'\}(s)=sF(s)-f(0)$, and
  $\mathcal L\{f''\}(s)=s^2F(s)-sf(0)-f'(0)$. Each derivative becomes a factor of s
  **plus the initial data** — the initial conditions enter automatically.

The tests verify both rules numerically (e.g. L{ω cos ωt} = s·L{sin ωt} − 0).

## 3. Convolution
The **convolution** (f∗g)(t)=∫₀ᵗ f(τ)g(t−τ)dτ has the transform [B §10
*Convolution* p.445, definition p.446]:
$$\mathcal L\{f*g\}(s)=F(s)\,G(s).$$
A product in s-space is a convolution in t-space (the same duality as Fourier,
`~MA-09`). Worked check: e^{−t}∗e^{−2t}=e^{−t}−e^{−2t}, whose transform is
1/(s+1)·1/(s+2). Code: `convolve`; the test confirms both the time integral and
the product rule.

## 4. Solving an initial-value problem (the payoff)
For y″ + p y′ + q y = f(t) with y(0)=y₀, y′(0)=v₀, transform every term and use
the derivative rule [B §9 *Solution of Differential Equations by Laplace
Transforms* p.440]:
$$(s^2+ps+q)\,Y(s)=(s+p)\,y_0+v_0+F(s)\ \Rightarrow\ Y(s)=\frac{(s+p)y_0+v_0+F(s)}{s^2+ps+q}.$$
The ODE is now **algebra**, with the initial conditions already baked in. Invert
by partial fractions over the characteristic quadratic s²+ps+q; its discriminant
p²−4q selects the case (`invert_quadratic`):
- **p²>4q** distinct real roots → A e^{r₁t}+B e^{r₂t} (overdamped),
- **p²=4q** repeated root → (A+Bt)e^{rt} (critically damped),
- **p²<4q** complex pair α±iβ → e^{αt}(C cos βt+D sin βt) (underdamped).
Code: `solve_ivp_laplace` (constant forcing F₀ adds the steady state y_p=F₀/q);
the test cross-checks all four damping regimes and the step response against `rk4`.

## 5. Inversion in general — the Bromwich integral
Inverting "by table" works because the table is complete enough for rational
F(s). The general inverse is a contour integral,
$$f(t)=\frac1{2\pi i}\int_{c-i\infty}^{c+i\infty}F(s)\,e^{st}\,ds,$$
a vertical line to the right of all singularities, closed to the left and summed
by **residues** — i.e. Laplace inversion *is* complex analysis (`~MA-06`). This
module inverts by the table/partial-fraction route (Boas's method) and leaves the
Bromwich contour to MA-06.

## Where this goes
- `~CM-15`/`~EM-12`: the damped driven oscillator and RLC circuit are exactly the
  s²+ps+q problem of §4 — poles = natural frequencies, forcing = the source term.
- `~MA-14`: the causal Green's function H(t−τ)sin ω(t−τ)/ω of y″+ω²y=δ(t−τ) is
  the inverse transform of 1/(s²+ω²); convolving it with f reproduces §4.
- `~MA-09`: Fourier and Laplace are the same idea on different contours; the
  convolution theorem (§3) is shared.
