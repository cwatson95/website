# MA-08 — Problems

Work by hand, then check with `code/pde.py`. Citations in `../refs.md`.

### P1.  Heat equation by separation of variables  *(Boas 3e §13.3, p.628; Griffiths §3.3, p.130)*
On [0,L] with u(0)=u(L)=0 and u(x,0)=sin(πx/L), separate variables to get
u(x,t)=sin(πx/L)e^{−α(π/L)²t}. *Check:* `heat_1d` started from that initial
condition matches `heat_mode(L, alpha, 1)` at later t.

**Solution.** Seek $u(x,t)=X(x)T(t)$. Substituting into $u_t=\alpha u_{xx}$ and dividing by
$\alpha XT$ gives $\dfrac{T'}{\alpha T}=\dfrac{X''}{X}$. The two sides depend on different
variables, so each equals a constant $-k^2$. The spatial equation $X''=-k^2X$ with
$X(0)=X(L)=0$ forces $k=n\pi/L$, $X=\sin\frac{n\pi x}{L}$; the temporal equation
$T'=-\alpha k^2 T$ gives $T=e^{-\alpha k^2 t}$. The initial shape $\sin(\pi x/L)$ is already
the $n=1$ mode, so
$$u(x,t)=\sin\frac{\pi x}{L}\,e^{-\alpha(\pi/L)^2 t}.$$
This is exactly `heat_mode(L, alpha, 1)`; starting `heat_1d` from $\sin(\pi x/L)$ reproduces
it — at $u(0.5,0.1)$ the FTCS solver returns $0.37272$ vs $0.37271$ from the mode.

### P2.  Vibrating string (standing wave)  *(Boas 3e §13.4, p.633)*
For u_tt=c²u_xx with fixed ends and u(x,0)=sin(πx/L), u_t(x,0)=0, show
u=sin(πx/L)cos(cπt/L). *Check:* `wave_1d(u0, [0]*N, c, dx, dt, n)` vs
`wave_mode(L, c, 1)`.

**Solution.** Separation $u=X(x)T(t)$ in $u_{tt}=c^2u_{xx}$ gives
$\dfrac{T''}{c^2T}=\dfrac{X''}{X}=-k^2$. As in P1 the fixed ends force $X=\sin\frac{n\pi x}{L}$
with $k=n\pi/L$. The temporal equation $T''=-c^2k^2T$ now oscillates instead of decaying:
$T=A\cos(ckt)+B\sin(ckt)$. The zero initial velocity $u_t(x,0)=0$ kills the sine ($B=0$), and
$u(x,0)=\sin(\pi x/L)$ selects $n=1$ with $A=1$:
$$u(x,t)=\sin\frac{\pi x}{L}\cos\frac{c\pi t}{L}.$$
This is `wave_mode(L, c, 1)`. At $t=0.2$ (with $c=L=1$), $\cos(0.2\pi)=0.80902$, matching
`wave_1d`, which returns $0.80902$.

### P3.  Laplace on a square  *(Boas 3e §13.2, p.621; Griffiths §3.1, p.113)*
Solve ∇²u=0 with a harmonic boundary u=x²−y² and show the interior reproduces
x²−y² exactly (the 5-point stencil is exact for quadratics). *Check:*
`laplace_2d` interior equals x²−y².

**Solution.** First, $u=x^2-y^2$ is harmonic: $\nabla^2u=u_{xx}+u_{yy}=2-2=0$. The
Gauss–Seidel update sets each interior node to the four-neighbour average; for $u=x^2-y^2$ at
spacing $h$,
$$u(x{+}h,y)+u(x{-}h,y)=2x^2+2h^2-2y^2,\qquad u(x,y{+}h)+u(x,y{-}h)=2x^2-2y^2-2h^2,$$
so $\tfrac14\big[\,\cdot\,+\,\cdot\,+\,\cdot\,+\,\cdot\,\big]=\tfrac14(4x^2-4y^2)=x^2-y^2=u(x,y)$,
the $+2h^2$ and $-2h^2$ cancelling. Thus $x^2-y^2$ is an *exact* fixed point of the 5-point
stencil, so relaxation reproduces it to machine precision: `laplace_2d` returns
$u(0.5,0.5)=-0.000000$ against the exact $0$.

### P4.  Fourier's trick for the coefficients  *(Griffiths §3.3, p.136; → `~MA-09`)*
For an initial condition that is a sum of sine modes, the coefficients bₙ are
extracted by multiplying by sin(mπx/L) and integrating (orthogonality). Predict
the decay of each mode and confirm a two-mode initial condition splits into two
exponentials. *Check:* `heat_1d` from `sin(πx)+0.5 sin(3πx)`; compare modes.

**Solution.** Write the initial data as $f(x)=\sum_n b_n\sin\frac{n\pi x}{L}$. Multiply by
$\sin\frac{m\pi x}{L}$ and integrate, using orthogonality
$\int_0^L\sin\frac{n\pi x}{L}\sin\frac{m\pi x}{L}\,dx=\tfrac{L}{2}\delta_{nm}$:
$$b_m=\frac{2}{L}\int_0^L f(x)\sin\frac{m\pi x}{L}\,dx.$$
Each mode then carries its own decay $e^{-\alpha(n\pi/L)^2t}$, so the rate scales as $n^2$. For
$f=\sin(\pi x)+\tfrac12\sin(3\pi x)$ on $[0,1]$ ($\alpha=1$),
$$u(x,t)=\sin(\pi x)\,e^{-\pi^2 t}+\tfrac12\sin(3\pi x)\,e^{-9\pi^2 t}.$$
The $n=3$ mode decays $9\times$ faster: by $t=0.05$ its amplitude is only $0.96\%$ of the
fundamental. `heat_1d` from `sin(πx)+0.5 sin(3πx)` matches this two-exponential split to
$3\times10^{-4}$.

### P5.  Stability of the explicit scheme  *(numerical)*
Show that FTCS for the heat equation is unstable once r = α dt/dx² > ½ by running
`heat_1d` with a too-large dt and watching it blow up; then halve dt and see it
behave. *(A hands-on look at the CFL/stability condition in `notes.md` §3.)*

**Solution.** Von Neumann analysis: insert a Fourier mode $u_j^n=\xi^n e^{ikj\Delta x}$ into the
FTCS update $u_j^{n+1}=u_j^n+r\,(u_{j+1}-2u_j+u_{j-1})$, $r=\alpha\,\Delta t/\Delta x^2$. The
amplification factor is
$$\xi=1+r\big(e^{ik\Delta x}-2+e^{-ik\Delta x}\big)=1-4r\sin^2\!\frac{k\Delta x}{2}.$$
Stability needs $|\xi|\le1$ for every $k$; the worst case $\sin^2=1$ gives $1-4r\ge-1$, i.e.
$r\le\tfrac12$. With $\Delta x=0.05,\ \alpha=1$: $r=0.6$ ($dt=0.0015$) blows up to
$\max|u|\approx7.6\times10^{10}$ after 200 steps, whereas halving to $r=0.3$ leaves a smooth
decaying $\max|u|\approx0.227$ — exactly the CFL threshold of `notes.md` §3.
