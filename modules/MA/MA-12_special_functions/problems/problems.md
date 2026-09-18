# MA-12 — Problems

Work by hand, then check with `code/special_functions.py`. Citations in `../refs.md`.

### P1.  Legendre by recurrence and Rodrigues  *(Boas 3e §2 p.564; §4 p.568)*
From (n+1)P_{n+1}=(2n+1)xP_n−nP_{n−1} build P₂,P₃,P₄. Verify P₂=(3x²−1)/2 also
follows from Rodrigues' formula P₂=(1/8)d²/dx²(x²−1)². Confirm P_n(1)=1.
*Check:* `legendre(2, x)`, `legendre(4, 1.0)`.

**Solution.** Start from $P_0=1,\ P_1=x$ and the recurrence $(n{+}1)P_{n+1}=(2n{+}1)xP_n-nP_{n-1}$:
$$2P_2=3x\,P_1-P_0=3x^2-1\ \Rightarrow\ P_2=\tfrac{3x^2-1}{2},\qquad 3P_3=5x\,P_2-2P_1=\tfrac{15x^3-9x}{2}\ \Rightarrow\ P_3=\tfrac{5x^3-3x}{2},$$
$$4P_4=7x\,P_3-3P_2=\tfrac{35x^4-30x^2+3}{2}\ \Rightarrow\ P_4=\tfrac{35x^4-30x^2+3}{8}.$$
Rodrigues reproduces $P_2$: $(x^2-1)^2=x^4-2x^2+1$, so $\frac{d^2}{dx^2}(x^2-1)^2=12x^2-4$ and $\frac1{8}(12x^2-4)=\frac{3x^2-1}{2}$. At $x=1$ the generating function $1/\sqrt{1-2t+t^2}=1/(1-t)=\sum_n t^n$ forces $P_n(1)=1$; indeed `legendre(4, 1.0)` $=1$.

### P2.  The generating function = multipole expansion  *(Boas 3e §5, p.569)*
Show 1/√(1−2xt+t²)=ΣP_n(x)tⁿ and that expanding 1/|r−r′| in t=r'/r reproduces it
with x=cosθ — the monopole/dipole/quadrupole series of `~EM-05`. *Check:*
`legendre_generating(0.3, 0.5)` → series equals the closed form.

**Solution.** Let $g(x,t)=(1-2xt+t^2)^{-1/2}$. With $x=\cos\theta$ the law of cosines makes $\sqrt{1-2xt+t^2}=|\mathbf r-\mathbf r'|/r$ when $t=r'/r$, so
$$\frac1{|\mathbf r-\mathbf r'|}=\frac1r\,\frac1{\sqrt{1-2(r'/r)\cos\theta+(r'/r)^2}}=\frac1r\sum_{n=0}^\infty\Big(\frac{r'}{r}\Big)^{\!n}P_n(\cos\theta),$$
the monopole ($n{=}0$), dipole ($n{=}1$), quadrupole ($n{=}2$)… series of `~EM-05`. Expanding $g$ in powers of $t$ and collecting terms returns $P_0=1,\,P_1=x,\,P_2=\tfrac{3x^2-1}2,\dots$ Numerically at $x=0.3,\,t=0.5$ both sides equal $1.02597835$, so `legendre_generating(0.3, 0.5)` reports matching series and closed form.

### P3.  Orthogonality with the right weight  *(Boas 3e §7 p.577; §19 p.601)*
Verify ∫_{−1}^1 P_m P_n dx = 2/(2n+1)δ_mn, ∫H_mH_n e^{−x²}dx=2ⁿn!√π δ_mn, and
∫₀^∞ L_mL_n e^{−x}dx=δ_mn. Each weight is the one that makes the operator
self-adjoint (`~MA-11`). *Check:* `orthogonality_legendre`, `_hermite`, `_laguerre`.

**Solution.** Each family is the eigenfunction set of a Sturm–Liouville operator made self-adjoint by its weight $w$ ($1$, $e^{-x^2}$, $e^{-x}$), so eigenfunctions of different eigenvalue are $w$-orthogonal (`~MA-11`). The diagonal norms come from the generating functions; e.g. for Legendre $\int_{-1}^1 g^2\,dx=\sum_n t^{2n}\!\int_{-1}^1\! P_n^2\,dx$, while the left side integrates directly to $\frac1t\ln\frac{1+t}{1-t}=2\sum_n\frac{t^{2n}}{2n+1}$, giving
$$\int_{-1}^1 P_n^2\,dx=\frac{2}{2n+1}.$$
The demo confirms the diagonals $2,\tfrac23,0.4,\tfrac27$ for Legendre, $2^n n!\sqrt\pi$ for Hermite, and $1$ for Laguerre, with off-diagonals $\sim10^{-17}$ — exactly what `orthogonality_legendre/_hermite/_laguerre` return.

### P4.  Each function solves its ODE  *(Boas 3e §2 p.564; §12 p.587; §22 p.607)*
Plug P_n, H_n, L_n, J_n into their defining ODEs and confirm the residual is ~0.
*Check:* `ode_residual('legendre', 3, 0.4)`, `ode_residual('bessel', 2, 3.0)`, etc.

**Solution.** Each function is built to satisfy its defining ODE, so substituting it and forming the left-hand side must give zero:
$$(1{-}x^2)P_n''-2xP_n'+n(n{+}1)P_n=0,\qquad H_n''-2xH_n'+2nH_n=0,$$
$$xL_n''+(1{-}x)L_n'+nL_n=0,\qquad x^2J_n''+xJ_n'+(x^2{-}n^2)J_n=0.$$
`ode_residual` forms these with $y',y''$ from central differences, so the output is the finite-difference truncation error rather than an exact zero: `ode_residual('legendre', 3, 0.4)` $\approx-2.3\times10^{-8}$ and `ode_residual('bessel', 2, 3.0)` $\approx-1.9\times10^{-6}$ — both $\sim0$, confirming each function solves its equation.

### P5.  Bessel two ways  *(Boas 3e §12, p.587)*
Compute J₀(1), J₁(2.5) from the integral J_n(x)=(1/π)∫₀^π cos(nτ−x sinτ)dτ and
from the power series; confirm they agree and that J₀(0)=1, J₁(0)=0. *Check:*
`bessel_j(0, 1.0)` ≈ 0.7651976.

**Solution.** The power series is $J_n(x)=\sum_{k=0}^\infty\frac{(-1)^k}{k!\,(n{+}k)!}\big(\tfrac{x}{2}\big)^{2k+n}$. For $J_0(1)$ set $n=0,\,x=1$:
$$J_0(1)=\sum_{k=0}^\infty\frac{(-1)^k}{(k!)^2}\Big(\tfrac12\Big)^{2k}=1-\tfrac14+\tfrac1{64}-\tfrac1{2304}+\cdots=0.7651977,$$
identical to the integral $\frac1\pi\int_0^\pi\cos(\sin\tau)\,d\tau$. The leading power is $(x/2)^n$, so $J_0(0)=1$ (its $k{=}0$ term) while $J_1(0)=0$ (every term carries a factor of $x$). This matches `bessel_j(0, 1.0)` $\approx0.7651976$.

### P6.  Spherical harmonics building blocks  *(Boas 3e §10 p.583; Ch.13 p.651)*
Build P_l^m for l=1,2 and verify P_1^1=−√(1−x²), P_2^2=3(1−x²), and that P_l^0=P_l.
These times e^{imφ} are the Y_l^m of `~QM-10`. *Check:* `assoc_legendre(2, 2, x)`,
`assoc_legendre(2, 0, x) == legendre(2, x)`.

**Solution.** The associated functions start from $P_m^m=(-1)^m(2m{-}1)!!\,(1-x^2)^{m/2}$. For $m=1$, $(2m{-}1)!!=1!!=1$:
$$P_1^1=(-1)^1\cdot1\cdot(1-x^2)^{1/2}=-\sqrt{1-x^2}.$$
For $m=2$, $(2m{-}1)!!=3!!=3$, so $P_2^2=(-1)^2\cdot3\cdot(1-x^2)=3(1-x^2)$. When $m=0$ the prefactor is $1$ and the $l$-recurrence is the ordinary Legendre one, so $P_l^0=P_l$. At $x=0.4$, `assoc_legendre(2, 2, x)` $=2.52=3(1-0.16)$ and `assoc_legendre(2, 0, x)` $=-0.26=$ `legendre(2, x)`; multiplied by $e^{im\phi}$ these are the $Y_l^m$ of `~QM-10`.
