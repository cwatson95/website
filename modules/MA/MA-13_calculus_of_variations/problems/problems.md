# MA-13 — Problems

Work by hand, then check with `code/variational.py`. Citations in `../refs.md`.

### P1.  Derive the Euler–Lagrange equation  *(Boas 3e §2, p.474)*
Vary y→y+εη with η(x₁)=η(x₂)=0, set dJ/dε|₀=0, integrate the η′ term by parts, and
read off ∂L/∂y − d/dx(∂L/∂y′)=0. *Check:* `euler_lagrange_residual` is ~0 along an
extremal.

**Solution.** Put $y\to y+\varepsilon\eta$ with $\eta(x_1)=\eta(x_2)=0$ and expand $J(\varepsilon)=\int_{x_1}^{x_2}L(x,y+\varepsilon\eta,y'+\varepsilon\eta')\,dx$. Stationarity is
$$\frac{dJ}{d\varepsilon}\Big|_{0}=\int_{x_1}^{x_2}\!\Big(\frac{\partial L}{\partial y}\,\eta+\frac{\partial L}{\partial y'}\,\eta'\Big)dx=0.$$
Integrate the second term by parts: $\int L_{y'}\eta'\,dx=\big[L_{y'}\eta\big]_{x_1}^{x_2}-\int\frac{d}{dx}L_{y'}\,\eta\,dx$, and the boundary term vanishes since $\eta$ dies at the ends. Hence $\int\!\big(L_y-\frac{d}{dx}L_{y'}\big)\eta\,dx=0$ for every $\eta$, and the fundamental lemma gives $\frac{\partial L}{\partial y}-\frac{d}{dx}\frac{\partial L}{\partial y'}=0$. `euler_lagrange_residual` evaluates this left side and returns $\sim10^{-7}$ along the recovered extremal.

### P2.  Shortest path is a straight line  *(Boas 3e §3, p.478)*
For L=√(1+y′²) show ∂L/∂y=0 forces ∂L/∂y′=const ⇒ y′=const ⇒ a line. Confirm the
minimizer recovers y=x with J=√2. *Check:* `minimize_path(lambda x,y,p: (1+p*p)**0.5,
0,0,1,1)`; `functional(...)` → √2.

**Solution.** For $L=\sqrt{1+y'^2}$ we have $\partial L/\partial y=0$, so Euler–Lagrange collapses to $\frac{d}{dx}\frac{\partial L}{\partial y'}=0$, i.e.
$$\frac{\partial L}{\partial y'}=\frac{y'}{\sqrt{1+y'^2}}=\text{const}\ \Longrightarrow\ y'=\text{const},$$
a straight line. Through $(0,0)$ and $(1,1)$ that line is $y=x$, with $J=\int_0^1\sqrt{1+1}\,dx=\sqrt2\approx1.414214$. `minimize_path` starts from a path bent by $0.3$ and relaxes it back to $y=x$ ($\max|y-x|\approx5.6\times10^{-8}$), and `functional` returns $1.414214=\sqrt2$.

### P3.  The Beltrami first integral  *(Boas 3e §3–4, p.478)*
When L has no explicit x, show d/dx(L − y′L_{y′}) = 0 using the Euler–Lagrange
equation. Hence L − y′L_{y′}=const. *Check:* `beltrami(L, x, y, p)` along an
extremal is constant.

**Solution.** Differentiate $B=L-y'L_{y'}$ along the path:
$$\frac{dB}{dx}=L_x+L_y\,y'+L_{y'}y''-y''L_{y'}-y'\frac{d}{dx}L_{y'}=L_x+y'\Big(L_y-\frac{d}{dx}L_{y'}\Big).$$
On an extremal the bracket is zero by Euler–Lagrange, leaving $dB/dx=L_x$. So when $L$ carries no explicit $x$ ($L_x=0$),
$$L-y'\frac{\partial L}{\partial y'}=\text{const},$$
the first integral — the variational ancestor of energy conservation (`~CM-19`). `beltrami(L, x, y, p)` returns this $B$, which stays constant along each analytic extremal.

### P4.  Brachistochrone → cycloid  *(Boas 3e §4, p.482)*
Minimize T=∫√((1+y′²)/(2gy))dx. Apply Beltrami to get y(1+y′²)=const, and show
its solution is the cycloid x=a(θ−sinθ), y=a(1−cosθ). Verify the Beltrami constant
equals 1/√(2a). *Check:* `cycloid_brachistochrone(1.0, thetas)` with the exact
slope sin t/(1−cos t).

**Solution.** $T\propto\int\sqrt{(1+y'^2)/y}\,dx$ has no explicit $x$, so Beltrami applies. With $L=\sqrt{(1+y'^2)/y}$, $L_{y'}=y'/\sqrt{y(1+y'^2)}$, giving
$$L-y'L_{y'}=\frac{(1+y'^2)-y'^2}{\sqrt{y(1+y'^2)}}=\frac1{\sqrt{y(1+y'^2)}}=\text{const}\ \Longrightarrow\ y(1+y'^2)=2a.$$
The cycloid $x=a(\theta-\sin\theta),\ y=a(1-\cos\theta)$ has $y'=\frac{\sin\theta}{1-\cos\theta}$, so $1+y'^2=\frac{2}{1-\cos\theta}$ and $y(1+y'^2)=a(1-\cos\theta)\cdot\frac{2}{1-\cos\theta}=2a$ ✓. The Beltrami constant is $1/\sqrt{2a}$; at $a=1$, `cycloid_brachistochrone(1.0, thetas)` gives $B=0.70711=1/\sqrt2$.

### P5.  Catenary (minimal surface of revolution)  *(Boas 3e §3, p.478)*
Minimize ∫y√(1+y′²)dx. Beltrami gives y/√(1+y′²)=c, whose solution is
y=c cosh(x/c). Confirm B=c along it. *Check:* `catenary(1.3, xs)`;
`beltrami(lambda x,y,p: y*(1+p*p)**0.5, x, y, sinh(x/c))` ≈ 1.3.

**Solution.** $L=y\sqrt{1+y'^2}$ has no explicit $x$. With $L_{y'}=yy'/\sqrt{1+y'^2}$,
$$L-y'L_{y'}=\frac{y(1+y'^2)-yy'^2}{\sqrt{1+y'^2}}=\frac{y}{\sqrt{1+y'^2}}=c.$$
Squaring gives $y'=\sqrt{y^2-c^2}/c$; separating, $\int\frac{dy}{\sqrt{y^2-c^2}}=\int\frac{dx}{c}$ yields $\cosh^{-1}(y/c)=x/c$, i.e. $y=c\cosh(x/c)$. On it $y'=\sinh(x/c)$ and $1+y'^2=\cosh^2(x/c)$, so $B=y/\sqrt{1+y'^2}=c$. With $c=1.3$, `catenary(1.3, xs)` and `beltrami(...)` return $B\equiv1.3$.

### P6.  Several variables = Lagrange's equations  *(Boas 3e §5, p.485)*
For L=L(x,y₁,y₂,y₁′,y₂′) derive one Euler–Lagrange equation per yᵢ. Identify
x→t and L=T−V to obtain Newton's equations — the bridge to `~CM-17`. (Pen-and-paper;
no code check.)

**Solution.** With $L=L(x,y_1,y_2,y_1',y_2')$ vary each $y_i\to y_i+\varepsilon\eta_i$ independently ($\eta_i$ vanishing at the ends). Integrating each $\eta_i'$ term by parts as in P1,
$$\delta J=\int\sum_{i}\Big(L_{y_i}-\frac{d}{dx}L_{y_i'}\Big)\eta_i\,dx=0.$$
Because the $\eta_i$ are arbitrary and independent, every coefficient must vanish: $\frac{\partial L}{\partial y_i}-\frac{d}{dx}\frac{\partial L}{\partial y_i'}=0$, one equation per $y_i$. Setting $x\to t$ and $L=T-V$ with $T=\tfrac12\sum_i m_i\dot y_i^2$ gives $L_{\dot y_i}=m_i\dot y_i$ and $L_{y_i}=-\partial V/\partial y_i$, so $m_i\ddot y_i=-\partial V/\partial y_i=F_i$ — Newton's equations, the bridge to `~CM-17`.
