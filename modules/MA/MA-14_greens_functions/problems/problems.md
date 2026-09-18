# MA-14 — Problems

Work by hand, then check with `code/greens_function.py`. Citations in `../refs.md`.

### P1.  Build the Green's function from two solutions  *(Boas 3e §12, p.461)*
For −u″=f on [0,1], u(0)=u(1)=0, take y₁=x and y₂=1−x. Splice them at x=ξ with
continuity and a unit jump in slope to get G=x_<(1−x_>). Verify G(0,ξ)=G(1,ξ)=0
and that ∂G/∂x jumps by −1 at x=ξ. *Check:* `green_dirichlet`; the kink test.

**Solution.** Write $G=A\,y_1(x)=Ax$ on $x<\xi$ (so $G(0,\xi)=0$) and $G=B\,y_2(x)=B(1-x)$
on $x>\xi$ (so $G(1,\xi)=0$). Continuity at $x=\xi$ gives $A\xi=B(1-\xi)$, and integrating
$-G''=\delta$ across $\xi$ fixes the slope jump $G_x(\xi^+)-G_x(\xi^-)=-1$, i.e. $-B-A=-1$.
Solving, $A=1-\xi,\ B=\xi$, so
$$G(x,\xi)=\begin{cases}(1-\xi)x,&x<\xi\\[2pt]\xi(1-x),&x>\xi\end{cases}=x_<\,(1-x_>).$$
Then $G(0,\xi)=G(1,\xi)=0$, and the slope drops from $1-\xi$ to $-\xi$ at $x=\xi$ — a jump of
$-1$ — matching `green_dirichlet` and the kink test.

### P2.  Solve a BVP and compare to the exact answer  *(Boas 3e §12, p.461)*
Use u(x)=∫₀¹ G(x,ξ)f(ξ)dξ with f=sin πx to get u=sin(πx)/π², and with f=1 to get
u=x(1−x)/2. *Check:* `solve_bvp_greens(lambda x: math.sin(math.pi*x), xs)`.

**Solution.** Since $L_xG=\delta$, the integral $u(x)=\int_0^1G(x,\xi)f(\xi)\,d\xi$ obeys
$-u''=f$ with $u(0)=u(1)=0$. For $f=\sin\pi x$, try $u=\sin(\pi x)/\pi^2$: then
$-u''=\pi^2\sin(\pi x)/\pi^2=\sin\pi x$ ✓ and $u(0)=u(1)=0$ ✓. For $f=1$, $u=x(1-x)/2$ gives
$-u''=1$ with the same boundary values. Numerically at $x=\tfrac14$,
$\sin(\pi/4)/\pi^2=0.071645$ — exactly the value
`solve_bvp_greens(lambda x: math.sin(math.pi*x), xs)` returns.

### P3.  Symmetry from self-adjointness  *(Boas 3e §12, p.461; ~MA-11)*
Argue that a self-adjoint L gives a symmetric Green's function G(x,ξ)=G(ξ,x), and
confirm it numerically (including the Helmholtz case). *Check:*
`green_dirichlet(0.2,0.7)` == `green_dirichlet(0.7,0.2)`.

**Solution.** Green's second identity for a self-adjoint $L$ reads
$\int(v\,Lu-u\,Lv)\,dx=$ boundary terms, which vanish under homogeneous BCs. Put
$u=G(x,\xi_1),\ v=G(x,\xi_2)$, so $Lu=\delta(x-\xi_1)$ and $Lv=\delta(x-\xi_2)$:
$$\int\!\big[G(x,\xi_2)\delta(x-\xi_1)-G(x,\xi_1)\delta(x-\xi_2)\big]dx=G(\xi_1,\xi_2)-G(\xi_2,\xi_1)=0.$$
Hence $G$ is symmetric. Concretely $G(0.2,0.7)=0.2\,(1-0.7)=0.06=G(0.7,0.2)$, so
`green_dirichlet(0.2,0.7)` == `green_dirichlet(0.7,0.2)` (the same holds for the Helmholtz $G$).

### P4.  The spectral (eigenfunction) expansion  *(Boas 3e Ch.13, p.657; ~MA-11)*
Show G=Σ φₙ(x)φₙ(ξ)/λₙ with φₙ=√2 sin(nπx), λₙ=(nπ)². Sum the series and watch it
converge to the closed-form tent. Which n dominate? (The small-λ, low-n modes.)
*Check:* `green_series(0.3, 0.7, 2000)` ≈ `green_dirichlet(0.3, 0.7)` = 0.09.

**Solution.** Expand $G(x,\xi)=\sum_n c_n(\xi)\varphi_n(x)$ in the eigenbasis
$L\varphi_n=\lambda_n\varphi_n$. Using completeness $\delta(x-\xi)=\sum_n\varphi_n(x)\varphi_n(\xi)$
and $LG=\delta$,
$$\sum_n c_n\lambda_n\varphi_n(x)=\sum_n\varphi_n(x)\varphi_n(\xi)\ \Rightarrow\ c_n=\frac{\varphi_n(\xi)}{\lambda_n},\qquad G=\sum_n\frac{\varphi_n(x)\varphi_n(\xi)}{\lambda_n}.$$
With $\varphi_n=\sqrt2\sin(n\pi x)$ and $\lambda_n=(n\pi)^2$, the $1/\lambda_n=1/(n\pi)^2$ weight makes
the small-$\lambda$, low-$n$ modes dominate. At $(0.3,0.7)$ the series → $0.090000$, matching
`green_series(0.3, 0.7, 2000)` ≈ `green_dirichlet(0.3, 0.7)` $=0.3(1-0.7)=0.09$.

### P5.  The Helmholtz Green's function  *(Boas 3e §12, p.461)*
Build G for −u″+k²u with y₁=sinh kx, y₂=sinh k(1−x) and Wronskian giving the
denominator k sinh k. Solve a BVP with it and match a direct finite-difference
solve. *Check:* `solve_bvp_greens(f, xd, k=3)` vs `solve_bvp_direct(f, 49, k=3)`.

**Solution.** Take $G=A\sinh(kx)$ on $x<\xi$ and $G=B\sinh\!\big(k(1-x)\big)$ on $x>\xi$; each
piece kills one boundary condition. Continuity gives $A\sinh k\xi=B\sinh k(1-\xi)$, and
integrating $-G''+k^2G=\delta$ across $\xi$ gives the unit jump $G_x(\xi^+)-G_x(\xi^-)=-1$.
Using $\sinh(k\xi)\cosh k(1-\xi)+\cosh(k\xi)\sinh k(1-\xi)=\sinh k$, one solves
$$G(x,\xi)=\frac{\sinh(kx_<)\,\sinh\!\big(k(1-x_>)\big)}{k\sinh k},$$
the Wronskian of $\sinh kx,\ \sinh k(1-x)$ supplying the $k\sinh k$. With $k=3$ the Green
integral matches the finite-difference solve to $\sim10^{-4}$, i.e.
`solve_bvp_greens(f, xd, k=3)` ≈ `solve_bvp_direct(f, 49, k=3)`.

### P6.  The causal propagator  *(Boas 3e §12, p.461; ~MA-10)*
For y″+ω²y=f, y(0)=y′(0)=0, show G(t,τ)=sin ω(t−τ)/ω for t≥τ (the inverse Laplace
transform of 1/(s²+ω²)). Solve a unit step f=1 to get y=(1−cos ωt)/ω² and check it
against RK4. *Check:* `solve_oscillator_greens(lambda t: 1.0, t, 2.0)` vs
`rk4_oscillator(...)`.

**Solution.** For $t<\tau$ causality forces $y=0$. Integrating $y''+\omega^2y=\delta(t-\tau)$
across $\tau$ imparts a unit velocity jump: $y(\tau^+)=0,\ y'(\tau^+)=1$. For $t>\tau$ the
homogeneous solution $y=C\cos\omega(t-\tau)+D\sin\omega(t-\tau)$ with these data has $C=0,\
D=1/\omega$, so $G(t,\tau)=\dfrac{\sin\omega(t-\tau)}{\omega}\,H(t-\tau)$ — the inverse Laplace
transform of $1/(s^2+\omega^2)$. For a unit step $f=1$,
$$y(t)=\int_0^t\frac{\sin\omega(t-\tau)}{\omega}\,d\tau=\frac{1-\cos\omega t}{\omega^2}.$$
At $\omega=2,\ t=1$ this is $(1-\cos2)/4=0.354037$, matching
`solve_oscillator_greens(lambda t: 1.0, t, 2.0)` and `rk4_oscillator(...)`.
