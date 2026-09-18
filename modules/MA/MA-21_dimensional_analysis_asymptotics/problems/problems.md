# MA-21 — Problems

Work by hand, then check with `code/asymptotics.py`. Citations in `../refs.md`.

### P1.  Buckingham Pi for the pendulum  *(dimensional analysis — see refs)*
With {period T, length L, gravity g, mass m} over (M,L,T), write the dimension
matrix, find its rank, and conclude there is exactly one dimensionless group
Π=gT²/L ⇒ T∝√(L/g). Why does the mass drop out? *Check:* `buckingham_pi(D)`.

**Solution.** With columns $(T_{\text{period}},L,g,m)$ and rows $(M,L,T)$,
$$D=\begin{pmatrix}0&0&0&1\\0&1&1&0\\1&0&-2&0\end{pmatrix},\qquad \operatorname{rank}D=3,$$
so there are $n-\operatorname{rank}=4-3=1$ dimensionless groups (the null space of $D$).
Solving $D\mathbf p=\mathbf 0$ gives $\mathbf p=(2,-1,1,0)$, i.e.
$\Pi=T^2L^{-1}g^{1}m^{0}=gT^2/L$. The **mass** column $(0,0,0,1)$ is the *only* one with
an $M$-entry, so cancelling mass forces its exponent to $0$ — $m$ cannot appear. With a
single group the law is $\Pi=\text{const}$, hence $T\propto\sqrt{L/g}$. This is exactly
the vector `buckingham_pi(D)` returns, `[[2.0, -1.0, 1.0, -0.0]]`.

### P2.  The Reynolds number  *(dimensional analysis — see refs)*
For {ρ, U, L, μ} (density, speed, length, viscosity) over (M,L,T), show the single
Pi group is Re=ρUL/μ. *Check:* `buckingham_pi` on the dimension matrix; verify
`is_dimensionless`.

**Solution.** In $(M,L,T)$: $\rho=ML^{-3}$, $U=LT^{-1}$, $L=L$, $\mu=ML^{-1}T^{-1}$, so
$$D=\begin{pmatrix}1&0&0&1\\-3&1&1&-1\\0&-1&0&-1\end{pmatrix},\qquad \operatorname{rank}D=3\ \Rightarrow\ 4-3=1\text{ group}.$$
Solving $D\mathbf p=\mathbf0$ gives $\mathbf p\propto(1,1,1,-1)$, the exponents of
$\rho,U,L,\mu$ — i.e. $\Pi=\rho UL/\mu=\mathrm{Re}$. Check the three rows:
$M:1{-}1{=}0$, $L:-3{+}1{+}1{+}1{=}0$, $T:-1{+}1{=}0$. `buckingham_pi` returns the
reciprocal vector $(-1,-1,-1,1)=\mu/(\rho UL)=1/\mathrm{Re}$ — the same group — and
`is_dimensionless(D,[1,1,1,-1])` is `True`, confirming $\mathrm{Re}=\rho UL/\mu$.

### P3.  An asymptotic (divergent) series  *(Boas 3e §10, p.549)*
For g(x)=x eˣE₁(x)∼Σ(−1)ᵏk!/xᵏ, show the terms eventually grow, so the series
diverges, yet the partial sums approximate g(x) for large x. *Check:*
`exp_integral_scaled_asymptotic(x, N)` vs `exp_integral_scaled_true(x)`.

**Solution.** The terms are $a_k=(-1)^k k!/x^k$, so the ratio of successive magnitudes is
$$\left|\frac{a_{k+1}}{a_k}\right|=\frac{k+1}{x}.$$
For $k+1>x$ this exceeds $1$ and the terms **grow without bound**, so $\sum a_k$ diverges
for every fixed $x$. It is nonetheless asymptotic: truncating before the smallest term,
the error is bounded by the first omitted term $\sim k!/x^{k}$, which is small for large
$x$. At $x=10,\ N=2$: $1-\tfrac1{10}+\tfrac{2}{100}=0.92$ versus the true
$g(10)=0.91563$ — a $4\times10^{-3}$ error. So
`exp_integral_scaled_asymptotic(10, 2)` $=0.92$ tracks `exp_integral_scaled_true(10)`
even though the full series diverges.

### P4.  Optimal truncation  *(Boas 3e §10, p.549)*
Show the best truncation stops near the smallest term (N≈x) with residual error
~that term. Confirm adding more terms makes the answer worse. *Check:*
`optimal_truncation(8.0)` → best N≈8.

**Solution.** From P3 the term magnitude $|a_k|=k!/x^k$ falls while $(k+1)/x<1$, i.e.
$k\lesssim x-1$, then rises — so it is **smallest near $k\approx x$**, and the best
truncation stops there. The residual error is of order that smallest term, which by
Stirling is $\sim\sqrt{2\pi x}\,e^{-x}$ (at $x=8$, $\sqrt{16\pi}\,e^{-8}\approx2.4\times10^{-3}$).
`optimal_truncation(8.0)` returns best $N=7\approx x=8$ with minimal error
$1.2\times10^{-3}$; pushing $N$ past this makes the error *grow* — the defining signature
of an asymptotic (rather than convergent) series.

### P5.  Stirling's formula  *(Boas 3e §11, p.552)*
Derive ln n! ≈ n ln n − n + ½ln(2πn) (e.g. by the integral ∫ln x dx or the
saddle point of Γ). Check the 1/(12n) correction against exact ln n!. *Check:*
`ln_factorial_stirling(n, 3)` vs `math.lgamma(n+1)`.

**Solution.** Start from $\ln n!=\sum_{k=1}^{n}\ln k$ and compare the sum to the integral
$$\int_1^n\ln x\,dx=\big[x\ln x-x\big]_1^n=n\ln n-n+1.$$
The Euler–Maclaurin correction sharpens the constant to $\tfrac12\ln(2\pi n)$ and adds the
next term $\tfrac1{12n}$, giving
$$\ln n!\approx n\ln n-n+\tfrac12\ln(2\pi n)+\frac1{12n}.$$
At $n=5$ this is $4.78751$ versus the exact $\ln\Gamma(6)=4.78749$ (error $2.2\times10^{-5}$),
and the $1/(12n)$ term shrinks the error roughly $10\times$ over the two-term form. So
`ln_factorial_stirling(5, 3)` $=4.78751$ matches `math.lgamma(6)` to five digits.

### P6.  Regular perturbation  *(Boas 3e §10, p.549)*
Solve x²+εx−1=0 perturbatively about x=1: substitute x=1+a₁ε+a₂ε²+… and match
powers of ε to get a₁=−½, a₂=⅛. Compare to the exact root. *Check:*
`perturbed_root(eps, 2)` vs the quadratic formula.

**Solution.** Substitute $x=1+a_1\varepsilon+a_2\varepsilon^2+\cdots$ into $x^2+\varepsilon x-1=0$:
$$\big(1+a_1\varepsilon+a_2\varepsilon^2\big)^2+\varepsilon\big(1+a_1\varepsilon\big)-1
=2a_1\varepsilon+\big(a_1^2+2a_2\big)\varepsilon^2+\varepsilon+a_1\varepsilon^2+O(\varepsilon^3).$$
Match orders: $O(\varepsilon):\ 2a_1+1=0\Rightarrow a_1=-\tfrac12$;
$O(\varepsilon^2):\ a_1^2+2a_2+a_1=0\Rightarrow \tfrac14+2a_2-\tfrac12=0\Rightarrow a_2=\tfrac18$. Thus
$$x\approx 1-\tfrac{\varepsilon}{2}+\tfrac{\varepsilon^2}{8}.$$
At $\varepsilon=0.2$ this gives $0.905$, versus the exact root
$\big(-\varepsilon+\sqrt{\varepsilon^2+4}\big)/2=0.904988$ — so `perturbed_root(0.2, 2)`
$=0.905$ matches the quadratic formula to $O(\varepsilon^3)$.
