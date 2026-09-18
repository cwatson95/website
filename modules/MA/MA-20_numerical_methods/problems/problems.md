# MA-20 — Problems

Work by hand, then check with `code/numerical.py`. Citations in `../refs.md`.

### P1.  Order of accuracy by step halving  *(see notes §0)*
For ∫₀¹eˣdx, compute the trapezoid and Simpson errors at N and 2N and show the
error ratios are ≈4 and ≈16, i.e. orders 2 and 4. *Check:*
`quad_order(simpson, math.exp, 0, 1, math.e-1)` ≈ 4.

**Solution.** A method of order $p$ has error $E(h)\approx C\,h^{p}$, so halving the
step ($N\to 2N$, $h\to h/2$) shrinks the error by $E(h)/E(h/2)=2^{p}$ and
$p=\log_2\!\big(E(N)/E(2N)\big)$. Trapezoid is $p=2$, Simpson $p=4$:
$$\text{trap: }E(16)=5.59\times10^{-4},\ E(32)=1.40\times10^{-4},\ \tfrac{E(16)}{E(32)}=4.00,$$
$$\text{simp: }E(16)=1.46\times10^{-7},\ E(32)=9.10\times10^{-9},\ \tfrac{E(16)}{E(32)}=16.0.$$
So the ratios are $4=2^2$ and $16=2^4$, giving orders $2$ and $4$ — and
`quad_order(simpson, math.exp, 0, 1, math.e-1)` returns $\log_2 16=3.999\approx4$.

### P2.  Gauss is exact for high-degree polynomials  *(see refs)*
Show the 2-node Gauss rule integrates any cubic on [−1,1] exactly, and the 3-node
rule any quintic (degree ≤ 2n−1). *Check:* `gauss_legendre(lambda x: x**3, -1, 1, 2, 1)`
→ 0.

**Solution.** The 2-node rule has nodes $\pm1/\sqrt3$ and weights $1,1$; an $n$-node
Gauss rule is exact for degree $\le 2n-1$. Check the monomial basis up to $x^3$:
$$\int_{-1}^{1}1\,dx=2=1+1,\qquad \int_{-1}^{1}x^2\,dx=\tfrac23=\big(\tfrac1{\sqrt3}\big)^2+\big(\tfrac1{\sqrt3}\big)^2=\tfrac13+\tfrac13,$$
and the odd powers $\int_{-1}^{1}x\,dx=\int_{-1}^{1}x^3\,dx=0$ are reproduced because
the symmetric nodes/weights cancel: $(-\tfrac1{\sqrt3})^3+(\tfrac1{\sqrt3})^3=0$. By
linearity every cubic is integrated exactly. Likewise the 3-node rule ($2n-1=5$) is
exact through quintics. Hence `gauss_legendre(lambda x: x**3, -1, 1, 2, 1)` $\to 0$.

### P3.  Newton's quadratic convergence  *(Schaum's p.233)*
Apply Newton to x²−2=0 from x₀=1.5 and tabulate the error each step; confirm it
roughly squares (eₖ₊₁≈C eₖ²). *Check:* `newton(lambda x: x*x-2, lambda x: 2*x, 1.5)`.

**Solution.** For $f(x)=x^2-2$ the Newton step is
$x\leftarrow x-\dfrac{x^2-2}{2x}=\dfrac12\!\left(x+\dfrac2x\right)$. Writing
$e_k=x_k-\sqrt2$, a Taylor expansion gives the quadratic law
$e_{k+1}=\dfrac{f''(\xi)}{2f'(x_k)}e_k^2=\dfrac{e_k^2}{2x_k}\to\dfrac{e_k^2}{2\sqrt2}$,
so $C=1/(2\sqrt2)\approx0.354$. From $x_0=1.5$ the iterates' errors are
$$e_0=8.6\times10^{-2},\ e_1=2.5\times10^{-3},\ e_2=2.1\times10^{-6},\ e_3=1.6\times10^{-12},$$
each roughly the square of the previous ($0.354\times(8.6\times10^{-2})^2\approx2.6\times10^{-3}=e_1$).
This is the iterate history `newton(lambda x: x*x-2, lambda x: 2*x, 1.5)` returns,
reaching $\sqrt2$ in 4 steps — the digits double each iteration.

### P4.  Bisection vs Newton  *(Schaum's p.233)*
Solve cos x = x both ways. Bisection needs a bracket and converges linearly;
Newton needs f′ and converges quadratically. *Check:* `bisection`, `newton` on
f(x)=cos x − x.

**Solution.** Let $f(x)=\cos x-x$. Since $f(0)=1>0$ and $f(1)=\cos1-1=-0.46<0$, a
root is bracketed in $[0,1]$. **Bisection** halves the bracket each step, killing one
bit of error per iteration ($e_{k+1}=\tfrac12 e_k$, linear/order 1). **Newton** uses
$f'(x)=-\sin x-1$:
$$x\leftarrow x-\frac{\cos x-x}{-\sin x-1},$$
which squares the error each step. Both converge to the Dottie number
$$x^\*=0.7390851332,$$
but Newton reaches $10^{-13}$ in 4 steps while bisection needs ~40. So
`bisection(f,0,1)` and `newton(f, fp, 0.5)` agree at $0.7390851332$, the second far faster.

### P5.  RK4 vs Euler order  *(Schaum's p.236; Chicone §1.1 p.3)*
Integrate y′=y, y(0)=1 to y(1)=e. Measure the order of Euler (≈1) and RK4 (≈4) by
halving the step. Why is RK4 worth 4 function evaluations per step? *Check:*
`ode_order(rk4, lambda t,y: y, 1, 1, math.e)` ≈ 4.

**Solution.** For $y'=y,\ y(0)=1$ the exact solution is $y(1)=e$. **Euler**
$y\leftarrow y+hf$ has local truncation error $O(h^2)$, accumulating to a global error
$O(h)$ — order 1. **RK4** combines four slopes ($k_1$–$k_4$ in the $1\!:\!2\!:\!2\!:\!1$
weighting) to cancel the Taylor series through $h^4$, giving global error $O(h^4)$ —
order 4. Step-halving confirms the exponents:
$$p_{\text{Euler}}=\log_2\frac{E(n)}{E(2n)}\approx0.98,\qquad p_{\text{RK4}}\approx3.98.$$
RK4 is worth its 4 evaluations because halving $h$ cuts its error $16\times$ versus
$2\times$ for Euler, so far fewer total steps reach a tolerance. Hence
`ode_order(rk4, lambda t,y: y, 1, 1, math.e)` $\approx4$.

### P6.  Dominant eigenvalue by power iteration  *(see notes §4; ~MA-04)*
Iterate A=[[2,1,0],[1,2,1],[0,1,2]] on a starting vector and watch it align with
the top eigenvector; read λ_max=2+√2 from the Rayleigh quotient. *Check:*
`power_iteration(A)`.

**Solution.** Expand the start vector in eigenvectors, $x_0=\sum c_i v_i$. Then
$A^k x_0=\sum c_i\lambda_i^k v_i$, and after normalizing, the term with the largest
$|\lambda|$ dominates: $x_k\to v_{\max}$. The eigenvalue is read off by the Rayleigh
quotient $\lambda=\dfrac{x^{\mathsf T}Ax}{x^{\mathsf T}x}$. The matrix
$\begin{pmatrix}2&1&0\\1&2&1\\0&1&2\end{pmatrix}$ has eigenvalues $2+\sqrt2,\,2,\,2-\sqrt2$
(its characteristic polynomial is $(2-\lambda)\big[(2-\lambda)^2-2\big]$), so the
dominant one is
$$\lambda_{\max}=2+\sqrt2\approx3.41421356.$$
`power_iteration(A)` converges to $\lambda=3.41421356$, matching $2+\sqrt2$.
