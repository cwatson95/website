# MA-11 — Problems

Work by hand, then check with `code/sturm_liouville.py`. Citations in `../refs.md`.

### P1.  Put an equation in Sturm–Liouville form  *(Boas 3e Ch.12 misc., p.617)*
Write Legendre's equation (1−x²)y″−2xy′+l(l+1)y=0 as −((1−x²)y′)′ = l(l+1)y, i.e.
p=1−x², q=0, w=1, λ=l(l+1). Do the same for Bessel's equation to read off its
p, q, w. (This is why Legendre/Bessel functions are automatically orthogonal.)

**Solution.** Expand the SL derivative with the product rule:
$\frac{d}{dx}\big[(1-x^2)y'\big]=(1-x^2)y''+\frac{d}{dx}(1-x^2)\,y'=(1-x^2)y''-2x\,y'$,
which is exactly the first two terms of Legendre's equation. Hence
$$-\frac{d}{dx}\big[(1-x^2)y'\big]=l(l+1)\,y\;\Rightarrow\; p=1-x^2,\ q=0,\ w=1,\ \lambda=l(l+1).$$
For Bessel's equation $x^2y''+xy'+(k^2x^2-\nu^2)y=0$, divide by $x$ and use $xy''+y'=(xy')'$:
$$(xy')'-\frac{\nu^2}{x}\,y+k^2x\,y=0\;\Rightarrow\;-\frac{d}{dx}(x\,y')+\frac{\nu^2}{x}y=k^2\,x\,y,$$
so $p=x,\ q=\nu^2/x,\ w=x,\ \lambda=k^2$. Both have $p>0$ and a positive weight, so by §2 their
eigenfunctions ($P_l$ with $w=1$, $J_\nu$ with $w=x$) are automatically $w$-orthogonal.

### P2.  The canonical spectrum  *(Boas 3e §6, p.575; §9, p.580)*
For −y″=λy on [0,π], y(0)=y(π)=0, derive λₙ=n² and yₙ=sin nx by hand. Confirm
numerically. *Check:* `sl_eigenpairs(1, 0, 1, 0, math.pi, 200, 5)` → λ ≈ 1,4,9,16,25.

**Solution.** With $p=w=1,\ q=0$ the equation is $y''+\lambda y=0$. For $\lambda>0$ the general
solution is $y=A\cos\sqrt\lambda\,x+B\sin\sqrt\lambda\,x$. The condition $y(0)=0$ kills the cosine
($A=0$); then $y(\pi)=B\sin\sqrt\lambda\,\pi=0$ forces
$$\sqrt\lambda\,\pi=n\pi\;\Rightarrow\;\lambda_n=n^2,\qquad y_n(x)=\sin(nx),\quad n=1,2,\dots$$
($\lambda\le0$ gives only $y\equiv0$.) The finite-difference solver returns
$\lambda\approx0.99998,\,3.9997,\,8.998,\,15.995,\,24.987$ — i.e. $1,4,9,16,25$ with a small
downward grid bias, so `sl_eigenpairs(1, 0, 1, 0, math.pi, 200, 5)` $\approx n^2$.

### P3.  Orthogonality with a weight  *(Boas 3e §7, p.577)*
Show directly that ∫₀^π sin(mx)sin(nx)dx = (π/2)δₘₙ. Then confirm the computed
eigenfunctions are orthogonal under `inner_w`. *Check:* `inner_w(ys[m], ys[n], w, h)`
≈ 0 for m≠n.

**Solution.** Use the product-to-sum identity
$\sin(mx)\sin(nx)=\tfrac12\big[\cos((m-n)x)-\cos((m+n)x)\big]$. For integers $m\ne n$,
$$\int_0^\pi\!\sin(mx)\sin(nx)\,dx=\frac12\!\left[\frac{\sin((m-n)x)}{m-n}-\frac{\sin((m+n)x)}{m+n}\right]_0^\pi=0,$$
since $\sin(k\pi)=0$. For $m=n$, $\int_0^\pi\sin^2(nx)\,dx=\int_0^\pi\tfrac12(1-\cos 2nx)\,dx=\pi/2$.
Hence $\int_0^\pi\sin(mx)\sin(nx)\,dx=\tfrac{\pi}{2}\delta_{mn}$. Numerically `inner_w(ys[0], ys[1], w, h)`
$\approx1.1\times10^{-16}\approx0$, while the diagonal `inner_w(ys[0], ys[0], w, h)` $=0.0156\ne0$
(nonzero because the code normalizes each eigenvector to unit length, not to $\sin$).

### P4.  Completeness and Parseval  *(Boas 3e §6, p.575; §9, p.580)*
Expand f(x)=x(π−x) in the eigenfunctions. Verify it reconstructs f and that
⟨f,f⟩_w = Σ cₙ²⟨yₙ,yₙ⟩_w (Parseval). *Check:* `expand(f, ys, w, h)`,
`reconstruct(c, ys)`; compare the two energies.

**Solution.** Write $f=\sum_n c_n y_n$ with $c_n=\langle f,y_n\rangle_w/\langle y_n,y_n\rangle_w$
(theorem 3); `reconstruct(c, ys)` returns $f$ to grid accuracy. Taking the weighted inner product
of $f$ with itself and using $w$-orthogonality collapses the double sum to its diagonal:
$$\langle f,f\rangle_w=\Big\langle\textstyle\sum_m c_m y_m,\sum_n c_n y_n\Big\rangle_w=\sum_n c_n^2\,\langle y_n,y_n\rangle_w\quad(\text{Parseval}).$$
Analytically $\langle f,f\rangle_w=\int_0^\pi x^2(\pi-x)^2\,dx=\pi^5/30\approx10.2007$. The code gives both
sides $=10.200653$ (only odd $n$ contribute, since $f$ is symmetric about $x=\pi/2$), confirming completeness.

### P5.  Rayleigh quotient bound  *(Boas 3e §6, p.575)*
Use the trial function y=x(π−x) (which satisfies the boundary conditions) to show
R[y]=10/π²≈1.0132 is an upper bound on λ_min=1. Try a worse guess and watch the
bound loosen. *Check:* `rayleigh_quotient(1, 0, 1, [x*(pi-x) for x in xs], 0, pi)`.

**Solution.** With $p=1,q=0,w=1$ and $y=x(\pi-x)$ (so $y'=\pi-2x$ and $y(0)=y(\pi)=0$),
$$\int_0^\pi (y')^2dx=\int_0^\pi(\pi-2x)^2dx=\frac{\pi^3}{3},\qquad \int_0^\pi y^2dx=\int_0^\pi x^2(\pi-x)^2dx=\frac{\pi^5}{30}.$$
Hence $R[y]=\dfrac{\pi^3/3}{\pi^5/30}=\dfrac{10}{\pi^2}\approx1.0132\ge\lambda_{\min}=1$ — a one-line guess
overshooting the true ground eigenvalue by only $1.3\%$. The code returns
`rayleigh_quotient(...)` $=1.013187$ (vs $10/\pi^2=1.013212$, the gap pure discretization); a trial
shaped less like $\sin x$ raises the numerator and loosens the bound.

### P6.  The Sturm sequence as a root counter  *(Boas 3e Ch.12 misc., p.617)*
For the 5×5 matrix with diagonal 2 and off-diagonal −1, evaluate `sturm_count` at
a few μ and confirm it is nondecreasing and jumps by one at each eigenvalue
2−2cos(kπ/6). This is Sturm's theorem doing the eigenvalue bookkeeping.
*Check:* `sturm_count([2]*5, [-1]*4, mu)` for μ = 0, 1, 2, 3, 4.

**Solution.** The $5\times5$ matrix $T=\mathrm{tridiag}(-1,2,-1)$ is the discrete Laplacian, with known
eigenvalues $\lambda_k=2-2\cos(k\pi/6)=\{0.268,\,1,\,2,\,3,\,3.732\}$ for $k=1,\dots,5$. `sturm_count`
returns the number of eigenvalues strictly below $\mu$, so sampling $\mu=0,1,2,3,4$ gives
$$0,\ 1,\ 2,\ 3,\ 5,$$
which is nondecreasing. The count rises by exactly one as $\mu$ crosses each $\lambda_k$; the apparent
jump of $2$ between $\mu=3$ and $\mu=4$ merely means two eigenvalues ($3$ and $3.732$) lie in $(3,4)$.
This sign-change count is Sturm's theorem, and bisecting on it is how `tridiag_eigenvalues` isolates each $\lambda_k$.
